from collections import deque
import random
from math import sqrt

def print_labyrinth(maze):
    for row in maze:
        for element in row:
            print(element, end=' ')
        print()

def bfs_labyrinth(maze, start, end, iterations, dead_ends, states):
    queue = deque()
    queue.append(start)
    visited = [[False for i in range(len(maze[0]))] for i in range(len(maze))]
    visited[start[0]][start[1]] = True
    parent = [[None for i in range(len(maze[0]))] for i in range(len(maze))]
    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]
    unique_nodes = set()
    unique_nodes.add(start)

    while queue:
        curr = queue.popleft()
        iterations += 1
        unvisited_neighbors = 0
        if curr == end:
            return construct_path(parent, end), iterations, dead_ends, states, unique_nodes
        x, y = curr[0], curr[1]
        for i in range(4):
            states += 1
            if is_valid(maze, x + row[i], y + col[i]) and not visited[x + row[i]][y + col[i]]:
                unvisited_neighbors += 1
                visited[x + row[i]][y + col[i]] = True
                parent[x + row[i]][y + col[i]] = curr
                queue.append((x + row[i], y + col[i]))
                unique_nodes.add((x + row[i], y + col[i]))
        if unvisited_neighbors == 0:
            dead_ends += 1
    return None

def is_valid(maze, x, y):
    if x < 0 or y < 0 or x >= len(maze) or y >= len(maze[0]):
        return False
    if maze[x][y] == '#':
        return False
    return True

def construct_path(parent, curr):
    if not parent[curr[0]][curr[1]]:
        return [curr]
    return construct_path(parent, parent[curr[0]][curr[1]]) + [curr]

def generate_labyrinth(n, m, density):
    maze = [['.' for i in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if random.random() < density:
                maze[i][j] = '#'
    start = (random.randint(0, n-1), random.randint(0, m-1))
    end = (random.randint(0, n-1), random.randint(0, m-1))
    while maze[start[0]][start[1]] == '#':
        start = (random.randint(0, n-1), random.randint(0, m-1))
    while maze[end[0]][end[1]] == '#':
        end = (random.randint(0, n-1), random.randint(0, m-1))
    maze[start[0]][start[1]] = 'S'
    maze[end[0]][end[1]] = 'E'
    return maze, start, end

def euclidean_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def rbfs(maze, start, end, iterations, dead_ends, states):
    visited = [[False for i in range(len(maze[0]))] for i in range(len(maze))]
    parent = [[None for i in range(len(maze[0]))] for i in range(len(maze))]
    f = euclidean_distance(start, end)
    unique_states = set()
    unique_states.add(start)
    path, iterations, dead_ends, states, unique_states = rbfs_recursive(maze, start, end, f, visited, parent, iterations, dead_ends, states, unique_states)
    return path, iterations, dead_ends, states, unique_states

def rbfs_recursive(maze, curr, end, f, visited, parent, iterations, dead_ends, states, unique_states):
    visited[curr[0]][curr[1]] = True
    # increment the counter variable
    iterations += 1
    states += 1
    unique_states.add(curr)
    if curr == end:
        return construct_path(parent, end), iterations, dead_ends, states, unique_states
    x, y = curr[0], curr[1]
    min_f = float('inf')
    next_node = None
    dead_end = True
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if is_valid(maze, x + dx, y + dy) and not visited[x + dx][y + dy]:
            dead_end = False
            g = euclidean_distance(curr, (x + dx, y + dy))
            h = euclidean_distance((x + dx, y + dy), end)
            temp_f = max(f, g + h)
            if temp_f < min_f:
                min_f = temp_f
                next_node = (x + dx, y + dy)
                parent[x + dx][y + dy] = curr
    if dead_end:
        dead_ends += 1
    if not next_node:
        return None, iterations, dead_ends, states, unique_states
    return rbfs_recursive(maze, next_node, end, min_f, visited, parent, iterations, dead_ends, states, unique_states)

def main():
    iterations = 0
    states = 0
    dead_ends = 0
    unique_states = 0
    m = int(input('Enter the size of maze: '))
    maze, start, end = generate_labyrinth(m, m, 0.2)

    option = -1
    while option != 1 and option != 2:
        option = int(input('Print 1 to use BFS\nPrint 2 to use RBFS\n'))


    if option == 1:
        bfs_path, iterations, dead_ends, states, unique_states = bfs_labyrinth(maze, start, end, iterations, dead_ends,
                                                                                states)
        print(f'bfs {bfs_path}\n')
        print_labyrinth(maze)

    if option == 2:
        rbfs_path, iterations, dead_ends, states, unique_states = rbfs(maze, start, end, iterations, dead_ends, states)
        while rbfs_path == None:
            maze, start, end = generate_labyrinth(m, m, 0.2)
            rbfs_path, iterations, dead_ends, states, unique_states = rbfs(maze, start, end, iterations, dead_ends, states)
        print(f'rbfs {rbfs_path}')
        print_labyrinth(maze)

    print(f'start: {start}, end: {end}\niterations: {iterations}\ndead ends: {dead_ends}\namount of states: {states}\nstates in memory: {len(unique_states)}')


if __name__ == "__main__":
    main()