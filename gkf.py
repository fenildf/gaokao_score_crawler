import urllib.request
import re
import pickle
from bs4 import BeautifulSoup 

url = 'http://kaoshi.edu.sina.com.cn/collegedb/collegebang.php?majorname=&collegename=&provid=0&wl=0&syear=2004&_action=college_major_score&page=1&dpc=1'

for provid in range(0,32):
	url = url.replace('provid='+str(provid)+'&','provid='+str(provid+1)+'&')
	for wlid in range(0,3):
		url = url.replace('wl='+str(wlid)+'&','wl='+str(wlid+1)+'&')
		for syear in range(2004,2012):
			url = url.replace('syear='+str(syear)+'&','syear='+str(syear+1)+'&')
			print('====================')
			print('REQUEST_URL : '+url)
			print('provid:'+str(provid+1)+' wlid:'+str(wlid+1)+' syear:'+str(syear+1))
			print('====================')
			f = urllib.request.urlopen(url)
			soup = BeautifulSoup(f)
			totalPagesNum =0 
			tagZuiMoYe = soup.find(text='最末页 ')
			if(tagZuiMoYe == None):
				print('***没有数据***')
				continue
			totalPagesTag = tagZuiMoYe.findParent()
			pattern = re.compile(r'page=\d+')
			match = pattern.search(str(totalPagesTag))
			if match:
				strMatch = match.group()
				totalPagesNum = strMatch[5:len(strMatch)]
			url = url.replace('page='+str(1)+'&','page='+str(0)+'&')
			for i in range(0,int(totalPagesNum)):
				url = url.replace('page='+str(i)+'&','page='+str(i+1)+'&')
				print('====================')
				print('REQUEST_URL : '+url)
				print('PAGE : '+str(i+1)+'/'+str(totalPagesNum))
				print('====================')
				f = urllib.request.urlopen(url)
				soup = BeautifulSoup(f)
				tbody = soup.findAll('tbody',id='college_score_bang')
				for tb in tbody:
					for tr in tb.findChildren(recursive=False):
						print(str(i)+':',end='')
						with open('/Users/lianghongyun/Codes/python/adata3','a') as dataFile:
							dataFile.write(str(i)+':')
							for td in tr.findChildren(recursive=False):
								print(td.getText(),end='\t')
								dataFile.write(td.getText()+'\t')
							print()
							dataFile.write('\n')
				dataFile.close()
			url = url.replace('page='+str(totalPagesNum)+'&','page='+str(0)+'&')
		url = url.replace('syear='+str(2012)+'&','syear='+str(2004)+'&')
	url = url.replace('wl='+str(3)+'&','wl='+str(0)+'&')



