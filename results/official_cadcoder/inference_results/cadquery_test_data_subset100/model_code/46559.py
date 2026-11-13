import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.6015625, -0.1484375, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.1950657894736842, 0.0).threePointArc((1.3444490131578948, 0.14938322368421053), (1.1950657894736842, 0.29876644736842106)).lineTo(0.0, 0.29876644736842106).threePointArc((-0.14938322368421053, 0.14938322368421053), (0.0, 0.0)).close()
loop1=wp_sketch0.moveTo(0.0, 0.1564967105263158).circle(0.07113486842105264)
loop2=wp_sketch0.moveTo(1.1950657894736842, 0.1564967105263158).circle(0.07113486842105264)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).extrude(0.1484375)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/46559.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/46559.step")
