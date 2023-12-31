# IdFm-stalker
Ile de France Mobilité - Récupération des informations de l'API Open Data

## Prérequis
- Python 3.6 ou supérieur
- pip

## Installation
- Cloner le projet
- Installer les dépendances avec la commande `pip install -r requirements.txt`

## Utilisation
- Lancer le script `python main.py`
- Le script va créer un fichier `lines.json` avec la liste des lignes de métro (tram et RER à ajouter plus tard)
- Le script va créer un fichier `disruptions.json` avec la liste des perturbations sur les lignes de métro (tram et RER à ajouter plus tard)
- Lancer le conteneur docker en fond :
    - `docker build -t idfm-stalker .`
    - `docker run -d --rm --network elastic-cluster_default --name idfm-stalker idfm-stalker`

## Lancer l'agent Filebeat
- Se connecter au conteneur docker
    - `docker exec -it idfm-stalker bash`
- Lancer l'agent Filebeat
    - `cd /etc/filebeat`
    - `./filebeat -e -c ./filebeat.yml`

## TODO
- [x] Récupérer la liste des lignes de métro
- [x] Récupérer la liste des perturbations sur les lignes de métro
- [ ] Dockeriser le projet pour le lancer en tâche de fond
- [ ] Ajouter les lignes de tram et RER
- [ ] Ajouter les perturbations sur les lignes de tram et RER
- [ ] Ajouter les horaires des prochains passages sur certaines stations