import pygame
import time

class Algorithm:
    def __init__(self, n):
        pygame.init()
        self.n = n
        self.screen = pygame.display.set_mode((600, 400))
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        
        self.tower_positions = [(100, 300), (300, 300), (500, 300)]
        self.palet_widths = [60, 50, 40, 30]
        
        self.towers = {0: list(range(1, n + 1)), 1: [], 2: []}
        self.moves = []
        
        self.hanoi(n, 0, 1, 2)
        
    def draw_towers(self):
        for i, pos in enumerate(self.tower_positions):
            pygame.draw.rect(self.screen, self.BLACK, (pos[0] - 10, 100, 20, 200))
            pygame.draw.circle(self.screen, self.BLACK, pos, 15)

    def draw_palets(self):
        for i, tower in self.towers.items():
            for j, palet in enumerate(tower):
                palet_index = palet - 1
                pygame.draw.rect(self.screen, self.BLUE, 
                                 (self.tower_positions[i][0] - self.palet_widths[palet_index] // 2, 
                                  280 - j * 20, self.palet_widths[palet_index], 20))
    
    def hanoi(self, n, source, auxiliary, destination):
        if n == 1:
            self.move_palet(source, destination)
            self.moves.append((source, destination))
            return
        self.hanoi(n - 1, source, destination, auxiliary)
        self.move_palet(source, destination)
        self.moves.append((source, destination))
        self.hanoi(n - 1, auxiliary, source, destination)
    
    def move_palet(self, source, destination):
        if self.towers[source]:
            palet = self.towers[source].pop()
            self.towers[destination].append(palet)
        else:
            print(f"Erreur: Pas de disque à déplacer depuis la tour {source}")
    
    def run(self):
        running = True
        index = 0
        while running:
            self.screen.fill(self.WHITE)
            self.draw_towers()
            self.draw_palets()
            
            if index < len(self.moves):
                source, destination = self.moves[index]
                self.move_palet(source, destination)
                index += 1
            
            pygame.display.flip()
            time.sleep(1)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        
        pygame.quit()

if __name__ == "__main__":
    game = Algorithm(4)
    game.run()
