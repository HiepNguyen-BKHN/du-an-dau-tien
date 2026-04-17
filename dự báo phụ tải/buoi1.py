import numpy as np
import pandas as pd
#import openpyxl
"""
1.Tạo 1 file excel chứa dữ liệu phụ tải, nhiệt độ, dữ liệu chưa sạch viết các hàm để xử lý dữ liệu
-Chạy với 1 bộ dữ liệu thực
-Nhiệt độ loanh quanh 30 độ : 30 + 5sin(2pi.t/24) + random

"""
time_index = pd.date_range(start='2024-01-01',periods=720, freq='h')
# print(time_index)
t = np.arange(720)
temp = 30 + 5*np.sin(2*np.pi*t/24) + np.random.normal(0,1,720)

# Tạo dữ liệu phụ tải giả định (ví dụ: phụ tải tăng theo nhiệt độ + nhiễu ngẫu nhiên)
base_load = 100
a_cool = 8 #khi nhiệt độ vượt quá 25 độ thì nếu t tăng 1 thì load tăng 8 đơn vị 
t_comfort = 25
load = base_load + a_cool * np.maximum(0,temp-t_comfort) + 50*np.sin(2*np.pi*t/24) + np.random.normal(0,1,720)

#tạo dữ liệu noise
load[100] = -100 
load[10:15] = np.nan 
load[200] = 500 

#Tạo bảng (DataFrame) chứa các dữ liệu đã tạo
df = pd.DataFrame({
    'time': time_index,
    'temperature': temp,
    'load': load
})
df.to_excel('data.xlsx', index=False)
print(df)