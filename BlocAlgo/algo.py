from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QTimer
import sys

class HanoiAlgorithm:
    def __init__(self, n):
        self.n = n
        self.towers = {0: list(range(1, n + 1)), 1: [], 2: []}
        self.moves = []
        self.move_matrix = []
        self.generate_moves(n, 0, 1, 2)
    
    def generate_moves(self, n, source, auxiliary, destination):
        if n == 1:
            self.record_move(source, destination)
            return
        self.generate_moves(n - 1, source, destination, auxiliary)
        self.record_move(source, destination)
        self.generate_moves(n - 1, auxiliary, source, destination)
    
    def record_move(self, source, destination):
        nb_palets_origine = len(self.towers[source])
        nb_palets_destination = len(self.towers[destination])
        self.moves.append((source, destination))
        self.move_matrix.append((len(self.moves), source, destination, nb_palets_origine, nb_palets_destination))

class HanoiSimulation(QWidget):
    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.tower_positions = [100, 300, 500]
        self.disk_widths = [60, 50, 40, 30][:self.algorithm.n]
        self.towers = {0: list(range(1, self.algorithm.n + 1)), 1: [], 2: []}
        self.index = 0
        
        self.setWindowTitle("Tower of Hanoi - PyQt6")
        self.setGeometry(100, 100, 600, 400)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_move)
        self.timer.start(1000)
    
    def move_disk(self, source, destination):
        if self.towers[source]:
            disk = self.towers[source].pop()
            self.towers[destination].append(disk)
        else:
            print(f"Erreur: Pas de disque à déplacer depuis la tour {source}")
        
    def next_move(self):
        if self.index < len(self.algorithm.moves):
            source, destination = self.algorithm.moves[self.index]
            self.move_disk(source, destination)
            self.index += 1
            self.update()
        else:
            self.timer.stop()
            print("Matrice des mouvements:", self.algorithm.move_matrix)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        
        for x in self.tower_positions:
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawRect(x - 10, 100, 20, 200)
            painter.drawEllipse(x - 15, 80, 30, 30)
        
        for i, tower in self.towers.items():
            for j, disk in enumerate(tower):
                disk_index = disk - 1
                painter.setBrush(QBrush(QColor(0, 0, 255)))
                painter.drawRect(
                    self.tower_positions[i] - self.disk_widths[disk_index] // 2, 
                    280 - j * 20, 
                    self.disk_widths[disk_index], 20
                )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    algorithm = HanoiAlgorithm(4)
    window = HanoiSimulation(algorithm)
    window.show()
    sys.exit(app.exec())