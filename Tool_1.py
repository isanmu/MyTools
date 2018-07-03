#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# Author: Winson
# User: sanmu
# Date: 2018/6/26 0:02
# Project: MyTools
# File Name: Tool_1.py

import time
import pyperclip
# import win32clipboard


def star_unordered_list():
    # TODO: add optional input to get unordered symbol
    text = pyperclip.paste()
    lines = text.split('\n')
    # for line in lines:
    #     lines[lines.index(line)] = '\t😁 ' + line
    # '\t◉ '; '\t• '; '\t😁 '...... (by 'shift+ctrl+B' under ch)

    # for i in range(len(lines)):
    #     lines[i] = '* ' + lines[i]

    for i, line in enumerate(lines):
        lines[i] = '\t😁 ' + line
    pyperclip.copy('\n'.join(lines))
    return lines


start = time.time()
# print(pyperclip.is_available())
print(star_unordered_list())
end = time.time()
print('run time:', end-start)
