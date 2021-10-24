---
title: recorderBot 使用说明
toc: true
date: 2021-07-26 21:59:41
categories: Minecraft
tags:
    - Minecraft
    - Python
---

**此为版本草图, 插件仍处于预开发周期.**  
你可以在[此处](https://github.com/XavierWah/recorderBot)找到项目的 Github 仓库.

# 简介

recorderBot 是由 XavierWah 开发用于 MCDReforged 的插件. 此插件基于 carpet 的 `/player` 命令进行拓展, 加入了记录信息, 查询历史记录等功能, 辅助玩家在服务器中更好的使用 Bot 协作.  
此使用说明适用于 `recorderBot v1.0-alpha` .

<!-- more -->

# 安装

请将 recorderBot 主体以及其 API 目录放入任一 MCDReforged 插件目录中 ( 默认为 `/plugins` ) , 并启动 MCDReforged , 等待插件向 `/recorderBot` 中写入日志文件等信息, 本插件运行中储存的任何数据都将保存在此目录中.

# 指令大纲

- **`!!bot`** 插件总指令, 调出帮助菜单.
- **`!!bot create`** [参数] 生成 Bot .
- **`!!bot info`** < Bot 识别号> 查询 Bot 的信息.
- **`!!bot list`** [页码] 查看服务器内的 Bot .
- **`!!bot modify`** < Bot 识别号> <修改项> [修改值] 修改 Bot 的属性.
- **`!!bot remove`** < Bot 识别号> 删除 Bot .  

**其中<>表示必须项, [ ]表示可选项. 下同.**

# Bot 识别号

Bot 识别号用于分辨不同的 Bot , 在本插件的使用过程中十分重要. 每个 Bot 识别号指代唯一的 Bot , 但多个 Bot 识别号可用于指代同一个 Bot . Bot 识别号使用以下方法生成:

- **名称** 直接使用 Bot 的游戏名. 此处是否加入 *Bot_* 前缀均可识别.
- **序号** 使用 Bot 生成时的唯一序号.

# `!!bot create` 详解

`!!bot create` 用于生成 Bot . 其后可选的参数用来指定其坐标, 注释, 名称, 占用时长等属性. 若使用 `/player spawn` 生成 Bot , 其属性同样将被记录至此插件. `!!bot create` 可接受参数, 使 Bot 在生成时即拥有某些属性. 参数应逐个追加在命令后, 错误的格式有可能导致插件解析错误, 以下是可选参数:

- **`-autoleave 或 -a`** 设置 Bot 到时后自动退出，此项无需参数. 必须与 `-time` 共同使用.
- **`-coordinate 或 -c` <X坐标> <Y坐标> <Z坐标>** 指定 Bot 坐标, 必须为整数. 默认为创建Bot时的坐标.
- **`-description 或 -d` <注释内容>** 注释 Bot , 可用于记录Bot的作用等, 为字符串, 多个空格将会被缩减为单个. 默认为创建Bot时的坐标.
- **`-name 或 -n` <名称>** 指定 Bot 名称, 必须为字母、数字或下划线. 默认为其创建时的时间.
- **`-time 或 -t` <时间>** 指定占用 Bot 的时长, 为一连续字符串(不可包含空格). 此占用时长仅作为显示, 提示他人何时合适将Bot删除, 并不阻挡玩家删除Bot. 默认为随时可以删除. 下列形式可表述此处的时长：
  - **时长** 例如 `10m` 表示 10 分钟内一直有用处, `1d12h` 表示 1 天 12 小时内一直有用处, `1d` 表示一天内一直有用处等. 支持 `m` (分钟), `h` (小时), `d` (天)等单位, 不同时间单位可以混用. 当时长结束时, 将自动改为 `instant` .
  - **特殊** 仅有 `eternity` (或 `e` , 永远不要删除)与 `instant` (或 `i` , 随时可以删除)这 2 种候选. 如果你不清楚具体需要使用多久Bot, 那么推荐选用此种表述.

# `!!bot modify` 详解

`!!bot modify` 用于修改 Bot 的属性, 可以在不重新生成 Bot 的基础上修改如注释, 名称, 使用玩家, 占用时长等属性. 修改项代表将要修改的属性名, 不同的属性名对应不同格式的修改值, 以下是可选修改项:

- **`autoleave 或 a`** 设置 Bot 到时后是否自动退出, 修改值为 `true` 或 `false` .
- **`description 或 d`** 修改 Bot 的注释, 修改值为字符串.
- **`name 或 n`** 修改 Bot 的名称, 修改值为字母、数字或下划线. 修改此项时, Bot 将重新进入游戏.
- **`takeover`** 修改使用 Bot 的玩家, 此项无需填入修改值, 自动修改为输入指令的玩家.
- **`time 或 t`** 修改占用 Bot 的时长, 请参照`!!bot create -t`部分填入内容. 在字符串前添加单个字符`+`表示在原有时间上延长对应时间, 添加单个字符`-`表示在原有时长上缩短对应时间.

# v2 的坑先挖起来

- 增加 `!!bot history` 语法, 支持查看曾经的 Bot .
- 增加 `!!bot create -resume` 语法, 支持恢复曾经的 Bot .

# v3 的坑先挖起来

- 增加 `!!bot preset`, `!!bot create preset` 语法, 支持自定义 Bot 模板.
- 增加 `!!bot schedule` 语法, 支持自定义 Bot 工作周期.
