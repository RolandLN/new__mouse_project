#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author：liuneng
import pythoncom
import pyHook
import time
import threading

a = False
b = False
# c = False
# d = False


def onmouse_leftdown(event):
    # 监听鼠标左键按下事件
    global Ldown_num, a
    a = False
    Ldown_num += 1
    print("left DOWN " + str(Ldown_num))
    a = True

    return True
    # 返回 True 表示响应此事件，False表示拦截


def onmouse_leftup(event):
    # 监听鼠标左键弹起事件
    global Lup_num, b
    b = False
    Lup_num += 1
    print("left UP " + str(Lup_num))
    b = True

    return True


# def onMouse_rightdown(event):
#     # 监听鼠标右键按下事件
#     global Rdown_num, c
#     c = False
#     Rdown_num += 1
#     print("right DOWN " + str(Rdown_num))
#     c = True
#
#     return True
#
#
# def onMouse_rightup(event):
#     # 监听鼠标右键弹起事件
#     global RTup_num, d
#     d = False
#     RTup_num += 1
#     print("right UP " + str(RTup_num))
#     d = True
#
#     return True


def onmouseevent(event):
    # "处理鼠标position事件"
    global a, b, c, d
    # fobj.writelines('ME.B  ')
    # fobj.writelines("%f  " % time.time())
    # fobj.writelines("%s" % time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    # fobj.writelines("MessageName:%s\n" % str(event.MessageName))
    # fobj.writelines("Message:%d\n" % event.Message)
    # fobj.writelines("Time_sec:%d\n" % event.Time)
    # fobj.writelines("Window:%s" % str(event.Window))
    # fobj.writelines("%s " % str(event.WindowName))
    # fobj.writelines("%s  " % str(event.Position))

    # 调用鼠标button函数
    if a:
        fobj.writelines("%f  " % time.time())
        fobj.writelines('LFDW ')
        fobj.writelines("%s  " % str(event.Position))
        fobj.writelines('\n')
        # a = False
    elif b:
        fobj.writelines("%f  " % time.time())
        fobj.writelines('LFUP ')
        fobj.writelines("%s  " % str(event.Position))
        # b = False
    # elif c:
        # fobj.writelines('RGDW ')
        # c = False
    # elif d:
        # fobj.writelines('RGUP ')
        # d = False
    # else:
    #     fobj.writelines('NONE ')

    # fobj.writelines('\n')
    return True


def main(hm1):

    hm1.MouseLeftDown = onmouse_leftdown

    hm1.MouseLeftUp = onmouse_leftup

    # hm1.MouseRightDown = onMouse_rightdown

    # hm1.MouseRightUp = onMouse_rightup

    hm1.HookMouse()

    # 进入循环，如不手动关闭，程序将一直处于监听状态


if __name__ == "__main__":

    # 打开日志文件
    T = input("请输入姓名首字母并按序输入录入次数（0,1,2....10）\n：")
    file_name = "D:\pycharm\pydataZ\mouse" + T + " .text"
    fobj = open(file_name, 'a')

    # 新线程执行的代码:
    print('thread %s is running...' % threading.current_thread().name)

    # 创建hook句柄
    hm = pyHook.HookManager()

    # 监控鼠标position
    hm.MouseAll = onmouseevent
    hm.HookMouse()

    # 监控鼠标button命令
    Ldown_num = 0
    Lup_num = 0
    Rdown_num = 0
    RTup_num = 0
    main(hm)

    # 循环获取消息
    pythoncom.PumpMessages()

    # 关闭日志文件
    fobj.close()
