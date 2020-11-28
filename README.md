# Hidden-message
La solution va permettre de cacher ou de lire un message dans ou depuis un fichier png. 

> **_NOTE:_**  Version du python de developpement --> python 3.8.5 64-bit


### Structure du project :
Le projet est constitué uniquement de deux modules : **main.py et utilities.py**. Le module #main# contient les instructions nécessaire à l'éxecution et le module **utilities.py** contient les fonctions pour la réalistion des tâches.

### Méthode : 
Pour cacher des messages dans un image PNG, on procède comme suite :
- Ajouter au message la chaine de carcatère de **\#FIN\#** 
- On prend un caractère du message, on le convertit en decimale avec la fonction #ord# de python et on récupère l'octet de poids fort et l'octet de poids faible
- On insère les deux octets dans la matrice à 2 dimensions réprentant de l'image
- On sépare chaque insertion dans la matrice d'un decalage de **600** elements pour amoindrir l'impact visuel .

Maintenant, pour trouver un message depuis une fichier image PNG, on procède comme suite :
- On parcours la matrice en se deplacant toujours de **600** elements
- Pour chaque elements corresondant à notre message, on récupère le l'octet de poids fort et l'octet de poids faible
- On les combine et avec la fontion **chr** de python, on trouve l'equivalent ascii qu'on concatène à une chaine de caractère qui constitue le message lu
- On continue cette procédure jusqu'à retrouver la chaine de caractère **\#FIN\#**.
