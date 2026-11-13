import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.25, 0.0, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.5, 0.0).lineTo(0.5, 0.5).lineTo(0.0, 0.5).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.03125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop1=wp_sketch1.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.5)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch2.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.5)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop3=wp_sketch3.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop3).extrude(0.5)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop4=wp_sketch4.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop4).extrude(0.5)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop5=wp_sketch5.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid5=wp_sketch5.add(loop5).extrude(0.5)
solid=solid.union(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop6=wp_sketch6.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid6=wp_sketch6.add(loop6).extrude(0.5)
solid=solid.union(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop7=wp_sketch7.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid7=wp_sketch7.add(loop7).extrude(0.5)
solid=solid.union(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop8=wp_sketch8.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid8=wp_sketch8.add(loop8).extrude(0.5)
solid=solid.union(solid8)
# Generating a workplane for sketch 9
wp_sketch9 = cq.Workplane(cq.Plane(cq.Vector(-0.25, -0.03125, -0.25), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop9=wp_sketch9.moveTo(0.5, 0.0).lineTo(0.5, 0.031578947368421054).lineTo(0.0, 0.031578947368421054).lineTo(0.0, 0.0).close()
solid9=wp_sketch9.add(loop9).extrude(0.5)
solid=solid.union(solid9)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/137986.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/137986.step")
