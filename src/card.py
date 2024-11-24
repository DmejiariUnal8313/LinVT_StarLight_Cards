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
    ("ZeroV0lt", "assets/cards/Carta_16.jpg"),
    ("Compadrito", "assets/cards/Carta_17.jpg"),
    ("Migue", "assets/cards/Carta_18.jpg"),
    ("Natari", "assets/cards/Carta_19.jpg"),
    ("Kimura", "assets/cards/Carta_20.jpg"),
    ("Trester", "assets/cards/Carta_21.jpg"),
    ("Rakkun", "assets/cards/Carta_22.jpg"),
    ("Tomoe", "assets/cards/Carta_23.jpg"),
    ("Yumiko", "assets/cards/Carta_24.jpg"),
    ("Rekky", "assets/cards/Carta_25.jpg"),
    ("Niños", "assets/cards/Carta_26.jpg"),
    ("Espada", "assets/cards/Carta_27.jpg"),
    ("Puños", "assets/cards/Carta_28.jpg"),
    ("Mascara", "assets/cards/Carta_29.jpg"),
    ("Paz", "assets/cards/Carta_30.jpg"),
    ("Propuesta", "assets/cards/Carta_31.jpg"),
    ("Caos", "assets/cards/Carta_32.jpg"),
    ("Parry", "assets/cards/Carta_33.jpg"),
    ("Worthcat", "assets/cards/Carta_34.jpg"),
    ("Ataque Sorpresa", "assets/cards/Carta_35.jpg"),
    ("MalaMujer", "assets/cards/Carta_36.jpg"),
    ("Verdadera", "assets/cards/Carta_37.jpg"),
    ("BajoPerfil", "assets/cards/Carta_38.jpg"),
    ("DobleONada", "assets/cards/Carta_39.jpg"),
    ("Neru", "assets/cards/Carta_40.jpg"),
    ("Interesante", "assets/cards/Carta_41.jpg"),
    ("TwistedZid", "assets/cards/Carta_42.jpg"),
    ("Secreto", "assets/cards/Carta_43.jpg"),
    ("Comienzo", "assets/cards/Carta_44.jpg")
]

# Crear las cartas
cards = [Card(name, image_path, lambda target: None) for name, image_path in cards_info]

