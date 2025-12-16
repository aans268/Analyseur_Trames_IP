# Analyseur de Trames IP

## 📋 Description
Analyseur et visualiseur de trafic réseau développé dans le cadre d'une UE Réseaux (L3). Le projet permet de comprendre le fonctionnement du modèle TCP/IP en décodant et visualisant graphiquement les échanges de trames entre deux machines.

**Contexte**: Projet académique - Réseaux informatiques

## 🚀 Technologies
- **Langage**: Python 3
- **Interface graphique**: Tkinter
- **Protocoles supportés**: Ethernet, IPv4, TCP, HTTP

## 📁 Structure
```
Analyseur_Trames_IP/
├── projet.py      # Script principal d'analyse
├── trames.txt     # Fichier exemple de trames
└── howto.txt      # Manuel d'utilisation détaillé
```

## ⚙️ Installation & Usage

### Prérequis
```bash
python3
```

### Lancement
```bash
# Avec le fichier par défaut (trames.txt)
python3 projet.py

# Avec un fichier personnalisé
python3 projet.py <nom_fichier>
```

### Résultat
- **Interface graphique**: Visualisation du trafic avec code couleur par couche OSI
  - 🟠 Orange = Ethernet (couche 2)
  - 🟡 Jaune = IP (couche 3)
  - 🟢 Vert = TCP (couche 4)
  - 🔵 Bleu = HTTP (couche 7)
- **Terminal**: Détails complets de chaque trame (adresses MAC/IP, ports, flags TCP, options, etc.)

## 🎯 Fonctionnalités principales
- Parsing de trames réseau au format hexadécimal
- Décodage multi-couches (Ethernet → IP → TCP → HTTP)
- Visualisation graphique des échanges bidirectionnels
- Affichage détaillé des en-têtes de protocoles
- Support des options IP et TCP
- Extraction et affichage du contenu HTTP

## 📝 Notes
- Le fichier de trames doit se terminer par la ligne `FIN`
- Format d'entrée: hexdump (compatible tcpdump/Wireshark)
- Navigation dans l'interface: utiliser les flèches haut/bas ou la scrollbar
