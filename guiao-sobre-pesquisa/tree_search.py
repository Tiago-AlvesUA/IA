# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:                                                           #NÓ COMPOSTO PELA CIDADE E PELA CIDADE ANTERIOR (PAI)
    def __init__(self,state,parent,depth,cost,heuristic,action):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action = action
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem,strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, self.problem.domain.heuristic(problem.initial,problem.goal),None)                         
                                                                            # EXC2: Raíz da árvore de pesquisa está na profundidade 0...
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.terminals = 0
        self.non_terminals = 0
        self.highest_cost_nodes = [root]
        self.average_depth = 0
        self.plan = []

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self,limit=None):                                            # EXC4: Aqui metemos o argumento limit para que pesquisa possa ter um limite                                                              
        while self.open_nodes != []:                                        #       de depth, e default value None para poder ser utilizada sem limite
            self.terminals = len(self.open_nodes)                           # EXC5: Número nós-abertos após pesquisa; Tem que ser antes do pop do nó a analisar
            node = self.open_nodes.pop(0)                                   #       porque este vai ser retirado para analisar e os terminais são todos, incluindo a solução
            if self.problem.goal_test(node.state):
                self.solution = node
                self.average_depth /= self.non_terminals + self.terminals   # EXC16: Divide soma das profundidades por todos os nós para obter média
                parent = node
                while parent:
                    self.plan = [parent.action] + self.plan
                    parent = parent.parent
                self.plan = self.plan[1:]
                return self.get_path(node)
            lnewnodes = []
            self.non_terminals += 1
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state, a)
                if newstate not in self.get_path(node):                     # EXC1: Só aceita novos estados (cidades) se não estiverem já no path do nó
                    newnode = SearchNode(newstate,node,node.depth + 1,node.cost + self.problem.domain.cost(node.state,a), self.problem.domain.heuristic(newstate,self.problem.goal), a)    
                                                                            # EXC8: Vamos buscar o custo ao domínio do problema (neste caso é a distância de uma cidade à outra)
                                                                            # EXC2: A cada novo nó procurado a profundidade aumenta em +1
                    lnewnodes.append(newnode)
                    if newnode.cost > self.highest_cost_nodes[0].cost:      # EXC15: Usamos newnode porque mesmo que não seja a solução por ter custo maior são sempre nós abertos da árvore (pelo menos abertos, claro que podem ser também não terminais)
                        self.highest_cost_nodes = [newnode]                
                    elif newnode.cost == self.highest_cost_nodes[0].cost:   # EXC15: Se custo do nó for igual ao custo do nó com custo maior este é adicionado à lista
                        self.highest_cost_nodes.append(newnode)
                    self.average_depth += newnode.depth                     # EXC16: Vai somando profundidade novos nós
            if limit == None or node.depth < limit:                         # EXC4: Só acrescenta nós abertos se o nó não tiver limite ou ainda estiver
                self.add_to_open(lnewnodes)                                 #       abaixo desse limite
            
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':                                    # EXC10: Sort por custo e assim escolhe os de custo menor (que passam para primeiro na lista)
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n : n.cost)                     
        elif self.strategy == 'greedy':                                     # EXC13: Pesquisa gulosa -> pela heurística
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n : n.heuristic)                
        elif self.strategy == 'a*':                                         # EXC14: A* tem em conta custo e heur+istica
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda n : n.cost + n.heuristic) 
    
    
    
    @property                                                               # EXC3: Devolve o comprimento da solução encontrada
    def length(self):
        return self.solution.depth

    @property
    def avg_branching(self):                                                # EXC6: Average branching -> ratio entre nº nós filhos (terminais) e nós pais (não terminais)
        return (self.terminals + self.non_terminals - 1)/self.non_terminals  
    
    @property
    def cost(self):
        return self.solution.cost