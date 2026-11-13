import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.421875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 0.8368421052631579).lineTo(0.0, 0.8368421052631579).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.0078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.421875, 0.0078125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.007894736842105263, 0.0).lineTo(0.007894736842105263, 0.8359375).lineTo(0.0, 0.8359375).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(-0.0078125)
solid=solid.cut(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.7421875, -0.421875, 0.0078125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.007894736842105263, 0.0).lineTo(0.007894736842105263, 0.8359375).lineTo(0.0, 0.8359375).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(-0.0078125)
solid=solid.cut(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/95249.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/95249.step")
