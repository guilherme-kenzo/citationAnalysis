#!/usr/bin/env python3

import textract
import re
from string import punctuation
from sys import argv
from nltk.data import load
from nltk.corpus import stopwords

class PdfText(object):

    def __init__(self, pdfFile):
        self.text = ""
        self.sentTokens = []
        self.sentTokensNoStopWords = []
        self.fileName = pdfFile
        self.citations = []
        self.pageList = []
        self.getText()
        self.splitToList()
        self.nPages = ""
        self.ngrams = []
        self.removeMatching()


    def removeMatching(self):
        self.text = re.sub('página \d ?\d? de \d\d',' ' , self.text)
        self.text = re.sub('documento: \d+ - inteiro teor do acórdão - site certificado - dje: \d{2}/\d{2}/\d{4}',' ' ,self.text)

    def getText(self):
        """ extract text from pdf file"""
        try:
            self.text = textract.process(self.fileName).decode('utf-8').lower().replace('\n', ' ')
            return self.text
        except textract.exceptions.MissingFileError as e:
            raise e


    def removeStopWords(self):
        """Remove stopWords from a given list of sentences"""
        stopWords = stopwords.words('portuguese')
        noPunctSents = [self.stripPunct(i) for i in self.sentTokens]
        # sentences = self.stripPunct(self.sentTokens)
        # print(sentences)
        newList = []
        for sent in noPunctSents:
            tmpSent = [i for i in sent.split() if i not in stopWords]
            newList.append(' '.join(tmpSent))

        self.sentTokensNoStopWords = newList
        return self.sentTokensNoStopWords

    def stripPunct(self, textString):
        """remove punctuation"""
        table = str.maketrans({key: None for key in punctuation})
        return textString.translate(table)
        # newList = []
        # for i in tokens:
        #     newList.append(i.translate(table))
        # return newList

    def tokenizer(self):
        """Tokenize string to list of sentences"""
        sentTokenizer = load('tokenizers/punkt/portuguese.pickle')
        self.sentTokens = sentTokenizer.tokenize(self.text)
        # self.sentTokensNoStopWords = removeStopWords(self.sentTokens)
        # self.sentTokensNoStopWords = stripPunct(self.sentTokensNoStopWords)
        return self.sentTokens


    def splitToList(self):
        """Splits document into list of pages, with each item corresponding
        to a page in the pdf file"""
        self.pageList = re.split('página \d ?\d? de \d\d', self.text)
        self.nPages = len(self.pageList)
        return self.pageList


    def nGrammer(self, tokenList, n):
        """Returns N-gram of list of sentences"""
        newList = []
        for i in tokenList:
            newList.append(list(zip(*[tokenList[i:] for i in range(n)])))
        self.ngrams = newList
        return self.ngrams

    def getMinistros(self):
        listOfMatches = []
        for i in self.pageList:
            matchedMinistros = re.findall('(?<=Ministro |Ministra )\w+',
                                          self.text)
            for j in matchedMinistros:
                listOfMatches.append(j)
        return listOfMatches

if __name__ == '__main__':
    obj = PdfText('ITA.pdf')
    obj.tokenizer()
    obj.removeStopWords()
    obj.sentTokensNoStopWords
    
