# createaccountbyphone
# 用户注册功能

# 安装环境
```
pip install -r requirements.txt
mysql -u root -p Tel < Tel.sql
python3 SMS-send.py
```
```
修改榛子云id：mainland函数下app_id
修改榛子云秘钥：mainland函数下app_secret
修改云片api秘钥：abroad，HK_TW_Macao两个函数下apikey变量
修改云片模板id：abroad，HK_TW_Macao两个函数下tpl_id变量
```

# 短信服务供应商
```
国内短信：榛子云
国际短信：云片
```
# 国际短信测试手机号获取网址
```
https://smsreceivefree.com/
剩余测试条数：7条
```
# 短信验证码接口

```
请求端口http://localhost:8349/post
```
```
参数类型：
        area（国际区号）
        phone（手机号码）
        verification_code（手机验证码）
        user_name（账户名）
        owner_key（公钥1）
        active_key（公钥2）
```
# 注册流程
```
获取验证码

import requests

url = "http://127.0.0.1:8349/post"

querystring = {"area":"86","phone":"13110651535"}

payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "8bcd4c80-8f17-45c6-9ce8-6bcd750f9b52"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

#return
{"code":0,"data":"发送成功"}
```
```
判断验证码是否正确

import requests

url = "http://127.0.0.1:8349/post"

querystring = {"area":"86","phone":"13123392061","verification_code":"7604"}

payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "d538d79d-8967-4726-b1c9-92af9daa02fe"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

#return
{"code": 240, "result": " Verifying Pass"}
```
```
输入公钥以及合法用户名完成注册

import requests

url = "http://127.0.0.1:8349/post"

querystring = {"area":"86","phone":"13123392061","verification_code":"7604","active_key":"EOS7Wpfx1s679kmq2wbTwc1q1yk2vt2cEVhwgLSqNyddEwFfoPEDC","owner_key":"EOS6msLCpSH3bxAKPeaWUt1PmBc4JeRTjqYyasYpx1KpDnf7ffydH","user_name":"uuos12344321"}

payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "4980cee4-d17d-4826-8144-8f4cf5425f0a"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)

#return
{"code": 320, "result": "Registration success"}
```
# 返回值&对应结果
```
code = 0：验证码发送成功
code = 210：手机号码已注册
code = 220：手机号码格式错误
code = 230：验证码错误
code = 240：验证码正确
code = 260：验证码已发送，请勿重复获取
code = 320：注册成功
code = 330：公钥错误
code = 350：用户名已存在
code = 340： 用户名格式错误
code = 503：未知错误（可能由于服务器宕机，nodes不通等等情况）
```
