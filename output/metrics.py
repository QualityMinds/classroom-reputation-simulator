import numpy as np

def printMetrics(name, reputationVector, groups):
    distinction, correctness, inversionQ = getMetrics(reputationVector, groups)
    print("")
    print("######## Final Metrics: " + name + " ########")
    print("Distinction: " + str(distinction))
    print("Correctness: " + str(correctness))
    print("Inversion Quality: " + str(inversionQ))

def printStdDevMetrics(name, intermediateResults, groups):
    meanDis, stdDis, meanCor, stdCor, meanInvQ, stdInvQ = getMetricsStdDev(intermediateResults, groups)
    print("")
    print("######## Mean & Std. Dev.: " + name + " ########")
    print("Distinction: " + str(meanDis) + " ± " +  str(stdDis))
    print("Correctness: " + str(meanCor) + " ± " +  str(stdCor))
    print("Inversion Quality: " + str(meanInvQ) + " ± " +  str(stdInvQ))

def getMetricsStdDev(intermediateResults, groups):
    disList = list()
    corList = list()
    invQList = list()

    for result in intermediateResults:
        dis, cor, invQ = getMetrics(result, groups)
        disList.append(dis)
        corList.append(cor)
        invQList.append(invQ)

    meanDis = np.mean(disList)
    stdDis = np.std(disList)

    meanCor = np.mean(corList)
    stdCor = np.std(corList)

    meanInvQ = np.mean(invQList)
    stdInvQ = np.std(invQList)

    return meanDis, stdDis, meanCor, stdCor, meanInvQ, stdInvQ


def count_members(data, group):
    return len([l for (_, l, _) in data if l == group])


def isInCorrectZone(groups, reputationVector, label, index):
    minimum = 0
    maximum = 0
    for i in range(0, len(groups)):
        if groups[i] == label:
            maximum = minimum + count_members(reputationVector, label)
            break
        else:
            minimum +=  count_members(reputationVector, groups[i])

    return index >= minimum and index < maximum


def convertToRankingArray(groups, reputationVector):
    result = list()
    for i in range(0, len(reputationVector)):
        for j in range(0, len(groups)):
            if(reputationVector[i][1] == groups[j]):
                result.append(j)
    return result


def getMetrics(reputationVector, groups):
    inversions = 0
    inversionRatio = 0
    distinction = 0
    correctness = 0

    count = len(reputationVector)

    #Distinction
    averageDiff = 0
    for i in range(0, count - 1):
        averageDiff += reputationVector[i+1][0] - reputationVector[i][0]

    averageDiff = averageDiff / count

    currIdx = 0
    for i in range(0, len(groups) - 1):
        currIdx += count_members(reputationVector, groups[i])
        distinction += (reputationVector[currIdx][0] - reputationVector[currIdx - 1][0]) / averageDiff

    if(len(groups) > 1):
        distinction /= (len(groups) - 1)

    #Correctness
    for i in range(0, count):
        if isInCorrectZone(groups, reputationVector, reputationVector[i][1], i):
            correctness += 1

    correctness = correctness / count

    #Inversions
    rankedArr = convertToRankingArray(groups, reputationVector)
    for i in range(0, count):
        for j in range(0, i):
            if rankedArr[j] > rankedArr[i]:
                inversions += 1

    maxInversions = (count * (count - 1)) / 2

    for group in groups:
        groupSize = count_members(reputationVector, group)
        maxInversions -= (groupSize * (groupSize - 1)) / 2

    inversionRatio = inversions / maxInversions
    inversionRatio = 1 - inversionRatio

    return distinction, correctness, inversionRatio