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
def add(p): parts.append(p);return p
# Broad pedestal and framed PS1 dialogue plaque.
add(box(0,0,16,190,100,32))
add(box(0,-50.7,16,180,2,26))
for x in [-89,89]:add(box(x,-52,16,1.5,1.4,25))
for z in [4,28]:add(box(0,-52,z,179,1.4,1.5))
# Faceted cropped shoulders; neck reaches the jaw.
add(rings([(31,86,-39,35),(53,86,-38,34),(71,63,-30,29),(83,32,-23,24)]))
add(rings([(66,26,-18,23),(114,26,-20,24),(122,29,-23,25)]))
# Tall uniform collar, supported at the shoulder and neck.
for s in [-1,1]:
    add(hull([(s*13,-28,67),(s*36,-26,70),(s*36,-26,103),(s*13,-28,98),(s*13,-18,67),(s*36,-16,70),(s*36,-16,103),(s*13,-18,98)]))
    add(box(s*24.5,-27,100,25,3,4))
    # Flat shoulder braid, three stepped segments.
    for x,z in [(51,57),(66,53),(79,48)]:add(box(s*x,-30,z,17,19,4))
    # Chunky silver chest insignia fused onto jacket surface.
    for x,z in [(41,68),(37,63),(32,58),(37,53),(42,48)]:add(box(s*x,-37,z,10,8,7))
add(box(0,-38.8,51,4,3,40))
# Broad polygon face: flattened front, stepped chin and angular cheeks.
head=rings([(105,18,-22,22),(113,29,-30,27),(131,40,-35,31),(161,42,-35,34),(181,36,-31,32),(192,27,-24,27)])
# Square recessed eyes and mouth remain visible with a single filament.
for x in [-19,19]:head=head-box(x,-35.1,152,19,6,6)
head=head-box(0,-33.9,123,17,6,4.5)
add(head)
for x in [-19,19]:add(box(x,-33.2,152,5.5,2.2,5.2))
# Low-poly nose and blocky brow planes.
add(hull([(-5,-34,151),(5,-34,151),(-6,-34,136),(6,-34,136),(-4,-41,136),(4,-41,136)]))
for s in [-1,1]:add(box(s*19,-35,158,21,3,3))
for s in [-1,1]:add(box(s*42,0,143,12,22,24))
# Chunky stepped hair cap. Columns overlap, giving a robust connected shell.
for x in range(-48,49,8):
    for y in range(-24,33,8):
        q=(x/55)**2+((y-4)/47)**2
        if q<1:
            top=184+8*round(4.4*(1-q)**.5)
            add(box(x,y,(174+top)/2,8.2,8.2,top-174))
# Rear hair fills the back of the head with blunt stepped ends.
for x in range(-40,41,8):
    low=129+8*round(abs(x)/18)
    add(box(x,31,(low+190)/2,8.5,14,190-low))
# Layered bangs, carefully attached through their rear surfaces to head/cap.
# Each lock is a stair-stepped solid silhouette in the front view.
locks=[(-44,182,135,12),(-34,193,159,14),(-23,201,169,15),(-10,207,146,12),(3,209,174,15),(16,204,164,16),(29,197,133,13),(40,187,145,13),(49,174,158,12)]
for x,top,bottom,w in locks:
    # shallow side-to-side staircase across each chunky lock
    add(box(x,-32,(top+bottom)/2,w,18,top-bottom))
    add(box(x+3,-39,(top+bottom+6)/2,max(w-4,6),6,top-bottom-6))
# Big swept diagonal clumps layered over the bangs; no fine hair strands.
for x,z in [(6,207),(16,199),(26,191),(36,183),(46,175)]:
    add(box(x,-40,z,22,9,13))
for x,z in [(-15,202),(-26,194),(-36,184),(-46,174)]:
    add(box(x,-38,z,17,9,12))
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
