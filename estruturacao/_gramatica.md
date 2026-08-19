# Glossario
* é o simbolo da raiz da árvore;
variavel começa com letra maiscula;
palavra em UPPERCASE é folha, terminal;
& é uma folha/terminal;
* ++ Um e -- Um são só pre-fixado

# Erros encontrados:


## Linguagem D

### FUNÇOES
Prog* ->        Func RestoProg
RestoProg ->    LAMBDA 
                | Func RestoProg
Func ->         TipoFunc IDENT (ListaArgs) Corpo
TipoPrim ->     INT 
                | FLOAT 
                | STRING
TipoFunc ->     VOID 
                | TipoPrim
ListaArgs ->    LAMBDA 
                | Arg RestoListaArgs
RestoListaArgs -> , Arg RestoListaArgs
                | LAMBDA
Arg ->          TipoPrim OpcRef IDENT OpcColchete
OpcColchete ->  LAMBDA | [ ]
OpcRef ->       LAMBDA
                | &
Corpo ->        { ListaDeclar ListaCom }

### DECLARAÇÕES

ListaDeclar ->  LAMBDA
                | Declar ListaDeclar
Declar ->       TipoPrim IDENT OpColchete OpcInicializa ListaIdent ; 
ListaIdent ->   LAMBDA 
                | , IDENT OpColchete ListaIdent
OpcInicializa -> LAMBDA | = Exp

### COMANDOS DE REPETIÇÃO

ListaCom ->     LAMBDA
                | Com ListaCom
Com ->          ComRepeticao
                | ComDecisao
                | ComIO
                | Exp ;
                | BREAK ;
                | CONTINUE ;
                | RETURN OpcExp ;
                | Bloco
Bloco ->        Corpo
ComRepeticao -> LOOP Bloco
                | WHILE ( Exp ) Bloco
                | FOR ( IDENT IN IDENT ) Bloco
                | FOR ( OpcExp ; OpcExp ; OpcExp ) Bloco
ComDecisao ->   IF ( Exp ) Bloco ListaElif ElseOpc
ListaElif ->   LAMBDA
                | ELIF ( Exp ) Bloco ListaElif
ElseOpc ->      LAMBDA
                | ELSE Bloco
ComIO ->        READ( IDENT ) ;
                | WRITE ( ListaExp ) ;
ListaExp ->     Exp RestoListaExp
RestoListaExp -> , Exp RestoListaExp
                | LAMBDA


### EXPRESSOES

OpcExp ->       LAMBDA 
                | Zero
Exp →           Zero
Zero →          ++ Um 
                | -- Um 
                | Um
Um →            Um OR Dois 
                | Dois
Dois →          Dois AND Tres 
                | Tres
Tres →          NOT Tres
                | Quatro
Quatro →        Cinco > Cinco 
                | Cinco >= Cinco
                | Cinco < Cinco 
                | Cinco <= Cinco
                | Cinco == Cinco 
                | Cinco != Cinco 
                | Cinco
Cinco →         Cinco + Seis 
                | Cinco - Seis 
                | Seis
Seis →          Seis * Sete 
                | Seis / Sete 
                | Seis DIV Sete 
                | Seis MOD Sete 
                | Sete
Sete →          + Sete 
                | - Sete 
                | Oito
Oito →          IDENT OpcPos = Oito 
                | Folha
Folha ->        VALORINT 
                | VALORFLOAT 
                | VALORSTRING 
                | ValorLista
                | IDENT
                | IDENT [ Zero ]
                | ( Zero )
                | Call

Call ->         IDENT ( ListaParam )

ListaParam ->   LAMBDA
                | Param RestoListParam
RestoListParam-> , Param RestoListParam
                | LAMBDA
Param ->        Zero
ValorLista   -> [ ListaParam ] 

OpcPos  ->      LAMBDA | [ Exp ]





