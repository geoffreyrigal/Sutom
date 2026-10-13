from random import randint

def choixDuMot(lettre_min:int, lettre_max:int) -> list:
    """
    Demande à l'utilisateur de saisir le mot à deviner. 
    
    Entrées : 
        - Entier représentant le minimum de lettres dans le mot
        - Entier représentant le maximum de lettres dans le mot
    
    Sortie : 
        - Liste contenant les lettres du mot à deviner
    """

    mot: str

    # Saisie initiale du mot par l'utilisateur
    mot = str(input(f"Quel sera le mot à deviner (entre {lettre_min} et {lettre_max} lettres) : ")).lower()
    
    # Boucle de vérification de la longueur du mot
    while len(mot) > lettre_max or len(mot) < lettre_min:
        print(f"Le mot doit faire entre {lettre_min} et {lettre_max} lettres.")
        mot = str(input(f"Quel sera le mot à deviner (entre {lettre_min} et {lettre_max} lettres) : ")).lower()
    
    # Conversion de la chaîne en liste de caractères pour le jeu
    return list(mot)

def nbr_lignes_dico() -> int:
    """
    Retourne le nombre de ligne contenues dans le dictionnaire

    Sortie : 
        - Entier représentant le nombre de lignes dans le dictionnaire ou None si le fichier n'est pas trouvé
    """

    nombre_lignes: int
    ligne: str

    nombre_lignes = 0
    try:
        with open('../data/dictionnaire.txt', 'r') as dico:
            # On parcourt chaque ligne pour incrémenter le compteur
            for ligne in dico:
                nombre_lignes += 1
        return nombre_lignes
    except FileNotFoundError:
        return None

def recuperation_mot_aleatoire() -> str:
    """
    Récupère un mot aléatoirement dans le dictionnaire sans utiliser break.
    
    Sortie:
        - chaine de caractère représentant le mot obtenu aléatoirement
    """
    mot_selectionne = "" 
    
    try:
        with open('../data/dictionnaire.txt', 'r', encoding='utf-8') as dico:
            # Chargement de toutes les lignes pour éviter les boucles complexes
            lignes = dico.readlines()
            
            if len(lignes) > 0:
                # Sélection d'un index au hasard dans la liste des lignes
                rdm_nbr = randint(0, len(lignes) - 1)
                mot_selectionne = lignes[rdm_nbr].strip()
            else:
                print("Le fichier est vide.")
                
    except FileNotFoundError:
        print("Erreur : Le fichier dictionnaire.txt n'a pas été trouvé.")

    return mot_selectionne

def random_mot(lettre_min:int, lettre_max:int) -> str:
    """
    Fonction récursive qui s'exécute jusqu'à trouver un mot qui convient aux bornes

    Entrées : 
        - Entier représentant le minimum de lettres dans le mot
        - Entier représentant le maximum de lettres dans le mot
    
    Sortie : 
        - Chaine de caractères représentant le mot
    """

    mot: str

    # On récupère un mot au hasard une première fois
    mot = recuperation_mot_aleatoire()
    
    # Si le mot ne respecte pas les critères, on relance la fonction (récursion)
    while len(mot) < lettre_min or len(mot) > lettre_max:
        mot = random_mot(lettre_min, lettre_max)
    
    return mot