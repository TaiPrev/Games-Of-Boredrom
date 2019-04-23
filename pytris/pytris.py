#TETRIS

import pygame, sys, random
from pygame.locals import *


#MEASUREMENTS
#CUBES = 20X20
#CUBES PER LINE = 12
#TOTAL LINES = 20

#PLAYAREA = 240X 400Y

FPS = 60

top = 300
bottom = 700
left = 180
right = 420

#####################################################################

def is_Line_Empty(line):
	for x in range(0,11):
		if (line[x]):
			return True;
	return False;

#####################################################################

def is_Line_Complete(line):
	for x in range(0,11):
		if (not line[x]):
			return False;
	return True;

#####################################################################

def clear_lines(old_mem):
	new_mem = [[False for x in range(12)] for y in range(21)] 
	i = 0
	for k in range(0, 20):
		if (not is_Line_Complete(old_mem[k][:])):
			for j in range(0, 12):
				new_mem[i][j] = old_mem[k][j]
			i+=1
	return new_mem
#####################################################################

def generate_piece(piece_names):
	return random.choice(piece_names)

#####################################################################

def rotate(piece):
	return

#####################################################################

def draw_playArea():
	#X: 180 ; 420
	#Y: 300 ; 700
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, top-1), (left-1, bottom), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (right, top-1), (right, bottom), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, top-1), (right, top-1), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, bottom), (right, bottom), 1)

#####################################################################

def draw_cube(col, row):
	pos_x = 180 + 20*col
	pos_y = 300 + 20*row
	pygame.draw.rect(DISPLAYSURF, GREEN, (pos_x, pos_y, 20, 20))
	pygame.draw.rect(DISPLAYSURF, BLUE, (pos_x+1, pos_y+1, 18, 18))

#####################################################################

def draw_laid_cubes(mem):
	for x in range(0, 21):
		for y in range(0, 12):
			if (mem[x][y]):
				print("Draw laid cube") #THE CUBES ARE BEING DRAW, SOMEWHERE
				draw_cube(x, y)

#####################################################################

def draw_piece(piece, col, row):
	for i in range(0, len(piece)):
		for j in range(0, len(piece)):
			if (piece[i][j]==1):
				draw_cube(col+i, row+j)

#####################################################################

def draw_piece_stack(stack):
	#X: 440 > col = 14
	#Y: 320 > row = 1
	row = 0
	col = 14
	for i in range(0, 4):
		draw_piece(stack[i], col, row)
		row += 5

#####################################################################

def draw(mem, stack, pos, piece):
	DISPLAYSURF.fill(BLACK)
	draw_playArea()
	draw_laid_cubes(mem)
	draw_piece_stack(stack)
	draw_piece(piece, pos[1], pos[0])

#####################################################################

def reset_memory(mem):
	for x in range(0, 21):
		for y in range(0, 12):
			mem[x][y] = False
	return mem

#####################################################################

def contact_floor(pos, piece): 
	for i in range(0, len(piece)):
		if (piece[len(piece)-1][i] == 1 and pos[0] == (22-len(piece)-1)):
			print("GROUND TOUCHED")
			return True
	print("THE GROUND IS FAR AWAY")
	return False

#####################################################################

def contact(mem, pos, piece): # pos: line, col ; mem: line, col
	length = len(piece)
	#print(pos)
	for i in range(0, length):
		for j in range(0, length):
			line = pos[0]+(i)
			row = pos[1]+(j)
			#print(i, j, line, pos)
			if (piece[i][j]==1 and mem[line][row]): #there's SOMETHING BELOW, BLOCKS IT IN PLACE
				print("THERE'S SOMETHING BELLOW")
				return True		
	return False

#####################################################################
#TODO: FIX THIS, MEMORY ISN'T UPDATED CORRECTLY
def update_memory(old_memory, pos, piece):
	new_mem = [[False for x in range(12)] for y in range(21)] 
	for k in range(0, 20):
		for j in range(0, 12):
			new_mem[k][j] = old_memory[k][j]

	for x in range(0, len(piece)):
		for z in range(0, len(piece)):
			col = pos[0]+x
			row = pos[1]+z
			if (piece[x][z]==1):
				print(col, row)
				new_mem[col][row] = True
		
	#print(new_mem)		
	return new_mem

#####################################################################

cubeSize = 20
CPL = 12
lines = 21

ticks_per_level = [1.5, 1.45, 1.4, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1]

#PIECES
l = [[0, 0, 0, 0],
	 [1, 1, 1, 1],
	 [0, 0, 0, 0],
	 [0, 0, 0, 0]
	]
o = [[1, 1],
	 [1, 1]
	]

s = [[0, 0, 0],
	 [0, 1, 1],
	 [1, 1, 0]
	]

z = [[0, 0, 0],
	 [1, 1, 0],
	 [0, 1, 1]
	]

L = [[1, 0, 0],
	 [1, 0, 0],
	 [1, 1, 0]
	]

j = [[0, 0, 1],
	 [0, 0, 1],
	 [0, 1, 1]
	]

t = [[0, 0, 0],
	 [1, 1, 1],
	 [0, 1, 0]
	]

piece_names = [l, o, s, z, L, j, t]

#COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

memory = [[False for x in range(12)] for y in range(21)] 
level = 0
score = 0
start = True
piece_position = [0,6] #line, col
piece_stack = []
piece_current = []
pygame.init()
time_mark = pygame.time.get_ticks()
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((600,1000))

while True: #main loop
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	#if (level == -1): #GAME_OVER
		#DISPLAY RESTART OPTIONS

	if (start):
		start = False;
		memory = reset_memory(memory)
		level = 9
		score = 0
		piece_stack = []
		piece_current = generate_piece(piece_names)
		piece_position = [0,6]
		for x in range(0, 4):
			piece_stack.append(generate_piece(piece_names))
		memory = clear_lines(memory)

	if(level != -1):
		#print(memory)
		draw(memory, piece_stack, piece_position, piece_current)
		time_current = pygame.time.get_ticks()
		if ((time_current - time_mark) >= (1000 * ticks_per_level[level])):
			piece_position[0] = piece_position[0]+1
			time_mark = time_current
			#if (contact(memory, piece_position, piece_current) or contact_floor(piece_position, piece_current)): #check if it has made contact, if so, update memory, generate new piece and pop the one on top of the list
			#	memory = update_memory(memory, piece_position, piece_current)
			#	piece_current = piece_stack.pop(0)
			#	piece_stack.append(generate_piece(piece_names))
			#	piece_position = [0,6]
			if(contact_floor(piece_position, piece_current)):
				memory = update_memory(memory, piece_position, piece_current)
				piece_current = piece_stack.pop(0)
				piece_stack.append(generate_piece(piece_names))
				piece_position = [0,6]
				
		if is_Line_Empty(memory[0][:]): #if game_over, aka something in line 21), LEVEL = -1
			level = -1
			print("GAME_OVER")
		pygame.display.update()
		fpsClock.tick(FPS)

#end while
