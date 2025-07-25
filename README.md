# Projet ESGI3 – Système Linux Client-Serveur Synchronisé et Sécurisé

## Auteurs
* Binôme : Étudiant 1 & Étudiant 2  
* Année : 2024/2025  
* Enseignant : Dr Zouhour GUIRAS  

---

## 🎯 Objectif

Déployer un environnement Debian client-serveur avec les services suivants :
- Serveur NTP (Chrony)
- Serveur de messagerie (Postfix) avec alertes automatisées
- Sécurité système via PAM
- Interface graphique d’administration (Tkinter)
- Scripts d’automatisation pour supervision et alertes

---

## 📁 Arborescence du projet

.
├── scripts/
│ ├── setup_chrony.sh
│ ├── setup_postfix.sh
│ ├── pam_log_monitor.sh
│ └── send_alert.sh
├── pam/
│ ├── common-auth
│ ├── common-password
│ ├── login
│ └── sshd
├── service/
│ └── reboot-alert.service
├── README.md
└── rapport.pdf

yaml
Copier
Modifier

---

## 🔐 Fichier `secret.env`

Créer le fichier `/root/secret.env` contenant les identifiants du compte Gmail utilisé pour envoyer les alertes :

```env
EMAIL_SENDER=adresse@gmail.com
APP_PASSWORD=motdepasse_application
EMAIL_RECEIVER=destinataire@example.com
Sécuriser ce fichier :

bash
Copier
Modifier
sudo chown root:root /root/secret.env
sudo chmod 600 /root/secret.env
🔧 Service d’alerte au redémarrage
Copier le fichier reboot-alert.service :

bash
Copier
Modifier
sudo cp service/reboot-alert.service /etc/systemd/system/
Sécuriser le fichier :

bash
Copier
Modifier
sudo chown root:root /etc/systemd/system/reboot-alert.service
sudo chmod 600 /etc/systemd/system/reboot-alert.service
Activer le service :

bash
Copier
Modifier
sudo systemctl daemon-reload
sudo systemctl enable reboot-alert.service
Ce service exécute /usr/local/bin/send_alert.sh au redémarrage et utilise les variables d’environnement définies dans /root/secret.env.

🔒 Configuration PAM
Les fichiers suivants doivent être modifiés comme décrit dans le rapport :

/etc/pam.d/common-auth

/etc/pam.d/common-password

/etc/pam.d/login

/etc/pam.d/sshd

Des exemples personnalisés sont fournis dans le dossier pam/.

✅ Modules PAM à utiliser
Notamment :

pam_tally2.so ou pam_faillock.so pour limiter les tentatives de connexion

pam_time.so pour restreindre les connexions à certaines plages horaires

pam_pwquality.so pour appliquer une politique de mot de passe robuste

Attention : ne pas utiliser libpwquality.so — le bon module PAM est pam_pwquality.so
Le paquet libpam-pwquality doit être installé :

bash
Copier
Modifier
sudo apt install libpam-pwquality
🧪 Instructions de test
🕒 Chrony
Sur le serveur : chronyc sources et chronyc tracking

Sur le client : comparer l’heure avant/après synchronisation

📬 Postfix
Redémarrer la machine ou changer un mot de passe

Vérifier la réception d’un mail d’alerte

🔐 PAM
Essayer une connexion en dehors des horaires autorisés

Essayer un mot de passe trop simple

Observer les logs /var/log/auth.log

🖥 Interface graphique (Tkinter)
Depuis la machine client :

bash
Copier
Modifier
ssh -X user@serveur
python3 dashboard.py
🎥 Démo
Une vidéo de démonstration de 5 minutes est fournie pour garantir le bon fonctionnement même en cas de problème lors de la soutenance.

📄 Rapport
Le fichier rapport.pdf contient :

Des explications détaillées

Des captures d’écran

La configuration exacte de chaque service
