from mazegen import *
import pyxel
PlayerX = 0
PlayerY = 21
def print_maze(maze):
	column = 0
	for row in maze:
		for index, item in enumerate(row):
			if index * 16 - PlayerX < 48 and index * 16 - PlayerX > - 48 and column * 16 - PlayerY < 48 and column * 16 - PlayerY > - 48:
				if item == 1:
					pyxel.rect(index*16,column*16,16,16,0)
				if item == 0:
					pyxel.blt(index * 16, column * 16, 0, 0, 0, 16,16)
			else:
				pyxel.rect(index*16,column*16,16,16,0)
		column += 1

def isColliding(PlayerX, PlayerY, x2, y2, w2, h2):
    return (PlayerX < x2 + w2 and
            PlayerX + 5 > x2 and
            PlayerY < y2 + h2 and
            PlayerY + 5 > y2)

def isEnd():
	global PlayerX,PlayerY
	if PlayerX > 272:
		maze = generate_maze(width, height)
		PlayerX = 0
		PlayerY = 0


def isCollidingWithWall(maze):
	global PlayerX, PlayerY
	column = 0
	for row in maze:
		for index, item in enumerate(row):
			if isColliding(PlayerX,PlayerY, index*16,column*16,16,16) == True and maze[column][index] == 1:
				PlayerX = 1
				PlayerY = 21
		column += 1

#dimension du labyrinthe de default
width = 8
height = 8
#on genere le labyrinthe
maze = generate_maze(width, height)
pyxel.init(width=272,height = 272, title= "Maze Runner")
pyxel.load("my_resource.pyxres")

def update():
	global PlayerX,PlayerY
	if pyxel.btnp(pyxel.KEY_Q):
		pyxel.quit()
	if pyxel.btn(pyxel.KEY_D):
		PlayerX += 2
	if pyxel.btn(pyxel.KEY_A):
		PlayerX -= 2
	if pyxel.btn(pyxel.KEY_W):
		PlayerY -= 2
	if pyxel.btn(pyxel.KEY_S):
		PlayerY += 2
	isCollidingWithWall(maze)
	isEnd()
def draw():
	print_maze(maze)
	pyxel.rect(PlayerX,PlayerY,5,5,8)
pyxel.run(update, draw)