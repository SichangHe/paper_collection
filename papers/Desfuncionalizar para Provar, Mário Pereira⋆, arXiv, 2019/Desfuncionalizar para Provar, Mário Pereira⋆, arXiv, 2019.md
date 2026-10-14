                                                            Desfuncionalizar para Provar

                                                                             Mário Pereira⋆

                                                                             NOVA – LINCS



                                                 Abstract. Este artigo explora a ideia de utilizar a desfuncionalização
                                                 como uma técnica de prova de programas de ordem superior. A des-
arXiv:1905.08368v1 [cs.LO] 20 May 2019




                                                 funcionalização consiste em representar valores funcionais por uma rep-
                                                 resentação de primeira. O seu interesse é portanto poder utilizar pos-
                                                 teriormente uma ferramenta de prova de programas existente, sem ser
                                                 necessário estender esta ferramenta com suporte para ordem superior.
                                                 Este artigo ilustra e discute esta abordagem através de diversos exemplos
                                                 práticos, construídos e validados na ferramenta de verificação dedutiva
                                                 Why3.


                                         1     Introdução

                                         Um programa de ordem superior é um programa que utiliza funções como val-
                                         ores de primeira classe. Em tais programas, funções podem ser passadas como
                                         argumentos a outras funções ou devolvidas como o resultado de computações. O
                                         conceito de ordem superior é amplamente conhecido e utilizado em linguagens
                                         ditas funcionais, tais como OCaml, Haskell ou SML. Recentemente, linguagens
                                         como Java ou C++ introduziram suporte para funções de ordem superior.
                                             A prova de correcção de programas de ordem superior coloca desafios com-
                                         plexos, em particular no contexto de programas com efeitos. Metodologias exis-
                                         tentes [2, 14] empregam assistentes de prova interactivos e uma codificação dos
                                         efeitos directamente na lógica destes assistentes de prova. No contexto de prova
                                         automática de programas, Kanig e Filliâtre [12] propuseram um sistema de tipos
                                         e efeito, assim como um cálculo de pré-condições mais fracas, com o propósito
                                         de especificar e provar a correção funcional de programas de ordem superior. No
                                         entanto, tal sistema é difícil de utilizar de forma prática.
                                             Neste artigo, propomos uma nova metodologia para a verificação de progra-
                                         mas de ordem superior que potencialmente comportam efeitos secundários. Ex-
                                         ploramos a ideia de empregar a técnica de desfuncionalização para verificar tais
                                         programas. A utilização da desfuncionalização permite-nos obter um programa
                                         de primeira ordem equivalente ao programa de ordem superior original, o que nos
                                         conduz a um contexto de programas de primeira ordem. Assim, podemos recor-
                                         rer a ferramentas de prova existentes, sem que para tal seja necessário estender
                                         tais ferramentas com suporte de ordem superior. Esta técnica apresenta como
                                         ⋆
                                             Este trabalho foi realizado enquanto o autor se encontrava afiliado ao LRI – Labo-
                                             ratoire de Recherche en Informatique, CNRS, Université Paris-Sud – na qualidade
                                             de aluno de doutoramento.
limitação o facto de ser necessário conhecer à priori todas as funções que serão
utilizadas como valores de primeira classe. Mesmo se, teoricamente, tal nos im-
pede de aplicar a técnica de desfuncionalização para provar qualquer programa, é
possível identificar uma classe interessante e representativa de programas de or-
dem superior aos quais nos é possível aplicar a desfuncionalização para provar a
sua correcção. Neste artigo, apresentamos a nossa abordagem através de diversos
exemplos escritos e verificados no sistema de prova de programas Why3 [7].
    Este artigo encontra-se organizado como se segue. A secção 2 introduz a
técnica de desfuncionalização, com base num exemplo completo. Na secção 3 ap-
resentamos em detalhe a nossa abordagem de utilização da desfuncionalização
como meio de prova. Ilustramos a nossa proposta através de diferentes exemp-
los. O artigo termina sobre algumas perspectivas e conclusões sobre o nosso tra-
balho. O código Why3 apresentado neste artigo pode ser encontrado no seguinte
endereço electrónico: http://www.lri.fr/~mpereira/defunc.


2     Desfuncionalização
A desfuncionalização é uma técnica de transformação de programas de ordem
superior para programas de primeira ordem. Esta técnica foi introduzida por
Reynolds [18] como forma de obter um interpretador de ordem superior a partir
de um interpretador de primeira ordem. Recentemente, esta técnica tem sido
amplamente explorada por Danvy e seus colaboradores [3,4]. Em particular, estes
autores mostraram de que forma é possível derivar máquinas abstractas para
diferentes estratégias de avaliação do cálculo-lambda a partir de interpretadores
composicionais [1].
    Passamos a explicar o princípio da desfuncionalização através de um exemplo
escrito em OCaml1 Consideremos o programa que calcula a altura de uma árvore
binária, escrito em estilo CPS [15]:
    type ’a tree = E | N of ’a tree * ’a * ’a tree

    let rec heigth_tree_cps (t: ’a tree) (k: int → ’b) : ’b = match t with
      | E → k 0
      | N (l, x, r) →
         heigth_tree_cps l (fun hl →
         heigth_tree_cps r (fun hr → k (1 + max hl hr)))

    let heigth_tree t = heigth_tree_cps t (fun x → x)
Este programa foi cuidadosamente escrito em estilo CPS para evitar quaisquer
problemas de stack overflow, independentemente da forma da árvore. A transfor-
mação CPS pode ser usada como um meio automático para evitar problemas de
stack overflow, desde que o compilador optimize chamadas recursivas terminais.
    Chamamos a atenção para a presença, na função heigth_tree_cps , do ar-
gumento k do tipo int → ’b. É a utilização deste argumento que confere à
1
    Este código pode ser facilmente adaptado a qualquer linguagem que suporte funções
    como valores de primeira classe.


                                          2
função heigth_tree_cps a sua natureza de ordem superior. Este argumento ac-
tua como uma continuação, ou seja, ao invés de devolver um resultado, a função
heigth_tree_cps passa-o como argumento a k. No caso da árvore vazia (primeiro
ramo da filtragem), por exemplo, aplicamos k a 0 em detrimento de devolver
directamente tal resultado.
    Três funções anónimas são utilizadas no código do programa que calcula a al-
tura da árvore. Na chamada heigth_tree_cps l a continuação (fun hl → ...)
é aplicada ao resultado do cálculo da altura da sub-árvore esquerda l. O ar-
gumento hl representa a altura de l já calculada. No interior desta continu-
ação encontramos uma segunda chamada recursiva com uma outra continuação,
desta vez sobre a sub-árvore direita r. Aquando da aplicação da função anónima
(fun hr → ...), conhecemos já todos os ingredientes necessários para calcular
a altura da árvore inicial t. Também neste caso não devolvemos directamente
o resultado da expressão 1 + max hl hr, mas é sim passado a k. A terceira e
última função anónima que encontramos neste programa é a função identidade
(fun x → x). A aplicação desta função garante que o resultado devolvido por
heigth_tree t é de facto a altura da árvore t.
    Para desfuncionalizar este programa, precisamos de uma representação de
primeira ordem para as três abstracções utilizadas. Para isso, substituímos o
tipo funcional por um tipo algébrico, através do qual capturamos os valores das
variáveis livres utilizadas em cada função. Para o exemplo apresentado acima,
introduzimos o tipo seguinte:
  type ’a kont = Kid | Kleft of ’a tree * ’a | Kright of ’a kont * int

O construtor Kid representa a função identidade e por isso não contém variáveis
livres. Os construtores Kleft e Kright representam, respectivamente, as funções
(fun hl → ...) e (fun hr → ...). Os seus argumentos capturam as variáveis
livres utilizadas em cada uma das duas funções. No caso de Kleft guardamos a
sub-árvore r e a continuação k; no caso de Kright o primeiro argumento é o valor
de k e o segundo representa hl, a altura da sub-árvore esquerda.
    Tendo entre mãos uma representação de primeira ordem, podemos agora
proceder à substituição de todas as abstracções pelo construtor de ’a kont cor-
respondente:
  let rec heigth_tree_cps t (k: ’a kont) = match t with
    | E → ??? (* aplicar k desfuncionalizado ao seu argumento *)
    | N (l, x, r) → heigth_tree_cps l (Kleft (r, k))

  let heigth_tree t = heigth_tree_cps t Kid

A segunda etapa do processo de desfuncionalização consiste em introduzir uma
função apply para substituir as aplicações no programa original. Esta função
aceita como argumentos um valor do tipo kont ’a sobre o qual é realizada uma
análise por casos. Para cada construtor, a função apply executa o código da
abstracção que corresponde a esse mesmo construtor. O segundo argumento de
apply trata-se do argumento da aplicação no programa original. A função apply
para o nosso exemplo é a seguinte:

                                       3
    type ’a tree = E | N of ’a tree * ’a * ’a tree

    type ’a kont = Kid | Kleft of ’a tree * ’a kont | Kright of ’a kont * int

    let rec apply (k: ’a kont) arg = match k with
      | Kid → let x = arg in x
      | Kleft (r, k) → let hl = arg in heigth_tree_cps r (Kright (k, hl))
      | Kright (k, hl) → let hr = arg in apply k (1 + max hl hr)
    and heigth_tree_cps t (k: ’a kont) = match t with
      | E → apply k 0
      | N (l, x, r) → heigth_tree_cps l (Kleft (r, k))

    let heigth_tree t = heigth_tree_cps t Kid



         Fig. 1. Programa que calcula a altura da árvore, desfuncionalizado.


    let rec apply (k: ’a kont) arg = match k with
      | Kid → let x = arg in x
      | Kleft (r, k) → let hl = arg in heigth_tree_cps r (Kright (k, hl))
      | Kright (k, hl) → let hr = arg in apply k (1 + max hl hr)
Para obter o programa completamente desfuncionalizado, basta então substituir
todas as aplicações da continuação k por chamadas à função apply. O código
completo resultante para este exemplo pode ser encontrado na Fig. 1.

3     Prova por desfuncionalização
Nesta secção exploramos a ideia de utilizar a desfuncionalização como uma téc-
nica de prova para programas de ordem superior com efeitos. A nossa proposta
é a seguinte:
1. dado um programa de ordem superior (possivelmente contendo efeitos),
   juntamos-lhe uma especificação lógica.
2. desfuncionalizamos este programa e ao mesmo tempo traduzimos a sua es-
   pecificação a fim que esta se torne uma especificação do programa desfun-
   cionalizado.
3. utilizamos uma ferramenta de prova de programas existente para produzir a
   prova de que o programa desfuncionalizado respeita a especificação dada.
Passamos a ilustrar esta proposição através de diferentes exemplos: o programa
que calcula a altura de uma árvore (Sec. 3.1); um programa que calcula o número
de elementos distintos de uma árvore (Sec. 3.2); um interpretador small-step
para uma pequena linguagem (Sec. 3.3). Todas as experiências descritas são
realizadas com ajuda da ferramenta de verificação Why3. Como actualmente o
Why3 não nos permite racionar sobre programas de ordem superior, em geral,
todos os exemplos de especificação de programas de ordem superior são escritos
num sistema hipotético, uma possível extensão do Why3.

                                         4
3.1    Altura de uma árvore
Recuperemos o exemplo da Sec. 2. A fim de especificar este programa, devemos
instrumentar as funções heigth_tree_cps e heigth_tree com contratos. A função
heigth_tree devolve a altura da árvore t passada como argumento, tal como
especificamos na sua pós-condição:
  let heigth_tree (t: tree ’a) : int
    ensures { result = height t }
  = heigth_tree_cps t (fun x → x)
Aqui, result trata-se uma palavra-chave do Why3 para representar o valor de-
volvido e height é uma função lógica que devolve a altura de uma árvore.
   O valor devolvido pela função height_tree_cps é o resultado da aplicação da
continuação k à altura da árvore t. Seria assim natural de equipar height_tree_cps
com a seguinte pós-condição:
      ensures { result = k (height t) }
No entanto, esta especificação coloca-nos o problema de como interpretar a uti-
lização de funções de programa na lógica. Em geral, tal utilização pode facilmente
produzir incoerências lógicas, já que funções de programa podem conter efeitos,
e.g., divergência. Fazemos então a escolha de restringir a nossa linguagem de
especificação: podemos utilizar os nomes de funções de programa, mas impomos
uma barreira de abstracção entre o mundo lógico e o programa. Para esse fim,
adoptamos um sistema no qual as funções são abstraídas sob a forma de um par
de predicados que representam as suas pré-condição e pós-condição [17]. Assim,
no interior de uma fórmula lógica, uma função f do tipo τ1 → τ2 é vista como o
par de predicados
                             pre f : τ1 → prop
                            post f : τ1 → τ2 → prop
Utilizamos pre f e post f para nos referirmos à pré-condição e à pós-condição
de f , respectivamente.
    Voltemos ao exemplo da altura de uma árvore. Podemos então escrever, uti-
lizando a notação apresentada acima, o contrato seguinte para a função height_tree_cps :
  let rec height_tree_cps (t: tree ’a) (k: int → ’b) : ’b
    ensures { post k (height t) result }
Esta pós-condição impõe uma relação entre o valor passado a k (a altura de t)
e o resultado devolvido (result). Seguindo a nossa metodologia, podemos igual-
mente fornecer contratos às funções anónimas utilizadas no interior de height_tree_cps :
  let rec heigth_tree_cps (t: tree ’a) (k: int → ’b) : ’b
    ensures { post k (heigth t) result }
  = match t with
    | Empty → k 0
    | Node l x r →
        heigth_tree l (fun hl → ensures { post k (1 + max hl (height r)) result }
        heigth_tree r (fun hr → ensures { post k (1 + max hl hr) result }
          k (1 + max hl hr)))
    end


                                        5
Para a primeira abstracção, especificamos que o resultado da sua aplicação se
relaciona com a altura da árvore completa, através da altura hl da sub-árvore
esquerda e da altura da sub-árvore direita, que ainda não conhecemos. Juntamos
à segunda abstracção uma pós-condição semelhante, com a nuance de que no
momento de aplicar esta função já conhecemos a altura hr.
    Procedemos agora à desfuncionalização deste programa, assim como da sua
especificação, para em seguida provar a sua correcção funcional com a ajuda da
ferramenta Why3. O código obtido é o seguinte:
  type kont ’a = Kid | Kleft (tree ’a) (kont ’a) | Kright int (kont ’a)

  let rec heigth_tree_cps (t: tree ’a) (k: kont ’a) : int
    ensures { post k (height t) result }
  = match t with
    | Empty → apply k 0
    | Node l _ r → heigth_tree_cps l (Kleft r k)
    end
  with apply (k: kont ’a) (arg: int) : int
    ensures { post k arg result }
  = match k with
    | Kid → arg
    | Kleft r k → heigth_tree_cps r (Kright arg k)
    | Kright hl k → apply k (1 + max hl arg)
    end

  let height_tree (t: tree ’a) : int
    ensures { result = height t }
  = heigth_tree_cps t Kid

Como podemos observar, este programa é em tudo semelhante ao programa
OCaml da Fig. 1, excepção feita às pequenas diferenças sintácticas em relação à
linguagem do Why3 e à presença das anotações lógicas. De notar que as funções
heigth_tree_cps e apply se mantém como funções mutuamente recursivas.
    A especificação do programa desfuncionalizado é a mesma do programa orig-
inal. Em particular, mantemos a nossa utilização da projecção post para a pós-
condição de heigth_tree_cps . Precisamos então de fornecer uma especificação à
função apply, a nova função gerada pelo processo de desfuncionalização. Como a
função apply simula a aplicação de uma função ao seu argumento, a única especi-
ficação que lhe podemos fornecer é a de que a sua pós-condição é a pós-condição
da função k. Da mesma forma, a pré-condição de apply seria a pré-condição de k,
à qual podemos aceder utilizando a projecção pre. Escolhemos não o fazer para
este exemplo, visto tratar-se da pré-condição trivial.
    Finalmente, precisamos de introduzir o predicado post na especificação lóg-
ica desfuncionalizada. Para tal, criamos um predicado post que reúne as pós-
condições fornecidas no programa original. Tal como para a função apply, um tal
predicado efectua uma filtragem sobre o tipo algébrico kont ’a e para cada con-
strutor copiamos a pós-condição fornecida na abstracção correspondente. Para
este exemplo, o predicado post é o seguinte:

                                       6
  predicate post (k: kont ’a) (arg result: int) = match k with
   | Kid → let x = arg in x = result
   | Kleft r k’ → let hl = arg in post k’ (1 + max hl (height r)) result
   | Kright hl k’ → let hr = arg in post k’ (1 + max hl hr) result
   end

Como pós-condição do construtor Kid utilizamos a pós-condição trivial result = x.
Esta fórmula representa a pós-condição mais forte desta função, podendo ser
automaticamente inferida. Utilizando a ferramenta Why3 sobre este programa,
todas as obrigações de prova geradas são automaticamente provadas por demon-
stradores SMT.
    Um aspecto importante a ressalvar é de que a forma como desfuncionalizámos
este programa e a sua especificação, em particular a forma de construir o pred-
icado post e o contrato da função apply, pode ser mecanizada. Podemos assim
imaginar uma ferramenta que recebe um programa de ordem superior anotado,
que o desfuncionaliza e finalmente o envia à ferramenta Why3.

Terminação. Um aspecto importante que não foi abordado neste exemplo é o
da prova de terminação. Nada nos impede de provar que o programa desfun-
cionalizado termina, fornecendo medidas de decréscimo adequadas. Para isso,
introduzimos funções lógicas que contam o número de nós de uma árvore e dos
construtores do tipo kont ’a. Tais medidas são bastante subtis e requerem um
pouco de imaginação:
  function var_tree (t: tree ’a) : int = match t with
    | Empty → 1
    | Node l _ r → 3 + var_tree l + var_tree r
    end

  function var_kont (k: kont ’a) : int = match k with
    | Kid → 0
    | Kleft r k → 2 + var_tree r + var_kont k
    | Kright _ k → 1 + var_kont k
    end

Podemos provar que efectivamente estas funções podem ser utilizadas como me-
didas de decréscimo, visto que são limitadas inferiormente:
  lemma var_tree_nonneg: forall t: tree ’a. var_tree t ≥ 0

  lemma var_kont_k_nonneg: forall k: kont ’a. var_kont k ≥ 0

Resta-nos juntar as anotações de terminação adequadas ao nosso programa:
  let rec height (t: tree ’a) (k: kont ’a) : int
    variant { var_tree t + var_kont k }
    ...
  with apply (k: kont ’a) (arg: int) : int
    variant { var_kont k }
    ...


                                       7
Todas as obrigações de prova geradas respeitantes à terminação são também
provadas automaticamente.
    Seria interessante ter um mecanismo para fornecer uma especificação sobre
a terminação de um programa de ordem superior e traduzi-la automaticamente,
tal como para o predicado post.


3.2   Nombre d’éléments distincts dans un arbre
O próximo exemplo apresenta um programa com o propósito de calcular o
número de elementos distintos de uma árvore binária, com complexidade linear
no número de nós da árvore. Como anteriormente, adoptamos um estilo CPS
para evitar qualquer problema de stack overflow. Este programa difere do da
secção anterior pela presença de efeitos. Utilizamos um conjunto mutável (uma
referência para um conjunto finito) a fim de guardar os elementos já encontra-
dos. No final do programa devolvemos o cardinal deste conjunto, obtendo assim
o número de elementos distintos de uma árvore. Segue-se a implementação em
Why3 :
  let n_distinct_elements (t: tree ’a) : int =
    let h = ref empty in
    let rec distinct_elements_loop (t: tree ’a) (k: unit → unit) : unit =
      match t with
      | Empty → k ()
      | Node l x r →
          h := add x !h;
          distinct_elements_loop l (fun () →
          distinct_elements_loop r (fun () → k ()))
      end
    in
    distinct_elements_loop t (fun x → x);
    cardinal !h

As operações sobre conjuntos utilizadas neste programa provêm da biblioteca
standard do Why3. As continuações presentes neste programa têm uma utilização
semelhante às que podemos encontrar no programa da Sec. 3.1. A sub-árvore
esquerda é tratada pela chamada distinct_elements_loop l (fun () → ...); a
chamada distinct_elements_loop r (fun () → ...) é utilizada para tratar a
sub-árvore direita; para assegurar que de facto devolvemos o resultado correcto,
a primeira chamada a distinct_elements_loop no interior de distinct_elements
é feita com a função identidade.
    Estando escrito em estilo CPS, este programa combina a utilização de ordem
superior com efeitos. Devemos, por isso, considerar a noção de estado do pro-
grama na sua especificação. Para tal, modificamos a representação das funções
ao nível da lógica, segundo a tese de J. Kanig [11]. Introduzimos, em primeiro
lugar, um novo tipo state e estendemos o tipo das funções na lógica como se
segue:
                    pre f : τ1 → state → prop
                  post f : τ1 → state → state → τ2 → prop

                                       8
O argumento extra da pré-condição corresponde ao estado no momento da
chamada da função. Os dois argumentos extra da pós-condição representam,
respectivamente, o estado antes e após a execução da função. A natureza do
tipo state dependerá das funções consideradas. Para este exemplo, o estado é
simplesmente set ’a.
    Voltemos ao código da função n_distinct_elements . Para especificar n_distinct_elements
e distinct_elements_loop introduzimos, em primeiro lugar, uma função lógica
set_of_tree. Esta função calcula a união do conjunto de elementos de uma árvore
com um conjunto s dado, que desempenha aqui o papel de acumulador:
  function set_of_tree (t: tree ’a) (s: set ’a) : set ’a = match t with
    | Empty → s
    | Node l x r → set_of_tree r (set_of_tree l (add x s))
    end

Para calcular o conjunto de elementos de uma árvore, basta applicar set_of_tree
ao conjunto vazio como segundo argumento. Damos à função n_distinct_elements
o seguinte contrato:
  let n_distinct_elements (t: tree ’a) : int
    ensures { result = cardinal (set_of_tree t empty) }

Especificamos distinct_elements_loop e as continuações utilizadas de forma
semelhante:
  let rec distinct_elements_loop (t: tree ’a) (k: unit → unit) : unit
    ensures { post k () (set_of_tree t (old !h)) !h () }
  = match t with
    | Empty → k ()
    | Node l x r →
        h := add x !h;
        distinct_elements_loop l (fun () → ensures { post k () (set_of_tree r (old !h)) !h () }
        distinct_elements_loop r (fun () → ensures { post k () (old !h) !h () }
          k ()))
    end

A pós-condição de distinct_elements_loop deve ser alvo de uma explicação de-
talhada. Dado que utilizamos a continução k no interior de distinct_elements_loop ,
a pós-condição desta função depende da pós-condição de k. É assim necessário
caracterizar o estado do programa quando chamamos k e o estado após a sua
execução. Este último é o estado obtido após a execução, por inteiro, da função
distinct_elements_loop , representado pelo valor contido na referência h. O es-
tado inicial é mais subtil. Recordemos que no momento de aplicar k teremos já
percorrido toda a árvore t. Assim, o estado a partir do qual chamamos a função k
é o conjunto de todos os elementos de t reunidos com o valor contido em h no
momento da chamada a distinct_elements_loop . Podemos recuperar este valor
através da etiqueta old do Why3, que nos permite aceder ao valor contido numa
referência no momento de entrada de uma função.
    A especificação das continuações utilizadas no interior das chamadas re-
cursivas a distinct_elements_loop segue o raciocínio que acabamos de descr-

                                       9
ever. As pós-condições destas duas abstracções dependem, igualmente, da pós-
condição de k. Na chamada a distinct_elements_loop l, especificamos na pós-
condição da sua continuação que o estado com o qual aplicaremos a continuação
é set_of_tree r (old !h). Aqui, old !h representa o estado antes de se aplicar a
continuação, isto é, após se ter percorrido a sub-árvore l. Como esta continuação
é utilizada para percorrer toda a sub-árvore direita, no momento de se aplicar k
a referência h contem, assim, o conjunto dos elementos distintos de l e x, que
juntámos inicialmente. Enfim, para a função distinct_elements_loop r, a sua
continuação nada mais faz que aplicar k e por isso esta aplicação é feita com o
estado inicial old !h, exactamente o estado antes da chamada a k.
    Para desfuncionalizar este programa e traduzir a sua especificação, começamos
por introduzir o tipo algébrico que representa as continuações:
  type kont ’a = Kid | Kleft (tree ’a) (kont ’a) | Kright (kont ’a)

Os únicos efeitos produzidos neste exemplo são o acesso (para escrita e leitura) à
referência h. Assim, podemos definir o tipo state como sendo o tipo dos valores
guardados em h:
  type state ’a = set ’a

Finalmente, introduzimos o predicado post:
  predicate post (k: kont ’a) (arg: unit) (old cur: state ’a) (result: unit)
  = match k with
    | Kid → let () = arg in old == cur
    | Kleft r k → let () = arg in post k () (set_of_tree r old) cur result
    | Kright k → let () = arg in post k () old cur result
    end

Para o caso da função identidade, este predicado especifica que o estado à saída
da função é o mesmo que à entrada. O símbolo (==) representa a igualdade
extensional entre dois conjuntos. Utilizando esta definição de post, podemos
gerar a função apply com a sua especificação, como se segue:
  let n_distinct_elements (t: tree ’a) : int
    ensures { result = cardinal (set_of_tree t empty) }
  = let h = ref empty in
    let rec apply (k: kont ’a) (arg: unit) : unit
      ensures { post k arg (old !h) !h () }
    = match k with
      | Kid → let x = arg in x
      | Kleft r k → let _ = arg in distinct_elements_loop r (Kright k)
      | Kright k → let _ = arg in apply k arg
      end
    with distinct_elements_loop (t: tree ’a) (k: kont ’a) : unit
      ensures { post k () (set_of_tree t (old !h)) !h () }
    = match t with
      | Empty → apply k ()
      | Node l x r →
          h := add x !h;


                                       10
            distinct_elements_loop l (Kleft r k)
        end
      in
      distinct_elements_loop t Kid;
      cardinal !h
Uma vez processado pelo Why3, todas as obrigações de prova geradas para este
programa são automaticamente descartadas. A terminação deste programa pode-
ria ser igualmente provada, utilizando argumentos de terminação idênticos aos
que foram utilizados para o exemplo anterior. De facto, as medidas de decréscimo
introduzidas para o programa da secção anterior poderiam ser também utilizadas
para este programa, tomando em conta as pequenas diferenças entre os dois tipo
kont.


3.3    Interprète à petits pas
O último exemplo que apresentamos é o de um interpretador small-step para uma
mini linguagem de expressões aritméticas. Trata-se de uma linguagem limitada
a constantes literais e subtracções:
    type exp = Const int | Sub exp exp
A fim de equipar esta linguagem com uma noção de avaliação, definimos a
seguinte função lógica eval:
    function eval (e: exp) : int = match e with
      | Const n → n
      | Sub e1 e2 → (eval e1) - (eval e2)
      end
Esta função representa a semântica natural (big-step) da nossa linguagem.
                                                                        ǫ
   Para definir uma relação de redução, começamos por definir a relação −
                                                                        →, que
corresponde a uma redução à cabeça da expressão. Para esta linguagem existe
uma só regra de redução à cabeça:
                                               ǫ
                 Sub (Const v1 ) (Const v2 )   →
                                               −    Const (v1 − v2 )
                ǫ
Para traduzir −
              → em Why3 introduzimos a função head_reduction :
    let head_reduction (e: exp) : exp = match e with
      | Sub (Const v1) (Const v2) → Const (v1 - v2)
      | _ → absurd
      end
O segundo ramo da filtragem represente o caso em que uma expressão passada
como argumento não é um redex. Como desejamos aplicar head_reduction uni-
camente a expressões que possam ser reduzidas à cabeça, utilizamos a palavra-
chave absurd do Why3 para marcar este ramo como um ponto inatingível do
código. Para provar que este ramo é efectivamente inatingível2 , é necessário exi-
gir que o argumento de head_reduction seja um redex. Para isso, introduzimos o
seguinte predicado is_redex:
2
    A construção absurd exige uma prova de falso.


                                         11
  predicate is_redex (e: exp) = match e with
    | Sub (Const _) (Const _) → true
    | _ → false
    end

Podemos agora juntar a head_reduction a pré-condição desejada:
  let head_reduction (e: exp) : exp
    requires { is_redex e }
    ...

O resultado da chamada head_reduction e é uma expressão e’ que se avalia ao
mesmo valor que e. Juntamos a head_reduction uma pós-condição que especifica
exactamente este raciocínio:
  let head_reduction (e: exp) : exp
    requires { is_redex e }
    ensures { eval result = eval e }
    ...

Todas as obrigações de prova geradas para a função head_reduction são auto-
maticamente descartadas.
   Para reduzir em profundidade, introduzimos agora a regra de inferência
                                      ǫ
                                   e−→ e′
                                C[e] → C[e′ ]

onde C representa um contexto de redução, definido pela seguinte gramática:

                          C ::= 
                               | C[Sub  e]
                               | C[Sub (Const v) ]

O símbolo  representa o buraco. Definimos C[e] como sendo o contexto C no
qual o buraco foi completamente substituído pela expressão e. A esta operação
damos o nome de composition. O resultado desta operação é uma nova expressão.
A gramática apresentada induz uma construção de contextos bottom-up. A nossa
escolha de contextos define, ainda, uma ordem de avaliação por valor e da es-
querda para a direita.
   O ponto interessante deste exemplo é a maneira como escolhemos repre-
sentar os contextos. Em detrimento de uma representação baseada num tipo
algébrico com três construtores, escolhemos aqui representar um contexto como
uma função. Um contexto c é assim uma função que recebe como argumento
uma expressão e e devolve a expressão obtida por substituição do buraco de c
para uma expressão e:
  type context = exp → exp

O contexto vazio, o buraco, é representado pela função identidade:
  let hole = fun x → x


                                      12
Os contextos para a redução sobre o primeiro ou sobre o segundo argumento de
Sub são representados, respectivamente, como se segue:
    let sub_left e2 c = fun e1 → c (Sub e1 e2)
    let sub_right v c = fun e1 → c (Sub (Const v) e1)
Esta maneira de representar os contextos conduz-nos a um código de ordem
superior elegante, mais compacto que um código utilizando um tipo concreto
para os contextos, tal como observaremos em seguida.
    Tendo definida a noção de contexto, a próxima etapa na implementação
de um interpretador small-step para a nossa linguagem consiste na implemen-
tação de uma função que decompõe uma expressão e em um redex e’ e um
contexto C, tais que C[e′ ] = e. Para a nossa linguagem esta decomposição é
única. Tal operação pode ser implementada com base na seguinte função auxil-
iar decompose_term :
    let rec decompose_term (e: exp) (c: context) : (context, exp) =
      match e with
      | Const _ → absurd
      | Sub (Const v1, Const v2) → (c, e)
      | Sub (Const v, e) → decompose_term e (fun x → c (Sub (Const v) x))
      | Sub (e1, e2) → decompose_term e1 (fun x → c (Sub x e2))
      end
Explicamos agora em detalhe o funcionamento da função decompose_term . Esta
função recebe como argumento um contexto c e uma expressão e que dese-
jamos decompor. Para isso, procedemos a uma análise por casos sobre a forma
da expressão e. Não podemos decompor um valor, logo utilizamos absurd para
marcar o primeiro ramo como um ponto inatingível. Se a expressão é da forma
Sub (Const v1) (Const v2), trata-se de um redex. Encontramos assim a decom-
posição que procurávamos, com a função decompose_term a devolver este redex
e o contexto c. Se, pelo contrário, existem em e sub-expressões que possamos
ainda reduzir, devemos continuar o processo de decomposição. Se a primeira
sub-expressão de Sub se encontra já reduzida, continuamos a decomposição so-
bre a segunda sub-expressão com um novo contexto de redução sobre a segunda
sub-expressão. Se, por seu lado, a primeira sub-expressão de Sub não está ainda
reduzida, a decomposição continua com um contexto de redução sobre a primeira
sub-expressão3
    Apresentamos em seguida a especificação lógica para a função decompose_term .
Pretendemos aplicar decompose_term unicamente a expressões que não são ainda
valores. Para tal, introduzimos uma função lógica is_value com o propósito de
testar se uma expressão é uma constante:
    predicate is_value (e: exp) = match e with
      | Const _ → true
      | _ → false
      end
3
    O leitor notará que o código das funções hole, sub_left e sub_right se encontra
    expandido na construção dos contextos.


                                         13
Munidos deste predicado, podemos agora equipar decompose_term e as abstracções
utilizadas no seu interior com os devidos contratos:
  let rec decompose_term (e: exp) (c: context) : (context, exp)
    requires { not (is_value e) }
    ensures { let (c’, e’) = result in
                  is_redex e’ && forall res. post c e res → post c’ e’ res }
  = match e with
    ...
    | Sub (Const v, e) →
        decompose_term e (fun x → ensures { post c (Sub (Const v) x) result } ...)
    | Sub (e1, e2) →
        decompose_term e1 (fun x → ensures { post c (Sub x e) result } ...)
    end
De notar que este programa não apresenta efeitos. Consequentemente, utilizamos
uma projecção post de dois argumentos, em semelhança ao que fizemos na
Sec. 3.1. A função decompose_term deve verificar a propriedade C ′ [e′ ] = C[e], C ′
e e′ sendo o contexto e a expressão devolvida e C et e os argumentos. Ora, dado
que escolhemos representar os contextos como funções, esta operação de com-
posição corresponde precisamente à aplicação de um contexto ao seu argumento.
A fim de especificar esta aplicação, utilizamos a projecção post sobre um con-
texto e a quantificação universal para referir que para qualquer expressão res que
verifica post c e res, então post c’ e’ res é igualmente verificada. Por outro
lado, a pós-condição de decompose_term assegura (à esquerda do símbolo &&) que
a expressão e’ devolvida é um redex.
    Passamos agora a introduzir a função decompose e a sua especificação. Esta
função toma como argumento uma expressão e não faz mais que chamar decompose_term ,
dando-lhe como argumento o contexto vazio, aqui representado pela função iden-
tidade:
  let decompose (e: exp) : (context, exp)
    requires { not (is_value e) }
    ensures { let (c’, e’) = result in is_redex e’ && post c’ e’ e          }
  = decompose_term e (fun x → x)
Para avaliar uma expressão e em um valor, introduzimos uma função de iteração
que se comporta como o fecho transitivo da relação →. O seu código Why3 é o
seguinte:
  let rec red (e: exp) : int = match e with
    | Const v → v
    | _ →
      let (c, r) = decompose e in
      let     r’ = head_reduction r in
      red (c r’)
    end
Se a expressão e é da forma Const v, esta encontra-se já em forma normal e por
isso não pode ser reduzida. Se, por outro lado, e não é ainda uma constante temos
então de (1) decompor esta expressão no redex r e no contexto c; (2) reduzir r à

                                       14
cabeça e obter a expressão r’; (3) continuar a iteração com a expressão obtida
pela composição de c e r’. A composição materializa-se, de uma forma elegante,
como a aplicação de c a r’. O valor devolvido pela chamada red e deve ser o
mesmo que aquele que é devolvido por uma avaliação big-step. Equipamos assim
red com o contrato seguinte:
  let rec red (e: exp) : int
    ensures { result = eval e }

   Procedemos à desfuncionalização deste exemplo para mostrar a sua correcção
através do Why3. Começamos por introduzir o tipo context desfuncionalizado:
  type context = CHole | CApp_left context exp | CApp_right int context

A partir das abstracções presentes no programa original, podemos gerar a função
apply conjuntamente com a sua especificação:
  let rec apply (c: context) (arg: exp) : exp
    ensures { post c arg result }
  = match c with
    | CHole → let x = arg in x
    | CApp_left c e → let x = arg in apply c (Sub x e)
    | CApp_right v c → let x = arg in apply c (Sub (Const v) x)
    end

onde o predicado post pode ser deduzido das pós-condições igualmente presentes
no programa original:
  predicate post (c: context) (arg result: exp) = match c with
    | CHole → let x = arg in x = result
    | CApp_left c e → let x = arg in post c (Sub x e) result
    | CApp_right v c → let x = arg in post c (Sub (Const v) x) result
    end

Para obter o programa desfuncionalizado final, basta, assim como demonstrado
para os exemplos anteriores, substituir todas as aplicações das abstracções por
chamadas a apply e todas as ocorrências dessas mesmas abstracções pelo con-
strutor respectivo do tipo context desfuncionalizado.
     Dando ao Why3 o programa desfuncionalizado e a respectiva especificação,
tal como apresentados, seriamos capazes de provar todas as obrigações de prova
geradas, excepto a pós-condição da função red. Para ajudar os demonstradores
automáticos a descartar esta pós-condição, introduzimos o seguinte lema auxil-
iar:
  lemma post_eval: forall c arg1 arg2 r1 r2.
    eval arg1 = eval arg2 → post c arg1 r1 → post c arg2 r2 →
    eval r1 = eval r2

Este lema exprime que para qualquer expressão arg1 e arg2 cuja a avaliação
produz o mesmo valor, então as expressões obtidas pela composição de arg1 e
arg2 com o mesmo contexto c devem-se avaliar no mesmo valor. Provamos este
resultado por indução sobre c e para tal escrevemos um lemma function, isto é,

                                      15
um programa fantasma que termina e que não possui efeitos observáveis, cujo
contrato será automaticamente traduzido para o enunciado apresentado acima:
    let rec lemma post_eval (c: context) (arg1 arg2 r1 r2: exp)
      requires { eval arg1 = eval arg2 }
      requires { post c arg1 r1 && post c arg2 r2 }
      ensures { eval r1 = eval r2 }
      variant { c }
    = match c with
      | CHole → ()
      | CApp_left c e → post_eval c (Sub arg1 e) (Sub arg2 e) r1 r2
      | CApp_right n c →
          post_eval c (Sub (Const n) arg1) (Sub (Const n) arg2) r1 r2
      end

As chamadas recursivas deste programa simulam a aplicação da hipótese de
indução. Com este lemma auxiliar, a pós-condição de red é provada automati-
camente por demonstradores SMT. O enunciado deste lema quantifica univer-
salmente sobre valores do tipo context. Escrever tal enunciado directamente so-
bre o programa de ordem superior poderia conduzir a uma contradição, visto que
não nos é possível afirmar tal resultado para qualquer função do tipo exp → exp.
Ainda assim, seria interessante ter um mecanismo que nos permitisse escrever
este género de enunciados no código original (restringindo as funções abstractas
aceites), traduzindo-os automaticamente para o código desfuncionalizado.
    É interessante notar que o tipo dos contextos desfuncionalizado corresponde a
um zipper [10] para expressões da nossa linguagem. Esta forma de representar os
contextos permite-nos implementar uma função de avaliação eficaz. Esta função é
normalmente designada como refocusing [5]. Utilizando contextos como funções,
as nossas operações de decomposição e composição apresentam uma complexi-
dade linear no pior caso, o que confere à função red um custo potencialmente
quadrático sobre o tamanho de uma expressão.


4     Discussão e perspectivas

Neste artigo explorámos a utilização da desfuncionalização como uma técnica
de prova para programas de ordem superior contendo potencialmente efeitos.
O que propomos é que um programa de ordem superior seja directamente an-
otado, e em seguida desfuncionalizar este programa e a sua especificação para
um programa de primeira ordem. Uma ferramenta de verificação dedutiva exis-
tente pode ser então utilizada para demonstrar a correcção deste programa. Esta
abordagem permite-nos utilizar ferramentas de verificação dedutiva de progra-
mas de primeira ordem existentes, sem necessidade de estender estas mesmas
ferramentas com suporte para ordem superior (o que implicaria, muito provavel-
mente, uma mudança profunda no core destas ferramentas, nomeadamente ao
nível da sua linguagem de programação, lógica subjacente e cálculo de obrigações
de prova). Ilustrámos a nossa proposta através de três exemplos desfuncionaliza-
dos (manualmente). Os programas de primeira ordem obtidos foram automati-

                                       16
camente verificados no sistema Why3. A utilização da desfuncionalização num
contexto de prova é, tanto quanto sabemos, nova.
    A desfuncionalização é geralmente considerada uma técnica global de trans-
formação de programas, isto é, é necessário conhecer todas as funções utilizadas
como valores de primeira classe num programa no momento de aplicar esta
transformação. Tal cenário implica que não poderemos ambicionar provar todos
os programas de ordem superior através da desfuncionalização. Ainda assim,
o método proposto aplica-se com sucesso a programas escritos em estilo CPS,
visto tratarem-se de programas para os quais conhecemos todas as abstracções
utilizadas em funções de ordem superior.

Perspectivas. O trabalho apresentado neste artigo mantém-se, para já, explo-
ratório. Utilizámos a desfuncionalização para provar diversos exemplos de pro-
gramas de ordem superior e os resultados encorajam-nos a continuar a exploração
desta metodologia. O nosso objectivo é melhorar e formalizar a nossa utilização
da desfuncionalização sobre programas de ordem superior. O primeiro passo será
definir formalmente a classe de programas sobre os quais esta técnica pode ser
aplicada, a fim de compreender se a desfuncionalização pode ser utilizada como
uma técnica robusta de prova de programas de ordem superior com efeitos.
    A função apply, gerada durante a desfuncionalização, simula a aplicação de
uma função (representada como um valor de um tipo algébrico obtido por des-
funcionalização) ao seu argumento. A função apply procede por análise de casos
sobre cada função presente no programa original, onde cada ramo corresponde
à definição da abstracção correspondente. Assim, cada um destes ramos deve
devolver um valor do mesmo tipo, o que é apenas verdade quando todas as ab-
stracções do programa têm o mesmo tipo τ1 → τ2 . Para resolver este problema,
Pottier e Gauthier [16] propuseram a utilização de tipos algébricos generaliza-
dos (do inglês generalized algebraic data types, GADT) para desfuncionalizar um
programa contendo abstracções de diferentes tipos. Tal solução interessa-nos e
por isso pretendemos estudar possíveis mecanismos para estender a linguagem
e lógica do sistema Why3 com suporte para os GADT. Por agora, introduzimos
diferentes funções apply caso o programa inicial apresente abstracções de tipos
diferentes.
    A fim de apresentar garantias fortes sobre a fiabilidade de um programa, a
sua prova de terminação desempenha um papel fundamental. Neste artigo men-
cionámos como poderia ser demonstrado que um programa desfuncionalizado
termina, mas sempre através de uma intervenção manual sobre o programa ger-
ado. Seria, por isso, desejável podermos especificar directamente a terminação
no programa de ordem superior com medidas de decréscimo apropriadas, que
seriam depois traduzidas durante a desfuncionalização.
    Os iteradores são exemplos de funções de ordem superior frequentemente uti-
lizadas para enumerar os elementos de uma estrutura de dados. Em trabalhos
anteriores [8, 9], propusemos técnicas para provar a correcção de programas que
implementam tais iteradores, assim como programas que os utilizam. Para tal,
iniciámos o desenvolvimento de uma ferramenta que recebe como input progra-
mas de ordem superior anotados e que se serve do Why3 para gerar obrigações de

                                      17
prova. Pretendemos estender esta ferramenta com suporte para a desfuncional-
ização e aumentar, assim, o conjunto de programas de ordem superior aceites
pela ferramenta.
    Finalmente, para melhor avaliar a sua utilidade, desejamos aplicar a prova
por desfuncionalização a um caso de estudo mais complexo. Um bom candidato
é o algoritmo de Koda-Ruskey [13] para a enumeração de todos os ideais de um
conjunto parcialmente ordenado. É nossa intenção partir da implementação de
ordem superior existente deste algoritmo [6], e provar a sua correcção através da
nossa metodologia.


Agradecimentos

Agradeço a Lucas Baudin, Richard Bonichon, Martin Clochard e Léon Gondel-
man pelos comentários e sugestões durante a preparação deste artigo. Agradeço
profundamente ao Jean-Christophe Filliâtre. Os seus conselhos, re-leituras aten-
tas e correcções foram cruciais para a conclusão deste trabalho.


References

 1. Mads Sig Ager, Dariusz Biernacki, Olivier Danvy, and Jan Midtgaard. A func-
    tional correspondence between evaluators and abstract machines. In Proceedings
    of the 5th International ACM SIGPLAN Conference on Principles and Practice of
    Declarative Programming, 27-29 August 2003, Uppsala, Sweden, pages 8–19. ACM,
    2003.
 2. Arthur Charguéraud. Characteristic formulae for the verification of imperative
    programs. In Manuel M. T. Chakravarty, Zhenjiang Hu, and Olivier Danvy, editors,
    Proceeding of the 16th ACM SIGPLAN international conference on Functional
    Programming (ICFP), pages 418–430, Tokyo, Japan, September 2011. ACM.
 3. Olivier Danvy and Kevin Millikin. Refunctionalization at work. Science of Com-
    puter Programming, 74(8):534–549, 2009. Special Issue on Mathematics of Program
    Construction (MPC 2006).
 4. Olivier Danvy and Lasse R. Nielsen. Defunctionalization at work. In Proceedings
    of the 3rd ACM SIGPLAN International Conference on Principles and Practice of
    Declarative Programming, PPDP ’01, pages 162–174. ACM Press, 2001.
 5. Olivier Danvy and Lasse R. Nielsen. Syntactic theories in practice. Electr. Notes
    Theor. Comput. Sci., 59(4):358–374, 2001.
 6. Jean-Christophe Filliâtre. La supériorité de l’ordre supérieur. In Journées Fran-
    cophones des Langages Applicatifs, pages 15–26, Anglet, France, January 2002.
 7. Jean-Christophe Filliâtre and Andrei Paskevich. Why3 — where programs meet
    provers. In Matthias Felleisen and Philippa Gardner, editors, Proceedings of the
    22nd European Symposium on Programming, volume 7792 of Lecture Notes in Com-
    puter Science, pages 125–128. Springer, March 2013.
 8. Jean-Christophe Filliâtre and Mário Pereira. Itérer avec confiance. In Vingt-
    septièmes Journées Francophones des Langages Applicatifs, Saint-Malo, France,
    January 2016.


                                         18
 9. Jean-Christophe Filliâtre and Mário Pereira. A modular way to reason about it-
    eration. In Sanjai Rayadurgam and Oksana Tkachuk, editors, 8th NASA Formal
    Methods Symposium, volume 9690 of Lecture Notes in Computer Science, Min-
    neapolis, MN, USA, June 2016. Springer.
10. Gérard Huet. The Zipper. Journal of Functional Programming, 7(5):549–554,
    September 1997.
11. Johannes Kanig. Spécification et preuve de programmes d’ordre supérieur. Thèse
    de doctorat, Université Paris-Sud, 2010.
12. Johannes Kanig and Jean-Christophe Filliâtre. Who: A Verifier for Effectful
    Higher-order Programs. In ACM SIGPLAN Workshop on ML, Edinburgh, Scot-
    land, UK, August 2009.
13. Yasunori Koda and Frank Ruskey. A Gray Code for the Ideals of a Forest Poset.
    Journal of Algorithms, (15):324–340, 1993.
14. Aleksandar Nanevski, Greg Morrisett, Avi Shinnar, Paul Govereau, and Lars
    Birkedal. Ynot: Reasoning with the awkward squad. In Proceedings of ICFP’08,
    2008.
15. Gordon D. Plotkin. Call-by-name, call-by-value and the lambda-calculus. Theor.
    Comput. Sci., 1(2):125–159, 1975.
16. François Pottier and Nadji Gauthier. Polymorphic typed defunctionalization and
    concretization. Higher-Order and Symbolic Computation, 19:125–162, March 2006.
17. Yann Régis-Gianas and François Pottier. A Hoare logic for call-by-value functional
    programs. In Proceedings of the Ninth International Conference on Mathematics
    of Program Construction (MPC’08), pages 305–335, 2008.
18. John C. Reynolds. Definitional interpreters for higher-order programming lan-
    guages. Higher-Order and Symbolic Computation, 11(4):363–397, December 1998.




                                         19
