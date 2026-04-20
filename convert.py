import sys
import csv
import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


def select_png_file():
    """打开文件选择对话框，返回所选PNG文件的路径"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择PNG文件",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path


def image_to_binary(image_path, threshold=127):
    """
    读取图像，转换为灰度图，再二值化。
    返回二值图像（True表示黑色，False表示白色）以及图像尺寸。
    """
    img = Image.open(image_path).convert('L')  # 转为灰度图
    width, height = img.size
    # 二值化：像素值 <= threshold 为黑(True)，否则为白(False)
    binary_img = np.array(img) <= threshold
    return binary_img, width, height


def get_black_pixel_coords(binary_img):
    """
    从二值图像中提取所有黑色像素的坐标 (x, y)，原点在左下角。
    y 坐标已转换：原始行号（从上向下） -> 新 y = height - 1 - 行号
    """
    # np.where 返回 (row_indices, col_indices)，row 对应原始 y，col 对应 x
    y_orig, x_vals = np.where(binary_img)  # y_orig 从上向下递增
    height = binary_img.shape[0]           # 图像高度（像素数）
    # 转换 y 坐标：使原点位于左下角
    y_new = height - 1 - y_orig
    coords = list(zip(x_vals, y_new))
    return coords


def save_coords_to_csv(coords, csv_path):
    """将坐标列表保存到CSV文件，不包含表头"""
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(coords)


def plot_black_points(coords, width, height):
    """
    绘制黑点散点图（左下角原点），并添加一个“Continue”按钮。
    点击按钮后关闭所有图形窗口并退出程序。
    """
    if not coords:
        print("警告：图像中没有黑色像素点，无法绘制。")
        sys.exit(0)

    x_vals = [p[0] for p in coords]
    y_vals = [p[1] for p in coords]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x_vals, y_vals, s=1, c='black', marker='.', alpha=0.1)
    ax.set_title("Black Pixel Distribution (origin at bottom-left)")
    ax.set_xlabel("X coordinate (column)")
    ax.set_ylabel("Y coordinate (row, from bottom)")
    # 设置坐标轴范围，确保显示完整图像区域
    ax.set_xlim(0, width - 1)
    ax.set_ylim(0, height - 1)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linestyle='--', alpha=0.1)

    # 添加 "Continue" 按钮
    ax_button = plt.axes([0.8, 0.01, 0.15, 0.05])  # [left, bottom, width, height]
    btn = Button(ax_button, 'Continue')
    # 绑定点击事件：关闭图形并退出
    btn.on_clicked(lambda event: (plt.close('all'), sys.exit(0)))

    plt.show()


def main():
    # 1. 选择PNG文件
    png_path = select_png_file()
    if not png_path:
        print("未选择文件，程序退出。")
        sys.exit(0)

    # 2. 转换为二值图，获取黑色像素坐标（已转换至左下角原点）
    binary_img, width, height = image_to_binary(png_path)
    black_coords = get_black_pixel_coords(binary_img)

    # 3. 保存为CSV文件（无表头）
    csv_path = 'data.csv'
    save_coords_to_csv(black_coords, csv_path)
    print(f"已保存 {len(black_coords)} 个黑点坐标到文件：{csv_path}")

    # 4. 绘制散点图并显示“Continue”按钮
    plot_black_points(black_coords, width, height)


if __name__ == "__main__":
    main()