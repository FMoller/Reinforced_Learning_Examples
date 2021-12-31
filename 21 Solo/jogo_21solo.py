import numpy as np
import matplotlib.pyplot as plt




class baralho():
    def __init__(self):
        self.cartas = list(range(1,14))
        np.random.shuffle(self.cartas)

    def comprar(self):
        return self.cartas.pop()

    def len(self):
        return len(self.cartas)

    def reset(self):
        self.cartas = []
        self.cartas = list(range(1,14))
        np.random.shuffle(self.cartas)

class player():
    """ Jogador """

    def __init__(self, baralho, epsilon = 0.1, rltw = None, rltl = None, rltwq = None, rltlq = None, tipo = False):

        self.mao = []
        self.tipo = tipo #0: Guloso, 1: e-greedy
        self.resultados = 0     
        self.baralho = baralho
        self.epsilon = epsilon
        self.rltw = rltw
        self.rltl = rltl
        self.rltwq = rltwq
        self.rltlq = rltlq
        self.last_mv = 1 #0 passou, 1 comprou
        self.last_t = 0

    def f_compra(self):
        nova_carta = self.baralho.comprar()
        self.mao.append(nova_carta)

    def tomar_dec(self):
        if self.tipo:
            self.dec_egreedy()
        else:
            self.dec_greedy()

    def dec_greedy(self):
        total = np.sum(self.mao)
        self.last_t = total
        o_card = np.max(self.mao)
        if total <=21:
            dec = [self.rltw[total,o_card],self.rltl[total,o_card]]
            if dec[0]<dec[1]:
                nova_carta = self.baralho.comprar()
                self.mao.append(nova_carta)
                self.last_mv = 1
            else:
                self.last_mv = 0
        else:
            self.last_mv = 0

    def dec_egreedy(self):
        total = np.sum(self.mao)
        self.last_t = total
        o_card = np.max(self.mao)
        if total<=21:
            dec = [self.rltw[total,o_card],self.rltl[total,o_card]]
            if np.random.rand() <= self.epsilon:
                if dec[0]>=dec[1]:
                    nova_carta = self.baralho.comprar()
                    self.mao.append(nova_carta)
                    self.last_mv = 1
                else:
                    self.last_mv = 0
            else:
                self.dec_greedy()
        else:
            self.last_mv = 0

    def update(self):
        o_card = np.max(self.mao)
        total = self.last_t
        if total <=21:
            Q = 21 - np.sum(self.mao) 
            if Q < 0:
                Q = 21
            if self.last_mv:
                self.rltwq[total,o_card]+=1
                self.rltw[total,o_card]+= (Q - self.rltw[total,o_card])/self.rltwq[total,o_card]
            else:
                self.rltlq[total,o_card]+=1
                self.rltl[total,o_card]+= (Q - self.rltl[total,o_card])/self.rltlq[total,o_card]

    def reset_mao(self):
        #del self.mao
        self.mao = []
        self.last_mv = 1
        self.last_t = 0


deck_rl = baralho()
deck_gd = baralho()

r_comp_rl = np.zeros((22,14))
r_comp_g = np.zeros((22,14))

r_parar_rl = np.zeros((22,14))
r_parar_g = np.zeros((22,14))

q_comp_rl = np.zeros((22,14))
q_comp_g = np.zeros((22,14))
        
q_parar_rl = np.zeros((22,14))
q_parar_g = np.zeros((22,14))    

p_rl = player(deck_rl, epsilon = 0.1, rltw = r_comp_rl, rltl = r_parar_rl, rltwq = q_comp_rl, rltlq = q_parar_rl, tipo = True)
p_gd = player(baralho = deck_gd, epsilon = 0.1, rltw = r_comp_g, rltl = r_parar_g, rltwq = q_comp_g, rltlq = q_parar_g, tipo = False)

tracking_rl = []
tracking_gd = []
rounds_ct = []

G = 1000
M = 300
for i in range(G):
    pontos_rl = 0
    pontos_gd = 0
    for j in range(M):
        game_run = True
        rounds_c = 0
        p_rl.f_compra()
        p_gd.f_compra()
        while game_run:
            if p_rl.last_mv:
                p_rl.tomar_dec()
                p_rl.update()
            if p_gd.last_mv:
                p_gd.tomar_dec()
                p_gd.update()
            game_run = p_rl.last_mv or p_gd.last_mv
            rounds_c+=1
        #print(rounds_c)
        rounds_ct.append(rounds_c)
        tm_rl = np.sum(p_rl.mao)
        tm_gd = np.sum(p_gd.mao)
        if tm_rl <=21:
            pontos_rl += tm_rl
        if tm_gd <=21:
            pontos_gd += tm_gd
        p_rl.reset_mao()
        p_gd.reset_mao()
        deck_rl.reset()
        deck_gd.reset()
    tracking_rl.append(pontos_rl/M)
    tracking_gd.append(pontos_gd/M)

fig, ax = plt.subplots()
ax.plot(tracking_rl)
ax.plot(tracking_gd)


fig, axs = plt.subplots(1,2)
axs[0].imshow(r_comp_rl < r_parar_rl)
axs[1].imshow(r_comp_g < r_parar_g)

fig, axs = plt.subplots(1,2)
axs[0].imshow(q_comp_rl > 30)
axs[1].imshow(q_comp_g > 30)
plt.show()
        
        
        
    
