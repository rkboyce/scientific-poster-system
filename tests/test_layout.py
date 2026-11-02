from posterkit.layout import Box,MeasuredText,Overflow,PosterCanvas,PangoMeasurer
import pytest

def test_edges_not_overlap():
    assert not Box(0,0,100,100).intersects(Box(100,0,100,100))
    assert Box(0,0,100,100).intersects(Box(99,0,100,100))

def test_minimum_font():
    with pytest.raises(Overflow):MeasuredText('bad','test',Box(0,0,100,100),17,min_pt=20).validate(PangoMeasurer())

def test_wrap_fails():
    with pytest.raises(Overflow):MeasuredText('bad','This paragraph certainly exceeds the short width',Box(0,0,80,70),30,min_pt=25).validate(PangoMeasurer())

def test_collisions():
    p=PosterCanvas(2,2)
    p.add_text(MeasuredText('one','A',Box(0,0,70,70),20,min_pt=20))
    p.add_text(MeasuredText('two','B',Box(35,35,70,70),20,min_pt=20))
    result=p.preflight();assert not result['ok'];assert result['errors'][0].startswith('overlap:')
