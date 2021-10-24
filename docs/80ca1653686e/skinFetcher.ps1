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