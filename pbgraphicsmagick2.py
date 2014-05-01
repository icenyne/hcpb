#!/usr/bin/python
import threading
import time
import piggyphoto
from pbfiles import *

# define image sizes for display and print...
disp_size = '495x330' 
print_size = '1200x800' #  '1000x667'
# create a list of image sizes
#sizes = [ disp_size, print_size]
sizes = [ print_size]
suffix = [ 'a', 'b', 'c', 'd' ]

 
# create PTP connection to camera...
C = piggyphoto.camera()

def grab_image(filename, i, quiet=False):
		if not(quiet): 
			print
			print 'Count down: 3...'
			time.sleep(0.25)
			print '2...'
			time.sleep(0.25)
			print '1...'
			time.sleep(0.25)
			print 'Capturing image', i+1
		else: time.sleep(1)
		C.capture_image(filename+'_'+suffix[i] + '.jpg')
		if not(quiet): 
			print 'Downloading image', i+1
			print

# function to change incoming image to various sizes to make tile-ups easier...
def change_size(filename, insizes):
	for size in sizes:
		#print 'convert ' + filename+'.jpg' + ' -resize ' + size + ' '  + filename+'_'+size+'.jpg'
		#os.system('convert ' + filename+'.jpg' + ' -resize ' + size + ' '  + filename+'_'+size+'.jpg')
		cmd = 'gm convert -size '+ size +' ' + filename+'.jpg -resize '+ size +' ' + filename+'_'+size+'.jpg'
		shellcmd(cmd) 

# function to make display 4-tile-up
def display_4up(filename, size=print_size):
	yloc = ['+124+12 ', '+124+373 ', '+652+373 ', '+652+12 ']
        for i in range(4):
		cmd = 'gm composite -resize 504x336 -geometry  ' 
		cmd = cmd + yloc[i] + filename + '_' + suffix[i] + '.jpg '
		if i==0: cmd = cmd + ' images/backscreen.jpg'
		else: cmd = cmd + ' boutput.jpg'
        	cmd = cmd + ' -quality 100 boutput.jpg'
	        shellcmd(cmd)
	shellcmd('gm composite -geometry +340+210 -resize 600x images/overlay.png  boutput.jpg -quality 100 ' + filename + '_display.jpg')


def print_4up(filename, size=print_size):	
	yloc = ['+60+498 ', '+60+1124 ', '+60+1750 ', '+60+2376 ']
        for i in range(4):
		cmd = 'gm composite -resize 878x582 -geometry ' 
		cmd = cmd + yloc[i] + filename + '_' + suffix[i] + '.jpg '
		if i==0: cmd = cmd + ' images/background-half-rot.jpg'
		else: cmd = cmd + ' output.jpg'
        	cmd = cmd + ' -quality 100 output.jpg'
	        shellcmd(cmd)
	shellcmd('gm composite -geometry +200+150 -resize 1000x images/overlay.png  output.jpg -quality 100 ' + filename + '_phone.jpg')

	shellcmd('gm composite -geometry +0+0 ' + filename + '_phone.jpg images/background-rot.jpg -quality 100 done.jpg')
	shellcmd('gm composite -geometry +1001+0 ' + filename + '_phone.jpg done.jpg -quality 100 done.jpg')
	shellcmd('gm convert -stroke gray -draw "line 1000,0 1000,3000" done.jpg -quality 100 ' + filename + '_print.jpg')

def display_composite(filename):
	shellcmd('geog -f /media/photobooth/for-display/' + filename + '_display.jpg &')

def do_composite(filename):
	starttime = time.time() # save start time so we can tell how long things take...

	t_disp = threading.Thread( target=display_4up, args=(filename, ) )
	t_disp.start()
	t_print = threading.Thread( target=print_4up, args=(filename, ) )
	t_print.start()

	while ( t_disp.isAlive() or t_print.isAlive() ): 
		time.sleep(1)
		print 'processing...', time.time()-starttime
	print
	print 'time: ', time.time()-starttime
