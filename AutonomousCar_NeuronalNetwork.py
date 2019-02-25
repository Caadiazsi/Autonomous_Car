import pygame as py
import math
from NeuralNetwork import DeepQLearning
import random
from Funk import text_to_screen

def flip(p):
    if random.random() <= p:
        return "RANDOM" # RANDOM
    else:
        return "NETWORK" # NETWORK

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

def check_collide_distances(window, center, rot, color, coll_mult, sensor_distance):
    collide_distances, collide_states = [0,0,0,0,0],[0,0,0,0,0]
    for collide_mar in range(0,5):
        temp_rot = math.radians(rot+(coll_mult[collide_mar]))
        temp = 9
        while (temp<sensor_distance):
            temp_X = int(center[0] + (temp * math.sin(temp_rot)))
            temp_Y = int(center[1] + (temp * math.cos(temp_rot)))
            if temp_X>=0 and temp_X<= 736 and temp_Y>=0 and temp_Y<=736:
                if(window.get_at((temp_X,temp_Y))) == color:
                    collide_states[collide_mar] = 0
                    collide_distances[collide_mar] = temp
                    break
                else:
                    collide_states[collide_mar] = 1
                    temp+=1
            else:
                collide_states[collide_mar] = 0
                collide_distances[collide_mar] = temp
                break
        if collide_states[collide_mar] == 1:
            collide_distances[collide_mar] = sensor_distance
    return collide_states, collide_distances

def draw_sensors(window, center, rot, collide_distances, collide_states, collide_multip, ccr, color1, color2):
    for i in range(0,5):
        temp_rot = math.radians(rot+(collide_multip[i]))
        temp_X = int(center[0] + (collide_distances[i] * math.sin(temp_rot)))
        temp_Y = int(center[1] + (collide_distances[i] * math.cos(temp_rot)))
        if(collide_states[i]==0):
            py.draw.circle(window, color1, ( temp_X, temp_Y), ccr)
        else:
            py.draw.circle(window, color2, ( temp_X, temp_Y), ccr)

def check_collision(collide_distances, collide_states):
    for i in range(0,5):
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

def check_reward(old_distances, new_distances):
    ##MEJORAR: CUANDO SE MANTIENE DAR REWARD. DAR MAS REWARD AL ALEJARSE Y QUITAR MUCHO AL ACERCARSE
    old = 0
    new = 0
    for i in range (0,5):
        old = old + old_distances[i]
        new = new + new_distances[i]
    old = old/3
    new = new/3
    if old > new:
        return -80
    elif new > old:
        return 80
    else:
        return 100

def main():
    py.init()
    print("----------WELCOME TO HOT WHEELS AI----------")
    iterations = 1
    temp = 0
    state = "WAITING"
    final = False
    iper = 200
    #CAR SETTINGS
    INIT_X,INIT_Y,WIDTH,HEIGHT,vel,rot,rot_speed, sensor_distance = 64,32,16,16,6,0,20,45
    #COLORS
    BLACK,LIGHTGREY,RED,GREEN,BLUE = (0,0,0),(100,100,100),(255,0,0),(0,255,0),(0,0,255)
    WHITE,PURPLE,LIGHTBLUE,LIGHTYELLOW = (255,255,255),(102,0,102),(153,255,255),(248,252,158)
    #COLLIDE_STUFF
    collide_sensors = [1,1,1,1,1]
    collide_distances = [sensor_distance,sensor_distance,sensor_distance,sensor_distance,sensor_distance]
    temp_collide_sensors = [1,1,1,1,1]
    temp_collide_distances = [sensor_distance,sensor_distance,sensor_distance,sensor_distance,sensor_distance]
    COLL_MULTI = (90,45,0,-45,-90)
    COLLIDE_CIRCLES_RADIUS = 3
    #WINDOW SETTINGS
    WIN_WIDTH,WIN_HEIGHT,FPS,TILESIZE = 736,736,30,16
    WIN = py.display.set_mode((WIN_WIDTH+100,WIN_HEIGHT))
    py.display.set_caption("Autonomous_Car")
    CLOCK = py.time.Clock()
    GRIDWIDTH = WIN_WIDTH / TILESIZE
    GRIDHEIGHT = WIN_HEIGHT / TILESIZE
    #TRAINING CIRCUIT
    TRAIN_WALLS = [(1,1,1,6),(0,1,1,6),(0,2,7,2),(0,3,9,4),(1,4,10,10),(1,14,9,2),(0,16,7,2),(1,17,6,5),(0,6,1,4),(1,7,5,5),(0,12,3,2),(0,13,1,2)
                  ,(1,14,1,11),(1,25,2,4),(0,27,3,6),(0,26,9,1),(1,24,10,2),(1,20,11,4),(0,19,12,2),(1,18,14,1),(1,7,15,11),(0,2,13,2)
                  ,(0,6,16,22),(0,1,15,26),(0,2,41,2),(0,3,43,1),(1,4,43,4),(0,8,42,2),(0,9,40,2),(0,10,21,19),(1,11,20,10),(0,21,18,2)
                  ,(0,22,16,2),(1,23,15,5),(0,28,13,2),(1,29,12,10),(1,29,1,14),(0,31,5,7),(0,35,2,6),(0,39,5,7),(0,43,2,13),(0,42,15,2)
                  ,(1,32,17,12),(0,31,18,2),(1,26,20,5),(0,25,21,3),(1,15,24,10),(0,14,25,13),(0,11,40,2),(0,12,42,2),(1,13,43,4),(1,17,43,1)
                  ,(0,18,41,2),(0,19,29,12),(1,20,28,9),(0,29,25,5),(1,30,24,10),(0,35,22,2),(1,36,21,4),(0,40,22,15),(0,44,18,23),(0,43,41,2)
                  ,(1,42,43,1),(1,38,43,4),(0,37,42,2),(0,36,40,2),(0,35,29,12),(0,34,40,2),(0,33,42,2),(1,29,43,4),(0,28,42,2),(0,27,33,9)
                  ,(0,31,25,12),(1,30,29,1),(0,26,42,2),(1,22,43,4),(1,21,43,1),(0,20,41,2),(0,23,29,10)]
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
    epsilon = 1
    loop = True
    while loop:
        keys = py.key.get_pressed()
        if keys[py.K_s]:
            state = "TRAINING"
        if keys[py.K_c]:
            Network.cargar()
            state = "TESTING"
            epsilon = 0
        if state != "WAITING":
            if state == "TESTING" and keys[py.K_g]:
                Network.guardar()
            if keys[py.K_t]:  #TEST
                temp = epsilon
                epsilon = 0
                state = "TESTING"
            if keys[py.K_p]:
                epsilon = temp
                state = "TRAINING"
            if(state == "TRAINING"):
                if(iterations%iper==0):
                    iterations = 0
                    if epsilon >= 0.2:
                        epsilon = epsilon -0.1
                        if epsilon < 0.2:
                            state = "TESTING"
                            epsilon = 0
                iterations += 1
            CLOCK.tick(FPS)
            WIN.fill(BLACK)
    	    #COPY_CAR_POSITION
            old_center = rect.center
            #DRAW_GRID
            #draw_grid(WIN, WIN_WIDTH,WIN_HEIGHT,TILESIZE,LIGHTGREY)
            #DRAW_WALLS
            draw_walls(WIN,TILESIZE, PURPLE, TRAIN_WALLS)
            #THE_OBJECTIVE
            #py.draw.rect(WIN, LIGHTYELLOW, py.Rect(20*TILESIZE,29*TILESIZE,TILESIZE*3,TILESIZE*3))
            #CHECK_COLIDE_MARKERS
            collide_sensors, collide_distances = check_collide_distances(WIN, old_center, rot, PURPLE, COLL_MULTI, sensor_distance)
            ############################MADE A DECISION#########################################
            decision = flip(epsilon)
            if(decision=="RANDOM"):
                action = random.randint(0,2)
            elif(decision=="NETWORK"):
                action = Network.actuar(collide_sensors)   #0-Seguir derecho. 1-Girar Not-Clockwise. 2-Girar Clockwise
            #print(action)
            #MOVE CAR
            old_center, rot = movement(rect.center, vel, rot, rot_speed, action)
            temp_collide_sensors, temp_collide_distances = check_collide_distances(WIN, old_center, rot, PURPLE, COLL_MULTI, sensor_distance)
            #DRAW_SENSORS
            draw_sensors(WIN, old_center, rot, collide_distances, collide_sensors, COLL_MULTI, COLLIDE_CIRCLES_RADIUS, RED, GREEN)
            #CHECK COLLISION AND REWARD --- UPDATE NETWORK
            collision = check_collision(collide_distances, collide_sensors)
            if collision:
                old_center = (INIT_X,INIT_Y)
                rot = 0
                last_reward = -100
                final = True
                if state == "TRAINING":
                    Network.recordar(collide_distances, action, last_reward, temp_collide_distances, final)
                    Network.aprender()
            else:
                last_reward = check_reward(collide_distances, temp_collide_distances)
                final = False
                if state == "TRAINING":
                    Network.recordar(collide_distances, action, last_reward, temp_collide_distances, final)
            #UPDATE CAR (RECT)
            new_image = py.transform.rotate(image_car, rot)
            rect = new_image.get_rect()
            rect.center = old_center
            WIN.blit(new_image,rect)
        text_to_screen(WIN, epsilon, 720, 20)
        text_to_screen(WIN, iper-iterations, 720, 80)
        text_to_screen(WIN, state, 720, 140)

        #CLOSE_WINDOW
        for event in py.event.get():
            if event.type == py.QUIT:
                loop = False
        py.display.flip()
        py.display.update()
    print("----------------DRIVE SAFE!!----------------")
    py.quit()

if __name__ == '__main__':
    main()
