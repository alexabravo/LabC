from graphviz import Digraph

from arbol import *
from regex import *

def convertir(user_input):
    operadores = ['|','*','+','?']
    resultado = []
    for c in range(len(user_input)):
        if (c != 0):
            if (user_input[c-1] not in operadores and user_input[c-1] != '('  and user_input[c] == '('):
                resultado.append('ß')
                resultado.append(user_input[c])
            elif (user_input[c-1] in operadores[1:] and user_input[c] not in operadores and user_input[c] != ')'):
                resultado.append('ß')
                resultado.append(user_input[c])
            elif (user_input[c-1] == ')' and user_input[c] not in operadores and user_input[c] != '(' and user_input[c] != ')'):
                resultado.append('ß')
                resultado.append(user_input[c])
            elif (user_input[c-1] not in operadores and user_input[c-1] != '(' and user_input[c-1] != ')' and user_input[c] not in operadores and user_input[c] != '(' and user_input[c] != ')'):
                resultado.append('ß')
                resultado.append(user_input[c])
            else:
                resultado.append(user_input[c])
        else:
            resultado.append(user_input[c])
    return resultado

def readYalex(path):
    with open(path, 'r', encoding='utf-8') as file:
        contenido = file.read()
        linebreak_sequence = file.newlines
        print((linebreak_sequence))
        file.close()
    return contenido

def limpiarLlaves(text):
    resultado = ''
    saltar = False
    ignorar = False
    for caracter in text:
        if ignorar:
            if caracter == 'n':
                resultado += '\n'
            elif caracter == 't':
                resultado += '\t'
            elif caracter == 's':
                resultado += ' '
            else:
                resultado += '\\' + caracter
            ignorar = False
        elif caracter == '\\':
            ignorar = True
        elif caracter == '{':
            saltar = True
        elif caracter == '}':
            saltar = False
        elif not saltar:
            resultado += caracter
    return resultado

def limpiarComentarios(raw_input):
    cadenaLimpia = ''
    aprobado = True
    for c in range(len(raw_input)):
        if raw_input[c] == '(':
            if (c+1 < len(raw_input) and raw_input[c+1] == '*'):
                aprobado = False
        elif raw_input[c] == ')':
            if (c-1 >= 0 and raw_input[c-1] == '*'):
                aprobado = True
                continue
        if aprobado:
            cadenaLimpia += raw_input[c]
    return limpiarLlaves(cadenaLimpia)

def concatenarCadenaOr(lista, operador = '|'):
    resultado = ['(']
    if len(lista) > 0:
        resultado.append(lista[0])
        for i in range(1, len(lista)):
            resultado.append(operador)
            resultado.append(lista[i])
    resultado.append(')')
    return resultado

def operadoresExcluidos(user_input):
    resultado = []
    operadores = ['|','*','+','?']
    for c in user_input:
        if c in operadores:
            resultado.append('\\' + c)
        else:
            resultado.append(c)
    return resultado

def caracteresRango(caracter1, caracter2):
    posicion1 = ord(caracter1)
    posicion2 = ord(caracter2)
    if posicion1 > posicion2: 
        posicion1, posicion2 = posicion2, posicion1
    return [chr(pos) for pos in range(posicion1, posicion2 + 1)]

def concatenarOr(lista):
    resultado = '('
    if len(lista) > 0:
        resultado += lista[0]
        for i in range(1, len(lista)):
            resultado += '|' + lista[i]
    return resultado+')'

def automataDirectoDet(user_input):
    user_input = convertir(user_input)
    output = regex_to_postfix(user_input)
    arbol, followpos, listaCaracteres = arbolDirecto(output)
    automataDeta = construccionDirectaAutomata(followpos, arbol.firstPos, arbol.lastPos, listaCaracteres)
    transicionesDirectas(automataDeta)
    return automataDeta

def concatenarString(cadenaString):
    resultado = ""
    for string in cadenaString:
        resultado += string
    return resultado

def arbolFinal(user_input):
    user_input = convertir(user_input)
    print('Expresion Regular: ', user_input)
    output = regex_to_postfix(user_input)
    print('Expresion Postfix: ', output)
    arbol = arbolSimple(output)
    grafo = Digraph(graph_attr={'dpi': str(200)})
    graficarArbol(arbol, grafo)
    grafo.render('arbol', format='png')
    return arbol



