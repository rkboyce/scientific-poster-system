import pytest
import svgwrite
from posterkit.evidence_section import BarDatum, add_evidence_section
from posterkit.layout import Box, Overflow, LayoutError

def test_section_draws_and_reports_bounds():
    d=svgwrite.Drawing(size=('20in','16in'))
    x=add_evidence_section(d,Box(0,0,1300,1000),key='test',
         heading='Evidence section',caption='Synthetic values, not research data.',
         interpretation='A clear conclusion.',values=[BarDatum('A',3),BarDatum('B',5)])
    assert x['report']['ok']
    assert set(x['bounds'])=={'heading','chart','caption','interpretation'}
    assert 'test-figure' in d.tostring()

def test_short_region_rejects_content():
    d=svgwrite.Drawing()
    with pytest.raises(Overflow):
        add_evidence_section(d,Box(0,0,1200,320),key='small',heading='Heading',
          caption='Caption',interpretation='Summary',values=[BarDatum('A',1)])

def test_negative_data_rejected():
    d=svgwrite.Drawing()
    with pytest.raises(LayoutError):
        add_evidence_section(d,Box(0,0,1200,1000),key='negative',heading='Heading',
          caption='Caption',interpretation='Summary',values=[BarDatum('A',-1)])
