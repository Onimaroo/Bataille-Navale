from upemtk import *
from time import sleep
from random import*

############################# Fonctions #############################

def appartient(lst, val):
    i = 0
    while i < len(lst):
        if lst[i] == val:
            return i
        i += 1
    return None
    
def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """

    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case
    
#### Fonctions: Menus ####
    
def affiche_cases_choix(position):
    """Fonction qui gère le curseur du menu (position = position du curseur)"""
    x, y = position
    if x == 0: #x = abscisse
        if y == 0: #y = ordonnee
            f = (0, 0, 299, 200) #f = coordonnee du rectangle a creer
        elif y == 1:
            f = (0, 200, 299, 400)
        elif y == 2:
            f = (0, 400, 299, 599)
    if x == 1:
        if y == 0:
            f = (299, 0, 599, 200)
        elif y == 1:
            f = (299, 200, 599, 400)
        elif y == 2:
            f = (299, 400, 599, 599)
    (x1, y1, x2, y2) = f
    rectangle(x1, y1, x2, y2,
    couleur = 'Black', remplissage = 'grey')
    texte(65, 60, ("1 navire de\n   6 cases"))
    texte(370, 60,("2 navires de\n   5 cases"))
    texte(65, 260,("3 navires de\n   4 cases"))
    texte(370, 260,("4 navires de\n   3 cases"))
    texte(65, 460,("5 navires de\n   2 cases"))
    texte(370, 460,("6 navires de\n   1 case"))
    
def position_choix(position, touche): 
    """Fonction qui gère le déplacement du curseur avec les évènements du clavier (touche = Variable qui stocke l'évènement saisi au clavier)
    >>> position_choix((0 , 1), 'Down')
    [0, 2, True]
    """
    x, y = position
    condition = True #Condition utilise pour plus tard: True pour faire fonctionner la fonction, False pour le cas contraire
    if touche == 'z' or touche == 'Up': 
        if y > 0: #Si le curseur n'est pas au bord de la fenetre
            y -= 1 # y = Ordonnee du curseur
    elif touche == 's' or touche == 'Down':
        if y < 2 :
            y += 1
    elif touche == 'q' or touche == 'Left':
        if x > 0:
            x -= 1 # x = Abscisse du curseur
    elif touche == 'd' or touche == 'Right':
        if x < 1: #Si le curseur n'est pas au bord de la fenetre
            x += 1
    elif touche == 'Return':
        condition = False
    fe = [x, y, condition]
    return fe
    
#### Fonctions: Placement des bateaux ####


def quadrillage(ordre):
    """Fonction qui dessine le quadrillage (ordre = Valeur de condition qui verifie dans quel partie du jeu nous sommes pour creer un quadrillage adéquat)"""

    if ordre == 'Placement':  #Plateau de jeu pour le moment du placement
        x = 0
        y = - taille_case
        while x < 1000: #Boucle qui trace les colonnes
            x += taille_case #On se decale pour tracer une nouvelle ligne/colonne
            ligne(x, 0, x , 1000, couleur='Grey', epaisseur=1)
        while y < 1000: #Boucle qui trace les lignes
            y += taille_case
            ligne(0, y, 1000, y, couleur='Grey', epaisseur=1)
        texte(1070, 0, 'Instructions:')
        rectangle(1050, 40, 1150, 160, epaisseur = 2)
        texte(1158, 90, 'Monter')
        image(1100, 100, 'Z.png')
        rectangle(1050,190, 1150, 310, epaisseur = 2)
        texte(1158, 240, 'Gauche')
        image(1100, 250, 'Q.png')
        rectangle(1050, 340, 1150, 460, epaisseur = 2)
        texte(1158, 390, 'Descendre')
        image(1100, 400, 'S.png')
        rectangle(1050, 490, 1150, 610, epaisseur = 2)
        texte(1158, 540, 'Droite')
        image(1100, 550, 'D.png')
        rectangle(1050, 640, 1150, 760, epaisseur = 2)
        texte(1158, 690, 'Rotation Gauche')
        image(1100, 700, 'A.png')
        rectangle(1050, 790, 1150, 910, epaisseur = 2)
        texte(1158, 840, 'Rotation Droite')
        image(1100, 850, 'E.png')
        
    if ordre == 'Bataille': #Plateau de jeu pour le moment de la bataille
        x = 0
        y = - taille_case
        while x < 600: #Quadrillage de gauche
            x += taille_case
            ligne(x, 0, x , 600, couleur='Grey', epaisseur=1)
        while y < 600:
            y += taille_case
            ligne(0, y, 600, y, couleur='Grey', epaisseur=1)
        x = taille_case * largeur_plateau
        y = - taille_case
        while x > 900: #Quadrillage de droite
            x -= taille_case
            ligne(x, 0, x, 600, couleur='Grey', epaisseur=1)
        while y < 600:
            y += taille_case
            ligne(900, y, taille_case * largeur_plateau, y, couleur='Grey', epaisseur=1)
            
def bateau_liste(taille_bateau, position_initiale_bateau, sens): 
    """Fonction qui regroupe toutes les coordonnées des bateaux dans une liste (taille_bateau: Taille du bateau, position_initiale_bateau: Coordonnées (liste) initiales du bateau, sens: Sens du bateau)
    >>> bateau_liste(3, [6 , 5], 1)
    [ [6, 5], [7, 5], [8 , 5] ]
    """
    x = position_initiale_bateau[0][0] #Abscisse de la position du bateau
    y = position_initiale_bateau[0][1] #Ordonnee de la position du bateau
    compteur = 0 #Compteur qui va aussi designer la case du bateau
    if sens == 0: #Si le bateau est du sens vertical
        while compteur < taille_bateau - 1:
            compteur += 1
            y -= 1 #On deincremente la valeur de l'ordonnee pour placer le "corps' du bateau derriere la tete
            position_initiale_bateau[compteur][1] = y #Et on applique cette valeur à la liste de la position du bateau
            position_initiale_bateau[compteur][0] = x
    elif sens == 1: #Si le bateau est tournee horizontalement vers la droite
        while compteur < taille_bateau - 1:
            compteur += 1
            x += 1 
            position_initiale_bateau[compteur][0] = x
            position_initiale_bateau[compteur][1] = y
    elif sens == -1: #Si le bateau est tournee horizontalement vers la gauche
        while compteur < taille_bateau -1:
            compteur += 1
            x -= 1
            position_initiale_bateau[compteur][0] = x
            position_initiale_bateau[compteur][1] = y
    return position_initiale_bateau
    

def affichage_bateau(liste_bateau, taille_bateau, lst_bateau_place, placé, couleur):
    """Sert a afficher le bateau a partir des coordonnees stockes dans les autres fonctions. (Liste du bateau qu'on va placer, taille des bateaux, liste des bateaux placés, variable de condition qui distingue les bateaux placés et les bateaux non placés, variable de condition qui gère la couleur du rectangle.)"""
    compteur = -1
    if liste_bateau[0][0] != None:
        while compteur < taille_bateau - 1: #On fait une boucle pour prendre toutes les valeurs de la liste de position du bateau pour ensuite la convertir en pixel pour ainsi creer le rectangle a partir de ces valeurs nouvellement converties.
            compteur += 1
            ff = liste_bateau[compteur][0]
            gg = liste_bateau[compteur][1]
            x, y = case_vers_pixel((ff, gg))
            rectangle(x-taille_case/2, y-taille_case/2, x+taille_case/2, y+taille_case/2, couleur='Green', remplissage='Green', tag = 'visible')
    compteur = -1
    compteur2 = -1
    if placé == 1: #Si un bateau a deja ete placee:
        while compteur < len(lst_bateau_place)-1: #On fait une boucle pour ainsi reprendre les valeurs de la liste du bateau deja place pour re-creer le bateau à sa place
            compteur += 1
            while compteur2 < taille_bateau - 1:
                compteur2 += 1
                ff = lst_bateau_place[compteur][compteur2][0]
                gg = lst_bateau_place[compteur][compteur2][1]
                x, y = case_vers_pixel((ff, gg))
                if couleur == 'Visible':
                    rectangle(x-taille_case/2, y-taille_case/2, x+taille_case/2, y+taille_case/2, couleur='Green', remplissage='Green', tag = 'visible')
                elif couleur == 'Invisible':
                    efface('visible')
            compteur2 = -1

def tourner_bateau(sens, touche, liste_bateau, taille_bateau):
    """Fonction qui fait tourner le bateau (Sens = Sens du bateau (0 pour sens vertical, -1 et 1 pour sens horizontal), liste_bateau = Liste des coordonnées du bateau, taille_bateau = Taille du bateau)
    
    >>> tourner_bateau(1, 'a', [ [6, 5], [7, 5], [8,5] ], 3)
    0
    """
    if sens == 0:
        if touche == 'e' and bateau_liste(taille_bateau, liste_bateau, 1)[taille_bateau - 1][0] <= 19: #Si le bateau n'est pas a cote des bords de la fenetre
            sens = 1  #Direction a laquelle le bateau va tourner
    #Sinon, le bateau ne peut pas tourner
        elif touche == 'a' and bateau_liste(taille_bateau, liste_bateau, -1)[taille_bateau - 1][0] >= 0:
            sens = -1
    elif sens == 1:
        if touche == 'a' and bateau_liste(taille_bateau, liste_bateau, 0)[taille_bateau - 1][1] >= 0:
            sens = 0
    elif sens == -1:
        if touche == 'e' and bateau_liste(taille_bateau, liste_bateau, 0)[taille_bateau - 1][1] >= 0:
            sens = 0
    return sens
            
def placer_bateaux(liste_bateau, touche, taille_bateau): 
    """Fonction utilise pour deplacer et placer les bateaux (liste_bateau = Liste des coordonnées du bateau, touche = Variable qui stocke l'évènement saisi au clavier, taille_bateau = Taille du bateau)
    >>> placer_bateau([ [6, 5], [7, 5], [8,5] ], 'Up', 3)
    [6, 4, True]
    >>> placer_bateau([ [6, 5], [7, 5], [8,5] ], 'Return', 3)
    [6, 5, False]
    """
    x = liste_bateau[0][0]
    y = liste_bateau[0][1]
    xx = liste_bateau[taille_bateau - 1][0]
    yy = liste_bateau[taille_bateau - 1][1] #x, y, xx, yy = Coordonnées du rectangle
    condition = True #Condition utilise pour plus tard: True pour faire fonctionner la fonction, False pour le cas contraire
    if touche == 'Up' or touche == 'z':
        if y > 0 and yy > 0: #Si le bateau n'est pas aux bords de la fenetre
            y -= 1 #Le bateau se deplace vers la gauche. Etc.
    elif touche == 'Down' or touche == 's':
        if y < 19 and yy < 19:
            y += 1
    elif touche == 'Left' or touche == 'q':
        if x > 0 and xx > 0:
            x -= 1
    elif touche == 'Right' or touche == 'd':
        if x < 19 and xx < 19:
            x += 1
    elif touche == 'Return':
        condition = False
    fe = [x, y, condition]  #On retourne cette valeur pour qu'on puisse reprendre les coordonnees du bateau apres un deplacement
    return fe
    

def superposition(bateau_placé, bateau_a_placer, taille_bateau):
    """Fonction qui evite la superposition de bateaux (bateau_placé = Liste du bateau qu'on cherche a placer, bateau_a_placer = Liste du bateau déjà placé, taille_bateau = Taille des deux bateaux)
    >>>superposition([ [6, 5], [7, 5], [8, 5] ] , [ [6, 7], [6, 6], [6, 5] ] , 3)
    True"""
    compteur  = taille_bateau
    while compteur >= 0:
        compteur -= 1
        x = bateau_a_placer[compteur][0]
        y = bateau_a_placer[compteur][1]
        compteur2 = len(bateau_placé)
        while compteur2 > 0:
            compteur2 -= 1
            compteur3 = taille_bateau
            while compteur3 > 0:
                compteur3 -= 1
                if x == bateau_placé[compteur2][compteur3][0] and y == bateau_placé[compteur2][compteur3][1]:
                    return True
    return False
            
### Fonctions: Gestion de la bataille ###

def afficher_croix(x, y, tour):
    """Fonction qui affiche une croix (croix = Symbole qui signifie que le joueur/ordi a manqué son tir) à la position du clic (x et y = Coordonnées du clic, tour = Variable de condition: Si tour = 'Joueur', c'est le tir du joueur et si tour = 'Ordi', c'est le tir de l'ordinateur)""" 
    x, y = case_vers_pixel((x, y))
    if tour == 'Joueur':
        if x > taille_case * 30 and y < taille_case * 20:
            ligne(x - taille_case/2, y - taille_case/2, x + taille_case/2, y + taille_case/2, couleur = 'Red', epaisseur = 2)
            ligne(x + taille_case/2, y - taille_case/2, x - taille_case/2, y + taille_case/2, couleur = 'Red', epaisseur = 2)
            return True
        else:
            return False
    elif tour == 'Ordi':
        ligne(x - taille_case/2, y - taille_case/2, x + taille_case/2, y + taille_case/2, couleur = 'Red', epaisseur = 2)
        ligne(x + taille_case/2, y - taille_case/2, x - taille_case/2, y + taille_case/2, couleur = 'Red', epaisseur = 2)

    
def contact(clic, liste_bateau, tour):
    """Vérifie le contact entre le tir et le bateau, puis change l'état du bateau si c'est le cas (True si touché, False sinon) (clic = Coordonnées du clic, liste_bateau = Liste du bateau, tour = Variable qui determine le tour)
    >>> contact([34, 14, False] , [[[36, 14, False], [35, 14, False], [34, 14, False], [33, 14, False], [32, 14, False], [31, 14, False]]], 'Joueur')
    [[[36, 14, False], [35, 14, False], [34, 14, True], [33, 14, False], [32, 14, False], [31, 14, False]]]
    """
    global touche_joueur, touche_ordi, score_joueur, score_ordi #Commande qui permet d'utiliser les variables en dehors de la fonction
    bateau = 0
    while bateau < len(liste_bateau): #Pour chaque bateau
        case = 0
        while case < len(liste_bateau[bateau]): #Pour chaque case du bateau
            if liste_bateau[bateau][case] == clic: #Si la case parcourut est égal aux coordonnées du clic:
                a = liste_bateau[bateau][case]
                x, y, veri = a
                liste_bateau[bateau][case] = [x, y, True]
                if tour == 'Joueur':
                    touche_joueur = True
                    score_joueur +=  1
                elif tour == 'Ordi':
                    touche_ordi = True
                    score_ordi += 1
                return liste_bateau
            case += 1
        bateau += 1
    return liste_bateau
    
def affiche_toucher(liste_bateau):
    """Fonction qui affiche un rectangle rouge ( = Symbole qui signifie que le joueur/ordi a touché un bateau) à la position du clic (liste_bateau = Liste des coordonnées des bateaux du joueur)"""
    bateau = 0 #Compteur qui va permettre de parcourir la liste des bateaux
    while bateau < len(liste_bateau):
        case = 0 #Compteur qui va permettre de parcourir les coordonnées des cases de chaque bateau
        while case < len(liste_bateau[bateau]):
            verif = liste_bateau[bateau][case][2]
            if verif == True:
                x = liste_bateau[bateau][case][0]
                y = liste_bateau[bateau][case][1]
                x, y = case_vers_pixel((x, y))
                rectangle(x - taille_case / 2, y - taille_case / 2, x + taille_case / 2, y + taille_case / 2, remplissage = 'red')
            case += 1
        bateau += 1

def en_vue(x, y, liste_bateau):
    """Fonction qui renvoie True si l'une des 8 cases adjacentes du tir est une case d'un navire (x = abscisse du clic , y = ordonnee du clic, liste_bateau = Liste du bateau)
   >>> en_vue(35, 15, [[[36, 14, False], [35, 14, False], [34, 14, False], [33, 14, False], [32, 14, False], [31, 14, False]]])
   True
    """
    bateau = 0
    while bateau < len(liste_bateau):
        case = 0
        while case < len(liste_bateau[0]):
            if [x - 1, y - 1, False] == liste_bateau[bateau][case] or [x - 1, y, False] == liste_bateau[bateau][case] or [x - 1, y + 1, False] == liste_bateau[bateau][case] or [x, y - 1, False] == liste_bateau[bateau][case] or [x, y + 1, False] == liste_bateau[bateau][case] or [x + 1, y - 1, False] == liste_bateau[bateau][case] or [x + 1, y, False] == liste_bateau[bateau][case] or [x + 1, y + 1, False] == liste_bateau[bateau][case]: #On etudie une condition qui prend les 8 cases adjacentes à la case cliqué, puis verifie si la coordonnée d'au moins une ces cases appartient à la liste des coordonnées du bateau.
                return True
            case += 1
        bateau += 1
    return False
    
def coule(liste_bateau, taille_bateau, tour):
    """
    Tableau qui verifie si un bateau a coulé (liste_bateau = Liste des coordonnées du bateau du joueur, taille_bateau = Taille (nombre de cases) des bateaux)
    >>> coule ( [[[36, 14, True], [35, 14, True], [34, 14, True], [33, 14, True], [32, 14, True], [31, 14, True]]], 6, "Joueur" )
    True
    """
    global coule_nb_joueur, coule_nb_ordi
    bateau = 0
    coule = 0 
    nbre_cases_touche = 0
    while bateau < len(liste_bateau): #Pour chaque bateau
        case = 0
        nbre_cases_touche = 0
        while case < len(liste_bateau[0]): #Pour chaque case du bateau
            if liste_bateau[bateau][case][2] == True: #Si la case d'un bateau a été touché:
                nbre_cases_touche += 1 #On incrémente cette variable
            else:
                break
            case += 1
            if nbre_cases_touche == taille_bateau: #Si la variable incrementé atteint la taille du bateau
                coule += 1
                break #On sort de la boucle

        bateau += 1
    if tour == 'Joueur':
        if coule == coule_nb_joueur: #Si la variable coule est egal au nombre de bateaux coulés du joueur
            coule_nb_joueur += 1
            return True
    elif tour == 'Ordi':
        if coule == coule_nb_ordi:
            coule_nb_ordi += 1
            return True
    else:
        return False
        
def fin_de_jeu(liste_bateau):
    """Tableau qui verifie l'état des bateaux (liste_bateau = Liste des coordonnées du bateau du joueur)
    >>> fin_de_jeu( [[[36, 14, True], [35, 14, True], [34, 14, True], [33, 14, True], [32, 14, True], [31, 14, True]]]
    False
    """
    bateau = 0
    while bateau < len(liste_bateau): #On crée une boucle imbriqué pour gérer les deux cas ou la liste des coordonnées des bateaux est soit une liste avec 6 coordonnées (1 bateau à 6 cases), soit plusieurs listes possèdant chacune leurs coordonnées propres (tout les autres types de bateau)
        case = 0
        while case < len(liste_bateau[0]):
            if liste_bateau[bateau][case][2] == False:
                return True
            case += 1
        bateau += 1
    return False
   
############################# Jeu #############################

### Jeu: Menu ###

taille_case = 10
largeur_plateau = 60
hauteur_plateau = 60
framerate = 10
cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
efface_tout()

ordre = (0, 0)
SortieDuMenu = True

#Boucle qui affiche le menu de choix de navire

while True:
    efface_tout()
    affiche_cases_choix(ordre)
    mise_a_jour()
    ev = donne_ev()
    ty = type_ev(ev)
    if ty == 'Quitte':
        break
    elif ty == 'Touche':
        print(touche(ev))
        position = position_choix(ordre, touche(ev))
        x = position[0]
        y = position[1]
        SortieDuMenu = position[2]
        ordre = x, y
    if SortieDuMenu == False:
        break
    sleep(0.5/framerate)
ferme_fenetre()

taille_case = 50
largeur_plateau = 28
hauteur_plateau = 20

cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
efface_tout()

lst_bateaux_place = [] #la liste de tous les bateaux placé sur le terrain
liste_bateau = [[6, 5]] #Soit la position au temps 0 du bateau
sens = 0  #Soit le sens dans lequel le bateau est(peut etre egal soit a -1, 0 ou 1)
x, y = ordre
if x == 0: #Determine le nombre de bateau et sa taille en fonction de la position choisi par l'utilisateur
    if y == 0:
        nbbateau = 1
        taille_bateau = 6
    elif y == 1:
        nbbateau = 3
        taille_bateau = 4
    elif y == 2:
        nbbateau = 5
        taille_bateau = 2
elif x == 1:
    if y == 0:
        nbbateau = 2
        taille_bateau = 5
    elif y == 1:
        nbbateau = 4
        taille_bateau = 3
    elif y == 2:
        nbbateau = 6
        taille_bateau = 1

nbbateau_bataille = nbbateau #On stocke le nombre de bateaux dans une variable pour l'utiliser plus tard dans le programme

placé = 0
lst_bateaux_place_pre = []
lst_bateaux_place = []
compteur = taille_bateau -1
while compteur > 0: #Boucle qui permet d'initialiser liste_bateau
    compteur -= 1
    liste_bateau += [[liste_bateau[0][0], liste_bateau[0][1]]]
    
#### Jeu: Placements ###


## Boucle principale qui gère le placement des bateaux ##

while True:
    efface_tout()
    ev = donne_ev()
    ty = type_ev(ev)
    if ty == 'Touche':
        print(touche(ev))
        if touche(ev) == 'a' or touche(ev) == 'e':
            sens = tourner_bateau(sens, touche(ev), liste_bateau, taille_bateau)
        if touche(ev) == 'Return':
            if superposition(lst_bateaux_place, liste_bateau, taille_bateau) == False:
                compteur = -1
                while compteur < taille_bateau - 1: # Cette boucle while n'est active que si l'utilisateur appuie sur entré et que la fonction superposition confirme ce deplacement. Le but est de créer une autre liste qui prend toutes les coordonnées de position_actuelle et ensuite de les insérer dans la liste lst_bateaux_place
                    compteur += 1
                    lst_bateaux_place_pre += [[liste_bateau[compteur][0], liste_bateau[compteur][1]]] #On stocke les valeurs des bateaux places pour les utiliser dans les fonctions de superposition ou encore de placement de bateaux
                    placé = 1
                lst_bateaux_place += [lst_bateaux_place_pre]
                lst_bateaux_place_pre = []
                nbbateau -= 1 #Le nombre de bateaux diminue
        fe = placer_bateaux(liste_bateau, touche(ev), taille_bateau) #Pour deplacer les bateaux
        ff, gg , verif_bateau = fe
        liste_bateau[0][0] = ff #Coordonnees du bateau à placer.
        liste_bateau[0][1] = gg
    liste_bateau = bateau_liste(taille_bateau, liste_bateau, sens)
    affichage_bateau(liste_bateau, taille_bateau, lst_bateaux_place, placé, 'Visible') #On convertit les coordonnees en rectangles
    if nbbateau <= 0: #Une fois qu'il y a plus de bateaux, on sort de la boucle
        break
    quadrillage('Placement')
    mise_a_jour()
ferme_fenetre()

### Jeu: Bataille ###

#Boucle qui ajoute l'état aux bateaux du joueur (False = Non touchée, True = Touché)
bateau = 0
while bateau < len(lst_bateaux_place):
    case = 0
    while case < len(lst_bateaux_place[bateau]):
        lst_bateaux_place[bateau][case] += [False]
        case += 1
    bateau += 1
    
#Initialisation

taille_case = 30
largeur_plateau = 50
hauteur_plateau = 25
lst_croix = []
lst_croix_ordi = [[None, None, False]] # [[Abscisse, Ordonnee, Etat du bateau]]
cree_fenetre(taille_case * largeur_plateau, taille_case * hauteur_plateau)
efface_tout()
touche_joueur = False
touche_ordi = False
coule_nb_joueur = 1
coule_nb_ordi = 1
score_joueur = 0
score_ordi = 0
etat = 0

#Placement des bateaux adverses

taille_bateau_ordi = randint(1, 6)
position_act_ordi = [[None, None, False]]
if taille_bateau_ordi == 1: #1 navire a 6 cases
    bateau_ordi = 6
    place_bateaux_ordi = [[[36, 14, False], [35, 14, False], [34, 14, False], [33, 14, False], [32, 14, False], [31, 14, False]]]
elif taille_bateau_ordi == 2: #2 navires a 5 cases
    bateau_ordi = 5
    place_bateaux_ordi = [[[36, 14, False], [35, 14, False], [34, 14, False], [33, 14, False], [32, 14, False]], [[40, 5, False], [40, 6, False], [40, 7, False], [40, 8, False], [40, 9, False]]]
elif taille_bateau_ordi == 3: #3 navires a 4 cases
    bateau_ordi = 4
    place_bateaux_ordi = [[[32, 2, False], [33, 2, False], [34, 2, False], [35, 2, False]], [[36, 19, False], [36, 18, False], [36, 17, False], [36, 16, False]], [[47, 11, False], [47, 12, False], [47, 13, False], [47, 14, False]]]
elif taille_bateau_ordi == 4: #4 navires a 3 cases
    bateau_ordi = 3
    place_bateaux_ordi = [[[35, 12, False], [35, 13, False], [35, 14, False]], [[32, 9, False], [33, 9, False], [34, 9, False]], [[30, 17, False], [30, 18, False], [30, 19, False]], [[30, 0, False], [31, 0, False], [32, 0, False]]]
elif taille_bateau_ordi == 5: #5 navires a 2 cases
    bateau_ordi = 2
    place_bateaux_ordi = [[[37, 14, False], [37, 15, False]], [[39, 5, False], [40, 5, False]], [[45, 0, False], [45, 1, False]], [[48, 19, False], [49, 19, False]], [[30, 1, False], [30, 2, False]]]
elif taille_bateau_ordi == 6: #6 navires a 1 case
    bateau_ordi = 1
    place_bateaux_ordi = [[[37, 14, False]], [[38, 15, False]], [[39, 16, False]], [[40, 17, False]], [[41, 18, False]], [[42, 19, False]]]

### Boucle principale qui gere la bataille ###

while True:
    efface('texte')
    ev = donne_ev()
    ty = type_ev(ev)
    if ty == 'Quitte':
        break
    quadrillage('Bataille')
    if ev is not None:
        if touche(ev) == 'v' or touche(ev) == 'V':
            if etat % 2 == 0:
                affichage_bateau(liste_bateau, taille_bateau, lst_bateaux_place, 1, 'Visible')
                affichage_bateau(position_act_ordi, bateau_ordi, place_bateaux_ordi, 1, 'Visible')
                etat += 1
            else:
                affichage_bateau(liste_bateau, taille_bateau, lst_bateaux_place, 1, 'Invisible')
                affichage_bateau(position_act_ordi, bateau_ordi, place_bateaux_ordi, 1, 'Invisible')
                etat += 1
    if ty == 'ClicGauche':
        touche_joueur = False
        touche_ordi = False
        efface('texte2') #Pour éviter le surplomb d'affichage de textes
        x_joueur, y_joueur = (abscisse(ev) // taille_case, ordonnee(ev) // taille_case)
        coord_clic = [x_joueur, y_joueur, False]
        x_ordi = randint(0, 19) # = Abscisse du tir de l'ordi
        y_ordi = randint(0, 19) # = Ordonnée du tir de l'ordi
        place_bateaux_ordi = contact(coord_clic, place_bateaux_ordi, 'Ordi')
        tir_joueur = afficher_croix(x_joueur, y_joueur, 'Joueur')
        if appartient(lst_croix, coord_clic) == None and tir_joueur == True:
            lst_croix += [[x_joueur, y_joueur, False]] #On stocke les coordonnées de la croix dans une liste
            boucle = False #Pour la boucle suivante (qui gère les tirs de l'ordi)
            coord_croix = [x_ordi, y_ordi, False]
            while boucle != True:
                if appartient(lst_croix_ordi, coord_croix) == None:
                    boucle = True
                    lst_croix_ordi += [[x_ordi, y_ordi]]
                    lst_bateaux_place = contact(coord_croix, lst_bateaux_place, 'Joueur')
                    afficher_croix(x_ordi, y_ordi, 'Ordi')
            affiche_toucher(place_bateaux_ordi)
            affiche_toucher(lst_bateaux_place)
            
            # Annonces du plateau du joueur
            
            if coule(lst_bateaux_place, taille_bateau, 'Ordi') == True:
                texte(100, 600 , "Coulé !", couleur = 'red', taille = 24, tag = 'texte2')
            elif touche_joueur == True:
                texte(100, 600, "Touché !", couleur = 'red', taille = 24, tag = 'texte2')
            elif en_vue(x_ordi, y_ordi, lst_bateaux_place) == True:
                texte(100, 600, "En vue !", couleur = 'yellow', taille = 24, tag = 'texte2')
            elif touche_joueur == False:
                texte(100, 600, "Rien", couleur = 'black', taille = 24, tag = 'texte2')
            
            #Annonces du plateau de l'ordi
            
            if coule(place_bateaux_ordi, bateau_ordi, 'Joueur') == True:
                texte(1000, 600, "Coulé !", couleur = 'green', taille = 24, tag = 'texte2')
            elif touche_ordi == True:
                texte(1000, 600, "Touché !", couleur = 'green', taille = 24, tag = 'texte2')
            elif en_vue(x_joueur, y_joueur, place_bateaux_ordi) == True:
                texte(1000, 600, "En vue !", couleur = 'yellow', taille = 24, tag = 'texte2')
            elif touche_ordi == False:
                texte(1000, 600, "Rien", couleur = 'black', taille = 24, tag = 'texte2')
            
        #Nombre de bateaux des joueurs
         
        score_joueur = nbbateau_bataille - (coule_nb_joueur - 1)
        score_ordi = taille_bateau_ordi - (coule_nb_ordi - 1)
        
    #Gestion de fin de jeu
    
    alive_joueur = fin_de_jeu(lst_bateaux_place)
    alive_ordi = fin_de_jeu(place_bateaux_ordi)
    if alive_ordi == False: #Si l'ordi n'a plus de bateaux:
        sleep(2)
        efface_tout()
        texte((largeur_plateau * taille_case) // 2.5, (hauteur_plateau * taille_case) // 2, "VICTOIRE !", couleur="blue", ancrage = 'center', taille = 25)
        attend_ev()
        break
    if alive_joueur == False: #Si le joueur n'a plus de bateaux:
        sleep(2)
        efface_tout()
        texte((largeur_plateau * taille_case) // 1.5, (hauteur_plateau * taille_case) // 2, "DEFAITE", couleur="blue", ancrage = 'center', taille = 25)
        attend_ev()
        break
        
    # Gestion des textes
    
    textscore_joueur = "Bateaux presents:",nbbateau_bataille - (coule_nb_ordi - 1)
    textscore_ordi = "Bateaux presents:",taille_bateau_ordi - (coule_nb_joueur - 1)
    texte(100, 650, textscore_joueur, couleur = 'black', taille = 24, tag = 'texte')
    texte(950, 650, textscore_ordi, couleur = 'black', taille = 24, tag = 'texte')
    texte(650, 240, " <- Joueur", taille = 24)
    texte(650, 360, "Ordi -> ", taille = 24)
    texte(605, 300, "(Appuyez sur 'v' pour passer en mode visuel)", taille = 11)
    mise_a_jour()
    
ferme_fenetre()
