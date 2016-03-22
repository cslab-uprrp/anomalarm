import MySQLdb

ONE_DAY       = 86400        # Total number of seconds in a day.
ONE_WEEK      = ONE_DAY * 7  # Total number of seconds in a week.
FIVE_MINS_DAY = 288          # Total number of five minute intervals in a day.
FIVE_MINS_WEEK = 2016        # Total number of five minute intervals in a week.
FIVE_MINS_MONTH = 2016 * 4   # Total number of five minute intervals in a month.

class DataQuery:
    def GetDataRange(self, c, id, start, finish):
        c.execute("""select ioctect, ooctect, ipacks, opacks,
        iflows, oflows, time_unix from rrd_n where nid='%s' and time_unix>='%s'
        and time_unix<='%s' order by time_unix""" % (id, start, finish))
        return c.fetchall()

    def EveryFiveMinutesForDay(self, c, id, now):
        instant = now
        qrange = "%s" % instant
        i = 0
        while i <= FIVE_MINS_DAY:
            instant = instant - 300
            qrange = "%s, %s" % (instant, qrange)
            i+=1
        c.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
        oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
        time_unix""" % (id, qrange))
        return c.fetchall()

    def EveryFiveMinutesForWeek(self, c, id, now):
        instant = now
        qrange = "%s" % instant
        i = 0
        while i <= FIVE_MINS_WEEK:
            instant = instant - 300
            qrange = "%s,%s" % (instant, qrange)
            i+=1
        c.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
        oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
        time_unix""" % (id, qrange))
        return c.fetchall()

    def EveryFiveMinutesForMonth(self, c, id, now):
        instant = now
        qrange = "%s" % instant
        i = 0
        while i <= FIVE_MINS_MONTH:
            instant = instant - 300
            qrange = "%s, %s" % (instant, qrange)
            i+=1
        c.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
        oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
        time_unix""" % (id, qrange))
        return c.fetchall()

    # To get the same time every day for 2 weeks.
    def GetSameTimeAFewDaysBack(self, c, id, now):
        instant = now
        qrange = "%s" % instant
        i = 0
        while i < 15:
            instant = instant - ONE_DAY
            qrange = "%s, %s" % (instant, qrange)
            i+=1
        c.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
        oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
        time_unix""" % (id, qrange))
        return c.fetchall()

    # To get the same time / day every week for 10 weeks.
    def GetSameTimeAFewWeeksBack(self, c, id, now):
        instant = now
        qrange = "%s" % instant
        i = 0
        while i < 10:
            instant = instant - ONE_WEEK
            qrange = "%s, %s" % (instant, qrange)
            i+=1
        c.execute("""select ioctect, ooctect, ipacks, opacks, iflows,
        oflows, time_unix from rrd_n where nid=%s and time_unix in (%s) order by
        time_unix""" % (id, qrange))
        return c.fetchall()

    def getIDs(self, c):
        # Fetch all of the IDs for the different Campuses
        c.execute("select n_id from NETWORK order by n_id")
        return c.fetchall()

    def queryJSON(self):
        return {
        'fiveMinsDay': self.EveryFiveMinutesForDay, 
        'fiveMinsWeek': self.EveryFiveMinutesForWeek, 
        'fiveMinsMonth': self.EveryFiveMinutesForMonth,
        'sameTimeEveryDay': self.GetSameTimeAFewDaysBack,
        'sameTimeEveryWeek': self.GetSameTimeAFewWeeksBack 
        }