from math import *
import random
import matplotlib.pyplot as plt
import numpy as np


def Syracuse(N):
    liste=[N]
    x=N
    n=0
    while x!=1:
        if x%2==0:
            x//=2
            liste+=[x]
        else:
            x=x*3+1
            liste+=[x]
        n+=1
    return liste
    #return max(liste), n (ça c'est pour la longueur et la valeur max)
#print(Syracuse(126))
'''plt.plot(Syracuse(126))
plt.show()'''

#liste=[0,0,1,0,2,0,2,2,1,6,0]
def VanEck(n):
    liste=[0]
    for _ in range(n):
        try:
            nv=liste.index(liste[0],1)
            liste.insert(0,nv)
        except:
            liste.insert(0,0)
    liste.reverse()
    return liste
#print(VanEck(1000))
'''plt.plot(VanEck(10000),".",markersize=2)
plt.show()'''

def Q(n): #Suite Q de Hofstadter
    liste = [0,1,1] # On met 0 en indice 0 juste pour décaler pour que les indices soient corrects ( pour que Q(1)=liste[1] ...)
    for i in range(3,n+1):
        liste.append(liste[i-liste[i-1]]+liste[i-liste[i-2]]) #Qn=Qn−Qn−1+Qn−Qn−2, n>2
    return liste[1:]


def u(n):
    if n==0: return 0
    else: return (n+0.15)*sqrt(n)

def x(n):
    liste=[0]
    for i in range(1,n+1):
        liste.append(liste[i-1]+cos(2*pi*u(n)))
    return liste

def y(n):
    liste=[0]
    for i in range(1,n+1):
        liste.append(liste[i-1]+sin(2*u(n+1)))
    return liste
'''
N=1000000
plt.axis('equal')
plt.plot(x(N),y(N), 'r', linewidth=0.3)
plt.show()'''

def u(mu,u0,n):
    liste=[u0]
    for i in range(n):
        liste.append(mu*liste[i]*(1-liste[i]))
    return liste

def dessiner(mu,u0,n):
    # Tracé de f(x) = mu * x * (1-x)
    X = np.linspace(0,1,100)
    Y = mu*X*(1-X)
    plt.plot(X, Y)
    
    # Tracé de y=x
    plt.plot([0,1])
    
    # Tracé de la suite
    U = u(mu,u0,n)
    for i in range(n):
        # Tracé du trait vertical joignant (u_i;u_i) à (u_i, u_(i+1))
        plt.plot([U[i],U[i]],[U[i],U[i+1]],"r",linewidth=0.5)
        # Tracé du trait horizontal joignant (u_i;u_(i+1)) à (u_(i+1); u_(i+1))
        plt.plot([U[i],U[i+1]],[U[i+1],U[i+1]],"r",linewidth=0.5)
    
    plt.axis("equal") # Pour avoir un repère orthonormé
    plt.show()

#print(dessiner(3.5,0.89999999,30))


def iteration(r, niter=100):

    x = random.uniform(0, 1)
    i = 0
    while i < niter and x < 1:
        x = r * x * (1 - x)
        i += 1

    return x if x < 1 else -1


def generate_diagram(r, ntrials=50):
    """
    Cette fonction retourne (jusqu'à) *ntrials* valeurs d'équilibre
    pour les *r* d'entrée.  Elle renvoie un tuple:

    + le premier élément est la liste des valeurs prises par le paramètre *r*
    + le second est la liste des points d'équilibre correspondants
    """

    r_v = []
    x_v = []
    for rr in r:
        j = 0
        while j < ntrials:
            xx = iteration(rr)
            if xx > 0:  # Convergence: il s'agit d'une valeur d'équilibre
                r_v.append(rr)
                x_v.append(xx)
            j += 1                      # Nouvel essai

    return r_v, x_v

r = np.linspace(0, 4, 1000)
x, y = generate_diagram(r)

plt.plot(x, y, 'k,')
plt.xlabel('r')
plt.ylabel('x')
plt.show()

'''while mu < 4 :
    plt.plot([u(k) for k in range(2, 5)],"r,")
    mu+=0.001
    
plt.show()'''
