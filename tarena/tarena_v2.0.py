import requests, re, time, sys, os
from Crypto.Cipher import AES

# 待优化：分两次匹配了视频和key的url

class Tarena_spider(object):
    def __init__(self):
        # 根据爬取需求进行修改
        self.course_no = 'aid18100401'
        self.menuId = '646585'
        self.version = 'AIDTN201809'

        self.url_am = 'http://videotts.it211.com.cn/' + self.course_no + 'am/' + self.course_no + 'am.m3u8'
        self.url_pm = 'http://videotts.it211.com.cn/' + self.course_no + 'pm/' + self.course_no + 'pm.m3u8'
        self.urls = [self.url_am, self.url_pm]
        self.headers = {
            'Origin': 'http://tts.tmooc.cn',
            # 'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=646590&version=AIDTN201809',
            'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=' + self.menuId + '&version=' + self.version,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                }
        self.root = os.getcwd()
        self.download_path = self.root + '/cache'

    # 获取视频的url和key
    def run(self):
        for index,url in enumerate(self.urls):
            res = requests.get(url=url,headers=self.headers)
            res.encoding = 'utf-8'
            html = res.text
            # 匹配ts文件地址
            p_url = re.compile(r'http://.*?\.ts')
            ts_list = p_url.findall(html)
            # 匹配密钥
            p_key = re.compile(r'http://.*?\.key')
            key_url = p_key.findall(html)[0]
            key_res = requests.get(url=key_url,headers=self.headers)
            # 返回二进制对象
            key = key_res.content
            self.download(key,ts_list,index)


    # 下载url并解密
    def download(self,key,ts_list,index):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        # 循环下载ts链接
        count = 0
        cryptor = AES.new(key, AES.MODE_CBC, key)
        for link in ts_list:
            res = requests.get(url=link,headers=self.headers)
            filename = self.download_path + '/' + '%03d'%count + '.mp4'
            with open(filename,'wb') as f:
                try:
                    f.write(cryptor.decrypt(res.content))
                except:
                    pass
            count += 1
            print('已爬完第%d个视频'%count)
            time.sleep(0.3)
        self.merge_file(index)

    # 合成视频文件
    def merge_file(self,index):
        os.chdir(self.download_path)
        cmd = "copy /b * new.tmp"
        os.system(cmd)
        os.system('del *.mp4')
        if index == 0:
            os.rename("new.tmp", self.root + "/" + self.course_no + "am.mp4")
        else:
            os.rename("new.tmp", self.root + "/" + self.course_no + "pm.mp4")
        
        os.chdir(self.root)

if __name__ == '__main__':
    spider = Tarena_spider()
    spider.run()
    