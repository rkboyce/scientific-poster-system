"""Reference-inspired poster header with contrast/spacing improvements."""
from pathlib import Path
import argparse
from .layout import PosterCanvas,MeasuredText,Box,Overflow

def build(out):
    p=PosterCanvas()
    navy='#16384C';green='#6AC181'
    p.rectangle('header-background',Box(0,0,2592,410),navy)
    p.rectangle('takeaway-background',Box(35,455,825,1660),'#1D3E50')
    p.rectangle('takeaway-accent',Box(35,455,9,1660),green)
    data=[
        MeasuredText('title','Understanding Clinician Practices and Challenges in Managing\nCannabis–Drug Interactions: A Qualitative Interview Study',Box(110,25,2372,205),65,bold=True,min_pt=60),
        MeasuredText('authors','McKenna K. Anderson¹,²   ·   Kojo Abanyie²   ·   Sandra Kane-Gill¹,²   ·   Richard D. Boyce²',Box(95,244,2402,70),31,font='Lato',bold=True,min_pt=28),
        MeasuredText('affiliations','¹ School of Pharmacy   |   ² Department of Biomedical Informatics\nUniversity of Pittsburgh · Pittsburgh, Pennsylvania, USA',Box(110,315,2372,85),27,font='Lato',min_pt=24),
        MeasuredText('takeaway','Clinicians in community\nsettings lack adequate\ntools to manage potential\ncannabis–drug interactions',Box(77,520,738,410),44,bold=True,min_pt=40),
        MeasuredText('figure-title','Measured header and takeaway',Box(960,510,1500,150),58,color=navy,bold=True,min_pt=50),
        MeasuredText('explanation','Pango measures text before the SVG is built.\nEach block rejects overflow rather than shrinking.',Box(960,710,1460,190),32,color=navy,min_pt=28),
    ]
    for item in data:p.add_text(item,layer='header' if item.key in {'title','authors','affiliations'} else 'body')
    for idx,name in enumerate(['Scientific hierarchy','Edit-ready SVG groups','Preflight bounds']):
        x=955+idx%2*745;y=1035+(idx//2)*460
        p.rectangle('card-'+str(idx),Box(x,y,705,395),'#F3F1EA')
        p.add_text(MeasuredText('card-title-'+str(idx),name,Box(x+25,y+30,655,90),36,bold=True,color=navy,min_pt=32))
    return p.save(out,out.with_suffix('.json'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='output/header-layout.svg');args=ap.parse_args()
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    report=build(path)
    print('Preflight:', 'PASS' if report['ok'] else 'FAIL',len(report['components']),'text components')
    print('Output:',path)
if __name__=='__main__':main()
