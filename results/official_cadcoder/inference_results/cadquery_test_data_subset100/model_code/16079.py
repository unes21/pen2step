import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, -0.0078125), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.078125, 0.0).lineTo(0.078125, 0.020230263157894737).lineTo(0.0, 0.020230263157894737).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.75)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.0390625, 0.015625), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.007894736842105263, 0.0).circle(0.007894736842105263)
solid1=wp_sketch1.add(loop1).extrude(-0.0390625)
solid=solid.cut(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.0390625, 0.0390625), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop2=wp_sketch2.moveTo(0.007894736842105263, 0.0).circle(0.007894736842105263)
solid2=wp_sketch2.add(loop2).extrude(-0.0390625)
solid=solid.cut(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.0390625, 0.015625), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch3.moveTo(0.007894736842105263, 0.0).circle(0.007894736842105263)
solid3=wp_sketch3.add(loop3).extrude(-0.0390625)
solid=solid.cut(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.0078125, -0.0390625, 0.0390625), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch4.moveTo(0.007894736842105263, 0.0).circle(0.007894736842105263)
solid4=wp_sketch4.add(loop4).extrude(-0.0390625)
solid=solid.cut(solid4)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/16079.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/16079.step")
