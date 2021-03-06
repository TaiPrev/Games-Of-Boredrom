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


ticks_per_level = [1.5, 1.45, 1.4, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1]

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
layPoints = 10
linePoints = 100
totalPoints = 0
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

def testPosition(temp): # piece_position: row, col ; memory: line, col
	global lineWidth, lines, memory, piece_current
	length = len(piece_current)
	for i in range(0, length):
		for j in range(0, length):
			row = temp[0] + j
			col = temp[1] + i
			if (col >= lineWidth or col < 0 or row > lines) or (piece_current[j][i]==1 and memory[row][col]):
				return False
	return True

#####################################################################

def realocateRecursive(queue):
	global lineWidth, lines, memory, piece_position, piece_current

	length = len(queue)
	if (length <= 0): return [0, 0]

	top = queue[0]
	temp = piece_position
	temp[0] = temp[0] + top[0]
	temp[1] = temp[1] + top[1]

	if testPosition(temp): return top

	if temp[0] > 0:
		up = [[top[0]-1, top[1]]]
		#print("up")
		queue = queue + up
	if temp[1] > 0:
		left = [[top[0], top[1]-1]]
		#print("left")
		queue = queue + left
	if temp[1] > lineWidth-1:
		right = [[top[0], top[1]+1]]
		#print("right")
		queue = queue + right

	length = len(queue)
	queue = queue[1:length]

	result = realocateRecursive(queue)

	return result

#####################################################################

def realocate():
	global lineWidth, lines, memory, piece_position, piece_current
	queue = [[0,0]]
	modifier = realocateRecursive(queue)
	if (modifier == [0, 0]): level = -1 #GAME OVER
	piece_position[0] = piece_position[0] + modifier[0]
	piece_position[1] = piece_position[1] + modifier[1]

#####################################################################

def rotate(): #ROTATE 90 degrees to the right
	global piece_current
	original = piece_current
	piece_current =  list(list(x)[::-1] for x in zip(*piece_current))
	if (overlap()):
		realocate()

#####################################################################

def draw_playArea():
	#X: 180 ; 420
	#Y: 300 ; 700
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, top-1), (left-1, bottom), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (right, top-1), (right, bottom), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, top-1), (right, top-1), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (left-1, bottom), (right, bottom), 1)

#####################################################################

def draw_outline():
	global piece_position, piece_current
	#X: 180 ; 420
	#Y: 300 ; 700
	length = len(piece_current)
	pos_x = left + cubeSize*piece_position[1]
	pos_y = top + cubeSize*piece_position[0]
	pos_xB = pos_x + length * cubeSize
	pos_yB = pos_y + length * cubeSize
	pygame.draw.line(DISPLAYSURF, WHITE, (pos_x-1, pos_y-1), (pos_x-1, pos_yB), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (pos_xB, pos_y-1), (pos_xB, pos_yB), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (pos_x-1, pos_y-1), (pos_xB, pos_y-1), 1)
	pygame.draw.line(DISPLAYSURF, WHITE, (pos_x-1, pos_yB), (pos_xB, pos_yB), 1)

#####################################################################

def draw_cube(col, row):
	global cubeSize
	pos_x = left + cubeSize*col
	pos_y = top + cubeSize*row
	pygame.draw.rect(DISPLAYSURF, GREEN, (pos_x, pos_y, 20, 20))
	pygame.draw.rect(DISPLAYSURF, BLUE, (pos_x+1, pos_y+1, 18, 18))

#####################################################################

def draw_laid_cubes():
	global lineWidth, lines, memory
	for x in range(0, lines):
		for y in range(0, lineWidth):
			if (memory[x][y]):
				draw_cube(y, x)

#####################################################################

def draw_piece(piece, col, row):
	for i in range(0, len(piece)):
		for j in range(0, len(piece)):
			if (piece[j][i]==1):
				draw_cube(col+i, row+j)

#####################################################################

def draw_future_pieces():
	global lineWidth, lines
	row = 0
	col = lineWidth + 2
	for i in range(0, len(piece_stack)):
		draw_piece(piece_stack[i], col, row)
		row += 5

#####################################################################

def draw_points():
	global totalPoints, DISPLAYSURF
	font = pygame.font.SysFont(None, 24)
	text = font.render(str(totalPoints), True, WHITE, None)
	DISPLAYSURF.blit(text, (20, 20))

#####################################################################

def draw():
	global memory, piece_position, piece_current
	DISPLAYSURF.fill(BLACK)
	draw_playArea()
	draw_laid_cubes()
	draw_future_pieces()
	draw_piece(piece_current, piece_position[1], piece_position[0])
	#draw_outline() #Only here for debugging purpouses
	draw_points()

#####################################################################

def contact_floor(): #Operation to check only for floor, optimized for that
	global lineWidth, lines, memory, piece_position, piece_current
	length = len(piece_current)
	for i in range(length-1, -1, -1):
		for j in range(length-1, -1, -1):
			row = piece_position[0] + j
			col = piece_position[1] + i
			if piece_current[j][i]==1 and ((row + 1 == lines) or (memory[row+1][col])):
				return 1

#####################################################################

def overlap(): #Operation to check only for floor, optimized for that
	global lineWidth, lines, memory, piece_position, piece_current
	length = len(piece_current)
	for i in range(length-1, -1, -1):
		for j in range(length-1, -1, -1):
			row = piece_position[0] + j
			col = piece_position[1] + i
			if piece_current[j][i]==1:
				if col < 0 or col >= lineWidth:
					return True
				elif row < 0 or row >= lines:
					return True
				elif memory[row][col]:
					return True
	return False

#####################################################################

def contact(): # piece_position: row, col ; memory: line, col
	global lineWidth, lines, memory, piece_position, piece_current
	length = len(piece_current)
	for j in range(0, length):
		for i in range(0, length):
			row = piece_position[0]+ j
			col = piece_position[1]+ i
			if (piece_current[j][i]==1):
				if ((row + 1 == lines) or (memory[row+1][col])): #there's SOMETHING BELOW
					return 1		
				elif ((col + 1 >= lineWidth) or (memory[row][col+1])): #THERE'S SOMETHING TO THE RIGHT
					return 2	
				elif ((col - 1 < 0) or (memory[row][col-1])): #THERE'S SOMETHING TO THE LEFT
					return 3	
				elif (row > 0 and memory[row-1][col]): #THERE'S SOMETHING TO THE ABOVE
					return 4
				elif(memory[row][col]): #THERE'S AN OVERLAP
					return 5
	return 0

#####################################################################

def update_memory():
	global lineWidth, lines, memory, piece_position, piece_current, totalPoints
	earnedPoints = layPoints
	completeLines = 0
	for x in range(0, len(piece_current)):
		for z in range(0, len(piece_current)):
			row = piece_position[0]+x
			col = piece_position[1]+z
			if piece_current[x][z]==1 and col < lineWidth and row < lines:
				memory[row][col] = True

	y = lines - 1
	while y >= 0:
		if (is_Line_Complete(memory[y])):
			memory.remove(memory[y])
			completeLines += 1
			earnedPoints += linePoints
			memory = [[False for x in range(lineWidth)]] + memory
			y += 1
		y -= 1

	earnedPoints += completeLines * earnedPoints

	totalPoints += earnedPoints
	#print(completeLines)
			
#####################################################################

def init_glob_variables():
	global lineWidth, lines, memory, level, score, piece_position, piece_stack, piece_current, totalPoints
	memory = [[False for x in range(lineWidth)] for y in range(lines)] 
	level = 0
	score = 0
	piece_position = [0,6] #line, col
	piece_stack = []
	piece_current = generate_piece(piece_names)
	totalPoints = 0
	for x in range(0, 4):
		piece_stack.append(generate_piece(piece_names))

#####################################################################

def spawn_new_piece():
	global time_mark, memory, piece_current, piece_stack, piece_position
	time_mark = time_current
	update_memory()
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
				rotate()
			if event.key == pygame.K_s: 
				if contact_floor() != 1:
					piece_position[0] = piece_position[0]+1
				elif contact_floor() == 1:
					spawn_new_piece()
			if event.key == pygame.K_d and contact() != 2:
				piece_position[1] = piece_position[1]+1
			if event.key == pygame.K_a and contact() != 3:
				piece_position[1] = piece_position[1]-1
			if event.key == pygame.K_r:
				start = True
			if event.key == pygame.K_SPACE:
				while contact_floor() != 1:
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
			if(contact_floor() != 1):
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
