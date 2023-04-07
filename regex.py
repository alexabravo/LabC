class Regex:
    def __init__(self, expresion_regular):
        self.expresion_regular =  expresion_regular


    def alfabeto(self, string):
        operadores = ['*', '+','?', 'ß', "|", "(", ")"]
        caracteres = []
        for x in string:
            if x not in operadores and x not in caracteres:
                caracteres.append(x)
        
        return caracteres

def regex_to_postfix(user_input):
    precedencia= {'|':1,'ß':2,'*':3,'+':3,'?':3,'(':-1,')':-1}
    operadores = ['|','*','+','?','ß']
    output = []
    pila = []
    for token in user_input:
        if token in operadores:
            while (len(pila)>0 and precedencia[token] <= precedencia[pila[-1]]):
                output.append(pila.pop())
            pila.append(token)
        else:
            if token != '(' and token != ')':
                output.append(token)
            elif token == '(':
                pila.append(token)
            elif token == ')':
                while (len(pila)>0 and pila[-1] != '('):
                    output.append(pila.pop())
                pila.pop()
    while (len(pila)>0):
        output.append(pila.pop())
    return output
