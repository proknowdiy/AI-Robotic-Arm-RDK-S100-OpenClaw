import sys


from task_executor import *



def execute(command, *args):


    if command == "scene":

        return show_scene()


    elif command == "status":

        return show_status()


    elif command == "sort_red":

        return sort_red_cubes()


    elif command == "sort_green":

        return sort_green_cubes()


    elif command == "pick":

        return pick_cube(args[0])


    elif command == "drop":

        return drop_cube(args[0])


    elif command == "move":

        return move_cube(args[0], args[1])


    elif command == "home":

        return go_home()


    else:

        return "Unknown command"



# =====================================

# Command Line Entry Point

# =====================================


if __name__ == "__main__":


    if len(sys.argv) < 2:


        print(

            "Usage:\n"

            "python3 arm_api.py scene\n"

            "python3 arm_api.py status\n"

            "python3 arm_api.py pick A\n"

            "python3 arm_api.py drop LEFT\n"

            "python3 arm_api.py move B RIGHT\n"

            "python3 arm_api.py sort_red\n"

            "python3 arm_api.py sort_green\n"

            "python3 arm_api.py home"

        )


        sys.exit(1)


    command = sys.argv[1]


    result = execute(

        command,

        *sys.argv[2:]

    )


    if result is not None:

        print(result)
