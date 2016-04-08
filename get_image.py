import numpy as np
import cv2



import urllib2
import time
import get_cam_detail
import os
import detect_bus_haar
import subprocess
is_debug=True
is_ocr=True
def send_response(url,cookies):
	"""
	>>> len(send_response) > 30
	True
	"""
	request = urllib2.Request(url)
	request.add_header("Cookie", cookies)
	opener=urllib2
	opener=urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
	user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
	opener.addheaders = [('User-agent', user_agent)]
	sock=opener.open(request)
	content=sock.read()
	sock.close()
	return content
def get_cookie(url):
	"""
	>>> len(get_cookie(url)) > 50
	True
	"""
	request = urllib2.Request(url)
	sock=urllib2.urlopen(request)
	cookies=sock.info()['Set-Cookie']
	content=sock.read()
	sock.close()
	return cookies
	


url="http://www.bmatraffic.com/"
def get_pictures(cookies):
	url="http://www.bmatraffic.com/"
	path=os.path.abspath('.')

	list_cam=get_cam_detail.get_cam_detail()
	list_cam_id=[cam[0] for cam in list_cam]
	
	sessionID=cookies.split("=")[1]
	for id in list_cam_id:
		id=str(id)		
		try: send_response(url+"PlayVideo.aspx?ID="+id,cookies)
		except: 
			is_working=False
			while not is_working:
				try: 
					cookies=get_cookie(url)
					is_working=True
				except: pass
			send_response(url+"PlayVideo.aspx?ID="+id,cookies)
		try: content=send_response(url+"show.aspx?image="+id,cookies)
		except: 
			is_working=False
			while not is_working:
				try: 
					cookies=get_cookie(url)
					is_working=True
				except: pass
			content=send_response(url+"show.aspx?image="+id,cookies)
		
		timestr = time.strftime("%Y%m%d_%H%M%S")
		f=open(path+'/images/'+id+'_'+timestr+'.jpg','wb')
		f.write(content)
		f.close()
		file_name= id+'_'+timestr#+'.jpg'
		cascade = cv2.CascadeClassifier(path+"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")
		rects=detect_bus_haar.detect_bus_haar(path,file_name,'.jpg',False,cascade)

		if is_debug: print "==================================================================================="
		if is_ocr: 
			output_process = subprocess.Popen(["/bin/grep","-r",'.','text_number'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			outputs = output_process.stdout.read().split('\n')
			f=open('buses.json','w')
			f.write('{'+"\n")
			is_first =True
			for output in outputs:
				try: 
					o=output.split('/')[1].split(':')
					if not is_first: f.write(',')
					else: is_first = False
				except:
					if is_debug: print output
					continue
				bus_detail = o[0].split('.')[0].split('_')
				bus_result = o[1]
				
				f.write('"'+str(bus_detail[1])+'_'+str(bus_detail[2])+'_'+str(bus_detail[3])+'_'+str(bus_detail[4])+'":'+"\n")
				f.write("[")
				for i in [0,1,2,4,7]:
					try: 
						f.write('"'+str(bus_detail[i])+'"')
						f.write(',')
					except: pass
				f.write('"'+str(bus_result[0])+'"')
				f.write("]\n")
			f.write('}'+"\n")
			f.close()
	return True

