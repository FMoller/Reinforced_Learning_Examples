import numpy as np



class card():
    """ Uma Carta do Baralho """
    def __init__(self,valor,naipe):
        self.valor = valor
        self.naipe = naipe #0: Copas, 1: Espadas, 2: Ouros 3: Paus"

    def get_valor(self):
        return self.valor

class mao():
    """ Mão de um jogador """

    def __init__(self):
        self.cartas = []
        self.total = 0

    def update(self):
        self.total= np.sum(list(map(card.get_valor, self.cartas)))
        
        
a = card(10,1)
b = card(1,2)
A = mao()
A.cartas.append(a)
A.cartas.append(b)
A.update()
