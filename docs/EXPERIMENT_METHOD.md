# Experimental Method and Record Template

## Iteration rules

1. State the failure or limitation before proposing a modification.
2. Predict which metric should change and why.
3. Preserve a baseline.
4. Initially vary one main factor where practical. Later use designed combinations if interactions matter.
5. Repeat trials under recorded conditions.
6. Record negative results and new disadvantages.
7. Evaluate promising designs under additional loads or speeds not used for tuning.

Bench performance is engineering evidence, not evidence that a device treats gait freezing or prevents falls.

## Candidate metrics

| Metric | Important qualification |
| --- | --- |
| Joint angle and motion time | Calibrate angle and synchronize timestamps |
| Cable tension and peak tension | State sensor range, calibration, sampling rate, and filtering |
| Tracking error | Define the desired trajectory and error calculation |
| Inactive resistance | Define whether the motor is powered, disabled, or mechanically disengaged |
| Electrical energy per cycle | Requires adequate voltage/current measurements; do not infer from motor rating |
| Module mass | State what is included and excluded |
| Repeated-cycle performance | Report drift, wear, failures, and maintenance |
| Assembly time and part count | Use a consistent definition |

Comparisons must account for geometry: cable force alone is not joint torque. Do not scale small-model findings directly to human assistance.

## Experiment record

### Identification
- Experiment ID:
- Date:
- Researcher:
- CAD revision:
- Firmware commit:
- Raw-data location:
- Contributors and external sources:

### Question and prediction
- Observed problem:
- Proposed explanation:
- Modification:
- Expected change:
- Possible disadvantage:

### Setup
- Diagram and dimensions:
- Simulated-leg mass and center of mass:
- Added loads:
- Transmission geometry:
- Motion range and speed:
- Power and control settings:
- Sensor installation and calibration:
- Sampling rate, units, and synchronization:
- Trial count and order:
- Safety limits and abort conditions:

### Results
- Link all raw data, including unsuccessful runs.
- Summarize repeated trials and variation.
- Record slipping, slack, jams, sensor saturation, and other failures.
- Separate measurements from interpretations.
- Explain excluded trials and keep their original records.

### Decision
- Was the prediction supported?
- What uncertainty remains?
- Did another metric become worse?
- Keep, revise, or reject the modification?
- Next experiment:

## Documentation practice

Keep original data unchanged and put cleaned/derived data in separate files. Use one unit convention and explicit column headers. Record contributions honestly, including AI assistance. Do not upload identifiable participant or family medical information.

For a potential Maker Portfolio, save build-process photos, failed mechanisms, drawings, version comparisons, and concise explanations of Linda's decisions. No prototype has yet been built or tested.
