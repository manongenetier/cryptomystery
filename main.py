import codage
import random

cartes = {
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
    "J-N" : 53, "J-R" :  53
}

def initPaquet():
  # Mélange des cartes
  paquet = list(cartes.items())
  random.shuffle(paquet)
  return dict(paquet)

# les deux paquets doivent être au même état
paquet1 = initPaquet()
paquet2 = paquet1.copy()


message = "coucou"
print("message à coder :", message)

code = codage.chiffrer(message,paquet1)
print("code envoyé : ", code)

message_dechiffre = codage.dechiffrer(code,paquet2)
print("message déchiffré :", message_dechiffre)


message = "bahdja et manon les stars ting ting ting"
print("\nmessage à coder :", message)

code = codage.chiffrer(message,paquet1)
print("code envoyé : ", code)

message_dechiffre = codage.dechiffrer(code,paquet2)
print("message déchiffré :", message_dechiffre)


message = "Ce message n'est pas ChiFfré"
print("\nmessage à coder : ",message)

code = codage.chiffrer(message, paquet1)
print("code envoyé : ", code)

message_decode = codage.dechiffrer(code, paquet2)
print("message decodé : ", message_decode)