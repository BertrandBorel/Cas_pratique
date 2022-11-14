# Cas pratique

## Objectif :

Application de reconnaissance et de validation d'un uniforme.


## Fonctionnement :
L’utilisateur doit se présenter face caméra. S’il a un gilet et un casque, alors l’application lui indique par message que sa tenue est correcte. Si un des éléments manque, alors l’application affiche le message contraire. 

## Affichage du message : 
Pour permettre d’afficher le message, nous avons choisi de stocker le résultat dans un fichier texte et d’écraser le résultat à chaque nouvelle reconnaissance.
L’application affiche le message indiquant le bon respect (ou non) du port du casque et du gilet à partir du fichier texte. 
