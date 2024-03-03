import random

def generate_maze(width, height):
		maze = [[1] * (width * 2 + 1) for _ in range(height * 2 + 1)]

		def depth_first_search(x, y):
				directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
				random.shuffle(directions)
				for dx, dy in directions:
						nx, ny = x + dx * 2, y + dy * 2
						if 0 < nx < width * 2 and 0 < ny < height * 2 and maze[ny][nx]:
								maze[y + dy][x + dx] = 0
								maze[ny][nx] = 0
								depth_first_search(nx, ny)

		depth_first_search(1, 1)
		maze[1][0] = 0  # entrance
		maze[height * 2 - 1][width * 2] = 0  # exit
		return maze

def print_maze(maze):
		for row in maze:
				print("".join(["#" if cell else " " for cell in row]))


width = 10
height = 10
maze = generate_maze(width, height)
print_maze(maze)
