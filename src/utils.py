import pygame

def load_image(path, size=(100, 150)):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)