from collections import deque
import random
from math import sqrt

def print_labyrinth(maze):
    for row in maze:
        for element in row:
            print(element, end=' ')
        print()

def bfs_labyrinth(maze, start, end):
    queue = deque()
    queue.append(start)
    # Create a 2D array to keep track of visited nodes
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    visited[start[0]][start[1]] = True
    # Create a 2D array to store the parent of each node
    parent = [[None for _ in range(len(maze[0]))] for _ in range(len(maze))]
    # Array of row and column vectors for traversing the maze
    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]

    while queue:
        curr = queue.popleft()
        # If the current node is the destination, construct and return the path
        if curr == end:
            return construct_path(parent, end)
        x, y = curr[0], curr[1]
        for i in range(4):
            if is_valid(maze, x + row[i], y + col[i]) and not visited[x + row[i]][y + col[i]]:
                visited[x + row[i]][y + col[i]] = True
                parent[x + row[i]][y + col[i]] = curr
                queue.append((x + row[i], y + col[i]))
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
    maze = [['.' for _ in range(m)] for _ in range(n)]
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

def rbfs(maze, start, end):
    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    parent = [[None for _ in range(len(maze[0]))] for _ in range(len(maze))]
    f = euclidean_distance(start, end)
    return rbfs_recursive(maze, start, end, f, visited, parent)

def rbfs_recursive(maze, curr, end, f, visited, parent):
    visited[curr[0]][curr[1]] = True
    if curr == end:
        return construct_path(parent, end)
    best_f = float('inf')
    for i in range(curr[0]-1,curr[0]+2):
        for j in range(curr[1]-1,curr[1]+2):
            if is_valid(maze, i, j) and not visited[i][j]:
                parent[i][j] = curr
                g = euclidean_distance(curr, (i, j))
                h = euclidean_distance((i, j), end)
                new_f = max(f, g + h)
                path = rbfs_recursive(maze, (i, j), end, new_f, visited, parent)
                if path is not None:
                    return path
                best_f = min(best_f, new_f)
    return None


if __name__ == "__main__":
    maze, start, end = generate_labyrinth(10, 20, 0.2)
    bfs_path = bfs_labyrinth(maze, start, end)
    rbfs_path = rbfs(maze, start, end)
    print_labyrinth(maze)
    print(f'bfs {bfs_path}\n')
    print(f'rbfs {rbfs_path}')