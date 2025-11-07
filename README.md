# interfaceModificationsSonore
TP Co_Inter info-physique sur la création d'un equalizer
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Installation :

Ouvrir un GitBash dans ses documents → clique droit, afficher d'autre option, Open Git Bash Here

Cloner le projet :
git clone https://github.com/mmarchive3570/interfaceModificationsSonore.git
cd Github

Installer les dépendences :
pip install numpy scipy sounddevice
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Utilisation :

1) Lancez l’application avec python 00-interfaceEqualizer.py
2) Cliquez sur “Sélectionner un fichier WAV” pour choisir votre fichier audio.
3) Ajustez les sliders pour chaque bande de fréquence.
4) Cliquez sur “Lire avec égaliseur” pour écouter le son traité.

Cliquez sur “Enregistrer le fichier modifié” pour sauvegarder le résultat.
Ou cliquez sur stop pour arrêter la lecture du fichier audio.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Détails techniques :

Filtrage : Utilisation de filtres Butterworth passe-bande via scipy.signal.sosfilt.
Gain : Les valeurs des sliders sont en dB et converties en gain linéaire.
Normalisation : Après traitement, le signal est normalisé pour éviter la saturation.
Stéréo → Mono : Les fichiers stéréo sont convertis en mono pour un traitement uniforme.
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Structure du projet :

Documents
|
Github/
|
interfaceModificationsSonore/
│
├─ 00-interfaceEqualizer.py      # Script principal
├─ README.md               # Documentation
└─ LW_20M_amis.wav       # Fichier de sortie après traitement
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

