from bomberman.moteur_jeu.agent import agent
import bomberman.moteur_jeu.board as map
import heapq


class agentIntentionel(agent):
    target = () #Non défini au début, mais égale à un agent ensuite
    just_place_bomb = False
    def __init__(self, associer_id_joueur) :
        super().__init__(associer_id_joueur)

    def get_joueur_by_position(self, board, i, j):
        if board.matrice[i][j] == board.CASE_MULTI_OBJET:
            list_objet = board.get_objet_multi_case(i, j)
            if list_objet != None:
                for k in range(len(list_objet[0])):
                    for joueur in board.conteneur_joueur:
                        if list_objet[0][k] in [joueur[0]] :
                            return joueur
        for joueur in board.conteneur_joueur:
            if board.matrice[i][j] in [joueur[0]]:
                return joueur
        return None

    def choisir_coup(self, board):
        print("")
        # Si l'agent est sur une case qui va exploser, aller à la case vide la plus proche
        if self.am_i_on_explosive_tile(board):
            print("JE suis sur une caseexplosive")
            empty_cell_path = self.get_nearest_empty_cell(board)
            print("empty_cell_path:", empty_cell_path)
            if empty_cell_path:
                next_empty_cell = empty_cell_path[0]
                super().move(next_empty_cell[0], next_empty_cell[1], board)
            else:
                # Aucune case vide trouvée à proximité, rester immobile ou prendre une autre décision
                pass
        else:
            # Obtenir les informations sur l'agent le plus proche
            infos_joueur_le_plus_proche = self.get_joueur_plus_proche_joueur(board)
            if infos_joueur_le_plus_proche is not None and infos_joueur_le_plus_proche[1] is not None:
                pos_next_moove = infos_joueur_le_plus_proche[1][0]
                pos_joueur_proche = infos_joueur_le_plus_proche[0]
                print("infos_joueur_le_plus_proche: ", infos_joueur_le_plus_proche)
                print("pos_next_moove: ", pos_next_moove)
                print("pos_joueur_proche: ", pos_joueur_proche)

                # Si possible, avancer vers la cible (agent le plus proche)
                if board.matrice[pos_next_moove[0]][pos_next_moove[1]] == board.CAISSE:
                    self.put_bombe(board)
                else:
                    super().move(pos_next_moove[0], pos_next_moove[1], board)
            else:
                pass

    """def choisir_coup(self, board):  # board est un objet de type board (voir class board)
        infos_joueur_le_plus_proche = self.get_joueur_plus_proche_joueur(board)
        pos_next_moove = infos_joueur_le_plus_proche[1][0]
        pos_joueur_proche = infos_joueur_le_plus_proche[0]
        print("infos_joueur_le_plus_proche: ", infos_joueur_le_plus_proche)
        print("pos_next_moove: ", pos_next_moove)
        print("pos_joueur_proche: ", pos_joueur_proche)

        print("self.need_to_change_target: ", self.need_to_change_target())
        print("target: ", self.get_joueur_by_position(board, pos_joueur_proche[0], pos_joueur_proche[1]))
        print("self.am_i_on_explosive_tile: ", self.am_i_on_explosive_tile(board))

        print("test mouvement si je suis sur zone explosive: ", super().move(pos_next_moove[0], pos_next_moove[1], board))
        print(board.matrice)

        print("board.get_case(pos_next_moove[0], pos_next_moove[1]) == board.case_vide :", board.get_case(pos_next_moove[0], pos_next_moove[1]) == board.case_vide)

        print("Tentative posage de bombe: ", self.put_bombe(board))
        print(board.matrice)
        print("Tentative de mouvement:")
        self.just_place_bomb = True
        infos_joueur_le_plus_proche = self.get_joueur_plus_proche_joueur(board)
        pos_next_moove = infos_joueur_le_plus_proche[1][0]
        super().move(pos_next_moove[0], pos_next_moove[1], board)

        return
        if self.need_to_change_target():
            self.target = self.get_joueur_by_position(board, pos_joueur_proche[0], pos_joueur_proche[1])

        if self.am_i_on_explosive_tile(board):
            # Aller dans la case la plus proche qui ne va pas exploser et qui est proche de la target
            super().move(pos_next_moove[0], pos_next_moove[1], board)
            self.just_place_bomb = False
        else:
            # Si case vide j'avance
            if board.get_case(pos_next_moove[0], pos_next_moove[1]) == board.case_vide:
                super().move(pos_next_moove[0], pos_next_moove[1], board)
                self.just_place_bomb = False
            else: # Sinon je pose une bombe, car le chemin cherché par get_joueur_plus_proche_joueur évite les murs
                self.put_bombe(board)
                self.just_place_bomb = True
        return -1"""

    def am_i_on_explosive_tile(self, board):
        for i in reversed(range(len(board.list_bombe_timer))):
            for direction in range(4):
                for j in range(board.RAYON_BOMBE):
                    if direction == 0:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][1] + j < board.taille and board.list_bombe_timer[i][1] + j >= 0:
                            for joueur in board.conteneur_joueur:
                                if board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] + j] in [joueur[0]]:
                                    if self.id_joueur in [joueur[0]] :
                                        return True
                                elif board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] + j] == board.CASE_MULTI_OBJET:
                                    list_objet = board.get_objet_multi_case(board.list_bombe_timer[i][0],board.list_bombe_timer[i][1] + j)
                                    if list_objet != None:
                                        for k in range(len(list_objet[0])):
                                            if self.id_joueur in [list_objet[0][k]]:
                                                return True
                    if direction == 1:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][1] - j >= 0 and board.list_bombe_timer[i][1] - j < board.taille:
                            for joueur in board.conteneur_joueur:
                                if board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] - j] in [joueur[0]]:
                                    if self.id_joueur in [joueur[0]] :
                                        return True
                                elif board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] - j] == board.CASE_MULTI_OBJET:
                                    list_objet = board.get_objet_multi_case(board.list_bombe_timer[i][0],board.list_bombe_timer[i][1] - j)
                                    if list_objet != None:
                                        for k in range(len(list_objet[0])):
                                            if self.id_joueur in [list_objet[0][k]]:
                                                return True
                    if direction == 2:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][0] + j < board.taille and board.list_bombe_timer[i][0] + j >= 0:
                            for joueur in board.conteneur_joueur:
                                if board.matrice[board.list_bombe_timer[i][0] + j][board.list_bombe_timer[i][1]] in [joueur[0]]:
                                    if self.id_joueur in [joueur[0]]:
                                        return True
                                elif board.matrice[board.list_bombe_timer[i][0] + j][board.list_bombe_timer[i][1]] == board.CASE_MULTI_OBJET:
                                    list_objet = board.get_objet_multi_case(board.list_bombe_timer[i][0] + j,board.list_bombe_timer[i][1])
                                    if list_objet != None:
                                        for k in range(len(list_objet[0])):
                                            if self.id_joueur in [list_objet[0][k]]:
                                                return True
                    if direction == 3:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][0] - j >= 0 and board.list_bombe_timer[i][0] - j < board.taille:
                            for joueur in board.conteneur_joueur:
                                if board.matrice[board.list_bombe_timer[i][0] - j][board.list_bombe_timer[i][1]] in [joueur[0]]:
                                    if self.id_joueur in [joueur[0]]:
                                        return True
                                elif board.matrice[board.list_bombe_timer[i][0] - j][board.list_bombe_timer[i][1]] == board.CASE_MULTI_OBJET:
                                    list_objet = board.get_objet_multi_case(board.list_bombe_timer[i][0] - j,board.list_bombe_timer[i][1])
                                    if list_objet != None:
                                        for k in range(len(list_objet[0])):
                                            if self.id_joueur in [list_objet[0][k]]:
                                                return True
        return False
    def need_to_change_target(self):
        if self.target == ():
            return True
        position_joueur = []
        for i in range(self.taille):
            for j in range(self.taille):
                # si la case un multi_objet, verifier le contenu de la case
                if self.matrice[i][j] == self.CASE_MULTI_OBJET:
                    list_objet = self.get_objet_multi_case(i, j)
                    if list_objet != None:
                        for k in range(len(list_objet[0])):
                            for joueur in self.conteneur_joueur:
                                if list_objet[0][k] in joueur[0]:
                                    return False
                # si la case est un joueur, on l ajoute a la liste
                for joueur in self.conteneur_joueur:
                    if self.matrice[i][j] in joueur[0]:
                        return False
        return True

    def get_joueur_plus_proche_joueur(self, board):
        posJoueur = board.get_position_joueur()[0]
        distances = {}  # Dictionnaire pour stocker les distances entre le joueur de départ et les autres joueurs

        for joueur in posJoueur:
            if not (joueur[0] == self.x and joueur[1] == self.y):
                path = self.astar(board, (self.x, self.y), (joueur[0], joueur[1]))
                #print("path: ", path)
                #print("cout:", len(path))
                if path:
                    distances[(joueur[0], joueur[1])] = len(path)

        if distances:
            # Retourne le joueur le plus proche en utilisant la distance minimale
            joueur_plus_proche = min(distances, key=distances.get)
            return (joueur_plus_proche, path)
        else:
            return None  # Aucun joueur trouvé

    def get_nearest_empty_cell(self, board):
        goal = None
        start = (self.x, self.y)

        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            # Si une case vide est trouvée, retourne le chemin
            if board.matrice[current_node[0]][current_node[1]] == board.case_vide:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return path[::-1]

            for dx, dy in neighbors:
                next_node = current_node[0] + dx, current_node[1] + dy
                new_cost = cost_so_far[current_node] + 1

                # Si la case est vide ou une caisse, alors on l'ajoute au chemin
                if self.is_empty_or_explosive_tile(board, next_node):
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + self.heuristic(goal, next_node)
                        heapq.heappush(open_set, (priority, next_node))
                        came_from[next_node] = current_node

        return None  # Aucune case vide trouvée

    def heuristic(self, a, b):
        if a is None or b is None:
            return 0
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def is_valid(self, board, position):
        x, y = position
        return 0 <= x < len(board.matrice) and 0 <= y < len(board.matrice[0])

    def is_empty_or_box(self, board, position):
        x, y = position

        if(self.just_place_bomb):
            return self.is_empty_or_box2(board, position)

        val = (self.is_valid(board, position) and
                not(self.is_this_explosive_tile(board, x,y)) and
                (board.matrice[x][y] == board.case_vide or
                 board.matrice[x][y] == board.CAISSE or
                 self.check_if_player_in_pos(board, x, y) or
                 (board.matrice[x][y] == board.CASE_MULTI_OBJET
                  and not(self.check_if_bomb_in_list(board, self.get_objet_from_multi_objet_case(board, x, y))))))
        return val

    def is_this_explosive_tile(self, board, x, y):
        for i in reversed(range(len(board.list_bombe_timer))):
            for direction in range(4):
                for j in range(board.RAYON_BOMBE):
                    if direction == 0:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][1] + j < board.taille and board.list_bombe_timer[i][1] + j >= 0:
                                if board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] + j] in [board.matrice[x][y]]:
                                    return True
                    if direction == 1:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][1] - j >= 0 and board.list_bombe_timer[i][1] - j < board.taille:
                                if board.matrice[board.list_bombe_timer[i][0]][board.list_bombe_timer[i][1] - j] in [board.matrice[x][y]]:
                                    return True
                    if direction == 2:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][0] + j < board.taille and board.list_bombe_timer[i][0] + j >= 0:
                                if board.matrice[board.list_bombe_timer[i][0] + j][board.list_bombe_timer[i][1]] in [board.matrice[x][y]]:
                                    return True
                    if direction == 3:
                        # verifier que l index ne sort pas de la matrice
                        if board.list_bombe_timer[i][0] - j >= 0 and board.list_bombe_timer[i][0] - j < board.taille:
                                if board.matrice[board.list_bombe_timer[i][0] - j][board.list_bombe_timer[i][1]] in [board.matrice[x][y]]:
                                    return True
        return False
    def is_empty_or_box2(self, board, position):
        x, y = position
        return (self.is_valid(board, position) and
                (board.matrice[x][y] == board.case_vide or board.matrice[x][y] == board.CAISSE or self.check_if_player_in_pos(board, x, y)))

    def is_empty_or_explosive_tile(self, board, position):
        x, y = position
        return (self.is_valid(board, position) and
                (board.matrice[x][y] == board.case_vide or
                 self.check_if_player_in_pos(board, x, y) or
                (board.matrice[x][y] == board.CASE_MULTI_OBJET
                 and not (self.check_if_bomb_in_list(board, self.get_objet_from_multi_objet_case(board, x, y)))) or
                 self.is_this_explosive_tile(board, x ,y)
                 )
                )

    def check_if_player_in_pos(self, board, x, y):
        posJoueur = board.get_position_joueur()[0]
        for joueur in posJoueur:
            if(joueur[0] == x and joueur[1] == y):
                return True
        return False

    def check_if_bomb_in_list(self, board, list):
        if board.BOMBE in list: return True
        return False
    def get_objet_from_multi_objet_case(self, board, x, y):
        for case in board.list_contenu_case:
            if(case[0] == x and case[1] == y):
                return case[2]

    def astar(self, board, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return path[::-1]

            for dx, dy in neighbors:
                next_node = current_node[0] + dx, current_node[1] + dy
                new_cost = cost_so_far[current_node] + 1
                if self.is_empty_or_box(board, next_node):
                    if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                        cost_so_far[next_node] = new_cost
                        priority = new_cost + self.heuristic(goal, next_node)
                        heapq.heappush(open_set, (priority, next_node))
                        came_from[next_node] = current_node

        return None  # No path found

if __name__ == "__main__":
    # -------------------------------initialisation board et agent ---------------------------------
    b = map.board(10)
    b.generer_mur()
    b.generer_caisse_indestructible()
    # je passe mon conteneur joueur a true pour dire que les joueurs sont attribués a un agent pour les tests
    b.conteneur_joueur[0][1] = True  # joueur 1
    b.conteneur_joueur[1][1] = True  # joueur 2
    # associer un agent a un id_joueur
    agent_1 = agentIntentionel(b.conteneur_joueur[0][0])
    agent_2 = agentIntentionel(b.conteneur_joueur[1][0])
    # initialisation des joueurs sur la map
    b.initialiser_pos_joueur_sur_map()  # ATTENTION : cette action doit etre faite avant de generer les caisses destructible
    # init pos agent
    list = b.get_position_joueur()
    if list != None:
        # recup id joueur et coordonnee correspondante a l agent
        for joueur in list[0]:
            if joueur[2] == agent_1.id_joueur:
                agent_1.init_pos_depart(joueur[0], joueur[1])
            if joueur[2] == agent_2.id_joueur:
                agent_2.init_pos_depart(joueur[0], joueur[1])
    b.generer_caisse_destructible(8)  # seuil equilibré...
    print(list)
    print(agent_1.x, agent_1.y)
    print(agent_1.id_joueur)
    print(b.matrice)
    print("agent1: x:", agent_1.x)
    print("agent1: y:", agent_1.y)
    print("agent2: x:", agent_2.x)
    print("agent2: y:", agent_2.y)
    #print("agent1 agent le plus proche:", agent_1.get_joueur_plus_proche_joueur(b))
    agent_1.choisir_coup(b)
    print(agent_1.x, agent_1.y)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
    agent_1.choisir_coup(b)
    print(b.matrice)
