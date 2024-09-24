# message_queue.py
# 共享消息队列，用于在Flask和GUI之间传递消息
import queue

# 创建一个线程安全的队列
message_queue = queue.Queue()

# 发送微信消息的模块，封装与微信的交互逻辑
import requests

def send_message(user_id, content):
    # 微信发送消息的逻辑
    access_token = "fornoodle"  # 替换为实际的access token
    url = f"https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={access_token}"

    message_data = {
        "touser": user_id,
        "msgtype": "text",
        "text": {
            "content": f"搞定了：{content}"
        }
    }

    response = requests.post(url, json=message_data)
    return response.json()
