import pygame
import time

# Initialize Pygame
pygame.init()

# Set up screen and colors
screen = pygame.display.set_mode((600, 400))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Tower positions and heights
tower_positions = [(100, 300), (300, 300), (500, 300)]
disk_widths = [60, 50, 40, 30]

def draw_towers():
    for i, pos in enumerate(tower_positions):
        pygame.draw.rect(screen, BLACK, (tower_positions[i][0] - 10, 100, 20, 200))  # Tower base
        pygame.draw.circle(screen, BLACK, tower_positions[i], 15)  # Tower top

def draw_disks(towers):
    for i, tower in enumerate(towers.values()):  # Corrected this line to access the lists of disks
        for j, disk in enumerate(tower):
            pygame.draw.rect(screen, BLUE, (tower_positions[i][0] - disk_widths[disk - 1] // 2, 280 - j * 20,
                                            disk_widths[disk - 1], 20))

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
    # Ensure that we pop a disk only if there is one available on the source tower
    if towers[source]:  # Check if the source tower has disks
        disk = towers[source].pop()
        towers[destination].append(disk)
    else:
        print(f"Error: No disk to move from tower {source}")

# Number of disks
n = 4
towers = {0: list(range(n, 0, -1)), 1: [], 2: []}  # Ensure towers are initialized with lists of disks
moves = []

# Generate moves using the Tower of Hanoi algorithm
hanoi(n, 0, 1, 2, towers, moves)

# Main loop
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
    time.sleep(1)  # Wait for 1 second between moves
    
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
