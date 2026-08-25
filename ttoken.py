from enum import IntEnum


class TOKEN(IntEnum):
    # Palavras reservadas
    VOID = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    LOOP = 5
    WHILE = 6
    FOR = 7
    IN = 8
    IF = 9
    ELIF = 10
    ELSE = 11
    READ = 12
    WRITE = 13
    BREAK = 14
    CONTINUE = 15
    RETURN = 16
    DIV = 17
    MOD = 18
    OR = 19
    AND = 20
    NOT = 21

    # Identificadores e valores
    IDENT = 22
    VALORINT = 23
    VALORFLOAT = 24
    VALORSTRING = 25

    # Operadores
    ATRIBUICAO = 26       # =
    INCREMENTO = 27       # ++
    DECREMENTO = 28       # --
    SOMA = 29             # +
    SUBTRACAO = 30        # -
    MULTIPLICACAO = 31    # *
    DIVISAO = 32          # /

    # Operadores relacionais
    IGUAL = 33             # ==
    DIFERENTE = 34         # !=
    MENOR = 35             # <
    MENOR_IGUAL = 36       # <=
    MAIOR = 37             # >
    MAIOR_IGUAL = 38       # >=

    # Símbolos
    REFERENCIA = 39        # &
    ABRE_PARENTESES = 40   # (
    FECHA_PARENTESES = 41  # )
    ABRE_CHAVES = 42       # {
    FECHA_CHAVES = 43      # }
    ABRE_COLCHETES = 44    # [
    FECHA_COLCHETES = 45   # ]
    VIRGULA = 46           # ,
    PONTO_VIRGULA = 47     # ;
    PONTO = 48             # .

    # Controle do analisador
    EOF = 49
    ERRO = 50           


    @classmethod
    def msg(cls, token):
        nomes = {
            1: "void",
            2: "int",
            3: "float",
            4: "string",
            5: "loop",
            6: "while",
            7: "for",
            8: "in",
            9: "if",
            10: "elif",
            11: "else",
            12: "read",
            13: "write",
            14: "break",
            15: "continue",
            16: "return",
            17: "div",
            18: "mod",
            19: "or",
            20: "and",
            21: "not",

            22: "ident",
            23: "valorInt",
            24: "valorFloat",
            25: "valorString",

            26: "=",
            27: "++",
            28: "--",
            29: "+",
            30: "-",
            31: "*",
            32: "/",

            33: "==",
            34: "!=",
            35: "<",
            36: "<=",
            37: ">",
            38: ">=",

            39: "&",
            40: "(",
            41: ")",
            42: "{",
            43: "}",
            44: "[",
            45: "]",
            46: ",",
            47: ";",
            48: ".",
            
            49: "<eof>",
            50: "erro"
        }

        return nomes[token]


    @classmethod
    def oprel(cls):
        return [
            TOKEN.IGUAL,
            TOKEN.MAIOR,
            TOKEN.MENOR,
            TOKEN.MAIOR_IGUAL,
            TOKEN.MENOR_IGUAL,
            TOKEN.DIFERENTE
        ]


    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'void': TOKEN.VOID,
            'int': TOKEN.INT,
            'float': TOKEN.FLOAT,
            'string': TOKEN.STRING,

            'loop': TOKEN.LOOP,
            'while': TOKEN.WHILE,
            'for': TOKEN.FOR,
            'in': TOKEN.IN,

            'if': TOKEN.IF,
            'elif': TOKEN.ELIF,
            'else': TOKEN.ELSE,

            'read': TOKEN.READ,
            'write': TOKEN.WRITE,

            'break': TOKEN.BREAK,
            'continue': TOKEN.CONTINUE,
            'return': TOKEN.RETURN,

            'div': TOKEN.DIV,
            'mod': TOKEN.MOD,
            'or': TOKEN.OR,
            'and': TOKEN.AND,
            'not': TOKEN.NOT
        }

        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.IDENT
        
    @classmethod
    def tabelaOperacoes(cls):
        return {
            # operações aritméticas
            frozenset({(TOKEN.INT, False), TOKEN.SOMA, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.SUBTRACAO, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.MULTIPLICACAO, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.DIVISAO, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.INT, False), TOKEN.MOD, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.SOMA, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.SOMA, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.MULTIPLICACAO, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.DIVISAO, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),

            # operações de concatenação
            frozenset({(TOKEN.STRING, False), TOKEN.SOMA, (TOKEN.STRING, False)}): (TOKEN.STRING, False),
            frozenset({(TOKEN.STRING, True), TOKEN.SOMA, (TOKEN.STRING, True)}): (TOKEN.STRING, True),
            frozenset({(TOKEN.INT, True), TOKEN.SOMA, (TOKEN.INT, True)}): (TOKEN.INT, True),
            frozenset({(TOKEN.FLOAT, True), TOKEN.SOMA, (TOKEN.FLOAT, True)}): (TOKEN.FLOAT, True),
            frozenset({(TOKEN.BOOLEAN, True), TOKEN.SOMA, (TOKEN.BOOLEAN, True)}): (TOKEN.BOOLEAN, True),
            frozenset({(None, True), TOKEN.SOMA, (None, True)}): (None, True),
            frozenset({(None, True), TOKEN.SOMA, (TOKEN.STRING, True)}): (None, True),
            frozenset({(None, True), TOKEN.SOMA, (TOKEN.INT, True)}): (None, True),
            frozenset({(None, True), TOKEN.SOMA, (TOKEN.FLOAT, True)}): (None, True),
            frozenset({(None, True), TOKEN.SOMA, (TOKEN.BOOLEAN, True)}): (None, True),

            # operações relacionais
            frozenset({(TOKEN.INT, False), TOKEN.IGUAL, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.DIFERENTE, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MENOR, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MENOR_IGUAL, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MAIOR, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MAIOR_IGUAL, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.IGUAL, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.DIFERENTE, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.MENOR, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.MENOR_IGUAL, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.MAIOR, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.MAIOR_IGUAL, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.STRING, False), TOKEN.IGUAL, (TOKEN.STRING, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.STRING, False), TOKEN.DIFERENTE, (TOKEN.STRING, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.IGUAL, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.DIFERENTE, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MENOR, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MENOR_IGUAL, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.MAIOR, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.IGUAL, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.DIFERENTE, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.AND, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.OR, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),

            # operações unárias
            frozenset({TOKEN.SOMA, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.SUBTRACAO, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.SOMA, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.SUBTRACAO, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.NOT, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),

            # valores hardcoded
            frozenset([(TOKEN.INT, False)]): (TOKEN.INT, True),
            frozenset([(TOKEN.FLOAT, False)]): (TOKEN.FLOAT, True),
            frozenset([(TOKEN.STRING, False)]): (TOKEN.STRING, True),
            frozenset([(TOKEN.TRUE, False)]): (TOKEN.BOOLEAN, False),
            frozenset([(TOKEN.INT, False), (TOKEN.FLOAT, False)]): (TOKEN.FLOAT, True),

            frozenset({(TOKEN.STRING, False), TOKEN.SOMA, (TOKEN.STRING, False)}): (TOKEN.STRING, False),
            frozenset({(TOKEN.STRING, True), TOKEN.SOMA, (TOKEN.STRING, False)}): (TOKEN.STRING, True),
        } 