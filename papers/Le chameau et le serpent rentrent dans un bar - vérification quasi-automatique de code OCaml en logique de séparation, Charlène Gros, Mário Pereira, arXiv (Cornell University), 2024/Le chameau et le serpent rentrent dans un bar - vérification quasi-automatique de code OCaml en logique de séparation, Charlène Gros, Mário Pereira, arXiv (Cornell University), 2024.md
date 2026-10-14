                                         Le chameau et le serpent rentrent dans
                                          un bar : vérification quasi-automatique
                                         de code OCaml en logique de séparation
                                                                  Charlène Gros1,2 et Mário Pereira2
arXiv:2412.14894v1 [cs.LO] 19 Dec 2024




                                                     1
                                                         Junia ISEN Lille, Lille, 59000, France — Tarides, Paris, 75005, France
                                                           2
                                                             Nova School of Science and Technology, NOVA LINCS, Portugal




                                                 Cet article présente une traduction de programmes OCaml spécifiés en Gospel
                                              vers Viper, un langage intermédiaire de preuves formelles supportant la logique
                                              de séparation. L’objectif pratique est d’ajouter à Cameleer un nouveau backend
                                              pour prouver des programmes OCaml manipulant le tas. La spécification logique
                                              de tels programmes OCaml est décrite dans le langage Gospel et nous détaillons
                                              ici les extensions apportées pour le support de la logique de séparation en Viper.


                                         1 Introduction
                                            Gospel (Generic OCaml Specification Language) [CFLP19] est un langage de spécifica-
                                         tion conçu pour OCaml permettant l’annotation de programmes avec des contrats formels.
                                         Celles-ci spécifient les invariants des types, les pré-conditions et post-conditions des fonc-
                                         tions, les effets, ainsi que les exceptions levées par une fonction. La syntaxe non intrusive
                                         de Gospel facilite la génération de documentation détaillée, permet la génération de tests à
                                         l’aide de l’outil Ortac [FP21] et intègre un support de preuve formelle via Cameleer [PR21]
                                         pour les programmes OCaml.
                                            Les annotations Gospel offrent un moyen fiable de formaliser les comportements attendus
                                         d’un programme OCaml. Elles sont intégrées dans le code source, ce qui fournit une descrip-
                                         tion claire et non ambiguë du comportement des modules et des fonctions, garantissant ainsi
                                         que la documentation reste en phase avec l’implémentation. Cela facilite la compréhension
                                         et la maintenance du code en offrant une référence formelle aux développeurs.
                                            Pour la vérification formelle des programmes OCaml, l’outil Cameleer s’appuie sur Gospel
                                         pour annoter le code OCaml et le traduit ensuite dans le langage WhyML, utilisé par la
                                         plateforme de vérification déductive Why3 [FP13]. Cette dernière s’appuie sur le calcul des
                                         plus faibles pré-conditions, une méthode de vérification déductive qui génère des conjectures
                                         logiques pour chaque programme et qui, une fois vérifiées, garantissent qu’un programme
                                         est conforme à sa spécification. Cette méthode permet de démontrer des propriétés comme
                                         les invariants et les conditions de validité d’un programme, en produisant des obligations de
                                         preuve transmises à des solveurs automatiques tels qu’Alt-Ergo, Z3, CVC5 et bien d’autres.
                                         Toutefois, bien que Why3 gère une forme de mutabilité, elle est limitée lorsqu’il s’agit de
                                         traiter des structures mutables récursives. En effet, le calcul des plus faibles pré-conditions
                                         et le système de types et d’effets de Why3 [FGP16] imposent la gestion statique de l’aliasing,
                                         ce qui empêche notamment l’utilisation de champs à la fois récursifs et mutables au sein de
                                         types ou de structures de données. L’exemple présenté ci-dessous illustre la définition d’une
                                         liste chaînée en WhyML.
                                                                                Gros, Pereira


type t = Nil | Cons cell
with cell = { mutable content: int; mutable next: cell }

  Error: Recursive types cannot have mutable fields
Le type cell est rejeté par Why3, qui interdit un type récursif à contenir un champ mutable
pointant vers lui-même.
   Les outils basés sur la logique de séparation [Rey02] permettent de résoudre une grande
partie de ces problèmes. Le principe fondamental est de raisonner sur des portions disjointes
de mémoire à l’aide de l’opérateur de conjonction séparante. Bien que Why3 impose des
restrictions via un suivi statique des alias, ce qui permet de déterminer précisément quelles
modifications affectent une valeur mutable, il ne peut pas exprimer explicitement la sépa-
ration ou la propriété (ownership) de ces portions de mémoire. En revanche, la logique
de séparation garantit grâce à la distinction des portions de mémoire et la fameuse frame
rule, qu’aucune modification externe n’a eu lieu. L’intégration de cette logique comme nou-
veau backend dans Cameleer permet d’élargir la vérification à un éventail plus vaste de
programmes OCaml annotés avec Gospel.
   Un mécanisme de traduction de code OCaml annoté avec Gospel vers la logique de
séparation est déjà en cours de développement 1 . Celui-ci traduit le programme OCaml
annoté en CFML [Cha11], une extension de Rocq (anciennement Coq) dédiée à la logique
de séparation. Cependant, faire une preuve avec CFML demande toujours une connaissance
de l’assistant de preuve Rocq et cette traduction est limitée aux interfaces OCaml.
   L’extension proposée ici est une traduction vers le langage intermédiaire Viper, qui nous
permet de conduire une preuve quasi-automatique de la correction d’un programme. Viper
(Verification Infrastructure for Permission-based Reasoning) [MSS16] est un outil basé sur
la logique de séparation et une de ses variantes : les Implicit Dynamic Frames [SJP09, PS12].
Il propose un langage intermédiaire ainsi que deux backends de vérification : l’un basé sur
l’exécution symbolique et l’autre sur la génération de conditions de vérification. Ces deux
approches s’appuient sur le solveur SMT « Z3 » pour résoudre les obligations de preuve. Le
langage intermédiaire Viper est un langage impératif et séquentiel, offrant des fonctionnali-
tés de haut niveau pour formuler des problèmes de vérification, tout en étant suffisamment
flexible pour automatiser la vérification dans divers langages de programmation. Il est no-
tamment utilisé pour Rust, Python et Go à travers les frontends respectifs Prusti [AMPS19],
Nagini [EM18], et Gobra [WAC+ 21].
   Le développement présenté dans cet article est une extension de l’outil Cameleer pour
traduire les programmes OCaml annotés vers Viper. Dans la suite nous nous référerons à
cette extension sous le nom de gospel2viper.

Remarque préliminaire. L’extension présentée ici est un travail toujours en cours de
développement. Nous ne traitons qu’un sous-ensemble réduit d’OCaml, qu’on pourrait dire
proche d’ocaml-light : en particulier, définitions et appels de fonctions, variables locales,
type algébriques (mais avec des records en argument), structure conditionnelle, filtrage, af-
fectation de champs mutables. Par conséquent, nous ne supportons ni les boucles ni les
tableaux. En ce qui concerne les définitions de types, nous ne traitons pas les types poly-
morphiques. Nous n’autorisons, pour l’instant, que des entiers comme type des éléments
d’une structure de données. Enfin, côté spécification, nous n’utilisons que des séquences
mathématiques comme modèle logique.


2 Présentation de gospel2viper
  Actuellement, Cameleer prend en charge la traduction vers WhyML, utilisé par Why3.
L’extension gospel2viper vise à résoudre certaines limitations imposées par l’utilisation

   1. voir https://github.com/ocaml-gospel/gospel2cfml
                                                                                 Gros, Pereira


de Why3. Il est toutefois nécessaire d’étendre aussi le langage Gospel avec des constructions
classiques de logique séparation, e.g., la notion de possession des champs d’un record. Dans
cette section nous introduisons au fur et à mesure les concepts les plus importants de Gospel
et Viper utilisés dans notre traduction. L’explication est complétée dans la Section 3, lorsque
ces mêmes concepts sont utilisés dans une étude de cas.
   En Viper, les données mutables sont des références déclarées en tant que champs par
le mot-clé field, et les structures de données sont décrites par des assertions dans des
prédicats de représentation via le mot-clé predicate. C’est dans ce prédicat qu’est notam-
ment décrit le footprint de mémoire d’une structure, ainsi que sa relation avec un modèle
logique. L’opérateur && agit comme la conjonction séparante de la logique de séparation.
En tant qu’abstraction de son contenu, Viper impose l’ouverture explicite d’un prédicat de
représentation par l’opération de dépliage (unfold), afin de révéler son contenu et accéder
aux permissions en mémoire. La fonction opposée est celle de pliage (fold), utilisée pour
abstraire le prédicat de nouveau.
   La traduction de certains éléments d’OCaml vers Viper se révèle triviale, comme la distinc-
tion effectuée par Viper entre les methods et les functions, qui correspond respectivement
aux fonctions OCaml et aux fonctions logiques Gospel définies par le mot-clé function. Le
backend proposé ici utilise l’AST (Abstract Syntax Tree) de Cameleer, lui-même basé sur
l’AST non-typé d’OCaml. Bien que le langage Viper nécessite les types explicites, nous de-
mandons pour le moment de les inclure dans le code OCaml et Gospel. L’ajout de l’inférence
de type au sein de l’extension viendra dans le futur.
   Les paragraphes suivants détaillent les spécificités du langage Viper, ainsi que les moyens
mis en place pour trouver l’ensemble des informations dans le code Cameleer pour procéder
à la traduction. Tous les exemples affichent à gauche le code Cameleer et à droite leur
traduction en Viper.

Références en Viper. Pour créer une ressource accessible via une référence en Viper,
celle-ci doit être déclarée comme un field. Ensuite, chaque variable de type Ref pourra
accéder à l’entièreté des champs déclarés, car il n’y a aucune notion d’encapsulation en
Viper. Cependant, pour préciser quels champs sont utilisés par une ressource donnée, il est
nécessaire de demander explicitement les permissions correspondantes à l’aide de l’instance
acc, comme illustré par la suite. La définition de champs est naturellement décrite en OCaml
par un record, ce qui nous permet d’avoir toutes les informations sur les types des différents
fields Viper.

Encodage des types algébriques en Viper. Prenons le type OCaml suivant. Il reprè-
sente une liste chainée avec deux champs mutables.
type cell = Nil | Cons { mutable content: int; mutable next: cell }
Comme Viper fournit la constante null pour le type Ref, il serait tentant de traduire le
constructeur Nil d’OCaml vers null. Néanmoins, une telle approche ne serait pas satisfai-
sante quand une définition de type OCaml présente plusieurs cas de base. Une extension
à Viper a été récemment proposée pour encoder dans ce langage une notion de type al-
gébrique [Mai22]. C’est exactement cette approche que nous utilisons dans gospel2viper.
Cela permet de décrire de manière très similaire en Viper la structure d’un type OCaml,
comme montré en Figure 1 pour la liste chaînée.
  En Viper, nous créons une instance d’un ADT (Algebraic DataTypes) Cell, qui est soit
Nil() (pas d’argument), soit Cons avec un argument de type Ref nommé ici cell (tout
autre nom serait également acceptable). Enfin, nous pouvons introduire les deux champs
content et next, que nous utiliserons uniquement lorsqu’une valeur du type Cell sera
non-Nil. Il est aussi important de mentionner que cette utilisation de la construction adt
en Viper nous donne automatiquement deux destructeurs mutuellement exclusifs d’une
Cell : isNil et isCons. Par exemple, pour un certain c de type Cell, si c.isNil se vérifie,
                                                                                Gros, Pereira


type cell =                                   adt Cell {
  | Nil                                         Nil()
  | Cons of { mutable content : int;            Cons(cell: Ref)
              mutable next : cell }           }
                                              field content : Int
                                              field next: Cell

      Figure 1. Encodage du type de listes chaînées à l’aide des ADTs en Viper.


alors Viper nous empêche d’accéder au champ next de c. Néanmoins, le filtrage par motif
(pattern-matching) doit encore être géré manuellement en utilisant ces mêmes destructeurs
dans une séquence imbriquée de if..else.

La possession d’un champ mutable. En Viper, le prédicat d’accessibilité acc est uti-
lisé pour la gestion des permissions d’accès aux champs d’un objet. Chaque opération, qu’il
s’agisse d’une expression, d’une assertion ou d’une modification d’état, nécessite explicite-
ment une permission afin d’accéder aux champs du programme. Ceci permet de déterminer
quelles portions de la mémoire sont affectées par une opération. Les permissions garantissent
la sécurité et l’intégrité du programme, notamment au travers du mécanisme de framing,
qui permet de préserver des propriétés sur la mémoire entre des appels de méthodes ou des
opérations distinctes. L’utilisation de acc(x.f) dans une pré-condition signifie que l’appe-
lant d’une méthode doit céder temporairement le droit d’accès au champ x.f à la méthode
appelée. En contrepartie, l’apparition de acc(x.f) dans une post-condition indique que
cette permission sera rendue à l’appelant une fois l’opération terminée. Si plusieurs champs
demandent la permission, les prédicats d’accéssibilité acc seront séparés par l’opérateur
&&, qui sera compris en tant que conjonction séparante. Cela permet de garantir que les
opérations n’interfèrent pas entre elles et ne modifient pas des champs pour lesquels elles
n’ont pas explicitement obtenu l’accès, assurant ainsi une gestion fine des ressources et une
absence d’aliasing entre les différentes parties du programme. Pour couvrir cette nouvelle
idée qui n’existe pas encore dans Gospel, nous avons ajouté l’opérateur wiggle arrow ( ).
Ci-dessous, l’annotation Gospel (à gauche) et sa traduction Viper (à droite) :

  c    {content; next}                           acc(c.content) && acc(c.next)


Cet opérateur permet de spécifier de manière précise la possession d’un record et la posses-
sion individuelle de chaque champ. Cette notion de possession des champs de record, ainsi
que l’opérateur ( ), sont fortement inspirées par CFML.

Définition de prédicats de représentation. En Viper, un prédicat de représentation
est un mécanisme d’abstraction sur les assertions, y compris sur les ressources telles que
les permissions d’accès à des champs. Il permet de regrouper sous une forme compacte
et paramétrée des propriétés et permissions liées à des structures de données potentielle-
ment récursives. Contrairement aux fonctions, les prédicats ne sont pas automatiquement
développés : leur corps qui constitue une assertion doit être explicitement révélé à l’aide
de l’instruction unfold, ou masqué avec l’instruction fold. Ces prédicats sont définis en
Gospel par le mot-clé predicate en exprimant les mêmes assertions.

Opérations fold / unfold et apply. L’opération unfold modifie l’état du programme
en remplaçant la ressource du prédicat par les assertions de son corps, donnant alors l’accès
aux fields. Une variante de cette opération existe pour temporairement exposer l’intérieur
du prédicat, avec unfolding ... in. L’opération inverse, fold, remplace les assertions
                                                                                  Gros, Pereira


par une instance du prédicat. Cette dernière, notée P(e1 , ..., en ), est une assertion de
ressource dans Viper qui peut être consommée ou produite.
   Ci-dessous, nous présentons l’implémentation d’une méthode Viper simple pour changer
la valeur d’une référence, en omissant les permissions sur les champs.
field v: Int
predicate P (c: Ref) { // prédicat cachant la possession du champ v }
method foo (c: Ref)
  requires P(c)
  ensures P(c)
    { ✿✿✿✿✿✿✿✿✿
       c.v := 0 }

Error: Assignment might fail. There might be insufficient permission to
       access c.v
Viper indique que cela peut échouer car il n’a pas la permission d’accès au champ c.v. Pour
que Viper puisse prouver cette implémentation, il faut ajouter en première instruction le
dépliage de P pour y exposer les permissions. À la fin, il faut utiliser fold pour rétablir le
prédicat. Sans ces appels à fold et unfold, Viper n’est pas capable de suivre l’évolution de
qui possède les permissions, et donc ne peut assurer que les modifications n’ont pas changé
un autre morceau de la mémoire.
  À ce jour, aucune solution de génération automatique de ces appels n’est connue, ce qui
oblige les programmeurs Viper à les spécifier manuellement. Par conséquent, il est également
nécessaire d’inclure dans les annotations Gospel cette notion, car l’utilisateur n’est pas censé
toucher à la traduction Viper.
  Pour permettre l’utilisation de lemmes auxiliaires traduits sous forme de méthodes en Vi-
per, nous avons introduit l’opération apply dans Gospel. Elle permet d’appeler ces lemmes
directement depuis les annotations sans interférer avec le code OCaml, bien qu’elles doivent
être placées dans l’implémentation OCaml, tout comme les appels à fold et unfold.


3 Étude de cas : module Queue d’OCaml
  Dans cette section, nous présentons la vérification formelle du module Queue de la biblio-
thèque standard d’OCaml. Dans cette implémentation, le type des files utilise des références
pour avoir des opérations d’ajout, de concaténation et de retrait en temps constant. Nous
présentons à gauche le code OCaml annoté et à droite sa traduction en Viper générée par
notre extension.

Définition de segments de liste. En utilisant l’encodage des listes chaînées comme
montré dans la Figure 1, nous introduisons le prédicat cellSeg comme suit :

  (*@ predicate cellSeg                           predicate CellSeg (from: Cell,
      (from: cell)                                  v: Seq[Int], to: Cell)
      (v: int sequence)                           { v == Seq[Int]() ?
      (to: cell)                                      to == from
     = if v = empty then to = from                  : from.isCons &&
       else                                           let c == (from.cell) in
         let Cons c = from in                         acc(c.content) &&
         c    {content; next} &&                      acc(c.next) &&
         c.content = v[0] &&                          c.content == v[0] &&
         cellSeg c.next (v[1 ..]) to *)               CellSeg(c.next, v[1 ..], to) }
Ce prédicat cellSeg (pour « segment de cellules ») décrit une succession de cellules entre
deux références : from et to, ayant pour modèle la séquence d’entiers v. Ce prédicat véri-
fie dans un premier temps que si le modèle est vide alors il n’y a aucune cellule entre les
deux bornes from et to. Sinon, nous avons accès aux champs content et next de l’élément
                                                                                  Gros, Pereira


courant et nous continuons la récursion sur la cellule suivante jusqu’à atteindre la fin du
segment. À chaque itération, il est vérifié que le contenu courant de la cellule est bien le
même que la tête du modèle, lui-même dépilé lors de l’appel récursif. L’accès aux champs
content et next par la cellule from est modélisé par le nouvel opérateur ( ) en Gospel. Il
se traduit en un appel au prédicat d’accessibilité acc de Viper et permet de demander le
transfert des permissions afin de pouvoir lire les valeurs des champs demandés.
  Remarquons la construction let Cons c = from in : sa sémantique est que from est for-
cément une cellule de la forme Cons. Cela se traduit en Viper par le destructeur from.isCons.

Définition de la structure de file. Nous présentons en ci-dessous le type queue et le
prédicat de représentation de la file.

  type queue = {                                  field length: Int
    mutable length : int;                         field first: Cell
    mutable first : cell;                         field last: Cell
    mutable last : cell
  }                                               predicate Queue (q: Ref, v: Seq[Int])
                                                  {
  (*@ predicate queue (q: queue)                    acc(q.length) && acc(q.first) &&
      (v: int sequence) =                           acc(q.last) &&
    q    {length; first; last} &&                   (v == Seq[Int]()
    if v = empty then                                ? q.first.isNil && q.last.isNil
      q.first = Nil && q.last = Nil &&                 q.length == 0
      q.length = 0                                   : |v| == q.length &&
    else                                               CellSeg(q.first, drop_last(v),
      length v = q.length &&                                   q.last) &&
      cellSeg q.first (drop_last v)                    CellSeg(q.last, take_last(v),
              q.last &&                                        Nil()))
      cellSeg q.last (take_last v) Nil *)         }
Elle est représentée par trois champs mutables : length qui stocke la longueur de la file,
first qui est la première cellule de la file et last qui est sa dernière cellule. Le prédicat
queue décrit l’état de la file par rapport au modèle v. Ensuite, deux cas sont possibles une
fois les accès en mémoire demandés : si la file est vide alors les cellules de début et de
fin sont Nil, ainsi que la taille vaut zéro ; sinon, les tailles doivent être les mêmes, et l’on
asserte que le segment de cellules de la première à l’avant dernière est bien formé et que la
dernière cellule contient effectivement le dernier élément du modèle.

Création de file. La fonction create est utilisée pour créer une nouvelle file vide. Voici
son implémentation et sa spécification logique :

  let create () : queue =                         method create () returns (q: Ref)
    let q : queue =                                 ensures Queue(q, Seq[Int]())
      Cons { length = 0;                          {
             first = Nil;                           q := new(length, first, last)
             last   = Nil } in                      q.length := 0
    (*@ fold queue q empty *)                       q.first := Nil();
    q                                               q.last := Nil();
  (*@ q = create ()                                 fold Queue(q, Seq[Int]())
        ensures queue q empty *)                  }
  La post-condition de cette fonction spécifie qu’à la fin de son exécution, la file renvoyée
sera bien formée. C’est l’instruction let ... = ... in qui remplit le record. Elle est scindée
en deux en Viper : en premier, l’instruction new{...} va assigner une nouvelle référence
pour q et aspirer les permissions d’écriture des champs entre accolades. Ces permissions
sont ensuite expirées via l’instruction fold, qui atteste que la file fraîchement crée est vide
                                                                                 Gros, Pereira


et bien formée. Ensuite les champs sont initialisés.

Ajout d’un élément. Nous continuons cette étude de cas par la présentation de la
spécification de la fonction qui ajoute un élément à la fin de la file. L’intégralité de cette
preuve ainsi que sa traduction en Viper est entièrement disponible en ligne 2 .
  Pour raisonner sur la concaténation de plusieurs segments de listes, nous devons faire
appel à des lemmes classiques de logique de séparation [Cha16]. En particulier, le lemme
sur la transitivité de la concaténation de trois segments de liste que l’on retrouve en Gospel
de la manière suivante :
(*@ lemma cellSeg_trans (c1: cell) (c2: cell) (c3: cell)
             (v1: int sequence) (v2: int sequence) (v3: int sequence)
    requires cellSeg(c1, v1, c2) && cellSeg(c2, v2, c3) &&
             cellSeg(c3, v3, Nil)
    ensures cellSeg(c1, v1 ++ v2, c3) && cellSeg(c3, v3, Nil) *)
Avec ce lemme nous allons pouvoir montrer qu’à chaque fois que l’on ajoute un élément à
la fin de la file, cela va créer un nouveau segment de liste qui sera ensuite concaténé au
segment de liste partant de la référence last. La spécification de la fonction d’ajout est
simple et sa traduction est triviale, comme visible ci-dessous :

  let add (q: queue) (x: int) = ...              method add (q: Ref, x: Int, v: Seq[Int])
  (*@ add x q [v: int sequence]                    requires Queue(q, v)
      requires queue q v                           ensures Queue(q, v ++ Seq(x))
      ensures queue q (v ++                      { ... }
               (singleton x)) *)
En entrée la fonction reçoit une file valide et doit en renvoyer une dans laquelle la valeur
x aura été ajoutée. La fonction logique singleton renvoie une séquence qui ne contient
que l’élément passé comme argument. Nous utilisons les arguments ghost de Gospel pour
transmettre le modèle à la fonction. Cet argument ghost, ici nommé v, est alors ajouté aux
arguments lors de la traduction en Viper.
  Bien que l’implémentation en OCaml soit simple, il est nécessaire de détailler les suc-
cessions de pliages et de dépliages des prédicats de représentation, ainsi que l’appel à
CellSegTrans. Nous détaillons dans le code suivant le cas où une valeur est ajoutée à
une file vide.

    let cell = Cons {                               var c : Ref := new(content, next)
      content = x;                                  c.content := x
      next = Nil                                    c.next := Nil()
    } in                                            var cell : Cell := Cons(c)
    match q.last with                               if (q.last.isNil) {
    | Nil ->                                          q.length := 1
      q.length <- 1;                                  q.first := cell
      q.first <- cell;                                q.last   := cell
      q.last   <- cell;                               fold CellSeg(Nil(), Seq[Int](),
      (*@ fold cellSeg Nil empty Nil *)                            Nil())
      (*@ fold cellSeg cell                           fold CellSeg(q.last, Seq(x), Nil())
               (singleton x) Nil *)                   fold CellSeg(q.first, Seq[Int](),
      (*@ fold cellSeg q.first empty                               q.last)
               q.last *)                            }


Notons que le filtrage de la valeur Nil est traduit vers le destructeur isNil en Viper. La
séquence de trois opérations fold nous permet de montrer la validité du prédicat queue
quand la file possède un seul élément. Les deux premiers folds sont utilisés pour montrer

  2. https://github.com/ocaml-gospel/gospel2viper/blob/main/example
                                                                                 Gros, Pereira


qu’entre q.last et Nil il existe effectivement un segment de liste contenant seulement l’élé-
ment x. Le dernier appel à fold montre qu’entre q.first et q.last il y a un segment de
liste vide.
   Pour ce qui est du cas de la file non vide, la preuve s’achève par un appel au lemme
CellSeg_trans comme suit :
    | Cons last -> ...                              else { ...
      (* cascade de [fold]s *)                        // cascade de [fold]s
      (*@ apply CellSeg_trans q.first                 CellSeg_trans(q.first, q.last,
            q.last cell (drop_last v)                                cell, drop_last(v),
            (take_last v) (singleton x) *)            q.last <- cell
      q.last <- cell                                }


La fonction logique drop_last renvoie une nouvelle séquence sans le dernier élément de
la séquence passée en argument tandis que la fonction take_last renvoie une séquence
qui ne contient que le dernier élément de son argument. Avec le lemme CellSeg_trans,
nous obtenons la possession d’un segment de liste entre q.first et cell avec la séquence
d’éléments v (drop_last(v) ++ take_last(v) = v). Enfin, avec ce résultat et la dernière
affectation q.last <- cell, nous parvenons à rétablir le prédicat de représentation de la
file étendue avec un nouvel élément. Nous omettons ici la « cascade » d’opérations fold qui
nous permet de reconstruire des segments de liste entre q.first, q.last et cell, réunissant
les permissions nécessaires pour l’appel au lemme auxiliaire.

Concaténation de deux files. Nous finissons notre étude de cas par la concaténation de
deux files. Dans le module Queue, la fonction qui concatène deux files est nommée transfer.
L’appel transfer q1 q2 va concaténer les éléments de q1 à la fin de q2, en vidant par la
même occasion le contenu de q1. En pratique, il s’agit tout simplement de relier le champ
last de q2 au champ first de q1 et puis d’affecter q2.last à q1.last. Cette opération
illustre tout à fait l’intérêt de maintenir des pointeurs vers le premier et dernier élément de
la file puisque nous arrivons à concaténer deux files en temps constant. La spécification de
la fonction transfer est tout aussi directe, comme illustré ci-dessous :

  let transfer                                    method transfer (q1: Ref, q2: Ref,
    (q1: queue) (q2: queue) =...                    v1: Seq[Int], v2: Seq[Int])
  (*@ transfer q1 q2 [v1: int sequence]             requires Queue(q1, v1) && Queue(q2, v2)
               [v2: int sequence]                   ensures Queue(q1, Seq[Int]())
      requires queue q1 v1 && queue q2 v2           ensures Queue(q2, v2 ++ v1)
      ensures queue q1 empty                      { ... }
      ensures queue v2 (v2 ++ v1) *)


En pré-condition, nous exigeons la possession des files q1 et q2 avec respectivement les mo-
dèles v1 et v2. À la fin de l’exécution, nous conservons la possession de q1 et q2 mais leurs
modèles respectifs sont mis à jour. Nous nous concentrons sur le cas le plus intéressant de
cette fonction : quand q1 et q2 sont toutes deux non vides. Le code OCaml, sa spécification
Gospel, ainsi que la traduction obtenue en Viper sont donnés ci-après.
                                                                                   Gros, Pereira



    if q1.length > 0 then                            if (q1.length > 0) {
      match q2.last with                               if (q2.last.isNil) { ... }
      | Nil -> ...                                     else {
      | Cons last ->                                     q2.length := q2.length + q1.length
        q2.length <- q2.length + q1.length;              unfold CellSeg(q2.last,
        (*@ unfold cellSeg q1.last                                      take_last(v1),
                   (take_last v1)                                       Nil())
                   Nil *)                                q2.last.cell.next := q1.first
        last.next <- q1.first;                           // cascade de [fold]s
        (* cascade de [fold]s *)                         fold ...
        (*@ fold ... *)                                  CellSeg_trans(q2.last, q1.first,
        (*@ apply CellSeg_trans q1.last                                q1.last,
                  q.first q.last                                       take_last(v1),
                  (take_last v1)                                       drop_last(v),
                  (drop_last v)                                        take_last(v))
                  (take_last v) *)                       CellSeg_trans(q2.first,
        (*@ apply CellSeg_trans                                        q2.last, q1.last,
                  q1.first q1.last                                     drop_last(v1),
                  q.last (drop_last v1)                                take_last(v1) ++
                  ((take_last v1)                                         drop_last(v),
                    ++ (drop_last v))                                  take_last(v))
                  (take_last v) *)                       q2.last := q1.last
        q2.last <- q1.last;                              clear(q1)
        clear q1                                       }


Commençons par noter que le filtrage de la valeur Cons last correspond en Viper, à la
branche else. Dans ce cas, nous sommes sûrs que la condition q2.last.isCons se vérifie.
La preuve s’appuie sur deux appels successifs au lemme CellSeg_trans. Le premier permet
d’établir l’existence d’un segment de liste entre q2.last et q1.last. Le second utilise le
segment construit par l’appel précédent et rend la possession d’un segment entre q2.first
et q1.last, ce qui permet d’établir la validité de file concaténée. Finalement, l’appel à
clear a pour but de vider le contenu de la file q1, respectant ainsi la post-condition de la
fonction transfer.


4 Conclusion et perspectives
   Dans cet article, nous avons présenté une extension de l’outil Cameleer permettant de
traduire des programmes OCaml annotés avec Gospel vers le langage intermédiaire Viper.
Cette traduction ajoute un backend de logique de séparation à Cameleer afin de permettre
la vérification formelle de programmes manipulant des structures allouées sur le tas. Nous
avons présenté les nouveaux éléments ajoutés au langage Gospel et pour chacun, détaillé
comment notre extension les transmet lors de la traduction vers Viper. Nous avons illus-
tré l’application de cette extension par la preuve formelle de l’implémentation de certaines
fonctions du module Queue d’OCaml. Il serait pertinent de tester la traduction sur d’autres
structures de données d’OCaml, comme les tables de hachage. Cela permettrait de varier les
types utilisés et d’identifier les limites potentielles de l’extension actuelle. L’ajout d’autres
éléments de spécification (e.g., multiensemble), le polymorphisme d’OCaml et d’autres struc-
tures de contrôle afin d’étendre les possibilités de programmes prouvables par ce backend
est aussi envisagé. Finalement, il serait intéressant d’étudier la génération automatique de
certaines opérations fold et unfold. Actuellement, ces opérations doivent être insérées ma-
nuellement dans le code OCaml, ce qui peut être à la fois laborieux et source d’erreurs.
L’automatisation de cette étape permettrait de simplifier la vérification, et des pistes dans
cette direction sont d’ores et déjà l’étude.
                                                                           Gros, Pereira


Références
[AMPS19] Vytautas Astrauskas, Peter Müller, Federico Poli et Alexander J. Sum-
          mers : Leveraging Rust types for modular specification and verification. Proc.
         ACM Program. Lang., 3(OOPSLA):147 :1–147 :30, 2019.
[CFLP19] Arthur Charguéraud, Jean-Christophe Filliâtre, Cláudio Lourenço et
          Mário Pereira : GOSPEL—providing OCaml with a Formal Specification
          Language. In Maurice H. ter Beek, Annabelle McIver et José N. Oliveira,
          éditeurs : Formal Methods – The Next 30 Years, pages 484–501, Cham, 2019.
          Springer International Publishing.
[Cha11]   Arthur Charguéraud : Characteristic formulae for the verification of im-
          perative programs. In Proceedings of the 16th ACM SIGPLAN International
         Conference on Functional Programming, ICFP ’11, pages 418–430, New York,
          NY, USA, 2011. Association for Computing Machinery.
[Cha16]   Arthur Charguéraud : Higher-order representation predicates in separation
          logic. In Proceedings of the 5th ACM SIGPLAN Conference on Certified Pro-
         grams and Proofs, CPP 2016, page 3–14, New York, NY, USA, 2016. Association
          for Computing Machinery.
[EM18]    Marco Eilers et Peter Müller : Nagini : A Static Verifier for Python. In Hana
          Chockler et Georg Weissenbacher, éditeurs : Computer Aided Verification
         - 30th International Conference, CAV 2018, Held as Part of the Federated Lo-
         gic Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings, Part I,
         volume 10981 de Lecture Notes in Computer Science, pages 596–603. Springer,
         2018.
[FGP16] Jean-Christophe Filliâtre, Léon Gondelman et Andrei Paskevich : A Prag-
          matic Type System for Deductive Verification. Rapport technique, février 2016.
          https://inria.hal.science/hal-01256434v3/file/main%20%281%29.pdf.
[FP13]    Jean-Christophe Filliâtre et Andrei Paskevich : Why3 - Where Programs
          Meet Provers. In Matthias Felleisen et Philippa Gardner, éditeurs : Pro-
         gramming Languages and Systems - 22nd European Symposium on Program-
         ming, ESOP 2013, Held as Part of the European Joint Conferences on Theory
         and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Pro-
         ceedings, volume 7792 de Lecture Notes in Computer Science, pages 125–128.
          Springer, 2013.
[FP21]    Jean-Christophe Filliâtre et Clément Pascutto : Ortac : Runtime Assertion
          Checking for OCaml (Tool Paper). In Lu Feng et Dana Fisman, éditeurs :
         Runtime Verification - 21st International Conference, RV 2021, Virtual Event,
         October 11-14, 2021, Proceedings, volume 12974 de Lecture Notes in Computer
         Science, pages 244–253. Springer, 2021.
[Mai22]   Alessandro Maissen : Adding algebraic data types to a verification language.
         Practical work, ETH Zurich, 2022.
[MSS16] Peter Müller, Malte Schwerhoff et Alexander J. Summers : Viper : A
         Verification Infrastructure for Permission-Based Reasoning. In Barbara Jobst-
          mann et K. Rustan M. Leino, éditeurs : Verification, Model Checking, and
         Abstract Interpretation - 17th International Conference, VMCAI 2016, St. Pe-
         tersburg, FL, USA, January 17-19, 2016. Proceedings, volume 9583 de Lecture
         Notes in Computer Science, pages 41–62. Springer, 2016.
[PR21]    Mário Pereira et António Ravara : Cameleer : A Deductive Verification Tool
          for OCaml. In Alexandra Silva et K. Rustan M. Leino, éditeurs : Computer
         Aided Verification - 33rd International Conference, CAV 2021, Virtual Event,
         July 20-23, 2021, Proceedings, Part II, volume 12760 de Lecture Notes in Com-
          puter Science, pages 677–689. Springer, 2021.
                                                                           Gros, Pereira


[PS12]     Matthew J. Parkinson et Alexander J. Summers : The Relationship Between
           Separation Logic and Implicit Dynamic Frames. Logical Methods in Computer
           Science, 8(3 :01):1–54, 2012.
[Rey02]    John C. Reynolds : Separation Logic : A Logic for Shared Mutable Data
           Structures. In Proceedings of the 17th Annual IEEE Symposium on Logic in
           Computer Science, LICS ’02, pages 55–74, USA, 2002. IEEE Computer Society.
[SJP09]    Jan Smans, Bart Jacobs et Frank Piessens : Implicit Dynamic Frames :
           Combining Dynamic Frames and Separation Logic. In European Conference on
           Object-Oriented Programming, 2009.
[WAC+ 21] Felix A. Wolf, Linard Arquint, Martin Clochard, Wytse Oortwijn,
          João Carlos Pereira et Peter Müller : Gobra : Modular Specification and
          Verification of Go Programs. In Alexandra Silva et K. Rustan M. Leino, édi-
          teurs : Computer Aided Verification - 33rd International Conference, CAV 2021,
          Virtual Event, July 20-23, 2021, Proceedings, Part I, volume 12759 de Lecture
          Notes in Computer Science, pages 367–379. Springer, 2021.
