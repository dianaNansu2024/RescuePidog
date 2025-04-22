import pygame
import random
import time
import heapq

# Set up Pygame
pygame.init()

# Constants
GRID_SIZE = 15  # Grid size (15x15)
CELL_SIZE = 50  # Size of each cell
WIDTH, HEIGHT = GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Survivor Representation
NUM_SURVIVORS = 10  # Number of survivors to find

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survivor Search Simulation with Dijkstra and SLAM")

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
        self.map = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # SLAM map
        self.visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # Visited cells
        self.path = []

    def dijkstra(self, start, goal):
        """ Dijkstra's algorithm for pathfinding """
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE:
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        heapq.heappush(open_set, (tentative_g_score, neighbor))

        return None

    def update_map(self, x, y, value):
        """ Update the SLAM map with new information """
        self.map[y][x] = value

    def systematic_move(self, survivors):
        """ Robot follows a systematic search pattern using Dijkstra's algorithm """
        if not self.path:
            # Find the nearest unvisited cell
            nearest_survivor = None
            min_distance = float('inf')
            for survivor in survivors:
                if not self.visited[survivor[1]][survivor[0]]:
                    distance = abs(self.x - survivor[0]) + abs(self.y - survivor[1])
                    if distance < min_distance:
                        min_distance = distance
                        nearest_survivor = survivor

            if nearest_survivor:
                self.path = self.dijkstra((self.x, self.y), nearest_survivor)

        if self.path:
            next_cell = self.path.pop(0)
            self.x, self.y = next_cell
            self.visited[self.y][self.x] = True
            self.update_map(self.x, self.y, 1)

    def mark_path(self):
        """ Mark the systematic path the robot takes """
        self.path.append(self.get_position())

# Create the grid (with survivors randomly placed)
def generate_survivors():
    survivors = []
    for _ in range(NUM_SURVIVORS):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        survivors.append((x, y))
    return survivors

# Draw the grid and entities
def draw_grid(robot, human, survivors, found_by_robot, found_by_human, elapsed_time):
    screen.fill(WHITE)

    # Draw grid lines
    for i in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))

    # Draw the survivors
    for survivor in survivors:
        pygame.draw.rect(screen, RED, (survivor[0] * CELL_SIZE, survivor[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the robot and human
    pygame.draw.circle(screen, robot.color, (robot.x * CELL_SIZE + CELL_SIZE // 2, robot.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
    pygame.draw.circle(screen, human.color, (human.x * CELL_SIZE + CELL_SIZE // 2, human.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

    # Display survivor count and elapsed time
    robot_text = font.render(f"Robot found: {len(found_by_robot)}", True, BLACK)
    human_text = font.render(f"Human found: {len(found_by_human)}", True, BLACK)
    time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)

    # Position the text on the screen
    screen.blit(robot_text, (10, HEIGHT - 50))
    screen.blit(human_text, (10, HEIGHT - 30))
    screen.blit(time_text, (WIDTH - 150, HEIGHT - 50))

    # Update the screen
    pygame.display.flip()

# Main simulation loop
def run_simulation():
    robot = Robot(x=0, y=0, color=BLUE, name="Robot")  # Ensure robot starts from the top-left corner
    human = Searcher(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1), YELLOW, "Human")

    survivors = generate_survivors()
    found_by_robot = []
    found_by_human = []

    start_time = time.time()  # Start the timer
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Simulate robot's systematic movement using Dijkstra's algorithm
        robot.systematic_move(survivors)
        robot.mark_path()

        # Simulate human's random movement
        human.move(random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']))
        human.mark_path()

        # Check for survivors
        if (robot.x, robot.y) in survivors and (robot.x, robot.y) not in found_by_robot:
            found_by_robot.append((robot.x, robot.y))
            survivors.remove((robot.x, robot.y))
        if (human.x, human.y) in survivors and (human.x, human.y) not in found_by_human:
            found_by_human.append((human.x, human.y))
            survivors.remove((human.x, human.y))

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Draw the grid and entities along with the stats
        draw_grid(robot, human, survivors, found_by_robot, found_by_human, elapsed_time)

        # Check if all survivors have been found
        if len(found_by_robot) + len(found_by_human) == NUM_SURVIVORS:
            running = False

        clock.tick(10)  # Set frame rate

    # Print final results to the console
    print(f"Robot found {len(found_by_robot)} survivors.")
    print(f"Human found {len(found_by_human)} survivors.")
    print(f"Total time: {elapsed_time:.2f} seconds.")

    pygame.quit()

# Run the simulation
run_simulation()