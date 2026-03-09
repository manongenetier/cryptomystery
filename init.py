# Il faut d'abord une liste de cartes
import random, json, os

DOSSIER_PARTAGE = "./partage"
CARTES = {
    # Trèfles (1–13)
    "As-T": 1,   "2-T": 2,   "3-T": 3,   "4-T": 4,   "5-T": 5,
    "6-T": 6,   "7-T": 7,   "8-T": 8,   "9-T": 9,   "10-T": 10,
    "Valet-T": 11, "Dame-T": 12, "Roi-T": 13,

    # Carreau (14–26)
    "As-D": 14,  "2-D": 15,  "3-D": 16,  "4-D": 17,  "5-D": 18,
    "6-D": 19,  "7-D": 20,  "8-D": 21,  "9-D": 22,  "10-D": 23,
    "Valet-D": 24, "Dame-D": 25, "Roi-D": 26,

    # Coeurs (27–39)
    "As-C": 27,  "2-C": 28,  "3-C": 29,  "4-C": 30,  "5-C": 31,
    "6-C": 32,  "7-C": 33,  "8-C": 34,  "9-C": 35,  "10-C": 36,
    "Valet-C": 37, "Dame-C": 38, "Roi-C": 39,

    # Piques (40–52)
    "As-P": 40,  "2-P": 41,  "3-P": 42,  "4-P": 43,  "5-P": 44,
    "6-P": 45,  "7-P": 46,  "8-P": 47,  "9-P": 48,  "10-P": 49,
    "Valet-P": 50, "Dame-P": 51, "Roi-P": 52,

    #Jokers
    "J-N" : 53, "J-R" : 53
}


def initPaquet():
  # Mélange des cartes
  paquet = list(CARTES.items())
  random.shuffle(paquet)
  return dict(paquet)


def init(spies):
    os.makedirs(DOSSIER_PARTAGE, exist_ok=True)
    
    paquet = initPaquet()
    
    for nom in spies:
        nom = nom.strip().lower()
        # fichier qui stock le paquet partagé (une fois)
        paquet_fic = os.path.join(DOSSIER_PARTAGE, f"paquet_{nom}.json")
        # fichier qui stock les messages reçus
        msg_fic = os.path.join(DOSSIER_PARTAGE, f"msg_{nom}.json")
        
        if os.path.exists(paquet_fic):
            print(f"Paquet pour ~{nom}~ existe déjà, NEXT")
        else: 
            with open(paquet_fic, "w") as f:
                json.dump(paquet, f, indent=2)
            print(f"paquet créé pour ~{nom}~")
        if not os.path.exists(msg_fic):
            with open(msg_fic, "w") as f:
                json.dump([], f)
                
    print(f"\n Dossier partagé prêt dans {DOSSIER_PARTAGE}/")
    print("IMPORTANT : Copier le dossier à tous les participant une seule fois")

if __name__ == "__main__" :
    print("Initialisation du système de messagerie Solitaire\n")
    noms = input("Noms des spies (séparés par une virgule) > ").split(",")
    init(noms)
            
