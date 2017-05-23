# -*- coding: utf-8 -*-

import sys  
import json
import datetime
from collections import defaultdict
from utils import cut_words, cut_words_noun 
reload(sys) 
sys.setdefaultencoding('utf-8')
    
class DocCluster:
    def __init__(self):
        self.index = dict()

    def add(self, clus_id, content):
        if clus_id in self.index:
            self.index[clus_id].append(content)
        else:
            d = []
            d.append(content)
            self.index[clus_id] = d

def view_docs_cluster(documents_cluster_file, features_file):
    """ 文档聚类
		inputs: documents_cluster_file 文档聚类结果文件
    """
    documents = []

    features = {}

    with open(documents_cluster_file) as f:
        documents = json.loads(f.read())

    with open(features_file) as f:
        features = json.loads(f.read())

    docCluster = DocCluster()
    for doc in documents:
        if len(doc.get("content","")) < 11:
            print 'filtered:', doc.get("content","")
            continue
        docCluster.add(doc.get("label"), doc.get("content",""))

    index = docCluster.index
    fw_content = ""
    for k, v in index.iteritems():
        fw_content += k + ':  ('+' '.join(features.get(k,list('')))+')\n'
        for d in v:
            fw_content += '      ' + d + '\n'
        fw_content += '\n\n'

    return fw_content

if __name__ == '__main__':

    f1 =  "保监会"
    f2 =  "校园贷"
    f3 =  "银监会"
    f4 =  "证监会"

    m1 = "tfidf_kmeans"
    m2 = "ngram_kmeans"
    m3 = "ncut_nmf"
    m4 = "wntm_kmeans"
                
    f = f1
    mm = m2

    documents_cluster_file = "doc_cluster_results/"+mm+"/"+f+"-评论详情-文档聚类结果.txt"
    features_file = "extracted_features/"+mm+"/"+f+"-评论详情-results.txt"

    fw_content = view_docs_cluster(documents_cluster_file, features_file)
    fw = file("doc_cluster_results/"+mm+"/view-"+f+"-评论详情-文档聚类结果.txt", "w")
    fw.write(fw_content)
    fw.close()




