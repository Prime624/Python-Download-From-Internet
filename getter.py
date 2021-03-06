import xml.etree.ElementTree as XML # Needed to get image urls from XML file.
import urllib as ul # Needed to download image from internet.
import pygame as pg,socket,sys # Needed to send image to display.
from threading import Thread # For multi-threading.
from Queue import Queue # Also for multi-threading.

def main():
	# Imports xml file containing urls.
	url_file=XML.parse('urls.xml')
	bg=[]
	# For every child in the 'backgrounds' child of the root...
	for child in url_file.getroot().find('backgrounds'):
		# ...add the text of the child to the list of urls.
		bg.append(child.text)
	pointer=[]
	for child in url_file.getroot().find('pointers'):
		pointer.append(child.text)
	lsi=[]
	for child in url_file.getroot().find('large'):
		lsi.append(child.text)
	
	# Sets up socket.
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# Queues are used when multi-threading to let threads communicate with eachother. q.put(object) adds an item to the end of the list and q.get() removes an item from the beginning of the list.
	q=Queue()
	procs=[]
	# Sets limit as the fewest number of links in any of the groups in the xml file, so that a link that doesn't exist is never requested.
	limit=min(len(bg),len(pointer),len(lsi))
	# Starts thread that accepts new clients.
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
	# Closes socket when done. Will only get here if client limit is reached and all clients are done being serviced.
	s.shutdown(socket.SHUT_RDWR)
	s.close()

def connect_to_open_port_and_accept_clients(s,q,bg,pointer,lsi,limit,port=55550,host=''):
	"""Documentation here"""
	# Connects to first open socket in range from 55550 to 55559.
	try:# If none of those sockets are available, then quits application.
		s.bind((host,port))
		hhh= socket.gethostname()
		print 'Connected to port {}.'.format(port)
	except socket.error:
		if port<55560:
			connect_to_open_port_and_accept_clients(s,q,bg,pointer,lsi,limit,port+1)
		else:
			s.shutdown(socket.SHUT_RDWR)
			s.close()
			print 'Could not find open port. Closing application.'
			sys.exit()
	current_client=0
	while True:
		# Listens for and accepts next client.
		s.listen(1)
		conn,addr=s.accept()
		print 'Connected to client at {}'.format(addr)
		# Creates service client process and puts it into the queue.
		q.put(Thread(target=start_service,args=(conn,bg[current_client],pointer[current_client],lsi[current_client],)))
		current_client+=1
		if current_client>limit-1:
			break

def start_service(conn,bg,pointer,largeSampleImage):
	images={'pointer':pointer,'bg':bg,'large':largeSampleImage}
	data=conn.recv(1024)
	while data:
		# Downloads image and puts image data into format readable by the client.
		print 'Responding to request "{}"...'.format(data)
		sendable=ul.urlopen(images[data]).read()
		# Sends image data.
		send_image_data(conn,sendable)
		# Listens for data.
		data=conn.recv(1024)

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
