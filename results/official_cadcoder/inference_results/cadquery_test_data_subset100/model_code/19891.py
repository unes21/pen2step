import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.1796875, -0.1796875, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.3515625, 0.0).lineTo(0.3515625, 0.3515625).lineTo(0.0, 0.3515625).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.32080592105263156, 0.03075657894736842).lineTo(0.32080592105263156, 0.32080592105263156).lineTo(0.03075657894736842, 0.32080592105263156).lineTo(0.03075657894736842, 0.03075657894736842).close()
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.75)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/19891.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/19891.step")
