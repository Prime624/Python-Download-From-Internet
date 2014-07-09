import socket # Needed to recieve image
import pygame as pg,sys,os,time # Needed to display image/time.

def main():
	#Sets up socket.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('',55556))
	#Requests first picture.
	s.send('bg')
	#Records number of parts to this picture.
	num_of_parts=int(s.recv(1024))
	bps=""
	#Requests and recieves each part.
	for i in range(0,num_of_parts):
		s.send("0")
		bps+=s.recv(4096)
	#Decodes image data from assemblage of data. (The first part is the image data, the middle part is the size.)
	backgroundPic=pg.image.fromstring(bps[bps.index('QQQQQ')+5:],(int(bps[1:bps.index(',')]),int(bps[bps.index(' ')+1:bps.index(')')])),"RGBA")
	#Repeats process for next image.
	s.send('pointer')
	num_of_parts=int(s.recv(1024))
	ps=""
	for i in range(0,num_of_parts):
		s.send("hello")
		ps+=s.recv(4096)
	pointerPic=pg.image.fromstring(ps[ps.index('QQQQQ')+5:],(int(ps[1:ps.index(',')]),int(ps[ps.index(' ')+1:ps.index(')')])),"RGBA")
	s.close()
	#Sets up pygame and displays image/time.
	pg.init()
	pg.mouse.set_visible(False)
	fpsClock = pg.time.Clock()
	font = pg.font.Font('freesansbold.ttf',26)
	mouseP=(0,0)
	point=(5000,5000)
	seconds=False
	window = pg.display.set_mode((backgroundPic.get_rect().size[0],backgroundPic.get_rect().size[1]))
	while 1:
		window.blit(backgroundPic,(0,0))
		window.blit(pointerPic,mouseP)
		if seconds:
			msgObj=font.render("It is {}".format(time.strftime("%H:%M:%S")), 1, pg.Color(0,0,0))
		else:
			msgObj=font.render("It is {}".format(time.strftime("%H:%M")), 1, pg.Color(0,0,0))
		window.blit(msgObj,point)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				sys.exit()
			elif event.type == pg.MOUSEMOTION:
				mouseP = event.pos
			elif event.type == pg.MOUSEBUTTONUP:
				if event.button in (1,2):
					point = event.pos
				elif event.button==3:
					point=(5000,5000)
				else:
					seconds=not seconds
		pg.display.update()
		fpsClock.tick(60)

if __name__=='__main__':
	main()
