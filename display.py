import socket,pickle # Needed to recieve image
import pygame as pg,sys,os,time # Needed to display image/time.

def main():##!!!!!! Need to transmit data over socket in chunks.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(('',55555))
	#s.send('bg')
	#bps=s.recv(4096)
	#backgroundPic=pg.image.fromstring(bps[bps.index('QQQQQ')+5:],(int(bps[1:bps.index(',')]),int(bps[bps.index(' ')+1:bps.index(')')])),"RGBA")
	s.send('pointer')
	ps=s.recv(12288)
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
	#window = pg.display.set_mode((backgroundPic.get_rect().size[0],backgroundPic.get_rect().size[1]))
	window = pg.display.set_mode((500,500))#DELETE_ME
	while 1:
		#window.blit(backgroundPic,(0,0))
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
