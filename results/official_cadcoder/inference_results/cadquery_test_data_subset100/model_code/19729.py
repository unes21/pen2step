import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.078125, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.07894736842105263, 0.0).circle(0.07894736842105263)
loop1=wp_sketch0.moveTo(0.07894736842105263, 0.0).circle(0.039473684210526314)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.078125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch1.moveTo(0.15000000000000002, 0.0).circle(0.15000000000000002)
loop3=wp_sketch1.moveTo(0.15000000000000002, 0.0).circle(0.07500000000000001)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.1015625)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/19729.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/19729.step")
