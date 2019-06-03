L'expérimentation se déroule sur un jeu de données maladies/symptômes provenant de la publication "Human symptoms-disease network, Zhou et al. 2014". Ce jeu contient initialement 4217 maladies. Cependant, nous exploitons 1755 d'entre elles pour le corpus 1 et 1005 pour le corpus 2. Pour le corpus 1 deux filtres sont employés. Le premier filtre les symptômes sur le nombre de co-occurrences avec la maladie, ce nombre doit être strictement supérieur à 1. Le second filtre considère uniquement les maladies qui ont un seul ascendant dans la branche C du Mesh (C pour Diseases "https://meshb.nlm.nih.gov/treeView"), ainsi nous nous situons au sein d'un problème multi classes mais mono label. Pour le corpus 2, les mêmes filtres sont conservés mais nous limitons le nombre de symptômes par maladie dans l'intervalle 5 à 50.

L'expérimentation menée au sein de cette étude repose sur la comparaison des distances vectorielles employées dans l'article et des distances sémantiques.

# Dépendances

* python3.6+ (à cause de la syntaxe print(f"{var}%") sinon remplacer par print(var,"%"))
* numpy
* scipy
* sklearn
* matplotlib

# Chaîne expérimentale

* Étape 1: Formater les fichiers queries.tsv (utilisé comme entrées pour la SML) et le fichier résultant de la SML (intitulé ici sml_results.tsv). Le script formatting.py avec l'option -a permet d'extraire l'ensemble des colonnes issues du fichier sml_results.tsv. Chaque mesure va créer un fichier dans le dossier mesh/pairwise_distances (pairwise pour des "pairwise" de maladies).

`python3.6 formatting.py -a`

* Étape 2: Calculer les distances vectorielle (baseline) entre les vecteurs de symptômes associés aux maladies. Dans l'article, ils exploitent la valeur de tf-idf extraite au sein des textes. Pour cela, le script baseline_compute_pairwise_distance.py créer un fichier baseline.json dans le dossier ./pairwise_distances. Pour utiliser des caractéristiques binaires, l'option -b doit être renseignée et l'option -e pour utiliser la distance euclidienne au lieu de la distance cosinus.

`python3.6 baseline_compute_pairwise_distance.py`

* Étape 3: Réaliser l'étape de partitionnement agglomérative en tenant compte des distances calculées entre les maladies. Le script clustering.py avec l'option -a permet de réaliser le clustering sur chaque fichier au sein du dossier pairwise_distances. Chaque sortie de cette étape créer un fichier dans le dossier ./clusters.

`python3.6 clustering.py -a`

* Étape 4: Évaluer les clusters au travers des mesures: pureté, f1-mesure et rand index. Pour cela utiliser le script evaluation.py avec l'option -a pour calculer les différentes évaluations sur l'ensemble des fichiers au sein du dossier ./clusters.

`python3.6 evaluation.py -a`
