import pygame
import os
import sys

def load_image(path):
    # Ajustar la ruta para PyInstaller
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, path)
    return pygame.image.load(path).convert_alpha()