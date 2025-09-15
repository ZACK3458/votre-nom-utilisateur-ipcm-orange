# Agent Motivationnel GitHub 🚀

Un système automatisé qui analyse les événements GitHub et envoie des messages de motivation pour encourager le travail d'équipe et maintenir la motivation des développeurs.

## Fonctionnalités

✨ **Analyse automatique des événements GitHub**
- Détection des commits (push)
- Suivi des pull requests (ouverture, fusion, fermeture)
- Monitoring des reviews de code

🎯 **Messages de motivation personnalisés**
- Messages aléatoires en français
- Différents types de messages selon l'événement
- Emojis et formatage attractif

📢 **Notifications multi-canaux**
- Slack (via webhook)
- Email (configurable)
- Extensible pour d'autres services

## Configuration

### 1. Secrets GitHub à configurer

Dans votre repository GitHub, ajoutez les secrets suivants dans `Settings > Secrets and variables > Actions`:

```
SLACK_WEBHOOK_URL: https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

### 2. Configuration Slack

1. Créez une application Slack ou utilisez une existante
2. Activez les Incoming Webhooks
3. Créez un webhook pour votre canal souhaité
4. Copiez l'URL du webhook dans les secrets GitHub

## Types de messages

### Commits (Push)
- "Excellent travail sur ce commit ! 🚀 Continue comme ça, tu es sur la bonne voie !"
- "Superbe commit ! 💪 Chaque ligne de code nous rapproche du succès !"
- "Bravo pour ce push ! 🎉 Ta détermination porte ses fruits !"

### Pull Requests ouvertes
- "Excellente PR ! 🎯 Ta contribution va faire la différence !"
- "Superbe pull request ! 🔥 L'équipe va adorer ton travail !"

### Pull Requests fusionnées
- "Pull request fusionnée ! 🎉 Allez, passe à la prochaine fonctionnalité !"
- "Merge réussi ! 🚀 Ton code est maintenant en production, félicitations !"

### Reviews de code
- "Merci pour cette review ! 👀 Ton œil expert améliore la qualité du code !"
- "Excellente review ! 🔍 Tes commentaires sont toujours constructifs !"

## Personnalisation

Vous pouvez personnaliser les messages en modifiant le fichier `.github/config/motivational-config.json`.

### Structure de configuration

```json
{
  "motivationalMessages": {
    "push": ["message1", "message2", ...],
    "pullRequestOpened": ["message1", "message2", ...],
    "pullRequestMerged": ["message1", "message2", ...],
    "pullRequestClosed": ["message1", "message2", ...],
    "review": ["message1", "message2", ...]
  },
  "settings": {
    "enabledEvents": ["push", "pull_request", "pull_request_review"],
    "enabledBranches": ["main", "master", "develop"]
  }
}
```

## Comment ça marche

1. **Déclenchement** : Le workflow GitHub Actions se déclenche sur les événements configurés
2. **Analyse** : Le script Node.js analyse le type d'événement et sélectionne un message approprié
3. **Génération** : Un message motivationnel aléatoire est choisi dans la catégorie correspondante
4. **Envoi** : Le message est envoyé via Slack (et/ou email si configuré)

## Exemples de notifications Slack

```
🚀 Agent Motivationnel

Excellent travail sur ce commit ! 🚀 Continue comme ça, tu es sur la bonne voie !

👤 john-doe | 📁 mon-projet | 🌿 feature/nouvelle-fonctionnalite
```

## Développement

### Test local

```bash
# Simuler un événement de commit
export GITHUB_EVENT_NAME=push
export GITHUB_ACTOR=test-user
export GITHUB_REPOSITORY=test/repo
export GITHUB_REF=refs/heads/main
export COMMIT_MESSAGE="Add new feature"

node .github/scripts/motivational-agent.js
```

### Ajout de nouveaux types d'événements

1. Modifiez le workflow `.github/workflows/motivational-messages.yml`
2. Ajoutez la logique dans `.github/scripts/motivational-agent.js`
3. Configurez les messages dans `.github/config/motivational-config.json`

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à proposer de nouveaux messages motivationnels ou des améliorations du système.

## Licence

Ce projet est sous licence MIT.