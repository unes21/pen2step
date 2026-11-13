import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.28125, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.28421052631578947, 0.0).circle(0.27828947368421053)
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/22599.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/22599.step")
