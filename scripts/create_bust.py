"""Build a single connected Squall-inspired pixel bust. Units: millimetres."""
from pathlib import Path
import json
import numpy as np
import trimesh as tm
import manifold3d as m
ROOT=Path(__file__).resolve().parents[1]
parts=[]
def box(x,y,z,dx,dy,dz):
    return m.Manifold.cube((dx,dy,dz),center=True).translate((x,y,z))
def hull(points):
    mesh=tm.convex.convex_hull(np.array(points,float))
    return m.Manifold(m.Mesh(np.asarray(mesh.vertices,dtype=np.float32),np.asarray(mesh.faces,dtype=np.uint32)))
def rings(spec):
    pts=[]
    for z,w,front,back in spec:
        pts.extend([(-w*.70,front,z),(w*.70,front,z),(w,front+10,z),(w,back-10,z),(w*.7,back,z),(-w*.7,back,z),(-w,back-10,z),(-w,front+10,z)])
    return hull(pts)
def add(p):
    assert p.status()==m.Error.NoError, (len(parts),p.status())
    assert not p.is_empty(), len(parts)
    parts.append(p);return p
# Broad pedestal and framed PS1 dialogue plaque.
add(box(0,0,16,190,100,32))
add(box(0,-50.7,16,180,2,26))
for x in [-89,89]:add(box(x,-52,16,1.5,1.4,25))
for z in [4,28]:add(box(0,-52,z,179,1.4,1.5))
# Polygonal forms follow the PS1 portrait, with swept tapered hair rather
# than stacked cubes. X is horizontal, negative Y faces the viewer, Z is up.
def profile(poly, front, back):
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))<0: poly=list(reversed(poly))
    return m.CrossSection([poly]).extrude(back-front).rotate((90,0,0)).translate((0,back,0))
def ribbon(sections):
    """Faceted tapered lock with a shallow central ridge; connected segments."""
    solids=[]
    for a,b in zip(sections,sections[1:]):
        pts=[]
        for x,z,w,y,depth in (a,b):
            pts.extend([(x-w/2,y+2,z),(x,y-2,z),(x+w/2,y+2,z),
                        (x-w/2,y+depth,z),(x+w/2,y+depth,z)])
        solids.append(hull(pts))
    return m.Manifold.batch_boolean(solids,m.OpType.Add)
# Broader, higher shoulders; cropped ceremonial uniform with an angled collar.
add(rings([(31,86,-39,35),(48,86,-38,34),(69,68,-29,29),(84,33,-19,24)]))
add(rings([(67,23,-15,22),(111,23,-17,24),(127,26,-21,24)]))
for side in [-1,1]:
    poly=[(side*9,70),(side*34,77),(side*33,103),(side*10,96)]
    add(profile(poly,-27,-14))
    add(ribbon([(side*10,96,4,-29,6),(side*23,100,4,-27,6),(side*33,103,4,-25,6)]))
    # Trim follows the sloping shoulder instead of hanging ahead of it.
    add(profile([(side*39,61),(side*79,48),(side*83,44),(side*40,57)],-39,-18))
    # Small connected polygon insignia, intentionally coarse like the screenshot.
    poly=[(side*35,78),(side*32,72),(side*36,67),(side*43,64),(side*39,60),
          (side*43,55),(side*38,51),(side*32,56),(side*30,63),(side*25,67),
          (side*29,72),(side*29,79)]
    add(profile(poly,-35,-21))
add(profile([(-3,32),(1,32),(5,77),(1,80)],-40,-25))
# Head built from explicit cross-sections, retaining flat PS1-style cheek planes.
# No global convex hull: the inset temples and jaw remain distinct.
def head_mesh():
    specs=[(107,12,-23,12),(112,22,-30,19),(123,30,-34,25),
           (138,36,-35,29),(155,37,-35,30),(173,35,-33,30),
           (188,31,-28,28),(198,19,-15,21)]
    vertices=[]
    for z,w,f,b in specs:
        vertices.extend([(-w*.48,f,z),(w*.48,f,z),(w*.84,f+4,z),
         (w,f+16,z),(w*.92,b-7,z),(w*.5,b,z),(-w*.5,b,z),
         (-w*.92,b-7,z),(-w,f+16,z),(-w*.84,f+4,z)])
    faces=[]
    for j in range(len(specs)-1):
        for i in range(10):
            a=j*10+i;b=j*10+(i+1)%10;c=(j+1)*10+(i+1)%10;d=(j+1)*10+i
            faces.extend([(a,b,c),(a,c,d)])
    for i in range(1,9):faces.extend([(0,i+1,i),(70,70+i,70+i+1)])
    mesh=tm.Trimesh(vertices,faces,process=True);mesh.fix_normals()
    return m.Manifold(m.Mesh(np.array(mesh.vertices,np.float32),np.array(mesh.faces,np.uint32)))
head=head_mesh()
# Narrow slanted eyes and a small closed mouth: avoid rectangular robot sockets.
for side in [-1,1]:
    eye=[(side*8,155),(side*14,156),(side*26,154),(side*26,151),(side*17,150),(side*9,151)]
    head=head-profile(eye,-40,-32.7)
# Deliberately uneven closed-mouth line seen in the reference.
head=head-profile([(-12,125),(-5,126),(2,125.5),(10,126),(12,124),
                   (4,123),(-3,124),(-11,123.5)],-38,-32.4)
add(head)
# Angular eyelids, pupils at the back of the recess, restrained eyebrows.
for side in [-1,1]:
    add(profile([(side*8,157),(side*15,158),(side*27,156),(side*26,154),(side*15,156),(side*8,155)],-35.5,-30))
    add(box(side*17,-33,153,3.8,1.3,3.5))
# Small nose bridge and a short angular tip; no giant triangular nose.
add(hull([(-3,-34,155),(3,-34,155),(-4,-35,139),(4,-35,139),
          (-3,-40,137),(3,-40,137),(0,-42,139)]))
add(hull([(-6,-32,137),(6,-32,137),(-5,-39,135),(5,-39,135),(0,-41,137)]))
# Slight lower-lip plane and chin, both shallow enough to retain the crude face.
add(profile([(-9,121.5),(7,121.5),(9,120),(-7,119.5)],-35.5,-32))
for side in [-1,1]:
    ear=profile([(side*33,152),(side*42,155),(side*44,149),(side*42,136),(side*35,134)],-7,10)
    ear=ear-profile([(side*38,148),(side*41,149),(side*40,140),(side*38,139)],-9,-3)
    add(ear)
# Faceted scalp, asymmetric off-center peak and fuller swept right side.
add(rings([(171,37,-23,32),(190,44,-28,37),(205,35,-18,31),(216,13,-2,16)]))
# Low-poly back locks hug the head rather than forming a cubic helmet.
for x,top,bottom in [(-38,193,133),(-27,204,128),(-12,211,130),(6,211,126),(24,204,135),(37,192,142)]:
    add(ribbon([(x,top,19,18,15),(x*1.08,(top+bottom)/2,18,27,13),(x*1.02,bottom,7,23,11)]))
# Main swept masses traced from the crown down toward the right temple.
# Broad sloping bands are the most distinctive feature of the source silhouette.
for sections in [
 [(-12,211,23,-15,18),(2,205,28,-29,20),(21,195,28,-34,21),(37,182,23,-29,20),(48,169,7,-18,18)],
 [(-19,204,17,-24,16),(-1,196,24,-37,19),(17,187,24,-40,20),(34,175,16,-34,19),(45,162,4,-22,18)],
 [(-4,216,20,-7,18),(14,209,24,-19,19),(30,198,22,-22,19),(43,184,14,-18,17),(49,174,5,-9,16)],
 [(-24,204,16,-20,17),(-36,192,18,-27,19),(-45,175,15,-23,18),(-46,158,8,-13,18)],
 [(-33,188,16,-30,19),(-42,170,13,-28,18),(-44,149,9,-17,18),(-43,124,5,-6,16)],
]:add(ribbon(sections))
# A few long, pointed bangs, with open forehead visible between them.
for sections in [
 [(-12,204,13,-30,18),(-10,184,10,-37,17),(-8,164,7,-39,13),(-7,148,4,-38,10)],
 [(-24,196,12,-29,18),(-29,181,10,-36,17),(-30,164,5,-36,12)],
 [(3,193,12,-36,19),(8,178,10,-40,16),(10,164,4,-39,11)],
 [(23,184,14,-34,19),(29,163,10,-37,17),(26,142,6,-36,13),(25,125,3.5,-30,13)],
 [(39,176,11,-22,20),(41,158,8,-23,19),(39,144,4,-17,17)]
]:add(ribbon(sections))
# Original 5x7 pixel alphabet; thin strokes are 1.4mm wide and 1.2mm raised.
FONT={
'Y':['10001','10001','01010','00100','00100','00100','00100'],
'o':['00000','00000','01110','10001','10001','10001','01110'],
'u':['00000','00000','10001','10001','10001','10011','01101'],
'r':['00000','00000','10110','11001','10000','10000','10000'],
'e':['00000','00000','01110','10001','11111','10000','01110'],
'’':['00100','00100','01000','00000','00000','00000','00000'],
"'":['00100','00100','01000','00000','00000','00000','00000'],
' ':['000','000','000','000','000','000','000'],
't':['00100','00100','11111','00100','00100','00101','00010'],
'h':['10000','10000','10110','11001','10001','10001','10001'],
'b':['10000','10000','10110','11001','10001','10001','11110'],
's':['00000','00000','01111','10000','01110','00001','11110'],
'l':['01100','00100','00100','00100','00100','00100','01110'],
'k':['10000','10000','10010','10100','11000','10100','10010'],
'i':['001','000','011','001','001','001','111'],
'n':['00000','00000','10110','11001','10001','10001','10001'],
'g':['00000','01110','10001','10001','01111','00001','01110'],
'y':['00000','00000','10001','10001','01111','00001','01110']}
def text(line,z):
    pitch=1.4
    width=sum(len(FONT[c][0])+1 for c in line)-1
    x=-width*pitch/2
    for c in line:
        glyph=FONT[c]
        for row,bits in enumerate(glyph):
            for col,b in enumerate(bits):
                if b=='1':add(box(x+(col+.5)*pitch,-52.1,z+(3-row)*pitch,pitch+.015,1.6,pitch+.015))
        x+=(len(glyph[0])+1)*pitch
text('You’re the best',21.4)
text('looking guy here',10.2)
print('Union',len(parts),'solids',flush=True)
solid=m.Manifold.batch_boolean(parts,m.OpType.Add)
assert solid.status()==m.Error.NoError,solid.status()
mesh=solid.to_mesh()
out=tm.Trimesh(np.asarray(mesh.vert_properties)[:,:3],np.asarray(mesh.tri_verts),process=True)
out.remove_unreferenced_vertices()
assert out.is_watertight and out.is_winding_consistent and out.volume>0
components=out.split(only_watertight=False)
print('Components:',[(c.volume,c.bounds.tolist()) for c in components],flush=True)
assert len(components)==1, f'{len(components)} disconnected parts'
ROOT.joinpath('models').mkdir(exist_ok=True)
out.export(ROOT/'models/squall_pixel_bust.stl')
report={'units':'mm','dimensions_xyz':out.extents.tolist(),'bounds':out.bounds.tolist(),'triangles':len(out.faces),'watertight':bool(out.is_watertight),'consistent_winding':bool(out.is_winding_consistent),'connected_components':len(components),'solid_volume_cm3':float(out.volume/1000),'letter_stroke_mm':1.4,'letter_height_mm':9.8,'text':'You’re the best looking guy here'}
(ROOT/'models/mesh_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
