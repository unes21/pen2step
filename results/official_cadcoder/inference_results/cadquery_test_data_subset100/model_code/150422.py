import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.75, 0.0).lineTo(0.75, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.12631578947368421, 0.12631578947368421).circle(0.031578947368421054)
loop2=wp_sketch0.moveTo(0.12631578947368421, 0.6236842105263158).circle(0.031578947368421054)
loop3=wp_sketch0.moveTo(0.6236842105263158, 0.12631578947368421).circle(0.031578947368421054)
loop4=wp_sketch0.moveTo(0.6236842105263158, 0.6236842105263158).circle(0.031578947368421054)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).extrude(0.1484375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop5=wp_sketch1.moveTo(0.75, 0.0).lineTo(0.75, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.0).close()
loop6=wp_sketch1.moveTo(0.12631578947368421, 0.12631578947368421).circle(0.031578947368421054)
loop7=wp_sketch1.moveTo(0.12631578947368421, 0.6236842105263158).circle(0.031578947368421054)
loop8=wp_sketch1.moveTo(0.6236842105263158, 0.12631578947368421).circle(0.031578947368421054)
loop9=wp_sketch1.moveTo(0.6236842105263158, 0.6236842105263158).circle(0.031578947368421054)
solid1=wp_sketch1.add(loop5).add(loop6).add(loop7).add(loop8).add(loop9).extrude(0.1484375)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch2.moveTo(0.75, 0.0).lineTo(0.75, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.0).close()
loop11=wp_sketch2.moveTo(0.12631578947368421, 0.12631578947368421).circle(0.031578947368421054)
loop12=wp_sketch2.moveTo(0.12631578947368421, 0.6236842105263158).circle(0.031578947368421054)
loop13=wp_sketch2.moveTo(0.6236842105263158, 0.12631578947368421).circle(0.031578947368421054)
loop14=wp_sketch2.moveTo(0.6236842105263158, 0.6236842105263158).circle(0.031578947368421054)
solid2=wp_sketch2.add(loop10).add(loop11).add(loop12).add(loop13).add(loop14).extrude(0.1484375)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop15=wp_sketch3.moveTo(0.75, 0.0).lineTo(0.75, 0.75).lineTo(0.0, 0.75).lineTo(0.0, 0.0).close()
loop16=wp_sketch3.moveTo(0.12631578947368421, 0.12631578947368421).circle(0.031578947368421054)
loop17=wp_sketch3.moveTo(0.12631578947368421, 0.6236842105263158).circle(0.031578947368421054)
loop18=wp_sketch3.moveTo(0.6236842105263158, 0.12631578947368421).circle(0.031578947368421054)
loop19=wp_sketch3.moveTo(0.6236842105263158, 0.6236842105263158).circle(0.031578947368421054)
solid3=wp_sketch3.add(loop15).add(loop16).add(loop17).add(loop18).add(loop19).extrude(0.1484375)
solid=solid.union(solid3)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/150422.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/150422.step")
