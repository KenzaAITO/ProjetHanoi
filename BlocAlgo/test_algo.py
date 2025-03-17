class HanoiIterative:
    def __init__(self, nb_palet_camera):
        self.nb_palet_camera = nb_palet_camera
        self.movements = []
        self.towers = {1: list(reversed(range(1, nb_palet_camera + 1))), 2: [], 3: []}
        self.solve()

    def solve(self):
        source, auxiliary, destination = 1, 2, 3

        # Si le nombre de disques est pair, on inverse auxiliaire et destination
        if self.nb_palet_camera % 2 == 0:
            auxiliary, destination = destination, auxiliary

        total_moves = (2 ** self.nb_palet_camera) - 1

        for move in range(1, total_moves + 1):
            if move % 3 == 1:
                from_tower, to_tower = source, destination
            elif move % 3 == 2:
                from_tower, to_tower = source, auxiliary
            else:
                from_tower, to_tower = auxiliary, destination

            # Vérification des mouvements valides
            if self.towers[from_tower] and (not self.towers[to_tower] or self.towers[from_tower][-1] < self.towers[to_tower][-1]):
                palet = self.towers[from_tower].pop()
                self.towers[to_tower].append(palet)
            elif self.towers[to_tower] and (not self.towers[from_tower] or self.towers[to_tower][-1] < self.towers[from_tower][-1]):
                palet = self.towers[to_tower].pop()
                self.towers[from_tower].append(palet)
                from_tower, to_tower = to_tower, from_tower  # Correction de l'ordre

            # Ajout du mouvement avec mise à jour du nombre de disques restants
            self.movements.append((move, from_tower, to_tower, len(self.towers[from_tower])))

    def afficher_mouvements(self):
        """
        Affiche les mouvements du jeu de Hanoï sous forme de tableau.
        """
        print("\n=== Mouvements du jeu de Hanoï ===")
        print(f"{'Coup':<6}{'Origine':<8}{'Destination':<12}{'Restants'}")
        print("-" * 35)

        for move in self.movements:
            print(f"{move[0]:<6}{move[1]:<8}{move[2]:<12}{move[3]}")

# Test avec 4 disques
if __name__ == "__main__":
    n_palets = 4
    hanoi = HanoiIterative(n_palets)
    hanoi.afficher_mouvements()
