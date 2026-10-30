import cadquery as cq
result = cq.Workplane('XY').box(80, 40, 8).faces('>Z').workplane().pushPoints([(-25, 0), (25, 0)]).hole(9)
