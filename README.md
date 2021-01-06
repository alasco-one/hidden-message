# Hidden-message
Une application qui permet de cacher ou de lire un message dans ou depuis un fichier png. 

> **_NOTE:_**  Version du python de developpement --> python 3.8.5 64-bit

## Utilisation :
En ayant python3 installé sur sa machine, on peut utiliser l'application de le manière suivante : 
-python3 main.py -w -t "<Un message>" <chemin du fichier PNG>  : Pour cacher **<Un message>** dans le fichier PNG
-python3 main.py -w -f <chemin du fichier texte> <chemin du fichier PNG> : Pour cacher le contenu du fichier texte dans le fichier PNG
-python3 main.py -w <chemin du fichier PNG> : Pour cacher le contenu du fichier texte tapé depuis l'entré standard vers le fichier PNG
-python3 main.py <chemin du fichier PNG> : Pour trouver un message caché dans le fichier PNG


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

### Application :
On va cacher le message contenu dans le fichier suivant dans notre image Png:
![Text](https://github.com/alasco-one/hidden-message/blob/main/img/text.png)

Voici notre fichier png :
![Text](https://github.com/alasco-one/hidden-message/blob/main/img/test.png)

On exécute la commande suivante pour cacher le contenu du fichier test.txt dans le fichier png : 
![Write](https://github.com/alasco-one/hidden-message/blob/main/img/write.png)

On lit message caché en exécutant la commande suivante :
![Write](https://github.com/alasco-one/hidden-message/blob/main/img/read.png)

Et voici l'etat du fichier test.png après l'operation.

![after](https://github.com/alasco-one/hidden-message/blob/main/img/after.png)








