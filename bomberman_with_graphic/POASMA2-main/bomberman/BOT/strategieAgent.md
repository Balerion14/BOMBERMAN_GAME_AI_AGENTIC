## Agent Intentionnel

1)
Si je n'ai pas de target ou que ma target est morte:
    Chercher le joueur le plus proche, le sauvegarder en le définissant comme target

2)
Si je ne suis pas dans une case qui va exploser
    Si caisse entre target et moi
        Poser une bombe
   Sinon je m'approche de target
Sinon
    Aller dans la case la plus proche qui ne va pas exploser et qui est proche de la target
        Poser une boombe

3) Répéter opération autant que nécessaire

## Agent Social
1)
Si je n'ai pas de target ou que ma target est morte:
   Si nombre de joueurs > 2
    Chercher le joueur le deuxieme joueur le plus proche, le sauvegarder en le définissant comme target
   Sinon
    Définir le dernier joueur comme target

2)
Si je ne suis pas dans une case qui va exploser
    Si caisse entre joueur le plus proche et moi
        Poser une bombe
   Sinon je m'approche de target
Sinon
    Aller dans la case la plus proche qui ne va pas exploser et qui est proche de la target
        Poser une boombe

3) Répéter opération autant que nécessaire

