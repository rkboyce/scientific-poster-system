"""Measured section compositor: heading, chart, caption, and interpretation.

Experimental: use illustrative data only unless explicitly supplied by caller.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import json
import svgwrite
from .layout import Box, PangoMeasurer, LayoutError, Overflow
from .composition import Component, ComponentRegistry, TextSpec, FixedSpec, VerticalStack

@dataclass(frozen=True)
class BarDatum:
    label: str
    value: float

@dataclass(frozen=True)
class SectionTheme:
    dark: str = '#16384C'
    accent: str = '#1D732B'
    light: str = '#F5F4EF'
    ink: str = '#203645'
    muted: str = '#686758'


def _draw_text_lines(svg, parent, text, region: Box, font_pt=26, color='#203645',
                     bold=False, font='Open Sans', line_factor=1.26):
    """Render intentional line breaks after Pango size checks; never shrink."""
    measurer = PangoMeasurer()
    met = measurer.measure(text, font, font_pt, region.w, bold)
    lines = text.split('\n')
    if met['lines'] != len(lines):
        raise Overflow(f'Unexpected line break for {text[:40]!r}')
    height = max(met['height'], len(lines)*font_pt*line_factor)
    if height > region.h:
        raise Overflow(f'Text requires {height:.1f}pt but box holds {region.h:.1f}pt')
    for i, line in enumerate(lines):
        parent.add(svg.text(line, insert=(region.x,region.y+font_pt*(1+i*line_factor)),
            font_family=font,font_size=font_pt,
            font_weight='bold' if bold else 'normal',fill=color))


def add_evidence_section(svg: svgwrite.Drawing, region: Box, *, key: str,
                         heading: str, caption: str, interpretation: str,
                         values: Sequence[BarDatum],
                         theme: SectionTheme=SectionTheme(),
                         measurer: PangoMeasurer | None=None) -> dict:
    """Draw an editable, grouped SVG results section and return registered bounds."""
    if not values or max(v.value for v in values) <= 0 or any(v.value < 0 for v in values):
        raise LayoutError('Chart requires nonnegative values and a positive maximum')
    m = measurer or PangoMeasurer()
    inner=Box(region.x+40,region.y+36,region.w-80,region.h-72)
    stack=VerticalStack(inner,gap=22)
    parts=[TextSpec('heading',heading,pt=38,min_pt=36,padding=8),
           FixedSpec('chart',300,260),
           TextSpec('caption',caption,pt=25,min_pt=23,padding=8),
           TextSpec('interpretation',interpretation,pt=27,min_pt=25,padding=8)]
    bounds=stack.allocate(parts,m)
    registry=ComponentRegistry(region)
    registry.add(Component(key,region,kind='panel'))
    g=svg.g(id=key)
    g.add(svg.rect(insert=(region.x,region.y),size=(region.w,region.h),rx=13,
                   fill='#FFFFFF',stroke='#D4DED8',stroke_width=2))
    entries={}
    for name,b in bounds.items():
        registry.add(Component(f'{key}-{name}',b,
                               kind='figure' if name=='chart' else 'text',parent=key))
        entries[name]=b.__dict__
    title_g=svg.g(id=f'{key}-heading')
    _draw_text_lines(svg,title_g,heading,bounds['heading'],38,theme.dark,True)
    title_g.add(svg.line(start=(bounds['heading'].x,
                                 bounds['heading'].y+bounds['heading'].h-3),
                         end=(bounds['heading'].x+bounds['heading'].w,
                              bounds['heading'].y+bounds['heading'].h-3),
                         stroke=theme.accent,stroke_width=2))
    g.add(title_g)
    fig=svg.g(id=f'{key}-figure')
    b=bounds['chart']
    chart_x=b.x+190; chart_w=b.w-300; n=len(values)
    row_h=min(68,(b.h-35)/n)
    vmax=max(d.value for d in values)
    for i,v in enumerate(values):
        yy=b.y+18+i*row_h
        fig.add(svg.text(v.label,insert=(b.x+8,yy+24),font_size=23,
                         font_family='Open Sans',fill=theme.ink))
        fig.add(svg.rect(insert=(chart_x,yy+4),size=(chart_w,30),fill='#ECF0EF'))
        fig.add(svg.rect(insert=(chart_x,yy+4),
                         size=(chart_w*v.value/vmax,30),fill=theme.accent))
        fig.add(svg.text(f'{v.value:g}',insert=(chart_x+chart_w+15,yy+28),
                         font_size=22,font_family='Open Sans',fill=theme.ink))
    g.add(fig)
    cap=svg.g(id=f'{key}-caption')
    _draw_text_lines(svg,cap,caption,bounds['caption'],25,theme.muted)
    g.add(cap)
    desc=svg.g(id=f'{key}-interpretation')
    _draw_text_lines(svg,desc,interpretation,bounds['interpretation'],27,theme.ink)
    g.add(desc)
    report=registry.assert_valid()
    svg.add(g)
    return {'report':report,'bounds':entries,'section':key}


def demo(out: str | Path='output/evidence-section.svg') -> dict:
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    svg=svgwrite.Drawing(str(out),size=('20in','12in'),viewBox='0 0 1440 864')
    svg.add(svg.rect(insert=(0,0),size=(1440,864),fill='#F7F5F1'))
    region=Box(55,55,1330,750)
    meta=add_evidence_section(svg,region,key='example-evidence',
        heading='Example: evidence-led results section',
        caption='Illustrative counts only (synthetic; not study data).',
        interpretation='Quantitative findings should be explained with\ndenominators, uncertainty, and a faithful takeaway.',
        values=[BarDatum('Group A',8),BarDatum('Group B',12),BarDatum('Group C',5)])
    svg.save()
    out.with_suffix('.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
    return meta

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='output/evidence-section.svg')
    args=parser.parse_args()
    print(json.dumps(demo(args.out)['report'],indent=2))
