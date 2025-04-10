import pygame
from char import NPC
from setting import *

class Player(NPC):
    def __init__(self, game, scene, group, pos, name):
        super().__init__(game, scene, group, pos, name)
        self.max_stamina = 10
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = 1
        self.is_attacking = False
        self.last_attack_time = 0 
        self.attack_cooldown = 100
    
    def movement(self):
        if INPUTS['left']: self.acc.x = -self.force
        elif INPUTS['right']: self.acc.x = self.force
        else: self.acc.x = 0
    
    def recover_stamina(self, dt):
        if not self.is_attacking:  # Only recover stamina if not attacking
            self.stamina += self.stamina_recovery_rate * dt
            if self.stamina > self.max_stamina:  # Cap stamina at max value
                self.stamina = self.max_stamina

class Idle:
    def enter_state(self, character):
        if character.vel.magnitude() > 30:
            return Run()
        elif INPUTS['1'] and character.stamina >= 1:
            return Attack1()
        elif INPUTS['2'] and character.stamina >= 1:
            return Attack2()
        elif INPUTS['3'] and character.stamina >= 1:
            return Attack3()
        else:
            return None
    def update(self, dt, character):
        character.is_attacking = False
        character.recover_stamina(dt)
        character.animate(f'idle_{character.get_direction()}', 10 * dt)
        character.movement()
        character.physics(dt)

class Run:
    def enter_state(self, character):
        if character.vel.magnitude() < 30:
            return Idle()
        elif INPUTS['1'] and character.stamina >= 1:
            return Attack1()
        elif INPUTS['2'] and character.stamina >= 1:
            return Attack2()
        elif INPUTS['3'] and character.stamina >= 1:
            return Attack3()
        else:
            return None
    def update(self, dt, character):
        character.is_attacking = False
        character.recover_stamina(dt)
        character.animate(f'run_{character.get_direction()}', 10 * dt)
        character.movement()
        character.physics(dt)

class Attack1:
    def enter_state(self, character):
        if character.frame_index == len(character.animations[f'attack_1_{character.get_direction()}']) - 1:
            character.last_attack_time = pygame.time.get_ticks()
            character.frame_index = 0
            if not character.stamina <= 0:
                character.stamina -= 1
            return Idle()
        return None
    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            character.is_attacking = True
            character.vel.magnitude == 0
            character.animate(f'attack_1_{character.get_direction()}', 10 * dt, loop = False)
        else:
            return Idle()

class Attack2:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'attack_2_{character.get_direction()}'])-1:
            character.last_attack_time = pygame.time.get_ticks()
            character.frame_index = 0
            if not character.stamina <= 0:
                character.stamina -= 1
            return Idle()
        return None
    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            character.is_attacking = True
            character.vel.magnitude == 0
            character.animate(f'attack_2_{character.get_direction()}', 8 * dt, loop = False)
        else:
            return Idle()
            
class Attack3:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'attack_3_{character.get_direction()}'])-1:
            character.last_attack_time = pygame.time.get_ticks()
            character.frame_index = 0
            if not character.stamina <= 0:
                character.stamina -= 1
            return Idle()
        return None
    def update(self, dt, character):
        current_time = pygame.time.get_ticks()
        if current_time - character.last_attack_time >= character.attack_cooldown and character.stamina >= 1:
            character.is_attacking = True
            character.vel.magnitude == 0
            character.animate(f'attack_3_{character.get_direction()}', 10 * dt, loop = False)
        else:
            return Idle()

