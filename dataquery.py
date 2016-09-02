import MySQLdb

ONE_DAY       = 86400        # Total number of seconds in a day.
ONE_WEEK      = ONE_DAY * 7  # Total number of seconds in a week.
FIVE_MINS_DAY = 288          # Total number of five minute intervals in a day.
FIVE_MINS_WEEK = 2016        # Total number of five minute intervals in a week.
FIVE_MINS_MONTH = 2016 * 4   # Total number of five minute intervals in a month.

"""
This class holds all of the queries to extract
the network flow data from the database.
"""
class DataQuery(object):
	def __init__(self, cursor):
		"""
		Set the database cursor.
		"""
		self.cursor = cursor

	def GetDataRange(self, id, start, finish):
		"""
		Helper function to easily fetch specific
		time range network flow data.
		"""
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks,
		iflows, oflows, time_unix from rrd_n where nid='%s' and time_unix>='%s'
		and time_unix<='%s' order by time_unix""" % (id, start, finish))
		return self.cursor.fetchall()

	def EveryFiveMinutesForDay(self, c, id, now):
		"""
		Fetches the network flow data for every
		five minute interval in a day.
		"""
		instant = now
		qrange = "%s" % instant
		i = 0
		while i <= FIVE_MINS_DAY:
			instant = instant - 300
			qrange = "%s, %s" % (instant, qrange)
			i+=1
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
		oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
		time_unix""" % (id, qrange))
		return self.cursor.fetchall()

	def EveryFiveMinutesForWeek(self, c, id, now):
		"""
		Fetches the network flow data for every
		five minute interval in a week.
		"""
		instant = now
		qrange = "%s" % instant
		i = 0
		while i <= FIVE_MINS_WEEK:
			instant = instant - 300
			qrange = "%s,%s" % (instant, qrange)
			i+=1
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
		oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
		time_unix""" % (id, qrange))
		return self.cursor.fetchall()

	def EveryFiveMinutesForMonth(self, c, id, now):
		"""
		Fetches the network flow data for every
		five minute interval in a month.
		"""
		instant = now
		qrange = "%s" % instant
		i = 0
		while i <= FIVE_MINS_MONTH:
			instant = instant - 300
			qrange = "%s, %s" % (instant, qrange)
			i+=1
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
		oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
		time_unix""" % (id, qrange))
		return self.cursor.fetchall()

	def GetSameTimeDays(self, c, id, now, days):
		"""
		Fetches network flow data for the same hour,
		every day, for N days. For example, 10:00am
		on Tuesday, Monday, Sunday, etc.
		"""
		instant = now
		qrange = "%s" % instant
		i = 0
		while i < days:
			instant = instant - ONE_DAY
			qrange = "%s, %s" % (instant, qrange)
			i+=1
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
		oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
		time_unix""" % (id, qrange))
		return self.cursor.fetchall()

	def GetSameTimeWeeks(self, c, id, now, weeks):
		"""
		Fetches network flow data for the same time / day
		every week for N weeks. For example, every Tuesday
		at 10:00am.
		"""
		instant = now
		qrange = "%s" % instant
		i = 0
		while i < weeks:
			instant = instant - ONE_WEEK
			qrange = "%s, %s" % (instant, qrange)
			i+=1
		self.cursor.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
		oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
		time_unix""" % (id, qrange))
		return self.cursor.fetchall()

	def getIDs(self, c):
		"""
		Fetches the IDs for all of the campuses and
		institutions being monitored.
		"""
		self.cursor.execute("select n_id from NETWORK order by n_id")
		return self.cursor.fetchall()

	def queryJSON(self):
		"""
		Generates a JSON dictionary with all of the query
		functions, which allows for easy calls and manipulation.
		"""
		return {
		'fiveMinsDay': self.EveryFiveMinutesForDay, 
		'fiveMinsWeek': self.EveryFiveMinutesForWeek, 
		'fiveMinsMonth': self.EveryFiveMinutesForMonth,
		'sameTimeEveryDay': self.GetSameTimeDays,
		'sameTimeEveryWeek': self.GetSameTimeWeeks 
		}