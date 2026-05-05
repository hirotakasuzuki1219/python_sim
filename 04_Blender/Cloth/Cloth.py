import bpy
import os

# --- 1. 保存パスの設定 ---
if bpy.data.filepath:
    base_dir = os.path.dirname(bpy.data.filepath)
else:
    base_dir = os.path.join(os.path.expanduser("~"), "Desktop")

save_dir = os.path.join(base_dir, "movie")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

output_path = os.path.join(save_dir, "blender_cloth_sim.mp4")

# --- 2. シーンのリセット ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- 3. 布（Cloth）の作成 ---
bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 2.5))
plane = bpy.context.active_object
plane.name = "Cloth"

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=30)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

# クロスモディファイア
cloth_mod = plane.modifiers.new(name="Cloth", type='CLOTH')
s = cloth_mod.settings

# 物理精度の設定
s.quality = 20
s.mass = 0.5
s.tension_stiffness = 15.0
s.bending_stiffness = 5.0

# 衝突判定の詳細設定
c_s = cloth_mod.collision_settings
c_s.collision_quality = 10
c_s.distance_min = 0.015
c_s.use_self_collision = True
c_s.self_distance_min = 0.01

# ピン止め（上端固定）
vg = plane.vertex_groups.new(name="PinGroup")
pin_indices = [v.index for v in plane.data.vertices if v.co.y > 1.95]
vg.add(pin_indices, 1.0, 'REPLACE')
s.vertex_group_mass = "PinGroup"

# --- 4. 衝突体（Sphere）の作成 ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0, 0, 0))
sphere = bpy.context.active_object
sphere.name = "CollisionSphere"
sphere.modifiers.new(name="Collision", type='COLLISION')
sphere.modifiers["Collision"].settings.thickness_outer = 0.04

# --- 5. 撮影環境 ---
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.ops.object.camera_add(location=(8, -8, 6), rotation=(1.1, 0, 0.78))
bpy.context.scene.camera = bpy.context.active_object

# --- 6. 物理演算のベイク（最新のBlender 4.x方式） ---
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 90

print("物理演算をベイク中...")
bpy.context.view_layer.update()

# 【ここが修正ポイント】Blender 4.0以降のコンテキスト・オーバーライド
with bpy.context.temp_override(
    scene=scene, 
    active_object=plane, 
    point_cache=cloth_mod.point_cache
):
    bpy.ops.ptcache.bake(bake=True)

# --- 7. レンダリング ---
scene.render.filepath = output_path
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'

print(f"レンダリング開始: {output_path}")
bpy.ops.render.render(animation=True)
print("完了しました！")