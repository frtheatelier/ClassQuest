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


class Bot(Player):
    """Bot class"""

    # expert: int
    word_bank: dict
    # starter_words: dict

    @staticmethod
    def _load_dictionary(filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)

        word_dictionary = {}
        for word in data['commonWords']:
            word_dictionary[word.lower()] = 1

        return word_dictionary

    def __init__(self):
        super().__init__()
        self.word_bank = self._load_dictionary(JSON_COMMON)
        # self.starter_words = {w: self.word_bank[w] for w in self.word_bank if w[len(w) - 1] in 'EARIOT'}


class WordChain:
    """Word chain manager class"""

    player1: Player | Bot
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

    def __init__(self, p1: Player | Bot, p2: Player | Bot):
        self.player1 = p1
        self.player2 = p2
        self.words_used = set()
        self.word_dictionary = self._load_dictionary(JSON_DICTIONARY)
