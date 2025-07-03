# Workflow Git pour le projet : Prédiction du prix au m² en immobilier en France

## Objectif
Organiser le travail de développement pour garder une branche `main` toujours propre, intégrer les nouveautés sur `dev` et développer chaque fonctionnalité sur des branches dédiées, idéalement liées à des tickets Jira.

---

## 1. Branches principales

- **main** : version stable/production, jamais de dev direct dessus.
- **dev** : branche d’intégration, reçoit toutes les features avant passage sur main.

---

## 2. Création et utilisation des branches

### A. Initialisation

```bash
git checkout main
git pull origin main
git checkout -b dev
git push origin dev
```

---

### B. Travailler sur une fonctionnalité (feature)

1. **Créer un ticket Jira pour la tâche à réaliser**  
   (ex : JIRA-001 Nettoyage des données)

2. **Créer une branche de fonctionnalité depuis dev :**

```bash
git checkout dev
git pull origin dev
git checkout -b feat/JIRA-001-nettoyage-donnees
git push origin feat/JIRA-001-nettoyage-donnees
```

3. **Développer sur la branche feature**  
   Commits réguliers avec messages incluant l’ID Jira.

```bash
git add .
git commit -m "[JIRA-001] Nettoyage des données"
git push origin feat/JIRA-001-nettoyage-donnees
```

4. **Fusionner la feature dans dev une fois terminée :**

```bash
git checkout dev
git pull origin dev
git merge feat/JIRA-001-nettoyage-donnees
git push origin dev
```

5. **(Optionnel) Supprimer la branche feature après merge :**

```bash
git branch -d feat/JIRA-001-nettoyage-donnees
git push origin --delete feat/JIRA-001-nettoyage-donnees
```

---

### C. Intégrer une version stable sur main

Quand plusieurs features sont prêtes et testées sur dev :

```bash
git checkout main
git pull origin main
git merge dev
git push origin main
```

---

## 3. Résumé schématique

```text
main  <--- version stable
  ^
  |
dev   <--- intégration / tests
  ^     ^     ^
  |     |     |
feat/JIRA-001-nettoyage-donnees
feat/JIRA-002-analyse-exploratoire
feat/JIRA-003-feature-engineering
```

---

## 4. Conseils

- Toujours partir de `dev` pour créer une branche de fonctionnalité.
- Toujours fusionner une feature sur `dev` avant de la supprimer.
- Ne jamais travailler directement sur `main`.
- Inclure l’ID Jira dans les noms de branches et les messages de commit.
- Pousser régulièrement sur le dépôt distant (`git push origin ...`).
- Utiliser Jira pour suivre l’avancement des tâches.

---

## 5. Liens utiles

- Documentation Git : https://git-scm.com/doc
- Documentation Jira : https://support.atlassian.com/jira-software-cloud/
