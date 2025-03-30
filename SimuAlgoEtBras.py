import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QTimer
from BlocAlgo.HanoiIterative import HanoiIterative

class SimuAlgoEtBras(QWidget):

    def __init__(self, algorithm):
        super().__init__()
        self.algorithm = algorithm
        self.tower_positions = [100, 300, 500]
        self.palet_widths = [80, 70, 60, 50, 40][:self.algorithm.nb_palet_camera]
        self.towers = {0: list(range(1, self.algorithm.nb_palet_camera + 1)), 1: [], 2: []}
        self.index = 0
        self.movements = self.algorithm.get_move_matrix()

        self.robot_arm_x = 100  
        self.robot_arm_y = 50   
        self.robot_holding_palet = None  
        self.last_palet_moved = None  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_move)
        self.timer.start(3000)  # ⏳ On ralentit à 3 secondes entre chaque mouvement

    def move_palet(self, source, destination):
        """Déplace un palet avec animation du bras."""
        if self.towers[source]:
            self.robot_holding_palet = self.towers[source].pop()
            self.last_palet_moved = self.robot_holding_palet  
            self.robot_arm_x = self.tower_positions[source]
            self.update()
            QTimer.singleShot(1500, lambda: self.descend_arm(destination))  # ⏳ Animation plus lente

    def next_move(self):
        """Exécute le prochain mouvement de la solution."""
        if self.index < len(self.movements):
            move_num, source, destination, _, _ = self.movements[self.index]
            self.move_palet(source - 1, destination - 1)  
            print(f"Mouvement {move_num}: Tour {source} → Tour {destination}")
            self.index += 1
            self.update()
        else:
            self.timer.stop()

    def descend_arm(self, destination):
        """Fait descendre le bras lentement et relâche le palet."""
        self.robot_arm_y = 250
        self.update()
        QTimer.singleShot(1500, lambda: self.drop_palet(destination))  # ⏳ Animation plus lente

    def drop_palet(self, destination):
        """Dépose le palet et remonte le bras."""
        self.towers[destination].append(self.robot_holding_palet)
        self.robot_holding_palet = None
        self.robot_arm_y = 50
        self.robot_arm_x = self.tower_positions[destination]
        self.update()

    def paintEvent(self, event):
        """Affiche les tours, les palets et le bras robotique."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # Dessiner les tours
        for x in self.tower_positions:
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            painter.drawRect(x - 10, 100, 20, 200)

        # Dessiner les palets
        for i, tower in self.towers.items():
            for j, palet in enumerate(tower):
                painter.setBrush(QBrush(QColor(255, 105, 180) if palet == self.last_palet_moved else QColor(0, 0, 255)))
                painter.drawRect(self.tower_positions[i] - self.palet_widths[palet - 1] // 2,
                                 280 - j * 20,
                                 self.palet_widths[palet - 1], 20)

        # Dessiner le bras du robot
        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawRect(self.robot_arm_x - 5, self.robot_arm_y, 10, 50)

        # Si le robot tient un palet, l'afficher en l'air
        if self.robot_holding_palet:
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawRect(self.robot_arm_x - self.palet_widths[self.robot_holding_palet - 1] // 2,
                             self.robot_arm_y + 50,
                             self.palet_widths[self.robot_holding_palet - 1], 20)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    algorithm = HanoiIterative(5)
    window = SimuAlgoEtBras(algorithm)
    window.show()
    sys.exit(app.exec())
