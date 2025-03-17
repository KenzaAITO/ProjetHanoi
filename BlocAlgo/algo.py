import pygame
import time

# Initialiser Pygame
pygame.init()

# Définir l'écran et les couleurs
screen = pygame.display.set_mode((600, 400))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Positions des tours et dimensions des disques
tower_positions = [(100, 300), (300, 300), (500, 300)]
disk_widths = [60, 50, 40, 30]  # Largeur des disques

def draw_towers():
    for i, pos in enumerate(tower_positions):
        pygame.draw.rect(screen, BLACK, (tower_positions[i][0] - 10, 100, 20, 200))  # Base des tours
        pygame.draw.circle(screen, BLACK, tower_positions[i], 15)  # Sommet des tours

def draw_disks(towers):
    for i, tower in enumerate(towers.values()):  # Accéder correctement aux tours
        for j, disk in enumerate(tower):  # Afficher les disques dans l'ordre classique (le plus grand en bas)
            disk_index = disk - 1  # Convertir le disque en index
            # Dessiner le disque à la bonne position
            pygame.draw.rect(screen, BLUE, 
                             (tower_positions[i][0] - disk_widths[disk_index] // 2, 
                              280 - j * 20,  # Position verticale des disques
                              disk_widths[disk_index], 20))  # Largeur et hauteur du disque

def hanoi(n, source, auxiliary, destination, towers, moves):
    if n == 1:
        move_disk(source, destination, towers)
        moves.append((source, destination))
        return
    hanoi(n - 1, source, destination, auxiliary, towers, moves)
    move_disk(source, destination, towers)
    moves.append((source, destination))
    hanoi(n - 1, auxiliary, source, destination, towers, moves)

def move_disk(source, destination, towers):
    # Vérifier qu'il y a un disque à déplacer
    if towers[source]:  # Vérifier si la tour source a des disques
        disk = towers[source].pop()
        towers[destination].append(disk)
    else:
        print(f"Erreur: Pas de disque à déplacer depuis la tour {source}")

# Nombre de disques
n = 4
# Initialisation des tours avec les disques dans l'ordre classique (le plus grand en bas et le plus petit en haut)
towers = {0: list(range(1, n + 1)), 1: [], 2: []}  # Disques dans l'ordre croissant (le plus petit en haut)
moves = []

# Générer les mouvements avec l'algorithme de Tower of Hanoi
hanoi(n, 0, 1, 2, towers, moves)

# Boucle principale
running = True
index = 0
while running:
    screen.fill(WHITE)
    draw_towers()
    draw_disks(towers)
    
    if index < len(moves):
        source, destination = moves[index]
        move_disk(source, destination, towers)
        index += 1
    
    pygame.display.flip()
    time.sleep(1)  # Attendre 1 seconde entre les déplacements
    
    # Vérifier si l'utilisateur ferme la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()