import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.5, 0.0, -0.75), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.9947368421052631, 0.0).lineTo(0.9947368421052631, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.25263157894736843, 0.25263157894736843).circle(0.04736842105263158)
loop2=wp_sketch0.moveTo(0.25263157894736843, 1.2473684210526317).circle(0.04736842105263158)
loop3=wp_sketch0.moveTo(0.7578947368421053, 0.25263157894736843).circle(0.04736842105263158)
loop4=wp_sketch0.moveTo(0.7578947368421053, 1.2473684210526317).circle(0.04736842105263158)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.1640625)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/143268.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/143268.step")
