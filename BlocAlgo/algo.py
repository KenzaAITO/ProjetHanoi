def hanoi_iterative(n, source="Source", auxiliary="Auxiliary", destination="Destination"):
    """
    Algorithme itératif pour résoudre la Tour de Hanoï.

    Parameters:
    n (int): Nombre de disques.
    source (str): Nom de la tour source.
    auxiliary (str): Nom de la tour auxiliaire.
    destination (str): Nom de la tour destination.

    Returns:
    list of tuple: Une liste de mouvements (numéro_du_disque, tour_depart, tour_arrivee).
    """
    # Liste des mouvements
    movements = []

    # Si le nombre de disques est pair, inverser auxiliaire et destination
    if n % 2 == 0:
    auxiliary, destination = destination, auxiliary

    # Initialisation des piles représentant les tours
    towers = {source: list(reversed(range(1, n + 1))), auxiliary: [], destination: []}

    # Nombre total de mouvements
    total_moves = (2 ** n) - 1

    for move in range(1, total_moves + 1):
    # Déterminer les tours entre lesquelles déplacer
    if move % 3 == 1:
        from_tower, to_tower = source, destination
    elif move % 3 == 2:
        from_tower, to_tower = source, auxiliary
    else:
        from_tower, to_tower = auxiliary, destination

    # Règle pour le déplacement
    if not towers[to_tower] or (towers[from_tower] and towers[from_tower][-1] < towers[to_tower][-1]):
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)
        movements.append((disk, from_tower, to_tower))
    else:
        disk = towers[to_tower].pop()
        towers[from_tower].append(disk)
        movements.append((disk, to_tower, from_tower))

    return movements

# Communication avec d'autres modules
def communicate_with_system(movements, move_disk, camera_check):
    """
    Communique les mouvements avec le bras robotisé et la caméra.

    Parameters:
    movements (list of tuple): La séquence des mouvements calculée par l'algorithme.
    move_disk (function): Fonction pour contrôler le bras robotisé.
    camera_check (function): Fonction pour vérifier l'état des tours avec la caméra.
    """
    for step, (disk, from_tower, to_tower) in enumerate(movements, start=1):
    print(f"Mouvement {step}: Déplacer le disque {disk} de {from_tower} à {to_tower}")
    
    # Envoyer la commande au bras robotisé
    move_disk(disk, from_tower, to_tower)
    
    # Vérifier l'état avec la caméra
    if not camera_check():
        print(f"Erreur détectée après le mouvement {step}. Arrêt.")
        break

    # Exemple d'utilisation
    if __name__ == "__main__":
    # Exemple de résolution pour 3 disques
    n_disks = 3
    movements = hanoi_iterative(n_disks)

# Simulations des fonctions du bras robotisé et de la caméra
def move_disk_simulation(disk, from_tower, to_tower):
    print(f"Bras robotisé : Déplacer le disque {disk} de {from_tower} à {to_tower}")

def camera_check_simulation():
    print("Caméra : Vérification des tours... OK")
    return True # Simule que tout est toujours correct

# Lancer la communication avec le système
communicate_with_system(movements, move_disk_simulation, camera_check_simulation)