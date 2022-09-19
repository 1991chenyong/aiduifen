# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/09/08
# @Email:775375798@qq.com
# @File: test_banner.py


import pytest
from common.parameters_util import read_testcase_yaml
from common.requests_util import RequestUtil
from common.common_util import write_extract_yaml,read_config_yaml
import allure


@allure.epic("爱兑分总后台项目")
@allure.feature("升级提示模块")
class TestUpgrade:

    @allure.story("升级-更新提示列表搜索测试用例")
    @pytest.mark.skip("用例跳过")
    @pytest.mark.run(ording=1)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/upgrade_search.yaml'))
    def test_search(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        RequestUtil().analysis_yaml(testcase_info)

    @allure.story("新建升级功能测试用例")
    @pytest.mark.skip("测试用例跳过")
    @pytest.mark.run(ording=2)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/create_version.yaml'))
    def test_create_version(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        RequestUtil().analysis_yaml(testcase_info)

    @allure.story("删除升级更新数据测试用例")
    @pytest.mark.skip("测试用例跳过")
    @pytest.mark.run(ording=3)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/delete_version.yaml'))
    def test_delete_upgrade_version(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        version_data = RequestUtil().analysis_yaml(read_testcase_yaml('testcases/marketManage/upgrade_search1.yaml')[0])["return_msg"]["list"]
        print("version_data=====", version_data)
        version_del_data= None
        for del_data in version_data:
            if del_data["appVerTitle"] == read_config_yaml('test_data', 'appVerTitle'):
                version_del_data = del_data
                write_extract_yaml({"_id": version_del_data["_id"]})
                break
        if version_del_data is None:
            write_extract_yaml({"_id": version_data[0]["_id"]})
        RequestUtil().analysis_yaml(testcase_info)





