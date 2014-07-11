import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.
import multiprocessing as mp # For multi-threading.

def main():
	# Sets image urls for use when requested.
	bg=[]
	bg.append('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1')
	bg.append('https://www.dropbox.com/s/tz8yk7h6chnzi9o/pyGame.png?dl=1')
	pointer=[]
	pointer.append('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1')
	pointer.append('https://www.dropbox.com/s/wxxqhwwkmn6o15b/mouseTwo.png?dl=1')
	lsi=[]
	lsi.append('http://scienceblogs.com/startswithabang/files/2012/12/globe_west_2048.jpeg')
	lsi.append('http://scienceblogs.com/startswithabang/files/2012/12/globe_west_2048.jpeg')
	
	# Sets up socket.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	procs=[]
	# Starts thread that accepts new clients.
	accept_proc=mp.Process(target=connect_to_open_port_and_accept_clients,args=(s,procs,bg,pointer,lsi,limit=2,))
	accept_proc.start()
	# Keeps application from closing if there are any running processes, or if no clients have yet been serviced.
	still_going=True
	while still_going:
		still_going=len(procs)==0
		for i in range(0,len(procs)):
			still_going=procs[i].is_alive() or still_going
	# Closes socket when done. Will only get here if client limit is reached.
	s.shutdown(socket.SHUT_RDWR)
	s.close()

def connect_to_open_port_and_accept_clients(s,procs,bg,pointer,lsi,limit=100,port=55550):
	# Connects to first open socket in range from 55550 to 55559.
	try:# If none of those sockets are available, then quits application.
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
	current_client=0
	while 1:
		# Listens for and accepts next client.
		s.listen(1)
		conn,addr=s.accept()
		# Starts process to service client.
		procs.append(mp.Process(target=start_service,args=(conn,bg[current_client],pointer[current_client],lsi[current_client],)))
		procs[current_client].start()
		current_client+=1
		if current_client>limit-2:
			break

def start_service(conn,bg,pointer,largeSampleImage):
	while 1:
		# Listens for data.
		data=conn.recv(1024)
		if not data: break
		if data:
			# Downloads image and puts image data into format readable by the client.
			print 'Responding to request "{}"...'.format(data)
			if data=='pointer':
				sendable=ul.urlopen(pointer).read()
			elif data=='bg':
				sendable=ul.urlopen(bg).read()
			elif data=='large':
				sendable=ul.urlopen(largeSampleImage).read()
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
