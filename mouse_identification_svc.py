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


txt_name = 'data_txt_v0_3.txt'   # 特征向量txt文件名
feature_number = 18  # 选择的特征数
# feature_list = [7, 10, 5, 8, 15, 6, 9, 16, 0, 4, 3, 1, 12, 14, 13, 18, 19, 11, 2, 17]  # small_txt特征重要度索引排序
# feature_list = [7, 15, 5, 8, 10, 6, 9, 4, 0, 16, 14, 1, 12, 3, 13, 11, 19, 18, 17, 2]  # middle_txt
# feature_list = [10, 7, 6, 5, 8, 15, 9, 16, 0, 1, 4, 3, 12, 14, 11, 18, 13, 19, 17, 2]  # v0_txt
# feature_list = [6, 10, 7, 5, 15, 8, 9, 0, 16, 1, 4, 12, 3, 14, 18, 11, 13, 19, 17, 2]  # v0_1_txt
# feature_list = [7, 6, 8, 10, 5, 15, 9, 16, 0, 4, 1, 12, 3, 14, 13, 11, 19, 18, 17, 2]  # v0_2_txt
feature_list = [7, 6, 8, 10, 5, 15, 9, 4, 0, 1, 14, 16, 12, 18,  3, 13, 11, 19, 17, 2]  # v0_3_txt
# feature_list = [7, 5, 15, 8, 6, 10, 9, 16, 4, 0, 1, 3, 14, 12, 13, 11, 19, 18, 17, 2]  # v01_txt
# feature_list = [6, 7, 10, 8, 15, 5, 9, 0, 1, 4, 3, 16, 14, 12, 18, 13, 11, 19, 2, 17]  # v02_txt
# feature_list = [7, 6, 8, 5, 15, 10, 9, 0, 4, 16, 3, 1, 14, 18, 12, 13, 11, 19, 2, 17]  # v03_txt
# feature_list = [7, 15, 8, 10, 5, 6, 9, 4, 0, 1, 14, 16, 11, 13, 12, 19, 18, 3, 17, 2]  # v04_txt


# 获取数据
start_time = time.time()
origin_data = pd.read_csv(txt_name, header=None, engine="python")
#     .replace(0, np.nan)
# for column in list(origin_data.columns[origin_data.isnull().sum() > 0]):  # 均值填充
#     mean_val = origin_data[column].mean()
#     origin_data[column].fillna(mean_val, inplace=True)
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
