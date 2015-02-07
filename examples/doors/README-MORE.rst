========
README
========

#
# projet Aribo
# Tests pour détection ouverture de porte
# 27/12/12
#

# imu sur table
output00_imu.csv 

imu 'horizontale' sur "le dos" la pile
imu sur l'autre face
imu sur la tranche coté lecteur SD
imu sur la tranche opposée
imu 'verticale' sur la tranche 'ours en l'air'
imu sur la tranche opposée
imu sur la position de départ ('horizontale' sur pile)

# imu sur porte en rotation
output01_imu.csv

porte fermée
ouverture/fermeture entière porte
ouverture/fermeture entière porte moins longtemps
ouverture/fermeture rapide porte
taper sur la porte

# imu sur porte en translation
output02_imu.csv

même procédure qu'au dessus


# visu.m
bleu : X (+ vers le connecteur USB)
vert : Y (+  vers la carte SD)
rouge: Z (+ opposée de la pile)

#
# projet Aribo
# Tests pour détection ouverture de porte
# 18/03/13
#
porte_01.RAW
----------

Test de Gaelle avec le protocole identique mais une orientation différente
sur une porte à Bichat.
Avec l'ancien code, il fallait changer à la main dans les fonctions les
différents seuils d'états des portes (valeurs normes magnétos.)...

Mise à jour du code
--
* Modifications du code pour obtenir sur une fenetre temportelle donnée, la moyenne de la norme (imu_door_mean)
* Utilisation de cette fonction pour calculer automatiquement les seuils pour
imu_door_algo1. -> simplification de l'algo. La detection de mvt et de peak est dans 'doors_trials.py'

En enlevant le signal X, pour le calcul de la norme du magnéto., l'algo fonctionne. Y avait-il une perturbation ?

J'ai fait des tests sur différentes portes en rotation :
---

sur une porte chez moi  (test3)
 * orientation du noeud vertical, antenne vers le haut.
 * choix de l'essai maison00_imu.csv, maison01_imu.csv, maison02_imu.csv
   par la variable id_cfg (0,1,2)
 * protocole similaire à celui décrit en haut

sur une porte au bureau  (test4)
 * même orientation que précédamment
 * differents essai sur port en rotation:
   bureau00.csv (premier essai sans aimant avec 2 ouvertures rapides)
   bureau01.csv (avec faible aimant (style magnet) et protocole standard)
   bureau02.csv (avec aimant plus fort et protocole standard)
 * differents essai sur port en translation :
   bureau03.csv (avec faible aimant (style magnet) et protocole standard)
   bureau04.csv (idem)

 avec les aimants, il y a un effet "pic" mais cela est traitable si on ne
cherche pas à avoir l'état intermédiaire (0.5)
 nickel pour la translation
