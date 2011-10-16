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
        self.mute = False
        self.queue = set()
        self.sounds = {
            'bark':      getSound("bark.ogg", 0.7),
            'blast':     getSound("blast.ogg", 0.7),
            'drop':      getSound("drop.ogg", 0.2),
            'flyaway':   getSound("flyaway.ogg", 1.0),
            'gameover':  getSound("gameover.ogg", 0.7),
            'hit':       getSound("hit.ogg", 1.0),
            'nextround': getSound("next-round.ogg", 1.0),
            'point':     getSound("point.ogg", 1.0),
            'quack':     getSound("quack.ogg", 0.7)
        }

    def enqueue(self, sound):
        self.queue.add(self.sounds[sound])

    def flush(self):
        for sound in self.queue:
            if not self.mute:
                sound.play()
        self.queue.clear()

    def toggleSound(self):
        self.mute = not self.mute
        if self.mute:
            pygame.mixer.stop()
