## Introduction

Dans le cadre d'un projet collectif de l'ecole Polytech tours, Nous avons concu pour les journées portes ouvertes et autres demonstrations un programme qui permet au robot DOTOT magician de jouer au JEU DE HANOI. Le robot analyse le set qui est placé devant lui et est capable de resoudre le jeu de Hanoi grace à ca caméra.

## Fonctionnalité 

- **Deplacement :** Le robot possede des deplacemenst pres defini qui lui permettent de jouer ( deplacer et poser aux bons endroit les palets) pendant toute sla durée du jeu
- **Algorithme :** Le robot est capable grace a un algorithme de definir son prochain coup basé sur la vision du jeu en temps réel
- **Caméra:** Une caméra est installé sur la tete du robot pour visualiser en temps réel le plateau de jeu.


## Prerequisites

Robot: 
    Installer le logiciel DOBOTSTUDIO DobotStudio (DOBOT Magician)
    https://www.dobot-robots.com/service/download-center

Plateau de jeu:
    Un plateau de jeu est necessaire avec les palets qui servirons de pions.
    Voir libraries impression 3D : ***************************

Caméra:

Une caméra est necessaire pour que le robot connaisse l'emplacement des palets.
Reference caméra pour le projet: WebCam 
Impression 3D du support pour la caméra


## Libraries

Les libraries sont gére via l'environnement Poetry 
installation de poetry 
on mac 
on windows

## Dependencies

Camera







## Getting Started

### Setup

1. **Install MQTT Broker:** 


2. **Run the Project:**
    ```bash
    poetry run python main.py
    ```

### Visualization

The visualization code focuses on plotting the latest positions of the tags without printing updates. The plot should update with the latest positions received from the MQTT messages.

1. **Set up distances between anchors:** Ensure the distances are correctly set in `constants.py` and the tag's code.

2. **Run the visualization code:**
    ```bash
    python3 main.py
    ```
3. **Access the visualization:** Dash is running on `http://127.0.0.1:8050/`.

## Architecture


## Structure diagram 

graph TD;


## Devices


- **Robot:** An MQTT server to receive all the position data from the tags. Note: The default configuration may not allow you to correctly receive the tag's position.

- **Python Visualization:** Subscribes to the MQTT broker and visualizes the position data.

## Sequence Diagram: 


## Algoritm


## Future Enhancements

