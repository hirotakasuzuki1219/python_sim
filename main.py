import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 物理パラメータ ---
m = 1.0      # 質量 [kg]
k = 10.0     # バネ定数 [N/m]
# c = 0.2      # 減衰係数 [N s/m]
c = 0.0      # 減衰係数 [N s/m]
g = 9.81     # 重力加速度 [m/s^2]
L0 = 2.0     # バネの自然長 [m]

# つり合いの位置 (x_eq) の計算: k * x_eq = m * g
x_eq = (m * g) / k
# 理論上の周期 (減衰がない場合): T = 2 * pi * sqrt(m/k)
theoretical_period = 2 * np.pi * np.sqrt(m / k)

# --- シミュレーション設定 ---
# dt = 0.05
dt = 0.8
steps = 400
t_data = np.arange(0, steps * dt, dt)

# 初期状態
x = 0.0      # 位置 (天井からの距離。自然長の位置を0とする)
v = 0.0      # 速度
history_x = []

# --- シミュレーション（オイラー法） ---
for t in t_data:
    # 鉛直方向の運動方程式: ma = mg - kx - cv
    # 加速度 a = g - (k/m)x - (c/m)v
    a = g - (k / m) * x - (c / m) * v
    
    v += a * dt
    x += v * dt
    history_x.append(x)

# --- 可視化 ---
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(121) # アニメーション用
ax2 = fig.add_subplot(122) # グラフ用

# グラフの初期設定
ax2.set_xlim(0, t_data[-1])
ax2.set_ylim(min(history_x)-0.5, max(history_x)+0.5)
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Displacement [m]")
ax2.axhline(x_eq, color='r', linestyle='--', label="Equilibrium")
line_graph, = ax2.plot([], [], lw=2, color='b', label="Position")
ax2.legend()

# 周期の可視化用の補助線（最初の山から次の山までなど）
# ここでは簡易的に理論周期をテキスト表示
ax2.text(0.5, max(history_x), f"Theoretical Period: {theoretical_period:.2f}s", color='green')

# アニメーション更新関数
def update(i):
    ax1.clear()
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(max(history_x) + 0.5, -0.5) # 下向きを正とするためy軸反転
    
    current_x = history_x[i]
    
    # バネの描画（ジグザグ）
    num_points = 20
    spring_y = np.linspace(0, current_x, num_points)
    spring_x = 0.1 * np.sin(np.arange(num_points) * np.pi)
    ax1.plot(spring_x, spring_y, color='gray')
    
    # おもりの描画
    ax1.plot(0, current_x, 'ro', markersize=20)
    ax1.set_title(f"Time: {t_data[i]:.2f}s")
    
    # グラフの更新
    line_graph.set_data(t_data[:i], history_x[:i])
    return line_graph,

ani = FuncAnimation(fig, update, frames=steps, interval=50, blit=False)
plt.tight_layout()
plt.show()