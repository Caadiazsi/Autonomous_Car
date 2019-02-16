import pygame as py
import math 
py.init()
print("Hello Cruel World...")
win = py.display.set_mode((500,500))
py.display.set_caption("Autonomous_Car")
FPS = 30
clock = py.time.Clock()

#CAR SETTINGS
width = 20
height = 40
vel = 5
rot = 0
rot_speed = 5

BLACK = (0,0,0)
RED = (255,0,0)

# CAR
image_car = py.Surface((width,height))
image_car.set_colorkey(BLACK)
image_car.fill(RED)
image_copy = image_car.copy()
image_copy.set_colorkey(BLACK)
rect = image_copy.get_rect()
rect.center = (50,40)
loop = True
while loop:
	clock.tick(FPS)
	win.fill(BLACK)
	for event in py.event.get():
		if event.type == py.QUIT:
			loop = False
	keys = py.key.get_pressed()
	old_center = rect.center
	#RESET
	if keys[py.K_r]:
		old_center = (50,40)
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
	new_image = py.transform.rotate(image_car, rot)
	rect = new_image.get_rect()
	rect.center = old_center
	win.blit(new_image,rect)
	py.display.flip()
	py.display.update()
py.quit()
