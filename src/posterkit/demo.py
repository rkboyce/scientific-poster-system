"""Prototype scientific poster wireframe.

The demo is deliberately not a scientific poster: it is a layout/style test.
Replace text and figures after using finished posters to calibrate type sizes.
"""
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape
import argparse
import svgwrite

PT_PER_INCH = 72

@dataclass(frozen=True)
class Palette:
    navy: str = '#16384C'
    accent: str = '#1D732B'
    accent_light: str = '#6AC181'
    sand: str = '#EADDC5'
    muted: str = '#686758'
    paper: str = '#F9F8F5'
    white: str = '#FFFFFF'
    ink: str = '#203645'

@dataclass(frozen=True)
class Style:
    heading: str = 'Open Sans'
    body: str = 'Karla'
    display: str = 'Open Sans'
    title_pt: int = 66
    takeaway_pt: int = 62
    section_pt: int = 40
    body_pt: int = 31
    label_pt: int = 24
    foot_pt: int = 20

class Poster:
    def __init__(self, width_in=36, height_in=48, palette=Palette(), style=Style()):
        self.W = width_in * PT_PER_INCH
        self.H = height_in * PT_PER_INCH
        self.palette = palette
        self.style = style
        self.svg = svgwrite.Drawing(size=(f'{width_in}in', f'{height_in}in'),
                                    viewBox=f'0 0 {self.W} {self.H}', profile='full')
        self.rect(0, 0, self.W, self.H, palette.paper)

    def rect(self, x, y, w, h, fill, radius=0):
        self.svg.add(self.svg.rect(insert=(x,y), size=(w,h), rx=radius, ry=radius, fill=fill))

    def lines(self, x, y, text_lines, size, color, family, weight='normal', step=None,
              anchor='start'):
        if step is None:
            step = size * 1.27
        for i, line in enumerate(text_lines):
            self.svg.add(self.svg.text(line, insert=(x, y + i * step), font_size=size,
                     fill=color, font_family=family, font_weight=weight, text_anchor=anchor))

    def section(self, x, y, w, heading, lines, color=None):
        p = self.palette
        s = self.style
        self.lines(x, y, [heading], s.section_pt, p.navy, s.heading, 'bold')
        self.rect(x, y+24, w, 3, p.accent_light)
        self.lines(x, y+63, lines, s.body_pt, p.ink if color is None else color, s.body)

    def save(self, path):
        self.svg.saveas(str(path), pretty=True)


def create_example(out: Path, palette: Palette, style: Style):
    p = Poster(palette=palette, style=style)
    c = palette; f = style
    # All placement coordinates in points; poster nominally 2592 x 3456.
    p.rect(0, 0, 2592, 425, c.navy)
    p.lines(1296, 132,
        ['Working title of the scientific poster', 'Second line if needed'],
        f.title_pt, c.white, f.heading, 'bold', step=93, anchor='middle')
    p.lines(1296, 332, ['Authors | Affiliations'], 31, c.white, f.body, anchor='middle')
    # Left takeaway panel
    p.rect(36, 470, 760, 2510, c.navy)
    p.rect(36, 470, 12, 2510, c.accent_light)
    p.lines(96, 588,
        ['A memorable result', 'or conclusion that', 'can be read from', 'a distance'],
        f.takeaway_pt, c.white, f.display, 'bold', step=84)
    p.rect(96, 942, 640, 5, c.accent_light)
    p.lines(96, 1024, ['BACKGROUND'], 27, c.accent_light, f.heading, 'bold')
    p.lines(96, 1095, ['Short context line one', 'Short context line two'], 31, c.white, f.body, step=48)
    p.lines(96, 1370, ['OBJECTIVE'], 27, c.accent_light, f.heading, 'bold')
    p.lines(96, 1441, ['The study objective goes', 'here in readable prose'], 31, c.white, f.body, step=48)
    # Middle results
    p.section(838, 550, 1064, 'Primary scientific finding',
              ['Large figure or graphic goes here.'])
    p.rect(840, 760, 1062, 1000, c.white, radius=15)
    p.rect(880, 805, 982, 900, c.sand, radius=12)
    p.lines(1370, 1220, ['VECTOR FIGURE / CHART'], 39, c.navy, f.heading, 'bold', anchor='middle')
    p.section(838, 1922, 1064, 'Supporting evidence',
              ['Evidence is presented in this', 'second content block.'])
    p.rect(838, 2100, 1064, 800, c.white, radius=15)
    # Right methods and contextual findings
    p.section(1948, 550, 590, 'Methods',
              ['Brief study design', 'and sample details.'])
    p.rect(1948, 848, 590, 780, c.sand, radius=12)
    p.lines(1980, 931, ['METHODS / WORKFLOW'], 30, c.navy, f.heading, 'bold')
    p.section(1948, 1800, 590, 'Additional results',
              ['Interpretation or', 'supporting figure.'])
    p.rect(1948, 2090, 590, 810, c.white, radius=12)
    # full width implications/footer
    p.rect(36, 3008, 2520, 185, c.sand)
    p.lines(76, 3080, ['Interpretation and next steps'], 34, c.navy, f.heading, 'bold')
    p.lines(76, 3138, ['A concise statement of implications, limitations, and future work.'], 29, c.ink, f.body)
    p.lines(70, 3300, ['Logo | Funding'], 23, c.muted, f.body)
    p.lines(2520, 3300, ['References | QR'], 23, c.muted, f.body, anchor='end')
    p.save(out)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('output/poster-wireframe.svg'))
    parser.add_argument('--palette', choices=['navy-green','navy-orange'], default='navy-green')
    args=parser.parse_args()
    pal = Palette() if args.palette=='navy-green' else Palette(accent='#B6602B', accent_light='#DC9F67', sand='#F4E4CC')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    print(create_example(args.out, pal, Style()))

if __name__ == '__main__':
    main()
