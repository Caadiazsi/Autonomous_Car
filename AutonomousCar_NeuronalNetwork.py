import pygame as py
import math
from NeuralNetwork import DeepQLearning

def draw_grid(window, width,height,tilesize,color):
    for x_grid in range( 0, width+1, tilesize):
        py.draw.line(window, color, (x_grid,0),(x_grid, height))
    for y_grid in range ( 0, height+1, tilesize):
        py.draw.line(window, color, (0,y_grid), ( width, y_grid))

def draw_walls(window, tilesize, color, walls):
    for wall in walls:
        if wall[0] == 0:
            py.draw.rect(window, color, py.Rect(wall[1]*tilesize,wall[2]*tilesize,tilesize,wall[3]*tilesize))
        else:
            py.draw.rect(window, color, py.Rect(wall[1]*tilesize,wall[2]*tilesize,wall[3]*tilesize, tilesize))

def check_collide_distances(window, center, rot, color, coll_mult):
    collide_distances, collide_states = [0,0,0],[0,0,0]
    for collide_mar in range(0,3):
        temp_rot = math.radians(rot+(coll_mult[collide_mar]))
        temp = 9
        while (temp<33):
            temp_X = int(center[0] + (temp * math.sin(temp_rot)))
            temp_Y = int(center[1] + (temp * math.cos(temp_rot)))
            if(window.get_at((temp_X,temp_Y))) == color:
                collide_states[collide_mar] = 0
                collide_distances[collide_mar] = temp
                break
            else:
                collide_states[collide_mar] = 1
                temp+=1
        if collide_states[collide_mar] == 1:
            collide_distances[collide_mar] = 32
    return collide_states, collide_distances

def draw_sensors(window, center, rot, collide_distances, collide_states, collide_multip, ccr, color1, color2):
    for i in range(0,3):
        temp_rot = math.radians(rot+(collide_multip[i]))
        temp_X = int(center[0] + (collide_distances[i] * math.sin(temp_rot)))
        temp_Y = int(center[1] + (collide_distances[i] * math.cos(temp_rot)))
        if(collide_states[i]==0):
            py.draw.circle(window, color1, ( temp_X, temp_Y), ccr)
        else:
            py.draw.circle(window, color2, ( temp_X, temp_Y), ccr)

def check_collision(collide_distances, collide_states):
    for i in range(0,3):
        if collide_states[i]==0:
            if collide_distances[i]==9:
                return True
    return False

def movement(center, vel, rot,rot_speed, action):
    if action==1:
        rot = (rot+rot_speed)%360
    elif action ==2:
        rot = (rot-rot_speed)%360
    rot_radians = math.radians(rot)
    new_center = (center[0] + (vel * math.sin(rot_radians)),center[1] + (vel * math.cos(rot_radians)))
    return new_center, rot

def main():
    py.init()
    print("Hello Cruel World...")
    #CAR SETTINGS
    INIT_X,INIT_Y,WIDTH,HEIGHT,vel,rot,rot_speed = 64,32,16,16,4,0,20
    #COLORS
    BLACK,LIGHTGREY,RED,GREEN,BLUE = (0,0,0),(100,100,100),(255,0,0),(0,255,0),(0,0,255)
    WHITE,PURPLE,LIGHTBLUE,LIGHTYELLOW = (255,255,255),(102,0,102),(153,255,255),(248,252,158)
    #COLLIDE_STUFF
    collide_sensors = [1,1,1]
    collide_distances = [48,48,48]
    COLL_MULTI = (45,0,-45)
    COLLIDE_CIRCLES_RADIUS = 3
    #WINDOW SETTINGS
    WIN_WIDTH,WIN_HEIGHT,FPS,TILESIZE = 736,736,30,16
    WIN = py.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    py.display.set_caption("Autonomous_Car")
    CLOCK = py.time.Clock()
    GRIDWIDTH = WIN_WIDTH / TILESIZE
    GRIDHEIGHT = WIN_HEIGHT / TILESIZE
    #TRAINING CIRCUIT
    TRAIN_WALLS = [(1,1,1,6),(0,1,1,6),(0,2,7,2),(0,3,9,4),(1,4,10,10),(1,14,9,2),(0,16,7,2),(1,17,6,5),(0,6,1,4),(1,7,5,5),(0,12,3,2),(0,13,1,2)
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
    #NEURAL NETWORKS
    Network = DeepQLearning()
    loop = True
    while loop:
        CLOCK.tick(FPS)
        WIN.fill(BLACK)
	    #COPY_CAR_POSITION
        old_center = rect.center
        #DRAW_GRID
        draw_grid(WIN, WIN_WIDTH,WIN_HEIGHT,TILESIZE,LIGHTGREY)
        #DRAW_WALLS
        draw_walls(WIN,TILESIZE, PURPLE, TRAIN_WALLS)
        #THE_OBJECTIVE
        py.draw.rect(WIN, LIGHTYELLOW, py.Rect(20*TILESIZE,29*TILESIZE,TILESIZE*3,TILESIZE*3))
        #CHECK_COLIDE_MARKERS
        collide_sensors, collide_distances = check_collide_distances(WIN, old_center, rot, PURPLE, COLL_MULTI)
        ############################MADE A DECISION#########################################
        action = Network.actuar(collide_sensors)   #0-Seguir derecho. 1-Girar Not-Clockwise. 2-Girar Clockwise
        if action == 1:
            rot = rot - rot_speed
        elif action == 2:
            rot = rot + rot_speed
        #MOVE CAR
        old_center, rot = movement(rect.center, vel, rot, rot_speed, action)
        #DRAW_SENSORS
        draw_sensors(WIN, old_center, rot, collide_distances, collide_sensors, COLL_MULTI, COLLIDE_CIRCLES_RADIUS, RED, GREEN)
        #CHECK COLLISION
        collision = check_collision(collide_distances, collide_sensors)
        ##########################################CHECK REWARD########################################################
        last_reward = 0
        ######################################UPDATE NETWORK""""""""""""""""""""""""""
        #UPDATE CAR (RECT)
        new_image = py.transform.rotate(image_car, rot)
        rect = new_image.get_rect()
        rect.center = old_center
        WIN.blit(new_image,rect)
        #CLOSE_WINDOW
        for event in py.event.get():
            if event.type == py.QUIT:
                loop = False
        py.display.flip()
        py.display.update()
    print("See You, Cruel World!")
    py.quit()

if __name__ == '__main__':
    main()
