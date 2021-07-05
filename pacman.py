# importing pygame module
import pygame, random

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
    def update(self, pressed_keys):
        # we move player by arrow keys
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -15)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 15)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(15, 0)
        
        # this keeps player on the screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Ghost(Player):
    # ghost will have a direction it is currently going in
    direction = 0

    # get the direction ghost is currently going in
    def get_direction(self):
        return self.direction

    # set the ghost's direction to new direction
    def set_direction(self, direction):
        self.direction = direction

    def update(self, directions):
        self.rect.move_ip(directions[self.direction][0], directions[self.direction][1])
        collide = False
        if self.rect.left < 0:
            self.rect.left = 0
            collide = True
        if self.rect.top < 0:
            self.rect.top = 0
            collide = True
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            collide = True
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            collide = True
        return collide
        

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
    DC = [[-10, 0], [10, 0], [0, 10], [0, -10]]
    toggle = True

    # game loop
    run = True
    while run:
        for event in pygame.event.get():
            # window close button pressed ?
            # close the game
            if event.type == pygame.QUIT:
                run = False
            
            # add ghosts from all existing after certain time
            if event.type == ADD_GHOST:
                for ghost in ghosts:
                    new_ghost = Ghost(ghost.rect.left, ghost.rect.top, "images/Blinky.png")
                    new_ghost.set_direction(random.randint(0, 3))
                    ghosts.add(new_ghost)
                    all_sprite_list.add(new_ghost)

        # GHOST:
        # for now, ghosts just wiggles randomly and multiplies 
        # ghost movement tactic   
        for ghost in ghosts:
            # ghost moves by toggling speed + and -
            # we update each individually, if it collides we return false
            if ghost.update(DC):
                ghost.set_direction(random.randint(0, 3))

        # PLAYER:
        # player movement update based on pressed keys
        pressed_keys = pygame.key.get_pressed() 
        player.update(pressed_keys)  

        # kill ghosts on their death
        pygame.sprite.spritecollide(player, ghosts, True)
        
        # GAME exit conditions upon some conclusion
        if len(ghosts) == 0:
            run = False
            break
        elif len(ghosts) >= 10:
            run = False
            break

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