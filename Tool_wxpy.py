#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Winson
# User: sanmu
# Date: 2018/9/6 21:54
# Project: MyTools
# File Name: Tool_wxpy.py

import sys
import re
import datetime

from pylab import *
# from jieba import c
import wxpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pyecharts import Map
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QBrush, QColor
from emoji import emojize
import numpy as np
# from wxpy.api.chats import Chats as wxChats

from ui_files.wechat_window import Ui_MainWindow
from ui_files.msg_window import Ui_Form


class WeChatWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_ui()
        self.msg_win = MsgWindow(self)
        # self.init_wechat()
        self.status = False

        pass

    def init_ui(self):
        self.actionSex.triggered.connect(self.sex_rate_plot)
        self.actionProvince.triggered.connect(self.province_rate_plot)
        self.actionCity.triggered.connect(self.city_rate_plot)
        self.actionLogin.triggered.connect(self.login)
        self.actionLogout.triggered.connect(self.logout)
        pass

    #  def init_wechat(self):
    #     self.box = wxpy.Bot(cache_path=True)
    #     self.my_friend = self.bot.friends()
    #     pass

    def sex_rate_plot(self):
        if not hasattr(self, 'my_friend'):
            self.my_friend = self.bot.friends()
        friend_status = self.my_friend.stats()
        sex_a = friend_status['sex'].get(wxpy.MALE, 0)
        sex_b = friend_status['sex'].get(wxpy.FEMALE, 0)
        num_friend = len(self.my_friend)
        rate_a = sex_a / num_friend
        rate_b = sex_b / num_friend
        labels = ['Male', 'Female', 'Intersex']
        plot_pie_status(labels, sizes=[rate_a, rate_b, 1 - rate_a - rate_b])
        pass

    def province_rate_plot(self):
        if not hasattr(self, 'my_friend'):
            self.my_friend = self.bot.friends()
        stats = self.my_friend.stats()
        num = len(self.my_friend) * 0.001

        def top_n_list(attr, n):
            top_n = list(filter(lambda x: x[0], stats[attr].most_common()))[:n]
            return top_n

        item_list = []
        item_value = []
        for item, value in top_n_list('province', 7):
            item_list.append(item)
            item_value.append(value/num)
        user_title = 'Friends Top10 Province'
        print(item_list)
        print(item_value)
        plot_map_status(user_title, item_list, item_value)
        pass

    def city_rate_plot(self):
        if not hasattr(self, 'my_friend'):
            self.my_friend = self.bot.friends()
        stats = self.my_friend.stats()
        num = len(self.my_friend) * 0.01
        def top_n_list(attr, n):
            top_n = list(filter(lambda x: x[0], stats[attr].most_common()))[:n]
            # top_n = ['{}: {} ({:.2%})'.format(k, v, v / len(self)) for k, v in top_n]
            # return '\n'.join(top_n)
            return top_n

        item_label = []
        item_weight = []
        for k, v in top_n_list('city', 10):
            # print(k, type(k))
            item_label.append(k)
            item_weight.append(v/num)
        u_xlabel = 'City'
        u_ylabel = 'Percentage(%)'
        u_title = 'Friends Top10 City'
        plot_bar_status(item_len=10, item_weight=item_weight, item_label=item_label,
                        u_xlabel=u_xlabel, u_ylabel=u_ylabel, u_title=u_title,
                        bar_label='City')

    def nick_name_ana(self):
        pass

    def friend_list(self):
        if hasattr(self, 'bot'):
            self.my_friend = self.bot.friends()
            model_fri = QStandardItemModel()
            model_fri.setHorizontalHeaderLabels(['Friends', 'Nick_Name', 'Sex', 'Province', 'City'])
            for i, fri in enumerate(self.my_friend):
                model_fri.setItem(i, 0, QStandardItem(str(emojize(fri.name))))
                model_fri.setItem(i, 1, QStandardItem(str(emojize(fri.nick_name))))
                if fri.sex == wxpy.MALE:
                    sex = 'Male'
                    color = '#5CACEE'
                elif fri.sex == wxpy.FEMALE:
                    sex = 'Female'
                    color = '#EE82EE'
                else:
                    sex = 'Intersex'
                    color = '#FFFFFF'
                model_fri.setItem(i, 2, QStandardItem(str(sex)))
                model_fri.item(i, 2).setBackground(QBrush(QColor(color)))
                model_fri.setItem(i, 3, QStandardItem(str(fri.province)))
                model_fri.setItem(i, 4, QStandardItem(str(fri.city)))
                # print(fri.sex)
            self.friend_tableView.setModel(model_fri)

    def login(self):
        self.bot = wxpy.Bot(cache_path=True)
        # self.bot.self.add('123')

        self.bot.messages.max_history = 10000
        self.status = True
        self.friend_list()
        self.runthd = ReceiveMsgThread(self)
        self.runthd.start()

    def logout(self):
        if hasattr(self, 'bot'):
            self.status = False
            self.bot.logout()

    def msg_en(self, index):
        # self.bot.self.add()
        # self.bot.self.accept()
        # QtCore.QModelIndex.
        print(index.row())
        row = index.row()
        col1 = index.column()
        if col1 == 0:
            name = index.data()
            name_re = re.search('[(]' + '.*' + '[)]', str(name), re.M | re.I)
            if name_re:
                name = name_re.group().replace('(', '').replace(')', '')
            print(name)
        # print(col1, col2)
            try:
                # print('')
                self.now_msg_friend = wxpy.ensure_one(self.my_friend.search(name))
                if self.now_msg_friend.name == self.bot.self.name:
                    # self.now_msg_friend.add(None)
                    self.now_msg_friend.accept(None)
                self.msg_win = MsgWindow(self)
                self.msg_win.show()
            except ValueError:
                print('Not Found Friend')
            else:
                print(self.now_msg_friend.sex)


class MsgWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, win):
        super().__init__()
        self.setupUi(self)
        self.win = win
        if hasattr(self.win, 'now_msg_friend'):  # and isinstance(self.win.now_msg_friend, wxpy.api.chats.friend.Friend)
            self.bot = self.win.bot
            self.friend = self.win.now_msg_friend
            self.friend_label.setText(self.friend.name+'-'+self.friend.nick_name)
            history_msgs = self.bot.messages.search(sender=self.friend)
            print(history_msgs, type(history_msgs))
            for msg in history_msgs:
                print(msg, type(msg))
                self.msg_textBrowser.append(str(msg))
            # print(history_msgs)

    def send_func(self):
        msg = self.msg_textEdit.toPlainText()
        print(msg)
        self.msg = self.friend.send_msg(msg)
        self.msg_textBrowser.append(msg)
        # print(self.msg.create_time())
        self.msg_textBrowser.append(datetime.datetime.now().strftime('%b-%d-%Y %H:%M:%S'))
        pass

    def recall_func(self):
        self.msg.recall()
        pass


class ReceiveMsgThread(QtCore.QThread):
    def __init__(self, win):
        super().__init__()
        self.win = win

    def run(self):
        bot = self.win.bot
        print('')
        # while True:

        @bot.register(except_self=False)
        def auto_reply(msg):
            print(msg)
            # 如果是群聊，但没有被 @，则不回复
            print(msg.sender, msg.receiver)
            if msg.sender == bot.self:
                return bot.self.send_msg('收到消息111: {} ({})'.format(msg.text, msg.type))
            if msg.sender == self.win.now_msg_friend:
            # if isinstance(msg.chat, self.win.now_msg_friend):  # and not msg.is_at
            #     # 回复消息内容和类型
                return msg.reply_msg('收到消息: {} ({})'.format(msg.text, msg.type))
        # self.exec()
        wxpy.embed()


def run():
    bot = wxpy.Bot(cache_path=True)
    my_friend = bot.friends()  # .search('木', sex=wxpy.MALE)
    friend_status_text = my_friend.stats_text()
    friend_status = my_friend.stats()
    # text = friend_status_text.split("\n")
    sex_a = friend_status['sex'].get(wxpy.MALE, 0)
    sex_b = friend_status['sex'].get(wxpy.FEMALE, 0)
    num_friend = len(my_friend)
    rate_a = sex_a / num_friend
    rate_b = sex_b / num_friend
    labels = ['Male', 'Female', 'Intersex']
    plot_pie_status(labels, sizes=[rate_a, rate_b, 1-rate_a-rate_b])

    # print(bot.user_details(my_friend))
    pass


def plot_pie_status(labels=[], sizes=[]):
    # labels = labels
    # sizes = sizes
    explode = (0, 0, 0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=False_, startangle=90)
    ax1.axis('equal')
    plt.legend()
    plt.show()


def plot_map_status(user_title, item_list, item_value):
    map = Map(user_title, width=600, height=400)
    map.add('', item_list, item_value, maptype='china',
            is_visualmap=True, visual_text_color="#000",)
    map.render()


def plot_bar_status(item_len=10, item_weight=[], item_label=(),
                    u_xlabel='', u_ylabel='', u_title='', bar_label=''):
    if isinstance(item_label, list):
        item_label = tuple(item_label)
    # print(item_label, repr(item_label))
    font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=12)
    item_len = min(len(item_label), item_len)
    fig, ax = plt.subplots()
    index = np.arange(item_len)
    bar_width = 0.35
    opacity = 0.5
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, item_weight, bar_width, alpha=opacity,
                    color='b', error_kw=error_config, label=bar_label)
    ax.set_xlabel(str(u_xlabel))
    ax.set_ylabel(str(u_ylabel))
    ax.set_title(str(u_title))
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(item_label, fontproperties=font)
    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # run()
    app = QtWidgets.QApplication(sys.argv)
    main_window = WeChatWindow()
    main_window.show()
    sys.exit(app.exec_())
