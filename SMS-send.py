# -*- coding:utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from pyeoskit import wallet
from pyeoskit import eosapi
from pyeoskit import db as eosdb

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import datetime
import json
import random
import pymysql
import traceback
import http.client
import urllib
import urllib.parse
import zhenzismsclient as smsclient

os.chdir('/home/uuos2/pyeos/build/programs/data-dir')

def mainland(phone,code):
    api_url = 'https://sms_developer.zhenzikj.com'
    app_id = '100207'#榛子云id
    app_secret = '062ba82e-5c9b-4702-9105-feb2173123cb'#榛子云秘钥
    client = smsclient.ZhenziSmsClient(apiUrl=api_url,appId=app_id,appSecret=app_secret)
    code = code
    result = client.send(phone,'云区块---您的验证码为：%r'% code)
    return result

def check_member(phone,aera):
    phone_new = phone
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    select_sql = 'SELECT phone_num FROM Tel.member WHERE aera = "%s";' % aera
    cursor.execute(select_sql)
    phone_number = cursor.fetchall()
    tempoary_stack = []
    for phone_num in phone_number:
        tempoary_stack.append(phone_num[0])
    if phone_new in tempoary_stack:
        return False
    else:
        return True

def save_code(phone,code):
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_sql = 'INSERT INTO Tel.phone (phone_num,code,time) VALUES ("%s","%s","%s")' % (phone,code,date_time)
    cursor.execute(insert_sql)
    db.commit()
    db.close()


def check_code(phone,code):
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    date_time_now = datetime.datetime.now()
    date_time_now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    select_sql = 'SELECT code FROM Tel.phone WHERE phone_num="%s";' % (phone)
    select_time_sql = 'SELECT time FROM Tel.phone WHERE phone_num = "%s";' % (phone)
    execute = cursor.execute(select_sql)
    if execute:
        rewire_code = cursor.fetchall()[0][0]
        cursor.execute(select_time_sql)
        select_time = cursor.fetchall()[0][0]
        seconds = (date_time_now-select_time).seconds
        if seconds > 60:
            update_time_sql = 'UPDATE Tel.phone SET time = "%s" WHERE phone_num = "%s";' % (date_time_now_str,phone)
            cursor.execute(update_time_sql)
            update_code_sql = 'UPDATE Tel.phone SET code = "%s" WHERE phone_num = "%s";' % (code,phone)
            cursor.execute(update_code_sql)
            db.commit()
            db.close()
            return code
        else:
            return rewire_code
    else:
        return None

def get_code():
    code = ''
    j=4
    code = ''.join(str(i) for i in random.sample(range(0,9),j))
    return code

def abroad(phone,code):
    title = "+"
    mobile = title+phone
    apikey = 'a6830fe4f837bd77a69e4795c664b544'#云片秘钥
    tpl_id = 2626382
    tpl_value = {'#code#':code}
    sms_host = 'sms.yunpian.com'
    port = 443
    sms_tpl_send_url = '/v2/sms/tpl_single_send.json'
    params = urllib.parse.urlencode({
        'apikey':apikey,
        'tpl_id':tpl_id,
        'tpl_value':urllib.parse.urlencode(tpl_value),
        'mobile':mobile
    })
    headers = {
        'Content-type':'application/x-www-form-urlencoded',
        'Accept':'text/plain'
    }
    connect = http.client.HTTPSConnection(sms_host,port,timeout=30)
    connect.request('POST',sms_tpl_send_url,params,headers=headers)
    response = connect.getresponse()
    response_str = response.read()
    connect.close()
    return response_str

def register(phone):
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    sql = 'SELECT code FROM Tel.phone WHERE phone_num = "%s"' % (phone)
    execute = cursor.execute(sql)
    if execute:
        return cursor.fetchall()[0][0]
    else:
        return None

def delete_code(phone):
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    sql = 'DELETE FROM Tel.phone WHERE phone_num = "%s"' % (phone)
    cursor.execute(sql)
    db.commit()
    db.close()

def save_member(phone,aera,owner_key,active_key,user_name):
    db = pymysql.connect('localhost', 'root', 'morning321', 'Tel')
    cursor = db.cursor()
    sql = 'INSERT INTO Tel.member (phone_num,aera,owner_key,active_key,user_name) VALUES ("%s","%s","%s","%s","%s")' % (phone,aera,owner_key,active_key,user_name)
    cursor.execute(sql)
    db.commit()
    db.close()

def HK_TW_Macao(phone,code):
    title = "+"
    mobile = title + phone
    apikey = 'a6830fe4f837bd77a69e4795c664b544'
    tpl_id = 2626348
    tpl_value = {'#code#': code}
    sms_host = 'sms.yunpian.com'
    port = 443
    sms_tpl_send_url = '/v2/sms/tpl_single_send.json'
    params = urllib.parse.urlencode({
        'apikey': apikey,
        'tpl_id': tpl_id,
        'tpl_value': urllib.parse.urlencode(tpl_value),
        'mobile': mobile
    })
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    connect = http.client.HTTPSConnection(sms_host, port, timeout=30)
    connect.request('POST', sms_tpl_send_url, params, headers=headers)
    response = connect.getresponse()
    response_str = response.read()
    connect.close()
    return response_str

def create_account(active_key,owner_key,user_name):
    eosdb.reset()
    nodes = ['192.168.0.171:8888']
    eosapi.set_nodes(nodes)
    wallet.open('mywallet2')
    wallet.unlock('mywallet2', 'PW5KWRvBGMhinrSwoQK4WPWxj5jQa2nVfwwCMUazLTzoi7bsW9MEj')
    wallet.import_key('mywallet2', '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3')
    eosapi.create_account('eosio', user_name, active_key, owner_key)
    if eosapi.get_account(user_name):
        return True
    else:
        return False

def check_userid(s):
    if len(s) == 12:
        j=0
        for i in s:
            if i.isalpha()==True:
                if i.islower() == True:
                    continue
                else:
                    return False
            elif i.isdigit()==True:
                if int(i)>=1 and int(i)<=5:
                    continue
                else:
                    return False
            else:
                return False
        return True
    else:
        return False

def check_user_name_exist(user_name):
    db = pymysql.connect('localhost','root','morning321','Tel')
    cursor = db.cursor()
    sql = 'SELECT * FROM Tel.member WHERE user_name="%s";' % (user_name)
    execute = cursor.execute(sql)
    if execute:
        return False
    else:
        return True

class MainHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(32)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin","*")
        self.set_header("Access-Control-Allow-Headers","x-requested-with")
        self.set_header("Access-Control-Allow-Methods",'POST,GET,OPTIONS')

    @tornado.gen.coroutine
    def get(self):
        '''get接口'''
        htmlStr = '''
                         <!DOCTYPE HTML><html>
                         <meta charset="utf-8">
                         <head><title>Get page</title></head>
                         <body>
                         <form		action="/post"	method="post" >
                         area:<br>
                         <input type="text"      name ="area"     /><br>
                         phone:<br>
                         <input type="text"      name ="phone"     /><br>
                         Verification Code: <br>
                         <input type="text"      name ="verification_code"     /><br>
                         owner key:<br>
                         <input type="text"      name ="owner_key"     /><br>
                         active key:<br>
                         <input type="text"      name ="active_key"     /><br>
                         user name: <br>
                         <input type="text"      name ="user_name"     /><br>
                         
                         <input type="submit"	value="get code"	/>
                         </form></body> </html>
                     '''
        self.write(htmlStr)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        '''post接口， 获取参数'''
        aera = self.get_argument("area", None)
        phone = self.get_argument("phone", None)
        verification_code = self.get_argument("verification_code",None)
        owner_key = self.get_argument("owner_key",None)
        active_key = self.get_argument("active_key",None)
        user_name = self.get_argument("user_name",None)
        yield self.coreOperation(aera, phone,verification_code,owner_key,active_key,user_name)

    @run_on_executor
    def coreOperation(self, aera, phone,verification_code,owner_key,active_key,user_name):
        '''主函数'''
        try:
            code = get_code()
            mobile = aera + phone
            #aera=国际区号
            if owner_key and active_key and user_name :
                if check_userid(user_name):
                    if check_user_name_exist(user_name):
                        if create_account(owner_key,active_key,user_name):
                            save_member(phone,aera,owner_key,active_key,user_name)
                            delete_code(mobile)
                            result = json.dumps({'code':320,'result':'Registration success'})
                            self.write(result)
                        else:
                            result = json.dumps({'code':330,'result':'Key is error'})
                            self.write(result)
                    else:
                        result = json.dumps({'code':350,'result':' User name already exists. '})
                        self.write(result)
                else:
                    result = json.dumps({'code':340,'result':'User name format is error'})
                    self.write(result)
            else:
                if verification_code:
                    verification = register(mobile)
                    if verification == None or verification != verification_code:
                        result = json.dumps({'code':230,'result':' Invalid validation code.'})
                        self.write(result)
                    else:
                        delete_code(mobile)
                        result = json.dumps({'code':240,'result':' Verifying Pass'})
                        self.write(result)
                else:
                    if aera == '86':
                        if len(mobile) == 13:
                            check = check_member(phone,aera)  # 可调用其他接口
                            if check:
                                if check_code(mobile,code):
                                    if check_code(mobile,code) != code:
                                        result = json.dumps({'code':260,'result':' The verification code has been sent. '})
                                        self.write(result)
                                    else:
                                        send_sms = mainland(phone,check_code(mobile,code))
                                        result = send_sms
                                        self.write(result)
                                else:
                                    send_sms = mainland(phone,code)
                                    save_code(mobile,code)
                                    result = send_sms
                                    self.write(result)
                            else:
                                result = json.dumps({'code':210,'result':' Mobile phone number has been registered. '})
                                self.write(result)
                        else:
                            result = json.dumps({
                                'code':220,
                                'result':'Error phone number!'
                            })
                            self.write(result)
                    elif aera == '852' or aera == '853': #852=香港，853=澳门，886=台湾，1=加拿大，49=德国，33=法国，44=英国，81=日本，1=美国
                        mobile = aera+phone
                        if len(mobile) == 11:
                            check = check_member(phone,aera)
                            if check:
                                if check_code(mobile,code):
                                    if check_code(mobile, code) != code:
                                        result = json.dumps(
                                            {'code': 260, 'result': ' The verification code has been sent. '})
                                        self.write(result)
                                    else:
                                        send_sms = HK_TW_Macao(phone,check_code(mobile,code))
                                        result = send_sms
                                        self.write(result)
                                else:
                                    send_sms = HK_TW_Macao(phone,code)
                                    save_code(mobile,code)
                                    result = send_sms
                                    self.write(result)
                            else:
                                result = json.dumps({'code':210,'result':' Mobile phone number has been registered.'})
                                self.write(result)
                        else:
                            result = json.dumps({
                                'code': 220,
                                'result': 'Error phone number!'
                            })
                            self.write(result)
                    elif aera == '886':
                        mobile = aera+phone
                        if len(mobile) == 13:
                            check = check_member(phone, aera)
                            if check:
                                if check_code(mobile,code):
                                    if check_code(mobile, code) != code:
                                        result = json.dumps(
                                            {'code': 260, 'result': ' The verification code has been sent. '})
                                        self.write(result)
                                    else:
                                        send_sms = HK_TW_Macao(phone, check_code(mobile,code))
                                        result = send_sms
                                        self.write(result)
                                else:
                                    send_sms = HK_TW_Macao(phone, code)
                                    save_code(mobile, code)
                                    result = send_sms
                                    self.write(result)
                            else:
                                result = json.dumps({'code':210,'result':' Mobile phone number has been registered.'})
                                self.write(result)
                        else:
                            result = json.dumps({
                                'code': 220,
                                'result': 'Error phone number!'
                            })
                            self.write(result)
                    elif aera == '1' or aera == '33' :
                        mobile = aera+phone
                        if len(mobile) == 11:
                            check = check_member(phone,aera)
                            if check:
                                if check_code(mobile,code):
                                    if check_code(mobile, code) != code:
                                        result = json.dumps(
                                            {'code': 260, 'result': ' The verification code has been sent. '})
                                        self.write(result)
                                    else:
                                        send_sms = abroad(phone,check_code(mobile,code))
                                        result = send_sms
                                        self.write(result)
                                else:
                                    send_sms = abroad(phone,code)
                                    save_code(mobile,code)
                                    result = send_sms
                                    self.write(result)
                            else:
                                result = json.dumps({'code':210,'result':' Mobile phone number has been registered.'})
                                self.write(result)
                        else:
                            result = json.dumps({
                                'code': 220,
                                'result': 'Error phone number!'
                            })
                            self.write(result)
                    elif aera == '49' or aera == '44' or aera == '81':
                        mobile = aera + phone
                        if len(mobile) == 12:
                            check = check_member(phone, aera)
                            if check:
                                if check_code(mobile,code):
                                    if check_code(mobile, code) != code:
                                        result = json.dumps(
                                            {'code': 260, 'result': ' The verification code has been sent. '})
                                        self.write(result)
                                    else:
                                        send_sms = abroad(phone, check_code(mobile,code))
                                        result = send_sms
                                        self.write(result)
                                else:
                                    send_sms = abroad(phone, code)
                                    save_code(mobile, code)
                                    result = send_sms
                                    self.write(result)
                            else:
                                result = json.dumps({'code': 210, 'result': ' Mobile phone number has been registered.'})
                                self.write(result)
                        else:
                            result = json.dumps({
                                'code': 220,
                                'result': 'Error phone number!'
                            })
                            self.write(result)
        except Exception:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            result = json.dumps({'code': 503, 'result':'Unknown Error!'})
            self.write(result)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r'/post', MainHandler)], autoreload=False, debug=False)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8349)
    tornado.ioloop.IOLoop.instance().start()
