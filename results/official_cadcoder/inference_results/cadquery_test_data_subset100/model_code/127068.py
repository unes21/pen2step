import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.0, 0.0).threePointArc((0.013873889312216349, -0.03349453174041546), (0.04736842105263158, -0.04736842105263158)).lineTo(1.4526315789473685, -0.04736842105263158).threePointArc((1.4861261106877837, -0.03349453174041546), (1.5, 0.0)).lineTo(1.5, 1.5).threePointArc((1.4861261106877837, 1.5334945317404153), (1.4526315789473685, 1.5421052631578947)).lineTo(0.04736842105263158, 1.5421052631578947).threePointArc((0.013873889312216349, 1.5334945317404153), (0.0, 1.5)).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.25263157894736843, 0.25263157894736843).circle(0.031578947368421054)
loop2=wp_sketch0.moveTo(0.25263157894736843, 1.2473684210526317).circle(0.031578947368421054)
loop3=wp_sketch0.moveTo(1.2473684210526317, 0.25263157894736843).circle(0.031578947368421054)
loop4=wp_sketch0.moveTo(1.2473684210526317, 1.2473684210526317).circle(0.031578947368421054)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.078125)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/127068.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/127068.step")
