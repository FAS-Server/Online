# Online
一个可以查看多个服务器在线人数的 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 插件

***
## 简介
借助MC服务器原版的rcon功能, 发送list指令, 获得玩家列表

![image](./pictures/1.png)

***
## 使用方法

1. 安装前置 [multi_rcon_api](https://github.com/FAS-Server/MultiRconAPI) 并配置

2. 安装本插件

3. 启动 MCDReforged, 插件会在 `config/online/` 目录下自动生成配置文件, 名为 `config.json` 其内容如下:
```json
{
    "join": true,
    "click_event": true
}
```
其中,

- `join`为是否开启进服提示, `true` 为开启, `false` 为关闭

- `click_event` 为是否启用点击服务器名切换服务器的点击事件

- 如果`click_event` 设置为true，请确保 `multi_rcon_api` 中服务器名保持与跨服配置相同的服务器名，即 `/server` 指令后的对应名称

4. 最后,使用 `!!MCDR r all` 重载你的MCDR插件,或重启服务器,重新加入服务器即可看到服务器在线人数(如果 `join` 为 `true` 的话),也可以通过 `!!online` 指令来查看效果

