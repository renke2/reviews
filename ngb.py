# -*- coding: utf-8 -*-

import re
import nltk.tokenize
import sys   
import string
from collections import defaultdict
reload(sys) 
sys.setdefaultencoding('utf-8') 

__version__ = "0.2.0"


class Counter(dict):
    
    def add(self, other):
        for ngram in other.iterkeys():
            self[ngram] = self.get(ngram, 0) + other[ngram]

    def add_ngram_list(self, ngrams_list):
        ngram_count_dict = defaultdict(int)
        for ngram in ngrams_list:
            ngram_count_dict[ngram] += 1
        self.add(ngram_count_dict)
        

class NgramBuilder(object):
    
    def __init__(self, stopwords=None):
        self.stopwords = stopwords

    def find_ngrams_for_document(self, text, length=2):
        chinese = re.compile(u"[\u4e00-\u9fa5]")
        text_split = list(text.decode())
        start = 0
        end = 0
        ngrams = []
        for index,char in enumerate(text_split):
            if chinese.match(char):
                end += 1
                if index == (len(text_split)-1):
                    sub_text = ' '.join(text_split[start:end])
                    end += 1
                    sub_ngrams = self.find_ngrams(sub_text,2)
                    ngrams.extend(sub_ngrams)
            else:
                sub_text = ' '.join(text_split[start:end])
                end += 1
                sub_ngrams = self.find_ngrams(sub_text,2)
                ngrams.extend(sub_ngrams)
                start = end
        return ngrams

    def find_ngrams(self, text, length):
        ngrams = []
        num_unigrams, unigrams = self.split_into_unigrams(text)
        for i in xrange(num_unigrams):
            if (num_unigrams <= i + length - 1):
                break
            unigram_group = unigrams[i:i + length]
            if not self.ngram_is_filtered(unigram_group):
                ngram = ''.join(unigram_group)
                ngrams.append(ngram)
        return ngrams
    
    def split_into_unigrams(self, text):
        unigrams = []
        for token in text.split():
            unigrams.append(token.strip())
        return len(unigrams), unigrams
    

    def ngram_starts_or_ends_in_stopword(self, unigrams):
        if self.stopwords is None:
            return False
        return unigrams[0] in self.stopwords or unigrams[-1] in self.stopwords

    def ngram_is_filtered(self, unigrams):
        return self.ngram_starts_or_ends_in_stopword(unigrams)


stopwords = set([
    "a",
    "all",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "do",
    "for",
    "from",
    "had",
    "has",
    "have",
    "he",
    "his",
    "if",
    "in",
    "is",
    "it",
    "its",
    "it's",
    "my",
    "no",
    "not",
    "of",
    "on",
    "or",
    "our",
    "so",
    "that",
    "the",
    "their",
    "these",
    "they",
    "this",
    "to",
    "us",
    "was",
    "we",
    "were",
    "when",
    "where",
    "which",
    "who",
    "with",
    "would",
    "you",
])
