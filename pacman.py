# importing pygame module
import pygame

# initialize required components
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

    # # change the speed of the player
    # # incase we want to increase or decrease speed
    # def changeSpeed(self, nx, ny):
    #     self.change_x += nx
    #     self.change_y += ny
    
    # update position of the player
    # Find a new position for the player
    def update(self, pressed_keys):
        # Get the old position, in case we need to go back to it
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -30)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-30, 0)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 30)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(30, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# load icon and caption
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pacman")

# clock for framerate
clock = pygame.time.Clock()

def startGame():
    # instantiate player object
    player = Player(0, 0, "images/pacman.png")
    sprite_list = pygame.sprite.RenderPlain()
    sprite_list.add(player)
    # game loop
    run = True
    while run:
        for event in pygame.event.get():
            # window close button pressed ?
            # close the game
            if event.type == pygame.QUIT:
                run = False

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        # CODE FOR DRAWING GOES HERE
        screen.fill((0, 0, 0))
        sprite_list.draw(screen)
        # update changes this frame
        pygame.display.flip()

        # set framerate to 10
        clock.tick(10)
    return

startGame()

# uninitialize pygame
pygame.quit()