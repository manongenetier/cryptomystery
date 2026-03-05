# Il faut d'abord une liste de cartes
import random

cartes = {
    # Pique (1–13)
    "As-P": 1,   "2-P": 2,   "3-P": 3,   "4-P": 4,   "5-P": 5,
    "6-P": 6,   "7-P": 7,   "8-P": 8,   "9-P": 9,   "10-P": 10,
    "Valet-P": 11, "Dame-P": 12, "Roi-P": 13,

    # Coeur (14–26)
    "As-C": 14,  "2-C": 15,  "3-C": 16,  "4-C": 17,  "5-C": 18,
    "6-C": 19,  "7-C": 20,  "8-C": 21,  "9-C": 22,  "10-C": 23,
    "Valet-C": 24, "Dame-C": 25, "Roi-C": 26,

    # Carreau (27–39)
    "As-D": 27,  "2-D": 28,  "3-D": 29,  "4-D": 30,  "5-D": 31,
    "6-D": 32,  "7-D": 33,  "8-D": 34,  "9-D": 35,  "10-D": 36,
    "Valet-D": 37, "Dame-D": 38, "Roi-D": 39,

    # Trèfle (40–52)
    "As-T": 40,  "2-T": 41,  "3-T": 42,  "4-T": 43,  "5-T": 44,
    "6-T": 45,  "7-T": 46,  "8-T": 47,  "9-T": 48,  "10-T": 49,
    "Valet-T": 50, "Dame-T": 51, "Roi-T": 52,

    #Jokers
    "J-N" : 53, "J-R" : 53
}


def initPaquet():
  # Mélange des cartes
  paquet = list(cartes.items())
  random.shuffle(paquet)
  return dict(paquet)

