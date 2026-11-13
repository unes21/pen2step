import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.4736842105263158).lineTo(0.7578947368421053, 0.48947368421052634).lineTo(0.7578947368421053, 0.9157894736842106).lineTo(0.7578947368421053, 0.9315789473684211).lineTo(0.7421052631578947, 0.9315789473684211).lineTo(0.7421052631578947, 0.9157894736842106).lineTo(0.7421052631578947, 0.48947368421052634).lineTo(0.7421052631578947, 0.4736842105263158).lineTo(0.7421052631578947, 0.04736842105263158).lineTo(0.7421052631578947, 0.031578947368421054).lineTo(0.7578947368421053, 0.031578947368421054).lineTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.4736842105263158).lineTo(0.7578947368421053, 0.9157894736842106).lineTo(0.7578947368421053, 0.9315789473684211).lineTo(0.7421052631578947, 0.9315789473684211).lineTo(0.7421052631578947, 0.48947368421052634).lineTo(0.7421052631578947, 0.4736842105263158).lineTo(0.7421052631578947, 0.04736842105263158).lineTo(0.7421052631578947, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.04736842105263158).lineTo(0.0, 0.4736842105263158).lineTo(0.0, 0.48947368421052634).lineTo(0.0, 0.9157894736842106).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch1.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid1=wp_sketch1.add(loop2).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch2.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid2=wp_sketch2.add(loop3).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch3.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid3=wp_sketch3.add(loop4).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch4.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid4=wp_sketch4.add(loop5).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch5.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid5=wp_sketch5.add(loop6).extrude(0.0078125)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch6.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid6=wp_sketch6.add(loop7).extrude(0.0078125)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop8=wp_sketch7.moveTo(0.011842105263157895, 0.0).circle(0.011842105263157895)
solid7=wp_sketch7.add(loop8).extrude(0.0078125)
solid=solid.union(solid7)