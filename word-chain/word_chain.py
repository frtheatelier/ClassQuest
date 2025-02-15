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

    inp = input("Enter a word starting with k: ").lower().strip()
    while inp not in game.word_dictionary or inp in game.words_used or inp[0] != 'k':
        inp = input("That's not a word that starts with k! Try again: ")

    _ = input("And that's how it works! Note that no duplicate words are allowed. Press anything to quit")

    return True


def setup():
    """
    Setup game on console
    :return:
    """
    game_setup = {"players": 0, "bot_first": 0}
    inp = input("How many players are playing? [1 or 2]  ")
    while inp not in ['1', '2']:
        inp = input("Sorry, that's not a valid number. ")

    game_setup["players"] = int(inp)

    if int(inp) == 1:
        print("Alright! We'll set up a bot as your opponent.")
        inp = input("Do you want the bot to play first or second? [1 or 2] ")
        while inp not in ['1', '2']:
            inp = input("Enter 1 for bot to play first, 2 if you want to play first: ")

        game_setup["bot_first"] = int(inp)

    return game_setup


def get_user_input(last_letter: str, word_dictionary: dict, words_used: set) -> str | None:
    """

    :param last_letter:
    :param word_dictionary:
    :return:
    """
    att = 4
    word = ''
    while att > 0 and (word not in word_dictionary or word in words_used or word[0] != last_letter):
        if att == 4:
            word = input(f"Enter a word that starts with {last_letter} : ").lower().strip()
        else:
            word = input(f"You have {att} attempts left. Try again! ").lower().strip()

        att -= 1

    if word in word_dictionary and word not in words_used and word[0] == last_letter:
        return word
    else:
        return None


def get_bot_input(last_letter: str, word_dictionary: dict, words_used: set):
    """

    :param last_letter:
    :param word_dictionary:
    :return:
    """
    choices = [w for w in word_dictionary if w[0] == last_letter and w not in words_used]

    if len(choices) == 0:
        return None
    else:
        return random.choice(choices)


def get_word(curr_player: Bot | Player, last_letter: str, word_dictionary: dict, words_used: set):
    """

    :param curr_player:
    :param last_letter:
    :param word_dictionary:
    :param words_used:
    """
    if isinstance(curr_player, Bot):
        return get_bot_input(last_letter, curr_player.word_bank, words_used)
    else:
        return get_user_input(last_letter, word_dictionary, words_used)


def update_game_data(curr_player: Player | Bot, game: WordChain, word: str) -> None:
    """

    :param curr_player:
    :param game:
    :param word:
    """
    curr_player.score += 1
    game.words_used.add(word)


def game_play(game: WordChain):
    """

    :param game:
    :return:
    """
    curr_round = 1
    last_letter = random.choice('nesgjwdombiuhpycltarqkfv'.lower())
    while True:
        if curr_round % 2 != 0:
            curr_player = game.player1
        else:
            curr_player = game.player2

        word = get_word(curr_player, last_letter, game.word_dictionary, game.words_used)

        if word is None:
            return curr_round
        else:
            print(f"Player {curr_round % 2} chose the word '{word}'!")
            update_game_data(curr_player, game, word)
            last_letter = word[len(word) - 1]
            curr_round += 1


def setup_game(settings: dict):
    """

    :param settings:
    :return:
    """
    if settings["players"] == 2:
        game = WordChain(Player(), Player())
    elif settings["bot_first"] == 1:
        game = WordChain(Bot(), Player())
        # TODO erase print statements
        # print({w[0] for w in game.player1.word_bank})
    else:
        game = WordChain(Player(), Bot())
        # TODO erase print statements
        # print({w[0] for w in game.player1.word_bank})

    return game


def run_game():
    """Running main game in console"""

    print("Welcome to Word Chain")
    print("First, let's set up the game")
    game_setup = setup()
    game = setup_game(game_setup)

    inp = input("Have you played the game before? [Enter Yes/No]  ")

    if inp.upper().strip() in ['N', 'NO']:
        tutorial(game)

    print("Let's get started!")

    print("--------------------------------------------------------")

    if game_play(game) % 2 != 0:
        print(f"Player 2 won with {game.player2.score} points!")
        print(f"Player 1 lost with {game.player1.score} points!")
    else:
        print(f"Player 1 won with {game.player1.score} points!")
        print(f"Player 2 lost with {game.player2.score} points!")


if __name__ == "__main__":
    run_game()
