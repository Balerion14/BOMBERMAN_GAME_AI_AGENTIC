import sys

import pygame
from moteur_jeu.board import board
from Sprites.empty import Empty
from Sprites.bomb import Bomb
from Sprites.bomberman import Bomberman
from Sprites.caisse import Caisse


class GraphicBoard(board):
    TILE_SIZE = 25

    sprites = {0: Empty(TILE_SIZE),
               1: [pygame.image.load("Sprites/img/indestructible_covered.png"),
                   pygame.image.load("Sprites/img/indestructible.png")],
               2: Caisse(TILE_SIZE),
               3: Bomb(TILE_SIZE),
               4: pygame.surface.Surface((TILE_SIZE, TILE_SIZE)),
               5: Bomberman(TILE_SIZE, 0),
               6: Bomberman(TILE_SIZE, 1),
               7: Bomberman(TILE_SIZE, 2),
               8: Bomberman(TILE_SIZE, 3), }

    def __init__(self, taille):
        super().__init__(taille)
        pygame.init()
        pygame.mixer.init()

        self.bomb_sound = pygame.mixer.Sound("BGS/Small Bomb Explosion Sound Effect.mp3")

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((taille * self.TILE_SIZE, taille * self.TILE_SIZE))
        pygame.display.set_caption("BOMBERMAN")
        self.generer_mur()
        self.generer_caisse_indestructible()
        self.conteneur_joueur[0][1] = True
        self.conteneur_joueur[1][1] = True
        self.conteneur_joueur[2][1] = True
        self.conteneur_joueur[3][1] = True

        self.font = pygame.font.Font("SuperMario.ttf", 36)

        self.exploded_tiles = []  # [0 : frame, 1 : [x, y]]
        self.frame_explosion = []

        self.initExplosionFrame()
        self.tick_count = 10

    def initExplosionFrame(self):
        for i in range(5):
            img = pygame.image.load("Sprites/img/explosion/Calque " + str(i) + ".png")
            self.frame_explosion.append(img)

    def update_screen(self):  # mets à jour l'interface graphique
        self.window.fill([0, 0, 0])
        for i in range(self.taille):
            for j in range(self.taille):
                x = i * self.TILE_SIZE
                y = j * self.TILE_SIZE

                tile = self.matrice[i][j]

                if tile == 1:
                    if i == 0 and j != self.taille - 1 or i == self.taille - 1 and j != self.taille - 1:
                        self.window.blit(self.sprites[tile][0], (x, y))
                    else:
                        self.window.blit(self.sprites[tile][1], (x, y))
                else:
                    self.window.blit(self.sprites[0].display(), (x, y - 2))
                    if tile == 4:
                        for k in reversed(self.get_objet_multi_case(i, j)[0]):
                            if k == 5 or k == 6 or k == 7 or k == 8:
                                self.sprites[k].display(self.window)
                            else:
                                self.window.blit(self.sprites[k].display(), (x, y))
                    elif tile == 0 or isinstance(self.sprites[tile], Bomberman):
                        pass
                    else:
                        self.window.blit(self.sprites[tile].display(), (x, y))
        for sprite in self.sprites:
            if sprite != 1 and sprite != 4:
                self.sprites[sprite].update_sprite()
            if isinstance(self.sprites[sprite], Bomberman) and list(
                    filter(lambda contain: contain[2] == sprite, self.get_position_joueur()[0])) != []:
                self.sprites[sprite].display(self.window)
        for exp in self.exploded_tiles:
            if exp[0] < len(self.frame_explosion):
                if exp[0] >= 0:
                    self.window.blit(self.frame_explosion[exp[0]], exp[1])
                exp[0] += 1
            else:
                self.exploded_tiles.remove(exp)

    def explode(
            self):  # affiche l'explosion de bombes si une bombe explose, sinon mets juste à jour le timer des bombes
        for i in reversed(range(len(self.list_bombe_timer))):
            if self.list_bombe_timer[i][3] == 1:
                self.exploded_tiles.append([0, [self.list_bombe_timer[i][0] * 25, self.list_bombe_timer[i][1] * 25]])
                for j in range(1, self.RAYON_BOMBE):
                    self.exploded_tiles.append(
                        [-j, [(self.list_bombe_timer[i][0] + j) * 25, (self.list_bombe_timer[i][1]) * 25]])
                    self.exploded_tiles.append(
                        [-j, [(self.list_bombe_timer[i][0]) * 25, (self.list_bombe_timer[i][1] + j) * 25]])
                    self.exploded_tiles.append(
                        [-j, [(self.list_bombe_timer[i][0] - j) * 25, (self.list_bombe_timer[i][1]) * 25]])
                    self.exploded_tiles.append(
                        [-j, [(self.list_bombe_timer[i][0]) * 25, (self.list_bombe_timer[i][1] - j) * 25]])
                pygame.mixer.Sound.play(self.bomb_sound)

        self.mise_a_jour_timer_bombe()

    def move_player(self, x, y, x_origine, y_origine,
                    id_joueur):  # permets le deplacement des joueurs sur l'interface et sur la matrice, si un joueur est en deplacement, un autre deplacement est impossible
        if not self.sprites[id_joueur].is_moving():
            new_x, new_y = self.move_case(x, y, x_origine, y_origine, id_joueur)
            if new_x == x and new_y == y:
                self.sprites[id_joueur].set_target_position(new_x * self.TILE_SIZE, new_y * self.TILE_SIZE)

    def update_player_position(self, id_joueur):  # deplace le joueur en fonction de la matrice
        position = list(filter(lambda i: i[2] == id_joueur, self.get_position_joueur()[0]))
        if position:
            position = position[0]
            if position[0] != self.sprites[id_joueur].x and position[1] != self.sprites[id_joueur].y:
                self.sprites[id_joueur].set_target_position(position[0] * self.TILE_SIZE, position[1] * self.TILE_SIZE)

    def drop_bomb(self, x, y, id_joueur):
        if self.sprites[id_joueur].x / 25 == x and self.sprites[id_joueur].y / 25 == y:
            self.poser_bombe(x, y, id_joueur)

    def init_pos_player(self):  # initialise la position des joueurs sur la map
        for i in self.conteneur_joueur:
            x, y = next(filter(lambda pos: pos[2] == i[0], self.get_position_joueur()[0]))[:2]
            if i[1]:
                self.sprites[i[0]].initialise_position(x * self.TILE_SIZE, y * self.TILE_SIZE)
            else:
                self.matrice[x][y] = 0
        print(self.get_position_joueur())

    def setting_screen(self):  # ecran de parametre des agents (savoir quel agent devrait etre present)
        run = True
        selected = 0
        while run:
            self.clock.tick(self.tick_count)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit(0)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("BGM/Main Menu - Crazy Frog Racer OST.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            if keys[pygame.K_RIGHT]:
                selected = (selected + 1) % len(self.conteneur_joueur)
            elif keys[pygame.K_LEFT]:
                selected = (selected - 1 + len(self.conteneur_joueur)) % len(self.conteneur_joueur)
            elif keys[pygame.K_UP]:
                self.conteneur_joueur[selected][1] = not self.conteneur_joueur[selected][1]
            elif keys[pygame.K_DOWN]:
                self.conteneur_joueur[selected][1] = not self.conteneur_joueur[selected][1]
            elif keys[pygame.K_RETURN]:
                self.init_pos_player()
                run = False
            self.window.fill([0, 0, 0])
            for i in range(len(self.conteneur_joueur)):
                if i == selected:
                    color = [92, 200, 255]
                else:
                    color = [255, 255, 255]
                text = self.font.render(str(self.conteneur_joueur[i][1]), True, color)
                img = pygame.transform.scale(self.sprites[5 + i].get_current_image(),
                                             (text.get_width(), text.get_width()))
                if not self.conteneur_joueur[i][1]:
                    img.set_alpha(64)
                else:
                    img.set_alpha(255)

                marge = self.window.get_width() - (self.window.get_width() * (len(self.conteneur_joueur) - 1) / len(
                    self.conteneur_joueur) + text.get_width())
                self.window.blit(text,
                                 (marge / 2 + (self.window.get_width() / len(self.conteneur_joueur)) * i,
                                  (self.window.get_height() / 2) - text.get_height()))
                self.window.blit(img, (marge / 2 + (self.window.get_width() / len(self.conteneur_joueur)) * i,
                                       self.window.get_height() * (3 / 4)))
                self.sprites[5 + i].update_sprite()
            pygame.display.update()
        pygame.mixer.music.stop()

    def ending_screen(self):
        pygame.mixer.music.fadeout(1000)
        blackscreen = pygame.surface.Surface((self.window.get_width(), self.window.get_height()))
        img_v_y = 200
        img_pos_y = 0
        text_v_y = 120
        text_pos_y = 0
        run = True
        alpha = 0
        dark = False
        while run:
            self.clock.tick(self.tick_count)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit(0)
            if alpha <= 128:
                alpha += 32
            else:
                dark = True
            self.update_screen()
            blackscreen.set_alpha(alpha)
            self.window.blit(blackscreen, (0, 0))
            if dark:
                if self.get_position_joueur()[1] == 1:
                    id_joueur = self.get_position_joueur()[0][0][2]
                    img = pygame.transform.scale(self.sprites[id_joueur].get_current_image(), (100, 100))
                    text = self.font.render("l'Agent n° " + str(id_joueur) + " a gagné !", True, (255, 255, 255))
                    backtext = self.font.render("l'Agent n° " + str(id_joueur) + " a gagné !", True, (0, 0, 0))
                    self.window.blit(img, (137, img_pos_y))
                    img_v_y /= 2
                    img_pos_y += img_v_y
                else:
                    text = self.font.render("Aucun Agent n'a gagné...", True, (255, 255, 255))
                    backtext = self.font.render("Aucun Agent n'a gagné...", True, (0, 0, 0))
                self.window.blit(backtext, (((self.window.get_width() - text.get_width())/2)+5, text_pos_y + 5))
                self.window.blit(text, ((self.window.get_width() - text.get_width())/2, text_pos_y))
                text_v_y /= 2
                text_pos_y += text_v_y

            pygame.display.update()

    def graphic_loop(self):  # boucle de test de fonctionnalités
        run = True
        count = 0
        bombed = False
        moved = False
        loaded = False
        pos = [1, 1]
        timer_bomb = 0
        pause = False
        self.initialiser_pos_joueur_sur_map()
        self.generer_caisse_destructible(1)
        self.setting_screen()
        while run:
            self.clock.tick(self.tick_count)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit(0)
            if keys[pygame.K_SPACE]:
                pause = not pause
                blackscreen = pygame.surface.Surface(self.window.get_size())
                blackscreen.fill([0, 0, 0])
                blackscreen.set_alpha(128)
                self.window.blit(blackscreen, (0, 0))
            if not pause:
                if pygame.mixer.music.get_busy() and not loaded:
                    pygame.mixer.music.stop()
                    #pygame.mixer.music.load(...)
                    #pygame.mixer.music.set_volume(0.25)
                    #pygame.mixer.music.play(-1)
                    loaded = True
                self.update_screen()
                if count > 5 and not bombed:
                    # self.drop_bomb(pos[0], pos[1], 5)
                    bombed = True
                if bombed and not self.sprites[5].is_moving():
                    #self.drop_bomb(pos[0], pos[1], 5)
                    self.move_case(pos[0], pos[1] + 1, pos[0], pos[1], 5)
                    self.update_player_position(5)
                    pos[1] += 1

                if timer_bomb > self.tick_count:
                    self.explode()
                    timer_bomb = 0
                count += 1
                timer_bomb += 1

            pygame.display.update()


if __name__ == '__main__':
    wnd = GraphicBoard(15)
    wnd.graphic_loop()
