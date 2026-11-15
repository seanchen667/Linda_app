# Project Plan

## Selected starting point

Build an instrumented, single-joint simulated-leg rig and evaluate a lightweight hip-assistance transmission. This is a student engineering investigation, not a complete exoskeleton or clinical product.

Start with one pivot representing hip flexion and a rigid pendulum-like leg. Adding a knee, a second leg, a mobile base, or a wearable harness is outside the initial scope.

## Functional blocks

| Block | Function |
| --- | --- |
| Rigid base and pivot | Provide repeatable geometry and secure mounting |
| Simulated leg and secured masses | Provide a known, adjustable mechanical load |
| Motor and transmission | Apply controlled assistance |
| Force sensor | Measure transmission tension |
| Angle sensor | Measure joint angle and motion |
| Controller and data logging | Coordinate motion and record synchronized measurements |
| Independent protective features | Limit travel and energy, isolate moving parts, and remove drive power |

A cable-driven design is one starting hypothesis, not a final selection. Compare alternatives when the data justify them.

## Design questions

- How do routing, attachment geometry, and friction affect useful assistance?
- Can an elastic element reduce force peaks without making tracking unacceptable?
- How much resistance remains when the device is not assisting?
- What are the effects of slack, repeated cycling, and changes in test load?
- Which design gives a useful tradeoff between mass, complexity, repeatability, and performance?

## Requirements to determine before motor purchase

Record actual values and their rationale. Do not substitute human body dimensions or loads without analysis.

| Requirement | Initial status |
| --- | --- |
| Leg length, mass, center of mass, and pivot geometry | TBD |
| Allowed angle range and physical stop positions | TBD |
| Target motion speed and acceleration | TBD |
| Required joint torque and transmission tension | Calculate from selected geometry and loads |
| Maximum permitted electrical/mechanical energy | Set with adult engineering guidance |
| Force sensor range and expected measurement resolution | Select after load estimates |
| Motor voltage, torque-speed behavior, and current | Select as a compatible system |
| Emergency-stop and post-stop behavior | Document before powered testing |
| Test-rig footprint, mounting, and guarding | Verify before powered testing |

For an elementary static estimate, gravitational torque depends on mass, gravity, center-of-mass distance, and angle. Dynamic loads, transmission losses, and acceleration require additional consideration. Static estimates alone are insufficient for final component selection.

## Milestones

1. Manual rig: secure, repeatable motion and documented geometry.
2. Instrumentation: calibrated angle and force measurements with raw data.
3. Powered baseline: controlled, limited-range bench movement.
4. Comparative experiments: isolate a design question and compare versions.
5. Improved prototype: demonstrate tradeoffs across several loads and speeds.
6. Durability and fault characterization: preplanned tests within safe limits.

## Longer-term boundaries

A hip-flexion module does not provide balance, prevent knee collapse, support full body weight, or enable independent toileting. Fully non-weight-bearing users are a different target population from ambulatory people with gait initiation difficulty.

Any later move toward human-use research requires relevant engineering and rehabilitation collaborators, a new risk assessment, and applicable approvals. Successful bench tests are not authorization for human testing.
