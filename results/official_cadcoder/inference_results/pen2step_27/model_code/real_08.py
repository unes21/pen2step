import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop2=wp_sketch0.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch1.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop4=wp_sketch1.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop5=wp_sketch1.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid1=wp_sketch1.add(loop3).add(loop4).add(loop5).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch2.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop7=wp_sketch2.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop8=wp_sketch2.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid2=wp_sketch2.add(loop6).add(loop7).add(loop8).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch3.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop10=wp_sketch3.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop11=wp_sketch3.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid3=wp_sketch3.add(loop9).add(loop10).add(loop11).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch4.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop13=wp_sketch4.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop14=wp_sketch4.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid4=wp_sketch4.add(loop12).add(loop13).add(loop14).extrude(0.0078125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.5, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop15=wp_sketch5.moveTo(1.5, 0.0).lineTo(1.5, 0.9947368421052631).lineTo(0.0, 0.9947368421052631).lineTo(0.0, 0.0).close()
loop16=wp_sketch5.moveTo(0.7578947368421053, 0.5052631578947369).circle(0.5052631578947369)
loop17=wp_sketch5.moveTo(0.7578947368421053, 0.9947368421052631).circle(0.5052631578947369)
solid5=wp_sketch5.add(loop15).add(loop16).add(loop17).extrude(0.0078125)
solid=solid.union(solid5)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_08.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_08.step")
