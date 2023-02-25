from cmath import pi
import math
from re import sub

#Exercicio 4.1
impar = lambda x : x % 2 != 0
print(impar(3))
print(impar(4))

#Exercicio 4.2
positivo = lambda x : x > 0 and x != 0
print(positivo(3))
print(positivo(-4))

#Exercicio 4.3
comparar_modulo = lambda a, b: abs(a) < abs(b)
print(comparar_modulo(-4, 2))
print(comparar_modulo(3, -4))

#Exercicio 4.4
cart2pol = lambda x,y: (math.sqrt(x**2 + y**2), math.atan(y/x) if x != 0 else pi/2)
print(cart2pol(0, 1))

#Exercicio 4.5
ex5 = lambda f,g,h: lambda x,y,z: h(f(x,y), g(y,z))
t = ex5(lambda x,y: x+y, lambda x,y: x*y, lambda x,y: x < y)
print(t(1,2,3))

#FUNÇÕES DE ORDEM SUPERIOR: Recebem expressões lambda como entrada e/ou produzem expressões lambda como saída
#Exercicio 4.6
def quantificador_universal(lista, f):
    if lista == []:
        return True

    return f(lista[0]) and quantificador_universal(lista[1:], f)

quantificador_universal([11,12,13,14], lambda n: n > 10)

#Exercicio 4.8
def subconjunto(lista1, lista2):
    if lista1 == []:
        return True
    
    return lista1[0] in lista2 and subconjunto(lista1[1:], lista2)

subconjunto([11,12,13,14], [11,12,13,14,15,16])
subconjunto([11,12,13,14], [10,11,12,13,14])
subconjunto([11,12,13,14], [10,11,12,13,14,15])
subconjunto([11,12,33,14], [10,11,12,13,14,15])

#Exercicio 4.9
def menor_ordem(lista, f):
    if not lista:
        return None
    if len(lista)==1:
        return lista[0]

    m = menor_ordem(lista[1:],f)

    if f(lista[0],m):
        return lista[0]
    return m 

#menor_ordem([1,-1,4,0], lambda x,y: x < y) 
#menor_ordem([1,-1,4,0], lambda x,y: x > y) 

#Exercicio 4.10
def menor_e_resto_ordem(lista, f):
    if not lista: 
        return None
    m = menor_ordem(lista,f)
    return (m, list(filter(lambda elem: elem!=m, lista)))

#Exercicio 4.11
def ordem_triplo(lista,f):
    if len(lista)<2:
        return None
    m1 = menor_e_resto_ordem(lista,f)
    m2 = menor_ordem(m1[1],f)
    return (m1, m2, list(filter(lambda elem: elem!=m1 and elem!=m2,lista)))

#Exercicio 4.13
def mergeLists(lista1, lista2, f):
    if lista1 == []:
        return []
    if lista2 == []:
        return []

    l = mergeLists(lista1[1:], lista2[1:], f)

    if f(lista1[0], lista2[0]):
        return [lista1[0]] + mergeLists(lista1[1:],lista2[:], f)
    return [lista2[0]] + mergeLists(lista1[:],lista2[1:],f)

#Exercicio 4.14
def conc_lst(lista,f):
    if lista == []:
        return []

    l = [f(lista[0][0])] + conc_lst([lst[0][1:]] + list[1:], f)

    return l
    
#Exercicio 5.2
def ordenar_seleccao(lista, ordem):
    pass

def main():
    lst1 = [-5, -3, -1, 0, 0, 4, 5, 8]
    lst2 = [-3, 1, 1, 1, 5, 5, 5, 10]
    func = lambda x, y: x <= y
    print(mergeLists(lst1, lst2, func))


if __name__ == '__main__':
    main()
