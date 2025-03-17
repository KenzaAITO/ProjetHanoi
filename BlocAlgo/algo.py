import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def hanoi_iteratif(nb_palets):
    mouvements = []  # Liste pour enregistrer les mouvements effectués
    source, auxiliaire, destination = 1, 2, 3  # Définition des axes

    if nb_palets % 2 == 0:
        auxiliaire, destination = destination, auxiliaire

    # Initialisation des tours
    tours = {1: list(reversed(range(1, nb_palets + 1))), 2: [], 3: []}

    total_mouvements = (2 ** nb_palets) - 1

    for coup in range(1, total_mouvements + 1):
        if coup % 3 == 1:
            origine, destination = source, destination
        elif coup % 3 == 2:
            origine, destination = source, auxiliaire
        else:
            origine, destination = auxiliaire, destination

        # Calcul du nombre de palets avant le mouvement
        nb_palets_origine = len(tours[origine])
        nb_palets_destination = len(tours[destination])

        # Effectuer le mouvement
        if tours[origine] and (not tours[destination] or tours[origine][-1] < tours[destination][-1]):
            palet = tours[origine].pop()
            tours[destination].append(palet)
        elif tours[destination] and (not tours[origine] or tours[destination][-1] < tours[origine][-1]):
            palet = tours[destination].pop()
            tours[origine].append(palet)
            origine, destination = destination, origine

        # Enregistrement du mouvement avec les informations supplémentaires
        mouvements.append((origine, destination, nb_palets_origine, nb_palets_destination))

    return mouvements


def animate_hanoi(mouvements, nb_palets):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 4)
    ax.set_ylim(0, nb_palets + 1)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(['Source', 'Auxiliaire', 'Destination'])

    # Initialisation des tours et des palets
    tours = {1: list(reversed(range(1, nb_palets + 1))), 2: [], 3: []}
    barres = []

    # Afficher les barres représentant les palets pour chaque tour
    def update(frame):
        ax.clear()
        ax.set_xlim(0, 4)
        ax.set_ylim(0, nb_palets + 1)
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels(['Source', 'Auxiliaire', 'Destination'])

        # Récupération du mouvement à la frame
        origine, destination, nb_palets_origine, nb_palets_destination = mouvements[frame]

        # Effectuer le mouvement
        if tours[origine] and (not tours[destination] or tours[origine][-1] < tours[destination][-1]):
            palet = tours[origine].pop()
            tours[destination].append(palet)
        elif tours[destination] and (not tours[origine] or tours[destination][-1] < tours[origine][-1]):
            palet = tours[destination].pop()
            tours[origine].append(palet)
            origine, destination = destination, origine

        # Afficher les barres représentant les palets
        for i, (tour, palets) in enumerate(tours.items(), start=1):
            for j, palet in enumerate(palets):
                ax.bar(i, palet, width=0.5, bottom=j, color=plt.cm.viridis(palet / nb_palets))

        # Afficher les informations du mouvement actuel
        ax.text(2, nb_palets + 0.5, f"Déplacement {frame + 1}: Tour {origine} -> Tour {destination}",
                fontsize=12, ha='center')

        return barres

    ani = animation.FuncAnimation(fig, update, frames=len(mouvements), interval=1000, repeat=False)
    plt.show()


if __name__ == "__main__":
    n_palets = 4
    mouvements = hanoi_iteratif(n_palets)
    animate_hanoi(mouvements, n_palets)
