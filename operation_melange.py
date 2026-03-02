import itertools

def reculeJokerNoir(paquet):
  # Récupérer la position du joker
  ind = list(paquet.keys()).index('J-N')

  if(ind == 54): # Si en dernière position -> passe en 2ème position
    result = inverser(paquet, ind, 1)
  else : # Sinon permuter avec la carte juste derrière lui
    result = inverser(paquet, ind, ind+1)

  return dict(result)

def reculeJokerRouge(paquet) :
  # Récupérer la position du joker
  ind = list(paquet.keys()).index('J-R')

  if(ind == 54) : # Si en dernière position -> passe en 3ème position
    result = inverser(paquet, ind, 2)
  elif(ind == 53): # Si en avant dernière position -> pass en 2ème position
    result = inverser(paquet, ind, 1)
  else : # Sinon permuter avec la carte juste derrière lui
    result = inverser(paquet, ind, ind+2)

  return dict(result)

# inverser le joker noir avec la carte d'après
def inverser(d, ind1, ind2) :
  items = list(d.items())
  items[ind1], items[ind2] = items[ind2], items[ind1]
  return dict(items)

def doubleCoupe(paquet) :
  #récupérer les indices des jokers
  ind1 = list(paquet.keys()).index('J-R')
  ind2 = list(paquet.keys()).index('J-N')

  #récupérer les cartes au-dessus/au-dessous les jokers
  deb = min(ind1, ind2)
  fin = max(ind1, ind2)

  top = dict(itertools.islice(paquet.items(), 0, deb))
  middle = dict(itertools.islice(paquet.items(), deb, fin+1))
  down = dict(itertools.islice(paquet.items(), fin+1, len(paquet)))

  return down | middle | top

def simpleCoupe(paquet):
  n = list(paquet.values())[-1]

  n_cards = dict(itertools.islice(paquet.items(), 0, n))
  reste = dict(itertools.islice(paquet.items(), n, len(paquet)-1))
  last_card = dict(itertools.islice(paquet.items(), len(paquet)-1, len(paquet)))

  return reste | n_cards | last_card

def lecture(paquet):
  # lecture de la première carte
  n = list(paquet.values())[0]

  # lecture de la n+1ème carte et avoir son numéro
  m = list(paquet.values())[n+1]

  # Si c'est un joker on renvoie faux
  return m