import os, sys, time
import pygame
import gun, duck
from gun import Gun
from duck import Duck

HIT_POSITION = 245, 440
HIT_RECT = 0, 0, 287, 43
HIT_DUCK_POSITION = 329, 445
HIT_DUCK_WHITE_RECT = 217, 43, 19, 16
HIT_DUCK_RED_RECT = 199, 43, 19, 16
SCORE_POSITION = 620, 440
SCORE_RECT = 69, 43, 130, 43
FONT = os.path.join('media', 'arcadeclassic.ttf')
FONT_STARTING_POSITION = 730, 442
ROUND_POSITION = 60, 410
NOTICE_POSITION = 370, 120
NOTICE_RECT = 0, 86, 128, 63
NOTICE_WIDTH = 128
NOTICE_LINE_1_HEIGHT = 128
NOTICE_LINE_2_HEIGHT = 150

class Driver(object):
    def __init__(self, surface):
        self.surface = surface
        self.gun = Gun(surface)
        self.ducks = [Duck(surface), Duck(surface)]
        self.round = 1
        self.phase = 'gameover'
        self.score = 0
        self.timer = int(time.time())
        self.roundTime = 10 # Seconds in a round
        self.controlImgs = pygame.image.load(os.path.join('media', 'screenobjects.png'))
        self.hitDucks = [False for i in range(10)]
        self.hitDuckIndex = 0
        self.nextRoundSound = os.path.join('media', 'next-round.mp3')
        self.flyawaySound = os.path.join('media', 'flyaway.mp3')
        self.notices = ()
        self.event = None

    def handleEvent(self, event):
        self.event = event

        # If we are in the shooting phase, pass event off to the gun
        if event.type == pygame.MOUSEMOTION:
            self.gun.moveCrossHairs(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gunFired = self.gun.shoot()
            for duck in self.ducks:
                if gunFired:
                    if duck.isShot(event.pos):
                        self.score += 10
                        self.hitDucks[self.hitDuckIndex] = True
                        self.hitDuckIndex += 1
                else:
                    duck.flyOff = True

    def update(self):
        allDone = False

        # Update game based on phase
        if self.phase == 'start':
            self.startRound()
        elif self.phase == 'shoot':
            # Update all ducks
            for duck in self.ducks:
                duck.update(self.round)
            self.manageRound()
        elif self.phase == 'end':
            self.endRound()
        elif self.phase == 'gameover':
            self.gameOver()

    def render(self):
        # If there is a notice, display and return
        if len(self.notices) > 0:
            font = pygame.font.Font(FONT, 20)
            text = font.render(str(self.notices[0]), True, (255, 255, 255));
            x, y = NOTICE_POSITION
            x = x + (NOTICE_WIDTH - text.get_width()) / 2
            y = NOTICE_LINE_1_HEIGHT
            self.surface.blit(self.controlImgs, NOTICE_POSITION, NOTICE_RECT)
            self.surface.blit(text, (x, y));
            if len(self.notices) > 1:
                text = font.render(str(self.notices[1]), True, (255, 255, 255));
                x, y = NOTICE_POSITION
                x = x + (NOTICE_WIDTH - text.get_width()) / 2
                y = NOTICE_LINE_2_HEIGHT
                self.surface.blit(text, (x, y));

            return

        # Show the ducks
        for duck in self.ducks:
            duck.render()

        # Show round number
        font = pygame.font.Font(FONT, 20)
        text = font.render(("R= %d" % self.round), True, (154, 233, 0), (0, 0, 0));
        self.surface.blit(text, ROUND_POSITION);

        # Show the hit counter
        self.surface.blit(self.controlImgs, HIT_POSITION, HIT_RECT)
        startingX, startingY = HIT_DUCK_POSITION
        for i in range(10):
            x = startingX + (19 * i)
            y = startingY
            if self.hitDucks[i]:
                self.surface.blit(self.controlImgs, (x, y), HIT_DUCK_RED_RECT)
            else:
                self.surface.blit(self.controlImgs, (x, y), HIT_DUCK_WHITE_RECT)

        # Show the score
        self.surface.blit(self.controlImgs, SCORE_POSITION, SCORE_RECT)
        font = pygame.font.Font(FONT, 20)
        text = font.render(str(self.score), True, (255, 255, 255));
        x, y = FONT_STARTING_POSITION
        x -= text.get_width();
        self.surface.blit(text, (x,y));

        # Show the cross hairs
        self.gun.render()

    def manageRound(self):
        timer = int(time.time())

        # Check round end
        timesUp = (timer - self.timer) > self.roundTime
        if not (timesUp or (self.ducks[0].isFinished and self.ducks[1].isFinished)):
            return

        # Let any remaining ducks fly off
        for duck in self.ducks:
            if not duck.isFinished:
                duck.flyOff = True
                return

        # Check for fly offs and increment the index
        for duck in self.ducks:
            if not duck.isDead:
                self.hitDuckIndex += 1

        # Start new around if duck index is at the end
        if self.hitDuckIndex >= 9:
            pygame.mixer.music.load(self.nextRoundSound)
            pygame.mixer.music.play()
            self.phase = 'end'
            return

        # Populate screen with new ducks
        self.ducks = [Duck(self.surface), Duck(self.surface)]
        self.timer = int(time.time())
        self.gun.reloadIt()

    def startRound(self):
        timer = int(time.time())
        self.notices = ("ROUND", self.round)
        if (timer - self.timer) > 2:
            self.phase = 'shoot'
            self.notices = ()

    def endRound(self):
        # Pause game for new round music to play
        while pygame.mixer.music.get_busy():
            return

        # Count missed ducks - more than 4 and you're done
        missedCount = 0
        for i in self.hitDucks:
            if i == False:
                missedCount += 1
        if missedCount > 4:
            self.phase = "gameover"
            return

        # Prep for new round
        self.round += 1
        self.hitDucks = [False for i in range(10)]
        self.hitDuckIndex = 0
        self.phase = 'start'
        self.timer = int(time.time())

    def gameOver(self):
        self.notices = ("GAME OVER", "")
        # Start a new game
        if self.event.type == pygame.MOUSEBUTTONDOWN:
            self.ducks = [Duck(self.surface), Duck(self.surface)]
            self.round = 1
            self.phase = 'start'
            self.score = 0
            self.timer = int(time.time())
            self.hitDucks = [False for i in range(10)]
            self.hitDuckIndex = 0
            self.gun.reloadIt()
