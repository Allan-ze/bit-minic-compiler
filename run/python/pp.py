#!/usr/bin/python
# -*- coding: utf-8 -*-
# 预处理，实现的有删除注释，宏替换
import os
import sys
import re


def pp(input_lines=None):
    outstring = []
    patternstart = re.compile(r'/\*')
    patternend = re.compile(r'\*/')
    patterninclude = re.compile(r'#include')
    patterndefine = re.compile(r'#define')
    start = False
    for line in input_lines:

        pos = line.find("//")
        if pos != -1:
            line = line[0:pos] + '\n'
        if start == True:
            pos = line.find("*/")
            if pos != -1:
                start = False
                line = line[pos + 2:len(line)]
            else:
                line = '\n'
        else:
            pos = line.find("/*")
            if pos != -1:
                start = True
                line = line[0:pos]
        if patterndefine.match(line):
            line = '\n'
        if patterninclude.match(line):
            line = '\n'
        outstring.append(line)
    return outstring


def main(input_argv=None):
    '''
    主函数
    '''
    print "1"
    #若定义了输入文件名
    input_path = os.path.abspath('./data/test.c')
    output_path = os.path.abspath('./data/test.pp.c')
    if len(input_argv) > 1:
        #获取绝对路径
        input_path = os.path.abspath(input_argv[1])
    else:
        if os.name == 'nt':
            input_path = os.path.abspath('.\\data\\test.c')
        else:
            input_path = os.path.abspath('./data/test.c')
    #若定义了输出文件名
        if len(input_argv) > 2:
            output_path = os.path.abspath(input_argv[2])
        else:
            if os.name == 'nt':
                output_path = os.path.abspath('.\\data\\test.pp.c')
            else:
                output_path = os.path.abspath('./data/test.pp.c')
    #打开文件
    input_file = open(input_path, 'r')
    output_file = open(output_path, 'w')
    #出错处理
    if os.name == 'nt':
        error_path = os.path.abspath('.\\data\\test.err')
    else:
        error_path = os.path.abspath('./data/test.err')
    err_file = open(error_path, 'w')

    #进行处理，并将预处理结果写入文件
    linelist = input_file.readlines()
    output_str = pp(linelist)
    output_file.writelines(output_str)

    #关闭文件
    input_file.close()
    output_file.close()
    err_file.close()
    #print sys.argv

    print ' preprocess finished \n'
    return


if __name__ == "__main__":
    # 调用主函数
    main(sys.argv)
