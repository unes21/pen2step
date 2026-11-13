import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(0.0, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.16578947368421054).lineTo(0.6157894736842106, 0.16578947368421054).lineTo(0.6157894736842106, 0.0868421052631579).lineTo(0.5131578947368421, 0.0868421052631579).lineTo(0.5131578947368421, 0.25263157894736843).lineTo(0.3473684210526316, 0.25263157894736843).lineTo(0.3473684210526316, 0.0868421052631579).lineTo(0.25263157894736843, 0.0868421052631579).lineTo(0.25263157894736843, 0.16578947368421054).lineTo(0.0, 0.16578947368421054).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.0859375)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/39849.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/39849.step")
