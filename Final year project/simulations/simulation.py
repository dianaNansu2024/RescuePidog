import numpy as np
import matplotlib.pyplot as plt
import time

# Define larger grid size
GRID_SIZE = 15
grid = np.zeros((GRID_SIZE, GRID_SIZE))  # 0: Empty, 1: Random robot, 2: Target, 3: Target robot, -1: Obstacle

# Function to plot the grid with cell lines for easier selection
def plot_grid(ax, title, robot_grid, robot_pos, robot_label, step_count):
    ax.clear()
    ax.imshow(robot_grid, cmap='viridis', interpolation='nearest')
    ax.set_title(f"{title}\nSteps: {step_count}")
    ax.text(0, -1, f"{robot_label} Robot Position: {robot_pos}", fontsize=10, color='white')
    # Add grid lines for clarity
    ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)

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
def place_obstacles(ax):
    num_obstacles = 20
    placed = 0
    while placed < num_obstacles:
        x, y = get_position_from_click(f"Click to place obstacle {placed + 1}")
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and grid[x, y] == 0:
            grid[x, y] = -1
            ax.imshow(grid, cmap='viridis', interpolation='nearest')
            ax.set_title("Placing Obstacles")
            ax.set_xticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
            ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
            plt.pause(0.1)
            placed += 1
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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Prompt for obstacle placement
    place_obstacles(ax1)

    # Get target position
    TARGET = tuple(get_position_from_click("Click to place the target"))
    grid[TARGET] = 2  # Place the target
    ax1.imshow(grid, cmap='viridis', interpolation='nearest')
    ax1.set_title("Target Placed")
    ax1.set_xticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
    ax1.set_yticks(np.arange(-0.5, GRID_SIZE, 1), minor=True)
    ax1.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
    plt.pause(0.1)

    # Get robot positions
    random_robot_pos = place_robot("random")
    target_robot_pos = place_robot("target-oriented")

    # Copy grid to use for separate displays
    grid_random_robot = grid.copy()
    grid_target_robot = grid.copy()
    grid_random_robot[random_robot_pos[0], random_robot_pos[1]] = 1
    grid_target_robot[target_robot_pos[0], target_robot_pos[1]] = 3

    # Visualization initialization for both grids
    plot_grid(ax1, "Random Robot Movement", grid_random_robot, random_robot_pos, "Random", 0)
    plot_grid(ax2, "Target-Oriented Robot Movement", grid_target_robot, target_robot_pos, "Target-Oriented", 0)

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
    steps_random = 0
    steps_target = 0
    start_time = time.time()

    while True:
        steps_random += 1
        steps_target += 1

        # Clear robot positions from grids
        grid_random_robot[random_robot_pos[0], random_robot_pos[1]] = 0
        grid_target_robot[target_robot_pos[0], target_robot_pos[1]] = 0

        # Move robots
        random_robot_pos = move_random(random_robot_pos)
        target_robot_pos = move_towards_target(target_robot_pos, TARGET)

        # Update grids with new positions
        grid_random_robot[random_robot_pos[0], random_robot_pos[1]] = 1  # Random robot
        grid_target_robot[target_robot_pos[0], target_robot_pos[1]] = 3  # Target-oriented robot
        grid_random_robot[TARGET] = 2  # Target
        grid_target_robot[TARGET] = 2  # Target

        # Update visualizations
        plot_grid(ax1, "Random Robot Movement", grid_random_robot, random_robot_pos, "Random", steps_random)
        plot_grid(ax2, "Target-Oriented Robot Movement", grid_target_robot, target_robot_pos, "Target-Oriented", steps_target)
        plt.pause(0.5)

        # Check if robots found the target
        if tuple(random_robot_pos) == TARGET:
            total_time = time.time() - start_time
            print(f"Random robot found the target in {steps_random} steps! Time taken: {total_time:.2f} seconds")
            break
        if tuple(target_robot_pos) == TARGET:
            total_time = time.time() - start_time
            print(f"Target-oriented robot found the target in {steps_target} steps! Time taken: {total_time:.2f} seconds")
            break

    plt.show()

main()
