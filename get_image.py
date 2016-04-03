import numpy as np
import cv2



import urllib2
import time
import get_cam_detail
import os
is_debug=True

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

		if is_debug: print "==================================================================================="
	return True

