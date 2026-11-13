import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.0390625, 0.0).lineTo(0.0390625, 0.0390625).lineTo(0.0, 0.0390625).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.1015625, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop1=wp_sketch1.moveTo(0.0390625, 0.0).lineTo(0.0390625, 0.0390625).lineTo(0.0, 0.0390625).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.375)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.0703125, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch2.moveTo(0.0390625, 0.0).lineTo(0.0390625, 0.0390625).lineTo(0.0, 0.0390625).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.375)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(0.375, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop3=wp_sketch3.moveTo(0.0390625, 0.0).lineTo(0.0390625, 0.0390625).lineTo(0.0, 0.0390625).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop3).extrude(0.375)
solid=solid.union(solid3)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/129707.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/129707.step")
