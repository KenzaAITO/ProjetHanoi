from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class DobotCalibrator(QWidget):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        self.x = robot.cible_x
        self.z = robot.cible_z
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.label = QLabel(f"X: {self.x}, Z: {self.z}")
        layout.addWidget(self.label)
        
        self.btn_x_up = QPushButton("X +5")
        self.btn_x_up.clicked.connect(lambda: self.update_position(dx=5))
        layout.addWidget(self.btn_x_up)
        
        self.btn_x_down = QPushButton("X -5")
        self.btn_x_down.clicked.connect(lambda: self.update_position(dx=-5))
        layout.addWidget(self.btn_x_down)
        
        self.btn_z_up = QPushButton("Z +5")
        self.btn_z_up.clicked.connect(lambda: self.update_position(dz=5))
        layout.addWidget(self.btn_z_up)
        
        self.btn_z_down = QPushButton("Z -5")
        self.btn_z_down.clicked.connect(lambda: self.update_position(dz=-5))
        layout.addWidget(self.btn_z_down)
        
        self.btn_save = QPushButton("Enregistrer")
        self.btn_save.clicked.connect(self.save_values)
        layout.addWidget(self.btn_save)
        
        self.setLayout(layout)
    
    def update_position(self, dx=0, dz=0):
        self.x += dx
        self.z += dz
        self.robot.move_to_and_check(self.x, self.z)
        self.label.setText(f"X: {self.x}, Z: {self.z}")
    
    def save_values(self):
        self.robot.cible_x = self.x
        self.robot.cible_z = self.z
        print(f"✅ Calibration enregistrée: X={self.robot.cible_x}, Z={self.robot.cible_z}")
        self.close()