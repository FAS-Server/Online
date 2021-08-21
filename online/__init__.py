import os
import json
from typing import Optional

from mcdreforged.api.rtext import RAction, RText, RColor, RTextList
from mcdreforged.api.types import PluginServerInterface

from online.RCon import MCRcon, MCRconException

# 默认参数，不要修改
configPath = 'config/online.json'
defaultConfig = {
    "join": True,
    "click_event": True,
    "servers": {
        "serverA": {
            "host": "127.0.0.1",
            "port": 25575,
            "password": "ServerAPassword"
        }
    }
}

config: Optional[dict] = None


def main(host, port, password):  # 连接服务器
    rcon = MCRcon()
    rcon.connect(host, port, password)
    response = rcon.command('list')
    return response


def get_server_rtext(name):
    global config
    if config['click_event']:
        return RText(name, color=RColor.aqua).c(RAction.run_command, f"/server {name}")
    else:
        return RText(name, color=RColor.aqua)


def get_list():  # 获得玩家列表
    global config
    list_text = ''
    for server in config['servers']:
        name = server
        host = config['servers'][name]['host']
        port = config['servers'][name]['port']
        password = config['servers'][name]['password']
        try:
            result = main(host, port, password)
            if result[10] != '0':
                player_list = result[int(result.find(':')) + 1:]
                player_number = result.count(',') + 1
            else:
                player_list = ''
                player_number = 0
            list_text += RTextList(
                get_server_rtext(name),
                RText(" 在线人数:", color=RColor.gray),
                RText(str(player_number), color=RColor.green)
            )
            if player_number != 0:
                list_text += RTextList(
                    RText(" 在线列表:", color=RColor.gray),
                    RText(player_list, RColor.gold)
                )
            list_text += "\n"
        except:
            list_text += RTextList(
                RText(name, color=RColor.aqua),
                RText(" 未开启\n", color=RColor.red)
            )
    return list_text


def convent_config(server: PluginServerInterface):
    # server.logger.info("检测到旧的配置文件, 进行升级中...")
    old_config: dict = json.load(open(configPath))
    new_config = {'servers': {}}
    i = 1
    while True:
        if str(i) in old_config:
            rcon_server = old_config.pop(str(i))
            server_name = rcon_server.pop('name')
            new_config['servers'][server_name] = rcon_server
            new_config['servers'][server_name]['port'] = int(rcon_server['port'])
            i += 1
        else:
            break
    values = ["join", "click_event"]
    for var in values:
        if var in old_config:
            new_config[var] = old_config.pop(var)
    os.remove(configPath)
    server.save_config_simple(new_config)


def on_info(server: PluginServerInterface, info):  # 指令显示
    if info.content == '!!online':
        server.say(get_list())


def on_player_joined(server: PluginServerInterface, player, info):  # 进服提示
    if config['join']:
        server.tell(player, get_list())


def on_load(server: PluginServerInterface, old):  # 添加帮助
    global config
    server.register_help_message('!!online', '查询在线列表/人数')
    if os.path.exists(configPath):
        convent_config(server)
    config = server.load_config_simple(default_config=defaultConfig)
