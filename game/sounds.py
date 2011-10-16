import os
import pygame

SOUNDS_DIR = "media"

def getSound(name, volume):
    soundPath = os.path.join(SOUNDS_DIR, name)
    sound = pygame.mixer.Sound(soundPath)
    sound.set_volume(volume)
    return sound

class SoundHandler:
    def __init__(self):
        self.queue = set()
        self.sounds = {
            'blast':     getSound("blast.ogg", 1.0),
            'drop':      getSound("drop.ogg", 0.7),
            'flyaway':   getSound("flyaway.ogg", 1.0),
            'hit':       getSound("hit.ogg", 1.0),
            'nextround': getSound("next-round.ogg", 1.0),
            'point':     getSound("point.ogg", 1.0),
            'quack':     getSound("quack.ogg", 0.7)
        }

    def enqueue(self, sound):
        self.queue.add(self.sounds[sound])

    def flush(self):
        for sound in self.queue:
            sound.play()
        self.queue.clear()
