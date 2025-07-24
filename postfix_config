#!/bin/bash

# Arrête le script immédiatement si une commande échoue
set -e

# -- Variables de configuration
GMAIL_USER="lephacocheredu44@gmail.com"
GMAIL_APP_PASS="jdsc odnb chfh ibkj"
RELAY_HOST="[smtp.gmail.com]:587"
MY_HOSTNAME="debian.localdomain"
MY_NETWORKS="127.0.0.0/8 192.168.120.0/24 [::ffff:127.0.0.0]/104 [::1]/128"
MAIL_TEST="chapron.maxime@gmail.com"

# -- Vérification des droits root --
if [ "$(id -u)" -ne 0 ]; then
  echo "Veuillez exécuter ce script avec sudo ou en tant que root." >&2
  exit 1
fi

echo "--- Début de la configuration de Postfix ---"

echo "Installation de Postfix..."

# pour l'installation non-interactive de Postfix
debconf-set-selections <<< "postfix postfix/main_mailer_type select Satellite system"
debconf-set-selections <<< "postfix postfix/mailname string $MY_HOSTNAME"
debconf-set-selections <<< "postfix postfix/relayhost string $RELAY_HOST"

apt-get update
apt-get install -y postfix mailutils

# -- Configuration de main.cf avec postconf --
echo "Configuration des paramètres principaux (main.cf)..."

postconf -e "myhostname = $MY_HOSTNAME"
postconf -e "alias_maps = hash:/etc/aliases"
postconf -e "alias_database = hash:/etc/aliases"
postconf -e "mydestination = \$myhostname, debian, localhost.localdomain, , localhost"
postconf -e "relayhost = $RELAY_HOST"
postconf -e "mynetworks = $MY_NETWORKS"
postconf -e "inet_interfaces = all"
postconf -e "inet_protocols = ipv4"
postconf -e "smtp_sasl_auth_enable = yes"
postconf -e "smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd"
postconf -e "smtp_sasl_security_options = noanonymous"
postconf -e "smtp_use_tls = yes"
postconf -e "smtp_tls_CApath = /etc/ssl/certs"


# -- Création du fichier de mot de passe SASL --
echo "Création du fichier de mot de passe SASL..."
SASL_PASSWD_FILE="/etc/postfix/sasl_passwd"
echo "$RELAY_HOST    $GMAIL_USER:$GMAIL_APP_PASS" > "$SASL_PASSWD_FILE"

# Sécurisation du fichier de mot de passe
chmod 600 "$SASL_PASSWD_FILE"

# Création de la base de données de lookup pour Postfix
postmap "$SASL_PASSWD_FILE"

# -- Redémarrage de Postfix --
echo "Redémarrage de Postfix pour appliquer toutes les configurations..."
systemctl restart postfix

echo "Configuration de Postfix terminée avec succès !"
echo "Email de test envoyé"
echo "Ceci est un test" | mail -s "Test Postfix" "$MAIL_TEST"
