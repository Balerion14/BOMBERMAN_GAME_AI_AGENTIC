import agent as ag
import board as map
from bomberman.BOT.agentIntentionel import agentIntentionel


class game:

    board_1 = None
    list_agent = []

    def __init__(self, taille_map):
        b = map.board(taille_map)
        b.generer_mur()
        b.generer_caisse_indestructible()
        # je passe mon conteneur joueur a true pour dire que les joueurs sont attribués a un agent pour les tests
        b.conteneur_joueur[0][1] = True # joueur 1
        b.conteneur_joueur[1][1] = True # joueur 2
        b.conteneur_joueur[2][1] = True # joueur 3
        b.conteneur_joueur[3][1] = True # joueur 4
        # associer un agent a un id_joueur
        agent_1 = agentIntentionel(b.conteneur_joueur[0][0])
        agent_2 = agentIntentionel(b.conteneur_joueur[1][0])
        agent_3 = agentIntentionel(b.conteneur_joueur[2][0])
        agent_4 = agentIntentionel(b.conteneur_joueur[3][0])
        # initialisation des joueurs sur la map
        b.initialiser_pos_joueur_sur_map() # ATTENTION : cette action doit etre faite avant de generer les caisses destructible
        # init pos agent
        list = b.get_position_joueur()
        if list != None :
            # recup id joueur et coordonnee correspondante a l agent
            for joueur in list[0] :
                if joueur[2] == agent_1.id_joueur :
                    agent_1.init_pos_depart(joueur[0], joueur[1])
                if joueur[2] == agent_2.id_joueur :
                    agent_2.init_pos_depart(joueur[0], joueur[1])
                if joueur[2] == agent_3.id_joueur :
                    agent_3.init_pos_depart(joueur[0], joueur[1])
                if joueur[2] == agent_4.id_joueur :
                    agent_4.init_pos_depart(joueur[0], joueur[1])
        b.generer_caisse_destructible(8)# seuil equilibré...
        self.board_1 = b
        self.list_agent.append(agent_1)
        self.list_agent.append(agent_2)
        self.list_agent.append(agent_3)
        self.list_agent.append(agent_4)

    def loop_game(self):
        compteur = 1
        while self.board_1.get_position_joueur()[1] > 1:
            print("-----------------------------------------------------" + str(compteur) + "-----------------------------------------------------")
            print(self.board_1.matrice)
            for agent in self.list_agent :
                # appeler methode choix_action a faire pour faire l action sur l agent une fois qu elle sera implemante...
                agent.choisir_coup(self.board_1)
                #agent.move(agent.x+1, agent.y, self.board_1)
                #agent.put_bombe(self.board_1)
                print(self.board_1.matrice)
                print(self.board_1.list_contenu_case)
                print(self.board_1.list_bombe_timer)
                print(self.board_1.get_position_joueur())
                print(agent.x, agent.y)
                print(agent.id_joueur)
                print(self.board_1.matrice)
                print("-----------------------------------------------------" + str(agent.id_joueur) + "-----------------------------------------------------")
            #break # a enlever pour faire tourner tous le jeu
            self.board_1.mise_a_jour_timer_bombe()
            compteur += 1
            if compteur == 12000 :
                break
        print("fin de la partie")

if __name__ == "__main__":
    g = game(10)
    g.loop_game()
    # test ok ...