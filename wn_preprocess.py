# coding=utf-8 
import wn_co
import words_seg
import datetime
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
		
''' words network的所有预处理集成，涉及到python通过命令行调用java类的方法
'''
def generate_wn(input_file, output_file):
	''' inputs: num 文档数量
	'''
	words_seg.seg(input_file)
	
	comd = 'java -Xmx10g PrepareInput wn_inputs/words_network_inputs_test.txt wn_inputs/ words_network_inputs_test 10'
	os.system(comd)
	print comd
	wn_co.process_bak(output_file)

if __name__ == '__main__':

    f1 =  "保监会"
    f2 =  "校园贷"
    f3 =  "银监会"
    f4 =  "证监会"
                
    ff = f4

    input_file = ff+"-评论详情.jl"

    output_file = ff+"-评论详情-co.txt"
    starttime = datetime.datetime.now()

    generate_wn(input_file, output_file)
    
    endtime = datetime.datetime.now()
    print 'running time:', (endtime - starttime).seconds
	





