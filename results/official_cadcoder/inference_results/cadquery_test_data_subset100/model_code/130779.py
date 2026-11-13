import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.29210526315789476, 0.0).circle(0.29210526315789476)
loop1=wp_sketch0.moveTo(0.29210526315789476, 0.0).circle(0.15822368421052632)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.25)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.4609375, -0.2890625, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch1.moveTo(0.9245065789473684, 0.012664473684210526).threePointArc((1.199726646943896, 0.2912828947368421), (0.9245065789473684, 0.5699013157894737)).lineTo(0.0, 0.5699013157894737).threePointArc((0.2814750695419037, 0.28495065789473684), (0.0, 0.0)).close()
loop3=wp_sketch1.moveTo(0.9245065789473684, 0.2912828947368421).circle(0.16463815789473685)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.25)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch2.moveTo(0.29210526315789476, 0.0).circle(0.29210526315789476)
loop5=wp_sketch2.moveTo(0.29210526315789476, 0.0).circle(0.15822368421052632)
solid2=wp_sketch2.add(loop4).add(loop5).extrude(0.4921875)
solid=solid.union(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/130779.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/130779.step")
