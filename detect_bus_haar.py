import cv2
import os
from subprocess import call
import subprocess
import detect_bus_number,detect_bus_color
import shutil
#from start_wimb import check_init_files_and_folders
path=os.path.abspath('.')
file_type='.jpg'
is_ocr=False
is_debug=True
is_bgs = True
is_color_check = True
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
		if is_bgs and os.path.isfile(path+'/models/images_bgs_model_median/'+file_name.split('_')[0]+'_model_median'+file_type):
			call([path+'/get_DPMeanBGS_mask',path+'/images/'+file_name+file_type,path+'/models/images_bgs_model_median/'+file_name.split('_')[0]+'_model_median'+file_type,path+'/images_bgs_mask/'+file_name+'_bgs_mask'+file_type],stdout=open(os.devnull, 'wb'),stderr=subprocess.STDOUT)
			img_bgs_mask = cv2.imread(path+'/images_bgs_mask/'+file_name+'_bgs_mask'+file_type,0)
			ret,img_bgs_mask_2 = cv2.threshold(img_bgs_mask,200,255,cv2.THRESH_BINARY)
			img_bgs_mask_3 = img_bgs_mask_2[y1:y2,x1:x2]
			isWhite=False
			for i in xrange(len(img_bgs_mask_3)):
				for j in xrange(len(img_bgs_mask_3[i])):
					if img_bgs_mask_3[i][j]==255:
						isWhite=True
						break
				if isWhite: break
			if not isWhite: 
				continue # bgs unable to detect the moving object, so it skipped this cropped box 
		if is_color_check:
			if not detect_bus_color.detect_bus_color(img[y1:y2,x1:x2],file_name+'_result_'+str(count)+file_type): continue
				
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
	cascade = cv2.CascadeClassifier(path+"/models/wimb_cascade_26_stage_front_1000_pos_3000_net_wrong.xml")#cascade_wimb_bus_front_20_stages_1000_pos_3000_neg_wrong.xml")#cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml")#cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml")#cascade_bus_front_175_stages_1000_pos_3000_neg.xml")#"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"/models/cascade_bus_front_130_stages_1000_pos_3000_neg.xml")#"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"/models/cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml") #"/models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml")#"cascade_wimb_bus_front_100_stages_1000_pos_3000_neg.xml")#/cascade_front_30_stage_wrong.xml")#cascade_30_stages_1000_pos_3000_neg.xml")#cascade_front_30_stage_wrong.xml") #"cascade_front_19_stage_1000_pos_3000_neg.xml")#"/cascade_front_30_stage_wrong.xml")
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
	'images_bgs_mask',
	'images_color',
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
		try: bus_result = o[1]
		except: bus_result = ''
		
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
