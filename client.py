from graph import plotOriginalvsSmoothed
from dataquery import *
from anomalyAlgorithms import *
import time
import datetime
import sys
import json
import csv
import os
import traceback
import credentials

possibleIDs = [1, 2, 3, 4, 7, 10, 11, 12, 29]
keys = ['input octet', 'output octet', 'input packet', 'output packet']

def Usage():
    print "This script has a few ways to use it:\n"
    print """1) python %s <From: DD/MM/YEAR> <To: DD/MM/YEAR> <ID>""" % sys.argv[0]
    print """2) python %s <From: DD/MM/YEAR> <ID>""" % sys.argv[0]
    print """3) python %s <ID>\n""" % sys.argv[0]
    print "Possible IDs: 1 (RUM), 2(RCM), 3(RRP), 4(CAYEY), 7(FIU), 10(HPCf), 11(CUH), 12(PSM), 29(AO)\n"
    sys.exit()

class NetworkAnomaly:
    def handleAnomalies(self, data, smooth, query):
        length = len(data[keys[0]])

        # Generate the average JSON objects.
        average = aa.getAverage(data)
        smoothAverage = aa.getAverage(smooth)

        # Generate the standard deviation JSON objects.
        smoothStdDev = aa.smoothStdDev(data, smooth, 0.25)
        standardDev = aa.stdDev(data)

        regularfactor = 2
        smoothedfactor = 3
        countregular = 0
        countsmooth = 0

        if os.path.isfile("cron.csv") == True:
            f = csv.writer(open("cron.csv", "a"))
        else:
            f = csv.writer(open("cron.csv", "a"))
            f.writerow(["Algorithm", "Query", "Time", "Input Octects", 
                "Output Octects", "Input Packets", "Output Packets", 
                "InOctectSTDDev", "InOctectAvg", "OutOctectSTDDev", "OutOctectAvg",
                "InPacketSTDDev", "InPacketAvg", "OutPacketSTDDev", "OutPacketAvg"])

        smoothRow = ["Smooth", query, time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(data['time'][-1]))]
        normalRow = ["Regular", query, time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(data['time'][-1]))]
        changedNormal = False
        changedSmooth = False

        for key in keys:
            # First up is the exponential smoothing algorithm.
            '''
            print "Now checking the data and smooth stuff from the %s query" % query
            print "Length of data entry: %s" % len(data[key])
            print "First entry in data[%s]: %s" % (key, data[key][0])
            print "Last entry in data[%s]: %s" % (key, data[key][-1])
            print "First entry in smooth[%s]: %s" % (key, smooth[key][0])
            print "Last entry in smooth[%s]: %s" % (key, smooth[key][-1])
            print "REGULAR STD DEV for %s: %s" % (key, standardDev[key])
            print "SMOOTH STD DEV for %s: %s" % (key, smoothStdDev[key])
            print "REGULAR AVERAGE for %s: %s" % (key, average[key])
            print "SMOOTH AVERAGE for %s: %s" % (key, smoothAverage[key])
            print " "
            '''

            # If there's an anomaly, write it out with an X next to it.
            if (abs(data[key][-1] - average[key]) > (regularfactor * standardDev[key])):
                countregular += 1
                normalRow.append("X %s" % data[key][-1])
                changedNormal = True
            else:
                normalRow.append(data[key][-1])
            if (abs(smooth[key][-1] - smoothAverage[key]) > (smoothedfactor * smoothStdDev[key])):
                countsmooth += 1
                smoothRow.append("X %s" % smooth[key][-1])
                changedSmooth = True
            else:
                smoothRow.append(smooth[key][-1])

        for key in keys:
            smoothRow.append(smoothStdDev[key])
            smoothRow.append(smoothAverage[key])
            normalRow.append(standardDev[key])
            normalRow.append(average[key])

        # json.dumps(data, sort_keys=True)
        # print "Dumping data: %s" % data
        # print "\n"
        # json.dumps(smooth, sort_keys=True)
        # print "Dumping smooth: %s" % smooth

        if changedSmooth == True or changedNormal == True:
            f.writerow(smoothRow)
            f.writerow(normalRow)
            f.writerow([])
        del smoothRow[:]
        del normalRow[:]

    def anomaly(self, id, start, end = None):
        if end is None:
            queries = dq.queryJSON()
            for key, query in queries.iteritems():
                data = {'input octet': [], 'output octet': [], 'input packet': [], 'output packet': [], 'time': []}
                for item in query(c, id, start):
                    data['input octet'].append(item[0])
                    data['output octet'].append(item[1])
                    data['input packet'].append(item[2])
                    data['output packet'].append(item[3])
                    data['time'].append(item[6])

                smooth = aa.expoSmooth(data, 0.125)
                na.handleAnomalies(data, smooth, key)

        else:
            data = {'input octet': [], 'output octet': [], 'input packet': [], 'output packet': [], 'time': []}
            for item in dq.GetDataRange(c, id, end, start):
                data['input octet'].append(item[0])
                data['output octet'].append(item[1])
                data['input packet'].append(item[2])
                data['output packet'].append(item[3])
                data['time'].append(item[6])

            smooth = aa.expoSmooth(data, 0.4)
            timedump = smooth['time']
            print len(timedump)

            # To test the graph out.
            key = 'input octet'
            plotOriginalvsSmoothed(timedump, data, smooth, key)
            na.handleAnomalies(data, smooth, "DataRange")

# This function handles the Flask application, and
# gathers all of the data from the input.
def handle(id, start, end):
    global dq
    global na
    global aa
    global c
    # Create the MySQLdb object with the proper credentials to connect to
    # the data base with all of the network flow data.
    if 'port' in credentials.login:
        db = MySQLdb.connect(user = credentials.login['user'], 
        passwd = credentials.login['password'],
        db = credentials.login['db'],
        host = credentials.login['host'],
        port = int(credentials.login['port']))
    else:
        db = MySQLdb.connect(user = credentials.login['user'], 
            passwd = credentials.login['password'],
            db = credentials.login['db'],
            host = credentials.login['host'])
    c = db.cursor()

    # Create the DataQuery object to extract all of the data from the database,
    # the NetworkAnomaly object to handle anomaly detection with the data,
    # and the AnomalyAlgorithm object to handle any calculations and running
    # the data through the different algorithms.
    dq = DataQuery()
    na = NetworkAnomaly()
    aa = AnomalyAlgorithm()

    start = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
    end = time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y").timetuple())

    na.anomaly(id, start, end)
    db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        Usage()
    
    # Create the MySQLdb object with the proper credentials to connect to
    # the data base with all of the network flow data.
    if 'port' in credentials.login:
        db = MySQLdb.connect(user = credentials.login['user'], 
        passwd = credentials.login['password'],
        db = credentials.login['db'],
        host = credentials.login['host'],
        port = int(credentials.login['port']))
    else:
        db = MySQLdb.connect(user = credentials.login['user'], 
        	passwd = credentials.login['password'],
        	db = credentials.login['db'],
        	host = credentials.login['host'])
    c = db.cursor()

    # Create the DataQuery object to extract all of the data from the database,
    # the NetworkAnomaly object to handle anomaly detection with the data,
    # and the AnomalyAlgorithm object to handle any calculations and running
    # the data through the different algorithms.
    dq = DataQuery()
    na = NetworkAnomaly()
    aa = AnomalyAlgorithm()

    try:
        # If the user wants to specify a start and end time, as well as an ID.
        if len(sys.argv) == 4:
            script, start, end, id = sys.argv
            start = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
            end = time.mktime(datetime.datetime.strptime(end, "%d/%m/%Y").timetuple())
            if int(id) not in possibleIDs:
                raise Exception
            na.anomaly(id, start, end)

        # If the user wants to specify only a start time and ID.
        if len(sys.argv) == 3:
            script, start, id = sys.argv
            # If the start time parameter is actually a file
            # containing the start time in a single line
            # with he format "D/M/Y H:M:S", then open it up,
            # and convert the time to unix timestamp.
            # This will mostly be used to simply automate the
            # task with a cron job that will automatically
            # move the date forward for data gathering purposes.
            if os.path.isfile(start) == True:
                with open(start, 'r') as f:
                    start = f.readline()
                    start = start.replace('\n', '')
                    start = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y %H:%M:%S").timetuple())
                    print start
                    print type(start)
                    f.close()
            else:
                start = time.mktime(datetime.datetime.strptime(start, "%d/%m/%Y").timetuple())
            if int(id) not in possibleIDs:
                raise Exception
            na.anomaly(id, start)

        # If the user only wants to specify an ID, then the start time will be the current
        # time, and will run the sequence of time queries accordingly.
        if len(sys.argv) == 2:
            script, id = sys.argv
            now = time.time()
            now = int(now - now % 300)
            na.anomaly(id, now)
    except Exception as e:
        _, _, tb = sys.exc_info()
        print traceback.format_list(traceback.extract_tb(tb))
        print "Error in line %s: %s\n" % (sys.exc_info()[-1].tb_lineno, e)
        Usage()

    db.close()