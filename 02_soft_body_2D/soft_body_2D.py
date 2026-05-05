import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# --- 設定：動画の長さ ---
duration_sec = 5.0  # 保存したい動画の秒数
fps = 30            # フレームレート
total_frames = int(duration_sec * fps)
output_filename = "gif/soft_body_simulation.gif"

# --- 物理パラメータ ---
dt = 0.005
k = 400.0   
c = 2.0     
g = 9.8
m = 0.5
rows, cols = 4, 4
rest_length = 0.8

# --- 初期化 ---
nodes = []
for r in range(rows):
    for c_idx in range(cols):
        nodes.append([c_idx * rest_length + r*0.1, r * rest_length + 3.0])
nodes = np.array(nodes)
velocities = np.zeros_like(nodes)

edges = []
for r in range(rows):
    for c_idx in range(cols):
        idx = r * cols + c_idx
        if c_idx < cols - 1: edges.append((idx, idx + 1))
        if r < rows - 1: edges.append((idx, idx + cols))
        if r < rows - 1 and c_idx < cols - 1:
            edges.append((idx, idx + cols + 1))
            edges.append((idx + 1, idx + cols))

# --- シミュレーションと描画関数 ---
fig, ax = plt.subplots(figsize=(5, 5))

def update(frame):
    global nodes, velocities
    # 物理計算を1フレームにつき数回回す（安定化のため）
    for _ in range(4):
        forces = np.zeros_like(nodes)
        for i, j in edges:
            diff = nodes[j] - nodes[i]
            dist = np.linalg.norm(diff)
            unit_vec = diff / dist
            r_len = rest_length if abs(i-j) == 1 or abs(i-j) == cols else rest_length * 1.414
            f_spring = k * (dist - r_len) * unit_vec
            f_damping = c * np.dot(velocities[j] - velocities[i], unit_vec) * unit_vec
            forces[i] += f_spring + f_damping
            forces[j] -= f_spring + f_damping

        for i in range(len(nodes)):
            forces[i] += np.array([0, -m * g])
            # if nodes[i, 1] < 0:
            #     forces[i, 1] += -1500 * nodes[i, 1]
            #     velocities[i] *= 0.6
            
            if nodes[i, 1] < 0:
                # 地面の反発（バネ）
                f_repel = -2000 * nodes[i, 1] 
                # 地面の抵抗（速度にブレーキ）
                f_friction = -25.0 * velocities[i, 1] 
                
                forces[i, 1] += f_repel + f_friction
                
                # 横方向の摩擦も入れるとよりリアル
                forces[i, 0] += -5.0 * velocities[i, 0]

        velocities += (forces / m) * dt
        nodes += velocities * dt

    ax.clear()
    ax.set_xlim(-1, 5)
    ax.set_ylim(-0.5, 6)
    for i, j in edges:
        ax.plot([nodes[i,0], nodes[j,0]], [nodes[i,1], nodes[j,1]], 'orange', alpha=0.6)
    ax.scatter(nodes[:,0], nodes[:,1], color='brown', s=30)
    ax.axhline(0, color='black', lw=2)
    ax.set_title(f"Softbody Sim: {frame/fps:.1f}s / {duration_sec}s")

# --- 保存処理 ---
print(f"シミュレーション開始... {output_filename} を作成中")
ani = FuncAnimation(fig, update, frames=total_frames, interval=1000/fps)
writer = PillowWriter(fps=fps)
ani.save(output_filename, writer=writer)
print(f"保存完了: {output_filename}")