# TP Guidé - Kubernetes managé (AKS / EKS / GKE)

## 1. Préparation du cloud
- Choisir un cloud : **Azure (AKS)**, **GCP (GKE)** ou **AWS (EKS)**.
- Créer les ressources préalables :
  - Azure : Resource Group
  - GCP : Projet
  - AWS : Compte actif

---

## 2. Cluster Kubernetes
- Créer un cluster managé :
  - 2 nœuds minimum
  - Version Kubernetes récente par défaut
- Récupérer la configuration `kubeconfig`
- Vérifier l’accès :
  kubectl get nodes
NAME                                        STATUS   ROLES    AGE     VERSION
gke-tp-cluster-default-pool-ae48543d-h065   Ready    <none>   3m28s   v1.33.5-gke.1201000
gke-tp-cluster-default-pool-ae48543d-j5kf   Ready    <none>   3m27s   v1.33.5-gke.1201000
---

## 3. Namespace et objets de configuration
- Créer un namespace :
  kubectl create namespace tp-app
- Créer un ConfigMap dans `tp-app` avec au minimum :
  - APP_MESSAGE (string libre)
  - UPLOAD_ALLOWED_EXT (ex: .txt)
- Créer un Secret dans `tp-app` avec :
  - UPLOAD_PASSWORD (mot de passe attendu pour l’upload)

---

## 4. Application Python
- Créer un dossier `app/`
- Créer un fichier `requirements.txt` avec :
  - Flask ou FastAPI
- Créer `main.py` avec :
  - Lecture des variables d’environnement (APP_MESSAGE, UPLOAD_ALLOWED_EXT, UPLOAD_PASSWORD)
  - Route GET / : lit le contenu de /data et renvoie la liste des fichiers
  - Route POST /upload :
    - attend un champ password
    - attend un fichier à uploader
    - compare password à UPLOAD_PASSWORD
    - si mot de passe OK et extension autorisée → enregistre le fichier dans /data
    - sinon → renvoie une erreur
- Tester l’app en local :
  python main.py
Traceback (most recent call last):
  File "C:\Users\nolan\AppData\Local\Google\Cloud SDK\app\main.py", line 1, in <module>
    from flask import Flask, request, jsonify
ModuleNotFoundError: No module named 'flask'
---

## 5. Conteneurisation et registry
- Créer un Dockerfile :
  - image de base Python officielle
  - copie de requirements.txt
  - installation des dépendances
  - copie de main.py
  - exposition du port (ex: 8000)
  - commande de démarrage
- Builder l’image Docker :
  docker build -t monapp:1.0 .
  [+] Building 31.0s (10/10) FINISHED                                               docker:desktop-linux
 => [internal] load build definition from Dockerfile                                              0.0s
 => => transferring dockerfile: 186B                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.9                                     0.2s
 => [internal] load .dockerignore                                                                 0.0s
 => => transferring context: 2B                                                                   0.0s
 => [1/5] FROM docker.io/library/python:3.9@sha256:da5aee29682d12a6649f51c8d6f15b87deb3e6c524b9  26.4s
 => => resolve docker.io/library/python:3.9@sha256:da5aee29682d12a6649f51c8d6f15b87deb3e6c524b92  0.0s
 => => sha256:c9723aa529b03c40e66d0aee927a410b4719528ab865af6e0bac1b7c9b10829e 20.37MB / 20.37MB  3.7s
 => => sha256:91c91c91f1d23f4edf4280a8fe935f14340fec43a7a3576149a7cffcf70c2f9b 250B / 250B        0.6s
 => => sha256:081ccf923272c30c6072c6ff1617d9072e03ab2a90a431951d325d45e296962b 6.10MB / 6.10MB    2.1s
 => => sha256:79d5bd8a8d262418bf22e705535ce38c6789dc72e319d76b30aafa5c331b6 235.93MB / 235.93MB  23.1s
 => => sha256:26dfe2fac1c486e9aaf41d1028ed30be2c442aa84af44462bc7bac8c148ffb1 67.78MB / 67.78MB  10.5s
 => => sha256:89d573bf42b377ce6a5a0451c15388849686fa4058efd68999f3b014daeb5b55 25.62MB / 25.62MB  3.9s
 => => sha256:795dbedde24d2c72dafd2b71fe36643552e56859c0e29cdb095ed54b825fbaa2 49.28MB / 49.28MB  7.5s
 => => extracting sha256:795dbedde24d2c72dafd2b71fe36643552e56859c0e29cdb095ed54b825fbaa2         0.7s
 => => extracting sha256:89d573bf42b377ce6a5a0451c15388849686fa4058efd68999f3b014daeb5b55         0.3s
 => => extracting sha256:26dfe2fac1c486e9aaf41d1028ed30be2c442aa84af44462bc7bac8c148ffb13         1.0s
 => => extracting sha256:79d5bd8a8d262418bf22e705535ce38c6789dc72e319d76b30aafa5c331b6924         2.7s
 => => extracting sha256:081ccf923272c30c6072c6ff1617d9072e03ab2a90a431951d325d45e296962b         0.1s
 => => extracting sha256:c9723aa529b03c40e66d0aee927a410b4719528ab865af6e0bac1b7c9b10829e         0.3s
 => => extracting sha256:91c91c91f1d23f4edf4280a8fe935f14340fec43a7a3576149a7cffcf70c2f9b         0.0s
 => [internal] load build context                                                                 0.0s
 => => transferring context: 79B                                                                  0.0s
 => [2/5] WORKDIR /app                                                                            0.3s
 => [3/5] COPY requirements.txt .                                                                 0.0s
 => [4/5] RUN pip install -r requirements.txt                                                     3.2s
 => [5/5] COPY main.py .                                                                          0.0s
 => exporting to image                                                                            0.6s
 => => exporting layers                                                                           0.4s
 => => exporting manifest sha256:812ad74be3131172249614cd5d5e920b06a8d9f2a57fd54dfebc44c74ead51c  0.0s
 => => exporting config sha256:4206c06b0729fd130b85f5957696d7071b9959c84da8ec2870b3d8507e273791   0.0s
 => => exporting attestation manifest sha256:ad1adf01e9696e20a10d942dfde97dc94fe189515ef484a56c0  0.0s
 => => exporting manifest list sha256:a6b5709e5c69f65f744b5071a0d2335ebe59959710ad0a22203f1556ad  0.0s
 => => naming to docker.io/library/monapp:1.0                                                     0.0s
 => => unpacking to docker.io/library/monapp:1.0                                                  0.2s

- Tagger l’image pour le registry du cloud :
  docker tag monapp:1.0 <registry>/monapp:1.0
The push refers to repository [gcr.io/420465132868/monapp]
1ccc789abca5: Waiting
081ccf923272: Waiting
26dfe2fac1c4: Waiting
f300da6c2f1a: Waiting
c9723aa529b0: Waiting
3a43f7257796: Waiting
89d573bf42b3: Waiting
79d5bd8a8d26: Waiting
795dbedde24d: Waiting
7614f5e7c329: Waiting
91c91c91f1d2: Waiting
1f6e96a72078: Waiting
unknown: unexpected status from HEAD request to https://gcr.io/v2/420465132868/monapp/blobs/sha256:081ccf923272c30c6072c6ff1617d9072e03ab2a90a431951d325d45e296962b: 412 Precondition Failed
  
- Pousser l’image :
  docker push <registry>/monapp:1.0
The push refers to repository [gcr.io/420465132868/monapp]
1ccc789abca5: Waiting
081ccf923272: Waiting
26dfe2fac1c4: Waiting
f300da6c2f1a: Waiting
c9723aa529b0: Waiting
3a43f7257796: Waiting
89d573bf42b3: Waiting
79d5bd8a8d26: Waiting
795dbedde24d: Waiting
7614f5e7c329: Waiting
91c91c91f1d2: Waiting
1f6e96a72078: Waiting
unknown: unexpected status from HEAD request to https://gcr.io/v2/420465132868/monapp/blobs/sha256:081ccf923272c30c6072c6ff1617d9072e03ab2a90a431951d325d45e296962b: 412 Precondition Failed

---

## 6. Stockage – PVC RWX
- Créer dans `tp-app` un PVC nommé shared-pvc :
  - mode d’accès : ReadWriteMany
  - taille : 1Gi
- Vérifier que le PVC passe en état Bound :
  kubectl get pvc -n tp-app
NAME         STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
tp-pvc-rwx   Pending                                      standard       <unset>                 30m

---

## 7. Déploiement de l’application
- Créer un Deployment dans `tp-app` avec :
  - 2 replicas
  - container utilisant l’image poussée
  - envFrom pour injecter ConfigMap et Secret
  - volume :
    - type : persistentVolumeClaim
    - claimName : shared-pvc
    - monté sur /data
- Appliquer le manifeste :
  kubectl apply -f deployment.yaml
deployment.apps/tp-deployment created
  
- Vérifier que les Pods passent en Running :
  kubectl get pods -n tp-app
NAME                           READY   STATUS    RESTARTS   AGE
tp-deployment-fbd65f68-97z8m   0/1     Pending   0          37s
tp-deployment-fbd65f68-n2t2b   0/1     Pending   0          37s

---

## 8. Exposition de l’application
- Créer un Service de type LoadBalancer dans `tp-app` :
  - cible : Pods du Deployment
  - port externe : 80
  - port cible : 8000
- Appliquer le Service :
  kubectl apply -f service.yaml
service/tp-service created

- Récupérer l’IP publique :
  kubectl get svc -n tp-app

NAME         TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
tp-service   LoadBalancer   34.118.227.129   <pending>     80:30496/TCP   15s

---

## 9. Tests fonctionnels
- GET / :
  curl http://<EXTERNAL-IP>/
  → liste vide au départ
curl: (28) Failed to connect to 34.163.137.121 port 80 after 21051 ms: Could not connect to server

- POST /upload :
  - mauvais password → refusé
  - bon password + extension autorisée → accepté
- GET / après upload :
  curl http://<EXTERNAL-IP>/
  → le fichier apparaît

---

## 10. Tests RWX et stateless
- Vérifier que les 2 Pods sont en Running
- Se connecter en shell sur le premier Pod :
  kubectl exec -it <pod1> -n tp-app -- /bin/sh
  ls /data
Error from server (BadRequest): pod tp-deployment-fbd65f68-n2t2b does not have a host assigned

- Se connecter sur le deuxième Pod :
  kubectl exec -it <pod2> -n tp-app -- /bin/sh
  ls /data
  → mêmes fichiers visibles
- Supprimer un Pod :
  kubectl delete pod <pod1> -n tp-app
- Vérifier :
  - le Service continue de répondre
  - le Pod recréé voit immédiatement les fichiers dans /data

---

## 11. Nettoyage
- Dans `tp-app`, supprimer :
  kubectl delete deployment tp-deployment -n tp-app
  kubectl delete svc tp-service -n tp-app
  kubectl delete pvc shared-pvc -n tp-app
  kubectl delete configmap tp-config -n tp-app
  kubectl delete secret tp-secret -n tp-app
  kubectl delete namespace tp-app
- Dans le cloud, supprimer :
  - le cluster Kubernetes managé
  - le registry utilisé
  - les ressources associées créées uniquement pour le TP (Resource Group, projet, etc.)
