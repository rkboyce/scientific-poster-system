"""Regression tests for component geometry and intrinsic height."""
import pytest
from posterkit.composition import Component, ComponentRegistry, FixedSpec, TextSpec, VerticalStack
from posterkit.layout import Box, LayoutError, Overflow, PangoMeasurer


def test_panel_contains_text_without_false_collision():
    registry = ComponentRegistry(Box(0, 0, 500, 500))
    registry.add(Component("panel", Box(20, 20, 300, 300), kind="panel"))
    registry.add(Component("body", Box(35, 40, 250, 100), parent="panel"))
    assert registry.assert_valid()["component_count"] == 2


def test_sibling_overlap_is_error():
    registry = ComponentRegistry(Box(0, 0, 500, 500))
    registry.add(Component("panel", Box(20, 20, 300, 300), kind="panel"))
    registry.add(Component("a", Box(30, 30, 200, 100), parent="panel"))
    registry.add(Component("b", Box(150, 70, 100, 100), parent="panel"))
    assert any("unintended overlap" in e for e in registry.preflight()["errors"])


def test_child_beyond_parent_detected():
    registry = ComponentRegistry(Box(0, 0, 500, 500))
    registry.add(Component("panel", Box(20, 20, 150, 150), kind="panel"))
    registry.add(Component("child", Box(100, 100, 100, 100), parent="panel"))
    assert any("outside parent" in e for e in registry.preflight()["errors"])


def test_nested_container_no_false_positive():
    registry = ComponentRegistry(Box(0, 0, 500, 500))
    registry.add(Component("root", Box(10, 10, 400, 400), kind="panel"))
    registry.add(Component("inner", Box(20, 20, 200, 200), kind="panel", parent="root"))
    registry.add(Component("text", Box(30, 30, 100, 80), parent="inner"))
    assert registry.assert_valid()["ok"]


def test_text_intrinsic_height_and_no_shrink():
    m = PangoMeasurer()
    a = TextSpec("body", "This is a short readable poster sentence.", pt=30, min_pt=28)
    assert a.preferred_size(500, m)[1] > 30
    with pytest.raises(Overflow):
        TextSpec("bad", "test", pt=17, min_pt=22).preferred_size(500, m)


def test_vertical_stack_measures_then_allocates():
    stack = VerticalStack(Box(20, 20, 520, 400), gap=12, padding=10)
    specs = [TextSpec("heading", "Primary study finding", pt=30),
             FixedSpec("figure", 130, 90)]
    placed = stack.allocate(specs, PangoMeasurer())
    assert placed["figure"].y >= placed["heading"].y + placed["heading"].h + 12


def test_vertical_stack_rejects_oversize():
    stack = VerticalStack(Box(0, 0, 200, 100), gap=12)
    with pytest.raises(Overflow):
        stack.allocate([FixedSpec("image", 120, 100)], PangoMeasurer())


def test_registration_rejects_unknown_parent():
    registry = ComponentRegistry(Box(0, 0, 500, 500))
    with pytest.raises(LayoutError):
        registry.add(Component("orphan", Box(0, 0, 10, 10), parent="missing"))
