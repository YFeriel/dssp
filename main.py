import math
import csv

def calcul_dist(line1, line2):  #fonction pour calculer la distance
    cor1 = line1.split()
    cor2 = line2.split()
    x1, y1, z1 = float(cor1[6]), float(cor1[7]), float(cor1[8])
    x2, y2, z2 = float(cor2[6]), float(cor2[7]), float(cor2[8])
    distance_on = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2) + math.pow(z1-z2, 2))
    return cor1[3]+" "+ cor1[5]+"-"+cor2[3]+" "+cor2[5]+ " " " : {0:.3f}\n".format(distance_on)

#Fonction energie :
def calcul_energy(distance_on,distance_oh,distance_ch,distance_cn):
    e = 1.06217662*(10^-19)
    q1= 0.42*e
    q2= 0.2*e
    f= 332
    energy=[]
    for i in range(len(distance_on)):
        energy.append((q1*q2)*((1/distance_on[i])+(1/distance_ch[i])-(1/distance_oh[i])-(1/distance_cn[i]))*f)
    return energy

o_atome=[]
n_atome=[]
alpha=[]
c_atome=[]

elements=[]
elt = []
with open("chaine1.pdb") as chain:
    for line in chain:

        if line[13:15].startswith('O') and line[13:15].endswith(' '):
            o_atome.append(line)
            elt=line.split()
            chaine=elt[3]+elt[5]
            elements.append(chaine)
        if line[13:15].startswith('N') and line[13:15].endswith(' '):
            n_atome.append(line)
        if line[13:15].startswith('C') and line[13:15].endswith(' '):
            c_atome.append(line)
        if line[13:15]=='CA':
            alpha.append(line)

with open("Distance_O_N","w") as calculator:
    for i in range(len(o_atome)):
        for j in range(len(n_atome)):
            calculator.write(str(calcul_dist(o_atome[i],n_atome[j])))

with open("Distance_O_H","w") as calculator:
    for i in range(len(o_atome)):
        for j in range(len(alpha)):
            calculator.write(str(calcul_dist(o_atome[i],alpha[j])))

with open("Distance_C_N","w") as calculator:
    for i in range(len(c_atome)):
        for j in range(len(n_atome)):
            calculator.write(str(calcul_dist(c_atome[i],n_atome[j])))

with open("Distance_C_H","w") as calculator:
    for i in range(len(c_atome)):
        for j in range(len(n_atome)):
            calculator.write(str(calcul_dist(c_atome[i],alpha[j])))

distance_on = []
distance_cn = []
distance_oh = []
distance_ch = []

temp = []

with open("Distance_O_N","r") as f:
    for lines in f:
        line = lines.split()
        distance_on.append(float(line[-1]))
with open("Distance_C_N","r") as f:
    for lines in f:
        line = lines.split()
        distance_cn.append(float(line[-1]))
with open("Distance_O_H","r") as f:
    for lines in f:
        line = lines.split()
        distance_oh.append(float(line[-1]))
with open("Distance_C_H","r") as f:
    for lines in f:
        line = lines.split()
        distance_ch.append(float(line[-1]))

energy = calcul_energy(distance_on,distance_cn,distance_ch,distance_oh)

i=0
with open("Distance_O_N","r") as f:
    with open("Energy","w") as e :
        for lines in f:
            line = lines.split()
            e.write(line[0]+line[1]+line[2]+line[3]+" "+str(energy[i])+"\n")
            i+=1


liaison_h = []
pas_liaison = []
results=[]
with open("Energy","r") as f:
    for lines in f :
        line = lines.split()
        line[-1] = float(line[-1])
        if float(line[-1]) < -0.5 :
            liaison_h.append(line)
            results.append(1)
        else:
            pas_liaison.append(line)
            results.append(0)
cpt=1
header = [""]
for i in range(len(elements)):
    header.append(elements[i])
    cpt+=1

final = []
final.append(header)

temp=[]

j=0
k=1
var = 0
temp.append(header[1])
while j < len(results):
    temp.append(results[j])
    var+=1
    if var == len(o_atome):
        k += 1
        final.append(temp)
        temp=[]
        if k == len(o_atome)+1:
            break
        temp.append(header[k])
        var=0
    j += 1