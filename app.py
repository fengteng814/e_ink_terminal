# app.py
# Flask 应用，处理微信消息和作业内容的接收与响应
from flask import Flask, request
import hashlib
import xmltodict
import time
from message_queue import message_queue
from homework_records import homework_records, HomeworkRecord  # 导入作业记录

app = Flask(__name__)

# 定义允许的用户列表（微信ID）
ALLOWED_USERS = ['op0im6mAyuSX3VSALrBo1bQhlsPs', 'op0im6vauI2bVFi6fGPfySm6OYe4']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        token = 'fornoodle'

        # 获取微信服务器发送过来的参数
        data = request.args
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')

        # 对参数进行字典排序，拼接字符串
        temp = sorted([timestamp, nonce, token])
        temp_str = ''.join(temp)

        # 加密
        hashcode = hashlib.sha1(temp_str.encode('utf8')).hexdigest()
        if hashcode == signature:
            print("服务器验证成功，返回echostr。")
            return echostr
        else:
            print("服务器验证失败，返回错误。")
            return 'error', 403

    if request.method == 'POST':
        try:
            # 获取微信服务器post过来的xml数据
            xml = request.data
            # 把xml格式的数据进行处理，转换成字典进行取值
            req = xmltodict.parse(xml)['xml']

            # 获取消息类型、发送者微信ID和内容
            msg_type = req.get('MsgType')
            user_id = req.get('FromUserName')
            content = req.get('Content', '').strip()  # 去除首尾空格

            # 检查是否是允许的用户
            if user_id not in ALLOWED_USERS:
                print(f"来自非允许用户 {user_id} 的消息，忽略。")
                return '', 200  # 返回空响应，不回复

            if msg_type == 'text':
                if content.startswith("作业"):
                    # 提取“作业”后面的内容
                    homework_content = content[len("作业"):].strip()
                    reply_content = f"ok，收到作业\n\n{homework_content}"

                    # 在终端显示“作业”后面的内容
                    print(f"{user_id}：{homework_content}")

                    # 更新作业记录
                    record = HomeworkRecord(homework_content)
                    homework_records.append(record)

                    # 将消息插入到GUI队列
                    message_queue.put((user_id, homework_content))

                elif content.startswith("爱豆"):
                    reply_content = "我最爱爸爸"

                elif content.startswith("？"):
                    if homework_records:
                        content = "\n".join(
                            f"{record.content} - {'完成' if record.completed else '未完成'}"
                            for record in homework_records
                        )
                        reply_content = content
                    else:
                        reply_content = "我在玩呢，又没有作业"

                else:
                    reply_content = "Give me MORE homework!!!!"
                    # 不在终端显示消息内容

                # 构造回复消息
                resp = {
                    'ToUserName': req.get('FromUserName'),
                    'FromUserName': req.get('ToUserName'),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': reply_content
                }

                # 把构造的字典转换成xml格式
                response_xml = xmltodict.unparse({'xml': resp})
                return response_xml
            else:
                # 对于非文本消息，回复“What？”
                reply_content = "What？"
                resp = {
                    'ToUserName': req.get('FromUserName', ''),
                    'FromUserName': req.get('ToUserName', ''),
                    'CreateTime': int(time.time()),
                    'MsgType': 'text',
                    'Content': reply_content
                }
                response_xml = xmltodict.unparse({'xml': resp})
                return response_xml

        except Exception as e:
            print(f"处理请求时出错: {e}")
            return 'Internal Server Error', 500
