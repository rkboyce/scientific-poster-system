"""Native editable SVG figures for the Study Agent poster."""
from __future__ import annotations

from dataclasses import dataclass
from math import hypot
import svgwrite


@dataclass(frozen=True)
class ArrowGeometry:
    start: tuple[float, float]
    shaft_end: tuple[float, float]
    tip: tuple[float, float]
    triangle: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]


def explicit_arrow(start: tuple[float, float], target: tuple[float, float], *,
                   head_length: float = 20, head_width: float = 16,
                   clearance: float = 10) -> ArrowGeometry:
    """Return an arrow whose shaft ends at its explicit triangle base.

    ``target`` is the target boundary point.  The tip remains ``clearance`` points
    before it, so neither shaft nor arrowhead crosses into the target box.
    """
    dx, dy = target[0] - start[0], target[1] - start[1]
    distance = hypot(dx, dy)
    if distance <= head_length + clearance:
        raise ValueError("connector is too short for its arrowhead and clearance")
    ux, uy = dx / distance, dy / distance
    tip = (target[0] - clearance * ux, target[1] - clearance * uy)
    base = (tip[0] - head_length * ux, tip[1] - head_length * uy)
    nx, ny = -uy, ux
    left = (base[0] + nx * head_width / 2, base[1] + ny * head_width / 2)
    right = (base[0] - nx * head_width / 2, base[1] - ny * head_width / 2)
    return ArrowGeometry(start, base, tip, (tip, left, right))


def draw_arrow(drawing: svgwrite.Drawing, group, start, target, *, color: str,
               head_length: float = 20, head_width: float = 16, clearance: float = 10,
               stroke_width: float = 4) -> ArrowGeometry:
    geometry = explicit_arrow(start, target, head_length=head_length,
                              head_width=head_width, clearance=clearance)
    group.add(drawing.line(start=geometry.start, end=geometry.shaft_end, stroke=color,
                            stroke_width=stroke_width, stroke_linecap="round"))
    group.add(drawing.polygon(geometry.triangle, fill=color))
    return geometry
