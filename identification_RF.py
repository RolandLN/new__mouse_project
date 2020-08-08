# encoding='UTF-8'
# author：roland
# RF进行分类并计算特征重要度

import time
import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


txt_name = 'data_txt_v29_12345678_no_nan.txt'   # 特征向量矩阵txt文件名

start_time = time.time()
url1 = pd.read_csv(txt_name, header=None, engine='python', dtype="float64")
#     .replace(0, np.nan)

# for column in list(url1.columns[url1.isnull().sum() > 0]):
#     mean_val = url1[column].mean()
#     url1[column].fillna(mean_val, inplace=True)
# print(np.isnan(url1).any())
# url1.dropna(inplace=True)   # 删除有缺失值的行
print(url1)

url1.columns = ['Class label', "NONE_number", "L_number", "R_number", "LL_number", "J_number", "S_mean", "S_var",
                "V1_number", "V2_number", "V3_number", "V4_number", "V5_number",
                "v1_mean", "v1_var", "v2_mean", "v2_var", "v3_mean", "v3_var", "v4_mean", "v4_var",
                "D1", "D2", "D3", "D4", "D5", "L_time", "R_time", "LL_time", "J_time"]

x, y = url1.iloc[:, 1:].values, url1.iloc[:, 0].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
feat_labels = url1.columns[1:]
# n_estimators：树的数量
# n_jobs  整数 可选（默认=1） 适合和预测并行运行的作业数，如果为-1，则将使用全部cpu
forest = RandomForestClassifier(n_estimators=10000, random_state=0, n_jobs=10)
forest.fit(x_train, y_train)
print("文本文件：", txt_name)
print("测试集表现结果：", forest.score(x_test, y_test))


# 下面对训练好的随机森林，完成重要性评估
# feature_importances_  可以调取关于特征重要程度
importances = forest.feature_importances_
# print("重要性：", importances)
x_columns = url1.columns[1:]
indices = np.argsort(importances)[::-1]
print("重要性索引顺序: ", indices)

for f in range(x_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30, feat_labels[indices[f]], importances[indices[f]]))

# 可视化
plt.figure(figsize=(10, 6))
plt.title(txt_name + "特征数据集中各个特征的重要程度", fontsize=18)
plt.ylabel("import level", fontsize=15, rotation=90)
plt.rcParams['font.sans-serif'] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

x_columns1 = [x_columns[i] for i in indices]
print(x_columns1)

for i in range(x_columns.shape[0]):
    plt.bar(i, importances[indices[i]], color='orange', align='center')
    plt.xticks(np.arange(x_columns.shape[0]), x_columns1, rotation=90, fontsize=15)
plt.show()
end_time = time.time()

print("程序完成时间： ", end_time - start_time)
sys.exit()
