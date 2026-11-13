import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.4296875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.8526315789473684).lineTo(0.0, 0.8526315789473684).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.03125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.4296875, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.1105263157894737, 0.0).lineTo(0.1105263157894737, 0.8515625).lineTo(0.0, 0.8515625).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.03125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.6328125, -0.4296875, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.1105263157894737, 0.0).lineTo(0.1105263157894737, 0.8515625).lineTo(0.0, 0.8515625).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.03125)
solid=solid.union(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/145441.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/145441.step")
