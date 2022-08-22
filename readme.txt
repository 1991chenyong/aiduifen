YAML格式用例的约定
1. 必须包含一级关键字：name,request,validate
2. 在request关键字下必须包括：method, url, data 如data没有的话，那么输入默认值{{}}
3. 提取变量使用一级关键字extract，支持json提取和正则表达式提取，使用{{}}取值
4. 可以使用热加载的方式调用debug_talk.py中的DebugTalk类里面的方法，通过${}调用
5. 支持equals和contains两种断言
6. 使用parameters做csv文件的数据驱动，通过$csv{appid}这种格式取值
parameters:
    name-appid-grant_type-secret-eq_str: data/get_token_data.csv
7.框架支持断言非json格式的响应数据，需要在接口标识，使用方法如：
    response_type: text

--------------------------
注意事项
8. 当请求头Content-Type字段包含 json 时, 请求数据格式为键值对，不传表示支持接口请求数据格式为json，此时需要在请求头指定数据格式，如下
    Content-Type: application/json

data与json2个参数，类型既可以是str，也可以是dict
区别如下：

1、不管json是str还是dict，如果不指定headers中的content-type，默认为application/json
2、data参数为dict时，如果不指定content-type，默认为application/x-www-form-urlencoded，相当于普通form表单提交的形式，此时数据可以从request.POST里面获取，
而request.body的内容则为a=1&b=2的这种形式，注意，即使指定content-type=application/json，request.body的值也是类似于a=1&b=2，所以并不能用json.loads(request.body.decode())得到想要的值
3、data参数为str时，如果不指定content-type，默认为application/json
4、用data参数提交数据时，request.body的内容则为a=1&b=2的这种形式，用json参数提交数据时，request.body的内容则为'{"a": 1, "b": 2}'的这种形式
下图是data方式
————————————————
版权声明：本文为CSDN博主「春天的菠菜」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/legend818/article/details/103988698