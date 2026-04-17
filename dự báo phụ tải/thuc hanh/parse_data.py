import pandas as pd
import numpy as np

df = pd.read_excel(r"E:\LANGUAGE\PYTHON\dự báo phụ tải\thuc hanh\data_phutai_16_04.xlsx")

# print(df['Load'].std())
# print(df['Load'].mean())

#--------------------visualize data ------------------------------
import matplotlib.pyplot as plt 
import seaborn as sns

def plot_load(dat):

    plt.figure(figsize = (15,6))
    plt.plot(df['Timestamp'], dat, color = 'red', label = 'Demand (kW)')
    plt.title("maybe if you need")
    plt.xlabel('Time')
    plt.ylabel('Demand (kW)')
    plt.legend()
    plt.show()

def plot_correlation(dat):
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=dat, x = 'Temperature', y = 'Load', alpha = 0.5)
    plt.title ("...")
    plt.xlabel("nhiệt độ")
    plt.ylabel('phụ tải(kW)')
    plt.grid(True)
    plt.show()

def box_plot(dat):
    plt.figure(figsize=(6,4))
    sns.boxplot(y=dat, color = 'orange')
    plt.title('kiểm tra giá trị ngoại lai của phụ tải')
    plt.show()

def check_missing_data_auto():
    print(df.isnull().sum())

    # Dùng phương pháp nội suy tuyến tính để điền vào chỗ trống
    # df['Load'] = df['Load'].interpolate(method='linear')
    # print(df.isnull().sum())


def manual_check(narr):
    narr = narr.copy()
    n = len(narr)

    i = 0

    while i<n:
        if np.isnan(narr[i]):
            start = i 
            while i < n and np.isnan(narr[i]):
                i += 1
            
            left = start - 1
            right = i 

            if left >= 0  and right <n: 
                y1 = narr[left]
                y2 = narr[right]
                length = right - left

                for k in range (1, length):
                    narr[left + k] = y1 + (y2-y1)*k/length
        else:
            i+= 1    

    return narr



def check_missing_data_manual():
    
    df['Load'] = manual_check(df['Load'])

    print(df['Load'].isnull().sum())


def check_outliers():
    mean_load = df['Load'].mean()
    std_load = df['Load'].std()
    print(mean_load, std_load)
    lower_bound = mean_load - 3*std_load
    upper_bound = mean_load + 3 * std_load
    
    outliers = df[(df['Load'] < lower_bound) | (df['Load'] > upper_bound)]

    
    print(outliers)

    df.loc[(df['Load'] < lower_bound) | (df['Load'] > upper_bound), 'Load'] = mean_load
    df.loc[(df['Load']< 0), 'Load'] = mean_load
    #chỉ cách loại bỏ giá trị ngoại lai thay vì thay bằng mean
    return

def check_outliers_iqr():
    Q1 = df['Load'].quantile(0.25)
    Q3 = df['Load'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    mean_load = df['Load'].median()

   
    outliers = df[(df['Load'] < lower_bound) | (df['Load'] > upper_bound)]
    
    print(outliers)

    df.loc[(df['Load'] < lower_bound) | (df['Load'] > upper_bound), 'Load'] = mean_load
    return

def check_duplicates():
    num_duplicates = df.duplicated().sum()
    

    num_time_duplicates = df.duplicated(subset=['Timestamp']).sum()
    
    
    if num_time_duplicates > 0:
        print(df[df.duplicated(subset=['Timestamp'], keep=False)].sort_values(by='Timestamp'))

    df = df.drop_duplicates(keep='first')

    # Gom nhóm theo Timestamp và tính trung bình cho các cột số
    df = df.groupby('Timestamp', as_index=False).mean()
    print("Đã xử lý trùng lặp xong. Kích thước dữ liệu hiện tại:", df.shape)


def normalization_min_max(series):
    min_val = series.min()
    max_val = series.max()
    normalized_series = (series - min_val) / (max_val - min_val)
    return normalized_series

def normalization_z_score(series):
    mean_val = series.mean()
    std_val = series.std()
    normalized_series = (series - mean_val) / std_val
    return normalized_series


def normalization():
    df['Load'] = normalization_min_max(df['Load']) 

    return



if __name__=='__main__':
    # plot_correlation()
    # box_plot()
    # check_missing_data_auto()
    check_missing_data_manual()
    # check_outliers()
    check_outliers_iqr()

    normalization()
    # plot_load(df['Load'])
    plot_correlation(df)
    box_plot(df['Load'])
    


