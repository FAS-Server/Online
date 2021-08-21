import socket
import select
import struct
import time
import os
import json
from mcdreforged.api.rtext import RAction, RText, RColor, RTextList

PLUGIN_METADATA = {
    'id': 'online',
    'version': '1.1.0',
    'link': 'https://github.com/FAS-Server/online',
    'author': [
        'A_jiuA', 'Nine_King', 'YehowahLiu'
    ],
    'dependencies': {
        'mcdreforged': '>=1.0.0',
    }
}

# 默认参数，不要修改
configPath = 'config/online.json'
defultConfig = '''
{
    "join": true,
    "click_event": true,
    "1":{
        "name": "ServerA",
        "host": "127.0.0.1",
        "port": "25575",
        "password": "ServerAPassword"
    }
}'''


# mcrcon
class MCRconException(Exception):
    pass


class MCRcon(object):
    socket = None

    def connect(self, host, port, password):
        if self.socket is not None:
            raise MCRconException("Already connected")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.send(3, password)

    def disconnect(self):
        if self.socket is None:
            raise MCRconException("Already disconnected")
        self.socket.close()
        self.socket = None

    def read(self, length):
        data = b""
        while len(data) < length:
            data += self.socket.recv(length - len(data))
        return data

    def send(self, out_type, out_data):
        if self.socket is None:
            raise MCRconException("Must connect before sending data")

        # 发送请求包
        out_payload = struct.pack('<ii', 0, out_type) + out_data.encode('utf8') + b'\x00\x00'
        out_length = struct.pack('<i', len(out_payload))
        self.socket.send(out_length + out_payload)

        # 读取响应包
        in_data = ""
        while True:
            # 读包
            in_length, = struct.unpack('<i', self.read(4))
            in_payload = self.read(in_length)
            in_id, in_type = struct.unpack('<ii', in_payload[:8])
            in_data_partial, in_padding = in_payload[8:-2], in_payload[-2:]

            # 连接检查
            if in_padding != b'\x00\x00':
                raise MCRconException("Incorrect padding")
            if in_id == -1:
                raise MCRconException("Login failed")

            # 记录的响应
            in_data += in_data_partial.decode('utf8')

            # 如果没有更多的东西要接收，返回响应
            if len(select.select([self.socket], [], [], 0)[0]) == 0:
                return in_data

    def command(self, command):
        result = self.send(2, command)
        time.sleep(0.003)
        return result


def main(host, port, password):  # 连接服务器
    rcon = MCRcon()
    rcon.connect(host, port, password)
    response = rcon.command('list')
    return response


def get_config():  # 加载配置文件
    if not os.path.exists(configPath):  # 若文件不存在则写入默认值
        with open(configPath, 'w+', encoding='UTF-8') as f:
            f.write(defultConfig)
    with open('config/online.json', 'r', encoding='UTF-8') as f:
        config = json.load(f, encoding='UTF-8')
    return config


def get_number():  # 获取服务器数量
    config = get_config()
    number = 1
    try:
        while config[str(number + 1)]:
            number += 1
    except:
        pass
    return number


def get_server_rtext(name):
    config = get_config()
    if config['click_event']:
        return RText(name, color=RColor.aqua).c(RAction.run_command, f"/server {name}")
    else:
        return RText(name, color=RColor.aqua)


def get_list():  # 获得玩家列表
    times = 0
    list = ''
    config = get_config()
    number = get_number()
    while times < number:
        server = config[str(times + 1)]
        name = server['name']
        host = server['host']
        port = int(server['port'])
        password = server['password']
        try:
            result = main(host, port, password)
            if result[10] != '0':
                player_list = result[int(result.find(':')) + 1:]
                player_number = result.count(',') + 1
            else:
                player_list = ''
                player_number = 0
            list += RTextList(
                get_server_rtext(name),
                RText(" 在线人数:", color=RColor.gray),
                RText(str(player_number), color=RColor.green)
            )
            if player_number != 0:
                list += RTextList(
                    RText(" 在线列表:", color=RColor.gray),
                    RText(player_list, RColor.gold)
                )
            list += "\n"
        except:
            list += RTextList(
                RText(name, color=RColor.aqua),
                RText(" 未开启\n", color=RColor.red)
            )
        times += 1
    return list


def on_info(server, info):  # 指令显示
    if info.content == '!!online':
        server.say(get_list())


def on_player_joined(server, player, info):  # 进服提示
    config = get_config()
    if config['join']:
        server.tell(player, get_list())


def on_load(server, old):  # 添加帮助
    server.register_help_message('!!online', '查询在线列表/人数')
