#!/bin/bash

# Arrête le script immédiatement si une commande échoue
set -e

# -- Vérification des droits root --
if [ "$(id -u)" -ne 0 ]; then
  echo "Veuillez exécuter ce script avec sudo ou en tant que root." >&2
  exit 1
fi

# --- 1. Installation ---
echo "Installation de Chrony..."
sudo apt-get update
sudo apt-get install -y chrony

# --- 2. Configuration des serveurs NTP ---
echo "Configuration des serveurs NTP dans /etc/chrony/chrony.conf..."
CONF_FILE="/etc/chrony/chrony.conf"

# Commente les lignes "pool" et "server" existantes pour éviter les conflits
sudo sed -i 's/^\(pool\|server\)/#\1/' "$CONF_FILE"

# Ajoute les nouveaux serveurs à la fin du fichier
# Note : on utilise "tee -a" pour écrire dans un fichier avec sudo
echo "
# Serveurs NTP pour la France
server 0.fr.pool.ntp.org iburst
server 1.fr.pool.ntp.org iburst
server 2.fr.pool.ntp.org iburst
server 3.fr.pool.ntp.org iburst
" | sudo tee -a "$CONF_FILE" > /dev/null

# --- 3. Configuration de l'accès local ---
echo "Autorisation du réseau local..."
ALLOW_LINE="allow 192.168.120.0/24"

# Vérifie si la ligne existe déjà avant de l'ajouter
if grep -qFx "$ALLOW_LINE" "$CONF_FILE"; then
    echo "La règle d'autorisation existe déjà."
else
    echo "$ALLOW_LINE" | sudo tee -a "$CONF_FILE" > /dev/null
    echo "Règle d'autorisation ajoutée."
fi

# --- 4. Redémarrage et vérification ---
echo "Redémarrage du service Chrony..."
sudo systemctl restart chrony
# Laisse un peu de temps à Chrony pour se connecter
sleep 20

echo "Vérification du statut de Chrony :"
sudo chronyc tracking
echo "-------------------------------------"
echo "Sources de synchronisation actuelles :"
sudo chronyc sources
echo "Clients connectés au serveur :"
sudo chronyc clients


echo "Configuration de Chrony terminée avec succès !"
