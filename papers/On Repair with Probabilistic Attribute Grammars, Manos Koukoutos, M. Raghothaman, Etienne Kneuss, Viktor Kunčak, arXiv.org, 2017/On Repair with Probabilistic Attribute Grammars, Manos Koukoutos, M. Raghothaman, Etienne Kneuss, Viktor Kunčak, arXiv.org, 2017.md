                                                   On Repair with Probabilistic Attribute Grammars

                                                     Manos Koukoutos                  Mukund Raghothaman                    Etienne Kneuss
                                                               EPFL                     University of Pennsylvania                 EPFL
                                                emmanouil.koukoutos@epfl.ch            rmukund@seas.upenn.edu            etienne.kneuss@epfl.ch

                                                                                        Viktor Kuncak
                                                                                               EPFL
arXiv:1707.04148v1 [cs.PL] 13 Jul 2017




                                                                                    viktor.kuncak@epfl.ch


                                               Program synthesis and repair have emerged as an exciting area of research, driven by the potential
                                               for revolutionary advances in programmer productivity. Among most promising ideas emerging
                                               for synthesis are syntax-driven search, probabilistic models of code, and the use of input-output
                                               examples. Our paper shows how to combine these techniques and use them for program repair,
                                               which is among the most relevant applications of synthesis to general-purpose code. Our approach
                                               combines semantic specifications, in the form of pre- and post-conditions and input-output examples
                                               with syntactic specifications in the form of term grammars and AST-level statistics extracted from
                                               code corpora. We show that synthesis in this framework can be viewed as an instance of graph
                                               search, permitting the use of well-understood families of techniques such as A*. We implement our
                                               algorithm in a framework for verification, synthesis and repair of functional programs, demonstrating
                                               that our approach can repair programs that are beyond the reach of previous tools.


                                         1    Introduction
                                         Program synthesis has attracted significant attention as a promising and ambitious approach to improve
                                         software development productivity [21, 33, 1, 10, 30, 15, 12, 13, 23, 11, 26, 18, 20]. Among possibly de-
                                         ployment scenarios of synthesis is program repair, in which a tool localized an error repairs the program
                                         by synthesizing an alternative code fragment [24, 17].
                                              Synthesis tools typically leverage both semantic and syntactic specification of the synthesis process.
                                         Typical forms of semantic information are specifications in the form of input-output examples, as well
                                         as reference implementations and predicates. These specifications are important to identify the specific
                                         intent of the developer. Among the syntactic forms of specification are simple types and probabilistic
                                         models of code. Syntactic models of code are appealing for two main reasons: they can improve the
                                         efficiency of search, and they can provide implicit, reusable baseline specifications that apply across
                                         multiple synthesis problems, reducing the need to provide near-complete semantic specifications of the
                                         desired functionality.
                                              Our work aims to unify these two sources of specifications. To this extent, we describe a specification
                                         framework and an algorithms that efficiently searches for programs based on:
                                             • a probabilistic and polymorphic attribute grammar that restricts and prioritizes the relevant space,
                                               and
                                             • dynamically growing set of input examples along with test predicates, which narrows down the
                                               developer’s intent.
                                             Our attribute grammars describe the generation of trees and can be thought of as a probabilistic ex-
                                         tension of type systems used in previous work. The use of generics and attributes makes the grammars


                                         To appear in EPTCS.
2                                                        On Repair with Probabilistic Attribute Grammars


compact and enables us to naturally describe constructs such as conditionals that are needed to generate
more complex code fragments. Thanks to the fact that we use a language supporting generics and value
classes (Scala), we show how to describe such derived grammars in the form of a wrapper library. The
developers can therefore use mostly existing programming language constructs to describe the intended
models of use of their libraries. The use of attributes enables the developers to incorporate domain
knowledge, such as associativity of operators, which can break symmetries and reduce the search space.
In addition to explicitly writing such models, we present an algorithm to automatically derive models
from a corpus of code. Our results show that the derived corpus provides benefits in synthesis of mean-
ingful code fragments.
     Our algorithm efficiently supports specifications that include concrete inputs. In the case where
the provided set of inputs is not sufficient to narrow down the search, our system can also make use
of constraint solvers to generate additional inputs. To make search driven by probabilistic grammars
efficient, we adopt a top-down approach for search. We introduce techniques to prune the search for
expressions using partial evaluation of incomplete grammars on known input examples. Furthermore,
we show how to incorporate equivalence modulo input-output examples in such a search algorithm,
which is a technique that has so far been deployed primarily in bottom-up search techniques.
     The practical focus of our techniques is on program repair. We use manually supplied and automati-
cally derived examples to localize the expression likely to be responsible, then synthesize an alternative
expression in its place. Examples are particularly relevant because they can be used to localize the error
efficiently. The support of input examples in our algorithm makes it efficient for synthesizing candidate
repairs. Furthermore, our support for probabilistic grammars enabled us to adopt the following approach
to repair with probabilistic models: in addition to using grammars describing general Scala expressions,
we bias the search for repairs towards the constructs specific for a program being repaired, making the
synthesis more effective. We therefore show that our approach is able to produce program repairs whose
size puts them beyond the reach of analogous existing non-probabilistic repair approaches.


2    Synthesis Algorithm
2.1 Synthesis problem
Let φ = φ (ā, x) be the specification of a programming task, specifying a relation between a sequence
of input parameters ā and an output variable x. φ can be given as a logical predicate, a set of input-
output examples, a reference implementation, or a combination thereof. Also, let Π = Π(ā) be the path
condition for the problem, i.e. a relation satisfied by hypothesis by the input parameters. Let also t = t(ā)
express a term in the target language.
    The synthesis problem is then defined as asking for a constructive solution for the formula

                                          ∀ā.∃t.Π =⇒ φ [x 7→ t]
    In other words, we want to find an expression t such that replacing every occurrence of the output
variable x in the synthesis predicate φ causes the formula Π =⇒ φ to be valid. In this section, we will
describe the probabilistic enumeration procedure used to solve such formulas.

2.2 Counter-example guided inductive synthesis (CEGIS)
The synthesis algorithm is an instantiation of CEGIS, a widely used framework to describe program
synthesis algorithms [33, 12]. The main technical difficulty with finding a t which satisfies rule Terminal
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                              3


is the universally quantified “∀ā”, where the input variables ā may range over a large, or even potentially
infinite domain. We present the CEGIS routine in Algorithm 1. The procedure is parameterized by two
sub-procedures, Search and Verify. At each step, we maintain a finite set A of concrete input points. In
the search phase, the algorithm finds an expression t, such that
                                              ^
                                                    Π =⇒ φ [x 7→ t].                                           (1)
                                             ā∈A

Observe that for a specific choice of A, determining whether a given t satisfies requirement 1 reduces
to simply evaluating the resulting expression. In the verification phase, we confirm that the candidate
expression t works for all inputs ā. The procedure Verify(ā, Π, φ , x,t) returns either: (a) valid, if t
satisfies the synthesis predicate for all values of ā, or (b) a counter-example input ācex , such that Π[ā 7→
ācex ] ∧ ¬φ [ā 7→ ācex , x 7→ t] i.e. ācex satisfies the path condition Π, but t fails the synthesis predicate.

Algorithm 1 CEGIS(Jā hΠ ⊲ φ i xK).

   1. Initialize A := 0.
                      / A is a finite set of concrete instantiations of ā.
   2. Repeat forever:
        (a) Let t = Search(ā, A, Π, φ , x).
        (b) Let res = Verify(ā, Π, φ , x,t).
        (c) If res = valid, then return t.
        (d) Otherwise, if res = ācex , update A := A ∪ {ācex }.


   We discharge the calls to Verify by invoking Leon’s verification system [9]. The main technical
contribution of this paper is in using probabilistic enumeration to instantiate the Search subroutine. We
devote the rest of this section to describing this procedure.

2.3 Probabilistic expression grammars
The goal of the Search(ā, A, Π, φ , x) subroutine is to find a candidate expression t which satisfies the
synthesis predicate for all input points ā ∈ A. The expression t is drawn from the productions of a
probabilistic context-free grammar (PCFG), such as that shown below:
       IntExpr ::=       0                                                          (Rule R0 , p0 = 0.15)
                 |       1                                                          (Rule R1 , p1 = 0.3)
                 |       x                                                          (Rule Rx , px = 0.3)
                 |       IntExpr + IntExpr                                          (Rule R+ , p+ = 0.15)
                 |       if (BoolExpr) { IntExpr } else { IntExpr }                 (Rule Rite , pite = 0.1)
      BoolExpr ::=       IntExpr ≤ IntExpr                                          (Rule R≤ , p≤ = 0.8)
                 |       BoolExpr && BoolExpr                                       (Rule R∧ , p∧ = 0.2)
The productions of IntExpr expand to expressions of type Int, and the productions of BoolExpr expand
to expressions of type Bool. Each rule R of each non-terminal symbol N is annotated with a number pR ,
which indicates the probability of N expanding to R. Naturally, the probability pe of a production e is
then defined as the product of the probabilities of all rules invoked in the derivation tree: for example,
the production x + 1 has probability p+ px p1 = 0.0135.
    More generally, a PCFG is a pair G = (N , R), where:
4                                                              On Repair with Probabilistic Attribute Grammars


    1. N is a finite, non-empty set of non-terminal symbols, where each non-terminal N ∈ N is associ-
       ated with a type TN ,
    2. R maps each non-terminal N to a finite set of production rules R(N). Each production rule
       R ∈ R(N) is a well-typed construct of the form R = t(N1 , N2 , . . . , Nk ), where t is the top-level
       operator, N1 , N2 , . . . , Nk are the child non-terminal symbols, and such that the output types of t
       and N coincide: Tt = TN , and
    3. each rule R is associated with a probabiltiy pR ∈ [0, 1] such that for all non-terminals N, ∑R∈R(N) pR =
       1.
    Notice that N does not necessarily coincide with the set of types of the target language; we only
require that the mapping from non-terminals to types is surjective.
    We make two additional requirements of the PCFGs we consider in this paper: first, we require the
probability of each rule, pR < 1 (note the strict inequality), and second, we require that G be unam-
biguous, i.e. that every expression produced by the grammar have a unique derivation tree. If we relax
the first assumption, then there are some technical difficulties in setting up the probability space, and
results such as Theorem ?? will need additional constraints to be true. The second assumption simplifies
the definition of P(e), which would otherwise be the sum of the probabilities over all derivation trees.
Moreover, it reduces the search space to a tree (instead of a DAG), and thereby allows us to use stronger
versions of the guarantees provided by search algorithms.
    For simplicity of notation, and whenever the intent is clear, we will conflate productions e of the
grammar with the expressions te that they encode. We write EN for the set of all productions of a non-
terminal N. Given a production e ∈ EN , we define its probability, P(e), as the product of the probabilities
of all rules used in e. It can be shown that ∑e∈EN P(e) = 1. The productions of G will constitute ele-
ments of the sample space under consideration, and the space of events is, as usual, the powerset 2EN of
productions. We will discuss the extraction of PCFGs from a code corpus in Section 3.

2.4 Top-down expression enumeration as graph search
In the search phase of the CEGIS loop, we want to find an expression t which satisfies the requirement in
formula 1. One approach to implementing Search(ā, A, Π, φ , x) is to enumerate all candidate expressions,
in some order, until a suitable answer is found. Recall that, because A is a finite set, for a given choice
of A and t, determining the satisfaction of formula 1 reduces to evaluating the conjunction, and does not
involve expensive calls to an SMT solver. The enumerative SyGuS solver [34] uses a highly optimized
form of expression enumeration in the search phase, and is currently among the most competitive SyGuS
solvers. See Algorithm 2. In this section, we will show how we utilize a PCFG to enumerate expressions
in order of decreasing probability in order to accelerate the search process. We will now describe this
probabilistic enumeration algorithm.

Partial productions. Engineering the enumeration algorithm turns out to be much simpler if we enu-
merate expressions top-down rather than bottom-up. As a first step, we therefore extend the idea of a
grammar production into the more general notion of a partial production:

                                     ẽN   ::= ?N | t(ẽN1 , ẽN2 , . . . , ẽNk ),

where R = t(N1 , N2 , . . . , Nk ) is a production rule of N in G. In particular, notice that partial produc-
tions may contain incomplete sub-expressions, denoted by ?N . Examples of partial productions include
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                            5


Algorithm 2 Search(ā, A, Π, φ , x). Implements the search phase of the CEGIS loop by expression enu-
meration.
   1. Let G be the chosen PCFG, and N be the starting non-terminal such that the types coincide, i.e.
      TN = Tx .
   2. For each e emitted by Enumerate(G, N):
        (a) Let te be the expression encoded by e.
              V
        (b) If ā∈A Π =⇒ φ [x 7→ te ] = true, return te .
        (c) Otherwise, discard t and continue enumeration.


“x + ?” and “if (x ≤ ?) { x } else { ? }”. We write E˜N for the set of all partial productions of
a non-terminal N. We can also speak of the probability of partial productions: pẽ of a partial production
ẽ is the product of all production rules used to derive ẽ. It will be mathematically more convenient to
speak of negative log probabilities: the cost of a partial production ẽ,

                                    cost(ẽ) = − log(pẽ ) = − ∑ log(pR ).                                   (2)
                                                               R∈ẽ

     Given a pair of partial productions ẽ1 and ẽ2 , we say that ẽ1 and ẽ2 are related by the expansion
relation, and write ẽ1 → ẽ2 , if ẽ2 can be obtained by replacing the left-most instance of ? in ẽ1 by an
appropriate production rule. For example, if ẽ1 = x + ?, ẽ2 = x + 1, and ẽ3 = x + (? + ?), then
ẽ1 → ẽ2 and ẽ1 → ẽ3 .
     The expansion relation naturally induces a tree G on the partial productions of a grammar G. See
Figure 1. The initial node is the starting non-terminal, ?. There is an edge from the partial production
ẽ1 to the partial production ẽ2 if they are related by the expansion relation, ẽ1 → ẽ2 . The edge ẽ1 → ẽ2 ,
produced by an instantiation of the rule R, is annotated with the cost of the rule, − log(pR ). Then, the
resulting graph is a tree because of the unambiguity assumption on G, and the sum of the weights along
the path to ẽ is equal to cost(ẽ). The main insight of this paper is that Enumerate(G, N) can be thought
of as instantiations of various search algorithms on this tree.

Algorithm 3 Enumerate(G, N). Emits a sequence of complete productions of N.

   1. Let π : E˜N → R≥0 be a priority function mapping productions to non-negative real numbers.
   2. Let Q be a priority queue of partial productions ẽ ∈ E˜N arranged in ascending order according to
      π . Initialize Q := {?N }.
   3. While Q is not empty:
        (a) Let ẽ be the element at the front of Q. Dequeue ẽ.
        (b) If ẽ is a complete production, emit ẽ.
        (c) Otherwise, for every neighbor ẽ′ such that ẽ → ẽ′ in G , insert ẽ′ into Q.


    See Algorithm 3. It is helpful to visualize the operation of the algorithm as shown in Figure 2.
The algorithm maintains a priority queue Q of still-unexpanded partial productions. At each step, the
algorithm dequeues the element ẽ at the front of this priority queue and, if it is still incomplete, expands
the leftmost ? with an instance of every applicable production rule R. This results in a set of partial
6                                                                                     On Repair with Probabilistic Attribute Grammars


                                                ?
                                                          −l




                                  − log(0.15)
                   )
                 15                                         og
            g (0.                                              (0.
                                                                  1)
           o
         −l

                   )
             .3) .3
           (0 (0
        log log
            −

 0                                ? + ?                     if (?) { ? } else { ? }




                                                                                       − lo
                                 .3)
         −



                              g(0




                                                                                           g(0
                          − lo




                                                                                              .8)
 1
                     x + ?                          ···         if (? ≤ ?) { ? } else { ? }                         ···
                    .3)




 x
                 g(0
             − lo




           x + 1                         ···

Figure 1: The tree G of partial productions, connected by the expansion relation. The initial node is the
empty partial production ? of the non-terminal IntExpr. Each edge indicates the replacement of the
left-most incomplete sub-production by an instance of a production rule R. The edges are annotated with
the negative log probabilities, − log(pR ): because 0 ≤ pR ≤ 1, log(pR ) ≤ 0, so the weights − log(pR ) are
non-negative. A production is enclosed in a rectangle if it is complete.


productions ẽ1 , ẽ2 , . . . , ẽk . All of these new partial productions are inserted back into Q. If, on the
other hand, ẽ is already complete, it is emitted to be further processed by Search(ā, A, Π, φ , x). If π (ẽ) =
cost(ẽ) = − log(P(ẽ)), i.e. the priority function is equal to the cost of the partial production, then Q
forms the frontier maintained by Dijkstra’s algorithm.
    We begin analysing Algorithm 3 with the following invariant: Let Ec be the set of (complete) pro-
ductions emitted by Enumerate(G, N). Then, ∑ẽ∈Q∪Ec P(ẽ) = 1. We will now outline the proof of its
invariance. First, observe that, for all partial productions ẽ with at least one occurrence of ?,

                                                                   ∑            P(ẽ′ ) = P(ẽ).                                  (3)
                                                               ẽ′ s.t.ẽ→ẽ′

Informally, if each partial production ẽ is viewed as an event resulting from the PCFG, then the partial
productions ẽ′ obtained by a single application of the expansion relation encode a mutually exclusive
and exhaustive collection of sub-events of ẽ. We then have: (a) the base case: P(?) = 1, (b) inductive
case #1: whenever a complete production e is emitted from Q, the set Q ∪ Ec is left unchanged, (c) and
inductive case #2: whenever a partial production ẽ is further expanded into partial productions ẽ1 , ẽ2 ,
. . . , ẽk , the candidate invariant continues to hold because of Equation 3.
Theorem 2.1. If the priority function, π (ẽ) = cost(ẽ) = − log(P(ẽ)), then Enumerate(G, N) returns
some sequence σ containing all productions of N in G. Furthermore, the probability P(e) of productions
in σ is monotonically decreasing.

Proof. We begin by proving the second part of the claim. Consider a pair of partial productions, ẽ and
ẽ′ such that ẽ → ẽ′ . Then, P(ẽ) ≥ P(ẽ′ ). It therefore follows that the sequence of partial productions,
τ , dequeued by Enumerate(G, N) in line 3a has monotonically decreasing probability. Observe that the
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                                        7


                                                   Deduplicating priority queue

          Yes                                                                                     Indist.
 Emit!                Complete?                     ẽ1        ẽ2   ẽ3      ···
                                                                                                  Rewrite 2
                       No

                                                    Indist.
                  Partial evaluation                                       Expand ẽ1       {ẽ11 , ẽ12 , ẽ13 , . . .}
                                                    Rewrite 1

Figure 2: The operation of Enumerate(G, N) in Algorithm 3. We describe the partial evaluation and
indistinguishability-based optimizations, including production rewriting and queue deduplication, in
Section 2.5.


sequence σ of complete productions emitted by Enumerate(G, N) is a sub-sequence of τ , and therefore,
the probability of productions in σ monotonically decreases.
    Now, arbitrarily choose a complete production e ∈ EN . We will show that Enumerate(G, N) will
eventually emit e. Let phi be the highest probability of any production rule in G. Recall our require-
ment that for each rule R, pR < 1, and therefore, phi < 1 and log(phi ) < 0. Before processing e,
Enumerate(G, N) can only process those nodes which are at most log(P(e))/ log(phi ) steps away from
the root node ? of the search tree G . If there are N rules in the PCFG, then the out-degree of each
node is at most N, and it follows that there are only finitely many nodes which can be processed before
Enumerate(G, N) processes e. It follows that e is eventually emitted by the enumerator.

    Unfortunately, when the priority function is instantiated to emulate Dijkstra’s algorithm, enumeration
does not scale beyond a few hundred productions. The intuition may be found in the correctness proof
above: before emitting e, the enumerator must explore all partial productions with probability bigger
than P(e). The number of these productions rapidly grows with decreasing P(e), and furthermore, most
of the processed partial productions are “very incomplete”, i.e. containing many instances of ?, and
therefore many edges away from turning into complete productions. This suggests other graph search
algorithms, which we will now discuss.

Non-terminal horizons and A* search. When considering partial productions ẽ, we may speak of
two quantities: (a) the cost already paid, which we have defined as cost(ẽ) = − log(P(ẽ)), and (b) the
minimum cost yet to be paid, before ẽ turns into a complete production. We formalize this latter quantity
as the horizon, defined as:
                                  h(ẽ) = min ∗ cost(e f ) − cost(ẽ),                                 (4)
                                            e f s.t. ẽ→ e f

where e f ranges over all complete productions reachable from ẽ. Recall the intuition for the failure of
Dijkstra’s algorithm: before emitting e, we have to process every partial production with higher proba-
bility, and most such partial productions ẽ′ are themselves many steps away from complete productions.
Since the horizon encodes the distance from the partial production to its nearest completion, it is natural
to include it in the priority function π (ẽ). If we define π (ẽ) = cost(ẽ) + h(ẽ), then we obtain A* search.
     The important property of π (ẽ) is that it is admissible, i.e. that π (ẽ) is always less than the cost of
all complete productions descendant from ẽ). More formally, for all complete productions ec reachable
from ẽ,
                                            π (ẽ) = min∗ cost(ec ).                                          (5)
                                                     ec s.t.ẽ→ ec
8                                                           On Repair with Probabilistic Attribute Grammars


We then have the following well-known result of the A* algorithm:
Theorem 2.2. If π (ẽ) = cost(ẽ) + h(ẽ), then:
    1. The sequence of complete productions emitted by Enumerate(G, N), σ = e1 , e2 , e3 , . . . contains all
       productions in EN and has monotonically decreasing probability. (This is called the optimality
       property.)
    2. For all complete productions e, every complete optimal algorithm A′ (G, N) will, before producing
       e, visit all strictly less expensive nodes, ẽ, such that π (ẽ) < π (e) . (This is the property of optimal
       efficiency.)

Proof. First, we show that Enumerate(G, N) produces all complete productions e ∈ EN . Similar to The-
orem 2.1, we bound the number of nodes that can be processed in line 3a before processing e. Observe
that for all nodes, ẽ, π (ẽ) ≥ cost(ẽ), and for complete productions e, π (e) = cost(e). Therefore, all nodes
processed by Enumerate(G, N) before processing e are no more than log(P(e))/ log(phi ) steps from the
root of the search tree G , where, as before, phi < 1 is the highest probability appearing in the PCFG.
       We will now show that the productions emitted have monotonically decreasing probability. For this,
first observe that for each complete production e, and for each of its (necessarily incomplete) ancestors
ẽ′ , π (ẽ′ ) ≤ π (e). For the sake of contradiction, let there be some pair e1 , e2 of complete productions,
such that P(e1 ) < P(e2 ), but Enumerate(G, N) emits e1 before e2 . Both e1 and e2 are therefore reach-
able from the initial node ?. Consider the state of Q when e1 is dequeued from it. It has to be the case
that some ancestor ẽ′2 is present in Q. However, it follows that π (ẽ′2 ) ≤ π (e2 ) < π (e1 ), and therefore the
priority queue must have made a mistake in its ordering. It follows that the sequence of productions emit-
ted by Enumerate(G, N) has monotonically increasing costs, or equivalently, monotonically decreasing
probabilities.
       We will now prove the last part of the theorem. Assume otherwise, so for some algorithm A′ (G, N)
and some node ẽ such that such that π (ẽ) < π (e), A′ does not expand ẽ before producing e. We know
ẽ has some descendant e′ such that π (ẽ) = cost(e′ ) < π (e). Because the search space G is a tree, if A′
does not expand ẽ, it follows that it did not enumerate e′ before e, violating the assumption that A′ is a
complete optimal enumerator.

    Note that, in a certain sense, the second part of Theorem 2.2 says that this is the best possible enu-
meration algorithm among all algorithms that use the same priority function, because Enumerate(G, N)
does not expand any nodes ẽ′ such that π (ẽ′ ) > π (e). This also captures our intuition for the superiority
of this priority function over the simpler metric used by Dijkstra’s algorithm.

Computing the horizon, h(ẽ). It can be shown that the cost to be paid to complete ẽ is the sum of the
costs needed to expand each of its unexpanded nodes:

                                               h(ẽ) = ∑ h(?N ).                                              (6)
                                                      ?N ∈ẽ

Before starting the enumerator, we therefore compute the non-terminal horizons, h(?N ), for each non-
terminal symbol N. Observe that, by definition, this simply encodes the probability of the most likely
expansion, e ∈ EN :
                               h(?N ) = min cost(e) = − max log(P(e)).
                                            e∈EN               e∈EN

The values h(?N ) can be computed by the following fixpoint computation:
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                       9


   1. h0 (?N ) = min{− log(pR ) | Terminal rule R}.
   2. hi+1 (?N ) = min{hi (R) | Production rule R}, where the horizon of a production rule R is defined as
      hi (R) = − log(pR ) + ∑{hi (?N ′ ) | child non-terminal N ′ appearing in R}.

2.5 Optimizations
Eagerly discarding partial productions.       Given a single input variable a, consider the synthesis pred-
icate φ given by:
  if (a == 5) { x == 6 }
  else if (a == 7) { x == 9 }
  else { x == a }
During CEGIS, say the set of concrete input points, A = {2, 5, 7}. For this problem, Enumerate(G, N)
will consider partial productions such as

                                  ẽ = if (x < 6) { x } else { ? }.
                              V
Observe that the conjunction a∈A φ [x 7→ e] used in the CEGIS loop can only be evaluated for complete
productions e. However the partial production ẽ is already incorrect: for the input point a = 5, regardless
of the completion of ?, ẽ will evaluate to 5, and this fails the requirement that x == 6.
    This pattern of partial productions already failing requirements is particularly common with con-
ditionals and match statements. Our first optimization is therefore the partial evaluation box shown in
Figure 2. For each input point ā ∈ A, we partially evaluate the CEGIS predicate Π =⇒ φ [x 7→ ẽ]. If
the result is false, then we discard the partial production ẽ without processing, as we know that all its
descendants will fail the synthesis predicate. Otherwise, if it evaluates to true or unknown, then we
process ẽ as usual, and insert its neighbors back into the priority queue.

Extending the priority function with scores. We just observed that if a partial production fails the
synthesis predicate by partial evaluation, then it can be discarded without affecting correctness. The dual
heuristic optimization is to promote partial productions which definitely evaluate to true on some input
points. We do this by modifying the priority function:

                               π (ẽ) = cost(ẽ) + h(ẽ) + c × log(score(ẽ)),                          (7)

where score(ẽ) is the number of input points on which the partial production evaluates to true, and
c is a positive coefficient. Small positive values of c results in an enumerator which strictly follows
probabilistic enumeration, while large positive values of c results in the enumerator favoring partial
productions which already work on many points. While the use of this heuristic renders Theorem 2.2
inapplicable, we have observed improvements in performance as a result of this optimization.

Indistinguishability. Consider the partial production ẽ = if (x < 5) { x - x } else { ? }, and
focus on the sub-expression x - x. This expression is identically equal to 0, and it is therefore possi-
ble to simplify ẽ to if (x < 5) { 0 } else { ? }. If two expressions e and e′ are equivalent, and
P(e) > P(e′ ), then a desirable optimization is to never enumerate e′ . Observe that, if properly imple-
mented, this optimization produces exponential savings at each step of the search: if e and e′ are equiv-
alent, then, for example, it follows that both e + 3 and e′ + 3 are equivalent, and only one of them needs
to be enumerated to achieve completeness.
10                                                         On Repair with Probabilistic Attribute Grammars


     Indistinguishability [34] is a technique to mechanize this reasoning. Given a sequence of concrete
input points A = {ā1 , ā2 , . . . , ān }, a complete production e can be evaluated to produce a set of output
values Se = {x1 , x2 , . . . , xn }. During enumeration, if an expression e′ is encountered such that for some
previous expression e, Se = Se′ , then e′ is discarded as a potential expansion. The original expression e
can thus be regarded as the representative of the equivalence class of all expressions whose signature is
equal to Se .
     In this original formulation of indistinguishability-based pruning, the enumerator worked bottom-up,
rather than in the top-down style we consider in this paper. As a result, the enumerator only needs to
process complete productions, rather than the partial productions which populate Q in our setting.
     We have extended this optimization to work with partial expressions, and prune expressions in a
top-down enumerator. The idea is to replace the priority queue Q with a “deduplicating priority queue”,
with the additional feature that it removes duplicate elements from being dequeued. Such a queue can be
implemented as a combination of a traditional priority queue and a mutable set data structure commonly
available in standard language libraries. Next, we maintain a dictionary mapping all previously seen
signatures to the representatives of the respective equivalence classes. Every time we dequeue a partial
production ẽ from Q, we evaluate every complete sub-production esub on all input points ā ∈ A to obtain
its signature Ssub , and replace esub with the canonical representative. This forms the box labelled “Indist.
rewrite 1” in Figure 2.
     We also perform a second, fast indistinguishability rewrite after each partial production is expanded.
This is done by maintaining a map from previously seen expressions to their canonical representatives.
Consulting this map for every complete sub-production of the children, ẽ1 , ẽ2 , . . . , of the original produc-
tion ẽ is much faster than evaluating them on each concrete input point in A. There is some freedom in
choosing the placement of various optimizations in Figure 2: our motivation was that the priority queue
can get very large, and many elements enqueued into the queue will never be dequeued, and that it is
therefore wise to postpone as much processing as possible to when partial productions are extracted from
Q.


3     Term Grammars
In the previous section, we explained our synthesis algorithm using a PCFG as a black box. In this
section, we explain how the term grammars in our system are defined and extracted.
    We designed our grammars with the following goals in mind:
     • Flexibility. The system should allow the user to define and easily deploy a different grammar for
       each application or application domain.
     • Expressivity. The grammars should be able to express complex relations between expressions, in
       a more elaborate way than simply mapping each type of the target language to a set of production
       rules. This allows the user to constrain the space of synthesized programs to exclude redundant or
       irrelevant ones, thus improving the scalability of the synthesizer.
     • Automation. Apart from hand-coding the grammars, it should also be possible to automatically
       extract them from a corpus of programs, possibly taken from a specific application domain.
     To this end, we introduce Probabilistic Attribute Grammars, which address all of the above points:
     • A custom grammar is provided by the user along with the synthesis problem as a set of Scala
       source files (the grammar files), in which production rules are expressed as plain Scala functions.
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                   11


      Switching between grammars reduces to just including different files in compilation. It is also
      trivial to use any desired combination of such files. If the user does not want to manually provide
      a specific grammar for the task, they can always fall back to the system’s predefined grammar.
   • The nonterminal symbols of the grammar are not plain types, but instead are types contained in
     a wrapper class that annotates them with extra information. The wrapped types can represent a
     subtype of the underlying type, or some other condition under which specific rules are accessible,
     which would not be expressible if we used plain nonterminals as types. While processing the input
     grammar, our system will desugar away those wrappers to produce values of the underlying plain
     type.
     The approach of annotating types with attributes has already been introduced in [20], but there the
     attributes and their interpretation were predefined. Here we allow the user to provide their own
     wrapper classes.
     It is of course also possible to omit the wrappers completely and use plain Scala types as nonter-
     minals.
   • We provide a system to automatically extract grammar files from a corpus of PureScala programs.
    The grammar files undergo a series of preprocessing steps before generating a Probabilistic Attribute
Grammar, the exact form of which is conditional to the synthesis problem. The synthesizer itself is
oblivious to this procedure, which views the grammar just as a function from nonterminal symbols to
production rules.

3.1 Grammar files, rules and frequencies
As mentioned above, the user can provide a series of grammar files for compilation along with the
synthesis problem. The format of the files was designed with the aim to be readable and writable by a
human user, but also straightforward to extract from a corpus of programs.
    To illustrate the format though an example, let us look at a grammar file describing a set of simple
arbitrary precision integer programs:
@production(10)
def plus(a: BigInt, b: BigInt): BigInt = a + b

@production(5)
def minus(a: BigInt, b: BigInt): BigInt = a - b

@production(5)
def o: BigInt = BigInt(1)

@production(10)
def z: BigInt = BigInt(0)

@production(20)
def vBigInt: BigInt = variable[BigInt]
   A function annotated with @production is treated as a grammar production rule. A rule of the form
   def pFoo(a: T1, b: T2): T3 = foo(a, b)
   should be interpreted in CFG notation as
12                                                     On Repair with Probabilistic Attribute Grammars


    T3 ::= f oo(T 1, T 2)
    The annotation’s argument indicates the absolute frequency with which this rule is encountered. The
relative frequencies will be generated in the end of a processing procedure. In this example, though, they
can be computed straightforwardly from the absolute frequencies.
    An invocation of the built-in function variable[T], for some type T, indicates the absolute fre-
quency of generating any variable of type T. This built-in compensates for the fact that we do not know
the names of the variables accessible to the synthesizer a priori. When they become available, this
production will be instantiated to a concrete production for each variable of the correct type, with the
probability distributed equally among these variables. If, for example, we are synthesizing a function
with two parameters (x: BigInt, y: BigInt), the above grammar file would generate the following
grammar:

                               BigInt ::=    BigInt + BigInt   (p+ = 0.2)
                                        |    BigInt − BigInt   (p− = 0.1)
                                        |    0                 (p0 = 0.1)
                                        |    1                 (p1 = 0.2)
                                        |    x                 (px = 0.2)
                                        |    y                 (py = 0.2)

3.2 Generic productions
Generic grammar productions offer a concise way of representing operations on generic data-structures.
For instance, we could describe common operations on a generic list data-structure with a few user-
provided productions:
@production(..)
def single[A](a: A): List[A] = List(a, Nil)

@production(..)
def listInsert[A](a: A, l: List[A]): List[A] = List(a, l)

@production(..)
def listTail[A](l: List[A]): List[A] = l.tail

@production(..)
def listHead[A](l: List[A]): A = l.head

@production(..)
def listSize[A](l: List[A]): BigInt = l.size
    When looking for productions of a specific ground type, we instantiate generic productions that can
return that type, and introduce them as normal monomorphic productions. For example, if we are looking
for productions of List[BigInt], we consider the first three rules above instantiated with T 7→ BigInt,
and the forth with T 7→ List[BigInt]. The fifth rule is incompatible.
    Because the set of types is typically infinite, generic productions with a type variable absent from
the return type represent an infinite number of ground productions. This is for instance the case with
listSize.
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                       13


     Our enumeration procedure described above requires that each non-terminal symbol has a finite
number of ground productions. To solve this conflict, we abandon the theoretical completeness of the
instantiation by only considering a set of reasonable types T during instantiation. This set of types is ini-
tialized with all types returned by ground productions and then iteratively expanded by discovering new
return types of T -instantiations of generic productions. For example, starting with T = {Int}, running
one iteration yields T = {Int, List[Int]} as single[Int](..) returns a value of type List[Int].
     The number of discovery iterations we perform has a big practical impact on the number of final pro-
ductions, and thus on performance. On benchmarks with several generic data-structures, this discovery
is typically exponential. By under-approximating the size of the smallest expression of any discovered
type in T , we bound the search to reasonable types. We leave to future work how to better integrate the
instantiation of generic rules within the enumeration process.

3.3 Annotated nonterminals
Simple grammars like the one displayed above, where the nonterminal symbols are plain types, are not
expressive enough to handle all constraints that are obvious to a human programmer. For example, they
cannot express that an operand of an addition cannot be 0. When used as-is, such grammars generate a
large number of redundant programs, which prevent the synthesizer from scaling to larger program sizes.
    To amend this, we provide the programmer with a general mechanism to more accurately express the
restrictions of their grammar by enhancing their nonterminals with attributes in additional to the plain
Scala type. Nonterminals with the same type but different attributes are considered distinct, and can have
different production rules.
    As an example, suppose the user wants to more accurately specify the grammar of Section 3.1 to
exclude 0 from the operands of +, as well as the second operand of -. This can be captured with the
following attribute grammar:

                          BigInt ::= BigInt{BI}                          (p = 1.0)
                      BigInt{BI} | BigInt{NZ}                            (p = 0.8)
                                   | 0                                   (p = 0.2)
                     BigInt{NZ} | BigInt{NZ} + BigInt{NZ}                (p1 = 0.25)
                                   | BigInt{BI} − BigInt{NZ}             (p1 = 0.125)
                                   | x                                   (px = 0.5)
                                   | 1                                   (py = 0.125)

    The above grammar contains two annotated nonterminals, BigInt{NZ} and BigInt{BI}. The former
expresses nonzero integers and the second one the unrestricted integer type. Thus, generating BigInt
values reduces to generating values of the annotated type BigInt{BI}, which is captured in the first rule
of the grammar.
    In Scala source code, this is expressed by defining implicit Scala classes containing a field of the base
type, and annotating them with the @label annotation. The source file gets desugared by the system to
the above grammar.
@label implicit class NZ(val v: BigInt)

@label implicit class BI(val v: BigInt)

@production(10) def plus(a: NZ, b: NZ): NZ = a.v + b.v
14                                                     On Repair with Probabilistic Attribute Grammars



@production(5) def minus(a: BI, b: NZ): NZ = a.v - b.v

@production(5) def o: NZ = BigInt(1)

@production(10) def z: BI = BigInt(0)

@production(20) def vBigInt: NZ = variable[BigInt]

@production(40) def nz2Bi(nz: NZ): BI = nz.v

@production(1) def start(b: BI): BigInt = b.v


3.3.1   Built-in axiom system
In case the user does not want to manually implement a custom attribute grammar as above, they can
reside to a set of default built-in axioms described in [20]. In case of the default grammars, those
axioms are automatically applied to each combination of nonterminal and production rule. In case of a
manually provided grammar, the user has to guide the system by tagging the production rules with a set
of predefined tags. A couple of example tagged rules could be the following:
@production(10)
@tag("0")
def z: BigInt = BigInt(0)

@production(10)
@tag("commut")
def pFoo(b1: BigInt, b2: BigInt): BigInt = foo(b1, b2)
    @tag("0") indicates that this rule produces the constant 0 (e.g. it should be treated as neutral
element of addition), whereas @tag("commut") specifies foo as a commutative operation. These rules
will undergo a set of predetermined optimizations described in [20].

3.4 Extracting an attribute grammar form a corpus
Whereas manually specifying grammars is very useful for specific tasks and small DSLs, it would be
tedious to expect a user-provided grammar for generic programming tasks, where numerous types and
functions are in scope.
    To this end, we provide an automated system to extract a grammar from a corpus of Scala programs.
We provide two different grammar extractors, described in the following paragraphs.

3.4.1   Unconditional Frequency Extractor
The simpler Unconditional Frequency Extractor (UFE) uses plain Scala types as nonterminals, but auto-
matically tags them as in 3.3.1, so the built-in axioms can be instantiated on them. Each production rule
generated by the UFE corresponds to a specific kind of expression encountered in the corpus, whereas
the rule’s frequency reflects the number of occurrences of this kind. By kind of expression, we mean
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                   15


the expression type along with all information required to reconstruct the expression from its arguments
(except for variables, where the name is not preserved). More specifically,
   • For variables, only the variable type (the name does not get preserved). All variables of a specific
     type will all be summarized by an invocation to the variable built-in.
   • For literals, the literal itself (which takes 0 operands). E.g. 0, BigInt(42).
   • For function invocations, the invoked function along with its actual type parameters (which may
     be generic). E.g. foo[BigInt](?, ?), foo[T](?, ?), where by ? we denote a hole to be filled
     during synthesis.
   • For type constructors, the type constructor along with its actual type parameters. E.g. Cons[BigInt](?, ?),
     Nil[A]().
   • For every other expression, only the type of the AST of that expression, and if needed its type
     instantiation. E.g. ? + ?, Set[BigInt](?).
    Because the grammars generated by this extractor do not take into account the parent of the expres-
sion, we will call them depth-1 grammars.
    For example, a corpus containing only the expression (x * 2) would result in the following file:
@production(1)
@tag("const")
def pBigIntInfiniteIntegerLiteral0(): BigInt = BigInt(2)

@production(1)
@tag("times")
def pBigIntTimes(v0 : BigInt, v1 : BigInt): BigInt = v0 * v1

@production(1)
@tag("top")
def pBigIntVariable(): BigInt = variable[BigInt]


3.4.2   Conditional Frequency Extractor
The second, more sophisticated extractor, extracts the conditional probabilities of the occurrence of
each expression kind, given the expression’s relation with its parent. More specifically, along with each
expression, it stores a pair (par, pos), where par is the type of AST of the parent of the expression,
and pos the expression’s position in its parent’s operands. This pair is optional and omitted for a top-
level expression. For example, if the extractor encountered the expression (x * 2), it would store the
triples (? * ?, null, null), (<variable>, ? * ?, 0) and (2, ? * ?, 1). To express these
conditional probabilities in a grammar file, it uses annotated nonterminals as described in 3.3.
     Because these grammars express probabilities which are derived from an expression along with its
parent, we will call them depth-2 grammars.
     A corpus containing only the above expression would produce the following grammar file:
@label implicit class BigInt_TOPLEVEL(val v : BigInt)
@label implicit class BigInt_0_Times(val v : BigInt)
@label implicit class BigInt_1_Times(val v : BigInt)
16                                                      On Repair with Probabilistic Attribute Grammars


@production(1)
def pBigIntTimes(v0 : BigInt_0_Times, v1 : BigInt_1_Times): BigInt_TOPLEVEL =
  v0.v * v1.v
@production(1)
def pBigIntVariable(): BigInt_0_Times = variable[BigInt]
@production(1)
def pBigIntInfiniteIntegerLiteral(): BigInt_1_Times = BigInt(2)
@production(1)
def pBigIntStart(v0 : BigInt_TOPLEVEL): BigInt = v0.v


3.5 Biasing grammars for repair
The flexibility and automation of the system give us a great opportunity to exploit the local structure of
the program. Especially for program repair, we can ease the task of generating a reasonable patch for
an erroneous program by collecting information about how the user has chosen to program in the same
module.
    This is achieved as follows: before repair, we generate an additional grammar file from the file under
repair, and include it for compilation along with the general-purpose grammar file extracted from the cor-
pus. This way, we bias the synthesis process towards local definitions, without completely disregarding
the general programming model.


4     Experimental Results
To experimentally evaluate the above ideas, we integrated them into the Leon synthesis and repair frame-
work [18] The Probabilistic Enumeration (PE) of Section 2 is deployed as a closing deductive synthesis
rule in the synthesis framework, in place of Symbolic Term Exploration (STE) [20].
    For repair, we slightly modify Probabilistic Enumeration to generate terms similar to the erroneous
expression, in the spirit of [17]. This can be achieved by automatically modifying the grammar passed
to Enumeration, without any other changes to the algorithm. This rule is deployed along with plain PE
within the synthesis stage of the repair pipeline, after test generation and fault localization
    In our evaluation, we aimed to measure how well our algorithms perform in isolation, rather than
how well they integrate with the synthesis framework. This is straightforward in repair, as the erroneous
implementation already defines the high-level structure of the function under repair, and the closing rules
can usually be deployed alone, without instantiating any decomposition rules first.
    In the following tables, we compare the efficiency of synthesizing repairs for a set of erroneous
benchmarks taken from [20], along with a few new, more challenging ones.
    In total, we test 4 tool configurations:

     • Symbolic Term Exploration with built-in grammars and built-in axioms, i.e. the old version of
       Leon (STE)
     • Probabilistic Enumeration with built-in grammars and built-in axioms (PB)
     • Probabilistic Enumeration with depth-1 extracted grammars and built in axioms (PD1)
     • Probabilistic Enumeration with depth-2 grammars, without built-in axioms (PD2)
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                          17


    In both the latter cases, the grammars come from a combination of grammar files extracted from a
corpus and the program under repair. We do not use built-in axioms with depth-2 grammars, as they
are redundant to some degree and they would overcomplicate the grammar, while yielding diminishing
returns.
    The detailed results are given in 1. The first two columns of the table give an indication of the
complexity of the problem by displaying the total size of the program and the size of the solution (which
might not be generated from scratch, but rather as a variation of the erroneous expression). The final
four columns display the repair times for the four deployments of the tool described above. Repair times
exclude compilation, test generation, and verification of the solution.
    To summarize the results, the new enumerator is slightly faster for the built-in grammars, whereas
the depth-1 grammars are sometimes slightly slower, but manage to solve a couple more benchmarks.
Unfortunately, there is a relatively easy benchmark that depth-1 fails to solve. The depth-2 grammars,
though they show some promise (in the Compiler.semUntyped benchmark), they generally perform
badly. One reason for this behavior are the conflicts between annotated nonterminal symbols generated
from the general corpus with those from the file under repair. Both sources will generate annotated
non-terminals that express the same conditional probability, overloading the synthesizer with duplicated
work. This is a shortcoming we plan to address in the near future.


5    Related Work
5.1 Program synthesis
Program synthesis has been a challenge problem in computer science since its early days (see, for ex-
ample, [21]). With increasing computing power, and rapid improvements in the performance of SAT
and SMT solvers starting from the early 2000s, the problem of program synthesis has recently received
renewed attention. The seminal Sketch project [33] was the first to demonstrate the feasibility of using
modern constraint solving technology in synthesis tools, and used the popular counter-example guided
inductive synthesis (CEGIS) framework to solve synthesis problems [12].
    Syntax-guided synthesis (SyGuS) has emerged as a common formulation and interchange format in
which to express many program synthesis problems [4]. Our problem formulation within Leon shares
two important similarities with SyGuS:
    1. Multi-modal specifications, which can include any combination of input-output examples (such as
       “ f (2, 3) = 8”), logical constraints (such as “∀x, y, f (x, y) > x + y + 2”), and even partial implemen-
       tations (such as “∀x, y, x < y =⇒ f (x, y) = x + y + 3”).
    2. Expression grammars, or equivalently, a library of components [15], are used to syntactically
       constrain the space of programs. This is important both to make synthesis feasible for complicated
       specifications, and for when the results are to be used in specialized domains, such as assembly
       code for new computer architectures [25].
Of the various techniques to solve SyGuS problems, ESolver, which enumerates pairwise distinguishable
expressions [34], EUSolver, which combines indistinguishability-based enumeration with decision-tree
based condition inference [5], and the refutation-proof-based CVC4 solver [30] have broadly emerged as
the most efficient SyGuS solvers. Our present work may be viewed as an attempt to bias the enumerative
solver with statistical facts learned from a code corpus.
    We would like to highlight that program synthesis and code repair within Leon is a much more
challenging problem than synthesis within SyGuS and related systems: the main difficulties include the
18                                   On Repair with Probabilistic Attribute Grammars




     Operation                Sizes      STE    PB     PD1    PD2
                            Prog Sol
     Compiler.desugar        717    3     3.3   1.9     2.3    2.9
     Compiler.desugar        715    2     5.2   3.7     4.3    3.4
     Compiler.desugar        719    7     3.0   1.8     2.1    2.0
     Compiler.desugar        719    7     3.8   3.0     3.0    3.2
     Compiler.desugar        719 14       5.2   3.4     3.2    3.7
     Compiler.simplify       765    4     2.8   1.8     1.8    3.1
     Compiler.semUntyped     738    5                  16.8    5.1
     Heap.merge              382    3     6.0   4.9     5.1    5.2
     Heap.merge              382    1     2.8   2.0     2.0    2.2
     Heap.merge              382    3     5.7   4.7     5.1    5.3
     Heap.merge              382    9     4.4   3.6     3.4    3.7
     Heap.merge              384    5     5.1   6.4     5.2   15.6
     Heap.merge              382    2     4.2   2.6     2.7    2.9
     Heap.insert             345    8     3.0   2.8     2.9    2.9
     Heap.makeN              384    7     5.6   7.9     8.7    8.6
     List.pad                830    8     2.3   1.5     1.6    2.7
     List.++                 740    3     2.6   1.5     1.2    8.1
     List.:+                 772    1     3.0   1.1     1.2    1.9
     List.replace            774    6     3.3   1.7     1.7    1.7
     List.count              827    3     2.2   1.2     1.4    1.3
     List.find               827    2     2.5   1.7     1.6    1.7
     List.find               829    4     2.8   1.6     1.8    1.7
     List.find               830    4     2.7   1.7     1.9    1.7
     List.size               755    4     2.5   1.1
     List.sum                774    4     2.3   1.5     1.5    1.5
     List.-                  774    1     1.5   0.5     0.5    1.7
     List.drop               815    4     2.4   1.4     1.6    1.5
     List.drop               815    3     4.0   3.3    46.9    2.4
     List.&                  774    4                   3.1
     List.count              774    1                 170.7
     Numerical.power         225    5     2.9   1.1     1.2
     Numerical.moddiv        174    3     1.9   0.8     0.8    1.0
     MergeSort.split         284    5     3.6   2.3     2.5    8.4
     MergeSort.merge         286    7     3.3   2.3     2.5    2.2
     MergeSort.merge         286    3     5.9   4.8     5.2    5.0
     MergeSort.merge         284    5     3.3   2.4     2.3   13.7
     MergeSort.merge         286    1     2.3   1.6     1.7    1.7

                    Table 1: Benchmarks for repair
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                      19


rich type system and algebraic data types of Scala, and the synthesis of recursive functions. In this light,
our problem is most similar to Escher [1] and λ 2 [10]: the main differences are that Escher enumerates
programs bottom-up rather than top-down, and our use of PCFGs to improve the performance of the
enumeration algorithm.


5.2 Type-driven synthesis

One appealing approach to program synthesis is to phrase the problem as the type-inhabitation problem in
a sufficiently expressive type system. Examples of such systems include InSynth [13], and Synquid [26].
The Myth project [23, 11] extends the type system of the host language with refinement types corre-
sponding to input-output examples. It can therefore be viewed as an attempt to provide a type-theoretic
interpretation to Escher. The Synquid system [26] is an elegant extension of this idea, by encoding the
specification as part of the type of the required expression using the liquid type framework.
    Previous work on synthesis within Leon [18, 20] may also be viewed as being implicitly type-driven.
The path conditions and postcondition obtained after each invocation of the deduction rules can be
rephrased as additional typing constraints on the expression being synthesized. As discussed in Sec-
tion 2, the present PCFG-based enumeration is intended as a drop-in substitute for the symbolic term
exploration rule previously used by Leon.


5.3 Statistical analysis of code corpora

With increasing availability of large open-source code repositories such as GitHub and Bitbucket, the
statistical analysis of code corpora has become an exciting research problem. Code repositories have
been used to learn coding idioms [3], to automatically suggest names for program elements [2], and
to deobfuscate JavaScript code [28]. Our paper is an attempt to apply similar techniques to accelerate
program synthesis.
     The program completion tool Slang [29] uses n-grams and recurrent neural networks to predict miss-
ing API calls in code snippets. There are two main aspects which distinguish our work from Slang: (a) the
presence of hard correctness requirements in Leon in the form of pre-/post-conditions, and (b) program
synthesis in Leon is fundamentally about synthesizing expressions rather than API call sequences, and
prediction systems such as n-grams are insufficient to create the nested recursive structure inherent in
the output we produce. The DeepCoder tool [6] uses a recurrent neural network (RNN) to predict the
presence of elements in the program being synthesized. The output of this neural network is then used
to guide a more exhaustive search over the space of possible programs. In this sense, DeepCoder is sim-
ilar to the PCFG-guided enumeration of Leon, and the use of neural networks to accelerate the program
synthesis problem is an intriguing direction for future research.
     Probabilistic context-free grammars (PCFGs) are a classical extension of context-free grammars [16].
They may be used both to model ambiguity (for applications in natural language processing), and to
model probability distributions over the generated language, which motivates our application in acceler-
ating code synthesis. The more recent model of probabilistic higher-order grammars (PHOGs) [7, 27]
extends PCFGs by allowing the expansion probabilities of a non-terminal node to depend on attributes
such as node siblings and DFS-predecessors. Experiments indicate that the PHOG model is significantly
better at predicting elements of JavaScript programs than PCFGs. Extending the probabilistic model of
our paper to use PHOGs instead of PCFGs is an immediate area of future work.
20                                                       On Repair with Probabilistic Attribute Grammars


5.4 Search algorithms
One of the main technical insights of this paper is to phrase syntax-guided program synthesis as an
instance of graph search. In this space, A* [14] is a classical algorithm used for path finding and graph
traversal. As described in Section 2, A* orders the queue of still-unexplored nodes by their priority
values, f (n) = g(n) + h(n), where g(n) is the cost required to reach the node n, and the heuristic function
h(n) is the estimated cost from n to the target node. The historically older Dijkstra’s algorithm for
shortest paths through graphs is a special case, where the heuristic function h(n) is identically equal to 0.
    Recall that the graph of partial expansions forms a tree: in this setting, if the cost function h(n) is
admissible, i.e. that h(n) ≤ h̃(n), where h̃(n) is the actual cost of the shortest path from n to the target
node, then A* discovers the shortest path to the target node (optimality). The second important property
of A* is that of optimal efficiency: of all algorithms using the same heuristic function, A* explores the
fewest nodes to reach the target. In the setting of this paper, optimality implies discovering the expansion
with highest probability. By extending h(n) to include the number of satisfied examples, we have relaxed
optimality in favour of empirical performance improvements.
    A* is simply the best known of a large family of search algorithms (see chapters 3 and 4 of [32]),
including iterative deepening A* (IDA*, [19]), simplified memory-bounded A* (SMA*, [31]), fringe
search [8], beam search, swarm search, and various instantiations of genetic algorithms [22]. Extending
the techniques of this paper to these algorithms is an exciting direction of future work.


6    Conclusion + Future Work
In this paper, we present a technique to use statistical information extracted from code corpora, encoded
as probabilistic attribute grammars, to guide program synthesis techniques. The method is based on
rephrasing expression enumeration as graph search, and applying classical techniques such as A* to
solve these problems. We implemented the algorithm in the Leon synthesis and verification system, and
obtained a much more robust and scalable synthesizer in comparison to the previous implementation.
Our end goal is a predictable one-touch program synthesizer in a rich programming environment such
as Scala: there are several exciting directions of future work, such as investigating other search methods
including swarm search and genetic algorithms, incorporating richer models of statistics such as prob-
abilistic higher-order grammars (PHOGS) [7], and combining type- and syntax-driven and statistical
techniques into a highly expressive and performant program synthesizer.


References
 [1] Aws Albarghouthi, Sumit Gulwani & Zachary Kincaid (2013):           Recursive Program Synthe-
     sis.  In Natasha Sharyngina & Helmut Veith, editors: 25th International Conference on Com-
     puter Aided Verification, Springer, pp. 934–950, doi:10.1007/978-3-642-39799-8.    Available at
     http://dx.doi.org/10.1007/978-3-642-39799-8_67.
 [2] Miltiadis Allamanis, Earl Barr, Christian Bird & Charles Sutton (2015): Suggesting Accurate
     Method and Class Names. In: Proceedings of the 10th Joint Meeting on Foundations of Soft-
     ware Engineering, ESEC/FSE 2015, ACM, pp. 38–49, doi:10.1145/2786805.2786849. Available at
     http://doi.acm.org/10.1145/2786805.2786849.
 [3] Miltiadis Allamanis & Charles Sutton (2014): Mining Idioms from Source Code. In: Pro-
     ceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                         21


     Engineering, FSE 2014, ACM, pp. 472–483, doi:10.1145/2635868.2635901.                       Available at
     http://doi.acm.org/10.1145/2635868.2635901.
 [4] Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo Martin, Mukund Raghothaman, Sanjit Seshia, Rishabh
     Singh, Armando Solar-Lezama, Emina Torlak & Abhishek Udupa (2013): Syntax-guided synthesis. In: 2013
     Formal Methods in Computer-Aided Design, pp. 1–8, doi:10.1109/FMCAD.2013.6679385.
 [5] Rajeev Alur, Arjun Radhakrishna & Abhishek Udupa (2017): Scaling Enumerative Program Synthe-
     sis via Divide and Conquer. In Axel Legay & Tiziana Margaria, editors: 23rd International Confer-
     ence on Tools and Algorithms for the Construction and Analysis of Systems, Springer, pp. 319–336,
     doi:10.1007/978-3-662-54577-5. Available at http://dx.doi.org/10.1007/978-3-662-54577-5.
 [6] Matej Balog, Alexander Gaunt, Marc Brockschmidt, Sebastian Nowozin & Daniel Tarlow (2017): Deep-
     Coder: Learning to Write Programs. In: International Conference on Learning Representations,
     abs/1611.01989. Available at http://arxiv.org/abs/1611.01989.
 [7] Pavol Bielik, Veselin Raychev & Martin Vechev (2016): PHOG: Probabilistic Model for Code. In Maria Flo-
     rina Balcan & Kilian Q. Weinberger, editors: Proceedings of The 33rd International Conference on Ma-
     chine Learning, Proceedings of Machine Learning Research 48, PMLR, pp. 2933–2942. Available at
     http://proceedings.mlr.press/v48/bielik16.html.
 [8] Yngvi Björnsson, Markus Enzenberger, Robert Holte & Jonathan Schaeffer (2005): Fringe Search: Beat-
     ing A* at Pathfinding on Game Maps. In: Proceedings of the 2005 IEEE Symposium on Computational
     Intelligence and Games. Available at http://csapps.essex.ac.uk/cig/2005/papers/p1039.pdf.
 [9] Régis Blanc, Viktor Kuncak, Etienne Kneuss & Philippe Suter (2013): An Overview of the Leon
     Verification System: Verification by Translation to Recursive Functions. In: Proceedings of the 4th
     Workshop on Scala, SCALA ’13, ACM, pp. 1:1–1:10, doi:10.1145/2489837.2489838. Available at
     http://doi.acm.org/10.1145/2489837.2489838.
[10] John Feser, Swarat Chaudhuri & Isil Dillig (2015): Synthesizing Data Structure Transformations from Input-
     output Examples. In: Proceedings of the 36th ACM SIGPLAN Conference on Programming Language
     Design and Implementation, PLDI ’15, ACM, pp. 229–239, doi:10.1145/2737924.2737977. Available at
     http://doi.acm.org/10.1145/2737924.2737977.
[11] Jonathan Frankle, Peter-Michael Osera, David Walker & Steve Zdancewic (2016): Example-directed
     Synthesis: A Type-theoretic Interpretation. In: Proceedings of the 43rd Annual ACM SIGPLAN-
     SIGACT Symposium on Principles of Programming Languages, POPL ’16, ACM, pp. 802–815,
     doi:10.1145/2837614.2837629. Available at http://doi.acm.org/10.1145/2837614.2837629.
[12] Sumit Gulwani, Susmit Jha, Ashish Tiwari & Ramarathnam Venkatesan (2011): Synthesis of Loop-
     free Programs. In: Proceedings of the 32nd ACM SIGPLAN Conference on Programming Language
     Design and Implementation, PLDI ’11, ACM, pp. 62–73, doi:10.1145/1993498.1993506. Available at
     http://doi.acm.org/10.1145/1993498.1993506.
[13] Tihomir Gvero, Viktor Kuncak, Ivan Kuraj & Ruzica Piskac (2013): Complete Completion Using Types
     and Weights. In: Proceedings of the 34th ACM SIGPLAN Conference on Programming Language De-
     sign and Implementation, PLDI 2013, ACM, pp. 27–38, doi:10.1145/2491956.2462192. Available at
     http://doi.acm.org/10.1145/2491956.2462192.
[14] Peter Hart, Nils Nilsson & Bertram Raphael (1968): A formal basis for the heuristic determination of mini-
     mum cost paths. IEEE Transactions on Systems, Science, and Cybernetics SSC-4(2), pp. 100–107.
[15] Susmit Jha, Sumit Gulwani, Sanjit Seshia & Ashish Tiwari (2010): Oracle-guided Component-based
     Program Synthesis. In: Proceedings of the 32nd ACM / IEEE International Conference on Software
     Engineering - Volume 1, ICSE ’10, ACM, pp. 215–224, doi:10.1145/1806799.1806833. Available at
     http://doi.acm.org/10.1145/1806799.1806833.
[16] Daniel Jurafsky & James Martin (2008): Speech and Language Processing, 2nd edition. Prentice Hall. See
     chapter 14 on statistical parsing.
22                                                       On Repair with Probabilistic Attribute Grammars


[17] Etienne Kneuss, Manos Koukoutos & Viktor Kuncak (2015): Deductive Program Repair.               In
     Daniel Kroening & Corina Păsăreanu, editors: Proceedings of the 27th International Conference on
     Computer Aided Verification, Springer, pp. 217–233, doi:10.1007/978-3-319-21668-3. Available at
     http://dx.doi.org/10.1007/978-3-319-21668-3_13.
[18] Etienne Kneuss, Ivan Kuraj, Viktor Kuncak & Philippe Suter (2013): Synthesis Modulo Recursive Functions.
     In: Proceedings of the 2013 ACM SIGPLAN International Conference on Object Oriented Programming
     Systems Languages and Applications, OOPSLA 2013, ACM, pp. 407–426, doi:10.1145/2509136.2509555.
     Available at http://doi.acm.org/10.1145/2509136.2509555.
[19] Richard  Korf   (1985):        Depth-first    iterative-deepening.          Artificial   Intelligence
     27(1),  pp. 97–109,     doi:http://dx.doi.org/10.1016/0004-3702(85)90084-0.            Available at
     http://www.sciencedirect.com/science/article/pii/0004370285900840.
[20] Manos Koukoutos, Etienne Kneuss & Viktor Kuncak (2016): An Update on Deductive Synthesis and Re-
     pair in the Leon Tool. In: Proceedings Fifth Workshop on Synthesis, SYNT@CAV 2016, pp. 100–111,
     doi:10.4204/EPTCS.229.9. Available at https://doi.org/10.4204/EPTCS.229.9.
[21] Zohar Manna & Richard Waldinger (1971): Toward Automatic Program Synthesis.    Com-
     munications of the ACM 14(3), pp. 151–165, doi:10.1145/362566.362568.   Available at
     http://doi.acm.org/10.1145/362566.362568.
[22] Melanie Mitchell (1998): An Introduction to Genetic Algorithms. MIT Press.
[23] Peter-Michael Osera & Steve Zdancewic (2015):  Type-and-example-directed Program Synthe-
     sis.    In: Proceedings of the 36th ACM SIGPLAN Conference on Programming Language
     Design and Implementation, ACM, pp. 619–630, doi:10.1145/2737924.2738007.    Available at
     http://doi.acm.org/10.1145/2737924.2738007.
[24] Yu Pei, Carlo A. Furia, Martı́n Nordio & Bertrand Meyer (2015): Automated Program Repair in an Integrated
     Development Environment. In: 37th IEEE/ACM International Conference on Software Engineering, ICSE
     2015, Florence, Italy, May 16-24, 2015, Volume 2, pp. 681–684, doi:10.1109/ICSE.2015.222. Available at
     https://doi.org/10.1109/ICSE.2015.222.
[25] Phitchaya Mangpo Phothilimthana, Tikhon Jelvis, Rohin Shah, Nishant Totla, Sarah Chasins &
     Rastislav Bodik (2014): Chlorophyll: Synthesis-aided Compiler for Low-power Spatial Architec-
     tures. In: Proceedings of the 35th ACM SIGPLAN Conference on Programming Language De-
     sign and Implementation, PLDI ’14, ACM, pp. 396–407, doi:10.1145/2594291.2594339. Available at
     http://doi.acm.org/10.1145/2594291.2594339.
[26] Nadia Polikarpova, Ivan Kuraj & Armando Solar-Lezama (2016): Program Synthesis from Polymorphic
     Refinement Types. In: Proceedings of the 37th ACM SIGPLAN Conference on Programming Language
     Design and Implementation, PLDI ’16, ACM, pp. 522–538, doi:10.1145/2908080.2908093. Available at
     http://doi.acm.org/10.1145/2908080.2908093.
[27] Veselin Raychev, Pavol Bielik & Martin Vechev (2016): Probabilistic Model for Code with Decision Trees.
     In: Proceedings of the 2016 ACM SIGPLAN International Conference on Object-Oriented Programming,
     Systems, Languages, and Applications, OOPSLA 2016, ACM, pp. 731–747, doi:10.1145/2983990.2984041.
     Available at http://doi.acm.org/10.1145/2983990.2984041.
[28] Veselin Raychev, Martin Vechev & Andreas Krause (2015): Predicting Program Properties from ”Big
     Code”. In: Proceedings of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     Programming Languages, POPL 2015, ACM, pp. 111–124, doi:10.1145/2676726.2677009. Available at
     http://doi.acm.org/10.1145/2676726.2677009.
[29] Veselin Raychev, Martin Vechev & Eran Yahav (2014): Code Completion with Statistical Language
     Models. In: Proceedings of the 35th ACM SIGPLAN Conference on Programming Language De-
     sign and Implementation, PLDI ’14, ACM, pp. 419–428, doi:10.1145/2594291.2594321. Available at
     http://doi.acm.org/10.1145/2594291.2594321.
M. Koukoutos, M. Raghothaman, E. Kneuss & V. Kuncak                                                       23


[30] Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli & Clark Barrett (2015): Counterexample-
     Guided Quantifier Instantiation for Synthesis in SMT.           In Daniel Kroening & Corina Păsăreanu,
     editors: 27th International Conference on Computer Aided Verification, Springer, pp. 198–216,
     doi:10.1007/978-3-319-21668-3. Available at http://dx.doi.org/10.1007/978-3-319-21668-3_12.
[31] Stuart Russell (1992): Efficient Memory-bounded Search Methods. In: Proceedings of the 10th Euro-
     pean Conference on Artificial Intelligence, ECAI ’92, John Wiley & Sons, Inc., pp. 1–5. Available at
     http://dl.acm.org/citation.cfm?id=145448.145476.
[32] Stuart Russell & Peter Norvig (2009): Artificial Intelligence: A Modern Approach, 3rd edition. Pearson.
[33] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia & Vijay Saraswat (2006): Combi-
     natorial Sketching for Finite Programs. In: Proceedings of the 12th International Conference on Archi-
     tectural Support for Programming Languages and Operating Systems, ASPLOS XII, ACM, pp. 404–415,
     doi:10.1145/1168857.1168907. Available at http://doi.acm.org/10.1145/1168857.1168907.
[34] Abhishek Udupa, Arun Raghavan, Jyotirmoy Deshmukh, Sela Mador-Haim, Milo Martin & Rajeev Alur
     (2013): TRANSIT: Specifying Protocols with Concolic Snippets. In: Proceedings of the 34th ACM SIG-
     PLAN Conference on Programming Language Design and Implementation, PLDI ’13, ACM, pp. 287–296,
     doi:10.1145/2491956.2462174. Available at http://doi.acm.org/10.1145/2491956.2462174.
