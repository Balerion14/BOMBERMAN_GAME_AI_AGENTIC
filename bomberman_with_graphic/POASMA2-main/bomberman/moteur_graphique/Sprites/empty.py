import pygame


class Empty(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = pygame.image.load("Sprites/img/empty.png")
        self.rect = self.image.get_rect()

    def display(self):
        return self.image

    def update_sprite(self):
        pass
