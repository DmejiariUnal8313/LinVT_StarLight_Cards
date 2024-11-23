from PIL import Image
import pytesseract
import os
import pygame
from utils import load_image

class Card:
    def __init__(self, name, image_path, effect):
        self.name = name
        self.image = load_image(image_path)
        self.effect = effect
    
    def use(self, target):
        self.effect(target)

def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def define_effect_from_text(text):
    if "reduce life points by 500" in text.lower():
        return lambda target: target.life_points
    return lambda target: None

def create_card_from_image(image_path):
    name = os.path.basename(image_path).split('.')[0]
    text = extract_text_from_image(image_path)
    effect = define_effect_from_text(text)
    return Card(name, image_path, effect)

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
cards = []
for name, image_path in cards_info:
    card = create_card_from_image(image_path)
    cards.append(card)

