# coding:utf-8
import time
import chardet
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

'''预处理文件，生成jl文件
'''
#-*- coding: utf8 -*-
import xlrd

def readExcel(fname):
	bk = xlrd.open_workbook(fname)
	shxrange = range(bk.nsheets)
	try:
		sh = bk.sheet_by_name("Sheet1")
	except:
		print "no sheet in %s named Sheet1" % fname
	#获取行数
	nrows = sh.nrows
	#获取列数
	ncols = sh.ncols
	print "nrows %d, ncols %d" % (nrows,ncols)
	#获取第一行第一列数据 
	cell_value = sh.cell_value(1,1)
	#print cell_value	  
	row_list = []
	#获取各行数据
	for i in range(1,nrows):
		row_data = sh.row_values(i)
		row_list.append(row_data)
	return row_list

def generate_jl_file(docs, fname, cluster_num):
	fw = file(fname, "w")
	file_content = '{"cluster_num":'+str(cluster_num)+'}\n'
	fw.writelines(file_content)
	i=0
	for line in docs:
		if i < 1:
			i += 1
		else: 
			#print line
			weibo = {}
			id = i	
			content = str(line[0])
			try:
				t = float(line[2])
			except ValueError:
				continue
			t = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(t))
			# 将其转换为时间数组  
			timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")  
			# 转换为时间戳  
			timestamp = int(time.mktime(timeArray))  

			weibo["content"] = content.decode("utf-8")
			weibo["text"] = content.decode("utf-8")
			# if len(content) < 11:
			# 	print 'filtered:', content
			# 	continue
			weibo["news_id"] = "weibo"
			weibo["id"] = id
			weibo["timestamp"] = timestamp
			i += 1
			fw.write(json.dumps(weibo)+'\n')
	fw.close()
	print 'over!'
	
if __name__ == '__main__':

	fw = "证监会-评论详情.jl"
	docs = readExcel("证监会-评论详情.xlsx")
	generate_jl_file(docs, fw, 90)







