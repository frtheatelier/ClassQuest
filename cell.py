import pygame


class Cell:
    """Shows the functions of each cell in the puzzle grid."""
    def __init__(self, row, col, cell_size, cell_id):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.cell_id = cell_id
        self.width = self.cell_size[0]
        self.height = self.cell_size[1]
        self.left = row * self.width
        self.top = col * self.height
        self.rect = pygame.Rect(
            self.left,
            self.top,
            self.width,
            self.height
        )
        self.occupying_piece = None

    def draw(self, display):
        """Draws the cells onto the game screen."""
        pygame.draw.rect(display, (0, 0, 0), self.rect)
        if self.occupying_piece is not None and self.occupying_piece.piece_id != 1:
            centering_rect = self.occupying_piece.img.get_rect()
            centering_rect.center = self.rect.center
            display.blit(self.occupying_piece.img, centering_rect.topleft)

