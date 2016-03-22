from math import sqrt 
import random

# This class implements all of the algorithms used
# to detect network anomalies, including any methods
# that may be necessary to calculate attributes.

class AnomalyAlgorithm:
    # Let's try to smooth the data.
    # Here we're going to use the already created list of
    # data (for octects and packets), an alpha value,
    # and apply the algorithm:
    # s_0 = x_0
    # s_i = a * x_i + (1 - a) * s_i-1, where i > 0
    def expoSmooth(self, data, alpha):
        # We'll store the smoothed data in a list.
        smoothed = {'input octet': [], 'output octet': [], 'input packet': [], 'output packet': [], 'time': []} 

        # Let's start with: smoothed[0] = data[0]
        for key, value in data.iteritems():
            if key == 'time':
                smoothed[key] = data[key]
            else:
                smoothed[key].append(value[0])

        # Now traversing the data to apply the algorithm.
        # Remove the 'time' key from the iterator, since
        # the smoothed time and regular time are the same
        # and have already been handled.
        keyList = data.keys()
        keyList.remove('time')
        length = len(data['time'])
        for key in keyList:
            for i in range(1, length):
                smoothed[key].append((alpha * float(data[key][i])) + ((1 - alpha) * float(smoothed[key][i-1])))
        return smoothed 

    def smoothStdDev(self, data, smoothdata, beta):
        smoothDev = {'input octet': 0, 'output octet': 0, 'input packet': 0, 'output packet': 0}
        keyList = data.keys()
        keyList.remove('time')
        length = len(data['time'])
        # keyList = ['input octet', 'output octet', 'input packet', 'output packet']
        for key in keyList:
            for i in range(0, length):
                smoothDev[key] = ((1 - beta) * smoothDev[key]) + (beta * abs(data[key][i] - smoothdata[key][i]))
        return smoothDev

    # Get that average.
    def avg(self, data, totalRow):
        return sum(data) / float(totalRow)

    def getAverage(self, data):
        average = {'input octet': 0, 'output octet': 0, 'input packet': 0, 'output packet': 0}
        keys = data.keys()
        keys.remove('time')
        length = len(data[keys[0]])
        for key in keys:
            average[key] = sum(data[key]) / float(length)
        return average

    # Get that variance.
    def variance(self, data, totalRow):
        arrVar = []
        average = self.avg(data, totalRow)
        for i in range(totalRow):
            arrVar.append((data[i] - average)**2)
        return arrVar

    # Get that standard deviation
    def stdDev(self, data):
        standardDev = {'input octet': 0, 'output octet': 0, 'input packet': 0, 'output packet': 0}
        keys = data.keys()
        keys.remove('time')
        length = len(data[keys[0]])
        for key in keys:
            standardDev[key] = sqrt(sum(self.variance(data[key], length)) / (length - 1))
        return standardDev

    def prepKNN(self, split, dataset, trainingSet, testSet):
        for x in range(len(dataset) - 1):
            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

    def euclideanDistance(self, setOne, setTwo, length):
        distance = 0
        for x in range(length):
            distance += pow((setOne[x] - setTwo[x]), 2)
        return sqrt(distance)

    def getNeighbors(self, trainingSet, testSet, k):
        distances = []
        length = len(testSet) - 1
        for x in range(len(trainingSet)):
            dist = self.euclideanDistance(testSet, trainingSet, length)
            distances.append((trainingSet, dist))
        distances.sort(key = operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors

    def getResponse(self, neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
            response = neighbors[x][-1]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        sortedVotes = sorted(classVotes.iteritems(), key = operator.itemgetter(1), reverse = True)
        return sortedVotes[0][0]

    def getAccuracy(self, testSet, predictions):
        correct = 0
        print len(predictions)
        for x in range(len(testSet)):
            if testSet[-1] == predictions[x]:
                correct += 1
        return (correct/float(len(testSet))) * 100.0