from task_executor import *

print()
print("AI Robotic Arm")
print("----------------")
print("Commands:")
print("scene")
print("status")
print("sort_red")
print("sort_green")
print("pick A")
print("drop LEFT")
print("move B RIGHT")
print("home")
print()

while True:

    cmd = input("> ").strip()

    # ------------------------------

    if cmd == "scene":

        show_scene()
        
    # ------------------------------
    
    elif cmd == "status":

        show_status()    

    # ------------------------------

    elif cmd == "sort_red":

        sort_red_cubes()

    # ------------------------------

    elif cmd == "sort_green":

        sort_green_cubes()

    # ------------------------------

    elif cmd == "home":

        go_home()

    # ------------------------------

    elif cmd.startswith("pick "):

        slot = cmd.split()[1].upper()

        pick_cube(slot)

    # ------------------------------

    elif cmd.startswith("drop "):

        side = cmd.split()[1].upper()

        drop_cube(side)

    # ------------------------------

    elif cmd.startswith("move "):

        parts = cmd.split()

        if len(parts) != 3:

            print(
                "Usage: move A LEFT"
            )

            continue

        slot = parts[1].upper()

        side = parts[2].upper()

        move_cube(
            slot,
            side
        )

    # ------------------------------

    else:

        print("Unknown command")
