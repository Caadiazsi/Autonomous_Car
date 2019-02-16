import pygame as py
import math 

py.init()
print("Hello Cruel World...")

#CAR SETTINGS
INIT_X = 64
INIT_Y = 64
WIDTH = 32
HEIGHT = 32
vel = 5
rot = 0
rot_speed = 5
BLACK = (0,0,0)
LIGHTGREY = (100,100,100)
RED = (255,0,0)
GREEN = (0,255,0) 
BLUE = (0,0,255)
WHITE = (255,255,255)
PURPLE = (102,0,102)
LIGHTBLUE = (153,255,255)
colide_markers = [1,1,1,1,1]
COL_MULTI = (2,1,0,-1,-2)
COLIDE_CIRCLES_RADIUS = 3
#WINDOW SETTINGS
WIN_WIDTH = 768
WIN_HEIGHT = 768
WIN = py.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
py.display.set_caption("Autonomous_Car")
FPS = 30
CLOCK = py.time.Clock()
TILESIZE = 16
GRIDWIDTH = WIN_WIDTH / TILESIZE
GRIDHEIGHT = WIN_HEIGHT / TILESIZE

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
	#BORDERS
	py.draw.rect(WIN, PURPLE, py.Rect(0,0,(GRIDWIDTH)*TILESIZE,TILESIZE))
	py.draw.rect(WIN, PURPLE, py.Rect(0,TILESIZE,TILESIZE,(GRIDHEIGHT-1)*TILESIZE))
	py.draw.rect(WIN, PURPLE, py.Rect((GRIDWIDTH-1)*TILESIZE,TILESIZE,TILESIZE,(GRIDHEIGHT-1)*TILESIZE))
	py.draw.rect(WIN, PURPLE, py.Rect(TILESIZE,(GRIDHEIGHT-1)*TILESIZE,(GRIDWIDTH-2)*TILESIZE,TILESIZE))
	#DRAW_COLIDE_MARKERS
	for colide_mar in range(0,5):
		temp_rot = math.radians(rot+(COL_MULTI[colide_mar]*45))
		temp = 17
		while (temp<48):
			temp_X = int(old_center[0] + (temp * math.sin(temp_rot)))
			temp_Y = int(old_center[1] + (temp * math.cos(temp_rot)))
			if(WIN.get_at((temp_X,temp_Y))) == PURPLE:
				colide_markers[colide_mar] = 0
				if(temp==17):
					old_center = (INIT_X,INIT_Y)
					rot = 0
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
	#ROTATE
	if keys[py.K_LEFT]:
		rot = (rot+rot_speed)%360 
	if keys[py.K_RIGHT]:
		rot = (rot-rot_speed)%360 
	#GOFORWARD
	if keys[py.K_UP]:
		rot_radians = math.radians(rot)
		old_center = (old_center[0] + (vel * math.sin(rot_radians)),old_center[1] + (vel * math.cos(rot_radians)))
	#UPDATE CAR
	new_image = py.transform.rotate(image_car, rot)
	rect = new_image.get_rect()
	rect.center = old_center
	WIN.blit(new_image,rect)
	py.display.flip()
	py.display.update()
py.quit()
