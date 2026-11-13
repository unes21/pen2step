import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.296875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.6).lineTo(0.0, 0.6).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.04736842105263158, 0.04736842105263158).circle(0.015789473684210527)
loop2=wp_sketch0.moveTo(0.04736842105263158, 0.5526315789473685).circle(0.015789473684210527)
loop3=wp_sketch0.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.5526315789473685).lineTo(0.7105263157894737, 0.5526315789473685).lineTo(0.7105263157894737, 0.04736842105263158).close()
loop4=wp_sketch0.moveTo(1.4526315789473685, 0.04736842105263158).circle(0.015789473684210527)
loop5=wp_sketch0.moveTo(1.4526315789473685, 0.5526315789473685).circle(0.015789473684210527)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).add(loop5).extrude(0.0234375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.7109375, -0.2578125, 0.0234375), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch1.moveTo(1.421875, 0.0).lineTo(1.421875, 0.5180921052631579).lineTo(0.0, 0.5180921052631579).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop6).extrude(-0.0078125)
solid=solid.cut(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.6796875, -0.2578125, 0.0234375), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch2.moveTo(1.3515625, 0.0).lineTo(1.3515625, 0.49300986842105265).lineTo(0.0, 0.49300986842105265).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop7).extrude(-0.0078125)
solid=solid.cut(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/19463.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/19463.step")
