from pidog import Pidog

# Initialize Pidog once
dog = Pidog()

def do_function(action):
    """Maps action names from frontend to PiDog commands."""
    if action == "forward":
        dog.do_action("forward", step_count=1, speed=85)
    elif action == "backward":
        dog.do_action("backward", step_count=1, speed=85)
    elif action == "left":
        dog.do_action("turn_left", step_count=1, speed=85)
    elif action == "right":
        dog.do_action("turn_right", step_count=1, speed=85)
    elif action == "sit":
        dog.do_action("sit")
    elif action == "stand":
        dog.do_action("stand")
    elif action == "shake_head":
        dog.do_action("shake_head", step_count=1, speed=80)
    else:
        return {"status": "error", "message": f"Unknown action: {action}"}

    return {"status": "ok", "action": action}
