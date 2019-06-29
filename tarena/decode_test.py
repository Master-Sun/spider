import datetime

# 自定义日期和时间
set_date = datetime.date(2018,1,31)   # 2018-01-25 
set_time = datetime.time(21,2,10)    # 21:02:10

# 组合日期和时间
set_datetime = datetime.datetime.combine(set_date,set_time)  # 2018-01-25 21:02:10

# 获取当前日期时间
now_time = datetime.datetime.now()    # 2019-05-11 22:05:50.652078

# 计算日期之间秒数差
total_diff = (set_datetime - now_time).total_seconds()   # 秒速总差值，结果有正负
diff = (set_datetime - now_time).seconds    # 仅获取时间部分的差值
diff2 = (now_time - set_datetime).seconds

# 日期加一天
target_date = set_date + datetime.timedelta(days=0)
print(target_date, set_date)
print(target_date.strftime('%Y%m%d'))