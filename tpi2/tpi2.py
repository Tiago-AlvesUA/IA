#encoding: utf8

# YOUR NAME: Tiago Alves
# YOUR NUMBER: 104110

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - Rafael Pinto, 103379
# - ...

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def is_object(self,user,obj):
        # IMPLEMENT HERE
        search = [d.relation.entity1 for d in self.declarations if isinstance(d.relation,Member) and d.user == user]
        search += [d.relation.entity1 and d.relation.entity2 
                        for d in self.declarations 
                            if isinstance(d.relation, Association) and d.user == user]
        if obj in search:
            return True
        return  False

    def is_type(self,user,type):
        # IMPLEMENT HERE
        search = [d.relation.entity2 for d in self.declarations 
                    if (isinstance(d.relation,Member) and d.user == user)]
        search += [d.relation.entity1 and d.relation.entity2 for d in self.declarations
                    if (isinstance(d.relation, Association) and d.user == user and d.relation.card != None)]
        if type in search:
            return True
        return False


    def infer_type(self,user,obj):
        # IMPLEMENT HERE

        # dicionario para guardar tipos associados as relaçoes
        relTypes = {}

        for d in self.declarations:
            if isinstance(d.relation,Member) and d.relation.entity1 == obj and d.user == user:
                return d.relation.entity2 
            if isinstance(d.relation,Association) and d.relation.card != None and d.user == user:
                tuplo = self.infer_signature(user,d.relation.name)
                #acrescentar os tipos associados à relação ao dict
                relTypes[d.relation.name] = tuplo
                
        for d in self.declarations:
            if d.user == user and isinstance(d.relation,Association):
                if d.relation.entity1 == obj and d.relation.name in relTypes.keys():
                    return relTypes[d.relation.name][0]
                if d.relation.entity2 == obj and d.relation.name in relTypes.keys():
                    return relTypes[d.relation.name][1]
                if (d.relation.entity2 == obj or d.relation.entity1 == obj) and d.relation.name not in relTypes.keys():
                    return "__unknown__"
        return None
        
 
    def infer_signature(self,user,assoc):
        # IMPLEMENT HERE
        for d in self.declarations: 
            if isinstance(d.relation,Association) and d.user == user and d.relation.name == assoc:
                if d.relation.card != None:
                    # se a relação tiver cardinal diferente de None tem-se os 2 tipos da e1 e e2
                    return (d.relation.entity1, d.relation.entity2)
                # se a rel tiver cardinal None chamamos a fc de inferir tipo porque e1 e e2 são objetos
                return (self.infer_type(user, d.relation.entity1), self.infer_type(user, d.relation.entity2))

        #se associação não existe retorna None
        return None

class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def markov_blanket(self,var):
        # IMPLEMENT HERE

        result = set()
        for key in self.dependencies:
            for dep in self.dependencies[key]:
                # por cada dependência nas dependências da key obter var's Verdadeiras e Falsas
                mtrue, mfalse, p = dep
                variables = [key]
                variables.extend(mtrue)
                variables.extend(mfalse)
                if var in variables:
                    # se a var pretendida se encontrar nesta lista de variáveis esta lista será adicionada ao resultado
                    result.update(variables)
        # resultado ja a contar com os pais da var, 
        # filhos da var
        # e pais dos filhos da var
        result.remove(var)

        return list(result)


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def propagate(self,domains,var):
        # IMPLEMENT HERE

        ledges = [ (v, z) for (v, z) in self.constraints if z == var ]
        #enquanto fila de arestas não vazia
        while ledges != []:
            # remover cabeça
            (xj, xi) = ledges.pop()

            numValsAnterior = len(domains[xj])
            
            c = self.constraints[xj, xi]
            #remover valores inconsistentes em xj
            domains[xj] = [ val_j for val_j in domains[xj] 
                            if any(c(xj, val_j, xi, val_i) for val_i in domains[xi]) ]

            #se removeu valores
            if len(domains[xj]) < numValsAnterior:
                #para cada vizinho xk, acrescentar (xk,xj) a ledges
                ledges += [ (xk, z) for (xk, z) in self.constraints if z == xj ]
        return domains
        

    def produto_cartesiano(self,dominios, lvars):
        if lvars == []:
            return [()]

        rec = self.produto_cartesiano(dominios, lvars[1:])
        v = lvars[0]
        # combinacao com todos os elementos v e rec
        return [(x,)+t for t in rec for x in dominios[v]]

    def higherorder2binary(self,ho_c_vars,unary_c):
        # IMPLEMENT HERE

        #high-order constraint vars
        #unary constraint

        aux = ''.join(ho_c_vars)

        # dominio da variavel auxiliar (com produto cartesiano)
        self.domains[aux] = [ t for t in self.produto_cartesiano(self.domains, ho_c_vars) if unary_c(t) ]
        
        # obter restricoes binarias
        for i,var in enumerate(ho_c_vars):
            self.constraints[var, aux] = lambda v,vx,av,avx : vx==avx[ho_c_vars.index(v)] 
            self.constraints[aux, var] = lambda av,avx,v,vx : vx==avx[ho_c_vars.index(v)]
        
        


