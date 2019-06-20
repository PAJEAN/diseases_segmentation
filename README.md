L'expérimentation se déroule sur un jeu de données maladies/symptômes provenant de la publication "*Human symptoms-disease network, Zhou et al. 2014*". Ce jeu contient initialement 4217 maladies. Dans le cadre de nos expérimentations, nous avons restreint ce jeu de données à 1517 maladies que nous considérons comme étant le corpus. Pour obtenir ce corpus, plusieurs filtres sont employés.
Le premier supprime les symptômes qui ont des descendants plus spécifiques dans la taxonomie. Par exemple, si une première maladie est associée au symptôme *Pain* et une seconde au symptôme *Abdominal Pain* alors, *Pain* est retiré de la liste des symptômes.
Le second vérifie le nombre de co-occurrences entre les symptômes et la maladie, ce nombre doit être strictement supérieur à 1.
Enfin, le troisième filtre considère uniquement les maladies qui ont un seul ascendant dans la branche C du Mesh (C pour Diseases https://meshb.nlm.nih.gov/treeView ) pour se positionner au sein d'une problèmatique multi classes.

L'expérimentation menée au sein de cette étude repose sur la comparaison des distances sur des espaces vectoriels et des mesures de similarité sémantiques.

# Dépendances

* python3.6+ (à cause de la syntaxe print(f"{var}%") sinon remplacer par print(var,"%"))
* numpy
* scipy
* sklearn
* matplotlib

# Auteurs

* Jocelyn Poncelet
* Pierre-Antoine Jean
* François Trousset
* Sebastien Harispe
* Nicolas Pecheur
* Jacky Montmain

# Chaîne expérimentale

* Étape 1: Formater les fichiers queries.tsv (utilisé comme entrées pour la SML) et le fichier résultant de la SML (intitulé ici sml\_results.tsv). Le script formatting.py avec l'option -a permet d'extraire l'ensemble des colonnes issues du fichier sml\_results.tsv. Chaque mesure va créer un fichier dans le dossier *./mesh/pairwise_distances* (*pairwise* pour des "*pairwise*" de maladies).

`python3.6 formatting.py -a`

* Étape 2: Calculer les distances vectorielle (*baseline*) entre les vecteurs de symptômes associés aux maladies. Dans l'article de *Zhou et al. 2014*, les auteurs exploitent la valeur de tf-idf extraite au sein des textes. Pour cela, le script baseline\_compute\_pairwise\_distance.py créer un fichier baseline.json dans le dossier *./pairwise_distances*. Pour utiliser des caractéristiques binaires, l'option -b doit être renseignée et l'option -e pour utiliser la distance euclidienne au lieu de la distance cosinus.

`python3.6 baseline_compute_pairwise_distance.py`

* Étape 3: Réaliser l'étape de partitionnement agglomérative en tenant compte des distances calculées entre les maladies. Le script clustering.py avec l'option -a permet de réaliser le clustering sur chaque fichier au sein du dossier *./pairwise\_distances*. Chaque sortie de cette étape créer un fichier dans le dossier *./clusters*. L'option -n permet de normaliser les vecteurs d'observation ou les matrices de distance.

`python3.6 clustering.py -a`

* Etape 4: Calculer le partitionnement en exploitant la méthode du *K-means*. Le fichier clustering\_kmeans.py permet d'attribuer une classe à l'ensemble des maladies par l'intermédiaire du *K-means* et des valeurs de tf-idf ou des valeurs binaires avec l'option -b. L'option -n permet de normaliser les vecteurs d'observation.

`python3.6 clustering_kmeans.py`

* Étape 5: Évaluer les clusters au travers des mesures: pureté, f1-mesure et rand index. Pour cela utiliser le script evaluation.py avec l'option -a pour calculer les différentes évaluations sur l'ensemble des fichiers au sein du dossier *./clusters*.

`python3.6 evaluation.py -a`
