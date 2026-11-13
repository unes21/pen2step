import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid0=wp_sketch0.add(loop0).extrude(0.1484375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop1=wp_sketch1.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid1=wp_sketch1.add(loop1).extrude(0.1484375)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch2.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid2=wp_sketch2.add(loop2).extrude(0.1484375)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop3=wp_sketch3.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid3=wp_sketch3.add(loop3).extrude(0.1484375)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop4=wp_sketch4.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid4=wp_sketch4.add(loop4).extrude(0.1484375)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop5=wp_sketch5.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid5=wp_sketch5.add(loop5).extrude(0.1484375)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop6=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid6=wp_sketch6.add(loop6).extrude(0.1484375)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop7=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid7=wp_sketch7.add(loop7).extrude(0.1484375)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop8=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid8=wp_sketch8.add(loop8).extrude(0.1484375)
solid=solid.union(solid8)
# Generating a workplane for sketch 9
wp_sketch9 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop9=wp_sketch9.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid9=wp_sketch9.add(loop9).extrude(0.1484375)
solid=solid.union(solid9)
# Generating a workplane for sketch 10
wp_sketch10 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop10=wp_sketch10.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid10=wp_sketch10.add(loop10).extrude(0.1484375)
solid=solid.union(solid10)
# Generating a workplane for sketch 11
wp_sketch11 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop11=wp_sketch11.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid11=wp_sketch11.add(loop11).extrude(0.1484375)
solid=solid.union(solid11)
# Generating a workplane for sketch 12
wp_sketch12 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop12=wp_sketch12.moveTo(0.0394736842