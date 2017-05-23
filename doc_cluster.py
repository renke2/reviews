# -*- coding: utf-8 -*-

import sys  
import json
import datetime
from collections import defaultdict
from build_ngrams import cut_ngrams
from utils import cut_words, cut_words_noun 
reload(sys) 
sys.setdefaultencoding('utf-8')   


def find_doc_label(doc, words_cluster, isNgram):
	features = []
	if isNgram is True:
		features = cut_ngrams(doc)
	else:
		features = cut_words(doc.encode('utf-8'))
	
	doc_cluster_count = defaultdict(int)
	for fea in features:
		for k, v in words_cluster.iteritems():
			if fea in v:
				doc_cluster_count[k] += 1
	max_label = "other"
	max_count = 0
	for k, v in doc_cluster_count.iteritems():
		if v > max_count:
			max_count = v
			max_label = k

	return max_label

def documents_clustering(jl_file, words_cluster_file, isNgram):
	""" 根据特征聚类结果对文档聚类
		inputs: jl_file 原始文档集文件
		        words_cluster_file 特征（词）聚类结果
		        isNgram 是否为Ngram，是为True，否则为False
	"""
	documents = [json.loads(line.decode()) for line in open(jl_file)]
	words_cluster = {}
	with open(words_cluster_file) as f:
		words_cluster = json.loads(f.read())
	for doc in documents:
		content = doc.get("title","")+" "+doc.get("content","")
		label = find_doc_label(content, words_cluster, isNgram)
		doc["label"] = label
	#docs = [json.dumps(doc) for doc in documents]
	return documents

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

    jl_file = ff+"-评论详情.jl"
    words_cluster_file = "words_cluster_results/"+mm+"/"+ff+"-评论详情-results.txt"

    results = documents_clustering(jl_file, words_cluster_file, False)

    endtime = datetime.datetime.now()
    fw = file("doc_cluster_results/"+mm+"/"+ff+"-评论详情-文档聚类结果.txt", "w")
    fw.write(json.dumps(results))
    fw.close()
    print 'end time passed in seconds:', (endtime - starttime).seconds



