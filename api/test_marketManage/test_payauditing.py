# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/09/08
# @Email:775375798@qq.com
# @File: test_banner.py


import pytest
from common.parameters_util import read_testcase_yaml
from common.requests_util import RequestUtil
from common.common_util import write_extract_yaml
import allure


@allure.epic("爱兑分后台项目")
@allure.feature("支付审核模块")
class TestPayaudting:

    @pytest.mark.run(ording=1)
    @pytest.mark.skip("支付审核列表搜索用例跳过")
    @allure.story("支付审核列表搜索功能测试用例")
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/payauting_search.yaml'))
    def test_payauting_search(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        pay_data = RequestUtil().analysis_yaml(testcase_info)["return_msg"]["list"]
        #将搜索出来的结果取第一条以便于后续进行审核操作
        if pay_data:
            data = {"pay_id": pay_data[0]["id"]}
            write_extract_yaml(data)

    @allure.story("支付功能测试用例")
    @pytest.mark.run(ording=2)
    @pytest.mark.skip("用例跳过")
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/payauting_pay.yaml'))
    def test_payauting_pay(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        RequestUtil().analysis_yaml(testcase_info)



