# encoding:utf8

import jieba


class WordsSpliter(object):
    '''
    use to split word from text
    '''

    def __init__(self, stopWordsPath='./data/stopWords.txt'):
        self.stopWords = set()
        with open(stopWordsPath, 'rb') as f:
            for line in f.readlines():
                try:
                    self.stopWords.add(line.replace('\t', '').replace('\n', '').decode('utf8'))
                except:
                    self.stopWords.add(line.replace('\t', '').replace('\n', ''))

    def __loadFile(self, paths):
        '''
        use to load the train data

        :param paths:input a file list
        :return:file list
        '''

        fileList = []
        for path in paths:
            fileList.append(open(path))

        return fileList

    def __fileText2WordsList(self, path):
        '''
        split file to words string list
        :param paths: file path
        :return: word string
        '''
        wordsStringList = []
        with open(path, 'rb') as f:
            for line in f.readlines():
                wordsStringList.append(' '.join(self.__text2WordsList(line)).replace('\n', '').replace('\r', ''))

        return wordsStringList

    def __text2WordsList(self, text):
        '''
        transform text to words list , then remove the stop word

        :param text:string
        :return:words list
        '''
        wordsList = []
        text = text.replace('\n', '').replace('\t', '').replace(' ', '').replace('\r', '').replace(' ', '')
        for word in jieba.cut(text):
            if word not in self.stopWords:
                try:
                    float(word)
                except:
                    wordsList.append(word)
        return wordsList

    def __saveToLocal(self, localpath, stringList):
        '''
        save the list of words list to local

        :param localpath:local path
        :param wordsListList:the list which need to be save to local
        '''
        with open(localpath, 'wb') as f:
            for line in stringList:
                f.write(line.encode('utf8') + '\n')

    def splitAText(self, text):
        '''
        split a text to words list
        :param text:String
        :return:words list
        '''
        return self.__text2WordsList(text)

    def splitFiles(self, paths, localpath='../data/'):
        '''
        split some file to words list, then save to local file

        :param paths:file path list
        :param localfile:local file path
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
