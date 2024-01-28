from settings import SCREEN_HEIGHT, SCREEN_WIDTH, CELLS, NUM_OF_APPLES
from pytimedinput import timedInput
import os
import random


from colorama import init, Fore, Back, Style

# Initialize colorama
init()


def print_filed():
    print("\033[H", end="")
    for cell in CELLS:
        if cell == snake_body[0]:
            if direction == DIRECTIONS["up"]:
                print(Fore.GREEN + "▲", end="")
            elif direction == DIRECTIONS["down"]:
                print(Fore.GREEN + "▼", end="")
            elif direction == DIRECTIONS["left"]:
                print(Fore.GREEN + "◀", end="")
            elif direction == DIRECTIONS["right"]:
                print(Fore.GREEN + "▶", end="")
        elif cell in snake_body:
            print(Fore.YELLOW + "■", end="")
        elif cell[0] == 0 and cell[1] == 0:
            print(Fore.CYAN + "┌", end="")
        elif cell[0] == SCREEN_WIDTH - 1 and cell[1] == 0:
            print(Fore.CYAN + "┐", end="")
        elif cell[0] == 0 and cell[1] == SCREEN_HEIGHT - 1:
            print(Fore.CYAN + "└", end="")
        elif cell[0] == SCREEN_WIDTH - 1 and cell[1] == SCREEN_HEIGHT - 1:
            print(Fore.CYAN + "┘", end="")
        elif cell[0] in (0, SCREEN_WIDTH - 1):
            print(Fore.CYAN + "│", end="")
        elif cell[1] in (0, SCREEN_HEIGHT - 1):
            print(Fore.CYAN + "─", end="")
        elif cell in apples_poses:
            print(Fore.RED + "●", end="")
        else:
            print(" ", end="")

        if cell[0] == SCREEN_WIDTH - 1:
            print("")


def update_snake_body():
    new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
    snake_body.insert(0, new_head)
    global eat
    if not eat:
        snake_body.pop()
    else:
        eat = False


def apple_place():
    col = random.randint(1, SCREEN_WIDTH - 2)
    row = random.randint(1, SCREEN_HEIGHT - 2)
    while (col, row) in snake_body or (
        col,
        row,
    ) in apples_poses:  # Check if the new apple is on top of another apple
        col = random.randint(1, SCREEN_WIDTH - 2)
        row = random.randint(1, SCREEN_HEIGHT - 2)
    return (col, row)


def apple_collision():
    global apples_poses, eat
    for apple_pose in apples_poses:  # Check for collisions with all apples
        if snake_body[0] == apple_pose:
            apples_poses.remove(apple_pose)  # Remove the eaten apple
            apples_poses.append(apple_place())  # Add a new apple
            eat = True


def print_start_menu():
    print(Fore.CYAN + "Welcome to the Snake Game!")
    print(Fore.CYAN + "Use the following keys to control the snake:")
    print(Fore.CYAN + "'w' - Move Up")
    print(Fore.CYAN + "'a' - Move Left")
    print(Fore.CYAN + "'s' - Move Down")
    print(Fore.CYAN + "'d' - Move Right")
    print(Fore.CYAN + "'q' - Quit Game")
    print(Fore.CYAN + "Press any key to start the game...")
    input()
    os.system("cls")


def print_end_menu():
    print(Fore.RED + "You died")
    print(Fore.MAGENTA + f"Final Score: {len(snake_body) - 3}")
    print(Fore.CYAN + "Press 'r' to retry or any other key to quit...")


def reset_game():
    global snake_body, direction, eat, apple_pose
    snake_body = [
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        (SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2),
        (SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2),
    ]
    direction = DIRECTIONS["up"]
    eat = False
    apple_pose = apple_place()


# snake_body
snake_body = [
    (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH // 2 + 1, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH // 2 + 2, SCREEN_HEIGHT // 2),
]
DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
direction = DIRECTIONS["up"]
eat = False

apples_poses = [
    (random.randint(1, SCREEN_WIDTH - 1), random.randint(1, SCREEN_HEIGHT - 1))
    for _ in range(NUM_OF_APPLES)
]


def main():
    print_start_menu()
    global direction
    while True:
        # os.system("cls")
        update_snake_body()

        apple_collision()

        # Get input
        key, _ = timedInput(timeout=0.2)  # type: ignore
        match key and key[0].lower():
            case "w":
                direction = DIRECTIONS["up"]
            case "a":
                direction = DIRECTIONS["left"]
            case "s":
                direction = DIRECTIONS["down"]
            case "d":
                direction = DIRECTIONS["right"]
            case "q":
                os.system("cls")
                print_end_menu()
                break
            case _:
                ...

        print_filed()
        print(Fore.MAGENTA + f"Score: {len(snake_body) - 3}")

        # Check if snake is dead
        if snake_body[0][0] in (0, SCREEN_WIDTH - 1) or snake_body[0][1] in (
            0,
            SCREEN_HEIGHT - 1,
        ):
            os.system("cls")
            print_end_menu()
            retry_key = input().lower()
            if retry_key == "r":
                reset_game()
                continue
            break


if __name__ == "__main__":
    main()
