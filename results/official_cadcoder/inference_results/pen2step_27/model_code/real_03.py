import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.04736842105263158, 0.8842105263157896).lineTo(0.04736842105263158, 0.04736842105263158).close()
loop2=wp_sketch0.moveTo(1.4526315789473685, 0.04736842105263158).lineTo(1.4526315789473685, 0.8842105263157896).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.7578947368421053, 0.04736842105263158).close()
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch1.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop4=wp_sketch1.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.04736842105263158, 0.8842105263157896).lineTo(0.04736842105263158, 0.04736842105263158).close()
loop5=wp_sketch1.moveTo(1.4526315789473685, 0.04736842105263158).lineTo(1.4526315789473685, 0.8842105263157896).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.7578947368421053, 0.04736842105263158).close()
solid1=wp_sketch1.add(loop3).add(loop4).add(loop5).extrude(0.0078125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch2.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop7=wp_sketch2.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.04736842105263158, 0.8842105263157896).lineTo(0.04736842105263158, 0.04736842105263158).close()
loop8=wp_sketch2.moveTo(1.4526315789473685, 0.04736842105263158).lineTo(1.4526315789473685, 0.8842105263157896).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.7578947368421053, 0.04736842105263158).close()
solid2=wp_sketch2.add(loop6).add(loop7).add(loop8).extrude(0.0078125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch3.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop10=wp_sketch3.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.04736842105263158, 0.8842105263157896).lineTo(0.04736842105263158, 0.04736842105263158).close()
loop11=wp_sketch3.moveTo(1.4526315789473685, 0.04736842105263158).lineTo(1.4526315789473685, 0.8842105263157896).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.7578947368421053, 0.04736842105263158).close()
solid3=wp_sketch3.add(loop9).add(loop10).add(loop11).extrude(0.0078125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.46875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch4.moveTo(1.5, 0.0).lineTo(1.5, 0.9315789473684211).lineTo(0.0, 0.9315789473684211).lineTo(0.0, 0.0).close()
loop13=wp_sketch4.moveTo(0.7578947368421053, 0.04736842105263158).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.04736842105263158, 0.8842105263157896).lineTo(0.04736842105263158, 0.04736842105263158).close()
loop14=wp_sketch4.moveTo(1.4526315789473685, 0.04736842105263158).lineTo(1.4526315789473685, 0.8842105263157896).lineTo(0.7578947368421053, 0.8842105263157896).lineTo(0.7578947368421053, 0.04736842105263158).close()
solid4=wp_sketch4.add(loop12).add(loop13).add(loop14).extrude(0.0078125)
solid=solid.union(solid4)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_stl/real_03.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/pen2step_27/model_step/real_03.step")
