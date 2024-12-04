import pygame
from pygame.locals import *
import sys
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

# Dimensiones de la ventana del juego
WIDTH = 800
HEIGHT = 600

# Colores
GRAY = (200, 200, 200)
JUGAR = (150, 255, 50)
INSTRUCCIONES = (255, 255, 0)
SALIR = (255, 50, 50)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
FONDO = (25, 25, 25)

# Clase para representar los discos
class Disk:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

# Clase para representar las torres
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.disks = []

    def add_disk(self, disk):
        if len(self.disks) == 0 or disk.width < self.disks[-1].width:
            self.disks.append(disk)
        else:
            messagebox.showerror("Movimiento inválido", "No puedes colocar un disco mayor sobre uno menor")

    def remove_disk(self):
        if self.disks:
            return self.disks.pop()

    def check_valid_move(self, disk):
        if not self.disks or disk.width < self.disks[-1].width:
            return True
        return False

# Función para dibujar el juego
def draw_game(window, towers, moves, min_moves, time_elapsed, show_button=True):
    window.fill(FONDO)

    for tower in towers:
        pygame.draw.rect(window, DARK_GRAY, (tower.x - 5, tower.y, 10, HEIGHT - tower.y))

        disk_y = HEIGHT - 20
        for disk in tower.disks:
            disk_x = tower.x - disk.width // 2
            pygame.draw.rect(window, disk.color, (disk_x, disk_y, disk.width, 20))
            disk_y -= 20

    # Dibujar contador de movimientos
    font = pygame.font.Font(None, 24)
    text = font.render("MOVIMIENTOS: {}".format(moves), True, (255, 150, 50))
    window.blit(text, (605, 15))

    # Dibujar mínimo de movimientos
    min_moves_text = font.render("MÍN. MOVIMIENTOS: {}".format(min_moves), True, (50, 150, 255))
    window.blit(min_moves_text, (605, 45))

    # Dibujar contador de tiempo
    time_text = font.render("TIEMPO: {}".format(format_time(time_elapsed)), True, "white")
    window.blit(time_text, (350, 25))

    if show_button:
        pygame.draw.rect(window, GRAY, (10, 10, 80, 50))
        button_text = font.render("VOLVER", True, FONDO)
        text_rect = button_text.get_rect(center=(10 + 80 // 2, 10 + 50 // 2))
        window.blit(button_text, text_rect)

    pygame.display.update()

# Función para dibujar el mensaje de victoria
def draw_game_won_message(window, moves, min_moves, time_elapsed, player_name):
    window.fill(FONDO)

    #pygame.draw.rect(window, GRAY, (135, 250, 545, 100))
    font = pygame.font.Font(None, 26)
    text = font.render("¡Felicidades, {}! Has completado el juego en {} movimientos.".format(player_name, moves), True, "white")
    text_rect = text.get_rect(center=(WIDTH // 2, 280))
    window.blit(text, text_rect)

    min_moves_text = font.render("El mínimo de movimientos para resolverlo es de {}.".format(min_moves), True, "white")
    min_moves_rect = min_moves_text.get_rect(center=(WIDTH // 2, 300))
    window.blit(min_moves_text, min_moves_rect)

    time_text = font.render("Además, tardaste un total de {}".format(format_time(time_elapsed)), True, "white")
    time_rect = time_text.get_rect(center=(WIDTH // 2, 320))
    window.blit(time_text, time_rect)

    pygame.draw.rect(window, JUGAR, (300, 400, 200, 50))
    text = font.render("VOLVER AL MENÚ", True, FONDO)
    text_rect = text.get_rect(center=(WIDTH // 2, 425))
    window.blit(text, text_rect)

    pygame.draw.rect(window, SALIR, (300, 480, 200, 50))
    text = font.render("SALIR", True, FONDO)
    text_rect = text.get_rect(center=(WIDTH // 2, 505))
    window.blit(text, text_rect)

    pygame.display.update()

# Función principal del juego
def play_game(window, num_disks, player_name):
    towers = [
        Tower(WIDTH // 4, 100),
        Tower(WIDTH // 2, 100),
        Tower(WIDTH - WIDTH // 4, 100)
    ]

    disk_widths = range(20, 240, 30)
    disk_colors = [(255, 50, 50), (255, 150, 50), (255, 255, 0), (150, 255, 50), (50, 150, 255), (50, 50, 255), (255, 50, 255)]

    for i in range(num_disks - 1, -1, -1):
        disk = Disk(disk_widths[i], 20, disk_colors[i])
        towers[0].add_disk(disk)

    selected_tower = None
    moves = 0
    start_time = time.time()

    while True:
        time_elapsed = int(time.time() - start_time)
        draw_game(window, towers, moves, get_min_moves(num_disks) if moves > 0 else "-", time_elapsed)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Verificar si se hizo clic en la torre de origen o destino
                for tower in towers:
                    if tower.x - 50 <= mouse_x <= tower.x + 50 and tower.y <= mouse_y <= HEIGHT:
                        if not selected_tower:
                            selected_tower = tower
                        else:
                            if tower != selected_tower:
                                disk = selected_tower.remove_disk()
                                if disk and tower.check_valid_move(disk):
                                    tower.add_disk(disk)
                                    moves += 1
                                else:
                                    selected_tower.add_disk(disk)
                            selected_tower = None

                # Verificar si se hizo clic en el botón de volver
                if 10 <= mouse_x <= 90 and 10 <= mouse_y <= 60:
                    return

        # Verificar si el juego ha sido completado
        if len(towers[0].disks) == 0 and len(towers[1].disks) == 0:
            draw_game_won_message(window, moves, get_min_moves(num_disks), time_elapsed, player_name)

            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()

                        # Verificar si se hizo clic en el botón de volver a jugar
                        if 300 <= mouse_x <= 500 and 400 <= mouse_y <= 450:
                            return True

                        # Verificar si se hizo clic en el botón de salir
                        if 300 <= mouse_x <= 500 and 480 <= mouse_y <= 530:
                            pygame.quit()
                            sys.exit()

        pygame.display.update()

# Función para obtener el mínimo de movimientos requeridos
def get_min_moves(num_disks):
    return 2 ** num_disks - 1

# Función para mostrar las instrucciones del juego
def show_instructions():
    messagebox.showinfo("INSTRUCCIONES", "El objetivo del juego es mover todos los discos de la torre de origen (izquierda) "
                                          "a la torre de destino (derecha), siguiendo las siguientes reglas:\n\n"
                                          "1. Solo puedes mover un disco a la vez.\n"
                                          "2. Un disco más grande no puede ser colocado sobre uno más pequeño.\n\n"
                                          "Haz clic en un disco para seleccionarlo, luego clic en otra torre para "
                                          "moverlo. ¡Buena suerte!")

# Función para dar formato al tiempo transcurrido
def format_time(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "{:02d}:{:02d}".format(minutes, seconds)

# Función principal del programa
def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Torres de Hanoi")

    while True:
        window.fill(FONDO)

        pygame.draw.rect(window, JUGAR, (150, 150, 500, 100))
        pygame.draw.rect(window, INSTRUCCIONES, (150, 300, 500, 100))
        pygame.draw.rect(window, SALIR, (150, 450, 500, 100))

        font = pygame.font.Font(None, 36)
        text = font.render("JUGAR", True, FONDO)
        text_rect = text.get_rect(center=(WIDTH // 2, 200))
        window.blit(text, text_rect)

        text = font.render("INSTRUCCIONES", True, FONDO)
        text_rect = text.get_rect(center=(WIDTH // 2, 350))
        window.blit(text, text_rect)

        text = font.render("SALIR", True, FONDO)
        text_rect = text.get_rect(center=(WIDTH // 2, 500))
        window.blit(text, text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Verificar si se hizo clic en el botón de jugar
                if 150 <= mouse_x <= 650 and 150 <= mouse_y <= 250:
                    player_name = simpledialog.askstring("Nombre del jugador", "Ingresa tu nombre:")
                    if player_name:
                        num_disks = simpledialog.askinteger("Número de discos",
                                                            "Ingresa el número de discos (entre 1 y 7):",
                                                            minvalue=1, maxvalue=7)
                        if num_disks:
                            play_game(window, num_disks, player_name)

                # Verificar si se hizo clic en el botón de instrucciones
                if 150 <= mouse_x <= 650 and 300 <= mouse_y <= 400:
                    show_instructions()

                # Verificar si se hizo clic en el botón de salir
                if 150 <= mouse_x <= 650 and 450 <= mouse_y <= 550:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
