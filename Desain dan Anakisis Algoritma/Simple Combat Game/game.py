import pygame, sys, os
from state import SplashScreen
from setting import *

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN| pygame.SCALED)
        self.font = pygame.font.Font(FONT, TILESIZE)
        self.fps = 0
        self.running = True

        self.states = []
        self.splash_screen = SplashScreen(self)
        self.states.append(self.splash_screen)

    def render_text(self, text, colour, font, pos, centralised = True):
        canvas = font.render(str(text), False, colour)
        rect = canvas.get_rect(center = pos) if centralised else canvas.get_rect(topleft = pos)
        self.screen.blit(canvas, rect)
    
    def custom_cursor(self):
        pygame.mouse.set_visible(False)

    def get_images(self, path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path, file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images

    def get_animations(self, path):
        animations = {}
        for file_name in os.listdir(path):
            animations.update({file_name:[]})
        return animations

    def get_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS['escape'] = True
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    INPUTS['space'] = True
                elif event.key == pygame.K_UP:
                    INPUTS['up'] = True
                elif event.key == pygame.K_LEFT:
                    INPUTS['left'] = True
                elif event.key == pygame.K_RIGHT:
                    INPUTS['right'] = True
                elif event.key == pygame.K_DOWN:
                    INPUTS['down'] = True
                elif event.key == pygame.K_1:
                    INPUTS['1'] = True
                elif event.key == pygame.K_2:
                    INPUTS['2'] = True
                elif event.key == pygame.K_3:
                    INPUTS['3'] = True
                elif event.key == pygame.K_4:
                    INPUTS['4'] = True
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    INPUTS['space'] = False
                elif event.key == pygame.K_UP:
                    INPUTS['up'] = False
                elif event.key == pygame.K_LEFT:
                    INPUTS['left'] = False
                elif event.key == pygame.K_RIGHT:
                    INPUTS['right'] = False
                elif event.key == pygame.K_DOWN:
                    INPUTS['down'] = False
                elif event.key == pygame.K_1:
                    INPUTS['1'] = False
                elif event.key == pygame.K_2:
                    INPUTS['2'] = False
                elif event.key == pygame.K_3:
                    INPUTS['3'] = False
                elif event.key == pygame.K_4:
                    INPUTS['4'] = False
    
    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False
    
    def loop(self):
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            self.custom_cursor()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.loop()




