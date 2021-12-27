import numpy as np

naipes = [(0,'C','\u2665'),
          (1,'E','\u2660'),
          (2,'O','\u2666'),
          (3,'P','\u2663')
          ]
simb_valores = {1:"A",
                11:"J",
                12:"Q",
                13:"K"}

class baralho():
    def __init__(self):
        self.cartas = []
        for i in range(4):
            for j in range(1,14):
                self.cartas.append(card(j,i))
        np.random.shuffle(self.cartas)

    def comprar(self):
        return self.cartas.pop()

    def len(self):
        return len(self.cartas)

    def reset(self):
        self.cartas = []
        for i in range(4):
            for j in range(1,14):
                self.cartas.append(card(j,i))
        np.random.shuffle(self.cartas)
        
                

class card():
    """ Uma Carta do Baralho """
    
    def __init__(self,valor,naipe):
        self.valor = valor
        self.naipe = naipe #0: Copas, 1: Espadas, 2: Ouros 3: Paus"

    def get_valor(self):
        return self.valor

    def get_naipe(self):
        return naipes[self.naipe]

class mao():
    """ Mão de um jogador """

    def __init__(self):
        self.cartas = []
        self.total = 0

    def update(self):
        self.total= np.sum(list(map(card.get_valor, self.cartas)))

    def add_card(self,card):
        self.cartas.append(card)

    def get_total(self):
        self.update()
        return self.total

    def print(self):
        pmao = ""
        for i in self.cartas:
            valor = i.get_valor()
            if valor in simb_valores.keys():
                valor = simb_valores[valor]
            else:
                valor = str(valor)
            pmao += valor+i.get_naipe()[2]+" "
        print(pmao)
        
        
class player():
    """ Jogador """

    def __init__(self, baralho, oponente=None, epsilon = 0.1, rltw = None, rltl = None, rltwq = None, rltlq = None, tipo = 0, utipo = 0):

        self.mao = mao()
        self.tipo = tipo #0: para de comprar com 14 ou mais, 1: Greedy, 2: RL, 3: Humano
        self.utipo = utipo #0: Olha apenas para a própria mão, #1: Olha apenas para vitórias e derrotas, 2: Olha ambos
        self.resultados = {'v':0,'e':0,'d':0}     
        self.baralho = baralho
        self.epsilon = epsilon
        self.oponente = oponente
        self.tracking = []
        self.rltw = rltw
        self.rltl = rltl
        self.rltwq = rltwq
        self.rltlq = rltlq
        self.last_mv = 0 #0 passou, 1 comprou
        self.last_t = 0

    def f_compra(self):
        nova_carta = self.baralho.comprar()
        self.mao.add_card(nova_carta)
        

    def tomar_dec(self):
        if self.tipo == 0:
            self.dec_14()
        elif self.tipo == 1:
            self.dec_greedy()
        elif self.tipo == 2:
            self.dec_egreedy()

    def dec_14(self):
        total = self.mao.get_total()
        self.last_t = total
        if total <= 14:
            nova_carta = self.baralho.comprar()
            self.mao.add_card(nova_carta)
            self.last_mv = 1
        else:
            self.last_mv = 0

    def dec_greedy(self):
        total = self.mao.get_total()
        self.last_t = total
        o_card = self.oponente.get_card()
        if total <=21:
            dec = [self.rltw[total,o_card],self.rltl[total,o_card]]
            if dec[0]<dec[1]:
                nova_carta = self.baralho.comprar()
                self.mao.add_card(nova_carta)
                self.last_mv = 1
            else:
                self.last_mv = 0
        else:
            self.last_mv = 0
        

    def dec_egreedy(self):
        total = self.mao.get_total()
        self.last_t = total
        o_card = self.oponente.get_card()
        if total<=21:
            dec = [self.rltw[total,o_card],self.rltl[total,o_card]]
            if np.random.rand() <= self.epsilon:
                if dec[0]>=dec[1]:
                    nova_carta = self.baralho.comprar()
                    self.mao.add_card(nova_carta)
                    self.last_mv = 1
                else:
                    self.last_mv = 0
            else:
                self.dec_greedy()
        else:
            self.last_mv = 0

    def get_card(self):
        try:
            return self.mao.cartas[0].get_valor()
        except:
            print("Sem cartas na mão")

    def update(self):
        if self.tipo not in [0,3]:
            o_card = self.oponente.get_card()
            total = self.last_t
            if self.utipo == 0:
                Q = 21 - self.mao.get_total() 
                if Q < 0:
                    Q = 21
                if self.last_mv:
                    self.rltwq[total,o_card]+=1
                    self.rltw[total,o_card]+= (Q - self.rltw[total,o_card])/self.rltwq[total,o_card]
                    
    

    def reset_mao(self):
        #del self.mao
        self.mao = mao()
        
                
                
        
            
                
            
            
            





#TESTE    
a = card(10,1)
b = card(1,2)
A = mao()
A.cartas.append(a)
A.cartas.append(b)
A.update()
