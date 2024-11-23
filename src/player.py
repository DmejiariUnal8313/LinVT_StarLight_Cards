class Player:
    def __init__(self, name):
        self.name = name
        self.life_points = 8000
        self.hand = []
        self.deck = []
        self.graveyard = []
        self.field = []
    
    def draw_card(self):
        if self.deck:
            self.hand.append(self.deck.pop())