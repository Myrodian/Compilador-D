Prog -> Func RestoProg
RestoProg -> LAMBDA | Func RestoProg
Func -> TipoFunc ident ( ListaArgs ) Corpo
TipoPrim -> int | float | string
TipoFunc -> void | TipoPrim
ListaArgs -> LAMBDA | Arg RestoListaArgs
RestoListaArgs -> , Arg RestoListaArgs | LAMBDA
Arg -> TipoPrim OpcRef ident OpcColchete
OpcRef -> LAMBDA | &
OpcColchete -> LAMBDA | [ ]
Corpo -> { ListaDeclar ListaCom }
ListaDeclar -> LAMBDA | Declar ListaDeclar
Declar -> TipoPrim ident OpcColchete OpcInicializa Listaident ;
Listaident -> LAMBDA | , ident OpcColchete Listaident
OpcInicializa -> LAMBDA | = Exp
ListaCom -> LAMBDA | Com ListaCom
Com -> ComRepete | ComDecisao | ComIO | Exp ;
Com -> break ; | continue ; | return OpcExp ;
Com -> Bloco
Bloco -> Corpo
ComRepete -> loop Bloco
ComRepete -> while ( Exp ) Bloco
ComDecisao -> if ( Exp ) Bloco ListaElif ElseOpc
ListaElif -> LAMBDA | elif ( Exp ) Bloco ListaElif
ElseOpc -> LAMBDA | else Bloco
ComIO -> read ( ident ) ; | write ( ListaExp );
ComRepete -> for ( RestoComRepete
RestoComRepete -> ident  in  ident ) Bloco
RestoComRepete -> OpcExp ; OpcExp ; OpcExp ) Bloco
ListaExp -> Exp RestoListaExp
RestoListaExp -> , Exp RestoListaExp | LAMBDA
OpcExp -> LAMBDA | Zero
Exp -> Zero
Zero -> ++ Um | -- Um | Um
Um -> Dois RestoUm
RestoUm -> LAMBDA | OR Dois RestoUm
Dois -> Tres RestoDois
RestoDois -> LAMBDA | AND Tres RestoDois
Tres -> NOT Tres | Quatro
Quatro -> Cinco Resto4
Resto4 -> > Cinco | >= Cinco | < Cinco | <= Cinco
Resto4 -> == Cinco | != Cinco | LAMDBA
Cinco -> Seis RestoCinco
RestoCinco -> LAMBDA | + Seis RestoCinco | - Seis RestoCinco
Seis -> Sete RestoSeis
RestoSeis -> LAMBDA | * Sete RestoSeis | / Sete RestoSeis
RestoSeis -> div Sete RestoSeis | mod Sete RestoSeis
Sete -> + Sete | - Sete | Oito
Oito -> ident OpcPos = Oito | Folha
Folha -> valorInt | valorFloat |  valorString | ValorLista
Folha -> ( Zero )
Folha -> ident RestoFolha
RestoFolha -> LAMBDA | [ Zero ] | ( ListaParam )
ListaParam -> LAMBDA | Param RestoListaParam
RestoListaParam -> , Param RestoListaParam | LAMBDA
Param -> Zero
ValorLista -> [ ListaParam ]
OpcPos -> LAMBDA | [ Exp ]