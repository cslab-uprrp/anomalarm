#!/usr/bin/env python
from math import sqrt 
import random
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

"""
This class implements all of the algorithms used
to detect network anomalies, including any methods
that may be necessary to calculate attributes.
"""
class AnomalyAlgorithms(object):
	def expoSmooth(self, data, alpha):
		"""
		Carries out exponential smoothing on the data
		using a specified alpha value:

		smooth[0] = data[0]
		smooth[i] = alpha * data[i] + (1 - alpha) * smooth[i - 1], where i > 0
		"""
		smoothed = {}
		for key, value in data.iteritems():
			if key == 'time':
				smoothed[key] = data[key]
			else:
				smoothed[key] = []
				smoothed[key].append(value[0])

		keys = [x for x in data.keys() if x != 'time']
		length = len(data[keys[0]])
		for key in keys:
			for i in range(1, length):
				smoothed[key].append((alpha * float(data[key][i])) + ((1 - alpha) * float(smoothed[key][i-1])))
		return smoothed 

	def avg(self, data):
		"""
		Calculates the average of a data list.
		"""
		return sum(data) / float(len(data))

	def average(self, data):
		"""
		Calculates the average of the data. Returns a
		dictionary with all of the averages for all of the
		keys.
		"""
		average = {}
		keys = [x for x in data.keys() if x != 'time']
		length = len(data[keys[0]])
		for key in keys:
			average[key] = sum(data[key]) / float(length)
		return average

	def variance(self, data):
		"""
		Calculates the variance of the data, which is used
		to calculate the standard deviation.
		"""
		variance = []
		average = self.avg(data)
		for x in data:
			variance.append((x - average)**2)
		return variance

	def stdDev(self, data):
		"""
		Calculates the standard deviation of the data. Returns
		a dictionary with all of the standard deviations.
		"""
		standardDev = {}
		keys = [x for x in data.keys() if x != 'time']
		length = len(data[keys[0]])
		for key in keys:
			standardDev[key] = sqrt(sum(self.variance(data[key])) / (length - 1))
		return standardDev

	def smoothStdDev(self, data, smooth, beta):
		"""
		Calculates the standard deviation for the
		smoothed values using the regular data and
		a beta value. Returns a dictionary with all
		of the standard variations.
		"""
		smoothDev = {}
		keys = [x for x in data.keys() if x != 'time']
		length = len(data[keys[0]])
		for key in keys:
			smoothDev[key] = 0
			for i in range(length):
				smoothDev[key] = ((1 - beta) * smoothDev[key]) + (beta * abs(data[key][i] - smooth[key][i]))
		return smoothDev

	def linearRegress(self, data):
		lm = LinearRegression()
		X = []
		dat = []
		keys = ['input packet','output octet', 'output packet']
		for i in range(len(data['input octet'])):
			temp = []
			for key in keys:
				temp.append(data[key][i])
			X.append(temp)
		for i in range(len(data['input octet'])):
			dat.append([data['input octet'][i]])
		print "X check", X
		lm.fit(X, data['input octet'])
		Y = lm.predict(X)
		# M = lm.predict(dat)
