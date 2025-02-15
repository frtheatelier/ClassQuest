"""pygame entities"""
import pygame

WIDTH = 1200
HEIGHT = 750
SCREEN_SIZE = (WIDTH, HEIGHT)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


# VERIFICATION
def verify_word(word: str, last_letter: str, word_dictionary: dict, words_used: set) -> None | str:
    """
    Verifies
    :param word:
    :param word_dictionary:
    :param words_used:
    """
    if word not in word_dictionary or word in words_used or word[0] != last_letter:
        return None
    else:
        return word


class Word:
    """Words that are shown in the display"""
    def __init__(self, text, bg_position):
        self.bg_color = None
        self.text_color = "black"
        self.bg_x = bg_position[0]
        self.bg_y = bg_position[1]
        self.bg_rect = (self.bg_x, self.bg_y, len(text)*15, 15)
        self.text = text
        self.text_position = (self.bg_x + 36, self.bg_y + 34)  # might change based on outcome
        self.text_surf = pygame.font.Font("...", 25).render(self.text, True, self.text_color)
        self.text_rec = self.text_surf.get_rect(center=self.text_position)

    def draw(self):
        """Displays the word on Pygame display at desired position"""
        pygame.draw.rect(WINDOW, self.bg_color, self.bg_rect)
        WINDOW.blit(self.text_surf, self.text_rec)
        pygame.display.update()
