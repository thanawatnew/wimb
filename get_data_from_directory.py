import os,json
import bus_station_list
import geopy
import geopy.distance
path = os.path.abspath('.')


def first_and_second_smallest(numbers):
	min_1, min_2 = float('inf'), float('inf')
	data_min_1,data_min_2=None,None
	for x in numbers:
		if x[1] < min_1: #x <= m1:
			min_1, min_2 = x[1], min_1
			data_min_1, data_min_2 = x, data_min_1
		elif x[1] < min_2:
			min_2 = x[1]
			data_min_2 = x
	return [data_min_1,data_min_2]

is_debug = True
count=0#0+215-1
for file_name_with_extension in os.listdir(path+'/images_old/data/')[count:]:
	#read data from js
	if is_debug: 
		print 'count = ' +str(count)+', file name = '+file_name_with_extension
	f=open(path+'/images_old/data/'+file_name_with_extension,'r')
	content=f.read()
	f.close()
	content=content.split('\n')
	content=content[1:]
	#content[-1]='}'
	#content[0]='{'
	if count==0: data=json.loads(''.join(content).replace("'",'"').replace(';',''))
	else:
		tmp = json.loads(''.join(content).replace("'",'"').replace(';',''))
		for key in tmp.keys():
			if not key in data: data[key]=tmp[key]
	count+=1
"""	
f=open('result_data_aggregate.py','w')
f.write('#!/usr/bin/env python\n')
f.write('# -*- coding: utf-8 -*-\n')
f.write('data = \n')
f.write(str(data))
f.close()
"""
is_first_in_file = True
is_get_bus_number_to_file = False
is_get_bus_number_to_file_by_siamtraffic= True
f=open('result_data_aggregate_bus_station_siamtraffic.js','w')
f.write('var locations = \n')
f.write('{\n')
for count,key in enumerate(data.keys()):
	print 'key = '+str(key)
	print 'count = '+str(count)+', total progress = '+str(float(count)/len(data.keys())*100.0)+' %'
	i=data[key]
	if not is_first_in_file: f.write(',')
	f.write('"'+str(i[0])+'"'+":\n")
	is_first_in_file=False
	f.write('[')
	lat,long = i[5],i[6]
	for count,j in enumerate(i): 
		if count==len(i)-1: break # last position got "{}" and become a problem
		if count!=0: f.write(',')
		if count in [5,6]: f.write(str(j)+"\n") # lat,long position on gps
		else: 
			try: f.write('"'+str(j)+'"\n')
			except: f.write('"'+j.encode('utf8')+'"\n')
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
		f.write(',')
		f.write('[')
		bus_station_list_to_file =  bus_station_list.bus_station_list
		#ccoordinate_list = [(11.6702634, 72.313323), (11.6723698, 78.114523), (31.67342698, 78.465323), (12.6702634, 72.313323), (12.67342698, 75.465323)]
		# id|station_id_siamtraffic|lat|lng|bus_no_set
		ccoordinate_list =  bus_station_list_to_file #[ bus_station_list_to_file[i] for i in  bus_station_list_to_file.keys()]
		coordinate = (lat,long)#(11.6723698, 78.114523)
		# the solution
		pts = [ [geopy.Point(p[2],p[3]),p] for p in ccoordinate_list ]
		onept = geopy.Point(coordinate[0],coordinate[1])
		alldist = [ (p[0],geopy.distance.distance(p[0], onept).km,p[1]) for p in pts ]
		#nearest_point = min(alldist, key=lambda x: (x[1]))[2] # or you can sort in by distance with sorted function
		nearest_points = first_and_second_smallest(alldist)#[2] 
		for count_nearest_point,nearest_point in enumerate(nearest_points):
			if count_nearest_point>0: f.write(',')
			nearest_point = nearest_point[2]
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
				try: f.write(i.encode('utf8')) #('"'+i.encode('utf8')+'"')
				except: f.write(i) #('"'+i+'"')
			f.write(']')
			f.write(']')
		f.write(']')
				
	f.write(']')

f.write("\n"+'}')
f.close()
