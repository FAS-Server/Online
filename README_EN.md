# Online

[简体中文](./README.md) | **English**

An [MCDReforged](https://github.com/Fallen-Breath/MCDReforged) plugin which can easily query the online players

***
## Introduction

Send `list` command to other sub-server through rcon, then parse the online players and display it, that's all!

![image](./pictures/1.png)

***
## Usage

1. Add the dependency [multi_rcon_api](https://github.com/FAS-Server/MultiRconAPI) and add your config!

2.Add this plugin

3. Launch the MCDReforged, the config file will automatically generated in `config/online/config.json` with the default value as following:
```json
{
    "join": true,
    "click_event": true
}
```

- `join` whether show the online list after player join

- `click_event` whether to add click event for switch between sub-servers by click the server name

- If `click_event` is set to true，please make sure the server name in `multi_rcon_api` is as the same with your server proxy (just the name after `/server` command)

4. Finally, use `!!MCDR r all` to reload, or restart your server to make it works
