import os

from ttoken import TOKEN

class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte
        with open(self.arqFonte, 'r', encoding='utf-8') as f:
            self.fonte = f.read()
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None
        self.linha = 1
        self.coluna = 0
        self.arqLog = None


    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte
    
    def getchar(self):
        if self.fimDoArquivo():
            return '\0'
        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
        if car == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return car

    def ungetchar(self, simbolo):
        if simbolo == '\0':
            # o getchar no fim do arquivo nao avancou o indice,
            # logo nao ha nada para devolver
            return
        if simbolo == '\n':
            self.linha -= 1
        if self.indiceFonte > 0:
            self.indiceFonte -=1
        self.coluna -= 1

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        if self.arqLog is None:
            # primeiro token da execucao: cria logs/<fonte>_tokens.log do zero
            os.makedirs('logs', exist_ok=True)
            nomeFonte = os.path.splitext(os.path.basename(self.arqFonte))[0]
            self.arqLog = os.path.join('logs', f'{nomeFonte}_tokens.log')
            modo = 'w'
        else:
            modo = 'a'
        with open(self.arqLog, modo, encoding='utf-8') as log:
            log.write(f'(token = {msg}\t lex = "{lexema}" \t lin = {linha} col = {coluna})\n')

    def getToken(self):
        estado = 1
        lexema = ''

        # descarta brancos e quebras de linha ANTES de marcar onde o token
        # comeca, senao lin/col apontam para o espaco em vez do lexema
        simbolo = self.getchar()
        while simbolo in [' ', '\t', '\n', '\r']:
            simbolo = self.getchar()

        lin = self.linha
        col = self.coluna

        while(True):
            if estado == 1:
                if simbolo.isalpha():
                    estado = 2 #idents, pal.reservadas
                
                elif simbolo.isdigit():
                    estado = 3 #numeros
                
                elif simbolo == '/':  # pode ser divisão ou comentário
                    estado = 4
                
                elif simbolo == '=': # verificar se é comparação ou atribuição
                    estado = 5

                elif simbolo == '<':
                    estado = 6

                elif simbolo == '>':
                    estado = 7

                elif simbolo == '\'':
                    estado = 8
                
                elif simbolo == '\"':
                    estado = 9

                elif simbolo == '!':
                    estado = 10
                elif simbolo == '+': # pode ser soma ou incremento
                    estado = 13

                elif simbolo == '-': # pode ser subtração ou decremento
                    estado = 14

                elif simbolo == '[':
                    return (TOKEN.ABRE_COLCHETES, simbolo, lin, col)

                elif simbolo == ']':
                    return (TOKEN.FECHA_COLCHETES, simbolo, lin, col)

                elif simbolo == '&':
                    return (TOKEN.REFERENCIA, simbolo, lin, col)

                elif simbolo == '*':
                    return (TOKEN.MULTIPLICACAO, simbolo, lin, col)
                
                elif simbolo == '(':
                    return(TOKEN.ABRE_PARENTESES, simbolo, lin, col)
                
                elif simbolo == ')':
                    return(TOKEN.FECHA_PARENTESES, simbolo, lin, col)
                
                elif simbolo == '{':
                    return(TOKEN.ABRE_CHAVES, simbolo, lin, col)
                
                elif simbolo == '}':
                    return(TOKEN.FECHA_CHAVES, simbolo, lin, col)
                
                elif simbolo == ',':
                    return (TOKEN.VIRGULA, simbolo, lin, col)

                elif simbolo == ';':
                    return (TOKEN.PONTO_VIRGULA, simbolo, lin, col)
                
                elif simbolo == '.':
                    return (TOKEN.PONTO, simbolo, lin, col)

                elif simbolo == '\0':
                    return (TOKEN.EOF, '', self.linha, self.coluna)
                
                elif simbolo in [' ', '\t', '\n', '\r']:
                    # ignora brancos e quebras de linha
                    lexema = ''
                    estado = 1
                else:
                    # qualquer outro caractere não reconhecido é erro
                    estado = 0

            elif estado == 2:
                if simbolo.isalnum():
                    estado = 2
                else:
                    self.ungetchar(simbolo)
                    token = TOKEN.reservada(lexema)
                    return (token, lexema, lin, col)
            
            elif estado == 3: # parte inteira do numero
                if simbolo.isdigit():
                    estado = 3
                elif simbolo == '.': # aqui entra o ponto: o numero pode virar float
                    estado = 11
                elif simbolo.isalpha():
                    estado = 0 # erro, numero nao pode conter letras
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.VALORINT, lexema, lin, col)

            elif estado == 11: # leu "digitos." e precisa de ao menos um digito depois
                if simbolo.isdigit():
                    estado = 12
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.ERRO, lexema, lin, col) # "10." nao e float valido

            elif estado == 12: # parte fracionaria
                if simbolo.isdigit():
                    estado = 12
                elif simbolo == '.' or simbolo.isalpha():
                    estado = 0 # "1.2.3" e "1.2a" sao erros
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.VALORFLOAT, lexema, lin, col)

            elif estado == 4:
                if simbolo == '/':  # é comentário
                    # descarta até fim da linha
                    while simbolo != '\n' and simbolo != '\0':
                        simbolo = self.getchar()
                    return self.getToken()  # continua analisando depois do comentário
                else:
                    self.ungetchar(simbolo)  # não era comentário, devolve o caractere
                    return (TOKEN.DIVISAO, lexema, lin, col)
                
            elif estado == 5:
                if simbolo == '=':
                    lexema += simbolo
                    return (TOKEN.IGUAL, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era igualdade, devolve o caractere
                    return (TOKEN.ATRIBUICAO, lexema, lin, col)
            
            elif estado == 6:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.MENOR_IGUAL, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era menorIgual, devolve o caractere
                    return (TOKEN.MENOR, lexema, lin, col)
            elif estado == 7:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.MAIOR_IGUAL, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era maiorIgual, devolve o caractere
                    return (TOKEN.MAIOR, lexema, lin, col)
            elif estado == 8: # string entre aspas simples
                if simbolo == "'":
                    lexema += simbolo
                    return (TOKEN.VALORSTRING, lexema, lin, col)
                elif simbolo == '\n' or simbolo == '\0':
                    # string nao fechada: devolve o caractere para nao
                    # engolir a quebra de linha nem o fim do arquivo
                    self.ungetchar(simbolo)
                    return (TOKEN.ERRO, lexema, lin, col)

            elif estado == 9: # string entre aspas duplas
                if simbolo == '"':
                    lexema += simbolo
                    return (TOKEN.VALORSTRING, lexema, lin, col)
                elif simbolo == '\n' or simbolo == '\0':
                    self.ungetchar(simbolo)
                    return (TOKEN.ERRO, lexema, lin, col)

            elif estado == 10:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.DIFERENTE, lexema, lin, col)
                else:
                    estado = 0 # não era diferente, erro

            elif estado == 13:
                if simbolo == '+':
                    lexema += simbolo
                    return (TOKEN.INCREMENTO, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era incremento, devolve o caractere
                    return (TOKEN.SOMA, lexema, lin, col)

            elif estado == 14:
                if simbolo == '-':
                    lexema += simbolo
                    return (TOKEN.DECREMENTO, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era decremento, devolve o caractere
                    return (TOKEN.SUBTRACAO, lexema, lin, col)

            elif estado == 0:
                if simbolo == '.' or simbolo.isalpha() or simbolo.isdigit():
                    estado = 0
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.ERRO, lexema, lin, col)
                
            if simbolo not in ['\n', '\r']:
                if estado == 8 or estado == 9: # quando for string ele mantém os espaços em branco no lexema
                    lexema += simbolo # evita adicionar quebra de linha
                else:
                    if simbolo not in [' ', '\t']: #quando não é string ele retira os espaços em branco do lexema
                        lexema += simbolo  
            simbolo = self.getchar()

if __name__ == '__main__':
    lexico = Lexico("sampleTest.txt")
    token = lexico.getToken()
    while(token[0] != TOKEN.EOF):
        lexico.imprimeToken(token)
        token = lexico.getToken()
    lexico.imprimeToken(token)
    print(f'Tokens gravados em {lexico.arqLog}')