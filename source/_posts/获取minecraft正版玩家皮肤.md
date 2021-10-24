---
title: 获取Minecraft正版玩家皮肤
date: 2021-07-26 19:18:02
toc: true
categories: Minecraft
tags:
  - Minecraft
  - Python
  - Powershell
---

# 引子

前段日子和朋友玩Hypixel的时候，朋友问我能不能把某个玩家的皮肤给下载下来私用。我当时使用了[NameMC](https://namemc.com)获取玩家皮肤，但后来用来获取玩家的UUID时，发现有些玩家没办法搜到。这也就催生了我去寻找远古方法，直接通过Mojang服务器获取玩家皮肤、UUID等信息的想法。

<!-- more -->

# 原理阐释

首先，我们通过Mojang提供的官方*API*（`api.mojang.com/users/profiles/minecraft/[ID]`）获取玩家的UUID。对应填入玩家ID，访问后就可以获取一段对应的JSON，格式大概如下：

``` JSON JSON
{"name":"XavierWah","id":"0be6e8232e5f4cb198320792b0da9188"}
```

很明显可以看出，这段信息中键`name`为玩家ID，键`id`为玩家UUID。玩家的UUID就到手后，我们可以通过*Session Server*（`sessionserver.mojang.com/session/minecraft/profile/[UUID]`）获取到玩家的材质信息，同样是一段JSON，格式大概如下：

``` JSON JSON
{
  "id" : "0be6e8232e5f4cb198320792b0da9188",
  "name" : "XavierWah",
  "properties" : [ {
    "name" : "textures",
    "value" : "ewogICJ0aW1lc3RhbXAiIDogMTYyNzI5Mjk3NDkwMCwKICAicHJvZmlsZUlkIiA6ICIwYmU2ZTgyMzJlNWY0Y2IxOTgzMjA3OTJiMGRhOTE4OCIsCiAgInByb2ZpbGVOYW1lIiA6ICJYYXZpZXJXYWgiLAogICJ0ZXh0dXJlcyIgOiB7CiAgICAiU0tJTiIgOiB7CiAgICAgICJ1cmwiIDogImh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvN2NiMzkxMTdhN2U4ZmYxYjE0M2VmMGU4YzRiMDg5MjA0ZTk3YTBlNmQwMGRjZjRlNjkxYWFmODlmNzhkOWQzMSIsCiAgICAgICJtZXRhZGF0YSIgOiB7CiAgICAgICAgIm1vZGVsIiA6ICJzbGltIgogICAgICB9CiAgICB9CiAgfQp9"
  } ]
}
```

这段里我们需要的信息，就是此处键`value`的值。这是一段经过Base64加密后的信息，解密后仍是一段JSON，格式大概如下：

``` JSON JSON
{
  "timestamp" : 1627294093042,
  "profileId" : "0be6e8232e5f4cb198320792b0da9188",
  "profileName" : "XavierWah",
  "textures" : {
    "SKIN" : {
      "url" : "http://textures.minecraft.net/texture/7cb39117a7e8ff1b143ef0e8c4b089204e97a0e6d00dcf4e691aaf89f78d9d31",
      "metadata" : {
        "model" : "slim"
      }
    }
  }
}
```

此处的`timestamp`为我们访问网站时的时间戳，`SKIN`中键`url`的值代表玩家皮肤的网址、键`model`的值代表玩家皮肤的种类（这个键不一定存在，但纤细一定是`slim`）。访问这个网址，就得到了玩家的皮肤。人工操作起来很复杂，需要辗转多次才能得到最终结果，并且中途还需要进行一次Base64解码，于是我便写了一个程序来帮助我获取玩家信息。

# 代码解剖

[<i class="fas fa-download"></i>](skinFetcher.py) `下载 skinFetcher.py` 下方的代码。

``` python Python 3
import requests
import base64
import json

username = input('输入要获取皮肤玩家ID：').split()[0]

# 获取用户 UUID
apiWeb = requests.get('https://api.mojang.com/users/profiles/minecraft/{}'.format(username)).content
useruuid = json.loads(apiWeb)['id']

# 获取用户信息对应 Base64
sessionWeb = requests.get('https://sessionserver.mojang.com/session/minecraft/profile/{}'.format(useruuid)).content
userbase = json.loads(sessionWeb)['properties'][0]['value'].encode('utf-8')

# 解码 Base64 并下载用户皮肤
userskin = json.loads(base64.b64decode(userbase))['textures']['SKIN']['url']
fetch = open('{}.png'.format(username), 'wb').write(requests.get(userskin).content)

input('已保存至同级目录下，按回车键退出。')
```

由于有些人没有装Python，所以我又用Powershell写了一个功能一样的。

[<i class="fas fa-download"></i>](skinFetcher.ps1) `下载 skinFetcher.ps1` 下方的代码。

``` powershell Powershell
$username = Read-Host '输入要获取皮肤玩家ID'

# 获取用户 UUID
$apiWeb = ( Invoke-WebRequest -Uri ( 'https://api.mojang.com/users/profiles/minecraft/' + $username ) ).Content
$useruuid = ( $apiWeb | ConvertFrom-Json ).id

# 获取用户信息对应 Base64
$sessionWeb = ( Invoke-WebRequest -Uri ( 'https://sessionserver.mojang.com/session/minecraft/profile/' + $useruuid ) ).Content
$userbase = ( $sessionWeb | ConvertFrom-Json ).properties.value

# 解码 Base64 并下载用户皮肤
$userskin = ( ( [Text.Encoding]::ASCII.GetString([Convert]::FromBase64String($userbase)) ) | ConvertFrom-Json ).textures.SKIN.url
Invoke-WebRequest $userskin -OutFile ( ($pwd).Path + '\' + $username + '.png' )

Read-Host '已保存至同级目录下，按回车键退出。'
```

以上代码的逻辑和我们人工操作是一个流程。运行程序之后，直接根据提示输入玩家ID即可，皮肤会自动下载到运行目录中。
