import cv2
import numpy as np
import os,sys
lower,upper = 0,1
def detect_bus_color(img,file_name_with_extension):
	#file_path='D:/mask_positive_front/mask_positive_front/12_20160106_174205_result_3_mask.jpg'
	path = os.path.abspath('.')
	#file_name_with_extension = sys.argv[1]
	file_type = '.jpg'
	color_dict = {
	'orange' : [(7,115,138),(12,217,182)],
	'yellow' : [(23,68,94),(43,136,247)],
	'blue' : [(102,57,96),(110,168,177)]
	}
	#frame = True, cv2.imread(path+'/images_haar/'+file_name_with_extension,1)
	frame = img 
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	for color_name in ['orange','yellow','blue']: #file_name in os.listdir('D:/mask_sample_mini/'):#'D:/mask_positive_front/mask_positive_front/'):
		print file_name_with_extension
		color = color_dict[color_name]
		#file_path=path+'/'+'images_color'+'/'+file_name_with_extension.split('.')[0]+'_'+color+file_type #'D:/mask_positive_front/mask_positive_front/'+file_name
		im = cv2.inRange(hsv, np.array(color[lower]), np.array(color[upper])) #mask
		cv2.imwrite(path+'/images_color/'+file_name_with_extension.split('.')[0]+"_"+color_name+".jpg",im)
		#im = cv2.imread(file_path,1)
		im = cv2.imread(path+'/images_color/'+file_name_with_extension.split('.')[0]+"_"+color_name+".jpg",1)
		gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
		blur=cv2.GaussianBlur(gray,(5,5),0)
		ret,binario=cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		
		kernel = np.ones((5,5),np.uint8)
		dilation = cv2.dilate(im,kernel,iterations = 1)
		#opening = cv2.morphologyEx(binario, cv2.MORPH_OPEN, kernel)
		#closing = cv2.morphologyEx(binario, cv2.MORPH_CLOSE, kernel)
		#gradient = cv2.morphologyEx(binario, cv2.MORPH_GRADIENT, kernel)
		#tophat = cv2.morphologyEx(binario, cv2.MORPH_TOPHAT, kernel)
		#blackhat = cv2.morphologyEx(binario, cv2.MORPH_BLACKHAT, kernel)
		
		bordes=cv2.Canny(dilation,100,100)
		contours,hierarchy = cv2.findContours(bordes,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
		
		#"""
		thresh = 1
		#rectList, weights = cv2.groupRectangles(contours, thresh)  # eps is optional
		rectangles=[]
		for cnt in contours:
			#cv2.imwrite(file_name.split('.')[0]+"_shape_contour.jpg",cnt)
			x,y,w,h = cv2.boundingRect(cnt)
			rectangles.append([x,y,w,h])
			rectangles.append([x,y,w,h])
			
			print w*h
			#if w*h<100: continue
			#cv2.rectangle(im,(x,y),(x+w,y+h),(200,0,0),2)
		#"""
		#cv2.imshow('img',im)
		#cv2.drawContours(im, contours, -1, (0,255,0), 3)
		rectList, weights = cv2.groupRectangles(rectangles, 1,1.175)
		print '----'
		for rect in rectList: 
			x,y,w,h=rect
			print w*h
			if w*h<1000: continue
			cv2.rectangle(im,(x,y),(x+w,y+h),(200,0,0),2)
		cv2.imwrite(path+'/images_color/'+file_name_with_extension.split('.')[0]+"_"+color_name+"_"+"_dilate.jpg",im)
		return True
	return False
