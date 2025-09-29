import os.path

import pygame


class Bomberman(pygame.sprite.Sprite):

    def __init__(self, size, id_bomberman):
        super().__init__()
        self.image = {
            "base_state": [],
            "right_arrow": [],
            "left_arrow": [],
            "up_arrow": [],
            "down_arrow": []
        }
        self.id_bomberman = id_bomberman
        self.initFrames(size)
        self.state = "base_state"
        self.x = -25
        self.y = -25
        self.target_x = 0
        self.target_y = 0

    def initFrames(self, size):
        for i in range(0, 16, 2):
            self.image["down_arrow"].append(pygame.image.load("Sprites/img/bomberman-"+ str(self.id_bomberman) + "/down_arrow/bomberman_test" + str(i+1) + ".png"))
            self.image["up_arrow"].append(pygame.image.load("Sprites/img/bomberman-" + str(self.id_bomberman) + "/up_arrow/bomberman_test" + str(i + 1) + ".png"))
            self.image["left_arrow"].append(pygame.image.load(
                "Sprites/img/bomberman-" + str(self.id_bomberman) + "/left_arrow/bomberman_test" + str(
                    i + 1) + ".png"))
            self.image["right_arrow"].append(pygame.image.load(
                "Sprites/img/bomberman-" + str(self.id_bomberman) + "/right_arrow/bomberman_test" + str(
                    i + 1) + ".png"))
            self.image["base_state"].append(pygame.image.load(
                "Sprites/img/bomberman-" + str(self.id_bomberman) + "/base_state/bomberman_test" + str(
                    i + 1) + ".png"))
        self.frame = 0

    def get_current_image(self):
        img = self.image[self.state][self.frame]
        return img

    def display(self, window):
        img = self.image[self.state][self.frame]
        window.blit(img, (self.x-4, self.y-8))
        if self.x > self.target_x and self.y % 25 == 0:
            self.x -= 5
            if self.state != "left_arrow":
                self.change_state("left_arrow")
        elif self.y > self.target_y and self.x % 25 == 0:
            self.y -= 5
            if self.state != "up_arrow":
                self.change_state("up_arrow")
        elif self.x < self.target_x and self.y % 25 == 0:
            self.x += 5
            if self.state != "right_arrow":
                self.change_state("right_arrow")
        elif self.y < self.target_y and self.x % 25 == 0:
            self.y += 5
            if self.state != "down_arrow":
                self.change_state("down_arrow")
        elif self.x == self.target_x and self.y == self.target_y and self.state != "base_state":
            self.change_state("base_state")

    def is_moving(self):
        return not (self.x == self.target_x and self.y == self.target_y)

    def update_sprite(self):
        self.frame = (self.frame + 1) % len(self.image[self.state])

    def change_state(self, new_state):
        if new_state in self.image.keys():
            self.state = new_state
            self.frame = 0
        else:
            print("Etat inconnu")

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def initialise_position(self, x, y):
        self.set_position(x,y)
        self.target_x = x
        self.target_y = y

    def set_target_position(self, new_x, new_y):
        self.target_x = new_x
        self.target_y = new_y