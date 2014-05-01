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
	cmd = 'gm montage '
	for i in range(4):
		#cmd = cmd + filename + '_' + suffix[i] + '_' + size + '.jpg '
		cmd = cmd + filename + '_' + suffix[i] + '.jpg '
	cmd = cmd + ' -tile 2x2  -geometry ' + '1080x720' + '+25+25 -quality 100 tileup.jpg'
	shellcmd(cmd)
	shellcmd('gm composite -gravity center images/overlay.png tileup.jpg -quality 90 tileup.jpg')
	shellcmd('gm composite -gravity center tileup.jpg images/backscreen.jpg -quality 90 ' + filename + '_display.jpg')

def print_4up(filename, size=print_size):
        cmd = 'gm montage -rotate -90 '
        for i in range(4):
                #cmd = cmd + filename + '_' + suffix[i] + '_' + size + '.jpg '
		cmd = cmd + filename + '_' + suffix[i] + '.jpg '
        cmd = cmd + ' -tile 4x1  -geometry x1000+25+70 -quality 100 tileup2.jpg'
        shellcmd(cmd)
	# add the event info overlay to the top of the two strips, then add the two image strips...
	shellcmd('gm composite -rotate -90 -gravity southwest -resize x1000 images/overlay.png  images/background.jpg -quality 100 done.jpg')
	shellcmd('gm composite -rotate -90 -gravity northwest -resize x1000 images/overlay.png  done.jpg -quality 100 done.jpg')
	shellcmd('gm composite -gravity northeast  tileup2.jpg done.jpg -quality 100 done.jpg')
        shellcmd('gm composite -gravity southeast tileup2.jpg done.jpg -quality 100 done.jpg')
	# draw a line for cutting the two strips apart...
	shellcmd('gm convert -stroke gray -draw "line 0,1000 3000,1000" done.jpg -rotate 90 -quality 90 ' + filename + '_print.jpg')

def display_composite(filename):
	shellcmd('eog -f /media/photobooth/for-display/' + filename + '_display.jpg &')

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
