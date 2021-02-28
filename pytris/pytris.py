#TETRIS

import pygame, sys, random
from pygame.locals import *


#MEASUREMENTS
#CUBES = 20X20
#CUBES PER LINE = 12
#TOTAL LINES = 20

#PLAYAREA = 240X 400Y

FPS = 60


cubeSize = 20
lines = 20
lineWidth = 12

top = 300
bottom = top + lines * cubeSize
left = 180
right = left + lineWidth * cubeSize


ticks_per_level = [10.5, 1.45, 1.4, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1]

#PIECES
l = [[1, 1, 1, 1],
	 [0, 0, 0, 0],
	 [0, 0, 0, 0],
	 [0, 0, 0, 0]
	]
o = [[1, 1],
	 [1, 1]
	]

s = [[0, 1, 1],
	 [1, 1, 0],
	 [0, 0, 0]
	]

z = [[1, 1, 0],
	 [0, 1, 1],
	 [0, 0, 0]
	]

L = [[1, 0, 0],
	 [1, 0, 0],
	 [1, 1, 0]
	]

j = [[0, 0, 1],
	 [0, 0, 1],
	 [0, 1, 1]
	]

t = [[1, 1, 1],
	 [0, 1, 0],
	 [0, 0, 0]
	]

piece_names = [l, o, s, z, L, j, t]

#COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#INFO
memory = [[False for x in range(lineWidth)] for y in range(lines)] 
level = 0
score = 0
start = True
gameloop = True
piece_position = [0,6] #line, col
piece_stack = []
piece_current = []
pygame.init()
time_mark = pygame.time.get_ticks()
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((600,1000))

#####################################################################

def is_Line_Empty(line):
	for x in range(0,lineWidth-1):
		if (line[x]):
			return True;
	return False;

#####################################################################

def is_Line_Complete(line):
	for x in range(0,lineWidth-1):
		if (not line[x]):
			return False;
	return True;

#####################################################################

def clear_lines(old_mem):
	new_mem = [[False for x in range(lineWidth)] for y in range(lines)] 
	i = 0
	for k in range(0, lines-1):
		if (not is_Line_Complete(old_mem[k][:])):
			for j in range(0, lineWidth):
				new_mem[i][j] = old_mem[k][j]
			i+=1
	return new_mem
#####################################################################

def generate_piece(piece_names):
	return random.choice(piece_names)

#####################################################################

def rotate(piece): #ROTATE 90 degrees to the right
	return list(list(x)[::-1] for x in zip(*piece))

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
	pos_x = left + cubeSize*col
	pos_y = top + cubeSize*row
	pygame.draw.rect(DISPLAYSURF, GREEN, (pos_x, pos_y, 20, 20))
	pygame.draw.rect(DISPLAYSURF, BLUE, (pos_x+1, pos_y+1, 18, 18))

#####################################################################

def draw_laid_cubes(mem):
	for x in range(0, lines):
		for y in range(0, lineWidth):
			if (mem[x][y]):
				draw_cube(y, x)

#####################################################################

def draw_piece(piece, col, row):
	for i in range(0, len(piece)):
		for j in range(0, len(piece)):
			if (piece[j][i]==1):
				draw_cube(col+i, row+j)

#####################################################################

def draw_future_pieces():
	row = 0
	col = lineWidth + 2
	for i in range(0, len(piece_stack)):
		draw_piece(piece_stack[i], col, row)
		row += 5

#####################################################################

def draw():
	global memory, piece_position, piece_current
	DISPLAYSURF.fill(BLACK)
	draw_playArea()
	draw_laid_cubes(memory)
	draw_future_pieces()
	draw_piece(piece_current, piece_position[1], piece_position[0])

#####################################################################

def contact(mem, pos, piece): # pos: line, col ; mem: line, col
	length = len(piece)
	for i in range(0, length):
		for j in range(0, length):
			row = pos[0]+ j
			col = pos[1]+ i
			#print(i, j, line, pos)
			if (piece[j][i]==1):
				if ((row + 1 == lines) or (mem[row+1][col])): #there's SOMETHING BELOW, BLOCKS IT IN PLACE
					print("THERE'S SOMETHING BELLOW")
					return 1		
				elif ((col + 1 >= lineWidth) or (mem[row][col+1])):
					#print("THERE'S SOMETHING TO THE RIGHT")
					return 2	
				elif ((col - 1 < 0) or (mem[row][col-1])):
					#print("THERE'S SOMETHING TO THE LEFT")
					return 3	
				elif (row > 0 and mem[row-1][col]):
					#print("THERE'S SOMETHING ABOVE")
					return 4	
	return 0

#####################################################################

def update_memory(old_memory):
	global memory, piece_position, piece_current
	new_mem = [[False for x in range(lineWidth)] for y in range(lines)] 
	for k in range(0, lines-1):
		for j in range(0, lineWidth):
			new_mem[k][j] = old_memory[k][j]

	for x in range(0, len(piece_current)):
		for z in range(0, len(piece_current)):
			col = piece_position[0]+x
			row = piece_position[1]+z
			if (piece_current[x][z]==1):
				new_mem[col][row] = True
			
	return new_mem

#####################################################################

def init_glob_variables():
	global memory, level, score, piece_position, piece_stack, piece_current
	memory = [[False for x in range(lineWidth)] for y in range(lines)] 
	level = 0
	score = 0
	piece_position = [0,6] #line, col
	piece_stack = []
	piece_current = generate_piece(piece_names)
	for x in range(0, 4):
		piece_stack.append(generate_piece(piece_names))

#####################################################################

def spawn_new_piece():
	global time_mark, memory, piece_current, piece_stack, piece_position
	time_mark = time_current
	memory = update_memory(memory)
	piece_current = piece_stack.pop(0)
	piece_stack.append(generate_piece(piece_names))
	piece_position = [0,6]
	
#####################################################################
#								MAIN 								#
#####################################################################

while gameloop: #main loop
	#INPUT
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			print("Exit")
			gameloop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
				print("Exit")
				gameloop = False
			if event.key == pygame.K_w:
				piece_current = rotate(piece_current)
			if event.key == pygame.K_s: 
				if contact(memory, piece_position, piece_current) != 1:
					piece_position[0] = piece_position[0]+1
					print("Post: ", piece_position)
				elif contact(memory, piece_position, piece_current) == 1:
					spawn_new_piece()
			if event.key == pygame.K_d and contact(memory, piece_position, piece_current) != 2:
				piece_position[1] = piece_position[1]+1
			if event.key == pygame.K_a and contact(memory, piece_position, piece_current) != 3:
				piece_position[1] = piece_position[1]-1
			if event.key == pygame.K_r:
				start = True
			if event.key == pygame.K_SPACE:
				while contact(memory, piece_position, piece_current) != 1:
					piece_position[0] = piece_position[0]+1
				spawn_new_piece()

	#INITIALISATION
	if (start):
		start = False
		init_glob_variables();

	#VISUALIZATION
	if(level != -1):
		time_current = pygame.time.get_ticks()
		if ((time_current - time_mark) >= (1000 * ticks_per_level[level])):
			if(contact(memory, piece_position, piece_current) != 1):
				piece_position[0] = piece_position[0]+1
				time_mark = time_current
			else:
				spawn_new_piece()

		draw()

		if is_Line_Empty(memory[0][:]): #if game_over, aka something in line 21), LEVEL = -1
			level = -1
			print("GAME_OVER")
		pygame.display.update()
		fpsClock.tick(FPS)
		pygame.event.pump()

	#if (level == -1): #GAME_OVER
		#DISPLAY RESTART OPTIONS
#end while