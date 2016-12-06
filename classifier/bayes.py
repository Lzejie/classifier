# encoding=utf8

import os

import numpy as np
from sklearn.cross_validation import train_test_split
from splitWords.split_words import WordsSpliter
from featureSelector.selector import  FeatureSelector

class BayesClassifier(object):
    '''
    贝叶斯分类器
    '''
    def __init__(self):
        '''
        初始化贝叶斯分类器，读取特征列表，生成一个分词器
        '''
        self.vectorList = []
        self.wordSpliter = WordsSpliter()
        self.featureList = map(lambda x:x.replace('\n', ''), open('./data/featureList.txt', 'rb').readlines())
        self.trainListList, self.classList = self.wordSpliter.getFeatureAndClass()
        self.classSet = sorted(list(set(self.classList)))
        self.bayesVec = np.ones((len(self.classSet), len(self.featureList)))
        self.featureDict = dict(zip(self.featureList, range(len(self.featureList))))

    def loadData(self):
        for index in range(len(self.trainListList)):
            textType = self.classList[int(index)]
            for feature in set(self.trainListList[index]) & set(self.featureList):
                self.bayesVec[textType][self.featureList.index(feature)] += 1

        self.bayesVec = self.bayesVec / np.sum(self.bayesVec, axis=0)

    def test(self):
        print 'now start test'
        trainData, testData, trainLabel, testLabel = train_test_split(self.trainListList, self.classList, test_size=0.2)
        classifier = np.ones(self.bayesVec.shape)
        # 构建一个字典，提高检索速度
        for index in range(len(trainData)):
            textType = trainLabel[int(index)]
            for feature in set(trainData[index]) & set(self.featureList):
                classifier[textType][self.featureDict[feature]] += 1
        classifier = classifier / np.sum(classifier, axis=0)

        result = self.__predict(testData, classifier=classifier)

        right = 0
        for index in range(len(testLabel)):
            if result[index] == testLabel[index]:
                right += 1
        print 'right count %s'%right
        print 'total count %s'%len(testLabel)
        print right*1.0/len(testLabel)

    def __predict(self,predictData, classifier=None):
        print 'now start predict'
        if classifier is None:
            classifier = self.bayesVec

        predictData = [predictData] if not isinstance(predictData, list) else predictData
        result = []
        for line in predictData:
            tmp = [0] * classifier.shape[1]
            for item in set(line) & set(self.featureList):
                tmp[self.featureDict[item]] = 1
            result.append(np.where(np.sum(np.log(classifier) * tmp, axis=1) == np.max(np.sum(np.log(classifier) * tmp, axis=1)))[0][0])

        return result

if __name__ == '__main__':
    reMakeTrainList = None
    while 1:
        reMakeTrainList = raw_input(u'是否重新生成trainList和classLabel?(y/n)')
        if reMakeTrainList == 'y' or reMakeTrainList == 'Y':
            files = []
            for root, dirs, f in os.walk('/home/dev/project/classify/data/source'):
                files = f
                break
            ws = WordsSpliter('../data/stopWords.txt')
            ws.splitFiles(map(lambda x: root + '/' + x, files), '../data/')
            break
        elif reMakeTrainList == 'n' or reMakeTrainList == 'N':
            break

    reMakeFeatureList = None
    while 1:
        reMakeFeatureList = raw_input(u'是否重新生成特征列表(y/n)')
        if reMakeFeatureList == 'y' or reMakeFeatureList == 'Y':
            fs = FeatureSelector(method='IG', trainListPath='../data/trainList.txt',
                                 classLabelPath='../data/classLabel.txt', featureListPath='../data/featureList.txt')
            fs.getFeature()
            break
        elif reMakeFeatureList == 'n' or reMakeFeatureList == 'N':
            break














