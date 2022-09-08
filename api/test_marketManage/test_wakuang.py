# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/8/29
# @Email:775375798@qq.com
# @File: test_wakuang.py.py

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
@allure.feature("ADF挖矿列表")
class TestWakuang:

    @pytest.mark.skip("挖矿列表搜索功能测试用例跳过")
    @allure.story("挖矿列表搜索功能测试用例")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/search_list.yaml'))
    def test_search_list(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        RequestUtil().analysis_yaml(testcase_info)

    @allure.story("获取挖矿任务详情测试用例")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/get_wakuangtask_detail.yaml'))
    def test_wakuangtask_detail(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        task_detail = RequestUtil().analysis_yaml(testcase_info)
        print("task_detail====", task_detail["return_msg"]["taskList"][0])
        task_data_0 = task_detail["return_msg"]["taskList"][0]
        task_data_1 = task_detail["return_msg"]["taskList"][1]
        task_data_2 = task_detail["return_msg"]["taskList"][2]
        task_data_3 = task_detail["return_msg"]["taskList"][3]
        print("task_data_0=====", task_data_0)
        edit_testcase_info = read_testcase_yaml('testcases/marketManage/edit_wakuangtask.yaml')[0]
        print("edit_testcase_info======", edit_testcase_info)
        edit_testcase_info["request"]["data"] = task_data_0
        edit_testcase_info_0 = edit_testcase_info
        edit_testcase_info["request"]["data"] = task_data_1
        edit_testcase_info_1 = edit_testcase_info
        edit_testcase_info["request"]["data"] = task_data_2
        edit_testcase_info_2 = edit_testcase_info
        edit_testcase_info["request"]["data"] = task_data_3
        edit_testcase_info_3 = edit_testcase_info
        print("edit_testcase_info_0===", edit_testcase_info_0)
        RequestUtil().analysis_yaml(edit_testcase_info_0)
        RequestUtil().analysis_yaml(edit_testcase_info_1)
        RequestUtil().analysis_yaml(edit_testcase_info_2)
        RequestUtil().analysis_yaml(edit_testcase_info_3)



