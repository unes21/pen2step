import cadquery as cq
result = cq.Workplane('XY').circle(16 / 2).circle(8.4 / 2).extrude(1.6)
