#! python3
# _*_ coding: utf-8 _*_
# Author: Winson
# User: sanmu
# Date: 2018/6/25 21:29
# Project: MyTools
# File Name: pil_to_sketch.py


# from PIL import Image
import PIL.Image
import numpy as np
import os
import join
import time
import traceback


def image(sta, end, depths=10):

    path = repr(os.getcwd())
    print(path)
    try:
        # im = PIL.Image.open(path + '\\photo.jpg')
        # print(im.size)

        a = np.asarray(PIL.Image.open(sta).convert('L')).astype('float')
    except:
        print(traceback.print_exc())
    else:
        depth = depths  # (0-100)
        grad = np.gradient(a) # 取图像灰度的梯度值
        grad_x, grad_y = grad # 分别取横纵图像梯度值
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A
        vec_el = np.pi / 2.2 # 光源的俯视角度，弧度值
        vec_az = np.pi / 4. # 光源的方位角度，弧度值
        dx = np.cos(vec_el) * np.cos(vec_az) # 光源对x 轴的影响
        dy = np.cos(vec_el) * np.sin(vec_az) # 光源对y 轴的影响
        dz = np.sin(vec_el) # 光源对z 轴的影响
        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z) # 光源归一化
        b = b.clip(0, 255)
        im = PIL.Image.fromarray(b.astype('uint8'))  # 重构图像
        im.save(end)


def mains(numbers):
    number = int(numbers)
    print(number)
    startss = os.listdir(".\输入----图片")
    print(startss)
    time.sleep(2)
    for starts in startss:
        start = ''.join(starts)
        # start = 'photo.jpg'
        print('正在转化--图片： ' + start)
        sta = './' + '输入----图片/' + start
        end = './' + '输出----图片/' + 'HD_20' + start
        # sta = start
        # end = 'HD_20' + start
        image(sta=sta, end=end, depths=number)
# 简单来说，就是利用python的Numpy库，将图像降维转化为数字化的数据，之后对数据进行操作，再利用pillow库将操作好的数据转化为素描效果的图片。
# GUI图形界面程序
# main.py
# from image import mains
from tkinter import *


def exists_mkdir():
    if os.path.exists('输出----图片') and os.path.exists('输入----图片'):
        pass
    else:
        os.mkdir('输出----图片')
        os.mkdir('输入----图片')


def images():
    try:
        s1 = e1.get()
        a = mains(s1)
        c["text"] = "我们的程序运行成功了"
    except Exception:
        c["text"] = "程序运行出错了,可能是缺少了两个配置文件"
#创建程序运行需要的工作目录
exists_mkdir()
tk = Tk()
# 设置窗口大小和位置
tk.geometry('430x350+80+60')
# 不允许改变窗口大小
tk.resizable(False, False)
## 用来显示Label组件
tk.title('素描图生成器')
w1 = Label(tk, text='作者博客')
w = Label(tk, text='')
w2 = Label(tk, text='欢迎使用：')
w3 = Label(tk, text='步骤一：将需要转化的图片放入 输入----图片 文件夹下')
w4 = Label(tk, text='步骤二：输入 0-100的数值，数值越大，颜色越深。--------标准参数是 10 ')
w5 = Label(tk, text='步骤三：点击确认 运行程序 等待出现提示')
w6 = Label(tk, text='步骤四：到输入----图片 文件夹找到素描图')
w1.grid(row=0, column=0, sticky=W)
w.grid(row=1, column=0, sticky=W)
w2.grid(row=2, column=0, sticky=W)
w3.grid(row=3, column=0, sticky=W)
w4.grid(row=4, column=0, sticky=W)
w5.grid(row=5, column=0, sticky=W)
w6.grid(row=6, column=0, sticky=W)
l = Label(tk, text="输入 0-100的数值")
l.grid(row=8, column=0, sticky=E)
## 用来显示输入框
e1 = Entry(tk)
e1.grid(row=10, column=0, sticky=E)
## 用来显示Button
b = Button(tk, text='确定', command=images)
b.grid(row=12, column=0, sticky=E)
c = Label(tk, text="", background="yellow")
c.grid(row=15)
# 启动消息主循环
tk.mainloop()
