import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.039473684210526314, 0.0).lineTo(0.039473684210526314, 0.003947368421052632).lineTo(0.07894736842105263, 0.003947368421052632).lineTo(0.07894736842105263, 0.0).lineTo(0.1171875, 0.0).lineTo(0.1171875, 0.019736842105263157).lineTo(0.07894736842105263, 0.019736842105263157).lineTo(0.07894736842105263, 0.039473684210526314).lineTo(0.039473684210526314, 0.039473684210526314).lineTo(0.039473684210526314, 0.019736842105263157).lineTo(0.0, 0.019736842105263157).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/158433.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/158433.step")
