import bomberman.moteur_jeu.board as map

class agent:

    x, y = -1, -1 # coordonnee de l'agent
    id_joueur = 0 # id du joueur auquel est associé l'agent qui correspond a un des elements de la liste des joueur possible a mettre sur sur la map (voir list "conteneur_joueur dans class board")
    list_coordonne_bombre_actif_enemie = [] # (x,y,rayon, temps_restant) tempps_restant en nombre tour
    list_coordonne_bombre_actif_allie = [] # (x,y,rayon, temps_restant) tempps_restant en nombre tour
    list_mur_and_caisse_indestructible = [] # (x,y) liste des coordonnee des murs et caisses indestructible
    list_caisse_destructible = [] # (x,y) liste des coordonnee des caisses destructible
    list_case_vide = [] # (x,y) liste des coordonnee des cases vide
    list_agent_enemie = [] # (x,y) liste des coordonnee des agents enemie (c est a dire tous les agent sauf lui meme)
    list_case_voisine_deplacement = [] # (x,y) liste des cases voisines ou l'agent peut se deplacer

    def __init__(self, associer_id_joueur) :
        self.id_joueur = associer_id_joueur
    
    def init_pos_depart(self, x, y) :
        self.x, self.y = x, y
    
    def choisir_coup(self, board) : # board est un objet de type board (voir class board)
        #Faire ici le calcul du coup a jouer
        return -1
    
    # false si erreur, true si ok
    def move(self, x_new, y_new, board) : # board est un objet de type board (voir class board)
        #Faire ici le deplacement de l'agent
        print(f"agent {self.id_joueur} essaye de  move depuis un x : {self.x} et y : {self.y} vers un x : {x_new} et y : {y_new}")
        x_verif, y_verif = board.move_case(x_new, y_new, self.x, self.y,  self.id_joueur)
        if x_verif == self.x and y_verif == self.y :
            print("Erreur deplacement agent")
            return False
        self.x, self.y = x_verif, y_verif # mettre a jour les coordonnee de l'agent
        print(f"agent {self.id_joueur} a move sur un x : {self.x} et y : {self.y}")
        return True
    
    def put_bombe(self, board) : # board est un objet de type board (voir class board)
        #Faire ici la pose de bombe
        print(f"agent {self.id_joueur} essaye de  put_bombe sur un x : {self.x} et y : {self.y}")
        verif_resultat = board.poser_bombe(self.x, self.y, self.id_joueur)
        if verif_resultat == False :
            print("Erreur pose bombe")
            return False
        print(f"agent {self.id_joueur} a put_bombe sur un x : {self.x} et y : {self.y}")
        return True

    def is_valid_move(self, x, y, board) : # board est un objet de type board (voir class board), x et y sont des coordonnee, matrice est la matrice du board
        # si la case est de type multi objet (plusieurs objet sur la meme case) verifier qu il n y a pas de bombe dessus
        if board.matrice[x][y] == board.CASE_MULTI_OBJET :
            for coordonnee_bombe in board.list_bombe_timer :
                if coordonnee_bombe[0] == x and coordonnee_bombe[1] == y :
                    return False
            # si aucune bombe sur la case alors on peut se deplacer dessus
            return True
        if board.matrice[x][y] == board.case_vide or board.matrice[x][y] in [joueur[0] for joueur in board.conteneur_joueur]:
            return True
        return False
    
    def calculer_liste_case_voisine_deplacement(self, board) :
        if self.is_valid_move(self.x+1, self.y, board) :
            self.list_case_voisine_deplacement.append([self.x+1, self.y])
        if self.is_valid_move(self.x-1, self.y, board) :
            self.list_case_voisine_deplacement.append([self.x-1, self.y])
        if self.is_valid_move(self.x, self.y+1, board) :
            self.list_case_voisine_deplacement.append([self.x, self.y+1])
        if self.is_valid_move(self.x, self.y-1, board) :
            self.list_case_voisine_deplacement.append([self.x, self.y-1])


if __name__ == "__main__":
    # -------------------------------initialisation board et agent ---------------------------------
    b = map.board(10)
    b.generer_mur()
    b.generer_caisse_indestructible()
    # je passe mon conteneur joueur a true pour dire que les joueurs sont attribués a un agent pour les tests
    b.conteneur_joueur[0][1] = True # joueur 1
    # associer un agent a un id_joueur
    agent_1 = agent(b.conteneur_joueur[0][0])
    # initialisation des joueurs sur la map
    b.initialiser_pos_joueur_sur_map() # ATTENTION : cette action doit etre faite avant de generer les caisses destructible
    # init pos agent
    list = b.get_position_joueur()
    if list != None :
        # recup id joueur et coordonnee correspondante a l agent
        for joueur in list[0] :
            if joueur[2] == agent_1.id_joueur :
                agent_1.init_pos_depart(joueur[0], joueur[1])
    b.generer_caisse_destructible(8)# seuil equilibré...
    print(list)
    print(agent_1.x, agent_1.y)
    print(agent_1.id_joueur)
    print(b.matrice)
    # ---------------------------------test deplacement --------------------------------------------
    # test deplacement
    agent_1.move(agent_1.x+1, agent_1.y, b)
    print(agent_1.x, agent_1.y)
    print(b.matrice)
    # test bombe
    agent_1.put_bombe(b)
    print(b.matrice)
    print(b.list_contenu_case)
    print(b.list_bombe_timer)
    # ok test...




    # Pas besoin de verifier leur validite car c est deja fait pour chaque action possible dans la classse board.
    # Faire methode : choisir coup et eventuellement d autre methodes si besoin pour calcule comme tout les coup possible pour un joueur
    # choisir coup retournera l action a faire et on aura juste a appeler soit methode de board  pour faire action soit de l agent.
    # l idee est qu on pourra redefinir un agent en heritant des methodes indispensables et en faire de nouvelle si besoin

    """
    _structure init
        -creation board...
        -creation agent (different type agent possible (heritage))
        init board avecen disant quel agent ont ete attribue a quel joueur
        gener leur position et les caisses...
    _boucle game
        affichage board
        mise_a_jour_timer_bombe
        choix_coup pour chaque agent
            faire action
            affichage gestion errreur
        affichage board
        gestion fin de partie # faire dans board
    """

        

    