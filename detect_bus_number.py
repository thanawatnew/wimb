import numpy as np
import cv2
import os
import subprocess
path=os.path.abspath('.')
is_ocr=True
file_type=".jpg"
is_debug=True
def detect_bus_number(path,file_name,file_type):
	img = cv2.imread(path+'/images_haar/'+file_name+file_type,0)
	img2 = cv2.imread(path+'/images_haar/'+file_name+file_type,1)
	if is_debug: print path+'/images_haar/'+file_name+file_type
	
	#equ = cv2.equalizeHist(img)
    #res = np.hstack((img,equ)) #stacking images side-by-side
	
	#image_name="test.jpg"#288_20160217_162343_result_12.jpg"#262_20160115_172655_result_5.jpg"#307_20160104_172033.jpg"
	try: color=img.copy()
	except:
		if is_debug: print 'color image copy error'
		return None
	#img = cv2.Canny(img,100,200)
	img=img[0:img.shape[0]/2,0:img.shape[1]]
	ret2,img = cv2.threshold(img,150,255,cv2.THRESH_BINARY)#+cv2.THRESH_OTSU)
	#img2=np.invert(img)
	#cv2.imshow("threshold",img)
	contour,hier = cv2.findContours(img.copy(),cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
	screenCnt = None
	count_file_saved=0
	for c in contour:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if cv2.contourArea(c)/img.size*100 > 1:#len(approx) == 4 and 	
			count_file_saved+=1
			screenCnt = approx
			cv2.drawContours(color, [screenCnt], -1, (0, 255, 0), 3)
			y=0
			x,y,w,h = cv2.boundingRect(c)
			if is_debug: print x,y,w,h
			# break
			roi = img[y:y+h,x:x+w]
			cv2.imwrite(path+'/images_number/'+file_name+'_result_number_'+str(count_file_saved)+file_type, roi);
			if is_ocr: subprocess.call(["tesseract",path+'/images_number/'+file_name+'_result_number_'+str(count_file_saved)+file_type,path+'/text_number/'+file_name+'_result_number_'+str(count_file_saved),'-psm','7','digits','nobatch'],stdout=open(os.devnull, 'wb'),stderr=subprocess.STDOUT)
	cv2.imwrite(path+'/images_number/'+file_name+file_type,img)
	if is_debug: print 'amount of contour in this picture: '+str(len(contour))
	return img

def detect_bus_number_group():
	count=0
	for file_name_with_extension in os.listdir(path+'/images_haar/')[count:]:
		count+=1
		if is_debug: print 'progress = '+str(count)+'/'+str(len(os.listdir(path+'/images_haar/')))+' '+str(count*100.0/len(os.listdir(path+'/images_haar/')))
		file_name,file_type=file_name_with_extension.split('.')[0],'.'+file_name_with_extension.split('.')[1]
		if is_debug: print 'file name = '+file_name+', file_type = '+file_type
		
		# cv2.drawContours(color, contour, -1, (0, 255, 0), 3)
		detect_bus_number(path,file_name,file_type)

	#"""

