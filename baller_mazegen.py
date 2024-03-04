import random, time, os

class Cell: 
    def __init__(self, x, y, with_walls=True):
        self.x = x
        self.y = y
        self.visited = False
        # Walls are  N, E, S, W
        if with_walls:
            self.walls = [True for _ in range(4)] 
        else:
            self.walls = [False for _ in range(4)]

    def nxt(self, grid):
        o = []
        for x, y in [(1, 0), (-1,0), (0, 1), (0, -1)]:
            if self.x+x in [len(grid), -1] or self.y+y in [-1, len(grid)]:
                continue
            child = grid[self.y+y][self.x+x]
            if child.visited:
                continue
            o.append(child)
        return o

def carve(c1, c2):
    # c1 is above c2
    if c2.y > c1.y:
        c1.walls[2] = False
        c2.walls[0] = False

    # c1 is below c2
    elif c2.y < c1.y:
        c1.walls[0] = False
        c2.walls[2] = False

    # c1 is to the left of c2
    elif c2.x > c1.x:
        c1.walls[1] = False
        c2.walls[3] = False

    # c1 is to the right of c2
    elif c2.x < c1.x:
        c1.walls[3] = False
        c2.walls[1] = False

def show(maze):
    os.system('clear')
    w = len(maze[0])
    h = len(maze)

    # Top border
    print(" _" * w)

    for y in range(h):
        # Start with the west wall
        print("|", end="")

        for x in range(w):
            # Bottom wall
            if maze[y][x].walls[2]:
                print("_", end="")
            else:
                print(" ", end="")

            # East wall
            if maze[y][x].walls[1]:
                # For the last cell in a row, always print a wall
                if x == w - 1:
                    print("|", end="")
                else:
                    # Check if the adjacent cell has a west wall
                    if maze[y][x + 1].walls[3]:
                        print("|", end="")
                    else:
                        print(" ", end="")
            else:
                print(" ", end="")

        print()

    # Bottom border
    print()
    return maze


def dfs(side, showProgress=False):
    # create empty maze
    maze = [[Cell(x,y) for x in range(side)] for y in range(side)]
    st = []
    c = maze[0][0]
    while True:
        c.visited = True
        n = c.nxt(maze)
        if n:
            st.append(c)
            nxt = random.choice(n)
            carve(c, nxt)
            c = nxt
            show(maze) if showProgress else None
        elif st:
            c = st.pop()
        else:
            break
    return maze

def wilson(side, showProgress=False):
    maze = [[Cell(x,y) for x in range(side)] for y in range(side)]
    unvisited = set(sum(maze, []))
    initial = random.choice(random.choice(maze))
    initial.visited = True
    unvisited.remove(initial)
    while unvisited:
        # random walk on path
        path = [random.choice(list(unvisited))]
        while not path[-1].visited: # while we haven't hit the existing maze
            for dx, dy in random.sample([(1, 0), (-1, 0), (0, 1), (0, -1)], 4): # random neighbor order
                nx, ny = path[-1].x + dx, path[-1].y + dy # next cell coords
                if 0 <= nx < len(maze) and 0 <= ny < len(maze): # if in bounds of maze
                    next_cell = maze[ny][nx]
                    if next_cell in path: # if loop
                        path = path[:path.index(next_cell) + 1] # remove loop by only keeping the path until the loop
                    else:
                        path.append(next_cell)
                    break
        # carve path
        for i in range(len(path) - 1):
            carve(path[i], path[i + 1])
            path[i].visited = True
            unvisited.remove(path[i])
            show(maze) if showProgress else None
    return maze


def prim_walliter(cell, walls_list, maze):
    x, y = cell.x, cell.y
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] # E, W, S, N
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze) and not maze[ny][nx].visited:
            walls_list.append(((x, y), (nx, ny)))

def prim(side, showProgress=False):
    maze = [[Cell(x, y) for x in range(side)] for y in range(side)]
    walls_list = []

    # Start from a random cell
    start_x, start_y = random.randint(0, side - 1), random.randint(0, side - 1)
    start_cell = maze[start_y][start_x]
    start_cell.visited = True
    prim_walliter(start_cell, walls_list, maze)

    while walls_list:
        # Pick a random wall
        wall = random.choice(walls_list)
        (x1, y1), (x2, y2) = wall

        cell1, cell2 = maze[y1][x1], maze[y2][x2]

        # check if only one of the two cells that the wall divides is visited
        if cell1.visited != cell2.visited:
            carve(cell1, cell2)
            new_cell = cell2 if cell1.visited else cell1
            new_cell.visited = True
            prim_walliter(new_cell, walls_list, maze)
        
        walls_list.remove(wall)

        show(maze) if showProgress else None

    return maze


def btree(side, showProgress=False):
    maze = [[Cell(x, y) for x in range(side)] for y in range(side)]
    for y in range(side):
        for x in range(side):
            neighbors = []
            if y > 0:  # North neighbor
                neighbors.append((x, y - 1))
            if x < side - 1:  # East neighbor
                neighbors.append((x + 1, y))
            
            if neighbors:
                nx, ny = random.choice(neighbors)
                carve(maze[y][x], maze[ny][nx])
            show(maze) if showProgress else None
    return maze

def sidewinder(side, showProgress=False):
    maze = [[Cell(x, y) for x in range(side)] for y in range(side)]

    for y in range(side):
        run = []
        for x in range(side):
            cell = maze[y][x]
            run.append(cell)

            if (x == side - 1) or (not (y == 0) and random.randint(0, 1) == 0):
                # carve north from a random cell in the run
                north_cell = random.choice(run)
                if north_cell.y > 0:
                    carve(north_cell, maze[north_cell.y - 1][north_cell.x])
                run = [] 
            elif not (x == side - 1):
                # carve east
                carve(cell, maze[y][x + 1])
            show(maze) if showProgress else None

    return maze


def maze_generator(alg, side, showProgress=False):
    # match case
    match alg:
        case "dfs":
            # dfs is, well, dfs, nothing much to it
            return dfs(side, showProgress)
        case "wilson":
            # wilson takes a random point on the maze, does a random walk until it hits the existing maze, then carves the path 
            # now w loop removal, 10% off for the first 50 lucky callers
            return wilson(side, showProgress)
        case "prim":
            # prim starts from a random cell, starts removing walls from the cell to its neighbors
            # keeps doing that until all cells are visited
            return prim(side, showProgress)
        case "btree":
            # literally just binary tree
            return btree(side, showProgress)
        case "sidewinder":
            # literally just binary tree, but with a twist *finger guns*
            return sidewinder(side, showProgress)
        case _:
            raise ValueError("Invalid algorithm")



maze = maze_generator("prim", 50, False)
show(maze)



def convert_maze_to_ferris_system(maze):
    h = len(maze)
    w = len(maze[0])
    
    out = [[1] * (w * 2 + 1)]  # preinited with top border

    for y in range(h):
        r1 = [1]
        r2 = [1]

        for x in range(w):
            cell = maze[y][x]
            
            # bottom and right wall
            r1.append(0)
            r1.append(1 if cell.walls[1] else 0)
            r2.append(1 if cell.walls[2] else 0)
            r2.append(1)  # shared wall
            
        # last wall in row2 for border
        r2[-1] = 1

        out.append(r1)
        out.append(r2)

    # bottom border is already in there btw
    return out

for row in convert_maze_to_ferris_system(maze):
    # print with white and black squares
    print("".join("⬜" if x == 1 else "⬛" for x in row))


def benchmark():
    import timeit
    runs = 50
    
    times = {
        "DFS": timeit.timeit(lambda: dfs(50, False), number=runs),
        "Wilson": timeit.timeit(lambda: wilson(50, False), number=runs),
        "Prim": timeit.timeit(lambda: prim(50, False), number=runs),
        "Btree": timeit.timeit(lambda: btree(50, False), number=runs),
        "Sidewinder": timeit.timeit(lambda: sidewinder(50, False), number=runs),
    }
    
    sorted_times = sorted(times.items(), key=lambda x: x[1], reverse=True)

    for i in range(len(sorted_times) - 1):
        print(f"{sorted_times[i][0]} is {sorted_times[i][1]/sorted_times[i+1][1]}x ({sorted_times[i][1]-sorted_times[i+1][1]}s) slower than {sorted_times[i+1][0]}")
    
    print(f"Fastest algorithm ({sorted_times[-1][0]}) is {sorted_times[0][1] / sorted_times[-1][1]}x faster than the slowest one ({sorted_times[0][0]})")
    print("raw times:")
    print(times)
#benchmark()


