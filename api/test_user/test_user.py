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
@allure.feature("用户管理模块测试")
class TestUser:

    @pytest.mark.skip("用户管理列表接口跳过")
    @allure.story("用例管理列表搜索功能测试用例")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/userManage.yaml'))
    def test_userManage(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

    # @pytest.mark.skip("导出接口跳过")
    @allure.story("测试用例管理列表导出功能")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/userManage_export.yaml'))
    def test_userManage_export(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

    @pytest.mark.skip("单个发放ADFun接口跳过")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/userManage_giveadf.yaml'))
    def test_userManage_giveadf(self, testcases_info):
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

    @pytest.mark.skip("批量上传adf接口跳过")
    @allure.story("批量上传adf接口")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('testcases_info', read_testcase_yaml('testcases/userManage_load_adf.yaml'))
    def test_userManage_load_adf(self, testcases_info):
        print("测试用例: ", testcases_info)
        allure.dynamic.title(testcases_info["name"])
        RequestUtil().analysis_yaml(testcases_info)

