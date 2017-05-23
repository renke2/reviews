# coding=utf-8 
import jieba
import re
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def process_bak(filename):
	'''合并结点和邻接点文件
		inputs 文档数量
	'''
	fw = file(filename, "w") 
	words = []
	with open("wn_inputs/words_network_inputs_test.words") as f1:	
		for line1 in f1:
			words.append(line1.strip())
	adjacent = []
	with open("wn_inputs/words_network_inputs_test.adjacent") as f2:	
		t = 0	
		for line2 in f2:
			#print type(f)
			if t == 0:
				t += 1
				continue
			adjacent.append(line2.strip())
			t += 1
	co = []
	h = 0
	for w in words:
		if len(w) < 4:
			h += 1
		else:
			co = w+' '+adjacent[h]
			fw.write(co+'\n')
			h += 1

	fw.close()
		

if __name__ == '__main__':
	process_bak()





