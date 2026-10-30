import cadquery as cq
head = cq.Workplane('XY').circle(30).extrude(10).faces('>Z').workplane().pushPoints([(22, 0)]).hole(13)
result = head.faces('<Z').workplane().circle(20).extrude(150)
