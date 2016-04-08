"""
find cam detail from bmatraffic
>>> len(get_cam_detail()) > 200
True
"""

import urllib2
import json
import re
from bs4 import BeautifulSoup
is_is_debug=False
def get_cam_detail():
	website_url = "http://www.bmatraffic.com"
	web = urllib2.urlopen(website_url)
	pattern = re.compile('var locations = (.*?);')

	soup = BeautifulSoup(web.read(), "lxml")
	scripts = soup.find_all('script')

	data  = soup.find_all("script")[32].string

	a=data.index("locations") #find variable locations from bmatraffic

	locations_string=data[a+len("locations = [ \r\n"):data.index("newsdata")] 
	locations=locations_string.split(']')
	locations.pop()
	locations.pop()
	cam_id=[]

	for i in locations:
		if is_is_debug: print i
		c=[]
		for count,l in enumerate(i.split("'")):
			if is_is_debug: print 'count=',str(count)
			if count in xrange(1,11+1,2): c.append(l)
			if count==10: 
				c.append(l.split(',')[1])
				c.append(l.split(',')[2])
			if is_is_debug: print l
			if is_is_debug: print '-------'
		cam_id.append(c)
		if is_is_debug: print c
		if is_is_debug: raw_input()
		if is_is_debug: print '======================='


	f=open('data.json','w')
	f.write('var locations='+"\n")
	f.write('{'+"\n")


	is_first_in_file=True
	for i in cam_id:
		if not is_first_in_file: f.write(',')
		f.write('"'+str(i[0])+'"'+":\n")
		is_first_in_file=False
		f.write('[')
		for count,j in enumerate(i):
			if count!=0: f.write(',')
			if count in [5,6]: f.write(str(j)+"\n")
			else: 
				try: f.write("'"+str(j)+"'\n")
				except: f.write("'"+j.encode('utf8')+"'\n")
			first=False
		f.write(',{}]')

	f.write("\n"+'};')
	f.close()
	return cam_id
