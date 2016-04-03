"""
work every five minutes, after that, rename the picture's folder name with minute
"""
import sched, time
import os

debug = True
def check_init_files_and_folders():
	"""
	check if file exist
	>>> check_init_files_and_folders() 
	file models/cascade_wimb_bus_front_33_stages_1000_pos_3000_neg_wrong.xml existed: True
	file detect_bus_haar_group.py existed: True
	file get_cam_id.py existed: True
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
	'get_cam_id.py', 
	'get_image.py', 
	#'gui_hsv.py', 
	#'knaps.py', 
	#'knapsack_2.py', 
	#'maps.html', 
	#'program_detect_rectangle.zip', 
	'start_wimb.py',
	]
	directory_list=[
	'images',
	'images_haar',
	'images_number',
	'models',
	]
	
	for file_name in file_list: print 'file '+file_name+' existed: '+str(os.path.isfile(file_name))
	for directory_name in directory_list: print 'directory '+directory_name+' existed: '+str(os.path.isdir(directory_name))


def capture_pictures(): 
	execfile('get_image.py')
if debug: print 'current absolute path of the project(path) is '+os.path.abspath('.')

"""
import get_image
path=os.path.abspath('.')
s=sched.scheduler(time.time,time.sleep)
starttime=time.time()
get_image.get_pictures()
while time.time()<starttime+5*60: # less than five minutes, just keep taking and processing pictures
	s.enter(5,1,get_image.get_pictures,()) #set first parameter in seconds
	s.run()
"""