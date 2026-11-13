import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.3).lineTo(0.0, 0.3).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.031578947368421054, 0.031578947368421054).circle(0.015789473684210527)
loop2=wp_sketch0.moveTo(0.031578947368421054, 0.26842105263157895).circle(0.015789473684210527)
loop3=wp_sketch0.moveTo(0.718421052631579, 0.031578947368421054).circle(0.015789473684210527)
loop4=wp_sketch0.moveTo(0.718421052631579, 0.26842105263157895).circle(0.015789473684210527)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch1.moveTo(0.75, 0.0).lineTo(0.75, 0.3).lineTo(0.0, 0.3).lineTo(0.0, 0.0).close()
loop6=wp_sketch1.moveTo(0.031578947368421054, 0.031578947368421054).circle(0.015789473684210527)
loop7=wp_sketch1.moveTo(0.031578947368421054, 0.26842105263157895).circle(0.015789473684210527)
loop8=wp_sketch1.moveTo(0.718421052631579, 0.031578947368421054).circle(0.015789473684210527)
loop9=wp_sketch1.moveTo(0.718421052631579, 0.26842105263157895).circle(0.015789473684210527)
solid1=wp_sketch1.add(loop5).add(loop6).add(loop7).add(loop8).add(loop9).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch2.moveTo(0.75, 0.0).lineTo(0.75, 0.3).lineTo(0.0, 0.3).lineTo(0.0, 0.0).close()
loop11=wp_sketch2.moveTo(0.031578947368421054, 0.031578947368421054).circle(0.015789473684210527)
loop12=wp_sketch2.moveTo(0.031578947368421054, 0.26842105263157895).circle(0.015789473684210527)
loop13=wp_sketch2.moveTo(0.718421052631579, 0.031578947368421054).circle(0.015789473684210527)
loop14=wp_sketch2.moveTo(0.718421052631579, 0.26842105263157895).circle(0.015789473684210527)
solid2=wp_sketch2.add(loop10).add(loop11).add(loop12).add(loop13).add(loop14).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop15=wp_sketch3.moveTo(0.75, 0.0).lineTo(0.75, 0.3).lineTo(0.0, 0.3).lineTo(0.0, 0.0).close()
loop16=wp_sketch3.moveTo(0.031578947368421054, 0.031578947368421054).circle(0.015789473684210527)
loop17=wp_sketch3.moveTo(0.031578947368421054, 0.26842105263157895).circle(0.015789473684210527)
loop18=wp_sketch3.moveTo(0.718421052631579, 0.031578947368421054).circle(0.015789473684210527)
loop19=wp_sketch3.moveTo(0.718421052631579, 0.26842105263157895).circle(0.015789473684210527)
solid3=wp_sketch3.add(loop15).add(loop16).add(loop17).add(loop18).add(loop19).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop20=wp_sketch4.moveTo(0.75, 0.0).lineTo(0.75, 0.3).lineTo(0.0, 0.3).lineTo(0.0, 0.0).close()
loop21=wp_sketch4.moveTo(0.031578947368421054, 0.031578947368421054).circle(0.015789473684210527)
loop22=wp_sketch4.moveTo(0.031578947368421054, 0.26842105263157895).circle(0.015789473684210527)
loop23=wp_sketch4.moveTo(0.718421052631579, 0.031578947368421054).circle(0.015789473684210527)
loop24=wp_sketch4.moveTo(0.718421052631579, 0.26842105263157895).circle(0.015789473684210527)
solid4=wp_sketch4.add(loop20).add(loop21).add(loop22).add(loop23).add(loop24).extrude(0.0078125)
solid=solid.union(solid4)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/cs_05.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/cs_05.step")
