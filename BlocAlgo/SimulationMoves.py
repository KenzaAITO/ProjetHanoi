import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QTimer

#from BlocAlgo.HanoiAlgorithm import HanoiAlgorithm
from BlocAlgo.algooo import hanoi_iterative
from BlocAlgo.HanoiIterative import HanoiIterative

class SimulationMoves(QWidget):
    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.tower_positions = [100, 300, 500]
        self.palet_widths = [60, 50, 40, 30][:self.algorithm.n]
        self.towers = {0: list(range(1, self.algorithm.n + 1)), 1: [], 2: []}
        self.index = 0
        
        self.setWindowTitle("Tower of Hanoi - PyQt6")
        self.setGeometry(100, 100, 600, 400)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_move)
        self.timer.start(1000)
    
    def move_palet(self, source, destination):
        if self.towers[source]:
            palet = self.towers[source].pop()
            self.towers[destination].append(palet)
        else:
            print(f"Erreur: Pas de disque à déplacer depuis la tour {source}")
        
    def next_move(self):
        if self.index < len(self.algorithm.moves):
            source, destination = self.algorithm.moves[self.index]
            self.move_palet(source, destination)
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
            for j, palet in enumerate(tower):
                palet_index = palet - 1
                painter.setBrush(QBrush(QColor(0, 0, 255)))
                painter.drawRect(
                    self.tower_positions[i] - self.palet_widths[palet_index] // 2, 
                    280 - j * 20, 
                    self.palet_widths[palet_index], 20
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #algorithm = HanoiAlgorithm(4)
    #algorithm = hanoi_iterative(4)
    algorithm = HanoiIterative(4)
    window = SimulationMoves(algorithm)
    window.show()
    sys.exit(app.exec())