import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.6484375, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 1.2947368421052632).lineTo(0.0, 1.2947368421052632).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.25263157894736843, 0.25263157894736843).circle(0.12631578947368421)
loop2=wp_sketch0.moveTo(0.25263157894736843, 1.0421052631578949).circle(0.12631578947368421)
loop3=wp_sketch0.moveTo(0.7578947368421053, 0.6473684210526316).circle(0.09473684210526316)
loop4=wp_sketch0.moveTo(1.2473684210526317, 0.25263157894736843).circle(0.12631578947368421)
loop5=wp_sketch0.moveTo(1.2473684210526317, 1.0421052631578949).circle(0.12631578947368421)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).add(loop3).add(loop4).add(loop5).extrude(0.25)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.125, -0.25, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop6=wp_sketch1.moveTo(0.25263157894736843, 0.0).lineTo(0.25263157894736843, 0.5).lineTo(0.0, 0.5).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop6).extrude(0.25)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(-0.125, -0.25, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop7=wp_sketch2.moveTo(0.25263157894736843, 0.0).lineTo(0.25263157894736843, 0.5).lineTo(0.0, 0.5).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop7).extrude(0.25)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.125, -0.25, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop8=wp_sketch3.moveTo(0.25263157894736843, 0.0).lineTo(0.25263157894736843, 0.5).lineTo(0.0, 0.5).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop8).extrude(0.25)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(-0.125, -0.25, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop9=wp_sketch4.moveTo(0.25263157894736843, 0.0).lineTo(0.25263157894736843, 0.5).lineTo(0.0, 0.5).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop9).extrude(0.25)
solid=solid.union(solid4)
# Generating a workplane for sketch 5
wp_sketch5 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.25), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop10=wp_sketch5.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid5=wp_sketch5.add(loop10).extrude(-0.25)
solid=solid.cut(solid5)
# Generating a workplane for sketch 6
wp_sketch6 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.25), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop11=wp_sketch6.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid6=wp_sketch6.add(loop11).extrude(-0.25)
solid=solid.cut(solid6)
# Generating a workplane for sketch 7
wp_sketch7 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.25), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop12=wp_sketch7.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid7=wp_sketch7.add(loop12).extrude(-0.25)
solid=solid.cut(solid7)
# Generating a workplane for sketch 8
wp_sketch8 = cq.Workplane(cq.Plane(cq.Vector(-0.0390625, 0.0, 0.25), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop13=wp_sketch8.moveTo(0.039473684210526314, 0.0).circle(0.039473684210526314)
solid8=wp_sketch8.add(loop13).extrude(-0.25)
solid=solid.cut(solid8)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/86699.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/86699.step")
