# coding=utf-8 
import re
import sys
import json
from utils import cut_words, cut_words_noun
reload(sys)
sys.setdefaultencoding('utf-8')

def seg(filename):
	'''读取jl文件，并切词
	'''

	#number为要计算的数据量
	fw = file("wn_inputs/words_network_inputs_test.txt", "w") 
	count = 0
	with open(filename) as f:
		for line in f:
			line_dict = json.loads(line)
			line = line_dict.get("text","").encode("utf-8")
			li_content = ""
			words_list = cut_words(line)
			count += len(words_list)
			words = " ".join(words_list)
			li_content += words+'\n'
			fw.writelines(li_content.encode("utf-8"))
	print 'computation over!!'
	print '词数:', count
	fw.close()
		
if __name__ == '__main__':
	seg()





