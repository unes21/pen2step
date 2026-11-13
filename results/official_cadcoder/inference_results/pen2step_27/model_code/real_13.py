import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.49736842105263157).lineTo(0.0, 0.49736842105263157).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.039473684210526314, 0.039473684210526314).circle(0.015789473684210527)
loop2=wp_sketch0.moveTo(0.039473684210526314, 0.4578947368421053).circle(0.015789473684210527)
loop3=wp_sketch0.moveTo(0.7105263157894737, 0.039473684210526314).circle(0.015789473684210527)
loop4=wp_sketch0.moveTo(0.7105263157894737, 0.4578947368421053).circle(0.015789473684210527)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch1.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop6=wp_sketch1.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid1=wp_sketch1.add(loop5).add(loop6).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch2.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop8=wp_sketch2.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid2=wp_sketch2.add(loop7).add(loop8).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch3.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop10=wp_sketch3.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid3=wp_sketch3.add(loop9).add(loop10).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop11=wp_sketch4.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop12=wp_sketch4.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid4=wp_sketch4.add(loop11).add(loop12).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop13=wp_sketch5.moveTo(0.75, 0.0).lineTo(0.75, 0.49736842105263157).lineTo(0.0, 0.49736842105263157).lineTo(0.0, 0.0).close()
loop14=wp_sketch5.moveTo(0.039473684210526314, 0.039473684210526314).circle(0.015789473684210527)
loop15=wp_sketch5.moveTo(0.039473684210526314, 0.4578947368421053).circle(0.015789473684210527)
loop16=wp_sketch5.moveTo(0.7105263157894737, 0.039473684210526314).circle(0.015789473684210527)
loop17=wp_sketch5.moveTo(0.7105263157894737, 0.4578947368421053).circle(0.015789473684210527)
solid5=wp_sketch5.add(loop13).add(loop14).add(loop15).add(loop16).add(loop17).extrude(0.0078125)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop18=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop19=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid6=wp_sketch6.add(loop18).add(loop19).extrude(0.0078125)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop20=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop21=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid7=wp_sketch7.add(loop20).add(loop21).extrude(0.0078125)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop22=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop23=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.015789473684210527)
solid8=wp_sketch8.add(loop22).add(loop23).extrude(0.0078125)
solid=solid.union(solid8)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_13.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_13.step")
