LIMITES DU CODE:
FIN nécessaire à la fin du fichier contenant les trames

DETAILS DU FONCTIONNEMENT DU CODE (projet.py):

ouverture du fichier
création interface graphique

étape analyse de trame:
lecture trame
lire les informations concernant ETHERNET et les afficher dans le terminal
afficher les informations les plus pertinentes dans l'interface graphique
si la trame n'est pas de type IP sauter à l'étape finale
lire les informations concernant le datagramme IP et les afficher dans le terminal
afficher les informations les plus pertinentes dans l'interface graphique
si la trame n'est pas un Transmission Control Protocol sauter à l'étape finale
lire les informations concernant TCP et les afficher dans le terminal
afficher les informations les plus pertinentes dans l'interface graphique
si la trame n'est pas HTTP sauter à l'étape finale
lire les informations concernant HTTP et les afficher dans le terminal
afficher les informations les plus pertinentes dans l'interface graphique

étape finale:
si il reste des trames dans le fichier retourner à l'étape d'analyse de trame