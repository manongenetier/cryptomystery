from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import codage
import random

app = FastAPI(title="CryptoAPI")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173", "http://localhost:3000"],
  allow_credentials =True,
  allow_methods=["*"],
  allow_headers=["*"]
)

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
    "J-N" : 53, "J-R" :  53
}

# methodes pydantics Request/ Resp 
class Carte(BaseModel):
    carte: str
    valeur: int

class EtatPaquet(BaseModel):
  cartes: List[Carte]
  
class CodageRequest(BaseModel):
  message: str
  paquet: List[Carte]
  
class CodageResponse(BaseModel):
  result: List[int]
  message_a_afficher: str
  etat_paquet: List[Carte]
  
class DecodageRequest(BaseModel):
  code: List[int]
  paquet: List[Carte]
  
class DecodageResponse(BaseModel):
  decode: str
  etat_paquet: List[Carte]
  
# fonctions helpers
def dict_to_json(paquet):
  return [{"carte": k, "valeur": v} for k, v in paquet.items()]

def json_to_dict(paquet):
  return {item.carte: item.valeur for item in paquet}
  
def initPaquet():
  # Mélange des cartes
  paquet = list(CARTES.items())
  random.shuffle(paquet)
  return dict(paquet)

@app.get("/")
async def root():
  return {
    "message": "Crypto Mystery API",
    "endpoints": {
      "/init" :"GET - Initialisation",
      "/coder": "POST - Coder le message",
      "/decoder" : "POST - Decoder un message"
    }
  }
  
@app.get("/init", response_model=EtatPaquet)
async def init_paquet():
    paquet = initPaquet()
    return EtatPaquet(cartes=dict_to_json(paquet))
  
@app.post("/coder", response_model=CodageResponse)
async def coder_message(request: CodageRequest):
  try:
    paquet = json_to_dict(request.paquet)
    chiffrage, new_paquet = codage.chiffrer(request.message, paquet)
   
    return CodageResponse(
      result=chiffrage,
      message_a_afficher="Message affiché avec succès",
      etat_paquet=dict_to_json(new_paquet)
    )
  except Exception as e:
    print(f"ERREUR CODAGE: {e}")
    raise HTTPException(status_code=400, detail=str(e))

@app.post("/decoder", response_model=DecodageResponse)
async def decoder_message(request: DecodageRequest):
  try:
    paquet = json_to_dict(request.paquet)
    text_decrypte, new_paquet = codage.dechiffrer(request.code, paquet)
    
    return DecodageResponse(
      decode=text_decrypte,
      etat_paquet=dict_to_json(new_paquet)
    )
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
  

'''
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
'''
