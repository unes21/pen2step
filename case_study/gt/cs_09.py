import cadquery as cq
import math
def hexagon(wp, s, h):
    return wp.polygon(6, s / math.cos(math.pi / 6)).extrude(h)
result = hexagon(cq.Workplane('XY'), 19, 7.5).faces('<Z').workplane().circle(6).extrude(30)
