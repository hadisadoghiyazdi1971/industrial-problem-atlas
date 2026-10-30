#!/usr/bin/env python3
"""Educational synthetic sensor analysis. NOT evidence of industrial performance.

No third-party dependencies. Generates 500 simulated observations, fits detector
thresholds ONLY on clean training steps 0..199 and evaluates on steps 200..499.
"""
import argparse
import csv
import json
import math
import random
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / 'output'
SEED = 2026
TRAIN_N = 200
N = 500
EVENTS = [(260, 285), (390, 420)]  # [start, end) synthetic events


def quantile(values, q):
    data = sorted(values)
    position = (len(data) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    return data[lo] * (hi-position) + data[hi] * (position-lo) if lo != hi else data[lo]


def synthetic_series():
    rng = random.Random(SEED)
    out = []
    for t in range(N):
        normal = 10 + 0.27 * math.sin(t / 11) + rng.gauss(0, 0.23)
        if any(start <= t < end for start, end in EVENTS):
            normal += 1.3 if t < 285 else 0.95
        out.append(round(normal, 6))
    return out


def ewma(values, alpha=0.24):
    result = []
    last = values[0]
    for x in values:
        last = alpha*x + (1-alpha)*last
        result.append(last)
    return result


def event_metrics(flags):
    test_steps = range(TRAIN_N, N)
    true_positive_steps = sum(1 for t in test_steps if flags[t] and any(a <= t < b for a, b in EVENTS))
    false_alarm_steps = sum(1 for t in test_steps if flags[t] and not any(a <= t < b for a, b in EVENTS))
    normal_steps = sum(1 for t in test_steps if not any(a <= t < b for a, b in EVENTS))
    event_delays = []
    for start, end in EVENTS:
        hits = [t for t in range(start, end) if flags[t]]
        event_delays.append(hits[0]-start if hits else None)
    return {
        'true_positive_steps': true_positive_steps,
        'false_alarm_steps': false_alarm_steps,
        'normal_test_steps': normal_steps,
        'false_alarm_rate_per_normal_step': round(false_alarm_steps/normal_steps, 6),
        'event_detection_delays_steps': event_delays,
        'events_detected': sum(delay is not None for delay in event_delays),
        'total_events': len(EVENTS)
    }


def build_svg(values, threshold, smoothed, smooth_limit, flags_a, flags_b):
    width, height = 1000, 360
    left, right, top, bottom = 54, 18, 20, 57
    chart_w, chart_h = width-left-right, height-top-bottom
    y_min = min(values+[threshold, smooth_limit])-0.3
    y_max = max(values+[threshold, smooth_limit])+0.3
    x=lambda t: left+t*chart_w/(N-1)
    y=lambda v: top+(y_max-v)*chart_h/(y_max-y_min)
    path=lambda series: ' '.join(('M' if i==0 else 'L')+f'{x(i):.2f},{y(v):.2f}' for i,v in enumerate(series))
    # Static visualization; every series is labeled as synthetic and in the output metadata.
    blocks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Synthetic sensor signal; baseline threshold and EWMA">',
              '<rect width="100%" height="100%" fill="#ffffff"/>']
    for start,end in EVENTS:
        blocks.append(f'<rect x="{x(start):.1f}" y="{top}" width="{x(end)-x(start):.1f}" height="{chart_h}" fill="#fcebd6"/>')
    blocks.append(f'<line x1="{left}" y1="{top+chart_h}" x2="{width-right}" y2="{top+chart_h}" stroke="#738394"/>')
    blocks.append(f'<line x1="{left}" y1="{y(threshold):.1f}" x2="{width-right}" y2="{y(threshold):.1f}" stroke="#a25d20" stroke-dasharray="5 5"/>')
    blocks.append(f'<line x1="{left}" y1="{y(smooth_limit):.1f}" x2="{width-right}" y2="{y(smooth_limit):.1f}" stroke="#008b87" stroke-dasharray="6 5"/>')
    blocks.append(f'<path d="{path(values)}" fill="none" stroke="#6576a2" stroke-width="1.6"/>')
    blocks.append(f'<path d="{path(smoothed)}" fill="none" stroke="#008b87" stroke-width="2"/>')
    blocks.append(f'<line x1="{x(TRAIN_N):.1f}" y1="{top}" x2="{x(TRAIN_N):.1f}" y2="{top+chart_h}" stroke="#b32733" stroke-width="2" stroke-dasharray="3 4"/>')
    for t in range(TRAIN_N,N):
        if flags_a[t] and t % 3 == 0:
            blocks.append(f'<circle cx="{x(t):.1f}" cy="{y(values[t]):.1f}" r="2.5" fill="#b64b29"/>')
        if flags_b[t] and t % 3 == 0:
            blocks.append(f'<circle cx="{x(t):.1f}" cy="{y(smoothed[t]):.1f}" r="2.3" fill="#137968"/>')
    blocks.append(f'<text x="{left}" y="{height-26}" font-size="15" font-family="Arial" fill="#263847">SYNTHETIC DATA ONLY — shaded areas = simulated events; red dashed = train/test split (t={TRAIN_N})</text>')
    blocks.append('</svg>')
    return '\n'.join(blocks)


def main():
    parser=argparse.ArgumentParser(description='Synthetic educational experiment, not industrial performance evidence.')
    parser.add_argument('--check', action='store_true', help='Validate demo without writing output files')
    args=parser.parse_args()
    values=synthetic_series()
    train=values[:TRAIN_N]
    mu=sum(train)/TRAIN_N
    std=math.sqrt(sum((v-mu)**2 for v in train)/(TRAIN_N-1))
    # Both detectors train/calibrate ONLY on steps 0..199.
    threshold=mu+3*std
    flag_base=[v>threshold for v in values]
    smooth=ewma(values)
    smooth_threshold=quantile(smooth[:TRAIN_N], .995)
    flag_smooth=[v>smooth_threshold for v in smooth]
    metrics={'source': 'SYNTHETIC_DATA_ONLY', 'seed': SEED,
             'train_index_range': [0, TRAIN_N-1], 'test_index_range':[TRAIN_N,N-1],
             'event_windows_test_only': EVENTS,
             'detectors': {
                 'raw_3sigma': {'threshold':round(threshold,6), **event_metrics(flag_base)},
                 'ewma_calibrated': {'threshold':round(smooth_threshold,6), **event_metrics(flag_smooth)}
             },
             'disclaimer': 'Simulation and method demonstration only; no real-factory claims.'}
    assert all(a>=TRAIN_N for a,b in EVENTS)
    assert len(values)==N and len(smooth)==N
    for result in metrics['detectors'].values():
        assert result['events_detected'] <= len(EVENTS)
        assert 0 <= result['false_alarm_rate_per_normal_step'] <= 1
    if args.check:
        print('PASS: synthetic demo self-check; no outputs written.')
        return
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT/'summary.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
    with (OUTPUT/'sensor_data.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['time_step','value_synthetic','ewma','event_synthetic','split','alarm_raw','alarm_ewma'])
        for i in range(N):
            writer.writerow([i,values[i],round(smooth[i],6),
                             int(any(a<=i<b for a,b in EVENTS)),
                             'train' if i<TRAIN_N else 'test', int(flag_base[i]),int(flag_smooth[i])])
    (OUTPUT/'synthetic_signal.svg').write_text(
        build_svg(values,threshold,smooth,smooth_threshold,flag_base,flag_smooth),encoding='utf-8')
    print('SYNTHETIC DATA ONLY — no industrial results are claimed.')
    print('Raw 3-sigma:',metrics['detectors']['raw_3sigma'])
    print('EWMA:',metrics['detectors']['ewma_calibrated'])
    print('Saved:',OUTPUT)


if __name__ == '__main__':
    main()
