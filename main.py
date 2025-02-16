import pygame
from settings import *
from frame import Frame
from game import Game


class Puzzle:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((menu_width, menu_height))
        pygame.display.set_caption(title)
        self.running = True
        self.is_arranged = False
        self.font = pygame.font.SysFont("Times New Roman", 40)
        self.message_color = message_color

    def draw(self, frame):
        """Draws the screen and any updates."""
        bg = pygame.image.load("background.jpeg")
        self.screen.blit(bg, (0, 0))
        frame.draw(self.screen)
        self.instruction()
        pygame.display.update()

    def instruction(self):
        """Gives instructions on how to play the game to users."""
        instructions = self.font.render("Use Arrow Keys to Move", True, message_color)
        self.screen.blit(instructions, (50, 700))

    def main(self, frame_size):
        """Runs the main game loop and events in the game."""
        while True:
            pygame.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((menu_width, menu_height))
            pygame.display.set_caption(title)
            self.running = True
            self.is_arranged = False
            self.font = pygame.font.SysFont("Times New Roman", 40)
            self.background_color = background_color
            self.message_color = message_color
            self.menu()
            level = self.level_selection()
            self.screen.fill(background_color)
            frame = Frame(frame_size, level)
            self.screen = pygame.display.set_mode((width, height))
            game = Game()
            self.running = True
            pygame.display.update()

            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if not self.is_arranged:
                            if game.clicked(event):
                                frame.handle_click(event)

                    if game.game_over(frame):
                        self.is_arranged = True
                        game.message(self.screen, frame)
                        self.screen = pygame.display.set_mode((menu_width, menu_height))
                        self.main(frame_size)

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit(0)

                self.draw(frame)
                self.instruction()
                pygame.display.update()

    def menu(self):
        """Displays the main menu where players can start or quit the game."""
        while True:
            bg = pygame.image.load("background.jpeg")
            self.screen.blit(bg, (0, 0))
            # title = self.font.render("Sliding Fruits Puzzle!", True, self.message_color)
            play_option = self.font.render("1. Play", True, self.message_color)
            quit_option = self.font.render("2. Quit", True, self.message_color)

            # self.screen.blit(title, (100, 500))
            self.screen.blit(play_option, (100, 550))
            self.screen.blit(quit_option, (100, 600))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return self.level_selection()
                    elif event.key == pygame.K_2:
                        pygame.quit()
                        quit()

    def level_selection(self):
        """Displays the level selection screen and returns the chosen level."""
        while True:
            bg = pygame.image.load("background-no-text.jpeg")
            self.screen.blit(bg, (0, 0))

            title = self.font.render("Choose a Level", True, self.message_color)
            levels = [self.font.render(f"{i}. Level {i}", True, self.message_color) for i in range(1, 6)]

            self.screen.blit(title, (500, 200))
            for i, level_text in enumerate(levels):
                self.screen.blit(level_text, (500, 300 + i * 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 4
                    elif event.key == pygame.K_5:
                        return 5


if __name__ == "__main__":
    pygame.display.set_caption("Class Quest")
    puzzle = Puzzle()
    puzzle.main(width)

