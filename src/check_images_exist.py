"""Comprueba que las rutas de imagen listadas en `cards_info` de `card.py` existan en disco.

No requiere pygame; analiza `card.py` para extraer `cards_info`.
"""
import ast
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_cards_info(card_py_path):
    with open(card_py_path, 'r', encoding='utf-8') as f:
        src = f.read()
    tree = ast.parse(src, filename=card_py_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'cards_info':
                    # safe literal_eval of the assigned value
                    return ast.literal_eval(node.value)
    raise RuntimeError('No se encontró cards_info en ' + card_py_path)


def main():
    repo_root = os.path.dirname(os.path.dirname(__file__))
    card_py = os.path.join(repo_root, 'src', 'card.py') if os.path.exists(os.path.join(repo_root, 'src', 'card.py')) else os.path.join(repo_root, 'card.py')
    # fallback: try workspace src/card.py
    if not os.path.exists(card_py):
        card_py = os.path.join(os.path.dirname(__file__), 'card.py')
    if not os.path.exists(card_py):
        logger.error('No se encontró file card.py en rutas conocidas.')
        sys.exit(1)

    cards_info = extract_cards_info(card_py)
    missing = []
    for entry in cards_info:
        # cada entry es (name, path, atk, def)
        if len(entry) < 2:
            continue
        path = entry[1]
        # Ruta relativa al repositorio
        candidate = os.path.join(repo_root, path)
        if not os.path.exists(candidate):
            missing.append((entry[0], path))

    if missing:
        logger.warning('Faltan %d archivos de imagen:', len(missing))
        for name, path in missing:
            logger.warning(' - %s -> %s', name, path)
        sys.exit(2)
    else:
        logger.info('Todas las rutas de imagen existen.')


if __name__ == '__main__':
    main()
