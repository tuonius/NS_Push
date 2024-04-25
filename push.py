#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import os

tg_user_id = os.environ.get('tg_user_id')
tg_bot_token = os.environ.get('tg_bot_token')


def push_message(title: str, content: str) -> None:
    """
    使用 telegram 机器人 推送消息。
    """
    # 检查环境变量是否设置
    if tg_user_id is None or tg_bot_token is None:
        print("请确保 tg_user_id 和 tg_bot_token 环境变量已设置！")
        return
    else:
        print("tg_user_id:", tg_user_id)
        print("tg_bot_token:", tg_bot_token)

    url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "chat_id": tg_user_id,
        "text": f"{title}\n----\n{content}",
        "disable_web_page_preview": "true",
    }
    proxies = None
    response = requests.post(
        url=url, headers=headers, params=payload, proxies=proxies
    ).json()

    if response["ok"]:
        print("tg 推送成功！")
    else:
        print("tg 推送失败！")
