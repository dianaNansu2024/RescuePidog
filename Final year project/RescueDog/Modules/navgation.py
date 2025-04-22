import time
import math
from queue import PriorityQueue
from pidog import Pidog
from modules.pidog_control import do_function

# SLAM and Grid Setup
GRID_SIZE = 41
GRID_CENTER = GRID_SIZE // 2
grid_map = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
robot_pos = [GRID_CENTER, GRID_CENTER]
robot_facing = 0  # Degrees, 0 = facing forward (Y−)

# Obstacle Mapping
def update_obstacle(angle_deg, distance_cm):
    angle_rad = math.radians(angle_deg + robot_facing)
    distance_m = distance_cm / 100.0
    x_offset = distance_m * math.cos(angle_rad)
    y_offset = -distance_m * math.sin(angle_rad)

    gx = int(robot_pos[0] + x_offset * 5)
    gy = int(robot_pos[1] + y_offset * 5)

    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        grid_map[gy][gx] = '#'

# A* Pathfinding
def neighbors(pos):
    x, y = pos
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    result = []
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid_map[ny][nx] != '#':
            result.append((nx, ny))
    return result

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star(start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        _, current = frontier.get()
        if current == goal:
            break
        for next in neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put((priority, next))
                came_from[next] = current

    path = []
    node = goal
    while node and node in came_from:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path

# Movement + SLAM scan
def scan_with_ultrasonic(dog):
    for angle in range(-90, 91, 15):
        dog.head_move([[angle, 0, 0]], immediately=True, speed=50)
        time.sleep(0.2)
        dist = round(dog.ultrasonic.read_distance(), 2)
        if 3 < dist < 250:
            update_obstacle(angle, dist)
    dog.head_move([[0, 0, 0]], immediately=True)

def move_to(target):
    global robot_pos
    dx = target[0] - robot_pos[0]
    dy = target[1] - robot_pos[1]
    if dx == 1:
        do_function("right")
    elif dx == -1:
        do_function("left")
    elif dy == 1:
        do_function("backward")
    elif dy == -1:
        do_function("forward")
    robot_pos = list(target)

# Autonomous Logic
latest_path = []
def start_autonomous_mode():
    global latest_path
    dog = Pidog()
    scan_with_ultrasonic(dog)

    goal = [robot_pos[0] + 5, robot_pos[1]]  # Move 5 cells forward
    path = a_star(tuple(robot_pos), tuple(goal))

    if not path:
        return {"status": "error", "message": "Path not found"}

    latest_path = path
    for step in path[1:]:
        move_to(step)
        scan_with_ultrasonic(dog)
        time.sleep(0.5)

    return {"status": "success", "message": "Autonomous path complete"}

def latest_path_data():
    return {
        "path": latest_path,
        "robot": tuple(robot_pos),
        "map": ["".join(row) for row in grid_map]
    }
