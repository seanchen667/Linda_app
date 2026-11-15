# Equipment and Prerequisites

## Existing resources to check

A household Bambu Lab P1S printer, calipers, and prior ESP32 experience may be available. Verify availability and condition before purchase. Give Linda a separate controller and project records where practical; do not assume equipment from another active project is free to use.

## First-stage equipment

| Item | Purpose | Selection notes |
| --- | --- | --- |
| Laptop or desktop computer | CAD, firmware, data analysis | A phone is not an adequate primary development workstation |
| 3D printer | Guides, sensor brackets, interchangeable geometry | Printed parts require validation; do not assume printed structures are suitable for critical loads |
| Rigid base, brackets, clamps | Secure the rig | Stability must be checked throughout the intended motion |
| Pivot shaft, bearings, fasteners, leg member | Single-joint mechanism | Select dimensions after drawing the geometry |
| Small secured test masses | Repeatable loading | Prevent falling, swinging, or accidental release |
| One ESP32 or Arduino board | Sensor reading and control | Choose one platform initially |
| Angle sensor or encoder | Joint motion measurement | Range, resolution, mounting, and voltage compatibility matter |
| Force sensor with compatible interface | Cable tension measurement | Use a sensor rated for the intended loading direction; calibrate the complete installation |
| Geared motor and compatible driver | Controlled assistance | Buy only after load and speed estimates |
| Current-limited low-voltage DC supply | Bench power | Match supply, driver, motor, wiring, and current limits |
| Multimeter | Electrical checks | Learn safe measurement methods before use |
| Stop switch, fuse, travel switches, mechanical stops, guards | Protective functions | Design before powered operation; software stop alone is insufficient |
| Cable, pulleys, elastic elements | Transmission experiments | Select after routing and loading are defined |
| Ruler, calipers, hand tools, labels | Assembly and documentation | Use consistent units and identify each revision |

Power removal can allow a mechanism to coast or fall. Design the rig so its behavior after a stop, cable failure, or loss of power remains controlled by appropriate mechanical constraints.

Do not drive a motor from a controller GPIO pin. Motor selection must consider startup and stall current, not only nominal running current. Confirm logic voltage compatibility, particularly with 3.3 V controllers.

## Defer these purchases

- Human-sized exoskeleton kits, lifting actuators, and wearable support harnesses.
- High-power motors and large battery packs.
- EMG sensors, cameras, machine-learning accelerators, and mobile-app hardware.
- Expensive measurement systems before the required accuracy is understood.

Use external bench power initially. Do not choose a motor, driver, or sensor range before calculating the small model's requirements.

## Workspace

- A stable table with sufficient clearance around every moving part.
- A way to clamp or bolt the rig down.
- Guards and a clear exclusion area for pinch points and moving masses.
- Organized electrical wiring and accessible power isolation.
- Adult supervision for initial powered experiments and unfamiliar tools.
- Appropriate facilities and guidance for drilling or soldering, if required.

## Skills to learn progressively

| Area | Initial capability |
| --- | --- |
| CAD | Dimensioned sketches, parts, assemblies, and revisions; Onshape is a suggested option |
| Mechanics | Torque, levers, friction, springs, center of mass, and free-body diagrams |
| Electronics | Voltage, current, polarity, grounding, sensor interfaces, and motor drivers |
| Programming | Read sensors, apply limits, control motion, and log timestamps |
| Experiments | Calibration, repeatability, uncertainty, controls, and failure analysis |
| Communication | Explain why a change was made and what the evidence shows |

Competition programming and machine learning are not prerequisites. Linda must nevertheless learn to understand and modify the control code.

## Time and support

A proposed starting commitment is about 4–6 hours per week, adjusted around school and rest. An adult should support unfamiliar tools and electrical setup. Mechanical/control engineering mentorship becomes increasingly important as complexity or stored energy grows. Clinical expertise is required for any later patient-facing work.

No precise budget or shopping model has been approved. Purchase in stages after inspecting existing tools and completing the initial drawings.
