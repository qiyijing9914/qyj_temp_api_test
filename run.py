# -*- coding:utf-8 -*-																		
# Author : 小吴老师                                                                        
# Data ：2019/7/12 7:41
import pytest
import subprocess

if __name__ == '__main__':
    pytest.main(['-s', '-v', '--alluredir', "reports/xml/", "test_case/get_class"])

    cmd="allure generate reports/xml/ -o reports/html --clean"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    cmd="allure serve reports/xml"
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()