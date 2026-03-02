import operation_melange as melange

# création d'une lettre de la clé
def code_lettre(paquet):

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
def code(paquet, taille_message):

    code = []
    for _ in range(taille_message):
        l = code_lettre(paquet)
        code.append(l)

    return code

