"""
work every five minutes, after that, rename the picture's folder name with minute
"""
import sched, time
import os
import get_image
import shutil

is_debug = True
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
	'models',
	'images_old',
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
	s=sched.scheduler(time.time,time.sleep)
	starttime=time.time()
	#get_image.get_pictures()
	while time.time()-starttime<15*60: # less than five minutes, just keep taking and processing pictures
		s.enter(5,1,get_image.get_pictures(get_image.get_cookie(url)),()) #set first parameter in seconds
		try: s.run()
		except: pass
	directory_list=[
	'images',
	'images_haar',
	'images_haar_result',
	'images_number',]
	timestr = time.strftime("%Y%m%d_%H%M%S")
	for directory_name in directory_list: 
		shutil.move(directory_name,"images_old/"+directory_name+'_'+timestr)
		
#""" #for a multiple line comment
