# -*- coding: utf-8 -*-

import ngb
import sys   
reload(sys) 
sys.setdefaultencoding('utf-8')   

def build_ngrams(text_list, length=2):
	''' generate ngrams
		inputs: text_list, text list to build ngrams
				length, the length of each ngrams
	'''

	builder = ngb.NgramBuilder()
	counter = ngb.Counter()
	older_percent = 0
	for index, text in enumerate(text_list):
		percent = int(float(index)/len(text_list)*100)
		if percent % 10 == 0 and percent != older_percent:
			print int(float(index)/len(text_list)*100), '%', 'generating ngrams....'
			older_percent = int(float(index)/len(text_list)*100)
		ngrams = builder.find_ngrams_for_document(text, length=2)
		counter.add_ngram_list(ngrams)
	return counter

def cut_ngrams(text, length=2):
	''' generate ngrams
		inputs: text, text to build ngrams
				length, the length of each ngrams
	'''
	builder = ngb.NgramBuilder()
	ngrams = builder.find_ngrams_for_document(text, length=2)	
	return ngrams


if __name__ == '__main__':

	# text_list = []
	# with open("/Users/mac/data-and-code/data/original/2W_documents.txt") as f:
	# 	for line in f:
	# 		text_list.append(line.strip().decode('utf-8'))
	# ngram_count_dict = build_ngrams(text_list,2)
	

	# sorted_ngrams = sorted(ngram_count_dict.iteritems(), key = lambda asd:asd[1],reverse = True)
	# fw = file('ngrams_statistics.txt','w')
	# content = ''
	# for sn in sorted_ngrams:
	# 	content += sn[0]+'  '+str(sn[1])+'\n'
	# fw.write(content)
	# fw.close()
	# print 'over!!'

    text = '习近平在人民大会堂同沙特国王举行会谈'

    ngrams = cut_ngrams(text, 2)
    for ng in ngrams:
    	print ng
