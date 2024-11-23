import pygame
from game import Game
from player import Player
from card import cards

pygame.init()

# Ajustar la resolución de la ventana a 1920x1080
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Proyecto comunidad LinVT")

game = Game()
player1 = Player("Player 1")
player2 = Player("Player 2")

# Inicializar los mazos de los jugadores
player1.deck = cards[:8]  # Asignar las primeras 8 cartas a player1
player2.deck = cards[8:]  # Asignar las siguientes 8 cartas a player2

# Distribuir cartas iniciales a los jugadores
for _ in range(5):
    player1.draw_card()
    player2.draw_card()

print("Iniciando el bucle del juego...")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    # Dibujar las cartas en la mano de player1
    for i, card in enumerate(player1.hand):
        screen.blit(card.image, (50 + i * 150, 900))  # Posicionar las cartas en la parte inferior de la pantalla
    
    # Dibujar las cartas en la mano de player2
    for i, card in enumerate(player2.hand):
        screen.blit(card.image, (50 + i * 150, 50))  # Posicionar las cartas en la parte superior de la pantalla
    
    pygame.display.flip()

pygame.quit()
print("Juego terminado.")