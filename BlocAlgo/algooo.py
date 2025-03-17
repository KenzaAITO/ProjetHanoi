def hanoi_iterative(nb_palet_camera):
    """
    Algorithme itératif pour résoudre la Tour de Hanoï en partant toujours de l'axe 1.

    Parameters:
    nb_palet_camera (int): Nombre de disques.

    Returns:
    list of tuple: Liste des mouvements sous la forme 
                   (numéro_du_coup, axe_d'origine, axe_destination, nb_palets_restants_sur_origine)
    """
    movements = []
    source, auxiliary, destination = 1, 2, 3

    # Si le nombre de disques est pair, on inverse auxiliaire et destination
    if nb_palet_camera % 2 == 0:
        auxiliary, destination = destination, auxiliary

    # Initialisation des tours
    towers = {1: list(reversed(range(1, nb_palet_camera + 1))), 2: [], 3: []}

    total_moves = (2 ** nb_palet_camera) - 1

    for move in range(1, total_moves + 1):
        if move % 3 == 1:
            from_tower, to_tower = source, destination
        elif move % 3 == 2:
            from_tower, to_tower = source, auxiliary
        else:
            from_tower, to_tower = auxiliary, destination

        # Vérification des mouvements valides
        if towers[from_tower] and (not towers[to_tower] or towers[from_tower][-1] < towers[to_tower][-1]):
            palet = towers[from_tower].pop()
            towers[to_tower].append(palet)
        elif towers[to_tower] and (not towers[from_tower] or towers[to_tower][-1] < towers[from_tower][-1]):
            palet = towers[to_tower].pop()
            towers[from_tower].append(palet)
            from_tower, to_tower = to_tower, from_tower  # Correction de l'ordre

        # Ajout du mouvement avec mise à jour du nombre de disques restants
        movements.append((move, from_tower, to_tower, len(towers[from_tower])))

    return movements


def afficher_mouvements(movements):
    """
    Affiche les mouvements du jeu de Hanoï sous forme de tableau.

    Parameters:
    movements (list): Liste des mouvements sous forme de tuples.
    """
    print("\n=== Mouvements du jeu de Hanoï ===")
    print(f"{'Coup':<6}{'Origine':<8}{'Destination':<12}{'Restants'}")
    print("-" * 35)

    for move in movements:
        print(f"{move[0]:<6}{move[1]:<8}{move[2]:<12}{move[3]}")


# Test avec 5 disques
if __name__ == "__main__":
    n_palets = 4
    result = hanoi_iterative(n_palets)

    afficher_mouvements(result)
