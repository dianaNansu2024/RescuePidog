#!/usr/bin/env python3
import time
from pidog import Pidog
from modules.slam import update_obstacle, print_map

dog = Pidog()
dog.do_action('stand', speed=80)
dog.wait_all_done()
time.sleep(0.5)

DANGER_DISTANCE = 15

stand = dog.legs_angle_calculation([[0, 80], [0, 80], [30, 75], [30, 75]])

def scan_with_ultrasonic():
    """Performs a head sweep and updates the SLAM map."""
    for angle in range(-90, 91, 15):
        dog.head_move([[angle, 0, 0]], immediately=True, speed=50)
        time.sleep(0.2)
        distance = round(dog.ultrasonic_read_distance(), 2)
        if 5 < distance < 300:
            update_obstacle(angle, distance)
    dog.head_move([[0, 0, 0]], immediately=True)

def patrol():
    distance = round(dog.ultrasonic_read_distance(), 2)
    print(f"distance: {distance} cm", end="", flush=True)

    if distance < DANGER_DISTANCE:
        print("\033[0;31m DANGER !\033[m")
        dog.body_stop()
        dog.rgb_strip.set_mode('bark', 'red', bps=2)
        dog.tail_move([[0]], speed=80)
        dog.legs_move([stand], speed=70)
        dog.wait_all_done()
        time.sleep(0.5)

        scan_with_ultrasonic()
        print_map()

        while distance < DANGER_DISTANCE:
            distance = round(dog.ultrasonic_read_distance(), 2)
            print(f"distance: {distance} cm \033[0;31m DANGER !\033[m" if distance < DANGER_DISTANCE else f"distance: {distance} cm", end="", flush=True)
            time.sleep(0.01)

    else:
        print("")
        dog.rgb_strip.set_mode('breath', 'white', bps=0.5)
        dog.do_action('forward', step_count=2, speed=95)
        dog.do_action('shake_head', step_count=1, speed=80)

def start_autonomous_mode():
    try:
        for _ in range(100):  # Run limited patrol steps
            patrol()
            time.sleep(0.05)
        return {"status": "success", "message": "Autonomous patrol complete"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
