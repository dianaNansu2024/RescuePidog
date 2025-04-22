import pygame
import random
import time
import heapq
from collections import deque
import matplotlib.pyplot as plt

# Set up Pygame
pygame.init()

# Constants
GRID_SIZE = 15  # Grid size (15x15)
CELL_SIZE = 40  # Size of each cell
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Survivor Representation
NUM_SURVIVORS = 5  # Number of survivors to find

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Algorithm Performance Comparison")

# Initialize font for displaying text
font = pygame.font.SysFont('Arial', 24)

# Define the robot and human classes
class Searcher:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.path = []

    def move(self, direction):
        """ Move the searcher in a given direction """
        if direction == 'UP' and self.y > 0:
            self.y -= 1
        elif direction == 'DOWN' and self.y < GRID_SIZE - 1:
            self.y += 1
        elif direction == 'LEFT' and self.x > 0:
            self.x -= 1
        elif direction == 'RIGHT' and self.x < GRID_SIZE - 1:
            self.x += 1

    def get_position(self):
        return (self.x, self.y)

    def mark_path(self):
        """ Mark the path that the searcher has traveled """
        self.path.append(self.get_position())

class Robot(Searcher):
    def __init__(self, x=0, y=0, color=BLUE, name="Robot"):
        super().__init__(x, y, color, name)
        self.direction = 'RIGHT'  # Start moving right
        self.row = 0  # Start at the first row
        self.col = 0  # Start at the first column
        self.grid_map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Occupancy grid

    def move(self, x, y):
        """ Move the robot to a new position """
        self.x = x
        self.y = y
        self.grid_map[y][x] = 1  # Mark the position as visited

    def mark_path(self):
        """ Mark the path the robot takes """
        self.path.append(self.get_position())

    def update_grid(self):
        """ Update the grid map during the robot's movement """
        self.grid_map[self.y][self.x] = 1

    def get_position(self):
        return (self.x, self.y)

# Dijkstra's Algorithm for pathfinding
def dijkstra(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[1]][neighbor[0]] == 0:
                new_cost = current_cost + 1  # Each step has the same cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost, neighbor))
                    came_from[neighbor] = current
    return []

# A* Algorithm for pathfinding
def a_star(start, goal, grid):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[1]][neighbor[0]] == 0:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor)
                    heapq.heappush(open_set, (priority, neighbor))
                    came_from[neighbor] = current
    return []

# Breadth-First Search (BFS) for pathfinding
def bfs(start, goal, grid):
    queue = deque()
    queue.append(start)
    came_from = {}
    came_from[start] = None

    while queue:
        current = queue.popleft()

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[1]][neighbor[0]] == 0:
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
    return []

# Depth-First Search (DFS) for pathfinding
def dfs(start, goal, grid):
    stack = []
    stack.append(start)
    came_from = {}
    came_from[start] = None

    while stack:
        current = stack.pop()

        if current == goal:
            # Reconstruct the path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and grid[neighbor[1]][neighbor[0]] == 0:
                if neighbor not in came_from:
                    stack.append(neighbor)
                    came_from[neighbor] = current
    return []

# Simulate search with a given algorithm
def simulate_search(algorithm, start, survivors, grid):
    path = []
    found_survivors = []
    start_time = time.time()
    time_data = []
    saved_data = []

    while survivors:
        goal = survivors[0]
        if algorithm == 'dijkstra':
            path = dijkstra(start, goal, grid)
        elif algorithm == 'a_star':
            path = a_star(start, goal, grid)
        elif algorithm == 'bfs':
            path = bfs(start, goal, grid)
        elif algorithm == 'dfs':
            path = dfs(start, goal, grid)

        if path:
            for (x, y) in path:
                start = (x, y)
                # Record time and number of survivors saved
                elapsed_time = time.time() - start_time
                time_data.append(elapsed_time)
                saved_data.append(len(found_survivors))

            found_survivors.append(goal)
            survivors.remove(goal)

    return time_data, saved_data

# Plot the results as a line graph
def plot_results(results):
    plt.figure(figsize=(10, 6))

    # Plot each algorithm's performance
    for algorithm, (time_data, saved_data) in results.items():
        plt.plot(time_data, saved_data, label=algorithm.capitalize(), marker='o')

    plt.title('Search Algorithm Performance Comparison')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Number of Survivors Saved')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main simulation loop
def run_simulation():
    # Initialize survivors
    survivors = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(NUM_SURVIVORS)]

    # Simulate each algorithm
    results = {}
    algorithms = ['dijkstra', 'a_star', 'bfs', 'dfs']
    for algorithm in algorithms:
        survivors_copy = survivors.copy()
        time_data, saved_data = simulate_search(algorithm, (0, 0), survivors_copy, [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])
        results[algorithm] = (time_data, saved_data)

    # Plot results
    plot_results(results)

# Run the simulation
run_simulation()