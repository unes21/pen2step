import cadquery as cq
# Generating a workplane for sketch 0
wp_sketch0 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(1.0, 0.0, 0.0), cq.Vector(0.0, 0.0, 1.0)))
loop0=wp_sketch0.moveTo(1.5, 0.0).lineTo(1.5, 1.5).lineTo(0.0, 1.5).lineTo(0.0, 0.0).close()
solid0=wp_sketch0.add(loop0).extrude(0.1484375)
solid=solid0
# Generating a workplane for sketch 1
wp_sketch1 = cq.Workplane(cq.Plane(cq.Vector(-0.75, -0.75, 0.0), cq.Vector(0.9993977281025862, 0.024541228522912326, 0.024533837163709046), cq.Vector(0.024541228522912326, 0.0, -0.9996988186962042)))
loop1=wp_sketch1.moveTo(0.15000000000000002, 0.0).lineTo(0.15000000000000002, 0.15000000000000002).lineTo(0.0, 0.15000000000000002).lineTo(0.0, 0.0).close()
solid1=wp_sketch1.add(loop1).extrude(0.296875)
solid=solid.union(solid1)
# Generating a workplane for sketch 2
wp_sketch2 = cq.Workplane(cq.Plane(cq.Vector(0.6015625, -0.75, 0.0), cq.Vector(0.9993977281025862, 0.024541228522912326, 0.024533837163709046), cq.Vector(0.024541228522912326, 0.0, -0.9996988186962042)))
loop2=wp_sketch2.moveTo(0.15000000000000002, 0.0).lineTo(0.15000000000000002, 0.15000000000000002).lineTo(0.0, 0.15000000000000002).lineTo(0.0, 0.0).close()
solid2=wp_sketch2.add(loop2).extrude(0.296875)
solid=solid.union(solid2)
# Generating a workplane for sketch 3
wp_sketch3 = cq.Workplane(cq.Plane(cq.Vector(-0.75, 0.6015625, 0.0), cq.Vector(0.9993977281025862, 0.024541228522912326, 0.024533837163709046), cq.Vector(0.024541228522912326, 0.0, -0.9996988186962042)))
loop3=wp_sketch3.moveTo(0.15000000000000002, 0.0).lineTo(0.15000000000000002, 0.15000000000000002).lineTo(0.0, 0.15000000000000002).lineTo(0.0, 0.0).close()
solid3=wp_sketch3.add(loop3).extrude(0.296875)
solid=solid.union(solid3)
# Generating a workplane for sketch 4
wp_sketch4 = cq.Workplane(cq.Plane(cq.Vector(0.6015625, 0.6015625, 0.0), cq.Vector(0.9993977281025862, 0.024541228522912326, 0.024533837163709046), cq.Vector(0.024541228522912326, 0.0, -0.9996988186962042)))
loop4=wp_sketch4.moveTo(0.15000000000000002, 0.0).lineTo(0.15000000000000002, 0.15000000000000002).lineTo(0.0, 0.15000000000000002).lineTo(0.0, 0.0).close()
solid4=wp_sketch4.add(loop4).extrude(0.296875)
solid=solid.union(solid4)
import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_stl/27987.stl")

import cadquery as cq
cq.exporters.export(solid, "./inference/inference_results/CAD-Coder/cadquery_test_data_subset100/model_step/27987.step")
