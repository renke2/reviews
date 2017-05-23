# coding=utf-8 
import re
import sys
import datetime
import math
import json
import numpy as np
import time
from utils import cut_words,cut_words_noun
reload(sys)
sys.setdefaultencoding('utf-8')

def coherence(set_i,set_j):
	'''writen by Nana
	'''
	inter = len(set_i & set_j)
	print len(set_i),inter,len(set_j)
	return np.log2((inter+math.pow(math.e,-12))/len(set_i))

def compute_coherence(original_docs, features_file):
	'''计算topic coherence
		inputs: 
	'''
	starttime = datetime.datetime.now()
	docseg = [] 
	#原始文档数据	
	for line in original_docs:
		lineseg = cut_words(line)
		docseg.append(lineseg)
	coherence = {}
	#要计算的词聚类结果所在的文件
	with open(features_file) as f2:	
		content = f2.read()
		wcr = json.loads(content)
		#wcr = eval(content) 
		for c in wcr:
			#topic coherence definition
			ws = wcr[c]
			word_doc = documents_set(ws,docseg)
			tocoh = 0 #topic coherence
			for m in range(1,len(ws)):
				for l in range(0,m):
					set_m = word_doc[ws[m]]
					set_l = word_doc[ws[l]]
					inter = len(set_m & set_l)
					if len(set_l)>0:
						tocoh += np.log((inter+math.pow(math.e,-12))/len(set_l))
			if len(ws)>1:
				tocoh = 2.0/(len(ws)*(len(ws)-1))*tocoh
			coherence[c] = tocoh
			print '已计算 ',c,tocoh

	midtime = datetime.datetime.now()
	print 'mid time passed in seconds:',(midtime - starttime).seconds

	coherence_sorted = sorted(coherence.iteritems(),key = lambda asd:asd[1],reverse = True)
	co_va = 0
	topic_coh = []
	for c in coherence.keys():
		co_va += coherence.get(c)
		topic_coh.append(coherence.get(c))
	average_coherence = co_va/float(len(coherence))
	fw_content = 'average coherence: '+str(average_coherence)+'\n'
	for clco in coherence_sorted:
		fw_content += str(clco) + ':\n'
		for w in wcr.get(clco[0]):
			fw_content += '      '+w+'\n'

	endtime = datetime.datetime.now()
	print 'end time passed in seconds:',(endtime - starttime).seconds
	return fw_content, topic_coh
		
def documents_set(words,docseg):
	'''计算词所属的文档集合
		inputs: word 词
				docseg 已经分好词的文档列表，list类型
	'''
	word_doc = {}
	for word in words:
		i = 0
		doc_list = []
		for d in docseg:
			if word in d:
				doc_list.append(i)
			i += 1
		word_doc[word] = set(doc_list)
	return word_doc


if __name__ == '__main__':

    f1 =  "保监会"
    f2 =  "校园贷"
    f3 =  "银监会"
    f4 =  "证监会"
                
    ff = f4

    original_docs_file = ff+"-评论详情.jl"
    original_docs = []
    with open(original_docs_file) as f:
    	for line in f:
    		doc = json.loads(line)
    		original_docs.append(doc.get("text","").encode('utf-8'))

	features_file = "extracted_features/tfidf_kmeans/"+ff+"-评论详情-results.txt"
	fw_content, topic_coh = compute_coherence(original_docs, features_file)

	fw = file("topic_coherence/tfidf_kmeans/"+ff+"-评论详情_topic_coherence.txt","w")
	fw.write(fw_content)
	fw.close()





