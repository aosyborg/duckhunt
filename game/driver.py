import os, sys, time
import pygame
import registry, states, sounds

class Driver(object):
    def __init__(self, surface):
        # Set a global registry
        self.registry = registry.Registry()
        self.registry.set('surface', surface)
        self.registry.set('soundHandler', sounds.SoundHandler())
        self.registry.set('controlImgs', pygame.image.load(os.path.join ('media', 'controls.png')))
        self.registry.set('sprites', pygame.image.load(os.path.join ('media', 'sprites.png')))
        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the game
        self.state = states.StartState(self.registry)
        self.state = self.state.start()

    def handleEvent(self, event):
        self.state.execute(event)

    def update(self):
        newState = self.state.update()

        if newState:
            self.state = newState

    def render(self):
        self.state.render()
        self.registry.get('soundHandler').flush()
