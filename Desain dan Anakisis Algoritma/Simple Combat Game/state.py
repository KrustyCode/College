import pygame
from setting import *
from char import Player, Enemy

class State:
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def update (self, dt):
        pass

    def draw (self, screen):
        pass

class SplashScreen(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.blink_timer = 0
    
    def update (self, dt):
        if INPUTS['space']:
            self.game.reset_inputs()
            Scene(self.game).enter_state()
        
        self.blink_timer += dt
        if self.blink_timer >= 1:  # Reset every 1 second
            self.blink_timer = 0

    def draw (self, screen):
        screen.fill(COLOURS['blue'])
        self.game.render_text('Welcome to Simple A-RPG' , COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))
        if self.blink_timer < 0.5:
            self.game.render_text('press space to start' , COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2 + 30))

class Scene(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites], (WIDTH/2, HEIGHT/2), CHAR[0])
        self.enemy = Enemy(self.game, self, [self.update_sprites, self.drawn_sprites], (WIDTH/4, HEIGHT/2), CHAR[1], self.player)

    def debugger (self, debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name, COLOURS['black'], self.game.font, (10, 15 * index), False)

    def update (self, dt):
        self.update_sprites.update(dt)
        if self.player.die or self.enemy.die:
            self.game.reset_inputs()
            GAME_OVER(self.game, self.enemy.die).enter_state()
    
            
    def draw (self, screen):
        screen.fill(COLOURS['white'])
        self.drawn_sprites.draw(screen)
        text_player = self.game.font.render("Player", True, COLOURS['black'])
        text_enemy = self.game.font.render("Enemy", True, COLOURS['red'])
    
        player_x = self.player.rect.centerx - text_player.get_width() // 2
        player_y = self.player.rect.top - text_player.get_height() - 5
        
        enemy_x = self.enemy.rect.centerx - text_enemy.get_width() // 2
        enemy_y = self.enemy.rect.top - text_enemy.get_height() - 5  

        screen.blit(text_player, (player_x, player_y))
        screen.blit(text_enemy, (enemy_x, enemy_y))  
        self.debugger(
            [
                str('Attack : 1 2 3'),
                str('Move: Arrow Left & Right'),
        #         str('FPS: ' + str(round(self.game.clock.get_fps(), 2))),
        #         str('player dir: ' + str(self.player.direction)),
        #         str ('player frame: ' + str(self.player.vel.magnitude())),
        #         str('Stamina: ' + str(self.enemy.stamina)),
                str ('Player HP: ' + str(self.player.health)),
                str ('Enemy HP: ' + str(self.enemy.health)),
        #         str ('enemy x: ' + str(self.enemy.rect.centerx)),
        #         str ('player x: ' + str(self.player.rect.centerx)),
        #         str ('player vel: ' + str(self.player.vel.x)),
        #         str ('enemy vel: ' + str(self.enemy.vel.x)),
        #         # str ('enemy: ' + str(self.enemy.low_stamina))
            ]
        )

class GAME_OVER(State):
    def __init__(self, game, enemy):
        State.__init__(self, game)
        self.enemy = enemy
        self.blink_timer = 0

    
    def update (self, dt):
        self.blink_timer += dt
        if self.blink_timer >= 1:  # Reset every 1 second
            self.blink_timer = 0

        if INPUTS['space']:
            self.game.reset_inputs()
            SplashScreen(self.game).enter_state()
            

    def draw (self, screen):
        screen.fill(COLOURS['black'])
        if self.enemy:
            self.game.render_text('YOU WIN' , COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))
        else:
            self.game.render_text('YOU LOSE' , COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2))  
        if self.blink_timer < 0.5:
            self.game.render_text('press space to start' , COLOURS['white'], self.game.font, (WIDTH/2, HEIGHT/2 + 30))

        # pygame.draw.rect(screen, COLOURS['red'], self.player.rect, 1)  # Player rect
        # pygame.draw.rect(screen, COLOURS['blue'], self.player.hitbox, 1)

        # pygame.draw.rect(screen, COLOURS['red'], self.enemy.rect, 1)  # Player rect
        # pygame.draw.rect(screen, COLOURS['blue'], self.enemy.hitbox, 1)

        # if self.player.check_for_attack():  # Ensure attack_area is valid
        #     pygame.draw.rect(screen, COLOURS['green'], self.player.check_for_attack(), 1)