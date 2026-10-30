import cadquery as cq
import math
def hexagon(wp, s, h):
    return wp.polygon(6, s / math.cos(math.pi / 6)).extrude(h)
result = hexagon(cq.Workplane('XY'), 17, 6.4).faces('<Z').workplane().circle(5).extrude(130)
