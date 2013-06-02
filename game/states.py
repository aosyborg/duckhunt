import os, time
import pygame
import sounds
from registry import adjpos, adjrect, adjwidth, adjheight
from gun import Gun
from duck import Duck

DOG_POSITION = adjpos (250, 350)
DOG_FRAME = adjpos (122, 110)
DOG_REPORT_POSITION = adjpos (450, 325)
DOG_LAUGH_RECT = adjrect (385, 120, 80, 85)
DOG_ONE_DUCK_RECT = adjrect (650, 0, 100, 100)
DOG_TWO_DUCKS_RECT = adjrect (630, 115, 120, 100)
HIT_POSITION = adjpos (245, 440)
HIT_RECT = adjrect (0, 0, 287, 43)
HIT_DUCK_POSITION = adjpos (329, 445)
HIT_DUCK_WHITE_RECT = adjrect (218, 44, 18, 15)
HIT_DUCK_RED_RECT = adjrect (200, 44, 18, 15)
SCORE_POSITION = adjpos (620, 440)
SCORE_RECT = adjrect (69, 43, 130, 43)
FONT = os.path.join('media', 'arcadeclassic.ttf')
FONT_STARTING_POSITION = adjpos (730, 442)
FONT_GREEN = 154, 233, 0
FONT_BLACK = 0, 0, 0
FONT_WHITE = 255, 255, 255
ROUND_POSITION = adjpos (60, 410)
SHOT_BG_POSITION = adjpos (60, 440)
SHOT_POSITION = adjpos (60, 440)
SHOT_RECT = adjrect (0, 43, 70, 43)
BULLET_RECT = adjrect (200, 59, 13, 17)
NOTICE_POSITION = adjpos (370, 120)
NOTICE_RECT = adjrect (0, 86, 128, 63)
NOTICE_WIDTH = adjwidth (128)
NOTICE_LINE_1_HEIGHT = adjheight (128)
NOTICE_LINE_2_HEIGHT = adjwidth (150)

registry = None

class BaseState(object):
    def __init__(self):
        global registry
        self.registry = registry
        self.timer = int(time.time())
        self.notices = set()
        self.gun = Gun(self.registry)
        self.hitDucks = [False for i in range(10)]
        self.hitDuckIndex = 0

    def renderNotices(self):
        if len(self.notices) is 0:
            return
        elif len(self.notices) is 1:
            self.notices.add("")

        surface = self.registry.get('surface')
        controlImgs = self.registry.get('controlImgs')
        font = pygame.font.Font(FONT, adjheight (20))
        line1 = font.render(str(self.notices[0]), True, (255, 255, 255))
        line2 = font.render(str(self.notices[1]), True, (255, 255, 255))
        x, y = NOTICE_POSITION
        x1 = x + (NOTICE_WIDTH - line1.get_width()) / 2
        x2 = x + (NOTICE_WIDTH - line2.get_width()) / 2
        surface.blit(controlImgs, NOTICE_POSITION, NOTICE_RECT)
        surface.blit(line1, (x1, NOTICE_LINE_1_HEIGHT))
        surface.blit(line2, (x2, NOTICE_LINE_2_HEIGHT))

    def renderControls(self):
        img = self.registry.get('controlImgs')
        surface = self.registry.get('surface')
        round = self.registry.get('round')
        controlImgs = self.registry.get('controlImgs')

        # Show round number
        font = pygame.font.Font(FONT, adjheight (20))
        text = font.render(("R= %d" % round), True, FONT_GREEN, FONT_BLACK);
        surface.blit(text, ROUND_POSITION);

        # Show the bullets
        startingX, startingY = SHOT_POSITION
        surface.blit(controlImgs, SHOT_POSITION, SHOT_RECT)
        for i in range(self.gun.rounds):
            x = startingX + adjwidth (10) + adjwidth (i * 18)
            y = startingY + adjheight (5)
            surface.blit(controlImgs, (x, y), BULLET_RECT)

        # Show the hit counter
        surface.blit(controlImgs, HIT_POSITION, HIT_RECT)
        startingX, startingY = HIT_DUCK_POSITION
        for i in range(10):
            x = startingX + adjwidth (i * 18)
            y = startingY
            if self.hitDucks[i]:
                surface.blit(img, (x, y), HIT_DUCK_RED_RECT)
            else:
                surface.blit(img, (x, y), HIT_DUCK_WHITE_RECT)

        # Show the score
        surface.blit(img, SCORE_POSITION, SCORE_RECT)
        font = pygame.font.Font(FONT, adjheight (20))
        text = font.render(str(self.registry.get('score')), True, FONT_WHITE);
        x, y = FONT_STARTING_POSITION
        x -= text.get_width();
        surface.blit(text, (x,y));

class StartState(BaseState):
    def __init__(self, reg):
        global registry
        registry = reg

    def start(self):
        return RoundStartState()

class RoundStartState(BaseState):
    def __init__(self):
        super(RoundStartState, self).__init__()
        self.frame = 1
        self.animationFrame = 0
        self.animationDelay = 10
        self.dogPosition = DOG_POSITION
        self.barkCount = 0

    def execute(self, event):
        pass

    def update(self):
        timer = int(time.time())

        # The whole animation only takes two seconds so move to play state after its done
        if (timer - self.timer) > 2:
            self.showNotice = False
            return PlayState()

        # Update frame count and set notice
        self.notices = ("ROUND", self.registry.get('round'))
        self.frame += 1

    def render(self):
        timer = int(time.time())
        surface = self.registry.get('surface')
        sprites = self.registry.get('sprites')
        x, y = self.dogPosition
        width, height = DOG_FRAME

        # Always have round + controls
        self.renderNotices()
        self.renderControls()

        # Update animation frame
        if (self.frame % 15) == 0:
            self.animationFrame += 1

        # First the dog walks/sniffs
        if self.animationFrame < 5:
            x += 1
            self.dogPosition = (x, y)
            rect = ((width * self.animationFrame), 0, width, height)

        # Then the dog jumps
        else:
            self.animationDelay = 16
            animationFrame = self.animationFrame % 5
            rect = ((width * animationFrame), height, width, height)

            # Trigger barking
            if (self.barkCount < 2) and not pygame.mixer.get_busy():
                self.registry.get('soundHandler').enqueue('bark')
                self.barkCount += 1

            # First Jump frame
            if (animationFrame == 1):
                self.dogPosition = (x + adjwidth (5)), (y - adjheight (10))

            # Second jump frame
            elif (animationFrame == 2):
                self.dogPosition = (x + adjwidth (5)), (y + adjheight (5))

            elif (animationFrame > 2):
                return # Animation is over

        # Add the dog
        surface.blit(sprites, self.dogPosition, rect)

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.ducks = [Duck(self.registry), Duck(self.registry)]
        self.roundTime = 10 # Seconds in a round
        self.frame = 0
        self.dogCanComeOut = False
        self.dogPosition = DOG_REPORT_POSITION
        self.dogdy = 5

    def execute(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.gun.moveCrossHairs(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            hasFired = self.gun.shoot()
            for duck in self.ducks:
                if hasFired and duck.isShot(event.pos):
                    self.registry.set('score', self.registry.get('score') + 10)
                    self.hitDucks[self.hitDuckIndex] = True
                    self.hitDuckIndex += 1
                elif not duck.isDead and self.gun.rounds <= 0:
                     duck.flyOff = True

    def update(self):
        timer = int(time.time())

        # Don't update anything if running dog sequences
        if self.dogCanComeOut:
            return

        # Update the ducks
        for duck in self.ducks:
            duck.update()

        # Check round end
        timesUp = (timer - self.timer) > self.roundTime
        if not (timesUp or (self.ducks[0].isFinished and self.ducks[1].isFinished)):
            return None

        # Let any remaining ducks fly off
        for duck in self.ducks:
            if not duck.isFinished and not duck.isDead:
                duck.flyOff = True
                return None

        # Check for fly offs and increment the index
        for duck in self.ducks:
            if not duck.isDead:
                self.hitDuckIndex += 1

        # Start new around if duck index is at the end
        if self.hitDuckIndex >= 9:
            return RoundEndState(self.hitDucks)

        self.dogCanComeOut = True

    def render(self):
        timer = int(time.time())
        surface = self.registry.get('surface')
        sprites = self.registry.get('sprites')

        # Show the controls
        self.renderControls()

        # Show the ducks
        for duck in self.ducks:
            duck.render()

        # Show the dog
        if self.dogCanComeOut:
            self.frame += 3
            ducksShot = 0
            for duck in self.ducks:
                if duck.isDead:
                    ducksShot += 1

            # One duck shot
            if ducksShot == 1:
                x2, y2, width, height = DOG_ONE_DUCK_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('hit')

            # Two ducks shot
            elif ducksShot == 2:
                x2, y2, width, height = DOG_TWO_DUCKS_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('hit')

            # No ducks shot
            else:
                x2, y2, width, height = DOG_LAUGH_RECT
                if self.frame == 3:
                    self.registry.get('soundHandler').enqueue('flyaway')

            # Dog comes up and goes back down
            x1, y1 = self.dogPosition
            if self.frame < height:
                self.dogPosition = x1, (y1 - 3)
                height = self.frame
            else:
                self.dogPosition = x1, (y1 + 3)
                height -= (self.frame - height)

            # If dog is no longer visible, move on
            if height <= 0:
                self.dogPosition = DOG_REPORT_POSITION
                self.frame = 0
                self.dogCanComeOut = False
                self.ducks = [Duck(self.registry), Duck(self.registry)]
                self.timer = timer
                self.gun.reloadIt()
            else:
                surface.blit(sprites, self.dogPosition, (x2, y2, width, height))

        # Show the cross hairs
        self.gun.render()

class RoundEndState(BaseState):
    def __init__(self, hitDucks):
        super(RoundEndState, self).__init__()
        self.isGameOver = False
        self.hitDucks = hitDucks

        # Count missed ducks
        missedCount = 0
        for i in self.hitDucks:
            if i == False:
                missedCount += 1
        # Miss 4 or more and you're done
        if missedCount >= 4:
            self.isGameOver = True
            self.notices = ("GAMEOVER", "")
            self.registry.get('soundHandler').enqueue('gameover')
        else:
            self.registry.get('soundHandler').enqueue('nextround')

    def execute(self, event):
        pass

    def update(self):
        # Wait for the sound to finish before allowing user to restart
        while pygame.mixer.get_busy():
            return

        if self.isGameOver:
            return GameOverState()
        else:
            self.registry.set('round', self.registry.get('round') + 1)
            return RoundStartState()

    def render(self):
        self.renderNotices()
        self.renderControls()

class GameOverState(BaseState):
    def __init__(self):
        super(GameOverState, self).__init__()
        self.state = None

    def execute(self, event):
        # Click to restart
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.registry.set('score', 0)
            self.registry.set('round', 1)
            self.state = RoundStartState()

    def update(self):
        self.notices = ("GAMEOVER", "")
        if self.state:
            return self.state

    def render(self):
        self.renderNotices()
        self.renderControls()
