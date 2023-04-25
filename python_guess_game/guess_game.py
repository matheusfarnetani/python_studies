from random import randint
import json

DIFFICULTY = None


def set_difficulty():
    """Set constant difficulty"""

    difficulty_data = {
        "easy": {"life": 6, "score": [0, 10, 20, 40, 60, 80, 100]},
        "medium": {"life": 4, "score": [0, 60, 80, 100, 120]},
        "hard": {"life": 2, "score": [0, 140, 160]},
    }

    while True:
        chosen_difficulty = str(input("Difficulty: 'easy', 'medium' or 'hard': ")).lower()
        try:
            life = difficulty_data[chosen_difficulty]["life"]
        except KeyError:
            print("You entered an invalid difficulty.")
        else:
            global DIFFICULTY
            DIFFICULTY = difficulty_data[chosen_difficulty]
            break
    return life


def new_player():
    """Set player name"""
    
    player_name = str(input("Player Name: ")).lower()
    return player_name


def player_life_message(player_life):
    if player_life > 1:
        print(f"You have: {player_life} lifes\n")
    else:
        print(f"You have: {player_life} life\n")


def scoreboard(player_life, player_name):
    """Calculate and save score"""

    score = DIFFICULTY["score"][player_life]
    print(score)

# Try: This block will test the excepted error to occur
# Except:  Here you can handle the error
# Else: If there is no exception then this block will be executed
# Finally: Finally block always gets executed either exception is generated or not

    try:
        with open("python_guess_game/data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("python_guess_game/data.json", mode="a") as data_file:
            new_data = {
                player_name:{
                    "score": score,
                    "plays": 1,
                }}
            json.dump(new_data, data_file, indent=4)
    else:
        if player_name in data:
            total_score = data[player_name]["score"]
            total_plays = data[player_name]["plays"]
            updated_total_score = total_score + score
            updated_total_plays = total_plays + 1

            updated_data = {
                player_name:{
                    "score": updated_total_score,
                    "plays": updated_total_plays,
                }}

            data.update(updated_data)
        else:
            data[player_name] = {
                    "score": score,
                    "plays": 1,
                }

        with open("python_guess_game/data.json", mode = "w") as file:
            json.dump(data, file, indent=4)

def guess_question():
    """Ask guess and check characters"""

    while True:
        guess = input("Guess a number between 0 and 10: ")
        try:
            guess = int(guess)
        except ValueError:
            print("You entered an invalid number.")
        else:
            return guess


def play():
    """Play the game"""

    player_name = new_player()
    player_life = set_difficulty()
    computer_number = randint(0, 10)

    while True:
        player_life_message(player_life)
        if player_life > 0:
            guess = guess_question()
            if guess == computer_number:
                print("Win!")
                scoreboard(player_life, player_name)
                return
            else:
                print("Wrong! You lost a life.\n")
                player_life -= 1
        else:
            print("You lost.")
            return

# START
while True:
    play()

    play_again = input("Do you wan't to play again? ").lower()
    if play_again.lower() == "yes" or play_again.lower() == "y":
        pass
    else:
        break
