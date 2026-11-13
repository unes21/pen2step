import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.25, -0.75), cq.Vector(3.749399456654644e-33, 1.0, -6.123233995736766e-17), cq.Vector(1.0, 0.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.12631578947368421, 0.0).lineTo(0.12631578947368421, 0.12631578947368421).lineTo(0.25263157894736843, 0.12631578947368421).lineTo(0.25263157894736843, 0.7578947368421053).lineTo(0.3736842105263158, 0.7578947368421053).lineTo(0.3736842105263158, 1.5).lineTo(0.25263157894736843, 1.5).lineTo(0.25263157894736843, 1.3736842105263158).lineTo(0.12631578947368421, 1.3736842105263158).lineTo(0.12631578947368421, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.25263157894736843, 0.12631578947368421).circle(0.06315789473684211)
loop2=wp_sketch0.moveTo(0.25263157894736843, 1.3736842105263158).circle(0.06315789473684211)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).extrude(0.25)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/20372.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/20372.step")
