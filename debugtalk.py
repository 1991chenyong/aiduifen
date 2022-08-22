import time
import random
import pymysql
from common.logger_util import write_error_log, write_log


class DebugTalk(object):

    def get_random_number(self):
        return random.randint(20190616000001, 20190616999999)

    def get_token_data(self):
        return [
            {"appid": "wx07df0de943e4669f", "grant_type": "client_credential", "secret": "970cad5163a8954fc4d8423a8a15ced0", "eq_str": "access_token"},
            {"appid": "", "grant_type": "client_credential", "secret": "client_credential", "eq_str": "errcode"},
            {"appid": "2222", "grant_type": "client_credential", "secret": "970cad5163a8954fc4d8423a8a15ced0", "eq_str": "errcode"}
        ]

    # 获取时间
    def get_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    def get_addone_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+1))

    def get_addtwo_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+2))

    def get_addthree_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+3))

    def get_reduceone_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-1))

    def get_reducetwo_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-2))

    def get_reducethree_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-3))

    def get_reducefour_time(self, num=0):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()-4))


if __name__ == "__main__":
    # sql_dict = {
    #     "token": 'select token from bs_customer_tokens where customer_id = (select id from bs_customers where code = "WMS");',
    #     "code": 'select temp_token from sys_users where user_name = "lishenping";'
    # }
    # sql_search = 'select temp_token from sys_users where user_name = "lishenping";'
    # data_dict = DebugTalk().connect_mysql(sql_search)
    # print(data_dict)
    sql1 = 'SELECT shipping_no from warehouse_handover where handover_no = "REC202103090006";'
    sql2 = 'SELECT id,send_time from shipping where shipping_no = "SLN2103090003";'
    print(DebugTalk().get_time())
    print(DebugTalk().get_time(10))
