import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop1=wp_sketch0.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.75)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch1.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop3=wp_sketch1.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.75)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch2.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop5=wp_sketch2.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid2=wp_sketch2.add(loop4).add(loop5).extrude(0.0390625)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch3.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop7=wp_sketch3.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid3=wp_sketch3.add(loop6).add(loop7).extrude(0.0390625)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop8=wp_sketch4.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop9=wp_sketch4.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid4=wp_sketch4.add(loop8).add(loop9).extrude(0.0390625)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch5.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop11=wp_sketch5.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid5=wp_sketch5.add(loop10).add(loop11).extrude(0.0390625)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop13=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid6=wp_sketch6.add(loop12).add(loop13).extrude(0.0390625)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop14=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop15=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid7=wp_sketch7.add(loop14).add(loop15).extrude(0.0390625)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop16=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop17=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid8=wp_sketch8.add(loop16).add(loop17).extrude(0.0390625)
solid=solid.union(solid8)
# Generating a workplane for sketch 9
wp_sketch9 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop18=wp_sketch9.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop19=wp_sketch9.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid9=wp_sketch9.add(loop18).add(loop19).extrude(0.0390625)
solid=solid.union(solid9)
# Generating a workplane for sketch 10
wp_sketch10 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop20=wp_sketch10.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop21=wp_sketch10.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid10=wp_sketch10.add(loop20).add(loop21).extrude(0.0390625)
solid=solid.union(solid10)
# Generating a workplane for sketch 11
wp_sketch11 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop22=wp_sketch11.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop23=wp_sketch11.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid11=wp_sketch11.add(loop22).add(loop23).extrude(0.0390625)
solid=solid.union(solid11)
# Generating a workplane for sketch 12
wp_sketch12 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop24=wp_sketch12.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
loop25=wp_sketch12.moveTo(0.039473684210526314, 0.0).circle(0.03453947368421052)
solid12=wp_sketch12.add(loop24).add(loop25).extrude
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_19.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_19.step")
