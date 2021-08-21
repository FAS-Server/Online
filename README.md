# Online
一个可以查看多个服务器在线人数的[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)插件

***
## 简介
借助MC服务器原版的rcon功能,发送list指令,获得玩家列表

![image](./pictures/1.png)

***
## 使用方法
下载Online.py,放入MCDReforged根目录下的plugins文件夹里,开启服务器的rcon功能。以原版服务器为示例,进入服务端根目录下,打开`server.properties`文件,找到`enable-rcon`,改为true,找到`rcon.password`,修改为你的密码,找到`rcon.port`,修改为你的端口  
修改完成后的这三项示例:
```
enable-rcon=true
rcon.password=passwd
rcon.port=25575
```
启动MCDReforged,插件会在`config`目录下自动生成配置文件,其名为`online.json`其内容如下:
```json
{
    "join": true,
    "servers":{
        "ServerA":{
            "host": "127.0.0.1",
            "port": 25575,
            "password": "ServerAPassword"
        }
    }
}
```
其中,  
 `"join"`为是否开启进服提示,true为开启,false为关闭

 `"click_event"`为是否启用点击服务器名切换服务器的点击事件

   `"ServerA"`为服务器名称, 如果`"click_event"`设置为true，请保持与跨服配置相同的服务器名，即`/server`指令后的对应名称

   `"host"`为服务器的IP,如:127.0.0.1

   `"port"`为你设置的服务器rcon端口,如:25575

   `"password"`为你设置的服务器rcon密码

多个服务器的`online.json`示例:
```json
{
    "join": true,
    "click_event": true,
    "servers": {
        "Survival":{
            "host": "127.0.0.1",
            "port": 25575,
            "password": "passwd"
        },
        "Mirror":{
            "host": "127.0.0.1",
            "port": 25595,
            "password": "passwd"
        },
        "Creative":{
            "host": "127.0.0.1",
            "port": 25555,
            "password": "passwd"
        },
        "Mods":{
            "host": "10.1.1.191",
            "port": 200001,
            "password": "passwd"
        }
    }
}
```
最后,使用`!!MCDR reload all`重载你的MCDR插件,或重启服务器,重新加入服务器即可看到服务器在线人数(如果`"join"`为true的话),也可以通过`!!online`指令来查看效果

