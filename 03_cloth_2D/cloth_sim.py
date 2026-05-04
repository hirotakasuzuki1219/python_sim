import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- 1. シミュレーション設定 ---
duration_sec = 6.0
fps = 30
total_frames = int(duration_sec * fps)
output_filename = "gif/cloth_sim.gif"

# --- 2. 物理パラメータ（リポジトリの他コードと整合） ---
dt = 0.004
k_struct = 800.0  # 隣接する点同士のバネ定数（構造維持）
k_bend = 50.0    # 1つ飛ばしの点同士のバネ定数（曲げ抵抗）
c = 15.0          # 減衰係数（ボヨンボヨン抑制）
g = 9.8
m = 0.5           # 各頂点の質量
num_nodes = 25 
rest_len = 0.18 

# --- 3. 衝突体（テーブル）の設定 ---
table_center = np.array([2.5, 0.0])
table_radius = 1.2

# --- 4. 初期化 ---
# 落下開始位置（y=2.5、テーブルの真上付近に配置）
nodes = []
start_x = table_center[0] - (num_nodes * rest_len) / 2
for i in range(num_nodes):
    nodes.append([start_x + i * rest_len, 2.5])
nodes = np.array(nodes)
velocities = np.zeros_like(nodes)

# バネ接続リスト (点i, 点j, 自然長, 硬さ)
edges = []
for i in range(num_nodes):
    # 【構造バネ】隣り合う点
    if i < num_nodes - 1:
        edges.append((i, i + 1, rest_len, k_struct))
    # 【曲げバネ】1つ飛ばしの点（これによって角度変化に抵抗が生まれる）
    if i < num_nodes - 2:
        edges.append((i, i + 2, rest_len * 2, k_bend))

# --- 5. メインループ ---
def update(frame):
    global nodes, velocities
    # 精度と安定性のためのサブステップ
    for _ in range(5):
        forces = np.zeros_like(nodes)
        
        # A. 内部バネの力計算（構造＋曲げ）
        for i, j, r_len, k_val in edges:
            diff = nodes[j] - nodes[i]
            dist = np.linalg.norm(diff)
            if dist < 1e-6: continue
            unit_vec = diff / dist
            
            f_spring = k_val * (dist - r_len) * unit_vec
            f_damping = c * np.dot(velocities[j] - velocities[i], unit_vec) * unit_vec
            
            forces[i] += f_spring + f_damping
            forces[j] -= f_spring + f_damping

        # B. 外力（重力）と衝突判定（テーブル）
        for i in range(len(nodes)):
            forces[i] += np.array([0, -m * g])
            
            dist_to_center = np.linalg.norm(nodes[i] - table_center)
            if dist_to_center < table_radius:
                normal_vec = (nodes[i] - table_center) / dist_to_center
                overlap = table_radius - dist_to_center
                
                # 地面反発力（ペナルティ法）
                f_repel = 5000 * overlap * normal_vec
                # 速度に比例する抵抗力（恣意性を排除した摩擦・減衰）
                f_friction_v = -50.0 * np.dot(velocities[i], normal_vec) * normal_vec
                tangent_vec = np.array([-normal_vec[1], normal_vec[0]])
                f_friction_h = -20.0 * np.dot(velocities[i], tangent_vec) * tangent_vec
                
                forces[i] += f_repel + f_friction_v + f_friction_h

        # C. 積分（速度と位置の更新）
        velocities += (forces / m) * dt
        nodes += velocities * dt

    # --- 6. 描画処理 ---
    ax.clear()
    ax.set_xlim(-1, 6)
    ax.set_ylim(-1, 4)
    ax.set_aspect('equal')
    
    # テーブル（お皿/台）の描画
    theta = np.linspace(0, np.pi, 50)
    ax.plot(table_center[0] + table_radius * np.cos(theta), 
            table_center[1] + table_radius * np.sin(theta), color='black', lw=2)
    
    # 布の描画（線を太く設定）
    ax.plot(nodes[:,0], nodes[:,1], color='#8B4513', marker='o', markersize=3, lw=4)
    ax.set_title(f"Cloth Draping Sim (Bending Enabled): {frame/fps:.1f}s")

# --- 7. 保存 ---
fig, ax = plt.subplots(figsize=(8, 6))
print(f"レンダリング中: {output_filename}")
ani = FuncAnimation(fig, update, frames=total_frames)
ani.save(output_filename, writer=PillowWriter(fps=fps))
print("完了しました。")