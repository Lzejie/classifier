# encoding=utf8

import numpy as np

from featureStatic import FeatureStatic


class FeatureSelector(object):

    def __init__(self, method='IG', trainListPath='./data/trainList.txt', classLabelPath='./data/classLabel.txt',
                 featureListPath='./data/featureList.txt'):
        '''
        :param method:筛选方法
        :param trainListPath: 训练集路径
        :param classLabelPath: 每行训练数据的归属类别
        :param featureListPath: 特征数组最终保存路径
        '''
        self.featureVector = None
        self.method = method
        self.trainListPath = trainListPath
        self.classLabelPath = classLabelPath
        self.featureListPath = featureListPath

    def __featureSelectionIG(self, classCountList, featureOrderList, featureClassStatic):
        '''
        使用信息增益打方式筛选特征
        '''
        A = featureClassStatic
        B = np.array([(sum(word) - word) for word in featureClassStatic])
        C = np.tile(classCountList, (A.shape[0], 1)) - A
        N = sum(classCountList)
        D = N - A - B - C
        classCount = len(classCountList)

        # the probability of
        p_t = np.sum(A, axis=1) / N
        p_not_t = 1 - p_t
        p_c_t = (A + 1.0) / (A + B + classCount)
        p_c_not_t = (C + 1.0) / (C + D + classCount)

        p_c_t_score = np.sum(p_c_t * np.log2(p_c_t), axis=1)
        p_c_not_t_score = np.sum(p_c_not_t * np.log2(p_c_not_t), axis=1)

        featureScore = p_t * p_c_t_score + p_not_t * p_c_not_t_score
        featureScoreList = featureScore.argsort()[::-1]

        return [featureOrderList[index] for index in featureScoreList]


    def __featureSelectionMI(self, classCountList, featureOrderList, featureClassStatic):
        '''
        使用互信息打方式筛选特征
        '''
        A = featureClassStatic
        B = np.array([(sum(word) - word) for word in featureClassStatic])
        C = np.tile(classCountList, (A.shape[0], 1)) - A
        N = sum(classCountList)

        featureScore = np.log2(((A + 1.0) * N) / ((A + C) * (A + B + len(classCountList))))
        featureScoreList = np.max(featureScore, axis=1).argsort()[::-1]

        return [featureOrderList[index] for index in featureScoreList]

    def __featureSelectionWLLR(self, classCountList, featureOrderList, featureClassStatic):
        pass

    def getFeature(self, count=50000):
        '''
        获取特征
        :param count: 截取多少个特征
        :return:返回特征数组
        '''
        fs = FeatureStatic()
        classCountList, featureOrderList, featureClassStatic = fs.getStaticData(
            self.trainListPath, self.classLabelPath)

        featureVec = []
        if self.method == "IG":
            featureVec = self.__featureSelectionIG(classCountList, featureOrderList, featureClassStatic)
        elif self.method == "MI":
            featureVec = self.__featureSelectionMI(classCountList, featureOrderList, featureClassStatic)
        # elif self.method == "WLLR":
        #     featureVec = self.__featureSelectionWLLR(classCountList, featureOrderList, featureClassStatic)

        with open(self.featureListPath, 'wb') as f:
            for item in featureVec[:count]:
                f.write(item + '\n')
        return featureVec[:count]










