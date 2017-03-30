#!/usr/bin/env python3

import textract
import re
from nltk.corpus import stopwords
from nltk import word_tokenize, Text
from nltk.data import load
from string import punctuation

class STJparser(object):

    def __init__(self, pdfFile):
        self.pdfFile = pdfFile
        self.text = self.pdfTextExtracter()
        self.tokens = self.wordTokenizer()
        self.sentTokens = self.sentTokenizer()
        self.citations = self.citationExtracter()
        self.stoplessTokens = self.removeStopWords()
        self.stoplessSentTokens = self.sentTokensNoStopWords()
        self.wordFreq = self.wordFrequenizer()
        self.ngrams = self.nGrammer()

    def pdfTextExtracter(self):
        text = textract.process(self.pdfFile).decode('utf-8').lower().replace('\n',' ')
        text = re.sub('página \d ?\d? de \d\d',' ' , text)
        text = re.sub('documento: \d+ - inteiro teor do acórdão - site certificado - dje: \d{2}/\d{2}/\d{4}',' ' , text)
        return text
        print("---------->>>>>>>>>>>>>", type(self.text))

    def wordTokenizer(self):
        return word_tokenize(self.text)

    def citationExtracter(self):
        return []

    def sentTokenizer(self):
        tokenMaker = load('tokenizers/punkt/portuguese.pickle')
        return tokenMaker.tokenize(self.text)

    def removeStopWords(self):
        stopWords = stopwords.words('portuguese')
        return [i for i in self.tokens if i not in stopWords]

    def sentTokensNoStopWords(self):
        stopWords = stopwords.words('portuguese')
        doubleTokenizedSent = []
        for i in self.sentTokens:
            tmpList = [j for j in word_tokenize(i) if j not in stopWords]
            doubleTokenizedSent.append(tmpList)
        return doubleTokenizedSent

    def wordFrequenizer(self):
        return dict(Text(self.stoplessTokens).vocab())

    def stripPunct(self, textString):
        """remove punctuation"""
        table = str.maketrans({key: None for key in punctuation})
        return textString.translate(table)

    def nGrammer(self, n=2):
        nGramList = []

        for sent in self.stoplessSentTokens:
            tmpList = [word_tokenize(self.stripPunct(i)) for i in sent]
            nGramList.append(tmpList)
        return nGramList


if __name__ == '__main__':
    ob = STJparser('ex2.pdf')
    print(ob.ngrams)
