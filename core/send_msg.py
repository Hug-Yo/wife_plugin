"""
这个模块将利用napcat的/send_group_msg接口进行消息发送

send_today_wife：发送抽取到的群老婆的格式化信息
send_already_obtained_wife：用户今日已抽取过老婆，则调用此函数发送已获取的群老婆的格式化信息
send_bot_selected：如果麦麦被选中，则调用此函数发送格式化信息

"""
import json
from typing import Union
import aiohttp
from plugins.wife_plugin.core.wife_info_fetch import MemberInfo

async def send_today_wife(port: int , user_id: str|int , wife_info: MemberInfo) -> tuple[bool, Union[None, str]] :
    """
    成功抽取到今日群老婆后调用此函数

    Args:
        port: napcat设置的port
        user_id: 抽取群老婆的群u的qq号
        wife_info: 抽取到的群老婆信息
    Returns:
        bool:是否执行成功
        None|str: 成功返回None，失败返回错误信息
    """
    url = "send_group_msg"
    base_napcat_url = f"http://127.0.0.1:{port}/{url}"

    payload = json.dumps({
        "group_id": wife_info.group_id,
        "message": [
            {
                "type": "at",
                "data":
                {
                    "qq": user_id
                }
            },
            {
                "type": "text",
                "data":
                    {
                        "text": "\n你今天的群老婆是:"
                    }
            },
            {
                "type": "image",
                "data":
                    {
                        "file": f"https://q1.qlogo.cn/g?b=qq&nk={wife_info.user_id}&s=640",
                        "summary": "[图片]"
                    }
            },
            {
                "type": "text",
                "data":
                    {
                        "text": f"{wife_info.nickname}({wife_info.user_id})"
                    }
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.request(method='POST', url=base_napcat_url, headers=headers, data=payload) as response:
            if response.status != 200:
                return False, "发送失败"
            return True, None

async def send_already_obtained_wife(port: int , user_id : int|str , data: MemberInfo) -> tuple[bool, Union[None, str]] :
    """
    用户输入抽老婆指令后，如果今日已经抽过老婆，则执行此函数告知今日已有群老婆
    """
    url = "send_group_msg"
    base_napcat_url = f"http://127.0.0.1:{port}/{url}"
    payload = json.dumps({
        "group_id": data.group_id,
        "message": [
            {
                "type": "at",
                "data":
                    {
                        "qq": user_id
                    }
            },
            {
                "type": "text",
                "data":
                    {
                        "text": "\n你今天已经有群老婆了，要好好对待她哦~"
                    }
            },
            {
                "type": "image",
                "data":
                    {
                        "file": f"https://q1.qlogo.cn/g?b=qq&nk={data.user_id}&s=640",
                        "summary": "[图片]"
                    }
            },
            {
                "type": "text",
                "data":
                    {
                        "text": f"{data.nickname}({data.user_id})"
                    }
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.request(method='POST', url=base_napcat_url, headers=headers, data=payload) as response:
            if response.status != 200:
                return False, "发送失败"
            return True , None

async def send_bot_selected(bot_id: int|str , port: int , user_id: str|int , group_id: str|int) -> tuple[bool, Union[None, str]]:
    url = "send_group_msg"
    base_napcat_url = f"http://127.0.0.1:{port}/{url}"
    bot_id = bot_id
    payload = json.dumps({
        "group_id": group_id,
        "message": [
            {
                "type": "at",
                "data":
                    {
                        "qq": user_id
                    }
            },
            {
                "type": "text",
                "data":
                    {
                        "text": "\n你今天的群老婆是我哦~"
                    }
            },
            {
                "type": "image",
                "data":
                    {
                        "file": f"https://q1.qlogo.cn/g?b=qq&nk={bot_id}&s=640",
                        "summary": "[图片]"
                    }
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.request(method='POST', url=base_napcat_url, headers=headers, data=payload) as response:
            if response.status != 200:
                return False , "发送失败"
            return True , None