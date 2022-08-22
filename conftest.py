# _*_ coding:utf-8 _*-
# 作者：陈勇
# @Time: 2022/5/18
# @Email:775375798@qq.com
# @File: conftest.py

from common.common_util import read_config_yaml
import requests
import pytest
import json
import common.common_util as commonutil
import yaml
import os


# 进行清空extract文件操作
@pytest.fixture(scope="session", autouse=True)
def clean_extract():
    commonutil.clear_extract_yaml()

#登录前置，获取登录信息
@pytest.fixture(scope="session", autouse=True)
def program_login():
    session = requests.session()
    base_data = read_config_yaml('base')
    user_data = {
        "userName": base_data["userName"],
        "password": base_data["password"]
    }
    code = {"code": base_data["code"]}
    session.request(method='post', url='http://admin-test.idouzi.com/amount/login', data=user_data)
    res2 = session.request(method='post', url='http://admin-test.idouzi.com/amount/verify-code', data=code)
    t = json.loads(res2.content)["return_msg"]
    commonutil.write_extract_yaml({"t": t})


if __name__ == '__main__':
    filename = os.path.join(commonutil.get_rootpath(), 'config.yaml')
    with open(file=filename, mode='w', encoding='utf-8') as f:
        yaml.dump(data={"test": "cy"}, stream=f)




