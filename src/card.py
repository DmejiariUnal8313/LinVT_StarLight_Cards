from utils import load_image

class Card:
    def __init__(self, name, image_path, effect):
        self.name = name
        self.image_path = image_path
        self.image = load_image(image_path)
        self.effect = effect
    
    def use(self, target):
        self.effect(target)

# Definir las cartas con sus nombres y rutas de imagen
cards_info = [
    ("Yon", "assets/cards/Carta_1.jpg"),
    ("Igna", "assets/cards/Carta_2.jpg"),
    ("Ado", "assets/cards/Carta_3.jpg"),
    ("Osado", "assets/cards/Carta_4.jpg"),
    ("Bortex", "assets/cards/Carta_5.jpg"),
    ("Mizuki", "assets/cards/Carta_6.jpg"),
    ("Lin", "assets/cards/Carta_7.jpg"),
    ("Flin", "assets/cards/Carta_8.jpg"),
    ("Lia", "assets/cards/Carta_9.jpg"),
    ("Endy", "assets/cards/Carta_10.jpg"),
    ("Yukki Udagawa", "assets/cards/Carta_11.jpg"),
    ("Cockito", "assets/cards/Carta_12.jpg"),
    ("Holy Knight", "assets/cards/Carta_13.jpg"),
    ("Primuss", "assets/cards/Carta_14.jpg"),
    ("Foxy Sutaru", "assets/cards/Carta_15.jpg"),
    ("ZeroV0lt", "assets/cards/Carta_16.jpg")
    
]

# Crear las cartas
cards = [Card(name, image_path, lambda target: None) for name, image_path in cards_info]

