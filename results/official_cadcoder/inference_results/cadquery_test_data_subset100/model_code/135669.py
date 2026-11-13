import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.6484375, -0.375, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.6552631578947369, -0.3685855263157895).lineTo(1.296875, 0.0).lineTo(1.296875, 0.7508223684210527).lineTo(0.6552631578947369, 1.1194078947368422).lineTo(0.0, 0.7508223684210527).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.6552631578947369, 0.3685855263157895).circle(0.5870065789473684)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.2890625)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.5859375, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch1.moveTo(0.5921052631578947, 0.0).circle(0.5921052631578947)
solid1=wp_sketch1.add(loop2).extrude(0.2890625)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/135669.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/135669.step")
