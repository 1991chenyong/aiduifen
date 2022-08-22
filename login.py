import requests
import pytest
import json



params2 = {
    "t": t,
    "isgray": 1,
    "page": 0,
    "pagesize": 10
}
res3= session.request(method='get', url="http://miniprogram-aiduifen-test.tongdui8.com/superAdmin/points-mall-authorization/get-nft-manage-list", params = params2)
print(res3.content)