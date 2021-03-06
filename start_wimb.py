"""
work every five minutes, after that, rename the picture's folder name with minute
"""
import sched, time
import os
import get_image
import shutil
import subprocess
is_debug = True
is_ocr = True
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
	'images_bgs',
	'images_bgs_mask',
	#'images_bgs_result',
	'images_color',
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

url="http://www.bmatraffic.com/"
if is_debug: print 'current absolute path of the project(path) is '+os.path.abspath('.')
path=os.path.abspath('.')

while True:
	check_init_files_and_folders()
	starttime=time.time()
	#get_image.get_pictures()
	while time.time()-starttime<15*60: # less than five minutes, just keep taking and processing pictures
		get_image.get_pictures(get_image.get_cookie(url)) #set first parameter in seconds
		time.sleep(5)
	directory_list=[
	'images',
	#'images_haar',
	#'images_haar_result',
	#'images_number',
	#'text_number',
	]
	timestr = time.strftime("%Y%m%d_%H%M%S")
	for directory_name in directory_list: 
		shutil.move(directory_name,"images_old/"+directory_name+'_'+timestr)
	directory_list=[
	'images_bgs',
	'images_bgs_mask',
	#'images_bgs_result',
	'images_color',
	'images_haar',
	'images_haar_result',
	'images_number',
	'images_number_result',
	'text_number',
	]
	for directory_name in directory_list: 
		shutil.rmtree(directory_name)
	shutil.move('data.json',"images_old/"+'data'+'_'+timestr+'.json')
	shutil.move('buses.json',"images_old/"+'buses'+'_'+timestr+'.json')
		
#""" #for a multiple line comment
