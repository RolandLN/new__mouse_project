# coding = "UTF-8"
# author：roland
# 将鼠标原始数据提取出各项特征到txt_file中
# 有以下统计量的方差信息V1-4速度值以及其方差，S及其方差
# 共提取特征29个
# 解决了空列表np.mean()、np.var()两个方法产生的nan值问题


import sys
import numpy as np


user_number = "8"
txt_file_place = open("D:/pyfile/project/biyelunwen/data_txt_v29_12345678_no_nan.txt", "a")
raw_data_place = r"E:\论文\data\2018鼠标数据集\Retlatijoum_Njoou_Nion\mouse-2019-01-04-08-24-34.txt"

with open(raw_data_place, "r") as file:
    while True:
        # i = 0   # 数据个数
        # NONE_number = 0    # ..移动事件个数
        # L_number = 0  # ..左键单击事件个数
        # R_number = 0  # ..右键单击事件个数
        # L_time = 0    # 所有左键单击间隔时间之和（L_time/L_number为单击时间间隔的均值）
        # R_time = 0    # 所有右键单击间隔时间之和（同上）
        # LFDW = 0      # ..左键按下时间
        # LFUP = 0      # ..左键弹起时间
        # RGDW = 0      # ..右键按下时间
        # LL_time = 0   # 所有双击事件事件间隔之和（LL_time/LL_number为一组数据左键双击时间间隔的均值)
        # J_number = 0  # 静止事件次数（两个数据时间间隔在0.5s-3.0秒之间的事件为静止事件）
        # J_time = 0    # 每组数据静止事件静止时间之和（J_time/J_number为一组数据静止事件事件均值)
        # last_time = 0 # 记录上一次事件的时间
        # D1 = 0        # D1方向上的移动次数
        # D2_number = 0
        # D3_number = 0
        # D4_number = 0
        # D5_number = 0        # 前后两指针位置无变化
        # X_Last = 0    # 假定开始时指针在（0，0）处，对统计结果几乎没有影响
        # Y_Last = 0
        # s_list = []   # 两个数据之间的距离列表
        # First_time    # 第一个数据的时间

        # v1_list = []  # 一个样本内速度v1的列表
        # v2_list = []  #
        # v3_list = []  #
        # v4_list = []  #

        # V1_number = 0        # 速度在0-100的次数
        # V2_number = 0        #
        # V3_number = 0        #
        # V4_number = 0        #
        # V5_number = 0        # 前后两次数据时间差为0，时间刻度没有捕获到时间差，速度描述为V5，速度非常大。
        Eigenvalue_dict = {"i": 0, "NONE_number": 0, "L_number": 0, "L_time": 0, "R_number": 0, "R_time": 0,
                           "LFDW": 0, "LFUP": 0, "RGDW": 0, "LL_time": 0, "LL_number": 0, "J_number": 0,
                           "J_time": 0, "last_time": 0, "D1_number": 0, "D2_number": 0, "D3_number": 0, "D4_number": 0,
                           "X_Last": 0, "Y_Last": 0, "D5_number": 0, "s_list": [], "First_time": 0, "V5_number": 0,
                           "v1_list": [], "v2_list": [], "v3_list": [], "v4_list": []}    # 特征字典

        for line in file:
            line_list = line.strip().split("  ")  # 两个空格
            # print(line_list)
            if len(line_list) < 4 or line == "":  # 判断最后一行是否完整，确保提取完整事件名
                txt_file_place.close()
                print("数据读取完毕")
                sys.exit()

            action = line_list[2][0:4]    # 鼠标事件类型（NONE、LFDW、LFUP、RGDW、RGUP）

            # -----指针移动方向-----以及距离----速度-------(X,Y)为指针坐标-----
            try:
                X = int(line_list[1].partition("(")[2].partition(",")[0][:])
                print(line_list[0])
                Y = int(line_list[1].partition(" ")[2].partition(")")[0])
            except BaseException:
                continue
            if X > Eigenvalue_dict["X_Last"] and Y >= Eigenvalue_dict["Y_Last"]:  # 移动方向
                Eigenvalue_dict["D1_number"] += 1
            if X >= Eigenvalue_dict["X_Last"] and Y < Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D2_number"] += 1
            if X < Eigenvalue_dict["X_Last"] and Y <= Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D3_number"] += 1
            if X <= Eigenvalue_dict["X_Last"] and Y > Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D4_number"] += 1
            if X == Eigenvalue_dict["X_Last"] and Y == Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D5_number"] += 1

            if Eigenvalue_dict["i"] != 0:    # 移动距离以及速度
                B_A_Ditence = ((X-Eigenvalue_dict["X_Last"])**2 + (Y-Eigenvalue_dict["Y_Last"])**2)**0.5  # 前后两次数据距离
                B_A_Time = float(float(line_list[0]) - Eigenvalue_dict["First_time"])  # 前后两次数据时间差
                if B_A_Time >= 50:          # 剔除伪鼠标静止动作
                    break
                # Eigenvalue_dict["S"] += B_A_Ditence
                Eigenvalue_dict["s_list"].append(B_A_Ditence)
                if B_A_Time == 0:   # 速度较高的表现，毫秒刻度无法区分前后两数据时间差
                    Eigenvalue_dict["V5_number"] += 1
                else:
                    V_B_A = B_A_Ditence / B_A_Time
                    if 0 < V_B_A < 100:   # 等于0时，视为静止状态
                        Eigenvalue_dict["v1_list"].append(V_B_A)
                        # Eigenvalue_dict["V1_number"] += 1
                    if 100 <= V_B_A < 200:
                        # Eigenvalue_dict["V2_number"] += 1
                        Eigenvalue_dict["v2_list"].append(V_B_A)
                    if 200 <= V_B_A < 300:
                        # Eigenvalue_dict["V3_number"] += 1
                        Eigenvalue_dict["v3_list"].append(V_B_A)
                    if 300 <= V_B_A < 400:
                        # Eigenvalue_dict["V4_number"] += 1
                        Eigenvalue_dict["v4_list"].append(V_B_A)

            Eigenvalue_dict["First_time"] = float(line_list[0])
            Eigenvalue_dict["X_Last"] = X
            Eigenvalue_dict["Y_Last"] = Y
            # ................................................................

            # --------真静止事件次数--------------------------------------------
            Time_interval = float(line_list[0]) - Eigenvalue_dict["last_time"]
            # print(Time_interval)
            if 0.5 <= Time_interval <= 5:
                Eigenvalue_dict["J_number"] += 1
                Eigenvalue_dict["J_time"] += Time_interval
            Eigenvalue_dict["last_time"] = float(line_list[0])
            # ..............................................

            # 鼠标NONE（移动）事件计数 其他特征---------------------------------
            if action == "NONE":
                Eigenvalue_dict["NONE_number"] += 1
                # print("NONE_number", Eigenvalue_dict["NONE_number"])
            # ...............................................

            # 鼠标左键单键时间间隔---单击事件个数---左键双击事件个数---以及双击时间间隔
            if action == "LFDW":
                Eigenvalue_dict["LFDW"] = float(line_list[0])
                if Eigenvalue_dict["LFDW"] - Eigenvalue_dict["LFUP"] < 1.5:   # 判断为左键双击事件(事件间隔1.5以内为双击事件）
                    Eigenvalue_dict["LL_number"] += 1
                    Time_interval = float(line_list[0]) - Eigenvalue_dict["LFUP"]
                    Eigenvalue_dict["LL_time"] += Time_interval
            if action == "LFUP":          # 单击事件
                Eigenvalue_dict["LFUP"] = float(line_list[0])
                Eigenvalue_dict["L_number"] += 1
                Time_interval = float(line_list[0]) - Eigenvalue_dict["LFDW"]
                if Time_interval <= 2:
                    # Eigenvalue_dict["L_time"] = (Eigenvalue_dict["L_time"]+Time_interval)
                    Eigenvalue_dict["L_time"] += Time_interval
                    # print(Eigenvalue_dict["L_time"], Eigenvalue_dict["LFDW"], line_list[0])
                    # print("L_time", Eigenvalue_dict["L_time"])
                else:
                    pass
            # ................................................

            # 鼠标右键击键时间间隔-----右击事件个数----------------------
            if action == "RGDW":
                Eigenvalue_dict["RGDW"] = float(line_list[0])
            if action == "RGUP":
                Eigenvalue_dict["R_number"] += 1
                Time_interval = (float(line_list[0]) - float(Eigenvalue_dict["RGDW"]))
                if Time_interval <= 2:
                    # Eigenvalue_dict["R_time"] = (Eigenvalue_dict["R_time"]+Time_interval)
                    Eigenvalue_dict["R_time"] += Time_interval
                    # print("R_time", Eigenvalue_dict["R_time"])
                else:
                    pass
            # ...............................................

            Eigenvalue_dict["i"] += 1
            # print("data_nume",i)
            if Eigenvalue_dict["i"] >= 1000:    # 每一千个数据为一组提取特征
                if Eigenvalue_dict["J_number"] == 0:
                    J_time = 0
                else:
                    J_time = round(Eigenvalue_dict["J_time"]/Eigenvalue_dict["J_number"], 2)

                # S = round(Eigenvalue_dict["S"]/999, 3)
                if Eigenvalue_dict["L_number"] == 0:
                    L_time = 0
                else:
                    L_time = round(Eigenvalue_dict["L_time"]/Eigenvalue_dict["L_number"], 2)

                if Eigenvalue_dict["R_number"] == 0:
                    R_time = 0
                else:
                    R_time = round(Eigenvalue_dict["R_time"]/Eigenvalue_dict["R_number"], 2)
                if Eigenvalue_dict["LL_number"] == 0:
                    LL_time = 0
                else:
                    LL_time = round(Eigenvalue_dict["LL_time"]/Eigenvalue_dict["LL_number"], 2)

                # 前六个字段
                txt_file_place.write(
                    user_number + "," + str(Eigenvalue_dict["NONE_number"]) + "," + str(Eigenvalue_dict["L_number"])
                    + "," + str(Eigenvalue_dict["R_number"]) + "," + str(Eigenvalue_dict["LL_number"]) + ","
                    + str(Eigenvalue_dict["J_number"]) + ",")

                # 第7-8字段
                s_list_mean = 0 if np.isnan(np.mean(Eigenvalue_dict["s_list"])) else np.round(np.mean(Eigenvalue_dict["s_list"]), 2)
                s_list_var = 0 if np.isnan(np.var(Eigenvalue_dict["s_list"])) else np.round(np.var(Eigenvalue_dict["s_list"]), 2)
                txt_file_place.write(str(s_list_mean) + "," + str(s_list_var) + ",")

                # 第9-12字段
                for v_list in ["v1_list", "v2_list", "v3_list", "v4_list"]:
                    txt_file_place.write(str(len(Eigenvalue_dict[v_list])) + ",")

                # 第13字段
                txt_file_place.write(
                    str(Eigenvalue_dict["V5_number"]) + ",")

                # 第14-21字段
                for list_name in ["v1_list", "v2_list", "v3_list", "v4_list"]:
                    list_mean = 0 if np.isnan(np.mean(Eigenvalue_dict[list_name])) else np.round(np.mean(Eigenvalue_dict[list_name]), 2)
                    list_var = 0 if np.isnan(np.var(Eigenvalue_dict[list_name])) else np.round(np.var(Eigenvalue_dict[list_name]), 2)
                    txt_file_place.write(str(list_mean) + "," + str(list_var) + ",")

                # 第22到26字段
                for D_number in ["D1_number", "D2_number", "D3_number", "D4_number", "D5_number"]:
                    txt_file_place.write(str(Eigenvalue_dict[D_number]) + ",")

                # 第27到30字段
                txt_file_place.write(str(L_time) + "," + str(R_time) + "," + str(LL_time) + "," + str(J_time) + "\n")
                txt_file_place.flush()
                break   # 此处break不能省略!!!!!

        continue
