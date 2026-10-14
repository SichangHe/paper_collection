                        Verified Path Indexing

                Mohamed Chaabani1,2         and Simon Robillard1(B)
        1
            LIRMM, Université de Montpellier and CNRS, Montpellier, France
                  {mohamed.chaabani,simon.robillard}@lirmm.fr
               2
                 LIMOSE, University of Boumerdès, Boumerdès, Algeria



       Abstract. The indexing of syntactic terms is a key component for
       the eﬃcient implementation of automated theorem provers. This paper
       presents the ﬁrst veriﬁed implementation of a term indexing data struc-
       ture, namely a formalization of path indexing in the proof assistant
       Isabelle/HOL. We deﬁne the data structure, maintenance operations,
       and retrieval operations, including retrieval of uniﬁable terms, instances,
       generalizations and variants. We prove that maintenance operations pre-
       serve the invariants of the structure, and that retrieval operations are
       sound and complete.


1    Introduction

In the realm of program veriﬁcation, automated deduction algorithms hold a
special place. They are a cornerstone of automated program veriﬁcation, and as
such, they are also a natural target for veriﬁcation. Indeed, veriﬁed automated
deduction programs would be useful not only as trusted implementations, but
also as witnesses to the usability of program veriﬁcation. After all, if the program
veriﬁcation community hopes to convince industrial actors to adopt and use its
techniques for software development, it should ﬁrst be able to do the same.
    However, automated deduction algorithms present a particularly diﬃcult
challenge for formal veriﬁcation, as they rely on a rich and complex meta-
theory, as well as on optimized implementations and data structures that are
crucial for performance. Many eﬀorts have been undertaken to formalize the
meta-theory of CDCL SAT solving [1], ﬁrst-order resolution [10], or saturation
theorem proving [13]. These formalizations focus on high-level properties of the
calculi used in automated reasoning tools. They are typically expressed in a
relational rather than functional style, and thus do not directly yield executable
programs. The second step toward formal veriﬁcation of automated deduction
techniques is to formalize and verify the algorithms and data structures used
to implement the calculi. State-of-the-art (non-veriﬁed) automated deduction
tools employ advanced algorithms and data structures. In order to obtain ver-
iﬁed executable automated reasoning tools with a decent performance, these
implementation-oriented details have to be veriﬁed as well. For example, the
veriﬁed SAT solver IsaSAT [2] relies on a two-watched-literal data structure for
unit propagation and conﬂict detection, similarly to its unveriﬁed competitors.
 c The Author(s) 2025
C. Barrett and U. Waldmann (Eds.): CADE 2025, LNAI 15943, pp. 249–260, 2025.
https://doi.org/10.1007/978-3-031-99984-0_14
250      M. Chaabani and S. Robillard

    Automated reasoning tools for ﬁrst-order logic are signiﬁcantly more complex
than those for propositional logic, and for now, a veriﬁed executable prover for
ﬁrst-order logic has yet to be implemented. One key ingredient for performance
in automated reasoning in ﬁrst-order logic is eﬃcient term indexing. Virtually
all modern reasoning techniques for ﬁrst-order logic are based on term uniﬁca-
tion, and therefore require a way to ﬁnd uniﬁable terms among a set of candi-
dates. The term uniﬁcation problem is quasi-linear in the size of the candidate
terms, but since theorem provers can handle millions of candidates, it is not fea-
sible to iterate through pairs of candidates and attempt to unify them. Instead,
theorem provers rely on specialized data structures to store terms and retrieve
those that are uniﬁable with a given query term.
    This paper presents the formalization1 , in the Isabelle/HOL proof assis-
tant [7, 8], of path indexing [9,12], a term indexing technique that relies on a
trie to store candidate terms. After an introduction to Isabelle/HOL (Sect. 2)
and its notations, and some preliminary notions on terms and term index-
ing (Sect. 3), this paper presents the formalization of path indexing (Sect. 4).
We deﬁne the data structure, its invariants, maintenance and retrieval opera-
tions, and we sketch the correctness proofs for the diﬀerent operations. This
work represents the ﬁrst veriﬁed implementation of a term indexing technique.
Although path indexing has been studied from the perspective of implementa-
tion and performance [3, 6], this is also, to our knowledge, the ﬁrst detailed proof
of correctness for this technique.


2     Proofs and Programs in Isabelle/HOL

Isabelle/HOL is an interactive proof assistant for higher-order logic. It oﬀers
powerful features that simplify and automate the proof process: its rewriting
engine allows substituting terms with equivalents, the axiom of substitution
allows replacing any subterm of the proof with an equal term, and the rule
of extensionality allows proving the equality of two functions by proving that
they produce the same result for each argument.
    Isabelle allows the deﬁnition of inductive datatypes. For example, the type
of lists can be deﬁned as follows:
datatype a list =
   Nil ([])
 | Cons (hd : a) (tl : a list) (infix # 65 )

   This is a polymorphic deﬁnition with a type parameter a, that declares
Nil and Cons as the two constructors of the type. In addition, it also deﬁnes
two partial functions hd and tl to access the two arguments of lists built from
Cons, and adds notations [] and # for the constructors, the second being an
inﬁx operator. Predicates can likewise be deﬁned inductively, for example list
membership can be deﬁned as:

1
    Available at https://seaﬁle.lirmm.fr/f/d76bb08ee2cf4cacb823/.
                                                     Veriﬁed Path Indexing      251

inductive ListMem :: a ⇒ a list ⇒ bool where
  ListMem x (x # xs)
| ListMem x xs =⇒ ListMem x (y # xs)

In this deﬁnition, Isabelle’s metalogical implication, =⇒, is used to set the condi-
tion for the second case. Within statements, the object-logic implication, denoted
−→ must be used instead. The ﬁrst notation is not to be confused with the nota-
tion for function types, ⇒.
    We can also deﬁne functions such as the following
fun nth :: a list ⇒ nat ⇒ a where
  nth [] n = undefined
| nth (x # xs) n = (case n of 0 ⇒ x | Suc m ⇒ nth xs m)

that performs pattern matching on a value of nat, the type of natural numbers
with constructors 0 and Suc, in order to return the nth element of the list.
The Isabelle library use the inﬁx notation l ! i for nth l i, and we will use this
notation in the following. Functions can be partial (non-exhaustive), but their
termination must be proven. In simple cases such as the structural recursion
above, this obligation is discharged automatically.
    Isabelle also features type deﬁnitions that identify a new type with a subset
of an existing type. For example ﬁnite maps are deﬁned as
typedef ( a, b) fmap = {m. finite {a. m a = None} } :: ( a ⇒ b option) set

the subset of partial functions (a ⇒ b option) that are deﬁned for a ﬁnite num-
ber of values. Such a deﬁnition requires a proof that the newly deﬁned type is
inhabited. It also introduces coercion functions. The Lifting package allows func-
tions on the supertype to be conveniently adapted to the subtype, provided that
the necessary proofs of membership are given. We will use ﬁnite maps in this for-
malization, and in particular we rely on the following notations: fmempty stands
for the map that associates every value to None, fmdom m and fmran m are
the domain and range of a map m, m $$ v is the evaluation of m at value v,
while m $$! k is the evaluation of m at value v provided that v ∈ fmdom m
(i.e., $$ is a total function that returns an element of b option, while $$! returns
an element of b and may be undeﬁned).


3    Preliminaries

This formalization relies on a pre-existing deﬁnition of syntactic terms, avail-
able in the Archive of Formal Proofs (AFP), the main repository of Isabelle
formalizations. The deﬁnition is the following:
datatype ( f , v ) term =
  Var v
| Fun f ( f , v ) term list
252     M. Chaabani and S. Robillard

This deﬁnition is parameterized by a type f of function symbols, and a type v
of variables. Since there are no constraints on the number of arguments that a
function symbol is applied to, symbols in terms are uniquely identiﬁed by a pair
of type ( f × nat), the second element being the arity. For example, the term
Fun s [Fun s []] is valid but features two distinct symbols (s, 1 ) and (s, 0 ).
    A term index is a data structure that stores a set S of terms, and that is
able, given a query term t, to retrieve all the terms s ∈ S that satisfy R(s, t),
for some R called the retrieval condition. In practice, there are four retrieval
conditions that are of particular interest, all related to uniﬁcation problems (t ·
σ denotes the application of a substitution σ to a term t):
definition term-unification :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
 term-unification t1 t2 = (∃ σ :: ( f , v ) subst. t1 · σ = t2 · σ)

definition term-instantiation :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
 term-instantiation t1 t2 = (∃ σ :: ( f , v ) subst. t1 = t2 · σ)

definition term-generalization :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
 term-generalization t1 t2 = term-instantiation t2 t1

definition term-variant :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
  term-variant t1 t2 = (∃ σ :: ( f , v ) subst. (∀ t ∈ subst-range σ. is-Var t) ∧ t1 · σ =
t2 )

     For example, retrieval of uniﬁable terms is used to implement resolution
rules or to ﬁnd closing substitutions in analytical tableaux. Resolution theorem
provers rely on retrieval of instances to implement forward subsumption and
demodulation, and retrieval of generalizations for backward subsumption and
demodulation. Aside from automated deduction, other applications that perform
computations over terms can beneﬁt from term indexing, including functional
programming, logic programming and deductive databases. For an overview of
these applications, and what retrieval conditions they use, we refer the reader
to the work of Sekar et al. [11].
     Like many term indexing techniques, path indexing is a so-called imperfect
filter, i.e., its retrieval conditions are broader that the aforementioned relations.
Consequently, the set that is returned for a given query is a superset of the
intended result, and must be ﬁltered using a standard uniﬁcation algorithm
(which is also an opportunity to construct the uniﬁers, for applications that
need that information). More speciﬁcally, the retrieval conditions used in path
indexing ignores the non-linearity of terms, i.e., the fact that a single variable
may occur multiple times in the query term and/or indexed terms, and the
resulting constraints w.r.t. term uniﬁcation. Instead, it relies on the following
relations as retrieval conditions:
inductive linear-unification :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
  linear-unification (Var x ) t
| linear-unification t (Var x )
| length args1 = length args2 =⇒
                                                        Veriﬁed Path Indexing   253

   (∀ i. i < length args1 −→ linear-unification (args1 ! i) (args2 ! i)) =⇒
     linear-unification (Fun f args1 ) (Fun f args2 )


inductive linear-instance :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
  linear-instance t (Var x )
| length args1 = length args2 =⇒
    (∀ i. i < length args1 −→ linear-instance (args1 ! i) (args2 ! i)) =⇒
      linear-instance (Fun f args1 ) (Fun f args2 )


definition linear-generalization t e = linear-instance e t


inductive linear-variant :: ( f , v ) term ⇒ ( f , v ) term ⇒ bool where
  linear-variant (Var x ) (Var y)
| length args1 = length args2 =⇒
    (∀ i. i < length args1 −→ linear-variant (args1 ! i) (args2 ! i)) =⇒
      linear-variant (Fun f args1 ) (Fun f args2 )

We can check that these relations are necessary conditions for their non-linear
counterparts, and the set returned by the index for a given query is in fact a
superset of the intended result, e.g.:
lemma linear-unification-necessary-condition:
  term-unification t1 t2 =⇒ linear-unification t1 t2

    Since path indexing ignores the speciﬁc names of variables, we introduce the
following datatype to describe the symbols that it operates on, together with a
function that extracts said symbol from a term:
datatype f symbol =
  Star
| F f nat

fun to-symbol :: ( f , v ) term ⇒ f symbol where
  to-symbol (Var x ) = Star
| to-symbol (Fun f ts) = F f (length ts)

    Path indexing relies on the path strings (simply called paths in the following)
of terms to index them. A path string is a list of symbol-number pairs that
corresponds to a path from the root to a node in the tree structure of a term.
type-synonym f tpath = ( f symbol × nat) list

   Although this is not speciﬁed in the type itself, in a valid path, each symbol
s can only be paired with a number i such that i < symbol-arity s, except if
symbol-arity s = 0, in which case, i is 0 by convention.
   We may use paths to navigate a term, e.g., subterm-at-path t p t’ holds if
and only if t is the subterm found by following the path p from the root of t:
254     M. Chaabani and S. Robillard




Fig. 1. The path indexing trie that stores the four following terms:
– t1 ≡ Fun f [Fun a []],
– t2 ≡ Fun f [Var x ],
– t3 ≡ Fun g [Var x, Var y] and
– t4 ≡ Fun g [Fun f [Fun b []], Var x ].


inductive subterm-at-path :: ( f , v ) term ⇒ f tpath ⇒ ( f , v ) term ⇒ bool where
  subterm-at-path t [] t
| i < length fargs =⇒ fargs = [] =⇒ subterm-at-path (fargs ! i) p t =⇒
    subterm-at-path (Fun f fargs) ((F f (length fargs), i) # p) t

    In particular, we are interested in the paths to leaves (constant or variables)
of a term. A string p is a path to a leaf of a term t if and only if it satisﬁes
path-of-term t p, deﬁned as follows:
inductive path-of-term :: ( f , v ) term ⇒ f tpath ⇒ bool where
  path-of-term (Var x ) [(Star , 0 )]
| path-of-term (Fun f []) [(F f 0 , 0 )]
| ts = [] =⇒ i < length ts =⇒ path-of-term (ts ! i) p =⇒
    path-of-term (Fun f ts) ((F f (length ts), i) # p)

    When we mention the paths of a term t, we refer exclusively to those paths p
that satisfy path-of-term t p. For example, given the variable x and the symbols
a, f, and g, the term Fun f [Fun g [Var x ], Fun a] has two paths, namely [(F f
2, 0 ), (F g 1, 0 ), (Star, 0 )] and [(F f 2, 1 ), (F a 0, 0 )].


4     Path Indexing
4.1   Structure and Invariants

In path indexing, terms are stored in a trie, a tree structure in which edges are
decorated with symbol-number pairs. We deﬁne this structure as follows:
                                                         Veriﬁed Path Indexing        255

datatype (plugins del : size) ( f , v ) trie =
  Leaf ( f , v ) term set
| SymbolNode (children: (( f symbol , (nat, ( f , v ) trie) fmap) fmap))

Each node stores its children in nested fmaps, with the outer maps indexed by
 f symbol s and the inner maps indexed by nats. The terms themselves are stored
in the leaves of the trie. Figure 1 gives an example of a path indexing trie.
     Because the recursive structure of this datatype is obfuscated by the maps,
the size function that is automatically generated by Isabelle as a termination
measure for the datatype is of no help in this case. Instead, we deactivate this
feature and deﬁne our own function, based on the depth of the trie, prove its ter-
mination and register it as a termination measure. The proof of termination for
functions that are deﬁned by structural induction can subsequently be discharged
automatically. This is, for example, the case with the following function, that
collects all the terms stored in the trie:
fun to-set :: ( f , v ) trie ⇒ ( f , v ) term set where
  to-set (Leaf x ) = x
| to-set (SymbolNode m) =           (to-set ‘    (fmran ‘ (fmran m)))

where the backquote ‘ denotes the application of a function to all the elements
of a set.
    Just as we use paths to navigate the tree structure of terms, we can use them
to navigate tries. In particular, the trie tr2 is the subtree of the trie tr1 found
by following the path p along the edges if and only if subtrie-at-path tr1 p tr2,
deﬁned as follows:
inductive subtrie-at-path :: ( f , v ) trie ⇒ f tpath ⇒ ( f , v ) trie ⇒ bool where
  subtrie-at-path tr [] tr
| m1 $$ s = Some m2 =⇒ m2 $$ i = Some tr =⇒
    subtrie-at-path tr ps tr0 =⇒ subtrie-at-path (SymbolNode m1 ) ((s, i) # ps) tr0

    The main invariant of a path indexing trie is that each term is stored in the
leaves that are found at the end of paths of that term:
definition sound-storage :: ( f , v ) trie ⇒ bool where
 sound-storage tr =
   (∀ t p. (∃ s. subtrie-at-path tr p (Leaf (insert t s))) −→ path-of-term t p)

where insert is the set insertion function. Since a term is stored in multiple
leaves (as many as the constants and variables in that term), we must deﬁne a
second invariant that ensures that any term present in the trie is present in all
the relevant leaves of that trie:
definition complete-storage :: ( f , v ) trie ⇒ bool where
  complete-storage tr =
(∀ t∈to-set tr . ∀ p. path-of-term t p −→ (∃ s. subtrie-at-path tr p (Leaf (insert t s))))

We deﬁne a third invariant that ensures that the structure of the trie is consistent
with the arity of symbols, and that edges decorated with a symbol of arity 0 lead
to a leaf. This property is needed in many proofs to eliminate vacuous cases.
256       M. Chaabani and S. Robillard

inductive well-structured :: ( f , v ) trie ⇒ bool
and well-structured-map-entry :: f symbol ⇒ (nat, ( f , v ) trie) fmap ⇒ bool
where
  (∀ s. s ∈ fmdom m −→ well-structured-map-entry s (m $$! s)) =⇒
    well-structured (SymbolNode m)
| fmdom m = {0 } =⇒ (∀ t. t ∈ fmran m −→ (∃ s. t = Leaf s)) =⇒
    well-structured-map-entry Star m
| fmdom m = {0 } =⇒ (∀ t. t ∈ fmran m −→ (∃ s. t = Leaf s)) =⇒
    well-structured-map-entry (F f 0 ) m
| arity = 0 =⇒ fmdom m = {..< arity} =⇒
    (∀ t. t ∈ fmran m −→ well-structured t) =⇒
      well-structured-map-entry (F f arity) m
    Lastly, we deﬁne a fourth invariant that ensures that the trie contains no
empty leaves or childless nodes, except possibly the root itself. While not needed
for functional correctness, this is a desirable property that should be preserved
by maintenance operations, in particular term removal.
inductive minimal-storage :: ( f , v ) trie⇒ bool where
  x = {} =⇒ minimal-storage (Leaf x )
| (∀ t ∈ fmran m. ∀ r ∈ fmran t. minimal-storage r ∧ r = SymbolNode fmempty) =⇒
    minimal-storage (SymbolNode m)
Proofs on tries require induction, however, properties sound-storage and
complete-storage hold only for the root of the trie, and not for subtries. To
address this, these invariants must be reformulated in a way that accounts for the
position (given by a path) of a subtrie within the trie.
definition sound-storage-from-position :: ( f , v ) trie ⇒ f tpath ⇒ bool where
  sound-storage-from-position tr p =
(∀ t p2 s. subtrie-at-path tr p2 (Leaf (insert t s)) −→ path-of-term t (p @ p2 ))

definition complete-storage-from-position :: ( f , v ) trie ⇒ f tpath ⇒ bool where
 complete-storage-from-position tr p =
   (∀ t ∈ to-set tr . ∀ p2 . path-of-term t (p @ p2 ) −→
     (∃ s. subtrie-at-path tr p2 (Leaf (insert t s))))
where @ is the append operator on lists. The properties sound-storage and
complete-storage of the root are simply special cases of the above, from the
path/position []. We can easily verify that, given the correct position, these
properties hold recursively for subtries, e.g.:
lemma complete-storage-from-position-subtrie:
  assumes complete-storage-from-position (SymbolNode m1 ) p
   and m1 $$ f = Some m2 and m2 $$ i = Some tr
  shows complete-storage-from-position tr (p @ [(f , i)])
      With these invariants, we can deﬁne a new type for valid tries:
typedef ( f , v ) index = { tr :: ( f , v ) trie. well-structured tr ∧ sound-storage tr
                           ∧ complete-storage tr ∧ minimal-storage tr }
Note that the root of such a trie must be a SymbolNode. In particular the empty
trie is SymbolNode fmempty rather than an empty leaf.
                                                         Veriﬁed Path Indexing        257

4.2     Maintenance Operations

We have formalized and proved the correctness of a term insertion function
and a term deletion function. Both functions traverse the trie from the root
node to the leaves, following the paths of the term to insert/delete, updating or
creating/deleting nodes along the path as needed.
    Let us brieﬂy deﬁne some helper functions used in the insertion function.
insert-leaf tr t is deﬁned only if tr is a Leaf, in which case it adds the term
t to the terms contained in that leaf. update-entry is a higher-order function
that modiﬁes a map in the following way: given a map m, a key k, a function
f and a default value v, update-entry m k f v outputs the map that associates
k to Some (f (m $$! k )) if k is deﬁned in m, and to Some (f v ) otherwise, and
associates other keys k to m $$ k . update-entries is similar but operates on
a list of keys rather than a single key (the update function f also take the key
as parameter). We can now deﬁne the auxiliary recursive function insert-aux,
such that insert-aux tr t1 t2 is a trie where the term t2 is present in all the
leaves found on the paths of term t1.
fun insert-aux :: ( f , v ) trie ⇒ ( f , v ) term ⇒ ( f , v ) term ⇒ ( f , v ) trie where
  insert-aux (Leaf s) t t0 = undefined
| insert-aux (SymbolNode m) (Var x ) t0 =
   SymbolNode (update-entry m Star (λm2 . update-entry m2 0 (λtr . insert-leaf tr t0 )
(Leaf {})) fmempty)
| insert-aux (SymbolNode m) (Fun f []) t0 =
    SymbolNode (update-entry m (F f 0 ) (λm2 . update-entry m2 0 (λtr . insert-leaf tr
t0 ) (Leaf {})) fmempty)
| insert-aux (SymbolNode m) (Fun f fargs) t0 =
   SymbolNode (update-entry m (F f (length fargs))
      (λm2 . update-entries m2 [0 ..<length fargs] (λi tr . insert-aux tr (fargs ! i) t0 )
empty-trie) {$$})

This auxiliary function is called by the main insertion function
definition insert-term :: ( f , v ) trie ⇒ ( f , v ) term ⇒ ( f , v ) trie where
 insert-term tr t = insert-aux tr t t

      which we lift to the type of valid tries
lift-definition index-insert :: ( f , v ) index ⇒ ( f , v ) term ⇒ ( f , v ) index is
insert-term

The type of this lifted function indicates the preservation of the four invari-
ants, which we need to prove. The proof of preservation of well-structured and
minimal-storage are direct, but for sound-storage and complete-storage, we
need to generalize, e.g., for completeness, with the following lemma:
lemma insert-preserves-complete:
  assumes well-structured tr and complete-storage-from-position tr p
   and subterm-at-path t p t
  shows complete-storage-from-position (insert-aux tr t t) p
258       M. Chaabani and S. Robillard

Finally we specify the behavior of insert-term w.r.t. the content of the trie, using
the function to-set and set insertion:
lift-definition index-to-set :: ( f , v ) index ⇒ ( f , v ) term set is to-set


theorem index-insert-spec: index-to-set (index-insert tr t) = insert t (index-to-set tr )

Here, for the proof of membership of the newly inserted term, it is enough to
focus on a single arbitrary path of that term.
    The term removal function, not shown here, works in the same way as inser-
tion, however, it also ensures that leaves and nodes are deleted from the trie if
they are emptied by the removal. We prove that it preserves the invariants, and
we specify its behavior w.r.t. the content of the trie, as we did for term insertion.


4.3     Retrieval Operations

We have formalized and proved the correctness of four retrieval operations,
namely retrieval of uniﬁcations, generalizations, instances and variants. We only
present here the formalization of the retrieve-unifications function, but similar
ideas are used for the other functions.
   We ﬁrst deﬁne the function var-terms that returns all the terms in the leaf
under a Star edge, if any. We use the partial lookup function $$!, since in a
well-structured node, the key 0 must be deﬁned for the map m2.
fun var-terms :: (( f symbol , (nat, ( f , v ) trie) fmap) fmap) ⇒ ( f , v ) term set where
  var-terms m = (case m $$ Star of None ⇒ {} | Some m2 ⇒ to-set (m2 $$! 0 ))

Then we can deﬁne the main function for the retrieval of terms that are uniﬁable
with a given query term:
fun retrieve-unifications :: ( f , v ) trie ⇒ ( f , v ) term ⇒ ( f , v ) term set where
  retrieve-unifications (Leaf ts) t = undefined
| retrieve-unifications (SymbolNode m) (Var x ) = to-set (SymbolNode m)
| retrieve-unifications (SymbolNode m) (Fun f fargs) =
     var-terms m ∪
     (case m $$ (F f (length fargs)) of
        None ⇒ {}
      | Some m2 ⇒ if fargs = [] then to-set (m2 $$! 0 )
                     else   i ∈ fmdom m2 . retrieve-unifications (m2 $$! i) (fargs ! i))

      Finally we can lift the function to the type index and prove its speciﬁcation:


lift-definition index-retrieve-unifications ::
               ( f , v ) index ⇒ ( f , v ) term ⇒ ( f , v ) term set is retrieve-unifications


theorem index-retrieve-unifications-spec:
 index-retrieve-unifications tr t1 = {t2 . t2 ∈ index-to-set tr ∧ linear-unification t1 t2 }
                                                       Veriﬁed Path Indexing      259

For this, we need to show that the answer set only contains elements from to-set
that are linear uniﬁcations of the query term (soundness), and that all linear
uniﬁcations in to-set are in the answer set (completeness). Once again this is
achieved through more general inductive lemmas, e.g., for completeness:
lemma retrieve-unifications-complete:
  assumes well-structured tr and complete-storage-from-position tr p
   and sound-storage-from-position tr p
   and linear-unification t t and t ∈ to-set tr and subterm-at-path t    pt
  shows t ∈ retrieve-unifications tr t



5   Conclusion

We have presented an Isabelle/HOL formalization of path indexing, the ﬁrst
veriﬁed implementation of a term indexing data structure. In future work, we
plan to formalize other term indexing techniques, starting with discrimination
trees. While Isabelle allows code extraction, to obtain eﬃcient implementations,
we will need to verify imperative code with mutable data structures, as opposed
to the purely functional implementation presented here. Reﬁnement techniques
exist to derive, from functional Isabelle programs, Imperative HOL code [4] or
even an LLVM intermediate representation [5].

Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.


References
 1. Blanchette, J.C., Fleury, M., Lammich, P., Weidenbach, C.: A veriﬁed SAT solver
    framework with learn, forget, restart, and incrementality. J. Autom. Reason. 61,
    333–365 (2018)
 2. Fleury, M., Blanchette, J.C., Lammich, P.: A veriﬁed SAT solver with watched
    literals using imperative HOL. In: Proceedings of the 7th ACM SIGPLAN Inter-
    national Conference on Certiﬁed Programs and Proofs, pp. 158–171 (2018)
 3. Graf, P.: Path indexing for term retrieval. Technical report, Max-Planck-Institut
    für Informatik (1992)
 4. Lammich, P.: Automatic data reﬁnement. In: International Conference on Interac-
    tive Theorem Proving, pp. 84–99. Springer (2013)
 5. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In: 10th International
    Conference on Interactive Theorem Proving (ITP 2019). Schloss Dagstuhl-Leibniz-
    Zentrum für Informatik (2019)
 6. McCune, W.: Experiments with discrimination-tree indexing and path indexing
    for term retrieval. J. Autom. Reason. 9(2), 147–167 (1992)
 7. Nipkow, T., Klein, G.: Concrete semantics with Isabelle/HOL. Springer (2014)
 8. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL: a proof assistant for higher-
    order logic. LNCS, vol. 2283. Springer (2002)
260     M. Chaabani and S. Robillard

 9. Ramesh, R., Ramakrishnan, I., Warren, D.S.: Automata-driven indexing of Pro-
    log clauses. In: Proceedings of the 17th ACM SIGPLAN-SIGACT Symposium on
    Principles of Programming Languages, pp. 281–291 (1989)
10. Schlichtkrull, A., Blanchette, J., Traytel, D., Waldmann, U.: Formalizing Bachmair
    and Ganzinger’s ordered resolution prover. J. Autom. Reason. 64(7), 1169–1195
    (2020)
11. Sekar, R., Ramakrishnan, I., Voronkov, A.: Term indexing. In: Handbook of Auto-
    mated Reasoning, pp. 1853–1964. Elsevier (2001)
12. Stickel, M.E.: The path-indexing method for indexing terms. SRI International,
    Artiﬁcial Intelligence Center (1989)
13. Waldmann, U., Tourret, S., Robillard, S., Blanchette, J.: A comprehensive frame-
    work for saturation theorem proving. J. Autom. Reason., 1–41 (2022)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
