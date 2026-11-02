"""Content-driven poster sizing and component-aware collision preflight.

All coordinates are points (72/in). The registry distinguishes intentional
parent-child containment from unintended sibling collisions. Shapes are
registered by their declared bounds, not by introspecting SVG paths.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .layout import Box, LayoutError, Overflow, PangoMeasurer


@dataclass(frozen=True)
class Component:
    key: str
    bounds: Box
    kind: str = "content"
    parent: str | None = None
    allow_overlap: bool = False


class ComponentRegistry:
    def __init__(self, canvas: Box):
        self.canvas = canvas
        self.items: dict[str, Component] = {}

    def add(self, item: Component) -> Component:
        if item.key in self.items:
            raise LayoutError(f"duplicate component id: {item.key}")
        if item.bounds.w <= 0 or item.bounds.h <= 0:
            raise LayoutError(f"non-positive component size: {item.key}")
        if item.parent and item.parent not in self.items:
            raise LayoutError(f"unknown parent {item.parent}: {item.key}")
        self.items[item.key] = item
        return item

    def _ancestor(self, ancestor: str, child: str) -> bool:
        seen = set()
        while child in self.items and self.items[child].parent:
            if child in seen:
                raise LayoutError("parent cycle detected")
            seen.add(child)
            child = self.items[child].parent
            if child == ancestor:
                return True
        return False

    def preflight(self) -> dict:
        errors = []
        parts = list(self.items.values())
        for item in parts:
            if not item.bounds.inside(self.canvas):
                errors.append(f"outside canvas: {item.key}")
            if item.parent and not item.bounds.inside(self.items[item.parent].bounds):
                errors.append(f"outside parent: {item.key} / {item.parent}")
        for i, a in enumerate(parts):
            for b in parts[i+1:]:
                if not a.bounds.intersects(b.bounds):
                    continue
                if a.allow_overlap or b.allow_overlap:
                    continue
                if self._ancestor(a.key, b.key) or self._ancestor(b.key, a.key):
                    continue
                errors.append(f"unintended overlap: {a.key} / {b.key}")
        return {"ok": not errors, "errors": errors, "component_count": len(parts)}

    def assert_valid(self) -> dict:
        report = self.preflight()
        if report["errors"]:
            raise LayoutError("; ".join(report["errors"]))
        return report


@dataclass(frozen=True)
class TextSpec:
    key: str
    text: str
    font: str = "Open Sans"
    pt: float = 32
    min_pt: float = 26
    bold: bool = False
    padding: float = 12
    line_spacing: float = 1.25

    def preferred_size(self, width: float, measurer: PangoMeasurer) -> tuple[float, float]:
        if self.pt < self.min_pt:
            raise Overflow(f"{self.key}: {self.pt}pt below {self.min_pt}pt minimum")
        inner = width - 2*self.padding
        if inner <= 0:
            raise Overflow(f"{self.key}: no space inside padding")
        metrics = measurer.measure(self.text, self.font, self.pt, inner, self.bold)
        required = max(metrics["height"], metrics["lines"]*self.pt*self.line_spacing)
        return width, required + 2*self.padding


@dataclass(frozen=True)
class FixedSpec:
    key: str
    preferred_height: float
    minimum_height: float

    def preferred_size(self, width: float, measurer: PangoMeasurer) -> tuple[float, float]:
        if self.preferred_height < self.minimum_height:
            raise Overflow(f"{self.key}: fixed visual below minimum height")
        return width, self.preferred_height


class VerticalStack:
    """Flow items by measured height without automatically shrinking fonts."""
    def __init__(self, region: Box, gap: float = 12, padding: float = 0):
        if gap < 0 or padding < 0:
            raise LayoutError("negative gap or padding")
        self.region, self.gap, self.padding = region, gap, padding

    def allocate(self, specs: Iterable[TextSpec | FixedSpec],
                 measurer: PangoMeasurer) -> dict[str, Box]:
        specs = list(specs)
        width = self.region.w - 2*self.padding
        y = self.region.y + self.padding
        allocated = {}
        for idx, spec in enumerate(specs):
            if spec.key in allocated:
                raise LayoutError(f"duplicate stack key: {spec.key}")
            _, height = spec.preferred_size(width, measurer)
            limit = self.region.y + self.region.h - self.padding
            if y+height > limit+1e-6:
                raise Overflow(f"{spec.key}: needs bottom {y+height:.1f}pt; "
                               f"available {limit:.1f}pt")
            allocated[spec.key] = Box(self.region.x+self.padding, y, width, height)
            y += height + (self.gap if idx < len(specs)-1 else 0)
        return allocated
