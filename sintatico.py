from lexico import TOKEN, Lexico
class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico
        self.tokenLido = None
        self.tokenEspiado = None

    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        try:
            self.prog()
            self.consome(TOKEN.EOF)
        except SyntaxError:
            return False
        print("Analise sintatica concluida sem erros")
        return True

    def tokenAtual(self):
        return self.tokenLido[0]

    def espia(self):
        # devolve o token seguinte ao tokenLido sem consumir nenhum dos dois;
        # so o FOR precisa disso (ver comRepeticao)
        if self.tokenEspiado is None:
            self.tokenEspiado = self.lexico.getToken()
        return self.tokenEspiado[0]

    def consome(self, tokenEsperado):
        if self.tokenAtual() == tokenEsperado:
            if self.tokenEspiado is not None:
                self.tokenLido = self.tokenEspiado
                self.tokenEspiado = None
            else:
                self.tokenLido = self.lexico.getToken()
        else:
            self.erro(TOKEN.msg(tokenEsperado))

    def erro(self, esperado):
        (token, lexema, linha, coluna) = self.tokenLido
        print(f"Erro na linha {linha}, coluna {coluna}")
        if token == TOKEN.ERRO:
            print(f'Erro lexico: "{lexema}" nao e um token valido')
        else:
            print(f'Era esperado {esperado} mas veio {TOKEN.msg(token)} "{lexema}"')
        raise SyntaxError()

    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.tokenLido
        while token != TOKEN.EOF:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.tokenLido

    # ----------------------- a partir daqui vamos seguir a gramática -------------

    # ---------------------------------------- FUNCOES ----------------------------------------

    def prog(self):
        # Prog -> Func RestoProg
        self.func()
        self.restoProg()

    def restoProg(self):
        # RestoProg -> LAMBDA | Func RestoProg
        # LAMBDA quando o arquivo acaba
        if self.tokenAtual() != TOKEN.EOF:
            self.func()
            self.restoProg()
        else:
            pass

    def func(self):
        # Func -> TipoFunc IDENT ( ListaArgs ) Corpo
        self.tipoFunc()
        self.consome(TOKEN.IDENT)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.listaArgs()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.corpo()

    def tipoPrim(self):
        # TipoPrim -> INT | FLOAT | STRING
        if self.tokenAtual() == TOKEN.INT:
            self.consome(TOKEN.INT)
        elif self.tokenAtual() == TOKEN.FLOAT:
            self.consome(TOKEN.FLOAT)
        elif self.tokenAtual() == TOKEN.STRING:
            self.consome(TOKEN.STRING)
        else:
            self.erro("um tipo (int, float ou string)")

    def tipoFunc(self):
        # TipoFunc -> VOID | TipoPrim
        if self.tokenAtual() == TOKEN.VOID:
            self.consome(TOKEN.VOID)
        else:
            self.tipoPrim()

    def listaArgs(self):
        # ListaArgs -> LAMBDA | Arg RestoListaArgs
        # LAMBDA quando chega o ) que fecha os argumentos
        if self.tokenAtual() != TOKEN.FECHA_PARENTESES:
            self.arg()
            self.restoListaArgs()
        else:
            pass

    def restoListaArgs(self):
        # RestoListaArgs -> , Arg RestoListaArgs | LAMBDA
        if self.tokenAtual() == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.arg()
            self.restoListaArgs()
        else:
            pass

    def arg(self):
        # Arg -> TipoPrim OpcRef IDENT OpcColchete
        self.tipoPrim()
        self.opcRef()
        self.consome(TOKEN.IDENT)
        self.opcColchete()

    def opcColchete(self):
        # OpcColchete -> LAMBDA | [ ]
        if self.tokenAtual() == TOKEN.ABRE_COLCHETES:
            self.consome(TOKEN.ABRE_COLCHETES)
            self.consome(TOKEN.FECHA_COLCHETES)
        else:
            pass

    def opcRef(self):
        # OpcRef -> LAMBDA | &
        if self.tokenAtual() == TOKEN.REFERENCIA:
            self.consome(TOKEN.REFERENCIA)
        else:
            pass

    def corpo(self):
        # Corpo -> { ListaDeclar ListaCom }
        self.consome(TOKEN.ABRE_CHAVES)
        self.listaDeclar()
        self.listaCom()
        self.consome(TOKEN.FECHA_CHAVES)

    # ---------------------------------------- DECLARACOES ----------------------------------------

    def listaDeclar(self):
        # ListaDeclar -> LAMBDA | Declar ListaDeclar
        # declaracao sempre comeca com o tipo
        if self.tokenAtual() in [TOKEN.INT, TOKEN.FLOAT, TOKEN.STRING]:
            self.declar()
            self.listaDeclar()
        else:
            pass

    def declar(self):
        # Declar -> TipoPrim IDENT OpcColchete OpcInicializa ListaIdent ;
        self.tipoPrim()
        self.consome(TOKEN.IDENT)
        self.opcColchete()
        self.opcInicializa()
        self.listaIdent()
        self.consome(TOKEN.PONTO_VIRGULA)

    def listaIdent(self):
        # ListaIdent -> LAMBDA | , IDENT OpcColchete ListaIdent
        if self.tokenAtual() == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.consome(TOKEN.IDENT)
            self.opcColchete()
            self.listaIdent()
        else:
            pass

    def opcInicializa(self):
        # OpcInicializa -> LAMBDA | = Exp
        if self.tokenAtual() == TOKEN.ATRIBUICAO:
            self.consome(TOKEN.ATRIBUICAO)
            self.exp()
        else:
            pass

    # ---------------------------------------- COMANDOS ----------------------------------------

    def listaCom(self):
        # ListaCom -> LAMBDA | Com ListaCom
        # LAMBDA quando chega o } que fecha o bloco; o EOF entra para um
        # } esquecido virar "esperado }" em vez de erro no meio de um comando
        if self.tokenAtual() not in [TOKEN.FECHA_CHAVES, TOKEN.EOF]:
            self.com()
            self.listaCom()
        else:
            pass

    def com(self):
        # Com -> ComRepete | ComDecisao | ComIO | Exp ;
        # Com -> break ; | continue ; | return OpcExp ;
        # Com -> Bloco
        if self.tokenAtual() in [TOKEN.LOOP, TOKEN.WHILE, TOKEN.FOR]:
            self.comRepete()
        elif self.tokenAtual() == TOKEN.IF:
            self.comDecisao()
        elif self.tokenAtual() in [TOKEN.READ, TOKEN.WRITE]:
            self.comIO()
        elif self.tokenAtual() == TOKEN.BREAK:
            self.consome(TOKEN.BREAK)
            self.consome(TOKEN.PONTO_VIRGULA)
        elif self.tokenAtual() == TOKEN.CONTINUE:
            self.consome(TOKEN.CONTINUE)
            self.consome(TOKEN.PONTO_VIRGULA)
        elif self.tokenAtual() == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.opcExp()
            self.consome(TOKEN.PONTO_VIRGULA)
        elif self.tokenAtual() == TOKEN.ABRE_CHAVES:
            self.bloco()
        else:
            self.exp()
            self.consome(TOKEN.PONTO_VIRGULA)

    def bloco(self):
        # Bloco -> Corpo
        self.corpo()

    def comRepete(self):
        # ComRepete -> loop Bloco
        # ComRepete -> while ( Exp ) Bloco
        # ComRepete -> for ( RestoComRepete
        if self.tokenAtual() == TOKEN.LOOP:
            self.consome(TOKEN.LOOP)
            self.bloco()
        elif self.tokenAtual() == TOKEN.WHILE:
            self.consome(TOKEN.WHILE)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.exp()
            self.consome(TOKEN.FECHA_PARENTESES)
            self.bloco()
        else:
            self.consome(TOKEN.FOR)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.restoComRepete()

    def restoComRepete(self):
        # RestoComRepete -> ident in ident ) Bloco
        # RestoComRepete -> OpcExp ; OpcExp ; OpcExp ) Bloco
        # o OpcExp tambem pode comecar com ident ("a in v" e "a = 0"), entao
        # so o token depois do ident decide qual producao usar: por isso o espia()
        if self.tokenAtual() == TOKEN.IDENT and self.espia() == TOKEN.IN:
            self.consome(TOKEN.IDENT)
            self.consome(TOKEN.IN)
            self.consome(TOKEN.IDENT)
        else:
            self.opcExp()
            self.consome(TOKEN.PONTO_VIRGULA)
            self.opcExp()
            self.consome(TOKEN.PONTO_VIRGULA)
            self.opcExp()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.bloco()

    def comDecisao(self):
        # ComDecisao -> IF ( Exp ) Bloco ListaElif ElseOpc
        self.consome(TOKEN.IF)
        self.consome(TOKEN.ABRE_PARENTESES)
        self.exp()
        self.consome(TOKEN.FECHA_PARENTESES)
        self.bloco()
        self.listaElif()
        self.elseOpc()

    def listaElif(self):
        # ListaElif -> LAMBDA | ELIF ( Exp ) Bloco ListaElif
        if self.tokenAtual() == TOKEN.ELIF:
            self.consome(TOKEN.ELIF)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.exp()
            self.consome(TOKEN.FECHA_PARENTESES)
            self.bloco()
            self.listaElif()
        else:
            pass

    def elseOpc(self):
        # ElseOpc -> LAMBDA | ELSE Bloco
        if self.tokenAtual() == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.bloco()
        else:
            pass

    def comIO(self):
        # ComIO -> READ ( IDENT ) ; | WRITE ( ListaExp ) ;
        if self.tokenAtual() == TOKEN.READ:
            self.consome(TOKEN.READ)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.consome(TOKEN.IDENT)
            self.consome(TOKEN.FECHA_PARENTESES)
            self.consome(TOKEN.PONTO_VIRGULA)
        else:
            self.consome(TOKEN.WRITE)
            self.consome(TOKEN.ABRE_PARENTESES)
            self.listaExp()
            self.consome(TOKEN.FECHA_PARENTESES)
            self.consome(TOKEN.PONTO_VIRGULA)

    def listaExp(self):
        # ListaExp -> Exp RestoListaExp
        self.exp()
        self.restoListaExp()

    def restoListaExp(self):
        # RestoListaExp -> , Exp RestoListaExp | LAMBDA
        if self.tokenAtual() == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.exp()
            self.restoListaExp()
        else:
            pass

    # ---------------------------------------- EXPRESSOES ----------------------------------------

    def opcExp(self):
        # OpcExp -> LAMBDA | Zero
        # LAMBDA quando chega o que vem depois dela: ; (return e for) ou ) (for)
        if self.tokenAtual() not in [TOKEN.PONTO_VIRGULA, TOKEN.FECHA_PARENTESES]:
            self.zero()
        else:
            pass

    def exp(self):
        # Exp -> Zero
        self.zero()

    def zero(self):
        # Zero -> ++ Um | -- Um | Um
        if self.tokenAtual() == TOKEN.INCREMENTO:
            self.consome(TOKEN.INCREMENTO)
            self.um()
        elif self.tokenAtual() == TOKEN.DECREMENTO:
            self.consome(TOKEN.DECREMENTO)
            self.um()
        else:
            self.um()

    def um(self):
        # Um -> Dois RestoUm
        self.dois()
        self.restoUm()

    def restoUm(self):
        # RestoUm -> OR Dois RestoUm | LAMBDA
        if self.tokenAtual() == TOKEN.OR:
            self.consome(TOKEN.OR)
            self.dois()
            self.restoUm()
        else:
            pass

    def dois(self):
        # Dois -> Tres RestoDois
        self.tres()
        self.restoDois()

    def restoDois(self):
        # RestoDois -> AND Tres RestoDois | LAMBDA
        if self.tokenAtual() == TOKEN.AND:
            self.consome(TOKEN.AND)
            self.tres()
            self.restoDois()
        else:
            pass

    def tres(self):
        # Tres -> NOT Tres | Quatro
        if self.tokenAtual() == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.tres()
        else:
            self.quatro()

    def quatro(self):
        # Quatro -> Cinco Resto4
        self.cinco()
        self.resto4()

    def resto4(self):
        # Resto4 -> > Cinco | >= Cinco | < Cinco | <= Cinco
        # Resto4 -> == Cinco | != Cinco | LAMBDA
        if self.tokenAtual() in TOKEN.oprel():
            self.consome(self.tokenAtual())
            self.cinco()
        else:
            pass

    def cinco(self):
        # Cinco -> Seis RestoCinco
        self.seis()
        self.restoCinco()

    def restoCinco(self):
        # RestoCinco -> + Seis RestoCinco | - Seis RestoCinco | LAMBDA
        if self.tokenAtual() == TOKEN.SOMA:
            self.consome(TOKEN.SOMA)
            self.seis()
            self.restoCinco()
        elif self.tokenAtual() == TOKEN.SUBTRACAO:
            self.consome(TOKEN.SUBTRACAO)
            self.seis()
            self.restoCinco()
        else:
            pass

    def seis(self):
        # Seis -> Sete RestoSeis
        self.sete()
        self.restoSeis()

    def restoSeis(self):
        # RestoSeis -> LAMBDA | * Sete RestoSeis | / Sete RestoSeis
        # RestoSeis -> div Sete RestoSeis | mod Sete RestoSeis
        if self.tokenAtual() in [TOKEN.MULTIPLICACAO, TOKEN.DIVISAO, TOKEN.DIV, TOKEN.MOD]:
            self.consome(self.tokenAtual())
            self.sete()
            self.restoSeis()
        else:
            pass

    def sete(self):
        # Sete -> + Sete | - Sete | Oito
        if self.tokenAtual() == TOKEN.SOMA:
            self.consome(TOKEN.SOMA)
            self.sete()
        elif self.tokenAtual() == TOKEN.SUBTRACAO:
            self.consome(TOKEN.SUBTRACAO)
            self.sete()
        else:
            self.oito()

    def oito(self):
        # Oito -> ident OpcPos = Oito | Folha
        # Folha -> ident RestoFolha tambem comeca com ident, e nem espiando um
        # token da para decidir: "v[i] = 1" e "v[i] + 1" so se separam depois
        # do "]". Por isso o ident em comum foi fatorado:
        #   Oito       -> ident RestoIdent | Folha      (Folha sem o ident)
        #   RestoIdent -> ( ListaParam )                (RestoFolha da chamada)
        #               | OpcPos OpcAtrib               (RestoFolha LAMBDA / [ Zero ] e a atribuicao)
        #   OpcAtrib   -> = Oito | LAMBDA
        # OpcPos -> [ Exp ] e RestoFolha -> [ Zero ] sao iguais, ja que Exp -> Zero
        if self.tokenAtual() == TOKEN.IDENT:
            self.consome(TOKEN.IDENT)
            self.restoIdent()
        else:
            self.folha()

    def restoIdent(self):
        # RestoIdent -> ( ListaParam ) | OpcPos OpcAtrib
        if self.tokenAtual() == TOKEN.ABRE_PARENTESES:
            self.consome(TOKEN.ABRE_PARENTESES)
            self.listaParam()
            self.consome(TOKEN.FECHA_PARENTESES)
        else:
            self.opcPos()
            self.opcAtrib()

    def opcAtrib(self):
        # OpcAtrib -> = Oito | LAMBDA
        if self.tokenAtual() == TOKEN.ATRIBUICAO:
            self.consome(TOKEN.ATRIBUICAO)
            self.oito()
        else:
            pass

    def opcPos(self):
        # OpcPos -> LAMBDA | [ Exp ]
        if self.tokenAtual() == TOKEN.ABRE_COLCHETES:
            self.consome(TOKEN.ABRE_COLCHETES)
            self.exp()
            self.consome(TOKEN.FECHA_COLCHETES)
        else:
            pass

    def folha(self):
        # Folha -> valorInt | valorFloat | valorString | ValorLista
        # Folha -> ( Zero )
        # (Folha -> ident RestoFolha esta em Oito)
        if self.tokenAtual() == TOKEN.VALORINT:
            self.consome(TOKEN.VALORINT)
        elif self.tokenAtual() == TOKEN.VALORFLOAT:
            self.consome(TOKEN.VALORFLOAT)
        elif self.tokenAtual() == TOKEN.VALORSTRING:
            self.consome(TOKEN.VALORSTRING)
        elif self.tokenAtual() == TOKEN.ABRE_COLCHETES:
            self.valorLista()
        elif self.tokenAtual() == TOKEN.ABRE_PARENTESES:
            self.consome(TOKEN.ABRE_PARENTESES)
            self.zero()
            self.consome(TOKEN.FECHA_PARENTESES)
        else:
            self.erro("uma expressao")

    def valorLista(self):
        # ValorLista -> [ ListaParam ]
        self.consome(TOKEN.ABRE_COLCHETES)
        self.listaParam()
        self.consome(TOKEN.FECHA_COLCHETES)

    def listaParam(self):
        # ListaParam -> LAMBDA | Param RestoListaParam
        # LAMBDA quando chega o ) da chamada ou o ] da lista
        if self.tokenAtual() not in [TOKEN.FECHA_PARENTESES, TOKEN.FECHA_COLCHETES]:
            self.param()
            self.restoListaParam()
        else:
            pass

    def restoListaParam(self):
        # RestoListaParam -> , Param RestoListaParam | LAMBDA
        if self.tokenAtual() == TOKEN.VIRGULA:
            self.consome(TOKEN.VIRGULA)
            self.param()
            self.restoListaParam()
        else:
            pass

    def param(self):
        # Param -> Zero
        self.zero()


# inicia a traducao
if __name__ == "__main__":
    sintatico = Sintatico(Lexico("sampleTest.txt"))
    sintatico.traduz()
