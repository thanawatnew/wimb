execfile('get_bus_detail_website_to_dict.py')

f=open('result_bus_number_110416.csv','r')
content=f.read()
f.close()
for c in content.split('\n'):
 try: d[c.split(',')[0]].append(str(float(c.split(',')[1])))
 except: continue
 d[c.split(',')[0]].append(str(float(c.split(',')[2])))
f=open('result_110416.csv','r')
content=f.read()
f.close()
f=open('bus_id_siamtraffic.csv','r')
content=f.read().split('\n')
f.close()
id_web_list =[[i for i in content[0].split(',')],[j.strip() for j in content[1].split(',')]]
for i,id_name in enumerate(id_web_list[1]):
 try:  d[id_web_list[0][i].strip()].append(id_name)
 except: pass

 
 """
 f=open('bus_station.js','w')
# TODO: convert from dict with id:bus_no_set|lat|long|station_id_siamtraffic
# to
# id|station_id_siamtraffic|lat|lng|bus_no_set
f.write('var bus_station = ')
f.write('[')
for count,key in enumerate(d.keys()):
	if count>0: f.write(',')
	f.write('[')
	f.write('"'+key+'"') # id
	f.write(',')
	try: f.write(d[key][3]) #station_id_siamtraffic, don't need to add double quote because they're added already.
	except: f.write(d[key][1])
	f.write(',')
	try:
		f.write(d[key][1]) #lat	
		f.write(',')
		f.write(d[key][2]) #long	
		f.write(',')
	except: f.write('0,0,')
	#bus_no_set
	f.write('[')
	for count,i in enumerate(d[key][0]):
		if count>0: f.write(',')
		try: f.write('"'+i.encode('utf8')+'"')
		except: f.write('"'+i+'"')
	f.write(']')
	f.write(']')

f.write(']')
f.close()
#"""

bus_station_list = []
# id|station_id_siamtraffic|lat|lng|bus_no_set
for count,key in enumerate(d.keys()):
	try: station_id_siamtraffic=d[key][3] #station_id_siamtraffic, don't need to add double quote because they're added already.
	except: station_id_siamtraffic=d[key][1]
	try:
		lat = d[key][1]	
		long = d[key][2]	
	except: lat,long = 0,0
	#bus_no_set
	bus_no_set = []
	for count,i in enumerate(d[key][0]):
		try: bus_no_set_each = '"'+i.encode('utf8')+'"'
		except: bus_no_set_each = '"'+i+'"'
		bus_no_set.append(bus_no_set_each)
	bus_station_list.append([key,station_id_siamtraffic,lat,long,bus_no_set])
	


f=open('bus_station_list.py','w')
f.write('bus_station_list = ')
f.write(str(bus_station_list))
f.close()