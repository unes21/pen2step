import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.4296875, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.21907894736842107, -0.3741776315789474).lineTo(0.648108552631579, -0.3741776315789474).lineTo(0.8671875000000001, 0.0).lineTo(0.648108552631579, 0.3741776315789474).lineTo(0.21907894736842107, 0.3741776315789474).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/2229.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/2229.step")
