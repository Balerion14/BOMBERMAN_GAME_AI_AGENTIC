import numpy as np

class board:
    taille = 0
    matrice = np.zeros((taille, taille), dtype=int)
    CASE_MULTI_OBJET = 4
    MUR = 1
    CAISSE = 2
    case_vide = 0
    BOMBE = 3
    RAYON_BOMBE = 3 # rayon de la bombe (destruction en croix sur 3 cases de rayon)
    TIMER = 3 # temps avant explosion de la bombe en nombre de tour
    conteneur_joueur = [[5, False], [6, False], [7, False], [8, False]] # 1 element = [id_joueur, attribue ou pas sur un agent]
    list_bombe_timer = [] # 1 element = [x,y,rayon, temps_restant] temps_restant en nombre tour
    list_contenu_case = [] # 1 element = [x,y,[contenu,contenu,...]] liste des coordonnees des cases avec leur contenu si elle contiennent plus de 1 objet: (contenu peut etre plusieurs joueur et une bombe par exemple).Attention, une bombe par case maximum par contre plusieurs joueurs peuvent etre sur une meme case

    def __init__(self, taille):
        self.taille = taille
        self.matrice = np.zeros((taille, taille), dtype=int)
    
    # ATTENTION, cette fonction doit etre modifiee si on decide de mettre plus de 4 joueurs sur la map
    def initialiser_pos_joueur_sur_map(self):
        est_place = False
        for i in range(len(self.conteneur_joueur)):
            est_place = False
            if self.conteneur_joueur[i][1] == True: # si le joueur est attribue a un agent
                for x in range(self.taille):
                    if est_place:
                        break
                    for y in range(self.taille):
                        if (x == 1 or x == self.taille - 2) and (y == 1 or y == self.taille - 2):
                            if self.matrice[x][y] == self.case_vide:
                                self.matrice[x][y] = self.conteneur_joueur[i][0]
                                est_place = True
                                break

    def verif_if_this_case_is_neighbour(self, x, y, x_origine, y_origine, id_joueur):
        # verif que id_joueur est bien un joueur de la matrice
        if id_joueur not in [joueur[0] for joueur in self.conteneur_joueur]:
            print("id joueur n est pas un joueur de la matrice")
            return False
        # on verifie que le x_origine et y_origine sont bien les coordonnees d un joueur d id id_joueur
        if self.matrice[x_origine][y_origine] != id_joueur and self.matrice[x_origine][y_origine] != self.CASE_MULTI_OBJET:
            print("x_origine et y_origine ne sont pas les coordonnees d un joueur d id id_joueur")
            return False
        # si la case est multi objet, on verifie que id_joueur est bien sur la case
        if self.matrice[x_origine][y_origine] == self.CASE_MULTI_OBJET:
            if id_joueur not in self.get_objet_multi_case(x_origine, y_origine)[0]:
                print("id_joueur n est pas sur la case multi objet")
                return False
        if x == x_origine + 1 and y == y_origine:
            # on verifie que la case est soit vide soit contient un multi_objet
            if self.matrice[x][y] == self.case_vide or self.matrice[x][y] == self.CASE_MULTI_OBJET:
                return True
        if x == x_origine - 1 and y == y_origine:
            if self.matrice[x][y] == self.case_vide or self.matrice[x][y] == self.CASE_MULTI_OBJET:
                return True
        if x == x_origine and y == y_origine + 1:
            if self.matrice[x][y] == self.case_vide or self.matrice[x][y] == self.CASE_MULTI_OBJET:
                return True
        if x == x_origine and y == y_origine - 1:
            if self.matrice[x][y] == self.case_vide or self.matrice[x][y] == self.CASE_MULTI_OBJET:
                return True
        return False
    
    def verif_if_deplacement_is_not_egale_to_case_origine(self, x, y, x_origine, y_origine):
        if x == x_origine and y == y_origine:
            return False
        return True
    
    def mise_a_jour_ancienne_case(self, x, y, x_origine, y_origine, id_joueur):
        # si notre case d'origine est egale a notre id_joueur, on peut la mettre a case vide
        if self.matrice[x_origine][y_origine] == id_joueur:
            self.matrice[x_origine][y_origine] = self.case_vide
            print("ancienne case passe a vide car j etait seul dessus")
        else:
            # si notre case est sur une case avec plusieurs objet, on doit supprimer notre id_joueur de la liste des contenu de la case
            verif_case_multi_objet = False
            if self.matrice[x_origine][y_origine] == self.CASE_MULTI_OBJET:
                for i in range(len(self.list_contenu_case)):
                    if verif_case_multi_objet:
                        break
                    if self.list_contenu_case[i][0] == x_origine and self.list_contenu_case[i][1] == y_origine:
                        for j in range(len(self.list_contenu_case[i][2])):
                            if self.list_contenu_case[i][2][j] == id_joueur:
                                self.list_contenu_case[i][2].pop(j)
                                print("ancienne case n etait pas vide donc j ai supp mon id_joueur de la liste des contenu de la case")
                                if len(self.list_contenu_case[i][2]) == 1:
                                    self.matrice[x_origine][y_origine] = self.list_contenu_case[i][2][0]
                                    # on supprime la case de la liste des case avec plusieurs objet
                                    self.list_contenu_case.pop(i)
                                    print("il n y a plus qu un seul objet sur la case donc je le met en case simple et mon ancienne case est egale à l objet qui restait dessus sans moi..")
                                verif_case_multi_objet = True
                                break
    
    # si return (x_origine, y_origine) alors le deplacement n a pas ete effectue, si return (x, y) alors le deplacement a ete effectue
    def move_case(self, x, y, x_origine, y_origine, id_joueur):
        # verif deplacement dans la matrice est valide
        if not ((x >= 0 and x < self.taille) and (y >= 0 and y < self.taille)):
            print("deplacement en dehors de la matrice")
            return (x_origine, y_origine)
        # verif aussi les x et y d origine sont valide
        if not ((x_origine >= 0 and x_origine < self.taille) and (y_origine >= 0 and y_origine < self.taille)):
            print("x_origine ou y_origine n est pas valide")
            return (x_origine, y_origine)
        # verif deplacement != case origine
        if not self.verif_if_deplacement_is_not_egale_to_case_origine(x, y, x_origine, y_origine):
            print("impossible de se deplacer sur la meme case que celle d origine")
            return (x_origine, y_origine)
        # verif neighbour # a desactiver pour les tests...
        if not self.verif_if_this_case_is_neighbour(x, y, x_origine, y_origine, id_joueur):
            print("impossible de se deplacer sur cette case car elle n est pas voisine de notre case d origine ou bien on peut pas aller dessus...")
            return (x_origine, y_origine)
        # si c est une case vide, on peut se deplacer dessus
        if self.matrice[x][y] == self.case_vide:
            self.matrice[x][y] = id_joueur
            print("deplacement sur case vide")
            self.mise_a_jour_ancienne_case(x, y, x_origine, y_origine, id_joueur)
            return (x, y) # on renvoie les nouvelles coordonnees
        # si il y a deja un joueur sur la case, on peut se deplacer dessus
        if self.matrice[x][y] in [joueur[0] for joueur in self.conteneur_joueur] or self.matrice[x][y] == self.CASE_MULTI_OBJET:
            save_id_joueur = self.matrice[x][y]
            self.matrice[x][y] = self.CASE_MULTI_OBJET # case avec plusieurs objet
            # regarder dans la liste liste_contenucase si la case est deja presente, si oui on ajoute le joueur a la liste des contenu, sinon on cree une nouvelle case
            for i in range(len(self.list_contenu_case)):
                if self.list_contenu_case[i][0] == x and self.list_contenu_case[i][1] == y:
                    # si il n y a pas de bombe sur la case, on peut ajouter le joueur a la liste des contenu
                    if self.BOMBE not in self.list_contenu_case[i][2]:
                        self.list_contenu_case[i][2].append(id_joueur)
                        print("deplacement sur case avec deja un joueur mais qui etait deja recence comme case special, cettte objet sera ajoute...")
                        self.mise_a_jour_ancienne_case(x, y, x_origine, y_origine, id_joueur)
                        return (x, y)
                    else:
                        # si il y a deja une bombe sur la case, on ne peut pas ajouter le joueur a la liste des contenu
                        print("impossible de se deplacer sur cette case car il y a deja une bombe dessus")
                        return (x_origine, y_origine)
            # si on arrive ici, c est que la case n est pas dans la liste, on la cree et ajoute id_joueur et le joueur qui etait deja sur la case
            self.list_contenu_case.append([x, y, [id_joueur, save_id_joueur]])
            print("deplacement sur case avec deja un joueur mais qui n etait pas dans la liste des cases special a plus de 1 objet...")
            self.mise_a_jour_ancienne_case(x, y, x_origine, y_origine, id_joueur)
            return (x, y)
        else:
            print("impossible de se deplacer sur cette case")
            return (x_origine, y_origine)
    
    def get_objet_multi_case(self, x, y):
        for i in range(len(self.list_contenu_case)):
            if self.list_contenu_case[i][0] == x and self.list_contenu_case[i][1] == y:
                return (self.list_contenu_case[i][2], i)
        return None

    # return False si impossible de poser une bombe, True sinon
    def poser_bombe(self, x, y, id_joueur = 0): # valeur par default pour les tests afin de pouvoir placer des bombes la ou on veut mais en situation de jeu, mettre un argument(id_joueur)
        if id_joueur != 0:
            # verif si id_joueur est bien un joueur de la matrice
            if id_joueur not in [joueur[0] for joueur in self.conteneur_joueur]:
                print("impossible de poser une bombe car id_joueur n est pas un joueur de la matrice")
                return False
            # verif si x et y sont valide
            if not ((x >= 0 and x < self.taille) and (y >= 0 and y < self.taille)):
                print("impossible de poser une bombe car x ou y n est pas valide")
                return False
            # verif si x et y est bien la position du joueur id_joueur pour faire en sorte qu on puisse poser uen bombe que sur sa case
            if self.matrice[x][y] != id_joueur and self.matrice[x][y] != self.CASE_MULTI_OBJET:
                    print("impossible de poser une bombe car x et y ne corresponde pas a id_joueur ni a une case multi objet")
                    return False
            # si c est un multi objet et que x et y ne  corresponde a id joueur dedans
            if self.matrice[x][y] == self.CASE_MULTI_OBJET:
                    if id_joueur not in self.get_objet_multi_case(x, y)[0]:
                        print("impossible de poser une bombe car id_joueur n est pas sur la case x, y multi objet")
                        return False
        if self.matrice[x][y] == self.case_vide:
            self.matrice[x][y] = self.BOMBE
            self.list_bombe_timer.append([x, y, self.RAYON_BOMBE, self.TIMER])
            print("bombe pose sur une case vide")
            return True
        elif self.matrice[x][y] == self.CASE_MULTI_OBJET:
            for i in range(len(self.list_contenu_case)):
                if self.list_contenu_case[i][0] == x and self.list_contenu_case[i][1] == y:
                    # si il n y a pas deja une bombe sur la case, on peut en poser une
                    if self.BOMBE not in self.list_contenu_case[i][2]:
                        self.list_contenu_case[i][2].append(self.BOMBE)
                        self.list_bombe_timer.append([x, y, self.RAYON_BOMBE, self.TIMER])
                        print("bombe pose sur une case multi objet de base")
                        return True
                        #break
                    else:
                        print("impossible de poser une bombe ici car il y en a deja une")
                        #break
                        return False
        elif self.matrice[x][y] in [joueur[0] for joueur in self.conteneur_joueur]:
            # si on est la c est que la case contient un joueur, on peut poser une bombe en creant une case multi objet
            self.list_contenu_case.append([x, y, [self.BOMBE, self.matrice[x][y]]])
            self.matrice[x][y] = self.CASE_MULTI_OBJET
            self.list_bombe_timer.append([x, y, self.RAYON_BOMBE, self.TIMER])
            print("bombe pose car il y avait un joueur sur la case")
            return True
        else:
            print("impossible de poser une bombe ici")
            return False
    
    def mise_a_jour_timer_bombe(self): # tester
        for i in reversed(range(len(self.list_bombe_timer))):
            if self.list_bombe_timer[i][3] > 1:
                self.list_bombe_timer[i][3] = self.list_bombe_timer[i][3] - 1
                print("timer bombe: ", self.list_bombe_timer[i][3])
            else:
                # si il y a une bombe sur la case, on la supprime
                if self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1]] == self.BOMBE:
                    self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1]] = self.case_vide
                else:
                    # si on est sur une case avec plusieurs objet, on doit supprimer la bombe de la liste des contenu de la case ainsi que les autre objets
                    if self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1]] == self.CASE_MULTI_OBJET:
                        list_objet = self.get_objet_multi_case(self.list_bombe_timer[i][0], self.list_bombe_timer[i][1])
                        if list_objet != None:
                            self.list_contenu_case.pop(list_objet[1])
                            self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1]] = self.case_vide
                # destruction des cases en croix sur RAYON_BOMBE cases de rayon à partir de la position de la bombe qui doit exploser
                for direction in range(4):
                    for j in range(self.RAYON_BOMBE):
                        if direction == 0:
                            # verifier que l index ne sort pas de la matrice
                            if self.list_bombe_timer[i][1] + j < self.taille and self.list_bombe_timer[i][1] + j >= 0:
                                if self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] == self.CAISSE or self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] in [joueur[0] for joueur in self.conteneur_joueur]:
                                    self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] = self.case_vide
                                elif self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] == self.CASE_MULTI_OBJET:
                                    list_objet = self.get_objet_multi_case(self.list_bombe_timer[i][0], self.list_bombe_timer[i][1] + j)
                                    if list_objet != None:
                                        # on verfie que la case ne contient pas de bombe
                                        if list_objet[0].count(self.BOMBE) == 0:
                                            # on supprime la case de la liste des case avec plusieurs objet
                                            self.list_contenu_case.pop(list_objet[1])
                                            # la case est maintenant vide
                                            self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] = self.case_vide
                                        else:
                                            # on supprimer juste tout les objet sauf la bombe
                                            list_intermediaire = []
                                            for k in range(len(self.list_contenu_case[list_objet[1]][2])):
                                                if self.list_contenu_case[list_objet[1]][2][k] != self.BOMBE:
                                                    list_intermediaire.append(k)
                                            for b in reversed(list_intermediaire):
                                                self.list_contenu_case[list_objet[1]][2].pop(b)
                                            # si il n y a plus qu une bombe sur la case, on met a jour la matrice
                                            if len(self.list_contenu_case[list_objet[1]][2]) == 1:
                                                self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] + j] = self.list_contenu_case[list_objet[1]][2][0]
                                                # supprimer la case de la liste des case avec plusieurs objet
                                                self.list_contenu_case.pop(list_objet[1])
                        if direction == 1:
                            # verifier que l index ne sort pas de la matrice
                            if self.list_bombe_timer[i][1] - j >= 0 and self.list_bombe_timer[i][1] - j < self.taille:
                                if self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] == self.CAISSE or self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] in [joueur[0] for joueur in self.conteneur_joueur]:
                                    self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] = self.case_vide
                                elif self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] == self.CASE_MULTI_OBJET:
                                    list_objet = self.get_objet_multi_case(self.list_bombe_timer[i][0], self.list_bombe_timer[i][1] - j)
                                    if list_objet != None:
                                        # on verfie que la case ne contient pas de bombe
                                        if list_objet[0].count(self.BOMBE) == 0:
                                            # on supprime la case de la liste des case avec plusieurs objet
                                            self.list_contenu_case.pop(list_objet[1])
                                            # la case est maintenant vide
                                            self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] = self.case_vide
                                        else:
                                            # on supprimer juste tout les objet sauf la bombe
                                            list_intermediaire = []
                                            for k in range(len(self.list_contenu_case[list_objet[1]][2])):
                                                if self.list_contenu_case[list_objet[1]][2][k] != self.BOMBE:
                                                    list_intermediaire.append(k)
                                            for b in reversed(list_intermediaire):
                                                self.list_contenu_case[list_objet[1]][2].pop(b)
                                            # si il n y a plus qu une bombe sur la case, on met a jour la matrice
                                            if len(self.list_contenu_case[list_objet[1]][2]) == 1:
                                                self.matrice[self.list_bombe_timer[i][0]][self.list_bombe_timer[i][1] - j] = self.list_contenu_case[list_objet[1]][2][0]
                                                # supprimer la case de la liste des case avec plusieurs objet
                                                self.list_contenu_case.pop(list_objet[1])
                        if direction == 2:
                            # verifier que l index ne sort pas de la matrice
                            if self.list_bombe_timer[i][0] + j < self.taille and self.list_bombe_timer[i][0] + j >= 0:
                                if self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] == self.CAISSE or self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] in [joueur[0] for joueur in self.conteneur_joueur]:
                                    self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] = self.case_vide
                                elif self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] == self.CASE_MULTI_OBJET:
                                    list_objet = self.get_objet_multi_case(self.list_bombe_timer[i][0] + j, self.list_bombe_timer[i][1])
                                    if list_objet != None:
                                        # on verfie que la case ne contient pas de bombe
                                        if list_objet[0].count(self.BOMBE) == 0:
                                            # on supprime la case de la liste des case avec plusieurs objet
                                            self.list_contenu_case.pop(list_objet[1])
                                            # la case est maintenant vide
                                            self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] = self.case_vide
                                        else:
                                            # on supprimer juste tout les objet sauf la bombe
                                            list_intermediaire = []
                                            for k in range(len(self.list_contenu_case[list_objet[1]][2])):
                                                if self.list_contenu_case[list_objet[1]][2][k] != self.BOMBE:
                                                    list_intermediaire.append(k)
                                            for b in reversed(list_intermediaire):
                                                self.list_contenu_case[list_objet[1]][2].pop(b)
                                            # si il n y a plus qu une bombe sur la case, on met a jour la matrice
                                            if len(self.list_contenu_case[list_objet[1]][2]) == 1:
                                                self.matrice[self.list_bombe_timer[i][0] + j][self.list_bombe_timer[i][1]] = self.list_contenu_case[list_objet[1]][2][0]
                                                # supprimer la case de la liste des case avec plusieurs objet
                                                self.list_contenu_case.pop(list_objet[1])
                        if direction == 3:
                            # verifier que l index ne sort pas de la matrice
                            if self.list_bombe_timer[i][0] - j >= 0 and self.list_bombe_timer[i][0] - j < self.taille:
                                if self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] == self.CAISSE or self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] in [joueur[0] for joueur in self.conteneur_joueur]:
                                    self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] = self.case_vide
                                elif self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] == self.CASE_MULTI_OBJET:
                                    list_objet = self.get_objet_multi_case(self.list_bombe_timer[i][0] - j, self.list_bombe_timer[i][1])
                                    if list_objet != None:
                                        # on verfie que la case ne contient pas de bombe
                                        if list_objet[0].count(self.BOMBE) == 0:
                                            # on supprime la case de la liste des case avec plusieurs objet
                                            self.list_contenu_case.pop(list_objet[1])
                                            # la case est maintenant vide
                                            self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] = self.case_vide
                                        else:
                                            # on supprimer juste tout les objet sauf la bombe
                                            list_intermediaire = []
                                            for k in range(len(self.list_contenu_case[list_objet[1]][2])):
                                                if self.list_contenu_case[list_objet[1]][2][k] != self.BOMBE:
                                                    list_intermediaire.append(k)
                                            for b in reversed(list_intermediaire):
                                                self.list_contenu_case[list_objet[1]][2].pop(b)
                                            # si il n y a plus qu une bombe sur la case, on met a jour la matrice
                                            if len(self.list_contenu_case[list_objet[1]][2]) == 1:
                                                self.matrice[self.list_bombe_timer[i][0] - j][self.list_bombe_timer[i][1]] = self.list_contenu_case[list_objet[1]][2][0]
                                                # supprimer la case de la liste des case avec plusieurs objet
                                                self.list_contenu_case.pop(list_objet[1])
                self.list_bombe_timer.pop(i)

    def get_taille(self):
        return self.taille* self.taille
    
    def get_matrice(self):
        return self.matrice
    
    def get_case(self, x, y):
        return self.matrice[x][y]
    
    def set_case(self, x, y, valeur):
        self.matrice[x][y] = valeur
    
    def get_position_objet(self, joueur, mur, caisse, case_vide):
        position_joueur = []
        for i in range(self.taille):
            for j in range(self.taille):
                if joueur:
                    if self.matrice[i][j] in self.contenuter_joueur:
                        position_joueur.append((i, j, self.matrice[i][j]))
                if mur:
                    if self.matrice[i][j] == self.MUR:
                        position_joueur.append((i, j))
                if caisse:
                    if self.matrice[i][j] == self.CAISSE:
                        position_joueur.append((i, j))
                if case_vide:
                    if self.matrice[i][j] == self.case_vide:
                        position_joueur.append((i, j))
        if len(position_joueur) == 0:
            return None
        else:
            return position_joueur
    
    def generer_mur(self):
        for i in range(self.taille):
            self.matrice[i][0] = self.MUR
            for j in range(self.taille):
                if j == 0 or j == self.taille - 1:
                    self.matrice[i][j] = self.MUR
                if i == 0 or i == self.taille - 1:
                    self.matrice[i][j] = self.MUR

    def generer_caisse_indestructible(self):
        for i in range(self.taille):
            for j in range(self.taille):
                if i % 2 == 0 and j % 2 == 0 and self.matrice[i][j] != self.MUR:
                    if self.matrice[i][j - 1] != self.MUR and self.matrice[i][j + 1] != self.MUR and self.matrice[i - 1][j] != self.MUR and self.matrice[i + 1][j] != self.MUR:
                        self.matrice[i][j] = self.MUR
    
    # plus densite_caisse est élevé, plus il y aura de caisses, car il sera plus probable que le nombre aléatoire soit inférieur au produit seuil * densite_caisse.
    def generer_caisse_destructible(self, densite_caisse=4):
        seuil = 10 # seuil fixe pour la comparaison
        for i in range(self.taille):
            for j in range(self.taille):
                if self.matrice[i][j] == self.case_vide:
                    if (i == 1 or i == self.taille - 2) and (j == 1 or j == self.taille - 2):
                        continue
                    # si la case est une voisine directe d un joueur, on ne met pas de caisse
                    if self.matrice[i][j - 1] in [joueur[0] for joueur in self.conteneur_joueur] or self.matrice[i][j + 1] in [joueur[0] for joueur in self.conteneur_joueur] or self.matrice[i - 1][j] in [joueur[0] for joueur in self.conteneur_joueur] or self.matrice[i + 1][j] in [joueur[0] for joueur in self.conteneur_joueur]:
                        continue
                    # tirage au sort pour savoir si on met une caisse ou pas
                    if np.random.randint(0, 100) < seuil * densite_caisse:
                        self.matrice[i][j] = self.CAISSE

    # recuperer les coordonnees des joueurs sur la map et le nombre de joueur
    # si return None alors il n y a pas de joueur sur la map
    # sinon return (position_joueur, len(position_joueur))
    # si il y a 1 joueur, il a gagne et fin de partie
    def get_position_joueur(self):
        position_joueur = []
        for i in range(self.taille):
            for j in range(self.taille):
                # si la case un multi_objet, verifier le contenu de la case
                if self.matrice[i][j] == self.CASE_MULTI_OBJET:
                    list_objet = self.get_objet_multi_case(i, j)
                    if list_objet != None:
                        for k in range(len(list_objet[0])):
                            if list_objet[0][k] in [joueur[0] for joueur in self.conteneur_joueur]:
                                position_joueur.append((i, j, list_objet[0][k]))
                # si la case est un joueur, on l ajoute a la liste
                if self.matrice[i][j] in [joueur[0] for joueur in self.conteneur_joueur]:
                    position_joueur.append((i, j, self.matrice[i][j]))
        if len(position_joueur) == 0:
            print("aucun joueur sur la map")
            return (position_joueur, len(position_joueur))
        else:
            return (position_joueur, len(position_joueur))
        

if __name__== "__main__":
    # ---------------------init et test de la generation de la map-------------------------------------------
    b = board(10)
    b.generer_mur()
    b.generer_caisse_indestructible()
    # je passe mon conteneur joueur a true pour dire que les joueurs sont attribués a un agent pour les tests
    b.conteneur_joueur[0][1] = True # joueur 1
    b.conteneur_joueur[1][1] = True # joueur 2
    b.conteneur_joueur[2][1] = True # joueur 3
    b.conteneur_joueur[3][1] = True # joueur 4
    # initialisation des joueurs sur la map
    b.initialiser_pos_joueur_sur_map() # ATTENTION : cette action doit etre faite avant de generer les caisses destructible
    b.generer_caisse_destructible(8)# seuil equilibré...
    # ------------------------test des bombes simple pour detruire caisse ou joueur (le test n inclut pas les case_multi_objet)---------------------------------------------------------
    """b.poser_bombe(8, 1)
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print(f"Map avant explosion")
    print(b.get_matrice())
    # test de la mise a jour des bombes
    for i in range(10): # Si le timer d une bombe est a 1, au prochain tour elle explose
        b.mise_a_jour_timer_bombe()
    print(f"Map apres explosion")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print(b.get_matrice())"""
    # ------------------------test des deplacements---------------------------------------------------------
    # test deplacement sur case vide
    print(f"test deplacement sur case vide")
    print(f"Map avant deplacement")
    print(b.get_matrice())
    b.move_case(1, 2, 1, 1, 5)
    print(f"Map apres deplacement")
    print(b.get_matrice())
    # test deplacement sur case non valide
    print("test deplacement case non valide")
    print("map avant deplacement")
    print(b.get_matrice())
    b.move_case(0, 0, 1, 1, 5)
    print("map apres deplacement")
    print(b.get_matrice())
    # test deplacement sur case avec un joueur
    print("test deplacement case avec un joueur")
    print("map avant deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    b.move_case(1, 8, 1, 2, 5)
    print("map apres deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    # test deplacement sur case avec plusieurs objet
    print("test deplacement case avec plusieurs objet")
    print("map avant deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    b.move_case(1, 8, 8, 1, 7)
    print("map apres deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    # test deplacement sur case avec une bombe
    print("test deplacement case avec une bombe")
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    b.poser_bombe(1, 1)
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print("map avant deplacement")
    print(b.get_matrice())
    b.move_case(1, 1, 1, 8, 7)
    print("map apres deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    # test deplacement sur case avec plusieurs objet et une bombe ---test 5---
    """print("test deplacement case avec plusieurs objet et une bombe")
    b.poser_bombe(1, 8)
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print("map avant deplacement")
    print(b.get_matrice())
    b.move_case(1, 8, 8, 8, 8)
    print("map apres deplacement")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")"""
    # -----------------------------------test explosion bombe-----------------------
    # test explosion bombe sur case avec plusieurs objet dont que des joueurs et une bombe
    print("test explosion bombe sur case avec plusieurs objet dont que des joueurs et une bombe")
    b.poser_bombe(2, 8)
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print("map avant explosion")
    print(b.get_matrice())
    for i in range(10): # Si le timer d une bombe est a 1, au prochain tour elle explose
        b.mise_a_jour_timer_bombe()
    print("map apres explosion")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    # test explosion bombe sur case avec plusieurs objet dont que des joueurs et une bombe mais la bombe sur case multi objet n explose pas pour voir si la bombe n est bien pas detruite par l autre bombe
    """print("test explosion bombe sur case avec plusieurs objet dont que des joueurs et une bombe")
    b.poser_bombe(2, 8)
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print("map avant explosion")
    print(b.get_matrice())
    for i in range(10): # Si le timer d une bombe est a 1, au prochain tour elle explose
        if i == 6: # pour reactiver test 5, mettre en la condition i == 6 et b.poser_bombe(1, 8).Et decommenter b.poser_bombe(1, 8) dans le test 5
            b.poser_bombe(1, 8)
        b.mise_a_jour_timer_bombe()
    print("map apres explosion")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")"""
    # test explosion bombe sur case avec plusieurs objet dont des joueurs et pas de bombe
    """print("test explosion bombe sur case avec plusieurs objet dont des joueurs et pas de bombe")
    b.poser_bombe(2, 8)
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")
    print("map avant explosion")
    print(b.get_matrice())
    for i in range(10): # Si le timer d une bombe est a 1, au prochain tour elle explose
        b.mise_a_jour_timer_bombe()
    print("map apres explosion")
    print(b.get_matrice())
    print(f"tableau des cases avec plusieurs objet: {b.list_contenu_case}")
    print(f"tableau des bombes: {b.list_bombe_timer}")"""
    # ------------------------------------------------------Poser des bombes--------------------------------------------
    # test poser bombe sur case vide
    print("test poser bombe sur case vide")
    print("map avant pose bombe")
    print(b.get_matrice())
    print("tableau des bombes avant pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant pose bombe", b.list_contenu_case)
    b.poser_bombe(8, 1)
    print("map apres pose bombe")
    print(b.get_matrice())
    print("tableau des bombes apres pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres pose bombe", b.list_contenu_case)
    # test poser bombe sur case avec un joueur
    print("test poser bombe sur case avec un joueur")
    print("map avant pose bombe")
    print(b.get_matrice())
    print("tableau des bombes avant pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant pose bombe", b.list_contenu_case)
    b.poser_bombe(8, 8)
    print("map apres pose bombe")
    print(b.get_matrice())
    print("tableau des bombes apres pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres pose bombe", b.list_contenu_case)
    # test poser bombe sur case avec plusieurs objet
    print("test poser bombe sur case avec plusieurs objet")
    print("map avant pose bombe")
    print(b.get_matrice())
    print("tableau des bombes avant pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant pose bombe", b.list_contenu_case)
    b.poser_bombe(1, 8)
    print("map apres pose bombe")
    print(b.get_matrice())
    print("tableau des bombes apres pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres pose bombe", b.list_contenu_case)
    # test poser bombe sur case avec une bombe multi objet
    print("test poser bombe sur case avec une bombe multi objet")
    print("map avant pose bombe")
    print(b.get_matrice())
    print("tableau des bombes avant pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant pose bombe", b.list_contenu_case)
    b.poser_bombe(1, 8)
    print("map apres pose bombe")
    print(b.get_matrice())
    print("tableau des bombes apres pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres pose bombe", b.list_contenu_case)
    # test poser bombe sur case en dehors des clou
    """print("test poser bombe sur case en dehors des clou")
    print("map avant pose bombe")
    print(b.get_matrice())
    print("tableau des bombes avant pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant pose bombe", b.list_contenu_case)
    #b.poser_bombe(-1, -1)
    #b.poser_bombe(11, 11, 5)
    #b.poser_bombe(0, 0, 5)
    #b.poser_bombe(1, 1, 20)
    #b.poser_bombe(8, 8, 5)
    #b.poser_bombe(1, 2, 5)
    print("map apres pose bombe")
    print(b.get_matrice())
    print("tableau des bombes apres pose bombe", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres pose bombe", b.list_contenu_case)"""
    # -------------------------crash test deplacement------------------------
    #b.move_case(1, 1, 1, 1, 5)
    print("test deplacement crash test")
    print("map avant deplacement")
    print(b.get_matrice())
    print("tableau des bombes avant deplacement", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet avant deplacement", b.list_contenu_case)
    #b.move_case(1, 7, 1, 8, 6)
    #b.move_case(1, 8, 1, 34, 6)
    #b.move_case(1, 8, 1, 3, 5)
    #b.move_case(2, 8, 1, 8, 5)
    b.move_case(2, 8, 1, 8, 6)
    print("map apres deplacement")
    print(b.get_matrice())
    print("tableau des bombes apres deplacement", b.list_bombe_timer)
    print("tableau des cases avec plusieurs objet apres deplacement", b.list_contenu_case)
    # tout les tests ok.....
    # --------------------------test pour recup position joueur-------------------------
    print("test pour recup position joueur")
    print(b.get_position_joueur())
    # test ok...


    



    


    