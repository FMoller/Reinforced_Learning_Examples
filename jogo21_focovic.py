import numpy as np
import blackjack_classes as bjcl
import matplotlib.pyplot as plt

QV = 0
QE = 5
QD = 20

try:
    rltw = np.loadtxt('jogador_e_fv2_rltw.txt')
except:
    print("rlwt criada")
    rltw = np.zeros((22,14))
    np.savetxt('jogador_e_fv2_rltw.txt',rltw)
    np.savetxt('jogador_e_fv2_rltw_0.txt',rltw)

try:
    rltwq = np.loadtxt('jogador_e_fv2_rltwq.txt')
except:
    rltwq = np.zeros((22,14))
    np.savetxt('jogador_e_fv2_rltwq.txt',rltwq)
    np.savetxt('jogador_e_fv2_rltwq_0.txt',rltwq)

try:
    rltl = np.loadtxt('jogador_e_fv2_rltl.txt')
except:
    rltl = np.zeros((22,14))
    for i in range(22):
        for j in range(14):
            rltl[i,j] = 21-i
    np.savetxt('jogador_e_fv2_rltl.txt',rltl)
    np.savetxt('jogador_e_fv2_rltl_0.txt',rltl)

try:
    rltlq = np.loadtxt('jogador_e_fv2_rltlq.txt')
except:
    rltlq = np.zeros((22,14))
    np.savetxt('jogador_e_fv2_rltlq.txt',rltlq)
    np.savetxt('jogador_e_fv2_rltlq_0.txt',rltlq)

try:
    record = np.loadtxt('record_e_fv2.txt')
except:
    print("record")
    record = np.array([[0,0,0]])
    np.savetxt('record_e_fv2.txt',record)

baralho = bjcl.baralho()




inimigo = bjcl.player(baralho)
jogador = bjcl.player(baralho,inimigo,0.1,rltw,rltl,rltwq,rltlq,tipo = 1, utipo = 1)

gc = 100000


for i in range(gc):
    if i % 10000 == 0:
        print(i/10000)
    game_going = True
    jogador.f_compra()
    inimigo.f_compra()
    #print('fim compras')
    #print(jogador.mao.get_total())
    while game_going:
        jogador.tomar_dec()
        inimigo.tomar_dec()
        jogador.update()
        game_going = jogador.last_mv or inimigo.last_mv
    PJ = 21 - jogador.mao.get_total()
    PI = 21 - inimigo.mao.get_total()
    if PJ >= 0 and PI >= 0:
        if PI < PJ:
            resultado = [0,0,1]
            Q = QD
        elif PI > PJ:
            resultado = [1,0,0]
            Q = QV
        else:
            resultado = [0,1,0]
            Q = QE
    elif PJ < 0 and PI >= 0:
        resultado = [0,0,1]
        Q = QD
    elif PJ >= 0 and PI < 0:
        resultado = [1,0,0]
        Q = 0
    else:
        resultado = [0,1,0]
        Q = QE
    record = np.append(record,[resultado],axis = 0)
    jogador.f_update(Q)
    baralho.reset()
    jogador.reset_mao()
    inimigo.reset_mao()
        
        
np.savetxt('jogador_e_fv2_rltw.txt',rltw)
np.savetxt('jogador_e_fv2_rltwq.txt',rltwq)
np.savetxt('jogador_e_fv2_rltl.txt',rltl)
np.savetxt('jogador_e_fv2_rltlq.txt',rltlq)
np.savetxt('record_e_fv2.txt',record)

np.savetxt('jogador_e_fv2_rltw_'+str(len(record))+'.txt',rltw)
np.savetxt('jogador_e_fv2_rltwq_'+str(len(record))+'.txt',rltwq)
np.savetxt('jogador_e_fv2_rltl_'+str(len(record))+'.txt',rltl)
np.savetxt('jogador_e_fv2_rltlq_'+str(len(record))+'.txt',rltlq)

vic = []
der = []
emp = []
t_vic = 0
t_der = 0
t_emp = 0
for i in record:
    t_vic+= i[0]
    t_emp+= i[1]
    t_der+= i[2]
    vic.append(t_vic)
    der.append(t_der)
    emp.append(t_emp)
for i in range(len(vic)):
    vic[i] = vic[i]/(i+1)
    der[i] = der[i]/(i+1)
    emp[i] = emp[i]/(i+1)
    
fig, ax = plt.subplots()
dados = {'vic':vic,'der':der,'emp':emp}
d = np.array(range(len(vic)))
ax.stackplot(d,dados.values(),labels = dados.keys(),alpha = 0.8)
ax.legend(loc='upper left')

fig, axs = plt.subplots()
axs.imshow(rltw > rltl)

plt.show()
