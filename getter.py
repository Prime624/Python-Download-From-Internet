import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.

def main():
	print 'Downloading images...'
	# Downloads images.
	bg=ul.urlopen('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1')
	pointer=ul.urlopen('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1')
	largeSampleImage=ul.urlopen('http://scienceblogs.com/startswithabang/files/2012/12/globe_west_2048.jpeg')
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
			print 'Responding to request "{}"...'.format(data)
			if data=='pointer':
				sendable=pointer.read()
			elif data=='bg':
				sendable=bg.read()
			elif data=='large':
				sendable=largeSampleImage.read()
			# Sends image data. (Might be good to put this method into a separate thread.)
			send_image_data(conn,sendable)
	s.shutdown(socket.SHUT_RDWR)
	s.close()

def connect_to_open_port(s,port=55550):# Connects to first open socket in range from 55550 to 55559.
	try:#							If none of those sockets are available, then quits application.
		s.bind(('',port))
		print 'Connected to port {}.'.format(port)
	except socket.error:
		if port<55560:
			connect_to_open_port(s,port+1)
		else:
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			print 'Could not find open port. Closing application.'
			sys.exit()

def send_image_data(conn,sendable):
	# Tells client how much data will be sent.
	lenData=len(sendable)
	conn.sendall(str(lenData))
	# Waits for confirmation that client is ready.
	conn.recv(4)
	# Sends all information (socket.sendall() continues sending information until all is sent).
	conn.sendall(sendable)

if __name__=='__main__':
	main()
