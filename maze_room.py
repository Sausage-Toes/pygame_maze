import pygame
import random
from Commodore_64_color_palettes import *
from datetime import datetime
random.seed(datetime.now())

pygame.init()

TITLE = "Maze Room"
BGCOLOR = BLACK #(0, 0, 0)
WALL_COLOR  =  CYAN #(170, 255, 238)
WALL_THIC = 9
PILLAR_COLOR = CYAN
PILLAR_RAD = 4
maze_width = 620
maze_height = 400
x0=10
y0=10

screen_width = 640 
screen_height = 480 
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(TITLE)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Clear the screen
screen.fill(BGCOLOR)
    
#draw room boarders
def draw_room_boarders():
    pygame.draw.line(screen, WALL_COLOR, [x0,y0],[x0 + (2*maze_width//5),y0], WALL_THIC)
    pygame.draw.line(screen, WALL_COLOR, [x0+ (3*maze_width//5),y0],[x0+  maze_width,y0], WALL_THIC)
    
    pygame.draw.line(screen, WALL_COLOR, [x0,y0],[x0, y0 + (maze_height//3)], WALL_THIC)
    pygame.draw.line(screen, WALL_COLOR, [x0+maze_width,y0],[x0+maze_width,y0+(maze_height//3)]
                 , WALL_THIC)
    
    pygame.draw.line(screen, WALL_COLOR, [x0,y0+(2*maze_height//3)],[x0,y0+maze_height]
                 , WALL_THIC)
    pygame.draw.line(screen, WALL_COLOR, [x0,y0+maze_height],[x0+(2*maze_width//5),y0+maze_height]
                 , WALL_THIC)

    pygame.draw.line(screen, WALL_COLOR, [x0+maze_width,y0+(2*maze_height//3)]
                 ,[x0+maze_width,y0+maze_height], WALL_THIC)
    pygame.draw.line(screen, WALL_COLOR, [x0+(3*maze_width//5),y0+maze_height]
                 ,[x0+maze_width,y0+maze_height], WALL_THIC)

    #doors
    #top
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 + (2*maze_width//5),y0],PILLAR_RAD , 0)
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 + (3*maze_width//5),y0],PILLAR_RAD , 0)
    #left
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 ,y0+(maze_height//3)],PILLAR_RAD , 0)
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 ,y0+(2*maze_height//3)],PILLAR_RAD , 0)
    #right
    pygame.draw.circle(screen, PILLAR_COLOR, [x0+maze_width ,y0+(maze_height//3)],PILLAR_RAD , 0)
    pygame.draw.circle(screen, PILLAR_COLOR, [x0+maze_width ,y0+(2*maze_height//3)],PILLAR_RAD , 0)
    #bottom
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 + (2*maze_width//5),y0+maze_height],PILLAR_RAD , 0)
    pygame.draw.circle(screen, PILLAR_COLOR, [x0 + (3*maze_width//5),y0+maze_height],PILLAR_RAD , 0)

def draw_maze():
    #draw maze walls
    x = (maze_width//5) 
    y = (maze_height//3) 
    for i in range(1,5):
        for j in range(1,3):
            #print (i,x,j,y)
            xd=x0 + i*x
            yd=y0 + j*y
            wall_dir = random.randrange(4)
            if wall_dir == 0:
                xd = x0 + i*x - maze_width//5
            if wall_dir == 1:
                yd = y0 + j*y + maze_height//3
            if wall_dir == 2:
                xd = x0 + i*x + maze_width//5
            if wall_dir == 3:
                yd = y0 + j*y - maze_height//3

            pygame.draw.line(screen, WALL_COLOR, [x0 + i*x,y0 + j*y],[xd,yd], WALL_THIC)

            pygame.draw.circle(screen, PILLAR_COLOR, [x0 + i*x,y0 + j*y],PILLAR_RAD, 0)

draw_room_boarders()
draw_maze()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Clear the screen
            screen.fill(BGCOLOR)
            draw_room_boarders()
            draw_maze()
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
