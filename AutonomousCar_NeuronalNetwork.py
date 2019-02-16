import pygame as py
import math 

py.init()
print("Hello Cruel World...")

#CAR SETTINGS
INIT_X = 48
INIT_Y = 64
WIDTH = 32
HEIGHT = 64
vel = 5
rot = 0
rot_speed = 5
BLACK = (0,0,0)
RED = (255,0,0)
LIGHTGREY = (100,100,100)

#WINDOW SETTINGS
WIN_WIDTH = 768
WIN_HEIGHT = 768
WIN = py.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
py.display.set_caption("Autonomous_Car")
FPS = 30
CLOCK = py.time.Clock()
TILESIZE = 32
GRIDWIDTH = WIN_WIDTH / TILESIZE
GRIDHEIGHT = WIN_HEIGHT / TILESIZE

# CAR "IMAGE"
image_car = py.Surface((WIDTH,HEIGHT))
image_car.set_colorkey(BLACK)
image_car.fill(RED)
image_copy = image_car.copy()
image_copy.set_colorkey(BLACK)
rect = image_copy.get_rect()
rect.center = (INIT_X,INIT_Y)


loop = True
while loop:
	CLOCK.tick(FPS)
	WIN.fill(BLACK)
	#DRAW_GRID
	for x_grid in range( 0, WIN_WIDTH, TILESIZE):
		py.draw.line(WIN, LIGHTGREY, (x_grid,0),(x_grid, WIN_HEIGHT))
	for y_grid in range ( 0, WIN_HEIGHT, TILESIZE):
		py.draw.line(WIN, LIGHTGREY, (0,y_grid), ( WIN_WIDTH, y_grid))
	#CLOSE_WINDOW
	for event in py.event.get():
		if event.type == py.QUIT:
			loop = False
	keys = py.key.get_pressed()
	#COPY_CAR
	old_center = rect.center
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
