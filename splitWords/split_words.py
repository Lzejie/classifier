# encoding:utf8

import jieba


class WordsSpliter(object):
    '''
    1. 用于将文本文件转化为词语向量字符串，并保存在data目录下打trainList和classLabel中
    2. 用于将字符串转化为词语数组并返回
    '''

    def __init__(self, stopWordsPath='../data/stopWords.txt'):
        self.stopWords = set()
        with open(stopWordsPath, 'rb') as f:
            for line in f.readlines():
                try:
                    self.stopWords.add(line.replace('\t', '').replace('\n', '').decode('utf8'))
                except:
                    self.stopWords.add(line.replace('\t', '').replace('\n', ''))

    # def __loadFile(self, paths):
    #     '''
    #     用于读取文本文件
    #     :param paths:文件路径数组
    #     :return:返回文件列表
    #     '''
    #     fileList = []
    #     for path in paths:
    #         fileList.append(open(path))
    #
    #     return fileList

    def __fileText2WordsList(self, path):
        '''
        将文本文件转化为词语数组并返回
        :param path: 文本文件路径
        :return: word string
        '''
        wordsStringList = []
        with open(path.decode('utf8'), 'rb') as f:
            for line in f.readlines():
                wordsStringList.append(' '.join(self.__text2WordsList(line)).replace('\n', '').replace('\r', ''))

        return wordsStringList

    def __text2WordsList(self, text):
        '''
        将文本转化为词语数组，并去停用词
        :param text:文本内容
        :return:词语数组
        '''
        wordsList = []
        text = text.replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace(' ', '')
        for word in jieba.cut(text):
            if word not in self.stopWords:
                try:
                    float(word)
                except:
                    wordsList.append(word) if word else None
        return wordsList

    def __saveToLocal(self, localpath, stringList):
        '''
        save the list of words list to local
        将词语数组转化为字符串，并保存到本地
        :param localpath:本地路径
        :param wordsListList:词语数组的数组
        '''
        with open(localpath, 'wb') as f:
            for line in stringList:
                f.write(line.encode('utf8').replace('\n', '') + '\n') if line else None

    def getFeatureAndClass(self, trainListPath, classLabelPath):
        '''
        返回训练集和label
        '''
        featureListList = map(lambda x: x.split(' '), open(trainListPath, 'rb').readlines())
        classLabelList = open(classLabelPath, 'rb').readlines()

        return featureListList, classLabelList

    def splitAText(self, text):
        '''
        将一个文本转化为词语数组
        :param text:字符串
        :return:词语数组
        '''
        return self.__text2WordsList(text)

    def splitFiles(self, paths, localpath='../data/'):
        '''
        将一些文本文件转化为trainList和classLabel
        :param paths:文件路径数组
        :param localfile:本、保存路径
        '''
        print 'now running splitFiles '
        wordsStringListList = []
        labelList = []
        for index in range(len(paths)):
            print 'now start to split %s' % paths[index]
            wordsStringList = self.__fileText2WordsList(paths[index])
            label = ['%s'%index] * len(wordsStringList)
            wordsStringListList += wordsStringList
            labelList += label

        self.__saveToLocal(localpath=localpath+'trainList.txt', stringList=wordsStringListList)
        self.__saveToLocal(localpath=localpath+'classLabel.txt', stringList=labelList)


if __name__ == '__main__':
    paths = [u'../data/军事.txt', u'../data/房产.txt', u'../data/游戏.txt',
             u'../data/财经.txt', u'../data/科技.txt', u'../data/社会.txt']
    spliter = WordsSpliter('../data/stopWords.txt')
    spliter.splitFiles(paths)
