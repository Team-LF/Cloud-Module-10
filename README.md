# Cloud-Module-10

TP guidé 
1. Préparation du cloud
  Choisir un cloud : Azure AKS ou GCP GKE ou AWS EKS.
  Créer les ressources préalables :
 Azure  Resource Group.
 GCP  Projet.
 AWS  Compte actif.
 2. Cluster Kubernetes
  Créer un cluster managé :
 2 nœuds minimum.
 Version Kubernetes récente par défaut.
 7
 Module 10  Kubernetes managé  AKS / EKS / GKE
 Récupérer la configuration 
kubeconfig .
  Vérifier lʼaccès avec 
kubectl get nodes .
 3. Namespace et objets de configuration
  Créer un namespace 
tp-app .
  Créer un ConfigMap dans 
tp-app avec au minimum :
 APP_MESSAGE (string libre).
 UPLOAD_ALLOWED_EXT (ex : 
.txt ).
  Créer un Secret dans 
tp-app avec :
 UPLOAD_PASSWORD (mot de passe attendu pour lʼupload).
 4. Application Python
  Créer un dossier 
app/ .
  Créer un fichier 
requirements.txt avec :
 un micro framework HTTP Flask ou FastAPI,
 les libs nécessaires standard (pas de SDK cloud).
  Créer 
main.py avec :
 Lecture des variables dʼenvironnement :
 APP_MESSAGE ,
 UPLOAD_ALLOWED_EXT ,
 UPLOAD_PASSWORD (depuis les env injectées par le Secret).
 Route 
GET / :
 lit le contenu du répertoire 
/data ,
 renvoie la liste des fichiers (au minimum : nom de fichier).
 Route 
POST /upload :
 attend un champ 
password ,
 attend un fichier à uploader,
 compare 
password à 
UPLOAD_PASSWORD ,
 8
 Module 10  Kubernetes managé  AKS / EKS / GKE
/data ,
 si mot de passe OK et extension autorisée → enregistre le fichier 
dans 
sinon → renvoie une erreur.
  Tester lʼapp en local avec un serveur intégré.
 5. Conteneurisation et registry
  Créer un 
Dockerfile :
 image de base Python officielle,
 copie de 
requirements.txt ,
 installation des dépendances,
 copie de 
main.py ,
 exposition du port de lʼapp (ex  8000,
 commande de démarrage de lʼapp.
  Builder lʼimage Docker en local.
  Tagger lʼimage pour le registry du cloud :
 Azure  ACR,
 GCP  Artifact Registry,
 AWS  ECR.
  Pousser lʼimage dans le registry choisi.
 6. Stockage – PVC RWX 
 Créer dans le namespace 
tp-app un PVC nommé 
mode dʼaccès : 
ReadWriteMany ,
 taille  1Gi,
  Vérifier que le PVC passe en état 
Bound
 shared-pvc avec :
 7. Déploiement de lʼapplication
  Créer un Deployment dans le namespace 
tp-app avec :
 9
 Module 10  Kubernetes managé  AKS / EKS / GKE
2 replicas,
 container utilisant lʼimage poussée au registry,
 envFrom ou 
env pour :
 injecter le ConfigMap APP_MESSAGE, UPLOAD_ALLOWED_EXT,
 injecter le Secret UPLOAD_PASSWORD,
 volume :
 type : 
persistentVolumeClaim ,
 claimName: shared-pvc ,
 volumeMounts :
 monter le volume sur 
/data .
  Appliquer le manifeste du Deployment.
  Vérifier que les Pods passent en 
Running .
 8. Exposition de lʼapplication
  Créer un Service de type 
LoadBalancer dans 
cible : les Pods du Deployment,
 port externe  80,
 tp-app :
 port cible : port de lʼapp dans le container (ex  8000.
  Appliquer le Service.
  Récupérer lʼIP publique du Service.
 9. Tests fonctionnels
  Appeler 
GET / sur lʼIP publique :
 vérifier que la liste des fichiers est vide au départ.
  Tester 
POST /upload :
 avec un mauvais 
password → upload refusé,
 avec le bon 
password (valeur du Secret) et une extension autorisée → 
upload accepté.
 10
 Module 10  Kubernetes managé  AKS / EKS / GKE
 Refaire 
GET / :
 vérifier que le fichier apparaît dans la liste.
 10. Tests RWX et stateless
  Vérifier que les 2 Pods du Deployment sont en 
 Se connecter en shell sur le premier Pod :
 lister les fichiers dans 
/data .
  Se connecter sur le deuxième Pod :
 Running .
 vérifier que les mêmes fichiers sont visibles dans 
/data .
  Supprimer un des Pods du Deployment.
  Vérifier :
 le Service continue de répondre via lʼautre Pod,
 le Pod recréé par le Deployment voit immédiatement les fichiers dans 
/data .
 11. Nettoyage
  Dans le namespace 
tp-app , supprimer :
 Deployment,
 Service,
 PVC,
 ConfigMap,
 Secret,
 namespace 
tp-app .
 Dans le cloud, supprimer :
 le cluster Kubernetes managé,
 le registry utilisé,
 les ressources associées créées uniquement pour le TP Resource 
Group, projet, etc.)
