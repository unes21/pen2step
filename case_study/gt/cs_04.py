import cadquery as cq
result = cq.Workplane('XY').circle(21 / 2).circle(13 / 2).extrude(12)
