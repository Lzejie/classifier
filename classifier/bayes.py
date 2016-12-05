# encoding=utf8

import os

from splitWords.split_words import WordsSpliter
from featureSelector.featureStatic import  FeatureStatic

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
        self.featureList = open('../data/featureList.txt', 'rb').readlines()
        



if __name__ == '__main__':
    reMakeTrainList = None
    while 1:
        reMakeTrainList = raw_input(u'是否重新生成trainList和classLabel?(y/n)')
        if reMakeTrainList == 'y' or reMakeTrainList == 'Y':
            files = []
            for root, dirs, f in os.walk('/home/dev/project/classify/data/source'):
                files = f
                break
            ws = WordsSpliter()
            ws.splitFiles(map(lambda x: root + '/' + x, files))
            break
        elif reMakeTrainList == 'n' or reMakeTrainList == 'N':
            break

    reMakeFeatureList = None
    while 1:
        reMakeFeatureList = raw_input(u'是否重新生成特征列表(y/n)')
        if reMakeFeatureList == 'y' or reMakeFeatureList == 'Y':
            fs = FeatureStatic()
            fs.getStaticData()
            break
        elif reMakeFeatureList == 'n' or reMakeFeatureList == 'N':
            break














