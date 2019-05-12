import requests, re, time, sys, os
from Crypto.Cipher import AES
from multiprocessing import Queue
from threading import Thread
import datetime

# 待优化：分两次匹配了视频和key的url
# 如果遇到网站服务器异常，无法正常响应的，可写入日志中供后续处理时参考
# 线程有时会卡死，可能是服务器的问题，得记录爬取日志，不然后续没法分析解决


class Tarena_spider(object):
    def __init__(self):
        # 根据爬取需求进行修改
        self.course_name = 'wfd1811a'
        self.course_date = datetime.date(2019,3,5)
        self.course_num = 6
        self.menuId = '643814'
        self.version = 'WEBTN201805'
        self.headers = {
            'Origin': 'http://tts.tmooc.cn',
            # 'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=646590&version=AIDTN201809',
            'Referer': 'http://tts.tmooc.cn/video/showVideo?menuId=' + self.menuId + '&version=' + self.version,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                }

        self.root = os.getcwd()
        self.folder = self.root + '/VUEECOSYSTEM'
        self.down_list = Queue()
        self.tlist = []    # 存放线程的列表

    # 创建线程爬取url和下载
    def run(self):
        th1 = Thread(target=self.get_url)
        th1.start()
        self.tlist.append(th1)
        # 多线程下载
        for i in range(5):
            th = Thread(target=self.download,args=(i,))
            th.start()
            self.tlist.append(th)
        print('--------------所有线程创建完毕，等待回收...')
        for th in self.tlist:
            th.join()
        print('所有线程已回收，爬取结束!')


    def get_url(self):
        success_count = 0    # 记录url爬取次数，与course_num对应
        i = 0
        while success_count < self.course_num:
            print('开始爬取第%d天url'%(success_count+1))
            self.course_date += datetime.timedelta(days=i)
            course_no = self.course_name + self.course_date.strftime("%Y%m%d")[4:]
            url_am = 'http://videotts.it211.com.cn/' + course_no + 'am/' + course_no + 'am.m3u8'
            url_pm = 'http://videotts.it211.com.cn/' + course_no + 'pm/' + course_no + 'pm.m3u8'
            urls = [url_am, url_pm]

            for index,url in enumerate(urls):
                res = requests.get(url=url,headers=self.headers,timeout=1)
                if res.status_code == 200:
                    # 响应成功，转去处理页面信息，解析key和ts的链接
                    self.handle(res,index,course_no)
                # 若响应失败了，则可能无此url，跳出for循环进行下一次请求
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
                print('第%d天url爬取完成'%success_count)
                time.sleep(0.2)
        print('----------url爬取线程结束')


    # 解析页面，获取key和ts视频的链接
    def handle(self,res,index,course_no):
        res.encoding = 'utf-8'
        html = res.text
        # 匹配ts文件地址
        regex_url = re.compile(r'http://.*?\.ts')
        ts_list = regex_url.findall(html)
        # 匹配密钥
        regex_key = re.compile(r'http://.*?\.key')
        key_url = regex_key.findall(html)[0]
        key_res = requests.get(url=key_url,headers=self.headers)
        # 返回二进制对象
        key = key_res.content
        t = (key,ts_list,index,course_no)
        self.down_list.put(t)


    # 下载url并解密
    def download(self,i):
        while True:
            try:
                t = self.down_list.get(block=True,timeout=2)
            except:
                print('线程%d爬取结束'%(i+1))
                break
            key = t[0]
            ts_list = t[1]
            index = t[2]
            course_no = t[3]
            download_path = self.root + '\\cache' + str(i)
            if not os.path.exists(download_path):
                os.mkdir(download_path)

            # 循环下载ts链接
            count = 0
            cryptor = AES.new(key, AES.MODE_CBC, key)
            err_count = 0
            for link in ts_list:
                res = requests.get(url=link,headers=self.headers)
                filename = download_path + '\\' + '%03d'%count + '.mp4'
                with open(filename,'wb') as f:
                    try:
                        f.write(cryptor.decrypt(res.content))
                    except:
                        print('-----------第%d个视频解密出错'%count)
                        err_count += 1
                count += 1
                print('下载线程%d:已爬完第%d个视频'%(i,count))
                time.sleep(0.2)
            print('***************解密出错次数:%d'%err_count)
            self.merge_file(index,course_no,download_path)
        

    # 合成视频文件
    def merge_file(self,index,course_no,download_path):
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        src = download_path + '\\*.mp4'
        dst = download_path + '\\new.tmp'
        cmd = "copy /b " + src + ' ' + dst
        os.system(cmd)
        os.system('del ' + src)
        if index == 0:
            os.rename(dst, self.folder + '/' + course_no + "am.mp4")
        else:
            os.rename(dst, self.folder + '/' + course_no + "pm.mp4")


if __name__ == '__main__':
    spider = Tarena_spider()
    spider.run()
    
    
