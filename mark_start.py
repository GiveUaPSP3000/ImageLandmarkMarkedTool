
# -*- coding:utf-8 -*-

from __future__ import division
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import os
import numpy as np

# 存储照片的文件名
image_filename = 'original_images/'
# 存储标签的文件名
labeling_filename = 'labeling_images/'
# 标签文件名
label_txt = 'label.csv'
# 标签点
label_list = ['Left_Eye_(Left)',
              'Left_Eye(Top)',
              'Left_Eye_(Right)',
              'Left_Eye(Bottom)',
              'Right_Eye_(Left)',
              'Right_Eye(Top)',
              'Right_Eye_(Right)',
              'Right_Eye(Bottom)',
              'Nose',
              'Lip_Left',
              'Upper_Lip',
              'Lip_Right',
              'Lower_Lip']


class LabelTool():
    def __init__(self, master):
        # 初始化变量
        # 初始路径
        self.file_dir = ''
        # 初始图片列表
        self.list_image = []
        # 图片列表总个数
        self.image_count = 0
        # 图片当前第几个
        self.image_now = 0
        # 当前图片名字
        self.show_name = ''
        # 显示图片状态量
        self.tkimg =None
        # 标签计数
        self.label_count = 0
        # 标签记录
        self.label_record = []
        # 标签绘画
        self.cycle_paint = []
        # 标记点半径
        self.r_length = 2

        # 设置主要框架
        self.parent = master
        self.parent.title("特征点标注")
        self.frame = tk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.parent.resizable(width=TRUE, height=TRUE)

        # 文件主目录加载
        self.label = tk.Label(self.frame, text="路径:")
        self.label.grid(row=0, column=0, sticky=E)
        self.entry = tk.Entry(self.frame)
        self.entry.grid(row=0, column=1, sticky=W + E)
        self.ldBtn = tk.Button(self.frame, text="开始加载", command=self.loadDir)
        self.ldBtn.grid(row=0, column=2, sticky=W + E)

        # 显示窗口
        self.mainPanel = Canvas(self.frame, cursor='arrow')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.grid(row=1, column=1, rowspan=4, sticky=W + N)

        # 标签信息和删除按钮
        self.lb1 = Label(self.frame, text='特征点记录')
        self.lb1.grid(row=1, column=2, sticky=S)

        self.listbox = Listbox(self.frame, width=38, height=20)
        self.listbox.grid(row=2, column=2, sticky=N)

        self.btnNone = Button(self.frame, text='ValueNone', command=self.valueNone)
        self.btnNone.grid(row=3, column=2, sticky=W + E + N)
        self.btnDel = Button(self.frame, text='Delete', command=self.delOne)
        self.btnDel.grid(row=4, column=2, sticky=W + E + N)
        self.btnClear = Button(self.frame, text='ClearAll', command=self.delAll)
        self.btnClear.grid(row=5, column=2, sticky=W + E + N)

        # 控制和显示台
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row=6, column=1, columnspan=2, sticky=W + E)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width=10, command=self.nextshow)
        self.nextBtn.pack(side=LEFT, padx=5, pady=3)
        # 支持s键入翻页
        self.parent.bind("s", self.nextshow)
        self.progLabel = Label(self.ctrPanel, text="Progress:     /    ")
        self.progLabel.pack(side=RIGHT, padx=5)

    def _findOne(self):
        """
        内部函数，寻找第一个第一张图
        :return:
        """
        while 1:
            # 如果列表为空，则全标注完成
            if len(self.list_image) == 0:
                messagebox.showinfo("INFO", message="图片全已标完")
                break
            else:
                self.image_now += 1
                # 成功找寻到未标注图片
                if not self.list_image[0].startswith('#'):
                    # 当前展示图片名字
                    self.show_name = self.list_image[0]
                    # 查看label表是否存在, 不存在则加如句首
                    label_dir = self.file_dir + labeling_filename + label_txt
                    if not os.path.exists(label_dir):
                        file = open(label_dir, 'w')
                        file.write('image_name')
                        for n in label_list:
                            file.write(',' + n + '_x' + ',' + n + '_y')
                        file.write('\n')
                        file.close()
                    self._loadImage()
                    break
                else:
                    del self.list_image[0]

    def loadDir(self):
        """
        路径加载
        :return:
        """
        or_dir = self.entry.get()
        or_dir = or_dir.replace('\\', '/')
        if not or_dir.endswith('/'):
            or_dir += '/'
        self.file_dir = or_dir
        or_dir += image_filename
        # 路径是否存在
        if not os.path.isdir(or_dir):
            messagebox.showerror("Error!", message="路径不存在")
        else:
            self.list_image = os.listdir(or_dir)
            self.image_count = len(self.list_image)
            # 寻找第一个还未标注过的图片
            self._findOne()

    def _loadImage(self):
        """
        内部函数，加载显示区域
        :return:
        """
        imagepath = self.file_dir + image_filename + self.show_name
        pil_image = Image.open(imagepath)
        # 加载图像
        self.tkimg = ImageTk.PhotoImage(pil_image)
        self.mainPanel.config(width=max(self.tkimg.width(), 512), height=max(self.tkimg.height(), 512))
        self.mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)
        # 加载初始显示
        self.listbox.insert(END, label_list[self.label_count])
        # 加载进度
        self.progLabel.config(text="%d/%d" % (self.image_now, self.image_count))

    def _addValue(self, x=None, y=None, is_empty=1):
        """
        内部函数，加值
        :param x: 增加的点的坐标x轴
        :param y: 增加的点的坐标y轴
        :param is_empty: 是否增加空值
        :return:
        """
        # 删除本该有的提示，并加入最新的提示和坐标
        self.listbox.delete(self.label_count)
        self.listbox.insert(END, f'{label_list[self.label_count]}------{str([x, y])}')
        # 如果标签完成，则默认定位至最后一个
        if self.label_count < len(label_list) - 1:
            self.label_count += 1
            self.listbox.insert(END, label_list[self.label_count])
        # 否则且如果坐标收集完成，则删除最后一个数据，收集新的数据
        elif len(self.label_record) == len(label_list):
            del self.label_record[-1]
            self.mainPanel.delete(self.cycle_paint[-1])
            del self.cycle_paint[-1]
        # 画标记点并增加一个记录，画椭圆其实是指定一个矩形，然后在起内部画内接椭圆
        if is_empty:
            self.cycle_paint.append(self.mainPanel.create_oval(0, 0, 0, 0, fill="red", tag="r1"))
            self.label_record.append([np.NaN, np.NaN])
        else:
            self.cycle_paint.append(self.mainPanel.create_oval(x-self.r_length, y-self.r_length, x+self.r_length, y+self.r_length, fill="red", tag="r1"))
            self.label_record.append([x, y])

    def mouseClick(self, event):
        """
        鼠标点击动作，增加一个记录
        :param event:
        :return:
        """
        self._addValue(x=event.x, y=event.y, is_empty=0)

    def valueNone(self):
        """
        设置一个空值
        :return:
        """
        self._addValue()

    def delOne(self):
        """
        删除单个记录, 删除标记点，计数器减一，展示栏减少2再恢复1，记录值减少
        :return:
        """
        if len(self.label_record):
            # 删除最后一个标记点
            self.mainPanel.delete(self.cycle_paint[-1])
            del self.cycle_paint[-1]
            # 删除最后一个显示坐标与记录，并恢复最后一个提示
            if len(self.label_record) < len(label_list):
                self.listbox.delete(first=self.label_count-1, last=self.label_count)
                self.label_count -= 1
            else:
                self.listbox.delete(self.label_count)
            self.listbox.insert(END, label_list[self.label_count])
            del self.label_record[-1]

    def delAll(self):
        """
        删除所有记录，计数器清0，展示栏清0，记录值清0
        :return:
        """
        # 删除所有tag为r1的item
        self.mainPanel.delete("r1")
        self.cycle_paint = []
        self.listbox.delete(first=0, last=self.label_count)
        self.label_count = 0
        self.label_record = []
        self.listbox.insert(END, label_list[0])

    def nextshow(self):
        """
        下一张，完成上一张的保存，并初始化下一张
        :return:
        """
        if len(self.label_record) == len(label_list):
            # 已完成图改名
            os.rename(self.file_dir + image_filename + self.show_name,self.file_dir + image_filename + "#" + self.show_name)
            # 标签信息写入文档
            file = open(self.file_dir + labeling_filename + label_txt, 'a')
            file.write("#"+self.show_name)
            for i in self.label_record:
                file.write(","+str(i[0])+","+str(i[1]))
            file.write("\n")
            file.close()
            # 初始化
            self.delAll()
            self.listbox.delete(0)
            # 切换下一张图片
            del self.list_image[0]
            self._findOne()
        else:
            messagebox.showerror("Error!", message="规定点未标注完")


root = tk.Tk()
tool = LabelTool(root)
root.mainloop()
