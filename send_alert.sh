#!/bin/bash

EVENT_TYPE="$1"
RECIPIENT="chapron.maxime@gmail.com"
SENDER="lephacocheredu44@gmail.com"

# Utilise une structure "case" pour gérer les différents événements
case "$EVENT_TYPE" in
  "login_failure")
    SUBJECT="Alerte de Sécurité: Connexion échouée"
    BODY="Une tentative de connexion a échoué.
Utilisateur: $PAM_USER
Depuis l'IP: $PAM_RHOST
Service: $PAM_SERVICE"
    ;;
  "password_change")
    SUBJECT="Alerte de Sécurité: Mot de passe modifié"
    BODY="Le mot de passe a été changé pour l'utilisateur: $PAM_USER
Service: $PAM_SERVICE"
    ;;
  "reboot")
    SUBJECT="Information: Redémarrage du serveur"
    # Note: les variables PAM ne sont pas disponibles ici
    BODY="Le serveur a redémarré le $(date)"
    ;;
  *)
    # Au cas où le type d'événement est inconnu
    SUBJECT="Alerte Système Inconnue"
    BODY="Un événement non identifié a été déclenché."
    ;;
esac

# Envoi du mail
echo "$BODY" | mail -s "$SUBJECT" -a "From: Serveur Debian <$SENDER>" "$RECIPIENT"
