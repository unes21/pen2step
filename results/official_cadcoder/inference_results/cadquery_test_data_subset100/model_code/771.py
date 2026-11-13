import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.375, -0.1875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.09473684210526316, 0.0).lineTo(0.09473684210526316, 0.18947368421052632).lineTo(0.37894736842105264, 0.18947368421052632).lineTo(0.37894736842105264, 0.0).lineTo(0.4736842105263158, 0.0).lineTo(0.4736842105263158, 0.37894736842105264).lineTo(0.37894736842105264, 0.37894736842105264).lineTo(0.37894736842105264, 0.5605263157894737).lineTo(0.09473684210526316, 0.5605263157894737).lineTo(0.09473684210526316, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/771.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/771.step")
