import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.007894736842105263).lineTo(0.0, 0.007894736842105263).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch3.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop3).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch4.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop4).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch5.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid5=wp_sketch5.add(loop5).extrude(0.0078125)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch6.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid6=wp_sketch6.add(loop6).extrude(0.0078125)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch7.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid7=wp_sketch7.add(loop7).extrude(0.0078125)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop8=wp_sketch8.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid8=wp_sketch8.add(loop8).extrude(0.0078125)
solid=solid.union(solid8)
# Generating a workplane for sketch 9
wp_sketch9 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch9.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid9=wp_sketch9.add(loop9).extrude(0.0078125)
solid=solid.union(solid9)
# Generating a workplane for sketch 10
wp_sketch10 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch10.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid10=wp_sketch10.add(loop10).extrude(0.0078125)
solid=solid.union(solid10)
# Generating a workplane for sketch 11
wp_sketch11 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop11=wp_sketch11.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid11=wp_sketch11.add(loop11).extrude(0.0078125)
solid=solid.union(solid11)
# Generating a workplane for sketch 12
wp_sketch12 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch12.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid12=wp_sketch12.add(loop12).extrude(0.0078125)
solid=solid.union(solid12)
# Generating a workplane for sketch 13
wp_sketch13 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop13=wp_sketch13.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid13=wp_sketch13.add(loop13).extrude(0.0078125)
solid=solid.union(solid13)
# Generating a workplane for sketch 14
wp_sketch14 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop14=wp_sketch14.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid14=wp_sketch14.add(loop14).extrude(0.0078125)
solid=solid.union(solid14)
# Generating a workplane for sketch 15
wp_sketch15 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop15=wp_sketch15.moveTo(0.0, 0.0).threePointArc((0.1125, -0.1125), (0.225, 0.0)).lineTo(0.0, 0.0).close()
solid15=wp_sketch15.add(loop15).extrude(0.0078125)
solid=solid.union(solid15)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_14.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_14.step")
