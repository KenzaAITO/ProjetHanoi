import tkinter as tk

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Dashboard de Simulation")
        self.geometry("300x200")  # Taille de la fenêtre du dashboard
        
        # État de la ventouse
        self.grab_state_label = tk.Label(self, text="Ventouse (Grab): Off", font=("Arial", 12))
        self.grab_state_label.grid(row=0, column=0, padx=10, pady=10)

        # Lumière verte ou rouge
        self.grab_light = tk.Canvas(self, width=20, height=20)
        self.grab_light.grid(row=0, column=1, padx=10, pady=10)
        self.update_grab_light(False)  # Initialement OFF

        # Coup en cours
        self.current_move_label = tk.Label(self, text="Coup actuel: Aucun", font=("Arial", 12))
        self.current_move_label.grid(row=1, column=0, padx=10, pady=10)

        # Hauteur
        self.height_label = tk.Label(self, text="Hauteur (Etage): 0", font=("Arial", 12))
        self.height_label.grid(row=2, column=0, padx=10, pady=10)

    def update_grab_light(self, grab_on):
        """Met à jour la couleur de la lumière en fonction de l'état de la ventouse."""
        color = "green" if grab_on else "red"
        self.grab_light.create_oval(0, 0, 20, 20, fill=color, outline=color)

    def update_current_move(self, move_info):
        """Met à jour le coup en cours."""
        self.current_move_label.config(text=f"Coup actuel: {move_info}")

    def update_height(self, pick_height, drop_height):
        """Met à jour les hauteurs d'étage."""
        self.height_label.config(text=f"Hauteur (Etage): Prise {pick_height} / Dépose {drop_height}")
        
    def update_grab_state(self, grab_on):
        """Met à jour l'état de la ventouse."""
        state = "On" if grab_on else "Off"
        self.grab_state_label.config(text=f"Ventouse (Grab): {state}")
        self.update_grab_light(grab_on)


class Simulation:
    def __init__(self):
        self.dashboard = Dashboard()  # Créer le dashboard

        # Variables de simulation
        self.grab_on = False  # L'état de la ventouse
        self.current_move = None  # Coup en cours
        self.current_height_pick = 0  # Hauteur de prise du palet
        self.current_height_drop = 0  # Hauteur de dépose du palet
        
        # Mettre à jour le dashboard à chaque étape
        self.dashboard.update_grab_state(self.grab_on)
        self.dashboard.update_current_move("Aucun")
        self.dashboard.update_height(self.current_height_pick, self.current_height_drop)

    def start_simulation(self):
        """Démarre la simulation."""
        self.dashboard.mainloop()  # Lancer le dashboard Tkinter
        self.execute_move()

    def execute_move(self):
        """Simuler un mouvement de palet."""
        # Exemple de mouvement avec état grab et mise à jour des informations
        self.grab_on = True  # Ventouse allumée (ON)
        self.dashboard.update_grab_state(self.grab_on)
        self.dashboard.update_current_move("Tour 0 -> Tour 1")  # Exemple de coup en cours
        self.dashboard.update_height(0, 1)  # Exemple de hauteur de prise et dépose
        self.grab_on = False  # Après avoir déplacé, la ventouse s'éteint
        self.dashboard.update_grab_state(self.grab_on)


# Initialiser et démarrer la simulation
simulation = Simulation()
simulation.start_simulation()
