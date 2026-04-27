import numpy as np
from visualizer import run_simulation_visualizer

# --- 物理パラメータ ---
m, k, c, g = 1.0, 20.0, 0.3, 9.81
L0 = -2.0
y_eq = L0 - (m * g / k)

# --- シミュレーション設定 ---
dt, duration = 0.05, 10.0
t_data = np.linspace(0, duration, int(duration / dt))

# ロジック部分
y, v = L0, 0.0
history_y = []

for t in t_data:
    a = -g - (k / m) * (y - L0) - (c / m) * v
    v += a * dt
    y += v * dt
    history_y.append(y)

# 描画・保存関数を呼び出す
run_simulation_visualizer(t_data, history_y, y_eq, L0, duration)