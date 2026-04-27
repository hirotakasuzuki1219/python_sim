import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 物理パラメータ ---
m = 1.0      # 質量 [kg]
k = 20.0     # バネ定数 [N/m]
c = 0.3      # 減衰係数 [N s/m]
g = 9.81     # 重力加速度 [m/s^2]
L0 = -2.0    # 自然長（天井0から下向きなので負の値） [m]

# --- シミュレーション設定 ---
dt = 0.05
duration = 10.0  # 目標時間 [s]
steps = int(duration / dt)
t_data = np.linspace(0, duration, steps)

# 初期状態（上向き正：y軸）
y = L0       # 自然長の位置からスタート
v = 0.0      # 初期速度
history_y = []

# --- シミュレーション（オイラー法） ---
# 運動方程式: ma = -mg - k(y - L0) - cv
# ※ y, L0 ともに負の値。yがL0より小さければ（より伸びれば）上向きの復元力が発生する。
for t in t_data:
    a = -g - (k / m) * (y - L0) - (c / m) * v
    v += a * dt
    y += v * dt
    history_y.append(y)

# --- 可視化の設定 ---
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(121)  # 左：アニメーション
ax2 = fig.add_subplot(122)  # 右：グラフ

def draw_spring(ax, y_end):
    """バネをギザギザで描画（端は直線）"""
    n_turns = 10     # ギザギザの数
    width = 0.1      # バネの振幅
    top_margin = 0.2 # 上部の直線長
    bot_margin = 0.2 # 下部の直線長
    
    length = abs(y_end)
    # 座標リストの初期化
    y_points = [0, -top_margin]
    x_points = [0, 0]
    
    # ギザギザ部分の生成
    mid_length = length - top_margin - bot_margin
    if mid_length > 0:
        for i in range(n_turns * 2):
            # ギザギザの各頂点のy座標を等間隔に配置
            y_p = -top_margin - (mid_length * (i + 0.5) / (n_turns * 2))
            x_p = width if i % 2 == 0 else -width
            x_points.append(x_p)
            y_points.append(y_p)
            
    # 下部の直線と終点
    y_points.extend([y_end + bot_margin, y_end])
    x_points.extend([0, 0])
    
    return ax.plot(x_points, y_points, color='gray', lw=1.5)

# グラフ（右側）の初期設定
ax2.set_xlim(0, duration)
ax2.set_ylim(min(history_y) - 0.5, max(history_y) + 0.5)
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Position (y) [m]")
ax2.grid(True)
line_graph, = ax2.plot([], [], color='blue', lw=2)

def update(i):
    ax1.clear()
    # 天井を0とし、描画範囲を固定（上向き正）
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(min(history_y) - 1.0, 0.5) 
    ax1.axhline(0, color='black', lw=3) # 天井
    
    current_y = history_y[i]
    
    # バネと質点（おもり）の描画
    draw_spring(ax1, current_y)
    ax1.plot(0, current_y, 'ro', markersize=20) # 質点
    
    ax1.set_title(f"Time: {t_data[i]:.2f}s")
    
    # 右側のグラフ更新
    line_graph.set_data(t_data[:i], history_y[:i])
    
    # 目標時間に達したらウィンドウを閉じる
    if i == steps - 1:
        plt.close()
    
    return line_graph,

# アニメーションの作成
# interval=50ms なので 20fps 相当
ani = FuncAnimation(fig, update, frames=steps, interval=50, blit=False)

# --- 保存処理 ---
# FFmpegを使わず、Pillowを使用してGIFとして保存
save_filename = "simulation.gif"
print(f"Simulating and saving to {save_filename}...")
try:
    ani.save(save_filename, writer='pillow', fps=20)
    print("Save completed successfully.")
except Exception as e:
    print(f"Save failed: {e}")

# 保存が終わった後に画面に表示（※ ani.saveで一度最後まで回るため、再度表示されます）
plt.tight_layout()
plt.show()