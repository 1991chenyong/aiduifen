import re
import yaml



result = '{"return_code":"SUCCESS","return_msg":{"taskId":88,"checkErrNum":0}}'
data = re.search('{"taskId":(.+?),', result)
