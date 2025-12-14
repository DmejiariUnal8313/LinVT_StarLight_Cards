"""Script de comprobación de recursos que no abre ventana.

Ejecuta una comprobación rápida de todas las imágenes de cartas usando el driver
SDL_VIDEODRIVER=dummy para evitar mostrar una ventana.
"""
import os
import logging

# Forzar driver dummy antes de importar pygame para que no abra una ventana
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

import pygame
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_cards(cards_module):
    pygame.init()
    try:
        # Intenta inicializar un display oculto si es posible
        try:
            pygame.display.init()
            pygame.display.set_mode((1, 1))
        except Exception:
            # si falla, seguimos; muchas operaciones de imagen funcionan sin display
            pass

        bad = []
        for c in cards_module.cards:
            name = getattr(c, 'name', '<unknown>')
            img = getattr(c, 'image', None)
            if img is None:
                logger.error('Carta %s no tiene atributo image', name)
                bad.append(name)
                continue
            try:
                # intentar escalar para comprobar la Surface
                pygame.transform.smoothscale(img, (64, 96))
            except Exception as e:
                logger.exception('Fallo escalando imagen de %s: %s', name, e)
                bad.append(name)

        if bad:
            logger.warning('Recursos problemáticos: %s', bad)
        else:
            logger.info('Todas las imágenes de cartas comprobadas correctamente.')

    finally:
        pygame.quit()


if __name__ == '__main__':
    # Importar el módulo de cartas
    try:
        import card as cards_module
    except Exception as e:
        logger.exception('No se pudo importar módulo card: %s', e)
        sys.exit(1)
    check_cards(cards_module)
