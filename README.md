# Online

**简体中文** | [English](./README_EN.md)

一个可以查看多个服务器在线人数的 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) 插件

***
## 简介

借助MC服务器原版的rcon功能, 发送list指令, 获得玩家列表

![image](./pictures/1.png)

***
## 使用方法

1. 安装前置 [multi_rcon_api](https://github.com/FAS-Server/MultiRconAPI) 并配置

2. 安装本插件

3. 启动 MCDReforged, 插件会自动生成名为 `config/online/config.json` 的配置文件, 其默认内容如下:
```json
{
    "join": true,
    "click_event": true
}
```

- `join`为是否开启进服提示, `true` 为开启, `false` 为关闭

- `click_event` 为是否启用点击服务器名切换服务器的点击事件

- 如果`click_event` 设置为 `true`, 请确保 `multi_rcon_api` 中服务器名保持与跨服配置相同的服务器名, 即 `/server` 指令后的对应名称

4. 最后,使用 `!!MCDR r all` 重载你的MCDR插件, 或重启服务器来让插件工作起来
