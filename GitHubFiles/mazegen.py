import random
#on determine les dimensions de defaut
height = 8
width = 8

def generate_maze(width, height):
		maze = [[1] * (width * 2 + 1) for i in range(height * 2 + 1)]
        #on initalize le labyrinthe
		def depth_first_search(x, y):
				directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
				#la liste de directions possible
				random.shuffle(directions)
				for direction_x, direction_y in directions:
						#on ajoute le direction choisie a la position actuelle pour obtenir la nouvelle position 
						next_x, next_y = x + direction_x * 2, y + direction_y * 2
						#on verifie que la position est bien dans le labyrinthe
						if 0 < next_x < width * 2 and 0 < next_y < height * 2 and maze[next_y][next_x]:
								maze[y + direction_y][x + direction_x] = 0
								maze[next_y][next_x] = 0
								#on appelle la fonction pour la nouvelle position reccursivement
								depth_first_search(next_x, next_y)
        #on genere le labyrinthe
		depth_first_search(1, 1)
		maze[1][0] = 0  # entre
		maze[height * 2 - 1][width * 2] = 0  # sortie
		return maze


