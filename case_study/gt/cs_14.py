import cadquery as cq
result = cq.Workplane('XY').circle(20 / 2).circle(10.5 / 2).extrude(2)
