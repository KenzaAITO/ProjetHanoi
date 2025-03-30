import pandas as pd
import matplotlib.pyplot as plt

class RobotLogger:
    def __init__(self):
        self.data = []

    def log_movement(self, x, y, z, r, action):
        """Enregistre chaque mouvement du robot avec ses coordonnées."""
        self.data.append({
            "x": x, "y": y, "z": z, "r": r, "action": action
        })

    def save_logs(self, filename="robot_movements.csv"):
        """Sauvegarde les logs dans un fichier CSV."""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        print(f"Logs sauvegardés dans {filename}")

    def plot_movements(self):
        """Affiche la trajectoire du robot en 3D."""
        df = pd.DataFrame(self.data)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df["x"], df["y"], df["z"], c='b', marker='o')

        for i in range(len(df)):
            ax.text(df["x"][i], df["y"][i], df["z"][i], df["action"][i])

        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        ax.set_title("Trajectoire du robot")
        plt.show()

if __name__ == "__main__":
    self.logger = RobotLogger()
    robot.logger.save_logs()
    robot.logger.plot_movements()
