# importing pygame module
import pygame, random
from pygame import sprite

# initialize required components
pygame.init()

SCREEN_WIDTH = 606
SCREEN_HEIGHT = 606

# Player class
class Player(pygame.sprite.Sprite):
    
    # speed vectors
    change_x = 0
    change_y = 0
    
    def __init__(self, x, y, filename):
        super().__init__()
        self.image = pygame.image.load(filename).convert()
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

    # function that changes speed of sprite
    def changespeed(self, nx, ny):
        self.change_x += nx
        self.change_y += ny
    
    # function that updates position of player
    def update(self):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        self.rect.top = new_y

        # if player goes out of bound we rectify it
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.rect.left = old_x
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = old_y

        # collide = pygame.sprite.spritecollide(self, list, False)
        # if collide:
        #     self.rect.left = old_x
        #     self.rect.top = old_y


class Ghost(Player):
    # ghost will have a direction it is currently going in
    direction = 0

    # get the direction ghost is currently going in
    def get_direction(self):
        return self.direction

    # set the ghost's direction to new direction
    def set_direction(self, direction):
        self.direction = direction

    def update(self):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        self.rect.top = new_y

        # if ghost collides with edges,
        # we return that it has collided
        collide = False
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.rect.left = old_x
            collide = True
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = old_y
            collide = True
        # everthing is well and good then no need
        if collide:
            return True
        else:
            return False

# initializing our screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load icon and caption
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pacman")

# clock for framerate
clock = pygame.time.Clock()

def startGame():
    # different sprite groups
    all_sprite_list = pygame.sprite.RenderPlain()
    ghosts = pygame.sprite.RenderPlain()

    # instantiate player object
    player = Player(0, 0, "images/pacman.png")
    all_sprite_list.add(player)

    # initial ghost in game
    ghost = Ghost(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), "images/Blinky.png")
    ghosts.add(ghost)
    all_sprite_list.add(ghost)

    # creating event to multiply ghost every 30 seconds
    ADD_GHOST = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_GHOST, 5000)

    # ghost directions
    DC = [[-20, 0], [20, 0], [0, 20], [0, -20]]
    toggle = True

    # game loop
    run = True
    while run:
        for event in pygame.event.get():
            # window close button pressed ?
            # close the game
            if event.type == pygame.QUIT:
                run = False

            # increase speed to move when key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.changespeed(0, -30)
                if event.key == pygame.K_LEFT:
                    player.changespeed(-30, 0)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 30)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(30, 0)
               
            # reduce speed to stop when key up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.changespeed(0, 30)
                if event.key == pygame.K_LEFT:
                    player.changespeed(30, 0)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -30)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-30, 0)
            
            # add ghosts from all existing after certain time
            if event.type == ADD_GHOST:
                for ghost in ghosts:
                    new_ghost = Ghost(ghost.rect.left, ghost.rect.top, "images/Blinky.png")
                    new_ghost.direction = random.randint(0, 3)
                    ghosts.add(new_ghost)
                    all_sprite_list.add(new_ghost)

        # for now, ghosts just wiggles randomly and multiplies 
        # ghost movement tactic   
        for ghost in ghosts:
            # ghost moves by toggling speed + and -
            # we update each individually, if it collides we return false
            if toggle:
                ghost.changespeed(DC[ghost.direction][0], DC[ghost.direction][1])
                toggle = False
            else:
                ghost.changespeed(-DC[ghost.direction][0], -DC[ghost.direction][1])
                toggle = True
            if ghost.update():
                ghost.direction = random.randint(0, 3)

        # kill ghosts on their death
        pygame.sprite.spritecollide(player, ghosts, True)
        
        # if we kill all ghosts then you win, if they reach above certain number, you lose
        if len(ghosts) == 0:
            run = False
            break
        elif len(ghosts) >= 10:
            run = False
            break
    
        # update information change for player
        player.update()
        # CODE FOR DRAWING GOES HERE
        screen.fill((0, 0, 0))
        ghosts.draw(screen)
        all_sprite_list.draw(screen)
        # update changes this frame
        pygame.display.flip()

        # set framerate to 10
        clock.tick(10)
    return

startGame()

# uninitialize pygame
pygame.quit()