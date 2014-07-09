import urllib as ul,urllib2 as ul2 # Needed to download pages/files from internet.
import json # Needed to convert JSON file to a Python Dict.
import pygame as pg,sys,os,time # To display image.

#Downloads webpage/file from url. In this case, it is a sample text file.
response=ul2.urlopen('https://www.dropbox.com/s/6oo9gyaa880hmai/aaa.txt?dl=1')
fyle=response.read()
#Prints entire file.
print fyle
print ''
#Separates the text file by line into a list of Strings.
lines=fyle.split("\n")
#Prints out the fourth line.
print lines[3]
print ''
print ''
print ''
print ''

#Downloads sample JSON (initially from Google Maps).
response2=ul2.urlopen('https://www.dropbox.com/s/jrxgmvwuk3ujysy/aaa.json?dl=1')
#Converts the JSON to a Python Dict.
dec=json.load(response2)
#Prints entire file.
print dec
print ''
#Prints a specific property.
print dec["results"][0]["address_components"][2]["long_name"]

#Downloads sample image to temporary location.
response3=ul.urlretrieve('https://www.dropbox.com/s/2iz8c2f5pbdrh6d/aaa.png?dl=1','tmpImage.png')
#Loads image into Pygame.
image=pg.image.load('tmpImage.png')
#Deletes temporary image.
os.remove('tmpImage.png')
#Repeat above steps for second image.
response4=ul.urlretrieve('https://www.dropbox.com/s/z4w5sgaueirxpsa/bbb.png?dl=1','tmpImage2.png')
image2=pg.image.load('tmpImage2.png')
os.remove('tmpImage2.png')
#Sets up pygame and displays image/time.
pg.init()
pg.mouse.set_visible(False)
fpsClock = pg.time.Clock()
font = pg.font.Font('freesansbold.ttf',26)
mouseP=(0,0)
point=(5000,5000)
seconds=False
window = pg.display.set_mode((image.get_rect().size[0],image.get_rect().size[1]))
while 1:
	window.blit(image,(0,0))
	window.blit(image2,mouseP)
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
