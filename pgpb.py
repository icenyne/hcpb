#!/usr/bin/python
import pygame 
from pygame.locals import *
from pbfiles import *
from pbgraphicsmagick2 import *


# main run loop...
while 1:

	thread_list = []
	answer=raw_input('continue?: ')
	if answer == 'n' or answer=='N': break

	# grab next filename from nonvolatile store
	filename = new_filename() 

	for i in range(4):  
		grab_image(filename, i)

	# kick off threaded composite generation...
	do_composite(filename)

	# use eye of gnome to display before moving over to pygame...
	display_composite(filename)

	# copy files to local and SAMBA share...
	move_files(filename)
