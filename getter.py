import urllib as ul,urllib2 as ul2 # Needed to download image from internet.
import pygame as pg,socket,os # Needed to load and send image to display.
import sys#DELETE_ME

def main():
	print 'Downloading images...'
	#Downloads sample image to temporary location.
	bgr=ul.urlretrieve('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1','tmpImage.png')
	#Loads image into Pygame.
	bg=pg.image.load('tmpImage.png')
	#Deletes temporary image.
	os.remove('tmpImage.png')
	#Repeat above steps for second image.
	pointerr=ul.urlretrieve('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1','tmpImage2.png')
	pointer=pg.image.load('tmpImage2.png')
	os.remove('tmpImage2.png')
	print 'Images downloaded successfully!'
	
	#Sets up socket(server) and listens/accepts 1 client.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind(('',55556))
	s.listen(1)
	conn,addr=s.accept()
	while 1:
		#Listens for data.
		data=conn.recv(1024)
		if not data: break
		if data:
			#Sends requested image over socket.
			if data=='pointer':
				size=pointer.get_size()
				conn.send("{}QQQQQ{}".format(size,pg.image.tostring(pointer,"RGBA")))
			elif data=='bg':
				print sys.getsizeof(pg.image.tostring(bg,"RGBA"))
				size=bg.get_size()
				conn.send("{}QQQQQ{}".format(size,pg.image.tostring(bg,"RGBA")))
	conn.close()

if __name__=='__main__':
	main()
