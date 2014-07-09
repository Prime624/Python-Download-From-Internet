import socket,pickle # Needed to recieve image
import pygame as pg,sys,os,time # Needed to display image.

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('',55556))
#s.send('bg')
#backgroundPic=s.recv(1024)
s.send('pointer')
aaa=s.recv(35840)
bbb=pickle.loads(aaa)
pointerPic=pg.surfarray.make_surface(bbb)
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
