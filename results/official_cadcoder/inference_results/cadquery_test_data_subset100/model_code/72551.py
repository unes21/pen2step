import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.375, 0.0, -0.75), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.7578947368421053, 0.0).lineTo(0.7578947368421053, 0.7578947368421053).lineTo(0.7105263157894737, 0.7578947368421053).lineTo(0.7105263157894737, 0.7894736842105263).lineTo(0.04736842105263158, 0.7894736842105263).lineTo(0.04736842105263158, 0.7578947368421053).lineTo(0.0, 0.7578947368421053).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.046875)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.375, 0.0, -0.0625), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop1=wp_sketch1.moveTo(0.046875, 0.0).lineTo(0.046875, 0.046875).lineTo(0.0, 0.046875).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.75)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.375, 0.0, 0.6953125), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch2.moveTo(0.046875, 0.0).lineTo(0.046875, 0.046875).lineTo(0.0, 0.046875).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.75)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.375, 0.0, -0.75), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop3=wp_sketch3.moveTo(0.046875, 0.0).lineTo(0.046875, 0.046875).lineTo(0.0, 0.046875).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop3).extrude(0.75)
solid=solid.union(solid3)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/72551.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/72551.step")
