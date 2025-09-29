import pygame


class Caisse(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = pygame.image.load("Sprites/img/box.png")

    def display(self):
        return self.image

    def update_sprite(self):
        pass
