import cadquery as cq
result = cq.Workplane('XY').circle(55 / 2).circle(50 / 2).extrude(30)
