# 猫眼电影：字头反扒

import requests, re, sys
from bs4 import BeautifulSoup
import base64
from fontTools.ttLib import TTFont 

# font_face = 'd09GRgABAAAAAAgcAAsAAAAAC7gAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAABHU1VCAAABCAAAADMAAABCsP6z7U9TLzIAAAE8AAAARAAAAFZW7lelY21hcAAAAYAAAAC4AAACTEa50bhnbHlmAAACOAAAA5EAAAQ0l9+jTWhlYWQAAAXMAAAALwAAADYVQybGaGhlYQAABfwAAAAcAAAAJAeKAzlobXR4AAAGGAAAABIAAAAwGhwAAGxvY2EAAAYsAAAAGgAAABoGpAWCbWF4cAAABkgAAAAfAAAAIAEZADxuYW1lAAAGaAAAAVcAAAKFkAhoC3Bvc3QAAAfAAAAAWwAAAI/gSeONeJxjYGRgYOBikGPQYWB0cfMJYeBgYGGAAJAMY05meiJQDMoDyrGAaQ4gZoOIAgCKIwNPAHicY2Bk0mWcwMDKwMHUyXSGgYGhH0IzvmYwYuRgYGBiYGVmwAoC0lxTGBwYKn7oMev812GIYdZhuAIUZgTJAQDa0gs4eJzFkjEOgzAMRX8KpRQ6dIOVGcTEvRAbK0tP0JN06nHYAgMRG2z0B7NUgrV19CLZSWzLPwDOABySERdQbyhYezGq1riDYI27eNCPcWfER91GuuqaPhlSk5liLCc958vCG8cne6aYcW/ZE4c1A4TwcGGfV5xYF8o7yPQDU/8r/W23dX9uXkjqDbbYRoLVVVeC1bZrBKtnnwj27ZAKnDNMJnDiMIVg/8hYClQBkxaoB+ZcgP8BA049WHicPVNNb9pmHH8eU9kpoYQUGxfSAsbENiYJjt8I4ACFQJtXRgKEkJaGqKU0W9ssarq0jbaWvUjttA/QXirtsEu1Q++dNK2nrVWbwz7ApF13W6VeIrLHQOaD5ecv/f17fQAE4OgfIAMSYABEFYr0kgJAjzn/Fx5h70EYzb1QkXWV59gAEaVlXVPRF07welRXZNoLSZzwQorE2QDHt4cu6MkyHzI8Qas9tpbSlRlr1RGLl+LypCZPpi48bl3ZP/n7fKayzwvWRZiYllLJzFAtMuk5U92Ydw1dyl/+ertmckCMjj5gAHFgQaTPIgmjSTgNVR4nTDhNRQxMbDtkAzzHwy4ziqRdsv79oCGJCd6OE9AdGYuu3f9qc2bXSNwtlFXdClvLU4lKSLxX+NnQRpOaRx8ZOIGLHs/DrZvfzv/QfvJjeSJShomFtfpSPhRe7XuCXkfYa+AEwKkxlN1C4ASLKOmIVDQCD9jsjOJ0D6zDYYcv4U0z2K1yLti49yBd+1RsGnu3Y5e4Y13wEOkigQ/9SUXbyEcX7UIeEj0lURIpcPBcgMBFt6e1tJM463DY7CPXCteNfK14f0UUHgTHYaM9t1RaF9PGzVSTX1qZq755eWcXbiTiSuYYp4Nw/GAMMee6AZoIlAno6rmGPOzG6KIh2c0ZpRvA4TMbFVRFv0jbTvnXldX9+NXMrScL2c/LumbrPOVznF4s3C1hLpUepX2xcyv65ES7mb0z/fzVQX1Zmih13oyVw7XF2dVK37ddxMMGAMMO2yGhdR1T4G7V3xJmp0aEwRgmeQ1HOSC7JbrnEdo5xN4CKziFtjRGg8qwQrEUP2yB2c4fMH+x0aj+9aIIDzpS8cUhmv2CViz/d8b0dhy5a3bE1NqrKLIWnZG7ihzVTaEWEvmOVPdOLz/bfrWzlcm1/zyfzksZVWKZbPP82cBoIORXqFDpyyL8Rtj65MbthZbgupK5vJ80Gvn6T2rK76tn053HfI50UiT/cLnYv0MfsBPYb2bK/TvUuzhOhmKIfgZmj1Fzv7PO6ulqJRvOkis5eLXzN++fYeuPYrkvNqeTA69zmc2nFc5nhdulX130o+sbF1f1qdpxJz8ivUEARikGdcliWnuMlIRyv1UEaiv82OEHrSNCjIsXqNC8kVqAtZN77/aYMJmVBJk+PVAq+bzuSETzS3Pnpq7NzuWtzRs75fFFmU4JzPgZGmXxH/3i4MIAAAB4nGNgZGBgAGJjN8GJ8fw2Xxm4WRhA4Kbgx3YE/f8NCwPTeSCXg4EJJAoAEFQKWgB4nGNgZGBg1vmvwxDDwgACQJKRARXwAAAzYgHNeJxjYQCCFAYGJh3iMAA3jAI1AAAAAAAAAAwATgCWALoA7gEyAUwBaAGuAeACGgAAeJxjYGRgYOBhMGBgZgABJiDmAkIGhv9gPgMADoMBVgB4nGWRu27CQBRExzzyAClCiZQmirRN0hDMQ6lQOiQoI1HQG7MGI7+0XpBIlw/Id+UT0qXLJ6TPYK4bxyvvnjszd30lA7jGNxycnnu+J3ZwwerENZzjQbhO/Um4QX4WbqKNF+Ez6jPhFrp4FW7jBm+8wWlcshrjQ9hBB5/CNVzhS7hO/Ue4Qf4VbuLWaQqfoePcCbewcLrCbTw67y2lJkZ7Vq/U8qCCNLE93zMm1IZO6KfJUZrr9S7yTFmW50KbPEwTNXQHpTTTiTblbfl+PbI2UIFJYzWlq6MoVZlJt9q37sbabNzvB6K7fhpzPMU1gYGGB8t9xXqJA/cAKRJqPfj0DFdI30hPSPXol6k5vTV2iIps1a3Wi+KmnPqxVhjCxeBfasZUUiSrs+XY82sjqpbp46yGPTFpKr2ak0RkhazwtlR86i42RVfGn93nCip5t5gh/gPYnXLBAHicbco7DoAgEATQHfygiHcBNIKtCnexsTPx+Mbd1mleZjKkSGLoPxYKFWo0aKHRoYfBAIuR8Oj7OkvM8TM7L8bo2TzN7BE26WHnfwqZdUvhPSX5r8ETvRyNF4sA'
# font2.saveXML('002.xml')    #将ttf文件转化成xml格式并保存到本地，方便查看内部数据结构

def get_font_dict(font_face):
    '''
    返回字符编码对应的数字
    '''
    # 对页面上的font_face进行解码并保存字体文件
    font_code = base64.b64decode(font_face)
    with open('002.ttf','wb')as f:
        f.write(font_code)

    # 打开字体文件,001.ttf为基准比对文件,002.ttf为本次页面中的字体文件
    font1 = TTFont('001.ttf')    
    font2 = TTFont('002.ttf')    
    
    # 获取字体文件中uin编码的列表，去掉头尾
    # font1.getGlyphOrder() 也能获取，但顺序不一样
    uni_list_1 = font1.getGlyphNames()[1:-1]
    uni_list_2 = font2.getGlyphNames()[1:-1]

    # 手动匹配001.ttf中编码对应的数字
    font_dict_1 = { 'uniE035': 5, 'uniE285': 0, 'uniE8D4': 9, 'uniED7F': 7, 'uniF11E': 8, 
                    'uniF137': 2, 'uniF1BF': 4, 'uniF4EC': 1, 'uniF59C': 3, 'uniF750': 6 }

    # 用来存放本次页面中编码和数字的对照字典
    font_dict_2 = {}

    # 根据字体对象是否一致进行匹配
    for uni_code2 in uni_list_2:
        for uni_code1 in font_dict_1:
            if font2['glyf'][uni_code2] == font1['glyf'][uni_code1]:
                font_dict_2[uni_code2] = font_dict_1[uni_code1]

    return font_dict_2

# print(font['glyf'].__dict__)
# print(font['glyf']['uniF1BF'])
# {'tableTag': 'glyf', 
# 'glyphs': {
#     'glyph00000': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF390>, 
#     'x': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF3C8>, 
#     'uniF4EC': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF400>, 
#     'uniED7F': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF438>, 
#     'uniF1BF': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF470>, 
#     'uniF750': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF4A8>, 
#     'uniF11E': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF4E0>, 
#     'uniF137': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF518>, 
#     'uniE285': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF550>, 
#     'uniF59C': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF588>, 
#     'uniE035': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF5C0>, 
#     'uniE8D4': <fontTools.ttLib.tables._g_l_y_f.Glyph object at 0x000001FD99AFF5F8>}, 
#     'glyphOrder': ['glyph00000', 'x', 'uniF4EC', 'uniED7F', 'uniF1BF', 'uniF750', 'uniF11E', 'uniF137', 'uniE285', 'uniF59C', 'uniE035', 'uniE8D4']}


url = "https://piaofang.maoyan.com/?ver=normal"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(url, headers=headers)
html = res.text

rList = re.findall(r';base64,(.*)?\) ', html)
if len(rList) == 1:
    font_face = rList[0]
else:
    raise Exception('没匹配到')
    sys.exit()

font_dict = get_font_dict(font_face)


soup = BeautifulSoup(html, 'lxml')
rList = soup.find_all('ul', attrs={'class': 'canTouch'})

for r in rList:
    move_name = r.find('b').get_text()
    up_time = r.find('em').get_text()
    piaofang = r.find('i', attrs={'class': 'cs'}).get_text()
    result = re.findall(r'&#x(.{4});', piaofang)
    print(result)
    # print(html)
    sys.exit()

