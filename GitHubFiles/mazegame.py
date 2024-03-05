from mazegen import *
import pyxel

PlayerX = 0
PlayerY = 21
anim_state = 240
# La variable qui initialize quelle direction le sprite du personnage fais face
player_face_state = 1

gameStarted = False


def print_maze(maze):
    column = 0
    for row in maze:
        for index, item in enumerate(row):
            #On verifie quelles coordonnees devres etre cree et quelles devraient etre laisser dans le "broullard"(Qui veut dire qu'on cache leur nature) car elle est trop loin
            if index * 16 - PlayerX < 48 and index * 16 - PlayerX > - 48 and column * 16 - PlayerY < 48 and column * 16 - PlayerY > - 48:
                #Si la coordonnee est un mur on met la texture d'un mur
                if item == 1:
                    pyxel.blt(index * 16, column * 16, 0, 0, 0, 16, 16)
                # Si la coordonnee est un chemin on met la texture du chemin
                if item == 0:
                    pyxel.blt(index * 16, column * 16, 0, 0, 16, 16, 16)
            #Si ce n'est pas une coordonnes qui est assez pres du joueur donc on met la texture d'un mur ombrage
            else:
                pyxel.blt(index * 16, column * 16, 0, 48, 0, 16, 16)
        column += 1


def isColliding(PlayerX, PlayerY, x2, y2, w2, h2):
    #On verifie si le joueur est en contacte avec l'objet
    return (PlayerX < x2 + w2 and
            PlayerX + 5 > x2 and
            PlayerY < y2 + h2 and
            PlayerY + 5 > y2)


def isEnd():
    global PlayerX, PlayerY, width, height, maze
    #On verifie si le joueur a passe la fin
    if PlayerX > window_size:
        #On genere un nouveau labyrinthe
        maze = generate_maze(width, height)
        #On transporte le joueur au debut
        PlayerX = 1
        PlayerY = 21

def isStart():
    global PlayerX
    #On verifie si le joueur essaie de partir du labyrinthe par l'entree
    if PlayerX < 0:
        # On transporte le joueur au debut
        PlayerX = 1
        PlayerY = 21

def CollidingWithWall(maze):
    global PlayerX, PlayerY
    column = 0
    for row in maze:
        for index, item in enumerate(row):
            #On verifie si le joueur est en contact avec un 'cell' qui est un mur
            if isColliding(PlayerX, PlayerY, index * 16, column * 16, 16, 16) == True and maze[column][index] == 1:
                #Pour chaque pat qu'il prend vers le mur, il prend la meme quantite en arriere donc sa revient a pas de mouvement
                if pyxel.btn(pyxel.KEY_D):
                    PlayerX -= 2
                if pyxel.btn(pyxel.KEY_A):
                    PlayerX += 2
                if pyxel.btn(pyxel.KEY_W):
                    PlayerY += 2
                if pyxel.btn(pyxel.KEY_S):
                    PlayerY -= 2
        column += 1


# on calcule la taille du window en fonction du width et height
window_size = width * 2 * height * 2 + 16
# on genere le labyrinthe
maze = generate_maze(width, height)
pyxel.init(width=window_size, height=window_size, title="Maze Runner")
pyxel.load("my_resource.pyxres")


def update():
    global PlayerX, PlayerY, player_face_state, gameStarted
    # On ferme le jeux si le joueur pousse Q
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    #On verifie si le jeux a commence
    if gameStarted == False:
        #On commence le jeu si le joueur pousse ENTER
        if pyxel.btn(pyxel.KEY_RETURN):
            gameStarted =True
    # On verifie si le jeux a commence
    if gameStarted == True:
        #On deplace le joueur si il pousse WASD, aussi on communique quelle direction if faut afficher qu'il bouche(1,gauche;2,droite;3,en haut;4,en bas)
        if pyxel.btn(pyxel.KEY_D):
            PlayerX += 2
            player_face_state = 2
        if pyxel.btn(pyxel.KEY_A):
            PlayerX -= 2
            player_face_state = 1
        if pyxel.btn(pyxel.KEY_W):
            PlayerY -= 2
            player_face_state = 3
        if pyxel.btn(pyxel.KEY_S):
            PlayerY += 2
            player_face_state = 4
        #On appelle les fonctions qui doivent etre appeles chaque frame(voir documentation pour leurs utilite)
        CollidingWithWall(maze)
        isEnd()
        isStart()


def draw():
    # On verifie si le jeux a commence
    if gameStarted == False:
        global anim_state
        for row in range(window_size // 16):
            for column in range(window_size // 16):
                #On va de droite en gauche dans l'image cree avec pyxel editor, si on attent la limit de gauche on recommence a droite
                if anim_state == 0:
                    pyxel.blt(column * 16, row * 16, 0, anim_state, 120, 16, 16)
                    anim_state = 240
                else:
                    pyxel.blt(column * 16, row * 16, 0, anim_state, 120, 16, 16)
            #On specifie sur quelle row on veux le mot START
            if row == 9:
                for column in range(window_size // 16):
                    #Sur chaque colonne on affiche une lettre
                    if column == 6:
                        pyxel.blt(column * 16, row * 16, 1, 0, 24, 16, 16)
                    if column == 7:
                        pyxel.blt(column * 16, row * 16, 1, 16, 24, 16, 16)
                    if column == 8:
                        pyxel.blt(column * 16, row * 16, 1, 32, 24, 16, 16)
                    if column == 9:
                        pyxel.blt(column * 16, row * 16, 1, 48, 24, 16, 16)
                    if column == 10:
                        pyxel.blt(column * 16, row * 16, 1, 64, 24, 16, 16)
        anim_state -= 1

    # On verifie si le jeux a commence
    elif gameStarted == True:
        #On appelle cette fonction pour afficher graphiquement le labyrinthe
        print_maze(maze)
        #On change la texture du joueur dependant de quelle direction il bouge
        if player_face_state == 1:
            pyxel.blt(PlayerX, PlayerY, 0, 0, 41, 7, 5)
        elif player_face_state == 2:
            pyxel.blt(PlayerX, PlayerY, 0, 9, 41, 7, 5)
        elif player_face_state == 3:
            pyxel.blt(PlayerX, PlayerY, 0, 0, 48, 5, 7)
        elif player_face_state == 4:
            pyxel.blt(PlayerX, PlayerY, 0, 10, 48, 5, 7)

#pyxel.run commence la boucle du jeu
pyxel.run(update, draw)
