# ---------------------------------------------------
# Tradutor para a linguagem CALC
#
# versao 1a (mar-2024)
# ---------------------------------------------------
from lexico import TOKEN, Lexico


class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico

    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        try:
            self.p()
        except:
            pass

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f"Erro na linha {linha}, coluna {coluna}")
            print(f"Era esperado {msgTokenAtual} mas veio {msgTokenLido}")
            raise Exception

    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.tokenLido
        while token != TOKEN.eof:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.tokenLido

    # --------------------------------- a partir daqui vamos seguir a gramática -------------------------------------
    def p(self):
        # <p> --> program ident ; <declaracoes> <corpo> .
        self.consome(TOKEN.PROGRAM)
        self.consome(TOKEN.ident)
        self.consome(TOKEN.ptoVirg)
        self.declaracoes()
        self.corpo()
        self.consome(TOKEN.pto)

    def declaracoes(self):
        #< declaracoes > -> LAMBDA | var < listavars >;
        if self.tokenLido == TOKEN.VAR:
            self.consome(TOKEN.VAR)
            self.listavars()
            self.consome(TOKEN.ptoVirg)
        else:
            pass

    def listavars(self):
        # <listavars> -> ident <restoListavars>
        self.consome(TOKEN.ident)
        self.restoListavars()

    def restoListaVars(self):
        # <restoListavars> -> LAMBDA | , <listavars>
        if self.tokenLido == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.listavars()
        else:
            pass

    def corpo(self):
        #<corpo> -> begin <cons> end
        self.consome(TOKEN.BEGIN)
        self.cons()
        self.consome(TOKEN.END)

    def cons(self):
        #<cons> -> LAMBDA | <com> <cons>
        if self.tokenLido in [TOKEN.ident,TOKEN.IF,TOKEN.WHILE,TOKEN.READ,TOKEN.PRINT]:
            self.com()
            self.cons()
        else:
            pass

    def com(self):
        #<com> -> <atrib> | <if> | <while> | <ler> | <escrever> | <bloco>
        if self.tokenLido == TOKEN.atrib:
            self.atrib()
        elif self.tokenLido == TOKEN.IF:
            self.se()
        elif self.tokenLido == TOKEN.WHILE:
            self.enquanto()
        elif self.tokenLido == TOKEN.READ:
            self.ler()
        elif self.tokenLido == TOKEN.PRINT:
            self.escrever()
        else:
            self.bloco()

    def atrib(self):
        #<atrib> -> ident = <exp> ;
        self.consome(TOKEN.ident)
        self.consome(TOKEN.atrib)
        self.exp()
        self.consome(TOKEN.ptoVirg)
    def se(self):
        #<if> -> if ( <exp> ) <com> <elseopc>
        self.consome(TOKEN.IF)
        self.consome(TOKEN.abrePar)
        self.exp()
        self.consome(TOKEN.fechaPar)
        self.com()
        self.elseopc()

    def elseopc(self):
        #<elseopc> -> LAMBDA | else <com>
        if self.tokenLido == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.com()
        else:
            pass
    def bloco(self):
        #<bloco> -> { <cons> }
        self.consome(TOKEN.abreChave)
        self.cons()
        self.consome(TOKEN.fechaChave)
    def ler(self):
        #<ler> -> read ( string , ident ) ;
        self.consome(TOKEN.READ)
        self.consome(TOKEN.abrePar)
        self.consome(TOKEN.string)
        self.consome(TOKEN.virg)
        self.consome(TOKEN.ident)
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
    def escrever(self):
        #<escrever> -> print ( <msg> ) ;
        self.consome(TOKEN.PRINT)
        self.consome(TOKEN.abrePar)
        self.msg()
        self.consome(TOKEN.fechaPar)
        self.consome(TOKEN.ptoVirg)
    def msg(self):
        #<msg> -> <coisa> <restomsg>
        self.coisa()
        self.restomsg()

    def coisa(self):
        #<coisa> -> string | ident
        if self.tokenLido == TOKEN.string:
            self.consome(TOKEN.string)
        else:
            self.consome(TOKEN.ident)

    def restomsg(self):
        #<restomsg> -> LAMBDA | , <msg>
        if self.tokenLido == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.msg()
        else:
            pass
    def enquanto(self):
        #<while> -> while ( <exp> ) <com>
        self.consome(TOKEN.WHILE)
        self.consome(TOKEN.abrePar)
        self.consome(TOKEN.fechaPar)
        self.exp()
        self.com()
    def exp(self):
        #<exp> -> <or>
        self.ou()

    def ou(self):
        #<or> -> <and> <restoOr>
        self.e()
        self.restoOr()

    def restoOr(self):
       #<restoOr> -> or <and> <restoOr> | LAMBDA
        if self.tokenLido == TOKEN.OR:
            self.consome(TOKEN.OR)
            self.e()
            self.restoOr()
        else:
            pass

    def e(self):
        #<and> -> <not> <restoAnd>
        self.nao()
        self.restoAnd()

    def restoAnd(self):
        #<restoAnd> -> and <not> <restoAnd> | LAMBDA
        if self.tokenLido == TOKEN.AND:
            self.consome(TOKEN.AND)
            self.nao()
            self.restoAnd()
        else:
            pass

    def nao(self):
        #<not> -> not <not> | <rel>
        if self.tokenLido == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.nao()
        else:
            self.rel()

    def rel(self):
        #<rel> -> <uno> <restoRel>
        self.uno()
        self.restoRel()

    def restoRel(self):
        #<restoRel> -> LAMBDA | <oprel> <uno>
        if self.tokenLido in [TOKEN.igual,TOKEN.diferente,TOKEN.menor,
                              TOKEN.menorIgual,TOKEN.maior,TOKEN.maiorIgual]:
            self.oprel()
            self.uno()
        else:
            pass

    def oprel(self):
        #<oprel> -> == | != | < | > | <= | >=
        if self.tokenLido == TOKEN.igual:
            self.consome(TOKEN.igual)
        elif self.tokenLido == TOKEN.diferente:
            self.consome(TOKEN.diferente)
        elif self.tokenLido == TOKEN.menor:
            self.consome(TOKEN.menor)
        elif self.tokenLido == TOKEN.maior:
            self.consome(TOKEN.maior)
        elif self.tokenLido == TOKEN.menorIgual:
            self.consome(TOKEN.menorIgual)
        elif self.tokenLido == TOKEN.maiorIgual:
            self.consome(TOKEN.maiorIgual)

    def uno(self):
        #<uno> -> + <uno> | - <uno> | <soma>
        if self.tokenLido == TOKEN.mais:
            self.consome(TOKEN.mais)
            self.uno()
        elif self.tokenLido == TOKEN.menos:
            self.consome(TOKEN.menos)
            self.uno()
        else:
            self.soma()

    def soma(self):
        #<soma> -> <mult> <restosoma>
        self.mult()
        self.restosoma()

    def restosoma(self):
        #<restosoma> -> + <mult> <restosoma> | - <mult> <restosoma> | LAMBDA
        if self.tokenLido == TOKEN.mais:
            self.consome(TOKEN.mais)
            self.mult()
            self.restosoma()
        elif self.tokenLido == TOKEN.menos:
            self.consome(TOKEN.menos)
            self.mult()
            self.restosoma()
        else:
            pass

    def mult(self):
        #<mult> -> < folha > < restomult >
        self.folha()
        self.restomult()

    def restomult(self):
        #< restomult > -> * < folha > < restomult > | / < folha > < restomult > | LAMBDA
        if self.tokenLido == TOKEN.multiplica:
            self.consome(TOKEN.multiplica)
            self.folha()
            self.restomult()
        elif self.tokenLido == TOKEN.divide:
            self.consome(TOKEN.divide)
            self.folha()
            self.restomult()
        else:
            pass

    def folha(self):
        # <folha> -> num | ident | ( <exp> )
        if self.tokenLido == TOKEN.num:
            self.consome(TOKEN.num)
        elif self.tokenLido == TOKEN.ident:
            self.consome(TOKEN.ident)
        else:
            self.consome(TOKEN.abrepar)
            self.exp()
            self.consome(TOKEN.abrePar)

# inicia a traducao
if __name__ == "__main__":
    print("Para testar, chame o Tradutor")
