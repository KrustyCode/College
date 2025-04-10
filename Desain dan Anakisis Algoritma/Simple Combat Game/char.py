import pygame, random
from setting import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, game, scene, group, pos, name):
        super().__init__(group)
        self.health = 100
        self.game = game
        self.scene = scene
        self.name = name
        self.import_images(f'assets/characters/{self.name}/')
        self.frame_index = 0
        self.image = self.animations['idle_right'][self.frame_index].convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/3, -self.rect.height/3)
        self.force = 3000
        self.acc = vec()
        self.vel = vec()
        self.fric = -15
        self.direction = 'left'
        self.state = Idle()
        self.attack = False
        self.hurt = False
        self.max_stamina = 10
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = 1
        self.last_attack_time = 0 
        self.attack_cooldown = 100
        self.is_attacking = False
        self.die = False

    def deal_damage(self, amount):
        if not self.hurt:
            self.health -= amount
            self.hurt = True
    
    def stay_in_bounds(self):
        self.hitbox.left = max(self.hitbox.left, LEFT_BOUND)
        self.hitbox.right = min(self.hitbox.right, WIDTH)
        self.hitbox.top = max(self.hitbox.top, TOP_BOUND)
        self.hitbox.bottom = min(self.hitbox.bottom, HEIGHT)

    def import_images(self, path):
        self.animations = self.game.get_animations(path)
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = self.game.get_images(full_path)

    def get_collide_list(self, attack_area):
        collided_npcs = [
                npc for npc in self.scene.update_sprites
                if npc != self and attack_area.colliderect(npc.hitbox)
            ]
        return collided_npcs
        

    def physics(self, dt):
        self.acc.x += self.vel.x * self.fric
        self.vel.x += self.acc.x * dt
        self.pos.x += self.vel.x * dt + 0.5 * self.acc.x * dt * dt
        self.rect.centerx = round(self.pos.x)
        self.hitbox.centerx = self.rect.centerx
        

    def animate(self, state, fps, loop = True):
        self.frame_index += fps
        if self.frame_index >= len(self.animations[state]):
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animations[state])-1
        self.image = self.animations[state][int(self.frame_index)].convert_alpha()

    def get_direction(self):
        angle =  self.vel.angle_to(vec(0.1))
        angle = (angle + 360) % 360
        if angle == 45: self.direction = 'right'
        elif angle == 225: self.direction = 'left'
    
    def movement(self):
        pass

    def change_state(self):
        new_state = self.state.enter_state(self)
        if new_state: self.state = new_state
        else: self.state
    
    def check_for_attack(self):
        attack_area = None
        if self.is_attacking and not self.attack:
            # Create an attack area (hitbox)
            if self.direction == 'right':
                attack_area = self.rect.inflate(10, 0).move(15, 0)
            elif self.direction == 'left':
                attack_area = self.rect.inflate(10, 0).move(-15, 0)
            else:
                attack_area = self.rect

            for npc in self.get_collide_list(attack_area):
                if npc.health > 0:
                    npc.deal_damage(10)
                    npc.hurt = True
            
            self.attack = True

        return attack_area
    
    def recover_stamina(self, dt):
        if not self.attack:  # Only recover stamina if not attacking
            self.stamina += self.stamina_recovery_rate * dt
            if self.stamina > self.max_stamina:  # Cap stamina at max value
                self.stamina = self.max_stamina

    def update(self, dt):
        self.get_direction()
        self.change_state()
        self.stay_in_bounds()
        self.state.update(dt, self)

class Enemy(NPC):
    def __init__(self, game, scene, group, pos, name, player):
        super().__init__(game, scene, group, pos, name)
        self.max_stamina = 10
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = 1
        self.is_attacking = False
        self.last_attack_time = 0 
        self.attack_cooldown = 300
        self.state = Idle()
        self.player = player
        self.distance = self.player.rect.centerx - self.rect.centerx
        self.max_speed = 200
        self.attack_1 = False
        self.attack_2 = False
        self.attack_3 = False
        self.low_stamina = 0
        self.low_stamina_update = 3000
        self.low_stamina_last_update = 0

    def get_distance(self):
        self.distance = self.player.rect.centerx - self.rect.centerx
    
    def get_direction(self):
        if -3 < self.vel.x < 3:
            if self.player.rect.centerx > self.rect.centerx:
                self.direction = 'right'
            else:
                self.direction = 'left'
        else:
            angle =  self.vel.angle_to(vec(0.1))
            angle = (angle + 360) % 360
            if angle == 45: self.direction = 'right'
            elif angle == 225: self.direction = 'left'
    
    def retreat(self):
        self.low_stamina = random.randint(0, 4)

    def do_attack(self):
        if -45 <= self.distance <= 45 and self.stamina >= self.low_stamina and not self.player.die and -1 < self.vel.x < 1:
            self.is_attacking = True
        
        if self.is_attacking:
            options = random.randint(0, 2)
            if options == 0:
                self.attack_1 = True
                self.attack_2 = False
                self.attack_3 = False
            elif options == 1:
                self.attack_1 = False
                self.attack_2 = True
                self.attack_3 = False
            else:
                self.attack_1 = False
                self.attack_2 = False
                self.attack_3 = True
        
        else:
            self.is_attacking = False
            self.attack_1 = False
            self.attack_2 = False
            self.attack_3 = False
        
    def movement(self):
        if self.stamina < self.low_stamina:
            if -1 >= self.distance > -100 and WIDTH - self.rect.centerx - self.distance > 120 or 1 <= self.distance < 100 and self.rect.centerx + self.distance < 100:
                self.acc.x = self.force
            elif 1 <= self.distance < 100 and self.rect.centerx + self.distance > 120 or -1 >= self.distance > -100 and WIDTH - self.rect.centerx - self.distance < 100 :
                self.acc.x = -self.force
            else:
                self.acc.x = 0
                
        
        else:
            if self.distance < -45:
                self.acc.x = -self.force
            elif self.distance > 45:
                self.acc.x = self.force
            else: 
                self.acc.x = 0

    def update(self, dt):
        super().update(dt)
        self.get_distance()
        self.do_attack()
        if (pygame.time.get_ticks() - self.low_stamina_last_update) > self.low_stamina_update:
            self.low_stamina_last_update = pygame.time.get_ticks()
            self.retreat()



class Player(NPC):
    def __init__(self, game, scene, group, pos, name):
        super().__init__(game, scene, group, pos, name)
        self.max_stamina = 10
        self.health = 100
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = 1
        self.is_attacking = False
        self.last_attack_time = 0 
        self.attack_cooldown = 100
        self.attack_1 = False
        self.attack_2 = False
        self.attack_3 = False
        self.max_stamina = 200
    
    def movement(self):
        if INPUTS['left']: self.acc.x = -self.force
        elif INPUTS['right']: self.acc.x = self.force
        else: 
            self.acc.x = 0
    def do_attack(self):
        if INPUTS['1']:
            self.is_attacking = True
            self.attack_1 = True
            self.attack_2 = False
            self.attack_3 = False
        elif INPUTS['2']:
            self.is_attacking = True
            self.attack_1 = False
            self.attack_2 = True
            self.attack_3 = False
        elif INPUTS['3']:
            self.is_attacking = True
            self.attack_1 = False
            self.attack_2 = False
            self.attack_3 = True
        else:
            self.attack_1 = False
            self.attack_2 = False
            self.attack_3 = False

    def update(self, dt):
        super().update(dt)  # Call the parent update method  # Check for attacks
        self.do_attack()
        

class Idle:
    def enter_state(self, character):
        if character.hurt:
            character.frame_index = 0
            return Hurt()
        elif character.vel.magnitude() > 30:
            character.frame_index = 0
            return Run()
        elif character.attack_1 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack1()
        elif character.attack_2 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack2()
        elif character.attack_3 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack3()
    def update(self, dt, character):
        character.recover_stamina(dt)
        character.animate(f'idle_{character.direction}', 10 * dt)
        character.movement()
        character.physics(dt)

class Run:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'run_{character.direction}']) - 1:
            character.frame_index = 0
        if character.hurt:
            character.frame_index = 0
            return Hurt()
        elif character.vel.magnitude() < 30:
            character.frame_index = 0
            return Idle() 
        elif character.attack_1 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack1()
        elif character.attack_2 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack2()
        elif character.attack_3 and character.stamina >= 1 and character.is_attacking:
            character.frame_index = 0
            return Attack3()
    def update(self, dt, character):
        character.recover_stamina(dt)
        character.animate(f'run_{character.direction}', 10 * dt, False)
        character.movement()
        character.physics(dt)

class Attack1:
    def enter_state(self, character):
        if character.frame_index == len(character.animations[f'attack_1_{character.direction}']) - 1:
            character.attack = False
            character.is_attacking = False
            character.last_attack_time = pygame.time.get_ticks()
            if not character.stamina <= 0:
                character.stamina -= 1
            character.frame_index = 0
            return Idle()
        
    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            if character.frame_index >= len(character.animations[f'attack_1_{character.direction}'])/2:
                character.check_for_attack()
            character.animate(f'attack_1_{character.direction}', 10 * dt, loop = False)
        else:
            return Idle()

class Attack2:
    def enter_state(self, character):
        if character.frame_index > len(character.animations[f'attack_2_{character.direction}']) - 1:
            character.attack = False
            character.is_attacking = False
            character.last_attack_time = pygame.time.get_ticks()
            if not character.stamina <= 0:
                character.stamina -= 1
            character.frame_index = 0
            return Idle()

    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            if character.frame_index >= len(character.animations[f'attack_2_{character.direction}'])/2:
                character.check_for_attack()
            character.animate(f'attack_2_{character.direction}', 8 * dt, loop = False)
        else:
            return Idle()
            
class Attack3:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'attack_3_{character.direction}'])-1:
            character.attack = False
            character.is_attacking = False
            character.last_attack_time = pygame.time.get_ticks()
            if not character.stamina <= 0:
                character.stamina -= 1
            character.frame_index = 0
            return Idle()
    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            if character.frame_index >= len(character.animations[f'attack_3_{character.direction}'])/2:
                character.check_for_attack()
            character.animate(f'attack_3_{character.direction}', 8 * dt, loop = False)
        else:
            return Idle()

class Hurt:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'hurt_{character.direction}'])-1:
            character.hurt = False
            character.frame_index = 0
            if character.health == 0:
                character.frame_index = 0
                return Die()
            else:
                return Idle()
           
    def update(self, dt, character):
        character.is_attacking = False
        character.animate(f'hurt_{character.direction}', 12 * dt)

class Die:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'die_{character.direction}'])-1:
            print(f'{character.name} has died')
            character.die = True
            character.kill()
           
    def update(self, dt, character):
        character.animate(f'die_{character.direction}', 12 * dt)

