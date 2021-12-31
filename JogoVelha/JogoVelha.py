import numpy as np
import matplotlib.pyplot as plt

politicas_rl = np.zeros((3**9,9))
politicas_rlq = np.zeros((3**9,9))

politicas_gd = np.zeros((3**9,9))
politicas_gdq = np.zeros((3**9,9))
base3 = []
for i in range(9):
    base3.append([3**i])
base3 = np.array(base3)

def busca_estado(tabuleiro):
    return int(np.dot(tabuleiro,base3))




def verifica_vitoria(tabuleiro,jogador):
    marcas = tabuleiro == jogador
    if np.sum(marcas[0:3]) == 3 or np.sum(marcas[3:6]) == 3 or np.sum(marcas[6:9]) == 3:
        return True
    if np.sum(marcas[0:9:3]) == 3 or np.sum(marcas[1:9:3]) == 3 or np.sum(marcas[2:9:3]) == 3:
        return True
    if np.sum(marcas[0:9:4]) == 3 or np.sum(marcas[2:8:2]) == 3:
        return True
    return False

def jogador_gd(tabuleiro,politicas):
    estado = busca_estado(tabuleiro)
    possiveis = tabuleiro == 0
    possiveis_list = list(np.where(tabuleiro == 0)[0])
    best = np.max(politicas[estado,possiveis])
    pos = list(np.where(politicas[estado,:] == best)[0])
    politica = pos.pop()
    while politica not in possiveis_list:
        politica = pos.pop()
    return (estado,politica)

def jogador_rl(tabuleiro,politicas,epsilon):
    estado = busca_estado(tabuleiro)
    possiveis = tabuleiro == 0
    possiveis_list = list(np.where(tabuleiro == 0)[0])
    if np.random.rand() > epsilon:
        best = np.max(politicas[estado,possiveis])
        pos = list(np.where(politicas[estado,:] == best)[0])
        #print(pos)
        politica = pos.pop()
        while politica not in possiveis_list:
            politica = pos.pop()
        return (estado,politica)
    else:
        np.random.shuffle(possiveis_list)
        return (estado,possiveis_list[0])

     
tab_jogo = np.zeros(9)

def atualiza_simples(Qval,track,politicas,politicas_q):
    for i in track:
        estado = i[0]
        pol = i[1]
        politicas_q[estado,pol] += 1
        politicas[estado,pol] += (Qval - politicas[estado,pol])/politicas_q[estado,pol]

def partida():
    tab_jogo = np.zeros(9)
    rl_track = []
    gd_track = []
    jogo_on = True
    while jogo_on:
        jogada_rl = jogador_rl(tab_jogo,politicas_rl,0.1)
        rl_track.append(jogada_rl)
        tab_jogo[jogada_rl[1]] = 1
        if verifica_vitoria(tab_jogo,1):
            return (1,rl_track,gd_track)
        vagas = np.sum(tab_jogo==0)
        if vagas == 0:
            return (0,rl_track,gd_track)
        jogada_gd = jogador_gd(tab_jogo,politicas_gd)
        gd_track.append(jogada_gd)
        tab_jogo[jogada_gd[1]] = 2
        if verifica_vitoria(tab_jogo,2):
            return (2,rl_track,gd_track)

def partida_s():
    tab_jogo = np.zeros(9)
    rl_track = []
    gd_track = []
    jogo_on = True
    while jogo_on:
        jogada_gd = jogador_gd(tab_jogo,politicas_gd)
        gd_track.append(jogada_gd)
        tab_jogo[jogada_gd[1]] = 2
        if verifica_vitoria(tab_jogo,2):
            return (2,rl_track,gd_track)     
        vagas = np.sum(tab_jogo==0)
        if vagas == 0:
            return (0,rl_track,gd_track)
        jogada_rl = jogador_rl(tab_jogo,politicas_rl,0.1)
        rl_track.append(jogada_rl)
        tab_jogo[jogada_rl[1]] = 1
        if verifica_vitoria(tab_jogo,1):
            return (1,rl_track,gd_track)
        
    
        
        
def campeonato(jogos):
    resultados = np.array([0,0,0])
    for i in range(jogos):
        Q = [0,0]
        jogo = partida_s()
        if jogo[0] == 1:
            Q = [2,-2]
            resultados[0]+=1
        elif jogo[0] == 2:
            Q = [-2,2]
            resultados[2]+=1
        else:
            Q = [1,1]
            resultados[1]+=1
        atualiza_simples(Q[0],jogo[1],politicas_rl,politicas_rlq)
        atualiza_simples(Q[1],jogo[2],politicas_gd,politicas_gdq)
        Q = [0,0]
        jogo = partida()
        if jogo[0] == 1:
            Q = [2,-2]
            resultados[0]+=1
        elif jogo[0] == 2:
            Q = [-2,2]
            resultados[2]+=1
        else:
            Q = [1,1]
            resultados[1]+=1
        atualiza_simples(Q[0],jogo[1],politicas_rl,politicas_rlq)
        atualiza_simples(Q[1],jogo[2],politicas_gd,politicas_gdq)
    return resultados/(jogos*2)
        
    
        
tempo = 100    
placar = np.zeros((tempo,3))
for i in range(1,tempo):
    placar[i,:] = campeonato(30)

d = np.array(range(tempo))
dados = {'Vitorias':placar[:,0],'Derrotas':placar[:,2],'Empates':placar[:,1]}
fig, ax = plt.subplots()

ax.stackplot(d,dados.values(),labels = dados.keys(),alpha = 0.8)
ax.legend(loc='upper left')
ax.set_xlabel('Campeonatos')
ax.set_ylabel('Proporção de resultados')

plt.show()


