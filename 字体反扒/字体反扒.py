import requests
from lxml import etree
from fontTools.ttLib import TTFont

url = "http://shaoq.com/font"
font_url = "http://shaoq.com/static/fonts/1e74211083b76836061e7e92514fa6ac.woff"

headers = {
    "User-Agent": "Mozilla/5.0"
}

font_name = "ea714a222f53ac8307399dd35c090357.woff"
font1 = TTFont(font_name)


obj_list2=font1.getGlyphNames()[1:-1]
uni_list2=font1.getGlyphOrder()[2:]
# print(obj_list2)
print(uni_list2)

# font1.saveXML('qidian.xml')

# mappings = {}
# for k, v in font1.getBestCmap().items():
#     if v.startswith('uni'):
#         mappings['&#x{:x}'.format(k)] = chr(int(v[3:], 16))
#     else:
#         mappings['&#x{:x}'.format(k)] = v

# print(mappings)





