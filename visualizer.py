import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def run_simulation_visualizer(t_data, history_y, y_eq, L0, duration, save_filename="simulation.gif"):
    """
    シミュレーション結果を受け取り、アニメーション表示と保存を行う関数
    """
    y_min, y_max = min(history_y) - 0.7, 0.5
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    line_graph, = ax2.plot([], [], color='blue', lw=2)

    def draw_spring(ax, y_end):
        n_turns = 10
        width, top_margin, bot_margin = 0.1, 0.2, 0.2
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
        # 左：物理アニメーション
        ax1.set_xlim(-1, 1)
        ax1.set_ylim(y_min, y_max)
        ax1.axhline(0, color='black', lw=3)
        ax1.axhline(y_eq, color='red', linestyle='--', alpha=0.4)
        # 右：時系列グラフ
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

    ani = FuncAnimation(fig, update, frames=len(t_data), interval=50, blit=False, repeat=False)

    if save_filename:
        print(f"Saving to {save_filename}...")
        ani.save(save_filename, writer='pillow', fps=20)
        print("Save completed.")