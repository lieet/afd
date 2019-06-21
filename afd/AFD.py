class AFD:
    "Classe para representar um AFD"
    
    def __init__(self, e, ei, a):
        self.estados = e #Os estados do AFD
        self.estadoInicial = ei #O estado inicial do AFD
        self.alfabeto = a #O alfabeto do AFD
        self.estadosFinais = [] #Os estados de aceitacao do AFD
        self.transicoes = {} #As funcoes de transicao no formato {(p, 0): q} -> p recebe 0 vai para q

    def addEF(self, ef):
        if ef in self.estados:
            self.estadosFinais.append(ef)

    def addTransicao(self, p, q, r):
        if p in self.estados and r in self.estados and q in self.alfabeto: #Testa se os valores da funcao de transicao estao no conjunto de estados e no alfabeto
            if (p, q) not in self.transicoes.keys():
                self.transicoes[(p, q)] = r

    def teste(self, s):
        atual = "" #Variavel que armazena o estado que esta sendo percorrido depois de digerir um caractere do alfabeto
        s = s.replace(" ", "") #Retira os espacos da string de entrada

        for c, q in self.transicoes.keys(): #Olha as transicoes do estado inicial
            if c == self.estadoInicial and q == s[0:len(q)]:
                atual = self.transicoes[(c, q)]
                s = s[len(q):] #Retira o primeiro valor da sequencia
                break

        while s:
            v = True

            for c, q in self.transicoes.keys():
                if c == atual and q == s[0:len(q)]:
                    atual = self.transicoes[(c, q)]
                    s = s[len(q):] #Retira o primeiro valor da sequencia
                    v = False
                    break

            if v: #Erro: a string de entrada tem um caractere que nao faz parte do alfabeto, ou, durante o percurso, o algoritmo de passagem morreu porque tem uma transicao nao definida nas trasicoes.
                return ""

        return atual

    def efinal(self, e):
        return 1 if e in self.estadosFinais else 0
