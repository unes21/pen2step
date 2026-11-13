import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.7421875, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.37302631578947365, -0.6372532894736842).lineTo(1.1035361842105262, -0.6372532894736842).lineTo(1.4765625, 0.0).lineTo(1.1035361842105262, 0.6372532894736842).lineTo(0.37302631578947365, 0.6372532894736842).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.5)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.6015625, 0.0, 0.5), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.6078947368421053, 0.0).circle(0.6078947368421053)
solid1=wp_sketch1.add(loop1).extrude(0.25)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/89304.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/89304.step")
