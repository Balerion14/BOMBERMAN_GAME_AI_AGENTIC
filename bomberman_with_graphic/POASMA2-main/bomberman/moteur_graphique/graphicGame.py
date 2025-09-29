from moteur_graphique.graphicBoard import GraphicBoard
from moteur_jeu.game import game
import pygame
import sys
from BOT.agentIntentionel import agentIntentionel as Agent


class GraphicGame(game):
    def __init__(self, taille_map):
        super().__init__(taille_map)
        self.board_1 = GraphicBoard(self.board_1.taille)
        self.board_1.generer_mur()
        self.board_1.generer_caisse_indestructible()
        self.board_1.initialiser_pos_joueur_sur_map()
        self.board_1.generer_caisse_destructible(4)

    def setting(self):
        self.board_1.setting_screen()
        # reinitialiser les agents avec les parametres souhaités...
        self.list_agent = []
        for joueur in self.board_1.conteneur_joueur:
            if joueur[1]:
                agent = Agent(joueur[0])
                x, y = list(filter(lambda pos: pos[2] == joueur[0], self.board_1.get_position_joueur()[0]))[0][:2]
                agent.init_pos_depart(x, y)
                self.list_agent.append(agent)

    def loop_game(self):
        run = True
        timer_bomb = 0
        self.setting()
        #pygame.mixer.music.load(...)
        #pygame.mixer.music.set_volume(0.25)
        #pygame.mixer.music.play(-1)
        while run:
            self.board_1.clock.tick(self.board_1.tick_count)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit(0)
            for agent in self.list_agent:
                if not self.board_1.sprites[agent.id_joueur].is_moving():
                    agent.choisir_coup(self.board_1)
                    self.board_1.update_player_position(agent.id_joueur)

            if self.board_1.get_position_joueur()[1] <= 1:
                run = False
            if timer_bomb > self.board_1.tick_count:  # mets à jour le timer des bombes toutes les secondes
                self.board_1.explode()
                timer_bomb = 0
            timer_bomb += 1

            self.board_1.update_screen()
            pygame.display.update()
        self.board_1.ending_screen()




if __name__ == "__main__":
    game = GraphicGame(15)
    game.loop_game()
