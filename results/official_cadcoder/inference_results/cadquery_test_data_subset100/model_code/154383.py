import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.328125, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop0=wp_sketch0.moveTo(0.33157894736842103, 0.0).circle(0.33157894736842103)
loop1=wp_sketch0.moveTo(0.33157894736842103, 0.0).circle(0.29605263157894735)
solid0=wp_sketch0.add(loop0).add(loop1).extrude(0.75)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.296875, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop2=wp_sketch1.moveTo(0.30394736842105263, 0.0).circle(0.30394736842105263)
loop3=wp_sketch1.moveTo(0.30394736842105263, 0.0).circle(0.29605263157894735)
solid1=wp_sketch1.add(loop2).add(loop3).extrude(0.75)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.296875, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop4=wp_sketch2.moveTo(0.30394736842105263, 0.0).circle(0.30394736842105263)
loop5=wp_sketch2.moveTo(0.30394736842105263, 0.0).circle(0.29605263157894735)
solid2=wp_sketch2.add(loop4).add(loop5).extrude(0.03125)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.296875, 0.0, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop6=wp_sketch3.moveTo(0.30394736842105263, 0.0).circle(0.30394736842105263)
loop7=wp_sketch3.moveTo(0.30394736842105263, 0.0).circle(0.29605263157894735)
solid3=wp_sketch3.add(loop6).add(loop7).extrude(0.03125)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.75, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop8=wp_sketch4.moveTo(0.0, 0.0).threePointArc((0.03699703816590974, 0.12212182064040162), (0.12236842105263158, 0.20526315789473684)).threePointArc((0.06118421052631579, 0.26644736842105265), (0.0, 0.20526315789473684)).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop8).extrude(-0.03125)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(0.0, -0.75, 0.0), cq.Vector(1.0, 6.123233995736766e-17, -6.123233995736766e-17), cq.Vector(6.123233995736766e-17, -1.0, 6.123233995736766e-17)))
loop9=wp_sketch5.moveTo(0.0, 0.0).threePointArc((0.06118421052631579, 0.26644736842105265), (0.12236842105263158, 0.20526315789473684)).threePointArc((0.03699703816590974, 0.12212182064040162), (0.0, 0.0)).close()
solid5=wp_sketch5.add(loop9).extrude(-0.03125)
solid=solid.union(solid5)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/154383.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/154383.step")
