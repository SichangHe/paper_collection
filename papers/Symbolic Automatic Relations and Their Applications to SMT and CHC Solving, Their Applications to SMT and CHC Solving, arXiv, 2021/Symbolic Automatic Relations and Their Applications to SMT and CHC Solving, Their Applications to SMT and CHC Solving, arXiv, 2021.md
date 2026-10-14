                                                  Symbolic Automatic Relations and
                                             Their Applications to SMT and CHC Solving

                                         Takumi Shimoda1 , Naoki Kobayashi1 , Ken Sakayori1 , and Ryosuke Sato1
arXiv:2108.07642v1 [cs.LO] 17 Aug 2021




                                                                 The University of Tokyo, Tokyo, Japan



                                                 Abstract. Despite the recent advance of automated program verifica-
                                                 tion, reasoning about recursive data structures remains as a challenge
                                                 for verification tools and their backends such as SMT and CHC solvers.
                                                 To address the challenge, we introduce the notion of symbolic automatic
                                                 relations (SARs), which combines symbolic automata and automatic re-
                                                 lations, and inherits their good properties such as the closure under
                                                 Boolean operations. We consider the satisfiability problem for SARs,
                                                 and show that it is undecidable in general, but that we can construct a
                                                 sound (but incomplete) and automated satisfiability checker by a reduc-
                                                 tion to CHC solving. We discuss applications to SMT and CHC solving
                                                 on data structures, and show the effectiveness of our approach through
                                                 experiments.


                                         1     Introduction
                                         The recent advance of automated or semi-automated program verification tools
                                         owes much to the improvement of SMT (Satisfiability Modulo Theory) and CHC
                                         (Constrained Horn Clauses) solvers. The former [1, 23] can automatically check
                                         the satisfiability of quantifier-free formulas modulo background theories (such
                                         as linear integer arithmetic), and the latter [6, 17, 20] can automatically reason
                                         about recursively defined predicates (which can be used to model loops and
                                         recursive functions). Various program verification problems can be reduced to
                                         CHC solving [3]. The current SMT and CHC solvers are, however, not very good
                                         at reasoning about recursive data structures (such as lists and trees), compared
                                         with the capability of reasoning about basic data such as integers and real num-
                                         bers. Indeed, improving the treatment of recursive data structures has recently
                                         been an active research topic, especially for CHC solvers [6, 9, 13, 27].
                                             In the present paper, we propose an automata-based approach for check-
                                         ing the satisfiability of formulas over recursive data structures. (For the sake
                                         of simplicity, we focus on lists of integers; our approach can, in principle, be
                                         extended for more general data structures). More precisely, we introduce the no-
                                         tion of symbolic automatic relations, which is obtained by combining automatic
                                         relations [4] and symbolic automata [8, 28, 29].
                                             A k-ary automatic relation is a relation on k words1 that can be recognized
                                         by a finite state automaton that reads k words in a synchronous manner (so,
                                         1
                                             We use “lists”, “words”, and “sequences” interchangeably.
2         T. Shimoda et al.


Msync                          Msymb                                   M<
         (a, a)                                  0<x                            l0 < l1
                                       q0                      q1
            q      (b, b)                                                          q
                                                 x<0

    Fig. 1. Examples of synchronous, symbolic and symbolic synchronous automaton.


given k words, x01 · · · x0m , . . . , x(k−1)1 · · · x(k−1)m , the automaton reads a tuple
(x0i , . . . , x(k−1)i ) at each transition; if the input words have different lengths,
the special padding symbol  is filled at the end). For example, the equality
relation on two words over the alphabet {a, b} is an automatic relation, since
it is recognized by the automaton with a single state q (which is both initial
and accepting) with the transition δ(q, (a, a)) = q and δ(q, (b, b)) = q. By using
automatic relations, we can express and manipulate relations on data structures.
    Since data structures typically contain elements from an infinite set, we ex-
tend automatic relations by using symbolic automata. Here, a symbolic automa-
ton is a variation of finite state automaton whose alphabet is possibly infinite,
and whose transition is described by a formula over elements of the alphabet. For
example, Msymb on Fig. 1 is a symbolic automaton that accepts the sequences of
integers in which positive and negative integers occur alternately, and the first
element is a positive integer. The symbolic automatic relations introduced in this
paper are relations recognized by symbolic automata that read input words (over
a possibly infinite alphabet) in a synchronous manner. For example, consider the
binary relation:
    R< = {(l01 · · · l0n , l11 · · · l1n ) ∈ Z∗ × Z∗ | l0i < l1i for every i ∈ {1, . . . , n}}.
It is a symbolic automatic relation, as it is recognized by the symbolic syn-
chronous automaton M< on Fig. 1 (where l0 and l1 are bound to l0i and l1i at
the i-th transition step).
    Symbolic automatic relations (SARs) inherit good properties of automatic
relations and symbolic automata: SARs are closed under Boolean operations,
and the emptiness problem of SAR (the problem of deciding whether R = ∅,
given the representation of a SAR R) is decidable if the underlying theory (e.g.
linear integer arithmetic) used for representing transitions is decidable.
    We are interested in the satisfiability problem for SARs, i.e., the problem
of checking whether a given existentially-quantified formula (obtained by ex-
tending the signature of linear integer arithmetic with SARs and list construc-
tors/destructors) is satisfiable. For example, whether R< (X, Y ) ∧ R< (Y, X) is
satisfiable (the answer is “No”) is an instance of the problem. The class of
existentially-quantified formulas considered in the satisfiability problem is rea-
sonably expressive. For example, although the sortedness predicate sorted (X)
and the predicate nth(X, i, x) (the i-th element of X is x) are themselves not
automatic relations, we can allow those predicates to occur in the formulas, as
explained later. (Unfortunately, however, we cannot express the “append” rela-
tion.)
                                              Symbolic Automatic Relations        3

    We first show that the satisfiability problem for SARs is undecidable, unfor-
tunately. The proof is based on a reduction from the undecidability of the halting
problem for Minsky machines (or, two-counter machines). Next, we show that
the satisfiability problem for SARs can be reduced to the satisfiability problem
for Constrained Horn Clauses (CHCs) over integers (without lists). Thanks to
the recent development of efficient CHC solvers [6, 17, 20], we can thus obtain a
sound, automated (but incomplete) procedure for solving the satisfiability prob-
lem for SARs. We show, through experiments, that our reduction is effective, in
that the combination of our reduction with off-the-shelf CHC solvers can solve
the satisfiability problem for various formulas over lists that cannot be solved
by state-of-the-art SMT solvers such as Z3 and CVC4.
    Besides the above-mentioned improvement of SMT solvers on recursive data
structures, we also have in mind an application to CHC solving (indeed, im-
proving CHC solvers was the original motivation of our work). The goal of CHC
solving is to check whether a given set of CHCs has a model (interpretations for
predicate variables that make all the clauses valid). Many of the CHC solvers
prove the satisfiability of given CHCs by constructing an actual model. The
main problem on such CHC solvers in dealing with recursive data structures is
that the language for describing models is too restrictive: especially, it cannot
express recursively defined predicates on recursive data structures (apart from
some built-in predicates such as the “length” predicate). Our symbolic auto-
matic relations can be used to enhance the expressive power of the language. The
above-mentioned procedure for the SAR satisfiability problem can be directly
applied to an ICE-based CHC solver like HoIce [6]. HoIce consists of a learner,
which constructs a candidate model, and a teacher, which checks whether the
candidate is indeed a model. Our procedure can be used by the teacher, when
a given candidate is described by using symbolic automatic relations. Later in
the paper, we give examples of CHCs whose models can only be expressed by
using symbolic automatic relations, and show through experiments that our pro-
cedure can indeed be used for checking the validity of models described by using
symbolic automatic relations.
    Our contributions are: (i) introduction of symbolic automatic relations and
discussions of applications to SMT and CHC solving; (ii) a proof of the unde-
cidability of the satisfiability problem on SARs; (iii) a sound (but incomplete)
decision procedure for the satisfiability problem on SARs, via a reduction to
CHC solving on integers (iv) an implementation and experiments to confirm the
effectiveness of the above decision procedure.
    The rest of this paper is structured as follows. Section 2 briefly reviews the
notions used in many-sorted first-order logic. Section 3 defines symbolic auto-
matic relations and demonstrates how they can be used to express predicates
over lists. Section 4 shows that the satisfiability problem for SARs is undecidable.
Section 5 shows a reduction from the satisfiability problem for SARs to CHC
solving, and Section 6 reports experimental results. Section 7 discusses related
work and Section 8 concludes the paper.
4       T. Shimoda et al.

2     Preliminaries
This section introduces basic notions and notations used in the sequel.

Notations Given a set S, we write S ∗ for the set of all finite sequences over S. A
word w ∈ S ∗ is either written as w = a1 · · · an or w = [a1 , . . . , an ], where ai ∈ S;
the empty word is denoted as ǫ or [ ]. The set of integers is written as Z.

2.1    FOL with list
Syntax A (multi-sorted) signature is a triple (Ty, Fn, Pd), where Ty is a
set of sorts (aka types), Fn is a set of (typed) function symbols and, Pd is
a set of (typed) predicate symbols. There are two signatures that play im-
portant roles in this paper: the signature of integer arithmetic and the sig-
nature for integer lists. We define the signature of integer arithmetic τint as
({Int}, Fnint , Pdint ). The set Fnint contains the function symbols for integer
arithmetic such as 0, s, + and Pdint contains the predicates for integer arith-
metic such as =int , <, ≤; the precise definition is not important. The signature of
                                  def
integer lists is defined by τlist = ({Int, List Int }, Fnint ∪ Fnlist , Pdint ∪ {=list }),
              def
where Fnlist = {nil , cons, head , tail }. Here, nil and cons have type List Int and
(Int, List Int) → List Int and their intended meanings are the empty list and
the “cons function”, respectively. As the name suggests, head : List Int → Int
and tail : List Int → List Int will be interpreted as head and tail functions.
    The set of terms and the set of formulas over a signature τ = (Ty, Fn, Pd)
is defined as follows:

          t ::= x | f (t1 , . . . , tn )
          ϕ ::= ⊤ | ⊥ | P (t1 , . . . , tn ) | ¬ϕ | ϕ1 ∧ ϕ2 | ϕ1 ∨ ϕ2 | ∀xϕ | ∃xϕ

where x ranges over the denumerable set of variables, f ranges over Fn and P
ranges over Pd. In what follows, we only consider well-typed formulas; we omit
the definition of typing rules as they are standard.
    Let us set some notational conventions for terms and formulas over the sig-
nature τlist (or τint ). We use X, Y, Z, . . . to range over the set of variables of type
List Int and x, y, z, . . . to range over the set of variables of type Int. A term is
called an integer term if it has type Int and is called a list term if it has type
List Int. We use T and t to range over the set of list terms and integer terms,
respectively. We write x             e to represent a possibly empty sequence of
                            e (resp. X)
integer variables (resp. list variables); e  t and Te are defined similarly.

Semantics A model M (or structure) over a signature τ = (Ty, Fn, Pd) is
a triple ((Uι )ι∈Ty , (f M )f ∈Fn , (P M )P ∈Pd ), where each Uι is a non-empty set
called a universe, f M is a function over the universes, P M is a relation over the
universes. If f has type (ι1 , . . . , ιn ) → ιn+1 then f M is a function from Uι1 ×· · ·×
Uιn to Uιn+1 ; the same applies to RM . We write (Z, (f Z )f ∈Fnint , (P Z )P ∈Pdint )
                                                   Symbolic Automatic Relations            5

or simply Z for the standard model of integer arithmetic. The standard model
                                                               def                      def
for integer lists Mlist is a model over τlist such that UInt = Z and UList Int =
              def                             def
Z∗ ; f Mlist = f Z for f ∈ Fnint ; P Mlist = P Z for P ∈ Pdint ; =M        list
                                                                               list
                                                                                    is the
                        ∗
diagonal relation on Z ; and the interpretations for symbols in Fnlist are defined
in a natural way. Formally, interpretations for symbols in Fnlist is defined by
          def                                          def                    def
nil Mlist = ǫ; cons Mlist (i, w) = iw; head Mlist (iw) = i and head Mlist (ǫ) = 0; and
                def                     def
tail Mlist (iw) = w and tail Mlist (ǫ) = ǫ, where i ∈ Z and w ∈ Z∗ .2
     The semantics of terms and formulas are defined in the standard way. Let τ
be a signature and M be a model over τ . An assignment α in M maps variables
of type ι to elements of the universe associated with ι. A triple (t, M, α) of a term
with type ι, a model and an assignment determines an element of the universe
associated with ι, which we write as JtKM,α . Similarly, a triple (ϕ, M, α), where
ϕ is a formula, determines whether the satisfaction relation M, α |= ϕ holds.
We omit the precise definitions of JtKM,α and the satisfaction relation as they
are defined as usual. Since the truth or falsity of M, α |= ϕ depends only on
the values of α for free variables of ϕ, we may write M, [e       x 7→ e  a] |= ϕ if the free
variables of ϕ are among x  e = x1 , . . . , xn and e
                                                    a = α(x1 ), . . . , α(xn ). We say that
a formula ϕ is satisfiable in M if there is an assignment α such that M, α |= ϕ
and ϕ is satisfiable if there is a model M in which ϕ is satisfiable. A formula ϕ
is valid in M if M, α |= ϕ holds for all assignments α; ϕ is valid if it is valid in
all the models. Two formulas ϕ1 and ϕ2 are M-equivalent if, for all assignments
α, M, α |= ϕ1 if and only if M, α |= ϕ2 .


3     Symbolic Automatic Relations
In this section, we introduce the notion of symbolic automatic relations. We first
introduce the notion of a symbolic synchronous automaton in Section 3.1, which
is a special kind of symbolic automaton [8], which serves as the representation of
a symbolic automatic relation. We then define symbolic automatic relations in
Section 3.2. For the sake of simplicity we consider symbolic automatic relations
on integer sequences (or, lists of integers). It would not be difficult to extend
them to deal with tree-structured data, by using (symbolic, synchronous) tree
automata; see also Remark 3.

3.1     Symbolic Synchronous Automata
We first extend the model Z by adding the special padding symbol , which will
be used in the definition of symbolic synchronous automata.
Definition 1 (Partial model for integer arithmetic). A partial model for
integer arithmetic (Z , (f Z )f ∈Fnint , (P Z )P ∈Pdint ) is a model over the signature
          def
τint∪{} = ({Int}, Fnint , Pdint ∪ {pad }), where
2
    Note that head Mlist and tail Mlist are defined as total functions. This matches the
    behaviors of the existing SMT solvers such as Z3 or CVC4.
6          T. Shimoda et al.

    – the universe Z is Z ∪ {}, where  ∈
                                          / Z is called a padding symbol,
                                                                        def
    – for every k-ary function symbol f , f Z (a1 , . . . , ak ) = f Z (a1 , . . . , ak ) if ai ∈
                                                      def
      Z for all 1 ≤ i ≤ k and f Z (a1 , . . . , ak ) =  otherwise, and
                                         def                   def
    – for every P ∈ Pdint , P Z = P Z and pad Z = {}.

By abuse of notation, we may write Z to denote the partial model for integers.

Remark 1. The semantics of the negation ¬ is a little tricky for the partial model.
For example, the interpretation of x < y is different from ¬(x ≥ y): “1 < ” is
false but “¬(1 ≥ )” is true.

Definition 2 (Symbolic synchronous automaton). A k-ary symbolic syn-
chronous nondeterministic finite automaton with n parameters3 x e = x0 , . . . , xn−1
((k, n)-ary ss-NFA for short) is a quadruple M (e
                                                x) = (Q, I, F, ∆) where

    – Q is a finite set of states,
    – I ⊆ Q is the set of initial states,
    – F ⊆ Q is the set of final states,
    – ∆ ⊆ Q×Ψkxe ×Q is a finite set of transitions. Here Ψkxe is a subset of formulas
      over the signature τint∪{} containing only formulas, whose free variables are
      among l0 , . . . , lk−1 , x0 , . . . , xn−1 .

Intuitively, the free variables li are bound to the i-th input at each transition step
and xi are bound to integer values that do not change at each step. Formally, for
e
j = (j0 , . . . , jn−1 ) ∈ Zn and a = (i0 , . . . , ik−1 ) ∈ Zk , an a-transition of M (e     j) is
                     ϕ
a transition q −                           x 7→ e
                     → q ′ such that Z , [e        j, l0 7→ i0 , . . . , lk−1 7→ ik−1 ] |= ϕ. This
                                   a                      a
a-transition is denoted as q −     →M(ej) q ′ (or q −    → q ′ when M (e       j) is clear from the
context).
    A (k, n)-ary ss-NFA M (e      x) = (Q, I, F, ∆) is effective if

           {(i0 , . . . , ik−1 , j0 , . . . , jn−1 ) ∈ Zk × Zn | Z , [e
                                                                        l 7→ ei, x
                                                                                 e 7→ e
                                                                                      j] |= ϕ}
                                     ϕ
                             → q ′ ∈ ∆. We sometimes call a (k, 0)-ary ss-NFA
is a decidable set for all q −
just a k-ary ss-NFA.

    The existence of parameters allows us to use ss-NFAs as representations of
relations that take not only words but also integers as arguments.

Definition 3 (Language of ss-NFA). Let M (e x) = (Q, I, F, ∆) be a (k, n)-ary
ss-NFA and j ∈ Z . A word w ∈ (Z ) is accepted by M (e
           e    n               k ∗
                                                      j) if

    – w = ǫ and I ∩ F 6= ∅, or
                                                                         ai
    – w = a1 · · · am and for all 1 ≤ i ≤ m, there exist transitions qi −→    j) qi+1
                                                                            M(e
      such that q1 ∈ I and qm+1 ∈ F .
3
     The parameters x
                    e are “bound variables” and we identify “α-equivalent” automata.
                                                    Symbolic Automatic Relations               7

                                                       M3 (x)
M1                M2 (x)
                                                      l0 > 0 ∧ l0 = l1 + 1
    ¬(l0 > l1 )    l0 = l1 + 1

                             l0 = 0 ∧ l2 = x                    q0                        q1
        q               q0                     q1                    (l0 = 0 ∧ l2 6= x)
                                                                         ∨ l0 < 0

                             Fig. 2. Examples of ss-NFAs.


A word accepted by M (e  j) is called an accepting run of M (e  j). The language
accepted by M (ej), denoted L(M (e j)), is the set of words accepted by M (e
                                                                           j). We
                x)) for the relation {(w, e
also write L(M (e                          j) | w ∈ L(M (ej))}.
Example 1. Consider the ss-NFAs in Fig. 2. The automaton M1 is formally de-
                                                     def
fined as a 2-ary ss-NFA without parameter M1 = ({q}, {q}, {q}, {(q, ¬(l0 >
l1 ), q)})). The automaton M2 (x) is a 3-ary ss-NFA, with one parameter x, defined
            def                                        def
by M2 (x) = ({q0 , q1 }, {q0 }, {q1 }, ∆), where ∆ = {(q0 , l0 = l1 + 1, q0 ), (q0 , l0 =
0 ∧ l2 = x, q1 ), (q1 , ⊤, q1 )}; the automaton M3 (x) can be formally described in
a similar manner. These automata will be used to define predicates sorted (X)
and nth(i, x, X) later in this section.
    The acceptance language of M2 (x), i.e. L(M2 (x)) ⊆ Z3 × Z, is given as
                                                                          
         a01           a0n          ∃m. 1 ≤ m ≤ n ∧ a0m = 0 ∧ a2m = j           
       a11  · · ·  a1n  , j                                                    .
                                         ∧ (∀i. 1 ≤ i < m =⇒ a0i = a1i + 1)
          a21           a2n
                                                                                               ⊓
                                                                                               ⊔
     We introduce some terminology on ss-NFAs. A (k, n)-ary ss-NFA M (e            x) =
                                                                   ϕ1             ϕ2
(Q, I, F, ∆) is deterministic if |I| = 1 and for all transitions q −→ q1 and q −→ q2 ,
if ϕ1 ∧ ϕ2 is satisfiable in Z then q1 = q2 . A state q of M (e  x) is called complete
                                                                 a
if for all a ∈ Zk and ej ∈ Zn there exists an a-transition q −  →M(ej) q ′ for some q ′ .
A ss-NFA M (e   x) is complete if all states of M (ex) are complete.
     Since ss-NFA are just a special kind of symbolic automata and symbolic
automata can be determinized and completed, it can be shown that ss-NFAs are
closed under Boolean operations using variants of the complement construction
and the product construction of standard automata.4
Proposition 1 (Closure under boolean operations [29]). Given (k, n)-
ary ss-NFAs M1 (e x) and M2 (ex), one can effectively construct ss-NFAs M1c (e    x)
and (M1 × M2 )(e                    x)) = ((Zk )∗ × Zn ) \ L(M1 (e
                x) such that L(M1c (e                             x)) and L((M1 ×
     x)) = L(M1 (e
M2 )(e            x)) ∩ L(M2 (e
                              x)). Moreover, if M1 (e x) and M2 (e x) are effective,
so are M1c (e
            x) and (M1 × M2 )(ex).                                                 ⊓
                                                                                   ⊔
4
    The fact that determinization is possible and that symbolic automata are closed
    under boolean operations were originally shown for symbolic automata without pa-
    rameters [29], but the existence of parameters does not affect the proof.
8        T. Shimoda et al.

3.2    Symbolic Automatic Relations
A symbolic automatic relation (SAR) is basically an acceptance language of a
ss-NFA, but not every acceptance language of a ss-NFA is a SAR. Recall that
a run of a k-ary ss-NFA is a word w ∈ (Zk )∗ and thus it does not necessarily
correspond to tuples of words over Z since the “padding symbol” can appear at
any position of w. In order to exclude such “invalid inputs”, we first define the
convolution operation, which converts a tuple of words to a word of tuples.

Definition 4 (Convolution). Given k words w0 , ..., wk−1 ∈ Z∗ , with wi =
ai1 · · · aili and l = max(l0 , ..., lk−1 ), the convolution of words w0 , ..., wk−1 , de-
noted as c(w0 , ..., wk−1 ), is defined by
                                                         
                                   a′01               a′0l
                          def       ..          .          
                                                              k ∗                def
       c(w0 , ..., wk−1 ) =          .   · · ·  ..  ∈ Z       and c() = ǫ
                                a′(k−1)1           a′(k−1)l

where a′ij = aij if j ≤ li and a′ij =  otherwise. The padding symbol is appended
to the end of some words wi to make sure that all words have the same length.
                                                                       def
   We write Z⊗k for the set of convoluted words, i.e. Z⊗k = {c(w0 , . . . , wk−1 ) |
(w0 , . . . , wk−1 ) ∈ (Z∗ )k }. This set can be recognized by a ss-NFA.
Proposition 2. Let k and n be natural numbers. Then there is a (k, n)-ary ss-
NFA M (e                 x)) = Z⊗k × Zn .
       x) such that L(M (e                                                 ⊓
                                                                           ⊔
Because of this proposition, there is not much difference between ss-NFAs that
only take convoluted words as inputs and ss-NFAs that take any word w ∈ (Zk )∗
as inputs. Given a ss-NFA M (e x), we can always restrict the form of inputs by
taking the product with the automaton that recognizes Z⊗k × Zn .

Definition 5 (Symbolic automatic relation).
    A relation R ⊆ (Z∗ )k × Zn is called a (k, n)-ary symbolic automatic relation
(SAR) if {(c(w0 , . . . , wk−1 ), e
                                  j) | (w0 , . . . , wk−1 , e
                                                            j) ∈ R} = L(M (e      x)) for some
(k, n)-ary ss-NFA M (e    x); in this case, we say that R is recognized by M (e          x).
    Given a (k, n)-ary ss-NFA M (e      x), the (k, n)-ary SAR represented by M (e             x),
denoted as R(M (e  x)), is defined as {(w0 , . . . , wk−1 , e   j) | (c(w0 , . . . , wk−1 ), e
                                                                                             j) ∈
L(M (ex))}. Note that R(M (e     x)) is indeed a SAR because R(M (e         x)) is recognized
by the product of M (e  x) and the automaton that recognizes Z⊗k × Zn .

3.3    Expressing Predicates on Lists
We demonstrate that various predicates over lists can be expressed as logical
formulas obtained by extending the signature τlist with SARs. Moreover, we
show that those predicates belong to a class of formulas called Σ1sar -formulas.
We are interested in Σ1sar -formulas because, as we shall see in Section 6, checking
whether a simple Σ1sar -formula is satisfiable can often be done automatically.
                                                 Symbolic Automatic Relations           9

    Henceforth, we allow SARs to appear in the syntax of formulas. Formally,
we consider formulas over τsar , where τsar is defined as the signature obtained
by adding predicate symbols of the form RM(ex) , which we also call SAR, to the
signature τlist . Here the subscript M (e
                                        x) represents ss-NFAs. In what follows, the
term “formula” means a formula over the signature τsar , unless the signature is
explicitly specified. The predicate symbols RM(ex) are interpreted symbols. We
consider a fixed model M in which every predicate symbol of the form RM(ex) is
interpreted as the symbolic automatic relation represented by M (e   x) and other
symbols are interpreted as in Mlist .

Definition 6. A formula ϕ is a ∆sar   0 -formula if one can effectively construct
a formula RM(ex) (Te, e
                      t) (where RM(ex) is a SAR) that is M-equivalent to ϕ. A
formula ϕ is a Σ1sar -formula if one can effectively construct a formula of the
form ∃e  e 0 that is M-equivalent to ϕ and ϕ0 is a ∆sar
      x∃Xϕ                                               0 -formula. We say that
a formula ϕ is a ∆sar
                    1  -formula if both ϕ and ¬ϕ  are Σ sar
                                                        1 -formulas.

Example 2. Let us consider the predicate sorted (X), which holds just if X is
sorted in ascending order. The predicate sorted can be defined as a ∆sar
                                                                     0 -formula,
               def
by sorted (X) = RM1 (X, tail (X)), where M1 is the ss-NFA used in Example 1.
    The predicate nth(i, x, X), meaning that “the i-th element of X is x”, can be
defined as a ∆sar
              1 -formula. To show this, we use the automata M2 and M3 used in
                                                   def
Example 1. We can define nth by nth(i, x, X) = ∃Y. RM2 (x) (cons(i, Y ), Y, X, x).
In this definition, the list represented by Y works as a “counter”. Suppose that
cons(i, Y ) is interpreted as w0 and assume that the first n transitions were all
    l =l +1
       0   1
q0 −−    −−  −→ q0 . Then we know that the list w0 must be of the form [i, (i −
1), . . . (i − n), . . .], which can be seen as a decrementing counter starting from i.
The transition from q0 to q1 is only possible when the counter is 0 and this allows
us to “access to the i-th element” of the list represented by X. The negation
of nth(i, x, X) can be defined as ∃Y.RM3 (x) (cons(i, Y ), Y, X, x). Using the same
technique, we can define the predicate length(X, i) (“the length of X is i”) as a
∆sar
  1 -formula.                                                                        ⊓
                                                                                     ⊔

  The following proposition and example are useful for constructing new ex-
amples of Σ1sar -formulas.

Proposition 3. The class of ∆sar              sar
                             0 -formulas and ∆1 -formulas are closed under
boolean operations.

Proof. The fact that ∆sar0 -formulas are closed under boolean operations follows
from the fact that ss-NFAs are closed under boolean operations (Prop. 1) and
that the set of convoluted words is a language accepted by a ss-NFA (Prop. 2).
    By the definition of ∆sar                   sar
                              1 -formulas, ∆1 -formulas are clearly closed under
negation. Given formulas ∃e         e
                               x∃Xϕ1 and ∃e     y ∃Ye ϕ2 , where ϕ1 and ϕ2 are ∆sar    0 -
            x∃Xϕ
formulas, (∃e   e 1 )∧(∃e y ∃Ye ϕ2 ) is equivalent to ∃exye∃Xe Ye (ϕ1 ∧ϕ2 ). Since ϕ1 ∧ϕ2
is a ∆sar                               sar
      0 -formula, it follows that ∆1 -formulas are closed under conjunction. ⊓           ⊔
10          T. Shimoda et al.

Example 3. Every arithmetic formula, i.e. a formula over the signature τint , is a
∆sar
 0 -formula. Given an arithmetic formula ϕ whose free variables are x0 , . . . , xk−1 ,
                                                                                               def
we can construct a M-equivalent formula RMϕ ([x0 ], . . . , [xk−1 ]), where [xi ] =
                          def
cons(xi , nil ) and Mϕ = ({q0 , q1 }, {q0 }, {q1 }, {(q0 , ϕ[l0 /x0 , . . . , lk−1 /xk−1 ], q1 )}).
Similar transformation works even if a formula of the form head (X) appears
inside a formula ϕ of type Int.
    Equality relation on two lists is also a ∆sar    0 -formula because it can be de-
scribed by a ss-NFA.                                                                             ⊓
                                                                                                 ⊔

    Thanks to Proposition 3 and Example 3, we can now write various specifi-
cation over lists as (negations of) closed Σ1sar -formulas. For example, consider
the following formula that informally means “if the head element of a list sorted
in ascending order is greater or equal to 0, then all the elements of that list is
greater or equal to 0”:
     def
ϕ = ∀x. ∀i. ∀X. X 6= nil ∧ sorted (X) ∧ head (X) ≥ 0 ∧ nth(i, x, X) =⇒ x ≥ 0

The negation of ϕ is a Σ1sar -formula because sorted (X) and nth(i, x, X) are ∆sar
                                                                               1 -
formulas as we saw in Example 2. Note that the validity of ϕ can be checked by
checking that ¬ϕ is unsatisfiable, which can be done by a satisfiability solver for
Σ1sar -formulas.

3.4        An Application to ICE-Learning-Based CHC Solving with Lists
We now briefly discuss how a satisfiability solver for Σ1sar -formulas may be used
in the teacher part of ICE-learning-based CHC solvers for lists. As mentioned
in Section 1, ICE-learning-based CHC solvers [6, 12] consist of a learner, which
constructs a candidate model, and a teacher, which checks whether the candidate
is indeed a model, i.e., whether the candidate model satisfies every clause. Each
clause is of the form

                                ∀e   e 1 ∧ · · · ∧ An =⇒ B
                                 x. ∀X.A

where A1 , . . . , An and B are either primitive constraints or atoms of the form
P (t1 , . . . , tk ) where P is a predicate variable. Assuming that the learner returns
an assignment θ of ∆sar     1 -formulas to predicate variables, the task of the teacher
is to check that

                         ϕ := ∀e   e
                               x. ∀X.θA1 ∧ · · · ∧ θAn =⇒ θB


is a valid formula for each clause ∀e      e
                                       x. ∀X.θA 1 ∧ · · · ∧ θAn =⇒ θB. The negation
of ϕ can be expressed as a closed Σ1sar -formula ∃e          e M(ey ) (Te, e
                                                       x. ∃X.R             t). By invoking
a satisfiability solver for a Σ1 -formulas we can check whether RM(ey) (Te, e
                                 sar
                                                                                        t) is
unsatisfiable, which is equivalent to checking if ϕ is valid. If RM(ey) (Te, e  t) is satisfi-
able, then ϕ is invalid. In this case, the teacher should generate a counterexample
against ϕ.
                                              Symbolic Automatic Relations        11

Example 4. Let us consider the following set of constrained horn clauses:

 P (X) ⇐ X = nil ∨ X = cons(x, nil)
 P (cons(x, cons(y, X))) ⇐ x ≤ y ∧ P (cons(y, X))
 Q(cons(0, X)) ⇐ ⊤ Q(cons(x, X)) ⇐ Q(X) ⊥ ⇐ P (cons(1, X)) ∧ Q(X)

A model of this set of CHCs is P (X) 7→ sorted (X), Q(X) 7→ hasZero(X), where
sorted is the predicate we have seen in Example 2 and hasZero(X) is a predicate
that holds if 0 appears in the list X. It is easy to check that hasZero is a ∆sar
                                                                              0 -
formula.Hence, if there is a learner part, which is yet to be implemented, that
provides sorted and hasZero as a candidate model, then a satisfiability solver for
Σ1sar -formulas can check that this candidate model is a valid model.           ⊓
                                                                                ⊔

Remark 2. As discussed later in Section 5, the satisfiability problem for SARs is
solved by a reduction to CHC solving without data structures. Thus, combined
with the translation above, we translate a part of the problem of solving CHCs
with data structures to the problem of solving CHCs without data structures.
This makes sense because solving CHCs without data structures is easier in
practice (although the problem is undecidable in general, even without data
structures). One may wonder why we do not directly translate CHCs with data
structures to those without data structures, as in [9, 10]. The detour through
SARs has the following advantages. First, it provides a uniform, streamlined
approach thanks to the closure of SARs under Boolean operations. Second, SARs
serve as certificates of the satisfiability of CHCs.


4   Undecidability Result
This section shows that the satisfiability problem for SARs is undecidable in
general. The satisfiability problem for SARs is the problem of deciding whether
there is an assignment α such that M, α |= ϕ, given a τsar -formula ϕ. We prove
that the satisfiability problem is undecidable even for the class of ∆sar
                                                                      0 -formulas,
by reduction from the halting problem for two-counter machines.

Definition 7 (Minsky’s two-counter machine [22]). Minsky’s two-counter
machine consists of (i) two integer registers r0 and r1 , (ii) a set of instructions,
and (iii) a program counter that holds a non-negative integer. Intuitively, the
value of the program counter corresponds to the line number of the program
currently being executed.
    A program is a pair P = (Line, Code), where Line is a finite set of non-
negative integers such that 0 ∈ Line and Code is a map from a finite set of
non-negative integers to Inst, the set of instructions. The set Inst consists of:
 – inc(i, j) : Increment the value of register ri and set the program counter to
   j ∈ Line.
 – jzdec(i, j, k) : If the value of register ri is positive, decrement it and set
   the program counter to j ∈ Line. Otherwise, set the program counter to
   k ∈ Line.
12          T. Shimoda et al.

 – halt : Stop operating.
Initially, r0 , r1 and the program counter are all set to 0. Given a program P =
(Line, Code) the machine executes Code(i), where i is the value of the program
counter until it executes the instruction halt.
   Given a program P we simulate its execution using a formula of the form
RM (X0 , X1 , tail (X0 ), tail (X1 )). The states and edges of M are used to model
the control structure of the program, and the list variables X0 and X1 are used
to model the “execution log” of registers r0 and r1 , respectively.
Theorem 1 (Undecidability of satisfiability of SARs). Given a k-ary
symbolic automatic relation RM represented by an effective (k, 0)-ary ss-NFA
M and list terms T1 , . . . , Tk , it is undecidable whether RM (T1 , . . . , Tk ) is satis-
fiable.
Proof. We show that for a given program P = (Line, Code), we can effec-
tively construct a SAR RMP that satisfies “P halts iff there are assignments
for X0 and X1 that satisfy RMP (X0 , X1 , tail (X0 ), tail (X1 ))”. Intuitively, Xi
denotes the “execution log of ri ”, i.e., the sequence of values taken by ri in
a terminating execution sequence of P , and RMP takes as arguments both Xi
and tail (Xi ) to check that Xi represents a valid sequence. The ss-NFA MP is
                                          def                                         def
defined as (Q, I, F, ∆), where Q = {qi | i ∈ Line} ∪ {qaccept}, I = {q0 }, and
     def
F = {qaccept}. We define the set of transitions so that MP has a transition
     (c0 ,c1 ,c′ ,c′ )
qi −−−−−−0−− 1
              → qj iff the two-counter machine has a transition from the config-
uration (i, c0 , c1 ) (where i is the current program pointer and ci is the value
of ri ) to (j, c′0 , c′1 ). We also add transition from qi to the final state qaccept if
Code(i) = halt. Formally, ∆ is defined as the smallest set that satisfies the
following conditions:
 – (qi , lr′ = lr + 1 ∧ l1−r = l1−r , qj ) ∈ ∆ if Code(i) = inc(r, j).
 – (qi , lr > 0 ∧ lr′ = lr − 1 ∧ l1−r′
                                           = l1−r , qj ), (qi , lr = 0 ∧ l0′ = l0 ∧ l1′ = l1 , qk ) ∈ ∆
   if Code(i) = jzdec(r, j, k).
 – (qi , pad (l0′ ) ∧ pad (l1′ ), qaccept ) ∈ ∆ if Code(i) = halt.
Here, we have written l0′ and l1′ for l2 and l3 .
    Based on the intuitions above, it should be clear that P halts and the
execution log of ri obtained by running P is wi , if and only if MP accepts
c(w0 , w1 , w0′ , w1′ ), where wi′ is the tail of wi . Thus, P halts if and only if RMP is
satisfiable. Since the halting problem for two-counter machines is undecidable,
so is the satisfiability of RM .                                                        ⊓
                                                                                        ⊔

5      Reduction to CHC Solving
This section describes the reduction from the satisfiability problem of SARs
to CHC solving, whose constraint theory is mere integer arithmetic. Precisely
speaking, the reduction works for a fragment of τsar -formulas, namely the Σ1sar -
formulas. This section starts with a brief overview of the reduction. We then
give the formal definition and prove the correctness of the reduction.
                                                     Symbolic Automatic Relations        13

5.1     Overview

Let us first present intuitions behind our reduction using an example. Con-
sider the predicate nth we defined in Example 2. Let i be a non-negative in-
teger constant, and suppose that we wish to check whether nth(i, x, X) is sat-
isfiable, i.e., whether ∃x∃X.nth(i, x, X) holds. We construct a set of CHCs Π
such that M |= ∃x∃X.nth(i, x, X) iff Π is unsatisfiable. That is, we translate
the ∆sar
       0 -formula RM2 (x) (cons(i, Y ), Y, X, x) preserving its satisfiability. The fol-
lowing CHCs are obtained by translating RM2 (x) (cons(i, Y ), Y, X, x).

   q0 (v0 , v1 , v2 , x) ⇐ v0 = i                                                        (1)
   q0 (v0 , v1 , v2 , x) ⇐ q0 (u0 , u1 , u2 , x) ∧ u0 = u1 + 1 ∧ v0 = u1 ∧ ¬ϕend         (2)
   q1 (v0 , v1 , v2 , x) ⇐ q0 (u0 , u1 , u2 , x) ∧ u0 = 0 ∧ u2 = x ∧ v0 = u1 ∧ ¬ϕend     (3)
   q1 (v0 , v1 , v2 , x) ⇐ q1 (u0 , u1 , u2 , x) ∧ v0 = u1 ∧ ¬ϕend                       (4)
                  ⊥ ⇐ q1 (u0 , u1 , u2 , x) ∧ ϕend                                       (5)

               def V
Here ϕend = j∈{0,1,2} pad (uj ). The predicate q corresponds to the state q and
q(v0 , v1 , v2 , x) intuitively means “there exists an assignment α for X, Y and x
such that given (cons(i, α(Y )), α(Y ), α(X)) as input, M2 (α(x)) visits state q,
with the next input letters being (v0 , v1 , v2 )”. The clause (1) captures the fact
that M2 (α(x)) is initially at state q0 , with the first element v0 of the initial
                                                                        0  1   l =l +1
input is i. The clauses (2), (3), and (4) correspond to transitions q0 −− −− −→ q0 ,
      l =0∧l =x
      1    2                    ⊤
q0 −−   −−−− −→ q1 , and q1 −  → q1 respectively. The constraints in the bodies of
those clauses consist of: (i) the labels of the transitions (e.g., u0 = u1 + 1 in (2)),
(ii) the equation u1 = v0 , which captures the co-relation between the arguments
cons(i, Y ) and Y of RM2 (x), (iii) ¬ϕend indicating that there is still an input to
read. The last clause (5) captures the acceptance condition: a contradiction is
derived if M2 (x) reaches the final state q1 , having read all the inputs. It follows
from the intuitions above that the set of CHCs above is unsatisfiable, if and only
if, RM2 (x) (cons(i, Y ), Y, X, x) is satisfiable.


5.2     Translation

We now formalize the translation briefly discussed in the previous subsection.
To simplify the definition of the translation, we first define the translation
for terms in a special form. Then we will show that every term of the form
RM (T1 , . . . , Tk , t1 , . . . , tn ) can be translated into the special form, preserving
the satisfiability (or the unsatisfiability).

Definition 8. Let L be a set of list terms. Then L is

 – cons-free if for all T ∈ L, T is of the form nil or tail n (X).
 – gap-free if tail n (X) ∈ L implies tail m (X) ∈ L for all 0 ≤ m ≤ n.
14       T. Shimoda et al.

                                                      def                          def
Here tail m (X) is defined by tail 0 (X) = X and tail m+1 (X) = tail (tail m (X)).
   We say that a formula of the form RM(ex) (T1 , . . . , Tk , t1 , . . . , tn ) is normal if
{T1 , . . . , Tk } is cons-free and gap-free, and every ti is an integer variable.
                                                                             def
                                                       x) = (Q, I, F, ∆), Te =
Definition 9. Let RM(ex) be a (k, n)-ary SAR, where M (e
                                                def
T0 , . . . , Tk−1 be list terms and ye = y0 , . . . , yn−1 be integer variables. Suppose
that RM(ex) (Te, ye) is normal. Then the set of CHCs translated from RM(ex) (Te, ye),
written LRM(ex) (Te, ye)M, consists of the following clauses:
                                     ϕ
 1. The clause (written Lp −
                           → qM):

                                                                  e) ∧ ϕ[u0 /l0 , . . . , uk−1 /lk−1 ]
                                            p(u0 , . . . , uk−1 , x
                                  e) ⇐
            q(v0 , . . . , vk−1 , x
                                                            ∧ϕshift ∧ ϕpad ∧ ¬ϕend
                    ϕ
    for each p −
               → q ∈ ∆.
 2. The clause

                                                e) ⇐ ϕnil ∧ ϕtail(nil) ∧ x
                          q(v0 , . . . , vk−1 , x                        e = ye

    for each q ∈ I.
 3. The clause:

                                                              e) ∧ ϕend
                                    ⊥ ⇐ q(u0 , . . . , uk−1 , x

      for each q ∈ F .
Here the definitions and the informal meanings of ϕend , ϕshift , ϕpad , ϕnil and
ϕtail(nil) are given as follows:
          def
                     ^
     ϕend =                     pad (ui )             “there is no letter to read”
                i∈{0,...,k−1}
          def
                ^
     ϕshift =       {vi = uj ∨ (pad (vi ) ∧ pad (uj )) | Ti = tail m (X), Tj = tail m+1 (X)}
          “the l-th element of the list represented by tail m+1 (X) is
          the (l + 1)-th element of the list represented by tail m (X)”
          def
                  ^
     ϕpad =              pad (ui ) ⇒ pad (vi )
                i∈{0,...,k−1}

          “if a padding symbol  is read, then the next input is also ”
           def
               ^
      ϕnil =     {pad (vi ) | Ti = nil }
          “there is no letter to read from an empty list”
           def
               ^
ϕtail(nil) =     {pad (vi ) ⇒ pad (vj ) | Ti = tail m (X), Tj = tail m+1 (X)}
          “if there is no letter to read from the input represented by tail m (X)
          then there is nothing to read from the input represented by tail m+1 (X)”
                                                         Symbolic Automatic Relations                15

 M2′ (x, y)



                              q11
                                                                l0 = l1 + 1
     l0 = 0 ∧ l2 = x
                      l0 = l1 + 1                 y = l1 + 1              l0 = 0 ∧ l2 = x
              q00                      q01                           q0                        q1



                                                            y = 0 ∧ l2 = x

              Fig. 3. The ss-NFA used to explain the idea behind Lemma 1.


    We next show that we can assume that RM(ex) (Te, e     t) is normal without loss
of generality. First, observe that ensuring that T is gap-free is easy. If Te is
                                                      e
not gap-free then we just have to add additional inputs, corresponding to the
list represented by tail n (X), to the automaton M (e   x) and ignore those inputs.
Ensuring that et is a sequence of integer variables is also easy. If t is not an integer
variable, then we can embed t to the transitions of the automaton and add the
free variables of t to the parameter or as inputs of the automaton. Therefore,
the only nontrivial condition is the cons-freeness:
                                                             def
Lemma 1. Let RM(ex) be a (k, n)-ary SAR, Te = T1 , . . . , Tk be list terms and
    def
e
t = t1 , . . . , tn be integer terms. Then we can effectively construct a (k, n +
                                                     def                                             def
m)-ary ss-NFA M ′ (e           e′ ), list terms f
                            x, x                 T ′ = T1′ , . . . , Tk′ and integer terms te′ =
t′1 , . . . , t′n+m such that (1) RM(ex) (Te, et) is satisfiable in M iff RM ′ (ex,ex′ ) (f
                                                                                          T ′ , te′ ) is
                                      ′       ′
satisfiable in M and (2) {T1 , . . . , Tk } is cons-free.                                             ⊓
                                                                                                      ⊔

Instead of giving a proof, we look at an example. (The proof is in Appendix A.1.)
                                def
Consider the formula ϕ = RM2 (x) (cons(1, cons(t, Y )), cons(0, Y ), X, x), where
M2 (x) is the automaton given in Example 1. We explain how to remove cons(t, ·)
from the first argument; by repeating this argument we can remove all the “cons”.
       def
Let ϕ′ = RM2′ (x,y) (cons(1, Y ), cons(0, tail (Y )), X, x, t), where M2′ (x, y) is the ss-
NFA in Fig. 3. Then it is easy to see that ϕ is satisfiable in M iff ϕ′ is satisfiable
in M. If M, α |= ϕ with α(Y ) = w and JtKM,α = i then M, α[Y 7→ iw] |= ϕ′ ;
the opposite direction can be checked in a similar manner. The idea is to embed
the information that “the second element is t” into the ss-NFA by replacing l0
with y in the edges that corresponds to the “second step” and passing t as the
actual argument. Note that we had to “unroll the ss-NFA M2 (x)” to ensure that
the transition that contains y is used at most once.

Remark 3. We have so far considered symbolic automatic relations on lists. We
expect that the reduction above can be extended to deal with symbolic automatic
16        T. Shimoda et al.

relations on tree structures, as follows. Let us consider a (symbolic, synchronous)
bottom-up tree automaton, with transitions of the form

                        hl1 , . . . , lk , x1 , . . . , xn i(q1 , . . . , qm ), ϕ → q,

which means “when the current node is labeled with hl1 , . . . , lk , x1 , . . . , xn i and
the i-th child has been visited with state qi , then the current node is visited with
state q if l1 , . . . , lk , x1 , . . . , xn satisfy ϕ”. To reduce the satisfiability problem to
CHCs on integers, it suffices to prepare a predicate q for each state q, so that
q(l1 , . . . , lk , x1 , . . . , xn ) holds just if there exists an input that allows the automa-
ton to visit state q after reading hl1 , . . . , lk , x1 , . . . , xn i. As for the definition of
“normal form”, it suffices to replace tail (T ) with childi (T ) (which denotes the
i-th child of tree T ), and define the cons-freeness and gap-freeness conditions
accordingly. The formalization of the extension is left for future work.

5.3     Correctness
The correctness of the translation is proved by associating a derivation of ⊥ to
an accepting run and vice versa.
   We first define the notion of derivations for CHCs, as a special case of the
SLD resolution derivation [21]. Since the system of CHCs obtained by translating
a ∆sar
    0 -formula is linear, which means that each clause contains at most one
predicate in the body, we specialize the notion of derivations for linear CHCs.
Definition 10 (Derivation). A derivation state (or simply a state) is a pair
hA | ψi, where A is either ⊤ or P (e      t), i.e. an uninterpreted predicate symbol P
applied to terms e   t, and ψ is a constraint. Let C be a linear constrained horn
clause of the form P (e  t1 ) ⇐ A ∧ ψ ′ , where A is either ⊤ or formula of the form
                                                                (C,θ)
Q(et2 ) and ψ ′ is a constraint. Then we write hP (e    t) | ψi       hθA | θ(ψ ∧ ψ ′ )i, if
P (e
   t) and P (et1 ) are unifiable by a unifier θ.
    Let Π be a system of linear CHCs, i.e. a finite set of linear constrained horn
clauses. A derivation from state S0 with respect to Π is a finite sequence of the
           (C1 ,θ1 )   (C2 ,θ2 )     (Cn ,θn )
form S0         S1       ···        Sn such that (i) Ci ∈ Π for all i and (ii) Sn
is of the form h⊤ | ψi such that ψ is a constraint that is satisfiable in Z .
      Now we are ready to prove the correctness of the translation.
Theorem 2. Let RM(ex) be a (k, n)-ary SAR, and suppose that RM(ex) (Te, ye) is
normal. Then RM(ex) (Te, ye) is satisfiable in M iff LRM(ex) (Te, ye)M is unsatisfiable
modulo Z .
Proof (Sketch). We only sketch the proof; a detailed version is in Appendix A.2.
Suppose that M (e x) = (Q, I, F, ∆), Te = T0 , . . . , Tk−1 , ye = y0 , . . . , yn−1 and let
   def
Π = LRM(ex) (Te, ye)M. By the completeness of the SLD resolution, it suffices to
show that RM(ex) (Te, ye) is satisfiable if and only if there is a derivation starting
from hq(e  e) | ϕend i with respect to Π for some q ∈ F . We separately sketch
        u, x
the proof for each direction.
                                                              Symbolic Automatic Relations                      17

   (Only if) Since RM(ex) (Te, ye) is satisfiable, there exists an assignment α such
                                      def                                           def
that M, α |= RM(ex) (Te, ye). Let wi = JTi KM,α for each i ∈ {0, . . . , k − 1}, ji =
                                           def
α(yi ) for i ∈ {0, . . . , n − 1} and e  j = j0 , . . . , jn−1 . Because M, α |= RM(ex) (Te, ye),
                                                  a0         a2         am−1
we have an accepting run of M (e          j), q0 −→      q1 −→    · · · −−−→ qm , where the run
a0 a2 · · · am−1 is c(w0 , . . . , wk−1 ). From this run, we can construct a derivation
                   ξm−1                                       ξm−2       ξ0                         (C,θ)
hqm (e  e) | ϕend i
     u, x                 hqm−1 (am−1 , e
                                        j) | ψm−1 i                ···        hq0 (a0 , e
                                                                                        j) | ψ0 i           h⊤ | ψi

where ξi = (Ci , θi ). Here, qi (ai , e
                                      j) means the predicate symbol qi applied to
constants that represent the elements of ai and ej. In particular, the derivation can
                                                                              ai
be constructed by taking the clause that corresponds to the transition qi −→     qi+1
for the clause Ci .
    (If) By assumption, there is a derivation
                               (Cm ,θm )         (C1 ,θ1 )                        (C0 ,θ0 )
           hqm (e  e) | ψm i
                u, x                       ···               hq0 (e  e) | ψ0 i
                                                                  u, x                        h⊤ | ψi

where ψm = ϕend . We construct an accepting run of M (e      x) using an assignment
in Z and the unifiers. Take an assignment α such that Z , α |= ψ, which exists
                                         def
because ψ is satisfiable in Z . Let θ≤i = θ0 ◦ θ1 ◦ · · · ◦ θi . We define aij ∈ Z ,
                                                                   def                                          def
where 0 ≤ i ≤ m and 0 ≤ j ≤ k − 1, by aij = Jθ≤i (uj )KZ ,α and set ai =
                                          def
(ai0 , . . . , aik−1 ). We also define ji = Jθ0 (xi )KM,α and write e
                                                                    j for j0 , . . . , jn . Then
we can show that a0 a1 · · · am−1 is an accepting run of M (e       j). Moreover, we can
show that a0 a1 · · · am−1 can be given as a convolution of words c(w0 , . . . , wk−1 )
by using the constraint ¬ϕend that appears in clauses corresponding to transition
relations. Finally, we can show that there is an assignment β in M such that
JTi KM,β = wi for every i ∈ {0, . . . , k − 1} by using the cons-freeness and gap-
freeness, and the constraints ϕshift , ϕnil and ϕtail(nil) .                                   ⊓
                                                                                               ⊔

     The correspondence between resolution proofs and accepting runs should al-
low us to generate a witness of the satisfiability of RM(ex) (Te, ye). A witness of the
satisfiability is important because it serves as a counterexample that the teacher
part of an ICE-learning-based CHC solver provides (cf. 3.4). Since some CHC
solvers like Eldarica [17] outputs a resolution proof as a certificate of the unsat-
isfiability, it should be able to generate counterexamples by using these solvers
as a backend of the teacher part. The formalization and the implementation of
this counterexample generation process are left for future work.


6    Experiments

We have implemented a satisfiability checker for ∆sar    1 -formulas. An input of
the tool consists of (i) definitions of ∆sar
                                         1   -predicates (expressed  using ss-NFA),
and (ii) a ∆sar
             1  -formula  consisting  of the   defined predicates, list constructors
and destructors, and integer arithmetic. For (i), if a predicate is defined using
18      T. Shimoda et al.

existential quantifiers, both the definitions of a predicate and its negation should
be provided (recall nth in Example 1); we do not need to provide the predicates
in normal forms because our tool automatically translates the inputs into normal
forms. The current version of our tool only outputs SAT, UNSAT, or TIMEOUT
and does not provide any witness of the satisfiability. We used Spacer [20], HoIce
[6], and Eldarica [17] as the backend CHC solver (to solve the CHC problems
obtained by the reduction in Section 5). The experiments were conducted on
a machine with AMD Ryzen 9 5900X 3.7 GHz and 32 GB of memory, with a
timeout of 60 seconds. The implementation and all the benchmark programs
are available in the artifact [25]. The detailed experimental results are shown in
Appendix B.
     We have tested our tool for three benchmarks. All the ss-NFAs used in
the benchmarks are effective; in fact, all the formulas appearing as the labels
of transitions are formulas in quantifier-free linear integer arithmetic. The first
benchmark “IsaPlanner” is obtained from the benchmark [18] of IsaPlanner [11],
which is a proof planner for the interactive theorem prover Isabelle [24]. We man-
ually converted the recursively defined functions used in the original benchmark
into SARs. The second benchmark “SAR SMT” consists of valid/invalid formu-
las that represent properties of lists.
     Each instance of the third benchmark “CHC” consists of (i) CHCs on data
structures and (ii) a candidate model (given as a map from predicate variables
to ∆sar
      1 -formulas); the goal is to check that the candidate is a valid model for the
CHCs (which is the task of the “teacher” part of ICE-based CHC solving [6]).
This benchmark includes CHCs obtained by a reduction from the refinement
type-checking problem for functional programs [15, 26, 27, 30]. For many of the
instances in the benchmark set, symbolic automatic relations are required to
express models. For example, the set of CHCs given in Example 4 is included in
the benchmark.
     To compare our tool with the state-of-the-art SMT solvers, Z3 (4.8.11) [23]
and CVC4 (1.8) [1], which support user-defined data types and recursive func-
tion definition, we manually translated the instances to SMT problems that use
recursive functions on lists. We tested two different translations. One is to trans-
late the ∆sar
            1 -predicates (such as nth) directly into recursive functions by using
define-fun-rec, and the other is to translate the predicates into assertions, like
(assert (forall ...)), that describe the definition of functions.
     Table 1 summarizes the experimental results. In the first column, “Ours-
XXX” means our tool with the underlying CHC solver XXX, “(rec)” means
the translation to recursive functions, and “(assert)” means the translation to
assertions. The row “Benchmark” shows the names of the benchmarks. The
column “All” show the summary of the all benchmarks. The row “#Instances”
shows the number of instances in the benchmark, and the first two numbers in
the parentheses show the numbers of valid and invalid instances respectively,
and the last number in the parentheses shows the number of solved instances
that were not solved by the other tools. The row “#Solved” shows the number
of solved instances, and the numbers in the parentheses are the same as ones in
                                              Symbolic Automatic Relations         19

                  Table 1. Summary of the experimental results

   Benchmark          IsaPlanner      SAR SMT             CHC                All
   #Instances            15 (15/0)     60 (47/13)      12 (12/0)     87 (74/13)
   Ours-Spacer
    #Solved              8 (8/0/0)   43 (30/13/0)      8 (8/0/0)   59 (46/13/0)
    Average time             0.995          0.739          1.981          0.942
   Ours-HoIce
    #Solved            14 (14/0/1)   55 (42/13/0)   11 (11/0/0)    80 (67/13/1)
    Average time             7.296          4.498         6.584           5.275
   Ours-Eldarica
    #Solved            14 (14/0/0)   59 (46/13/2)   12 (12/0/0)    85 (72/13/2)
    Average time             4.539          2.441        11.078           4.006
   Z3 (rec)
    #Solved              5 (5/0/0)   32 (19/13/0)      1 (1/0/0)   38 (25/13/0)
    Average time             0.023          0.022          0.017          0.022
   CVC4 (rec)
    #Solved              5 (5/0/0)   32 (19/13/0)      3 (3/0/0)   40 (27/13/0)
    Average time             0.014          0.015          0.050          0.017
   Z3 (assert)
    #Solved              7 (7/0/0)    20 (20/0/0)      3 (3/0/0)    30 (30/0/0)
    Average time             0.018          0.018          0.022          0.019
   CVC4 (assert)
    #Solved              6 (6/0/0)    19 (19/0/0)      3 (3/0/0)    28 (28/0/0)
    Average time             0.057          0.008          0.015          0.019



“#Instances”. The row “Average time” shows the average running time of the
solved instances in seconds.
    Ours-Eldarica successfully verified all the instances except two. Since one
of them needs non-linear properties on integers such as x ≥ y × z, the reduced
CHC problem cannot be proved by the underlying CHC solvers used in the
experiments. The other one is proved by Ours-HoIce. As shown in the rows
“Z3” and “CVC4”, many of the problems were not verified by the SMT solvers
regardless of the way of translation. Especially, they did not verify most of the
instances that require inductions over lists. Moreover, all the invalid instances
translated by using assertions were not verified by Z3 nor CVC4, while those
translated by using recursive functions were verified by Z3 and CVC4.
    We explain some benchmark instances below. The instance “prop 77” in
IsaPlanner benchmark is the correctness property of insert function of insertion
sort. That is, if a list X is sorted and a list Y is X with some integer inserted by
insert , then Y is sorted. As stated above, we manually converted the recursively
defined functions into SARs. As an example, we now describe how to translate
insert function into a SAR. The original insert function is defined as follows
(written in OCaml-like language):
let rec insert(x, y) = match y with
  | [] -> x :: []
20       T. Shimoda et al.

Mins (x)
                       l1 = l2                                   l0 = l2

                                 x = l2 ∧ (x ≤ l1 ∨ pad (l1 ))
                         q0                                        q1


                       Fig. 4. The ss-NFA for function insert .


     | z::xs -> if x <= z then x::y else z::insert(x, xs)

We first translate it into the following recursively defined predicate.

let rec insert’(x, ys, rs) = match ys, rs with
  | [],     r::rs’             -> x = r && ys = rs’
  | y::ys’, r::rs’ when x <= y -> x = r && ys = rs’
  | y::ys’, r::rs’ when x > y -> y = r && insert’(x, ys’, rs’)
  | _                          -> false

The predicate insert’(x,ys,rs) means that insert(x,ys) returns rs. We can
now translate it into a SAR. To express this predicate, we need two states—one
for insert’ and one for equality of lists (ys = rs’). In addition, to check the
equality of ys and the tail of rs, we need a one-shifted list of ys that has a dummy
integer 0 in its head, i.e., cons(0, ys). Hence, predicate insert(x, X, Y ) (which
means Y is X with x inserted) can be expressed as RMins (x) (cons(0, X), X, Y )
where Mins (x) is shown in Fig. 4. The transition from q0 to q0 corresponds to
the third case of the pattern matching of insert’, and the transition from q0
to q1 corresponds to the first two cases.
    The instance “prefix trans” in SAR SMT benchmark is the transitivity prop-
erty of predicate prefix . The predicate prefix takes two lists, and it holds if the
first argument is the prefix of the second argument. The transitivity of prefix
is that, if prefix (X, Y ) and prefix (Y, Z), then prefix (X, Z) holds. The instance
“sorted” in CHC benchmark is the problem explained in Example 4. All the
instances explained here were solved by our tool, while neither Z3 nor CVC4
verified them.


7     Related Work

Although both automatic relations/structures [4,14,19] and symbolic automata [8,
28, 29] and their applications to verification have been well studied, the combi-
nation of them is new to our knowledge, at least in the context of program
verification. D’Antoni and Veanes [7] studied the notion of extended symbolic
finite automata (ESFA) which take a single word as an input, but read mul-
tiple consecutive symbols simultaneously. ESFA is related to our symbolic au-
tomatic relations in that the language accepted by ESFA can be expressed as
{w | R(w, tail (w), . . . , tail k−1 (w))} using a symbolic automatic relation R.
                                             Symbolic Automatic Relations       21

    Haudebourg [16, Chapter 6] recently applied tree automatic relations to CHC
solving. Since he uses ordinary (i.e. non-symbolic) automata, his method can only
deal with lists and trees consisting of elements from a finite set.
    As mentioned in Section 1, the current SMT solvers do not work well for
recursive data structures. In the case of lists, one may use decidable theories on
arrays or inductive data types [2, 5]. The decidable fragments of those theories
are limited. Our procedure is necessarily incomplete (due to the undecidability of
the satisfiability problem), but can be used as complementary to the procedures
implemented in the current SMT solvers, as confirmed by the experiments. We
have focused on lists in this paper, but our approach can be extended to deal
with more general recursive data structures, by replacing automatic relations
with tree automatic ones.
    There are other approaches to solving CHCs on recursive data structures.
Unno et al. [27] proposed a method for automatically applying induction on data
structures, and De Angelis et al. [9,10] proposed a method based on fold/unfold
transformation. An advantage of our approach is that we can generate a symbolic
automatic relation as a certificate of the satisfiability of CHCs. To make a proper
comparison, however, we have to devise and implement a missing component –
a procedure for automatically generating a candidate model (recall that we have
given only a procedure for checking the validity of a candidate model).


8   Conclusion
We have introduced the notion of symbolic automatic relations (SARs) and con-
sidered the satisfiability problem for SARs, with applications to SMT and CHC
solving on recursive data structures in mind. We have shown that the satisfiabil-
ity problem is undecidable in general, but developed a sound (but incomplete)
procedure to solve the satisfiability problem by a reduction to CHC solving on
integers. We have confirmed the effectiveness of the proposed approach through
experiments. We plan to implement an ICE-based CHC solver based on the
proposed approach. To that end, we need to implement a learner’s algorithm
to automatically discover appropriate SARs, following the approach of Haude-
bourg [16].
22      T. Shimoda et al.

References
 1. Barrett, C.W., Conway, C.L., Deters, M., Hadarean, L., Jovanovic, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: Gopalakrishnan, G., Qadeer, S. (eds.) Com-
    puter Aided Verification - 23rd International Conference, CAV 2011, Snowbird, UT,
    USA, July 14-20, 2011. Proceedings. Lecture Notes in Computer Science, vol. 6806,
    pp. 171–177. Springer (2011). https://doi.org/10.1007/978-3-642-22110-1 14
 2. Barrett, C.W., Shikanian, I., Tinelli, C.: An abstract decision procedure for a
    theory of inductive data types. J. Satisf. Boolean Model. Comput. 3(1-2), 21–46
    (2007). https://doi.org/10.3233/sat190028
 3. Bjørner, N., Gurfinkel, A., McMillan, K.L., Rybalchenko, A.: Horn clause solvers
    for program verification. In: Fields of Logic and Computation II - Essays Dedicated
    to Yuri Gurevich on the Occasion of His 75th Birthday. LNCS, vol. 9300, pp. 24–51.
    Springer (2015). https://doi.org/10.1007/978-3-319-23534-9 2
 4. Blumensath, A., Grädel, E.: Automatic structures. In: 15th Annual IEEE
    Symposium on Logic in Computer Science, Santa Barbara, California,
    USA, June 26-29, 2000. pp. 51–62. IEEE Computer Society (2000).
    https://doi.org/10.1109/LICS.2000.855755
 5. Bradley, A.R., Manna, Z., Sipma, H.B.: What’s decidable about arrays? In: Emer-
    son, E.A., Namjoshi, K.S. (eds.) Verification, Model Checking, and Abstract In-
    terpretation, 7th International Conference, VMCAI 2006, Charleston, SC, USA,
    January 8-10, 2006, Proceedings. Lecture Notes in Computer Science, vol. 3855,
    pp. 427–442. Springer (2006). https://doi.org/10.1007/11609773 28
 6. Champion, A., Chiba, T., Kobayashi, N., Sato, R.: ICE-based refinement type
    discovery for higher-order functional programs. J. Autom. Reason. 64(7), 1393–
    1418 (2020). https://doi.org/10.1007/s10817-020-09571-y
 7. D’Antoni, L., Veanes, M.: Extended symbolic finite automata and
    transducers.    Formal      Methods      Syst.   Des.   47(1),     93–119   (2015).
    https://doi.org/10.1007/s10703-015-0233-4
 8. D’Antoni, L., Veanes, M.: The power of symbolic automata and transducers. In:
    Majumdar, R., Kuncak, V. (eds.) Computer Aided Verification - 29th International
    Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 10426, pp. 47–67. Springer (2017).
    https://doi.org/10.1007/978-3-319-63387-9 3
 9. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Solving horn clauses
    on inductive data types without induction. TPLP 18(3-4), 452–469 (2018).
    https://doi.org/10.1017/S1471068418000157
10. De Angelis, E., Fioravanti, F., Pettorossi, A., Proietti, M.: Removing algebraic
    data types from constrained horn clauses using difference predicates. In: Peltier,
    N., Sofronie-Stokkermans, V. (eds.) Automated Reasoning - 10th International
    Joint Conference, IJCAR 2020, Paris, France, July 1-4, 2020, Proceedings, Part
    I. Lecture Notes in Computer Science, vol. 12166, pp. 83–102. Springer (2020).
    https://doi.org/10.1007/978-3-030-51074-9 6
11. Dixon, L., Fleuriot, J.D.: IsaPlanner: A prototype proof planner in Isabelle. In:
    Baader, F. (ed.) Automated Deduction - CADE-19, 19th International Confer-
    ence on Automated Deduction Miami Beach, FL, USA, July 28 - August 2, 2003,
    Proceedings. Lecture Notes in Computer Science, vol. 2741, pp. 279–283. Springer
    (2003). https://doi.org/10.1007/978-3-540-45085-6 22
12. Ezudheen, P., Neider, D., D’Souza, D., Garg, P., Madhusudan, P.: Horn-ICE
    learning for synthesizing invariants and contracts. Proc. ACM Program. Lang.
    2(OOPSLA), 131:1–131:25 (2018). https://doi.org/10.1145/3276501
                                               Symbolic Automatic Relations        23

13. Fedyukovich, G., Ernst, G.: Bridging arrays and adts in recursive proofs. In:
    Groote, J.F., Larsen, K.G. (eds.) Tools and Algorithms for the Construction and
    Analysis of Systems - 27th International Conference, TACAS 2021, Held as Part
    of the European Joint Conferences on Theory and Practice of Software, ETAPS
    2021, Luxembourg City, Luxembourg, March 27 - April 1, 2021, Proceedings, Part
    II. Lecture Notes in Computer Science, vol. 12652, pp. 24–42. Springer (2021).
    https://doi.org/10.1007/978-3-030-72013-1 2
14. Grädel, E.: Automatic structures: Twenty years later. In: Hermanns, H., Zhang,
    L., Kobayashi, N., Miller, D. (eds.) LICS ’20: 35th Annual ACM/IEEE Symposium
    on Logic in Computer Science, Saarbrücken, Germany, July 8-11, 2020. pp. 21–34.
    ACM (2020). https://doi.org/10.1145/3373718.3394734
15. Hashimoto, K., Unno, H.: Refinement type inference via horn constraint opti-
    mization. In: Blazy, S., Jensen, T.P. (eds.) Static Analysis - 22nd International
    Symposium, SAS 2015, Saint-Malo, France, September 9-11, 2015, Proceedings.
    Lecture Notes in Computer Science, vol. 9291, pp. 199–216. Springer (2015).
    https://doi.org/10.1007/978-3-662-48288-9 12
16. Haudebourg, T.: Automatic verification of higher-order functional programs using
    regular tree languages. Ph.D. thesis, Universitéx Rennes (2020)
17. Hojjat, H., Rümmer, P.: The ELDARICA horn solver. In: Bjørner, N., Gurfinkel,
    A. (eds.) 2018 Formal Methods in Computer Aided Design, FMCAD 2018,
    Austin, TX, USA, October 30 - November 2, 2018. pp. 1–7. IEEE (2018).
    https://doi.org/10.23919/FMCAD.2018.8603013
18. Johansson, M., Dixon, L., Bundy, A.: Case-analysis for rippling and inductive
    proof. In: Kaufmann, M., Paulson, L.C. (eds.) Interactive Theorem Proving, First
    International Conference, ITP 2010, Edinburgh, UK, July 11-14, 2010. Proceed-
    ings. Lecture Notes in Computer Science, vol. 6172, pp. 291–306. Springer (2010)
19. Khoussainov, B., Nerode, A.: Automatic presentations of structures. In: Leivant,
    D. (ed.) Logical and Computational Complexity. Selected Papers. Logic and Com-
    putational Complexity, International Workshop LCC ’94, Indianapolis, Indiana,
    USA, 13-16 October 1994. Lecture Notes in Computer Science, vol. 960, pp. 367–
    392. Springer (1994). https://doi.org/10.1007/3-540-60178-3 93
20. Komuravelli, A., Gurfinkel, A., Chaki, S.: SMT-based model checking for
    recursive programs. Formal Methods Syst. Des. 48(3), 175–205 (2016).
    https://doi.org/10.1007/s10703-016-0249-4
21. Kowalski, R.A.: Predicate logic as programming language. In: Rosenfeld, J.L. (ed.)
    Information Processing, Proceedings of the 6th IFIP Congress 1974, Stockholm,
    Sweden, August 5-10, 1974. pp. 569–574. North-Holland (1974)
22. Minsky, M.L.: Recursive unsolvability of post’s problem of “tag” and other topics
    in theory of turing machines. Annals of Mathematics pp. 437–455 (1961)
23. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: Ramakrish-
    nan, C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and
    Analysis of Systems, 14th International Conference, TACAS 2008, Held as
    Part of the Joint European Conferences on Theory and Practice of Soft-
    ware, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings.
    Lecture Notes in Computer Science, vol. 4963, pp. 337–340. Springer (2008).
    https://doi.org/10.1007/978-3-540-78800-3 24
24. Paulson, L.C.: Isabelle - A Generic Theorem Prover (with a contribution by
    T. Nipkow), Lecture Notes in Computer Science, vol. 828. Springer (1994).
    https://doi.org/10.1007/BFb0030541
24      T. Shimoda et al.

25. Shimoda, T., Kobayashi, N., Sakayori, K., Sato, R.: Symbolic automatic re-
    lations and their applications to SMT and CHC solving [data set] (2021).
    https://doi.org/10.5281/zenodo.5140576
26. Unno, H., Kobayashi, N.: Dependent type inference with interpolants. In:
    Porto, A., López-Fraguas, F.J. (eds.) Proceedings of the 11th International
    ACM SIGPLAN Conference on Principles and Practice of Declarative Pro-
    gramming, September 7-9, 2009, Coimbra, Portugal. pp. 277–288. ACM (2009).
    https://doi.org/10.1145/1599410.1599445
27. Unno, H., Torii, S., Sakamoto, H.: Automating induction for solving horn clauses.
    In: Majumdar, R., Kuncak, V. (eds.) Computer Aided Verification - 29th Inter-
    national Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceed-
    ings, Part II. Lecture Notes in Computer Science, vol. 10427, pp. 571–591. Springer
    (2017). https://doi.org/10.1007/978-3-319-63390-9 30
28. Veanes, M., Bjørner, N., de Moura, L.M.: Symbolic automata constraint solving. In:
    Fermüller, C.G., Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence,
    and Reasoning - 17th International Conference, LPAR-17, Yogyakarta, Indonesia,
    October 10-15, 2010. Proceedings. Lecture Notes in Computer Science, vol. 6397,
    pp. 640–654. Springer (2010). https://doi.org/10.1007/978-3-642-16242-8 45
29. Veanes, M., de Halleux, P., Tillmann, N.: Rex: Symbolic regular expression ex-
    plorer. In: Third International Conference on Software Testing, Verification and
    Validation, ICST 2010, Paris, France, April 7-9, 2010. pp. 498–507. IEEE Com-
    puter Society (2010). https://doi.org/10.1109/ICST.2010.15
30. Zhu, H., Jagannathan, S.: Compositional and lightweight dependent type in-
    ference for ML. In: Giacobazzi, R., Berdine, J., Mastroeni, I. (eds.) Verifi-
    cation, Model Checking, and Abstract Interpretation, 14th International Con-
    ference, VMCAI 2013, Rome, Italy, January 20-22, 2013. Proceedings. Lec-
    ture Notes in Computer Science, vol. 7737, pp. 295–314. Springer (2013).
    https://doi.org/10.1007/978-3-642-35873-9 19
                                                       Symbolic Automatic Relations               25

A     Supplementary Material for Section 5
A.1     Proof of Lemma 1
Here we give the proof of Lemma 1, which has been omitted from the body of
the paper. For the idea behind the proof, please refer to Section 5.2.
                                                                                                 def
Lemma 2 (Identical to Lemma 1). Let RM(ex) be a (k, n)-ary SAR, Te =
                                    def
T1 , . . . , Tk be list terms and e
                                  t = t1 , . . . , tn be integer terms. Then we can effec-
                                                                                 def
tively construct a (k, n + m)-ary ss-NFA M ′ (e             e′ ), list terms f
                                                         x, x                T ′ = T ′, . . . , T ′
                                                                                          1        k
                                def
and integer terms te′ = t′1 , . . . , t′m+n such that (1) RM(ex) (Te, e          t) is satisfiable in
M iff RM ′ (ex,ex′ ) (f
                      T ′ , te′ ) is satisfiable in M and (2) {T1′ , . . . , T ′ } is cons-free.
                                                                            k

Proof. First, note that if a term T is of the form tail (cons(t, T ′ )) then the se-
mantics of T is equal to that of T ′ . Thus, we may assume that each Ti is of the
form cons(ti0 , cons(ti1 , cons(· · · cons(tili , Ti′′ ) · · · ))), where Ti′′ is either nil or
                                              def
tail m (X). We fix a natural number l = max{l0 , . . . , lk−1 }. To simplify the nota-
tion, we write cons(e t, T ) for the term cons(t0 , cons(t1 , cons(· · · cons(tm , T ) · · · )))
provided that e t = t0 , t1 , . . . , t m .
     Before we construct the automaton M ′ (e             e′ ) we first construct a ss-NFA
                                                       x, x
M (eexp
        x) that satisfies (i) given a word w such that |w| ≥ l, w ∈ L(M exp (e              j))
              e
iff w ∈ L(M (j)) and (ii) “states that are reached in the first l steps are always
distinct”. Suppose that M (e         x) = (Q, I, F, ∆). Such an automaton M exp (e    x) can
be defined as (Q , I , F , ∆exp ) where
                  exp exp           exp

           def
 – Qexp = Q × {0, . . . , l},
          def
 – I exp = {(q, 0) | q ∈ I},
         def
 – F exp = {(q, l) | q ∈ F } and
           def
 – ∆exp = {((p, i), ϕ, (q, i+1)) | (p, ϕ, q) ∈ ∆, i ∈ {0, . . . , l−1}}∪{((p, l), ϕ, (q, l)) |
   (p, ϕ, q) ∈ ∆}.
It is easy to check that this automaton M exp (e     x) satisfies the conditions (i) and
(ii) described above.
     Now we are ready to construct the ss-NFA M ′ (e         e′ ). We construct this au-
                                                          x, x
tomaton in a step-by-step manner and only show how each step work.
     Suppose that Ti = cons(e  s, cons(sm , Ti′′ )), where se = s1 , . . . , sm−1 . We de-
scribe how to remove the innermost cons by constructing a new (k, n + 1)-ary
ss-NFA M (i,m) (ex, y) from M exp (ex) and integer terms e    t′ and list terms Te′ such
that

  RM(ex) (Te, e
              t) is satisfiable in M iff RM (i,m) (ex,y) (Te′ , e
                                                                t′ , s′m ) is satisfiable in M
                                                                                              (6)

The set of states, initial states and final states of M (i,m) (e x, y) are the same as
that of M exp(e
              x). That is we define M (i,m) (e
                                             x, y) as (Qexp , I exp , F exp , ∆(i,m) ) with
26       T. Shimoda et al.

an appropriate transition relation ∆(i,m) (as described below). By repeating this
process, we can ensure the cons-freeness.
   We proceed by a case analysis on the shape of Ti′′ .
                                                              def
(Case where Ti′′ = nil ) In this case, we set Ti′ = cons(e   s, Y ), where Y is a
                        ′ def                            def           def
   fresh variable, and Tj = Tj if j 6= i. We also set e
                                                      t = e
                                                       ′
                                                             t and s′m = sm . We
     define ∆(i,m) as
        {((q, m − 1), ϕ[y/li ], (q ′ , m)) | ((q, m − 1), ϕ, (q ′ , m))) ∈ ∆exp }
        ∪ {((q, i), ϕ, (q ′ , i′ )) | ((q, i), ϕ, (q ′ , i′ ) ∈ ∆exp and i < m − 1}
        ∪ {((q, i), ϕ ∧ pad (li ), (q ′ , i′ )) | ((q, i), ϕ, (q ′ , i′ ) ∈ ∆exp and m − 1 < i}
   Now we check that the property (6) indeed holds. Suppose that M, α |=
   RM(ex) (Te, et) and Jsm KM,α = j. Then it is easy to check that M, α[Y 7→ j] |=
   RM (i,m) (ex,y) (Te′ , e
                          t′ , sm ) because JTi′ KM,α[Y 7→j] = JTi KM,α . Now suppose that
   M, α |= RM (i,m) (ex,y) (Te′ , e   t′ , s′m ). Then JY KM,α = j for some integer j (or
   JY K = ǫ), otherwise we cannot obtain an accepting run of the automaton
   because of the condition pad (li ) we added. So, JTi′ KM,α and JTi KM,α must
   coincide except for the m-th element, which is Jsm KM,α for the list JTi KM,α
   and j (or  if JY K = ǫ) for JTi′ KM,α . Since at the m-th step, the automaton
   M (i,m) (e
            x, y) ignores the input from JT ′ KM,α , and uses the integer Jsm KM,α
   instead, it follows that M, α |= RM(ex) (Te, e        t).
(Case where Ti′′ = tail r (X)) For this case, we define ∆(i,m) as

             {((q, m − 1), ϕ[y/li ], (q ′ , m)) | ((q, m − 1), ϕ, (q ′ , m))) ∈ ∆exp }
             ∪ {((q, i), ϕ, (q ′ , i′ )) | ((q, i), ϕ, (q ′ , i′ ) ∈ ∆exp and i 6= m}.
                def                                                      def
     We set Ti′ = cons(se′ , Ti′′ ), where se′ = se[tail (X)/X], and Tj′ = Tj [tail (X)/X]
                                    def                                        def
     if j 6= i. Similarly, we set t′i = ti [tail (X)/X] for each i and s′m = sm [tail (X)/X].
     We conclude the proof by checking the property (6). Suppose that M, α |=
     RM(ex) (Te, et) and α(X) = w. Then it is easy to check that M, α[X 7→ 0w] |=
     RM (i,m) (ex,y) (Te′ , e
                            t′ , s′m ). First, observe that

        JTi′ KM,α[X7→0w] = Js′1 KM,α[X7→0w] · · · Js′m−1 KM,α[X7→0w] JTi′′ KM,α[X7→0w]
                           = Js1 KM,α · · · Jsm−1 KM,α JTi′′ KM,α[X7→0w]
                           = Js1 KM,α · · · Jsm−1 KM,α a JTi′′ KM,α

     for some a ∈ Z, which is the word obtained by replacing the m-th element of
     JTi KM,α with a. Since (1) a is ignored by the automaton M (i,m) (e    x, y), and
     Js′m KM,α[X7→0w] = Jsm KM,α is used instead, (2) Jti KM,α = Jt′i KM,α[X7→0w] ,
     and (3) JTj KM,α = JTj′ KM,α[X7→0w] for j 6= i, it follows that M, α[X 7→
     0w] |= RM (i,m) (ex,y) (Te′ , e
                                   t′ , s′m ).
     Now assume that M, α |= RM (i,m) (ex,y) (Te′ , e
                                                    t′ , s′m ). If α(X) = iw for some
     i ∈ Z and w ∈ Z , then we can show that M, α[X 7→ w] |= RM(ex) (Te, e
                          ∗
                                                                                    t).
                                                                Symbolic Automatic Relations                   27

    Otherwise, α(X) = ǫ. Since we defined tail M (ǫ) = ǫ, we have JTj′ KM,α =
    JTj KM,α for j 6= i and the same hold for et′ , se′ and s′m . It follows that
                    e   e
    M, α |= RM(ex) (T , t).
                                                                               ⊓
                                                                               ⊔

A.2    Detailed proof of Theorem 2
We give a more detailed proof of Theorem 2. In particular, we explain how to
construct an assignment from a given derivation.
    The following lemma is a basic property of derivations that we will use to
prove the correctness of the reduction. We omit the proof for this lemma as it is
a standard property of SLD-resolution.
                                                                                                          (C1 ,θ1 )
Lemma 3. Let Π be a system of linear CHCs. Suppose that hA0 | ψ0 i
           (C2 ,θ2 )       (Cn ,θn )
hA1 | ψ1 i     ···        h⊤ | ψn i is a derivation with respect to Π and let α
be an assignment such that Z , α |= ψn . If ψi is of the form ψi1 ∧ ψi2 (up to
commutativity and associativity of conjunction) then Z , α |= θi+1 θi+2 · · · θn ψi1 .
                                                                                    ⊓
                                                                                    ⊔

Proof (Detailed proof of Theorem 2). Suppose that M (e            x) = (Q, I, F, ∆), Te =
                                                     def
T0 , . . . , Tk−1 , ye = y0 , . . . , yn−1 and let Π = LRM(ex) (Te, ye)M. As explained, it
suffices to show that RM(ex) (Te, ye) is satisfiable if and only if there is a derivation
starting from hq(e        e) | ϕend i with respect to Π for some q ∈ F . We omit the
                       u, x
only if direction. This is because we think the proof of the only if case is not
that difficult and the idea of the proof has already been given.
     (If) By assumption, there is a derivation
                                  (Cm ,θm )         (C1 ,θ1 )                           (C0 ,θ0 )
      hqm (e    em ) | ψm i
           um , x                             ···               hq0 (e    em ) | ψ0 i
                                                                     u0 , x                         h⊤ | ψi

where ψm = ϕend . Here we assume that variables u           em = ui0 , . . . , ui(k−1) and
x
ei = xi0 , . . . , xi(n−1) are appropriately renamed to avoid name clash. (We may
simply write u    e or uj to mean uei or uij for some i that is clear from the context.)
Because a clause in Π that contains predicates in both the body and the head
is a clause that corresponds to an element of the transition relation, for every
                                       ϕ                               ϕ
Ci (1 ≤ i ≤ m), we have Ci = Lq −      → pM for some transition (q −   → p) ∈ ∆.
    We construct an accepting run of M (e       x) using an assignment in Z and the
unifiers. Take an assignment α such that Z , α |= ψ, which exists because ψ is
                                  def
satisfiable in Z . Let θ≤i = θ0 ◦θ1 ◦· · ·◦θi . We define aij ∈ Z , where 0 ≤ i ≤ m
                                   def                                         def
and 0 ≤ j ≤ k − 1, by aij = Jθ≤i (uij )KZ ,α and set ai = (ai0 , . . . , aik−1 ). Note
that am = (, . . . , ) because M, α |= θ≤m ϕend must hold by Lemma 3. We
                def
also define ji = Jθ0 (xi )KM,α and write e j for j0 , . . . , jn . Our goal is to show that
a0 a1 · · · am−1 is an accepting run of M (e
                                           j) such that
             a
             0     1   a          am−1                            ai−1
         q0 −→ q1 −→ · · · −−−→ qm and qi−1 −−−→ qi corresponds to Ci .
28       T. Shimoda et al.

The fact that q0 is initial and qm is final is obvious because only predicate symbols
corresponding to initial (resp. final) states can appear in the initial (resp. final)
                                                            ai
derivation state. Thus, it suffices to check that qi −→          qi+1 is a valid transition for
every i ∈ {0, . . . , m− 1}. First observe that Jθ≤i (xl )K = jl for any i ∈ {0, . . . , m}.
                                                                  ϕ
                                                          (Lqi−1 −→qi M,θi )
Recall that, for each i, we have hqi (e         e) | ψi i
                                             u, x                            hqi−1 (e  e) | ψi−1 i
                                                                                    u, x
for some ϕ. Thus, ψi−1 is of the form θi (ϕ[u0 /l0 , . . . , uk−1 /lk−1 ]) ∧ ψ ′ for some
ψ ′ . By Lemma 3, Z , α |= θ≤i (ϕ[u0 /l0 , . . . , uk−1 /lk−1 ]) must hold. Since the free
variables of ϕ are among e       e, we have Z , [e
                              l, x                             e 7→ e
                                                     l 7→ ai , x    j] |= ϕ as desired.
      Next we show that the accepting run a0 a1 · · · am−1 can be given as a con-
volution of words c(w0 , . . . , wk−1 ); note that such w0 , . . . , wk−1 ∈ Z∗ are unique
                          def
if they exist. Let wi′ = a0i a1i · · · am−1i . It suffices to show that (i) for each i,
wi = wi wi for some wi ∈ Z∗ and wi′′ ∈ {}∗ and (ii) wi′ ∈ Z∗ for some i. Then
  ′         ′′

we have c(w0 , . . . , wl−1 ) = a0 a1 · · · am−1 . To prove (i), first note that, for each
i ∈ {0, . . . , m − 1}, ψi must be of the form θi ϕpad ∧ ψ ′ because ϕpad appears
in the body of Ci+1 . Since M, α |= θ≤i ϕpad holds Lemma 3, it follows that “if
aij =  then ai+1j = ”. Hence, (i) holds. To prove (ii) first observe that ψm−1
must be of the form ¬ϕend ∧ ψ ′ with the free variables of ¬ϕend being u                   em−1 .
Thus, by Lemma 3, we have M, α |= θ≤m−1 (¬ϕend ). This implies that there
exists i such that am−1i ∈ Z. Therefore, from (i), we have wi′ ∈ Z∗ .
      It remains to show that there is an assignment β in M such that JTi KM,β = wi
for every i ∈ {0, . . . , k − 1}. Since {T0 , . . . , Tk−1 } is gap-free, each list variable
                                                                                           def
X that is free in Te must be equal to some Ti . We define β by β(X) = wi
provided that X = Ti . What we need to verify is (i) wi = ǫ if Ti = nil and
(ii) wi = Jtail m (X)KM,β if Ti = tail m (X). It is easy to check that (i) holds
because, by the constraint ϕnil , a0i must be  if Ti = nil . The statement (ii)
is proved by induction on m. The case where m = 0 is trivial. Suppose that
0 < m, Tj ′ = tail m−1 (X) and Tj = tail m (X). By the induction hypothesis, we
have JTj ′ KM,β = wj ′ . If wj ′ = ǫ then we can easily check that wj = ǫ using
the constraint ϕtail(nil) . So, let us consider the case where wj 6= ǫ. Observe that,
for each i ∈ {0, . . . , m − 1}, ψi must be of the form θi ϕshift ∧ ψ ′ because ϕshift
appears in the body of Ci+1 . By Lemma 3, we have M, α |= θ≤i ϕshift . We thus
have aij ′ = a(i−1)j for all i ∈ {1, . . . , m}. (Note that in particular we have
a(m−1)j =  because amj = ). Therefore, wj is the tail of wj′ as desired.
                                                                                               ⊓
                                                                                               ⊔
                                            Symbolic Automatic Relations      29

B    Details of the Experiments

Tables 2 and 3 show the lists of the instances of the benchmark sets used in
the experiments. The column “Instance” shows the name of the instances. The
column “Property” shows the properties represented in the instances. The col-
umn “Validity” shows the validity of the property. The checkmark X indicates
that the property holds. In the benchmark “CHC”, “VC:” means the verification
condition for refinement types. We use a set-like notation x ∈ X for that x is an
element of the list X.
    Tables 4 and 5 show the experimental results. The numbers in the tables
show the running time of the tool for the instance in seconds. The empty cell
means the tool does not verify the instance by the timeout or aborts by out
of memory. The only instance that is not verified by our tool is “sumfold-gte”,
which is not verfied by also the other solvers.
30     T. Shimoda et al.


            Table 2. Lists of the instances in the benchmark sets (1/2)

Benchmark Instance             Property                                                       Validity
IsaPlanner prop 04           1 + count (n, X) = count (n, cons(n, X))                               X
IsaPlanner prop 05           n = x ⇒ 1 + count (n, X) = count (n, ins(x, X))                        X
IsaPlanner prop 15           length(ins(x, X)) = 1 + length(X)                                      X
IsaPlanner prop 16           X = nil ⇒ last (ins(x, X)) = x                                         X
IsaPlanner prop 29           count (x, (ins1 (x, X)))                                               X
IsaPlanner prop 30           count (x, (ins(x, X)))                                                 X
IsaPlanner prop 39           count (n, X) + count (n, cons(m, nil)) = count (n, cons(m, X))         X
IsaPlanner prop 40           take(0, X) = nil                                                       X
IsaPlanner prop 42           n ≥ 0 ∧ Y = take(n, X) ∧ zs = take(n + 1, ins(x, X))                   X
                                  ⇒ zs = ins(x, Y )
IsaPlanner prop 50           Y = butlast (X) ∧ n = length(X) ⇒ Y = take(n − 1, X)                   X
IsaPlanner prop 62           X 6= nil ⇒ last (cons(x, X)) = last (X)                                X
IsaPlanner prop 67           length(butlast (X)) = length(X) − 1                                    X
IsaPlanner prop 71           x 6= y ⇒ count (x, (ins(y, X))) = count (x, X)                         X
IsaPlanner prop 77           sorted (X) ∧ Y = insort (x, X) ⇒ sorted (Y )                           X
IsaPlanner prop 86           x < y ⇒ count (x, (ins(y, X))) = count (x, X)                          X
SAR SMT count cons           count (x, X) ≤ count (x, ins(y, X))                                    X
SAR SMT count cons eq        x = y ∧ n = count (x, X) ⇒ n + 1 = count (x, ins(y, X))                X
SAR SMT count cons invalid count (x, X) = count (x, ins(y, X))
SAR SMT count cons neq1      x 6= y ⇒ count (x, X) = count (x, ins(y, X))                           X
SAR SMT count cons neq2      x 6= y ⇒ count (x, X) = count (x, ins(y, X))                           X
SAR SMT count nil1           count (x, nil) = n ⇒ n = 0                                             X
SAR SMT count nil2           count (x, nil) = 0                                                     X
SAR SMT ins head1            x < y ⇒ ins(x, cons(y, X)) = ins(x, cons(y, X))                        X
SAR SMT ins head2            x ≥ y ∧ ins(x, X) = Y                                                  X
                                  ⇒ ins(x, cons(y, X)) = cons(y, cons(x, Y ))
SAR SMT ins insort           sorted (X) ⇒ ins(x, X) = insort (x, X)                                 X
SAR SMT ins insort invalid   ins(x, X) = insort (x, X)
SAR SMT ins nil              X = nil ⇒ ins(x, X) = cons (x, nil)                                    X
SAR SMT last nil             X = nil ⇒ last (nil) = 0                                               X
SAR SMT last singleton       Y = cons(x, nil) ⇒ last (Y ) = x                                       X
SAR SMT length 2             length(cons(x, cons(y, nil))) ≥ 3
SAR SMT length cons1         n = length(cons(x, X)) ∧ n′ = length(X) ⇒ n = n′ + 1                   X
SAR SMT length cons2         n = length(X) ⇒ n + 1 = length(cons(x, X))                             X
SAR SMT length cons invalid length(cons(x, X)) = length(X)
SAR SMT length count         length(X) ≥ count (x, X)                                               X
SAR SMT length count invalid length(X) > count (x, X)
SAR SMT length nat           length(X) ≥ 0                                                          X
SAR SMT length nil           X = nil ⇒ length(X) = 0                                                X
SAR SMT length non nil       length(cons(x, X)) ≥ 1                                                 X
SAR SMT prefix antisymetric prefix (X, Y ) ∧ prefix (Y, X) ⇒ X = Y                                  X
SAR SMT prefix cons          prefix (X, cons(x, X)) ⇒ ∀y ∈ X. x = y                                 X
SAR SMT prefix cons invalid prefix (X, cons(x, X))
SAR SMT prefix count         prefix (X, Y ) ⇒ count (x, X) ≤ count (x, Y )                          X
SAR SMT prefix count invalid prefix (X, Y ) ⇒ count (x, X) > count (x, Y )
                                               Symbolic Automatic Relations      31

            Table 3. Lists of the instances in the benchmark sets (2/2)

Benchmark Instance                  Property                                                   Validity
SAR SMT prefix exists             prefix (X, Y ) ∧ 0 ∈ X ⇒ 0 ∈ Y                                     X
SAR SMT prefix exists invalid     prefix (X, Y ) ∧ 0 ∈ Y ⇒ 0 ∈ X
SAR SMT prefix forall             prefix (X, Y ) ∧ (∀y ∈ Y. 0 ≤ y) ⇒ ∀x ∈ X. 0 ≤ x                   X
SAR SMT prefix forall invalid     prefix (X, Y ) ∧ (∀x ∈ X. 0 ≤ x) ⇒ ∀y ∈ Y. 0 ≤ y
SAR SMT prefix hd                 prefix ((cons(x, X)), (cons(y, Y ))) ⇒ x = y                       X
SAR SMT prefix length             prefix (X, Y ) ⇒ length(X) ≤ length(Y )                            X
SAR SMT prefix non nil            prefix ((cons(x, X)), Y ) ⇒ Y 6= nil                               X
SAR SMT prefix nth                prefix (X, Y ) ∧ x = nth(X, i) ⇒ x = nth(Y, i)                     X
SAR SMT prefix sum                prefix (X, Y ) ∧ (∀y ∈ Y. 0 ≤ y) ⇒ sum(X) ≤ sum(Y )                X
SAR SMT prefix sum invalid        prefix (X, Y ) ⇒ sum(X) ≤ sum(Y )
SAR SMT prefix trans              prefix (X, Y ) ∧ prefix (Y, zs) ⇒ prefix (X, zs)                   X
SAR SMT scan sum length           Y = sum(X) ⇒ length(X) = length(Y )                                X
SAR SMT scan sum pos              Y = sum(X) ∧ (∀y ∈ Y. 0 ≤ y) ⇒ ∀x ∈ X. 0 ≤ x                       X
SAR SMT scan sum pos invalid      Y = sum(X) ∧ (∀x ∈ X. 0 ≤ x) ⇒ ∀y ∈ Y. 0 ≤ y
SAR SMT sorted                    sorted(X) ∧ headX ≥ 0 ⇒ 0 ≤ nth(X, i)                              X
SAR SMT sorted forall             sorted ((cons(x, X))) ⇒ ∀x ∈ X. 0 ≤ x                              X
SAR SMT sorted neg                ¬(sorted ((cons(x, X))) ∧ (∃x′ ∈ X. 0 > x′ ) ∧ x ≥ 0)              X
SAR SMT sorted nth                sorted ((cons(x, X))) ⇒ x ≤ nth(X, i)                              X
SAR SMT sorted pos                sorted ((cons(x, X))) ∧ 0 ≤ x ⇒ ∀x ∈ X. 0 ≤ x                      X
SAR SMT sorted prefix             sorted (Y ) ∧ prefix (X, Y ) ⇒ sorted (X)                          X
SAR SMT sorted singleton          sorted ((cons(x, X))) ∧ (∃x′ ∈ X. x > x′ ) ⇒ X = nil               X
SAR SMT sumfold gte               (∀x ∈ X. 0 ≤ x) ∧ sum(X) ≥ x × length(X)                           X
SAR SMT take cons                 n > 0 ∧ Y = take(n − 1, X)                                         X
                                       ⇒ cons(x, Y ) = take(n, (cons(x, X)))
SAR SMT take exists               Y = take(n, X) ∧ 0 ∈ X ⇒ 0 ∈ Y                                     X
SAR SMT take length               n ≥ 0 ∧ Y = take(n, X) ⇒ length(Y ) ⇒ n                            X
SAR SMT take length invalid       Y = take(n, X) ⇒ length(Y ) = n
SAR SMT take nil                  take(n, X) = nil                                                   X
SAR SMT take sum                  Y = take ′ (n, X) ∧ (∀x ∈ X. 0 ≤ x) ⇒ sum(Y ) ≤ sum(X)             X
SAR SMT take total count          Y = take ′ (n, X) ⇒ count (x, X) ≤ count (x, Y )                   X
SAR SMT take total length eq      Y = take ′ (n, X) ∧ 0 ≤ n ≤ length(Y ) ⇒ n = length(X)             X
SAR SMT take total length invalid Y = take ′ (n, X) ∧ n ≤ length(Y ) ⇒ n = length(X)
SAR SMT take total length leq     X = take ′ (n, Y ) ∧ n1 = length(X) ∧ n2 = length(Y )              X
                                       ⇒ n1 ≤ n2
CHC     compare length            properties on comparisons of list lengths                          X
CHC     fib                       a property on the length of lists of the fibonacci numbers         X
CHC     filter                    VC: filter reduces the length of the given list                    X
CHC     insert sort               VC: sortedness of insertion sort                                   X
CHC     insertion                 sortedness of insertion                                            X
CHC     leq list                  antisymetricity of the dictionary order on lists                   X
CHC     make length               VC: make generates a list of the given length                      X
CHC     merge sort                VC: sortedness of merge sort                                       X
CHC     rev length                VC: reverse preserves lengths                                      X
CHC     same                      (∀x ∈ X. x = y) ∧ (∃x ∈ X. x = y + 1) ⇒ ⊥                          X
CHC     sorted                    sorted (cons(1, X)) ∧ (0 ∈ X) ⇒ ⊥                                  X
CHC     sum                       a property on element-wise summation                               X
32     T. Shimoda et al.

                       Table 4. Experimental results (1/2)

                                        Ours                  (rec)              (assert)
                              Spacer   HoIce    Eldarica     Z3   CVC4          Z3    CVC4
IsaPlanner
  prop 04.smt2                          1.891      3.741                      0.018    0.012
  prop 05.smt2                          4.756       5.42
  prop 15.smt2                          4.103      3.725                               0.287
  prop 16.smt2                 0.823    0.877      1.531 0.019        0.009 0.018      0.006
  prop 29.smt2                  0.17    0.168      0.657 0.019        0.012 0.019      0.013
  prop 30.smt2                 0.179    0.178      0.649 0.019        0.014
  prop 39.smt2                                     6.151                    0.017      0.016
  prop 40.smt2                 0.285      0.3      1.003 0.017        0.006 0.018
  prop 42.smt2                         58.646      8.199                    0.013      0.007
  prop 50.smt2                          0.922
  prop 62.smt2                 2.837    3.266      3.917 0.041    0.0209 0.020
  prop 67.smt2                         16.086      16.73
  prop 71.smt2                 1.644    4.566      4.849
  prop 77.smt2                 0.456    1.067      2.227
  prop 86.smt2                 1.564    5.321      4.741
SAR SMT
  count cons.smt2                      13.543      3.536 0.018        0.011 0.018      0.008
  count cons eq.smt2                    1.913      2.857 0.014        0.012 0.021       0.01
  count cons invalid.smt2      1.275    1.613      3.462 0.021        0.015
  count cons neq1.smt2                  20.32      5.371                    0.016      0.008
  count cons neq2.smt2                              3.55 0.017        0.014 0.021      0.008
  count nil1.smt2              0.434    0.432      0.916 0.019        0.009 0.018      0.007
  count nil2.smt2              0.092    0.087       0.58 0.019        0.010 0.019      0.008
  ins head1.smt2               0.608    0.613      1.174 0.019        0.007 0.017      0.009
  ins head2.smt2               1.993    5.792      4.222 0.016        0.012 0.021      0.009
  ins insort.smt2              0.784    4.061      2.073
  ins insort invalid.smt2      0.716    1.165      1.847 0.020        0.031
  ins nil.smt2                 0.246    0.261      0.926 0.020        0.013 0.020      0.005
  last nil.smt2                0.426     0.42      0.893 0.018        0.009 0.015      0.006
  last singleton.smt2          0.495     0.66      1.276 0.019        0.007 0.018      0.005
  length 2.smt2                0.639     0.65      1.325 0.018        0.013
  length cons1.smt2                     2.705      2.542 0.018        0.010 0.019      0.007
  length cons2.smt2                     0.528      1.446 0.020        0.010 0.019       0.01
  length cons invalid.smt2     1.209    1.421       2.44 0.017         0.01
  length count.smt2                    29.491      2.628
  length count invalid.smt2    1.257    1.355      2.485 0.019        0.007
  length nat.smt2              0.493    0.534      1.312
  length nil.smt2              0.155    0.114      0.743 0.036        0.028 0.018      0.008
  length non nil.smt2            0.5    0.528      1.364
  prefix antisymetric.smt2     0.148    0.087      0.678
  prefix cons.smt2             0.184      0.2      0.827
  prefix cons invalid.smt2     0.161    0.184      0.962 0.019         0.01
  prefix count.smt2                                2.666
  prefix count invalid.smt2     1.31    1.794      2.705 0.017        0.011
                                               Symbolic Automatic Relations           33

                       Table 5. Experimental results (2/2)

                                       Ours                   (rec)              (assert)
                             Spacer   HoIce    Eldarica    Z3    CVC4           Z3    CVC4
 prefix exists                0.147    0.141       0.628
 prefix exists invalid        0.192    0.202       1.052 0.016         0.01
 prefix forall                0.091    0.087       0.568
 prefix forall invalid        0.139    0.162       0.958 0.019        0.011
 prefix hd                    0.214    0.212       0.697 0.018        0.009 0.019      0.005
 prefix length                         1.778        2.58 0.016        0.010 0.015      0.007
 prefix non nil                0.06    0.062       0.554 0.020        0.010 0.019      0.007
 prefix nth                            1.732       5.454
 prefix sum                   1.319   20.028       2.612
 prefix sum invalid           1.363    1.641       2.622 0.041        0.034
 prefix trans                 0.134    0.083       0.675
 scan sum length                       2.043       3.058
 scan sum pos                 0.214    0.199       1.232
 scan sum pos invalid         0.212    0.204       1.296 0.043        0.048
 sorted                       0.999    1.153       2.322
 sorted forall                0.175    0.211       0.988
 sorted neg                   0.424    0.505       1.439
 sorted nth                   0.565    0.721       1.706
 sorted pos                    0.32    0.404       1.243
 sorted prefix                0.152    0.165       1.266
 sorted singleton             0.208    0.271        0.89 0.017        0.013 0.019
 sumfold gte
 take cons                             3.306       3.908 0.039         0.03 0.017      0.010
 take exists                  0.385    0.771       1.834
 take length                           4.801       4.203
 take length invalid          1.289    1.664       3.048 0.019        0.008
 take nil                     0.169    0.118       0.707 0.039        0.028 0.018      0.008
 take sum                     3.523   47.381       6.189
 take total count                                   7.01
 take total length eq                              10.85
 take total length invalid     6.36   55.695       9.545 0.018        0.012
 take total length leq                11.185       6.054
CHC
 compare length               1.174    1.328       5.629
 fib                                  16.824      20.671
 filter                                4.763      10.414                      0.035    0.013
 insert sort                  3.013   28.891      13.806              0.048
 insertion                    3.786     8.14      12.265                      0.018
 leq list                     0.407     0.66       2.428
 make length                            3.84       9.109 0.017        0.022 0.013      0.022
 merge sort                   5.185               33.017               0.08
 rev length                            4.746      12.024                    0.023      0.011
 same                         0.571    0.628       3.809
 sorted                         0.9    1.473       4.967
 sum                          0.809    1.129       4.797
