class Arbol:
    def __init__(self, raiz, firstPos = None, lastPos = None, nullable = None):
        self.key = raiz
        self.hijoI = None
        self.hijoR = None
        self.firstPos = firstPos
        self.lastPos = lastPos
        self.nullable = nullable

def arbolSimple(postfix):
    operadores1 = ['*','+','?']
    operadores2 = ['|','ß']
    pila = []
    for token in postfix:
        if token not in operadores1 and token not in operadores2:
            pila.append(Arbol(token))
        elif token in operadores2:
            operadorArbol = Arbol(token)
            operadorArbol.hijoR = pila.pop()
            operadorArbol.hijoI = pila.pop()
            pila.append(operadorArbol)
        elif token in operadores1:
            operadorArbol = Arbol(token)
            operadorArbol.hijoI = pila.pop()
            pila.append(operadorArbol)
    return pila.pop()


def arbolDirecto(postfix):
    operadores1 = ['*','+','?']
    operadores2 = ['|','ß']
    pila = []
    posicionHoja =[]
    tablaFp = []
    
    for token in postfix:
        if token not in operadores1 and token not in operadores2:
            if token == 'ε':
                pila.append(Arbol(token, set(), set(), True))
            else:
                pila.append(Arbol(token, {len(posicionHoja)}, {len(posicionHoja)}, False))
                posicionHoja.append(token)
                tablaFp.append(set())

        elif token in operadores2:
            operadorArbol = Arbol(token)
            operadorArbol.hijoR = pila.pop()
            operadorArbol.hijoI = pila.pop()

            if token == '|':
                operadorArbol.nullable = operadorArbol.hijoI.nullable or operadorArbol.hijoR.nullable
                operadorArbol.firstPos = operadorArbol.hijoI.firstPos.union(operadorArbol.hijoR.firstPos)
                operadorArbol.lastPos = operadorArbol.hijoI.lastPos.union(operadorArbol.hijoR.lastPos)
            elif token == 'ß':
                operadorArbol.nullable = operadorArbol.hijoI.nullable and operadorArbol.hijoR.nullable
                if operadorArbol.hijoI.nullable:
                    operadorArbol.firstPos = operadorArbol.hijoI.firstPos.union(operadorArbol.hijoR.firstPos)
                else:
                    operadorArbol.firstPos = operadorArbol.hijoI.firstPos.copy()
                if operadorArbol.hijoR.nullable:
                    operadorArbol.lastPos = operadorArbol.hijoI.lastPos.union(operadorArbol.hijoR.lastPos)
                else:
                    operadorArbol.lastPos = operadorArbol.hijoR.lastPos.copy()
                for c in operadorArbol.hijoI.lastPos:
                    tablaFp[c] = tablaFp[c].union(operadorArbol.hijoR.firstPos)
            pila.append(operadorArbol)

        elif token in operadores1:
            operadorArbol = Arbol(token)
            operadorArbol.hijoI = pila.pop()
            if token == '*':
                operadorArbol.nullable = True
                operadorArbol.firstPos = operadorArbol.hijoI.firstPos.copy()
                operadorArbol.lastPos = operadorArbol.hijoI.lastPos.copy()
                for c in operadorArbol.lastPos:
                    tablaFp[c] = tablaFp[c].union(operadorArbol.firstPos)
                
            elif token == '+':
                operadorArbol.nullable = operadorArbol.hijoI.nullable
                operadorArbol.firstPos = operadorArbol.hijoI.firstPos.copy()
                operadorArbol.lastPos = operadorArbol.hijoI.lastPos.copy()
                for c in operadorArbol.lastPos:
                    tablaFp[c] = tablaFp[c].union(operadorArbol.firstPos)
            elif token == '?':
                operadorArbol.nullable = True
                operadorArbol.firstPos = operadorArbol.hijoI.firstPos.copy()
                operadorArbol.lastPos = operadorArbol.hijoI.lastPos.copy()
            pila.append(operadorArbol)
    
    arbolResultante = Arbol('ß')
    arbolResultante.hijoI = pila.pop()
    arbolResultante.hijoR = Arbol('#', {len(posicionHoja)}, {len(posicionHoja)}, False)
    tablaFp.append(set())

    arbolResultante.nullable = arbolResultante.hijoI.nullable and arbolResultante.hijoR.nullable
    if arbolResultante.hijoI.nullable:
        arbolResultante.firstPos = arbolResultante.hijoI.firstPos.union(arbolResultante.hijoR.firstPos)
    else:
        arbolResultante.firstPos = arbolResultante.hijoI.firstPos.copy()
    if arbolResultante.hijoR.nullable:
        arbolResultante.lastPos = arbolResultante.hijoI.lastPos.union(arbolResultante.hijoR.lastPos)
    else:
        arbolResultante.lastPos = arbolResultante.hijoR.lastPos.copy()
    for c in arbolResultante.hijoI.lastPos:
        tablaFp[c] = tablaFp[c].union(arbolResultante.hijoR.firstPos)

    return arbolResultante, tablaFp, posicionHoja

def graficarArbol(arbol, grafo):
    if arbol:
        if arbol.hijoI:
            grafo.edge(str(id(arbol)), str(id(arbol.hijoI)))
            graficarArbol(arbol.hijoI, grafo)
        if arbol.hijoR:
            grafo.edge(str(id(arbol)), str(id(arbol.hijoR)))
            graficarArbol(arbol.hijoR, grafo)
        node_label = r"'{}'".format(arbol.key)
        grafo.node(str(id(arbol)), node_label)
    else:
        return
    
class Automata:
    def __init__(self, estados, alfabeto, transiciones, estadoInicial, estadoFinal):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transiciones = transiciones
        self.estadoInicial = estadoInicial
        self.estadoFinal = estadoFinal
        self.estadoSimulacionActual = -1

    def movimiento(self, estado, operador):
        return [transicion[1] for transicion in self.transiciones if transicion[0] == (estado, operador)]
    
    def movimientoUnico(self, estado, operador):
        for transicion in self.transiciones:
            if transicion[0] == (estado, operador):
                self.estadoSimulacionActual = transicion[1]
                return transicion[1]
        self.estadoSimulacionActual = -1
        return -1
    
    def epsilon_closure(self, estado):
        closure = [estado]
        for closure_estado in closure:
            
            for transicion in self.transiciones:
                if transicion[0] == (closure_estado, 'ε'):
                    if transicion[1] not in closure:
                        closure.append(transicion[1])
        return closure
    
    def reSimulacion(self):
        self.estadoSimulacionActual = self.estadoInicial
    
    def simulacion(self, operador):
        if self.estadoSimulacionActual == -1:
            return -1
        next_estado = self.movimientoUnico(self.estadoSimulacionActual, operador)
        if next_estado == -1:
            return -1
        if self.estadoSimulacionActual in self.estadoFinal:
            return 1
        if self.estadoSimulacionActual not in self.estadoFinal:
            return 0

def transicionesDirectas(automata: Automata):
    operadoresDescartados = ['|', '(', ')', '*', '+', '?']
    transicionesNuevas = []
    alfabetoNuevo = set()
    for transicion in automata.transiciones:
        if len(transicion[0][1])==2 and transicion[0][1][0] == '\\' and transicion[0][1][1] in operadoresDescartados:
            transicionesNuevas.append(((transicion[0][0], transicion[0][1][1]), transicion[1]))
        else:
            transicionesNuevas.append(transicion)
    for token in automata.alfabeto:
        if len(token)== 2 and token[0] == '\\' and token[1] in operadoresDescartados:
            alfabetoNuevo.add(token[1])
        else:
            alfabetoNuevo.add(token)
    automata.alfabeto = alfabetoNuevo
    automata.transiciones = transicionesNuevas


def construccionDirectaAutomata(tablaFp, estadoInicial, estadoFinal, cadenaAbc):
    abcDeterminista  = set(cadenaAbc)
    estadosEquivalentes = [estadoInicial]
    posicionHoja = {character: [i for i in range(len(cadenaAbc)) if cadenaAbc[i] == character] for character in abcDeterminista}
    transicionesDir = []
    
    
    for estado in estadosEquivalentes:
        for operador in abcDeterminista:
            estadosSiguientes = []
            estadosSiguientes = set([nfa for nfa in estado if nfa in posicionHoja[operador]])
            estadosTemp = []
            for nfa in estadosSiguientes:
                estadosTemp.extend(tablaFp[nfa])
            estadosSiguientes = set(estadosTemp)

            if len(estadosSiguientes) != 0:
                if estadosSiguientes not in estadosEquivalentes:
                    estadosEquivalentes.append(estadosSiguientes)
                transicionesDir.append(((estadosEquivalentes.index(estado), operador), estadosEquivalentes.index(estadosSiguientes)))

    estadoFinalEq = []
    for c in range(len(estadosEquivalentes)):
        for estadoFinalisimo in estadoFinal:
            if estadoFinalisimo in estadosEquivalentes[c]:
                estadoFinalEq.append(c)
                break
    return Automata([i for i in range(len(estadosEquivalentes))], abcDeterminista, transicionesDir, 0, estadoFinalEq)

