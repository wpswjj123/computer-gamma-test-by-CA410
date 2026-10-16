from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
import time
import serial
import pandas as pd
from datetime import datetime
import os

def data_process(raw_data):
    try:
        if ',' in raw_data:
            parts=raw_data.split(',')
            if len(parts)>=6:
                return {
                    'CIE-x':float(parts[3]),
                    'CIE-y':float(parts[4]),
                    '亮度':float(parts[5])
                }
            else:
                return {
                    'CIE-x':"error",
                    'CIE-y':"error",
                    '亮度':"error"
                }
    except ValueError as e:
        print(f"出错:{e}")
        return None

class SimpleInputApp:
    def __init__(self, parent):
        # 使用Toplevel作为子窗口，而非新的Tk()
        self.root = tk.Toplevel(parent)
        self.root.title("简单数据输入")
        self.root.geometry("600x400")
        self.parent = parent  # 保存主窗口引用
        self.user_data = {}
        self.fields = self._init_fields()  # 初始化新字段（带默认值）
        self.create_simple_interface()
        # parent.withdraw()  # 隐藏主窗口
    
    def _init_fields(self):
        """初始化字段：(标签, 键名, 默认值)"""
        return [
            ("mingray_R:", "mingray_R", 0),    # R通道起始灰度
            ("step_R:", "step_R", 10),         # R通道步长
            ("mingray_G:", "mingray_G", 0),    # G通道起始灰度
            ("step_G:", "step_G", 10),         # G通道步长（修正笔误）
            ("mingray_B:", "mingray_B", 0),    # B通道起始灰度
            ("step_B:", "step_B", 10),         # B通道步长
            ("maxgray:", "maxgray", 255),      # 最大灰度值
            ("APL:", "APL", 1),               # APL参数
            ("path:", "path", save_path),       # 保存路径
            ("excelname:","excelname","W-120hz-normal"),
            ("端口","端口",DK)
        ]
    
    def create_simple_interface(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        fields = [("mingray_R:", "mingray_R"), ("step_R:", "step_R"),
                  ("mingray_G:", "mingray_G"),("step_G:", "step_G"),
                  ("mingray_B:", "mingray_B"),("step_B:", "step_B"),
                  ("maxgray:", "maxgray"),("APL:","APL"),
                  ("path:","path"),("excelname:","excelname"),
                  ("端口","端口")]
        self.entries = {}
        j = 0
        k = 0
        for i, (label, field) in enumerate(fields):
            t=k//4
            ttk.Label(main_frame, text=label).grid(row=k, column=j, sticky="w", padx=10, pady=10)
            entry = ttk.Entry(main_frame, width=10+8*t)
            entry.grid(row=k, column=j+1, padx=10, pady=10)
            self.entries[field] = entry
            j += 2
            if j >= 3:
                j = 0
                k += 1
        
        ttk.Button(main_frame, text="提交", command=self.submit).grid(row=len(fields), column=0, pady=20)
        ttk.Button(main_frame, text="取消", command=self.root.quit).grid(row=len(fields), column=1, pady=20)
    
    def choose_path(self):
        """选择保存路径并更新输入框"""
        path = filedialog.askdirectory(title="选择数据保存路径")
        if path:
            self.entries["path"].delete(0, tk.END)  # 清空现有内容
            self.entries["path"].insert(0, path)    # 插入新路径
        if excelname:
            self.entries["excel"].delete(0, tk.END)  # 清空现有内容
            self.entries["excelname"].insert(0, excelname)    # 插入新路径

    def submit(self):
        """提交数据：空输入时使用默认值"""
        data = {}
        for label, field, default in self.fields:
            user_input = self.entries[field].get().strip()
            # 空输入用默认值，否则用用户输入
            data[field] = default if not user_input else user_input
        
        self.user_data = data
        self.root.destroy()  # 关闭窗口

    # def submit(self):
    #     data = {field: entry.get() for field, entry in self.entries.items()}
        
    #     if not all(data.values()):
    #         messagebox.showerror("错误", "请填写所有字段")
    #         return
        # 验证输入是否为数字
        # try:
        #     for key in data[5:]:
        #         data[key] = int(data[key])
        # except ValueError:
        #     messagebox.showerror("错误", "所有输入必须为整数")
        #     return
        
        # self.user_data = data
        # self.root.destroy()  # 关闭子窗口
    
    def run(self):
        self.root.wait_window()  # 等待窗口关闭
        return self.user_data

save_path="D:/software/vs code/生成excel"
DK='COM3'
# 创建一个与屏幕大小相同的图像
root = tk.Tk()
app = SimpleInputApp(root)
data = app.run()
r=int(data['mingray_R'])
g=int(data['mingray_G'])
b=int(data['mingray_B'])
gray_max=int(data['maxgray'])
step_R=int(data['step_R'])
step_G=int(data['step_G'])
step_B=int(data['step_B'])
AA=data['excelname']
save_path=data['path']
APL=float(data['APL'])
DK=data['端口']

#excel设置

T=datetime.now().strftime('%Y年%m月%d日_%H_%M_%S')
excel_name=f"{save_path}/{AA}_{T}.xlsx"
print(excel_name)
data1=[]

#410连接
port=DK
baudrate=38400
timeout=1
ser=serial.Serial(port,baudrate,timeout=timeout)
if ser.is_open:
    print(f"串口已打开")
ser.write(b'COM,1\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")
time.sleep(1)
ser.write(b'SCS,4,60.00\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

ser.write(b'FSC,1\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

ser.write(b'OPR,1\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

# ser.write(b'MMS,0\n')
# response=ser.readline().decode().strip()
# print(f"设备响应：{response}")

# ser.write(b'FMS,0\n')
# response=ser.readline().decode().strip()
# print(f"设备响应：{response}")

ser.write(b'MDS,0\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

ser.write(b'MCH,0\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

ser.write(b'LUS,1\n')
response=ser.readline().decode().strip()
print(f"设备响应：{response}")

ser.write(b'ZRC\n')
time.sleep(4)
response=ser.readline().decode().strip()
print(f"设备响应：{response}")


ser.write(b'MES,1\n')
print(ser.readline().decode().strip())

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#切换画面
width=screen_width*1
height=screen_height*1
width=int(width*APL)
height=int(height*APL)

# 创建全屏窗口显示图像
# top = tk.Toplevel(root)
root.deiconify()  # 显示主窗口
root.attributes('-fullscreen', True)
root.configure(bg='black')

# 用于显示图像的标签
label = tk.Label(root)
label.pack(fill=tk.BOTH, expand=True)

#按Esc键退出全屏
def exit_fullscreen(event):
    root.destroy()
root.bind('<Escape>', exit_fullscreen)

root.update()
time.sleep(0.2)
# current_image = None

print(r)
print(g)
print(b)
i=0
while max(r,g,b) <= gray_max:
    img = Image.new('RGB', (width,height), (r, g, b))
    tk_img = ImageTk.PhotoImage(image=img)
    label.image = tk_img  # 保持引用，防止图像被垃圾回收
    current_image = tk_img  # 额外引用
    label.config(image=tk_img)
    
    # 刷新窗口
    root.update()
    if i==0:
        time.sleep(3)
    time.sleep(0.3)  
    ser.write(b'MES,1\n')
    time.sleep(0.2) 
    response=ser.readline().decode().strip()
    gray_r=f"gray_r:{r}"
    gray_g=f"gray_g:{g}"
    gray_b=f"gray_b:{b}"
    gray=[gray_r,gray_g,gray_b]
    data1.append(gray)
    data1.append(data_process(response))
    print(r)
    r=r+step_R
    g=g+step_G
    b=b+step_B
    i=i+1

df=pd.DataFrame(data1)
df.to_excel(excel_name,index=False)
root.destroy()