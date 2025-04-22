import numpy as np
import matplotlib.pyplot as plt

# Define grid size
GRID_SIZE = 10
grid = np.zeros((GRID_SIZE, GRID_SIZE))  # 0: Empty, 1: Random robot, 2: Target, 3: Target robot, -1: Obstacle

# Function to plot the grid and handle clicks
def plot_grid():
    plt.imshow(grid, cmap='viridis', interpolation='nearest')
    plt.title("Click to select positions")
    plt.pause(0.1)

# Function to get positions via mouse clicks
def get_position_from_click(prompt):
    print(prompt)
    plt.gcf().canvas.mpl_connect('button_press_event', on_click)
    global clicked_position
    clicked_position = None
    while clicked_position is None:
        plt.waitforbuttonpress()
    x, y = clicked_position
    return int(round(x)), int(round(y))

def on_click(event):
    global clicked_position
    x, y = event.xdata, event.ydata
    if x is not None and y is not None:
        clicked_position = (y, x)

# Prompt user to place obstacles
def place_obstacles():
    num_obstacles = 15
    placed = 0
    while placed < num_obstacles:
        x, y = get_position_from_click(f"Click to place obstacle {placed + 1}")
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x, y] == 0:
            grid[x, y] = -1
            placed += 1
            plot_grid()
        else:
            print("Invalid position or cell occupied. Try again.")

# Function to place a robot using clicks
def place_robot(robot_type):
    while True:
        x, y = get_position_from_click(f"Click to place {robot_type} robot")
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x, y] == 0:
            return [x, y]
        else:
            print("Invalid position or cell occupied. Try again.")

# Main function to run the simulation
def main():
    global clicked_position
    clicked_position = None

    print("--- Robot Searching Simulation ---")
    plot_grid()
    place_obstacles()

    # Get target position
    TARGET = tuple(get_position_from_click("Click to place the target"))
    grid[TARGET] = 2  # Place the target
    plot_grid()

    # Get robot positions
    random_robot_pos = place_robot("random")
    target_robot_pos = place_robot("target-oriented")
    grid[random_robot_pos[0], random_robot_pos[1]] = 1
    grid[target_robot_pos[0], target_robot_pos[1]] = 3
    plot_grid()

    # Function to move a robot randomly, avoiding obstacles
    def move_random(robot_pos):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        np.random.shuffle(directions)
        for move in directions:
            new_pos = [robot_pos[0] + move[0], robot_pos[1] + move[1]]
            if (
                0 <= new_pos[0] < GRID_SIZE and
                0 <= new_pos[1] < GRID_SIZE and
                grid[new_pos[0], new_pos[1]] != -1
            ):
                return new_pos
        return robot_pos  # Stay in place if no valid move

    # Function to move a robot towards the target, avoiding obstacles
    def move_towards_target(robot_pos, target):
        directions = []
        if robot_pos[0] < target[0]:
            directions.append((1, 0))
        elif robot_pos[0] > target[0]:
            directions.append((-1, 0))
        if robot_pos[1] < target[1]:
            directions.append((0, 1))
        elif robot_pos[1] > target[1]:
            directions.append((0, -1))

        for move in directions:
            new_pos = [robot_pos[0] + move[0], robot_pos[1] + move[1]]
            if (
                0 <= new_pos[0] < GRID_SIZE and
                0 <= new_pos[1] < GRID_SIZE and
                grid[new_pos[0], new_pos[1]] != -1
            ):
                return new_pos
        return robot_pos  # Stay in place if no valid move

    # Simulation loop
    steps = 0
    while True:
        steps += 1

        # Clear robot positions from grid
        grid[random_robot_pos[0], random_robot_pos[1]] = 0
        grid[target_robot_pos[0], target_robot_pos[1]] = 0

        # Move robots
        random_robot_pos = move_random(random_robot_pos)
        target_robot_pos = move_towards_target(target_robot_pos, TARGET)

        # Update grid with new positions
        grid[random_robot_pos[0], random_robot_pos[1]] = 1  # Random robot
        grid[target_robot_pos[0], target_robot_pos[1]] = 3  # Target-oriented robot
        grid[TARGET] = 2  # Target

        # Check if robots found the target
        if tuple(random_robot_pos) == TARGET:
            print(f"Random robot found the target in {steps} steps!")
            break
        if tuple(target_robot_pos) == TARGET:
            print(f"Target-oriented robot found the target in {steps} steps!")
            break

        # Visualization
        plt.imshow(grid, cmap='viridis', interpolation='nearest')
        plt.title("Robot Searching Simulation with Obstacles")
        plt.pause(0.5)

    plt.show()

main()
