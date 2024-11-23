import pygame
import random

pygame.init()

# Ajustar la resolución de la ventana a 1280x720
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Proyecto comunidad LinVT")

from game import Game
from player import Player
from card import cards  # Importar las cartas después de inicializar pygame

game = Game()
player1 = Player("Player 1")
player2 = Player("Player 2")

# Barajar las cartas
random.shuffle(cards)

# Inicializar los mazos de los jugadores
player1.deck = cards[8:]  # Asignar las cartas restantes a player1
player2.deck = cards[8:]  # Asignar las cartas restantes a player2

# Distribuir cartas iniciales a los jugadores
player1.hand = cards[:4]  # Asignar las primeras 4 cartas a player1
player2.hand = cards[4:8]  # Asignar las siguientes 4 cartas a player2
stacked_cards = cards[8:]  # Las 25 cartas restantes

print("Iniciando el bucle del juego...")

# Variables para arrastrar y soltar
dragging = False
dragged_card = None
offset_x = 0
offset_y = 0
hovered_card = None

# Posiciones iniciales de las cartas
card_positions = {
    card: (50 + i * 150, 50) for i, card in enumerate(player1.hand)
}
card_positions.update({
    card: (50 + i * 150, 600) for i, card in enumerate(player2.hand)
})
stack_position = (600, 300)  # Posición fija para las cartas apiladas
graveyard_position = (600, 500)  # Posición fija para el cementerio

# Espacios en el campo para las cartas
field_positions = {
    "player1": [(50 + i * 150, 200) for i in range(4)],
    "player2": [(50 + i * 150, 400) for i in range(4)]
}

# Estado de las cartas en el campo (ataque o defensa)
field_cards = {
    "player1": [None] * 4,
    "player2": [None] * 4
}
field_modes = {
    "player1": ["attack"] * 4,
    "player2": ["attack"] * 4
}

# Cementerio
graveyard = []
graveyard_index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if event.button == 1:  # Botón izquierdo del mouse
                for card, pos in card_positions.items():
                    card_rect = pygame.Rect(pos, (100, 150))
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        dragging = True
                        dragged_card = card
                        offset_x = pos[0] - mouse_x
                        offset_y = pos[1] - mouse_y
                        break
                if not dragging:
                    card_rect = pygame.Rect(stack_position, (100, 150))
                    if card_rect.collidepoint(mouse_x, mouse_y) and stacked_cards:
                        dragging = True
                        dragged_card = stacked_cards.pop()
                        offset_x = stack_position[0] - mouse_x
                        offset_y = stack_position[1] - mouse_y
                        card_positions[dragged_card] = stack_position
                    elif pygame.Rect(graveyard_position, (100, 150)).collidepoint(mouse_x, mouse_y) and graveyard:
                        dragging = True
                        dragged_card = graveyard.pop(graveyard_index)
                        offset_x = graveyard_position[0] - mouse_x
                        offset_y = graveyard_position[1] - mouse_y
                        card_positions[dragged_card] = graveyard_position
                    else:
                        for player, positions in field_positions.items():
                            for i, pos in enumerate(positions):
                                card_rect = pygame.Rect(pos, (100, 150))
                                if card_rect.collidepoint(mouse_x, mouse_y) and field_cards[player][i]:
                                    dragging = True
                                    dragged_card = field_cards[player][i]
                                    offset_x = pos[0] - mouse_x
                                    offset_y = pos[1] - mouse_y
                                    field_cards[player][i] = None
                                    card_positions[dragged_card] = pos
                                    break
                            if dragging:
                                break
            elif event.button == 3:  # Botón derecho del mouse
                mouse_x, mouse_y = event.pos
                for player, positions in field_positions.items():
                    for i, pos in enumerate(positions):
                        card_rect = pygame.Rect(pos, (100, 150))
                        if card_rect.collidepoint(mouse_x, mouse_y) and field_cards[player][i]:
                            if field_modes[player][i] == "attack":
                                field_modes[player][i] = "defense"
                            else:
                                field_modes[player][i] = "attack"
                            break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                # Colocar la carta en el campo si está en la posición correcta
                mouse_x, mouse_y = event.pos
                placed = False
                for player, positions in field_positions.items():
                    for i, pos in enumerate(positions):
                        card_rect = pygame.Rect(pos, (100, 150))
                        if card_rect.collidepoint(mouse_x, mouse_y) and not field_cards[player][i]:
                            field_cards[player][i] = dragged_card
                            card_positions.pop(dragged_card)
                            placed = True
                            break
                if not placed and pygame.Rect(graveyard_position, (100, 150)).collidepoint(mouse_x, mouse_y):
                    graveyard.append(dragged_card)
                    card_positions.pop(dragged_card)
                    placed = True
                dragging = False
                dragged_card = None
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            hovered_card = None
            if dragging:
                card_positions[dragged_card] = (mouse_x + offset_x, mouse_y + offset_y)
            else:
                for card, pos in card_positions.items():
                    card_rect = pygame.Rect(pos, (100, 150))
                    if card_rect.collidepoint(mouse_x, mouse_y):
                        hovered_card = card
                        break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and graveyard:
                graveyard_index = (graveyard_index + 1) % len(graveyard)

    screen.fill((0, 0, 0))

    # Dibujar el fondo ámbar para el stack
    pygame.draw.rect(screen, (255, 191, 0), (stack_position[0], stack_position[1], 100, 150), 2)

    # Dibujar el fondo celeste para el cementerio
    pygame.draw.rect(screen, (135, 206, 235), (graveyard_position[0], graveyard_position[1], 100, 150), 2)

    # Dibujar las cartas apiladas
    if stacked_cards:
        for card in stacked_cards:
            small_image = pygame.transform.smoothscale(card.image, (100, 150))
            screen.blit(small_image, stack_position)

    # Dibujar las cartas en sus posiciones actuales
    for card, pos in card_positions.items():
        small_image = pygame.transform.smoothscale(card.image, (100, 150))
        screen.blit(small_image, pos)

    # Dibujar las cartas en el campo
    for player, positions in field_positions.items():
        for i, pos in enumerate(positions):
            card = field_cards[player][i]
            if card:
                if field_modes[player][i] == "attack":
                    small_image = pygame.transform.smoothscale(card.image, (100, 150))
                else:
                    small_image = pygame.transform.smoothscale(card.image, (150, 100))
                    small_image = pygame.transform.rotate(small_image, 90)
                screen.blit(small_image, pos)

    # Dibujar las cartas en el cementerio
    if graveyard:
        small_image = pygame.transform.smoothscale(graveyard[graveyard_index].image, (100, 150))
        screen.blit(small_image, graveyard_position)

    # Dibujar la carta arrastrada en grande en la esquina superior derecha
    if hovered_card:
        large_image = pygame.transform.smoothscale(hovered_card.image, (300, 450))
        screen.blit(large_image, (980, 20))  # Posicionar la carta grande en la esquina superior derecha

    pygame.display.flip()

pygame.quit()
print("Juego terminado.")