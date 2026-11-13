import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.0, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(0.0, 0.0).threePointArc((0.03699703816590996, -0.08931875130777447), (0.12631578947368421, -0.12631578947368421)).lineTo(0.6236842105263158, -0.12631578947368421).threePointArc((0.7130029618340903, -0.08931875130777447), (0.75, 0.0)).lineTo(0.75, 0.12631578947368421).threePointArc((0.7130029618340903, 0.21563454078145864), (0.6236842105263158, 0.25263157894736843)).lineTo(0.12631578947368421, 0.25263157894736843).threePointArc((0.03699703816590996, 0.21563454078145864), (0.0, 0.12631578947368421)).lineTo(0.0, 0.0).close()
loop1=wp_sketch0.moveTo(0.06315789473684211, 0.06315789473684211).circle(0.031578947368421054)
loop2=wp_sketch0.moveTo(0.6868421052631579, 0.06315789473684211).circle(0.031578947368421054)
solid0=wp_sketch0.add(loop0).add(loop1).add(loop2).extrude(0.03125)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.7109375, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop3=wp_sketch1.moveTo(0.035526315789473684, 0.0).circle(0.035526315789473684)
solid1=wp_sketch1.add(loop3).extrude(0.125)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.6484375, 0.0, 0.03125), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop4=wp_sketch2.moveTo(0.035526315789473684, 0.0).circle(0.035526315789473684)
solid2=wp_sketch2.add(loop4).extrude(0.125)
solid=solid.union(solid2)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/159865.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/159865.step")
