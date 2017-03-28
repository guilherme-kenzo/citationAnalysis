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
        self.fileName = ""
        self.citations = []
        self.pageList = []
        self.getText(pdfFile)
        self.splitToList()
        self.nPages = ""
        self.ngrams = []
        self.tokenizer()


    def getText(self, pdfFile):
        """ extract text from pdf file"""
        try:
            self.text = textract.process(pdfFile).decode('utf-8').lower()
            return self.text
        except textract.exceptions.MissingFileError as e:
            raise e


    def removeStopWords(self, sentences):
        """Remove stopWords from a given list of sentences"""
        stopWords = stopwords.words('portuguese')
        newList = []
        for i in sentences:
            for j in stopWords:
                i = i.replace(j, '')
            newList.append(i)
        return newList


    def tokenizer(self):
        """Tokenize string to list of sentences"""
        sentTokenizer = load('tokenizers/punkt/portuguese.pickle')
        self.sentTokens = sentTokenizer.tokenize(self.text)
        self.sentTokensNoStopWords = removeStopWords(self.sentTokens)
        self.sentTokensNoStopWords = cleanUp(self.sentTokensNoStopWords)
        return self.sentTokens


    def cleanUp(self, stoplessTokens):
        """remove punctuation"""
        table = str.maketrans({key: None for key in punctuation})
        newList = []
        for i in stoplessTokens:
            newList.appen(i.translate(table))
        return newList


    def splitToList(self):
        """Splits document into list of pages, with each item corresponding
        to a page in the pdf file"""
        self.pageList = re.split('Página +\d+ +de +\d+', self.text)
        self.nPages = len(self.pageList)
        return self.pageList


    def find_ngrams(self, tokenList, n):
        """Returns N-gram of list of sentences"""
        newList = []
        for i in tokenList:
            newList.append(zip(*[input_list[i:] for i in range(n)]))
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
