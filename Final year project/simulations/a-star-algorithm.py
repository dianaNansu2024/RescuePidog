import pygame
import random
import time
import heapq

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
pygame.display.set_caption("A* Pathfinding with SLAM")

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

# A* Algorithm for pathfinding
def astar(start, goal, grid):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))  # (f, g, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current == goal:
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
                tentative_g_score = current_g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
                    came_from[neighbor] = current
    return []

# Draw the grid and entities
def draw_grid(robot, human, survivors, elapsed_time, robot_path):
    screen.fill(WHITE)

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

    # Draw the survivors
    for survivor in survivors:
        pygame.draw.rect(screen, RED, (survivor[0] * CELL_SIZE, survivor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the robot and its path
    for (x, y) in robot_path:
        pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
    pygame.draw.circle(screen, robot.color, (robot.x * CELL_SIZE + CELL_SIZE // 2, robot.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    # Display elapsed time
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
    screen.blit(time_text, (WIDTH - 150, HEIGHT - 50))

    pygame.display.flip()

# Main simulation loop with A* and SLAM
def run_simulation():
    robot = Robot(x=0, y=0, color=BLUE, name="Robot")  # Start robot at top-left
    survivors = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)) for _ in range(NUM_SURVIVORS)]
    found_by_robot = []

    start_time = time.time()  # Start the timer
    clock = pygame.time.Clock()
    running = True
    robot_path = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate A* pathfinding towards the first survivor (assuming the robot goes for the first survivor)
        if survivors:
            goal = survivors[0]
            path = astar((robot.x, robot.y), goal, robot.grid_map)
            if path:
                for (next_x, next_y) in path:
                    robot.move(next_x, next_y)
                    robot.update_grid()
                    robot_path.append((robot.x, robot.y))
                    draw_grid(robot, None, survivors, time.time() - start_time, robot_path)
                    time.sleep(0.2)  # Adjust speed of movement
            survivors.remove(goal)

        # Check if all survivors have been found
        if not survivors:
            running = False

        elapsed_time = time.time() - start_time
        draw_grid(robot, None, survivors, elapsed_time, robot_path)

        clock.tick(5)  # Slow down the robot's movement for visibility

    pygame.quit()

# Run the simulation
run_simulation()
