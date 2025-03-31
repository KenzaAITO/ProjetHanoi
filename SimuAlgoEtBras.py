import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout
from BlocAlgo.HanoiIterative import HanoiIterative
from Dashboard import Dashboard

VITESSE_MOVE = 80

class SimuAlgoEtBras(QMainWindow):

    def __init__(self, algorithm):
        super().__init__()

        self.setWindowTitle("Simulation de Hanoi avec Bras Robotisé")
        self.setGeometry(100, 100, 800, 600)  # Taille et position de la fenêtre

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
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)
        
        # Variables internes pour la simulation
        self.grab_on = False
        self.current_move = "Coup 1"
        self.pick_height = 0
        self.drop_height = 1

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
                    # Identifier le palet à retirer
                    removed_palet = self.towers[origin_tower_index].pop()  # Retirer le dernier palet de la tour
                    print(f"Palet {removed_palet} retiré de la tour {origin_tower_index}")
                    
                    # Garder la taille inchangée pendant ce processus
                    self.robot_holding_palet = removed_palet  # On garde ce palet en mémoire pour le déplacer
                else:
                    print("Erreur : La tour d'origine est vide ou l'index est invalide.")
                
                self.movement_stage += 1  # Passer à l'étape suivante
                self.update()

            elif self.movement_stage == 3:
                # Étape 4 : Remonter le bras avec le palet (la taille du palet reste inchangée)
                self.robot_arm_y = 50  # Remonter avec le palet
                self.update()
                self.movement_stage += 1

            elif self.movement_stage == 4:
                # Étape 5 : Se déplacer horizontalement vers la tour de destination
                self.deplacer_vers_axe(destination - 1)
                if self.robot_arm_x == self.tower_positions[destination - 1]:
                    self.movement_stage += 1  # Passer à l'étape suivante
                self.update()

            elif self.movement_stage == 5:
                # Étape 6 : Descendre le bras pour déposer le palet
                # La hauteur ne modifie pas la taille du palet
                self.robot_arm_y = 250 - len(self.towers[destination - 1]) * 20  # Ajuster la hauteur mais pas la taille du palet
                self.update()
                self.movement_stage += 1

            elif self.movement_stage == 6:
                # Étape 7 : Déposer le palet
                print(f"Avant dépôt : Tour destination ({destination}) - Palets avant : {palets_destination_before}")
                # Ajouter le dernier palet déplacé sur la tour de destination
                self.towers[destination - 1].append(self.robot_holding_palet)  # Déposer le palet dans la destination
                print(f"Palet {self.robot_holding_palet} déplacé vers la tour {destination - 1}")

                # Une fois le palet déposé, on conserve ce palet comme "dernier déplacé"
                self.last_palet = self.robot_holding_palet  # Garder une référence du dernier palet déplacé

                # Mettre à jour la variable `highlighted_palet` pour marquer le palet qui sera coloré
                self.highlighted_palet = self.robot_holding_palet  # Ce palet sera coloré pendant le tour suivant

                # Réinitialisation après le déplacement
                self.robot_holding_palet = None
                self.movement_stage += 1

            elif self.movement_stage == 7:
                # Étape 8 : Remonter à la position initiale
                self.robot_arm_y = 50
                self.update()
                self.movement_stage = 0
                self.index += 1
                self.current_move = None  # Réinitialiser pour passer au mouvement suivant

            elif self.movement_stage == 8:
                # Étape 9 : Mettre à jour les étapes et réinitialiser pour le mouvement suivant
                self.update()

                # Afficher le palet déplacé avec une couleur différente pour le tour suivant
                if self.highlighted_palet:
                    print(f"Palet {self.highlighted_palet} est maintenant visible en couleur différente")
                    # Logic to change color here, for example:
                    self.change_palet_color(self.highlighted_palet, "pink")  # Change couleur à rose

                    # Après un tour, réinitialiser la couleur
                    self.highlighted_palet = None

                self.movement_stage = 0
                self.index += 1
                self.current_move = None  # Réinitialiser pour passer au mouvement suivant

    def change_palet_color(self, palet, color):
        """Change la couleur d'un palet."""
        # Exemple de code pour changer la couleur d'un palet, selon sa position dans les tours
        if palet in self.towers[0]:
            # Code pour changer la couleur du palet sur la tour 0
            print(f"Palet {palet} coloré en {color} sur la tour 0")
            # Mettez à jour l'affichage graphique ici, pour l'affichage réel
        elif palet in self.towers[1]:
            # Code pour changer la couleur du palet sur la tour 1
            print(f"Palet {palet} coloré en {color} sur la tour 1")
            # Mettez à jour l'affichage graphique ici
        elif palet in self.towers[2]:
            # Code pour changer la couleur du palet sur la tour 2
            print(f"Palet {palet} coloré en {color} sur la tour 2")
            # Mettez à jour l'affichage graphique ici

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

    def grab_pallet(self, palets_before, grab):
        """Attrape ou relâche un palet."""
        if grab:
            if isinstance(palets_before, list) and palets_before:
                self.robot_holding_palet = palets_before[-1]  # Attrape le dernier palet
                self.last_palet_moved = self.robot_holding_palet
                # Ajout d'une vérification et affichage pour déboguer
                print(f"Valeur de self.robot_arm_x: {self.robot_arm_x}")
                print(f"Liste des positions de tours: {self.tower_positions}")
                
                if self.robot_arm_x not in self.tower_positions:
                    print(f"Erreur: {self.robot_arm_x} n'est pas dans {self.tower_positions}")
                    return  # Arrêter l'exécution si la position n'est pas valide

                current_tower = self.tower_positions.index(self.robot_arm_x)
                self.towers[current_tower].pop()
            elif isinstance(palets_before, int):
                self.robot_holding_palet = palets_before  # Si c'est un seul entier, on l'attrape directement
                self.last_palet_moved = palets_before
        else:
            if self.robot_holding_palet:
                # Ajout d'une vérification et affichage pour déboguer
                print(f"Valeur de self.robot_arm_x: {self.robot_arm_x}")
                print(f"Liste des positions de tours: {self.tower_positions}")
                
                if self.robot_arm_x not in self.tower_positions:
                    print(f"Erreur: {self.robot_arm_x} n'est pas dans {self.tower_positions}")
                    return  # Arrêter l'exécution si la position n'est pas valide
                
                current_tower = self.tower_positions.index(self.robot_arm_x)
                self.towers[current_tower].append(self.robot_holding_palet)
                self.robot_holding_palet = None

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    algorithm = HanoiIterative(5)
    window = SimuAlgoEtBras(algorithm)
    window.show()
    sys.exit(app.exec())


