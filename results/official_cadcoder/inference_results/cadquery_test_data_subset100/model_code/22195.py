import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.0, 0.0).threePointArc((0.07399407633181948, -0.17863750261554895), (0.25263157894736843, -0.25263157894736843)).lineTo(1.2473684210526317, -0.25263157894736843).threePointArc((1.4260059236681806, -0.17863750261554895), (1.5, 0.0)).lineTo(1.5, 0.12631578947368421).threePointArc((1.4260059236681806, 0.3049532920892331), (1.2473684210526317, 0.37894736842105264)).lineTo(0.25263157894736843, 0.37894736842105264).threePointArc((0.07399407633181948, 0.3049532920892331), (0.0, 0.12631578947368421)).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.1875)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.5, -0.1875, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop1=wp_sketch1.moveTo(0.18947368421052632, 0.0).circle(0.18947368421052632)
solid1=wp_sketch1.add(loop1).extrude(0.5625)
solid=solid.union(solid1)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/22195.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/22195.step")
