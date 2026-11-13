import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.5, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.9947368421052631, 0.0).lineTo(0.9947368421052631, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.5)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.125, -0.75, 0.5), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop1=wp_sketch1.moveTo(0.25263157894736843, 0.0).lineTo(0.25263157894736843, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(-0.375)
solid=solid.cut(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.5, -0.75, 0.25), cq.Vector(3.749399456654644e-33, 1.0, -6.123233995736766e-17), cq.Vector(1.0, 0.0, 6.123233995736766e-17)))
loop2=wp_sketch2.moveTo(0.06315789473684211, 0.0).circle(0.06315789473684211)
solid2=wp_sketch2.add(loop2).extrude(-0.9921875)
solid=solid.cut(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(0.5, 0.5, 0.25), cq.Vector(3.749399456654644e-33, 1.0, -6.123233995736766e-17), cq.Vector(1.0, 0.0, 6.123233995736766e-17)))
loop3=wp_sketch3.moveTo(0.06315789473684211, 0.0).circle(0.06315789473684211)
solid3=wp_sketch3.add(loop3).extrude(-0.9921875)
solid=solid.cut(solid3)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/71404.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/71404.step")
