"""Render the actual STL in Blender (run with blender -b -t 4 -P this_file)."""
import bpy, math
from mathutils import Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.wm.stl_import(filepath=str(ROOT/'models/squall_pixel_bust.stl'))
obj=bpy.context.object
mat=bpy.data.materials.new('Matte gray PLA');mat.diffuse_color=(.48,.50,.52,1);mat.use_nodes=True
mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.48,.50,.52,1)
mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.78
obj.data.materials.append(mat)
bpy.ops.mesh.primitive_plane_add(size=2000,location=(0,0,-.2))
floor=bpy.data.materials.new('Warm studio');floor.diffuse_color=(.25,.22,.20,1);bpy.context.object.data.materials.append(floor)
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(250,-700,310));cam=bpy.context.object;aim(cam,(0,0,110));cam.data.type='ORTHO';cam.data.ortho_scale=278;bpy.context.scene.camera=cam
for loc,power,size in [((-230,-350,440),4000000,260),((270,-80,230),1800000,220),((0,230,360),3000000,180)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;aim(o,(0,0,110))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=False;s.render.resolution_x=1100;s.render.resolution_y=1200;s.render.resolution_percentage=100
s.world.color=(.3,.3,.3);s.render.image_settings.file_format='PNG';s.render.filepath=str(ROOT/'models/actual_mesh_preview.png');bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'models/preview_scene.blend'));bpy.ops.render.render(write_still=True)
