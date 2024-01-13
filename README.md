# Projet 09 - LITRevu

<div align="center">
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/Nantosuelte88/Projet-09/blob/main/media/logoblanc.png">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/Nantosuelte88/Projet-09/blob/main/media/logo.png">
  <img alt="Logo de JustStreamIt" src="https://github.com/Nantosuelte88/Projet-09/blob/main/media/logoblanc.png">
</div>
<p align="center">
    “Découvrez grâce à LITRevu une expérience de critique littéraire interactive, <br>où partager et demander des avis sur des livres devient simple et captivant.”
</p>

## Pour commencer

Ce projet est créé dans le cadre de la formation de Développeur d'application Python proposée par [OpenClassrooms](https://openclassrooms.com/fr/).

### Le projet

Il est demandé de créer une application web MVP permettant de demander ou de publier des critiques de livres ou d'articles. 

### Les exigences :
  + Utiliser le framework Django.
  + Utiliser SQLite comme base de données locale.
  + Offrir une conception de base de données correspondant au schéma fourni.
  + Avoir une interface utilisateur correspondant à celle des wireframes dans son architecture, le design restant assez libre.
  + Avoir une interface utilisateur propre et minimale.
  + Suivre les bonnes pratiques d’accessibilité du référentiel WCAG
  + Respecter les directives de la PEP8.

### Prérequis

Vous devez avoir Django installé, en amont vous trouverez de plus amples informations concernant Django sur [ce lien](https://www.djangoproject.com/) ou [GitHub de Django](https://github.com/django/django).

> [!IMPORTANT]
> Nécessite une version de Python supérieure à 3


## Installation

D'abord, clonez le projet : 
```
$ git clone https://github.com/Nantosuelte88/Projet-09.git
```


Pour créer l'environnement :
```
$ python -m venv env
```

Pour l'activer sur Unix et MacOS :
```
$ source env/bin/activate
```

Pour l'activer sur Windows (Pas de ".bat" sous Powershell) :
```
$ env\Scripts\activate.bat
```

Installez les dépendances :
```
$ pip install -r requirements.txt
```

Appliquez les migrations :
```
$ python manage.py migrate
```

Lancez le serveur
```
$ python manage.py runserver
```

Vous devriez voir un message indiquant que le serveur tourne.


## Le site

Ouvrez votre navigateur et allez à [http://127.0.0.1:8000/](http://127.0.0.1:8000/) pour voir votre application en action.

<p align="center">
  <img alt="Démo du site LITRevu" src="https://github.com/Nantosuelte88/Projet-09/blob/main/media/site001.png">
  <em>Démo du site LITRevu</em>
</p>

Vous pourrez alors créer un compte ou vous connecter avec les identifiants fournis.

### Les catégories

**Points Forts du Site :**
- Accès facile aux tickets et reviews des utilisateurs que vous suivez, depuis la page Flux.
- Affichage clair de tous vos posts sur la page Posts.
- Voir et gérer qui vous suivez, qui vous suit et qui vous a bloqué depuis la page d'abonnement.


<p align="center">
  <img alt="Page d'abonnement du site LITRevu" src="https://github.com/Nantosuelte88/Projet-09/blob/main/media/site003.png">
  <em>Page d'abonnement du site LITRevu</em>
</p>



### Fonctionnalités

## Fonctionnalités du Flux

Depuis la page Flux de LITRevu, vous avez accès à plusieurs fonctionnalités puissantes pour faciliter votre expérience de critique littéraire :

1. **Demander une Critique :**
   - Vous pouvez solliciter des critiques sur des livres et des articles en cours de lecture.
   - Interagissez avec la communauté en demandant des opinions ou des recommandations.

2. **Créer une Critique :**
   - Créez une critique complète en un seul passage, en initiant une demande de critique et en partageant votre propre critique.
   - Simplifiez le processus en partageant vos réflexions pendant que vous demandez des critiques.

3. **Répondre à une Demande :**
   - Soyez un membre actif de la communauté en répondant aux demandes de critique d'utilisateurs que vous suivez.
   - Participez aux discussions et partagez vos connaissances littéraires.

4. **Modifier ou Supprimer vos Contributions :**
   - Ajustez vos demandes de critiques ou vos critiques existantes en fonction de l'évolution de votre expérience de lecture.
   - Supprimez des contributions si nécessaire pour maintenir votre profil à jour.

En tirant parti de ces fonctionnalités, LITRevu offre une plateforme interactive où les amateurs de livres peuvent se connecter, partager leurs pensées et découvrir de nouvelles œuvres à explorer. Profitez de ces outils pour créer une communauté littéraire dynamique.

<p align="center">
  <img alt="Exemple d'une demande de critique sur le site LITRevu" src="https://github.com/Nantosuelte88/Projet-09/blob/main/media/site002.png">
  <em>Page d'abonnement du site LITRevu</em>
</p>


## Langages Utilisés

* Python - framework Django
* HTML 5
* CSS 3 

  
> README rédigé à l'aide de :
> - [Docs GitHub](https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
> - [Template by PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
> - [Align items by DavidWells](https://gist.github.com/DavidWells/7d2e0e1bc78f4ac59a123ddf8b74932d)
