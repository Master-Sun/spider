import requests, time
from lxml import etree
from multiprocessing import Queue, Process
from threading import Thread
from contextlib import closing
from urllib.parse import unquote

# 待解决问题
# 文件下载不完整的问题(目前通过比较文件大小判断是否下载完整，可以支持断点续传吗？)
# 写日志记录源文件大小和下载后的文件大小
# closing的作用？

class Code_spider(object):
    def __init__(self):
        self.url = 'http://code.tarena.com.cn/BIGCode/big1811/javase/'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.folder = 'C:\\Users\\77962\\Desktop\\tarena_code/big1811/test/'
        # 创建消息队列，存放下载链接
        self.q = Queue()


    def work(self):
        self.get_link()
        # 开启多线程
        L = []
        for i in range(10):
            th = Thread(target=self.down_load, args=(i+1,))
            # th = Process(target=spider.down_load, args=(i+1,))
            th.start()
            L.append(th)

        for th in L:
            th.join()
        

    # 获取页面上的下载链接
    def get_link(self):
        res = requests.get(self.url,headers=self.headers,auth=('tarenacode','code_2014'))
        res.encoding = 'utf-8'
        html = res.text

        parseHtml = etree.HTML(html)
        r_list = parseHtml.xpath('//a/@href')[1:]

        for link in r_list:
            self.q.put(link)
        print("本次将下载",self.q.qsize(),"个文件")

    # 多线程循环执行的下载函数
    def down_load(self,n):
        while True:
            try:
                # 中文不能出现在链接地址中，因此会进行url编码，此处使用unquote进行解码
                filename = unquote(self.q.get(block=True,timeout=2))
            except:
                print('取不到链接了,%s号线程结束工作'%n)
                break
            link = self.url + filename
            # closing:可用于创建上下文管理器(保持下载连接?)
            # 设置stream=true时，并不会立即下载(但已获取响应头)
            # 会在使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。
            # 需要注意一点：文件没有下载之前，它也需要保持连接。
            with closing(requests.get(link,headers=self.headers,stream=True,auth=('tarenacode','code_2014'))) as response:
                chunk_size = 2048    # 设置单次请求大小
                total_size = int(response.headers['content-length'])  # 下载内容的总大小
                data_count = 0  # 已下载大小
                percent = 0    # 记录下载百分比
                with open(self.folder+filename,'wb') as fw:
                    # 循环下载并写入磁盘
                    for data in response.iter_content(chunk_size=chunk_size):
                        last_percent = percent
                        fw.write(data)
                        data_count += len(data)
                        percent = int((data_count/total_size)*100)
                        # 下载总进度有更新则打印
                        if percent > last_percent:
                            print("线程%s正在下载：%s：已完成%s%%(%s/%s)"%(n,filename,percent,data_count,total_size))
                # 判断文件是否下载完整
                if total_size == data_count:
                    print("下载完成，文件名：",filename," 总大小",total_size," 下载完成大小",data_count)
                else:
                    self.q.put(link)


if __name__ == '__main__':
    start_time = time.time()

    spider = Code_spider()
    spider.work()

    end_time = time.time()

    print("爬取总时间:",end_time-start_time)