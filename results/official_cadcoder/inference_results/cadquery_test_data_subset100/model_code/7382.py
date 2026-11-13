import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.109375, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.11052631578947367, 0.0).circle(0.11052631578947367)
loop1=wp_sketch0.moveTo(0.11052631578947367, 0.0).circle(0.009868421052631578)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.109375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(0.3203125, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch1.moveTo(0.15789473684210525, 0.0).circle(0.15789473684210525)
loop3=wp_sketch1.moveTo(0.15789473684210525, 0.0).circle(0.010526315789473684)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.109375)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.109375, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop4=wp_sketch2.moveTo(0.11052631578947367, 0.0).circle(0.11052631578947367)
loop5=wp_sketch2.moveTo(0.11052631578947367, 0.0).circle(0.009868421052631578)
solid2=wp_sketch2.add(loop4).add(loop5).extrude(0.109375)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.109375, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop6=wp_sketch3.moveTo(0.0, 0.0).threePointArc((0.010526315789473684, 0.010526315789473684), (0.021052631578947368, 0.0)).lineTo(0.021052631578947368, 0.1875).threePointArc((0.010526315789473684, 0.17703947368421053), (0.0, 0.1875)).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop6).extrude(0.109375)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.109375, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop7=wp_sketch4.moveTo(0.0, 0.0).threePointArc((0.010526315789473684, 0.010526315789473684), (0.021052631578947368, 0.0)).lineTo(0.021052631578947368, 0.1875).threePointArc((0.010526315789473684, 0.17703947368421053), (0.0, 0.1875)).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop7).extrude(0.109375)
solid=solid.union(solid4)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/7382.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/7382.step")
