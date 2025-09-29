import pygame
from board import *
from Sprites.empty import Empty
from Sprites.bomb import Bomb
from Sprites.bomberman import Bomberman
from Sprites.caisse import Caisse


class GraphicBoard(board):
    TILE_SIZE = 25

    sprites = {0: Empty(TILE_SIZE),
               1: pygame.surface.Surface((TILE_SIZE, TILE_SIZE)),
               2: Caisse(TILE_SIZE),
               3: Bomb(TILE_SIZE - 12),
               4: pygame.surface.Surface((TILE_SIZE, TILE_SIZE)),
               5: Bomberman(TILE_SIZE, 0),
               6: Bomberman(TILE_SIZE, 1),
               7: Bomberman(TILE_SIZE, 2),
               8: Bomberman(TILE_SIZE, 3), }

    def __init__(self, taille):
        super().__init__(taille)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((taille * self.TILE_SIZE, taille * self.TILE_SIZE))
        pygame.display.set_caption("BOMBERMAN")
        self.generer_mur()
        self.generer_caisse_indestructible()
        self.conteneur_joueur[0][1] = True
        self.conteneur_joueur[1][1] = True
        self.conteneur_joueur[2][1] = True
        self.conteneur_joueur[3][1] = True

        self.generer_caisse_destructible(4)

        self.sprites[1].fill([128, 0, 0])
        self.font = pygame.font.Font("SuperMario.ttf", 36)

    def update_screen(self):
        self.window.fill([0, 0, 0])
        for i in range(self.taille):
            for j in range(self.taille):
                x = i * self.TILE_SIZE
                y = j * self.TILE_SIZE

                tile = self.matrice[i][j]
                if tile == 1:
                    self.window.blit(self.sprites[tile], (x, y))
                elif tile == 4:
                    for k in reversed(self.get_objet_multi_case(i,j)[0]):
                        self.window.blit(self.sprites[k].display(), (x, y))
                else:
                    self.window.blit(self.sprites[tile].display(), (x, y))

    def explode(self):
        for i in reversed(range(len(self.list_bombe_timer))):
            if self.list_bombe_timer[i][3] == 1:
                blow = pygame.surface.Surface((self.TILE_SIZE, self.TILE_SIZE))
                blow.fill([255,0,0])
                self.window.blit(blow,(self.list_bombe_timer[i][0]*self.TILE_SIZE,self.list_bombe_timer[i][1]*self.TILE_SIZE))
                self.window.blit(blow, ((self.list_bombe_timer[i][0] + 1)*self.TILE_SIZE, (self.list_bombe_timer[i][1])*self.TILE_SIZE))
                self.window.blit(blow, ((self.list_bombe_timer[i][0] + 2) * self.TILE_SIZE, (self.list_bombe_timer[i][1]) * self.TILE_SIZE))
                self.window.blit(blow, (self.list_bombe_timer[i][0] * self.TILE_SIZE, (self.list_bombe_timer[i][1]+1)*self.TILE_SIZE))
                self.window.blit(blow, (self.list_bombe_timer[i][0] * self.TILE_SIZE, (self.list_bombe_timer[i][1] + 2) * self.TILE_SIZE))

        self.mise_a_jour_timer_bombe()

    def move_player(self, x, y, x_origine, y_origine, id_joueur):
        new_x, new_y = self.move_case(x, y, x_origine, y_origine, id_joueur)
        if new_x == x and new_y == y:
            self.sprites[id_joueur].change_state("right_arrow")
            for i in range(10):
             self.update_screen()

    def graphic_loop(self):
        tick_count = 10
        run = True
        setting = True
        count = 0
        bombed = False
        pos = [1, 1]
        timer_bomb = 0
        selected = 0
        while run:
            self.clock.tick(tick_count)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if setting:
                if keys[pygame.K_RIGHT]:
                    selected = (selected + 1) % len(self.conteneur_joueur)
                elif keys[pygame.K_LEFT]:
                    selected = (selected - 1 + len(self.conteneur_joueur)) % len(self.conteneur_joueur)
                elif keys[pygame.K_UP]:
                    self.conteneur_joueur[selected][1] = not self.conteneur_joueur[selected][1]
                elif keys[pygame.K_DOWN]:
                    self.conteneur_joueur[selected][1] = not self.conteneur_joueur[selected][1]
                elif keys[pygame.K_RETURN]:
                    self.initialiser_pos_joueur_sur_map()
                    setting = False
                self.window.fill([0,0,0])
                for i in range(len(self.conteneur_joueur)):
                    if i == selected:
                        color = [92, 200, 255]
                    else:
                        color = [255, 255, 255]
                    text = self.font.render(str(self.conteneur_joueur[i][1]), True, color)
                    marge = self.window.get_width() - (self.window.get_width() * (len(self.conteneur_joueur)-1)/len(self.conteneur_joueur) + text.get_width())
                    self.window.blit(text,
                                     (marge/2 + (self.window.get_width()/len(self.conteneur_joueur))*i, (self.window.get_height()/2)-text.get_height()))
            else:
                self.update_screen()
                if count > 5 and not bombed:
                    self.poser_bombe(pos[0], pos[1], 5)
                    self.move_player(2, 1, 1, 1, 5)
                    bombed = True

                if timer_bomb > tick_count:
                    self.explode()
                    timer_bomb = 0
                count += 1
                timer_bomb += 1

            pygame.display.update()


if __name__ == '__main__':
    wnd = GraphicBoard(15)

    wnd.graphic_loop()
