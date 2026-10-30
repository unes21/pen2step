import cadquery as cq
base = cq.Workplane('XY').box(100, 60, 8).faces('>Z').workplane().pushPoints([(-35, 0), (35, 0)]).hole(11)
arm = cq.Workplane('XZ').center(0, 49).rect(60, 90).extrude(-8).translate((0, -26, 0))
arm = arm.faces('<Y').workplane(centerOption='CenterOfMass').hole(40)
result = base.union(arm)
