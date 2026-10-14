                                        Journal of Automated Reasoning manuscript No.
                                        (will be inserted by the editor)




                                        A Framework for the Verification of Certifying
                                        Computations

                                        Eyad Alkassar · Sascha Böhme ·
                                        Kurt Mehlhorn · Christine Rizkallah




                                        the date of receipt and acceptance should be inserted later
arXiv:1301.7462v1 [cs.LO] 30 Jan 2013




                                        Abstract Formal verification of complex algorithms is challenging. Verifying their
                                        implementations goes beyond the state of the art of current automatic verification
                                        tools and usually involves intricate mathematical theorems. Certifying algorithms
                                        compute in addition to each output a witness certifying that the output is correct.
                                        A checker for such a witness is usually much simpler than the original algorithm –
                                        yet it is all the user has to trust. The verification of checkers is feasible with current
                                        tools and leads to computations that can be completely trusted. We describe a
                                        framework to seamlessly verify certifying computations. We use the automatic
                                        verifier VCC for establishing the correctness of the checker and the interactive
                                        theorem prover Isabelle/HOL for high-level mathematical properties of algorithms.
                                        We demonstrate the effectiveness of our approach by presenting the verification of
                                        typical examples of the industrial-level and widespread algorithmic library LEDA.


                                        1 Introduction

                                        One of the most prominent and costly problems in software engineering is cor-
                                        rectness of software. In this article, we are concerned with software for difficult
                                        algorithmic problems, e.g., in the domain of graphs. The algorithms for such prob-
                                        lems are complex; formal verification of the resulting programs is not tractable,
                                        which explains why few graph algorithms have been verified. We show how to
                                        obtain formal instance correctness, i.e., formal proofs that outputs for particular
                                        inputs are correct. We do so by combining the concept of certifying algorithms
                                        with methods for code verification and theorem proving.
                                            A certifying algorithm [6, 36, 23] produces with each output a certificate or witness
                                        that the particular output is correct. The accompanying checker for a certifying

                                        E. Alkassar
                                        Fachbereich Informatik, Universität des Saarlandes, Germany
                                        S. Böhme
                                        Institut für Informatik, Technische Universität München, Germany
                                        K. Mehlhorn · C. Rizkallah
                                        Max-Planck-Institut für Informatik, Saarbrücken, Germany
2                                         E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah



                                       Program for
                             x      IO-behavior (ϕ, ψ)       y




                                                                       accept y
                         Certifying                x
                        program for                      Checker C
               x                               y
                     IO-behavior (ϕ, ψ)
                                              w                         reject

Fig. 1: The top figure shows the I/O behavior of a conventional program for IO-
behavior (ϕ, ψ ). The user feeds an input x satisfying ϕ(x) to the program, and
the program returns an output y satisfying ψ (x, y ). A certifying algorithm for IO-
behavior (ϕ, ψ ) computes y and a witness w. The checker C accepts the triple
(x, y, w) if and only if w is a valid witness for the postcondition ψ (x, y ), i.e., it
proves ψ (x, y ).


algorithm with input x, output y , and witness w takes as input the triple (x, y, w)
and accepts the triple if w proves that y is a correct output for input x. Otherwise,
the checker rejects the output or witness as buggy1 .
    Figure 1 contrasts a standard algorithm with a certifying algorithm for IO-
behavior (ϕ, ψ ). An algorithm for IO-behavior (ϕ, ψ ) receives an input x satisfying
a precondition ϕ(x) and is supposed to deliver an output y satisfying the postcon-
dition ψ (x, y ). We call such a y a correct output. If the input does not satisfy the
precondition, the result of the computation is unspecified. A user of a standard
algorithm has, in general, no means of knowing that y is a correct output and has
not been compromised by a bug. In contrast, if the accompanying checker of a
certifying algorithm accepts, the user may proceed with the complete confidence
that output y has not been compromised by a bug. If the checker rejects, either y
is incorrect or w is not a proof of the correctness of y .
    We illustrate the concept of certifying algorithms with an example. The great-
est common divisor of two nonnegative integers a and b, not both zero, is the
largest integer g that divides a and b. We write g = gcd (a, b). The extended Eu-
clidean algorithm is a certifying algorithm for greatest common divisor. In addition
to the output g = gcd(a, b), it also computes as a witness2 integers s and t such
that g = s·a + t·b. The checker checks that g divides a and b and that g = s·a + t·b.
Why does this prove that g is the greatest common divisor of a and b? Consider
any integer d that divides a and b. Then g = s · a + t · b = (s · (a/d) + t · (b/d)) · d,
and hence, d divides g .
    Certifying algorithms are a key design principle of the algorithmic library
LEDA [24]: Checkers are an integral part of the library and may (optionally) be
invoked after every execution of a LEDA algorithm. The adoption of the principle
 1 Throughout the paper, we say the checker accepts if the checker returns True; otherwise,

we say it rejects.
 2 It is known that such integers s and t always exist.
A Framework for the Verification of Certifying Computations                            3


greatly improved the reliability of the library. However, how can one be sure that
the checker programs are correct? The third author used to answer: “Checkers are
simple programs with little algorithmic complexity. Hence, one may assume that
their implementations are correct.” We give a better answer in this paper.
    We take the certifying-algorithms approach a step further by developing a
methodology to verify the checkers. We demonstrate it on three examples: the
connectivity of graphs, single-source shortest paths in graphs with nonnegative
edge weights, and maximum cardinality matching in graphs. The latter is one of
the more complex algorithms in LEDA. The description of the algorithm and its
implementation in [24] comprises 15 pages. In contrast, the checker fits on one
page. Our formalization effort has revealed that the checker program in LEDA is
incorrect in that it does not check that the matching of a graph is a subset of the
edges of the graph (see Section 4.3 for a definition of matching).
    We introduce our methodology in Section 2 and give detailed case studies in
Section 4 before evaluating our approach and the obtained results in Section 5.
In Section 3, we survey the verification tools VCC and Isabelle/HOL. Section 6
discusses related work, and Section 7 offers conclusions. The companion web page
http://www21.in.tum.de/~ boehmes/certifying_computations.html contains addi-
tional material, in particular, the program listings including VCC annotations and
the Isabelle/HOL proofs.
    This article is a revised and extended version of a paper published by the
same authors at CAV 2011 [1]. We have added two case studies to underline
the feasibility and elegance of our approach. Moreover, we have strengthened and
simplified our approach. We now prove the total correctness of the checkers instead
of only partial correctness. Furthermore, we establish that the checker accepts a
triple (x, y, w) if and only if w is a valid witness for output y . Previously, we only
proved the if direction. The simplification results from having only one kind of
specification in VCC instead of two. Furthermore, a new version of VCC allows
for shorter specifications and proofs.


2 Outline of Methodology

We consider algorithms that take an input from a set X and produce an output in
a set Y and a witness in a set W . The input x ∈ X is supposed to satisfy a precon-
dition ϕ(x), and the input together with the output y ∈ Y is supposed to satisfy
a postcondition ψ (x, y ). A witness predicate for a specification with precondition ϕ
and postcondition ψ is a predicate W ⊆ X × Y × W , where W is a set of witnesses
with the following witness property :

                            ϕ(x) ∧ W (x, y, w) −→ ψ (x, y ).                         (1)
In contrast to algorithms that work on abstract sets X , Y , and W , the implement-
ing programs operate on concrete representations of abstract objects. We use X ,
Y , and W for the set of representations of objects in X , Y , and W , respectively,
and assume the mappings iX : X → X , iY : Y → Y , and iW : W → W .
    We illustrate these definitions through the example from the introduction. In
the case of greatest common divisors, X and W are the set of pairs of integers, and
Y is the set of integers. For input (a, b), output g and witness (s, t), the precondition
4                                             E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


ϕ((a, b)) states that the inputs a and b are nonnegative integers and that at least
one of them is not zero. The postcondition ψ ((a, b), g ) states that g = gcd (a, b). The
witness predicate W ((a, b), g, (s, t)) states that g = sa + tb and that g divides a and
b. A typical representation of integers in implementations is via bitstrings. Hence,
X and W are each the set of pairs of bit strings, and Y is the set of bit strings. The
mappings iX , iY , and iW map (pairs of) bit strings to the corresponding (pairs
of) integers.
    The checker program C receives a triple (x, y, w) and is supposed to check
whether it fulfills the witness property. More precisely, let x = iX (x), y = iY (y),
and w = iW (w). If ¬ϕ(x), C may do anything (run forever or halt with an arbitrary
output). If ϕ(x), C must halt and either accept or reject. It is required to accept
if W (x, y, w) holds and is required to reject otherwise.

Checker Correctness: We need to prove that C checks the witness predicate, as-
   suming that the precondition3 holds, i.e., on input (x, y, w) and with x = iX (x),
   y = iY (y ), and w = iW (w):
    1. If ϕ(x), C halts.
    2. If ϕ(x) and W (x, y, w), C accepts (x, y, w), and if ϕ(x) and ¬W (x, y, w), C
       rejects the triple.
Witness Property: We need to prove implication (1).

        In our running example, the witness property is

          a ≥ 0 ∧ b ≥ 0 ∧ a + b > 0 ∧ g|a ∧ g|b ∧ g = a · s + b · t =⇒ g = gcd (a, b).

Here a, b, g , s and t are assumed to be nonnegative integers.

Theorem 1 Assume that the proof obligations are discharged. Let (x, y, w) ∈ X × Y ×
W and let x = iX (x), y = iY (y), and w = iW (w).
    If C accepts a triple (x, y, w), ϕ(x) −→ ψ (x, y ) by a formal proof. If C rejects a
triple (x, y, w), ¬ϕ(x) ∨ ¬W (x, y, w) by a formal proof.

Proof If C accepts (x, y, w), we have ϕ(x) −→ W (x, y, w) by the correctness proof
of C . Then by (1) we have a formal proof for ϕ(x) −→ ψ (x, y ). Conversely, if C
rejects the triple, the correctness proof of C establishes ¬ϕ(x) ∨ ¬W (x, y, w). ⊓
                                                                                 ⊔

    We next discuss how we fulfill the proof obligations in a comprehensive and effi-
cient framework, see Figure 2. Comprehensive means that the final proof formally
combines (as much as possible at the syntactic level) the correctness arguments
for all levels (implementation, abstraction, and mathematical theory). Efficient
means using the right tool for the right task. For example, applying a general
theorem prover to verify imperative code would involve a lot of language-specific
overhead and lead to less automation; similarly, a specialized code verifier is of-
ten not powerful enough to cover nontrivial mathematical properties. The goals
of comprehensiveness and efficiency seem to be conflicting because different tools
usually come with different languages, axiomatization sets, etc. Our solution is to
use second-order logic as a common interface language.
    LEDA is written in C++ [24]. Our aim is to verify code which is as close as
possible to the original implementation; by this, we demonstrate the feasibility of
    3   We stress that the checker has the same precondition as the algorithm.
A Framework for the Verification of Certifying Computations                                            5


                                         Witness property: ϕ(x) ∧ W(x, y, w) −→ ψ(x, y)
 Isabelle/HOL




                                  ϕ⊆X             W ⊆ X ×Y ×W                             ψ ⊆ X ×Y


                                                            VCC-Isabelle translation
                Specification




                                  ϕ⊆X             W ⊆ X ×Y ×W                             ψ ⊆ X ×Y

                                                  Checker correctness:
                                                  if ϕ(iX (x)), C halts and outputs ACCEPT or REJECT
                                                  if ϕ(iX (x)), C accepts (x, y, w) if and only if
  VCC




                                                  W(iX (x), iY (y), iW (w))
                 Code




                                    the checker
                                    program C




                                Fig. 2: Verification Framework and Proof Obligations.


verifying already established libraries written in imperative languages such as C.
Thus, we verify code with VCC [14], an automatic code verifier for full C. Verifying
the C++ implementations remains open. Our choosingVCC is motivated by the
maturity of the tool and the provision of an assertion language that is rich enough
for our requirements. In the Verisoft XT project [38], VCC was successfully used
to verify tens of thousands of lines of C code. The assertion language offers ghost
code and ghost types such as maps and unbounded integers. This gives enough
expressiveness to quantify over graphs, labelings, etc., and simplifies the translation
to other proof systems. For verifying the mathematical part, we use Isabelle/HOL,
a higher-order-logic interactive theorem prover [26], because of the large amount
of already formalized mathematics, its descriptive proof format, and its various
automatic proof methods and tools. In Section 3, we review both systems. Figure 2
shows the workflow for verifying checkers.

Checker Verification: The starting point is the checker code written in C. Using
   VCC, we annotate the functions and data structures such that the witness
   predicate W can be established as the postcondition of the checker function.
   We define the witness predicate and the pre- and postcondition as well as the
   mappings iX , iY , and iW as pure mathematical objects using VCC ghost types
   and ghost functions.
Export to Isabelle/HOL: Establishing the witness property involves, in general,
   mathematical reasoning beyond what is conveniently done in VCC. We there-
   fore translate the precondition, witness predicate, postcondition, and the ab-
   stract representations of the input, output, and witness from VCC to Is-
   abelle/HOL. Since we formulated them as pure mathematical objects in VCC,
   this translation is purely syntactical and does not involve any VCC specifics.
   The translation could easily be automated.
6                                       E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


Witness Property: We prove the witness property using Isabelle/HOL. It is conve-
   nient to formulate this theorem on yet a higher level of abstraction and provide
   linking proofs to connect the exported VCC predicates with their abstracted
   counterparts.

     We stress that the overall correctness theorem, i.e., the witness property, can
be formulated in VCC; this is important for usability. The user of a verified checker
only has to look at its VCC specification; the fact that we outsource the proof of the
witness property to Isabelle/HOL is of no concern to the user. We formulate the
witness property as an axiom in VCC. This is sound since we restrict the language
for describing the witness property to second-order logic, which guarantees that
we can express it equivalently in Isabelle’s higher-order logic (cf. Section 3). More
precisely, since the VCC formulation of the witness property is valid if and only
if its translation to Isabelle is valid, and since Isabelle is consistent, and hence,
only valid statements can be proven, it is sound to add the witness property as an
axiom to VCC.
     The reader may wonder why we do not formally prove the existence of a wit-
ness:
                        ∀x y. ϕ(x) ∧ ψ (x, y ) −→ ∃w. W (x, y, w).

The existence of a witness is part of the correctness argument of the solution
algorithm (e.g., the shortest-path algorithm, the maximum-matching algorithm).
As previously mentioned, we do not verify the solution algorithms. Rather, the
execution of the solution algorithm establishes the existence of a witness whenever
it is called for a specific input x. It returns y and w, which we then hand to the
checker C . In this way, we obtain formal instance correctness without having to
verify the solution algorithm. Of course, this leaves the possibility that the solution
algorithm is incorrect and does not always provide a y and w such that the checker
accepts (x, y, w).
     For a user, the checker is what counts. The user can trust it because it has been
formally verified. Moreover, if it accepts a triple (x, y, w), the user can be sure that
y is a correct output, provided that x satisfies the precondition of the algorithm.
This is because the witness property has been formally verified. If the checker
rejects a triple, the user knows that either x does not satisfy the precondition or
(x, y, w) does not satisfy the witness predicate. The method by which y and w were
produced is of no concern to the user.
     The witness property is formulated with respect to a certain IO-behavior (ϕ, ψ )
and not with respect to a particular algorithm that realizes the IO-behavior.
Therefore, a checker can be used in connection with any certifying algorithm for
IO-behavior (ϕ, ψ ) that produces the appropriate witnesses.


3 Tool Overview: Isabelle/HOL and VCC

Isabelle/HOL [26] is an interactive theorem prover for classical higher-order logic
based on Church’s simply typed lambda calculus. The system is built on top of an
inference kernel, which provides only a small number of rules to construct theo-
rems; complex deductions (especially by automatic proof methods) ultimately rely
on these rules only. This approach, called LCF due to its pioneering system [18],
A Framework for the Verification of Certifying Computations                          7


guarantees the correctness of theorems proven in the system as long as the infer-
ence kernel is correct. Isabelle/HOL comes with a rich set of already formalized
theories, among which are natural numbers and integers as well as sets, finite sets,
and—as a recent addition [30]—graphs. New types can, for example, be introduced
by defining them as records (isomorphic to tuples with named update and selector
functions). New constants can be introduced, for example, via definitions relative
to already existing constants.
    Proofs in Isabelle/HOL can be written in a style close to that of mathematical
textbooks. The user structures the proof, and the system fills in the gaps with its
automatic proof methods. Moreover, the user can use locales, which allow defining
local scopes in which constants are defined and assumptions about them are made.
Theorems can be proven in the context of a locale and can use the constants and
depend on the assumptions of this locale. A locale can be instantiated to concrete
entities if the user is able to show that the latter fulfill the locale assumptions.

VCC     [14] is an assertional, automatic, deductive code verifier for full C. Specifi-
cations in the form of function contracts, data invariants, and loop invariants as
well as further annotations to maintain inductively defined information or to guide
VCC otherwise, are added directly into the C source code as comments. During
builds with a C compiler, these annotations are ignored. From the annotated pro-
gram, VCC generates verification conditions for partial or total correctness, which
it then tries to discharge using the automatic theorem prover Z3 [25] through the
Boogie verifier [3].
    Verification in VCC makes heavy use of ghost data and code, enclosed by (
and ), for reasoning about the program but omitted from the concrete implemen-
tation. VCC provides ghost objects, ghost fields of structured data types, local
ghost variables, ghost function parameters, and ghost code. Ghost data and ghost
code can use both C data types and additional mathematical data types, e.g.,
mathematical integers (\integer) and natural numbers (\natural), records (similar
to C structures), and maps (with a syntax similar to C arrays). VCC ensures that
information does not flow from a ghost state to a non-ghost state and that all ghost
code terminates; these checks guarantee that program execution, when projected
to the non-ghost code, is not affected by the ghost code.

Export from VCC to Isabelle/HOL. For the types and propositions that we pass from
VCC to Isabelle/HOL, we restrict ourselves to a subset of VCC’s specification
language. Simple types are natural numbers, integers, algebraic datatypes over
simple types, and ghost records whose fields are simple types. Rich types are simple
types, ghost records whose fields are rich types, and maps from simple types to
rich types. Propositions can be formed by usual logical connectives, quantifiers
over variables of rich types, arithmetic expressions, equalities, and user-defined
pure, stateless functions whose argument and result types are rich and whose
definitions or contracts are again propositions, possibly using pattern matching
over algebraic datatypes. Any type or function of this subset can be expressed
equivalently in Isabelle/HOL, essentially by syntactic rewriting. More precisely,
VCC algebraic datatypes can be translated into Isabelle datatypes, VCC ghost
records can be translated into Isabelle records, and pure VCC ghost functions can
be translated into Isabelle function definitions. The former two translations are
sound and complete because the semantics of datatypes and records is the same in
8                                         E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


both systems; the latter is sound and complete because VCC’s underlying logic is
subsumed by the higher-order logic of Isabelle/HOL. The translation maps VCC
specification types (\bool, \natural, \integer, and map types) to equivalent Isabelle
types (bool , nat , int , and function types) and maps VCC expressions comprising
logical connectives, quantifiers, arithmetic operations, equality, and specification
functions to corresponding Isabelle terms.


4 Case Studies

We present three case studies from the domain of graphs. We start with the certi-
fying algorithms and the corresponding checkers in LEDA. We give formal proofs
for the correctness of the checkers, for the related witness properties, and for the
connection between them. Except for the witness properties, which are proven in
Isabelle/HOL, all presented abstractions and functions have been formally verified
using VCC.
    All files related to our formalization can be obtained from the following URL:
http://www21.in.tum.de/~ boehmes/certifying_computations.html


4.1 Connected Components in Graphs

Our first case study considers the connected components problem. Given an undi-
rected graph G = (V, E ), we consider an algorithm that decides whether G is
connected, i.e., whether there is a path between any pair of vertices [24, Section
7.4]. In the negative case, i.e., when the graph is not connected, there is a simple
witness. It consists of a cut S , i.e., a nonempty subset S of the vertices with S 6= V
such that every edge of the graph has either both or no endpoint in S . In other
words, no edge crosses the cut. In the positive case, i.e., when the given graph is
connected, the algorithm can produce a spanning tree of G as a witness. A span-
ning tree of G is a subgraph of G, which is a tree and contains all vertices of G.
We concentrate here on the more complicated positive case. We describe a checker
for the spanning tree witness and the verification of this checker. On a high level,
we instantiate our general approach as follows:
      input x      =   an undirected graph G = (V, E )
     output y      =   either True or False , indicating whether G is connected
    witness w      =   a cut or a spanning tree
          ϕ(x)     =   G is wellformed, i.e., E ⊆ V × V , V and E are finite sets
    W (x, y, w)    =   y is True and w is a spanning tree of G, or y is False and w
                       is a cut
       ψ (x, y )   =   if y is True , G is connected, and if y is False , G is not con-
                       nected.
We restrict ourselves to the positive case y = True . Figure 3 shows a graph G
and a spanning tree of it. We represent spanning trees by functions parent -edge
and num and by a root vertex r , and we view the edges of the tree oriented
towards r : for v 6= r , parent -edge (v ) is the first edge on the path from v to r ,
parent -edge (r ) = ⊥, and num (v ) is the length of the path from v to r for all v .
The function num is needed in order to show that parent -edge encodes a forest. We
A Framework for the Verification of Certifying Computations                                 9


                 8           9

                 0                           0
     0                   1           0               1
             2
                     4                           2            vertex   0   1    2   3   4
 1                           3   1
                                                         parent-edge   ⊥   0    1   2   6
                                                                num    0   1    1   1   2
                 5
     2                   3           2               3

         6           7                   6
                 4                           4

(a) A connected graph G (b) A spanning tree of G         (c) Spanning tree representation

Fig. 3: An example of a connected graph G and a spanning tree of G witnessing its
connectivity. The vertices belong to the set {0, . . . , n − 1} and the edges are pairs
of vertices indexed by an identifier ranging from 0 to m − 1, where n and m are the
number of vertices and edges in G. The spanning tree in (b) can be represented
by a root vertex r = 0 and functions parent -edge and num as shown in the table
in (c). Graphs may have self-loops and parallel edges.


present the implementation of a checker in Section 4.1.1, detail the formalization of
the witness predicate and the verification of the checker in Section 4.1.2, and prove
the witness property in Section 4.1.3. The relevant files in the companion website
are check connected.c (C-code and checker correctness), check connected.thy (Is-
abelle/HOL representation of the VCC checker specification and witness property),
ConnectedComponents.thy (abstract verification of the witness property in a lo-
cale), and ConnectedComponents Link.thy (instantiation of the locale with the
Isabelle/HOL representation of the VCC specification).

4.1.1 Connected-Components Checker

We begin by fixing a representation of graphs in the programming language C, see
Listing 1. Vertices are numbered consecutively from 0 to n − 1. Edges are pairs
where the first vertex is labeled s (for source), and the second vertex is labeled t
(for target). Edges are stored in an array es, which is indexed by edge identifiers
ranging from 0 to m − 1. We require that the two vertices of each edge belong to
the graph, i.e., that they are from the range {0, . . . , n− 1}, and call graphs with this
property wellformed. We use the same data structure for directed and undirected
graphs. For directed graphs, an edge e with e.s = u and e.t = v is directed from u
to v. For undirected graphs, it represents the unordered pair {u,v}.
    We represent spanning trees as explained before. Instead of functions, we use
two arrays, parent edge and num, in addition to a root vertex r. The parent edge
array maps r to a negative value, i.e., to a value that does not identify any edge.
    The connected-graph checker is a function that succeeds if the two functions
check r and check parent num (Listing 2) succeed. The first function checks that r is
indeed the root of the spanning tree. The second function checks for every vertex
v different from r that the edge parent edge[v] is incident to v and that the other
endpoint of the edge has a number one smaller than num[v].
10                                         E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


typedef unsigned Nat;
typedef Nat Vertex;
typedef Nat Edge Id;
typedef struct { Nat s; Nat t; } Edge;
typedef struct { Nat m; Nat n; Edge∗ es; } Graph;


Listing 1: A representation of graphs in C. The field m gives the number of edges
(and hence the length of the array es), and n gives the maximum number of vertices
in the graph.


int check r(Graph∗ G, Vertex r, int∗ parent edge, Nat∗ num)
{
    return r < G−>n && num[r] == 0 && parent edge[r] == −1;
}

int check parent num(Graph∗ G, Vertex r, int∗ parent edge, Nat∗ num)
{
    Vertex v, a, b; Edge Id e;

     for (v = 0; v < G−>n; v++)
     {
         if (v == r) continue;

       if (parent edge[v] < 0 || ((Edge Id)parent edge[v]) >= G−>m) return FALSE;

       e = (Edge Id)parent edge[v];
       a = G−>es[e].s;
       b = G−>es[e].t;

       if (v == a && num[v] == num[b] + 1) continue;
       if (v == b && num[v] == num[a] + 1) continue;
       return FALSE;
     }
     return TRUE;
}


                     Listing 2: The connected-components checker.


4.1.2 Checker Correctness

To prove the two checker functions correct, we need to provide abstract repre-
sentations for graphs and paths. We decided to keep them close to the concrete
representation for two reasons. First, it makes detecting differences, and hence po-
tential bugs, easier for the programmer. Second, it also makes reasoning for VCC
simpler. The declaration of abstract graphs is given in Listing 3 together with the
ghost predicate \wellformed for describing when an abstract graph is wellformed.
This ghost predicate plays the role of the precondition ϕ in this case study. Our
abstract version of the num array is a mapping from vertices to natural numbers.
The abstract version of the parent edge array is a mapping from vertices to the set
N ∪ {⊥}; we use ⊥ to model an undefined value. To represent this set, we define
an algebraic datatype Option:
A Framework for the Verification of Certifying Computations                         11


 (typedef \natural \Vertex)                (def \bool \wellformed(\Graph G)
 (typedef \natural \Edge Id)              {
 (record \Edge {                             return
   \Vertex src;                                  ∀ \Edge Id i; i < G.num edges −→
   \Vertex trg;                                     G.edge[i].src < G.num verts ∧
})                                                  G.edge[i].trg < G.num verts;
 (record \Graph {                         })
   \natural num verts;
   \natural num edges;
   \Edge edge[\Edge Id];
})


    Listing 3: Abstract graphs and a predicate to describe wellformed graphs.


     (datatype \Option
    {
       case \none();
       case \some(\Edge Id e);
    })

with operations \is some(o) for the test o 6= ⊥ and \the(o) for extracting an edge
identifier. The abstraction functions that map concrete data to pure mathematical
data are straightforward to define. For example,
     (def \Graph \abs graph(Graph∗ G)
    {
       return (\Graph) {
           .num verts = G−>n,
           .num edges = G−>m,
           .edge =
              \lambda \Edge Id i;
                 (i < G−>m) ?
                    (\Edge) { .src = G−>es[i].s, .trg = G−>es[i].t } :
                    (\Edge) { .src = 0, .trg = 0 }};
    })

abstracts a concrete graph G into an abstract graph of type \Graph. Using the
abstract types, we define the witness predicate as a conjunction of two properties,
one for each of the checker functions in Listing 2.

check r: Vertex r is the root of the spanning tree:
        r < G.num verts ∧ ¬\is some(parent edge[r]) ∧ num[r] = 0

check parent num: Every vertex of the graph is connected to some other vertex
    closer to r:
        ∀ \Vertex v; v < G.num verts ∧ v 6= r −→
           \is some(parent edge[v]) ∧ \the(parent edge[v]) < G.num edges ∧
           (G.edge[\the(parent edge[v])].trg == v ∧
              num[v] == num[G.edge[\the(parent edge[v])].src] + 1 ∨
            G.edge[\the(parent edge[v])].src == v ∧
              num[v] == num[G.edge[\the(parent edge[v])].trg] + 1)


   Thanks to the low level of abstraction in the above predicates, the two checker
functions are easily verified. For the verification of check parent num, we need to
annotate the loop with the second conjunct above in which G.num verts is replaced
12                                             E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


by the loop variable as a loop invariant. Moreover, for every return FALSE, we need
to assert, or restate, on the abstract level the properties that are violated to guide
VCC. Otherwise, it would fail to show completeness of the checker. For instance,
     if (parent edge[v] < 0 || ((Edge Id)parent edge[v]) >= G−>m)
     {
          (assert ¬\is some(P[v]) ∨ \the(P[v]) ≥ \abs graph(G).num edges)
         return FALSE;
     }

is one of the two occurrences of such extra assertions in check parent num.
    We express the postcondition of the checker, i.e., that any pair of vertices of
the graph G is connected by a path as follows:
     ∀ \Vertex u, v; u < G.num verts ∧ v < G.num verts −→
        ∃ \Path p; \natural n; \is path(G, p, n, u, v)

Here, the type \Path is a sequence of vertices, represented as a mapping from
natural numbers to vertices, and the predicate \is path(G, p, n, u, v) holds if the
path p of length n starts at u, ends at v, and only contains pairwise distinct
vertices that are connected by edges of the graph:
     p[0] == u ∧
     p[n] == v ∧
     (∀ \natural i; i ≤ n −→ p[i] < G.num verts) ∧
     (∀ \natural i; i < n −→ \is edge(G, p[i], p[i+1])) ∧
     (∀ \natural i, j; i ≤ n ∧ j ≤ n ∧ i 6= j −→ p[i] 6= p[j])

The predicate \is edge(G, u, v), for any two vertices u and v of G, is true if and only
if u and v are the endpoints of an edge of G:
     ∃ \Edge Id i; i < G.num edges ∧
        (G.edge[i].src = u ∧ G.edge[i].trg = v ∨
         G.edge[i].src = v ∧ G.edge[i].trg = u)

We give a formal proof for the implication, from precondition and witness predicate
to the postcondition, in the next section.

4.1.3 Proof of the Witness Property for the Connected-Components Checker

We prove in Isabelle that a spanning tree witnesses the connectivity of a graph.
We do so in two steps. First, we perform a high-level proof in which we abstract
from concrete representations of graphs and spanning trees. We then instantiate
this proof with the data structures and corresponding properties exported from
VCC.
     Our formalization builds on the Isabelle graph library developed by Lars No-
schinski [30]. Graphs in this library are directed. A pseudo-digraph is a wellformed
directed graph with a finite set of vertices and a finite set of edges; the library
reserves the word digraph for graphs without parallel edges and self-loops. Unlike
in VCC, in Isabelle we represent undirected graphs as bidirected graphs4 , i.e.,
directed graphs containing for every edge (u, v ) also the reversed edge (v, u). The
function mk -symmetric maps a pseudo-digraph to a bidirected pseudo-digraph by
appropriately extending the set of edges with missing reversed edges. A vertex v
is reachable from a vertex u in a (bi)directed graph G if there exists a directed walk
 4   We do so in order to directly use the Isabelle graph library.
A Framework for the Verification of Certifying Computations                                     13


locale connected-components-locale = pseudo-digraph +
   fixes num :: α ⇒ nat
   fixes parent-edge :: α ⇒ β option
   fixes r :: α
   assumes r assms: r ∈ verts G ∧ parent-edge r = None ∧ num r = 0
   assumes
      V       parent-num-assms :
        v. v ∈ verts G ∧ v 6= r =⇒
         ∃e ∈ edges G.
             parent-edge v = Some e ∧
             target G e = v ∧
             num v = num (start G e) + 1

                                                                                                V
Listing 4: Locale for the connected-components proof in Isabelle. The symbol
stands for universal quantification.



from u to v in G, i.e., a sequence (u1 , v1 ), (u2 , v2 ), . . . , (uk , vk ) of edges with u1 = u,
vk = v , and vi = ui+1 for 1 ≤ i < k. An alternative and equivalent formalization of
reachability between vertices u and v in G is via sequences of vertices v1 , v2 , . . . , vk ,
where v1 = u, vk = v and (vi , vi+1 ) is an edge of G for 1 ≤ i < k. We say a vertex
v is reachable through a path from a vertex u in G if v is reachable from u through
a path in G. An undirected graph is connected if for any two vertices of the graph,
one is reachable through a path from the other.
    Our high-level proof rests on the Isabelle locale connected - components -locale
(Listing 4) that describes the assumptions of our theorem. We fix G to be a pseudo-
digraph where α is an abstraction of the type of vertices and β is an abstraction
of the type of edges. Furthermore, we fix a representation of spanning trees with
functions parent -edge and num and vertex r as the root. Based on these assump-
tions, we prove that G is connected. We show first that every vertex v in the graph
is reachable from the root r by induction on num v , i.e., the length of the walk from
r to v in the spanning tree. The base case follows directly from our assumptions.
For the inductive step, we can assume a walk from r to the parent of a vertex v .
Using the assumptions, this walk can be extended to a walk from r to v since there
is an edge between v and its parent. Now, since G is bidirected, we can establish
that there is a walk between any two vertices of G by combining the walks that
connect them with the root r . If there is a walk between two vertices, there is also
a path between them. Therefore, all vertices in G are reachable through a path
from one another, and hence, G is connected.
    The final part of the formal proof—linking the high-level proofs with the prop-
erties exported from VCC to Isabelle—is fairly straightforward. Proving that the
precondition and the witness predicate (cf. Section 4.1.2) match the assumptions
specified in the locale connected - components -locale involves no reasoning beyond
syntactical rewriting. To instantiate these assumptions, we provide lifting func-
tions that abstract from the concrete representations of graphs and spanning trees
stemming from our VCC specification to the high-level representation used by
the Isabelle graph library. Thus, if the checker accepts, the lifted high-level graph
is connected. Establishing the checker postcondition (the connectivity of unlifted
graphs) requires showing that any high-level path witnessing reachability between
two vertices corresponds to an unlifted path. This is straightforward because our
14                                                     E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


             0/1
      s                 t                          0
                                               s           t
           2/1                                                          vertex    s    t   u   v    w
1/1                         4/0            1           3           parent-edge    ⊥   0    1   3   ⊥
                  3/0
                                                                          num     0   1    1   2   ∞
      u      5/2        v                                                  dist   0   1    1   1   ∞
                                               u           v


              w                                    w
(a) A directed graph G (b) A shortest-path tree of G                     (c) Tree representation

Fig. 4: A directed graph G = (V, E ) with the edges labeled i/k, where i is a unique
edge index and where k is the cost of that edge, and a shortest-path tree of G
rooted at start vertex s ∈ V . The tree is encoded by parent -edge , num and dist
according to the table in (c). Observe that vertex w is not reachable from s and
that the cycle t → v → t has cost zero.


representation of paths in the VCC formalization (cf. Section 4.1.2) is close to the
path representation of the Isabelle graph library.


4.2 Shortest Paths in Graphs

Our second case study is about the single-source shortest-path problem in directed
graphs with nonnegative edge weights. It can be solved, for instance, using Dijk-
stra’s algorithm [24, Sections 6.6 and 7.5]. Instead of verifying this algorithm, we
request that it returns, along with the computed shortest distance for each vertex
of a graph, the corresponding shortest path as witness. That is, we instantiate our
general approach as follows:

       input x          =         a directed graph G = (V, E ), a function cost : E → N for edge
                                  weights, a vertex s
      output y          =         a mapping dist : V → (N ∪ ∞)
     witness w          =         a tree rooted at s
           ϕ(x)         =         G is wellformed, V and E are finite sets, and s ∈ V
     W (x, y, w)        =         w is a shortest-path tree, i.e., for each v reachable from s,
                                  the tree path from s to v has length dist (v )
          ψ (x, y )     =         for each v ∈ V , dist (v ) is the cost of a shortest path from s
                                  to v (or ∞ if there is no path from s to v ).

Figure 4 shows a directed graph and a shortest-path tree rooted at s. We encode
a shortest-path tree by functions parent -edge , dist , and num . For each v reachable
from s, dist (v ) is the shortest-path distance from s to v and num (v ) is the depth of
v in the shortest-path tree. For vertices v that are not reachable from s, dist (v ) =
num (v ) = ∞. For reachable vertices v different from s, the edge parent -edge (v ) is
the last edge on a shortest path from s to v . This witness is somewhat verbose.
As we will see in Section 4.2.3, we could do without the parent -edge function. If all
edge costs are positive, no witness is required beyond the dist function. If one also
A Framework for the Verification of Certifying Computations                             15


allows cost zero for edges as we do, the depth function num is indispensable [23,
Section 2.4].
    We present the implementation of a checker in Section 4.2.1, detail the for-
malization of the witness predicate and the verification of the checker in Sec-
tion 4.2.2, and prove the witness property in Section 4.2.3. The relevant files in
the companion website are check shortest path.c (C-code and checker correctness),
check shortest path.thy (Isabelle/HOL representation of the VCC checker specifi-
cation, and witness property), ShortestPath.thy (abstract verification of the wit-
ness property in a locale), and ShortestPath Link.thy (instantiation of the locale
with the Isabelle/HOL representation of the VCC specification).




4.2.1 Shortest-Paths Checker

We adopt the data structures of the previous case study (Section 4.1.1) with the
exception that the num array stores elements of type int instead of Nat. This is
because vertices may now also be unreachable from the source vertex, and we
encode this by requiring that num takes a negative value for such vertices. We
represent distances from the source vertex to any other vertex by an array dist
with elements of type int. Any negative value encodes ∞. Finally, the edge weights
are modeled by an array cost that gives for every edge a value of type ushort (an
abbreviation for unsigned short).
     Based on these types, we implement the shortest-path checker as a function
that succeeds when all of the four functions given in Listing 5 succeed. That is,
we check that the source vertex s is indeed the starting point (in check start val),
that the dist and num arrays are consistent with respect to unreachable vertices,
i.e., either both are finite or both are infinite (in check no path), that the triangle
inequality property (Section 4.2.3) is fulfilled (in check trian), and that the parent
edge of every vertex v defines its distance value (in check just).
    There is a subtle point in the checker code. We want to establish the trian-
gle inequality (dist (u) + cost(u, v ) ≥ dist (v ) for all edges (u, v )) and the distance
justification (dist (u) + cost(u, v ) = dist (v ) if (u, v ) is the parent edge of v ) over
the extended natural numbers N ∪ {∞}. However, C knows only finite precision
arithmetic. We solve the case of infinite distances by appropriate case distinctions.
We solve the case of potential overflow in finite precision arithmetic as follows:
Distances are of type int, i.e., from the set {−231 , . . . , 231 − 1} on a 32-bit plat-
form, and edge costs are of type ushort, i.e., between 0 and 216 − 1, and hence
contained in the set of nonnegative values of type int. In arithmetic expressions,
we cast all nonnegative values to unsigned with range 0 . . . 232 − 1. This guarantees
that finite precision arithmetic is exact and allows VCC to conclude equalities and
inequalities between natural numbers.
   Note that there is an alternative approach where parent edge is not part of the
witness. In that case check just has to be rewritten. When considering a node v, it
has to iterate over all edges into v to find the edge that defines dist[v]. An efficient
implementation of this iteration requires providing each vertex with the list of
edges into it.
16                                            E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


bool check start val(Vertex s, int∗ dist, int∗ num)
{
  return dist[s] == 0;
}

bool check no path(Graph∗ G, int∗ dist, int∗ num)
{
  Vertex v;

     for (v = 0; v < G−>n; v++)
     {
         if (INF(dist[v]) != INF(num[v])) return FALSE;
     }
     return TRUE;
}

int check trian(Graph∗ G, ushort∗ cost, int∗ dist)
{
    Edge Id e; Vertex source, target;

     for (e = 0; e < G−>m; e++)
     {
         source = G−>es[e].s;
         target = G−>es[e].t;

        if (INF(dist[source])) continue;
        if (INF(dist[target])) return FALSE;
        if (VAL(dist[target]) > VAL(dist[source]) + cost[e]) return FALSE;
     }
     return TRUE;
}

bool check just(Graph∗ G, Vertex s, ushort∗ cost, int∗ dist, int∗ parent edge, int∗ num)
{
  Vertex v, source; Edge Id e;

     for (v = 0; v < G−>n; v++)
     {
         if (v == s || INF(num[v])) continue;
         if (parent edge[v] < 0 || ((Edge Id)parent edge[v]) >= G−>m) return FALSE;

        e = (Edge Id)parent edge[v];
        source = G−>es[e].s;

        if (G−>es[e].t != v) return FALSE;
        if (INF(dist[source]) || VAL(dist[v]) != VAL(dist[source]) + cost[e]) return FALSE;
        if (INF(num[source]) || VAL(num[v]) != VAL(num[source]) + 1) return FALSE;
     }
     return TRUE;
}


Listing 5: Functions composing the shortest-path checker. The predicate INF(x)
abbreviates x < 0, and VAL(x) stands for the type cast (Nat)x; Nat is the C type
unsigned as defined in Listing 1.
A Framework for the Verification of Certifying Computations                            17


4.2.2 Checker Correctness

We now define our abstract specification for the shortest-path checker. We use
the same data structures as in the previous case study (Section 4.1.2) with the
exception that the num mapping now takes vertices to extended naturals (N ∪{∞}),
represented by the type Enat. Extended naturals provide an explicit value for
infinity:
     (datatype \Enat
    {
       case \enat inf();
       case \enat val(\natural n);
    })

We define functions \is enat inf to check whether an extended natural is infinity
and \enat val of to convert an extended natural distinct from infinity into the
corresponding natural number. For better readability, we will write a =e ∞ for
\is enat inf(a). Moreover, we provide the predicates \enat eq (abbreviated by =e )
and \enat le (≤e ) to decide equality and less-or-equal of two extended naturals as
well as a function \enat add (+e ) for the sum of an extended natural and a natural
number:
     (def \bool \enat eq(\Enat e1, \Enat e2)
    {
       return
           (e1 =e ∞ ∧ e2 =e ∞) ∨
           (e1 6=e ∞ ∧ e2 6=e ∞ ∧ \enat val of(e1) = \enat val of(e2));
    })

     (def \bool \enat le(\Enat e1, \Enat e2)
    {
       return e2 =e ∞ ∨ (e1 6=e ∞ ∧ e2 6=e ∞ ∧ \enat val of(e1) ≤ \enat val of(e2));
    })

     (def \Enat \enat add(\Enat e, \natural n)
    {
       return (e =e ∞) ? \enat inf() : \enat val(\enat val of(e) + n);
    })

The type of extended natural numbers is also used for the abstract representation
of the dist array. Again, as in the previous case study, concrete types and abstract
types are sufficiently similar such that abstraction functions relating one to the
other are straightforward to define. We omit them here.
    The preconditions of this case study are that G is a wellformed graph and that
the source vertex s is a vertex of G, i.e., that s < G.num verts holds. We formalize
the witness predicate as a conjunction of four properties, one for each of the four
checker functions in Listing 5.
check start val: Vertex s is indeed the starting point:
        dist[s] =e \enat val(0)

check no path: The num mapping and the dist mapping are consistent with respect
   to unreachable vertices, i.e., both are either finite or infinite:
        ∀ \Vertex v; v < G.num verts −→ (dist[v] =e ∞ ←→ num[v] =e ∞)

check trian: The triangle inequality holds for all edges of the graph:
18                                             E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


         ∀ \Edge Id i; i < G.num edges −→
            dist[G.edge[i].trg] ≤e dist[G.edge[i].src] +e cost[i]

check just: The parent edges encode a tree rooted at s and define the distance
     values of reachable vertices:
         ∀ \Vertex v;
            v < G.num verts ∧ v 6= s ∧ num[v] 6=e ∞ −→
            \is some(parent edge[v]) ∧ \the(parent edge[v]) < G.num edges ∧
            v = G.edge[\the(parent edge[v])].trg ∧
            dist[v] =e dist[G.edge[\the(parent edge[v])].src] +e cost[\the(parent edge[v])] ∧
            num[v] =e num[G.edge[\the(parent edge[v])].src] +e 1



We have verified that each of these four properties holds if and only if the corre-
sponding checker function succeeds. The three functions check no path, check trian,
and check just need additional annotations before VCC can verify their correct-
ness. The loops in these functions have to be annotated with loop invariants that
are, just as in the previous case study (Section 4.1.2), only simple variants of the
postconditions above. Also, as for the connected-components checker, we need to
explicitly state properties that are violated before every return FALSE statement.
Such properties are reformulations of concrete properties on the abstract level. In
addition, both check trian and check just require the graph under consideration to be
wellformed, and check just, furthermore, requires that num and dist are consistent
(the postcondition of check no path). We add these requirements as preconditions
to the checker functions.
    In order to be able to express the postcondition of the shortest-path checker,
we define sequences of edges as a recursive datatype:
      (datatype \Path
     {
        case none();
        case path(\Edge Id i, \Path p);
     })

Only particular instances of this datatype are paths in the given graph G. To qualify
valid paths, we proceed in two steps. We first define a predicate that expresses the
conditions under which a sequence of edges constitutes a walk in graph G from
vertex u to vertex v (Listing 6). Second, we define a predicate to describe when
the set of vertices of an edge sequence is distinct (Listing 7). A path from vertex
u to vertex v in G is a walk p from u to v with distinct vertices. We define this as
a predicate \is path(G, p, u, v).
    With a recursive function \path cost that computes for a given path its length
using the cost mapping, we can finally state the postcondition of the shortest path
checker:
     (∀ \Vertex v; v < G.num verts −→
        ¬\is enat inf(dist[v]) ←→ (∃ \Path p; \is path(G, p, s, v))) ∧
     (∀ \Vertex v; v < G.num verts ∧ ¬\is enat inf(dist[v]) −→
        (∀ \Path p; \is path(G, p, s, v) −→ \enat val of(dist[v]) ≤ \path cost(cost, p)) ∧
        (∃ \Path p; \is path(G, p, s, v) ∧ \enat val of(dist[v]) = \path cost(cost, p)))

We formally prove this property, under the assumption of the precondition and
the witness predicate, in Isabelle below.
A Framework for the Verification of Certifying Computations                                       19


 (def \bool \is walk(\Graph G, \Path p, \Vertex u, \Vertex v)
{
   switch (p)
   {
       case none(): return u = v;
       case path(i, q):
          return i < G.num edges ∧ u = G.edge[i].src ∧ \is walk(G, q, G.edge[i].trg, v);
   }
})


Listing 6: A walk from vertex u to vertex v is a finite sequence of connected edges
of graph G where the source vertex of the first edge is u and the target vertex of
the last edge is v.


 (def \bool \occurs(\Graph G, \Vertex u, \Vertex v, \Path p)
    (decreases \size(p))
{
   switch (p)
   {
       case none(): return u = v;
       case path(i, q): return u = G.edge[i].src ∨ \occurs(G, u, G.edge[i].trg, q);
   }
})

 (def \bool \distinct verts(\Graph G, \Path p)
{
   switch (p)
   {
       case none(): return \true;
       case path(i, q): return ¬\occurs(G, G.edge[i].src, G.edge[i].trg, q) ∧ \distinct verts(G, q);
   }
})


Listing 7: Predicate \distinct verts(G, p) holds if the set of vertices connected by
path p is distinct. Predicate \occurs(G, u, v, p) is true if and only if u is either
equal to v or equal to any vertex touched by path p.


4.2.3 Proof of the Witness Property for the Shortest-Path Checker

We here present the outline of the Isabelle/HOL proof of the witness property,
namely that if G is wellformed (the precondition of this case study) and if the
witness predicate holds, then d ist(v ) is indeed the shortest-path distance from s
to v for all vertices v ∈ V . For the full formal proof, please check the companion
website.
    Listing 8 shows our Isabelle locales. We separate the assumptions into three
locales to avoid the use of unneeded assumptions when proving intermediate lem-
mas. This makes the intermediate lemmas more general, and hence, usable in
other contexts5. The first locale basic -sp subsumes the locale pseudo -digraph men-
  5 For example, we used some of those lemmas also for the verification of a checker for the

shortest-path problem with general edge weights (not only nonnegative edge weights as in this
case study) [33].
20                                       E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


locale basic-sp = pseudo-digraph +
   fixes dist :: α ⇒ ereal
   fixes c :: β ⇒ real
   fixes s :: α
   assumes generalVsource val: dist s ≤ 0
   assumes trian: e. e ∈ edges G =⇒ dist (target G e) ≤ dist (start G e) + c e

locale basic-just-sp = basic-sp +
   fixes num :: α ⇒ enat
   assumes
     V         just:
       v. v ∈ verts G =⇒ v 6= s =⇒ num v 6= ∞ =⇒
        ∃ e ∈ edges G.
            v = target G e ∧
            dist v = dist (start G e) + c e ∧
            num v = num (start G e) + enat 1

locale shortest-path-pos-cost = basic-just-sp +
   assumes s-in-G: s ∈ verts G
   assumes start val:V dist s = 0
   assumes no-path: Vv. v ∈ verts G =⇒ (dist v = ∞ ←→ num v = ∞)
   assumes pos-cost : e. e ∈ edges G =⇒ 0 ≤ c e


             Listing 8: Locales for the shortest-paths proof in Isabelle.


lemma (in basic-just-sp) dist-ge-µ:
   fixes v :: α
   assumes v ∈ verts G
   assumes num v 6= ∞
   assumes dist v 6= −∞
   assumes µ c s s = ereal 0
              V s=0
   assumes dist
   assumes u. u ∈ verts G =⇒ u 6= s =⇒ num u 6= ∞ =⇒ num u 6= enat 0
   shows dist v ≥ µ c s v


       Listing 9: The central lemma of the shortest-paths proof in Isabelle


tioned in Section 4.1.3. Moreover, it assumes it is given the function dist : V →
(R ∪ {∞, −∞}), an edge cost function c : E → R, and a start vertex s.
    Let µ be a function that takes a cost function c on edges and two vertices s
and v and returns the cost of a shortest path from s to v in G using the cost
function c. We split the proof into two parts. First, we prove a lemma dist -le -µ
using the locale basic -sp . The lemma states that dist v ≤ µ c s v for every vertex
v ∈ V . Then, we prove a lemma dist -ge -µ using the locale basic -just -sp . The lemma
states that dist v ≥ µ c s v for every vertex v ∈ V under some extra assump-
tions (Listing 9). Later, we show that these extra assumptions hold in the locale
shortest - path -pos -cost . Hence, we obtain a theorem stating that dist v = µ c s v for
every v ∈ V using the locale shortest - path -pos -cost .
    Linking this Isabelle proof with the specification exported from VCC is a mat-
ter of translating from one representation to another. We intentionally chose to de-
fine paths and their costs in VCC (Section 4.2.2) similar to the way they are defined
in the Isabelle graph library to ease our translation proofs. Since there are several
more concepts to relate than in the previous checker (Section 4.1.3), our proofs for
A Framework for the Verification of Certifying Computations                          21


                                  1

                             0         1             0          1

                                                          0

                             2         2             1          0

                                  2                       0

Fig. 5: The vertex labels certify that the indicated matching is of maximum car-
dinality: All edges of the graph have either both endpoints labeled as 2 or at least
one endpoint labeled as 1. Any matching can hence use at most one edge with
both endpoints labeled 2 and at most four edges that have an endpoint labeled 1.
Therefore, no matching has more than five edges. The matching shown consists of
five edges (in bold).


the shortest-path checker are more tedious. Nevertheless, no complex reasoning is
required. We establish that the assumptions of the shortest - path -pos -cost locale are
implied by the checker precondition and witness predicate, and we prove that our
final theorem proved in that locale implies the checker postcondition.


4.3 Maximum Cardinality Matching in Graphs

Our third case study is about maximum cardinality matching in general graphs.
A matching in a graph G is a subset M of the edges of G such that no two share an
endpoint. A matching has maximum cardinality if its cardinality is at least as large
as that of any other matching. Figure 5 shows a graph, a maximum cardinality
matching, and a witness of this fact. An odd-set cover L of a graph G is a labeling
of the vertices of G with integers such that every edge of G is either incident to
a vertex labeled 1 or connects two vertices labeled with the same number i and
i ≥ 2.

Theorem 2 (Edmonds [16]) Let M be a matching in a graph G, and let L be an
odd-set cover of G. For any i ≥ 0, let ni be the number of vertices labeled i. If
                                               X
                                 |M | = n1 +         ⌊ni /2⌋,                       (2)
                                               i≥2

then M is a maximum cardinality matching.

Proof Let N be any matching in G. For i ≥ 2, let Ni be the edges in N that
connect two vertices labeled i, and let N1 be the remaining edges in N . Then, by
the definition of odd-set cover, every edge in N1 is incident to a vertex labeled 1.
Since edges in a matching do not share endpoints, we have

                        |N1 | ≤ n1 and |Ni | ≤ ⌊ni /2⌋ for i ≥ 2.
                    P
Thus, |N | ≤ n1 +     i≥2 ⌊ni /2⌋ = |M |.                                             ⊓
                                                                                      ⊔
22                                      E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


    For every maximum cardinality matching M there is an odd-set cover L sat-
isfying equality (2); the proof of this is nontrivial and of no importance for the
purpose of this paper. The cover uses nonnegative vertex labels in the range 0
to |V | − 1 and all ni ’s with i ≥ 2 are odd. The certifying algorithm for maximum
cardinality matching in LEDA returns a matching M and an odd-set cover L such
that (2) holds. The relationship to Section 2 is as follows:

       input x      =   an undirected graph G
      output y      =   a set of edges M
     witness w      =   a vertex labeling L
           ϕ(x)     =   G and M are wellformed and have no self-loops
     W (x, y, w)    =   M is a matching in G, L is an odd-set cover for G, and
                        Equation (2) holds
        ψ (x, y )   =   M is a maximum cardinality matching in G.

    Theorem 2 is the witness property. We give a formal proof for it in Section 4.3.3.
It is easy to write a correct program that checks whether a set of edges is a
matching and a vertex labeling is an odd-set cover, which together satisfy Equa-
tion 2, see Section 4.3.1. In Section 4.3.2, we describe the verification of such a
checker. The relevant files in the companion website are check matching.c (C-code
and checker correctness), check matching.thy (Isabelle/HOL representation of the
VCC checker specification and witness property), Matching.thy (abstract verifica-
tion of the witness property in a locale), and Matching Link.thy (instantiation of
the locale with the Isabelle/HOL representation of the VCC specification).
    This case study is a modified version of the one we present in [1]. The proof
of the witness property is very similar to the one published in [32] except that it
uses the Isabelle graph library, which has been developed meanwhile.

4.3.1 Maximum-Cardinality-Matching Checker

We build the checker using the graph data structure as in the previous case studies
(Listing 1). We assume that graphs are wellformed and have neither self-loops nor
duplicate edges. We treat the edges of a graph as undirected edges. Matchings are
also represented by graphs. We require an additional witness in the form of an
array f that maps edge identifiers of the matching to edge identifiers of the input
graph. For instance, if a graph consists of three edges (identified as 0, 1 and 2) and
the computed matching consists of the third edge (i.e., 2), then f would be an array
with a single element 2 indicating how the only edge of the matching corresponds
to the edges of the input graph. Finally, the vertex labeling is represented by an
array osc, which is indexed by vertices and stores elements of type Nat. The checker
function requires an auxiliary array check that can store as many elements of type
Nat as there are vertices in the input graph, but at least two. We expect that this
array is allocated elsewhere and given as input to the checker.
    In addition to the checker function, there are four helper functions (Listing 10).
The checker succeeds if the first three of them succeed and if the fourth func-
tion returns a value that is equal to the number of edges of the matching M. In
short, the helper functions perform the following tasks. The function check subset
checks whether M is a subgraph of G with respect to the mapping f. The function
check matching checks that M is indeed a matching (contains no two edges that
A Framework for the Verification of Certifying Computations                         23


are incident). The function check osc checks whether the vertex labeling is an odd-
set cover and that vertex labels are in the range {0, . . . , G−>n − 1}. Finally, the
function weight computes the sum on the right-hand side of Equation (2). This
computation is optimized by first searching for the greatest vertex label, which
can be considerably smaller than the maximal G−>n − 1, and then summing up
partial sums only until this greatest label. The main checker function passes the
auxiliary array check to check matching as the degree in M argument and to weight
as the count argument.


4.3.2 Checker Correctness

We build on the abstract graph data structure of Listing 3. We require that graphs
are wellformed and contain no self-loops:
    ∀ \Edge Id i; i < G.num edges −→ G.edge[i].src 6= G.edge[i].trg

nor duplicate edges:
    ∀ \Edge Id i1, i2; i1 < G.num edges ∧ i2 < G.num edges ∧ i1 6= i2 −→
       G.edge[i1].src 6= G.edge[i2].src ∨ G.edge[i1].trg 6= G.edge[i2].trg

An abstract vertex labeling L is a mapping from vertices to natural numbers. The
mapping f from edge identifiers to edge identifiers has a straightforward represen-
tation as an abstract mapping. We omit here, as in the previous case studies, the
description of abstraction functions from concrete to abstract values.
    The witness predicate is a conjunction of four predicates, each related to one
of the helper functions in Listing 10.

check subset: M must be a subgraph of G w.r.t. the edge mapping f, i.e., every edge
    of M must also be an edge of G modulo symmetry of edges:
        ∀ \Edge Id i; i < M.num edges −→
           f[i] < G.num edges ∧
           (M.edge[i].src = G.edge[f[i]].src ∧ M.edge[i].trg = G.edge[f[i]].trg ∨
            M.edge[i].src = G.edge[f[i]].trg ∧ M.edge[i].trg = G.edge[f[i]].src)

check matching: M must be a matching, i.e., no two edges of M have a vertex in
   common:
        ∀ \Edge Id i1, i2;
           i1 < M.num edges ∧ i2 < M.num edges ∧ i1 6= i2 −→
           M.edge[i1].src 6= M.edge[i2].src ∧ M.edge[i1].src 6= M.edge[i2].trg ∧
           M.edge[i1].trg 6= M.edge[i2].src ∧ M.edge[i1].trg 6= M.edge[i2].trg

check osc: L must be an odd-set cover of G, i.e., for every edge of G, one of the
   edge’s vertices is labeled 1 or both vertices are labeled by the same number
   greater than or equal to 2:
        ∀ \Edge Id i; i < G.num edges −→
           L[G.edge[i].src] = 1 ∨
           L[G.edge[i].trg] = 1 ∨
           L[G.edge[i].src] = L[G.edge[i].trg] ∧ L[G.edge[i].src] ≥ 2

weight: Equation (2) must hold. We define it stepwise. The number of vertices
    labeled with c is defined recursively:
24                                            E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


bool check subset(Graph∗ G, Graph∗ M, Nat∗ f)
{
  Edge Id e;

     for (e = 0; e < M−>m; e++)
     {
         if (f[e] >= G−>m) return FALSE;
         if (M−>es[e].s == G−>es[f[e]].s && M−>es[e].t == G−>es[f[e]].t) continue;
         if (M−>es[e].s == G−>es[f[e]].t && M−>es[e].t == G−>es[f[e]].s) continue;
         return FALSE;
     }
     return TRUE;
}

bool check matching(Graph∗ M, Nat∗ degree in M)
{
  Vertex v; Edge Id e;

     for (v = 0; v < M−>n; v++) degree in M[v] = 0;
     for (e = 0; e < M−>m; e++)
     {
         if (degree in M[M−>es[e].s] == 1 || degree in M[M−>es[e].t] == 1) return FALSE;
         degree in M[M−>es[e].s] = 1;
         degree in M[M−>es[e].t] = 1;
     }
     return TRUE;
}

bool check osc(Graph∗ G, Nat∗ osc)
{
  Edge Id e; Vertex v, w;

     for (v = 0; v < G−>n; v++) if (osc[v] >= G−>n) return FALSE;
     for (e = 0; e < G−>m; e++)
     {
         v = G−>es[e].s;
         w = G−>es[e].t;
         if (osc[v] == 1 || osc[w] == 1 || (osc[v] == osc[w] && osc[v] ≥ 2)) continue;
         return FALSE;
     }
     return TRUE;
}

Nat weight(Graph∗ G, Nat∗ osc, Nat∗ count)
{
  Vertex v; Nat c, s, max = 1, r = (G−>n > 2) ? G−>n : 2;

     for (c = 0; c < r; c++) count[c] = 0;
     for (v = 0; v < G−>n; v++)
     {
         count[osc[v]] = count[osc[v]] + 1;
         if (osc[v] > max) max = osc[v];
     }
     s = count[1];
     for (c = 2; c < max + 1; c++) s += count[c] / 2;
     return s;
}


     Listing 10: Helper functions of the maximum-cardinality-matching checker.
A Framework for the Verification of Certifying Computations                             25


         (def \natural \label count(\Label L, \natural c, \natural i)
        {
           return (i = 0) ? 0 : ((L[i − 1] = c) ? 1 : 0) + \label count(L, c, i − 1);
        })

   We have nc = \label count(L, c, G.num verts) for a vertex label c. The sum of
   these numbers for labels greater than 1 is again defined recursively:
         (def \natural \rec weight(\Label L, \natural n, \natural i)
        {
           return (i < 2) ? 0 : \label count(L, i, n) / 2 + \rec weight(L, n, i − 1);
        })
             P
   We have i≥2 ⌊ni /2⌋ = \rec weight(L, G.num verts, m) where m is the greatest
   label assigned to any vertex by L. The complete sum is then:
         (def \natural \full weight(\Label L, \natural n, \natural i)
        {
           return \label count(L, 1, n) + \rec weight(L, n, i);
        })
                          P
   That is, we have n1 + i≥2 ⌊ni /2⌋ = \full weight(L, G.num verts, m) with the
   same m as before. Finally, the predicate capturing Equation (2) is as follows:
        M.num edges = \full weight(L, G.num verts, m) ∧
        ∀ \Vertex v; v < G.num verts −→ L[v] ≤ m


    Verifying the correctness of the checker (Section 4.3.1) is done in the same
way as the earlier case studies for the first three predicates above. We only have
to provide the right loop invariants, and simple variations of the predicates to be
proved are sufficient. In check matching, we need additional loop invariants. Along
with the first loop, we accumulate the knowledge about the initialization of the
degree in M array by specifying that the first positions of the array have already
been set to 0:
    ∀ Nat u; u < v −→ degree in M[u] = 0

Moreover, on the second loop, we need three additional loop invariants. One in-
variant states that values stored in degree in M are in range:
    ∀ Nat v; v < M−>n −→ degree in M[v] ≤ 1

Another invariant states that vertices, for which degree in M is still 0, cannot be
part of any already checked edge:
    ∀ Nat v; v < M−>n ∧ degree in M[v] = 0 −→
       ∀ Nat e1; e1 < e −→ M−>es[e1].s 6= v ∧ M−>es[e1].t 6= v

Finally, vertices for which degree in M has already been set to 1 are mapped by a
ghost mapping E to their adjacent edge in the matching M:
    ∀ Vertex v; v < M−>n ∧ degree in M[v] = 1 −→
       E[v] < e ∧ (M−>es[E[v]].s = v ∨ M−>es[E[v]].t = v)

This invariant is required to prove completeness. We maintain this invariant by
updating the ghost mapping E in the loop body accordingly.
    Proving the weight function correct is the most intricate part of the checker
verification. There are two properties that need to be shown: functional correctness
and the absence of overflows. The former requires that the function computes the
26                                           E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


ni and the overall sum of Equation (2) correctly, as specified in the above fourth
conjunct of the witness predicate. The latter requires that the additions in both
the second and third loop do not overflow. Surprisingly, the absence of overflows
is much harder to establish than functional correctness.
    We concentrate first on functional correctness. The second loop updates the
count array in a way that maintains the following property:
     ∀ Nat j; j < r −→ count[j] = \label count(L, j, v)

From this property follows this loop invariant on the third loop:
     s = \full weight(L, G−>n, c − 1))

Together with a further loop invariant for the second loop to guarantee that max
is the greatest label seen so far, we can conclude that the weight function is func-
tionally correct.
    The addition in the second loop can never overflow because in each loop it-
eration, the loop variable is an upper limit on the value count[i] for each label i.
Concerning the addition in the third loop, we observe that in each loop iteration,
the value of s is bounded by the number of vertices in G. To establish this prop-
erty, we build up a ghost map sum in the second loop in such a way that in every
iteration of that loop, this map fulfills the following invariant:
     sum[1] = count[1] ∧
     (∀ Nat j; 1 < j ∧ j < r −→ sum[j] = sum[j − 1] + count[j]) ∧
     (∀ Nat j; 1 < j ∧ j < r −→ sum[j] ≤ v)

Maintaining this invariant requires updating the sum map during each iteration
of the second loop. We do so in a nested ghost loop in which we propagate the
increment that happened on the count array to every possibly affected element
sum[j].
    The postcondition of the checker expresses that the cardinality of any matching
of G cannot be smaller than the cardinality of M:
     ∀ \Graph M2; \Edge Map I2; \is subset(G, M2, I2) ∧ \is matching(M2) −→
        M2.num edges ≤ M.num edges

   We give a formal proof that the checker preconditions and the witness predicate
imply this property in the following section.

4.3.3 Proof of the Witness Property for the Maximum-Cardinality-Matching Checker

We explain the Isabelle proof for the witness property, i.e., for Theorem 2. See
Listing 11 for an excerpt of our formal Isabelle proof development that can be
found in file Matching.thy. The formal proof follows the scheme of the textbook
proof and is split into two main parts.
    For i ≥ 2, let Mi be the edges in M that connect two vertices labeled i, and
let M1 be the remaining edges in M . The setsSMi , i ≥ 1, are disjoint. We  P use the
definition of an odd-set cover to prove M ⊆ i≥1 Mi , and thus |M | ≤ i≥1 |Mi |
by disjointness of the sets Mi . Let Vi be the vertices labeled i, and let ni = |Vi |.
We formally prove: |M1 | ≤ n1 and |Mi | ≤ ⌊ni /2⌋.
    In order to prove |M1 | ≤ n1 , we exhibit an injective function from M1 to V1 .
We first prove, using the definition of an odd-set cover, that every edge e ∈ M1
has at least one endpoint in V1 . This gives rise to a function endpoint V1 that maps
A Framework for the Verification of Certifying Computations                           27


type synonym label = nat

definition disjoint-edges :: (α, β) pre-graph ⇒ β ⇒ β ⇒ bool where
   disjoint-edges G e1 e2 = (
       start G e1 6= start G e2 ∧ start G e1 6= target G e2 ∧
       target G e1 6= start G e2 ∧ target G e1 6= target G e2 )

definition matching :: (α, β) pre-graph ⇒ β set ⇒ bool where
   matching G M = (
       M ⊆ edges G ∧
       (∀e1 ∈ M . ∀e2 ∈ M . e1 6= e2 −→ disjoint-edges G e1 e2 ))

definition OSC :: (α, β) pre-graph ⇒ (α ⇒ label ) ⇒ bool where
   OSC G L = (
       ∀e ∈ edges G.
          L (start G e) = 1 ∨ L (target G e) = 1 ∨
          L (start G e) = L (target G e) ∧ L (start G e) ≥ 2)

definition weight :: label P
                           set ⇒ (label ⇒ nat ) ⇒ nat where
   weight LV f = f 1 + i ∈ LV . (f i) div 2

definition N :: α set ⇒ (α ⇒ label ) ⇒ label ⇒ nat where
   N V L i = card {v ∈ V . L v = i}

locale matching-locale = digraph +
   fixes maxM :: β set
   fixes L :: α ⇒ label
   assumes matching: matching G maxM
   assumes OSC: OSC G L
   assumes weight: card maxM = weight {i ∈ L ‘ verts G. i > 1} (N (verts G) L)


       Listing 11: Definitions and locale for the matching proof in Isabelle.




from M1 to V1 . We then use that edges in a matching do not share endpoints
(i.e., edges in a matching are disjoint when interpreted as sets) to conclude that
endpoint V1 is injective. This establishes |M1 | ≤ |Vi |.

    For i ≥ 2, the proof of the inequality |Mi | ≤ ⌊ni /2⌋ is similar but more involved.
Mi is a set of edges. If we represent edges as sets, each with cardinality    two, then
Mi is a collection of sets. We define the set of vertices Vi′ to be i≥2 Mi and use
                                                                       S

the definition of an odd-set cover to prove Vi′ ⊆ Vi . Since the edges in a matching
are pairwise disjoint, we obtain Vi′ = 2 · |Mi |. Note also that Vi′ must be even
since |Mi | is a natural number. Thus, we can prove that |Mi | ≤ Vi′ / 2 , and
hence, |Mi | ≤ Vi′ / 2 ≤ ⌊|Vi | / 2⌋ = ⌊ni /2⌋.

    Instantiating this Isabelle proof for the data structures and properties exported
from VCC is fairly straightforward since both formalizations have been chosen
intentionally close to each other. We prove by induction that N {0 ..< n} L l
equals \label count(L, l, n) for every label l. Moreover, we prove by induction that
weight {2 .. k} f equals \full weight(L, n, k) if f l and \label count(L, l, n) coincide.
After showing that |M | equals M.num edges, we can establish the witness property
for the matching checker.
28                                     E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


5 Evaluation

We have shown that our methodology allows us to lift the trustworthiness of
certifying algorithms to a new level: one can obtain formal instance correctness of
certifying algorithms. A certifying algorithm returns for any input x satisfying the
precondition ϕ a pair (y, w). It is accompanied by a witness predicate W and an
associated checker program C . If x satisfies the precondition, C is supposed to halt
on input (x, y, w) and decide on the witness predicate. We have shown in three cases
that checker correctness can be established formally using VCC. Precondition plus
witness predicate are supposed to imply the postcondition ψ . We have shown in
the same three cases that the witness property can be established formally using
Isabelle/HOL. In all cases, we followed the same approach: (1) write the checker in
C and annotate it so that VCC can establish that the checker decides the witness
property, (2) translate precondition, witness predicate, and postcondition from
VCC to Isabelle/HOL, and (3) prove the witness property in Isabelle/HOL and
add the VCC-version of it as an axiom to VCC. We translated manually from VCC
to Isabelle/HOL. Since the translation is purely syntactical, it can be automated.
    We believe that our approach would work for all certifying algorithms dis-
cussed in the survey on certifying algorithms [23]. This might require formalizing
the subject matter in Isabelle/HOL first. Our work profited from the recent for-
malization of graphs in Isabelle/HOL [30]. A similar effort would be necessary
before geometric or randomized algorithms can be tackled.
    It is always a gratifying experience to see that a formalization reveals gaps in
paper and pen reasoning. In our case, we found that the checker for a maximum
cardinality matching in LEDA does not verify that the computed matching M is
a subgraph of G.
    The matching algorithm for general graphs and its efficient implementation
are advanced topics in graph algorithms. The algorithm is highly complex and is
not covered in the standard textbooks on algorithms. The following page numbers
illustrate the complexity gap between the original algorithm and the checker: In
the LEDA book, the description of the algorithm for computing the maximum
cardinality matching and the proof of its correctness fills about 15 pages, compared
to a one-page description of the checker implementation.
    All described theorems and lemmas have been formally verified using VCC and
Isabelle/HOL. Table 1 summarizes our effort in lines of code, lines of annotations,
and lines of Isabelle specifications and proofs. We observe an average ratio of
2.5 for the VCC annotation overhead, which includes our specifications for the
witness predicates besides annotations for code verification. The overhead grows
to an average ratio of 6.7 when also considering our Isabelle proofs. We believe
that this overhead is a small price to pay for verifying full functional correctness
of code with nontrivial mathematical properties. Observe that the Isabelle linking
proofs are much shorter than the high-level proofs in the Isabelle locales for the
two more complex checkers. Linking proofs, hence, cause only a small overhead
and, as we found, are fairly straightforward. In our opinion, splitting the proofs
into high-level proofs for mathematical concepts and lower-level linking proofs
improved productivity and certainly helped to reduce the overall proof size and
effort. The overall VCC proof time for all checkers is 10 seconds on a 2.9 GHz Intel
Core i7 machine. The overall Isabelle proof time is also well below one minute on
the same machine.
A Framework for the Verification of Certifying Computations                                29

                                              VCC                       Isabelle
                              C code       Annotations        Exports    Locales   Links

   Connected components          61            162              63        102      163
   Shortest paths               107            318             109        279      198
   Matching                     124            263              78        318      164


Table 1: Lines of C code, annotations for VCC, and Isabelle declarations and
proofs, excluding empty lines in all cases. For the latter, we give the numbers for
the specifications exported from VCC, abstract proofs performed within locales,
and proofs that link the concrete representation exported from VCC with the
abstract proofs separately.


    It took several months to develop the framework and complete the first example
as described in [1]. For this paper, we have reworked the framework, thereby
strengthening and simplifying it at the same time. We now prove total correctness
of the checkers and not only partial correctness. Moreover, we now establish that
the checker accepts a triple (x, y, w) if and only if w is a valid witness for output y ,
whereas previously, we only proved one direction. The simplification results from
dropping concrete specifications in VCC. Moreover, a new version of VCC has
allowed for shorter specifications and proofs.
    Our methodology is not confined to verifying certifying computations only.
Rather, any proposition that VCC fails to establish can be exported to Isabelle
and proved there; see [7, Section 4.5] for an example. Hence, our methodology
extends the applicability of VCC and allows, in conjunction with Isabelle, the
verification of complicated problems that were infeasible up to now.


6 Related Work

The notion of a certifying algorithm is ancient. Al-Khawarizmi already described
how to (partially) check the correctness of a multiplication in his book on algebra.
The extended Euclidean algorithm for greatest common divisors is also certifying;
it dates back to the 17th century. Yet, formal verification of checkers is recent.
    In 1997, Bright et al. [11] verified a checker for a sorting algorithm that has
been formalized in the Boyer-Moore theorem prover [10]. De Nivelle and Piskac
formally verified the checker for priority queues implemented in LEDA [27]. Bul-
wahn et al. [12] describe a verified SAT checker, i.e., a checker for certificates of
unsatisfiability produced by a SAT solver. They develop the checker and prove
its correctness within Isabelle/HOL. Similar proof checkers have been formalized
in the Coq [5] proof assistant [15, 2]. CeTA [37], a tool for certified termination
analysis, is also based on formally verified checkers. In contrast to our approach,
all mentioned checkers are entirely developed and verified within the language of
a theorem prover.
    VCC has been applied to verify tens of thousands of lines of C code. So far,
the majority of its verification targets have been restricted to system-level code
from the domain of microkernels and hypervisors [4, 21, 35]. Our work extends the
range of VCC applications to graph algorithms and, in general, to any code that
requires nontrivial mathematical reasoning to establish full functional correctness.
30                                     E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


    In contrast to using an automatic program verifier such as VCC as we did,
imperative code can also be verified in interactive theorem provers such as Coq,
HOL [19], or Isabelle/HOL. This requires a formalization of the imperative lan-
guage and its semantics within the theorem prover. Charguéraud describes a tool,
CFML, that is based on the idea of extracting characteristic formulae from pro-
grams [13]. CFML is embedded in Coq and targets imperative Caml programs. It
has been applied to verify imperative data structures such as mutable lists, sparse
arrays and union-find. Norrish presented a formal semantics of C formalized in
the HOL theorem prover [29]. Parallel to this work, a subset of C, called C0, was
formalized in Isabelle/HOL [22]. Schirmer developed a verification environment
for sequential imperative programs within Isabelle and embedded C0 into this en-
vironment [34]; his verification environment is written in the generic imperative
programming language Simpl. Shirmer’s work has been applied, for instance, to
verify a compiler for C0 [31]. More recently, the seL4 microkernel, written in C, has
been verified in Isabelle/HOL [21] based on the work of Norrish and Schirmer. The
underlying approach is refinement; one verifies an intermediate implementation in
Haskell against the abstract specification, then generates C code from the Haskell
code using a verified generator. The reverse process of turning C code into a hu-
man readable abstraction can partly be automated [20]. The latter work opens up
an alternative path for the verification of certifying computations. One writes the
checker in C, uses the trusted translation to obtain an equivalent Simpl program,
and then proves checker correctness and the witness property in Isabelle/HOL. We
plan to also try this alternative route. There are advantages and disadvantages for
both approaches, and it is too early to claim the superiority of one approach over
the other. An advantage of our current approach is that we annotate the source
program; a disadvantage is that we use two tools. An advantage of the alternative
approach is that only one tool is used; the disadvantage then is that one can-
not argue about the source program but rather about a program obtained by a
translation process.

    Previous work that proposes, as we do, the use of interactive theorem provers
as backends to code verification systems comprises, for instance, the link between
Boogie and Isabelle/HOL [9] and the link between Why and Coq [17]. Both systems
have a C verifier frontend. Such approaches for connecting code verifiers and proof
assistants usually give the latter the same information that is made available to
the first-order engine, overwhelming the users of the proof assistants with a mass
of detail. Instead, we allow only clean chunks of mathematics to move between
the verifier and the proof assistant. This hides details of the underlying program-
ming languages from the proof assistant, thus requiring the user to discharge only
interesting proof obligations.

    Shortest-path algorithms, especially imperative implementations thereof, are
popular as case studies for demonstrating code verification [13, 28, 8]. They target
full functional correctness as opposed to instance correctness. Verifying instance
correctness is orthogonal to verifying the implementation of a particular shortest
path algorithm. Our work is directly applicable to any implementation of shortest-
path that is instrumented to provide the necessary witness expected by our checker.

   To our knowledge, there has been no other attempt to verify algorithms or
checkers for connected components or maximum cardinality matchings.
A Framework for the Verification of Certifying Computations                                 31


7 Conclusion and Future Work

We have described a framework for the verification of certifying computations
and applied it to three nontrivial combinatorial problems: connectivity of graphs,
shortest paths in graphs, and maximum cardinality matchings in graphs. Our work
greatly increases the trustworthiness of certifying algorithms.
    Specifically, for each instance of the considered three problems, we can now
give a formal proof of the correctness of the result. Thus, the user has neither to
trust the implementation of the original algorithm nor the checker, nor does he
have to understand why the witness property holds. We stress that we did not
prove the correctness of the original programs but only verified the results of their
computations.
    Our methodology can be applied to any other problem for which a certifying
algorithm is known; see [23] for a survey. The fourth author is currently verifying
a checker for shortest paths with arbitrary edge costs [33], and Lars Noschinski is
verifying a checker for graph non-planarity testing.
    Our methodology is not restricted to verifying certifying computations. The
integration of VCC and Isabelle/HOL should be useful whenever verification of a
program requires nontrivial mathematical reasoning.

Acknowledgements We thank Ernie Cohen for his advice on VCC idioms, Mark Hillebrand
for insightful discussions on VCC, and Norbert Schirmer for his initial Isabelle support. More-
over, we thank Lars Noschinski for developing a powerful graph library in Isabelle/HOL. We
are grateful to Jasmin Christian Blanchette for providing useful comments on an earlier version
of this article.



References

 1. Alkassar, E., Böhme, S., Mehlhorn, K., Rizkallah, C.: Verification of certifying computa-
    tions. In: Computer Aided Verification, Lecture Notes in Computer Science, vol. 6806,
    pp. 67–82. Springer (2011)
 2. Armand, M., Grégoire, B., Spiwack, A., Théry, L.: Extending Coq with imperative features
    and its application to SAT verification. In: Interactive Theorem Proving, Lecture Notes
    in Computer Science, vol. 6172, pp. 83–98. Springer (2010)
 3. Barnett, M., Chang, B.Y.E., DeLine, R., Jacobs, B., Leino, K.R.M.: Boogie: A modular
    reusable verifier for object-oriented programs. In: Formal Methods for Components and
    Objects, Lecture Notes in Computer Science, vol. 4111, pp. 364–387. Springer (2006)
 4. Baumann, C., Beckert, B., Blasum, H., Bormer, T.: Formal verification of a microker-
    nel used in dependable software systems. In: Computer Safety, Reliability, and Security,
    Lecture Notes in Computer Science, vol. 5775, pp. 187–200. Springer (2009)
 5. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development—
    Coq’Art: The Calculus of Inductive Constructions. Texts in Theoretical Computer Science.
    An EATCS Series. Springer (2004)
 6. Blum, M., Kannan, S.: Designing programs that check their work. In: Symposium on
    Theory of Computing, pp. 86–97. ACM (1989)
 7. Böhme, S.: Proving theorems of higher-order logic with SMT solvers. Ph.D. thesis, Tech-
    nische Universität München (2012)
 8. Böhme, S., Leino, K.R.M., Wolff, B.: HOL-Boogie—An interactive prover for the Boogie
    program-verifier. In: Theorem Proving in Higher Order Logics, Lecture Notes in Computer
    Science, vol. 5170, pp. 150–166. Springer (2008)
 9. Böhme, S., Moskal, M., Schulte, W., Wolff, B.: HOL-Boogie—an interactive prover-
    backend for the Verifying C Compiler. Journal of Automated Reasoning 44(1–2), 111–144
    (2010)
32                                             E. Alkassar, S. Böhme, K. Mehlhorn, C. Rizkallah


10. Boyer, R.S., Moore, J.S.: A theorem prover for a computational logic. In: Conference on
    Automated Deduction, Lecture Notes in Computer Science, vol. 449, pp. 1–15. Springer
    (1990)
11. Bright, J.D., Sullivan, G.F., Masson, G.M.: A formally verified sorting certifier. IEEE
    Transactions on Computers 46(12), 1304–1312 (1997)
12. Bulwahn, L., Krauss, A., Haftmann, F., Erkök, L., Matthews, J.: Imperative functional
    programming with Isabelle/HOL. In: Theorem Proving in Higher Order Logics, Lecture
    Notes in Computer Science, vol. 5170, pp. 134–149. Springer (2008)
13. Charguéraud, A.: Characteristic formulae for the verification of imperative programs. In:
    International Conference on Functional Programming, pp. 418–430. ACM (2011)
14. Cohen, E., Dahlweid, M., Hillebrand, M., Leinenbach, D., Moskal, M., Santen, T., Schulte,
    W., Tobies, S.: VCC: A practical system for verifying concurrent C. In: Theorem Proving
    in Higher Order Logics, Lecture Notes in Computer Science, vol. 5674, pp. 23–42. Springer
    (2009)
15. Darbari, A., Fischer, B., Marques-Silva, J.: Industrial-strength certified SAT solving
    through verified SAT proof checking. In: Theoretical Aspects of Computing, Lecture Notes
    in Computer Science, vol. 6255, pp. 260–274. Springer (2010)
16. Edmonds, J.: Maximum matching and a polyhedron with 0,1-vertices. Journal of Research
    of the National Bureau of Standards 69B, 125–130 (1965)
17. Filliâtre, J.C., Marché, C.: The Why/Krakatoa/Caduceus platform for deductive program
    verification. In: Computer Aided Verification, Lecture Notes in Computer Science, vol.
    4590, pp. 173–177. Springer (2007)
18. Gordon, M., Milner, R., Wadsworth, C.P.: Edinburgh LCF: A Mechanised Logic of Com-
    putation, Lecture Notes in Computer Science, vol. 78. Springer (1979)
19. Gordon, M.J.C., Melham, T.F. (eds.): Introduction to HOL: A Theorem-Proving Envi-
    ronment for Higher-Order Logic. Cambridge University Press (1993)
20. Greenaway, D., Andronick, J., Klein, G.: Bridging the gap: Automatic verified abstraction
    of C. In: Interactive Theorem Proving, Lecture Notes in Computer Science, vol. 7406, pp.
    99–115. Springer (2012)
21. Klein, G., Andronick, J., Elphinstone, K., Heiser, G., Cock, D., Derrin, P., Elkaduwe, D.,
    Engelhardt, K., Kolanski, R., Norrish, M., Sewell, T., Tuch, H., Winwood, S.: seL4: Formal
    verification of an operating-system kernel. Communications of the ACM 53(6), 107–115
    (2010)
22. Leinenbach, D., Paul, W.J., Petrova, E.: Towards the formal verification of a C0 compiler:
    Code generation and implementation correctness. In: Software Engineering and Formal
    Methods, pp. 2–12. IEEE Computer Society (2005)
23. McConnell, R.M., Mehlhorn, K., Näher, S., Schweitzer, P.: Certifying algorithms. Com-
    puter Science Review 5(2), 119–161 (2011)
24. Mehlhorn, K., Näher, S.: The LEDA Platform for Combinatorial and Geometric Comput-
    ing. Cambridge University Press (1999)
25. de Moura, L.M., Bjørner, N.: Z3: An efficient SMT solver. In: Tools and Algorithms for
    the Construction and Analysis of Systems, Lecture Notes in Computer Science, vol. 4963,
    pp. 337–340. Springer (2008)
26. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL — A Proof Assistant for Higher-
    Order Logic, Lecture Notes in Computer Science, vol. 2283. Springer (2002)
27. de Nivelle, H., Piskac, R.: Verification of an off-line checker for priority queues. In: Software
    Engineering and Formal Methods, pp. 210–219. IEEE Computer Society (2005)
28. Nordhoff, B., Lammich, P.: Dijkstra’s shortest path algorithm. Archive of Formal Proofs
    2012 (2012). http://afp.sourceforge.net/entries/Dijkstra_Shortest_Path.shtml
29. Norrish, M.: C formalised in HOL. Ph.D. thesis, Computer Laboratory, University of
    Cambridge (1998)
30. Noschinski, L.: A formalization of graphs in Isabelle/HOL (2011). Ongoing work, available
    from author upon request
31. Petrova, E.: Verification of the C0 compiler implementation on the source code level. Ph.D.
    thesis, Saarland University, Saarbrücken (2007)
32. Rizkallah, C.: Maximum cardinality matching. Archive of Formal Proofs 2011 (2011).
    http://afp.sourceforge.net/entries/Max-Card-Matching.shtml
33. Rizkallah,         C.:      An        axiomatic         characterization        of       shortest-
    path        in     Isabelle/HOL       (2012).               Formal       proof     development,
    http://www.mpi-inf.mpg.de/~ crizkall/Publications/shortest_path.pdf
A Framework for the Verification of Certifying Computations                                   33


34. Schirmer, N.: Verification of sequential imperative programs in Isabelle/HOL. Ph.D. thesis,
    Technische Universität München (2006)
35. Shi, J., He, J., Zhu, H., Fang, H., Huang, Y., Zhang, X.: ORIENTAIS: Formal verified
    OSEK/VDX real-time operating system. In: Engineering of Complex Computer Systems,
    pp. 293–301. IEEE Computer Society (2012)
36. Sullivan, G.F., Masson, G.M.: Using certification trails to achieve software fault tolerance.
    In: Fault-Tolerant Computing, pp. 423–431. IEEE Computer Society (1990)
37. Thiemann, R., Sternagel, C.: Certification of termination proofs using CeTA. In: Theorem
    Proving in Higher Order Logics, Lecture Notes in Computer Science, vol. 5674, pp. 452–
    468. Springer (2009)
38. Verisoft XT. http://www.verisoftxt.de (2010)
