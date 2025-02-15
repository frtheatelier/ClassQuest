"""Contains entities for the game"""
import json

JSON_DICTIONARY = "words_dictionary.json"
JSON_COMMON = "common_words.json"


class Player:
    """Player class. can be either automated or user input
    type == 1: player
    type == 2: bot"""

    # type: int
    score: int

    def __init__(self):
        # self.type = p_type
        self.score = 0


class Bot:
    """Bot class"""

    expert: int
    word_bank: dict

    @staticmethod
    def _load_dictionary(filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)

        word_dictionary = {}
        for word in data:
            word_dictionary[word] = data[word]

        return word_dictionary

    def __init__(self, expert: int = 0):
        self.expert = expert
        if expert == 0:
            self.word_bank = self._load_dictionary(JSON_COMMON)
        else:
            self.word_bank = self._load_dictionary(JSON_DICTIONARY)


class WordChain:
    """Word chain manager class"""

    player1: Player
    player2: Player | Bot
    words_used: set[str]
    word_dictionary: dict[str, int]  # mapping of word to score

    @staticmethod
    def _load_dictionary(filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)

        word_dictionary = {}
        for word in data:
            word_dictionary[word] = data[word]

        return word_dictionary

    def __init__(self, p1: Player, p2: Player):
        self.player1 = p1
        self.player2 = p2
        self.words_used = set()
        self.word_dictionary = self._load_dictionary(JSON_DICTIONARY)
