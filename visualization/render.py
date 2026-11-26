"""Render two reward advantages over the transition-row cube."""

import math
import os
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path(os.environ.get("Q717_FONT_DIR", "/System/Library/Fonts/Supplemental"))
BG, PANEL, TEXT, MUTED, GRID = "#111a30", "#1e304b", "#f6f8ff", "#c7d5e9", "#526b8c"
VIOLET, TEAL, GOLD = "#c0b7ff", "#6df1ca", "#ffc487"
VERTICES = [(x,y,z) for x in (0,1) for y in (0,1) for z in (-1,2)]
EDGES = [(a,b) for i,a in enumerate(VERTICES) for b in VERTICES[i+1:]
         if sum(x!=y for x,y in zip(a,b))==1]
CASES = (
    (0, 0, "Deterministic endpoint", "p = 0: both prefer baseline.", "Advantages: −1 and −1"),
    (0, 8, "A mixed row reverses the order", "p = 2/5: opposite preferences.", "Advantages: −1/5 and +1/5"),
    (1, 0, "A boundary tie can differ", "p = 0: tie versus strict choice.", "Advantages: 0 and 1"),
)


def font(size, bold=False):
    return ImageFont.truetype(str(FONT_DIR / ("Arial Bold.ttf" if bold else "Arial.ttf")),size)


def value(mode, reward, p):
    if mode == 0:
        return (2+reward)*p-1
    return p if reward==0 else 1


def project(point, angle):
    p,q,a=point
    x,y,z=2*p-1,2*q-1,2*(a+1)/3-1
    u,v=math.cos(angle),math.sin(angle)
    return round(351+138*(u*x-v*y)),round(344+68*(v*x+u*y)-91*z)


def frame(index, angle):
    mode,period,title,note,values=CASES[index]
    p=period/20
    image=Image.new("RGB",(704,835),BG)
    draw=ImageDraw.Draw(image)
    draw.text((34,28),"One row can change order",font=font(48,True),fill=TEXT)
    draw.text((35,96),"Two rewards on one active row",font=font(33),fill=MUTED)
    draw.rounded_rectangle((30,151,674,578),radius=25,fill=PANEL)
    for a,b in EDGES:
        draw.line((project(a,angle),project(b,angle)),fill=GRID,width=3)
    for reward,colour,shade in ((0,VIOLET,"#595a86"),(1,TEAL,"#326d70")):
        a,b=value(mode,reward,0),value(mode,reward,1)
        plate=[project(q,angle) for q in ((0,.20,a),(1,.20,b),(1,.80,b),(0,.80,a))]
        draw.polygon(plate,fill=shade,outline=colour,width=2)
        draw.line((project((0,.52,a),angle),project((1,.52,b),angle)),fill=colour,width=4)
    a,b=[project((p,.52,value(mode,reward,p)),angle) for reward in range(2)]
    draw.line((a,b),fill=GOLD,width=4)
    for (x,y),colour,radius in ((b,TEAL,12),(a,VIOLET,8)):
        draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=colour,outline=BG,width=2)
    for x,colour,label in ((53,VIOLET,"Reward 1"),(258,TEAL,"Reward 2"),(461,GOLD,"Chosen p")):
        draw.rounded_rectangle((x,532,x+21,554),radius=4,fill=colour)
        draw.text((x+29,529),label,font=font(27,True),fill=TEXT)
    draw.text((34,608),title,font=font(40,True),fill=TEXT)
    draw.line(((35,670),(668,670)),fill=GRID,width=2)
    draw.text((36,691),note,font=font(33),fill=TEXT)
    draw.text((36,746),values,font=font(34,True),fill=TEXT)
    return image.quantize(colors=48,method=Image.Quantize.MEDIANCUT)


def main():
    frames,delays=[],[]
    for index in range(3):
        for i in range(20):
            angle=.42+.17*math.sin(math.tau*i/20)
            frames.append(frame(index,angle))
            delays.append(300 if i==0 else 170)
    frames[0].save(HERE/"transition-reversals.gif",save_all=True,append_images=frames[1:],
                   duration=delays,disposal=1,loop=0,optimize=True)
    item=ZipInfo("index.html",(1980,1,1,0,0,0))
    item.create_system=3
    item.external_attr=0o100644<<16
    with ZipFile(HERE/"transition-reversals-explorer.zip","w") as archive:
        archive.writestr(item,(HERE/"index.html").read_bytes(),ZIP_DEFLATED,compresslevel=9)


if __name__=="__main__":
    main()
