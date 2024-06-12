import random
import pygame
from pygame.locals import *
from actors import *

g_vars = {}
g_vars['width'] = 800
g_vars['height'] = 850
g_vars['fps'] = 30
g_vars['grid'] = 32
g_vars['window'] = pygame.display.set_mode([g_vars['width'], g_vars['height']], pygame.HWSURFACE)

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Frogger")
        
        self.running = None
        self.state = None
        self.frog = None
        self.score = None
        self.lanes = None

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Courier New', 16)

    def init(self):
        self.running = True
        self.state = 'START'
        
        self.frog = Frog(g_vars['width'] / 2 - g_vars['grid'] / 2, 24 * g_vars['grid'], g_vars['grid'])
        self.frog.attach(None)
        self.score = Score()

        self.lanes = []
        self.lanes.append(Lane(1, c=(50, 192, 122)))
        self.lanes.append(Lane(2, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=5))
        self.lanes.append(Lane(3, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-4))
        self.lanes.append(Lane(4, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=4))
        self.lanes.append(Lane(5, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-3))
        self.lanes.append(Lane(6, c=(50, 192, 122)))
        self.lanes.append(Lane(7, c=(50, 192, 122)))
        self.lanes.append(Lane(8, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-4))
        self.lanes.append(Lane(9, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-3))
        self.lanes.append(Lane(10, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=2.5))
        self.lanes.append(Lane(11, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=3))
        self.lanes.append(Lane(12, c=(50, 192, 122)))
        self.lanes.append(Lane(13, c=(50, 192, 122)))
        self.lanes.append(Lane(14, t='log', c=(153, 217, 234), n=2, l=6, spc=350, spd=2))
        self.lanes.append(Lane(15, t='log', c=(153, 217, 234), n=3, l=2, spc=180, spd=-1.6))
        self.lanes.append(Lane(16, t='log', c=(153, 217, 234), n=4, l=2, spc=140, spd=1.6))
        self.lanes.append(Lane(17, t='log', c=(153, 217, 234), n=2, l=3, spc=230, spd=-2))
        self.lanes.append(Lane(18, c=(50, 192, 122)))
        self.lanes.append(Lane(19, c=(50, 192, 122)))
        self.lanes.append(Lane(20, t='car', c=(195, 195, 195), n=3, l=2, spc=180, spd=-2))
        self.lanes.append(Lane(21, t='car', c=(195, 195, 195), n=2, l=4, spc=240, spd=-1))
        self.lanes.append(Lane(22, t='car', c=(195, 195, 195), n=4, l=2, spc=130, spd=2.5))
        self.lanes.append(Lane(23, t='car', c=(195, 195, 195), n=3, l=3, spc=200, spd=1))
        self.lanes.append(Lane(24, c=(50, 192, 122)))

    def event(self, event):
        if event.type == QUIT:
            self.running = False

        if event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.state == 'PLAYING':
                self.state = 'PAUSE'
            elif self.state == 'PAUSE':
                self.state = 'PLAYING'

        if self.state == 'START':
            if event.type == KEYDOWN and event.key == K_RETURN:
                self.state = 'PLAYING'

        if self.state == 'PLAYING':
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.frog.move(-1, 0)
            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.frog.move(1, 0)
            if event.type == KEYDOWN and event.key == K_UP:
                self.frog.move(0, -1)
            if event.type == KEYDOWN and event.key == K_DOWN:
                self.frog.move(0, 1)

        if self.state == 'PAUSE':
            if event.type == KEYDOWN:
                if event.key == K_r:
                    self.reset_game()  # Reset player position and lives
                    self.state = 'PLAYING'
                if event.key == K_m:
                    self.state = 'START'

    def reset_game(self):
        self.frog.reset()  # Reset frog's position
        self.score.lives = 3  # Reset lives to initial value
        self.score.score = 0  # Optionally reset score

    def update(self):
        if self.state == 'PLAYING':
            for lane in self.lanes:
                lane.update()
            
            lane_index = self.frog.y // g_vars['grid'] - 1
            if self.lanes[lane_index].check(self.frog):
                self.score.lives -= 1
                self.score.score = 0
            
            self.frog.update()

            if (g_vars['height'] - self.frog.y) // g_vars['grid'] > self.score.high_lane:
                if self.score.high_lane == 24:
                    self.frog.reset()
                    self.score.update(200)
                else:
                    self.score.update(10)
                    self.score.high_lane = (g_vars['height'] - self.frog.y) // g_vars['grid']

            if self.score.lives == 0:
                self.frog.reset()
                self.score.reset()
                self.state = 'START'
                
            if self.score.score >= 1000:
                self.state = 'CONGRATULATIONS'

    def draw(self):
        g_vars['window'].fill((0, 0, 0))
        if self.state == 'START':
            self.draw_text("Look B4U Cross!", g_vars['width'] / 2, g_vars['height'] / 2 - 15, 'center')
            self.draw_text("Press ENTER to start playing.", g_vars['width'] / 2, g_vars['height'] / 2 + 15, 'center')

        if self.state == 'PLAYING':
            self.draw_text("Lives: {0}".format(self.score.lives), 5, 8, 'left')
            self.draw_text("Score: {0}".format(self.score.score), 120, 8, 'left')
            self.draw_text("High Score: {0}".format(self.score.high_score), 240, 8, 'left')

            for lane in self.lanes:
                lane.draw()
            self.frog.draw()

        if self.state == 'PAUSE':
            self.draw_text("Paused", g_vars['width'] / 2, g_vars['height'] / 2 - 30, 'center')
            self.draw_text("Press R to reset", g_vars['width'] / 2, g_vars['height'] / 2, 'center')
            self.draw_text("Press M to return to main menu", g_vars['width'] / 2, g_vars['height'] / 2 + 30, 'center')
        
        if self.state == 'CONGRATULATIONS':
            self.draw_text("Congratulations!", g_vars['width'] / 2, g_vars['height'] / 2 - 30, 'center')
            self.draw_text("You are road safe.", g_vars['width'] / 2, g_vars['height'] / 2, 'center')
            self.draw_text("Press ENTER to restart", g_vars['width'] / 2, g_vars['height'] / 2 + 30, 'center')

        pygame.display.flip()

    def draw_text(self, t, x, y, a):
        text = self.font.render(t, False, (255, 255, 255))
        if a == 'center':
            x -= text.get_rect().width / 2
        elif a == 'right':
            x += text.get_rect().width
        g_vars['window'].blit(text, [x, y])

    def cleanup(self):
        pygame.quit()
        quit()

    def execute(self):
        if self.init() == False:
            self.running = False
        while self.running:
            for event in pygame.event.get():
                self.event(event)
                if self.state == 'CONGRATULATIONS' and event.type == KEYDOWN and event.key == K_RETURN:
                    self.reset_game()
                    self.state = 'START'
            self.update()
            self.draw()
            self.clock.tick(g_vars['fps'])
        self.cleanup()

if __name__ == "__main__":
    gameApp = App()
    gameApp.execute()

    
