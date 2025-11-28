"""
定义成员信息类以及获取群员信息和群老婆信息的函数

get_group_user_list：通过napcat的/get_group_member_list接口获取指定群的群员信息列表
get_member_info：通过user_id来查询某个群员的成员信息（用于读取已抽取到的群老婆信息）
select_wife：在群员信息列表中随机选择一个

"""
import json
import random
from typing import Union, Tuple
import aiohttp


class MemberInfo:
    group_id : str
    user_id : str
    nickname : str
    card : str
    sex : str
    age : int
    area : str
    level : str
    qq_level : int
    join_time : int
    last_send_time : int
    title_expire_time : int
    unfriendly : bool
    card_changeable : bool
    is_robot : bool
    shut_up_timestamp : int
    role : str
    title : str
    def __init__(self,data:dict) -> None:
        self.group_id = data.get("group_id")
        self.user_id = data.get("user_id")
        self.nickname = data.get("nickname")
        self.card = data.get("card")
        self.sex = data.get("sex")
        self.age = data.get("age")
        self.area = data.get("area")
        self.level = data.get("level")
        self.qq_level = data.get("qq_level")
        self.join_time = data.get("join_time")
        self.last_send_time = data.get("last_send_time")
        self.title_expire_time = data.get("title_expire_time")
        self.unfriendly = data.get("unfriendly")
        self.card_changeable = data.get("card_changeable")
        self.is_robot = data.get("is_robot")
        self.shut_up_timestamp = data.get("shut_up_timestamp")
        self.role = data.get("role")
        self.title = data.get("title")

async def get_group_user_list(port: int,group_id: Union[str,int]) -> Tuple[bool, Union[list, str]]:
    """
    Args:
        port: napcat设置的端口
        group_id:目标群组id
    Returns:
        bool:是否执行成功
        list | str :成功时返回包含群成员信息的列表，失败返回错误信息

    """
    url = "get_group_member_list"
    base_napcat_url = f"http://127.0.0.1:{port}/{url}"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        "group_id": group_id,
        "no_cache": False
    })
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request("POST",base_napcat_url,headers=headers,data=payload) as response:
                res = await response.json()
                data = res.get("data")
                return True, data

    except BaseException as e:
        # logger.error(f"成员列表请求发生错误{str(e)}")
        return False , f"成员列表请求发生错误{str(e)}"

async def get_member_info(port: int ,group_id : str|int , user_id: str|int) -> Tuple[bool, Union[MemberInfo, str]]:
    url = "get_group_member_info"
    base_napcat_url = f"http://127.0.0.1:{port}/{url}"
    payload = json.dumps({
        "group_id": group_id,
        "user_id": user_id,
        "no_cache": True
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request("POST", base_napcat_url, headers=headers, data=payload) as response:
                res = await response.json()
                data = res.get("data")
                if data is None:
                    return False, "获取群成员信息出错"
                return True, MemberInfo(data)
    except BaseException as e:
        return False , f"获取群成员信息出错:{str(e)}"

def select_wife(data: list) -> tuple[bool, Union[MemberInfo, str]]:
    try:
        wife_info = random.choice(data)
        return True , MemberInfo(wife_info)
    except BaseException as e:
        return False , f"抽老婆失败:{str(e)}"