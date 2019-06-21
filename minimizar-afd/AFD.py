from itertools import combinations

class AFD:
    "Representacao de um AFD (automato finito deterministico)"

    def __init__(self, e, ei, a, ef=[], t={}):
        self.estados = e #Os estados do AFD
        self.estadoInicial = ei #O estado inicial do AFD
        self.alfabeto = a #O alfabeto do AFD
        self.estadosFinais = ef #Os estados de aceitacao do AFD
        self.transicoes = t #As funcoes de transicao no formato {(p, c): q} -> p recebe c vai para q

    def __del__(self):
        del self.estados[:]
        self.estadoInicial = None
        del self.alfabeto[:]
        del self.estadosFinais[:]
        self.transicoes.clear()

    def addEF(self, ef):
        if ef in self.estados:
            self.estadosFinais.append(ef)

    def addTransicao(self, p, q, r):
        if p in self.estados and r in self.estados and q in self.alfabeto: #Testa se os valores da funcao de transicao estao no conjunto de estados e no alfabeto
            if (p, q) not in self.transicoes.keys(): #Nao permite que um par (p, q) tenha mais de um destino
                self.transicoes[(p, q)] = r
    
    def minimizar(self): #minimizacao de um afd
        e = list(self.estados)
        dic = {i:"-" for i in combinations(e, 2)} #criacao da tabela
        lista = [] #lista auxiliar que guarda pares para posterior analise

        #marcar estados trivialmente nao equivalentes
        for v, r in dic.keys():
            if (v in self.estadosFinais and r not in self.estadosFinais) or (r in self.estadosFinais and v not in self.estadosFinais):
                dic[(v, r)] = "x"

        #marcar outros estados
        for v, r in dic.keys():
            if dic[(v, r)] == "-":
                for a in self.alfabeto:
                    pu = self.transicoes[(v, a)]
                    pv = self.transicoes[(r, a)]
                    if pu != pv:
                        try:
                            if dic[(pu, pv)] == "-": #se nao esta marcado adiciona na lista
                                lista.append([(pu, pv), (v, r)])
                            else: #se esta marcado, entao marca o par (v, r) e se este encabeca uma lista marcar o outro par
                                dic[(v, r)] = "+"
                                for j in lista:
                                    if j[0] == (pu, pv) or j[0] == (pv, pu) or j[0] == (v, r):
                                        dic[j[1]] = "+"
                        except KeyError:
                            if dic[(pv, pu)] == "-": #se nao esta marcado adiciona na lista
                               lista.append([(pv, pu), (v, r)])
                            else: #se esta marcado, entao marca o par (v, r) e se este encabeca uma lista marcar o outro par
                                dic[(v, r)] = "+"
                                for j in lista:
                                    if j[0] == (pu, pv) or j[0] == (pv, pu) or j[0] == (v, r):
                                        dic[j[1]] = "+"

        listaFinal = []
        for v, r in dic.keys():
            if dic[(v, r)] == "-":
                listaFinal.append((v, r))

        return listaFinal
    
    #Para gerar o AFD minimizado
    def getEstadosMin(self, lista):
        estados = list(self.estados)

        for i, j in lista:
            estados.remove(i)
            estados.remove(j)
            estados.append("{" + i + "," + j + "}")

        return estados

    def getEIMin(self, lista):
        ei = self.estadoInicial

        for i, j in lista:
            if i == ei or j == ei:
                ei = "{" + i + "," + j + "}"
                break

        return ei

    def getEFMin(self, lista):
        ef = list(self.estadosFinais)

        for i, j in lista:
            if i in ef and j in ef:
                ef.remove(i)
                ef.remove(j)
                ef.append("{" + i + "," + j + "}")

        return ef

    def getTransicoesMin(self, lista):
        dic = {x: x for x in self.estados}
        resultado = {}

        for i, j in lista:
            dic[i] = "{" + i + "," + j + "}"
            dic[j] = "{" + i + "," + j + "}"

        for i, j in self.transicoes.keys():
            resultado[(dic[i], j)] = dic[self.transicoes[(i, j)]]

        return resultado
