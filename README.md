# TP Kubernetes - Déploiement d'une application Flask avec stockage RWX

## 1. Objectif
Ce TP a pour but de :
- Construire et pousser une image Docker dans Artifact Registry.
- Déployer une application Flask sur GKE.
- Utiliser un **PersistentVolumeClaim RWX** pour partager des fichiers entre plusieurs Pods.
- Exposer l’application via un **Service LoadBalancer**.
- Vérifier le caractère **stateless** de l’application.

---

## 2. Étapes réalisées

### a. Construction et push de l’image
```bash
# Construire l'image
docker build -t monapp:1.0 .

# Taguer pour Artifact Registry
docker tag monapp:1.0 europe-west9-docker.pkg.dev/420465132868/tp-repo/monapp:1.0

# Pousser l'image
docker push europe-west9-docker.pkg.dev/420465132868/tp-repo/monapp:1.0
