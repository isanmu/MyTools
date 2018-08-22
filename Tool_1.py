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


def star_unordered_list(symbol='·', plus=1, direct=1):
    text = pyperclip.paste()
    print(repr(text))
    if '\r\n' in text:
        lines = text.split('\r\n')
    elif '\n' in text:
        lines = text.split('\n')
    else:
        lines = [text]
    print('lines', lines)
    # '\t◉ '; '\t• '; '\t😁 '...... (by 'shift+ctrl+B' under ch)
    if symbol == 'smile':
        symbol = '😁'
    elif symbol == '·':
        symbol = '•'
    for i, line in enumerate(lines):
        if plus == 1:
            if direct >= 1:
                lines[i] = '\t' + symbol + ' ' + line
            elif direct == 0:
                # line = line.rstrip()
                lines[i] = line + symbol
        elif plus == 0:
            if symbol in line:
                if direct == 2:
                    lines[i] = line.replace(str(symbol), '')
                elif direct == 1:
                    lines[i] = line[:len(symbol)].replace(str(symbol), '')\
                               + line[len(symbol):]
                elif direct == 0:
                    lines[i] = line[-len(symbol):].replace(str(symbol), '')\
                               + line[:-len(symbol)]
    pyperclip.copy('\r\n'.join(lines))
    return lines


def self_var_list():
    #
    text = pyperclip.paste()
    if '\r\n' in text:
        lines = text.split('\r\n')
    elif '\n' in text:
        lines = text.split('\n')
    else:
        lines = text
    # lines = text.split()
    print(lines)
    newlines = []
    for i, line in enumerate(lines):
        if '//' in line:
            newlines.append('# ' + line.replace('//', ''))
        else:
            varline = line.split()
            # print(varline)
        # line = line.lstrip()
            for j, var in enumerate(varline):
                if ',' in var:
                    var = var.replace(',', '')
                elif ';' in var:
                    var = var.replace(';', '')
                newlines.append('self.' + var + ' = ' + var)
    pyperclip.copy('\n'.join(newlines))
    print(newlines)
    return newlines


def init_var_list(num):
    if num <= 0:
        raise ValueError('Wrong input num(to list)')
    else:
        #
        text = pyperclip.paste()
        print(repr(text))
        if '\r\n' in text:
            lines = text.split('\r\n')
        elif '\n' in text:
            lines = text.split('\n')
        else:
            lines = text
        print(lines)
        # lines = text.split()
        newlines = []
        for i, line in enumerate(lines):
            if '//' not in line:
                varline = line.split()
                for var in varline:
                    # line = line.lstrip()
                    newlines.append(var)
        print(newlines[:10])
        for i, var in enumerate(newlines, 1):
            if i % (num+1) == 0:
                newlines.insert(i-1, '\n')
        pyperclip.copy(' '.join(newlines))
        return newlines


if __name__ == '__main__':
    text_new = star_unordered_list(symbol='1', plus=0, direct=1)
    print(text_new)
    start = time.time()
    # print(pyperclip.is_available())
    # print(star_unordered_list())
    end = time.time()
    print('run time:', end-start)
