import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.6484375, -0.375, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.6552631578947369, -0.3685855263157895).lineTo(1.296875, 0.0).lineTo(1.296875, 0.7508223684210527).lineTo(0.6552631578947369, 1.1194078947368422).lineTo(0.0, 0.7508223684210527).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.3203125)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/9639.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/9639.step")
