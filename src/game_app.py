import pygame
import random
import sys
import logging

from game import Game
from player import Player
from card import cards

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GameApp:
    def __init__(self, start_resolution=(1600, 900)):
        pygame.init()
        self.resolutions = [
            (800, 600), (1024, 768), (1128, 634), (1280, 720), (1280, 1024),
            (1366, 768), (1600, 900), (1680, 1050), (1760, 990), (1920, 1080)
        ]
        self.current_resolution = start_resolution
        self.screen = pygame.display.set_mode(self.current_resolution)
        pygame.display.set_caption("Proyecto comunidad LinVT")

        # Colores
        self.WHITE = (255, 255, 255)
        self.AMBER = (255, 191, 0)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.clock = pygame.time.Clock()

        # Estado del juego
        self.game = Game()
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        # Cartas y mazos
        random.shuffle(cards)
        # repartir inicial
        self.player1.hand = cards[:4]
        self.player2.hand = cards[4:8]
        remaining = cards[8:]
        # separar el mazo restante entre ambos jugadores y una pila (stacked)
        half = len(remaining) // 2
        self.player1.deck = remaining[:half]
        self.player2.deck = remaining[half:]
        self.stacked_cards = list(remaining)  # copia para la pila

        # Variables visuales y posiciones calculadas por resolución
        self._compute_layout()

        # Cachear imágenes escaladas y fuentes
        self._cache_resources()

        # Dragging & UI state
        self.dragging = False
        self.dragged_card = None
        self.offset_x = 0
        self.offset_y = 0
        self.hovered_card = None

        # field state
        self.field_cards = {"player1": [None] * 7, "player2": [None] * 7}
        self.field_modes = {"player1": ["attack"] * 7, "player2": ["attack"] * 7}

        # graveyard
        self.graveyard = []
        self.graveyard_index = 0

        # life
        self.player1_life = 5000
        self.player2_life = 5000

        # inputs
        self.font = pygame.font.Font(None, 36)
        self.player1_name = ""
        self.player2_name = ""
        self.input_active = False
        self.active_player = None
        self.life_input_active = False
        self.active_life_player = None
        self.life_input = ""

        logger.info("GameApp inicializado con resolución %s", self.current_resolution)

    def _compute_layout(self):
        W, H = self.current_resolution
        self.W, self.H = W, H
        # card sizes proporcionales
        self.CARD_W = max(40, int(W * 100 / 1600))
        self.CARD_H = max(60, int(H * 150 / 900))

        # positions
        self.card_positions = {
            card: (50 + i * int(self.CARD_W * 1.5), 125) for i, card in enumerate(self.player1.hand)
        }
        self.card_positions.update({
            card: (50 + i * int(self.CARD_W * 1.5), H - 225) for i, card in enumerate(self.player2.hand)
        })

        self.stack_position = (W - 200, 30)
        self.graveyard_position = (W - 200, H - 200)

        self.field_positions = {
            "player1": [(50 + i * int(self.CARD_W * 1.5), 300) for i in range(7)],
            "player2": [(50 + i * int(self.CARD_W * 1.5), 500) for i in range(7)]
        }

        self.description_area = pygame.Rect(int(W * 0.44), int(H * 0.78), int(W * 0.2), int(H * 0.15))

    def _cache_resources(self):
        # cache fonts
        self.font_small = pygame.font.Font(None, 24)

        # cache scaled images for cards
        for card in cards:
            # ensure integer, positive sizes
            w = max(1, int(self.CARD_W))
            h = max(1, int(self.CARD_H))
            # small image
            try:
                small = pygame.transform.smoothscale(card.image, (w, h))
                try:
                    card.image_small = small.convert_alpha()
                except Exception:
                    card.image_small = small.convert()
            except Exception:
                s = pygame.Surface((w, h), pygame.SRCALPHA)
                s.fill((100, 100, 100))
                card.image_small = s

            # large image (cached) - avoid re-scaling every frame
            try:
                large_size = (max(1, int(w * 3)), max(1, int(h * 3)))
                large = pygame.transform.smoothscale(card.image, large_size)
                try:
                    card.image_large = large.convert_alpha()
                except Exception:
                    card.image_large = large.convert()
            except Exception:
                card.image_large = card.image_small

            # defense-oriented rotated image: derive from small to avoid double rescale
            try:
                card.image_def = pygame.transform.rotate(card.image_small, 90)
            except Exception:
                card.image_def = card.image_small

    def select_resolution(self):
        font = pygame.font.Font(None, 36)
        waiting = True
        while waiting:
            self.screen.fill(self.AMBER)
            for i, res in enumerate(self.resolutions):
                text = font.render(f"{res[0]}x{res[1]}", True, self.BLACK)
                self.screen.blit(text, (300, 100 + i * 40))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for i, res in enumerate(self.resolutions):
                        if 300 <= mx <= 500 and 100 + i * 40 <= my <= 140 + i * 40:
                            self.current_resolution = res
                            self.screen = pygame.display.set_mode(self.current_resolution)
                            self._compute_layout()
                            self._cache_resources()
                            waiting = False
                            break

    def draw_background(self):
        # simple animated stars
        if not hasattr(self, 'stars'):
            self.stars = [(random.randint(0, self.W), random.randint(0, self.H), random.choice([self.WHITE, self.BLACK])) for _ in range(50)]
        self.screen.fill(self.AMBER)
        for i, (x, y, color) in enumerate(self.stars):
            pygame.draw.circle(self.screen, color, (int(x), int(y)), 3)
            nx = x + 1
            if nx > self.W:
                nx = 0
                y = random.randint(0, self.H)
            self.stars[i] = (nx, y, color)

    def draw_description(self, card):
        if card:
            pygame.draw.rect(self.screen, self.BLACK, self.description_area)
            pygame.draw.rect(self.screen, self.WHITE, self.description_area, 2)
            lines = card.get_description().split("\n")
            for i, line in enumerate(lines):
                surf = self.font_small.render(line, True, self.WHITE)
                self.screen.blit(surf, (self.description_area.x + 8, self.description_area.y + 8 + i * 22))

    def draw(self):
        self.draw_background()

        # pila y cementerio
        pygame.draw.rect(self.screen, self.AMBER, (self.stack_position[0], self.stack_position[1], self.CARD_W, self.CARD_H), 2)
        pygame.draw.rect(self.screen, (135, 206, 235), (self.graveyard_position[0], self.graveyard_position[1], self.CARD_W, self.CARD_H), 2)

        if self.stacked_cards:
            # dibujar solo la cima (cached)
            top = self.stacked_cards[-1]
            self.screen.blit(top.image_small, self.stack_position)

        for card, pos in list(self.card_positions.items()):
            self.screen.blit(card.image_small, pos)

        # campo
        for player, positions in self.field_positions.items():
            for i, pos in enumerate(positions):
                pygame.draw.rect(self.screen, self.WHITE, (pos[0], pos[1], self.CARD_W, self.CARD_H), 2)
                card = self.field_cards[player][i]
                if card:
                    if self.field_modes[player][i] == 'attack':
                        self.screen.blit(card.image_small, pos)
                    else:
                        self.screen.blit(card.image_def, pos)
                    atk_text = self.font.render(f"ATK: {card.get_total_atk()}", True, self.RED)
                    def_text = self.font.render(f"DEF: {card.get_total_def()}", True, self.BLUE)
                    self.screen.blit(atk_text, (pos[0], pos[1] + self.CARD_H + 8))
                    self.screen.blit(def_text, (pos[0], pos[1] + self.CARD_H + 30))

        # graveyard
        if self.graveyard:
            self.screen.blit(self.graveyard[self.graveyard_index].image_small, self.graveyard_position)

        # hovered large (usar imagen cacheada)
        if self.hovered_card:
            large = getattr(self.hovered_card, 'image_large', None) or getattr(self.hovered_card, 'image_small', None)
            if large:
                self.screen.blit(large, (int(self.W * 0.78), int(self.H * 0.22)))

        # names and life
        p1_name = self.font.render(self.player1_name, True, self.WHITE)
        p2_name = self.font.render(self.player2_name, True, self.WHITE)
        self.screen.blit(p1_name, (50, 30))
        self.screen.blit(p2_name, (50, self.H - 75))

        p1_life = self.font.render(f": {self.player1_life}", True, self.WHITE)
        p2_life = self.font.render(f": {self.player2_life}", True, self.WHITE)
        self.screen.blit(p1_life, (250, 30))
        self.screen.blit(p2_life, (250, self.H - 75))

        pygame.display.flip()

    def handle_mouse_down(self, event):
        mx, my = event.pos
        self.hovered_card = None
        for card, pos in self.card_positions.items():
            rect = pygame.Rect(pos, (self.CARD_W, self.CARD_H))
            if rect.collidepoint(mx, my):
                self.hovered_card = card
                break

        if event.button == 1:
            for card, pos in list(self.card_positions.items()):
                rect = pygame.Rect(pos, (self.CARD_W, self.CARD_H))
                if rect.collidepoint(mx, my):
                    self.dragging = True
                    self.dragged_card = card
                    self.offset_x = pos[0] - mx
                    self.offset_y = pos[1] - my
                    return

            # click en pila
            if pygame.Rect(self.stack_position, (self.CARD_W, self.CARD_H)).collidepoint(mx, my) and self.stacked_cards:
                self.dragging = True
                self.dragged_card = self.stacked_cards.pop()
                self.card_positions[self.dragged_card] = self.stack_position
                self.offset_x = self.stack_position[0] - mx
                self.offset_y = self.stack_position[1] - my
                return

            # inputs de texto/vida
            if 250 <= mx <= 350 and 30 <= my <= 50:
                self.life_input_active = True
                self.active_life_player = 'player1'
                self.life_input = str(self.player1_life)
            elif 250 <= mx <= 350 and self.H - 75 <= my <= self.H - 35:
                self.life_input_active = True
                self.active_life_player = 'player2'
                self.life_input = str(self.player2_life)
            elif 50 <= mx <= 250 and 30 <= my <= 70:
                self.input_active = True
                self.active_player = 'player1'
            elif 50 <= mx <= 250 and self.H - 75 <= my <= self.H - 35:
                self.input_active = True
                self.active_player = 'player2'

        elif event.button == 3:
            # toggle attack/defense on field
            for player, positions in self.field_positions.items():
                for i, pos in enumerate(positions):
                    rect = pygame.Rect(pos, (self.CARD_W, self.CARD_H))
                    if rect.collidepoint(mx, my) and self.field_cards[player][i]:
                        self.field_modes[player][i] = 'defense' if self.field_modes[player][i] == 'attack' else 'attack'
                        return

    def handle_mouse_up(self, event):
        if not self.dragging:
            return
        mx, my = event.pos
        placed = False
        for player, positions in self.field_positions.items():
            for i, pos in enumerate(positions):
                rect = pygame.Rect(pos, (self.CARD_W, self.CARD_H))
                if rect.collidepoint(mx, my) and not self.field_cards[player][i]:
                    self.field_cards[player][i] = self.dragged_card
                    self.card_positions.pop(self.dragged_card, None)
                    placed = True
                    break
            if placed:
                break

        if not placed and pygame.Rect(self.graveyard_position, (self.CARD_W, self.CARD_H)).collidepoint(mx, my):
            self.graveyard.append(self.dragged_card)
            self.card_positions.pop(self.dragged_card, None)
            placed = True

        self.dragging = False
        self.dragged_card = None

    def handle_mouse_motion(self, event):
        mx, my = event.pos
        if self.dragging and self.dragged_card:
            self.card_positions[self.dragged_card] = (mx + self.offset_x, my + self.offset_y)
            return

        self.hovered_card = None
        for card, pos in self.card_positions.items():
            rect = pygame.Rect(pos, (self.CARD_W, self.CARD_H))
            if rect.collidepoint(mx, my):
                self.hovered_card = card
                return

        # check stack / grave
        if self.stacked_cards and pygame.Rect(self.stack_position, (self.CARD_W, self.CARD_H)).collidepoint(mx, my):
            self.hovered_card = self.stacked_cards[-1]
            return
        if self.graveyard and pygame.Rect(self.graveyard_position, (self.CARD_W, self.CARD_H)).collidepoint(mx, my):
            self.hovered_card = self.graveyard[self.graveyard_index]

    def handle_keydown(self, event):
        if event.key == pygame.K_SPACE and self.graveyard:
            self.graveyard_index = (self.graveyard_index + 1) % len(self.graveyard)
        elif event.key == pygame.K_RETURN:
            if self.input_active:
                self.input_active = False
                self.active_player = None
            elif self.life_input_active:
                try:
                    val = int(self.life_input)
                except ValueError:
                    val = None
                if val is not None:
                    if self.active_life_player == 'player1':
                        self.player1_life = val
                    else:
                        self.player2_life = val
                self.life_input = ""
                self.life_input_active = False
                self.active_life_player = None
        elif self.input_active:
            if event.key == pygame.K_BACKSPACE:
                if self.active_player == 'player1':
                    self.player1_name = self.player1_name[:-1]
                else:
                    self.player2_name = self.player2_name[:-1]
            else:
                if self.active_player == 'player1':
                    self.player1_name += event.unicode
                else:
                    self.player2_name += event.unicode
        elif self.life_input_active:
            if event.key == pygame.K_BACKSPACE:
                self.life_input = self.life_input[:-1]
            elif event.unicode.isdigit():
                self.life_input += event.unicode

    def run(self):
        # mostrar selector de resolución al inicio
        self.select_resolution()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_up(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            self.draw()
            self.clock.tick(30)

        pygame.quit()
        logger.info("Juego terminado.")


if __name__ == '__main__':
    GameApp().run()
