class HanoiAlgorithm:
    def __init__(self, n):
        self.n = n
        self.towers = {0: list(range(1, n + 1)), 1: [], 2: []}
        self.moves = []
        self.move_matrix = []
        self.generate_moves(n, 0, 1, 2)
    
    def generate_moves(self, n, source, auxiliary, destination):
        if n == 1:
            self.record_move(source, destination)
            return
        self.generate_moves(n - 1, source, destination, auxiliary)
        self.record_move(source, destination)
        self.generate_moves(n - 1, auxiliary, source, destination)
    
    def record_move(self, source, destination):
        nb_palets_origine = len(self.towers[source])
        nb_palets_destination = len(self.towers[destination])
        self.moves.append((source, destination))
        self.move_matrix.append((len(self.moves), source, destination, nb_palets_origine, nb_palets_destination))


if __name__ == "__main__":
    algorithm = HanoiAlgorithm(4)
    matrice = show.algorithm