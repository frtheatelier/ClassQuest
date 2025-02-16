import pygame
from settings import *


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 50)
        self.background_color = background_color
        self.message_color = message_color

    def clicked(self, click):
        """Returns whether the key clicked is valid."""
        if click.key == pygame.K_LEFT:
            return True
        elif click.key == pygame.K_RIGHT:
            return True
        elif click.key == pygame.K_UP:
            return True
        elif click.key == pygame.K_DOWN:
            return True
        else:
            return False

    def game_over(self, frame):
        """Updates and checks whether the game is over."""
        for row in frame.cells:
            for cell in row:
                if cell.occupying_piece is None or cell.occupying_piece.piece_id != cell.cell_id:
                    return False
        return True

    def message(self, screen, frame):
        """Prints a congratulatory message when the player completes the puzzle."""
        screen.fill(background_color)
        frame.draw(screen)
        instructions = self.font.render("You win!", True, self.message_color)
        screen.blit(instructions, (450, 450))
        pygame.display.update()
        pygame.time.delay(5000)
