# encoding=utf8

class BayesClassifier(object):
    '''
    A Bayes Classifier
    '''
    def __init__(self):
        self.vectorList = []

    def __loadDataSet(self, trainListPath='../data/trainList.txt', classLabelPath='../data/classLabel.txt'):
        '''
        load the train list and the class label
        :param trainListPath:the train list's path
        :param classLabelPath:the class label's path
        :return:return the words list and class label
        '''
        with open(trainListPath, 'rb') as f:
            wordsStringList = f.readlines()
        with open(classLabelPath, 'rb') as f:
            classLabelList = f.readlines()
        return wordsStringList, classLabelList

    def __createVectorList(self, wordsStringList):
        '''
        create a vector list which include all the words
        :param wordsStringList:the words string list
        '''
        vectorSet = set([])
        for line in wordsStringList:
            vectorSet = vectorSet | set(line.split(' '))

        with open('../data/vectorList.txt', 'wb') as f:
            f.write(' '.join(vectorSet))

        self.vectorList = list(vectorSet)

    def setOfWrods2Vector(self, wordsList):
        '''
        shift words to vector
        :param wordsList:words list
        :return:words list's vector
        '''
        tmpList = [0] * len(self.vectorList)
        for word in wordsList:
            if word in self.vectorList:
                tmpList[self.vectorList.index(word)] = 1
        return tmpList




