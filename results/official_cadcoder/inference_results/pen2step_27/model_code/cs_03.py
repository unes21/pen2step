import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0078125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop2=wp_sketch1.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid1=wp_sketch1.add(loop1).add(loop2).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.015625), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch2.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop4=wp_sketch2.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid2=wp_sketch2.add(loop3).add(loop4).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0234375), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch3.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop6=wp_sketch3.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid3=wp_sketch3.add(loop5).add(loop6).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch4.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop8=wp_sketch4.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid4=wp_sketch4.add(loop7).add(loop8).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch5.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop10=wp_sketch5.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid5=wp_sketch5.add(loop9).add(loop10).extrude(0.0078125)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop11=wp_sketch6.moveTo(0.75, 0.0).lineTo(0.75, 0.25263157894736843).lineTo(0.0, 0.25263157894736843).lineTo(0.0, 0.0).close()
loop12=wp_sketch6.moveTo(0.718421052631579, 0.031578947368421054).lineTo(0.718421052631579, 0.2210526315789474).lineTo(0.031578947368421054, 0.2210526315789474).lineTo(0.031578947368421054, 0.031578947368421054).close()
solid6=wp_sketch6.add(loop11).add(loop12).extrude(0.0078125)
solid=solid.union(solid6)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/cs_03.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/cs_03.step")
