import pygame as py
import math 

py.init()
print("Hello Cruel World...")

#MODE
state = 0

#CAR SETTINGS
INIT_X = 64
INIT_Y = 16
WIDTH = 16
HEIGHT = 16
vel = 4
rot = 0
rot_speed = 10

#COLORS
BLACK = (0,0,0)
LIGHTGREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0) 
BLUE = (0,0,255)
WHITE = (255,255,255)
PURPLE = (102,0,102)
LIGHTBLUE = (153,255,255)
LIGHTYELLOW = (248,252,158)

#COLIDE_STUFF
colide_markers = [1,1,1,1,1]
colide_distances = [48,48,48,48,48]
COL_MULTI = (2,1,0,-1,-2)
COLIDE_CIRCLES_RADIUS = 3

#WINDOW SETTINGS
WIN_WIDTH = 736
WIN_HEIGHT = 736
WIN = py.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
py.display.set_caption("Autonomous_Car")
FPS = 30
CLOCK = py.time.Clock()
TILESIZE = 16
GRIDWIDTH = WIN_WIDTH / TILESIZE
GRIDHEIGHT = WIN_HEIGHT / TILESIZE
#TRAINING CIRCUIT
TRAIN_WALLS = [(0,1,1,6),(0,2,7,2),(0,3,9,4),(1,4,10,10),(1,14,9,2),(0,16,7,2),(1,17,6,5),(0,6,1,4),(1,7,5,5),(0,12,3,2),(0,13,1,2)
              ,(1,14,1,11),(1,25,2,4),(0,27,3,6),(0,26,9,1),(1,24,10,2),(1,20,11,4),(0,19,12,2),(1,18,14,1),(1,7,15,11),(0,2,13,2)
              ,(0,6,16,22),(0,1,15,26),(0,2,41,2),(0,3,43,1),(1,4,44,4),(0,8,42,2),(0,9,40,2),(0,10,21,19),(1,11,20,10),(0,21,18,2)
              ,(0,22,16,2),(1,23,15,5),(0,28,13,2),(1,29,12,10),(1,29,1,14),(0,31,5,7),(0,35,2,6),(0,39,5,7),(0,43,2,13),(0,42,15,2)
              ,(1,32,17,12),(0,31,18,2),(1,26,20,5),(0,25,21,3),(1,15,24,10),(0,14,25,13),(0,11,40,2),(0,12,42,2),(1,13,44,4),(1,17,43,1)
              ,(0,18,41,2),(0,19,29,12),(1,20,28,9),(0,29,25,5),(1,30,24,10),(0,35,22,2),(1,36,21,4),(0,40,22,15),(0,44,18,23),(0,43,41,2)
              ,(1,42,43,1),(1,38,44,4),(0,37,42,2),(0,36,40,2),(0,35,29,12),(0,34,40,2),(0,33,42,2),(1,29,44,4),(0,28,42,2),(0,27,33,9)
              ,(0,31,25,12),(1,30,29,1),(0,26,42,2),(1,22,44,4),(1,21,43,1),(0,20,41,2),(0,23,29,10)]

# CAR "IMAGE"
image_car = py.Surface((WIDTH,HEIGHT))
image_car.set_colorkey(BLACK)
image_car.fill(BLUE)
image_copy = image_car.copy()
image_copy.set_colorkey(BLACK)
rect = image_copy.get_rect()
rect.center = (INIT_X,INIT_Y)


loop = True
while loop:
	CLOCK.tick(FPS)
	WIN.fill(BLACK)
	#COPY_CAR_POSITION
	old_center = rect.center
	#DRAW_GRID
	for x_grid in range( 0, WIN_WIDTH, TILESIZE):
		py.draw.line(WIN, LIGHTGREY, (x_grid,0),(x_grid, WIN_HEIGHT))
	for y_grid in range ( 0, WIN_HEIGHT, TILESIZE):
		py.draw.line(WIN, LIGHTGREY, (0,y_grid), ( WIN_WIDTH, y_grid))
	#DRAW_WALLS
	if state == 0:
		py.draw.rect(WIN, LIGHTYELLOW, py.Rect(20*TILESIZE,29*TILESIZE,TILESIZE*3,TILESIZE*3))
		for wall in TRAIN_WALLS:
			if wall[0] == 0:
				py.draw.rect(WIN, PURPLE, py.Rect(wall[1]*TILESIZE,wall[2]*TILESIZE,TILESIZE,wall[3]*TILESIZE))
			else:
				py.draw.rect(WIN, PURPLE, py.Rect(wall[1]*TILESIZE,wall[2]*TILESIZE,wall[3]*TILESIZE, TILESIZE))
	#DRAW_AND_CHECK_COLIDE_MARKERS
	for colide_mar in range(0,5):
		temp_rot = math.radians(rot+(COL_MULTI[colide_mar]*45))
		temp = 9
		while (temp<33):
			temp_X = int(old_center[0] + (temp * math.sin(temp_rot)))
			temp_Y = int(old_center[1] + (temp * math.cos(temp_rot)))
			if(WIN.get_at((temp_X,temp_Y))) == LIGHTYELLOW and temp<20:
				#WON
				state = 1
				old_center = (INIT_X,INIT_Y)
				rot = 0
			elif(WIN.get_at((temp_X,temp_Y))) == PURPLE:
				colide_markers[colide_mar] = 0
				if(temp==9):
					old_center = (INIT_X,INIT_Y)
					rot = 0
				colide_distances[colide_mar] = temp
				break
			else:
				colide_markers[colide_mar] = 1
				temp+=1
		if colide_markers[colide_mar] == 0:
			py.draw.circle(WIN, RED, ( temp_X, temp_Y), COLIDE_CIRCLES_RADIUS)
		else:
			py.draw.circle(WIN, GREEN, ( temp_X, temp_Y), COLIDE_CIRCLES_RADIUS)
	#CLOSE_WINDOW
	for event in py.event.get():
		if event.type == py.QUIT:
			loop = False
	keys = py.key.get_pressed()
	#RESET
	if keys[py.K_r]:
		old_center = (INIT_X,INIT_Y)
		rot = 0
	#ROTATEs
	if keys[py.K_LEFT]:
		rot = (rot+rot_speed)%360 
	if keys[py.K_RIGHT]:
		rot = (rot-rot_speed)%360
	if keys[py.K_p]: 
		if state == 0:
			print("Trained")
		state += 1
	#Movement
	if state == 0:
		rot_radians = math.radians(rot)
		old_center = (old_center[0] + (vel * math.sin(rot_radians)),old_center[1] + (vel * math.cos(rot_radians)))
	#UPDATE CAR
	new_image = py.transform.rotate(image_car, rot)
	rect = new_image.get_rect()
	rect.center = old_center
	WIN.blit(new_image,rect)
	py.display.flip()
	py.display.update()
print("See You, Cruel World!")
py.quit()