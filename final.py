import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取数据（跳过第一行，假设第一行为标题）
df = pd.read_csv('filtered_output.csv', skiprows=1, header=None, names=['x', 'y'])

# 2. 按 x 分组，计算 y 的平均值
grouped = df.groupby('x', as_index=False)['y'].mean()

# 3. 保存结果到 extract.csv
grouped.to_csv('extract.csv', index=False)
print("处理完成，结果已保存至 extract.csv")

# 4. 绘制数据
plt.figure(figsize=(8, 5))
plt.plot(grouped['x'], grouped['y'], marker='o', linestyle='-', color='b', markersize=4)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('picked points')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('extract_plot.png', dpi=150)  # 可选保存图片
plt.show()