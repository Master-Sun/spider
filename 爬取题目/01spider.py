import requests
import csv


url = "http://mnks.jxedt.com/get_question?r=0.7617952624528421&index=1"
img_url = "http://img.58cdn.com.cn/dist/jxedt/app/static/img/kaoshi_p/14069.jpg"


# # 单选
# http://mnks.jxedt.com/get_question?r=0.7617952624528421&index=1
# { "id": "1", "question": "驾驶机动车在道路上违反道路交通安全法的行为，属于什么行为？", "a": "违章行为", 
# "b": "违法行为", "c": "过失行为", "d": "违规行为", "ta": "2", "imageurl": "", "bestanswer": ""违反道路交通安全法"，
# 违反法律法规即为违法行为。官方已无违章/违规的说法。", "bestanswerid": "2600001", "Type": "2", "sinaimg": "" }
# # 带图单选
# http://mnks.jxedt.com/get_question?r=0.7100408020018876&index=7731
# { "id": "7731", "question": "如图所示，在这起交通事故中，以下说法正确的是什么？", "a": "A车负全部责任", 
# "b": "B车负全部责任", "c": "各负一半的责任", "d": "B车负主要责任", "ta": "1", "imageurl": "14069.webp", 
# "bestanswer": "这起交通事故主要是因为A车绕开障碍物时未提前观察减速为B车让行造成的，所以A车全责。", 
# "bestanswerid": "3086212520071528562", "Type": "2", "sinaimg": "14069.webp" }
# # 判断
# http://mnks.jxedt.com/get_question?r=0.6527851857841813&index=370
# { "id": "370", "question": "绿灯亮表示前方路口允许机动车通行。", "a": "", "b": "", "c": "", "d": "", "ta": "1", 
# "imageurl": "", "bestanswer": "《实施条例》第三十八条：机动车信号灯和非机动车信号灯表示：(一)绿灯亮时，
# 准许车辆通行，但转弯的车辆不得妨碍被放行的直行车辆、行人通行；(二)黄灯亮时，已越过停止线的车辆可以继续通行；(三)红灯亮时，
# 禁止车辆通行。在未设置非机动车信号灯和人行横道信号灯的路口，非机动车和行人应当按照机动车信号灯的表示通行。红灯亮时，
# 右转弯的车辆在不妨碍被放行的车辆、行人通行的情况下，可以通行。", "bestanswerid": "2600342", "Type": "1", "sinaimg": "" }

