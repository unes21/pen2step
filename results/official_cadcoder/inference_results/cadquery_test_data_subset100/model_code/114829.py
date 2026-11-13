import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.12631578947368421, 0.0).lineTo(0.12631578947368421, 0.12631578947368421).lineTo(0.12631578947368421, 1.3736842105263158).lineTo(0.12631578947368421, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.625, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.12631578947368421, 0.0).lineTo(0.12631578947368421, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 1.3736842105263158).lineTo(0.0, 0.12631578947368421).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.125)
solid=solid.union(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/114829.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/114829.step")
