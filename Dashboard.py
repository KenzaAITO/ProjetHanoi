import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsEllipseItem, QGraphicsScene, QGraphicsView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsScene, QGraphicsTextItem
from PyQt6.QtCore import QRectF

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard de Simulation")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        layout = QVBoxLayout(self)

        # Create labels
        self.grab_state_label = QLabel("Ventouse (Grab): Off", self)
        self.current_move_label = QLabel("Coup actuel: Aucun", self)
        self.height_label = QLabel("Hauteur (Etage): 0 / 0", self)

        # Add labels to the layout
        layout.addWidget(self.grab_state_label)
        layout.addWidget(self.current_move_label)
        layout.addWidget(self.height_label)

        # Canvas for the light (Ventouse)
        self.view = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)  # Attach the scene to the view

        # Add the view to the layout
        layout.addWidget(self.view)

        # Create a circle item (representing the light)
        self.grab_light = QGraphicsEllipseItem(0, 0, 50, 50)  # Circle representing the light
        self.grab_light.setBrush(Qt.GlobalColor.red)  # Default to red (off state)
        self.scene.addItem(self.grab_light)

        # Create a text item to display the status (on/off)
        self.grab_text = QGraphicsTextItem("🔴")  # Default text for "off" state
        self.grab_text.setPos(60, 10)  # Positioning the text next to the circle
        self.scene.addItem(self.grab_text)

    def update_grab_state(self, grab_on):
        """Updates the grab state light and text"""
        if grab_on:
            self.grab_light.setBrush(Qt.GlobalColor.green)  # Green for 'on'
            self.grab_text.setPlainText("🟢")  # Change text to green
        else:
            self.grab_light.setBrush(Qt.GlobalColor.red)  # Red for 'off'
            self.grab_text.setPlainText("🔴")  # Change text to red

    def update_grab_light(self, grab_on):
        """Update the grab light color based on the grab state."""
        self.grab_on = grab_on
        color = QColor("green") if grab_on else QColor("red")
        self.grab_light.setBrush(color)

    def update_current_move(self, move_info):
        """Update the current move."""
        self.current_move = move_info
        self.current_move_label.setText(f"Coup actuel: {move_info}")

    def update_height(self, pick_height, drop_height):
        """Update pick and drop heights."""
        self.pick_height = pick_height
        self.drop_height = drop_height
        self.height_label.setText(f"Hauteur (Etage): Prise {pick_height} / Dépose {drop_height}")

    def update_dashboard(self):
        """Update the dashboard information."""
        if self.current_move:
            self.update_current_move(self.current_move)
        
        # Update the grab state and heights during a move
        if self.grab_on:
            self.update_grab_light(True)
        else:
            self.update_grab_light(False)

        # Example of updating the heights for testing
        self.update_height(self.pick_height, self.drop_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = Dashboard()

    # Simulate the arm movement and update simulation info
    dashboard.update_current_move("Déplacer palet de Tour 1 à Tour 2")
    dashboard.update_height(1, 3)
    dashboard.update_grab_light(True)

    dashboard.show()
    sys.exit(app.exec())
