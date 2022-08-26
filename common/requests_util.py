import traceback
import datetime
import pytest
import json
import requests
import common.common_util as common_util
import jsonpath
import re
from common.logger_util import write_log, write_error_log
from debugtalk import DebugTalk
import time


class RequestUtil(object):

    # 用来存储cookie信息
    cookie = {}
    sessions =requests.session()

    def __init__(self):
        # 初始化一个基础路径
        self.base_url = common_util.read_config_yaml('base', 'base_url')
        # 初始化cookies
        self.last_cookies = RequestUtil.cookie
        # 初始化请求头
        self.last_headers = None

    # 封装提取变量(json提取器,正则表达式提取器)
    def analysic_extract(self, casetest_info, res):
        text_result = res.text
        json_result = res.json()
        if jsonpath.jsonpath(casetest_info, '$..extract'):
            print("************%s" % casetest_info['extract'])
            for key, value in dict(casetest_info['extract']).items():
                if '(.+?)' in value or '(.*?)' in value:
                    write_log("analysic_extract进入正则提取判断")
                    if key == 'cookie':
                        obj = res.cookies
                    else:
                        extract_data = re.search(value, text_result)
                        write_log("--------------提取到的值是：%s" %extract_data.group(1))
                        obj = extract_data.group(1)
                    if obj:
                        data_dict = {key: obj}
                        common_util.write_extract_yaml(data_dict)
                        write_log("--------------------%s提取成功--------------------\n\n" % key)
                elif key == value:
                    write_log("进入json提取判断")
                    temp_data = jsonpath.jsonpath(json_result, '$..%s' % value)
                    if temp_data:
                        data_dict = {key: temp_data[0]}
                        common_util.write_extract_yaml(data_dict)
                        write_log("--------------------%s提取成功--------------------\n\n" % key)
                # 此判断适用于提取的键值在返回的数据中存在且返回的数据为json
                elif value:
                    write_log("进入通过key值提取数据场景")
                    temp_data = jsonpath.jsonpath(json_result, '$..%s' % key)
                    if temp_data:
                        data_dict = {key: temp_data[0]}
                        common_util.write_extract_yaml(data_dict)
                        write_log("--------------------%s提取成功--------------------\n\n" % key)
                else:
                    write_error_log("暂不支持该提取方式")

    # 封装提取变量(适用于返回的数据为非json格式)(json提取器,正则表达式提取器)
    def analysic_text_extract(self, casetest_info, res):
        text_result = res.text
        if jsonpath.jsonpath(casetest_info, '$..extract'):
            for key, value in dict(casetest_info['extract']).items():
                if '(.+?)' in value or '(.*?)' in value:
                    write_log("analysic_text_extract进入正则提取判断")
                    if key == 'cookie':
                        obj = res.cookies
                    else:
                        obj = re.search(value, text_result).group(1)
                    if obj:
                        data_dict = {key: obj}
                        common_util.write_extract_yaml(data_dict)
                        write_log("--------------------%s提取成功--------------------\n\n" % key)
                    else:
                        write_error_log("--------------------%s提取失败，在返回的数据中不存在--------------------\n\n" % key)
                else:
                    write_error_log("暂不支持该提取方式")

    # 封装的分析yaml测试用例文件的方法
    def analysis_yaml(self, testcase_info):
        """
        :param casetest_info: yaml测试用例数据
        :return: 无
        """
        try:
            # 判断：name,request,validate关键字是否存在
            testcase_info = dict(testcase_info)
            keys = testcase_info.keys()
            if 'name' in keys and 'request' in keys and 'validate' in keys:
                request_data = testcase_info["request"]
                request_keys = request_data.keys()
                if 'url' in request_keys and 'method' in request_keys:
                    headers=files=None
                    if jsonpath.jsonpath(request_data, '$..headers'):
                        headers = request_data["headers"]
                        del request_data["headers"]
                    if jsonpath.jsonpath(request_data, '$..files'):
                        for key, value in request_data["files"].items():
                            request_data["files"][key] = open(value, 'rb')
                        files = request_data["files"]
                        del request_data["files"]
                        # 收集日志
                    write_log("------------------------接口请求开始-------------------------")
                    write_log("接口名称：%s" % testcase_info['name'])
                    write_log("请求头：%s" % headers)
                    write_log("请求路径：%s" % testcase_info['request']['url'])
                    if jsonpath.jsonpath(testcase_info['request'], '$..data'):
                        write_log("接口替换前的请求数据：%s" % testcase_info['request']['data'])
                    if jsonpath.jsonpath(testcase_info['request'], '$..files'):
                        write_log("请求文件：%s" % testcase_info['request']['files'])
                    res = self.send_request(method=request_data.pop('method'), url=request_data.pop('url'),
                                            headers=headers, files=files, **request_data)
                    #　write_log("---------接口返回结果：%s" % res.text)
                    yq_result = testcase_info['validate']
                    status_code = res.status_code
                    # 断言返回结果
                    if jsonpath.jsonpath(testcase_info, '$..response_type') and testcase_info[
                        'response_type'] == 'text':
                        write_log("------------------返回的响应结果非字典类型，调用result_text_validatee方法断言-------------------")
                        self.result_text_validate(yq_result=yq_result, real_result=res.text, status_code=status_code)
                        # 提取变量
                        self.analysic_text_extract(testcase_info, res)
                    else:
                        write_log("------------------默认返回的响应结果是字典，调用result_validate方法断言-------------------")
                        print('这是返回的数据' % res.json())
                        # 如果返回的响应结果是字典，则调用result_validate方法断言
                        self.result_validate(yq_result=yq_result, real_result=res.json(), status_code=status_code)
                        # 提取变量
                        self.analysic_extract(testcase_info, res)
                        return res.json()
                else:
                    print("request必须包含二级关键字：url、method!")
            else:
                write_error_log("测试用例一级关键字不符合规则")
        except Exception as e:
            write_error_log("分析yaml文件出错,异常信息：%s" % str(traceback.format_exc()))

    def send_request(self, method, url, headers=None, files=None, **kwargs):
        self.method = method.upper()
        url = self.base_url + url
        self.url = self.replace_value(url)
        if headers and isinstance(headers, dict):
            self.last_headers = self.replace_value(headers)
        # 对请求数据做参数替换
        for key, value in kwargs.items():
            if key in ['params', 'data', 'json']:
                kwargs[key] = self.replace_value(value)
        # 对请求数据做热加载处理
        for key, value in kwargs.items():
            if key in ['params', 'data', 'json']:
                kwargs[key] = self.replace_load(value)
        res = RequestUtil.sessions.request(self.method, self.url, headers=self.last_headers, files=files, **kwargs)
        return res

    def result_text_validate(self, yq_result, real_result, status_code):
        """
        :param yq_result: 预期结果
        :param real_result: 实际结果
        :param status_code: 状态码
        :return: 返回断言成功与否的标记
        """
        write_log("预期结果：%s" % yq_result)
        # write_log("实际结果：%s" % real_result)
        try:
            flag = 0
            if yq_result and isinstance(yq_result, list):
                for yq in yq_result:
                    if isinstance(yq, dict):
                        for key, value in yq.items():
                            if key == 'contains':
                                if value not in real_result:
                                    flag += 1
                                    write_error_log("contains断言失败, %s在返回结果中不存在！" % value)
                            else:
                                flag += 1
                                write_error_log("不支持的断言方式!")
                    else:
                        flag += 1
                        write_error_log("不支持的断言格式!")
            elif yq_result and isinstance(yq_result, dict):
                for key, value in yq_result.items():
                    if key == 'contains':
                        if value not in real_result:
                            flag += 1
                            write_error_log("contains断言失败, %s在返回结果中不存在！" % value)
                    else:
                        flag += 1
                        write_error_log("不支持的断言方式!")
            else:
                flag += 1
                write_error_log("不支持的断言格式!")
            assert flag == 0
            write_log("接口执行成功")
            write_log("------------------------接口请求结束-------------------------\n")
        except Exception as e:
            write_log("接口执行失败")
            write_error_log("断言出错,异常信息：%s" % str(traceback.format_exc()))
            write_log("------------------------接口请求结束-------------------------\n")

    def result_validate(self, yq_result, real_result, status_code):
        """
        :param yq_result: 预期结果
        :param real_result: 实际结果
        :param status_code: 状态码
        :return: 返回断言成功与否的标记
        """
        write_log("预期结果：%s" % yq_result)
        write_log("实际结果：%s" % real_result)
        try:
            flag = 0
            if yq_result and isinstance(yq_result, list):
                for yq in yq_result:
                    if isinstance(yq, dict):
                        for key, value in yq.items():
                            if key == 'equals':
                                if isinstance(value, dict):
                                    for assert_key, assert_value in value.items():
                                        if assert_key == 'status_code':
                                            if assert_value != status_code:
                                                flag += 1
                                                write_error_log("断言失败，status_code断言失败！")
                                        else:
                                            all_values = jsonpath.jsonpath(real_result, '$..%s' % assert_key)
                                            if not all_values or assert_value not in all_values:
                                                flag += 1
                                                write_error_log("断言失败，%s断言失败！" % assert_key)
                                else:
                                    flag += 1
                                    write_error_log("不支持的断言方式!")
                            elif key == 'contains':
                                # ensure_ascii=False 表示中文字符串不会转为unicode码
                                real_result_temp = json.dumps(real_result, ensure_ascii=False)
                                if value not in real_result_temp:
                                    flag += 1
                                    write_error_log("contains断言失败, %s在返回结果中不存在！" % value)
                            else:
                                flag += 1
                                write_error_log("不支持的断言方式!")
                    else:
                        flag += 1
                        write_error_log("不支持的断言格式!")
            else:
                flag += 1
                write_error_log("不支持的断言格式!")
            assert flag == 0
            write_log("接口执行成功")
            write_log("------------------------接口请求结束-------------------------\n")
        except Exception as e:
            write_log("接口执行失败")
            write_error_log("断言出错,异常信息：%s" % str(traceback.format_exc()))
            write_log("------------------------接口请求结束-------------------------\n")

    def get(self, url, headers, data, cookies):
        return requests.get(url=url, params=data, headers=headers, cookies=cookies)

    def post(self, url, data, params, headers, files, cookies):
        return requests.post(url=url, data=data, params=params, headers=headers, files=files, cookies=cookies)

    def put(self, url, data, headers, cookies):
        return requests.put(url=url, data=data, headers=headers, cookies=cookies)

    def dels(self, url, data, headers, cookies):
        return requests.delete(url=url, data=data, headers=headers, cookies=cookies)

    #处理热加载数据
    def replace_load(self, value):
        if value and isinstance(value, dict):
            str = json.dumps(value)
        else:
            str = value
        for i in range(0, str.count('${')):
            if '${' in str and '}' in str:
                index_start = str.index('${')
                index_end = str.index('}', index_start)
                old_value = str[index_start:index_end + 1]
                # print("old_value2= ", old_value)
                function_end_index = old_value.index('(')
                function_name = old_value[2:function_end_index]
                # print("function_name=", function_name)
                key_end = old_value.index(')', function_end_index)
                key_values = old_value[function_end_index + 1:key_end]
                # print("key_values=", key_values)
                value_list = key_values.split(',')
                # print("value_list=", value_list)
                new_value = getattr(DebugTalk(), function_name)(*value_list)
                str = str.replace(old_value, new_value)
        if value and isinstance(value, dict):
            value = json.loads(str)
        else:
            value = str
        return value

    # 处理关联取值
    def replace_value(self, value):
        if value and isinstance(value, dict):
            str = json.dumps(value)
        else:
            str = value
        for i in range(0, str.count('{{')):
            if '{{' in str and '}}' in str:
                index_start = str.index('{{')
                index_end = str.index('}}', index_start)
                old_value = str[index_start:index_end + 2]
                # print("old_value= ", old_value)
                key_value = old_value[2:-2]
                new_value = common_util.read_extract_yaml(key_value)
                # print("new_value= ", new_value)
                str = str.replace(old_value, new_value)
                #　print("str=====", str)
        if value and isinstance(value, dict):
            value = json.loads(str)
        else:
            value = str
        return value

if __name__ == "__main__":
    url = "http://miniprogram-aiduifen-test.tongdui8.com/superAdmin/user-manage/give-adfun"
    params = {"t": "LUZfZGpmOVp0MglUDxN2A0AXGxcsKE4DFT87UidWTG4AKAk2JVF9Cg=="}
    data = {
        "uid": 143,
        "amount": 1,
        "reason": "test"
    }
    res = requests.post(url=url,params=params,data=data)
    print(res.json())
