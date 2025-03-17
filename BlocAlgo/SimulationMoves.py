import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QTimer

from BlocAlgo.HanoiIterative import HanoiIterative  # Ensure this import is correct

class SimulationMoves(QWidget):

    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.tower_positions = [100, 300, 500]
        self.palet_widths = [80, 70, 60, 50, 40][:self.algorithm.nb_palet_camera]  # Support for 5 disks
        self.towers = {0: list(range(1, self.algorithm.nb_palet_camera + 1)), 1: [], 2: []}
        self.index = 0
        self.movements = self.algorithm.get_move_matrix()  # Ensure the movements are retrieved properly

        # Debug print to check if movements are correct
        print("Movements received in simulation:", self.movements)

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
        if self.index < len(self.movements):
            move_num, source, destination, palets_origin_before, palets_destination_before = self.movements[self.index]
            self.move_palet(source - 1, destination - 1)  # Adjust for zero-based indexing
            print(f"Mouvement {move_num}: Tour {source} → Tour {destination} | Palets avant (Origine: {palets_origin_before}, Destination: {palets_destination_before})")
            self.index += 1
            self.update()
        else:
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # Draw towers
        for x in self.tower_positions:
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawRect(x - 10, 100, 20, 200)
            painter.drawEllipse(x - 15, 80, 30, 30)

        # Draw disks on towers
        for i, tower in self.towers.items():
            for j, palet in enumerate(tower):
                palet_index = palet - 1
                if palet_index < len(self.palet_widths):  # Ensure index doesn't exceed available sizes
                    painter.setBrush(QBrush(QColor(0, 0, 255)))
                    painter.drawRect(
                        self.tower_positions[i] - self.palet_widths[palet_index] // 2, 
                        280 - j * 20, 
                        self.palet_widths[palet_index], 20
                    )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    algorithm = HanoiIterative(5)  # Set to 5 disks
    window = SimulationMoves(algorithm)
    window.show()
    sys.exit(app.exec())