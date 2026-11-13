import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.7578947368421053, 0.0).circle(0.7578947368421053)
loop1=wp_sketch0.moveTo(0.7578947368421053, 0.0).circle(0.6473684210526316)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.6484375, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch1.moveTo(0.6592105263157895, 0.0).circle(0.6592105263157895)
loop3=wp_sketch1.moveTo(0.22631578947368422, 0.0).circle(0.19226973684210524)
loop4=wp_sketch1.moveTo(0.6592105263157895, 0.0).circle(0.22631578947368422)
loop5=wp_sketch1.moveTo(0.6592105263157895, -0.42335526315789473).circle(0.19226973684210524)
loop6=wp_sketch1.moveTo(0.6592105263157895, 0.42335526315789473).circle(0.19226973684210524)
loop7=wp_sketch1.moveTo(1.082236842105263, 0.0).circle(0.19226973684210524)
solid1=wp_sketch1.add(loop2).add(loop3).add(loop4).add(loop5).add(loop6).add(loop7).extrude(0.1875)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/61429.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/61429.step")
