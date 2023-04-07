import sys
from lexer import *

def main(): 
    archivo = sys.argv[1] if len(sys.argv) > 1 else input('Ingrese el nombre de su archivo: ')
    contenidoYAL = readYalex(archivo)
    contenido = limpiarComentarios(contenidoYAL)
    print(contenido)

    ARCHIVO = len(contenido)

    letA = automataDirectoDet(list('let'))
    espaciosA = automataDirectoDet(list('(\n|\t| )+'))
    idA = automataDirectoDet(list('(' + concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|_)+'))
    eqA = automataDirectoDet(list('='))
    lLlave = automataDirectoDet(list('['))
    rLlave = automataDirectoDet(list(']'))
    lParen = automataDirectoDet(['\\('])
    rParen = automataDirectoDet(['\\)'])
    operadores = automataDirectoDet(['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'])
    caracterA = automataDirectoDet(["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"] +['|']+ list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126)))))
    stringA = automataDirectoDet(['"','(','('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list('('+chr(33) + ')|' + concatenarOr(caracteresRango(chr(35), chr(39)))+ '|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')','+',')','"'] +['|']+ list('('+chr(33) + ')|' + concatenarOr(caracteresRango(chr(35), chr(39)))+ '|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126)))))
    caracterEquis = automataDirectoDet(list('_'))
    rangeAa = automataDirectoDet(['('] + ["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"]+[')','-','('] + ["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"]+[')'])
    ruleA = automataDirectoDet(list('rule'))
    operadoresInvalidos = automataDirectoDet(["'"] + ['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ["'"])

    instancias = [letA, espaciosA, idA, eqA, lLlave, rLlave, lParen, rParen, operadores, caracterA, stringA, caracterEquis, rangeAa, ruleA, operadoresInvalidos]
    for instancia in instancias:
        instancia.reSimulacion()
    
    posicionActual = 0
    lastPosicionInicial = 0
    lastPosicionAceptada = 0
    ultimosAceptados = []
    tokensEncontrados = []

    
    while (posicionActual < ARCHIVO):
        dummyTokens = []
        
        letAEstado = letA.simulacion(contenido[posicionActual])
        espaciosAEstado = espaciosA.simulacion(contenido[posicionActual])
        idAEstado = idA.simulacion(contenido[posicionActual])
        eqAEstado = eqA.simulacion(contenido[posicionActual])
        lLlaveEstado = lLlave.simulacion(contenido[posicionActual])
        rLlaveEstado = rLlave.simulacion(contenido[posicionActual])
        lParenEstado = lParen.simulacion(contenido[posicionActual])
        rParenEstado = rParen.simulacion(contenido[posicionActual])
        operadoresEstado = operadores.simulacion(contenido[posicionActual])
        caracterAEstado = caracterA.simulacion(contenido[posicionActual])
        stringAEstado = stringA.simulacion(contenido[posicionActual])
        caracterEquisEstado = caracterEquis.simulacion(contenido[posicionActual])
        rangeAEstado = rangeAa.simulacion(contenido[posicionActual])
        ruleAEstado = ruleA.simulacion(contenido[posicionActual])
        operadoresInvalidosEstado = operadoresInvalidos.simulacion(contenido[posicionActual])

        if espaciosAEstado == 1 and posicionActual+1 <= ARCHIVO:
            lastPosicionInicial = lastPosicionAceptada = posicionActual+1
                
        if espaciosAEstado == -1:
            if lastPosicionAceptada == posicionActual:

                letA.reSimulacion()
                letAEstado = letA.simulacion(contenido[posicionActual])
                espaciosA.reSimulacion()
                espaciosAEstado = espaciosA.simulacion(contenido[posicionActual])
                idA.reSimulacion()
                idAEstado = idA.simulacion(contenido[posicionActual])
                eqA.reSimulacion()
                eqAEstado = eqA.simulacion(contenido[posicionActual])
                lLlave.reSimulacion()
                lLlaveEstado = lLlave.simulacion(contenido[posicionActual])
                rLlave.reSimulacion()
                rLlaveEstado = rLlave.simulacion(contenido[posicionActual])
                lParen.reSimulacion()
                lParenEstado = lParen.simulacion(contenido[posicionActual])
                rParen.reSimulacion()
                rParenEstado = rParen.simulacion(contenido[posicionActual])
                operadores.reSimulacion()
                operadoresEstado = operadores.simulacion(contenido[posicionActual])
                caracterA.reSimulacion()
                caracterAEstado = caracterA.simulacion(contenido[posicionActual])
                stringA.reSimulacion()
                stringAEstado = stringA.simulacion(contenido[posicionActual])
                caracterEquis.reSimulacion()
                caracterEquisEstado = caracterEquis.simulacion(contenido[posicionActual])
                rangeAa.reSimulacion()
                rangeAEstado = rangeAa.simulacion(contenido[posicionActual])
                ruleA.reSimulacion()
                ruleAEstado = ruleA.simulacion(contenido[posicionActual])
                operadoresInvalidos.reSimulacion()
                operadoresInvalidosEstado = operadoresInvalidos.simulacion(contenido[posicionActual])


        estado_tokens = {
            1: 'LET',
            2: 'RULE',
            3: 'EXTRA',
            4: 'ID',
            5: 'EQUAL',
            6: 'L-LLAVE',
            7: 'R-LLAVE',
            8: 'LPAREN',
            9: 'RPAREN',
            10: 'OPERADOR',
            11: 'OPERADOR-INVALIDO',
            12: 'CARACTER',
            13: 'STRING',
            14: 'RANGO'
        }
         
        for estado, token in estado_tokens.items():
            if estado == 1 and letAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 2 and ruleAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 3 and caracterEquisEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 4 and idAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 5 and eqAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 6 and lLlaveEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 7 and rLlaveEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 8 and lParenEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 9 and rParenEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 10 and operadoresEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 11 and operadoresInvalidosEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 12 and caracterAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 13 and stringAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual
            elif estado == 14 and rangeAEstado == 1:
                dummyTokens.append(token)
                lastPosicionAceptada = posicionActual

        if len(dummyTokens) > 0:
            ultimosAceptados = dummyTokens.copy()
            

        if((letAEstado==-1)and (espaciosAEstado==-1) and (idAEstado==-1) and (eqAEstado==-1) and (lLlaveEstado==-1) and (rLlaveEstado==-1) and (lParenEstado==-1) and (rParenEstado==-1) and (operadoresEstado==-1) and (caracterAEstado==-1) and (stringAEstado==-1) and (caracterEquisEstado==-1) and (rangeAEstado==-1)):
           
            tokensEncontrados.append((contenido[lastPosicionInicial:lastPosicionAceptada+1], ultimosAceptados[0]))
            
            instancias = [letA, espaciosA, idA, eqA, lLlave, rLlave, lParen, rParen, operadores, caracterA, stringA, caracterEquis, rangeAa, ruleA, operadoresInvalidos]

            for instancia in instancias:
                instancia.reSimulacion()

            lastPosicionInicial = posicionActual

        else:
            posicionActual += 1
        
        if (posicionActual == len(contenido) and espaciosAEstado !=1 ): 
            tokensEncontrados.append((contenido[lastPosicionInicial:lastPosicionAceptada+1], ultimosAceptados[0]))

    Lets = {}
    outputActual = []
    idActual = str()
    idDeclarado = False
    letDeclarado = False
    llavesContadas = 0
    primero = False
    for token in tokensEncontrados:
        if token[1] == 'LET':
            if(len(outputActual) > 0):
                Lets[idActual] = outputActual
            outputActual = []
            idActual = str()
            idDeclarado = True
            letDeclarado = True

        elif token[1] == 'ID':
            if idDeclarado:
                idActual = token[0]
            else:
                outputActual = outputActual + Lets[token[0]]
        
        elif token[1] == 'EQUAL':
            idDeclarado = False

        elif token[1] == 'RULE':
            if(len(outputActual) > 0):
                Lets[idActual] = outputActual
            outputActual = []
            idActual = str()
            idDeclarado = True
            letDeclarado = False
        
        elif token[1] == 'L-LLAVE':
            outputActual.append('(')
            primero = True
            llavesContadas += 1
        
        elif token[1] == 'R-LLAVE':
            outputActual.append(')')
            llavesContadas -= 1

        elif token[1] == 'LPAREN':
            outputActual.append('(')
        
        elif token[1] == 'RPAREN':
            outputActual.append(')')
        
        
        elif token[1] == 'OPERADOR':
            outputActual.append(token[0])
        elif token[1] == 'OPERADOR-INVALIDO':
            if llavesContadas > 0:
                if primero:
                    primero = False
                    outputActual.append('\\'+token[0][1])
                else:
                    outputActual.append('|')
                    outputActual.append('\\'+token[0][1])
            else:
                outputActual.append('\\'+token[0][1])
        elif token[1] == 'CARACTER':
            if llavesContadas > 0:
                if primero:
                    primero = False
                    outputActual.append(token[0][1])
                else:
                    outputActual.append('|')
                    outputActual.append(token[0][1])
            else:
                outputActual.append(token[0][1]) 
        elif token[1] == 'STRING':
            cantidadString = len(token[0])
            stringtReconocido = token[0][1:cantidadString-1]
            if llavesContadas > 0:
                if primero:
                    primero = False
                    outputActual = outputActual + concatenarCadenaOr(operadoresExcluidos(list(stringtReconocido)))
                else:
                    outputActual.append('|')
                    outputActual = outputActual + concatenarCadenaOr(operadoresExcluidos(list(stringtReconocido)))

            else:
                outputActual.append('(')
                outputActual = outputActual + operadoresExcluidos(list(stringtReconocido))
                outputActual.append(')')
        elif token[1] == 'RANGO':
            cantidadRango = len(token[0])
            cadenaRango = concatenarCadenaOr(operadoresExcluidos(caracteresRango(token[0][1], token[0][cantidadRango-2])))
            if llavesContadas > 0:
                if primero:
                    primero = False
                    outputActual = outputActual + cadenaRango
                else:
                    outputActual.append('|')
                    outputActual = outputActual + cadenaRango
            else:
                outputActual = outputActual + cadenaRango
        elif token[1] == 'EXTRA':
            if llavesContadas > 0:
                if primero:
                    primero = False
                    outputActual = outputActual + ['('] + ["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"] +['|']+ list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126)))) + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')']
                else:
                    outputActual.append('|')
                    outputActual = outputActual + ['('] + ["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"] +['|']+ list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126)))) + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')']
            else:
                outputActual = outputActual + ['('] + ["'",'('] + ['('] + list(concatenarOr(caracteresRango('a','z'))+'|'+concatenarOr(caracteresRango('A','Z'))+'|'+concatenarOr(caracteresRango('0','9'))+'|'+'(\n|\t| )'+'|')+['(','\\*','|','\\+','|', '\\?','|','\\|', '|','\\(','|','\\)',')'] + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')'] + [')',"'"] +['|']+ list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126)))) + ['|'] +list(concatenarOr(caracteresRango(chr(33), chr(38))) +'|'+ concatenarOr(caracteresRango(chr(44), chr(47)))+'|'+concatenarOr(caracteresRango(chr(58), chr(62))) + '|('+chr(64) + ')|' + concatenarOr(caracteresRango(chr(91), chr(96))) + '|(' + chr(123) + ')|' + concatenarOr(caracteresRango(chr(125), chr(126))))+[')']


    resultadoArbolFinal = arbolFinal(outputActual)
    print('Su árbol se genero exitosamente!')

if __name__ == "__main__":
    main()