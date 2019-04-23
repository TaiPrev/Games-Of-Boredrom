import pygame, sys
from pygame.locals import * 

pygame.init()

#FPS
FPS = 60
fpsClock = pygame.time.Clock()

#Set Window
DISPLAYSURF = pygame.display.set_mode((800,500))
pygame.display.set_caption('Pyko no Tatsujin! Py version!')

#Set up colors
Aqua=(0, 255, 255)
Black=(0, 0,0)
Blue=(0,0, 255)
Fuchsia=(255, 0, 255)
Gray=(128, 128, 128)
Green=(0, 128,0)
Lime=(0, 255, 0)
Maroon=(128,0,0)
NavyBlue=(0,0, 128)
Olive=(128, 128,0)
Purple=(128,0, 128)
Red=(255, 0,0)
Silver=(192, 192, 192)
Teal=(0, 128, 128)
White=(255, 255, 255)
Yellow=(255, 255,0)

donGFX = pygame.image.load('images/don40.png')
kaGFX = pygame.image.load('images/ka.png')
#markerGFX = pygame.image.load('images/marker40.png')

note_start_x = 840
note_start_y = 100
note_end_x = 20

marker_start_x = 821
marker_start_y = 100
marker_end_x = 10

#Score positions in x
perfect = 100
too_early = 140
too_late = 60

BPM = 120 #beats per minute
BPS = BPM / 60 #beats per second
RFB = BPS * FPS #refreshes per beat, in this case 120 frames <=> 2 seconds

pixObj = pygame.PixelArray(DISPLAYSURF)
del pixObj

#################################################################################################################

#STRUCTS
class Song:
	def __init__(self, BPM, division, mp3_string, name, don, ka, length):
		self.BPM = BPM
		self.division = division #How many sections does a beat have.
		self.mp3_string = mp3_string
		self.name = name
		self.don = don
		self.ka = ka
		self.length = (BPM/60)*division*length #MEASURED IN INSTANTS
		#self.instants = instants == BPM * division

	def get_Don_Ka_Map(self):
		final_map = []
		i=0
		j=0
		a=0
		b=1
		c=2
		for x in range (0,self.length):
			final_map.append(a)
			if(i<len(self.don)):
				if (self.don[i]==x):
					final_map[x]=b
					i+=1
			if (j<len(self.ka)):
				if (self.ka[j]==x):
					final_map[x]=c
					j+=1
		return final_map
	def get_name(self):
		return self.name

	def get_mp3_name(self):
		return self.mp3_string

	def get_BPM(self):
		return self.BPM

	def get_division(self):
		return self.division

	def get_length(self):
		return self.length

#################################################################################################################
#FUNCTIONS

def subtract(x): 
	return x - speed

def subtract_special(x):
	if (x<0):
		return x + speed
	else:
		return x - speed

#################################################################################################################
# 											DRAW FUNCTIONS
#################################################################################################################

def draw(game_status, INGAME_STATS, song):
	if (game_status == 0):
		return
	elif (game_status == 1):
		return drawInGame(INGAME_STATS, song)
#################################################################################################################

def drawBaseInGame():
	#CLEAN SCREEN
	DISPLAYSURF.fill(Black)
	#DRAW BASE BACGROUND
	#input circle
	pygame.draw.circle(DISPLAYSURF, Silver, (100, 100), 40, 0) #(surface, color, center_point, radius, width)
	#aesthetic lines
	pygame.draw.line(DISPLAYSURF, Aqua, (0,40), (800, 40), 5) #(surface, color, start_point, end_point, width)
	pygame.draw.line(DISPLAYSURF, Aqua, (0,160), (800, 160), 5)

#################################################################################################################

def drawInGame(STATS, song):
	##marker_counter, marker_instant, instant, markers_pos, don_ka_pos, DON-KA-MAP
	BPM = song.get_BPM()
	division = song.get_division()
	length = song.get_length()
	BPS = BPM / 60 #beats per second
	RPB = BPS * FPS  #refresh per beat
	RPI = RPB / division #refresh per instant

	don_ka_map = STATS[5]
	don_ka_pos = STATS[4]
	markers_pos = STATS[3]
	instant = STATS[2]
	marker_instant = STATS[1]
	if (instant == -1):
		marker_counter = RPB
		instant = 0

	else:
		marker_counter = STATS[0]

	#############
	#UPDATE MARKER_COUNTER
	if marker_counter >= RPB:
		marker_counter = -1
		markers_pos.append(marker_start_x)

	markers_pos = list(map(subtract, markers_pos))
	try:
		if (markers_pos[0]<=marker_end_x):
			markers_pos.pop(0)
	except:
		print("OOPSIE, empty markers!")

	drawBaseInGame()
	#UPDATE DON-KA situation
	if marker_instant>=RPI:
		marker_instant=-1
		instant += 1;
		note = don_ka_map.pop(0)
		if (note==1):
			don_ka_pos.append(note_start_x)
		elif (note==2):
			don_ka_pos.append(-note_start_x)

	don_ka_pos = list(map(subtract_special, don_ka_pos))
	try:
		if (abs(don_ka_pos[0])<=note_end_x):
			don_ka_pos.pop(0)
	except:
		print('OOPSIE, empty don_ka_map!')

	##############
	#DRAW DON-KA
	for x in don_ka_pos:
		pygame.draw.circle(DISPLAYSURF, White, (abs(x), 100), 39, 0)
		if (x<0): #KA
			pygame.draw.circle(DISPLAYSURF, Blue, (abs(x), 100), 38, 0)
		elif (x>0): #DON
			pygame.draw.circle(DISPLAYSURF, Red, (x, 100), 38, 0)
	#DRAW MARKERS
	for x in markers_pos:
		pygame.draw.line(DISPLAYSURF, White, (x, 160), (x, 40), 1)

	#UPDATES AND RETURN
	pygame.display.update()
	marker_counter +=1
	marker_instant +=1

	if (instant >=length):
		return [-1, -1, -1, [], [], []]
	return [marker_counter, marker_instant, instant, markers_pos, don_ka_pos, don_ka_map]
	##marker_counter, marker_instant, instant, markers_pos, don_ka_pos, DON-KA-MAP

#################################################################################################################

def drawInGame_SIMPLE(STATS, BPM):
	BPS = BPM / 60 #beats per second
	RPB = BPS * FPS  #refresh per beat

	markers_pos = STATS[1]
	marker_counter = STATS[0]

	#UPDATE MARKER_COUNTER
	if marker_counter >= RPB:
		marker_counter = 0;
		markers_pos.append(marker_start_x)

	markers_pos = list(map(subtract, markers_pos))
	try:
		if (markers_pos[0]<=marker_end_x):
			markers_pos.pop(0)
	except:
		print("OOPSIE, empty markers!")

	drawBaseInGame()
	for x in markers_pos:
		pygame.draw.line(DISPLAYSURF, White, (x, 160), (x, 40), 1)

	#UPDATES AND RETURN
	pygame.display.update()
	marker_counter +=1
	return [marker_counter, markers_pos]
#################################################################################################################



#################################################################################################################
# 											INPUT FUNCTIONS
#################################################################################################################

def interact(game_status, INGAME_STATS):
	if game_status==0:
		return
	if game_status==1:
		return game_input(INGAME_STATS)

#################################################################################################################
#TODO: INPUTS ;
#CONTROL SCHEMA:
#	- S, D, LEFT MOUSE = DON
#	- A, F, RIGHT MOUSE = KA
def game_input(STATS):
	#TODO
	don_ka_pos = STATS[4]
	print(don_ka_pos)
	if (don_ka_pos != []):
		if (abs(don_ka_pos[0])>too_early):
			return STATS
		else:
			#pos_note = don_ka_pos[0] - 100	
			for event in pygame.event.get():
				print("OTHER!")
				#TODO: FIX INPUT
				if event.type == KEYDOWN:
					if event.key == K_a:
						print("into A")
						return calculate_ka(STATS)
					if event.key == K_s:
						print("into S")
						return calculate_don(STATS)
					if event.key == K_d:
						print("into D")
						return calculate_don(STATS)
					if event.key == K_f:
						print("into F")
						return calculate_ka(STATS)
				#if event.type == MOUSEBUTTONDOWN:
				#	if event.button == LEFT:
				#		return calculate_don(STATS)
				#	if event.button == RIGHT:
				#		return calculate_ka(STATS)
	return STATS
#################################################################################################################

def calculate_ka(STATS): #Input is KA, verify if correct and score and eliminate first note from map
	don_ka_pos = STATS[4]
	note = don_ka_pos.pop(0)
	if (note<0): #KA, CORRECT
		pygame.draw.circle(DISPLAYSURF, Green, (100, 300), 40, 0)
	elif (note>0): #DON, ERROR
		pygame.draw.circle(DISPLAYSURF, Red, (100, 300), 40, 0)
	return [STATS[0], STATS[1], STATS[2], STATS[3], don_ka_pos, STATS[5]]
def calculate_don(STATS): #Input is DON, verify if correct and score and eliminate first note from map
	don_ka_pos = STATS[4]
	note = don_ka_pos.pop(0)
	if (note<0): #KA, ERROR
		pygame.draw.circle(DISPLAYSURF, Red, (100, 300), 40, 0)
	elif (note>0): #DON, CORRECT
		pygame.draw.circle(DISPLAYSURF, Green, (100, 300), 40, 0)
	return [STATS[0], STATS[1], STATS[2], STATS[3], don_ka_pos, STATS[5]]
#################################################################################################################

def check_Quit():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	return
#################################################################################################################

#COUNTERS

#marker_counter = RFB
#markers_pos = []
#instant = 0 #Instants are the divisions within a beat, a song is made of x instants, which are bpm
game_status = 1 # 0 = MENU; 1 = IN-GAME ; 2 = IN-GAME-SIMPLE

BMP_SIMPLE = 120
speed = 4
song1 = Song(91, 4, "001.mp3", "The Sound of Silence (Original Version from 1964)", [10, 15, 20, 30, 40, 42, 44, 60], [50, 55, 70, 80, 90], 185)

INGAME_STATS = [0, 0, -1, [], [], song1.get_Don_Ka_Map()] #marker_counter, marker_instant, instant, markers_pos, don_ka_pos, DON-KA-MAP
INGAME_STATS_simple = [0,[]]
score = 0
#TODO: Finer control of the length of play of a song to match things well.  FURTHER IMPROVE THE CALCULATIONS OF SONGS ; INTRODUCE MENU SYSTEM
#################################################################################################################


#GAME LOOP
while True: #main game loop
	check_Quit()

	if (INGAME_STATS[2]==-1): #start of song
		id = song1.get_mp3_name()
		pygame.mixer.music.load("mp3/"+id)
		pygame.mixer.music.play(-1, 0.0)

	#INGAME_STATS_simple = drawInGame_SIMPLE(INGAME_STATS_simple, BMP_SIMPLE)
	INGAME_STATS = draw(game_status, INGAME_STATS, song1)
	INGAME_STATS = interact(game_status, INGAME_STATS)
	#TODO: FIX THIS!!!
	#print(INGAME_STATS)
	if (INGAME_STATS[0]==-1): #end of song
		game_status=0
		pygame.mixer.music.stop()

	fpsClock.tick(FPS)
