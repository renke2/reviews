# -*- coding: utf-8 -*-

import sys  
import json
import math
import datetime
from collections import defaultdict
from gensim import corpora, models, similarities
from utils import cut_words, cut_words_noun 
reload(sys) 
sys.setdefaultencoding('utf-8')   

class DocCluster:  #记录词的tfidf值
    def __init__(self):
        self.index = dict()

    def add(self, clus_id, input):
        if clus_id in self.index:
            self.index[clus_id].append(input)
        else:
            d = []
            d.append(input)
            self.index[clus_id] = d

def tfidf_v2(inputs, topk):
    '''
    计算每条文本中每个词的tfidf，对每个词在各个文本中tfidf加和除以出现的文本次数作为该词的权值。
    输入数据：
        评论数据inputs，示例：[{'_id':评论id,'news_id':新闻id,'content':评论内容}]
        topk，每个类提取的主题词数量，根据tfidf值由大到小提取
    输出数据：
        result_tfidf[:topk]:前topk词及tfidf值的列表,示例：[词]
    '''
    total_document_count = len(inputs)
    tfidf_dict = {}#词在各个文本中的tfidf之和
    count_dict = {}#词出现的文本数
    count = 0#记录每类下词频总数

    all_words = []
    for input in inputs:
        # word_count = freq_word(input)
        text = input.get("content","").encode()
        words = cut_words_noun(text)
        input['cut_noun_words'] = words
        all_words.append(words)
    dictionary = corpora.Dictionary(all_words)  #获得set集
    corpus =[]
    for word in all_words:
        corpus.append(dictionary.doc2bow(word))  #转换成索引+数量，生成词向量
    #计算各个文档中的词的TFIDF
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    corpus_tfidf_list = [i for i in corpus_tfidf]

    for docid, doc in enumerate(corpus_tfidf_list):
        for word in doc:
            word_only = dictionary[word[0]]
            try:
                tfidf_dict[word_only] += word[1]
            except:
                tfidf_dict[word_only] = word[1]

    for k, v in tfidf_dict.iteritems():
        tfidf_dict[k] =  float(tfidf_dict[k])/float(len(inputs))

    sorted_tfidf = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1], reverse = True)
    result_tfidf = [k for k, v in sorted_tfidf]

    # topk = int(math.ceil(float(len(result_tfidf))*0.1)) #取前10%的tfidf词

    if topk > len(result_tfidf):
        topk = len(result_tfidf)

    return result_tfidf[:topk]
    

def extract_features(documents_cluster_file, topk):
    """ 为类簇提取关键词，每个类提取tfidf值排名前10的词语作为该类的主题词
		inputs: documents_cluster_file 文档聚类结果文件
                topk，每个类提取的主题词数量，根据tfidf值由大到小提取
    """
    documents = []
    with open(documents_cluster_file) as f:
        documents = json.loads(f.read())

    docCluster = DocCluster()
    for doc in documents:
        docCluster.add(doc.get("label"), doc)

    index = docCluster.index
    cluster_feature = {}
    for label, contents in index.iteritems():
        features = tfidf_v2(contents, topk)
        if len(features) > 0:
            print '特征数量：', len(features)
            cluster_feature[label] = features

    return json.dumps(cluster_feature) 


if __name__ == '__main__':

    f1 =  "保监会"
    f2 =  "校园贷"
    f3 =  "银监会"
    f4 =  "证监会"

    m1 = "tfidf_kmeans"
    m2 = "ngram_kmeans"
    m3 = "ncut_nmf"
    m4 = "wntm_kmeans"
                
    ff = f1
    mm = m4

    starttime = datetime.datetime.now()

    documents_cluster_file = "doc_cluster_results/"+mm+"/"+ff+"-评论详情-文档聚类结果.txt"

    results = extract_features(documents_cluster_file, 10)

    endtime = datetime.datetime.now()
    fw = file("extracted_features/"+mm+"/"+ff+"-评论详情-results.txt", "w")
    fw.write(results)
    fw.close()
    print 'end time passed in seconds:', (endtime - starttime).seconds


