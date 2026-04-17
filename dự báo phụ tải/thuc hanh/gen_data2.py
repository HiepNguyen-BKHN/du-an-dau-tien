import pandas as pd
import numpy as np

time_index = pd.date_range(start = '2024-01-01',periods = 720, freq = 'h')
# print(time_index)
t = np.arange(720)

temp = 30 + 5*np.sin(t*2*np.pi/24) +np.random.normal(0,1,720)

base_load = 100

a_cool = 8 # khi nhiệt độ vượt quá 25 độ thì nếu t tăng 1 thì load tăng 8 đơn vị (MW)

t_comfort = 25

load = base_load + a_cool * np.maximum(0, temp - t_comfort) + 50*np.sin(t*2*np.pi/24) + np.random.normal(0,10,720)

load[10:15] = np.nan
load[100] = -100
load[200] = 500

df = pd.DataFrame({'Time':time_index,'temperature': temp, "load": load})

df.to_excel('data_phutai_16_04.xlsx', index = False)




