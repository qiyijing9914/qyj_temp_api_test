#
import requests
import pytest
import allure
import json
from jsonpath import jsonpath
import time
from tools.data.mydb import myDB

from requests_toolbelt import MultipartEncoder

import config.env_config as config
from hashlib import md5
from faker import Faker
from tools.report import log_tool

f = Faker(locale='zh_CN')

pub_data = {}


@pytest.mark.run(order=1)
@allure.epic('登录')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d1_login(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d1_login-----------------')
        url = config.api_url + '/api/app/users/login'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

        req = {
            "username": "Jane_cm_qj",
            "password": "abc@123456"
        }
        allure.attach(json.dumps(req, ensure_ascii=False, indent=4), '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' + json.dumps(req, ensure_ascii=False, indent=4))

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, json=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200
        #assert resp.data != ""

    with allure.step('第5步：提取数据'):
        pub_data['token']=data["data"]["token"];
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + 'token='+pub_data['token'])
        log_tool.info('\n\n\n')


@pytest.mark.run(order=2)
@allure.epic('获取列表')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d2_reportlist(pub_data):
    with allure.step('第1步：准备请求报文'):
        endtime=time.time()
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d2_report-list-----------------')
        url = config.api_url + '/api/web/events/report-list?start=1609171200&end=1617264902&pageSize=10&page=1&sort=event_time' \
                               '&sort_type=0&isResolve=0&token='+pub_data['token']
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        headers = {}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

    with allure.step('第2步：调用接口'):
        resp = requests.get(url, headers=headers)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        #dic=json.loads(resp)
        event_id = jsonpath(data,"$..eventId")[10]
        pub_data['event_id']=event_id;
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + 'event_id:'+pub_data['event_id'])
        log_tool.info('\n\n\n')


@pytest.mark.run(order=3)
@allure.epic('受理立案并派遣')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d3_dispatch(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d3_mock-1616985940-----------------')
        url = config.api_url + '/api/web/events/'+pub_data['event_id']+'?token='+pub_data['token']+'&id='+pub_data['event_id']+'&currentStatus=1'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))
        sql = "SELECT department FROM department_assignment WHERE user_id=%s"
        a= myDB().executeSQL(sql=sql,params='5522')
        meta_id = myDB().get_one(a)


        reqdic = {"data": {"status": "12", "desc": "同意受理！", "withNext": 2,
                           "params": {"id": pub_data['event_id'], "meta_id":meta_id, "deps": [], "deal": "2021-04-06 16:41:59",
                                      "desc": "请及时处理！",
                                      "form_info": "{\"formType\":1,\"meta_name\":[\"建管委\"],\"depsName\":[],\"deal\":\"2021-04-06 16:41:59\",\"dispatchDesc\":\"请及时处理！\",\"desc\":\"同意受理！\"}"}}}
        req=json.dumps(reqdic)
        allure.attach(req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' + req)

    with allure.step('第2步：调用接口'):
        resp = requests.patch(url, headers=headers, data=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')


@pytest.mark.run(order=4)
@allure.epic('区部门')
@allure.feature('登录')
@allure.story('三级分类')
def test_d4_login(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d4_login-----------------')
        url = config.api_url + '/api/app/users/login'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

        req = {
            "username": "Jane",
            "password": "abc@123456"
        }
        allure.attach(json.dumps(req, ensure_ascii=False, indent=4), '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' + json.dumps(req, ensure_ascii=False, indent=4))

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, json=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        pub_data['token2'] = data['data']['token']
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')


@pytest.mark.run(order=5)
@allure.epic('区部门接单')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d5_accept_case(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d5_accept-case-----------------')
        url = config.api_url + '/api/web/case/accept-case?id='+pub_data['event_id']+'&token='+pub_data['token2']+'&currentStatus=23'
        #url ='http://172.16.25.62/api/web/case/accept-case?id=12319000115-0331142845&token=56c87be7631ce5647eeffb2726b3485b&currentStatus=23'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        # headers = {
        #     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryizUYY1QPAYHDOQCf"
        # }
        headers = {}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

        # req = ------WebKitFormBoundaryizUYY1QPAYHDOQCfContent - Disposition: form_data;
        # name = "id"
        # mock - 1616985940 - -----WebKitFormBoundaryizUYY1QPAYHDOQCfContent - Disposition: form - data;
        # name = "desc"
        # 接单。------WebKitFormBoundaryizUYY1QPAYHDOQCf - -
       # reqdic = {'id': pub_data['event_id'], 'desc': '接单'}
       # reqdic = {'id': 'c1231912345000103-0316160226', 'desc': 'acceot'}
        req={'id': pub_data['event_id'],
                 'desc': '接单'}
        files=[

        ]

        # print(type(req))
        json_req=json.dumps(req,ensure_ascii=False)
        allure.attach(json_req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' +json_req )

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, data=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')


@pytest.mark.run(order=6)
@allure.epic('区部门处置')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d6_call_complete(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d6_call-complete-----------------')
        url = config.api_url + '/api/web/case/call-complete?id='+pub_data['event_id']+'&token='+pub_data['token2']+'&currentStatus=11'
        #url = "http://172.16.25.62/api/web/case/call-complete?id=1231900013-0316102222&token=16b1e6129cea78837b2a349e71631d55&currentStatus=11"
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        # headers = {
        #     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarywHnXUAKrA0t0PHQu"
        # }
        headers={}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

        #       req = ------WebKitFormBoundarywHnXUAKrA0t0PHQuContent - Disposition: form - data;
        #       name = "extInfo"
        #       {"returns": "实际解决", "desc": "呜呜呜呜", "result": "",
        #        "formType": 5} - -----WebKitFormBoundarywHnXUAKrA0t0PHQuContent - Disposition: form - data;
        #       name = "id"
        #       mock - 1616985940 - -----WebKitFormBoundarywHnXUAKrA0t0PHQu - -
        # req = MultipartEncoder(fields={'extInfo': {"returns": "实际解决", "desc": "呜呜呜呜", "result": "", "formType": 5},
        #                                'id': pub_data['event_id']})
        req={'extInfo': '{"returns":"实际解决","desc":"处置测试","result":"","formType":5}',
             'id': pub_data['event_id']}
        files=[

        ]
        json_req=json.dumps(req,ensure_ascii=False)
        allure.attach(json_req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' +json_req)

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, data=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')


@pytest.mark.run(order=7)
@allure.epic('区核查')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d7_call_check(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d7_call-check-----------------')
        url = config.api_url + '/api/web/case/call-check?id='+pub_data['event_id']+'&token='+pub_data['token']+'&currentStatus=16'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        # headers = {
        #     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryATf16hwGxyWsNttf"

        headers={}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))

        req={'id': pub_data['event_id'],
             'desc': '核查测试',
             'skip': '1',
             'extInfo': '{"formType":6,"returns":"","desc":"核查测试","result":""}'}
        files=[

        ]
        # reqdic = {'id': pub_data['event_id'], 'desc': '核查测试'}
        # req=json.dumps(reqdic,ensure_ascii=False)
        json_req=json.dumps(req,ensure_ascii=False)
        allure.attach(json_req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' + json_req)

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, data=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')


@pytest.mark.run(order=8)
@allure.epic('结案')
@allure.feature('二级分类')
@allure.story('三级分类')
def test_d8_call_passed(pub_data):
    with allure.step('第1步：准备请求报文'):
        log_tool.info('\n-----------------test_case/get_class/test_get_class.py::d8_call-passed-----------------')
        url = config.api_url + '/api/web/case/call-passed?id='+pub_data['event_id']+'&token='+pub_data['token']+'&currentStatus=5'
        allure.attach(url, '请求地址', allure.attachment_type.TEXT)
        log_tool.info('\n请求地址：\n' + url)

        # headers = {
        #     "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarys0TwVz8KTMytfeXn"
        # }
        headers ={}
        allure.attach(json.dumps(headers, ensure_ascii=False, indent=4), '请求头', allure.attachment_type.TEXT)
        log_tool.info('\n请求头：\n' + json.dumps(headers, ensure_ascii=False, indent=4))
        sql = "SELECT id FROM order_case WHERE event_id=%s"
        params = pub_data['event_id']
        a = myDB().executeSQL(sql=sql, params=params)
        id = myDB().get_one(a)
        req = {'id': id,
               'desc': '结案通过',
               'result': '1',
               'extInfo': '{"returns":"","desc":"1212","result":"1","formType":7}'}
        json_req=json.dumps(req,ensure_ascii=False)
        allure.attach(json_req, '请求正文', allure.attachment_type.TEXT)
        log_tool.info('\n请求正文：\n' + json_req)

    with allure.step('第2步：调用接口'):
        resp = requests.post(url, headers=headers, data=req)

    with allure.step('第3步：接收响应'):
        data = resp.json()
        allure.attach(json.dumps(data, ensure_ascii=False, indent=4), '响应报文', allure.attachment_type.TEXT)
        log_tool.info('\n响应报文：\n' + json.dumps(data, ensure_ascii=False, indent=4))

    with allure.step('第4步：判断结果'):
        allure.attach("resp.status_code == 200", '断言条件', allure.attachment_type.TEXT)
        log_tool.info('\n断言条件：\n' + 'resp.status_code == 200')
        assert resp.status_code == 200

    with allure.step('第5步：提取数据'):
        # pub_data['data_name']='data_value';
        allure.attach('无', '提取数据列表', allure.attachment_type.TEXT)
        log_tool.info('\n提取数据列表：\n' + '无')
        log_tool.info('\n\n\n')
