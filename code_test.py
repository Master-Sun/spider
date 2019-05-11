#coding:utf-8
import requests
from contextlib import closing
 
#文件下载器
def Down_load(file_url,file_path):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    # with closing(requests.get(file_url,headers=headers,stream=True,auth=('tarenacode','code_2014'))) as response:
    response = requests.get(file_url,headers=headers,stream=True,auth=('tarenacode','code_2014'))
    chunk_size = 2048  # 单次请求最大值
    content_size = int(response.headers['content-length'])  # 内容体总大小
    print(response.headers)
    print("content_size=", content_size)
    data_count = 0
    with open(file_path, "wb") as file:
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            data_count = data_count + len(data)
            now_jd = (data_count / content_size) * 100
            print("\r 文件下载进度：%d%%(%d/%d) - %s" % (now_jd, data_count, content_size, file_path), end=" ")
 
 
if __name__ == '__main__':
    file_url = 'http://code.tarena.com.cn/BIGCode/big1811/JT_easymall/day06AM.zip' #文件链接
    file_path = "C:\\Users\\77962\\Desktop\\tarena_code\\big1811\\JT_easymall\\test.zip"   #文件路径
    Down_load(file_url,file_path)