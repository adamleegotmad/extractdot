import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pathlib import Path

class NormalizationApp:
    """
    交互式数据归一化工具
    功能：
    1. 读取 data.csv（两列：x, y）
    2. 在散点图上点击选取两个参考点
    3. 输入这两个点在真实坐标系中的坐标值
    4. 对全体数据执行线性归一化变换并绘图
    5. 导出变换后的数据为 data_true.csv
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Data Normalization Tool")
        self.root.geometry("1000x750")
        
        # 数据存储
        self.df_raw = None          # 原始数据 DataFrame
        self.x_raw = None           # numpy 数组，原始 x
        self.y_raw = None           # numpy 数组，原始 y
        self.selected_indices = []  # 存储选中的两个点的索引
        self.points_selected = [None, None]  # (x_raw, y_raw) 元组
        
        # 真实坐标输入变量
        self.var_x1_true = tk.StringVar()
        self.var_y1_true = tk.StringVar()
        self.var_x2_true = tk.StringVar()
        self.var_y2_true = tk.StringVar()
        
        # 状态显示
        self.status_var = tk.StringVar(value="Ready. Load data first.")
        
        # 创建界面组件
        self.create_widgets()
        
        # 自动加载数据（若文件存在）
        self.load_data()
    
    def create_widgets(self):
        """构建 GUI 布局"""
        # 主框架：左侧画布，右侧控制面板
        main_panel = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_panel.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：Matplotlib 画布
        left_frame = ttk.Frame(main_panel)
        main_panel.add(left_frame, weight=3)
        
        # 创建 Matplotlib 图形
        self.fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X raw")
        self.ax.set_ylabel("Y raw")
        self.ax.set_title("Raw Data (click to select reference points)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=left_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加 Matplotlib 工具栏（缩放、保存等）
        toolbar = NavigationToolbar2Tk(self.canvas, left_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 绑定鼠标点击事件
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        # 右侧：控制面板
        right_frame = ttk.Frame(main_panel, padding=10)
        main_panel.add(right_frame, weight=1)
        
        # 数据加载区域
        ttk.Label(right_frame, text="1. Data Loading", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0,5))
        ttk.Button(right_frame, text="Reload data.csv", command=self.load_data).pack(fill=tk.X, pady=2)
        self.label_data_info = ttk.Label(right_frame, text="No data loaded.")
        self.label_data_info.pack(anchor=tk.W, pady=5)
        
        # 选点区域
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, text="2. Select Reference Points", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0,5))
        
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Select Point 1", command=lambda: self.set_selection_mode(0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Select Point 2", command=lambda: self.set_selection_mode(1)).pack(side=tk.LEFT, padx=2)
        
        self.label_point1 = ttk.Label(right_frame, text="Point 1: not selected")
        self.label_point1.pack(anchor=tk.W, pady=2)
        self.label_point2 = ttk.Label(right_frame, text="Point 2: not selected")
        self.label_point2.pack(anchor=tk.W, pady=2)
        
        # 真实坐标输入区域
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, text="3. True Coordinates", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0,5))
        
        # 点1输入
        frame_p1 = ttk.LabelFrame(right_frame, text="Point 1 True Values", padding=5)
        frame_p1.pack(fill=tk.X, pady=5)
        ttk.Label(frame_p1, text="X1 true:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame_p1, textvariable=self.var_x1_true, width=12).grid(row=0, column=1, padx=5)
        ttk.Label(frame_p1, text="Y1 true:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        ttk.Entry(frame_p1, textvariable=self.var_y1_true, width=12).grid(row=0, column=3, padx=5)
        
        # 点2输入
        frame_p2 = ttk.LabelFrame(right_frame, text="Point 2 True Values", padding=5)
        frame_p2.pack(fill=tk.X, pady=5)
        ttk.Label(frame_p2, text="X2 true:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(frame_p2, textvariable=self.var_x2_true, width=12).grid(row=0, column=1, padx=5)
        ttk.Label(frame_p2, text="Y2 true:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        ttk.Entry(frame_p2, textvariable=self.var_y2_true, width=12).grid(row=0, column=3, padx=5)
        
        # 归一化与导出按钮
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, text="4. Normalize & Export", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0,5))
        
        ttk.Button(right_frame, text="Apply Normalization & Plot", command=self.normalize_and_plot).pack(fill=tk.X, pady=3)
        ttk.Button(right_frame, text="Export Normalized Data (data_true.csv)", command=self.export_csv).pack(fill=tk.X, pady=3)
        
        # 状态栏
        ttk.Separator(right_frame, orient='horizontal').pack(fill=tk.X, pady=10)
        ttk.Label(right_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, pady=5)
        
        # 初始化选点模式变量
        self.selection_mode = None  # None, 0 (point1), 1 (point2)
    
    def load_data(self):
        """从 data.csv 加载数据"""
        csv_path = Path("data.csv")
        if not csv_path.exists():
            messagebox.showerror("Error", "data.csv not found in current directory.")
            self.status_var.set("Error: data.csv not found.")
            return
        
        try:
            self.df_raw = pd.read_csv(csv_path)
            # 期望有两列，假设列名为 'x' 和 'y'；若没有，则取前两列
            if 'x' in self.df_raw.columns and 'y' in self.df_raw.columns:
                self.x_raw = self.df_raw['x'].values
                self.y_raw = self.df_raw['y'].values
            else:
                # 默认第一列为 x，第二列为 y
                cols = self.df_raw.columns[:2]
                self.x_raw = self.df_raw[cols[0]].values
                self.y_raw = self.df_raw[cols[1]].values
            
            self.label_data_info.config(text=f"Loaded {len(self.x_raw)} points.")
            self.status_var.set("Data loaded. Select reference points.")
            
            # 重置选点状态
            self.selected_indices = []
            self.points_selected = [None, None]
            self.update_point_labels()
            
            # 绘制原始数据
            self.plot_raw_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data:\n{e}")
            self.status_var.set("Data loading failed.")
    
    def plot_raw_data(self):
        """绘制原始散点图"""
        self.ax.clear()
        self.ax.scatter(self.x_raw, self.y_raw, s=20, c='blue', alpha=0.6, label='Raw data')
        self.ax.set_xlabel("X raw")
        self.ax.set_ylabel("Y raw")
        self.ax.set_title("Raw Data (click to select reference points)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        
        # 若已选点，则高亮显示
        for i, pt in enumerate(self.points_selected):
            if pt is not None:
                self.ax.scatter(pt[0], pt[1], s=100, c='red', marker='X', edgecolors='k', linewidths=1.5,
                                label=f'Point {i+1} (raw)')
        
        handles, labels = self.ax.get_legend_handles_labels()
        if handles:
            self.ax.legend()
        
        self.canvas.draw()
    
    def set_selection_mode(self, idx):
        """进入选点模式 (0 或 1)"""
        if self.x_raw is None:
            messagebox.showwarning("Warning", "Please load data first.")
            return
        self.selection_mode = idx
        self.status_var.set(f"Click on the plot to select Point {idx+1}...")
    
    def on_click(self, event):
        """处理画布点击事件"""
        if event.inaxes != self.ax:
            return
        if self.selection_mode is None:
            return
        if self.x_raw is None:
            return
        
        # 获取点击坐标
        click_x, click_y = event.xdata, event.ydata
        
        # 寻找最近的数据点
        distances = np.sqrt((self.x_raw - click_x)**2 + (self.y_raw - click_y)**2)
        nearest_idx = np.argmin(distances)
        nearest_x, nearest_y = self.x_raw[nearest_idx], self.y_raw[nearest_idx]
        
        # 检查是否与已选点重复
        if nearest_idx in self.selected_indices:
            messagebox.showwarning("Warning", "This point is already selected. Choose another.")
            return
        
        # 如果之前此位置已选点，先移除旧索引
        old_idx = self.selected_indices[self.selection_mode] if len(self.selected_indices) > self.selection_mode else None
        if old_idx is not None:
            self.selected_indices.remove(old_idx)
        
        # 更新列表
        if len(self.selected_indices) <= self.selection_mode:
            self.selected_indices.append(nearest_idx)
        else:
            self.selected_indices[self.selection_mode] = nearest_idx
        
        self.points_selected[self.selection_mode] = (nearest_x, nearest_y)
        
        # 更新标签显示
        self.update_point_labels()
        
        # 重新绘图以显示选中的点
        self.plot_raw_data()
        
        # 退出选点模式
        self.selection_mode = None
        self.status_var.set(f"Point {self.selection_mode+1 if self.selection_mode is not None else ''} selected. Ready.")
    
    def update_point_labels(self):
        """更新右侧面板上的选点信息"""
        if self.points_selected[0] is not None:
            x, y = self.points_selected[0]
            self.label_point1.config(text=f"Point 1: ({x:.4f}, {y:.4f})")
        else:
            self.label_point1.config(text="Point 1: not selected")
        
        if self.points_selected[1] is not None:
            x, y = self.points_selected[1]
            self.label_point2.config(text=f"Point 2: ({x:.4f}, {y:.4f})")
        else:
            self.label_point2.config(text="Point 2: not selected")
    
    def normalize_and_plot(self):
        """执行归一化变换并绘制结果"""
        # 检查是否已选取两个点
        if None in self.points_selected:
            messagebox.showwarning("Warning", "Please select both reference points first.")
            return
        
        # 获取真实坐标输入
        try:
            x1_true = float(self.var_x1_true.get())
            y1_true = float(self.var_y1_true.get())
            x2_true = float(self.var_x2_true.get())
            y2_true = float(self.var_y2_true.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for true coordinates.")
            return
        
        (x1_raw, y1_raw) = self.points_selected[0]
        (x2_raw, y2_raw) = self.points_selected[1]
        
        # 检查两点是否相同
        if np.isclose(x1_raw, x2_raw) or np.isclose(y1_raw, y2_raw):
            messagebox.showerror("Error", "The two reference points must have distinct x and y values to define a linear mapping.")
            return
        
        # 计算线性变换系数：x_true = a_x * x_raw + b_x
        a_x = (x2_true - x1_true) / (x2_raw - x1_raw)
        b_x = x1_true - a_x * x1_raw
        
        a_y = (y2_true - y1_true) / (y2_raw - y1_raw)
        b_y = y1_true - a_y * y1_raw
        
        # 对全体数据应用变换
        self.x_true = a_x * self.x_raw + b_x
        self.y_true = a_y * self.y_raw + b_y
        
        # 绘制归一化后的数据
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.scatter(self.x_true, self.y_true, s=20, c='green', alpha=0.6, label='Normalized data')
        
        # 也标记出两个参考点变换后的位置（应该与输入的真实坐标一致）
        self.ax.scatter([x1_true, x2_true], [y1_true, y2_true], s=100, c='red', marker='X',
                        edgecolors='k', linewidths=1.5, label='Reference points (true)')
        
        self.ax.set_xlabel("X true")
        self.ax.set_ylabel("Y true")
        self.ax.set_title("Normalized Data (linear mapping)")
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.legend()
        
        # 重新绑定点击事件（画布重建后需要重新连接）
        self.cid_press = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
        self.canvas.draw()
        self.status_var.set("Normalization applied. New plot displayed.")
        
        # 输出变换系数到命令行（中文提示）
        print(f"线性变换系数: X_true = {a_x:.6f} * X_raw + {b_x:.6f}")
        print(f"              Y_true = {a_y:.6f} * Y_raw + {b_y:.6f}")
    
    def export_csv(self):
        """导出归一化后的数据到 data_true.csv"""
        if not hasattr(self, 'x_true') or self.x_true is None:
            messagebox.showwarning("Warning", "Please perform normalization first.")
            return
        
        try:
            df_out = pd.DataFrame({'x_true': self.x_true, 'y_true': self.y_true})
            df_out.to_csv('data_true.csv', index=False)
            self.status_var.set("Normalized data exported to data_true.csv")
            print("归一化数据已保存至 data_true.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data:\n{e}")

def main():
    root = tk.Tk()
    app = NormalizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()