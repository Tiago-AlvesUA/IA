

# Guiao de representacao do conhecimento
# -- Redes semanticas
# 
# Inteligencia Artificial & Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2020
# v1.9 - 2019/10/20
#


# Classe Relation, com as seguintes classes derivadas:
#     - Association - uma associacao generica entre duas entidades
#     - Subtype     - uma relacao de subtipo entre dois tipos
#     - Member      - uma relacao de pertenca de uma instancia a um tipo
#

from collections import Counter

class Relation:
    def __init__(self,e1,rel,e2):
        self.entity1 = e1
#       self.relation = rel  # obsoleto
        self.name = rel
        self.entity2 = e2
    def __str__(self):
        return self.name + "(" + str(self.entity1) + "," + \
               str(self.entity2) + ")"
    def __repr__(self):
        return str(self)


# Subclasse Association
class Association(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

#   Exemplo:
#   a = Association('socrates','professor','filosofia')

class AssocOne(Relation):
    def __init__(self,e1,assoc,e2):
        Relation.__init__(self,e1,assoc,e2)

class AssocNum(Relation):
    def __init__(self, e1, e2, num):
        super().__init__(e1, e2, num)

# Subclasse Subtype
class Subtype(Relation):
    def __init__(self,sub,super):
        Relation.__init__(self,sub,"subtype",super)


#   Exemplo:
#   s = Subtype('homem','mamifero')

# Subclasse Member
class Member(Relation):
    def __init__(self,obj,type):
        Relation.__init__(self,obj,"member",type)

#   Exemplo:
#   m = Member('socrates','homem')

# classe Declaration
# -- associa um utilizador a uma relacao por si inserida
#    na rede semantica
#
class Declaration:
    def __init__(self,user,rel):
        self.user = user
        self.relation = rel
    def __str__(self):
        return "decl("+str(self.user)+","+str(self.relation)+")"
    def __repr__(self):
        return str(self)

#   Exemplos:
#   da = Declaration('descartes',a)
#   ds = Declaration('darwin',s)
#   dm = Declaration('descartes',m)

# classe SemanticNetwork
# -- composta por um conjunto de declaracoes
#    armazenado na forma de uma lista
#
class SemanticNetwork:
    def __init__(self,ldecl=None):
        self.declarations = [] if ldecl==None else ldecl
    def __str__(self):
        return str(self.declarations)
    def insert(self,decl):
        self.declarations.append(decl)
    def query_local(self,user=None,e1=None,rel=None,e2=None):
        self.query_result = \
            [ d for d in self.declarations
                if  (user == None or d.user==user)
                and (e1 == None or d.relation.entity1 == e1)
                and (rel == None or d.relation.name == rel)
                and (e2 == None or d.relation.entity2 == e2) ]
        return self.query_result
    def show_query_result(self):
        for d in self.query_result:
            print(str(d))

    #exc1 
    def list_associations(self):
        lassoc_names = [ d.relation.name for d in self.declarations
                    if isinstance(d.relation,Association) ]
        #print(lassoc_names)
        return list(set(lassoc_names))

    #exc2   **Instância de tipos -> tipo member**
    def list_objects(self):
        lobj = [ d.relation.entity1 for d in self.declarations 
                    if isinstance(d.relation,Member)]
        return list(set(lobj))

    #exc3
    def list_users(self):
        lusers = [ d.user for d in self.declarations ]
        return list(set(lusers))

    #exc4  VER AINDA CLERIGO
    def list_types(self):
        ltypes = [ d.relation.entity2 for d in self.declarations
                    if isinstance(d.relation,Member) or isinstance(d.relation,Subtype)]
        return list(set(ltypes))

    #exc5
    # Relation -> composta por e1, nome da rel, e2
    def list_local_associations(self, entity):
        localassoc = [ d.relation.name for d in self.declarations
                    if d.relation.entity1 == entity and isinstance(d.relation,Association)]
        return list(set(localassoc))

    #exc6
    def list_relations_by_user(self, user):
        lrelations = [ d.relation.name for d in self.declarations
                        if d.user == user]
        return list(set(lrelations))

    #exc7
    def associations_by_user(self,user):
        lrelations = [ d.relation.name for d in self.declarations
                        if d.user == user and isinstance(d.relation,Association)]
        return len(list(set(lrelations)))

    #exc8
    def list_local_associations_by_entity(self,entity):
        localassoc = [ (d.relation.name, d.user) for d in self.declarations
                        if d.relation.entity1 == entity and isinstance(d.relation, Association)]
        return list(set(localassoc))

    #exc9 verifica se é antecessor
    def predecessor(self, antecessor, sucessor):
        ldeclarations = self.query_local(e1=sucessor)
        #print(ldeclarations)
        lparents = [ d.relation.entity2 for d in ldeclarations 
                        if not isinstance(d.relation, Association)] #apenas relações de membro e subtipo
        #print(lparents)

        if antecessor in lparents:
            return True
        
        for p in lparents:
            if self.predecessor(antecessor,p): # Vai procurar o mesmo antecessor mas agora com os pais do sucessor inicial
                return True

        return False

    #exc10
    def predecessor_path(self, antecessor, sucessor):
        ldeclarations = self.query_local(e1=sucessor)
        lparents = [ d.relation.entity2 for d in ldeclarations
                        if not isinstance(d.relation, Association)]

        if antecessor in lparents:
            return [antecessor,sucessor]

        for p in lparents:
            path = self.predecessor_path(antecessor,p)
            if path != None:
                return path + [sucessor]

        return None

    #exc11 (a)
    # obter todas as declarações de associações locais ou herdadas por uma entidade
    def query(self,entity,assoc_name=None):
        local_decl = self.query_local(e1=entity)
        lparents = [d.relation.entity2 for d in local_decl
                        if not isinstance(d.relation, Association)]

        # adicionar às declarações as associações, inclusive a que foi passada como arg
        all_declarations = [ d for d in local_decl if isinstance(d.relation, Association)
                                            and (d.relation.name == assoc_name or assoc_name == None)] 

        for p in lparents:
            # fazer a pesquisa da hierarquia para adicionar as declarações restantes
            all_declarations += self.query(p,assoc_name)

        return all_declarations

    #exc11 (b)
    def query2(self,entity,rel_name=None):
        query_result = self.query(entity)
        
        local_decl = self.query_local(e1=entity)
        all_declarations = [ d for d in local_decl if not isinstance(d.relation,Association)
                                                    and (d.relation.name == rel_name or rel_name==None)]

        return query_result + all_declarations

    #exc12
    # quando uma associacao esta declarada numa entidade, a entidade nao herdara essa associacao das entidades predecessoras       
    def query_cancel(self,entity,assoc):
        local_decl = self.query_local(e1=entity)
        lparents = [ d.relation.entity2 for d in local_decl if not isinstance(d.relation, Association)]

        lassoc = [ d for d in local_decl if isinstance(d.relation, Association) and d.relation.name == assoc]

        #Se ainda não chegou a um "nível" da rede com a associação continua a procura
        if lassoc == []:
            for p in lparents:
                lassoc += self.query_cancel(p,assoc)

        return lassoc

    #exc13
    def query_down(self, type:str, assoc:str):
        stunf = []
        for d in self.declarations:
            if (isinstance(d.relation, Member) or isinstance(d.relation, Subtype)) and type == d.relation.entity2: # if is predecessor
                for dec in self.declarations: # append own associations (with assoc_name), then go to next child
                    if isinstance(dec.relation, Association) and dec.relation.name == assoc and dec.relation.entity1 == d.relation.entity1:
                        stunf.append(dec)
                return stunf + self.query_down(d.relation.entity1, assoc)
        return stunf

    #exc14
    def query_induce(self,entity,assoc):
        qdown = [ d.relation.entity2 for d in self.query_down(entity, assoc)]
        #get most common
        return max(set(qdown),key=qdown.count)

    #exc15
    def query_local_assoc(self,entity,assoc_name):
        local_decl = self.query_local(e1=entity,rel=assoc_name)

        for d in local_decl:
            if isinstance(d.relation,Association):
                c = Counter([la.relation.entity2 for la in local_decl])

                local_val = []
                for common in c.most_common():
                    local_val.append(common)
                    if sum([c/len(local_decl) for dummy,c in local_val]) > 0.75:
                        return [(val,c/len(local_decl)) for val,c in local_val]
            
            if isinstance(d.relation,AssocOne):
                c = Counter([la.relation.entity2 for la in local_decl])

                val, count = c.most_common(1)[0]
                return val,count/len(local_decl)
            
            if isinstance(d.relation,AssocNum):
                return sum([la.relation.entity2 for la in local_decl])/len(local_decl)








