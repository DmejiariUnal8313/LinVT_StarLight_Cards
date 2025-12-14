import pygame
import os
import sys
import logging

logger = logging.getLogger(__name__)


def load_image(path):
    """Carga una imagen con manejo de errores y compatibilidad PyInstaller.

    Devuelve una Surface válida incluso si la carga falla (placeholder).
    """
    # Ajustar la ruta para PyInstaller
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, path)
    try:
        img = pygame.image.load(path)
        try:
            return img.convert_alpha()
        except Exception:
            return img.convert()
    except Exception as e:
        logger.exception("Fallo cargando imagen %s: %s", path, e)
        # devolver placeholder gris
        w, h = 100, 150
        surf = pygame.Surface((w, h))
        surf.fill((100, 100, 100))
        return surf