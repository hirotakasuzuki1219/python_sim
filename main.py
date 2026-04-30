import numpy as np
from visualizer import run_simulation_visualizer

# --- 物理パラメータ ---
m = 1.0
k = 20.0
c = 0.3 
k = 1500.0 # 失敗条件
c = 0.0 # 失敗条件
g = 9.81
L0 = 2.0 # 自然長

# 描画用
save_filename="results/Results.gif" # 保存するGIFファイルの名前
save_filename="results/Results_error.gif" # 保存するGIFファイルの名前

# --- シミュレーション設定 ---
dt = 0.05
duration = 5.0

# タイムステップの生成
t_data = np.linspace(0, duration, int(duration / dt))

# ロジック部分の状態初期化
y = - 1.0
v = 0.0
history_y = []

# 数値シミュレーション実行
for t in t_data:
    # 運動方程式
    a = -g - (k / m) * (y + L0) - (c / m) * v
    
    # 速度と位置の更新
    v += a * dt
    y += v * dt
    
    # 履歴の保存
    history_y.append(y)

# 描画・保存関数を呼び出す（dtを渡してfpsを自動計算）
run_simulation_visualizer(t_data, history_y, duration, dt, save_filename)