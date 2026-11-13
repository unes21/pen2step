import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.4296875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.8526315789473684).lineTo(0.0, 0.8526315789473684).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.0, 0.0).threePointArc((0.23947368421052634, -0.15789473684210525), (0.39473684210526316, 0.0)).lineTo(0.39473684210526316, 0.8526315789473684).threePointArc((0.23947368421052634, 0.9904358552631579), (0.0868421052631579, 0.8526315789473684)).lineTo(0.0868421052631579, 0.0).close()
loop2=wp_sketch0.moveTo(0.0868421052631579, 0.0).threePointArc((0.4263157894736842, -0.2368421052631579), (0.7631578947368421, 0.0)).lineTo(0.7631578947368421, 0.8526315789473684).threePointArc((0.5289473684210526, 0.9904358552631579), (0.29210526315789476, 0.8526315789473684)).lineTo(0.29210526315789476, 0.0).close()
loop3=wp_sketch0.moveTo(0.29210526315789476, 0.0).threePointArc((0.75, -0.2368421052631579), (1.2078947368421053, 0.0)).lineTo(1.2078947368421053, 0.8526315789473684).threePointArc((1.063157894736842, 0.9904358552631579), (0.9, 0.8526315789473684)).lineTo(0.9, 0.0).close()
loop4=wp_sketch0.moveTo(1.5, 0.0).circle(0.04736842105263158)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.4296875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch1.moveTo(1.5, 0.0).lineTo(1.5, 0.8526315789473684).lineTo(0.0, 0.8526315789473684).lineTo(0.0, 0.0).close()
loop6=wp_sketch1.moveTo(0.0, 0.0).threePointArc((0.23947368421052634, -0.15789473684210525), (0.39473684210526316, 0.0)).lineTo(0.39473684210526316, 0.8526315789473684).threePointArc((0.23947368421052634, 0.9904358552631579), (0.0868421052631579, 0.8526315789473684)).lineTo(0.0868421052631579, 0.0).close()
loop7=wp_sketch1.moveTo(0.0868421052631579, 0.0).threePointArc((0.4263157894736842, -0.2368421052631579), (0.7631578947368421, 0.0)).lineTo(0.7631578947368421, 0.8526315789473684).threePointArc((0.5289473684210526, 0.9904358552631579), (0.29210526315789476, 0.8526315789473684)).lineTo(0.29210526315789476, 0.0).close()
loop8=wp_sketch1.moveTo(0.29210526315789476, 0.0).threePointArc((0.75, -0.2368421052631579), (1.2078947368421053, 0.0)).lineTo(1.2078947368421053, 0.8526315789473684).threePointArc((1.063157894736842, 0.9904358552631579), (0.9, 0.8526315789473684)).lineTo(0.9, 0.0).close()
loop9=wp_sketch1.moveTo(1.5, 0.0).circle(0.04736842105263158)
solid1=wp_sketch1.add(loop5).add(loop6).add(loop7).add(loop8).add(loop9).extrude(0.0078125)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_16.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_16.step")
