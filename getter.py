import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.
import multiprocessing as mp # For multi-threading.

def main():
	# Downloads images.
	print 'Downloading background images...'
	bg=[]
	bg.append(ul.urlopen('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1'))
	bg.append(ul.urlopen('https://www.dropbox.com/s/tz8yk7h6chnzi9o/pyGame.png?dl=1'))
	
	print 'Downloading pointer images...'
	pointer=[]
	pointer.append(ul.urlopen('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1'))
	pointer.append(ul.urlopen('https://www.dropbox.com/s/wxxqhwwkmn6o15b/mouseTwo.png?dl=1'))
	
	print 'Downloading sample large image...'
	lsi=[] # Same image downloaded twice, because each image is destroyed when it is read.
	lsi.append(ul.urlopen('http://scienceblogs.com/startswithabang/files/2012/12/globe_west_2048.jpeg'))
	lsi.append(ul.urlopen('http://scienceblogs.com/startswithabang/files/2012/12/globe_west_2048.jpeg'))
	
	print 'Images downloaded successfully!'
	
	# Sets up socket(server) and listens/accepts 1 client.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	connect_to_open_port(s)
	clients=2
	s.listen(clients)
	conns=[]
	procs=[]
	for i in range(0,clients):
		conn,addr=s.accept()
		conns.append(conn)
		procs.append(mp.Process(target=start_service,args=(conn,bg[i],pointer[i],lsi[i],)))
		procs[i].start()
	still_going=True
	while still_going:
		still_going=False
		for i in range(0,clients):
			still_going=procs[i].is_alive() or still_going
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

def start_service(conn,bg,pointer,largeSampleImage):
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
			# Sends image data.
			send_image_data(conn,sendable)

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
