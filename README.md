# 线性图像数据提取工具

本工具用于从线性图像中提取指定区域内数据点的坐标，并完成坐标标定与可视化。共包含四个脚本。
请在extractdot文件夹下运行以获得vscode的按钮运行支持！
首先请获得本项目
```git
git clone https://github.com/adamleegotmad/extractdot.git
```
bash下请：
```bash
cd extractdot
bash main.sh
```
powershell下：

```powershell
cd extractdot
.\main.ps1
```
首先：
在执行 `.\main.ps1` 之前，通常需要确保以下几点：

1. **PowerShell 执行策略**  
   默认情况下 PowerShell 可能禁止运行脚本。先用管理员权限运行以下命令查看并调整策略：
   ```powershell
   Get-ExecutionPolicy
   ```
   如果为 `Restricted`，请改为 `RemoteSigned` 或 `Unrestricted`：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
2. **运行权限**  
   某些操作（如修改注册表、系统服务）需要管理员权限。必要时以 **管理员身份** 启动 PowerShell。
3. **环境变量或配置文件**  
   如果脚本依赖特定环境变量或 `.env` 文件，请预先配置好。

完成这些准备后，再执行 `.\main.ps1` 即可。
```powershell
.\main.ps1
```

## 依赖环境

- Python 3.7+
- 需要安装以下第三方库：
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `Pillow`（即 PIL）
  - `opencv-python`

> 以下为 Python 标准库，无需额外安装：`sys`, `csv`, `tkinter`（含 `filedialog`, `ttk`, `messagebox`）, `pathlib`

### 安装命令

```bash
pip3 install numpy pandas matplotlib Pillow opencv-python
```

## 工作流程

### Step 1: 转换为二值黑白图像

```bash
python3 convert.py
```

**功能说明**  
将原始彩色/灰度图像转换为二值黑白图像（binary black-and-white image）。  
该步骤会突出图像中的目标点（通常为黑底白点或白底黑点），便于后续处理。

**输入**：原始图像（默认路径可自行在脚本中修改）  
**输出**：二值化图像文件（不输出），与对应坐标文件（`data.csv`），交互中直接关闭图像即可完成。

---

### Step 2: 坐标标定

```bash
python3 regular.py
```

**功能说明**  
根据图像上已知的两个标注点（横纵坐标均不同）的真实物理坐标值，建立图像像素坐标与真实坐标之间的映射关系（标定）。  
用户需交互式点击图像中的两个参考点，并输入它们对应的真实坐标值，脚本会计算出仿射变换或比例参数。

**输入**：二值化图像（由 Step 1 生成）  
**输出**：真实坐标文件（`data_true.csv`），交互中请根据图中的提示先后选择第一个点和第二个点，以及选择输出的文件。最好两者先后都选择。

---

### Step 3: 选择感兴趣区域

```bash
python3 choose.py
```

**功能说明**  
使用多边形工具在图像上手动选取需要提取数据点的区域（region of interest, ROI）。  
脚本会打开图像界面，用户通过鼠标点击绘制多边形，闭合后即完成区域选择。

**输入**：二值化图像（或原始图像叠加标定信息）  
**输出**：保存多边形顶点坐标的文件`filtered_output.csv`。交互结束直接关闭图像即可。

---

### Step 4: 提取坐标并可视化

```bash
python3 final.py
```

**功能说明**  
在 Step 3 选定的多边形区域内，提取所有目标点的像素坐标，并根据 Step 2 的标定参数转换为真实坐标。  
最终将坐标数据保存为 `extract.csv`，同时绘制出这些点的分布图并保存为图像文件。

**输入**：  
- 二值化图像  
- 标定参数文件  
- 多边形区域文件  

**输出**：  
- `extract.csv`：包含点真实坐标（x, y）  
- `extract_plot.png`：提取出的坐标点分布图，交互结束可以直接关闭文件。
---

## 完整流程示例

```bash
# 1. 二值化
python3 convert.py

# 2. 标定
python3 regular.py

# 3. 选择区域
python3 choose.py

# 4. 提取坐标
python3 final.py
```

执行完毕后，在当前目录下即可得到 `extract.csv` 和坐标点分布图。

## 注意事项

- Step 2 中选取的两个参考点应尽量距离较远，以提高标定精度，且不要共线。
- Step 3 选取多边形时，建议将所需区域完全包含，避免遗漏边缘点。

## 常见问题

**Q：中间某一步做错了怎么办？**  
A：目前还是重开方便一点；

**Q：标定时点错位置如何重新选择？**  
A：目前较为直接的方法是关闭图像窗口后重新运行 `regular.py`。

---

如有其他问题，请检查脚本内部注释或联系作者。

## 备注
可能会有2.0版本。具体方向是优化代码交互逻辑，以及添加非线性坐标系的读取等。

## 特别鸣谢

提出灵感的hay

*留言：扒古早文献光谱图太麻烦了（，需要vibe coding帮助扒细密数据点（是吗）感谢lhd，实在是太伟大了，深谙ai使用（是的）
没人觉得夸别人会用ai真的是一种很高级的夸赞吗？
另外，祝我自己和所有搞科研的大家都身体健康，平安幸福，在苦逼科研夹缝中美好的生存！*

