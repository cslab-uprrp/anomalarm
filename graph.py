#!/usr/bin/env python
import sys
import time
import os

def plotOriginalvsSmoothed(timearr, original, smoothed, key):
	value = 300 * 24

	if(timearr[0] % value == 0):
		stime = "'%s'" % time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(timearr[0]))
	else:
		stime = "''"
	soriginal = "%s" % str(original[key][0])
	ssmoothed = "%s" % str(smoothed[key][0])
	for i in range(1,len(original[key])):
		if(timearr[i] % value == 0):
			stime += ", '%s'" % time.strftime("%a, %d %b %Y %I:%M:%S %p", time.localtime(timearr[i]))
		else:
			stime += ",''"
		soriginal += ", %s" % str(original[key][i])
		ssmoothed += ", %s" % str(smoothed[key][i])

	stime += "],"
	soriginal += "]"
	ssmoothed += "]"
	js = """var lineChartData = {
		labels : ["""
	js += stime
	js += """
		datasets : [
			{
				label: "Original",
				fillColor : "rgba(40,40,205,0.1)",
				strokeColor : "rgba(40,40,205,1)",
				pointColor : "rgba(40,40,205,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(40,40,205,1)",
				data : ["""
	js += soriginal
	js += """
			},
			{
				label: "Smoothed",
				fillColor : "rgba(20,187,30,0.2)",
				strokeColor : "rgba(20,187,30,1)",
				pointColor : "rgba(20,187,30,1)",
				pointStrokeColor : "#fff",
				pointHighlightFill : "#fff",
				pointHighlightStroke : "rgba(151,187,205,1)",
				data : ["""
	js += ssmoothed
	js += """
			}]}
		window.onload = function(){
				var ctx1 = document.getElementById("canvas").getContext("2d");
				window.myLine = new Chart(ctx1).Line(lineChartData, {
						responsive: true
				});
		}
	"""
	script_dir = os.path.dirname(__file__)
	rel_path = "static/graph.js"
	abs_file_path = os.path.join(script_dir, rel_path)
	text_file = open(abs_file_path, "w")
	text_file.write(js)
	text_file.close()
