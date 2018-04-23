import pygame
import random
from Commodore_64_color_palettes import *
from datetime import datetime
random.seed(datetime.now())

pygame.init()
TITLE = "Wall Sprites"
BGCOLOR = BLACK #(0, 0, 0)
WALL_COLOR  =  CYAN #(170, 255, 238)
PLAYER_COLOR = WHITE #(255, 255, 255)

screen_width = 640 
screen_height = 480 
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption(TITLE)

#Offset to Origin (0,0)
x0=10
y0=10

wall_width = 10
player_size = 15
player_speed =  3

maze_width = screen_width - (2 * x0)
maze_height = screen_height - screen_height//6


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        
        # Call the parent's constructor
        super().__init__()

        if width < 0:
            x = x + width + wall_width
            width = abs(width) 
        if height < 0:
            y = y + height + wall_width
            height = abs(height)
            
        # Make a wall surface of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(WALL_COLOR)

        # Make top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Room(object):
    
    # Each room has a list of walls, and of enemy sprites.
    wall_list = None
    enemy_sprites = None
        
    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.add_boarder_walls()
        self.add_maze_walls()
    
    def  add_boarder_walls(self):
        wall = Wall(x0,y0,(2*maze_width//5),wall_width)
        self.wall_list.add(wall)
        wall = Wall(x0+(3*maze_width//5),y0,(2*maze_width//5),wall_width)
        self.wall_list.add(wall)

        wall = Wall(x0, y0, wall_width, (maze_height//3))
        self.wall_list.add(wall)
        wall = Wall(x0, y0+(2*maze_height//3)-wall_width, wall_width
                    , (maze_height//3))
        self.wall_list.add(wall)

        wall = Wall(x0+maze_width-wall_width, y0, wall_width, (maze_height//3))
        self.wall_list.add(wall)
        wall = Wall(x0+maze_width-wall_width, y0+(2*maze_height//3)-wall_width
                    , wall_width, (maze_height//3))
        self.wall_list.add(wall)

        wall = Wall(x0,y0+maze_height-2*wall_width,(2*maze_width//5)
                    ,wall_width)
        self.wall_list.add(wall)
        wall = Wall(x0+(3*maze_width//5),y0+maze_height-2*wall_width
                    ,(2*maze_width//5),wall_width)
        self.wall_list.add(wall)        
    
    def add_maze_walls(self):
        x = (maze_width//5) 
        y = (maze_height//3)
        
        for i in range(1,5):
            for j in range(1,3):
                wall_dir = random.randrange(4)
                xd = wall_width
                yd = wall_width
                if wall_dir == 0:
                    xd = -(maze_width//5)
                if wall_dir == 1:
                    yd = maze_height//3
                if wall_dir == 2:
                    xd = maze_width//5
                if wall_dir == 3:
                    yd = -(maze_height//3)
                    
                wall = Wall(x0 +i*x , y0 + j*y -wall_width, xd, yd)
                self.wall_list.add(wall)
        


class Player(pygame.sprite.Sprite):

    # Set speed vector
    change_x = 0
    change_y = 0

    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([player_size, player_size])
        self.image.fill(PLAYER_COLOR)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def changespeed(self, x, y):
        #Change the speed of the player. Called with a keypress. """
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom



def draw_text(text, size, col, x, y):
    # utility function to draw text on screen
    #font_name = pygame.font.match_font('arial')
    #font = pygame.font.Font(font_name, size)
    font = pygame.font.Font('Fixedsys500c.ttf', size)
    text_surface = font.render(text, True, col)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    
# for all the connected joysticks
joysticks = []
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize them all (-1 means loop forever)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print ("Detected joystick '", joysticks[-1].get_name() ,"'")
    
# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Clear the screen
screen.fill(BGCOLOR)

player = Player(x0+player_size*3, y0+ (maze_height//2) -player_size)
movingsprites = pygame.sprite.Group()
movingsprites.add(player)

rooms = []
for i in range(0,256):
    room = Room()
    rooms.append(room)

room_index = 0
current_room = rooms[room_index]


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
            
        if event.type == pygame.JOYAXISMOTION:
            joy_name = joysticks[event.joy].get_name().strip()
            joy_x = round(joysticks[event.joy].get_axis(0))
            joy_y = round(joysticks[event.joy].get_axis(1))
            player.change_x = joy_x * player_speed
            player.change_y = joy_y * player_speed

                        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-1 * player_speed, 0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(1 * player_speed, 0)
            if event.key == pygame.K_UP:
                player.changespeed(0, -1 * player_speed)
            if event.key == pygame.K_DOWN:
                player.changespeed(0, 1 * player_speed)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(1 * player_speed, 0)
            if event.key == pygame.K_RIGHT:
                player.changespeed(-1 * player_speed, 0)
            if event.key == pygame.K_UP:
                player.changespeed(0, 1 * player_speed)
            if event.key == pygame.K_DOWN:
                player.changespeed(0, -1 * player_speed)

    player.move(current_room.wall_list)

    #map logic 256 rooms total 4 floors 64 rooms per floor
    if player.rect.x < x0:
        if room_index%64 == 0:
            room_index = room_index + 64
        room_index = room_index - 1    
        player.rect.x = maze_width - player_size
        current_room = rooms[room_index]
    if player.rect.x > maze_width:
        room_index = room_index + 1
        if room_index%64 == 0:
            room_index = room_index - 64
        player.rect.x = x0 + player_size
        current_room = rooms[room_index]
    if player.rect.y < y0:
        room_index = room_index - 64
        if room_index < 0:
            room_index = 256 - abs(room_index)
        player.rect.y = maze_height - player_size
        current_room = rooms[room_index]
    if player.rect.y > maze_height - player_size:
        room_index = room_index + 64
        if room_index > 255:
            room_index = room_index  - 256
        player.rect.y = y0 + player_size
        current_room = rooms[room_index]
    
    screen.fill(BGCOLOR)
    movingsprites.draw(screen)
    current_room.wall_list.draw(screen)
    txt = "Room: {0}".format(room_index)
    draw_text(txt, 25, WHITE, x0, maze_height + y0)
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
