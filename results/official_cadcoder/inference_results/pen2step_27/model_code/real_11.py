import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch1.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop3=wp_sketch1.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch2.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop5=wp_sketch2.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid2=wp_sketch2.add(loop4).add(loop5).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch3.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop7=wp_sketch3.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid3=wp_sketch3.add(loop6).add(loop7).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop8=wp_sketch4.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop9=wp_sketch4.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid4=wp_sketch4.add(loop8).add(loop9).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch5.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop11=wp_sketch5.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid5=wp_sketch5.add(loop10).add(loop11).extrude(0.0078125)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch6.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop13=wp_sketch6.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid6=wp_sketch6.add(loop12).add(loop13).extrude(0.0078125)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop14=wp_sketch7.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop15=wp_sketch7.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid7=wp_sketch7.add(loop14).add(loop15).extrude(0.0078125)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop16=wp_sketch8.moveTo(0.75, 0.0).lineTo(0.75, 0.37894736842105264).lineTo(0.0, 0.37894736842105264).lineTo(0.0, 0.0).close()
loop17=wp_sketch8.moveTo(0.37894736842105264, 0.18947368421052632).circle(0.031578947368421054)
solid8=wp_sketch8.add(loop16).add(loop17).extrude(0.0078125)
solid=solid.union(solid8)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_11.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_11.step")
