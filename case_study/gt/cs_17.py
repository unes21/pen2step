import cadquery as cq
head = cq.Workplane('XY').circle(45).extrude(12).faces('>Z').workplane().pushPoints([(34, 0)]).hole(13)
result = head.faces('<Z').workplane().circle(30).extrude(200)
