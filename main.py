import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 物理パラメータ ---
m = 1.0
k = 20.0
c = 0.3
g = 9.81
L0 = -2.0  # 自然長 (天井を0として下向きが負)

# つり合い位置
y_eq = L0 - (m * g / k)

# --- シミュレーション設定 ---
dt = 0.05
duration = 10.0
steps = int(duration / dt)
t_data = np.linspace(0, duration, steps)

y = L0 
v = 0.0
history_y = []

# シミュレーション（オイラー法）
for t in t_data:
    a = -g - (k / m) * (y - L0) - (c / m) * v
    v += a * dt
    y += v * dt
    history_y.append(y)

# --- 可視化の設定 ---
# グラフの高さを一致させるため、y軸の範囲を固定
y_min, y_max = min(history_y) - 0.7, 0.5

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

line_graph, = ax2.plot([], [], color='blue', lw=2)

def draw_spring(ax, y_end):
    """バネのギザギザ描画（端は直線）"""
    n_turns = 10
    width = 0.1
    top_margin = 0.2
    bot_margin = 0.2
    
    length = abs(y_end)
    # y座標の生成
    y_points = [0, -top_margin]
    x_points = [0, 0]
    
    mid_length = length - top_margin - bot_margin
    if mid_length > 0:
        for i in range(n_turns * 2):
            y_p = -top_margin - (mid_length * (i + 0.5) / (n_turns * 2))
            x_p = width if i % 2 == 0 else -width
            x_points.append(x_p)
            y_points.append(y_p)
            
    y_points.extend([y_end + bot_margin, y_end])
    x_points.extend([0, 0])
    return ax.plot(x_points, y_points, color='gray', lw=1.5)

def setup_axes():
    # アニメーション側
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(y_min, y_max)
    ax1.axhline(0, color='black', lw=3) # 天井
    ax1.axhline(y_eq, color='red', linestyle='--', alpha=0.4, label="Equilibrium")
    ax1.set_title("Physical Simulation")
    
    # グラフ側
    ax2.set_xlim(0, duration)
    ax2.set_ylim(y_min, y_max) # 左側と高さを合わせる
    ax2.axhline(y_eq, color='red', linestyle='--', alpha=0.4)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Position [m]")
    ax2.grid(True, alpha=0.3)

def update(i):
    ax1.clear()
    setup_axes()
    
    current_y = history_y[i]
    
    # 描画
    draw_spring(ax1, current_y)
    ax1.plot(0, current_y, 'ro', markersize=20)
    
    # グラフ更新
    line_graph.set_data(t_data[:i], history_y[:i])
    
    return line_graph,

# アニメーション実行
ani = FuncAnimation(fig, update, frames=steps, interval=50, blit=False, repeat=False)

# --- 保存と表示 ---
save_filename = "simulation.gif"
print(f"Saving to {save_filename}...")
try:
    # 保存。エラー回避のため plt.show() の前に実行
    ani.save(save_filename, writer='pillow', fps=20)
    print("Save completed.")
except Exception as e:
    print(f"Save failed: {e}")