#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, make_response
import hashlib
import xmltodict
import time

app = Flask(__name__)

# 定义允许的用户列表
ALLOWED_USERS = ['op0im6mAyuSX3VSALrBo1bQhlsPs', '87654']

@app.route('/',methods=['GET','POST'])
def index():
    if request.method =='GET':
        token = 'fornoodle'

        # 获取微信服务器发送过来的参数
        data = request.args
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')

        # 对参数进行字典排序，拼接字符串
        temp = [timestamp, nonce, token]
        temp.sort()
        temp = ''.join(temp)

        # 加密
        if (hashlib.sha1(temp.encode('utf8')).hexdigest() == signature):
            return echostr
        else:
            return 'error', 403

    if request.method == 'POST':
        # 获取微信服务器post过来的xml数据
        xml = request.data
        # 把xml格式的数据进行处理，转换成字典进行取值
        req = xmltodict.parse(xml)['xml']
        # 判断post过来的数据中数据类型是不是文本

        msg_type = req.get('MsgType')
        user_id = req.get('FromUserName')
        content = req.get('Content', '').strip()  # 去除首尾空格        

        if user_id not in ALLOWED_USERS:
            print(f"来自非允许用户 {user_id} 的消息，忽略。")
            return '', 200  # 返回空响应，不回复

        if msg_type == 'text':
            if content.startswith("作业"):
                # 提取“作业”后面的内容
                homework_content = content[len("作业"):].strip()
                reply_content = f"ok，收到作业{homework_content}"
                # 在终端显示“作业”后面的内容
                print(homework_content)        

            # 获取用户的信息，开始构造返回数据，把用户发送的信息原封不动的返回过去，字典格式
                resp = {
                    'ToUserName':req.get('FromUserName'),
                    'FromUserName':req.get('ToUserName'),
                    'CreateTime':int(time.time()),
                    'MsgType':'text',
                    'Content':req.get('Content')
                }
            else:
                # 回复“What？”，并返回原消息内容
                reply_content = "GIVE me MORE homework!!!"
                resp = {
                    'ToUserName': req.get('FromUserName'),
                    'FromUserName': req.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': reply_content
                }
                
                # 把构造的字典转换成xml格式
            xml = xmltodict.unparse({'xml':resp})
            # 返回数据
            return xml
        else:
            resp = {
                'ToUserName': req.get('FromUserName', ''),
                'FromUserName': req.get('ToUserName', ''),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': 'I LOVE ITCAST'
            }
            xml = xmltodict.unparse({'xml':resp})
            return xml

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)