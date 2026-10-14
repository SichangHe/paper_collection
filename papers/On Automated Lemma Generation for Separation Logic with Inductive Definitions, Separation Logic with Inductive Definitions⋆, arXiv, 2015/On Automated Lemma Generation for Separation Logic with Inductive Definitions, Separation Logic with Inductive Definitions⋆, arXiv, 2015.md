                                                 On Automated Lemma Generation for
                                              Separation Logic with Inductive Definitions⋆

                                                       Constantin Enea1 , Mihaela Sighireanu1 and Zhilin Wu2,1
                                                           1
                                                              LIAFA, Université Paris Diderot and CNRS, France
arXiv:1507.05581v1 [cs.LO] 20 Jul 2015




                                                   2
                                                       State Key Laboratory of Computer Science, Institute of Software,
                                                                       Chinese Academy of Sciences, China


                                                 Abstract. Separation Logic with inductive definitions is a well-known
                                                 approach for deductive verification of programs that manipulate dynamic
                                                 data structures. Deciding verification conditions in this context is usu-
                                                 ally based on user-provided lemmas relating the inductive definitions.
                                                 We propose a novel approach for generating these lemmas automatically
                                                 which is based on simple syntactic criteria and deterministic strategies
                                                 for applying them. Our approach focuses on iterative programs, although
                                                 it can be applied to recursive programs as well, and specifications that
                                                 describe not only the shape of the data structures, but also their con-
                                                 tent or their size. Empirically, we find that our approach is powerful
                                                 enough to deal with sophisticated benchmarks, e.g., iterative procedures
                                                 for searching, inserting, or deleting elements in sorted lists, binary search
                                                 tress, red-black trees, and AVL trees, in a very efficient way.


                                         1     Introduction
                                         Program verification requires reasoning about complex, unbounded size data
                                         structures that may carry data ranging over infinite domains. Examples of such
                                         structures are multi-linked lists, nested lists, trees, etc. Programs manipulating
                                         such structures perform operations that may modify their shape (due to dynamic
                                         creation and destructive updates) as well as the data attached to their elements.
                                         An important issue is the design of logic-based frameworks that express asser-
                                         tions about program configurations (at given control points), and then to check
                                         automatically the validity of these assertions, for all computations. This leads to
                                         the challenging problem of finding relevant compromises between expressiveness,
                                         automation, and scalability.
                                              An established approach for scalability is the use of Separation logic
                                         (SL) [18, 24]. Indeed, its support for local reasoning based on the “frame rule”
                                         leads to compact proofs, that can be dealt with in an efficient way. However,
                                         finding expressive fragments of SL for writing program assertions, that enable
                                         efficient automated validation of the verification conditions, remains a major
                                         issue. Typically, SL is used in combination with inductive definitions, which pro-
                                         vide a natural description of the data structures manipulated by a program.
                                         ⋆
                                             Zhilin Wu is supported by the NSFC projects (No. 61100062, 61272135, and
                                             61472474), and the visiting researcher program of China Scholarship Council. This
                                             work was supported by the ANR project Vecolib (ANR-14-CE28-0018).
II

Moreover, since program proofs themselves are based on induction, using induc-
tive definitions instead of universal quantifiers (like in approaches based on first-
order logic) enables scalable automation, especially for recursive programs which
traverse the data structure according to their inductive definition, e.g., [22]. Nev-
ertheless, automating the validation of the verification conditions generated for
iterative programs, that traverse the data structures using while loops, re-
mains a challenge. The loop invariants use inductive definitions for fragments
of data structures, traversed during a partial execution of the loop, and proving
the inductiveness of these invariants requires non-trivial lemmas relating (com-
positions of) such inductive definitions. Most of the existing works require that
these lemmas be provided by the user of the verification system, e.g., [8, 17, 22]
or they use translations of SL to first-order logic to avoid this problem. However,
the latter approaches work only for rather limited fragments [20, 21]. In general,
it is difficult to have lemmas relating complex user-defined inductive predicates
that describe not only the shape of the data structures but also their content.
     To illustrate this difficulty, consider the simple example of a sorted singly
linked list. The following inductive definition describes a sorted list segment
from the location E to F , storing a multiset of values M :
         lseg(E, M, F ) ::= E = F ∧ M = ∅ ∧ emp                                                        (1)
         lseg(E, M, F ) ::= ∃X, v, M1 . E 7→ {(next, X), (data, v)} ∗ lseg(X, M1 , F )
                                         ∧ v ≤ M1 ∧ M = M1 ∪ {v}                                       (2)
where emp denotes the empty heap, E 7→ {(next, X), (data, v)} states that the
pointer field next of E points to X while its field data stores the value v, and
∗ is the separating conjunction. Proving inductive invariants of typical sorting
procedures requires such an inductive definition and the following lemma:
       ∃E2 . lseg(E1 , M1 , E2 ) ∗ lseg(E2 , M2 , E3 ) ∧ M1 ≤ M2 ⇒ ∃M. lseg (E1 , M, E3 ).
The data constraints in these lemmas, e.g., M1 ≤ M2 (stating that every element
of M1 is less or equal than all the elements of M2 ), which become more complex
when reasoning for instance about binary search trees, are an important obstacle
for trying to synthesize them automatically.
    Our work is based on a new class of inductive definitions for describing frag-
ments of data structures that (i) supports lemmas without additional data
constraints like M1 ≤ M2 and (ii) allows to automatically synthesize these
lemmas using efficiently checkable, almost syntactic, criteria. For instance, we use
a different inductive definition for lseg, which introduces an additional parame-
ter M ′ that provides a “data port” for appending another sorted list segment,
just like F does for the shape of the list segment:
     lseg(E, M, F, M ′ ) ::= E = F ∧ M = M ′ ∧ emp                                                     (3)
                       ′                                                                           ′
     lseg(E, M, F, M ) ::= ∃X, v, M1 . E 7→ {(next, X), (data, v)} ∗ lseg(X, M1 , F, M )
                                         ∧ v ≤ M1 ∧ M = M1 ∪ {v}                                       (4)
The new definition satisfies the following simpler lemma, which avoids the in-
troduction of data constraints:
     ∃E2 , M2 . lseg (E1 , M1 , E2 , M2 ) ∗ lseg(E2 , M2 , E3 , M3 ) ⇒ lseg(E1 , M1 , E3 , M3 ).       (5)
                                                                                      III

Besides such “composition” lemmas (formally defined in Sec. 4), we define (in
Sec. 5) other classes of lemmas needed in program proofs and we provide efficient
criteria for generating them automatically. Moreover, we propose (in Sec. 6) a
proof strategy using such lemmas, based on simple syntactic matchings of spa-
tial atoms (points-to atoms or predicate atoms like lseg) and reductions to SMT
solvers for dealing with the data constraints. We show experimentally (in Sec. 7)
that this proof strategy is powerful enough to deal with sophisticated bench-
marks, e.g., the verification conditions generated from the iterative procedures
for searching, inserting, or deleting elements in binary search trees, red-black
trees, and AVL trees, in a very efficient way. The appendix contains the proofs
of theorems and additional classes of lemmas.


2    Motivating Example

Fig. 1 lists an iterative implementation of a search procedure for binary search
trees (BSTs). The property that E points to the root of a BST storing a multiset
of values M is expressed by the following inductively-defined predicate:

       bst (E, M ) ::= E = nil ∧ M = ∅ ∧ emp                                          (6)
       bst (E, M ) ::= ∃X, Y, M1 , M2 , v. E 7→ {(left, X), (right, Y ), (data, v)}   (7)
                                     ∗ bst (X, M1 ) ∗ bst (Y, M2 )
                                     ∧ M = {v} ∪ M1 ∪ M2 ∧ M1 < v < M2

int search(struct Tree* root,       The predicate bst(E, M ) is defined by two
            int key) {              rules describing empty (eq. (6)) and non-
  struct Tree *t = root;            empty trees (eq. (7)). The body (right-hand
  while (t != NULL) {               side) of each rule is a conjunction of a pure
    if (t->data == key)             formula, formed of (dis)equalities between lo-
      return 1;
                                    cation variables (e.g. E = nil) and data con-
    else if (t->data > key)
                                    straints (e.g. M = ∅), and a spatial formula
      t = t->left;
    else                            describing the structure of the heap. The data
      t = t->right;                 constraints in eq. (7) define M to be the mul-
  }                                 tiset of values stored in the tree, and state the
  return 0;                         sortedness property of BSTs.
}           Fig. 1.                     The      precondition     of    search      is
                                    bst(root, M0 ), where M0 is a ghost vari-
able denoting the multiset of values stored in the tree, while its postcondition
is bst (root, M0 ) ∧ (key ∈ M0 → ret = 1) ∧ (key 6∈ M0 → ret = 0), where ret
denotes the return value.
    The while loop traverses the BST in a top-down manner using the pointer
variable t. This variable decomposes the heap into two domain-disjoint sub-
heaps: the tree rooted at t, and the truncated tree rooted at root which contains
a “hole” at t. To specify the invariant of this loop, we define another predicate
bsthole(E, M1 , F, M2 ) describing “truncated” BSTs with one hole F as follows:
IV

    bsthole(E, M1 , F, M2 ) ::= E = F ∧ M1 = M2 ∧ emp                                           (8)
    bsthole(E, M1 , F, M2 ) ::= ∃X, Y, M3 , M4 , v. E 7→ {(left, X), (right, Y ), (data, v)}
                                            ∗ bst (X, M3 ) ∗ bsthole(Y, M4 , F, M2 )            (9)
                                            ∧ M1 = {v} ∪ M3 ∪ M4 ∧ M3 < v < M4
    bsthole(E, M1 , F, M2 ) ::= ∃X, Y, M3 , M4 , v. E 7→ {(left, X), (right, Y ), (data, v)}
                                            ∗ bsthole(X, M3 , F, M2 ) ∗ bst (Y, M4 )       (10)
                                            ∧ M1 = {v} ∪ M3 ∪ M4 ∧ M3 < v < M4
Intuitively, the parameter M2 , interpreted as a multiset of values, is used to
specify that the structure described by bsthole(E, M1 , F, M2 ) could be extended
with a BST rooted at F and storing the values in M2 , to obtain a BST rooted at
E and storing the values in M1 . Thus, the parameter M1 of bsthole is the union
of M2 with the multiset of values stored in the truncated BST represented by
bsthole(E, M1 , F, M2 ).
    Using bsthole, we obtain a succinct specification of the loop invariant:
    Inv ::= ∃M1 . bsthole(root, M0 , t, M1 ) ∗ bst (t, M1 ) ∧ (key ∈ M0 ⇔ key ∈ M1 ). (11)
We illustrate that such inductive definitions are appropriate for automated
reasoning, by taking the following branch of the loop: assume(t != NULL);
assume(t->data > key); t′ = t->left (as usual, if statements are trans-
formed into assume statements and primed variables are introduced in assign-
ments). The postcondition of Inv w.r.t. this branch, denoted post (Inv ), is com-
puted as usual by unfolding the bst predicate:
∃M1 , Y, v, M2 , M3 . bsthole(root, M0 , t, M1 ) ∗ t 7→ {(left, t′ ), (right, Y ), (data, v)}
                      ∗ bst (t′ , M2 ) ∗ bst (Y, M3 ) ∧ M1 = {v} ∪ M2 ∪ M3 ∧ M2 < v < M3
                      ∧ (key ∈ M0 ⇔ key ∈ M1 ) ∧ v > key.                                  (12)
The preservation of Inv by this branch is expressed by the entailment
post (Inv ) ⇒ Inv ′ , where Inv ′ is obtained from Inv by replacing t with t′ .
     Based on the lemmas, this paper also proposes a deterministic proof strategy
for proving the validity of entailments of the form ϕ1 ⇒ ∃X.ϕ   ~ 2 , where ϕ1 , ϕ2 are
quantifier-free and X    ~ contains only data variables3 . The strategy comprises two
steps: (i) enumerating spatial atoms A from ϕ2 , and for each of them, carving out
a sub-formula ϕA of ϕ1 that entails A, where it is required that these subformulas
do not share spatial atoms (due to the semantics of separation conjunction), and
(ii) proving that the data constraints from ϕA imply those from ϕ2 (using SMT
solvers). The step (i) may generate constraints on the variables in ϕA and ϕ2
that are used in step (ii). If the step (ii) succeeds, then the entailment holds.
     For instance, by applying this strategy to the entailment post (Inv ) ⇒ Inv ′
above, we obtain two goals for step (i) which consist in computing two sub-
formulas of post (Inv ) that entail ∃M1′ . bsthole(root, M0 , t′ , M1′ ) and respectively,
∃M1′′ . bst(t′ , M1′′ ). This renaming of existential variables requires adding the
equality M1 = M1′ = M1′′ to Inv ′ . The second goal, for ∃M1′′ . bst (t′ , M1′′ ), is
solved easily since this atom almost matches the sub-formula bst(t′ , M2 ). This
matching generates the constraint M1′′ = M2 , which provides an instantiation of
3
    The existential quantifiers in ϕ1 are removed using skolemization.
                                                                                     V

the existential variable M1′′ useful in proving the entailment between the data
constraints in step (ii).
    Computing a sub-formula that entails ∃M1′ . bsthole(root, M0 , t′ , M1′ ) re-
quires a non-trivial lemma. Thus, according to the syntactic criteria defined
in Sec. 4, the predicate bsthole enjoys the following composition lemma:
            ∃F, M. bsthole(root, M0 , F, M ) ∗ bsthole(F, M, t′ , M1′ )
                                                                          
                                                                                  (13)
                                                ⇒ bsthole(root, M0 , t , M1′ ).
                                                                          ′


Intuitively, this lemma states that composing two heap structures described by
bsthole results in a structure that satisfies the same predicate. The particular
relation between the arguments of the predicate atoms in the left-hand side is
motivated by the fact that the parameters F and M are supposed to represent
“ports” for composing bsthole(root, M0 , F, M ) with some other similar heap
structures. This property of F and M is characterized syntactically by the fact
that, roughly, F (resp. M ) occurs only once in the body of each inductive rule of
bsthole, and F (resp. M ) occurs only in an equality with root (resp. M0 ) in the
base rule (we are referring to the rules (8)–(10) with the parameters of bsthole
substituted by (root, M0 , F, M )).
    Therefore, the first goal reduces to finding a sub-formula of post (Inv ) that
implies the premise of (13) where M1′ remains existentially-quantified. Recur-
sively, we apply the same strategy of enumerating spatial atoms and finding
sub-formulas that entail them. However, we are relying on the fact that all the
existential variables denoting the root locations of spatial atoms in the premise
of the lemma, e.g., F in lemma (13), occur as arguments in the only spatial
atom of the conclusion whose root location is the same as that of the conse-
quent, i.e., bsthole(root, M0 , F, M ) in lemma (13). Therefore, the first sub-goal,
∃F, M. bsthole(root, M0 , F, M ) matches the atom bsthole(root, M0 , t, M1 ), un-
der the constraint F = t∧M = M1 . This constraint is used in solving the second
sub-goal, which now becomes ∃M1′ . bsthole(t, M1 , t′ , M1′ ).
    The second sub-goal is proved by unfolding bsthole twice, using first the rule
(10) and then the rule (8), and by matching the resulting spatial atoms with
those in post (Inv ) one by one. Assuming that the existential variable M1 from
Inv ′ is instantiated with M2 from post (Inv ) (fact automatically deduced in the
first step), the data constraints in post (Inv ) entail those in Inv ′ . This completes
the proof of post (Inv ) ⇒ Inv ′ .

3    Separation Logic with Inductive Definitions
Let LVar be a set of location variables, interpreted as heap locations, and DVar
a set of data variables, interpreted as data values stored in the heap, (multi)sets
of values, etc. In addition, let Var = LVar ∪ DVar. The domain of heap locations
is denoted by L while the domain of data values stored in the heap is generically
denoted by D. Let F be a set of pointer fields, interpreted as functions L ⇀ L,
and D a set of data fields, interpreted as functions L ⇀ D. The syntax of the
Separation Logic fragment considered in this paper is defined in Tab. 1.
    Formulas are interpreted over pairs (s, h) formed of a stack s and a heap
h. The stack s is a function giving values to a finite set of variables (location
VI

               Table 1. The syntax of the Separation Logic fragment
           X, Y, E ∈ LVar location variables ρ ⊆ (F × LVar) ∪ (D × DVar)
           ~ ∈ Var∗ vector of variables
           F                                 P ∈ P predicates
           x ∈ Var variable                  ∆ formula over data variables
           Π ::= X = Y | X 6= Y | ∆ | Π ∧ Π                    pure formulas
           Σ ::= emp | E 7→ ρ | P (E, F~ ) | Σ ∗ Σ           spatial formulas
           ϕ ::= Π ∧ Σ | ϕ ∨ ϕ | ∃x. ϕ                               formulas
or data variables) while the heap h is a function mapping a finite set of pairs
(ℓ, pf ), where ℓ is a location and pf is a pointer field, to locations, and a finite set
of pairs (ℓ, df ), where df is a data field, to values in D. In addition, h satisfies
the condition that for each ℓ ∈ L, if (ℓ, df ) ∈ dom(h) for some df ∈ D, then
(ℓ, pf ) ∈ dom(h) for some pf ∈ F . Let dom(h) denote the domain of h, and
ldom(h) denote the set of ℓ ∈ L such that (ℓ, pf ) ∈ dom(h) for some pf ∈ F .
     Formulas are conjunctions between a pure formula Π and a spatial formula
Σ. Pure formulas characterize the stack s using (dis)equalities between location
variables, e.g., a stack models x = y iff s(x) = s(y), and constraints ∆ over
data variables. We let ∆ unspecified, though we assume that they belong to
decidable theories, e.g., linear arithmetic or quantifier-free first order theories
over multisets of values. The atom emp of spatial formulas holds iff the domain
of the heap is empty. The points-to atom E 7→ {(fi , xi )}i∈I specifies that the
heap contains exactly one location E, and for all i ∈ I, the field fi of E equals xi ,
i.e., h(s(E), fi ) = s(xi ). The predicate atom P (E, F~ ) specifies a heap segment
rooted at E and shaped by the predicate P ; the fragment is parameterized by a
set P of inductively defined predicates, formally defined hereafter.
     Let P ∈ P. An inductive definition of P is a finite set of rules of the form
P (E, F~ ) ::= ∃Z.Π
                 ~ ∧ Σ, where Z   ~ ∈ Var∗ is a tuple of variables. A rule R is called
a base rule if Σ contains no predicate atoms. Otherwise, it is called an inductive
rule. A base rule R is called spatial-empty if Σ = emp. Otherwise, it is called a
spatial-nonempty base rule. For instance, the predicate bst in Sec. 2 is defined
by one spatial-empty base rule and one inductive rule.
     We consider a class of restricted inductive definitions that are expressive
enough to deal with intricate data structures (see Sec. 7) while also enabling
efficient proof strategies for establishing the validity of the verification conditions
(see Sec. 6). For each rule R : P (E, F~ ) ::= ∃Z.Π   ~     ∧ Σ in the definition of a
                   ~
predicate P (E, F ) ∈ P, we assume that:
  – If R is inductive, then Σ = Σ1 ∗ Σ2 and the following conditions hold:
       • the root atoms: Σ1 contains only points-to atoms and a unique points-to
          atom starting from E, denoted as E 7→ ρ. Also, all the location variables
          from Z~ occur in Σ1 . Σ1 is called the root of R and denoted by root(R).
       • connectedness: the Gaifman graph of Σ1 , denoted by GΣ1 , is a connected
          DAG (directed acyclic graph) with the root E, that is, every vertex is
          reachable from E,
       • predicate atoms: Σ2 contains only atoms of the form Q(Z, Z        ~ ′ ), and for
          each such atom, Z is a vertex in GΣ1 without outgoing arcs.
                                                                                              VII

 – If R is a spatial-nonempty base rule, then Σ contains exactly one points-to
    atom E 7→ ρ, for some ρ.
The classic acyclic list segment definition [24] satisfies these constraints as well as
the first rule below; the second rule below falsifies the “root atoms” constraint:
       lsegeven(E, F ) ::= ∃X, Y. E 7→ (next, X) ∗ X 7→ (next, Y ) ∗ lsegeven(Y, F )
          lsegb(E, F ) ::= ∃X. lsegb(E, X) ∗ X 7→ (next, F ).
Since we disallow the use of negations on top of the spatial atoms, the semantics
of the predicates in P is defined as usual as a least fixed-point. The class of
inductive definitions defined above is in general undecidable, since with data
fields, inductive definitions can be used to simulate two-counter machines.
    A variable substitution η is a mapping from a finite subset of Var to the set
of terms over the respective domains. For instance, if X ∈ LVar and v, v1 ∈ DVar
be integer variables then the mapping η = {X → nil, v → v1 + 5} is a variable
substitution. We denote by free(ψ) the set of free variables of a formula ψ.
4     Composition Lemmas
As we have seen in the motivating example, the predicate bsthole(E, M1 , F, M2 )
satisfies the property that composing two heap structures described by this pred-
icate results in a heap structure satisfying the same predicate. We call this prop-
erty a composition lemma. We define simple and uniform syntactic criteria which,
if they are satisfied by a predicate, then the composition lemma holds.
    The main idea is to divide the parameters of inductively defined predicates
into three categories: The source parameters α        ~ = (E, C), the hole parameters
~ = (F, H), and the static parameters ξ~ ∈ Var∗ , where E, F ∈ LVar are called
β
the source and resp., the hole location parameter, and C, H ∈ DVar are called
the cumulative and resp., the hole data parameter4 .
    Let P be a set of inductively defined predicates and P ∈ P with the param-
eters (~   ~ ξ~ ). Then P is said to be syntactically compositional if the inductive
        α, β,
definition of P contains exactly one base rule, and at least one inductive rule,
and the rules of P are of one of the following forms:
  – Base rule: P (~     ~ ξ~ ) ::= α1 = β1 ∧ α2 = β2 ∧ emp. Note that here the
                     α, β,
     points-to atoms are disallowed.
  – Inductive rule: P (~     ~ ξ~ ) ::= ∃Z.
                         α, β,            ~ Π ∧ Σ, with (a) Σ , Σ1 ∗ Σ2 ∗ P (~γ , β,       ~ ξ~ ),
     (b) Σ1 contains only and at least one points-to atoms, (c) Σ2 contains only
     and possibly none predicate atoms, (d) ~γ ⊆ Z,     ~ and (d) the variables in β        ~ do
     not occur elsewhere in Π ∧Σ, i.e., not in Π, or Σ1 , or Σ2 , or ~γ . Note that the
     inductive rule also satisfies the constraints “root atom” and “connectedness”
     introduced in Sec. 3. In addition, Σ2 may contain P atoms.
    One may easily check that both the predicate lseg(E, M, F, M ′ ) in eq. (3)–(4)
and the predicate bsthole(E, M1 , F, M2 ) in eq. (8)–(10) are syntactically compo-
sitional, while the predicate lseg(E, M, F ) in eq. (1)–(2) is not.
    A predicate P ∈ P with the parameters (~            ~ ξ~ ) is said to be semantically
                                                     α, β,
compositional if the entailment ∃β. P (~~      ~  ~        ~ ~γ , ξ~ ) ⇒ P (~
                                            α, β, ξ ) ∗ P (β,               α, ~γ , ξ~ ) holds.
4
    For simplicity, we assume that α     ~ consist of exactly one location parameter
                                   ~ and β
    and one data parameter.
VIII

Theorem 1. Let P be a set of inductively defined predicates. If P ∈ P is syn-
tactically compositional, then P is semantically compositional.
The proof of Thm. 1 is done (see [12]) by induction on the size of the domain of
the heap structures. Suppose (s, h) |= P (~
                                          α, β,~ ξ~ ) ∗ P (β,
                                                           ~ ~γ , ξ~ ), then either s(~
                                                                                      α) =
  ~                ~
          α) 6= s(β). If the former situation occurs, then (s, h) |= P (~
s(β) or s(~                                                                        α, ~γ , ξ~ )
follows immediately. Otherwise, the predicate P (~         ~  ~
                                                        α, β, ξ ) is unfolded by using
some inductive rule of P , and the induction hypothesis can be applied to a sub-
                                        α, ~γ , ξ~ ) can be deduced by utilizing the
heap of smaller size. Then (s, h) |= P (~
property that the hole parameters occur only once in each inductive rule of P .
Remark 1. The syntactically compositional predicates are rather general in the
sense that they allow nestings of predicates, branchings (e.g. trees), as well as
data and size constraints. Therefore, composition lemmas can be obtained for
complex data structures like nested lists, AVL trees, red-black trees, and so on.
In addition, although lemmas have been widely used in the literature, we are
not aware of any work that uses the composition lemmas as simple and elegant
as those introduced above, when data and size constraints are included.

5      Derived Lemmas
Theorem 1 provides a mean to obtain lemmas for one single syntactically com-
positional predicate. In the following, based on the syntactic compositionality,
we demonstrate how to derive additional lemmas describing relationships be-
tween different predicates (proofs are detailed in [12]). We identify three cate-
gories of derived lemmas: “completion” lemmas, “stronger” lemmas, and “static-
parameter contraction” lemmas. Based on our experiences in the experiments
(cf. Sec. 7) and the examples from the literature, we believe that the composition
lemmas as well as the derived ones are natural, essential, and general enough
for the verification of programs manipulating dynamic data structures. For in-
stance, the “composition” lemmas and “completion” lemmas are widely used in
our experiments, the “stronger” lemmas are used to check the verification con-
ditions for rebalancing AVL trees and red-black trees. While “static parameter
contraction” lemmas are not used in our experiments, they could also be useful,
e.g., for the verification of programs manipulating lists with tail pointers.
5.1    The “completion” lemmas
We first consider the “completion” lemmas which describe relationships between
incomplete data structures (e.g., binary search trees with one hole) and complete
data structures (e.g., binary search trees). For example, the following lemma is
valid for the predicates bsthole and bst:
               ∃F, M2 . bsthole(E, M1 , F, M2 ) ∗ bst (F, M2 ) ⇒ bst (E, M1 ).
Notice that the rules defining bst (E, M ) can be obtained from those of
bsthole(E1 , M1 , F, M2 ) by applying the variable substitution η = {F →
nil, M2 → ∅} (modulo the variable renaming M1 by M ). This observation is
essential to establish the “completion lemma” and it is generalized to arbitrary
syntactically compositional predicates as follows.
                                                                                               IX

    Let P ∈ P be a syntactically compositional predicate with the parameters
(~  ~ ξ~ ), and P ′ ∈ P a predicate with the parameters (~
 α, β,                                                    α, ξ~ ). Then P ′ is a
completion of P with respect to a pair of constants ~c = c1 c2 , if the rules of
P ′ are obtained from the rules of P by applying the variable substitution η =
{β1 → c1 , β2 → c2 }. More precisely,

 – let α1 = β1 ∧ α2 = β2 ∧ emp be the base rule of P , then P ′ contains only one
   base rule, that is, α1 = c1 ∧ α2 = c2 ∧ emp,
 – the set of inductive rules of P ′ is obtained from those of P as follows: Let
   P (~   ~ ξ~ ) ::= ∃Z.
       α, β,                                    ~ ξ~ ) be an inductive rule of P , then
                       ~ Π ∧ Σ1 ∗ Σ2 ∗ P (~γ , β,
     ′
   P (~   ~          ~                         ~
       α, ξ ) ::= ∃Z. Π ∧ Σ1 ∗ Σ2 ∗ P (~γ , ξ ) is an inductive rule of P ′ (Recall
                                        ′

   that β~ does not occur in Π, Σ1 , Σ2 , ~γ ).


Theorem 2. Let P (~          ~ ξ~ ) ∈ P be a syntactically compositional predicate, and
                          α, β,
  ′
P (~     ~
    α, ξ ) ∈ P. If P is a completion of P with respect to ~c, then P ′ (~
                        ′
                                                                               α, ξ~ ) ⇔
P (~α, ~c, ξ~ ) and ∃β.
                     ~ P (~   ~ ξ~ ) ∗ P (β,
                          α, β,         ′ ~ ξ~ ) ⇒ P (~
                                                    ′
                                                      α, ξ~ ) hold.

5.2    The “stronger” lemmas

We illustrate this class of lemmas on the example of binary search trees.
Let natbsth(E, M1 , F, M2 ) be the predicate defined by the same rules as
bsthole(E, M1 , F, M2 ) (i.e., eq. (8)–(10)), except that M3 ≥ 0 (M3 is an exis-
tential variable) is added to the body of each inductive rule (i.e., eq. (9) and
(10)). Then we say that natbsth is stronger than bsthole, since for each rule R′
of natbsth, there is a rule R of bsthole, such that the body of R′ entails the body
of R. This “stronger” relation guarantees that the following lemmas hold:

                                          natbsth (E, M1 , F, M2 ) ⇒ bsthole(E, M1 , F, M2 )
∃E2 , M2 . natbsth (E1 , M1 , E2 , M2 ) ∗ bsthole(E2 , M2 , E3 , M3 ) ⇒ bsthole(E1 , M1 , E3 , M3 ).

In general, for two syntactically compositional predicates P, P ′ ∈ P with the
same set of parameters (~         ~ ξ~ ), P ′ is said to be stronger than P if for each
                               α, β,
inductive rule P ′ (~   ~ ξ~ ) ::= ∃Z.
                     α, β,                                       ~ ξ~ ), there is an inductive
                                     ~ Π ′ ∧ Σ1 ∗ Σ2 ∗ P ′ (~γ , β,
           ~  ~         ~                            ~ ~
        α, β, ξ ) ::= ∃Z. Π ∧ Σ1 ∗ Σ2 ∗ P (~γ , β, ξ ) such that Π ′ ⇒ Π holds. The
rule P (~
following result is a consequence of Thm. 1.

Theorem 3. Let P (~       ~ ξ~ ), P ′ (~
                       α, β,              ~ ξ~ ) ∈ P be two syntactically composi-
                                       α, β,
tional predicates. If P is stronger than P , then the entailments P ′ (~
                        ′                                                     ~ ξ~ ) ⇒
                                                                           α, β,
      ~  ~        ~   ′
   α, β, ξ ) and ∃β. P (~
P (~                        ~  ~         ~      ~
                         α, β, ξ ) ∗ P (β, ~γ , ξ ) ⇒ P (~       ~
                                                         α, ~γ , ξ ) hold.
The “stronger” relation defined above requires that the spatial formulas in the
inductive rules of P and P ′ are the same. This constraint can be relaxed by only
requiring that the body of each inductive rule of P ′ is stronger than a formula
obtained by unfolding an inductive rule of P for a bounded number of times.
This relaxed constraint allows generating additional lemmas, e.g., the lemmas
relating the predicates for list segments of even length and list segments.
X

5.3    The “static-parameter contraction” lemmas
Let tailbsth(E, M1 , F, M2 ) (resp. stabsth(E, M1 , F, M2 , B)) be the pred-
icate defined by the same rules as bsthole(E, M1 , F, M2 ), with the
modification that the points-to atom in each inductive rule is re-
placed by E 7→ {(left, X), (right, Y ), (tail, F ), (data, v)} (resp. E 7→
{(left, X), (right, Y ), (tail, B), (data, v)}). Intuitively, tailbsth (resp. stabsth)
is obtained from bsthole by adding a tail pointer to F (resp. B). Then tailbsth
is not syntactically compositional since F occurs in the points-to atoms of the
inductive rules. On the other hand, stabsth is syntactically compositional.
    From the above description, it is easy to observe that the inductive definition
of tailbsth(E, M1 , F, M2 ) can be obtained from that of stabsth(E, M1 , F, M2 , B)
by replacing B with F . Then the lemma tailbsth(E, M1 , F, M2 ) ⇔
stabsth(E, M1 , F, M2 , F ) holds. From this, we further deduce the lemma
    ∃E2 , M2 . stabsth (E1 , M1 , E2 , M2 , E3 ) ∗ tailbsth(E2 , M2 , E3 , M3 ) ⇒
                                                                   tailbsth(E1 , M1 , E3 , M3 ).
We call the aforementioned replacement of B by F in the inductive definition of
stabsth as the “static-parameter contraction”. This idea can be generalized to
arbitrary syntactically compositional predicates as follows.
     Let P ∈ P be a syntactically compositional predicate with the parameters
(~   ~ ξ~ ), P ′ ∈ P be an inductive predicate with the parameters (~
 α, β,                                                                      ~ ξ~′ ), ξ~ =
                                                                         α, β,
                  ~′    ′       ′         ′
ξ1 . . . ξk , and ξ = ξ1 . . . ξl . Then P is called a static-parameter contraction of
P if the rules of P ′ are obtained from those of P by a variable substitution η
s.t. dom(η) = ξ,    ~ for each i : 1 ≤ i ≤ k, either η(ξi ) = ξi , or η(ξi ) = βj for
some j = 1, 2 satisfying that ξi and βj have the same data type, and ξ~′ is the
tuple obtained from η(ξ~ ) by removing the βj ’s. The substitution η is called the
contraction function.
Theorem 4. Let P (~         ~ ξ~ ) ∈ P be a syntactically compositional predicate and
                         α, β,
P ′ (~  ~ ξ~′ ) ∈ P be an inductive predicate. If P ′ is a static-parameter contraction
     α, β,
of P with the contraction function η, then P ′ (~             ~ ξ~′ ) ⇔ P (~
                                                           α, β,              ~ η(ξ~ )) and
                                                                           α, β,
 ~
∃β. P (~    ~     ~      ′ ~       ~′     ′
         α, β, η(ξ )) ∗ P (β, ~γ , ξ ) ⇒ P (~       ~′
                                            α, ~γ , ξ ) hold.

Remark 2. The lemmas presented in the last two sections are incomplete in
the sense that they may not cover all the lemmas for a given set of inductive
predicates. Although various extensions of the lemmas are possible, generating
all the possible lemmas can be quite complex in general. Thm. 3 in [15] shows
that generating all the lemmas is at least EXPTIME-hard, even for a fragment
restricted to shape properties, without any data or size constraint.

6     A Proof Strategy Based on Lemmas
We introduce a proof strategy based on lemmas for proving entailments ϕ1 ⇒
  ~ 2 , where ϕ1 , ϕ2 are quantifier-free, and X
∃X.ϕ                                              ~ ∈ DVar∗ . The proof strategy
treats uniformly the inductive rules defining predicates and the lemmas defined in
Sec. 4–5. Therefore, we call lemma also an inductive rule. W.l.o.g. we assume that
                                                                                       XI

                     Σ1 = θ(Σ2 )      η = θ|X
                                            ~     Π1 ∧ EQ(η) |= EQ(θ|free(∃X.Σ
                                                                           ~  2)
                                                                                 )
        (Match1)
                                                        ~
                                        Π1 ∧ Σ1 |=η ∃X. Σ2
                                                  SUB



                                        Π1 ∧ Σ1 |=SUB
                                                  η
                                                       ~ Σ2
                                                      ∃X.
                          (Match2)
                                                      ~ Σ2
                                         Π1 ∧ Σ1 |=η ∃X.

                    Π1 ∧ Σ1 |=SUB
                              η1  ∃Z~ ′ . root(L) Π1 ∧ Σ1′ |=η2 ∃Z~′′ . η1 (Π ∧ Σ)
        (Lemma)
                                   Π1 ∧ Σ1 ∗ Σ ′ |=η| ∃X. ~ A
                                                  1    ~
                                                       X


               ~ Π ∧ root(L) ∗ Σ ⇒ A is a lemma,
     – L ::= ∃Z.
       ~ ′    ~
     – Z = (X ∪ Z) ~ ∩ free(root(L)), Z~′′ = (X  ~ ∪ Z)
                                                      ~ ∩ free(η1 (Π ∧ Σ)),
                                                                             ~ ∪ Z.
     – η = ext Π (η1 ∪ η2 ) is the extension of η1 ∪ η2 with Π s.t. dom(η) = X   ~

                                ~ ′ .A Π1 ∧ Σ2 |=η2 ∃Z~′′ .Σ Π1 ∧ EQ(η) |= Π2
                  Π1 ∧ Σ1 |=η1 ∃Z
        (Slice)
                                                  ~ Π2 ∧ A ∗ Σ
                               Π1 ∧ Σ1 ∗ Σ2 |=η ∃X.

     – Z~ ′ = X
              ~ ∩ free(A), Z~′′ = X ~ ∩ free(Σ),
                                                                               ~
     – η = ext Π2 (η1 ∪ η2 ) is the extension of η1 ∪ η2 with Π2 s.t. dom(η) = X.

                                                                    ~ ϕ2
          Fig. 2. The proof rules for checking the entailment ϕ1 ⇒ ∃X.
ϕ1 is quantifier-free (the existential variables can be skolemized). In addition,
we assume that only data variables are quantified in the right-hand side 5 .
    W.l.o.g., we assume that every variable in X       ~ occurs in at most one spatial
atom of ϕ2 (multiple occurrences of the same variable can be removed by intro-
ducing fresh variables and new equalities in the pure part). Also, we assume that
ϕ1 and ϕ2 are of the form Π ∧ Σ. In the general case, our proof strategy checks
that for every disjunct ϕ′1 of ϕ1 , there is a disjunct ϕ′2 of ϕ2 s.t. ϕ′1 ⇒ ∃X.ϕ  ~ ′2 .
    We present the proof strategy as a set of rules in Fig. 2. For a variable
substitution η and a set X ⊆ Var, we denote by η|X the restriction of η to
X . In addition, EQ(η) is the conjunction of the equalities X = t for every X
and t such that η(X) = t. Given two formulas ϕ1 and ϕ2 , a substitution η
with dom(η) = X,  ~ the judgement ϕ1 |=η ∃X.ϕ        ~ 2 denotes that the entailment
ϕ1 ⇒ η(ϕ2 ) is valid. Therefore, η provides an instantiation for the quantified
variables X ~ which witnesses the validity.
    The rules Match1 and Match2 consider a particular case of |=η , denoted
using the superscript SUB, where the spatial atoms of ϕ2 are syntactically
matched6 to the spatial atoms of ϕ1 modulo a variable substitution θ. The
substitution of the existential variables is recorded in η, while the substitu-
tion of the free variables generates a set of equalities that must be implied by
Π1 ∧ EQ(η). For example, let Π1 ∧ Σ1 ::= w = w′ ∧ E 7→ {(f, Y ), (d1 , v), (d2 , w)},
and ∃X.~ Σ2 ::= ∃X, v ′ . E 7→ {(f, X), (d1 , v ′ ), (d2 , w′ )}, where d1 and d2 are data
fields. If θ = {X → Y, v ′ → v, w′ → w}, then Σ1 = θ(Σ2 ). The substitution of
5
  We believe that this restriction is reasonable for the verification conditions appearing
  in practice and all the benchmarks in our experiments are of this form.
6
  In this case, the right-hand side contains no pure constraints.
XII

the free variable w′ from the right-hand side is sound since the equality w = w′
                                                                     ′
occurs in the left-hand side. Therefore, Π1 ∧ Σ1 |=SUBθ|{X,v′ } ∃X, v . Σ2 holds.

    The rule Lemma applies a lemma L ::= ∃Z.    ~ Π ∧ root(L) ∗ Σ ⇒ A. It consists
in proving that ϕ1 implies the LHS of the lemma where the variables in X           ~
                                      ~   ~
are existentially quantified, i.e., ∃X∃Z. Π ∧ root(L) ∗ Σ. Notice that Z may   ~
contain existential location variables. Finding suitable instantiations for these
variables relies on the assumption that root (L) in the LHS of L is either a unique
predicate atom or a separating conjunction of points-to atoms rooted at E (the
first parameter of A) and root (L) includes all the location variables in Z.  ~ This
assumption holds for all the inductive rules defining predicates in our fragment
(a consequence of the root and connectedness constraints) and for all the lemmas
defined in Sec. 4–5. The proof that ϕ1 implies ∃X∃   ~ Z.
                                                        ~ Π ∧ root(L) ∗ Σ is split
into two sub-goals (i) proving that a sub-formula of ϕ1 implies ∃X∃     ~ Z.
                                                                           ~ root(L)
                                                      ~  ~
and (ii) proving that a sub-formula of ϕ1 implies ∃X∃Z. Π ∧ Σ. The sub-goal (i)
relies on syntactic matching using the rule Match1, which results in a quantifier
instantiation η1 . The substitution η1 is used to instantiate existential variables
in ∃X∃~ Z.
         ~ Π ∧ Σ. Notice that according to the aforementioned assumption,
the location variables in Z ~ are not free in η1 (Π ∧ Σ). Let η2 be the quantifier
instantiation obtained from the second sub-goal. The quantifier instantiation η
is defined as the extension of η1 ∪ η2 to the domain X        ~ ∪Z~ by utilizing the
                                        7
pure constraints Π from the lemma . This extension is necessary since some
existentially quantified variables may only occur in Π, but not in root(L) nor
in Σ, so they are not covered by η1 ∪ η2 . For instance, if Π contains a conjunct
M = M1 ∪ M2 such that M1 ∈ dom(η1 ), M2 ∈ dom(η2 ), and M 6∈ dom(η1 ∪ η2 ),
then η1 ∪ η2 is extended to η where η(M ) = η1 (M1 ) ∪ η2 (M2 ).
    The rule Slice chooses a spatial atom A in the RHS and generates two
sub-goals: (i) one that matches A (using the rules Match2 and Lemma) with
a spatial sub-formula of the LHS (Σ1 ) and (ii) another that checks that the
remaining spatial part of the RHS is implied by the remaining part of the LHS.
The quantifier instantiations η1 and η2 obtained from the two sub-goals are used
to check that the pure constraints in the RHS are implied by the ones in LHS.
Note that in the rule Slice, it is possible that Σ2 = Σ = emp.
    The rules in Fig. 2 are applied in the order given in the figure. Note that they
focus on disjoint cases w.r.t. the syntax of the RHS. The choice of the atom A in
Slice is done arbitrary, since it does not affect the efficiency of proving validity.
    We apply the above proof strategy to the entailment ϕ1 ⇒ ∃M. ϕ2 where:
           ϕ1 ::= x1 6= nil ∧ x2 6= nil ∧ v1 < v2 ∧ x1 7→ {(next, x2 ), (data, v1 )}
                                                    ∗ x2 7→ {(next, nil), (data, v2 )}
           ϕ2 ::= lseg (x1 , M, nil, ∅) ∧ v2 ∈ M,



7
    The extension depends on the pure constraints Π and could be quite complex in gen-
    eral. In the experiments of Sec. 7, we use the extension obtained by the propagation
    of equalities in Π.
                                                                                 XIII

and lseg has been defined in Sec. 1 (eq. (3)–(4)). The entailment is valid be-
cause it states that two cells linked by next and storing ordered data val-
ues form a sorted list segment. The RHS ϕ2 contains a single spatial atom
and a pure part so the rule Slice is applied and it generates the sub-goal
ϕ1 |=η ∃M. lseg(x1 , M, nil, ∅) for which the syntactic matching (rule Match1)
can not be applied. Instead, we apply the rule Lemma using as lemma the induc-
tive rule of lseg, i.e., eq. (4) (page II). We obtain the RHS ∃M, X, M1 , v. x1 7→
{(next, X), (data, v)} ∗ lseg(X, M1 , nil, ∅) ∧ M = {v} ∪ M1 ∧ v ≤ M1 , where
x1 7→ {(next, X), (data, v)} is the root. The rule Match1 is applied with
Π1 ∧ Σ1 ::= x1 6= nil ∧ x2 6= nil ∧ v1 < v2 ∧ x1 7→ {(next, x2 ), (data, v1 )}
and it returns the substitution η1 = {X → x2 , v → v1 }. The second sub-goal is
Π1 ∧ Σ2 |=η2 ∃M, M1 .ψ ′ where Π1 ∧ Σ2 ::= x1 6= nil ∧ x2 6= nil ∧ v1 < v2 ∧ x2 7→
{(next, nil), (data, v2 )} and ψ ′ ::= M = {v1 }∪M1 ∧v1 ≤ M1 ∧lseg(x2 , M1 , nil, ∅).
For this sub-goal, we apply the rule Slice, which generates a sub-goal where the
rule Lemma is applied first, using the same lemma, then the rule Slice is ap-
plied again, and finally the rule Lemma is applied with a lemma corresponding
to the base rule of lseg, i.e., eq. (3) (page II). This generates a quantifier instan-
tiation η2 = {M → {v1 , v2 }, M1 → {v2 }}. Then, η1 ∪ η2 is extended with the
constraints from the pure part of the lemma, i.e., M = {v} ∪ M1 ∧ v1 ≤ M1 .
Since M ∈ dom(η1 ∪ η2 ), this extension has no effect. Finally, the rule Slice
checks that Π1 ∧ EQ(η|{M} ) |= Π2 holds, where EQ(η|{M} ) ::= M = {v1 , v2 } and
Π2 ::= v2 ∈ M . The last entailment holds, so the proof of validity is done.
    The following theorem states the correctness of the proof rules. Moreover,
since we assume a finite set of lemmas, and every application of a lemma L
removes at least one spatial atom from ϕ1 (the atoms matched to root (L)), the
termination of the applications of the rule Lemma is guaranteed.
Theorem 5. Let ϕ1 and ∃X.ϕ      ~ 2 be two formulas such that X ~ contains only data
variables. If ϕ1 |=η ∃X.ϕ~ 2 for some η, then ϕ1 ⇒ ∃X.ϕ  ~ 2.

7     Experimental results
We have extended the tool spen [25] with the proof strategy proposed in this
paper. The entailments are written in an extension of the SMTLIB format used in
the competition SL-COMP’14 for separation logic solvers. It provides as output
SAT, UNSAT or UNKNOWN, and a diagnosis for all these cases.
    The solver starts with a normalization step, based on the boolean abstrac-
tions described in [11], which saturates the input formulas with (dis)equalities
between location variables implied by the semantics of separating conjunction.
The entailments of data constraints are translated into satisfiability problems in
the theory of integers with uninterpreted functions, discharged using an SMT
solver dealing with this theory.
    We have experimented the proposed approach on two sets of benchmarks8 :
RDBI: verification conditions for proving the correctness of iterative procedures
    (delete, insert, search) over recursive data structures storing integer data:
    sorted lists, binary search trees (BST), AVL trees, and red black trees (RBT).
8
    http://www.liafa.univ-paris-diderot.fr/spen/benchmarks.html
XIV

                       Table 2. Experimental results on benchmark RDBI

     Data structure       Procedure        #VC           Lemma            ⇒D       Time (s)
                                                 (#b, #r, #p, #c, #d)           spen     SMT
     sorted lists          search            4        (1, 3, 3, 1, 3)      5    1.108     0.10
                           insert            8        (4, 6, 3, 1, 2)      7    2.902     0.15
                           delete            4        (2, 2, 4, 1, 1)      6    1.108     0.10
     BST                   search            4        (2, 3, 6, 2, 2)      6    1.191     0.15
                           insert           14      (15, 18, 27, 4, 6)    19    3.911     0.55
                           delete           25      (13, 19, 82, 8, 5)    23    8.412     0.58
     AVL                   search            4        (2, 3, 6, 2, 2)      6    1.573     0.15
                           insert           22      (18, 28, 74, 6, 8)    66    6.393     1.33
     RBT                   search            4        (2, 3, 6, 2, 2)      6    1.171     0.15
                           insert           21     (27, 45, 101, 7, 10)   80    6.962     2.53
                    Table 3. Experimental results on benchmark SL-COMP’14
        Data structure           #VC                Lemma              Time-spen(s)
                                            (#b, #r, #p, #c, #d)    spen     spen-TA
        Nested linked lists           16        (17,47,14,8,0)      4.428       4.382
        Skip lists 2 levels            4         (11,16,1,1,0)      1.629       1.636
        Skip lists 3 levels           10       (16,32,29,17,0)      3.858       3.485


SL-COMP’14: problems in the SL-COMP’14 benchmark, without data con-
   straints, where the inductive definitions are syntactically compositional.
Tab. 2 provides the experiment results9 for RDBI. The column #VC gives the
number of verification conditions considered for each procedure. The column
Lemma provides statistics about the lemma applications as follows: #b and #r
are the number of the applications of the lemmas corresponding to base resp.
inductive rules, #c and #d are the number of the applications of the composition
resp. derived lemmas, and #p is the number of predicates matched syntactically,
without applying lemmas. Column ⇒D gives the number of entailments between
data constraints generated by spen. Column Time-spen gives the “system” time
spent by spen on all verification conditions of a function10 excepting the time
taken to solve the data constraints by the SMT solver, which is given in the
column Time-SMT.
    Tab. 3 provides a comparison of our approach (column spen) with the de-
cision procedure in [11] (column spen-TA) on the same set of benchmarks from
SL-COMP’14. The times of the two decision procedures are almost the same,
which demonstrates that our approach, as an extension of that in [11], is robust.

8       Related work
There have been many works on the verification of programs manipulating mu-
table data structures in general and the use of separation logic, e.g., [1–5, 7–
 9
     The evaluations used a 2.53 GHz Intel processor with 2 GB, running Linux on VBox.
10
     spen does not implement a batch mode, each entailment is dealt separately, including
     the generation of lemma. The SMT solver is called on the files generated by spen.
                                                                              XV

11, 13–17, 21, 23, 26]. In the following, we discuss those which are closer to our
approach.
    The prover SLEEK [7, 17] provides proof strategies for proving entailments
of SL formulas. These strategies are also based on lemmas, relating inductive
definitions, but differently from our approach, these lemmas are supposed to
be given by the user (SLEEK can prove the correctness of the lemmas once
they are provided). Our approach is able to discover and synthesize the lemmas
systematically, efficiently, and automatically.
   The natural proof approach DRYAD [19, 22] can prove automatically the
correctness of programs against the specifications given by separation logic for-
mulas with inductive definitions. Nevertheless, the lemmas are still supposed to
be provided by the users in DRYAD, while our approach can generate the lem-
mas automatically. Moreover, DRYAD does not provide an independent solver
to decide the entailment of separation logic formulas, which makes difficult to
compare the performance of our tool with that of DRYAD. In addition, the in-
ductive definitions used in our paper enable succinct lemmas, far less complex
than those used in DRYAD, which include complex constraints on data variables
and the magic wand.
    The method of cyclic proofs introduced by [5] and extended recently in [9]
proves the entailment of two SL formulas by using induction on the paths of proof
trees. They are not generating the lemma, but the method is able to (soundly)
check intricate lemma given by the user, even ones which are out of the scope
of our method, e.g., lemmas concerning the predicate RList which is defined by
unfolding the list segments from the end, instead of the beginning. The cyclic
proofs method can be seen like a dynamic lemma generation using complex
reasoning on proof trees, while our method generates lemma statically by simple
checks on the inductive definitions. We think that our lemma generator could
be used in the cyclic proof method to cut proof trees.
    The tool SLIDE [14, 15] provides decision procedures for fragments of SL
based on reductions to the language inclusion problem of tree automata. Their
fragments contain no data or size constraints. In addition, the EXPTIME lower
bound complexity is an important obstacle for scalability. Our previous work [11]
introduces a decision procedure based on reductions to the membership problem
of tree automata which however is not capable of dealing with data constraints.
    The tool GRASShopper [21] is based on translations of SL fragments to
first-order logic with reachability predicates, and the use of SMT solvers to deal
with the latter. The advantage is the integration with other SMT theories to
reason about data. However, this approach considers a limited class of inductive
definitions (for linked lists and trees) and is incapable of dealing with the size
or multiset constraints, thus unable to reason about AVL or red-black trees.
    The truncation point approach [13] provides a method to specify and verify
programs based on separation logic with inductive definitions that may specify
truncated data structures with multiple holes, but it cannot deal with data con-
straints. Our approach can also be extended to cover such inductive definitions.
XVI

9     Conclusion
We proposed a novel approach for automating program proofs based on Sepa-
ration Logic with inductive definitions. This approach consists of (1) efficiently
checkable syntactic criteria for recognizing inductive definitions that satisfy cru-
cial lemmas in such proofs and (2) a novel proof strategy for applying these
lemmas. The proof strategy relies on syntactic matching of spatial atoms and on
SMT solvers for checking data constraints. We have implemented this approach
in our solver spen and applied it successfully to a representative set of examples,
coming from iterative procedures for binary search trees or lists.
    In the future, we plan to investigate extensions to more general inductive
definitions by investigating ideas from [9, 22] to extend our proof strategy. From
a practical point of view, apart from improving the implementation of our proof
strategy, we plan to integrate it into the program analysis framework Celia [6].


References

 1. P. A. Abdulla, L. Holik, B. Jonsson, O. Lengal, C. Q. Trinh, and T. Vojnar.
    Verification of heap manipulating programs with ordered data by extended forest
    automata. In ATVA, pages 224–239. Springer, 2013.
 2. T. Antonopoulos, N. Gorogiannis, C. Haase, M. I. Kanovich, and J. Ouaknine.
    Foundations for decision problems in separation logic with general inductive pred-
    icates. In FoSSaCS, pages 411–425. Springer, 2014.
 3. I. Balaban, A. Pnueli, and L. D. Zuck. Shape analysis by predicate abstraction.
    In VMCAI, pages 164–180. Springer, 2005.
 4. J. Berdine, C. Calcagno, and P. W. O’Hearn. Symbolic execution with separation
    logic. In APLAS, pages 52–68. Springer, 2005.
 5. J. Brotherston, D. Distefano, and R. L. Petersen. Automated cyclic entailment
    proofs in separation logic. In CADE, pages 131–146. Springer, 2011.
 6. CELIA. http://www.liafa.univ-paris-diderot.fr/celia.
 7. W.-N. Chin, C. David, H. H. Nguyen, and S. Qin. Automated verification of shape,
    size and bag properties via user-defined predicates in separation logic. Sci. Comput.
    Program., 77(9):1006–1036, 2012.
 8. A. Chlipala. Mostly-automated verification of low-level programs in computational
    separation logic. In PLDI, volume 46, pages 234–245. ACM, 2011.
 9. D. Chu, J. Jaffar, and M. Trinh. Automating proofs of data-structure properties
    in imperative programs. CoRR, abs/1407.6124, 2014.
10. B. Cook, C. Haase, J. Ouaknine, M. Parkinson, and J. Worrell. Tractable reasoning
    in a fragment of separation logic. In CONCUR, pages 235–249. Springer, 2011.
11. C. Enea, O. Lengál, M. Sighireanu, and T. Vojnar. Compositional entailment
    checking for a fragment of separation logic. In APLAS, pages 314–333. Springer,
    2014.
12. C. Enea, M. Sighireanu, and Z. Wu. On automated lemma generation for separation
    logic with inductive definitions. Technical Report hal-01175732, HAL, 2015.
13. B. Guo, N. Vachharajani, and D. I. August. Shape analysis with inductive recursion
    synthesis. In PLDI, pages 256–265. ACM, 2007.
14. R. Iosif, A. Rogalewicz, and J. Simacek. The tree width of separation logic with
    recursive definitions. In CADE, pages 21–38. Springer, 2013.
                                                                               XVII

15. R. Iosif, A. Rogalewicz, and T. Vojnar. Deciding entailments in inductive separa-
    tion logic with tree automata. In ATVA, pages 201–218. Springer, 2014.
16. S. Itzhaky, A. Banerjee, N. Immerman, O. Lahav, A. Nanevski, and M. Sagiv.
    Modular reasoning about heap paths via effectively propositional formulas. In
    POPL, pages 385–396. ACM, 2014.
17. H. H. Nguyen and W.-N. Chin. Enhancing program verification with lemmas. In
    CAV, pages 355–369, 2008.
18. P. W. O’Hearn, J. C. Reynolds, and H. Yang. Local reasoning about programs
    that alter data structures. In CSL, pages 1–19, 2001.
19. E. Pek, X. Qiu, and P. Madhusudan. Natural proofs for data structure manipula-
    tion in C using separation logic. In PLDI, pages 440–451. ACM, 2014.
20. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic using SMT. In
    CAV, pages 773–789. Springer, 2013.
21. R. Piskac, T. Wies, and D. Zufferey. Automating separation logic with trees and
    data. In CAV, pages 711–728. Springer, 2014.
22. X. Qiu, P. Garg, A. Stefănescu, and P. Madhusudan. Natural proofs for structure,
    data, and separation. In PLDI, pages 231–242. ACM, 2013.
23. Z. Rakamaric, J. Bingham, and A. J. Hu. An inference-rule-based decision proce-
    dure for verification of heap-manipulating programs with mutable data and cyclic
    data structures. In VMCAI, pages 106–121. Springer, 2007.
24. J. C. Reynolds. Separation logic: A logic for shared mutable data structures. In
    LICS, pages 55–74. ACM, 2002.
25. SPEN. http://www.liafa.univ-paris-diderot.fr/spen.
26. K. Zee, V. Kuncak, and M. Rinard. Full functional verification of linked data
    structures. In PLDI, pages 349–361. ACM, 2008.
XVIII

A       Proofs in Sec. 4

Theorem 1. Suppose that P is a set of inductively defined predicates. If P ∈ P
is syntactically compositional, then P is semantically compositional.

Proof. Suppose P is syntactically compositional and has parameters (~  ~ ξ~ ).
                                                                    α, β,
   It is sufficient to prove the following claim.

      For each pair (s, h), if (s, h) |= P (~    ~ 2 , ξ~′ ) ∗ P (~
                                            α1 , α                     ~ 3 , ξ~′ ), then (s, h) |=
                                                                  α2 , α
      P (~          ~′
              ~ 3 , ξ ).
         α1 , α

    We prove the claim by induction on the size of ldom(h).
    Suppose for each i : 1 ≤ i ≤ 3, α          ~ i = Ei vi , where Ei and vi are respectively
location and data variables.
    Since (s, h) |= P (~        ~ 2 , ξ~′ ) ∗ P (~
                           α1 , α                     ~ 3 , ξ~′ ), there are h1 , h2 such that h =
                                                 α2 , α
h1 ∗ h2 , (s, h1 ) |= P (~    ~ 2 , ξ~ ), and (s, h2 ) |= P (~
                         α1 , α       ′                                 ~ 3 , ξ~′ ).
                                                                   α2 , α
                    V2
    If (s, h1 ) |=     α1,i = α2,i ∧ emp, then ldom(h1 ) = ∅, and h2 = h. From this,
                       i=1
we deduce that (s, h) |= P (~                 α1 , α~ 3 , ξ~′ ).
     Otherwise, there are a recursive rule of P , say P (~                              α, β,~ ξ~ ) ::= ∃X.   ~ Π ∧
                        ~   ~
Σ1 ∗ Σ2 ∗ P (~γ , β, ξ ), and an extension of s, say s , such that (s , h1 ) |= Π ′ ∧
                                                                                 ′                     ′

Σ1′ ∗ Σ2′ ∗ P (γ~′ , α    ~ 2 , ξ~′ ), where Π ′ , Σ1′ , Σ2′ , γ ′ are obtained from Π, Σ1 , Σ2 , γ by
replacing α        ~ ξ~ with α~1 , α
               ~ , β,                     ~ 2 , ξ~′ respectively. From this, we deduce that there are
h1,1 , h1,2 , h1,3 such that h1 = h1,1 ∗ h1,2 ∗ h1,3 , (s′ , h1,1 ) |= Σ1′ , (s′ , h1,2 ) |= Σ2′ ,
and (s′ , h1,3 ) |= P (γ~′ , α       ~ 2 , ξ~′ ). Then (s′ , h1,3 ∗ h2 ) |= P (γ~′ , α    ~ 2 , ξ~′ ) ∗ P (~    ~ 3 , ξ~′ ).
                                                                                                           α2 , α
From the induction hypothesis, we deduce that (s , h1,3 ∗ h2 ) |= P (γ~′ , α      ′
                                                                                                                ~ 3 , ξ~′ ).
            ′
Then (s , h1,1 ∗ h1,2 ∗ h1,3 ∗ h2 ) |= Π ∧ Σ1 ∗ Σ2 ∗ P (γ , α  ′      ′        ′    ~′       ~′
                                                                                       ~ 3 , ξ ). We then deduce
that (s, h) |= ∃X.      ~ Π ′ ∧ Σ1′ ∗ Σ2′ ∗ P (γ~′ , α            ~ 3 , ξ~′ ).
     To prove (s, h) |= P (α~1 , α            ~ 3 , ξ~′ ), it is sufficient to prove that (s, h) |= ∃X.       ~ Π ′′ ∧
  ′′      ′′
Σ1 ∗ Σ2 ∗ P (γ , α  ~′′          ~′                    ′′      ′′   ′′ ~′′
                          ~ 3 , ξ ), where Π , Σ1 , Σ2 , γ are obtained from Π, Σ1 , Σ2 , ~γ by
replacing α        ~ ξ~ with α
               ~ , β,                     ~ 3 , ξ~′ respectively.
                                     ~ 1, α
     From the fact that no variables from β                           ~ occur in Π, Σ1 , Σ2 , or ~γ , we know
that Π ′′ = Π ′ , Σ1′′ = Σ1′ , Σ2′′ = Σ2′ , and γ~′′ = γ~′ . Since (s, h) |= ∃X.                         ~ Π ′ ∧ Σ1′ ∗
Σ2′ ∗ P (γ~′ , α~ 3 , ξ~′ ), we have already proved that (s, h) |= ∃X.                        ~ Π ′′ ∧ Σ1′′ ∗ Σ2′′ ∗
     ~′′
P (γ , α       ~′
         ~ 3 , ξ ). The proof is done.                                                                                    ⊓
                                                                                                                          ⊔


B       Proofs in Sec. 5

Theorem 2. Let P ∈ P be a syntactically compositional predicate with the
parameters (~     ~ ξ),
               α, β, ~ and P ′ ∈ P with the parameters (~   α, ξ~ ). If P ′ is a completion
                               ′    ~
                                 α, ξ ) ⇔ P (~
of P with respect to ~c, then P (~                  ~        ~ P (~
                                             α, ~c, ξ ) and ∃β.         ~ ξ~ )∗P ′ (β,
                                                                     α, β,          ~ ξ~ ) ⇒
  ′
P (~α, ξ~ ) hold.
                                                                                                       XIX

Proof. The fact P ′ (~     ~ ⇔ P (~
                       α, ξ)                ~ can be proved easily by an induction on
                                     α, ~c, ξ)
the size of the domain of the heap structures.
     The argument for ∃β.  ~ P (~   ~ ξ)∗P
                                 α, β, ~       ′ ~ ~
                                                (β, ξ) ⇒ P ′ (~   ~ goes as follows: Suppose
                                                               α, ξ)
(s, h) |= P (~   ~ ξ)∗P
              α, β, ~   ′  ~ ξ).
                          (β, ~ Then there are h1 , h2 such that h = h1 ∗h2 , (s, h1 ) |=
P (~   ~  ~                         ~ ξ).
    α, β, ξ), and (s, h2 ) |= P ′ (β,  ~ From the fact that P ′ (β,      ~ ξ)
                                                                            ~ ⇔ P (β,  ~ ~c, ξ),
                                                                                             ~
                                  ~    ~
we know that (s, h2 ) |= P (β, ~c, ξ). Therefore, (s, h) |= P (~           ~  ~        ~     ~
                                                                        α, β, ξ) ∗ P (β, ~c, ξ).
From Theorem 1, we deduce that (s, h) |= P (~                 ~ From the fact P (~
                                                       α, ~c, ξ).                         ~ ⇔
                                                                                   α, ~c, ξ)
P ′ (~  ~ we conclude that (s, h) |= P ′ (~
     α, ξ),                                        ~
                                                α, ξ).                                        ⊓
                                                                                              ⊔

Theorem 3. Let P, P ′ ∈ P be two syntactically compositional inductively defined
predicates with the same set of parameters (~      ~ ξ~ ). If P ′ is stronger than P ,
                                                α, β,
                      ′
then the entailment P (~   ~  ~
                        α, β, ξ ) ⇒ P (~  ~  ~         ~ P ′ (~
                                       α, β, ξ ) and ∃β.          ~ ξ~ ) ∗ P (β,
                                                              α, β,           ~ ~γ , ξ~ ) ⇒
   α, ~γ , ξ~ ) hold.
P (~

Proof. We first show that P ′ (~      ~ ξ~ ) ⇒ P (~
                                  α, β,              ~ ξ~ ). By induction on the size
                                                  α, β,
of ldom(h), we prove the following fact: For each (s, h), if (s, h) |= P ′ (~  ~ ξ~ ),
                                                                            α, β,
then (s, h) |= P (~  ~ ξ~ ).
                  α, β,
    Suppose (s, h) |= P ′ (~  ~ ξ~ ).
                           α, β,
                 V2
    If (s, h) |=    αi = βi ∧ emp, since P ′ and P have the same base rule, we
                    i=1
deduce that (s, h) |= P (~         ~ ξ~ ).
                                α, β,
      Otherwise, there are a recursive rule of P ′ , say P ′ (~         α, β, ~ ξ~ ) ::= ∃X. ~ Π ′ ∧ Σ1 ∗
           ′    ~  ~
Σ2 ∗ P (~γ , β, ξ ), and an extension of s, say s , such that (s , h) |= Π ′ ∧ Σ1 ∗ Σ2 ∗
                                                            ′                   ′

          ~ ξ~ ). Then there are h1 , h2 , h3 such that h = h1 ∗ h2 ∗ h3 , (s′ , h1 ) |= Σ1 ,
P ′ (~γ , β,
(s′ , h2 ) |= Σ2 , and (s′ , h3 ) |= P ′ (~γ , β, ~ ξ~ ). From the induction hypothesis, we
                     ′                ~  ~
deduce that (s , h3 ) |= P (~γ , β, ξ ). Moreover, from the assumption, we know that
there is a recursive rule of P of the form P (~                    ~ ξ~ ) ::= ∃X.
                                                                α, β,               ~ Π ∧ Σ1 ∗ Σ2 ∗
         ~ ξ~ ), such that Π ′ ⇒ Π holds. Then it follows that (s′ , h1 ∗ h2 ∗ h3 ) |=
P (~γ , β,
Π ∧Σ1 ∗Σ2 ∗P (~γ , β,  ~ ξ~ ). We then deduce that (s, h) |= ∃X.         ~ Π ∧Σ1 ∗Σ2 ∗P (~γ , β,      ~ ξ~ ).
From this, we conclude that (s, h) |= P (~                ~   ~
                                                      α, β, ξ ).
      We then prove the second claim of the theorem.
      From the argument above, we know that P ′ (~                     ~ ξ~ ) ⇒ P (~
                                                                    α, β,                    ~ ξ~ ) holds.
                                                                                         α, β,
Then P (~    ′    ~ ξ~ ) ∗ P (β,
               α, β,           ~ ~γ , ξ~ ) ⇒ P (~      ~ ξ~ ) ∗ P (β,
                                                   α, β,              ~ ~γ , ξ~ ) holds. In addition,
from Theorem 1, we know that P (~                α, β, ξ ) ∗ P (β, ~γ , ξ~ ) ⇒ P (~
                                                    ~   ~           ~                    α, ~γ , ξ~ ) holds.
Therefore,we conclude that P (~          ′    ~  ~          ~     ~
                                           α, β, ξ ) ∗ P (β, ~γ , ξ ) ⇒ P (~           ~
                                                                               α, ~γ , ξ ).                ⊓
                                                                                                           ⊔

Theorem 4. Let P ∈ P be a syntactically compositional predicate with the pa-
rameters (~       ~ ξ~ ) and P ′ ∈ P be an inductive predicate with the parameters
               α, β,
(~  ~ ξ~′ ). If P ′ is a static-parameter contraction of P with the contraction func-
 α, β,
tion η, then P ′ (~      ~ ξ~′ ) ⇔ P (~
                     α, β,               ~ η(ξ~ )) and ∃β.
                                      α, β,             ~ P (~  ~ η(ξ~ )) ∗ P ′ (β,
                                                             α, β,               ~ ~γ , ξ~′ ) ⇒
  ′
P (~        ~′
    α, ~γ , ξ ) hold.

Proof. The first claim can be proved by induction on the size of the domain of
the heap structures.
XX

     The argument for the second claim goes as follows: From the fact that
     ~ ~γ , ξ~′ ) ⇔ P (β,
P ′ (β,                ~ ~γ , η(ξ~ )), we deduce that

         ~ P (~
        ∃β.      ~ η(ξ~ )) ∗ P ′ (β,
              α, β,               ~ ~γ , ξ~′ ) ⇒ P (~  ~ η(ξ~ )) ∗ P (β,
                                                    α, β,             ~ ~γ , η(ξ~ )).

     From Theorem 1, we know that

                   P (~  ~ η(ξ~ )) ∗ P (β,
                      α, β,             ~ ~γ , η(ξ~ )) ⇒ P (~
                                                            α, ~γ , η(ξ~ )).

                                               α, ~γ , η(ξ~ )) ⇔ P ′ (~
Then the second claim follows from the fact P (~                      α, ~γ , ξ~′ ).    ⊓
                                                                                        ⊔


C      Extensions of the lemmas
In this section, we discuss how the the basic idea of syntactical compositionality
can be extended in various ways.

C.1     Multiple location and data parameters
At first, we would like to emphasize that although we restrict our discussions on
compositional predicates P (~   ~ ξ)
                             α, β, ~ to the special case that α        ~ contain
                                                              ~ (resp. β)
only two parameters: one location parameter, and one data parameter. But all
the results about the lemmas can be generalized smoothly to the situation that
~ and β
α       ~ contain multiple location and data parameters.


C.2     Pseudo-composition lemmas
We then consider syntactically pseudo-compositional predicates.
   We still use the binary search trees to illustrate the idea.
   Suppose neqbsthole is the predicate defined by the same rules as bsthole,
with the modification that E 6= F is added to the body of each inductive rule.
Then neqbsthole is not syntactically compositional anymore and the composition
lemma
     ∃E2 , M2 . neqbsthole(E1 , M1 , E2 , M2 ) ∗ neqbsthole(E2 , M2 , E3 , M3 ) ⇒
                                                       neqbsthole(E1 , M1 , E3 , M3 )

does not hold. This is explained as follows: Suppose h = h1 ∗h2 (where h = h1 ∗h2
denotes that h1 and h2 are domain disjoint and h is the union of h1 and h2 ),
(s, h1 ) |= neqbsthole(E1 , M1 , E2 , M2 ) and (s, h2 ) |= neqbsthole(E2 , M2 , E3 , M3 ),
in addition, both ldom(h1 ) and ldom(h2 ) are nonempty. Then from the inductive
definition of neqbsthole, we deduce that s(E1 ) 6= s(E2 ) and s(E2 ) 6= s(E3 ). On
the other hand, (s, h) |= bsthole1(E1 , M1 , E3 , M3 ) requires that s(E1 ) 6= s(E3 ),
which cannot be inferred from s(E1 ) 6= s(E2 ) and s(E2 ) 6= s(E3 ) in general.
Nevertheless, the entailment
 ∃E2 , M2 . neqbsthole(E1 , M1 , E2 , M2 ) ∗ neqbsthole(E2 , M2 , E3 , M3 ) ∗
            E3 7→ ((lef t, X), (right, Y ), (data, v)) ⇒
            neqbsthole(E1 , M1 , E3 , M3 ) ∗ E3 7→ ((lef t, X), (right, Y ), (data, v))
                                                                                         XXI

holds since the information E1 6= E3 can be inferred from the fact that E3 is
allocated and separated from E1 . Therefore, intuitively, in this situation, the
composition lemma can be applied under the condition that we already know
that E1 6= E3 . We call this as pseudo-compositionality. Our decision procedure
can be generalized to apply the pseudo-composition lemmas when proving the
entailment of two formulas.

C.3    Data structures with parent pointers
Next, we show how our ideas can be generalized to the data structures with
parent pointers, e.g. doubly linked lists or trees with parent pointers. We use
binary search trees with parent pointers to illustrate the idea. We can define the
predicates prtbst(E, P r, M ) and prtbsthole(E, P r1 , M1 , F, P r2 , M2 ) to describe
respectively binary search trees with parent pointers and binary search trees
with parent pointers and one hole. The intuition of E, F are still the source
and the hole, while P r and P r1 (resp. P r2 ) are the parent of E (resp. F ) (the
definition of prtbst is omitted here).

prtbsthole(E, P r1 , M1 , F, P r2 , M2 ) ::= E = F ∧ emp ∧ P r1 = P r2 ∧ M1 = M2
prtbsthole(E, P r1 , M1 , F, P r2 , M2 ) ::= ∃X, Y, M3 , M4 , v.
                              E 7→ {(lef t, X), (right, Y ), (parent, P r1 ), (data, v)}
                             ∗ prtbst(X, E, M3 ) ∗ prtbsthole(Y, E, M4 , F, P r2 , M2 )
                             ∧ M1 = {v} ∪ M3 ∪ M4 ∧ M3 < v < M4
prtbsthole(E, P r1 , M1 , F, P r2 , M2 ) ::= ∃X, Y, M3 , M4 , v.
                             E 7→ {(lef t, X), (right, Y ), (parent, P r1 ), (data, v)}
                             ∗ prtbsthole(X, E, M3 , F, P r2 , M2 ) ∗ prtbst(Y, E, M4 )
                             ∧ M1 = {v} ∪ M3 ∪ M4 ∧ M3 < v < M4

Then the predicate prtbsthole enjoys the composition lemma

 ∃E2 , P r2 , M2 . prtbsthole(E1 , P r1 , M1 , E2 , P r2 , M2 ) ∗
                   prtbsthole(E2 , P r2 , M2 , E3 , P r3 , M3 ) ⇒
                                               prtbsthole(E1 , P r1 , M1 , E3 , P r3 , M3 ).

C.4    Points-to atom in base rules
Finally, we discuss the constraint that the base rule of a syntactically composi-
tional predicate has an empty spatial atom. We use the predicates lsegeven and
lsegodd to illustrate the idea.

 lsegeven(E, F ) ::= E = F ∧ emp,
 lsegeven(E, F ) ::= ∃X, Y. E 7→ (next, X) ∗ X 7→ (next, Y ) ∗ lsegeven(Y, F ).

The definition of lsegodd(E, F ) can be obtained from that of lsegeven(E, F ) by
replacing the base rule with the rule lsegodd(E, F ) ::= E 7→ (next, F ). The only
difference between the inductive definition of lsegeven and and that of lsegodd
XXII

is that lsegeven has an empty base rule, while lsegodd does not. From this, we
deduce that
            lsegodd(E, F ) ⇔ ∃X. E 7→ {(next, X)} ∗ lsegeven(X, F ).
This idea can be generalized to arbitrary syntactically compositional predicates.


D      Full example of Sec. 6
We provide here the full details of the example considered in Section 6.
   Consider the following entailment which states that two cells linked by the
next pointer field, and storing ordered data values, form a sorted list segment:
          ϕ1 ::= x1 6= nil ∧ x2 6= nil ∧ v1 < v2 ∧ x1 7→ {(next, x2 ), (data, v1 )}
                                                 ∗ x2 7→ {(next, nil), (data, v2 )}
          ϕ2 ::= ∃M. lseg(x1 , M, nil, ∅) ∧ v2 ∈ M,
where lseg has been defined in Sec. 1 (eq. (3)–(4)).
   For convenience, let
       Π1 ::= x1 6= nil ∧ x2 6= nil ∧ v1 < v2 ,
       Σ1 ::= x1 7→ {(next, x2 ), (data, v1 )} ∗ x2 7→ {(next, nil), (data, v2 )},
       Π2 ::= v2 ∈ M,
       Σ2 ::= lseg(x1 , M, nil, ∅).
The first application of the rule Slice. Since the right-hand side contains a
single spatial atom, the rule Slice generates a sub-goal Π1 ∧Σ1 |=η ∃M. Σ2 . For
the sub-goal, the syntactic matching (rule Match1) cannot be applied. Instead,
we apply the rule Lemma using a lemma L that corresponds to the inductive
rule of lseg, i.e., eq. (4) (page II):
  L ::= ∃X, M1 , v. x1 7→ {(next, X), (data, v)} ∗ lseg(X, M1 , nil, ∅)∧
                                M = {v} ∪ M1 ∧ v ≤ M1 ⇒ lseg(x1 , M, nil, ∅).
For convenience, let
              Π ::= M = {v} ∪ M1 ∧ v ≤ M1 ,
              Σ ::= x1 7→ {(next, X), (data, v)} ∗ lseg(X, M1 , nil, ∅).
The first application of the rule Lemma. Since root(L) ::= x1 7→
{(next, X), (data, v)}, the rule Lemma generates a sub-goal Π1 ∧ Σ1′ |=SUB           η1
∃X, v. root(L), where Σ1′ ::= x1 7→ {(next, x2 ), (data, v1 )}. Then the rule
Match1 is applied, resulting in a quantifier instantiation η1 = {X → x2 , v →
v1 }. Note that, since EQ(η1 |free(∃X,v.root(L))) ::= true, the entailment Π1 ∧
EQ(η1 |{X,v} ) |= EQ(η1 |free(∃X,v.root(L)) ) holds. The variable substitution η1 is used
to instantiate the existentially quantified variables in the remaining part of the
lemma, that is, Π ∧ lseg(X, M1 , nil, ∅), resulting into the formula
          η1 (Π ∧ lseg(X, M1 , nil, ∅)) ::=
                        M = {v1 } ∪ M1 ∧ v1 ≤ M1 ∧ lseg(x2 , M1 , nil, ∅).
                                                                                        XXIII

Then, the rule Lemma generates another sub-goal Π1 ∧ Σ1′′ |=η2 ∃M, M1 . η1 (Π ∧
lseg(X, M1 , nil, ∅)), where Σ1′′ ::= x2 7→ {(next, nil), (data, v2 )}.
The second application of the rule Slice. For the sub-goal Π1 ∧ Σ1′′ |=η2
∃M, M1 . η1 (Π ∧lseg (X, M1 , nil, ∅)), the rule Slice is applied again. Since there is
a single spatial atom in the RHS, the rule Slice generates a sub-goal Π1 ∧Σ1′′ |=η3
∃M1 . lseg(x2 , M1 , nil, ∅).
The second application of the rule Lemma. For the sub-goal Π1 ∧ Σ1′′ |=η3
∃M1 . lseg(x2 , M1 , nil, ∅), the rule Lemma is applied again, using the lemma L′
(still corresponding to the inductive rule of lseg),

L′ ::= ∃X ′ , M1′ , v ′ . x2 7→ {(next, X ′ ), (data, v ′ )} ∗ lseg(X ′ , M1′ , nil, ∅)∧
                                    M1 = {v ′ } ∪ M1′ ∧ v ′ ≤ M1′ ⇒ lseg(x2 , M1 , nil, ∅).

For convenience, let
             Π ′ ::= M1 = {v ′ } ∪ M1′ ∧ v ′ ≤ M1′ ,
             Σ ′ ::= x2 7→ {(next, X ′ ), (data, v ′ )} ∗ lseg(X ′ , M1′ , nil, ∅).

Since root(L′ ) ::= x2 7→ {(next, X ′ ), (data, v ′ )}, the rule Lemma generates a
sub-goal Π1 ∧ Σ1′′ |=SUB     η1′    ∃X ′ , v ′ . root(L′ ). Then the rule Match1 is applied,
resulting in a quantifier instantiation η1′ = {X ′ → nil, v ′ → v2 }. Note that,
since EQ(η1′ |free(∃X ′ ,v′ .root(L′ )) ) ::= true, the entailment Π1 ∧ EQ(η1′ |{X ′ ,v′ } ) |=
EQ(η1′ |free(∃X ′ ,v′ .root(L′ )) ) holds. The variable substitution η1′ is used to instan-
tiate the existentially quantified variables in the remaining part of the lemma,
that is, Π ′ ∧ lseg(X ′ , M1′ , nil, ∅), resulting into the formula

     η1′ (Π ′ ∧ lseg(X ′ , M1′ , nil, ∅)) ::=
                                  M1 = {v2 } ∪ M1′ ∧ v2 ≤ M1′ ∧ lseg(nil, M1′ , nil, ∅).

Then, the rule Lemma generates another sub-goal Π1 ∧ emp                                   |=η2′
∃M1 , M1′ . η1′ (Π ′ ∧ lseg(X ′ , M1′ , nil, ∅)).
The third application of the rule Slice. For the sub-goal Π1 ∧ emp |=η2′
∃M1 , M1′ . η1′ (Π ′ ∧ lseg(X ′ , M1′ , nil, ∅)), since there is only one spatial atom
lseg(nil, M1′ , nil, ∅) in the RHS, the rule Slice generates a subgoal Π1 ∧ emp |=η3′
∃M1′ . lseg(nil, M1′ , nil, ∅), for which the rule Lemma is applied, with a lemma L′′
corresponding to the base rule of lseg, i.e., eq. (3) (page II),

             L′′ ::= nil = nil ∧ emp ∧ M1′ = ∅ ⇒ lseg(nil, M1′ , nil, ∅).

The third application of the rule Lemma. Since root(L′′ ) ::= emp, the
rule Lemma generates a sub-goal Π1 ∧ emp |=SUB           η1′′  root(L′′ ). Then the rule
Match1 is applied, resulting in a quantifier instantiation η1′′ = ∅. Note
that, since EQ(η1′′ |free(root(L′′ )) ) ::= true, the entailment Π1 ∧ EQ(η1′′ |∅ ) |=
EQ(η1′′ |free(root(L′′ )) ) holds. The substitution η1′′ is used to instantiate the ex-
istential variables in the remaining part of the lemma, that is, nil = nil ∧ M1′ = ∅,
resulting into the same formula. Then the rule Lemma generates a sub-goal
XXIV

Π1 |=η2′′ ∃M1′ . nil = nil ∧ M1′ = ∅, which holds clearly with η2′′ = ∅. Finally,
η1′′ ∪ η2′′ is extended with nil = nil ∧ M1′ = ∅, resulting into η3′ = {M1′ → ∅}.
The third application of the rule Slice (continued). The variable sub-
stitution η3′ is extended with M1 = {v2 } ∪ M1′ ∧ v2 ≤ M1′ , resulting into
η2′ = {M1 → {v2 } ∪ ∅, M1′ → ∅}. Then the rule Slice generates a sub-goal
Π1 ∧EQ(η2′ ) |= M1 = {v2 }∪M1′ ∧v2 ≤ M1′ . Because EQ(η2′ ) = M1 = {v2 }∪∅∧M1′ =
∅, we know that EQ(η2′ ) |= M1 = {v2 } ∪ M1′ ∧ v2 ≤ M1′ . Thus the sub-goal holds.
The second application of the rule Lemma (continued). The variable sub-
stitution η1′ ∪ η2′ should be extended with Π ′ ::= M1 = {v ′ } ∪ M1′ ∧ v ′ ≤ M1′ .
Since M1 ∈ dom(η2′ ), the extension makes no effect. Then η3 = (η1′ ∪ η2′ )|{M1 } =
{M1 → {v2 } ∪ ∅}.
The second application of the rule Slice (continued). The variable sub-
stitution η3 is extended with M = {v1 } ∪ M1 ∧ v1 ≤ M1 , resulting into η2 =
{M → {v1 } ∪{v2 } ∪∅, M1 → {v2 } ∪∅}. Then the rule Slice generates a sub-goal
Π1 ∧EQ(η2 ) |= M = {v1 }∪M1 ∧v1 ≤ M1 . Since Π1 ::= x1 6= nil∧x2 6= nil∧v1 < v2
and EQ(η2 ) ::= M = {v1 } ∪ {v2 } ∪ ∅ ∧ M1 = {v2 } ∪ ∅, the sub-goal holds.
The first application of the rule Lemma (continued). The variable substi-
tution η1 ∪ η2 should be extended with Π ::= M = {v} ∪ M1 ∧ v ≤ M1 . Since
M ∈ dom(η1 ∪η2 ), this extension makes no effect. Then η is obtained from η1 ∪η2
by restricting to {M }. So η = {M → {v1 } ∪ {v2 } ∪ ∅}.
The first application of the rule Slice (continued). The variable substi-
tution η is extended with Π2 ::= v2 ∈ M , and still getting η. Finally, Slice
generates the sub-goal Π1 ∧ EQ(η) |= Π2 . Since EQ(η) ::= M = {v1 } ∪ {v2 } ∪ ∅,
the entailment EQ(η) |= Π2 holds. Therefore, the sub-goal Π1 ∧EQ(η) |= Π2 holds
as well.
