@echo off
REM ============================================================
REM  build.bat —— 在 Windows 上本地一键打包 gamma_test_final.exe
REM  双击运行即可。需要已安装 Python 3.8+ 并勾选 Add to PATH
REM  生成文件：
REM     dist\gamma_test_final.exe   单文件图形界面版，双击即用
REM ============================================================
setlocal

echo.
echo ========== 1/3 检查 Python ==========
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装：https://www.python.org/downloads/
    echo        安装时务必勾选 "Add python.exe to PATH"
    pause
    exit /b 1
)
python --version

echo.
echo ========== 2/3 安装依赖 ==========
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
if errorlevel 1 (
    echo [错误] 依赖安装失败，检查网络或换用国内镜像：
    echo   python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    pause
    exit /b 1
)

echo.
echo ========== 3/3 打包 exe ==========
REM GUI 程序：--onefile 单文件 + --windowed 不弹黑框
REM 脚本不读取任何外部文件，无需 --add-data
REM pandas.to_excel 底层依赖 openpyxl，显式 --hidden-import 防止漏收集
python -m PyInstaller --onefile --noconfirm --clean --windowed ^
    --name gamma_test_final ^
    --hidden-import openpyxl ^
    gamma_test_final.py

echo.
echo ============================================================
echo  完成！可执行文件：
echo    dist\gamma_test_final.exe   ^<- 双击运行
echo ============================================================
pause