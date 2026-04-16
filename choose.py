import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector
from matplotlib.path import Path

def main():
    # 1. 解析命令行参数（此处硬编码，可根据需要恢复为命令行读取）
    csv_file = 'data_true.csv'
    try:
        skip_rows = 1
    except ValueError:
        print("Skip rows must be an integer")
        sys.exit(1)

    # 2. 读取 CSV 数据，跳过指定行，假设每行格式为 "x,y"
    try:
        # header=None 表示文件没有列名，我们直接用第0、1列作为 x, y
        df = pd.read_csv(csv_file, header=None, skiprows=skip_rows)
        x = df[0].values.astype(float)
        y = df[1].values.astype(float)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    if len(x) == 0:
        print("No valid data in file")
        sys.exit(1)

    # 3. 绘制散点图
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y, s=10, c='blue', alpha=0.1, label='Original points')
    ax.set_title("Draw a polygon with mouse, press Enter to confirm")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle='--', alpha=0.1)

    # 存储多边形顶点
    polygon_verts = []
    # 标志位，确保只处理一次选区
    processed = False

    def on_polygon_click(verts):
        """多边形绘制完成后的回调函数"""
        nonlocal processed
        if processed:
            return
        if len(verts) < 3:
            print("Polygon must have at least 3 vertices, please draw again")
            return

        # 判断每个点是否在多边形内部
        points = np.column_stack((x, y))
        path = Path(verts)
        inside_mask = path.contains_points(points)
        inside_points = points[inside_mask]

        # 输出结果到控制台
        print(f"\nNumber of points inside polygon: {len(inside_points)}")
        for pt in inside_points:
            print(f"{pt[0]:.6f},{pt[1]:.6f}")

        # 保存到文件
        out_file = "filtered_output.csv"
        np.savetxt(out_file, inside_points, delimiter=",", fmt="%.6f",
                   header="x,y", comments='')
        print(f"\nFiltered points saved to: {out_file}")

        # 在图上高亮选中的点
        ax.scatter(inside_points[:, 0], inside_points[:, 1],
                   s=20, c='red', alpha=0.8, label='Selected points')
        # 绘制多边形边界
        poly = plt.Polygon(verts, closed=True, fill=None, edgecolor='red', linewidth=2)
        ax.add_patch(poly)
        ax.legend()
        fig.canvas.draw_idle()

        # 禁用多边形选择器，防止重复选点
        selector.disconnect_events()
        processed = True
        print("Polygon selector disabled. You can close the figure window.")

    # 4. 创建多边形选择器（按 Enter 完成绘制，按 Esc 取消）
    selector = PolygonSelector(ax, on_polygon_click)

    # 显示窗口，等待用户交互
    plt.show()

if __name__ == "__main__":
    main()