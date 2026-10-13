def recup_scores() -> list:
    """
    Récupère les scores dans scores.bin puis les ajoute dans une matrice

    Sortie : 
        - Liste formant une matrice [[pseudo, score],...]
    """
    
    matrice_scores: list
    ligne: tuple
    resultat: list

    matrice_scores = []
    try:
        # Ouverture du fichier en mode lecture
        scores_bin = open("../data/scores.bin", "r")
        for ligne in enumerate(scores_bin):
            # Nettoyage de la ligne et séparation du pseudo et du score
            resultat = ligne[1].strip().split(" ")
            if len(resultat) == 2:
                matrice_scores.append([resultat[0], float(resultat[1])])
        scores_bin.close()
        return matrice_scores
    except FileNotFoundError:
        return None

def afficher_scores() -> None:
    """
    Récupère les scores et les affiche de manière lisible dans la console
    """

    matrice: list
    i: int
    j: int
    n: int
    temp: list

    matrice = recup_scores()

    if matrice is None or len(matrice) == 0:
        print("Aucun score enregistré.")
    else:
        # Tri à bulles pour classer les scores du plus grand au plus petit
        n = len(matrice)
        for i in range(n):
            for j in range(0, n - i - 1):
                if matrice[j][1] < matrice[j + 1][1]:
                    # Échange des éléments si le score suivant est plus grand
                    temp = matrice[j]
                    matrice[j] = matrice[j + 1]
                    matrice[j + 1] = temp

        # Affichage final du classement
        print("--- TABLEAU DES SCORES ---")
        for i in range(len(matrice)):
            print(i + 1, ".", matrice[i][0], ":", round(matrice[i][1]))
        print("--------------------------")
    return None

def ajouter_score(pseudo: str, score: float) -> None:
    """
    Ajoute ou met à jour le score d'un joueur dans la matrice

    Entrée : 
        - Chaine de caractère contenant le pseudo du joueur
        - Nombre décimal contenant le score du joueur
    """

    scores_actu: list
    trouve: bool
    i: int

    try:
        scores_bin = open("../data/scores.bin", "r")
        scores_actu = recup_scores()
        scores_bin.close()

        if scores_actu is None:
            scores_actu = []

        trouve = False
        index = 0
        # Recherche si le joueur existe déjà dans la liste
        while index < len(scores_actu) and trouve != True:
            if scores_actu[index][0] == pseudo:
                trouve = True
                # Mise à jour du score seulement si il est meilleur que l'ancien
                if score > scores_actu[index][1]:
                    scores_actu[index][1] = score
            index += 1
        
        # Si le joueur n'existe pas, on l'ajoute à la matrice
        if not trouve:
            scores_actu.append([pseudo, score])
            
        # Sauvegarde de la matrice mise à jour dans le fichier
        enregistrer_scores(scores_actu)
        return None
    except FileNotFoundError:
        return None
    
def supprimer_score() -> None:
    """
    Réinitialise les scores
    """

    # Écrase le fichier actuel par une liste vide
    enregistrer_scores([])
    return None

def enregistrer_scores(matrice: list) -> None:
    """
    Écrit la matrice entière dans scores.bin

    Entrée:
        - Matrice mise a jour contenant les pseudo et scores
    """

    pseudo: str
    score: float
    entree: list

    try:
        # Ouverture en mode écriture (écrase le contenu précédent)
        with open("../data/scores.bin", "w") as scores_bin:
            for entree in matrice:
                pseudo = entree[0]
                score = entree[1]
                # Écriture du couple pseudo score suivi d'un saut de ligne
                scores_bin.write(f"{pseudo} {score}\n")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des scores : {e}")
    
    return None