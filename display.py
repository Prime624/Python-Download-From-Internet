import socket # Needed to recieve image
from cStringIO import StringIO # Needed to load image data into buffer.
import pygame as pg,sys,os,time # Needed to display image/time.

def main():
	# Sets up socket.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connect_to_valid_server(s)
	
	# Requests and receives images.
	backgroundPic=request_and_recv_image(s,'bg')
	pointerPic=request_and_recv_image(s,'pointer')
	s.close()
	
	# Sets up pygame and displays image/time.
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

def connect_to_valid_server(s,port=55550):# Connects to first open server in range from 55550 to 55559.
	try:#							If none of those servers are available, then quits application.
		s.connect(('',port))
		print 'Connected to server on port {}.'.format(port)
	except socket.error:
		if port<55560:
			connect_to_valid_server(s,port+1)
		else:
			s.close()
			print 'Could not find server. Closing application.'
			sys.exit()

def request_and_recv_image(s,image_str):
	# Requests picture from server.
	s.send(image_str)
	# Records number of parts and size of last part.
	info=s.recv(1024).split(" ")
	num_of_parts=int(info[0])
	size_of_last_part=int(info[1])
	# Requests and recieves each part.
	pic_data=""
	for i in range(0,num_of_parts):
		s.send(str(i))
		# Each part is only 4080 bytes instead of 4096 so that the client can detect whether extra information was sent or not.
		part_data=s.recv(4096)
		# If this is not the last part, then there should be 4080 bytes recieved (because it is in ASCII encoding, 1 letter == 1 byte so using the len() method has the same effect as checking the number of bytes).
		if i<num_of_parts-1:
			while len(part_data)!=4080:
				s.send(str(i))
				part_data=s.recv(4096)
		else:# If this is the last part, then the amount of data should be equal to the specified amount recieved earlier. If not, ask for new information to be sent. When it is good, tell the server that the image has been correctly received.
			while len(part_data)!=size_of_last_part:
				s.send(str(i))
				part_data=s.recv(4096)
			s.send(' ')
		# Adds this piece of data to the collection.
		pic_data+=part_data
	# Decodes image data from assemblage of data.
	return pg.image.load(StringIO(pic_data))

if __name__=='__main__':
	main()
