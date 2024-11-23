class Game:
    def __init__(self):
        self.phase = "draw_phase"
    
    def next_phase(self):
        phases = ["draw_phase", "main_phase", "battle_phase", "end_phase"]
        current_index = phases.index(self.phase)
        self.phase = phases[(current_index + 1) % len(phases)]