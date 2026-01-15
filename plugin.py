"""
这里实现插件的主逻辑，将core中模块功能进行组装

 - 获取群成员列表：通过napcat的api获取指定群聊的成员列表
 - 抽老婆：随机选择一个群u，检测当日是否抽过老婆
 - 群老婆检测：若本日抽过老婆则不再抽取新的群老婆

 群老婆检测是基于文件读写实现的，群老婆数据将储存在data文件夹下，为一个字典，键为user_id，值为群老婆id
"""
import datetime
import json
import os
from pathlib import Path
from typing import Optional, Type, Tuple, List

from .core import (get_group_user_list,
                   select_wife,
                   get_member_info,
                   send_already_obtained_wife,
                   send_bot_selected,
                   send_today_wife)
from src.config.config import global_config
from src.plugin_system import (BaseCommand,
                               BasePlugin,
                               register_plugin,
                               ConfigField,
                               ComponentInfo,
                               chat_api,
                               get_logger)

logger = get_logger("wife_plugin")

class WifeCommand(BaseCommand):
    command_name = "wife_plugin"
    command_description = "这是一个抽老婆插件，可以在群里随机抽一位群u当一天群老婆~"
    command_pattern = r'\b抽老婆\b'

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        #读取配置文件
        bot_id = global_config.bot.qq_account
        port = self.get_config("napcat.port")
        target = self.get_config("other.target")
        napcat_token = self.get_config("napcat.napcat_token")
        #获取聊天流信息
        chat_stream = self.message.chat_stream
        stream_type = chat_api.get_stream_type(chat_stream)
        user_id = chat_stream.user_info.user_id
        if stream_type != "group":
            logger.error("私聊流不支持抽老婆功能")
            return False, "私聊流不支持抽老婆功能", False
        group_id = chat_stream.group_info.group_id
        #建立新文件夹，用来储存抽老婆数据
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        # 获取当前文件所在的绝对目录
        current_dir = Path(__file__).parent.absolute()
        # 构建绝对路径
        data_dir = current_dir / "data"
        json_file = data_dir / f"{date}_{group_id}.json"
        # 创建data目录
        os.makedirs(data_dir, exist_ok=True)
        if not os.path.exists(json_file):
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        #判断用户是否在target列表内
        if int(user_id) in target:
            flag , res = await send_bot_selected(bot_id , port , user_id , group_id , napcat_token)
            if not flag:
                error_message = res
                logger.error(error_message)
                return False , error_message , True
            return True , "执行成功" , True
        # 获取成员列表
        flag, group_member_list = await get_group_user_list(port ,group_id, napcat_token)
        if not flag:
            error_message = group_member_list
            logger.error(error_message)
            return False, error_message, True
        # 随机选择一位群u做群老婆
        while True:
            flag, wife_info = select_wife(group_member_list)
            if not flag:
                error_message = wife_info
                logger.error(error_message)
                return False, error_message, True
            if str(wife_info.user_id) != str(user_id):
                break
        #检测到用户今日抽过群老婆
        if not data.get(f"{user_id}") is None:
            wife_id = data.get(f"{user_id}")
            #获取已抽到的群老婆信息
            flag , wife_info = await get_member_info(port ,group_id, wife_id ,napcat_token)
            if not flag:
                error_message = wife_info
                logger.error(error_message)
                return False, error_message, True
            #判断抽到的群老婆是不是麦麦
            if str(wife_id) == str(bot_id):
                flag , res = await send_bot_selected(bot_id , port , user_id , group_id , napcat_token)
                if not flag:
                    error_message = wife_info
                    logger.error(error_message)
                    return False, error_message, True
                return True , "执行成功" , True
            #发送已抽取的群老婆信息
            flag , res = await send_already_obtained_wife(port , user_id, wife_info , napcat_token)
            if not flag:
                error_message = res
                logger.error(error_message)
                return False, error_message, True
            return True , "执行成功" , True
        #检测抽到的是麦麦自己，并发送抽老婆结果
        if str(wife_info.user_id) == str(bot_id):
            flag , res = await send_bot_selected(bot_id, port, user_id, group_id , napcat_token)
            if not flag:
                error_message = res
                logger.error(error_message)
                return False, error_message, True
            #保存抽老婆结果
            data[f"{user_id}"] = wife_info.user_id
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                return True, "执行成功", True
        #抽到的不是麦麦，直接发送抽老婆结果
        flag , res = await send_today_wife(port , user_id , wife_info , napcat_token)
        if not flag:
            error_message = res
            logger.error(error_message)
            return False , error_message, True
        #更新群老婆信息并保存到文件
        data[f"{user_id}"] = wife_info.user_id
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True, "执行成功" , True

@register_plugin
class WifePlugin(BasePlugin):
    """群老婆娱乐插件"""
    plugin_name = "wife_plugin"
    enable_plugin = True
    dependencies = []
    python_dependencies = []
    config_file_name = "config.toml"
    config_schema = {
        "plugin": {
            "name": ConfigField(type = str , default = "wife_plugin" , description = "插件名称"),
            "enabled": ConfigField(type = bool , default = True , description = "是否启用插件"),
            "config_version": ConfigField(type= str,default="1.0.1",description="配置文件版本")
        },
        "napcat":{
            "port": ConfigField(type = int , default = 6666 , description = "napcat端口"),
            "napcat_token": ConfigField(type=str , default='',description="token,建议设置以增强安全性")
        },
        "other":{
            "target": ConfigField(type = list , default= [0] , description = "神秘开关，改成某个qq号可以让此用户始终抽到麦麦")
        }
    }
    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        return [
            (WifeCommand.get_command_info(), WifeCommand)
        ]