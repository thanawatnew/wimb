import cv2
import os
from subprocess import call
import subprocess
import detect_bus_number
import shutil
#from start_wimb import check_init_files_and_folders
path=os.path.abspath('.')
file_type='.jpg'
is_ocr=False
is_debug=True
#file_name = 'rgb_20160112_123002'
def detect(img,cascade):
	rects = cascade.detectMultiScale(img, 1.3, 4, cv2.CASCADE_SCALE_IMAGE, (24,24))

	if len(rects) == 0:
		return [], img
	rects[:, 2:] += rects[:, :2]
	return rects, img

def box(rects, img,img2,img3,img4,path,file_name,file_type,is_detect_bus_number):
	count=0
	img_original=img2
	if is_ocr: img_ocr_0=img3
	if is_ocr: img_ocr_1=img4
	if is_debug: print 'total amount = '+str(len(rects))
	for x1, y1, x2, y2 in rects:
		#tesseract scan.png scanned.txt
		count+=1
		if is_debug: print 'current picture = '+str(count)+'/'+str(len(rects))+', '+str(count*100.0/len(rects))+'%'
		size_x,size_y=round(abs(x2-x1)/2.0),round(abs(y2-y1)/2.0)
		crop_img=img_original[y1:y2,x1:x2]
		if is_ocr: crop_img_ocr_0=img_ocr_0[y1:size_y+y1,x1:x2]
		if is_ocr: crop_img_ocr_1=img_ocr_1[y1:size_y+y1,x1:x2]
		cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
		cv2.imwrite(path+'/images_haar/'+file_name+'_result_'+str(count)+file_type, crop_img)
		if is_detect_bus_number: 
			detect_bus_number.detect_bus_number(path,file_name+'_result_'+str(count),file_type)		
	if is_ocr: cv2.imwrite(path+'/ocr/'+file_name+'_ocr_0_'+str(count)+file_type, crop_img_ocr_0);
	if is_ocr: cv2.imwrite(path+'/ocr/'+file_name+'_ocr_1_'+str(count)+file_type, crop_img_ocr_1);
	if is_ocr: call(["tesseract",path+'/ocr/'+file_name+'_ocr_0_'+str(count)+file_type,path+'/ocr_text/'+file_name+'_ocr_0_'+str(count)],stdout=open(os.devnull, 'wb'),stderr=subprocess.STDOUT)
	if is_ocr: call(["tesseract",path+'/ocr/'+file_name+'_ocr_1_'+str(count)+file_type,path+'/ocr_text/'+file_name+'_ocr_1_'+str(count)],stdout=open(os.devnull, 'wb'),stderr=subprocess.STDOUT)
	
	if is_debug: print 'save to '+path+'/images_haar_result/'+file_name+'_result'+file_type
	cv2.imwrite(path+'/images_haar_result/'+file_name+'_result'+file_type, img);

#cap = cv2.VideoCapture(0)
#cap.set(3,400)
#cap.set(4,300)

"""
while(True):
	ret, img = cap.read()
	rects, img = detect(img)
	box(rects, img)
	cv2.imshow("frame", img)
	if(cv2.waitKey(1) & 0xFF == ord('q')):
	break
"""

#ret, img = cap.read()
def detect_bus_haar(path,file_name,file_type,is_ocr,cascade):
	 is_detect_bus_number = True
	 if file_type!='.jpg': return None
	 img = cv2.imread(path+'/images/'+file_name+file_type,cv2.IMREAD_COLOR)
	 if is_ocr: call([path+"/DetectText",path+'/images/'+file_name+file_type,path+'/ocr/'+file_name+'_preprocess_0'+file_type,"0"])
	 if is_ocr: call([path+"/DetectText",path+'/images/'+file_name+file_type,path+'/ocr/'+file_name+'_preprocess_1'+file_type,"1"])
	 img2 = cv2.imread(path+'/images/'+file_name+file_type,cv2.IMREAD_COLOR)
	 if is_ocr: img3 = cv2.imread(path+'/ocr/'+file_name+'_preprocess_0'+file_type,cv2.IMREAD_COLOR)
	 if is_ocr: img4 = cv2.imread(path+'/ocr/'+file_name+'_preprocess_1'+file_type,cv2.IMREAD_COLOR)
	 #print img
	 rects, img = detect(img,cascade)
	 if is_ocr: box(rects, img,img2,img3,img4,path,file_name,file_type,is_detect_bus_number)
	 else: box(rects, img,img2,None,None,path,file_name,file_type,is_detect_bus_number)
	 return rects
	 #cv2.imshow("frame", img)
def detect_bus_haar_group(path):
	count=0#0+215-1
	cascade = cv2.CascadeClassifier(path+"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"/models/cascade_bus_front_130_stages_1000_pos_3000_neg.xml")#"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"/models/cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml") #"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml")#/cascade_front_30_stage_wrong.xml")#cascade_30_stages_1000_pos_3000_neg.xml")#cascade_front_30_stage_wrong.xml") #"cascade_front_19_stage_1000_pos_3000_neg.xml")#"/cascade_front_30_stage_wrong.xml")
	for file_name_with_extension in os.listdir(path+'/images/')[count:]:
	 count+=1
	 if is_debug: print 'progress = '+str(count)+'/'+str(len(os.listdir(path+'/images/')))+' '+str(count*100.0/len(os.listdir(path+'/images/')))
	 if is_debug: print 'file name = '+file_name_with_extension
	 file_name,file_type=file_name_with_extension.split('.')[0],'.'+file_name_with_extension.split('.')[1]
	 detect_bus_haar(path,file_name,file_type,False,cascade)

def check_init_files_and_folders():
	"""
	check if file exist
	>>> check_init_files_and_folders() 
	file models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml existed: True
	file detect_bus_haar_group.py existed: True
	file get_cam_detail.py existed: True
	file get_image.py existed: True
	file start_wimb.py existed: True
	directory images existed: True
	directory images_haar existed: True
	directory images_number existed: True
	directory models existed: True
	"""
	#['cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml', 'cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml', 'color_detect_2.py', 'dedupe.py', 'detect_image_group_ku.py', 'detect_shape_5.py', 'get_cam_id_2.py', 'get_image_8.py', 'gui_hsv.py', 'knaps.py', 'knapsack_2.py', 'maps.html', 'program_detect_rectangle.zip', 'start_capture.py']
	file_list=[
	#'cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml', 
	'models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml', 
	#'color_detect_2.py', 
	#'dedupe.py', 
	'detect_bus_haar_group.py', 
	#'detect_shape_5.py', 
	'get_cam_detail.py', 
	'get_image.py', 
	#'gui_hsv.py', 
	#'knaps.py', 
	#'knapsack_2.py', 
	#'maps.html', 
	#'program_detect_rectangle.zip', 
	'start_wimb.py',
	'g.php',
	]
	directory_list=[
	'images',
	'images_haar',
	'images_haar_result',
	'images_number',
	'images_number_result',
	'models',
	'images_old',
	'text_number',
	]
	
	for file_name in file_list: print 'file '+file_name+' existed: '+str(os.path.isfile(file_name))
	for directory_name in directory_list: 
		print 'directory '+directory_name+' existed: '+str(os.path.isdir(directory_name))
		if not os.path.isdir(directory_name): 
			os.makedirs(directory_name)
		if "images" in directory_name: shutil.copy(path+'/g.php',path+'/'+directory_name+'/g.php')
		
if __name__ == "__main__":
	check_init_files_and_folders()
	detect_bus_haar_group(path)
