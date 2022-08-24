# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/8/18
# @Email:775375798@qq.com
# @File: test_banner.py


import requests
import pytest
import json
import common.common_util as common_unitl
import os
from common.common_util import *
from common.parameters_util import read_testcase_yaml
from common.requests_util import RequestUtil
import allure
import time

@allure.epic("爱兑分后台自动化接口项目")
@allure.feature("营销模块测试")
class TestUser:

    @pytest.mark.skip("进入创建banner接口跳过")
    @allure.story("进入创建banner测试用例")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/marketManage/get_banner.yaml'))
    def test_get_banenr(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

    @pytest.mark.skip("新建banner接口跳过")
    @allure.story("新建banner功能测试用例")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/marketManage/create_banner.yaml'))
    def test_create_banenr(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

    # @pytest.mark.skip("搜索banner接口跳过")
    @allure.story("搜索banner功能测试用例")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/marketManage/search_banner.yaml'))
    def test_search_banenr(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)
