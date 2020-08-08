# coding="UTF-8"
# author: roland

import time
import sys
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV


txt_name = 'data_txt_v29_12345678_no_nan.txt'   # 特征向量txt文件名
feature_number = 16  # 选择的特征数
# feature_list = [11,19, 18, 7, 8, 6, 5, 9, 24, 10, 17, 16, 14, 15, 12, 4, 25, 0, 13, 1, 28, 3, 21, 20, 22, 23, 27, 26, 2]  # v29_123456_txt
# feature_list = [8, 7, 11, 18, 9, 6, 15, 12, 16, 19, 5, 24, 17, 10, 14, 13, 0, 25, 1, 4, 21, 3, 23, 27, 22, 20, 28, 26, 2]  # v29_123457_txt
# feature_list = [8, 14, 18, 19, 11, 9, 6, 15, 5, 7, 16, 12, 24, 10, 17, 13, 25, 0, 1, 3, 4, 21, 22, 23, 20, 28, 27, 26, 2]  # v29_1234567_no_nan_txt
feature_list = [8, 14, 18, 11, 9, 19, 6, 7, 16, 15, 5, 17, 24, 10, 12, 13, 4, 3, 25, 0, 1, 27, 23, 21, 22, 28, 20, 26, 2]  # v29_12345678_no_nan_txt
# feature_list = [8, 24, 18, 14, 9, 19, 16, 17, 11, 7, 6, 15, 5, 12, 10, 13, 4, 25, 0, 3, 1, 23, 20, 21, 22, 28, 27, 26, 2]  # v29_1-11_txt
# feature_list = [8, 18, 14, 19, 11, 9, 6, 16, 7, 15, 5, 17, 24, 12, 10, 13, 4, 25, 3, 0, 23, 21, 22, 20, 1, 27, 28, 26, 2]# v29_1-11_txt


# 获取数据
start_time = time.time()
origin_data = pd.read_csv(txt_name, header=None, engine="python")
#     .replace(0, np.nan)

# for column in list(origin_data.columns[origin_data.isnull().sum() > 0]):  # 均值填充，通过列表对不同列不同缺失值方案
#     mean_val = origin_data[column].mean()
#     origin_data[column].fillna(mean_val, inplace=True)
# print(np.isnan(origin_data).any())
# origin_data.dropna(inplace=True)   # 删除有缺失值的行
print(origin_data)


X = origin_data.iloc[:, 1:].values
Y = origin_data.iloc[:, 0].values

# 按照特征的重要性排序的所有特征
all_feature = feature_list
# 这里我们选取前N个特征
topN_feature = all_feature[:feature_number]

# 获取重要特征的数据
data_X = X[:, topN_feature]

# 原始数据标准化，为了加速收敛
# 最小最大规范化,对原始数据进行线性变换，变换到[0,1]区间
data_X = preprocessing.MinMaxScaler().fit_transform(data_X)

# 利用train_test_split 进行训练集和测试集进行分开
X_train, X_test, y_train, y_test = train_test_split(data_X, Y, train_size=0.7, test_size=0.3)

# 网格搜索,调参
C_range = np.logspace(-1, 3, 40)  # logspace(a,b,N)把10的a次方到10的b次方区间分成N份
gamma_range = np.logspace(-2, 2, 40)
param_grid = dict(gamma=gamma_range, C=C_range)
grid = GridSearchCV(SVC(kernel="rbf"), param_grid=param_grid, cv=5, n_jobs=10)  # 基于5折交叉验证的网格搜索。
grid.fit(X_train, y_train)

print("The best parameters are %s with a score of %0.4f"
      % (grid.best_params_, grid.best_score_))  # 找到最佳超参数

end_time = time.time()
print("数据文件：", txt_name)
print("选择特征数： ", feature_number)
print("测试集表现结果：", grid.score(X_test, y_test))
print("程序完成时间： ", end_time - start_time)
sys.exit()
