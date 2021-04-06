import json
import os
from urllib.parse import unquote
from wuling.bean.request import Request
from wuling.bean.response import Response
from ruamel import yaml

request = Request()
response = Response()
yaml_file_name = ''


def get_root_path():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")).replace('\\', '/')
    print(root_path)
    if root_path.find('venv') > 0:
        root_path = root_path[:root_path.find('venv') - 1]
    return root_path + '/'


def parse_req_query(values):
    items = values.split('&')
    for item in items:
        key = item.split('=')[0].strip()
        value = item.split('=')[1].strip()
        request.query[key] = value


def parse_req_line(line):
    global request
    index = line.index(' ')
    request.method = line[:index].strip()
    line = line[index + 1:]

    index = line.find('://')
    request.protocal = line[:index].strip()
    line = line[index + 3:]

    index = line.find(':')
    if index == -1 and request.protocal == 'http':
        index = line.find('/')
        request.ip = line[:index].strip()
        request.port = 80
        line = line[index:]
    elif index == -1 and request.protocal == 'https':
        index = line.find('/')
        request.ip = line[:index].strip()
        request.port = 443
        line = line[index:]
    else:
        request.ip = line[:index]
        line = line[index:]
        index = line.find('/')
        request.port = line[:index]

    # 解析uri
    index = line.find('?')
    if index == -1:
        index = line.find(' ')
        request.uri = line[:index]
        line = line[index + 1:]
    else:
        request.uri = line[:index].strip()
        line = line[index + 1:]
        # 解析params
        index = line.find(' ')
        query = unquote(line[:index], encoding="UTF-8")
        parse_req_query(query)
        line = line[index + 1:]

    print('解析请求行')


def parse_req_cookie(value):
    items = value.split(';')
    for item in items:
        request.cookies[item.split('=')[0].strip()] = item.split('=')[1]
    print('解析cookie')


def parse_req_header(line):
    global request
    ignore_list = ['Host', 'Connection', 'Content-Length', 'Accept','Pragma','Cache-Control',
                   'User-Agent', 'Origin', 'Referer', 'Accept-Encoding', 'Accept-Language']
    key = line.split(': ')[0]
    value = unquote(line.split(': ')[1], encoding="UTF-8")
    if key == 'Cookie':
        parse_req_cookie(value)
        return
    elif key not in ignore_list:
        request.header[key] = value
    print('解析请求头')


def parse_req_body(line):
    global request
    request.body += line
    print('解析请求正文')


def request2yaml(case_file, case_index):
    global request
    global yaml_file_name
    has_body_type = request.header.__contains__('Content-Type')
    if has_body_type == True:
        body_type = request.header['Content-Type']
        print(request.header['Content-Type'])
        if body_type.__contains__('application/json') and request.body != '':
            # print(request.body)
            body=request.body
            body=body[body.find('{'):]
            body=body[:body.rfind('}')+1]
            request.body = json.loads(body)
            # print(type(request.body))
            # print(request.body)
    dstr = request.__dict__

    print(dstr)
    # 处理false和true
    save_path = case_file + '/test_data'
    yaml_file_name = 'd' + str(case_index) + '_' + request.uri[request.uri.rfind('/') + 1:]
    save_file = yaml_file_name + '_req.yaml'
    print(case_file + '/test_data')
    is_exists = os.path.exists(save_path)
    if not is_exists:
        os.makedirs(save_path)
    with  open(save_path + '/' + save_file, 'w', encoding='utf-8') as f:
        yaml.dump(dstr, f, Dumper=yaml.RoundTripDumper, default_flow_style=False, encoding='utf-8', allow_unicode=True)


# 解析响应行
def parse_rsp_line(line):
    global response
    items = line.split(' ')
    response.status_code = items[1]
    if len(items) >= 3:
        response.status_desc = items[2]


def parse_rsp_cookie(value):
    print()


# 解析响应头
def parse_rsq_header(line):
    global response
    ignore_list = ['Server', 'Date', 'Connection', 'Vary',
                   'Access-Control-Allow-Origin', 'Access-Control-Expose-Headers', 'Content-Length']
    key = line.split(': ')[0]
    value = unquote(line.split(': ')[1], encoding="UTF-8")
    if key == 'Cookie':
        parse_rsp_cookie(value)
        return
    elif key not in ignore_list:
        response.header[key] = value


# 解析响应正文
def parse_rsp_body(line):
    global response
    response.body += line


def response2yaml(case_file, case_index):
    global response
    global yaml_file_name
    has_body_type = response.header.__contains__('Content-Type')
    if has_body_type == True:
        body_type = response.header['Content-Type']
        print(response.header['Content-Type'])
        if body_type.__contains__('application/json') and response.body != '':
            # 解决false和true的大小写问题
            # response.body=response.body.replace('false','Flase')
            # response.body=response.body.replace('true','True')
            body=response.body
            body=body[body.find('{'):]
            body=body[:body.rfind('}')+1]
            response.body = json.loads(body)
            # print(type(request.body))
            # print(request.body)
    dstr = response.__dict__
    print(dstr)
    save_path = case_file + '/test_data'
    save_file = yaml_file_name + '_rsp.yaml'
    print(case_file + '/test_data')
    is_exists = os.path.exists(save_path)
    if not is_exists:
        os.makedirs(save_path)

    with  open(save_path + '/' + save_file, 'w', encoding='utf-8') as f:
        yaml.dump(dstr, f, Dumper=yaml.RoundTripDumper, default_flow_style=False, encoding='utf-8', allow_unicode=True)



def generate_config_file():
    config_file = get_root_path() + 'config/env_config.py'
    has_api_url = False
    if os.path.isfile(config_file):
        for line in open(config_file, encoding='utf-8'):
            if line.startswith('api_url='):
                has_api_url = True
    if not has_api_url:
        with open(config_file, 'a+', encoding='utf-8') as f:
            code="api_url='{}://{}:{}'".format(request.protocal,request.ip,request.port)
            f.write(code)


def generate_test_case_file(file_name):
    code = '''
import requests
import pytest
import allure
import json
import config.env_config as config
from hashlib import md5
from faker import Faker
from tools.report import log_tool

f = Faker(locale='zh_CN')
'''
    if os.path.isfile(file_name):
        # ‘w+’ ==w+r（可覆盖可写，文件若不存在就创建
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(code)
    else:
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write(code)

def generate_conftest_file(file_name):
    index = file_name.rfind('/')
    file_name = file_name[:index] + '/conftest.py'
    has_pub_data_method = False
    if os.path.isfile(file_name):
        for line in open(file_name, encoding='utf-8'):
            if line.startswith('def pub_data():'):
                has_pub_data_method = True
    if not has_pub_data_method:
        with open(file_name, 'a+', encoding='utf-8') as f:
            code = '''
import pytest

@pytest.fixture(scope='session')
def pub_data():
    data={}
    yield data
'''
            f.write(code)


def generate_init_files(file_name):
    generate_test_case_file(file_name)
    generate_conftest_file(file_name)


def generate_method_def_code(file_name, case_index, case_name):
    code = '''


@pytest.mark.run(order={})
@allure.epic('一级分类')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_{}( pub_data):
'''.format(case_index, case_name)
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)


def generate_url_code(file_name,case_name):
    root_path=get_root_path()

    url = request.uri
    has_chines = False
    if len(request.query) > 0:
        url = url + '?'
        i = 0
        for key in request.query.keys():
            if i == 0:
                url += key + '=' + request.query[key]
            else:
                url += '&' + key + '=' + request.query[key]
            if u'\u4e00' <= request.query[key] <= u'\u9fff':
                has_chines = True
            i += 1
    code = '''
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\\n-----------------{}::{}-----------------')
        url = config.api_url+'{}'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\\n请求地址：\\n'+url)
'''.format(file_name.replace(root_path,''),case_name,url)
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)
    if has_chines:
        code = '''
        url = url.encode('utf-8').decode('latin-1')
'''
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write(code)


def generate_header_code(file_name):
    code = '''
        headers = {}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\\n请求头：\\n'+json.dumps(headers, ensure_ascii=False, indent=4))
    '''.format(json.dumps(request.header, indent=4, ensure_ascii=False))
    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)

    for key in request.header.keys():
        if u'\u4e00' <= request.header[key] <= u'\u9fff':
            code = '''
        headers['{}'] = '{}'.encode('utf-8').decode('latin-1')
            '''.format(key, request.header[key])
            with open(file_name, 'a+', encoding='utf-8') as f:
                f.write(code)


def generate_body_code(file_name):
    code = ''
    if request.body != '':
        if request.header.__contains__('Content-Type') and request.header['Content-Type'].find(
                'application/json') != -1:
            code = '''
        req = {}
        allure.attach(json.dumps(req, ensure_ascii=False, indent=4), '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\\n请求正文：\\n'+json.dumps(req, ensure_ascii=False, indent=4))
'''.format(json.dumps(request.body, indent=4, ensure_ascii=False))
        else:
            code = '''
        req = {}
        allure.attach(req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\\n请求正文：\\n'+req)
'''.format(request.body)
        # 解决false和true在python中异常
        code=code.replace('false','False')
        code=code.replace('true','True')
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write(code.replace('false','False'))


def generate_request_code(file_name):
    method = request.method.lower()
    body_param = ''
    if request.body != '':
        if request.header.__contains__('Content-Type') and request.header['Content-Type'].find(
                'application/json') != -1:
            body_param = ',json=req'
        else:
            body_param = ',data=req'
    cookie_param = ''
    # if len(request.cookies)>0 :
    #     cookie_param=', cookies=cookies'
    code = '''
    with allure.step('第2步：调用接口'):
        resp = requests.{}(url, headers=headers {})
'''.format(method, body_param)

    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)


def generate_response_code(file_name):
    data_code = 'resp.text'
    attach_data = 'data'
    if response.header.__contains__('Content-Type') and response.header['Content-Type'].find('application/json') != -1:
        data_code = 'resp.json()'
        attach_data = 'json.dumps(data, ensure_ascii=False, indent=4)'
    code = '''
    with allure.step('第3步：接收响应'):
        data = {}
        allure.attach({}, '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\\n响应报文：\\n'+{})
    '''.format(data_code, attach_data,attach_data)

    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)


def generate_assert_code(file_name):
    code = '''
    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\\n断言条件：\\n'+'resp.status_code == 200')
        assert resp.status_code == 200
    '''

    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)


def generate_data_code(file_name):
    code = '''
    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表',allure.attachment_type.TEXT)
        log_tool.info('\\n提取数据列表：\\n'+'无')
        log_tool.info('\\n\\n\\n')
    '''

    with open(file_name, 'a+', encoding='utf-8') as f:
        f.write(code)


def request2testcase(file_name, case_index):
    global request
    # 3. 生成def case
    case_name = 'd' + str(case_index) + '_' + request.uri[request.uri.rfind('/') + 1:]
    generate_method_def_code(file_name, case_index, case_name)
    # 4. 生成url
    generate_url_code(file_name,case_name)
    # 5. 生成请求头
    generate_header_code(file_name)
    # 6. 生成请求正文
    generate_body_code(file_name)
    # 7. 调用接口
    generate_request_code(file_name)
    # 8. 解析响应
    generate_response_code(file_name)
    # 9. 生成断言
    generate_assert_code(file_name)
    # 10. 提取数据
    generate_data_code(file_name)


def parse_http_file(file_addr, case_file):
    global request
    global response

    root_path = get_root_path()

    file_addr=root_path+file_addr
    case_file=root_path+case_file

    i = case_file.rfind('/')
    file_name = case_file + '/test_' + case_file[i + 1:] + '.py'
    generate_init_files(file_name)
    case_index = 1
    status_list = ['req_line', 'req_header', 'req_body', 'rsp_line', 'rsp_header', 'rsp_body']
    status = status_list[0]
    for line in open(file_addr, encoding='utf-8'):
        if status == 'req_line':
            if line != '\n':
                parse_req_line(line[:-1])
                status = status_list[1]
                generate_config_file()
        elif status == 'req_header':
            if line == '\n':
                status = status_list[2]
            else:
                parse_req_header(line[:-1])
        elif status == 'req_body':
            if line.startswith('HTTP/1.1'):
                status = status_list[4]
                parse_rsp_line(line[:-1])
            else:
                parse_req_body(line[:-1])
        elif status == status_list[4]:
            if line == '\n':
                status = status_list[5]
            else:
                parse_rsq_header(line[:-1])
        elif status == status_list[5]:
            if line == '------------------------------------------------------------------\n':
                status = status_list[0]
                request.to_string()
                request2yaml(case_file, case_index)
                response2yaml(case_file, case_index)
                request2testcase(file_name, case_index)
                request = Request()
                response = Response()
                case_index += 1
            else:
                parse_rsp_body(line[:-1])
        else:
            continue
