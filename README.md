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



## Libraries

Les libraries sont gére via l'environnement Poetry 
installation de poetry 
    sur mac 
    sur windows

## Dependencies

Caméra :
opencv-python

## Getting Started

### Setup


2. **Run the Project:**
    ```bash
    poetry run python main.py
    ```
    ou 
    ```bash
    make run 
    ```

### Visualization


1. **Obtenir la dimension des palets:** 

2. **Run the visualization code:**
    ```bash
    make vision
    ```

## Architecture

```
uwb_mqtt/
├── __init__.py
├── constants.py
├── data.py
├── data_raw_distance.py
├── db/
│   ├── __init__.py
│   └── init_db.py
├── manager.py
├── mqtt_manager.py
├── position_calculator.py
└── visualization.py
```

## Structure diagram 

graph TD;


## Devices


- **Robot:** DOBOT Magician dotée d'une ventouse 

- **Python Visualization:** WebCam 

## Sequence Diagram: 


## Algoritm


## Future Enhancements
