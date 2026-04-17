# 线性图像数据提取工具
一款用于从线性图像中提取指定区域数据点坐标，完成坐标标定与可视化的工具，包含四个核心脚本，支持 VS Code 快捷运行与多终端操作。

## 目录
1. [快速开始](#快速开始)
2. [依赖环境](#依赖环境)
3. [完整工作流程](#完整工作流程)
4. [完整流程示例](#完整流程示例)
5. [注意事项](#注意事项)
6. [常见问题](#常见问题)
7. [macOS 运行异常解决方案](#macos-运行异常解决方案)
8. [备注](#备注)
9. [特别鸣谢](#特别鸣谢)

---

## 快速开始
### 项目获取
```bash
git clone https://github.com/adamleegotmad/extractdot.git
```

### 运行方式
⚠️ **请在 `extractdot` 文件夹下运行，以支持 VS Code 按钮运行**

#### Bash 环境
```bash
cd extractdot
bash main.sh
```

#### PowerShell 环境
1. 前置配置（管理员权限）
```powershell
# 查看执行策略
Get-ExecutionPolicy
# 若为 Restricted，修改执行策略
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```
2. 运行脚本
```powershell
cd extractdot
.\main.ps1
```

---

## 依赖环境
### 基础环境
- Python 3.13 及以上版本

### 第三方库（需手动安装）
- `numpy`
- `pandas`
- `matplotlib`
- `Pillow` (PIL)
- `opencv-python`

### 内置库（无需安装）
`sys`、`csv`、`tkinter`（`filedialog`/`ttk`/`messagebox`）、`pathlib`

### 依赖安装命令
```bash
pip3 install numpy pandas matplotlib Pillow opencv-python
```

---

## 完整工作流程
### Step 1：转换为二值黑白图像
**运行命令**
```bash
python3 convert.py
```
**功能说明**
将原始彩色/灰度图像转换为二值黑白图像，突出目标点（黑底白点/白底黑点），为后续处理做准备。
**输入**：原始图像（路径可在脚本内自定义）
**输出**：坐标文件 `data.csv`（关闭图像窗口即可完成输出）

---

### Step 2：坐标标定
**运行命令**
```bash
python3 regular.py
```
**功能说明**
选取图像中两个横纵坐标不同的已知标注点，输入真实物理坐标，建立像素坐标与真实坐标的映射关系。
**输入**：Step 1 生成的二值化图像
**输出**：真实坐标文件 `data_true.csv`（按提示依次选择两个参考点，关闭窗口完成输出）

---

### Step 3：选择感兴趣区域
**运行命令**
```bash
python3 choose.py
```
**功能说明**
通过鼠标绘制多边形，手动选取需要提取数据的目标区域（ROI）。
**输入**：二值化图像/叠加标定信息的原始图像
**输出**：多边形顶点坐标文件 `filtered_output.csv`（关闭图像窗口完成输出）

---

### Step 4：提取坐标并可视化
**运行命令**
```bash
python3 final.py
```
**功能说明**
在选定区域内提取所有目标点坐标，结合标定参数转换为真实坐标，完成数据保存与可视化。
**输入**：二值化图像、标定参数文件、多边形区域文件
**输出**：
1. 真实坐标文件 `extract.csv`
2. 坐标点分布图 `extract_plot.png`（关闭图像窗口完成输出）

---

## 完整流程示例
```bash
# 1. 图像二值化
python3 convert.py

# 2. 坐标标定
python3 regular.py

# 3. 选取目标区域
python3 choose.py

# 4. 提取数据并可视化
python3 final.py
```
执行完成后，在当前目录获取最终结果文件。

---

## 注意事项
1. Step 2 标定时，两个参考点应保持较远间距，禁止共线，提升标定精度；
2. Step 3 绘制多边形时，完整包裹所需区域，避免边缘数据点遗漏。

---

## 常见问题
**Q：中间步骤操作错误怎么办？**
A：关闭窗口重新运行对应脚本即可。

**Q：标定时点错位置如何重新选择？**
A：再点击一次需要标定的第一个或者第二个点的按钮，然后可以覆盖上次的选项，再次选择图像上的点。

---

## macOS 运行异常解决方案
### 一、安装 Homebrew 版 Python
```bash
brew install python
```

### 二、配置 Python 环境变量
1. 确认 Shell 类型
```bash
echo $SHELL
```
- 输出 `/bin/zsh` → 编辑 `~/.zshrc`
- 输出 `/bin/bash` → 编辑 `~/.bash_profile`/`~/.bashrc`

2. 添加路径
- Apple Silicon (M1/M2/M3)
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```
- Intel 芯片
```bash
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

3. 验证配置
```bash
which python3
python3 --version
```

4. 快捷命令别名（可选）
```bash
echo 'alias python=python3' >> ~/.zshrc
echo 'alias pip=pip3' >> ~/.zshrc
source ~/.zshrc
```

5. VS Code 解释器配置
`Cmd+Shift+P` → 输入 `Python: Select Interpreter` → 选择 Homebrew 安装的 Python

### 三、解决 `_tkinter` 缺失报错
```bash
brew install python-tk
```

### 四、解决 `externally-managed-environment` 报错
安装库时添加参数：
```bash
pip3 install 包名 --break-system-packages
```

### 五、快速一键配置
```bash
# 安装 Python
brew install python
# 配置路径（M1/M2/M3 zsh）
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
# 安装 tkinter
brew install python-tk
# 安装依赖库
pip3 install numpy --break-system-packages
pip3 install matplotlib --break-system-packages
```

---

## 备注
工具后续计划推出 2.0 版本，优化交互逻辑，新增非线性坐标系读取功能。

---

## 特别鸣谢
灵感来源：hay

*留言：扒古早文献光谱图太麻烦了（，需要vibe coding帮助扒细密数据点（是吗）感谢lhd，实在是太伟大了，深谙ai使用（是的）
没人觉得夸别人会用ai真的是一种很高级的夸赞吗？
另外，祝我自己和所有搞科研的大家都身体健康，平安幸福，在苦逼科研夹缝中美好的生存！*

