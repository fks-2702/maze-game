import random
import pyxel


def generate_maze(width, height):
		maze = [[1] * (width * 2 + 1) for i in range(height * 2 + 1)]
        #on initalize le labyrinthe
		def depth_first_search(x, y):
				directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
				#la liste de directions possible
				random.shuffle(directions)
				for dx, dy in directions:
						#on ajoute le direction choisie a la position actuelle pour obtenir la nouvelle position 
						nx, ny = x + dx * 2, y + dy * 2
						#on verifie que la position est bien dans le labyrinthe
						if 0 < nx < width * 2 and 0 < ny < height * 2 and maze[ny][nx]:
								maze[y + dy][x + dx] = 0
								maze[ny][nx] = 0
								#on appelle la fonction pour la nouvelle position reccursivement
								depth_first_search(nx, ny)
        #on genere le labyrinthe
		depth_first_search(1, 1)
		maze[1][0] = 0  # entre
		maze[height * 2 - 1][width * 2] = 0  # sortie
		return maze

