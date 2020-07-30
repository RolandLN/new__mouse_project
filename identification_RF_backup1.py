# encoding='UTF-8'


import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'
url1 = pd.read_csv('data_txt.txt', header=None, engine='python').replace(0, np.nan)

for column in list(url1.columns[url1.isnull().sum() > 0]):  # 均值填充
    mean_val = url1[column].mean()
    url1[column].fillna(mean_val, inplace=True)
# url1 = pd.read_csv(url, header=None, engine='python')
print(url1)
# print(url1.values)
# url1 = pd.DataFrame(url1)
# df = pd.read_csv(url1,header=None)
url1.columns = ['Class label', "NONE_number", "L_number", "R_number", "LL_number", "J_number", "S", "V1", "V2", "V3",
                "V4", "V5", "D1", "D2", "D3", "D4", "D5", "L_time", "R_time", "LL_time", "J_time"]
# print(url1.columns)

# 查看几个标签
# Class_label = np.unique(url1['Class label'])
# print(Class_label,)
# 查看数据信息
# info_url = url1.info()
# print(info_url,'.......................')
# 下面将数据集分为训练集和测试集
# print(type(url1))
# url1 = url1.values
# x = url1[:,0]
# y = url1[:,1:]
print("....................")
x, y = url1.iloc[:, 1:].values, url1.iloc[:, 0].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
feat_labels = url1.columns[1:]
print(".....................")
# print(feat_labels)
# n_estimators：树的数量
# n_jobs  整数 可选（默认=1） 适合和预测并行运行的作业数，如果为-1，则将使用全部cpu
forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=-1)
forest.fit(x_train, y_train)
print(forest.score(x_test, y_test))


# 下面对训练好的随机森林，完成重要性评估
# feature_importances_  可以调取关于特征重要程度
importances = forest.feature_importances_
print("重要性：", importances)
x_columns = url1.columns[1:]
indices = np.argsort(importances)[::-1]
print("重要性索引顺序: ", indices, '...............')

for f in range(x_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))

# 筛选变量（选择重要性比较高的变量）
threshold = 0.15
x_selected = x_train[:, importances > threshold]
# print(x_selected)

# 可视化
plt.figure(figsize=(10, 6))
plt.title("特征数据集中各个特征的重要程度", fontsize=18)
plt.ylabel("import level", fontsize=15, rotation=90)
plt.rcParams['font.sans-serif'] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

x_columns1 = [x_columns[i] for i in indices]
print(x_columns1)
print("-------------------")

for i in range(x_columns.shape[0]):
    plt.bar(i, importances[indices[i]], color='orange', align='center')
    plt.xticks(np.arange(x_columns.shape[0]), x_columns1, rotation=90, fontsize=15)
plt.show()
