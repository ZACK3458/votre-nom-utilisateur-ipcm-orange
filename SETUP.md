# Configuration rapide de l'Agent Motivationnel

## 1. Création du webhook Slack

1. Allez sur https://api.slack.com/apps
2. Créez une nouvelle app ou sélectionnez une existante
3. Dans "Features > Incoming Webhooks", activez les webhooks
4. Cliquez sur "Add New Webhook to Workspace"
5. Sélectionnez le canal où vous voulez recevoir les messages
6. Copiez l'URL du webhook (ex: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX)

## 2. Configuration des secrets GitHub

1. Allez dans votre repository GitHub
2. Settings > Secrets and variables > Actions
3. Cliquez sur "New repository secret"
4. Nom: `SLACK_WEBHOOK_URL`
5. Valeur: L'URL copiée à l'étape 1

## 3. Test de fonctionnement

Une fois configuré, l'agent se déclenchera automatiquement sur:
- Les commits (push) sur main, master, ou develop
- L'ouverture de pull requests
- La fusion de pull requests
- Les reviews de code

## 4. Messages d'exemple

### Commit
> 🚀 Agent Motivationnel
> 
> **Excellent travail sur ce commit ! 🚀 Continue comme ça, tu es sur la bonne voie !**
> 
> 👤 john-doe | 📁 mon-projet | 🌿 main

### Pull Request fusionnée
> 🎉 Agent Motivationnel
> 
> **Pull request fusionnée ! 🎉 Allez, passe à la prochaine fonctionnalité !**
> 
> 👤 jane-dev | 📁 mon-projet | 🌿 feature/nouvelle-api

## 5. Personnalisation

Modifiez le fichier `.github/config/motivational-config.json` pour:
- Ajouter vos propres messages
- Configurer les événements déclencheurs
- Personnaliser les branches surveillées

## 6. Test local

```bash
# Installer les dépendances (aucune pour le moment)
npm install

# Tester l'agent
npm test

# Ou directement:
node .github/scripts/test-motivational-agent.js
```