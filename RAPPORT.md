---
lang: fr-FR
title: hashi
subtitle: Solveur de Hashiwokakero
author:
    - Thomas Evrard
    - Rémi Durieu
    - Kaci Hammoudi
date: Janvier 2020
documentclass: report
toc: true
fontsize: 12
mainfont: CMU Serif
monofont: CMU Typewriter Text Light
---

# Choix liés à la programmation

Pour l'implémentation, nous avons choisi Python afin de nous affranchir
des subtilités techniques liées aux langages C et Java. Le temps d'exécution
du programme en est probablement impacté mais nous gagnons un niveau
d'abstraction non-négligeable pour ce genre de projet à contrainte de temps.

## 1.1  Encodage des grilles

Le programme travaille avec des grilles encodées au format JSON et il ne peut
y avoir qu'une grille par fichier. La grille est décrite dans un attribut
"grid", lequel contient un tableau à deux dimensions dans lequel un zéro
correspond à une case vide et un chiffre strictement supérieur à zéro à une
île et au nombre de ponts auxquels cette île doit être reliée.

Cette notation permet d'être facilement compréhensible et est portable à
travers les implémentations. En effet, Python, comme beaucoup d'autres
langages incorpore un module JSON dans sa bibliothèque standard.

## 1.2 Description des structures de données

Nous avons décidé de représenter une grille de Hashiwokakero (classe`Grid`)
par une liste Python bidimensionnelle de cellules (classe `Cell`).
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

## 2.1 Notion de « ponts possibles »

Dans un premier temps, nous avons besoin d’expliquer une notion importante de
notre algorithme : les « ponts possibles ». À partir d’une île, les ponts
possibles représentent toutes les manières possibles de compléter cette île.
C'est-à-dire de lui ajouter autant de ponts qu'elle en a besoin.

### 2.1.1 Exemple 1

Voici un exemple où le curseur de la grille se trouve sur l’île 3, on veux la
compléter de toutes les façons possible. À gauche, la configuration initiale,
à droite, les deux configurations possibles.

```
-----------------------------------------------------------------
 2                  |      2                        2
 ║                  |      ║                        ║
 2     3     2      |      2     3 ═══ 2   -OU-     2     3 ─── 2
                    |            │                        ║
       2            |            2                        2
-----------------------------------------------------------------
```

Il n’y a que 2 possibilités pour compléter 3 car l’île à sa gauche est déjà
complète.

### 2.1.2 Exemple 2

On se trouve cette fois-ci sur le premier 2 (celui le plus en haut). À gauche,
la configuration initiale, à droite la seule configuration possible.

```
-----------------------------------------------------------------
                  2            |           2
            1     ║     1      |     1     ║     1
                  2            |     │     2
            1                  |     1
-----------------------------------------------------------------
```

Il n’y a qu’une possibilité car l’île sur laquelle on se trouve ne peut pas
créer de pont avec le 1 de droite.

## 2.2 Création des grilles

Pour comprendre l'algorithme de résolution, nous avons besoin de nous pencher
sur la méthode `Grid.__createGrids()`. Le but de cette méthode est, à partir
de la grille cible, de construire de nouvelles grilles qui contiennent les
ponts possibles pour l'île courante. Sur l'exemple 1, on applique cette
méthode à la grille de départ et on a deux nouvelles grilles qui contiennent
les ponts possibles.

## 2.3 Algorithmes de résolutions

### 2.3.1 Algorithme principal

Le fonctionnement de l'algorithme principal est le suivant : on crée une
liste de nouvelles grilles à partir des ponts possibles de l'île courante.
Puis, pour chacune de ces grilles, on teste si toutes les îles sont complétées,
et si le graphe décrit par la grille est un graphe connexe. Si c'est le cas,
la grille est solution. Sinon on déplace le curseur dans le sens de lecture
vers la prochaine île et on recommence à créer de nouvelles grilles. Cet
algorithme s'apparente à un parcours en largeur.

La méthode `Grid.solve()` implémente cet algorithme à l'aide d'une file qui
contient les grilles créées au fur et à mesure. Ci-dessous, le pseudo-code de
la logique principale.

```
Fonction TrouverSolution(G):
    f <- Nouvelle file
    Enfiler G dans f
    Placer le curseur de G sur la première île
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

### 2.3.2 Algorithme de pré-résolution

Pour améliorer le temps de résolution d'une grille, nous avons utilisé un
autre algorithme en amont, qui diminue la charge de travail de l'algorithme
principal. Cet algorithme consiste à trouver les îles pour lesquelles
l'ensemble des ponts possibles est réduit à un. Ce sont les ponts dont
l'emplacement est déterminé par les îles uniquement. Par exemple, une île ne
reliant qu’un seul pont et qui ne possède qu’une seule île voisine est obligé
d’être reliée à cette dernière par un pont unique.

Cette méthode varie grandement en efficacité en fonction de la complexité de la
grille à résoudre. Par exemple, la grille `grid-17-easy.json` fournie n'est
composée que de ponts de ce genre et peut être résout avec cet algorithme
uniquement. Sur notre machine de test, le temps de résolution est passé de 30 à
4 secondes en appliquant cet algorithme en premier. À contrario, la grille
`grid-17-hard.json` ne profite que très peu de cette pré-résolution et le gain
de temps est très faible. Toujours sur notre machine de test nous sommes
passés de 43 à 39 minutes.

À cause de cette irrégularité, il est inutile d'appliquer cet algorithme sur
chaque nouvelles grilles créées par l'algorithme principal. En effet, la
complexité temporelle de ce dernier est telle, comparée au gain potentiel,
qu'il n'est pas intéressant de l'appliquer à chaque nouvelle itération
car la probabilité de rencontrer une grille sur laquelle l'algorithme de
pré-résolution n'a aucun effet est très élevée.

# Difficultés rencontrées et pistes d'améliorations

Le choix de la structure de données qui représente une grille a été un réel
défi lors de la réalisation du projet. La difficulté majeure fût de trouver
une structure qui permet de gérer efficacement la notion de pont. C'est en
élaborant l'algorithme que nous avons réussi à déterminer de quelles données
nous aurions besoin et comment les organiser.

Dans un espoir d'améliorer la vitesse d'exécution, nous avons essayé
de paralléliser le processus en utilisant des threads. L'idée est la suivante :
les threads défilent la file de grilles précédemment crées et travaillent à la
création de nouvelles grilles chacun de leur côté. Malheureusement,
l'implémentation de cette parallélisation n'a eu, au mieux, aucun effet,
au pire, a grandement allongé les temps d'exécution. Nous pensons manquer de
maîtrise par rapport aux threads Python, et il nous aurait fallu plus de temps
pour mieux approfondir le sujet.

