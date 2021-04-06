#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： 小吴老师
# datetime： 2021/3/27 7:26

from wuling.tool import api_test_tool

if __name__ == '__main__':
    # fidller抓包文件路径（右键复制相对路径 【copy relative path】）
    data_file='test_data/12319_apil.txt'

    # 测试代码生成文件夹（test_case下新建文件夹，右键复制相对路径 【copy relative path】）
    test_case_path='test_case/get_class'

    # 调用代码生成器
    api_test_tool.generate_test_case(data_file,test_case_path)