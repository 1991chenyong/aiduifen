import re
import yaml



result = '{"return_code":"SUCCESS","return_msg":{"taskId":88,"checkErrNum":0}}'
data = re.search('{"taskId":(.+?),', result)
# with open('testcases/userManage_load_adf.yaml', encoding='utf-8') as f:
#     data2 = yaml.full_load(f.read())
# print("data2=", data2[0]["extract"]["taskId"])
# value = data2[0]["extract"]["taskId"]
print(data)
print(data.group(1))
# data3 = re.search(value, result)
# print(data3)

