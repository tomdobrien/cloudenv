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
# Model coordinates are millimetres. The front is negative Y.
# Image-space outlines refer to the approved 1199 x 1312 gray concept.
def profile(poly,front,back):
    if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))<0:poly=list(reversed(poly))
    return m.CrossSection([poly]).extrude(back-front).rotate((90,0,0)).translate((0,back,0))
def trace(poly,front,back):
    return profile([((x-580)*.18,(1270-y)*.175) for x,y in poly],front,back)
def patch(poly,front,back):
    solid=trace(poly,front,back)
    if min(y for x,y in poly)>775:
        solid=solid.transform([[1,0,0,0],[0,1,.20,-9],[0,0,1,0]])
    add(solid)
# Wide plinth and deep inset-looking dialogue panel.
add(box(0,0,20,190,100,40))
add(box(0,-50.7,20,180,2,33))
for x in [-89,89]:add(box(x,-52,20,1.5,1.4,32))
for z in [4.5,35.5]:add(box(0,-52,z,179,1.4,1.5))
# Shoulders follow the approved silhouette; depth tapers toward the neck.
add(rings([(39,85,-38,34),(60,83,-37,33),(71,65,-27,30),(82,34,-19,24)]))
add(rings([(76,27,-12,23),(105,26,-15,24),(124,27,-17,25)]))
# Tall SeeD uniform collar, with thick stepped upper trim.
patch([(346,736),(407,746),(407,798),(379,805),(379,833),(337,825)],-39,-10)
patch([(606,758),(698,735),(701,713),(837,695),(837,810),(739,837),(739,849),(608,865)],-37,-7)
patch([(343,730),(407,742),(407,757),(344,746)],-41,-12)
patch([(606,756),(700,731),(700,709),(837,690),(837,707),(715,724),(715,746),(606,772)],-39,-8)
# Center opening, placket and shoulder trim are shallow solid relief.
patch([(475,811),(512,815),(512,852),(533,852),(533,977),(499,977),(499,881),(475,881)],-39,-17)
patch([(153,901),(219,883),(219,868),(284,854),(284,870),(233,884),(233,899),(153,919)],-39,-10)
patch([(809,884),(902,861),(1035,848),(1035,867),(914,880),(914,897),(809,914)],-38,-6)
# Blocky ceremonial chest emblems, tracing the chunky approved design.
patch([(295,843),(355,832),(355,852),(334,852),(334,879),(308,879),(308,905),(287,905),(287,946),(264,946),(264,921),(240,921),(240,894),(271,894),(271,867),(295,867)],-40,-20)
patch([(710,786),(746,781),(746,814),(722,814),(722,846),(744,846),(744,877),(716,877),(716,855),(691,855),(691,883),(665,883),(665,914),(690,914),(690,943),(664,943),(664,964),(635,964),(635,935),(608,935),(608,906),(583,906),(583,880),(611,880),(611,852),(648,852),(648,825),(684,825),(684,805),(710,805)],-39,-15)
# Large asymmetric head, deliberately flat across the face, with faceted cheeks.
def make_head():
    specs=[(97,20,-25,17),(103,29,-32,22),(114,39,-37,28),(132,46,-38,31),
           (151,47,-38,33),(174,44,-35,32),(190,33,-24,29),(199,20,-11,22)]
    vertices=[]
    for z,w,f,b in specs:
        center=-9
        vertices.extend([(center-w*.70,f,z),(center+w*.45,f,z),(center+w*.83,f+8,z),
         (center+w,f+22,z),(center+w*.93,b-8,z),(center+w*.5,b,z),
         (center-w*.5,b,z),(center-w*.94,b-8,z),(center-w,f+16,z),(center-w*.88,f+4,z)])
    faces=[]
    for j in range(len(specs)-1):
        for i in range(10):
            a=j*10+i;b=j*10+(i+1)%10;c=(j+1)*10+(i+1)%10;d=(j+1)*10+i
            faces.extend([(a,b,c),(a,c,d)])
    for i in range(1,9):faces.extend([(0,i+1,i),(70,70+i,70+i+1)])
    mesh=tm.Trimesh(vertices,faces,process=True);mesh.fix_normals()
    return m.Manifold(m.Mesh(np.array(mesh.vertices,np.float32),np.array(mesh.faces,np.uint32)))
head=make_head()
# Square pixel eyes and the small block mouth are shallow recesses, not paint.
for poly in [[(348,421),(428,421),(428,445),(347,445)],[(492,424),(563,424),(563,447),(492,447)],
             [(438,602),(532,602),(532,628),(438,628)],[(440,549),(487,549),(487,568),(440,568)]]:
    head=head-trace(poly,-43,-34.5)
add(head)
# Inset pupils with a broad flat upper eyelid.
for px in [388,524]:
    add(box((px-580)*.18,-35.8,(1270-436)*.175,4.5,3.2,3.8))
patch([(341,400),(424,400),(424,420),(341,420)],-39.5,-33)
patch([(494,406),(566,406),(566,424),(494,424)],-39.5,-33)
# A tiny two-step nose projects above the pixel nostril.
patch([(461,468),(484,468),(484,514),(498,514),(498,537),(447,537),(447,521),(461,521)],-40,-33)
# Face pixel steps are low-relief surface facets, not decorative surface texture.
patch([(338,479),(359,479),(359,520),(379,520),(379,545),(402,545),(402,573),(424,573),(424,596),(405,596),(405,582),(383,582),(383,553),(360,553),(360,527),(338,527)],-36.2,-31)
# Visible right ear, recessed stepped inner ear.
ear=trace([(785,456),(831,453),(848,473),(848,526),(825,553),(783,553),(770,526),(770,478)],-4,17)
ear=ear-trace([(799,478),(827,478),(827,509),(813,509),(813,533),(797,533),(797,513),(786,513),(786,493),(799,493)],-6,3)
add(ear)
# Rear scalp: enough round depth to be a complete bust from every side.
add(rings([(163,51,-9,34),(184,62,-13,42),(202,47,-8,36),(214,25,0,24)]))
# Hair silhouette is traced in layers. Each layer has substantial overlap into
# the scalp/head so the print is a connected solid, with no dangling strands.
hair=[
# Back/top silhouette, with the large 3-4 mm steps from the concept.
([(245,201),(273,201),(273,150),(319,150),(319,103),(375,103),(375,52),(438,52),(438,10),(529,10),(529,39),(591,39),(591,65),(653,65),(653,93),(717,93),(717,122),(770,122),(770,164),(814,164),(814,202),(856,202),(856,253),(900,253),(900,299),(934,299),(934,360),(964,360),(964,443),(979,443),(979,507),(947,507),(947,472),(913,472),(913,448),(863,448),(863,408),(245,408)],-25,34),
# Left outer fringe silhouette extends down to jaw height.
([(273,163),(337,163),(337,237),(309,237),(309,298),(285,298),(285,362),(259,362),(259,424),(282,424),(282,485),(302,485),(302,556),(284,556),(284,610),(301,610),(301,684),(258,684),(258,623),(234,623),(234,555),(224,555),(224,490),(201,490),(201,410),(218,410),(218,342),(192,342),(192,278),(217,278),(217,222),(245,222),(245,190),(273,190)],-18,20),
# Crown ridge, behind the main sweep.
([(378,94),(442,94),(442,63),(513,63),(513,89),(577,89),(577,120),(641,120),(641,149),(706,149),(706,181),(760,181),(760,219),(815,219),(815,257),(861,257),(861,302),(899,302),(899,345),(930,345),(930,385),(888,385),(888,360),(844,360),(844,327),(790,327),(790,289),(736,289),(736,251),(675,251),(675,212),(612,212),(612,181),(549,181),(549,151),(486,151),(486,129),(378,129)],-35,24),
# Several distinct blunt, heavy vertical bangs.
([(330,197),(390,197),(390,258),(367,258),(367,321),(345,321),(345,383),(323,383),(323,432),(290,432),(290,367),(307,367),(307,302),(320,302),(320,245),(330,245)],-38,-5),
([(407,183),(449,183),(449,278),(460,278),(460,357),(474,357),(474,484),(431,484),(431,437),(414,437),(414,361),(403,361),(403,281),(390,281),(390,226),(407,226)],-43,-6),
([(514,257),(558,257),(558,339),(575,339),(575,424),(548,424),(548,387),(530,387),(530,337),(514,337)],-41,-3),
([(593,324),(640,324),(640,401),(662,401),(662,470),(651,470),(651,536),(623,536),(623,475),(607,475),(607,400),(593,400)],-45,4),
([(664,385),(700,385),(700,467),(683,467),(683,536),(665,536),(665,605),(649,605),(649,635),(626,635),(626,576),(642,576),(642,511),(652,511),(652,445),(664,445)],-43,13),
# Outside right bang, close to the ear.
([(736,385),(783,385),(783,452),(772,452),(772,516),(748,516),(748,565),(720,565),(720,510),(727,510),(727,449),(736,449)],-33,19),
# Principal diagonal sweep with the big stair-step edge from the approved bust.
([(376,118),(450,118),(450,143),(517,143),(517,177),(578,177),(578,208),(644,208),(644,239),(711,239),(711,271),(769,271),(769,307),(820,307),(820,344),(867,344),(867,379),(905,379),(905,410),(857,410),(857,388),(804,388),(804,361),(748,361),(748,335),(689,335),(689,307),(630,307),(630,277),(572,277),(572,245),(517,245),(517,218),(465,218),(465,189),(415,189),(415,161),(376,161)],-46,-8),
# Blunt sideburn behind the right ear.
([(814,550),(850,550),(850,601),(837,601),(837,655),(813,655),(813,610),(802,610),(802,577),(814,577)],2,27),
]
# Broad swept backing plane joins the layers without deep checkerboard gaps.
patch([(378,94),(442,63),(513,63),(653,120),(770,210),(899,345),
       (930,410),(857,410),(748,361),(630,307),(517,245),(415,189),(376,161)],-40,-3)
for poly,f,b in hair:
    if f == -35: f=-42
    patch(poly,f,b)
# Rear hair is faceted, not an open extruded plate.
for x,z,w in [(-51,149,16),(-32,145,20),(-12,142,22),(10,144,22),(30,151,20),(48,160,16)]:
    add(box(x,29,(z+184)/2,w,22,184-z))
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
text('You’re the best',27)
text('looking guy here',12)
print('Union',len(parts),'solids',flush=True)
solid=m.Manifold.batch_boolean(parts,m.OpType.Add)
assert solid.status()==m.Error.NoError,solid.status()
solid=solid.simplify(0.0001)
mesh=solid.to_mesh()
out=tm.Trimesh(np.asarray(mesh.vert_properties)[:,:3],np.asarray(mesh.tri_verts),process=True)
out.remove_unreferenced_vertices()
print('Mesh checks:',out.is_watertight,out.is_winding_consistent,out.volume,flush=True)
assert out.is_watertight and out.is_winding_consistent and out.volume>0
components=out.split(only_watertight=False)
# Fill tiny sealed internal pockets created where traced locks meet the scalp.
# Keep every positive-volume exterior; never silently drop detached features.
voids=[c for c in components if c.volume < 0]
assert all(abs(c.volume)<10 for c in voids)
components=[c for c in components if c.volume>0]
if voids: out=tm.util.concatenate(components)
print('Exterior components:',len(components),'filled tiny internal pockets:',len(voids),flush=True)
assert len(components)==1, [(c.volume,c.bounds.tolist()) for c in components]
ROOT.joinpath('models').mkdir(exist_ok=True)
out.export(ROOT/'models/squall_pixel_bust.stl')
report={'units':'mm','dimensions_xyz':out.extents.tolist(),'bounds':out.bounds.tolist(),'triangles':len(out.faces),'watertight':bool(out.is_watertight),'consistent_winding':bool(out.is_winding_consistent),'connected_components':len(components),'solid_volume_cm3':float(out.volume/1000),'letter_stroke_mm':1.4,'letter_height_mm':9.8,'text':'You’re the best looking guy here'}
(ROOT/'models/mesh_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
