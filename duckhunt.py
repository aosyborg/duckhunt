import os, sys
import pygame
import driver
from driver import Driver

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
TITLE = "Symons Media: Duck Hunt"
CLOCK_TICK = 50
BG_COLOR = 255, 255, 255

class Game(object):
    def __init__(self):
        self.running = True
        self.surface = None
        self.clock = pygame.time.Clock()
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        background = os.path.join('media', 'background.jpg')
        self.background = pygame.image.load(background)
        self.driver = None

    def init(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.mouse.set_visible(False)
        self.surface = pygame.display.set_mode(self.size)
        self.driver = Driver(self.surface)

    def handleEvent(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        else:
            self.driver.handleEvent(event)

    def loop(self):
        self.clock.tick(CLOCK_TICK)
        self.driver.update()

    def render(self):
        self.surface.blit(self.background, (0,0))
        self.driver.render()
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()
        sys.exit(0)

    def execute(self):
        self.init()

        while (self.running):
            for event in pygame.event.get():
                self.handleEvent(event)
            self.loop()
            self.render()

        self.cleanup()

if __name__ == "__main__":
    theGame = Game()
    theGame.execute()
