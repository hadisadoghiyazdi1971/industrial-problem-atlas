#!/usr/bin/env python3
"""IPA-004 method demo using synthetic cylinder-liner diameter measurements.

SYNTHETIC — NOT COMPANY DATA. The script calibrates Shewhart and EWMA
thresholds separately to the same alert-episode budget on clean simulations.
It demonstrates methodology only and makes no claim about a factory process.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
from pathlib import Path

SEED = 4004
CALIBRATION_SEED = 400400
VALIDATION_SEED = 400401
N = 400
TRAIN_N = 160
DRIFT_START = 225
SAMPLE_EVERY_PARTS = 5
NOMINAL_MM = 100.000
PROCESS_SIGMA_MM = 0.012
MEASUREMENT_SIGMA_MM = 0.004
DRIFT_PER_SAMPLE_MM = 0.00040
EWMA_LAMBDA = 0.20
TARGET_ALERT_EPISODES_PER_1000 = 5.0
CALIBRATION_RUNS = 600
VALIDATION_RUNS = 400
OUTPUT = Path(__file__).resolve().parent / "output" / "ipa004_synthetic_diameter"
LABEL = "SYNTHETIC — NOT COMPANY DATA"


def mean_std(values):
    mean = sum(values) / len(values)
    std = math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))
    return mean, std


def synthetic_series(rng, with_drift):
    rows = []
    for sample in range(N):
        drift = (sample - DRIFT_START + 1) * DRIFT_PER_SAMPLE_MM if with_drift and sample >= DRIFT_START else 0.0
        true_diameter = NOMINAL_MM + drift + rng.gauss(0, PROCESS_SIGMA_MM)
        measured = true_diameter + rng.gauss(0, MEASUREMENT_SIGMA_MM)
        rows.append({
            "sample": sample,
            "produced_part_index": sample * SAMPLE_EVERY_PARTS,
            "true_diameter_synthetic_mm": true_diameter,
            "measured_diameter_synthetic_mm": measured,
            "drift_synthetic_mm": drift,
        })
    return rows


def standardized(rows):
    training = [r["measured_diameter_synthetic_mm"] for r in rows[:TRAIN_N]]
    mean, std = mean_std(training)
    return [(r["measured_diameter_synthetic_mm"] - mean) / std for r in rows], mean, std


def detector_scores(z_values):
    shewhart = [abs(z) for z in z_values]
    ewma = []
    state = 0.0
    for index, z in enumerate(z_values):
        state = EWMA_LAMBDA * z + (1 - EWMA_LAMBDA) * state
        scale = math.sqrt(
            EWMA_LAMBDA / (2 - EWMA_LAMBDA)
            * (1 - (1 - EWMA_LAMBDA) ** (2 * (index + 1)))
        )
        ewma.append(abs(state) / scale)
    return {"shewhart": shewhart, "ewma": ewma}


def alert_episodes(scores, threshold, start=TRAIN_N, stop=N):
    flags = [False] * len(scores)
    episodes = 0
    previous = False
    for index in range(start, stop):
        current = scores[index] > threshold
        flags[index] = current
        if current and not previous:
            episodes += 1
        previous = current
    return episodes, flags


def clean_score_runs(seed, count):
    rng = random.Random(seed)
    result = {"shewhart": [], "ewma": []}
    for _ in range(count):
        rows = synthetic_series(rng, with_drift=False)
        z_values, _, _ = standardized(rows)
        scores = detector_scores(z_values)
        for name in result:
            result[name].append(scores[name])
    return result


def episode_rate(score_runs, threshold):
    episodes = sum(alert_episodes(scores, threshold)[0] for scores in score_runs)
    observations = len(score_runs) * (N - TRAIN_N)
    return episodes * 1000 / observations


def calibrate_threshold(score_runs):
    low = 0.0
    high = max(max(scores[TRAIN_N:]) for scores in score_runs) + 1.0
    for _ in range(42):
        middle = (low + high) / 2
        if episode_rate(score_runs, middle) > TARGET_ALERT_EPISODES_PER_1000:
            low = middle
        else:
            high = middle
    return high, episode_rate(score_runs, high)


def first_detection(flags):
    hits = [index for index in range(DRIFT_START, N) if flags[index]]
    return None if not hits else hits[0] - DRIFT_START


def build_svg(rows, mean, std, thresholds, flags):
    width, height = 1040, 390
    left, right, top, bottom = 70, 24, 28, 72
    chart_w, chart_h = width - left - right, height - top - bottom
    values = [(r["measured_diameter_synthetic_mm"] - mean) * 1000 for r in rows]
    limits = [thresholds["shewhart"] * std * 1000, -thresholds["shewhart"] * std * 1000]
    y_min = min(values + limits) - 8
    y_max = max(values + limits) + 8
    x = lambda index: left + index * chart_w / (N - 1)
    y = lambda value: top + (y_max - value) * chart_h / (y_max - y_min)
    path = " ".join(("M" if i == 0 else "L") + f"{x(i):.2f},{y(v):.2f}" for i, v in enumerate(values))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{LABEL}; simulated diameter drift and calibrated alerts">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        f'<rect x="{x(DRIFT_START):.1f}" y="{top}" width="{x(N-1)-x(DRIFT_START):.1f}" height="{chart_h}" fill="#fff1d8"/>',
        f'<line x1="{left}" y1="{y(0):.1f}" x2="{width-right}" y2="{y(0):.1f}" stroke="#7b8790"/>',
    ]
    for limit in limits:
        parts.append(f'<line x1="{left}" y1="{y(limit):.1f}" x2="{width-right}" y2="{y(limit):.1f}" stroke="#b05c28" stroke-dasharray="6 5"/>')
    parts.append(f'<path d="{path}" fill="none" stroke="#4a648a" stroke-width="1.7"/>')
    for name, color, offset in [("shewhart", "#a0392d", -4), ("ewma", "#087b73", 4)]:
        for index in range(TRAIN_N, N):
            if flags[name][index] and (index == TRAIN_N or not flags[name][index - 1]):
                parts.append(f'<circle cx="{x(index)+offset:.1f}" cy="{y(values[index]):.1f}" r="4" fill="{color}"/>')
    parts += [
        f'<text x="{left}" y="20" font-family="Arial" font-size="16" font-weight="bold" fill="#173344">{LABEL}</text>',
        f'<text x="{left}" y="{height-42}" font-family="Arial" font-size="14" fill="#173344">Measured deviation from training mean (micrometres); orange = simulated gradual drift</text>',
        f'<text x="{left}" y="{height-20}" font-family="Arial" font-size="13" fill="#52626b">Both detectors calibrated to {TARGET_ALERT_EPISODES_PER_1000:.1f} null alert episodes per 1000 monitored samples; circles mark alert starts.</text>',
        '</svg>',
    ]
    return "\n".join(parts)


def run():
    calibration = clean_score_runs(CALIBRATION_SEED, CALIBRATION_RUNS)
    thresholds = {}
    calibration_rates = {}
    for name, score_runs in calibration.items():
        thresholds[name], calibration_rates[name] = calibrate_threshold(score_runs)

    validation = clean_score_runs(VALIDATION_SEED, VALIDATION_RUNS)
    validation_rates = {name: episode_rate(validation[name], thresholds[name]) for name in thresholds}

    rows = synthetic_series(random.Random(SEED), with_drift=True)
    z_values, training_mean, training_std = standardized(rows)
    scores = detector_scores(z_values)
    flags = {}
    scenario = {}
    for name in thresholds:
        _, flags[name] = alert_episodes(scores[name], thresholds[name])
        pre_drift_episodes, _ = alert_episodes(scores[name], thresholds[name], TRAIN_N, DRIFT_START)
        scenario[name] = {
            "threshold_standardized_score": round(thresholds[name], 6),
            "calibration_alert_episodes_per_1000": round(calibration_rates[name], 6),
            "independent_null_alert_episodes_per_1000": round(validation_rates[name], 6),
            "clean_test_alert_episodes_before_drift": pre_drift_episodes,
            "first_detection_delay_samples_after_drift": first_detection(flags[name]),
            "first_detection_delay_produced_parts": None if first_detection(flags[name]) is None else first_detection(flags[name]) * SAMPLE_EVERY_PARTS,
        }

    result = {
        "label": LABEL,
        "purpose": "Method demonstration only; no industrial performance or benefit claim.",
        "seed": SEED,
        "unit": "mm",
        "nominal_diameter_synthetic_mm": NOMINAL_MM,
        "process_sigma_synthetic_mm": PROCESS_SIGMA_MM,
        "measurement_sigma_synthetic_mm": MEASUREMENT_SIGMA_MM,
        "sampling": {"one_measurement_every_produced_parts": SAMPLE_EVERY_PARTS, "observations": N},
        "split": {"training_samples": [0, TRAIN_N - 1], "test_samples": [TRAIN_N, N - 1]},
        "simulated_drift": {"starts_at_sample": DRIFT_START, "increment_mm_per_sample": DRIFT_PER_SAMPLE_MM},
        "false_alarm_budget": {
            "definition": "start of an alert episode per 1000 clean monitored samples",
            "target": TARGET_ALERT_EPISODES_PER_1000,
            "calibration_runs": CALIBRATION_RUNS,
            "independent_validation_runs": VALIDATION_RUNS,
            "note": "Thresholds are calibrated separately on clean synthetic sequences. Equal target budget does not imply identical realised alerts in one finite sequence.",
        },
        "training_estimates_synthetic": {"mean_mm": round(training_mean, 8), "std_mm": round(training_std, 8)},
        "detectors": scenario,
        "limitations": [
            "Synthetic Gaussian assumptions are chosen for illustration and are not evidence about company data.",
            "The gradual drift is imposed by the script and is not an observed tool-wear event.",
            "Detection delay in produced parts assumes the stated regular sampling interval.",
            "A real study must validate measurement, subgrouping, event labels and the current company method first.",
        ],
    }
    return rows, scores, flags, thresholds, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Run deterministic calibration and assertions without writing files.")
    args = parser.parse_args()
    rows, scores, flags, thresholds, result = run()
    assert result["label"] == LABEL
    assert all(abs(v["calibration_alert_episodes_per_1000"] - TARGET_ALERT_EPISODES_PER_1000) <= 0.05 for v in result["detectors"].values())
    assert all(3.0 <= v["independent_null_alert_episodes_per_1000"] <= 7.0 for v in result["detectors"].values())
    assert all(v["first_detection_delay_samples_after_drift"] is None or v["first_detection_delay_samples_after_drift"] >= 0 for v in result["detectors"].values())
    if args.check:
        print(f"PASS: {LABEL}; comparable false-alarm budget calibrated and independently checked.")
        print(json.dumps(result["detectors"], ensure_ascii=False, sort_keys=True))
        return
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUTPUT / "synthetic_diameter.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["label", "sample", "produced_part_index", "split", "true_diameter_synthetic_mm", "measured_diameter_synthetic_mm", "drift_synthetic_mm", "shewhart_score", "ewma_score", "shewhart_alert", "ewma_alert"])
        for index, row in enumerate(rows):
            writer.writerow([LABEL, index, row["produced_part_index"], "train" if index < TRAIN_N else "test", f'{row["true_diameter_synthetic_mm"]:.8f}', f'{row["measured_diameter_synthetic_mm"]:.8f}', f'{row["drift_synthetic_mm"]:.8f}', f'{scores["shewhart"][index]:.8f}', f'{scores["ewma"][index]:.8f}', int(flags["shewhart"][index]), int(flags["ewma"][index])])
    (OUTPUT / "synthetic_diameter.svg").write_text(build_svg(rows, result["training_estimates_synthetic"]["mean_mm"], result["training_estimates_synthetic"]["std_mm"], thresholds, flags), encoding="utf-8")
    print(LABEL)
    print(json.dumps(result["detectors"], ensure_ascii=False, indent=2))
    print("Saved:", OUTPUT)


if __name__ == "__main__":
    main()
