import pygame
import random
from game import Game
from player import Player
from card import cards

pygame.init()

# Ajustar la resolución de la ventana a 1280x720
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Proyecto comunidad LinVT")

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

print("Iniciando el bucle del juego...")

# Variables para arrastrar y soltar
dragging = False
dragged_card = None
offset_x = 0
offset_y = 0

# Posiciones iniciales de las cartas
card_positions = {
    card: (50 + i * 150, 50) for i, card in enumerate(player1.hand)
}
card_positions.update({
    card: (50 + i * 150, 900) for i, card in enumerate(player2.hand)
})

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for card, pos in card_positions.items():
                card_rect = pygame.Rect(pos, (100, 150))
                if card_rect.collidepoint(mouse_x, mouse_y):
                    dragging = True
                    dragged_card = card
                    offset_x = pos[0] - mouse_x
                    offset_y = pos[1] - mouse_y
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                dragged_card = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                card_positions[dragged_card] = (mouse_x + offset_x, mouse_y + offset_y)

    screen.fill((0, 0, 0))

    # Dibujar las cartas en sus posiciones actuales
    for card, pos in card_positions.items():
        small_image = pygame.transform.smoothscale(card.image, (100, 150))
        screen.blit(small_image, pos)

    # Dibujar la carta arrastrada en grande
    if dragging and dragged_card:
        large_image = pygame.transform.smoothscale(dragged_card.image, (400, 600))
        screen.blit(large_image, (440, 60))  # Posicionar la carta grande en el centro de la pantalla

    pygame.display.flip()

pygame.quit()
print("Juego terminado.")