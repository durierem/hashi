---
lang: fr-FR
title: hashi
subtitle: Solveur de Hashiwokakero
author:
    - Rémi Durieu
    - Thomas Evrard
    - Kaci Hammoudi
date: Janvier 2020
documentclass: report
toc: true
fontsize: 12
monofont: Liberation Mono
---

# 1) Choix liés à la programmation

Pour l'implémentation, nous avons choisi Python afin de nous affranchir
des subtilités techniques liées aux langages C et Java. Le temps d'exécution
du programme en est probablement impacté mais nous gagnons un niveau
d'abstraction non-négligeable pour ce genre de projet.

## 1.1) Encodage des grilles

Le programme travaille avec des grilles encodées au format JSON et il ne peut
y avoir qu'une grille par fichier. La grille est décrite dans un attribut
"grid", lequel contient un tableau à deux dimensions dans lequel un zéro
correspond à une case vide et un chiffre strictement supérieur à zéro à une
île et au nombre de ponts auxquels cette île doit être reliée.

Cette notation permet d'être facilement compréhensible et est portable à
travers les implémentations. En effet, Python, comme beaucoup d'autres
langages incorpore un module JSON dans sa bibliothèque standard.

## 1.2) Description des classes et structures de données

Pour cela nous avons décidé de représenter une grille de Hashiwokakero (classe
`Grid`) par une liste Python bidimensionnelle de cellules (classe `Cell`).
Chaque cellule contient soit une île, soit un ou plusieurs ponts, soit rien du
tout.

Pour se déplacer et se repérer dans les grilles, nous avons décidé d’ajouter
des curseurs (classe `Cursor`). Un curseur principal est lié à une grille et
plusieurs curseurs peuvent être utilisés sur la même grille.

Lorsque le curseur principal d'une grille pointe sur les coordonnées d'une
île, nous appellerons cette île l' « île courante ». Nous définirons également
le « sens de lecture » d'une grille : de la gauche vers la droite, et de haut
en bas.

# Algorithmes principaux

## Notion de « ponts possibles »

Dans un premier temps, nous avons besoin d’expliquer une notion importante de
notre algorithme : les « ponts possibles ». À partir d’une île, les ponts
possibles représentent toutes les manières possibles de compléter cette île. C'est-à-dire de lui ajouter autant de ponts qu'elle en a besoin.

### Exemple 1

Voici un exemple où le curseur de la grille se trouve sur l’île 3, on veux la compléter de toutes les façons possible. À gauche, la configuration initiale,
à droite, les deux configurations possibles.

```
----------------------------------------------------------------------
 2                  |        2                          2
 ║                  |        ║                          ║
 2     3     2      |        2     3 ═══ 2    -OU-      2     3 ─── 2
                    |              │                          ║
       2            |              2                          2
----------------------------------------------------------------------
```

Il n’y a que 2 possibilités pour compléter 3 car l’île à sa gauche est déjà
complète.

### Exemple 2

On se trouve cette fois-ci sur le premier 2 (celui le plus en haut). À gauche,
la configuration initiale, à droite la seule configuration possible.

```
----------------------------------------------------------------------
                      2            |           2
                1     ║     1      |     1     ║     1
                      2            |     │     2
                1                  |     1
----------------------------------------------------------------------
```

Il n’y a qu’une possibilité car l’île sur laquelle on se trouve ne peut pas créer de pont avec le 1 de droite.

## Création des grilles (`Grid.__createGrids()`)

Pour comprendre l'algorithme de résolution, nous avons besoin de nous pencher
sur la méthode `Grid.__createGrids()`. Le but de cette méthode est, à partir
de la grille cible, de construire de nouvelles grilles qui contiennent les
"ponts possibles" pour l'île courante.

En fait, sur l'[exemple 1], on applique cette méthode à la grille
de départ et on a deux nouvelles grilles qui contiennent les ponts possibles.

## Algorithme de résolution (`Grid.solve()`)

On créé de nouvelles grilles à partir des ponts possibles de l'île courante.
Pour chacune de ces grilles on teste si toutes les îles sont complètes, et si le graphe décrit par la grille est un graphe connexe. Si c'est le cas, la grille est solution. Sinon on recommence pour chaque grille ainsi créées.

La méthode `solve()` implémente l'algorithme décrit ci-dessus à l'aide d'une file qui contient les grilles à évaluer au fur et à mesure :

```
Fonction TrouverSolution(g):
    f <- Nouvelle file
    Enfiler g dans f
    Placer le curseur de g sur la première île
    TANT QUE f n'est pas vide FAIRE
        g <- Défiler f
        grilles <- Créer nouvelles grilles à partir de g
        POUR TOUT g DANS grilles FAIRE
            SI g n'a pas de prochaine île ALORS
                SI g est connexe ALORS
                    Renvoyer g
                SINON
                    ARRET ITERATION
                FIN SI
            FIN SI
            Déplacer le curseur de g vers la prochaine île
            Enfiler g dans f
        FIN POUR TOUT
    FIN TANT QUE
    Renvoyer Vide
```

# Difficultés rencontrées et pistes d'améliorations

Le choix de la structure de données qui représente une grille a été un réel
défi lors de la réalisation du projet. La difficulté majeure fût de trouver
une structure qui permet de gérer efficacement la notion de pont. C'est en
élaborant l'algorithme que nous avons réussi à déterminer de quels données
nous aurions besoin et comment les organiser.

Nous avons essayé d'améliorer la vitesse d'exécution du programme en appliquant
un algorithme en amont de l'algorithme principal. Le rôle de ce dernier aurait
été de placer les ponts dont la position est forcement déterminé par les îles
avoisinantes. Par exemple, une île ne reliant qu'un seul pont et qui ne possède
qu'une seule île voisine est obligé d'être reliée à cette dernière par un pont
unique.

Dans la même quête d'amélioration de la vitesse d'exécution, nous avons essayé
de paralléliser le processus avec des threads.

...
