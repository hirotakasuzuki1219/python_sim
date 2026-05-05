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

output_path = os.path.join(save_dir, "blender_softbody_sim.mp4")

# --- 2. シーンのリセット ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- 3. ソフトボディ本体（Cube）の作成 ---
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 4))
obj = bpy.context.active_object
obj.name = "SoftBody_Cube"

# メッシュの細分化（物理演算のために頂点を増やす）
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=5)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.shade_smooth()

# ソフトボディモディファイアの追加
sb_mod = obj.modifiers.new(name="SoftBody", type='SOFT_BODY')
s = sb_mod.settings

# 【重要設定】プリンのような挙動にするためのパラメータ
s.friction = 0.5            # 摩擦
s.mass = 1.0                # 質量
s.use_goal = False          # ゴール（形状維持）をオフにする（自由に落下させるため）
s.use_self_collision = True # 自己衝突（めり込み防止）

# 弾力の設定（Edges）
s.pull = 0.5                # 引っ張りへの耐性
s.push = 0.5                # 押し込みへの耐性（ここを下げると潰れやすくなる）
s.bend = 10.0               # 曲げ抵抗（自作コードでのk_bendに相当）

# --- 4. 衝突用の床（Floor）の作成 ---
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor.modifiers.new(name="Collision", type='COLLISION')

# --- 5. 撮影環境 ---
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.ops.object.camera_add(location=(10, -10, 8), rotation=(1.1, 0, 0.78))
bpy.context.scene.camera = bpy.context.active_object

# --- 6. 物理演算のベイク（4.x方式） ---
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120

print("ソフトボディ演算をベイク中...")
bpy.context.view_layer.update()

with bpy.context.temp_override(
    scene=scene, 
    active_object=obj, 
    point_cache=sb_mod.point_cache
):
    bpy.ops.ptcache.bake(bake=True)

# --- 7. レンダリング設定（mp4） ---
scene.render.filepath = output_path
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'

print(f"レンダリング開始: {output_path}")
bpy.ops.render.render(animation=True)
print("完了！")