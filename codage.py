import operation_melange as melange

# création d'une lettre de la clé
def lettre_cle(paquet):

    m = 53
    while(m==53) :

        paquet = melange.reculeJokerNoir(paquet)
        paquet = melange.reculeJokerRouge(paquet)
        paquet = melange.doubleCoupe(paquet)
        paquet = melange.simpleCoupe(paquet)

        m = melange.lecture(paquet)

    if m > 26 :
        m = m-26
    
    return m
    
# creation du code de la clé
def code_cle(paquet, taille_message):

    code = []
    for _ in range(taille_message):
        l = lettre_cle(paquet)
        code.append(l)

    return code

# transformer une chaine de caractere en nombres
def str2code(string):
    resultat = []
    for lettre in string.lower():
        if lettre.isalpha():
            resultat.append(ord(lettre) - ord('a') + 1)
    return resultat

# transformer une liste de nombres en chaine de caractere
def code2str(code):
    resultat = ""
    for n in code:
        resultat += chr(n + ord('a') - 1)
    return resultat

#print(str2code("coucou"))    

def chiffrer(string, paquet):
    message = str2code(string)
    cle = code_cle(paquet, len(message))
    for i in range(len(message)) : 
        message[i] = message[i] + cle[i]
    return message

def dechiffrer(string, paquet):
    code = string.copy()
    cle = code_cle(paquet, len(string))
    for i in range(len(string)) : 
        if code[i] > cle[i] : 
            code[i] = code[i] - cle[i]
        else : 
            code[i] = code[i]+26 - cle[i]
    message = code2str(code)
    return message
