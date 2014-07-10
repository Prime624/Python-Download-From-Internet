import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.
from random import randint

def main():
	print 'Downloading images...'
	# Downloads images.
	bg=ul.urlopen('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1')
	pointer=ul.urlopen('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1')
	print 'Images downloaded successfully!'
	
	# Sets up socket(server) and listens/accepts 1 client.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connect_to_open_port(s)
	s.listen(1)
	conn,addr=s.accept()
	while 1:
		# Listens for data.
		data=conn.recv(1024)
		if not data: break
		if data:
			# Puts image data into format readable by the client.
			if data=='pointer':
				sendable=pointer.read()
			elif data=='bg':
				sendable=bg.read()
			print '|||{}|||'.format(data)
			# Sends image data. (Might be good to put this method into a separate thread.)
			send_image_data(conn,sendable)
	s.close()

def connect_to_open_port(s,port=55550):# Connects to first open socket in range from 55550 to 55559.
	try:#							If none of those sockets are available, then quits application.
		s.bind(('',port))
		print 'Connected to port {}.'.format(port)
	except socket.error:
		if port<55560:
			connect_to_open_port(s,port+1)
		else:
			s.close()
			print 'Could not find open port. Closing application.'
			sys.exit()

def send_image_data(conn,sendable):
	# Determines how many portions of data it will have to send to limit maximum size to 4096 per message.
	numParts=len(sendable)/4080+(len(sendable)%4080!=0)
	# Sends number of parts and amount of data in last packet to client to prepare it for reception.
	conn.send("{} {}".format(numParts,len(sendable)%4080))
	while 1:
		# Waits for response from client requesting data.
		req=conn.recv(1024)
		if req==' ':
			# Signal that client has finished recieving image.
			break
		else:
			# Sends the requested piece of data.
			i=int(req)
			if 0:# Set this to True to simulate data inaccuracy over sockets.
				# Program accounts for limited data inaccuracies. They are very uncommon occurences when transferring such small pieces of data.
				mistake=randint(0,3)
				if mistake>1:# No errors simulated.
					conn.send(sendable[i*4080:(i+1)*4080])
				elif mistake==1:# Extra data simulated.
					conn.send('AAA{}AAA'.format(sendable[i*4080:(i+1)*4080]))
				elif mistake==0:# Data loss simulated.
					conn.send(sendable[i*4080+10:(i+1)*4080-10])
			else:
				conn.send(sendable[i*4080:(i+1)*4080])

if __name__=='__main__':
	main()
