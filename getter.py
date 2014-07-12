import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.
from threading import Thread # For multi-threading.
from Queue import Queue # Also for multi-threading.

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
	# Queues are used when multi-threading to let threads communicate with eachother. q.put(object) adds an item to the end of the list and q.get() removes an item from the beginning of the list.
	q=Queue()
	procs=[]
	# Starts thread that accepts new clients.
	limit=2
	accept_proc=Thread(target=connect_to_open_port_and_accept_clients,args=(s,q,bg,pointer,lsi,limit,))
	accept_proc.start()
	still_going=True
	while still_going:
		# Adds all new client-servicing threads to the list and starts them.
		while not q.empty():
			procs.append(q.get())
			procs[len(procs)-1].start()
		# The program should keep running if it is still accepting clients.
		still_going = accept_proc.is_alive()
		# The program should keep running if it is still servicing any client.
		for i in range(0,len(procs)):
			still_going = still_going or procs[i].is_alive()
		# The program checks one last time to make sure no clients were added to the queue when it wasn't looking.
		still_going = still_going or not q.empty()
	# Closes socket when done. Will only get here if client limit is reached.
	s.shutdown(socket.SHUT_RDWR)
	s.close()

def connect_to_open_port_and_accept_clients(s,q,bg,pointer,lsi,limit=100,port=55550):
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
		# Creates service client process and puts it into the queue.
		q.put(Thread(target=start_service,args=(conn,bg[current_client],pointer[current_client],lsi[current_client],)))
		current_client+=1
		if current_client>limit-1:
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
