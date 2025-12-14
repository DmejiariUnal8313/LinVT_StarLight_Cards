import ast
import os


def extract_cards_info(card_py_path):
    with open(card_py_path, 'r', encoding='utf-8') as f:
        src = f.read()
    tree = ast.parse(src, filename=card_py_path)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == 'cards_info':
                    return ast.literal_eval(node.value)
    raise RuntimeError('No se encontró cards_info en ' + card_py_path)


def test_card_images_exist():
    repo_root = os.path.dirname(os.path.dirname(__file__))
    card_py = os.path.join(repo_root, 'src', 'card.py')
    assert os.path.exists(card_py), f'No se encontró {card_py}'

    cards_info = extract_cards_info(card_py)
    missing = []
    for entry in cards_info:
        if len(entry) < 2:
            continue
        name, path = entry[0], entry[1]
        candidate = os.path.join(repo_root, path)
        if not os.path.exists(candidate):
            missing.append((name, path))

    assert not missing, f'Faltan imágenes: {missing}'
