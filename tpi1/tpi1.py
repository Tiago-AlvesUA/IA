# Autor: Tiago Alves nmec: 104110
# Código discutido com
# Rafael Pinto nmec: 103379

from tree_search import *
from cidades import *
from blocksworld import *


def func_branching(connections,coordinates):
    # para cada conexão temos cidade 1, 2 e distância
    # para calcular os vizinhos de uma cidade temos que ver as cidades que tem ao lado, quer
    # esteja em C1 ou C2
    # numero vizinhos podia ter ido buscar pelas coordinates
    cidades_diferentes = []
    vizinhos = 0
    for (C1,C2,D) in connections:
        if C1 not in cidades_diferentes:
            cidades_diferentes.append(C1)
        elif C2 not in cidades_diferentes:
            cidades_diferentes.append(C2)

    for cidade in cidades_diferentes:
        for (C1,C2,D) in connections:
            if C1 == cidade or C2 == cidade:
                vizinhos = vizinhos + 1
    return (vizinhos/len(cidades_diferentes)) - 1
    #IMPLEMENT HERE

class MyCities(Cidades):
    def __init__(self,connections,coordinates):
        super().__init__(connections,coordinates)
        # ADD CODE HERE IF NEEDED
        self.branching = func_branching(connections,coordinates)


class MySTRIPS(STRIPS):
    def __init__(self,optimize=False):
        super().__init__(optimize)

    def simulate_plan(self,state,plan):
        #IMPLEMENT HERE
        for action in plan:
            #dar update ao estado depois de feita a ação
            state = self.result(state,action)
        return state
 
class MyNode(SearchNode):
    def __init__(self,state,parent,cost=0,heuristic=0,depth=0):
        super().__init__(state,parent)
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic

        #ADD HERE ANY CODE YOU NEED

class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth',optimize=0,keep=0.25): 
        super().__init__(problem,strategy)
        self.optimize = optimize
        if(self.optimize == 0):
            root = MyNode(problem.initial, None, 0, problem.domain.heuristic(problem.initial, problem.goal), 0)
        if(self.optimize == 1):
            #(state,parent,cost,heuristic,depth)
            root = (problem.initial, None, 0, problem.domain.heuristic(problem.initial, problem.goal), 0)
        if(self.optimize == 2):
            #( f actions , f result , f cost , f heuristic , f satisfies ,branching)
            root = (problem[1], None, 0, problem[0][3](problem[1], problem[2]), 0)
        if(self.optimize == 4):
            root = (problem[1], None, 0, problem[0][3](problem[1], problem[2]), 0)
        self.all_nodes = [root]
        self.open_nodes = [0]
        self.keep = keep
        #ADD HERE ANY CODE YOU NEED

    def astar_add_to_open(self,lnewnodes):
        #A* tem em conta custo e heurística
        if self.optimize == 0:
            self.open_nodes.extend(lnewnodes)
            return self.open_nodes.sort(key = lambda nodeID : self.all_nodes[nodeID].cost + self.all_nodes[nodeID].heuristic)
        if self.optimize != 0:
            self.open_nodes.extend(lnewnodes)
            return self.open_nodes.sort(key = lambda nodeID : self.all_nodes[nodeID][2] + self.all_nodes[nodeID][3])


    # remove a fraction of open (terminal) nodes
    # with lowest evaluation function
    # (used in Incrementally Bounded A*)
    def forget_worst_terminals(self):
        #IMPLEMENT HERE
        #max_nodes_given_depth é o numero de nós num nível completo da tree com depth 'd'
        #numKeep = self.keep*max_nodes_given_depth

        pass

    # procurar a solucao
    def search2(self):
        if self.optimize == 0:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node.state):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    if newstate not in self.get_path(node):
                        newnode = MyNode(newstate,nodeID,node.cost + self.problem.domain.cost(node.state,a), self.problem.domain.heuristic(newstate,self.problem.goal),node.depth + 1)
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
        if self.optimize == 1:
                        #(state,parent,cost,heuristic,depth)
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.problem.goal_test(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path2(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem.domain.actions(node[0]):
                    newstate = self.problem.domain.result(node[0],a)
                    if newstate not in self.get_path2(node):
                        newnode = (newstate,nodeID,node[2] + self.problem.domain.cost(node[0],a),self.problem.domain.heuristic(newstate,self.problem.goal),node[4] + 1)   
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
        if self.optimize == 2:
                        #( f actions , f result , f cost , f heuristic , f satisfies ,branching)
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                node = self.all_nodes[nodeID]
                if self.goal_test2(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path2(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):
                    newstate = self.problem[0][1](node[0],a)
                    if newstate not in self.get_path2(node):
                        newnode = (newstate,nodeID,node[2] + self.problem[0][2](node[0],a),self.problem[0][3](newstate,self.problem[2]),node[4] + 1)   
                        lnewnodes.append(len(self.all_nodes))
                        self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
        if self.optimize == 4:
            while self.open_nodes != []:
                nodeID = self.open_nodes.pop(0)
                #print(nodeID)
                node = self.all_nodes[nodeID]
                #print(node)
                if self.goal_test2(node[0]):
                    self.solution = node
                    self.terminals = len(self.open_nodes)+1
                    return self.get_path2(node)
                lnewnodes = []
                self.non_terminals += 1
                for a in self.problem[0][0](node[0]):  # actions
                    newstate = self.problem[0][1](node[0],a) # result 
                    estadoExiste = False 
                    if newstate not in self.get_path2(node):
                        newnode = (newstate,nodeID,node[2] + self.problem[0][2](node[0],a),self.problem[0][3](newstate,self.problem[2]),node[4] + 1)
                        for idx in range(0,len(self.all_nodes)): # percorrer statesVisited
                        #for n in self.all_nodes:
                            print(self.all_nodes[idx][0])
                            if self.all_nodes[idx][0] == newstate: # transformar
                                estadoExiste = True
                                if self.all_nodes[idx][2] > newnode[2]:
                                    self.all_nodes[idx] = newnode
                                    # self.add_to_open(lnewnodes)
                        if not estadoExiste:
                            lnewnodes.append(len(self.all_nodes))
                            self.all_nodes.append(newnode)
                self.add_to_open(lnewnodes)
        return None
        #IMPLEMENT HERE

# If needed, auxiliary functions can be added

    def get_path2(self,node):
        if node[1] == None:
            return [node[0]]
        path = self.get_path2(self.all_nodes[node[1]])
        path += [node[0]]
        return(path)

    def goal_test2(self, state):
        #( f actions , f result , f cost , f heuristic , f satisfies ,branching)
        return self.problem[0][4](state,self.problem[2])
