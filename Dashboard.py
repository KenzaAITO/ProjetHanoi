import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor  # Ajout de l'import pour QColor

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard de Simulation")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Création des labels
        self.grab_state_label = QLabel("Ventouse (Grab): Off", self)
        self.grab_light = QLabel("🟢") 
        self.current_move_label = QLabel("Coup actuel: Aucun", self)
        self.height_label = QLabel("Hauteur (Etage): 0 / 0", self)

        # Ajout des labels au layout
        layout.addWidget(self.grab_state_label)
        layout.addWidget(self.current_move_label)
        layout.addWidget(self.height_label)

        # Canvas pour la lumière (Ventouse)
        self.grab_light_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.grab_light = QGraphicsEllipseItem(0, 0, 20, 20)
        self.grab_light.setBrush(QColor("red"))  # Utilisation de QColor pour la couleur rouge (OFF)
        self.scene.addItem(self.grab_light)
        self.grab_light_view.setScene(self.scene)
        layout.addWidget(self.grab_light_view)

        # Conteneur principal
        container = QWidget(self)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer pour simuler le changement d'état à chaque coup
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dashboard)
        self.timer.start(1000)  # Met à jour chaque seconde pour la démo
        # Variables pour l'état de la ventouse et du coup en cours
        self.grab_on = False
        self.current_move = None
        self.pick_height = 0
        self.drop_height = 0

    def update_grab_light(self, grab_on):
        """Met à jour la couleur de la lumière en fonction de l'état de la ventouse."""
        self.grab_on = grab_on
        color = QColor("green") if grab_on else QColor("red")
        self.grab_light.setBrush(color)

    def update_current_move(self, move_info):
        """Met à jour le coup en cours."""
        self.current_move = move_info
        self.current_move_label.setText(f"Coup actuel: {move_info}")

    def update_height(self, pick_height, drop_height):
        """Met à jour les hauteurs de prise et de dépose."""
        self.pick_height = pick_height
        self.drop_height = drop_height
        self.height_label.setText(f"Hauteur (Etage): Prise {pick_height} / Dépose {drop_height}")

    def update_dashboard(self):
        """Mise à jour du tableau de bord."""
        if self.current_move:
            # Mise à jour des informations (par exemple, le coup actuel)
            self.update_current_move(self.current_move)
        
        # Exemple de mise à jour de la ventouse et des hauteurs pendant un tour
        if self.grab_on:
            self.update_grab_light(True)
        else:
            self.update_grab_light(False)

        # Exemple de mise à jour des hauteurs pour le test
        self.update_height(self.pick_height, self.drop_height)

    def update_grab_state(self, grab_on):
        """Met à jour la couleur de la ventouse."""
        if grab_on:
            self.grab_light.setText("🟢")  # Vert pour 'on'
            self.grab_state_label.setText("Ventouse (Grab): On")
        else:
            self.grab_light.setText("🔴")  # Rouge pour 'off'
            self.grab_state_label.setText("Ventouse (Grab): Off")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()

    # Simuler le déplacement du bras et la mise à jour des informations de simulation
    dashboard.update_current_move("Déplacer palet de Tour 1 à Tour 2")
    dashboard.update_height(1, 3)
    dashboard.update_grab_light(True)

    dashboard.show()
    sys.exit(app.exec())
