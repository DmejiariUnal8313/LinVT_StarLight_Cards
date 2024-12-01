import pygame
import sys
import subprocess
import random

pygame.init()

# Ajustar la resolución de la ventana a 800x600 inicialmente
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Menú Principal")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
AMBER = (255, 191, 0)

# Fuentes
font = pygame.font.Font(None, 36)

# Botones
buttons = [
    {"text": "Iniciar Juego", "rect": pygame.Rect(300, 150, 200, 50), "action": "start_game"},
    {"text": "Ver Todas las Cartas", "rect": pygame.Rect(300, 250, 270, 50), "action": "view_cards"},
    {"text": "Modificar Resolución", "rect": pygame.Rect(300, 350, 270, 50), "action": "change_resolution"}
]

# Opciones de resolución
resolutions = [
    (800, 600), (1024, 768), (1128, 634), (1280, 720), (1280, 1024),
    (1366, 768), (1600, 900), (1680, 1050), (1760, 990), (1920, 1080)
]

# Generar posiciones de las estrellas una sola vez
stars = [(random.randint(0, 800), random.randint(0, 600)) for _ in range(50)]

def draw_background():
    screen.fill(AMBER)
    for x, y in stars:
        pygame.draw.circle(screen, WHITE, (x, y), 4)  # Estrellas más grandes

def draw_buttons():
    for button in buttons:
        pygame.draw.rect(screen, GRAY, button["rect"])
        text = font.render(button["text"], True, BLACK)
        screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

def start_game():
    subprocess.Popen([sys.executable, "D:\VSCode\LinVT_StarLight_Cards\src\main.py"])

def view_cards():
    # Aquí puedes agregar la lógica para ver todas las cartas
    print("Ver todas las cartas")

def change_resolution():
    global screen
    screen.fill(AMBER)
    for i, res in enumerate(resolutions):
        text = font.render(f"{res[0]}x{res[1]}", True, BLACK)
        screen.blit(text, (300, 100 + i * 40))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, res in enumerate(resolutions):
                    if 300 <= mouse_x <= 500 and 100 + i * 40 <= mouse_y <= 140 + i * 40:
                        screen = pygame.display.set_mode(res)
                        waiting = False
                        break

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for button in buttons:
                if button["rect"].collidepoint(mouse_x, mouse_y):
                    if button["action"] == "start_game":
                        start_game()
                    elif button["action"] == "view_cards":
                        view_cards()
                    elif button["action"] == "change_resolution":
                        change_resolution()

    draw_background()
    draw_buttons()
    pygame.display.flip()

pygame.quit()
sys.exit()