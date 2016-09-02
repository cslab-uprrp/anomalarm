#!/usr/bin/env python
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