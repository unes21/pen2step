import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.03125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.71875, -0.4375, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(1.4375, 0.0).lineTo(1.4375, 0.875).lineTo(0.0, 0.875).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(-0.25)
solid=solid.cut(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.5390625, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.027631578947368417, 0.0).circle(0.027631578947368417)
solid2=wp_sketch2.add(loop2).extrude(-0.25)
solid=solid.cut(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(0.46875, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch3.moveTo(0.027631578947368417, 0.0).circle(0.027631578947368417)
solid3=wp_sketch3.add(loop3).extrude(-0.25)
solid=solid.cut(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.5390625, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch4.moveTo(0.027631578947368417, 0.0).circle(0.027631578947368417)
solid4=wp_sketch4.add(loop4).extrude(-0.25)
solid=solid.cut(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(0.46875, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch5.moveTo(0.027631578947368417, 0.0).circle(0.027631578947368417)
solid5=wp_sketch5.add(loop5).extrude(-0.25)
solid=solid.cut(solid5)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/46804.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/46804.step")
