#!/usr/bin/python
import sys, threading, time
import pygame 
from pygame.locals import *
from pbgmlib import *
from progress import *

queue = {}

move=True
if len(sys.argv)>=2:
	print 'Not moving files...'
	move=False

pygame.init()
screen = pygame.display.set_mode(size)
#toggle_fullscreen()

# main run loop...
while 1:
	showtext(screen, "Push a button to start", 100)

	waitforkey([K_g, K_r, K_y])

	# get the next sequential filename from nonvolatile store (a file...)
	filename = new_filename(increment=True) 

	totaltime = time.time()

	# grab and begin processing four images...
	for i in range(4):  

		fillscreen(screen, black)
		flashtext(2, 0.5, screen, "Look at the camera", 100, (width/2, height*3/4))
		grab_image(filename, i) # take photo with camera
		
		displayimage(screen, filename+'_'+suffix[i]+'.jpg', camerasize, cameraloc)

		start = time.time()
		# process incrementally only the display image...
		t_disp = do_thread(display_4upHD, filename, i)
		# kick off phone and print processing with blocking, so it can run in background...
		if (i==0): queue[filename] = do_thread(print_4upbigall, filename, finish)

		time.sleep(4) # wait before entering loop...  but put graphic progress here...
		while ( t_disp.isAlive() ):# or t_print.isAlive() ): 
			time.sleep(1)
			print 'processing...'
		print 'Proc time: ', time.time()-start



	# finish out the compositing...
	start = time.time()
	t_disp = do_thread(display_4upHD, filename, finish)

	while ( t_disp.isAlive() ):
		time.sleep(3)

	displayimage(screen, filename+'_display.jpg', size)

	w,h = size
	prog = Ball( (int(0.02*w),int(0.85*h)), (0, 35))
	progsprite = pygame.sprite.RenderPlain(prog)
	progress = 0
	
	while (queue[filename].isAlive() ): 
		time.sleep(1)
		print 'processing...'

		try:
		  displayimage(screen, filename+'_display.jpg', size)
		  progsprite.update()
		  progsprite.draw(screen)

		  font = pygame.font.Font(None, 36)
		  text = font.render(str(int(progress))+"%", 1, (10, 10, 10))
		  textpos = text.get_rect()
		  textpos.centerx, textpos.centery = prog.rect.centerx, prog.rect.centery-15
		  screen.blit(text, textpos)
		  progress += 4

		  pygame.display.flip()
		except:
		  pass

	print 'Proc time: ', time.time()-start
	queue.pop(filename, None) # delete thread from queue, since it's finished...

	# copy files to local and SAMBA share...
	#if move==True: move_files(filename)

	print 'Total time: ', time.time()-totaltime
	pygame.event.clear() # clear to make sure no buttons were pushed while processing...



