import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def run_simulation_visualizer(t_data, history_y, y_eq, duration, dt, save_filename):
    """
    シミュレーション結果を受け取り、実時間に同期したアニメーション表示と保存を行う関数
    """
    
    # dtから理想的なFPSを計算 (例: dt=0.05s なら 20fps)
    # FuncAnimationのintervalはミリ秒単位なので、dt * 1000 を使用する
    calc_fps = 1.0 / dt
    anim_interval = dt * 1000
    
    # 描画範囲の設定
    y_min = min(history_y) - 0.7
    y_max = 0.5
    
    # フィギュアの作成
    fig = plt.figure(figsize=(12, 6))
    
    ax1 = fig.add_subplot(121)
    
    ax2 = fig.add_subplot(122)
    
    line_graph, = ax2.plot([], [], color='blue', lw=2)

    def draw_spring(ax, y_end):
        n_turns = 10
        width = 0.1
        top_margin = 0.2
        bot_margin = 0.2
        
        length = abs(y_end)
        
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
        # 左側：物理描画
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(y_min, y_max)
        ax1.axhline(0, color='black', lw=3)
        ax1.axhline(y_eq, color='red', linestyle='--', alpha=0.4)
        
        # 右側：グラフ描画
        ax2.set_xlim(0, duration)
        ax2.set_ylim(y_min, y_max)
        ax2.axhline(y_eq, color='red', linestyle='--', alpha=0.4)
        ax2.set_xlabel("Time [s]")
        ax2.set_ylabel("Position [m]")
        ax2.grid(True, alpha=0.3)

    def update(i):
        ax1.clear()
        setup_axes()
        
        current_y = history_y[i]
        
        draw_spring(ax1, current_y)
        ax1.plot(0, current_y, 'ro', markersize=20)
        
        line_graph.set_data(t_data[:i], history_y[:i])
        
        return line_graph,

    # アニメーションの設定 (intervalをdtに合わせることで実時間再生に近づける)
    ani = FuncAnimation(
        fig, 
        update, 
        frames=len(t_data), 
        interval=anim_interval, 
        blit=False, 
        repeat=False
    )

    if save_filename:
        print(f"Saving to {save_filename} at {calc_fps:.1f} fps...")
        # 保存時のfpsも計算値に連動させる
        ani.save(save_filename, writer='pillow', fps=calc_fps)
        print("Save completed.")