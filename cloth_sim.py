import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- 設定 ---
duration_sec = 6.0
fps = 30
total_frames = int(duration_sec * fps)
output_filename = "cloth_on_table_wide.gif"

dt = 0.004
k = 600.0   
c = 50.0
g = 9.8
num_nodes = 25 
rest_len = 0.15 

# --- テーブルの設定 ---
table_center = np.array([2.5, 0.0])
table_radius = 1.2

# --- 初期化 ---
# 落下開始位置（y=2.5、中央付近）
nodes = []
start_x = table_center[0] - (num_nodes * rest_len) / 2
for i in range(num_nodes):
    nodes.append([start_x + i * rest_len, 2.5])
nodes = np.array(nodes)
velocities = np.zeros_like(nodes)

def update(frame):
    global nodes, velocities
    for _ in range(5):
        forces = np.zeros_like(nodes)
        for i in range(num_nodes - 1):
            p1, p2 = nodes[i], nodes[i+1]
            v1, v2 = velocities[i], velocities[i+1]
            diff = p2 - p1
            dist = np.linalg.norm(diff)
            unit_vec = diff / dist
            f_spring = k * (dist - rest_len) * unit_vec
            f_damping = c * np.dot(v2 - v1, unit_vec) * unit_vec
            forces[i] += f_spring + f_damping
            forces[i+1] -= f_spring + f_damping

        for i in range(len(nodes)):
            forces[i] += np.array([0, -0.8 * g])
            dist_to_center = np.linalg.norm(nodes[i] - table_center)
            if dist_to_center < table_radius:
                normal_vec = (nodes[i] - table_center) / dist_to_center
                overlap = table_radius - dist_to_center
                f_repel = 4000 * overlap * normal_vec
                f_friction_v = -50.0 * np.dot(velocities[i], normal_vec) * normal_vec
                tangent_vec = np.array([-normal_vec[1], normal_vec[0]])
                f_friction_h = -20.0 * np.dot(velocities[i], tangent_vec) * tangent_vec
                forces[i] += f_repel + f_friction_v + f_friction_h

        velocities += (forces / 0.5) * dt
        nodes += velocities * dt

    ax.clear()
    # 表示範囲を負の方向にも広げる
    ax.set_xlim(0, 5)   # 左側に余裕を持たせる
    ax.set_ylim(-2, 3)   # 下側にも余裕を持たせる
    
    # テーブル
    theta = np.linspace(0, np.pi, 50)
    ax.plot(table_center[0] + table_radius * np.cos(theta), 
            table_center[1] + table_radius * np.sin(theta), 'k-', lw=3)
    ax.fill_between(table_center[0] + table_radius * np.cos(theta), 
                    -1, table_center[1] + table_radius * np.sin(theta), color='lightgray', alpha=0.3)
    
    # 布
    ax.plot(nodes[:,0], nodes[:,1], color='#8B4513', marker='o', markersize=3, lw=2, label="Caramel Cloth")
    ax.set_title(f"Cloth Draping: {frame/fps:.1f}s")
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)

fig, ax = plt.subplots(figsize=(8, 6))
print("シミュレーション中...")
ani = FuncAnimation(fig, update, frames=total_frames)
ani.save(output_filename, writer=PillowWriter(fps=fps))
print(f"保存完了: {output_filename}")