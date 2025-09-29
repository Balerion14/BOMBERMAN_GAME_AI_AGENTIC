import pygame


class Bomb(pygame.sprite.Sprite):

    def __init__(self, size):
        super().__init__()
        self.image = []
        self.frame = 0
        self.initFrames()


    def initFrames(self):
        for i in range(8):
            self.image.append(pygame.image.load("Sprites/img/bomb/Calque " + str(i+1) + ".png"))

    def display(self):
        img = self.image[self.frame]
        return img

    def update_sprite(self):
        self.frame = (self.frame + 1) % len(self.image)