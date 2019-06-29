<<<<<<< HEAD:tarena/tarena_v1.0.py
import requests, re, time, sys, os, shutil
from Crypto.Cipher import AES

url = 'http://videotts.it211.com.cn/aid18100313am/aid18100313am.m3u8'
# url = 'http://videotts.it211.com.cn/aid18100315am/aid18100315am-6.ts'
course_name = 'pandas_day09'
root = os.getcwd()

headers = {
    'Origin': 'http://tts.tmooc.cn',
    'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=646585&version=AIDTN201809',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

res = requests.get(url=url,headers=headers)
res.encoding = 'utf-8'
html = res.text
with open('xxx.html','w') as f:
    f.write(html)
# http://videotts.it211.com.cn/aid18100315pm/aid18100315pm-1.ts
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
    filename = root + '/cache/' + '%03d'%count + '.mp4'
    with open(filename,'ab') as f:
        try:
            f.write(cryptor.decrypt(res.content))
        except:
            pass
    count += 1
    print('已爬完第%d个视频'%count)
    time.sleep(0.3)


os.chdir(root + '/cache')
cmd = 'copy /b *.mp4 new.mp4'
os.system(cmd)
os.rename(root+'/cache/new.mp4',root+'/%s.mp4'%course_name)
cmd = 'del *.mp4'
os.system(cmd)













=======
import requests, re, time, sys, os, shutil
from Crypto.Cipher import AES

url = 'http://videotts.it211.com.cn/big18110427pm/big18110427pm.m3u8'
# url = 'http://videotts.it211.com.cn/aid18100315am/aid18100315am-6.ts'
course_name = 'big18110427pm'
root = os.getcwd()

headers = {
    'Origin': 'http://tts.tmooc.cn',
    'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=646585&version=AIDTN201809',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

res = requests.get(url=url,headers=headers)
res.encoding = 'utf-8'
html = res.text
with open('xxx.html','w') as f:
    f.write(html)
# http://videotts.it211.com.cn/aid18100315pm/aid18100315pm-1.ts
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
    filename = root + '/cache/' + '%03d'%count + '.mp4'
    with open(filename,'ab') as f:
        try:
            f.write(cryptor.decrypt(res.content))
        except:
            pass
    count += 1
    print('已爬完第%d个视频'%count)
    time.sleep(0.1)


os.chdir(root + '/cache')
cmd = 'copy /b *.mp4 new.mp4'
os.system(cmd)
os.rename(root+'/cache/new.mp4',root+'/%s.mp4'%course_name)
cmd = 'del *.mp4'
os.system(cmd)













>>>>>>> 487c4af1409965d7a91557a8a4a12f678e6ef0f7:tarena_v1.0.py
