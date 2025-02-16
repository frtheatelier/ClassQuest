import pygame


class Piece:
    """Shows the functionality of individual puzzle pieces, for this fruit's level."""
    def __init__(self, fruit_name, piece_size, piece_id):
        self.fruit_name = fruit_name
        self.piece_size = piece_size
        self.piece_id = piece_id
        if self.piece_id != 1:
            img_path = f'{self.fruit_name}_pieces/{self.fruit_name}_0{self.piece_id}.jpg'
            self.img = pygame.image.load(img_path)
            self.img = pygame.transform.scale(self.img, self.piece_size)
        else:
            self.img = None
