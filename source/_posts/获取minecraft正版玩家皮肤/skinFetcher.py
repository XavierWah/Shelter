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