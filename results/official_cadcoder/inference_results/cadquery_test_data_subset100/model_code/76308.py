import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.109375, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.05526315789473685, 0.0).lineTo(0.05526315789473685, 0.05526315789473685).lineTo(0.05526315789473685, 0.09473684210526316).lineTo(0.05526315789473685, 0.14210526315789473).lineTo(0.05526315789473685, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.14210526315789473).lineTo(0.0, 0.09473684210526316).lineTo(0.0, 0.05526315789473685).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0546875, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.05526315789473685, 0.0).lineTo(0.05526315789473685, 0.05526315789473685).lineTo(0.05526315789473685, 0.09473684210526316).lineTo(0.05526315789473685, 0.14210526315789473).lineTo(0.05526315789473685, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.14210526315789473).lineTo(0.0, 0.09473684210526316).lineTo(0.0, 0.05526315789473685).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.375)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/76308.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/76308.step")
