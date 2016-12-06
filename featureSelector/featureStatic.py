# encoding=utf8

import numpy as np

class FeatureStatic(object):

    def __loadFile(self, trainListPath, classLabelPath):
        '''
        读取trainList和classLabel
        '''
        with open(trainListPath, 'rb') as trainFile:
            with open(classLabelPath, 'rb') as classFile:
                trainWrodsList = map(lambda x : x.split(' '), trainFile.readlines())
                eachLineClassList = classFile.readlines()
                return map(lambda x: map(lambda y:y.replace('\n', ''),x),trainWrodsList), map(lambda x:x.replace('\n', ''),eachLineClassList)

    def __getClassDict(self, classLabel):
        '''
        生成classLable字典
        :return:classLabel字典，类别对应他的序号
        '''
        classSet = list(set(classLabel))
        classDict = dict(zip(classSet, range(len(classSet))))
        return classDict

    def __getFeatureDict(self, trainWordsList):
        '''
        返回一个特征字典，对应有他的序号
        :param trainWordsList:the trainWordsList
        :return:特征字典
        '''
        featureDict = {}
        for trainWords in trainWordsList:
            for word in set(map(lambda x:x.replace('\n', ''),trainWords)):
                featureDict[word] = 1
        featureSetList = sorted(featureDict.keys())
        featureDict = dict(zip(featureSetList, range(len(featureSetList))))
        return featureDict

    def __getEachTypesCount(self, classDict, eachLineClassList):
        '''
        获取每个class打数量
        :param classDict:list of each type
        :param eachLineClassList:
        :return:each type of class's count
        '''
        classCountList = [0] * len(classDict)
        for each in eachLineClassList:
            classCountList[classDict[each]] += 1
        return classCountList

    def __getEachFeatureInEachClassCount(self, trainWordsList, eachLineClassList, featureDict, classDict):
        '''
        static a word(feature) each line in trainWordsList on each class's count
        :return:an array which is [len(trainWordsList), len(classDict)], use to static the feature on each class's count
        '''
        featureClassStatic = np.zeros((len(featureDict), len(classDict)), np.float32)
        for index in range(len(trainWordsList)):
            classIndex = classDict[eachLineClassList[index]]
            trainWords = trainWordsList[index]
            for word  in set(map(lambda x: x.replace('\n', ''),trainWords)):
                featureIndex = featureDict[word]
                featureClassStatic[featureIndex][classIndex] += 1
        return featureClassStatic

    def getStaticData(self, trainListPath='../data/trainList.txt', classLabelPath='../data/classLabel.txt'):
        '''
        main function
        :return: classCountList, which include each class's count
                 featureOrderList is a list of feature that is sorted
                 featureClassStatic is each feature in each class's count
        '''
        trainWordsList, eachLineClassList = self.__loadFile(trainListPath, classLabelPath)
        classDict = self.__getClassDict(eachLineClassList)
        featureDict = self.__getFeatureDict(trainWordsList)
        classCountList = self.__getEachTypesCount(classDict, eachLineClassList)
        featureClassStatic = self.__getEachFeatureInEachClassCount(trainWordsList, eachLineClassList,
                                                                   featureDict, classDict)
        featureOrderList = [term[0] for term in sorted(featureDict.items(), key= lambda x:x[1])]
        return classCountList, featureOrderList, featureClassStatic


