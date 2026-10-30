import cadquery as cq
head = cq.Workplane('XY').circle(37.5).extrude(12).faces('>Z').workplane().pushPoints([(28, 0)]).hole(13)
result = head.faces('<Z').workplane().circle(25).extrude(180)
