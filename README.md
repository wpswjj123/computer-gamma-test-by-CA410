# gamma_test_final —— 灰阶扫描数据采集工具

一个 Windows 桌面小工具：通过串口控制色彩分析仪（CA-410 类），全屏显示纯色，逐级扫描灰度并采集 CIE-x / CIE-y / 亮度，最后导出 Excel。可打包成单文件 `.exe`，免安装 Python 直接运行。

## 功能

- **图形界面输入**：起始灰度（R/G/B）、步长、最大灰度、APL、保存路径、Excel 文件名、串口号，空输入自动取默认值。
- **串口控制**：以 38400 波特率向仪器发送初始化指令序列（COM/SCS/FSC/OPR/MDS/MCH/LUS/ZRC/MES），随后逐点读取测量值。
- **全屏纯色显示**：按屏幕尺寸 × APL 铺满纯色，逐点递增灰度。
- **数据导出**：每点采集后写入 Excel（`{保存路径}/{Excel文件名}_{时间戳}.xlsx`）。
- **退出**：运行中按 `Esc` 退出全屏并结束。

---

## 打包成 exe

### 方式一：GitHub Actions（推荐，自动）

仓库自带 workflow `.github/workflows/build.yml`：

- 每次 **push 到 `main`/`master`** 自动在 `windows-latest` 上构建；
- 也可在仓库 **Actions 页面手动点 “Run workflow”** 触发。

构建完成后，在对应运行记录的 **Artifacts** 里下载 `gamma_test_final-windows`（内含 `gamma_test_final.exe`）。

### 方式二：Windows 本地一键打包

双击仓库里的 **`build.bat`** 即可（需已安装 Python 3.8+ 并勾选 “Add python.exe to PATH”）。完成后可执行文件在：

```
dist\gamma_test_final.exe
```

### 打包命令说明

```bat
pyinstaller --onefile --noconfirm --clean --windowed ^
    --name gamma_test_final ^
    --hidden-import openpyxl ^
    gamma_test_final.py
```

| 参数 | 作用 |
|------|------|
| `--onefile` (`-F`) | 打成单个 exe |
| `--windowed` (`-w`) | GUI 程序，不弹黑色控制台窗口 |
| `--hidden-import openpyxl` | `pandas.to_excel` 底层依赖 openpyxl，显式声明防止漏收集 |

> 本脚本**不读取任何外部文件**，因此不需要 `--add-data`。

---

## 运行环境与依赖

| 依赖 | 用途 |
|------|------|
| `pillow` | 生成纯色图像、tkinter 显示 |
| `pyserial` | 串口通讯 |
| `pandas` + `openpyxl` | 采集结果写 Excel |

- **仅支持 Windows**（串口名如 `COM3`）。
- **必须连接对应色彩分析仪硬件**：exe 在未连接设备 / 无对应串口的机器上**无法实际工作**，会因串口打开失败而报错。
- 打包出的 exe 与机器架构、Python 版本相关，建议在同一 Windows 环境使用。

---

## 使用步骤

1. 双击 `gamma_test_final.exe`。
2. 在输入窗口填写参数（留空用默认值）：
   - 起始灰度 `mingray_R/G/B`、步长 `step_R/G/B`、最大灰度 `maxgray`
   - `APL`（屏幕铺满系数）、`path`（保存目录）、`excelname`、`端口`（如 `COM3`）
3. 点「提交」，程序连接仪器并进入全屏纯色扫描。
4. 扫描完成后，Excel 自动保存到指定目录。
5. 中途按 `Esc` 可退出。

---

## 已知行为（当前版本，未改动逻辑）

- 每个测量点在 Excel 中**占两行**（一行灰度值、一行 CIE 值），列结构为 `0 / 1 / 2 / CIE-x / CIE-y / 亮度`。
- 循环条件为 `while max(r,g,b) <= gray_max`，若步长不能整除则**不会测量到等于最大灰度的点**（例如起点 0、步长 10、maxgray 255 时停在 250）。

> 以上为脚本既有行为，本仓库仅做打包适配，未修改源码逻辑。