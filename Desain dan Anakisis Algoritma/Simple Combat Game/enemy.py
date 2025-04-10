import pygame
from setting import *
from char import NPC

class Enemy(NPC):
    def __init__(self, game, scene, group, pos, name):
        super().__init__(game, scene, group, pos, name)
        self.max_stamina = 10
        self.stamina = self.max_stamina
        self.stamina_recovery_rate = 1
        self.is_attacking = False
        self.last_attack_time = 0 
        self.attack_cooldown = 200

    def update(self, dt):
        self.state.update(dt, self)
        self.rect.center = self.hitbox.center
    
    def recover_stamina(self, dt):
        if not self.is_attacking:  # Only recover stamina if not attacking
            self.stamina += self.stamina_recovery_rate * dt
            if self.stamina > self.max_stamina:  # Cap stamina at max value
                self.stamina = self.max_stamina
    
    def update(self, dt):
        super().update(dt)
    
class Hurt:
    def enter_state(self, character):
        if character.frame_index >= len(character.animations[f'hurt_{character.get_direction()}'])-1:
            character.hurt = False
            character.frame_index = 0
            return Idle()
           
    def update(self, dt, character):
        character.is_attacking = False
        character.animate(f'hurt_{character.get_direction()}', 6 * dt)

class Idle:
    def enter_state(self, character):
        if character.hurt:
            return Hurt()
        else:
            return None
    def update(self, dt, character):
        character.is_attacking = False
        character.recover_stamina(dt)
        character.animate(f'idle_{character.get_direction()}', 10 * dt)
        character.movement()
        character.physics(dt)
