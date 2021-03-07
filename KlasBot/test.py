from datetime import datetime

print(datetime.now())

datetime_time = '2021-11-16 00:00:00'
datetime_obj = datetime.strptime(datetime_time, "%Y-%m-%d %H:%M:%S")
if datetime.now()< datetime_obj:
    print('not yey')
else:
    print('passed')