import sys
import time
import datetime

with open('time.md', 'r+b') as f:
	data = f.readline()
	data = data.replace('\n', '')
	data = time.mktime(datetime.datetime.strptime(data, "%d/%m/%Y %H:%M:%S").timetuple())
	data += 300
	f.seek(0)
	f.write(datetime.datetime.fromtimestamp(int(data)).strftime('%d/%m/%Y %H:%M:%S'))
	f.truncate()
	f.close()