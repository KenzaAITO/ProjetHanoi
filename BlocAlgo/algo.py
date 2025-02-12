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

        # Gérer le déplacement correct
        if towers[from_tower]:  # Si la tour d'origine n'est pas vide
            disk = towers[from_tower].pop()
            towers[to_tower].append(disk)
        else:  # Si la tour d'origine est vide, inversion
            disk = towers[to_tower].pop()
            towers[from_tower].append(disk)
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
    n_disks = 5
    result = hanoi_iterative(n_disks)

    afficher_mouvements(result)


def afficher_mouvements(movements):
    """
    Affiche les mouvements du jeu de Hanoï sous forme de tableau.

    Parameters:
    movements (list): Liste des mouvements sous forme de tuples ou dictionnaires.
    """
    print("\n=== Mouvements du jeu de Hanoï ===")
    print(f"{'Coup':<6}{'Origine':<8}{'Destination':<12}{'Restants'}")
    print("-" * 35)

    for move in movements:
        if isinstance(move, dict):  # Si format dictionnaire
            print(f"{move['step']:<6}{move['from']:<8}{move['to']:<12}{move['remaining']}")
        else:  # Si format tuple
            print(f"{move[0]:<6}{move[1]:<8}{move[2]:<12}{move[3]}")

# Exemple d'utilisation avec une liste de tuples
#movements_tuples = [
#    (1, 1, 3, 2),
#    (2, 1, 2, 1),
#    (3, 3, 2, 1),
#    (4, 1, 3, 0),
#]





# Exemple d'utilisation
if __name__ == "__main__":
    n_disks = 7
    result = hanoi_iterative(n_disks)
    
    # Affichage des mouvements
    for move in result:
        #print(move)

        afficher_mouvements(movements_tuples)
        #afficher_mouvements(movements_dicts)
