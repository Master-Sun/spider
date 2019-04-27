import requests, re, time, sys
from Crypto.Cipher import AES

url = 'http://videotts.it211.com.cn/aid18100325pm/aid18100325pm.m3u8'
# url = 'http://videotts.it211.com.cn/aid18100315am/aid18100315am-6.ts'

headers = {
    'Origin': 'http://tts.tmooc.cn',
    'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=646590&version=AIDTN201809',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

res = requests.get(url=url,headers=headers)
res.encoding = 'utf-8'
html = res.text
# http://videotts.it211.com.cn/aid18100315am/aid18100315am-1.ts
p = re.compile(r'http://.*?\.ts')
rList = p.findall(html)
p_key = re.compile(r'http://.*?\.key')
key_url = p_key.findall(html)[0]

key_res = requests.get(url=key_url,headers=headers)
key = key_res.content

count = 0
for link in rList:
    res = requests.get(url=link,headers=headers)
    cryptor = AES.new(key, AES.MODE_CBC, key)
    filename = '%03d'%count + '.mp4'
    with open(filename,'ab') as f:
        f.write(cryptor.decrypt(res.content))
    count += 1
    time.sleep(0.2)


    
