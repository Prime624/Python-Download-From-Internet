import urllib as ul # Needed to download image from internet.
import pygame as pg,socket # Needed to send image to display.
import sys

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
			# Decides which image to send.
			if data=='pointer':
				# Puts image data into format readable by the client.
				sendable=pointer.read()
				# Determines how many portions of data it will have to send to limit maximum size to 4096 per message.
				numParts=len(sendable)/4096+(len(sendable)%4096!=0)
				# Sends this info to client to prepare it for reception.
				conn.send(str(numParts))
				# Sends each part.
				for i in range(0,numParts):
					# Waits for response from client signaling that it is ready.
					conn.recv(1024)
					# Sends the next piece of data.
					conn.send(sendable[i*4096:(i+1)*4096])
			elif data=='bg':
				# Same as above.
				sendable=bg.read()
				numParts=len(sendable)/4096+(len(sendable)%4096!=0)
				conn.send(str(numParts))
				for i in range(0,numParts):
					conn.recv(1024)
					conn.send(sendable[i*4096:(i+1)*4096])
	conn.close()

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

if __name__=='__main__':
	main()
