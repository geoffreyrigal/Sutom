import os
import gestion_score as gs
import definition_mot as dm

if __name__ == "__main__":
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def tentativeJoueur(mot_a_deviner: list) -> list:
        """
        Demande à l'utilisateur de saisir sa tentative
        
        Entrée : Liste des lettres formant le mot a deviner
        Sortie : Liste des lettres formant la tentative du joueur
        """

        longeur_mot_a_deviner: int
        tentative_str: str

        print(f"Le mot a deviner commence par la lettre '{mot_a_deviner[0]}'")
        longeur_mot_a_deviner = len(mot_a_deviner) # Attribution de la longeur du mot a deviner pour les verifications
        tentative_str = str(input(f"Quel mot souhaitez vous essayer ({longeur_mot_a_deviner} lettres) ? ")).lower()
        while len(tentative_str) != longeur_mot_a_deviner or tentative_str[0] != mot_a_deviner[0]: # Verifiction de l'entrée selon la longueur et de la 1ere lettre
            print(f"Le mot entré n'est pas correct. Il doit faire {longeur_mot_a_deviner} lettres et commencer par '{mot_a_deviner[0]}'.")
            tentative_str = str(input(f"Quel mot souhaitez vous essayer ({longeur_mot_a_deviner} lettres) ? ")).lower()
        return list(tentative_str)

    class Couleur:
        ROUGE: str
        JAUNE: str
        GRIS: str
        FIN: str
        
        ROUGE = "\033[31m"
        JAUNE = "\033[33m"
        GRIS = "\033[90m"
        FIN = "\033[0m"

    def affichage_resultat_tentative(resultat_tentative: list, tentative: list) -> None:
        """
        Affiche les resultats de la tentative du joureur
        
        Entrée : 
            - Liste indiquant l'état de chaque lettre de la tentative du joueur
            - Liste contenant les lettres de la tentative du joueur
        """

        i: int
        statut: str
        element: list

        for i in range(len(tentative)): # Boucle qui parcours les lettres de la tentative
            statut = resultat_tentative[i] # CORRECTE, MAL_PLACEE, ABSENTE
            if statut == 'CORRECTE':
                tentative[i] = [tentative[i], Couleur.ROUGE] # Colorie en rouge si correct
            elif statut == 'MAL_PLACEE':
                tentative[i] = [tentative[i], Couleur.JAUNE] # Colorie en jaune si mal placé
            else:
                tentative[i] = [tentative[i], Couleur.GRIS] # Colorie en gris si absente
                
        for element in tentative: # Affichage une fois mis en couleur
            print(f"{element[1]}{element[0]}{Couleur.FIN}", end="") # element[1] = couleur, element[0] = lettre, Couleur.FIN = remise du texte en blanc
        print("\n")
        return None
    
    def tour_de_jeu(mot_a_deviner: list, lettres_exact: list, lettres_dans_mot: list, lettres_fausses: list) -> list:
        """
        Gère un tour de jeu:
        1. Demande la tentative du joueur.
        2. Affiche les indices de la tentative.
        3. Vérifie si le joueur a gagné.
        4. Met à jour les listes de lettres (exactes, correctes mais mal placées, fausses).
        
        Entrées: 
            - Liste des lettres formant le mot a deviner
            - Liste des lettres déja bien placées
            - Liste des lettres mal placées
            - Liste des lettres pas dans le mot

        Sortie:
            - Booleen représentant l'état de victoire ou défaite
            - Liste des lettres déja bien placées
            - Liste des lettres mal placées
            - Liste des lettres pas dans le mot
        """

        tentative: list
        resultat_tentative: list
        mot_restant_a_compter: list
        i: int
        lettre: str
        statut: str

        tentative = tentativeJoueur(mot_a_deviner) # Le joueur joue sa tentative
        
        if tentative == mot_a_deviner: # Si le joueur à correctement deviné
            affichage_resultat_tentative(['CORRECTE']*len(mot_a_deviner), mot_a_deviner)
            return [True, lettres_exact, lettres_dans_mot, lettres_fausses]
        
        # Initialisation des structures pour comparer la tentative au mot cible
        resultat_tentative = [''] * len(mot_a_deviner)
        mot_restant_a_compter = list(mot_a_deviner)
        
        # Premier passage : identification des lettres bien placées (CORRECTE)
        for i in range(len(mot_a_deviner)):
            if tentative[i] == mot_a_deviner[i]:
                resultat_tentative[i] = 'CORRECTE' 
                mot_restant_a_compter[i] = None # On retire la lettre pour ne pas la recompter
                
        # Second passage : identification des lettres mal placées ou absentes
        for i in range(len(mot_a_deviner)):
            if resultat_tentative[i] == '': 
                lettre = tentative[i]
                if lettre in mot_restant_a_compter:
                    resultat_tentative[i] = 'MAL_PLACEE' 
                    mot_restant_a_compter[mot_restant_a_compter.index(lettre)] = None 
                else:
                    resultat_tentative[i] = 'ABSENTE'
        
        # Mise à jour des listes de suivi des lettres
        for i in range(len(tentative)):
            lettre = tentative[i]
            statut = resultat_tentative[i]
            
            if statut == 'CORRECTE':
                if lettre not in lettres_exact:
                    lettres_exact.append(lettre)
                if lettre in lettres_dans_mot:
                    lettres_dans_mot.remove(lettre)

            elif statut == 'MAL_PLACEE':
                if lettre not in lettres_exact and lettre not in lettres_dans_mot:
                    lettres_dans_mot.append(lettre)
            
            elif statut == 'ABSENTE':
                if lettre not in lettres_exact and lettre not in lettres_dans_mot and lettre not in lettres_fausses:
                    lettres_fausses.append(lettre)
        
        # Affichage du mot coloré selon les indices trouvés
        affichage_resultat_tentative(resultat_tentative, tentative)

        return [False, lettres_exact, lettres_dans_mot, lettres_fausses]

    def choix_menu() -> int:
        """
        Permet au joueur de choisir son action  
        """
        
        choix:int
        verification:str

        clear_screen()
        print(r"""
   _____ _    _ _______ ____  __  __ 
  / ____| |  | |__   __/ __ \|  \/  |
 | (___ | |  | |  | | | |  | | \  / |
  \___ \| |  | |  | | | |  | | |\/| |
  ____) | |__| |  | | | |__| | |  | |
 |_____/ \____/   |_|  \____/|_|  |_|
    """)
        print("=====================================\n")
        
        # Affichage du menu
        choix = int(input(" 1 - Jouer \n 2 - Afficher les scores \n 3 - Reinitialiser les scores \n 4 - Quitter \n Faites votre choix : "))
        while choix < 1 or choix > 4: # Vérification de l'entrée choix
            print("Le choix n'est pas correct, ")
            choix = int(input(" 1 - Jouer \n 2 - Afficher les scores \n 3 - Reinitialiser les scores \n 4 - Quitter \n Faites votre choix : "))
        match choix: # Gestion du choix de l'utilisateur
            case 1: # Retourne pour continuer dans la fonction jeu()
                return 0
            case 2: # Affiche les scores puis relance cette fonction
                clear_screen()
                gs.afficher_scores()
                input("Appuyez sur n'importe quelle touche pour continuer...")
                return choix_menu()
            case 3: # Supprime les score puis relance cette fonction
                verification = str(input("Veuillez confirmer la réinitialisation des scores actuels en écrivant 'REINITIALISER', autrement les scores seront intouchés : "))
                if verification == "REINITIALISER": # Verifie que les scores ne soient pas effacés par erreur
                    gs.supprimer_score()
                    print("Les scores ont bien été réinitialisés.")
                    input("Appuyez sur n'importe quelle touche pour continuer...")
                    return choix_menu()
                else:
                    print("Les scores n'ont pas été modifés.")
                    input("Appuyez sur n'importe quelle touche pour continuer...")
                    return choix_menu()
            case 4: # Permet de quitter le programme
                clear_screen()
                print("Merci d'avoir joué à notre Sutom !")
                return 1
        return 1

    def jeu() -> None:
        """
        Fonction principale gérant l'initialisation et la logique du jeu
        """

        lettres_exact: list
        lettres_dans_mot: list
        lettres_fausses: list
        nombre_tentatives: int
        pseudo: str
        choix_jeu: int
        niveau: int
        score: float
        lettre_min: int
        lettre_max: int
        mot_a_deviner: list
        str_mot_a_deviner: str
        index: int
        tour: list
        fini: bool
        
        lettres_exact = []
        lettres_dans_mot = []
        lettres_fausses = []
        
        nombre_tentatives = 6

        choix = choix_menu() # Entrée dans le menu
        if choix == 1:
            return None

        # Début du jeu
        clear_screen()
        pseudo = str(input("Quel est le pseudo du joueur ? ")) # Choix du pseudo utilisé dans les scores
        clear_screen()
        choix_jeu = int(input("Souhaitez vous choisir le mot à faire deviner ou obtenir un mot aléatoire ?\n 1 - Choisir, 2 - Aléatoire : ")) # Choix du mode de jeu
        clear_screen()
        niveau = int(input("Souhaitez vous jouer au niveau Facile (entre 2 et 6 lettres), Moyen (entre 7 et 10 lettres), Difficile (entre 11 et 15) ?\n 1 - Facile, 2 - Moyen, 3 - Difficile : ")) # Choix du niveau influant sur les points
        clear_screen()

        match niveau: # Adaptation de la gestion des scores et du jeu en fonction du niveau choisi
            case 1:
                lettre_min = 2
                lettre_max = 6
                score = 10000
            case 2:
                lettre_min = 7
                lettre_max = 10
                score = 30000
            case 3:
                lettre_min = 11
                lettre_max = 15
                score = 50000
            case _:
                raise ValueError("Niveau invalide")
        
        if choix_jeu == 1: # Si l'utilisateur choisi le mot à deviner
            mot_a_deviner = list(dm.choixDuMot(lettre_min, lettre_max)) # list() : garantit une liste de lettres
            clear_screen()
        else: # Si l'utilisateur veut choisir un mot aléatoire
            mot_a_deviner = list(dm.random_mot(lettre_min, lettre_max)) # list() : random_mot renvoie une chaîne
        str_mot_a_deviner = ''.join(mot_a_deviner) # Copie du mot a deviner converti en str

        print(mot_a_deviner)
        
        index = 0
        fini = False
        while index < 6 and fini != True: # Boucle des tours de jeu
            index += 1
            print(f"--- Tentative n°{index} / {nombre_tentatives} ---")
            
            tour = tour_de_jeu(mot_a_deviner, lettres_exact, lettres_dans_mot, lettres_fausses) # Tour de jeu qui renvoie une liste
            if tour[0] == True: # Si le joueur à trouvé le mot exact ==> Victoire
                clear_screen()
                print("---")
                print(f"Bravo, vous avez gagné avec un score de {score}!")
                print(f"Le mot à deviner était : {str_mot_a_deviner}")
                print("---")

                gs.ajouter_score(pseudo, round(score,0)) # Ajoute ou met à jour le score si besoin, correspondant au pseudo dans scores.bin
                fini = True
            elif index == 6: # Si le joueur n'a pas trouvé après n tours (ici 6) ==> Echec
                clear_screen()
                print("---")
                print("Vous n'avez pas deviné dans les temps, perdu !")
                print(f"Le mot à deviner était : {str_mot_a_deviner}")
                print("---")
            else:
                score -= (score * 0.20) # Si le joueur n'a pas trouvé sans perdre la partie, on réduit le score gagnable
        # Fin de la partie

        # Choix de rejouer ou non
        rejouer = str(input("Souhaitez vous refaire une partie ? O/N : ")).upper()
        while rejouer != 'O' and rejouer != 'N':
            print("Le choix n'est pas correct,")
            rejouer = str(input("Souhaitez vous refaire une partie ? O/N : ")).upper()
        if rejouer == 'O': # Si le joueur veut rejouer, on relance la fonction
            jeu()
        else: # Si le joueur veut s'arreter, on retourne pour stopper le programme
            clear_screen()
            print("Merci d'avoir joué à notre Sutom")
            return None

    jeu()