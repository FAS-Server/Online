# Online

![MCDReforged](https://img.shields.io/badge/dynamic/json?label=MCDReforged&query=dependencies.mcdreforged&url=https%3A%2F%2Fraw.githubusercontent.com%2FFAS-Server%2FOnline%2Fmaster%2Fmcdreforged.plugin.json&style=plastic) ![license](https://img.shields.io/github/license/FAS-Server/Online?style=plastic) ![build status](https://img.shields.io/github/workflow/status/FAS-Server/Online/CI%20for%20MCDR%20Plugin?label=build&style=plastic) ![Release](https://img.shields.io/github/v/release/FAS-Server/Online?style=plastic) ![total download](https://img.shields.io/github/downloads/FAS-Server/Online/total?label=total%20download&style=plastic)

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
