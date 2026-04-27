import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ======================
# パラメータ
# ======================
k = 0.5      # バネ係数
c = 0.05     # ダンパー
m = 1.0      # 質量
dt = 0.05
L0 = 1.5

# 初期状態
x = 2.0
v = 0.0

# ======================
# 物理モデル
# ======================
def solver(x, v):
    a = (-k * (x - L0) - c * v) / m
    v += a * dt
    x += v * dt
    return x, v

# ======================
# バネのジグザグ生成
# ======================
def spring_points(x0, x1, n=20, amp=0.2, straight_ratio=0.15):
    # 全長
    L = x1 - x0
    
    # 直線部分の長さ
    s = L * straight_ratio
    
    # 各区間
    x_start = x0
    x_zig_start = x0 + s
    x_zig_end = x1 - s
    x_end = x1

    # ---- 直線（左）----
    xs1 = np.linspace(x_start, x_zig_start, 5)
    ys1 = np.zeros_like(xs1)

    # ---- ジグザグ ----
    xs2 = np.linspace(x_zig_start, x_zig_end, n)
    ys2 = np.zeros_like(xs2)
    for i in range(1, n-1):
        ys2[i] = amp if i % 2 == 0 else -amp

    # ---- 直線（右）----
    xs3 = np.linspace(x_zig_end, x_end, 5)
    ys3 = np.zeros_like(xs3)

    # 結合
    xs = np.concatenate([xs1, xs2, xs3])
    ys = np.concatenate([ys1, ys2, ys3])

    return xs, ys

# ======================
# 描画設定
# ======================
fig, ax = plt.subplots()
spring_line, = ax.plot([], [], 'k-')
point, = ax.plot([], [], 'ko', markersize = 24)
ax.plot([0], [0], 'ks', markersize = 8)  # 黒い四角
ax.axvline(L0, linestyle='--')
ax.set_xlim(0, 3)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal', adjustable='box')

# ======================
# アニメーション更新
# ======================
def update(frame):
    global x, v

    x, v = solver(x, v)

    # バネ
    xs, ys = spring_points(0, x)
    spring_line.set_data(xs, ys)

    # 質点
    point.set_data([x], [0])

    return spring_line, point

# ======================
# 実行
# ======================
ani = FuncAnimation(fig, update, frames=300, interval=30)
plt.title("Spring-Mass Simulation")
ani.save("spring.gif", writer="pillow", fps=30)
plt.show()