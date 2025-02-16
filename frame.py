import random
from settings import *

from cell import Cell
from piece import Piece


class Frame:
    """Manages the sliding fruit puzzle's frame."""

    def __init__(self, frame_size, level):
        self.tile_size = tile_size
        self.level = level
        self.fruit_name = FRUIT_NAMES.get(level)
        self.cell_width = frame_size // self.tile_size
        self.cell_height = frame_size // self.tile_size
        self.cell_size = (self.cell_width, self.cell_height)
        self.cells = self._generate_cell()
        self.pieces = self._generate_piece()
        self.setup()
        self.randomize()

    def _generate_cell(self):
        cells = []
        cell_id = 1
        for col in range(self.tile_size):
            new_row = []
            for row in range(self.tile_size):
                new_row.append(Cell(row, col, self.cell_size, cell_id))
                cell_id += 1
            cells.append(new_row)
        return cells

    def _generate_piece(self):
        pieces = []
        piece_id = 1
        for col in range(self.tile_size):
            for row in range(self.tile_size):
                level = self.level
                fruit_name = FRUIT_NAMES[level]
                pieces.append(Piece(fruit_name, self.cell_size, piece_id))
                piece_id += 1
        return pieces

    def setup(self):
        """Sets up the game."""
        for row in self.cells:
            for cell in row:
                tile_piece = self.pieces[-1]
                cell.occupying_piece = tile_piece
                self.pieces.remove(tile_piece)

    def randomize(self):
        """Randomizes the original position of the cells when the game starts."""
        moves = [(0, 1),  # move right
                 (0, -1),  # move left
                 (1, 0),  # move down
                 (-1, 0)]  # move up
        shuffle = random.choice(moves)
        for row in self.cells:
            for cell in row:
                tile_x = self.cells.index(row) + shuffle[0]
                tile_y = row.index(cell) + shuffle[1]
                if tile_x >= 0 and tile_x <= 2 and tile_y >= 0 and tile_y <= 2:
                    new_cell = self.cells[tile_x][tile_y]
                    if new_cell.occupying_piece.img is None:
                        c = (cell, new_cell)
                        try:
                            c[0].occupying_piece, c[1].occupying_piece = c[1].occupying_piece, c[0].occupying_piece
                        except:
                            return False
                else:
                    continue

    def draw(self, display):
        """Draws the cells created by generate cells on the screen."""
        for row in self.cells:
            for cell in row:
                cell.draw(display)

    def handle_click(self, click):
        """Handle arrow key clicks"""
        check_validity = self.validity(click)
        try:
            check_validity[0].occupying_piece, check_validity[1].occupying_piece = (
                check_validity[1].occupying_piece, check_validity[0].occupying_piece)
        except:
            return False

    def validity(self, click):
        """Determines whether the move made is valid."""
        moves = {
            79: (0, 1),
            80: (0, -1),
            81: (1, 0),
            82: (-1, 0)
        }
        for row in self.cells:
            for cell in row:
                move = moves[click.scancode]
                tile_x = self.cells.index(row) + move[0]
                tile_y = row.index(cell) + move[1]
                if tile_x >= 0 and tile_x <= 2 and tile_y >= 0 and tile_y <= 2:
                    new_cell = self.cells[tile_x][tile_y]
                    if new_cell.occupying_piece.img is None:
                        return [cell, new_cell]
                else:
                    continue

