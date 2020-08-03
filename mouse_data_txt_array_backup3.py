# coding = "UTF-8"
# author：roland
# 将鼠标原始数据提取出各项特征到txt_file中


import sys


user_number = "8"
txt_file_place = open("D:/pyfile/project/biyelunwen/data_txt_v0_3.txt", "a")
raw_data_place = r"E:\论文\data\2018鼠标数据集\Retlatijoum_Njoou_Nion\mouse-2019-01-08-13-21-44.txt"

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
        # D2 = 0
        # D3 = 0
        # D4 = 0
        # D5 = 0        # 前后两指针位置无变化
        # X_Last = 0    # 假定开始时指针在（0，0）处，对统计结果几乎没有影响
        # Y_Last = 0
        # S = 0          # 1000个数据距离和
        # First_time    # 第一个数据的时间
        # V1 = 0        # 速度在0-100的次数
        # V2 = 0        # 速度在100-200的次数
        # V3 = 0        # 速度在200-300的次数
        # V4 = 0        # 速度在300-400的次数
        # V5 = 0        # 前后两次数据时间差为0，时间刻度没有捕获到时间差，速度描述为V5，速度非常大。
        Eigenvalue_dict = {"i": 0, "NONE_number": 0, "L_number": 0, "L_time": 0, "R_number": 0, "R_time": 0,
                           "LFDW": 0, "LFUP": 0, "RGDW": 0, "LL_time": 0, "LL_number": 0, "J_number": 0,
                           "J_time": 0, "last_time": 0, "D1": 0, "D2": 0, "D3": 0, "D4": 0, "X_Last": 0,
                           "Y_Last": 0, "D5": 0, "S": 0, "First_time": 0, "V1": 0, "V2": 0, "V3": 0, "V4": 0,
                           "V5": 0}    # 特征字典

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
            except:
                continue
            if X > Eigenvalue_dict["X_Last"] and Y >= Eigenvalue_dict["Y_Last"]:  # 移动方向
                Eigenvalue_dict["D1"] += 1
            if X >= Eigenvalue_dict["X_Last"] and Y < Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D2"] += 1
            if X < Eigenvalue_dict["X_Last"] and Y <= Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D3"] += 1
            if X <= Eigenvalue_dict["X_Last"] and Y > Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D4"] += 1
            if X == Eigenvalue_dict["X_Last"] and Y == Eigenvalue_dict["Y_Last"]:
                Eigenvalue_dict["D5"] += 1

            if Eigenvalue_dict["i"] != 0:    # 移动距离以及速度
                B_A_Ditence = ((X-Eigenvalue_dict["X_Last"])**2 + (Y-Eigenvalue_dict["Y_Last"])**2)**0.5  # 前后两次数据距离
                B_A_Time = float(float(line_list[0]) - Eigenvalue_dict["First_time"])  # 前后两次数据时间差
                if B_A_Time >= 50:
                    break
                Eigenvalue_dict["S"] += B_A_Ditence
                if B_A_Time == 0:   # 速度较高的表现，时间刻度无法区分两数据时间差
                    Eigenvalue_dict["V5"] += 1
                else:
                    if 0 < B_A_Ditence/B_A_Time < 100:   # 等于0时，视为静止状态
                        Eigenvalue_dict["V1"] += 1
                    if 100 <= B_A_Ditence/B_A_Time < 200:
                        Eigenvalue_dict["V2"] += 1
                    if 200 <= B_A_Ditence/B_A_Time < 300:
                        Eigenvalue_dict["V3"] += 1
                    if 300 <= B_A_Ditence/B_A_Time < 400:
                        Eigenvalue_dict["V4"] += 1

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
                    J_time = round(Eigenvalue_dict["J_time"]/Eigenvalue_dict["J_number"], 3)

                S = round(Eigenvalue_dict["S"]/999, 3)
                if Eigenvalue_dict["L_number"] == 0:
                    L_time = 0
                else:
                    L_time = round(Eigenvalue_dict["L_time"]/Eigenvalue_dict["L_number"], 3)

                if Eigenvalue_dict["R_number"] == 0:
                    R_time = 0
                else:
                    R_time = round(Eigenvalue_dict["R_time"]/Eigenvalue_dict["R_number"], 3)
                if Eigenvalue_dict["LL_number"] == 0:
                    LL_time = 0
                else:
                    LL_time = round(Eigenvalue_dict["LL_time"]/Eigenvalue_dict["LL_number"], 3)

                txt_file_place.write(
                    user_number + "," + str(Eigenvalue_dict["NONE_number"]) + "," + str(Eigenvalue_dict["L_number"])
                    + "," + str(Eigenvalue_dict["R_number"]) + "," + str(Eigenvalue_dict["LL_number"]) + ","
                    + str(Eigenvalue_dict["J_number"]) + "," + str(S) + ","
                    + str(Eigenvalue_dict["V1"]) + "," + str(Eigenvalue_dict["V2"]) + "," + str(Eigenvalue_dict["V3"])
                    + "," + str(Eigenvalue_dict["V4"]) + "," + str(Eigenvalue_dict["V5"]) + ","
                    + str(Eigenvalue_dict["D1"]) + "," + str(Eigenvalue_dict["D2"]) + "," + str(Eigenvalue_dict["D3"])
                    + "," + str(Eigenvalue_dict["D4"]) + "," + str(Eigenvalue_dict["D5"]) + "," + str(L_time) + ","
                    + str(R_time) + "," + str(LL_time) + "," + str(J_time) + "\n")
                txt_file_place.flush()
                break   # 此处break不能省略!!!!!

        continue
