from utils import load_image

class Card:
    def __init__(self, name, image_path, atk, def_, effect):
        self.name = name
        self.image_path = image_path
        self.image = load_image(image_path)
        self.atk = atk
        self.def_ = def_
        self.effect = effect
    
    def use(self, target):
        self.effect(target)

# Definir las cartas con sus nombres y rutas de imagen
cards_info = [
    ("Yon", "assets/cards/Carta_1.jpg", 0, 0),
    ("Igna", "assets/cards/Carta_2.jpg", 500, 500),
    ("Ado", "assets/cards/Carta_3.jpg", 500, 500),
    ("Osado", "assets/cards/Carta_4.jpg", 1000, 0),
    ("Bortex", "assets/cards/Carta_5.jpg", 0, 0),
    ("Mizuki", "assets/cards/Carta_6.jpg", 0, 1000),
    ("Lin", "assets/cards/Carta_7.jpg", 250, 750),
    ("Flin", "assets/cards/Carta_8.jpg", 500, 500),
    ("Lia", "assets/cards/Carta_9.jpg", 1000, 0),
    ("Endy", "assets/cards/Carta_10.jpg",0, 0),
    ("Yukki Udagawa", "assets/cards/Carta_11.jpg",0,0),
    ("Cockito", "assets/cards/Carta_12.jpg",0,0),
    ("Holy Knight", "assets/cards/Carta_13.jpg",750,250),
    ("Primuss", "assets/cards/Carta_14.jpg",250,750),
    ("Foxy Sutaru", "assets/cards/Carta_15.jpg",550,450),
    ("ZeroV0lt", "assets/cards/Carta_16.jpg",0,0),
    ("Compadrito", "assets/cards/Carta_17.jpg",0,1000),
    ("Migue", "assets/cards/Carta_18.jpg",1000,0),
    ("Natari", "assets/cards/Carta_19.jpg",500,500),
    ("Kimura", "assets/cards/Carta_20.jpg",300,700),
    ("Trester", "assets/cards/Carta_21.jpg",100,600),
    ("Rakkun", "assets/cards/Carta_22.jpg",500,500),
    ("Tomoe", "assets/cards/Carta_23.jpg",500,500),
    ("Yumiko", "assets/cards/Carta_24.jpg",1000,0),
    ("Rekky", "assets/cards/Carta_25.jpg",600,400),
    ("Niños", "assets/cards/Carta_26.jpg",0,0),
    ("Espada", "assets/cards/Carta_27.jpg",0,0),
    ("Puños", "assets/cards/Carta_28.jpg",0,0),
    ("Mascara", "assets/cards/Carta_29.jpg",0,0),
    ("Paz", "assets/cards/Carta_30.jpg",0,0),
    ("Propuesta", "assets/cards/Carta_31.jpg",0,0),
    ("Caos", "assets/cards/Carta_32.jpg",0,0),
    ("Parry", "assets/cards/Carta_33.jpg",1000,0),
    ("Worthcat", "assets/cards/Carta_34.jpg",150,850),
    ("Ataque Sorpresa", "assets/cards/Carta_35.jpg",0,0),
    ("MalaMujer", "assets/cards/Carta_36.jpg",450,550),
    ("Verdadera", "assets/cards/Carta_37.jpg",300,300),
    ("BajoPerfil", "assets/cards/Carta_38.jpg",0,0),
    ("DobleONada", "assets/cards/Carta_39.jpg",0,0),
    ("Neru", "assets/cards/Carta_40.jpg",650,350),
    ("Interesante", "assets/cards/Carta_41.jpg",550,450),
    ("TwistedZid", "assets/cards/Carta_42.jpg",400,600),
    ("Secreto", "assets/cards/Carta_43.jpg",500,500),
    ("Comienzo", "assets/cards/Carta_44.jpg",500,500),
    ("Maxwell", "assets/cards/Carta_45.jpg",600,400),
    ("Alto Mando", "assets/cards/Carta_46.jpg",0,0),
    ("Lluvia de Ideas", "assets/cards/Carta_47.jpg",0,0),
    ("Día de Playa (Chicos)", "assets/cards/Carta_48.jpg",0,0),
    ("Día de Playa (Chicas)", "assets/cards/Carta_49.jpg",0,0),
    ("Y Eso Sería Todo por Hoy", "assets/cards/Carta_50.jpg",0,0)
]

# Crear las cartas
cards = [Card(name, image_path, atk, def_, lambda target: None) for name, image_path, atk, def_ in cards_info]

