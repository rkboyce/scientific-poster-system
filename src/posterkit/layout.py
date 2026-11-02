"""Linux Pango-backed measured text and simple collision-aware SVG compositor."""
from __future__ import annotations
import ctypes as C
from dataclasses import dataclass
from pathlib import Path
import json
import svgwrite

class LayoutError(ValueError): pass
class Overflow(LayoutError): pass

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float
    def intersects(self, other: 'Box', eps: float=0.2) -> bool:
        return (self.x < other.x + other.w - eps and self.x + self.w > other.x + eps and
                self.y < other.y + other.h - eps and self.y + self.h > other.y + eps)
    def inside(self, canvas: 'Box') -> bool:
        return self.x >= canvas.x and self.y >= canvas.y and self.x+self.w <= canvas.x+canvas.w and self.y+self.h <= canvas.y+canvas.h

class PangoMeasurer:
    def __init__(self):
        self.p=C.CDLL('libpango-1.0.so.0'); self.pc=C.CDLL('libpangocairo-1.0.so.0'); self.g=C.CDLL('libgobject-2.0.so.0')
        p,pc,g=self.p,self.pc,self.g
        pc.pango_cairo_font_map_get_default.restype=C.c_void_p
        p.pango_font_map_create_context.argtypes=[C.c_void_p];p.pango_font_map_create_context.restype=C.c_void_p
        p.pango_layout_new.argtypes=[C.c_void_p];p.pango_layout_new.restype=C.c_void_p
        p.pango_font_description_from_string.argtypes=[C.c_char_p];p.pango_font_description_from_string.restype=C.c_void_p
        p.pango_font_description_set_absolute_size.argtypes=[C.c_void_p,C.c_double]
        p.pango_layout_set_font_description.argtypes=[C.c_void_p,C.c_void_p]
        p.pango_layout_set_text.argtypes=[C.c_void_p,C.c_char_p,C.c_int]
        p.pango_layout_set_width.argtypes=[C.c_void_p,C.c_int]
        p.pango_layout_set_wrap.argtypes=[C.c_void_p,C.c_int]
        p.pango_layout_get_pixel_size.argtypes=[C.c_void_p,C.POINTER(C.c_int),C.POINTER(C.c_int)]
        p.pango_layout_get_line_count.argtypes=[C.c_void_p];p.pango_layout_get_line_count.restype=C.c_int
        p.pango_font_description_free.argtypes=[C.c_void_p]
        g.g_object_unref.argtypes=[C.c_void_p]
    def measure(self,text:str,font:str='Open Sans',pt:float=32,width:float|None=None,bold:bool=False)->dict:
        p=self.p
        ctx=p.pango_font_map_create_context(self.pc.pango_cairo_font_map_get_default())
        lay=p.pango_layout_new(ctx)
        desc=p.pango_font_description_from_string((font+(' Bold' if bold else '')).encode())
        try:
            p.pango_font_description_set_absolute_size(desc,pt*96/72*1024)
            p.pango_layout_set_font_description(lay,desc)
            data=text.encode('utf-8');p.pango_layout_set_text(lay,data,len(data))
            if width is not None:
                p.pango_layout_set_width(lay,round(width*96/72*1024));p.pango_layout_set_wrap(lay,0)
            w,h=C.c_int(),C.c_int()
            p.pango_layout_get_pixel_size(lay,C.byref(w),C.byref(h))
            lines=p.pango_layout_get_line_count(lay)
            return {'width':w.value*72/96,'height':h.value*72/96,'lines':lines}
        finally:
            p.pango_font_description_free(desc);self.g.g_object_unref(lay);self.g.g_object_unref(ctx)

@dataclass(frozen=True)
class MeasuredText:
    key: str
    value: str
    bounds: Box
    pt: float
    font: str = 'Open Sans'
    bold: bool = False
    color: str = '#FFFFFF'
    align: str = 'center'
    min_pt: float = 20
    line_factor: float = 1.22
    def validate(self,m:PangoMeasurer)->dict:
        if self.pt < self.min_pt:raise Overflow(f'{self.key}: {self.pt}pt below minimum {self.min_pt}pt')
        raw=self.value.split('\n')
        widths=[m.measure(line,self.font,self.pt,None,self.bold)['width'] for line in raw]
        if any(w>self.bounds.w for w in widths):raise Overflow(f'{self.key}: line width {max(widths):.1f} exceeds {self.bounds.w:.1f}pt')
        measured=m.measure(self.value,self.font,self.pt,self.bounds.w,self.bold)
        if measured['lines']!=len(raw):raise Overflow(f'{self.key}: Pango reports unexpected wrap: {measured["lines"]} vs {len(raw)}')
        required=max(measured['height'],len(raw)*self.pt*self.line_factor)
        if required>self.bounds.h:raise Overflow(f'{self.key}: height {required:.1f} exceeds {self.bounds.h:.1f}pt')
        return {**measured,'needed_height':required,'key':self.key,'pt':self.pt}
    def draw(self,d:svgwrite.Drawing,group,measurer:PangoMeasurer):
        measurements=self.validate(measurer)
        x,y,w,h=self.bounds.x,self.bounds.y,self.bounds.w,self.bounds.h
        lines=self.value.split('\n');lineh=self.pt*self.line_factor
        top=y+(h-lenh(lines,lineh))/2
        if self.align=='center':xx=x+w/2;anchor='middle'
        elif self.align=='right':xx=x+w;anchor='end'
        else:xx=x;anchor='start'
        for i,line in enumerate(lines):
            group.add(d.text(line,insert=(xx,top+(i+.82)*lineh),text_anchor=anchor,
                font_family=self.font,font_size=self.pt,font_weight='bold' if self.bold else 'normal',fill=self.color))
        return measurements

def lenh(lines,lineh):return len(lines)*lineh

class PosterCanvas:
    def __init__(self,width_in=36,height_in=48):
        self.width=width_in*72;self.height=height_in*72
        self.d=svgwrite.Drawing(size=(f'{width_in}in',f'{height_in}in'),viewBox=f'0 0 {self.width} {self.height}')
        self.m=PangoMeasurer();self.entries=[];self.d.add(self.d.rect(insert=(0,0),size=(self.width,self.height),fill='white'))
    def rectangle(self,key,box,fill,stroke=None):
        g=self.d.g(id=key);g.add(self.d.rect(insert=(box.x,box.y),size=(box.w,box.h),fill=fill,stroke=stroke or 'none'));self.d.add(g)
    def add_text(self,text:MeasuredText,layer='content'):
        group=self.d.g(id=text.key,**{'class':f'poster-component {layer}'})
        meta=text.draw(self.d,group,self.m);self.d.add(group)
        self.entries.append({'key':text.key,'bounds':text.bounds.__dict__,'measure':meta,'layer':layer})
    def preflight(self,allowed_overlaps=()):
        errors=[];canvas=Box(0,0,self.width,self.height)
        for e in self.entries:
            box=Box(**e['bounds'])
            if not box.inside(canvas):errors.append('outside canvas: '+e['key'])
        for i,a in enumerate(self.entries):
            for b in self.entries[i+1:]:
                pair=frozenset((a['key'],b['key']))
                if pair not in allowed_overlaps and Box(**a['bounds']).intersects(Box(**b['bounds'])):
                    errors.append(f'overlap: {a["key"]} / {b["key"]}')
        return {'ok':not errors,'errors':errors,'components':self.entries,'canvas':{'width_pt':self.width,'height_pt':self.height}}
    def save(self,path,report_path=None):
        pre=self.preflight()
        if not pre['ok']:raise LayoutError('; '.join(pre['errors']))
        self.d.saveas(str(path))
        if report_path:Path(report_path).write_text(json.dumps(pre,indent=2))
        return pre
