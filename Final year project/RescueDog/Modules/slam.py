# modules/slam.py

GRID_SIZE = 41
GRID_CENTER = GRID_SIZE // 2
grid_map = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
robot_pos = [GRID_CENTER, GRID_CENTER]

def update_obstacle(angle_deg, distance_cm):
    import math
    angle_rad = math.radians(angle_deg)
    distance_m = distance_cm / 100.0
    x_offset = distance_m * math.cos(angle_rad)
    y_offset = -distance_m * math.sin(angle_rad)

    gx = int(robot_pos[0] + x_offset * 5)
    gy = int(robot_pos[1] + y_offset * 5)

    if 0 <= gx < GRID_SIZE and 0 <= gy < GRID_SIZE:
        grid_map[gy][gx] = '#'

def get_latest_map():
    return {
        "map": ["".join(row) for row in grid_map],
        "robot": tuple(robot_pos)
    }

# ✅ ADD THIS FUNCTION TO FIX THE ERROR
def print_map():
    print("\n".join("".join(row) for row in grid_map))
    print("\n" + "=" * GRID_SIZE)
