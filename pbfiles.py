#!/usr/bin/python
import os
import shutil

def shellcmd(command):
	print command
	os.system(command)

# filename function: returns next sequential filename
def new_filename(storename='lastphoto'):
	last = eval(open(storename, 'r').read())
	filename = 'DSC' + (4-len(str(last)))*'0' + str(last)
	open(storename, 'w').write(str(last+1))
	return filename

# move files into local subdirectories and SAMBA share at path
def move_files(filename, path='/media/photobooth/'):
      try:
	print
	print 'filename = ', filename
	print 'Moving raw images...'
	shellcmd('cp DSC*_[a-d].jpg '+path+'raw-images')
	shellcmd('mv DSC*_[a-d].jpg raw-images')
	print 'Moving dislay image...'
        shellcmd('cp DSC*_display.jpg '+path+'for-display')
	shellcmd('mv DSC*_display.jpg for-display')
	print 'Moving print image...'
        shellcmd('cp DSC*_print.jpg '+path+'for-print')
	shellcmd('mv DSC*_print.jpg for-print')
	print 'Moving phone image...'
        shellcmd('cp DSC*_phone.jpg '+path+'for-phone')
	shellcmd('mv DSC*_phone.jpg for-phone')
      except:
	pass

