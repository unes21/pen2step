import cadquery as cq
result = cq.Workplane('XY').circle(44 / 2).circle(40 / 2).extrude(30)
