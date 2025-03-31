import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import dash
import threading
from dash import dcc, html
from dash.dependencies import Input, Output
from BlocAlgo.HanoiIterative import HanoiIterative
from Dashboard import Dashboard  # Assure-toi d'importer la classe Dashboard

VITESSE_MOVE = 80

class SimuAlgoEtBras(QMainWindow):

    def __init__(self, algorithm):
        super().__init__()

        self.setWindowTitle("Simulation de Hanoi avec Bras Robotisé")
        self.setGeometry(100, 100, 800, 600)  # Taille et position de la fenêtre

        # Variables internes pour la simulation
        self.grab_on = False
        self.current_move = "Coup 1"
        self.pick_height = 0
        self.drop_height = 1

        # Création de la simulation
        self.algorithm = algorithm  # Cela représente votre classe de simulation
        self.tower_positions = [100, 300, 500]
        self.palet_widths = [80, 70, 60, 50, 40][:self.algorithm.nb_palet_camera]
        self.towers = {0: list(range(1, self.algorithm.nb_palet_camera + 1)), 1: [], 2: []}
        self.index = 0
        self.movements = self.algorithm.get_move_matrix()

        self.robot_arm_x = 100  
        self.robot_arm_y = 50   
        self.robot_holding_palet = None  
        self.last_palet_moved = None  
        self.movement_stage = 0  # Nouvelle variable pour gérer les étapes du déplacement
        self.current_move = None  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(1000)  # Mettre à jour chaque seconde

        # Instancier le tableau de bord pour l'intégrer à la simulation
        self.dashboard = Dashboard()
        self.dashboard.show()  # Affiche la fenêtre du tableau de bord

        # Dash App Initialization
        self.dash_app = dash.Dash(__name__)
        self.dash_app.layout = self.create_dash_layout()

        # Thread pour exécuter le serveur Dash sans bloquer PyQt
        self.dash_thread = threading.Thread(target=self.run_dash_server)
        self.dash_thread.setDaemon(True)  # Ferme ce thread lorsque le programme principal se termine
        self.dash_thread.start()

    def create_dash_layout(self):
        """Crée la mise en page du tableau de bord Dash"""
        return html.Div([
            html.H1("Tableau de bord de la simulation"),
            html.Div([
                html.Label("Mouvement actuel:"),
                dcc.Textarea(id='current-move', value=self.current_move, style={'width': '100%'}),
            ]),
            html.Div([
                html.Label("Etat de la prise:"),
                dcc.Checklist(
                    id='grab-state',
                    options=[{'label': 'Prise active', 'value': 'active'}],
                    value=['active'] if self.grab_on else [],
                    inline=True,
                ),
            ]),
            html.Div([
                html.Label("Hauteurs du bras:"),
                html.Div([
                    html.Label(f"Hauteur de prise: {self.pick_height}"),
                    html.Label(f"Hauteur de dépose: {self.drop_height}")
                ])
            ])
        ])

    def run_dash_server(self):
        """Lance le serveur Dash dans un thread séparé"""
        self.dash_app.run_server(debug=True, use_reloader=False)

    def execute_next_step(self):
        """Exécute chaque étape d'un déplacement progressivement."""
        if self.current_move is None and self.index < len(self.movements):
            # Récupérer le prochain mouvement
            self.current_move = self.movements[self.index]
            self.movement_stage = 0  # Recommencer l'animation à l'étape 0

        if self.current_move:
            move_num, origine, destination, palets_origin_before, palets_destination_before = self.current_move

            if self.movement_stage == 0:
                # Étape 1 : Se déplacer horizontalement vers la tour d'origine
                self.deplacer_vers_axe(origine - 1)
                if self.robot_arm_x == self.tower_positions[origine - 1]:
                    self.movement_stage += 1  # Passer à l'étape suivante
                self.update()

            elif self.movement_stage == 1:
                # Étape 2 : Descendre pour attraper le palet
                self.robot_arm_y = 250
                self.update()
                self.movement_stage += 1

            elif self.movement_stage == 2:
                # Étape 3 : Attraper le palet et le retirer de la tour d'origine
                print(f"Avant attraper : Tour origine ({origine}) - Palets avant : {palets_origin_before}")

                # Suppression du palet de la tour d'origine ici, avant de "attraper" le palet
                origin_tower_index = self.tower_positions.index(self.robot_arm_x)
                if origin_tower_index != -1 and self.towers[origin_tower_index]:
                    removed_palet = self.towers[origin_tower_index].pop()
                    self.last_palet_moved = removed_palet
                    self.robot_holding_palet = removed_palet
                    self.grab_on = True
                    self.update()
                    self.movement_stage += 1

            elif self.movement_stage == 3:
                self.deplacer_vers_axe(destination - 1)
                if self.robot_arm_x == self.tower_positions[destination - 1]:
                    self.movement_stage += 1
                self.update()

            elif self.movement_stage == 4:
                self.robot_arm_y = 100
                self.update()
                self.movement_stage += 1

            elif self.movement_stage == 5:
                self.towers[destination - 1].append(self.robot_holding_palet)
                self.robot_holding_palet = None
                self.grab_on = False
                self.index += 1
                self.current_move = None
                self.movement_stage = 0
                self.update()

    def update_simulation(self):
        """Mise à jour de la simulation à chaque tick"""
        self.execute_next_step()

    def deplacer_vers_axe(self, cible):
        """Déplace le bras horizontalement de manière progressive, deux fois plus rapide."""
        target_x = self.tower_positions[cible]
        step = VITESSE_MOVE if target_x > self.robot_arm_x else -VITESSE_MOVE  # Doublé la vitesse en passant de 5 à 10

        # Si la distance est assez petite, on ajuste directement la position sans incrément
        if abs(self.robot_arm_x - target_x) <= VITESSE_MOVE:
            self.robot_arm_x = target_x
        else:
            self.robot_arm_x += step

        # Mise à jour de la vue
        self.update()

    def update(self):
        """Met à jour l'interface Dash et le tableau de bord PyQt"""
        # Mettre à jour les éléments Dash avec les nouvelles informations de simulation
        self.dash_app.layout = self.create_dash_layout()
        self.dash_app.layout.children[1].children[0].value = self.current_move
        self.dash_app.layout.children[2].children[0].value = ['active'] if self.grab_on else []
        self.dash_app.layout.children[3].children[0].children[0].children[0] = f"Hauteur de prise: {self.pick_height}"
        self.dash_app.layout.children[3].children[0].children[1].children[0] = f"Hauteur de dépose: {self.drop_height}"

        # Mise à jour du tableau de bord PyQt
        self.dashboard.update_grab_state(self.grab_on)
        self.dashboard.update_current_move(self.current_move)
        self.dashboard.update_height(self.pick_height, self.drop_height)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    algorithm = HanoiIterative(5)
    window = SimuAlgoEtBras(algorithm)
    window.show()
    sys.exit(app.exec())