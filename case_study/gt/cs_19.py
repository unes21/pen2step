import cadquery as cq
result = (cq.Workplane('XY').box(70, 35, 6).faces('>Z').workplane().pushPoints([(-20, 0)]).hole(9).faces('>Z').workplane().center(25, 0).rect(20, 12).cutThruAll())
