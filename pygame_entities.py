"""pygame entities"""
import pygame

WIDTH = 1200
HEIGHT = 750
SCREEN_SIZE = (WIDTH, HEIGHT)

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


class Background(pygame.sprite.Sprite):
    """Background class"""
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


bg = Background('assets/background-no-text.jpeg', [0, 0])

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dummy window")
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill([255, 255, 255])
        screen.blit(bg.image, bg.rect)
        pygame.display.update()
