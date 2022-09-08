# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/09/08
# @Email:775375798@qq.com
# @File: test_wakuang.py.py

import pytest
from common.parameters_util import read_testcase_yaml
from common.requests_util import RequestUtil
import allure


@allure.epic("爱兑分后台自动化接口项目")
@allure.feature("每日任务成就列表")
class TestTaskAndChievement:

    @pytest.mark.skip("用例跳过")
    @allure.story("每日任务详情获取-编辑测试用例")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/get_task_detail.yaml'))
    def test_task_detail(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        task_detail = RequestUtil().analysis_yaml(testcase_info)
        # 循环编辑7个任务
        for i in range(0, len(task_detail["return_msg"]["taskList"])):
            edit_testcase_info = read_testcase_yaml('testcases/marketManage/edit_wakuangtask.yaml')[0]
            print("edit_testcase_info===", edit_testcase_info)
            edit_testcase_info["request"]["data"] = task_detail["return_msg"]["taskList"][i]
            RequestUtil().analysis_yaml(edit_testcase_info)

    @pytest.mark.skip("用例跳过")
    @allure.story("成就配置详情获取-编辑测试用例")
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('testcase_info', read_testcase_yaml('testcases/marketManage/get_achievement_detail.yaml'))
    def test_achievement_detail(self, testcase_info):
        allure.dynamic.title(testcase_info["name"])
        task_detail = RequestUtil().analysis_yaml(testcase_info)
        # 循环编辑7个成就配置
        for i in range(0, len(task_detail["return_msg"]["taskList"])):
            edit_testcase_info = read_testcase_yaml('testcases/marketManage/edit_achievement.yaml')[0]
            edit_testcase_info["request"]["data"] = task_detail["return_msg"]["taskList"][i]
            RequestUtil().analysis_yaml(edit_testcase_info)






