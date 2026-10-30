# Research brief — Keyhan Sanat Ghaem, Mashhad

**Reviewed:** 2026-10-30  
**Evidence level:** Public company statements + public NIST methods. No private manufacturing data.  
**Purpose:** Low-risk, specific exploratory invitation — not a defect allegation or performance claim.

## What the company's website actually states

- The company dates its foundation to 1373 and says it makes cylinder liners for light and heavy vehicle engines. Source: https://www.ksgco.com/
- The casting unit describes centrifugal, shell and sand casting and induction furnaces; it **claims** over 20,000 tons/year (website figure; not independently verified as current). Source: https://www.ksgco.com/units/casting/
- Its machining unit mentions CNC, lean production, a diversity of cylinder liners and a claimed capacity over 180,000 pieces/month. These are **company statements without verified date for current capacity**. Source: https://www.ksgco.com/units/machining/
- The specialized quality-control laboratory states it uses air gauges for inner/outer diameter, roughness gauges, hardness tests, metallography and instruments with 0.001-mm resolution; **resolution is not the same as measurement uncertainty or confirmed process precision**. Source: https://www.ksgco.com/units/specialized-quality-control-laboratory/
- The company lists R&D and QC units. Source: https://www.ksgco.com/units/rd/
- Its company email is info@ksgco.com and its factory phone 051-38470009. Source: https://www.ksgco.com/contactus/

## What we DO NOT know

Scrap/rework rates; existing SPC systems; actual machine data exportability; production-line bottlenecks; access to company data; interest in a collaboration; present staffing or priorities. **Do not infer these facts from photos or company descriptions.**

## Proposed scientific question

For one product family and one dimensional measurement (e.g., inner diameter), can statistical process monitoring detect confirmed non-random drift earlier than the current workflow, under an agreed false-alarm budget? A negative outcome is valuable.

## Approach

1. Verify measurement system and calibration/GRR where applicable.
2. Specify engineering tolerance limits separately from statistical control limits.
3. Define rational subgrouping and baseline Shewhart/EWMA/CUSUM; calibrate on historical data only.
4. Test on later chronological data (not random-shuffled record splitting).
5. Compare at equal review/false-alarm budget; only then consider ML if there is evidence of improvement.
6. Run human-supervised shadow evaluation; do not automate machine control.

## Feasibility gate

If timestamped data, approved process labels or quality staff time are absent, stop after assessment. No AI purchase or sensor installation should be proposed before data/decision feasibility is shown.

## Send protocol

Publish the website case page first: `companies/keyhan-sanat-ghaem/`. Check the deployed URL in a browser; only then send the letter by email to official `info@ksgco.com`, addressed to the director/technical/QC/R&D unit without guessing a contact person's identity. No unsolicited large attachments, no mass mailing. Make only one polite follow-up after 7–10 working days. Do not imply company endorsement on the public page.

## References

- https://www.ksgco.com/units/machining/
- https://www.ksgco.com/units/casting/
- https://www.ksgco.com/units/specialized-quality-control-laboratory/
- https://www.ksgco.com/units/rd/
- https://www.ksgco.com/contactus/
- https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc12.htm
- https://www.nist.gov/publications/nistsematech-engineering-statistics-handbook-chapter-2-measurement-process
