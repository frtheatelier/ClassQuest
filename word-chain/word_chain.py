"""main game functions"""
import random
import time

from game_entities import Player, WordChain, Bot


def print_delay(text: str, after_pause=0.0) -> None:
    """Prints text a letter at a time after a brief pause"""
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.005)

    time.sleep(after_pause)


def tutorial(game: WordChain) -> bool:
    """
    Tutorial scene
    :param game: the game manager class to access word bank
    :return:
    """
    print("Your task is to type a word starting with the last letter of the previous word")
    print("Like this: ")

    print("My first word is 'Stack'")

    inp = input("Enter a word starting with k: ")
    while inp not in game.word_dictionary and inp in game.words_used and inp[0] != 'k':
        inp = input("That's not a word that starts with k! Try again: ")

    _ = input("And that's how it works! press anything to quit")

    return True


def setup():
    """
    Setup games
    :return:
    """
    game_setup = {"players": 0, "bot_first": 0}
    inp = input("How many players are playing? [1 or 2]  ")
    while inp not in ['1', '2']:
        inp = input("Sorry, that's not a valid number. ")

    game_setup["players"] = inp

    if inp == 1:
        print("Alright! We'll set up a bot as your opponent.")
        inp = input("Do you want the bot to play first or second? [1 or 2]")
        while inp not in ['1', '2']:
            inp = input("Enter 1 for bot to play first, 2 if you want to play first: ")

        game_setup["bot_first"] = inp

    return game_setup


def get_user_input(last_letter: str, word_dictionary: dict) -> str | None:
    """

    :param last_letter:
    :param word_dictionary:
    :return:
    """
    att = 4
    while att > 0:
        if att == 4:
            word = input(f"Enter a word that starts with {last_letter} : ")
        else:
            word = input(f"You have {att} attempts left. Try again! ")

        if word in word_dictionary and word[0] == last_letter:
            return word
        else:
            return None


def get_bot_input(last_letter: str, word_dictionary: dict):
    choices = [w for w in word_dictionary if w[0] == last_letter]

    if len(choices) == 0:
        return None
    else:
        return random.choice(choices)


def game_play(game: WordChain):
    round = 1
    last_letter = random.choice('ABCDEFGHIJKLMNOPPQRZTUVWXYZ')
    while True:
        if round % 2 != 0:
            curr_player = game.player1
        else:
            curr_player = game.player2

        if isinstance(curr_player, Bot):
            if round < 20:
                word = get_bot_input(last_letter, curr_player.starter_words)
            else:
                word = get_bot_input(last_letter, curr_player.word_bank)
        else:
            word = get_user_input(last_letter, game.word_dictionary)

        if word is None:
            return round
        else:
            curr_player.score += 1


def run_game():
    """Running main game"""

    print("Welcome to Word Chain")
    print("First, let's set up the game")
    game_setup = setup()

    if game_setup["players"] == 2:
        game = WordChain(Player(), Player())
    elif game_setup["bot_first"] == 1:
        game = WordChain(Bot(), Player())
    else:
        game = WordChain(Player(), Bot())

    inp = input("Have you played the game before? [Enter Yes/No]")

    if inp.upper() in ['N', 'NO']:
        tutorial(game)

    print("Let's get started!")

    print("--------------------------------------------------------")

    if game_play(game) % 2 == 0:
        print(f"Player 2 won with {game.player2.score} points!")
        print(f"Player 1 lost with {game.player1.score} points!")
    else:
        print(f"Player 1 won with {game.player1.score} points!")
        print(f"Player 2 lost with {game.player2.score} points!")
