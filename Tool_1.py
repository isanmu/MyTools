#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Winson
# User: sanmu
# Date: 2018/6/26 0:02
# Project: MyTools
# File Name: Tool_1.py

import time

import pyperclip
import win32clipboard
import markdown

# markdown.markdown()


def star_unordered_list():
    text = pyperclip.paste()
    print(text)
    lines = text.split('\n')
    # print(lines)
    for line in lines:
        lines[lines.index(line)] = '* ' + line
    # for i in range(len(lines)):
    #     lines[i] = '* ' + lines[i]

    pyperclip.copy('\n'.join(lines))
    return lines


start = time.time()
# print(pyperclip.is_available())
print(star_unordered_list())
end = time.time()
print('run time:', end-start)
