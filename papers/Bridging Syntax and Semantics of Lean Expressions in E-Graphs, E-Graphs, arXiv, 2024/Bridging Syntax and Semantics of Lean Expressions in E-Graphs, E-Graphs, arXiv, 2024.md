                                         Bridging Syntax and Semantics of Lean Expressions in
                                         E-Graphs
arXiv:2405.10188v1 [cs.SC] 16 May 2024




                                         MARCUS ROSSEL, Chair for Compiler Construction, TU Dresden, Germany
                                         ANDRÉS GOENS, University of Amsterdam, Netherlands

                                         Interactive theorem provers, like Isabelle/HOL, Coq and Lean, have expressive languages that allow
                                         the formalization of general mathematical objects and proofs. In this context, an important goal
                                         is to reduce the time and eﬀort needed to prove theorems. A signiﬁcant means of achieving this
                                         is by improving proof automation. We have implemented an early prototype of proof automation
                                         for equational reasoning in Lean by using equality saturation.1 To achieve this, we need to bridge
                                         the gap between Lean’s expression semantics and the syntactically driven e-graphs in equality
                                         saturation. This involves handling bound variables, implicit typing, as well as Lean’s deﬁnitional
                                         equality, which is more general than syntactic equality and involves notions like 𝛼-equivalence,
                                         𝛽-reduction, and 𝜂-reduction. In this extended abstract, we highlight how we attempt to bridge
                                         this gap, and which challenges remain to be solved. Notably, while our techniques are partially
                                         unsound, the resulting proof automation remains sound by virtue of Lean’s proof checking.

                                         1 OVERVIEW OF THE PROOF TACTIC
                                         We start with a brief overview of how we use equality saturation [8] with Lean [3] by connecting
                                         it to egg [9]. The setup, sketched in Figure 1, is both based on and extends the tactic described
                                         in [5].

                                                                               Goal Equation                     Goal Expressions
                                                            egg Tactic                                                                         egg
                                                                               Equational Theorems               Rewrites

                                                               Proof                                                                      Explanation

                                                                                Fig. 1. Overview of the egg proof tactic.

                                           Expressions. Lean is based [1] on the calculus of constructions [2], which is an expressive, dependently-
                                         typed 𝜆 calculus. In this calculus, data types and their values, as well as propositions and proofs
                                         are all terms of the same expression language:
                                                                            e ::= 𝑛ˆ | 𝑒 𝑒 | 𝜆𝑒, 𝑒 | ∀𝑒, 𝑒         where 𝑛 ∈ N
                                            It contains abstraction at the term and type level (𝜆 and ∀), based on de Bruijn indices (𝑛),
                                                                                                                                      ˆ and
                                         function application.2 The expression appearing directly after a binder provides the type of the
                                         bound variable 0̂. All terms in Lean are lowered to expressions of this language at elaboration
                                         (compile) time. Thus, to use Lean terms in egg, we directly encode this expression language in egg.
                                         When the speciﬁc representation of expressions is not important, we often write 𝜆-expressions
                                         with named variables and without explicit binder types in subsequent sections. Also, we often use
                                         the terms “term” and “expression” interchangeably.
                                         1 https://github.com/marcusrossel/lean-egg
                                         2 This is a simpliﬁcation of Lean’s expression language, to simplify the presentation of key aspects in this extended abstract.


                                         Authors’ addresses: Marcus Rossel, marcus.rossel@tu-dresden.de, Chair for Compiler Construction, TU Dresden, Germany;
                                         Andrés Goens, a.goens@uva.nl, University of Amsterdam, Netherlands.
2                                                                                   Marcus Rossel and Andrés Goens

   Proof Tactics. Proofs in Lean are seldom written as explicit expressions of the given 𝜆 calculus.
Instead, they are built by calling a sequence of proof tactics, which are small (meta-)programs that
construct the relevant proof terms. For example, the rfl tactic solves proof goals of the form 𝑥 = 𝑦,
if 𝑥 and 𝑦 are (deﬁnitionally) equal.3 The tactic rewrite [eqn1, eqn2, ...] rewrites the proof goal by
applying each given equational theorem once. We implement our proof automation as a tactic
egg [eqn1, eqn2, ...] , which solves proof goals of the form 𝑥 = 𝑦 by having egg ﬁnd a sequence of
given rewrites which transform 𝑥 to 𝑦.
   Proof Generation. One of the key properties of theorem provers like Lean is the LCF architec-
ture [6], where proofs are checked for correctness by a small trusted kernel of code assumed to be
correct. Thus, proof automation tools can play fast and loose without compromising soundness
of the system, as incorrect proofs will not be accepted by the kernel. This comes at the cost of
automated proof tools, like egg, having to generate proof witnesses for their results. Additionally,
these witnesses need to be converted into a format which Lean understands. Luckily, egg supports
generating explanations which can be expressed as linear sequences of rewrites. These rewrites
are then (more or less) easily converted into valid proofs in Lean.

2     THE (LACK OF) PROBLEMS WITH BINDERS
The choice of directly using Lean’s expression language in egg may raise immediate concerns
to some readers. Scalably representing 𝜆 calculus in e-graphs is notoriously diﬃcult due to the
presence of binders. Binders make it necessary to consider expressions in context instead of purely
syntactically. For example, when using de Bruijn indices, the expression 1̂ refers to a free variable
in 𝜆 1̂, but to a bound variable in 𝜆𝜆 1̂. The problem persists when using named variables where
𝑥 refers to a free variable in 𝜆𝑦, 𝑥 — but to a bound variable in 𝜆𝑥, 𝑥. Thus, directly representing
variables in e-graphs causes three classes of problems:

2.1    Free Variable Rebinding
The ﬁrst class of problems is well-known in 𝜆 calculus. When a term is rewritten, the resulting
substitutions may cause free variables to turn into bound variables – that is, they may be invalidly
captured by a binder. For example, if we apply the rewrite ?𝑥 ↦→ (𝜆 ?𝑥) 0 to the expression 𝜆 0̂, we
get the non-equivalent 𝜆((𝜆 0̂) 1).4 Notably, free variables can also become invalidly “un-captured”.
For example, if we apply the rewrite 𝜆(𝜆 ?𝑥) 0 ↦→ 𝜆 ?𝑥 to the open term 𝜆(𝜆 4̂) 0, we get the non-
equivalent 𝜆 4̂. Here, 4̂ would need to be shifted to 3̂ to retain its semantics. Both of these prob-
lems can be avoided by having every rewrite be a dynamic rewrite which checks whether a given
matched pattern variable refers to free variables, and if so, shifts them as needed. Checking for free
variables can be done eﬃciently by using an e-class analysis. Shifting variables, on the other hand,
is rather involved as it needs to be performed on the results of e-matching which are e-classes
instead of expressions. A procedure for this is discussed in Section 4.

2.2    Invalid Matching
The second class of problems is invalid matching of pattern variables against (1) syntactically equal
but semantically diﬀerent variables and (2) “locally bound” variables. An example of (1) occurs
when the pattern term 𝜆(𝜆 ?𝑥) ?𝑥 is matched against 𝜆(𝜆 0̂) 0̂. Here, the matched variables 0̂ refer
to diﬀerent variables, even though they are syntactically equal. An example of (2) occurs when
the rewrite (𝜆 ?𝑥) 1 ↦→ ?𝑥 is applied to (𝜆 0̂) 1, which produces the non-equivalent term 0̂. The

3We explain the notion of deﬁnitional equality in Section 3.
4 In this example, even though 0̂ appears under a binder, it is a free variable with respect to the left-hand side of the rewrite.
Bridging Syntax and Semantics of Lean Expressions in E-Graphs                                                            3

reason this fails is that the given rewrite is valid only when ?𝑥 is not bound.5 As ?𝑥 appears under
one binder in the trigger pattern, any matched variable with index < 1 is bound in the context
of the trigger pattern (we call this locally bound) and therefore invalid. Invalid matching is easily
avoided with dynamic rewrites which check for occurrences of (1) and (2) by a traversal of the
trigger pattern. If any pattern variable maps to a variable and appears under multiple diﬀerent
binders, we have case (1). If a pattern variable at binder depth 𝑑 maps to a variable whose index is
smaller than 𝑑, we have case (2). In either case, the rewrite is aborted.

2.3 Bound Variable Aliasing
A more fundamental problem with direct representation of variables is invalid aliasing. This occurs
when diﬀerent expressions use the same bound variable name, which is necessarily the case for de
Bruijn indices. For example, in an e-graph with expressions 𝜆 0̂ + 1 and 𝜆 ¬0̂, the same e-node for 0̂
is used by both expressions. Thus, any term shown equivalent to 0̂ in one expression automatically
becomes equivalent in both. This can easily become a problem in implicitly-typed languages like
Lean’s expression language. For example, if we rewrite 0̂ to 1 · 0̂ in the ﬁrst expression, then as a
result of aliasing the second one represents the term 𝜆 ¬(1 · 0̂), which is ill-typed.
   We believe the problem of bound variable aliasing to be partially solvable by adding explicit
type annotations to all terms. This directly solves aliasing of variables with diﬀerent types, as they
become syntactically distinct. It, thus, suﬃces to show that aliasing is a non-issue for variables of
the same type. While we do not have proof of this, we have an argument which relies on the fact
that expressions which are equivalent to variables must be equivalent in all contexts. Thus, one
only needs to consider what happens to the variables of terms which become equivalent to an-
other variable, as they can be invalidly un-/captured. We think that these scenarios are all benign,
though. A major caveat to this approach comes from the fact that adding explicit type annotation
might be non-trivial. As types in Lean can be parameterized, type annotations themselves may
need to contain variables. Thus, our argument may only apply to settings where all type are un-
parameterized. We have not found this to be an issue in practice, in any of the examples we have
seen so far.

3   SEMANTICS OF EQUALITY
Even if we ignore the problems of binders, Lean’s expression language does not naturally collabo-
rate with e-graphs’ syntax-driven approach to rewrites. In an e-graph, two expressions are equal
a priori only if they are syntactically equal. In Lean, expressions are equal a priori if they satisfy
a certain deﬁnitional equality relation (≡). For example, (𝜆 𝑥, 𝑥 + 0) 1 = 1 holds by reﬂexivity in
Lean, but is not provable without rewrites in an e-graph. This diﬀerence requires consideration
as it means that we might not identify a goal as being proven during equality saturation, simply
because we could only reach a term which was deﬁnitionally but not syntactically equal to the
goal. It also has eﬀects on how rewrites can be applied in Lean as compared to an e-graph. If we
have a rewrite like (𝜆 𝑙, 𝑙 + 1) 𝑙 1 = (𝜆 𝑙, 𝑙 + 1) 𝑙 2 , we cannot use it to prove 𝑙 1 + 1 = 𝑙 2 + 1 by equal-
ity saturation, as the rewrite does not match any goal term. To overcome these diﬀerences, we
add rewrites which allow conversion between diﬀerent deﬁnitionally equal representations of the
same expression. Some rules of deﬁnitional equality are already intrinsic to e-graphs and do not
require rewrites. Namely, those which express that deﬁnitional equality is an equivalence relation
which is a congruence with respect to application, and abstraction. All other forms of deﬁnitional
equality require various techniques outlined below.
5 All rewrites where the trigger pattern contains binders are valid only if pattern variables are not matched against bound

variables of those binders.
4                                                                                  Marcus Rossel and Andrés Goens

  Normalization. Some deﬁnitional equalities can be achieved by eliminating certain syntactic
constructs from all expressions – that is, by partially normalizing expressions. For example, Lean
has a notion of let-expressions in its language with a corresponding deﬁnitional equality rule. We
avoid this rule by completely reducing let-expressions (this is called 𝜁 -reduction) before equality
saturation. Thus, the expression language used in the e-graph has no concept of let-expressions,
making their deﬁnitional equality rules irrelevant.
  Erasure. Lean has a rule known as proof irrelevance which states that all proofs of the same
proposition are deﬁnitionally equal. We overapproximate this rule and make all proofs equal in an
e-graph by erasing proof terms completely. That is, if we encounter a proof term while encoding a
Lean expression to be used in an e-graph, we replace it by some constant symbol 𝜖. Reconstructing
these erased terms then requires additional work during proof generation in Lean. We are so far
unsure if there are cases where erased proof terms cannot be completely reconstructed.
  Dynamic Rewrites. The deﬁnitional equality rules 𝛽 and 𝜂 establish relationships between appli-
cation, abstraction and substitution.
                                                        0̂ ∉ fvars(𝑒)
                                 ′            ′
                                                 (𝛽)                   (𝜂)
                        (𝜆𝛼, 𝑒) 𝑒 ≡ 𝑒 [0̂ ↦→ 𝑒 ]       (𝜆𝛼, 𝑒 0̂) ≡ 𝑒
   When working with de Bruijn indices, both 𝛽- and 𝜂-reduction necessitate shifting indices of
free variables. Namely, in the case of 𝜂, the expression 𝜆 𝑒 0̂, is only equivalent to the 𝜂-reduced 𝑒
if all free variables in 𝑒 are shifted down by 1. This is necessary as we remove one binder above
𝑒. For 𝛽-reduction, the reduced expression 𝑓 [0̂ ↦→ 𝑒] also requires shifting all free variables in 𝑓
down by 1 as we again remove one binder above 𝑓 . Additionally, all free variables in 𝑒 need to
be shifted up by the number of binders appearing above the corresponding occurrence of 0̂ in 𝑓 .
This is necessary to compensate for the fact that we are (potentially) adding binders above 𝑒. Thus,
to encode 𝛽- and 𝜂-reduction we need dynamic rewrites. We start by implementing shifting of
variables which can be generalized to substitution of variables with constant expressions.6 Notably,
we cannot simply implement this function over expressions, but must implement it on e-classes,
as e-matching does not yield expressions but only e-classes. The required function subst can thus
be described as follows. Let 𝜎 : N × N → expr be a substitution mapping from a variable index
and binder depth to an expression. Let 𝑔 be an e-graph containing an e-class 𝑐. Then subst(𝑔, 𝑐, 𝜎)
extends 𝑔 with an e-class 𝑠 such that for every expression 𝑒 represented by 𝑐, 𝑠 represents 𝜎 ′ (𝑒).
We use 𝜎 ′ to denote the lifting of 𝜎 to apply to expressions with the binder depth being derived
starting at 𝑐. Using subst we can deﬁne 𝜂- and 𝛽-reduction entirely based on the choice of 𝜎.7
                                    eta(𝑔, 𝑐) := subst(𝑔, 𝑐, 𝜎± (−1))
                            beta(𝑔, 𝑐, arg) := subst(𝑔, 𝑐, 𝜎 𝛽 (arg))
                                               (
                                                  
                                                 idx + oﬀ if idx > depth
                       𝜎± (oﬀ ) (idx, depth) := c
                                                 idx          otherwise
                                                
                                                  
                                                  idx −1                               if idx > depth
                                                
                                                
                                                
                                                   c
                       𝜎 𝛽 (arg) (idx, depth) := idx                                   if idx < depth
                                                
                                                
                                                 subst(𝑔, arg, 𝜎± (depth))            if idx = depth
                                                

6We mean constant in the sense that the substituted expression will be inserted as is.
7 The last case in 𝜎
                  𝛽 returns an e-class instead of just a single expression. This does not match our deﬁnition of a substitution,
but subst can easily be adapted to handle this, too.
Bridging Syntax and Semantics of Lean Expressions in E-Graphs                                        5

   We can then construct dynamic rewrites for 𝛽- and 𝜂-reduction by e-matching on their respec-
tive pattern expressions, performing beta or eta on the e-class of the matched variable, and ﬁnally
forming the union of the resulting e-class with the pattern expression’s e-class. The implementa-
tion of subst is discussed in Section 4.

4   SUBSTITUTION ON E-CLASSES
Substitution on e-classes is another notoriously diﬃcult problem with diﬀerent solutions.
    (1) Make substitution an explicit constructor of the expression language and introduce rewrites
        which encode its semantics (with respect to other constructors), as described in [9].
    (2) Perform substitution by extracting a single expression 𝑒 from the e-class and performing
        substitution on 𝑒 before adding it back into the e-graph, as described in [4].
    (3) Traverse the subgraph of the target e-class and construct an equivalent subgraph where all
        relevant nodes are substituted.
   As (1) introduces subtleties with respect to correctly handling rewrite rules and makes scaling
harder by increasing the e-graph [4], and (2) lacks completeness by potentially never extracting all
represented expressions, we choose (3) for our implementation of the subst function. Recall that
our goal is for subst(𝑔, 𝑐, 𝜎) to extend the e-graph 𝑔 with an e-class 𝑠 such that for every expression
𝑒 represented by e-class 𝑐, 𝑠 represents 𝜎 ′ (𝑒) where 𝜎 : N × N → expr is a substitution mapping
from a variable index and binder depth to an expression. Thus, our approach is to traverse the
subgraph of 𝑐 and in the process construct a new e-class 𝑠 where variable nodes are substituted
according to 𝜎. Traversal of an e-graph rooted at a given e-class really means two kinds of traversal.
First, we must traverse all e-nodes in the e-class and, second, we must traverse all children of each
e-node. For this, we use a basic recursive depth-ﬁrst traversal which additionally iterates over each
e-node of a given e-class on visit. As e-graphs can contain cycles, we make sure to avoid inﬁnite
recursion by remembering which e-classes have already been visited. Problems then only arise
once we try to replace variable e-nodes with new e-nodes.
   E-Class Creation. The fundamental problem with replacing e-nodes is that it can only be done
bottom-up. For example, let 𝑐 1 be an e-class containing an e-node 𝑛 1 with child e-class 𝑐 2 con-
taining an e-node 𝑛 2 , etc, until ﬁnally 𝑛𝑘 is a terminal e-node. Then consider how to construct
the substituted e-class 𝑠 1 which represents the same terms as 𝑐 1 , but with 𝑛𝑘 replaced by some
other term 𝑚𝑘 . Intuitively, we might ﬁrst construct a new empty e-class for 𝑠 1 , then (recursively)
construct the substituted e-class 𝑠 2 and ﬁnally add e-node 𝑛 1 with new child 𝑠 2 into 𝑠 1 . Unfortu-
nately, we cannot construct empty e-classes and instead can only create new e-classes starting at
leaf nodes. Thus, we instead need to ﬁrst traverse all the way down to 𝑛𝑘 , create the new e-class
for 𝑚𝑘 , and then start constructing the new e-classes 𝑠𝑖 bottom-up. While this is arguably just as
simple as the “intuitive” approach, it breaks when the e-graph has a cycle. Namely, when we reach
an e-class 𝑐 which has been visited before, 𝑐 may not yet have an associated substituted e-class,
as potentially none of its child e-classes have completed substitution yet. Thus, we run into a sit-
uation akin to a deadlock, where in order to construct the substituted version 𝑠 of 𝑐, we need to
construct a substituted e-node which itself depends on 𝑠. Deciding how to continue the traversal
in that case is the key aspect of our substitution algorithm.
   Cycle Breaking. To break cyclic dependencies encountered during e-class creation, we rely on
an important cycle breaking property of e-graphs. Every cycle in an e-graph contains at least one
e-node 𝑛 where each child e-class of 𝑛 is either (1) the root of an acyclic subgraph or (2) the root
of a subgraph satisfying the cycle breaking property. Intuitively, this corresponds to the fact that
an e-graph can never contain an e-class which does not represent any (ﬁnite) term. This property
6                                                                               Marcus Rossel and Andrés Goens

holds trivially for an empty e-graph and is preserved under adding expressions. Thus, in a proof,
it suﬃces to show that it is also preserved under e-class merging. Based on the cycle breaking
property, our substitution algorithm resolves cyclic dependencies using an approach similar to
data driven scheduling in process networks [7].
   Let 𝑛 be an e-node for which we are trying to construct a substitute by recursively calling subst
on its child e-classes. If a child 𝑐 𝑖 has already been visited but does not yet have a substitute e-class
(that is, if we have encountered a cycle in the e-graph), then subst returns a failure value for 𝑐 𝑖 .
We record the failed child e-classes in a set C. If C = ∅, then we can immediately construct a
substitute for 𝑛 based on the substituted children. If C ≠ ∅, we record the fact that 𝑛 has not yet
been substituted and is waiting for the e-classes in 𝐶. The waiting e-nodes are then reconsidered
whenever a new substitute e-class is created. Speciﬁcally, we check whether any waiting e-node’s
dependencies have all been substituted, and, if so, construct the e-node’s substitute. Thus, by the
cycle breaking property, all waiting e-nodes will at some point be substituted.
   A major caveat to our algorithm is that we do not yet know how to properly handle justiﬁcations
(used for explanations). Thus, while the algorithms is perfectly suitable for applications which
trust egg, it sometimes falls short for our proof automation purposes by losing crucial rewrite
steps needed for proof reconstruction.

5   CONCLUSION
The semantics of Lean expressions rely on context-dependent constructs like binders and deﬁni-
tional equality, while rewriting in equality saturation is chieﬂy syntactic. This diﬀerence can lead
to rewrites applying when they should not (by invalid matching and bound variable aliasing), as
well as rewrites not applying when they should (by deﬁnitional but not syntactic equality). Various
approaches can be used to bridge this gap. Normalization of expressions, term erasure and dynamic
rewrites resolve diﬀerent deﬁnitional equalities. Dynamic rewriting based on free variable analy-
sis inhibits invalid matching and variable capture. Additionally, explicit type annotations could
restrict invalid bound variable aliasing. A common denominator between many dynamic rewrites
is their need for substitution, for which we have shown one approach by means of e-graph traver-
sal. Most of the given approaches are implemented as part of a proof tactic in Lean which uses egg
as an automated procedure for equational reasoning. Preliminary tests show that these techniques
are promising for this use case.

REFERENCES
[1] Carneiro, M. Lean4lean: Towards a formalized metatheory for the lean theorem prover. arXiv preprint
    arXiv:2403.14064 (2024).
[2] Coqand, T., and Huet, G. The calculus of constructions. Information And Computation 76, 2-3 (1988).
[3] de Moura, L., and Ullrich, S. The lean 4 theorem prover and programming language. In Automated Deduction–
    CADE 28: 28th International Conference on Automated Deduction, Virtual Event, July 12–15, 2021, Proceedings 28 (2021),
    Springer, pp. 625–635.
[4] Koehler, T. A domain-extensible compiler with controllable automation of optimisations. PhD thesis, University of
    Glasgow, UK, 2022.
[5] Koehler, T., Goens, A., Bhat, S., Grosser, T., Trinder, P., and Steuwer, M. Guided equality saturation. Proc. ACM
    Program. Lang. 8, POPL (2024), 1727–1758.
[6] Milner, R. Implementation and applications of scott’s logic for computable functions. In Proceedings of ACM Confer-
    ence on Proving Assertions About Programs, Las Cruces, New Mexico, USA, January 6-7, 1972 (1972), ACM, pp. 1–6.
[7] Parks, T. M. Bounded scheduling of process networks. PhD thesis, 1995.
[8] Tate, R., Stepp, M., Tatlock, Z., and Lerner, S. Equality saturation: a new approach to optimization. In Proceedings of
    the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2009, Savannah, GA, USA,
    January 21-23, 2009 (2009), Z. Shao and B. C. Pierce, Eds., ACM, pp. 264–276.
[9] Willsey, M., Nandi, C., Wang, Y. R., Flatt, O., Tatlock, Z., and Panchekha, P. egg: Fast and extensible equality
    saturation. Proc. ACM Program. Lang. 5, POPL (2021), 1–29.
