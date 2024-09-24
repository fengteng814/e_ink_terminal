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

    try:
        response = requests.post(url, json=message_data)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"发送消息失败: {e}")
        return None
