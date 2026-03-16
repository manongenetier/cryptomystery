import json, os, codage

DOSSIER_PARTAGE = "./partage"


# Méthodes helpers

def paquet_fic(nom):
    return os.path.join(DOSSIER_PARTAGE, f"paquet_{nom}.json")

def msg_fic(nom):
    return os.path.join(DOSSIER_PARTAGE, f"msg_{nom}.json")

def charger_paquet(nom):
    path = paquet_fic(nom)
    if not os.path.exists(path):
        print(f"Paquet introuvable pour '{nom}'.\nLancer d'abord init.py.")
        exit(1)
    with open(path) as f:
        return json.load(f)

def sauvegarder_paquet(nom, paquet):
    with open(paquet_fic(nom), "w") as f:
        json.dump(paquet, f)
    
def charger_messages(nom):
    path = msg_fic(nom)
    if not os.path.exists(path):
        return []

    with open(msg_fic(nom), "r") as f:
        return json.load(f)
        
def sauvgarder_messages(nom, msg):
    with open(msg_fic(nom), "w") as f:
        json.dump(msg, f)
        
        
# lecture des messages reçus
def lire_messages(moi):
    messages = charger_messages(moi)
    nb = len(messages)
    
    if nb == 0:
        print("Aucun nouveu message. YOU CAN REST\n")
        return
    
    paquet = charger_paquet(moi)
    print(f"\nTu as {nb} message(s) en attente : \n")
    print("-"*40+"\n")
    for i, code in enumerate(messages):
        message_decode = codage.dechiffrer(code, paquet)
        print(f"[{i+1}] {message_decode}")
    print("-"*40+"\n")
    
    # sauvegarder la nouvelle version du paquet et vider le fichier de messages
    sauvegarder_paquet(moi, paquet)
    sauvgarder_messages(moi, [])
    

# envoi des messages
def envoyer_message(destinataire, texte):
    paquet = charger_paquet(destinataire)
    code = codage.chiffrer(texte, paquet)
    
    # sauvegarder le paquet avancé + ajouter le message au fichier
    sauvegarder_paquet(destinataire, paquet)
    messages = charger_messages(destinataire)
    messages.append(code)
    sauvgarder_messages(destinataire, messages)
    
    print(f"Message déposé dans le fichier de {destinataire}")
    
def menu(moi, destinataire):
    while True:
        print(f"=== Connecté en tant que : {moi} ===")
        print(f"[1] Lire mes messages")
        print(f"[2] Envoyer un message à {destinataire}")
        print(f"[q] Quitter")    
        choix = input("Choix > ").strip().lower()
        
        if choix == "1" :
            lire_messages(moi)
        elif choix == "2" : 
            texte = input("Message > ").strip()
            if texte:
                  envoyer_message(destinataire, texte)
        elif choix == "q":
            print("Bye Bye !")
            break
        else:
            print("CHOOSE WISELYYYYY\n")
            
            
if __name__ == "__main__":
    print("WELCOME TO YOUR SUPEEERRR SECURE CHAT\n")
    
    moi=input("My Name > ").strip().lower()
    dest=input("Your Partner in crime > ").strip().lower()
    
     # Vérification que les fichiers existent
    if not os.path.exists(paquet_fic(moi)):
        print(f"Utilisateur {moi} inconnu. Lance d'abord init_paquet.py.")
        exit(1)
    if not os.path.exists(paquet_fic(dest)):
        print(f"Destinataire {dest} inconnu. Lance d'abord init_paquet.py.")
        exit(1)

    print(f"\nBonjour {moi} ! Tu communiques avec {dest}.\n")
    menu(moi, dest)
                  