from robot_controller import RobotController
from scene_detector import get_scene

robot = RobotController()


# =====================================
# Scene
# =====================================

def show_scene():

    return get_scene()

# =====================================
# Status
# =====================================    

def show_status():

    return robot.get_status()


# =====================================
# Basic Robot Commands
# =====================================

def pick_cube(slot):

    status = robot.get_status()

    if status["holding_cube"]:

        print(
            "Robot is already holding a cube"
        )

        return False

    scene = get_scene()

    if scene["slots"][slot] is None:

        print(
            f"No cube found in slot {slot}"
        )

        return False

    return robot.pick_cube(slot)


def drop_cube(side):

    status = robot.get_status()

    if not status["holding_cube"]:

        print(
            "Robot is not holding a cube"
        )

        return False

    return robot.drop_cube(side)


def move_cube(slot, side):

    scene = get_scene()

    if scene["slots"][slot] is None:

        print(
            f"No cube found in slot {slot}"
        )

        return False

    return robot.move_cube(
        slot,
        side
    )


def go_home():

    robot.go_home()


# =====================================
# Auto Sorting
# =====================================

def sort_red_cubes():

    scene = get_scene()

    bins = scene["bins"]

    red_bin_side = None

    if bins["LEFT"] == "red_bin":

        red_bin_side = "LEFT"

    elif bins["RIGHT"] == "red_bin":

        red_bin_side = "RIGHT"

    if not red_bin_side:

        print("Red bin not found")

        return

    found = False

    for slot, obj in scene["slots"].items():

        if obj == "cube_red":

            found = True

            print(
                f"Moving {slot} -> {red_bin_side}"
            )

            robot.move_cube(
                slot,
                red_bin_side
            )

    if not found:

        print("No red cubes found")
        
        return False
        
    return True    


def sort_green_cubes():

    scene = get_scene()

    bins = scene["bins"]

    green_bin_side = None

    if bins["LEFT"] == "green_bin":

        green_bin_side = "LEFT"

    elif bins["RIGHT"] == "green_bin":

        green_bin_side = "RIGHT"

    if not green_bin_side:

        print("Green bin not found")

        return

    found = False

    for slot, obj in scene["slots"].items():

        if obj == "cube_green":

            found = True

            print(
                f"Moving {slot} -> {green_bin_side}"
            )

            robot.move_cube(
                slot,
                green_bin_side
            )

    if not found:

        print("No green cubes found")
        
        return False
        
    return True    
