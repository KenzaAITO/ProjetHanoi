import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QTimer

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal du tableau de bord
        self.layout = QVBoxLayout()

        # État de la ventouse (grab)
        self.grab_state_label = QLabel("Ventouse (Grab): Off")
        self.grab_light = QLabel("🟢")  # Le cercle vert ou rouge
        self.grab_light.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.grab_state_label)
        self.layout.addWidget(self.grab_light)

        # Coup en cours
        self.current_move_label = QLabel("Coup actuel: Aucun")
        self.layout.addWidget(self.current_move_label)

        # Hauteur de la prise et de la dépose
        self.height_label = QLabel("Hauteur (Etage): Prise: 0 / Dépose: 0")
        self.layout.addWidget(self.height_label)

        self.setLayout(self.layout)

    def update_grab_state(self, grab_on):
        """Met à jour la couleur de la ventouse."""
        if grab_on:
            self.grab_light.setText("🟢")  # Vert pour 'on'
            self.grab_state_label.setText("Ventouse (Grab): On")
        else:
            self.grab_light.setText("🔴")  # Rouge pour 'off'
            self.grab_state_label.setText("Ventouse (Grab): Off")

    def update_current_move(self, move_info):
        """Met à jour le coup actuel dans le dashboard."""
        self.current_move_label.setText(f"Coup actuel: {move_info}")

    def update_height(self, pick_height, drop_height):
        """Met à jour la hauteur de la prise et de la dépose."""
        self.height_label.setText(f"Hauteur (Etage): Prise: {pick_height} / Dépose: {drop_height}")


class SimuAlgoEtBras(QMainWindow):
    def __init__(self, algorithm):
        super().__init__()

        self.setWindowTitle("Simulation de Hanoi avec Bras Robotisé")
        self.setGeometry(100, 100, 800, 600)  # Taille et position de la fenêtre

        # Création de la simulation
        self.algorithm = algorithm  # Cela représente votre classe de simulation

        # Tableau de bord pour afficher les informations
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)

        # Timer pour simuler l'animation et mise à jour périodique
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000)  # Mettre à jour chaque seconde

        # Variables internes pour la simulation
        self.grab_on = False
        self.current_move = "Coup 1"
        self.pick_height = 0
        self.drop_height = 1

    def update_simulation(self):
        """Simule l'animation et met à jour les informations."""
        # Met à jour les informations en fonction de l'état de la simulation
        self.dashboard.update_grab_state(self.grab_on)
        self.dashboard.update_current_move(self.current_move)
        self.dashboard.update_height(self.pick_height, self.drop_height)

    def update_grab(self, grab_on):
        """Met à jour l'état de la ventouse."""
        self.grab_on = grab_on
        self.update_simulation()

    def update_move(self, move_info):
        """Met à jour le coup en cours."""
        self.current_move = move_info
        self.update_simulation()

    def update_height(self, pick_height, drop_height):
        """Met à jour les hauteurs pour la prise et la dépose."""
        self.pick_height = pick_height
        self.drop_height = drop_height
        self.update_simulation()


# Application PyQt6
if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(f"Dash")
    # # Supposons que vous ayez une classe de simulation pour le Hanoi (ici `None` pour la démo)
    # window = SimuAlgoEtBras(algorithm)
    # window.show()

    # sys.exit(app.exec())