"""
find cam detail from bmatraffic
>>> len(get_cam_detail()) > 200
True
"""
import get_bus_number_from_locations 
import urllib2
import json
import re
from bs4 import BeautifulSoup


is_get_bus_number_to_file_by_siamtraffic = False
is_debug=False
is_get_bus_number_to_file=False
if is_get_bus_number_to_file_by_siamtraffic:
	import bus_station_list
	import geopy
	import geopy.distance
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
		if is_debug: print i
		c=[]
		for count,l in enumerate(i.split("'")):
			if is_debug: print 'count=',str(count)
			if count in xrange(1,11+1,2): c.append(l)
			if count==10: 
				c.append(l.split(',')[1])
				c.append(l.split(',')[2])
			if is_debug: print l
			if is_debug: print '-------'
		cam_id.append(c)
		if is_debug: print c
		if is_debug: raw_input()
		if is_debug: print '======================='

		f=open('data.json','w')
		f.write('var locations='+"\n")
		f.write('{'+"\n")


		is_first_in_file=True
		for i in cam_id:
			if not is_first_in_file: f.write(',')
			f.write('"'+str(i[0])+'"'+":\n")
			is_first_in_file=False
			f.write('[')
			lat,long = i[5],i[6]
			for count,j in enumerate(i):
				if count!=0: f.write(',')
				if count in [5,6]: f.write(str(j)+"\n") # lat,long position on gps
				else: 
					try: f.write("'"+str(j)+"'\n")
					except: f.write("'"+j.encode('utf8')+"'\n")
				first=False
			f.write(',{}')
			if is_get_bus_number_to_file:
				f.write(',[')
				for i,content in enumerate(list(get_bus_number_from_locations.get_bus_number_from_locations(float(i[5]),float(i[6])))):
					if i>0: f.write(',"'+content+'"')
					else: f.write('"'+content+'"')
				f.write(']')
			
			if is_get_bus_number_to_file_by_siamtraffic:
				# TODO: add detect_nearest_bus_station function here
				#f.write(',')
				bus_station_list_to_file =  bus_station_list.bus_station_list
				#ccoordinate_list = [(11.6702634, 72.313323), (11.6723698, 78.114523), (31.67342698, 78.465323), (12.6702634, 72.313323), (12.67342698, 75.465323)]
				# id|station_id_siamtraffic|lat|lng|bus_no_set

				ccoordinate_list =  bus_station_list_to_file #[ bus_station_list_to_file[i] for i in  bus_station_list_to_file.keys()]
				coordinate = (lat,long)#(11.6723698, 78.114523)
				# the solution
				pts = [ [geopy.Point(p[2],p[3]),p] for p in ccoordinate_list ]
				onept = geopy.Point(coordinate[0],coordinate[1])
				alldist = [ (p[0],geopy.distance.distance(p[0], onept).km,p[1]) for p in pts ]
				nearest_point = min(alldist, key=lambda x: (x[1]))[2] # or you can sort in by distance with sorted function
				
				key = nearest_point[0]
				f.write('[')
				f.write('"'+str(key)+'"') # id
				f.write(',')
				if is_debug: 
					print 'nearest_point ='
					print nearest_point
				f.write(nearest_point[1]) #station_id_siamtraffic, don't need to add double quote because they're added already.
				f.write(',')
				
				f.write(str(nearest_point[2])) #lat	
				f.write(',')
				f.write(str(nearest_point[3])) #long	
				f.write(',')
				
				#bus_no_set
				f.write('[')
				for count,i in enumerate(nearest_point[4]):
					if count>0: f.write(',')
					try: f.write('"'+i.encode('utf8')+'"')
					except: f.write('"'+i+'"')
				f.write(']')
				f.write(']')
				
			f.write(']')

		f.write("\n"+'};')
		f.close()
	return cam_id
