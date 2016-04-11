#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import re
#from urllib.request import urlopen, Request
import urllib2
import lxml
from lxml import html
import random
import json
is_debug = False#True
def get_bus_number_from_locations(lat,lng):
	#apikey='AIzaSyA_9End5x0EbeTY6XvA_dcmma8hXO-kuFc'
	apikey='AIzaSyC11ZMMk_Nk1lxbN-Oe8KBCsFj3INI63Uo'
	#lat,lng=13.771545, 100.505225 #13.7620205,100.5052676
	if is_debug: 
		print 'lat,long ='
		print lat,lng
		raw_input()
	places = urllib2.urlopen(
		'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' +
		'key=%s&location=%f,%f' % (apikey, lat, lng) +
		'&rankby=distance&language=th-TH&types=bus_station')
	places = json.load(places)
	print places
	buses_result=set()
	if places['status'] == 'OK':
		count = 0
		for result in places['results']:
			if count>1: break
			placeid = result['place_id']
			detail = urllib2.urlopen(
				'https://maps.googleapis.com/maps/api/place/details/' +
				'json?key=%s&placeid=%s' % (apikey, placeid) +
				'&language=th-TH')
			detail = json.load(detail)
			station = detail['result']['name']
			loc = detail['result']['geometry']['location']
			#buspage = get_webpage(detail['result']['url'])
			buspage = urllib2.urlopen(detail['result']['url']).read()
			buses = re.findall('bus.png\",0,\[15,15\],null,0\]\]\]\],\[5,\[\"(?:.{,4})\"',buspage)
			for bus in [i.split('"')[-2] for i in buses]:
				buses_result.add(bus)
			count+=1
			if is_debug: print buses_result
			#tree = lxml.html.document_fromstring(buspage)
			#bus_elm = tree.xpath("/html/body/div[1]/div/div[4]/div[4]/div/div/div[2]/div/div[2]/div[1]/div[2]/div/div/div[2]/div/table/tr/td")[0]
			#buses = list(filter(lambda s: len(s.strip()) > 0,
			#                    bus_elm.text_content().strip().split()))
			#print (station, float(loc['lat']), float(loc['lat']), buses)
	return list(buses_result)
