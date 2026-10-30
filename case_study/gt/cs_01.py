import cadquery as cq
result = cq.Workplane('XY').circle(65 / 2).circle(60 / 2).extrude(30)
