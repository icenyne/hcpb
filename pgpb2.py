#!/usr/bin/python
import sys, threading, time
import pygame 
from pygame.locals import *
from pbgmlib import *

queue = {}

move=True
if len(sys.argv)>=2:
	print 'Not moving files...'
	move=False



pygame.init()
size = width, height = 960, 540
black = 0,0,0
white = 255,255,255
screen = pygame.display.set_mode(size)

# main run loop...
while 1:

#	answer=raw_input('continue?: ')
#	if answer == 'n' or answer=='N': break
	waitforkey([K_g, K_r, K_y])

	# get the next sequential filename from nonvolatile store (a file...)
	filename = new_filename(increment=True) 

	totaltime = time.time()

	# grab four images...
	for i in range(4):  

		screen.fill(black)
		pygame.display.flip()

		grab_image(filename, i) # take photo with camera
		
		image = pygame.image.load(filename+'_'+suffix[i]+'.jpg')
		imagerect = image.get_rect()
		image = pygame.transform.scale(image, size)
		screen.blit(image, (0,0))
		pygame.display.flip()

		start = time.time()
		# process incrementally only the display image...
		t_disp = do_thread(display_4upHD, filename, i)
		# kick off phone and print processing with blocking, so it can run in background...
		if (i==0): queue[filename] = do_thread(print_4upbigall, filename, finish)

		time.sleep(6) # wait before entering loop...  but put graphic progress here...
		while ( t_disp.isAlive() ):# or t_print.isAlive() ): 
			time.sleep(1)
			print 'processing...'
		print 'Proc time: ', time.time()-start

	# finish out the compositing...
	start = time.time()
	#grab_image(filename, finish, process=True) # non-threaded equivalent...
	# but again, we want to thread so we can show progress visually...
	t_disp = do_thread(display_4upHD, filename, finish)
	#queue[filename] = do_thread(print_4upbigall, filename, finish)

	while ( t_disp.isAlive() ):
		time.sleep(3)

	image = pygame.image.load(filename+'_display.jpg')
	imagerect = image.get_rect()
	image = pygame.transform.scale(image, size)
	screen.blit(image, (0,0))
	pygame.display.flip()
	
	while (queue[filename].isAlive() ): 
		time.sleep(3)
		print 'processing...'
	print 'Proc time: ', time.time()-start
	queue.pop(filename, None) # delete thread from queue, since it's finished...

	# copy files to local and SAMBA share...
	#if move==True: move_files(filename)

	print 'Total time: ', time.time()-totaltime
	pygame.event.clear() # clear to make sure no buttons were pushed while processing...



