from datetime import datetime, timedelta

dept = "16:50"
arr = "18:00"

dur = datetime.strptime(arr, '%H:%M') - datetime.strptime(dept, '%H:%M')

print(type(datetime.strptime(arr, '%H:%M')))
print(type(dur))
print(dur)
print(type(str(dur)))

dur = datetime.strptime(str(dur), '%H:%M:%S')
dur = datetime.strftime(dur, '%H:%M:%S')
(h, m, s) = dur.split(':')
result = int(h) * 3600 + int(m) * 60 + int(s)

print(dur)
print(round(result/3600, 2))

dt1 = datetime.strptime('2022-12-28', '%Y-%m-%d')
dt2 = datetime.now()
intv = dt1 - dt2

print(dt1)
print(dt2)
print(intv.days)
print(type(int(intv.days)))
# print(type(datetime.strptime(dur, '%H:%M:%S')))
# print(timedelta(dur, '%H:%M:%S'))