"""Exploratory 18x12-inch font-aware SVG proof sheet. Run: uv run python experiments/layout_components.py"""
from pathlib import Path
import base64
import shutil
import subprocess
from xml.etree import ElementTree as ET

import svgwrite
from PIL import ImageFont
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
NAVY = "#16384C"

class Overflow(ValueError):
    pass

def measure(text, size, path=FONT):
    """Preliminary FreeType measurement, not full Pango text shaping."""
    return ImageFont.truetype(path, size).getlength(text)

def wrap(text, size, width):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
            candidate = (cur + " " + word).strip()
            if cur and measure(candidate, size) > width:
                lines.append(cur)
                cur = word
            else:
                cur = candidate
        lines.append(cur)
    return lines

class TextBlock:
    def __init__(self, text, width, height, size=22, minimum=20, padding=12):
        if size < minimum:
            raise Overflow("Font smaller than configured minimum")
        self.lines = wrap(text, size, width - 2*padding)
        self.size, self.padding = size, padding
        if len(self.lines)*size*1.30 + 2*padding > height:
            raise Overflow("Text exceeds allowed height")
        if max((measure(line,size) for line in self.lines), default=0) > width-2*padding:
            raise Overflow("Text exceeds allowed width")
    def draw(self, svg, group, x, y):
        for i,line in enumerate(self.lines):
            group.add(svg.text(line, insert=(x+self.padding,y+self.padding+self.size+i*self.size*1.3),
                font_family="DejaVu Sans", font_size=self.size, fill="#203747"))

class CodeListing:
    def __init__(self, source, language, width, height, size=19, minimum=18, padding=12):
        if size < minimum:
            raise Overflow("Code smaller than configured minimum")
        self.lines, self.language = source.rstrip("\n").split("\n"), language
        self.size, self.padding = size, padding
        mw = max((measure(x.expandtabs(4),size,MONO) for x in self.lines), default=0)+2*padding
        mh = len(self.lines)*size*1.45+2*padding
        if mw > width or mh > height:
            raise Overflow(f"{language} listing needs {mw:.0f} x {mh:.0f} pt, available {width} x {height} pt")
    def draw(self, svg, group, x, y):
        lexer = get_lexer_by_name(self.language)
        colors = [(Token.Comment,"#6D747A"),(Token.String,"#A55000"),
                  (Token.Keyword,"#005B9F"),(Token.Name.Function,"#226C43"),
                  (Token.Number,"#7A4BB1")]
        for i,line in enumerate(self.lines):
            xx,yy=x+self.padding,y+self.padding+self.size+i*self.size*1.45
            # Draw tokens at explicitly measured x coordinates: whitespace and
            # indentation cannot collapse across SVG tspan boundaries.
            for token,chunk in lex(line,lexer):
                chunk=chunk.rstrip("\n")
                if not chunk: continue
                col=next((c for t,c in colors if token in t),"#203747")
                group.add(svg.text(chunk,insert=(xx,yy),font_family="DejaVu Sans Mono",
                    font_size=self.size, fill=col,style="white-space:pre"))
                xx += measure(chunk.expandtabs(4),self.size,MONO)

class LatexEquation:
    def __init__(self, tex, width, height):
        self.tex, self.width, self.height = tex,width,height
    def draw(self, svg, group, x, y, name="risk_ratio"):
        latex=OUT/"latex"
        latex.mkdir(exist_ok=True)
        texfile=latex/(name+".tex")
        texfile.write_text(r"\documentclass[border=8pt]{standalone}"+"\n"+
            r"\usepackage{amsmath,amssymb}"+"\n"+r"\begin{document}"+"\n"+
            r"\begin{minipage}{7cm}\centering\Large" +"\n"+
            r"\["+self.tex+r"\]"+"\n"+r"\end{minipage}"+"\n"+
            r"\end{document}"+"\n",encoding="utf-8")
        subprocess.run(["pdflatex","-interaction=nonstopmode","-halt-on-error",
            "-output-directory",str(latex),str(texfile)],check=True,stdout=subprocess.DEVNULL)
        vector=latex/(name+".svg")
        subprocess.run(["pdftocairo","-svg",str(latex/(name+".pdf")),str(vector)],check=True)
        dims=ET.parse(vector).getroot().attrib["viewBox"].split()
        sw,sh=float(dims[2]),float(dims[3])
        scale=min(self.width/sw,self.height/sh)
        w,h=sw*scale,sh*scale
        data="data:image/svg+xml;base64,"+base64.b64encode(vector.read_bytes()).decode()
        group.add(svg.image(href=data,insert=(x+(self.width-w)/2,y+(self.height-h)/2),size=(w,h)))

def main():
    d=svgwrite.Drawing(str(OUT/"layout-components.svg"),size=("18in","12in"),
        viewBox="0 0 1296 864")
    d.add(d.rect(insert=(0,0),size=(1296,864),fill="white"))
    d.add(d.rect(insert=(0,0),size=(1296,110),fill=NAVY))
    d.add(d.text("Measured SVG components",insert=(42,58),font_family="DejaVu Sans",
        font_size=36,font_weight="bold",fill="white"))
    d.add(d.text("TextBlock | CodeListing | LatexEquation",
        insert=(42,90),font_family="DejaVu Sans",font_size=18,fill="white"))
    def card(x,y,w,h,title):
        g=d.g()
        g.add(d.rect(insert=(x,y),size=(w,h),rx=9,fill="#F8FAFB",stroke="#D5DEE3"))
        g.add(d.text(title,insert=(x+18,y+37),font_family="DejaVu Sans",
            font_size=23,font_weight="bold",fill=NAVY))
        d.add(g)
        return g
    g=card(42,144,575,245,"TextBlock: measured and wrapped")
    text=("Evidence-driven clinical decision support combines structured knowledge "
          "artifacts with patient-specific data. This experiment detects text "
          "overflow before authoring the SVG.")
    TextBlock(text,539,174).draw(d,g,50,201)
    g=card(642,144,612,245,"CodeListing: Python")
    py=("def risk_ratio(events_a, n_a, events_b, n_b):\n"
        "    # crude comparative risk\n"
        "    return (events_a / n_a) / (events_b / n_b)")
    CodeListing(py,"python",574,160).draw(d,g,650,201)
    g=card(42,417,575,325,"CodeListing: R")
    r=('library(dplyr)\ncohort |>\n'
       '  filter(age >= 65, exposure == "CBD") |>\n'
       '  summarise(n = n())')
    CodeListing(r,"r",538,232,size=18).draw(d,g,50,482)
    g=card(642,417,612,325,"LaTeX equation: source preserved")
    LatexEquation(r"\widehat{RR}=\frac{\Pr(Y=1\mid A=1)}{\Pr(Y=1\mid A=0)}",
        550,212).draw(d,g,665,490)
    try:
        CodeListing("SELECT a_very_long_column_identifier_that_does_not_fit FROM cohort;",
                    "sql",175,90,size=24,minimum=22)
    except Overflow as e:
        message="Preflight PASS: overlong SQL rejected — "+str(e)
    else:
        raise AssertionError("Expected overflow warning")
    d.add(d.text("Preflight PASS: undersized container rejected",
        insert=(42,813),font_family="DejaVu Sans",font_size=17,fill="#1D732B"))
    d.save()
    if shutil.which("inkscape"):
        for ext,args in (("pdf",[]),("png",["--export-width=2200"])):
            subprocess.run(["inkscape",str(OUT/"layout-components.svg"),
                *args,"--export-filename="+str(OUT/("layout-components."+ext))],check=True)
    (OUT/"layout-preflight.txt").write_text(message+"\n",encoding="utf-8")
    print(message)

if __name__=="__main__":
    main()
