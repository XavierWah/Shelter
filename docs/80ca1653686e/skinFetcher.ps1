$username = Read-Host '����Ҫ��ȡƤ�����ID'

# ��ȡ�û� UUID
$apiWeb = ( Invoke-WebRequest -Uri ( 'https://api.mojang.com/users/profiles/minecraft/' + $username ) ).Content
$useruuid = ( $apiWeb | ConvertFrom-Json ).id

# ��ȡ�û���Ϣ��Ӧ Base64
$sessionWeb = ( Invoke-WebRequest -Uri ( 'https://sessionserver.mojang.com/session/minecraft/profile/' + $useruuid ) ).Content
$userbase = ( $sessionWeb | ConvertFrom-Json ).properties.value

# ���� Base64 �������û�Ƥ��
$userskin = ( ( [Text.Encoding]::ASCII.GetString([Convert]::FromBase64String($userbase)) ) | ConvertFrom-Json ).textures.SKIN.url
Invoke-WebRequest $userskin -OutFile ( ($pwd).Path + '\' + $username + '.png' )

Read-Host '�ѱ�����ͬ��Ŀ¼�£����س����˳���'