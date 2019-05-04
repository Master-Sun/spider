import requests, re, time, sys, os
from Crypto.Cipher import AES

# 待优化：分两次匹配了视频和key的url
# 效率太低，如何启用多线程或多进程呢？？？

class Tarena_spider(object):
    def __init__(self):
        # 根据爬取需求进行修改
        # big18111130pm
        self.course_name = 'big'
        self.course_date = 18111206
        self.course_num = 18
        self.folder = os.getcwd() + '/java_basic'
        self.menuId = '632256'
        self.version = 'BIGTN201803'
        
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
        success_count = 0
        i = 0
        while success_count < self.course_num:
            print('开始爬取第%d天视频'%(success_count+1))
            self.course_date += i
            course_no = self.course_name + str(self.course_date)
            url_am = 'http://videotts.it211.com.cn/' + course_no + 'am/' + course_no + 'am.m3u8'
            url_pm = 'http://videotts.it211.com.cn/' + course_no + 'pm/' + course_no + 'pm.m3u8'
            urls = [url_am, url_pm]

            for index,url in enumerate(urls):
                res = requests.get(url=url,headers=self.headers,timeout=1)
                if res.status_code == 200:
                    self.handle(res,index,course_no)
                elif res.status_code == 404:
                    print('404了')
                    i = 1
                    break
                else:
                    print('艾玛呀出错了,status_code:',res.status_code)
                    i = 1
                    break
            else:
                success_count += 1
                i = 1
                print('第%d天视频爬取完成'%success_count)
                time.sleep(5)
        print('爬取结束')


    def handle(self,res,index,course_no):
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
        self.merge_file(index,course_no)


    # 下载url并解密
    def download(self,key,ts_list,index):
        if not os.path.exists(self.download_path):
            os.mkdir(self.download_path)

        # 循环下载ts链接
        count = 0
        cryptor = AES.new(key, AES.MODE_CBC, key)
        err_count = 0
        for link in ts_list:
            res = requests.get(url=link,headers=self.headers)
            filename = self.download_path + '/' + '%03d'%count + '.mp4'
            with open(filename,'wb') as f:
                try:
                    f.write(cryptor.decrypt(res.content))
                except:
                    print('-----------第%d个视频解密出错'%count)
                    err_count += 1
            count += 1
            print('已爬完第%d个视频'%count)
            time.sleep(0.4)
        print('***************解密出错次数:%d'%err_count)
        

    # 合成视频文件
    def merge_file(self,index,course_no):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        os.chdir(self.download_path)
        cmd = "copy /b * new.tmp"
        os.system(cmd)
        os.system('del *.mp4')
        if index == 0:
            os.rename("new.tmp", self.folder + '/' + course_no + "am.mp4")
        else:
            os.rename("new.tmp", self.folder + '/' + course_no + "pm.mp4")
        os.chdir(self.root)


if __name__ == '__main__':
    spider = Tarena_spider()
    spider.run()
    
