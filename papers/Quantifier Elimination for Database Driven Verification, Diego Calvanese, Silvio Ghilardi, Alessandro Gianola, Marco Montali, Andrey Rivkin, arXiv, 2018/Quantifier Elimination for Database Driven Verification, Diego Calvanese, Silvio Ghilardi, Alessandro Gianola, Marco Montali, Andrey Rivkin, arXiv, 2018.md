                                         Quantifier Elimination for Database Driven Verification

                                                        Diego Calvanese1 , Silvio Ghilardi2, Alessandro Gianola1 ,
                                                                   Marco Montali1 , Andrey Rivkin1
                                                   1 Faculty of Computer Science, Free University of Bozen-Bolzano (Italy)
arXiv:1806.09686v2 [cs.LO] 17 Jun 2019




                                                               {calvanese, gianola, montali, rivkin}@inf.unibz.it
                                                     2 Dipartimento di Matematica, Università degli Studi di Milano (Italy)

                                                                            silvio.ghilardi@unimi.it



                                                Abstract. Running verification tasks in database driven systems requires solving
                                                quantifier elimination problems of a new kind. These quantifier elimination prob-
                                                lems are related to the notion of a cover introduced in ESOP 2008 by Gulwani
                                                and Musuvathi.
                                                In this paper, we show how covers are strictly related to model completions, a
                                                well-known topic in model theory. We also investigate the computation of cov-
                                                ers within the Superposition Calculus, by adopting a constrained version of the
                                                calculus, equipped with appropriate settings and reduction strategies.
                                                In addition, we show that cover computations are computationally tractable for
                                                the fragment of the language used in applications to database driven verification.
                                                This observation is confirmed by analyzing the preliminary results obtained us-
                                                ing the MCMT tool on the verification of data-aware process benchmarks. These
                                                benchmarks can be found in the last version of the tool distribution.


                                         1 Introduction

                                         Declarative approaches to infinite state model checking [44] need to manipulate logical
                                         formulae in order to represent sets of reachable states. To prevent divergence, various
                                         abstraction strategies have been adopted, ranging from interpolation-based [35] to so-
                                         phisticated search via counterexample elimination [27]. Precise computations of the set
                                         of reachable states require some form of quantifier elimination and hence are subject to
                                         two problems, namely that quantifier elimination might not be available at all and that,
                                         when available, it is computationally very expensive.
                                             To cope with the first problem, [26] introduced the notion of a cover and proved
                                         that covers exist for equality with uninterpreted symbols (EUF) and its combination
                                         with linear arithmetic; also, it was shown that covers can be used instead of quantifier
                                         elimination and yield a precise computation of reachable states. Concerning the second
                                         problem, in [26] it was observed (as a side remark) that computing the cover of a con-
                                         junction of literals becomes tractable when only free unary function symbols occur in
                                         the signature. It can be shown (see Section 6 below) that the same observation applies
                                         when also free relational symbols occur.
                                             In [10,12] we propose a new formalism for representing read-only database
                                         schemata towards the verification of integrated models of processes and data [9], in
                                         particular so-called artifact systems [47,16,32,7]; this formalism (briefly recalled in
Section 4.1 below) uses precisely signatures comprising unary function symbols and
free n-ary relations. In [10,12] we apply model completeness techniques for verifying
transition systems based on read-only databases, in a framework where such systems
employ both individual and higher order variables.
     In this paper we show (see Section 3 below) that covers are strictly related to model
completions and to uniform interpolation [43], thus building a bridge between different
research areas. In particular, we prove that computing covers for a theory is equiva-
lent to eliminating quantifiers in its model completion. Model completeness has other
well-known applications in computer science. It has been applied: (i) to reveal inter-
esting connections between temporal logic and monadic second order logic [23,24];
(ii) in automated reasoning to design complete algorithms for constraint satisfiability
in combined theories over non disjoint signatures [18,1,21,39,37,38] and theory ex-
tensions [45,46]; (iii) to obtain combined interpolation for modal logics and software
verification theories [19,20].
     In the last part of the paper (Section 5 below), we prove that covers for (EUF)
can be computed through a constrained version of the Superposition Calculus [42]
equipped with appropriate settings and reduction strategies; the related completeness
proof requires a careful analysis of the constrained literals generated during the satura-
tion process. Complexity bounds for the fragment used in database driven verification
are investigated in Section 6; in Subsection 6.2 we give some details about our first
implementation in our tool MCMT.
     This paper is the extended version of [13].


2 Preliminaries

We adopt the usual first-order syntactic notions of signature, term, atom, (ground) for-
mula, and so on; our signatures are multi-sorted and include equality for every sort. This
implies that variables are sorted as well. For simplicity, most basic definitions in this
Section will be supplied for single-sorted languages only (the adaptation to multi-sorted
languages is straightforward). We compactly represent a tuple hx1 , . . . , xn i of variables
as x. The notation t(x), φ (x) means that the term t, the formula φ has free variables
included in the tuple x.
     We assume that a function arity can be deduced from the context. Whenever we
build terms and formulae, we always assume that they are well-typed, in the sense that
the sorts of variables, constants, and function sources/targets match.A formula is said
to be universal (resp., existential) if it has the form ∀x(φ (x)) (resp., ∃x(φ (x))), where φ
is a quantifier-free formula. Formulae with no free variables are called sentences.
     From the semantic side, we use the standard notion of a Σ -structure M and of truth
of a formula in a Σ -structure under a free variables assignment.
     A Σ -theory T is a set of Σ -sentences; a model of T is a Σ -structure M where all
sentences in T are true. We use the standard notation T |= φ to say that φ is true in all
models of T for every assignment to the variables occurring free in φ . We say that φ is
T -satisfiable iff there is a model M of T and an assignment to the variables occurring
free in φ making φ true in M.

                                             2
     We give now the definitions of constraint satisfiability problem and quantifier elim-
ination for a theory T .
     A Σ -formula φ is a Σ -constraint (or just a constraint) iff it is a conjunction of
literals. The constraint satisfiability problem for T is the following: we are given a
constraint (equivalently, a quantifier-free formula) φ (x) and we are asked whether there
exist a model M of T and an assignment I to the free variables x such that M, I |=
φ (x).
     A theory T has quantifier elimination iff for every formula φ (x) in the signature of
T there is a quantifier-free formula φ ′ (x) such that T |= φ (x) ↔ φ ′ (x). It is well-known
(and easily seen) that quantifier elimination holds in case we can eliminate quantifiers
from primitive formulae, i.e. from formulae of the kind ∃y φ (x, y), where φ is a con-
junction of literals (i.e. of atomic formulae and their negations). Since we are interested
in effective computability, we assume that when we talk about quantifier elimination,
an effective procedure for eliminating quantifiers is given.
     We recall also some basic definitions and notions from logic and model theory. We
focus on the definitions of diagram, embedding, substructure and amalgamation.

2.1 Substructures and embeddings
Let Σ be a first-order signature. The signature obtained from Σ by adding to it a set a of
new constants (i.e., 0-ary function symbols) is denoted by Σ a . Analogously, given a Σ -
structure M, the signature Σ can be expanded to a new signature Σ |M| := Σ ∪ {ā | a ∈
|M|} by adding a set of new constants ā (the name for a), one for each element a in
M, with the convention that two distinct elements are denoted by different ”name” con-
stants. M can be expanded to a Σ |M| -structure M := (M, a)a∈|M| just interpreting the
additional constants over the corresponding elements. From now on, when the meaning
is clear from the context, we will freely use the notation M and M interchangeably: in
particular, given a Σ -structure M and a Σ -formula φ (x) with free variables that are all
in x, we will write, by abuse of notation, M |= φ (a) instead of M |= φ (ā).
     A Σ -homomorphism (or, simply, a homomorphism) between two Σ -structures M
and N is any mapping µ : |M| −→ |N | among the support sets |M| of M and |N | of
N satisfying the condition
                                 M |= ϕ ⇒ N |= ϕ                                       (1)
for all Σ |M| -atoms ϕ (here M is regarded as a Σ |M| -structure, by interpreting each
additional constant a ∈ |M| into itself and N is regarded as a Σ |M| -structure by inter-
preting each additional constant a ∈ |M| into µ (a)). In case condition (1) holds for all
Σ |M| -literals, the homomorphism µ is said to be an embedding and if it holds for all
first order formulae, the embedding µ is said to be elementary. Notice the following
facts:
(a) since we have equality in the signature, an embedding is an injective function;
(b) an embedding µ : M −→ N must be an algebraic homomorphism, that is for
    every n-ary function symbol f and for every m1 , ..., mn in |M|, we must have
     f N (µ (m1 ), ..., µ (mn )) = µ ( f M (m1 , ..., mn ));
(c) for an n-ary predicate symbol P we must have (m1 , ..., mn ) ∈ PM iff
    (µ (m1 ), ..., µ (mn )) ∈ PN .

                                             3
It is easily seen that an embedding µ : M −→ N can be equivalently defined as a
map µ : |M| −→ |N | satisfying the conditions (a)-(b)-(c) above. If µ : M −→ N is
an embedding which is just the identity inclusion |M| ⊆ |N |, we say that M is a
substructure of N or that N is an extension of M. A Σ -structure M is said to be
generated by a set X included in its support |M| iff there are no proper substructures of
M including X.
     The notion of substructure can be equivalently defined as follows: given a Σ -
structure N and a Σ -structure M such that |M| ⊆ |N |, we say that M is a Σ -
substructure of N if:
 – for every function symbol f inf Σ , the interpretation of f in M (denoted using f M )
   is the restriction of the interpretation of f in N to |M| (i.e. f M (m) = f N (m) for
   every m in |M|); this fact implies that a substructure M must be a subset of N
   which is closed under the application of f N .
 – for every relation symbol P in Σ and every tuple (m1 , ..., mn ) ∈ |M|n , (m1 , ..., mn ) ∈
   PM iff (m1 , ..., mn ) ∈ PN , which means that the relation PM is the restriction of
   PN to the support of M.
    We recall that a substructure preserves and reflects validity of ground formulae, in
the following sense: given a Σ -substructure M1 of a Σ -structure M2 , a ground Σ |M1 | -
sentence θ is true in M1 iff θ is true in M2 .

2.2 Robinson Diagrams and Amalgamation
Let M be a Σ -structure. The diagram of M, denoted by ∆Σ (M), is defined as the set
of ground Σ |M| -literals (i.e. atomic formulae and negations of atomic formulae) that
are true in M.
    An easy but nevertheless important basic result, called Robinson Diagram
Lemma [14], says that, given any Σ -structure N , the embeddings µ : M −→ N are
in bijective correspondence with expansions of N to Σ |M| -structures which are models
of ∆Σ (M). The expansions and the embeddings are related in the obvious way: ā is
interpreted as µ (a).
    Amalgamation is a classical algebraic concept. We give the formal definition of this
notion.
Definition 1 (Amalgamation). A theory T has the amalgamation property if for every
couple of embeddings µ1 : M0 −→ M1 , µ2 : M0 −→ M2 among models of T , there
exists a model M of T endowed with embeddings ν1 : M1 −→ M and ν2 : M2 −→ M
such that ν1 ◦ µ1 = ν2 ◦ µ2
                                           M
                                 ν1                  ν2


                           M1                             M2                                ⊳
                                      µ1        µ2


                                           M0
The triple (M, µ1 , µ2 ) (or, by abuse, M itself) is said to be a T -amalgama of M1 , M2
over M0

                                                4
3 Covers, Uniform Interpolation and Model Completions

We report the notion of cover taken from [26]. Fix a theory T and an existential for-
mula ∃e φ (e, y); call a residue of ∃e φ (e, y) any quantifier-free formula belonging to
the set of quantifier-free formulae Res(∃e φ ) = {θ (y, z) | T |= φ (e, y) → θ (y, z)}. A
quantifier-free formula ψ (y) is said to be a T -cover (or, simply, a cover) of ∃e φ (e, y)
iff ψ (y) ∈ Res(∃e φ ) and ψ (y) implies (modulo T ) all the other formulae in Res(∃e φ ).
The following Lemma (to be widely used throughout the paper) supplies a semantic
counterpart to the notion of a cover:
Lemma 1. A formula ψ (y) is a T -cover of ∃e φ (e, y) iff it satisfies the following two
conditions: (i) T |= ∀y (∃e φ (e, y) → ψ (y)); (ii) for every model M of T , for every tuple
of elements a from the support of M such that M |= ψ (a) it is possible to find another
model N of T such that M embeds into N and N |= ∃e φ (e, a).                                    ⊳
Proof. Suppose that ψ (y) satisfies conditions (i) and (ii) above. Condition (i) says that
ψ (y) ∈ Res(∃e φ ), so ψ is a residue. In order to show that ψ is also a cover, we have to
prove that T |= ∀y, z(ψ (y) → θ (y, z)), for every θ (y, z) that is a residue for ∃e φ (e, y).
Given a model M of T , take a pair of tuples a, b of elements from |M| and suppose
that M |= ψ (a). By condition (ii), there is a model N of T such that M embeds into
N and N |= ∃eφ (e, a). Using the definition of Res(∃e φ ), we have N |= θ (a, b), since
θ (y, z) ∈ Res(∃x φ ). Since M is a substructure of N and θ is quantifier-free, M |=
θ (a, b) as well, as required.
     Suppose that ψ (y) is a cover. The definition of residue implies condition (i).
To show condition (ii) we have to prove that, given a model M of T , for every
tuple a of elements from |M|, if M |= ψ (a), then there exists a model N of T
such that M embeds into N and N |= ∃xφ (x, a). By reduction to absurdity, sup-
pose that this is not the case: this is equivalent (by using Robinson Diagram Lemma)
to the fact that ∆ (M) ∪ {φ (e, a)} is a T -inconsistent Σ |M|∪{e} -theory. By compact-
ness, there is a finite number of literals ℓ1 (a, b), ..., ℓm (a, b) (for some tuple b of
elements from |M|) such that M |= ℓi (for all i = 1, . . . , m) and T |= φ (e, a) →
¬(ℓ1 (a, b)∧· · · ∧ℓm (a, b)), which means that T |= φ (e, y) → (¬ℓ1 (y, z)∨· · ·∨¬ℓm (y, z)),
i.e. that T |= ∃e φ (e, y) → (¬ℓ1 (y, z) ∨ · · · ∨ ¬ℓm (y, z)). By definition of residue, clearly
(¬ℓ1 (y, z) ∨ · · · ∨ ¬ℓm (y, z)) ∈ Res(∃x φ ); then, since ψ (y) is a cover, T |= ψ (y) →
(¬ℓ1 (y, z) ∨ · · · ∨ ¬ℓm (y, z)), which implies that M |= ¬ℓ j (a, b) for some j = 1, . . . , m,
which is a contradiction. Thus, ψ (y) satisfies conditions (ii) too.                            ⊣
     We say that a theory T has uniform quantifier-free interpolation iff every existential
formula ∃e φ (e, y) (equivalently, every primitive formula ∃e φ (e, y)) has a T -cover.
     It is clear that if T has uniform quantifier-free interpolation, then it has ordinary
quantifier-free interpolation [8], in the sense that if we have T |= φ (e, y) → φ ′ (y, z) (for
quantifier-free formulae φ , φ ′ ), then there is a quantifier-free formula θ (y) such that
T |= φ (e, y) → θ (y) and T |= θ (y) → φ ′ (y, z). In fact, if T has uniform quantifier-free
interpolation, then the interpolant θ is independent on φ ′ (the same θ (y) can be used as
interpolant for all entailments T |= φ (e, y) → φ ′ (y, z), varying φ ′ ).
     We say that a universal theory T has a model completion iff there is a stronger the-
ory T ∗ ⊇ T (still within the same signature Σ of T ) such that (i) every Σ -constraint
that is satisfiable in a model of T is satisfiable in a model of T ∗ ; (ii) T ∗ eliminates

                                               5
quantifiers. Other equivalent definitions are possible [14]: for instance, (i) is equivalent
to the fact that T and T ∗ prove the same quantifier-free formulae or again to the fact
that every model of T can be embedded into a model of T ∗ . We recall that the model
completion, if it exists, is unique and that its existence implies the amalgamation prop-
erty for T [14]. The relationship between uniform interpolation in a propositional logic
and model completion of the the equational theory of the variety algebraizing it was
extensively studied in [25]. In the context of first order theories, we prove an even more
direct connection:

Theorem 1. Suppose that T is a universal theory. Then T has a model completion T ∗
iff T has uniform quantifier-free interpolation. If this happens, T ∗ is axiomatized by the
infinitely many sentences
                                 ∀y (ψ (y) → ∃e φ (e, y))                               (2)
where ∃e φ (e, y) is a primitive formula and ψ is a cover of it.                            ⊳

Proof. Suppose first that there is a model completion T ∗ of T and let ∃e φ (e, y) be a
primitive formula. Since T ∗ eliminates quantifiers, we have T ∗ |= ∃e φ (e, y) ↔ ψ (y)
for some quantifier-free formula ψ (y). Since T and T ∗ prove the same quantifier-free
formulae, we have that ψ (y) ∈ Res(∃e φ ). If θ (y, z) ∈ Res(∃e φ ), then we have T |=
φ (e, y) → θ (y, z); the same entailment holds in T ∗ too, where we have T ∗ |= ψ (y) →
θ (y, z). Since ψ (y) → θ (y, z) is quantifier-free, we have also T |= ψ (y) → θ (y, z), show-
ing that ψ is a cover of ∃e φ (e, y). Thus T has uniform interpolation, because we found
a cover for every primitive formula.
    Suppose vice versa that T has uniform interpolation. Let T ∗ be the theory axiom-
atized by all the formulae (2) above. From (i) of Lemma 1 and (2) above, we clearly
get that T ⋆ admits quantifier elimination: in fact, in order to prove that a theory enjoys
quantifier elimination, it is sufficient to eliminate quantifiers from primitive formulae
(then the quantifier elimination for all formulae can be easily shown by an induction
over their complexity). This is exactly what is guaranteed by (i) of Lemma 1 and (2).
    Let M be a model of T . We show (by using a chain argument) that there exists a
model M′ of T ⋆ such that M embeds into M′ . For every primitive formula ∃e φ (e, y),
consider the set {(a, ∃e φ (e, a))} such that M |= ψ (a) (where ψ is a cover of φ ). By Zer-
melo’s Theorem, the set {(a, ∃e φ (e, a))} can be well-ordered: let {(ai , ∃e φi (e, ai ))}i∈I
be such a well-ordered set (where I is an ordinal). By transfinite induction on this well-
                                                                            S
order, we define M0 := M and, for each i ∈ I, Mi as the extension  S
                                                                         of j<i M j such
that Mi |= ∃e φi (e, y), which exists for (ii) of Lemma 1 since j<i M j |= ψi (a) (re-
member that validity of ground formulae is preserved passing through substructures
and superstructures, and M0 |= ψi (a)).
                                             S
    Now we take the chain union M1 := i∈I Mi : since T is universal, M1 is again a
model of T , and it is possible to construct an analogous chain M2 as done above, start-
ing from M1 instead of M. Clearly, we get M0 := M ⊆ M1 ⊆ M2 by construction.
At this point, we iterate the same argument countably many times, so as to define a new
chain of models of T :
                            M0 := M ⊆ M1 ⊆ ... ⊆ Mn ⊆ ...

                                              6
                      S
      Defining M′ := n Mn , we trivially get that M′ is a model of T such that M ⊆ M′
and satisfies all the sentences of type (2). The last fact can be shown using the following
finiteness argument.
      Fix φ , ψ as in (2). For every tuple a′ ∈ M′ such that M′ |= ψ (a′ ), by definition of
M there exists a natural number k such that a′ ∈ Mk : since ψ (a′ ) is a ground formula,
    ′

we get that also Mk |= ψ (a′ ). Therefore, we consider the step k of the countable chain:
there, we have that the pair (a′ , ψ (a′ )) appears in the enumeration given by the well-
ordered set of pairs {(ai , ∃e φi (e, ai ))}i∈I (for some ordinal I) such that Mk |= ψi (a).
Hence, by construction and since ψ (a′ ) is a ground formula, we have that there exists
a j ∈ I such that Mkj |= ∃e φ (e, a′ ). In conclusion, since the existential formulae are
preserved passing to extensions, we obtain M′ |= ∃e φ (e, a′ ), as wanted.                ⊣


4 Model-Checking Applications

In this section we supply old and new motivations for investigating covers and model
completions in view of model-checking applications. We first report the considerations
from [26,10,12] on symbolic model-checking via model completions (or, equivalently,
via covers) in the basic case where system variables are represented as individual vari-
ables (for more advanced applications where system variables are both individual and
higher order variables, see [10,12]). Similar ideas (‘use quantifier elimination in the
model completion even if T does not allow quantifier elimination’) were used in [45]
for interpolation and symbol elimination.
Definition 2. A (quantifier-free) transition system is a tuple
                                S = hΣ , T, x, ι (x), τ (x, x′ )i
where: (i) Σ is a signature and T is a Σ -theory; (ii) x = x1 , . . . , xn are individual vari-
ables; (iii) ι (x) is a quantifier-free formula; (iv) τ (x, x′ ) is a quantifier-free formula
(here the x′ are renamed copies of the x).                                                   ⊳

A safety formula for a transition system S is a further quantifier-free formula υ (x)
describing undesired states of S. We say that S is safe with respect to υ if the system
has no finite run leading from ι to υ , i.e. (formally) if there are no model M of T and
no k ≥ 0 such that the formula
                       ι (x0 ) ∧ τ (x0 , x1 ) ∧ · · · ∧ τ (xk−1 , xk ) ∧ υ (xk )      (3)
is satisfiable in M (here xi ’s are renamed copies of x). The safety problem for S is the
following: given υ , decide whether S is safe with respect to υ .
    Suppose now that the theory T mentioned in Definition 2(i) is universal, has
decidable constraint satisfability problem and admits a model completion T ∗ . Al-
gorithm 1 describes the backward reachability algorithm for handling the safety
problem for S (the dual algorithm working via forward search is described in
equivalent terms in [26]). An integral part of the algorithm is to compute preim-
ages. For that purpose, for any φ1 (x, x′ ) and φ2 (x), we define Pre(φ1 , φ2 ) to
be the formula ∃x′ (φ1 (x, x′ ) ∧ φ2 (x′ )). The preimage of the set of states de-
scribed by a state formula φ (x) is the set of states described by Pre(τ , φ ).


                                              7
                                                         Algorithm 1: Backward reacha-
The subprocedure QE(T ∗ , φ ) in Line 6 ap-              bility algorithm
plies the quantifier elimination algorithm of            Function BReach(υ )
T ∗ to the existential formula φ . Algorithm 1        1       φ ←− υ ; B ←− ⊥;
computes iterated preimages of υ and applies          2       while  φ ∧ ¬B is T -satisfiable do
to them quantifier elimination, until a fixpoint      3           if ι ∧ φ is T -satisfiable. then
                                                                        return unsafe
is reached or until a set intersecting the initial
                                                      4           B ←− φ ∨ B;
states (i.e., satisfying ι ) is found. Inclusion      5           φ ←− Pre(τ , φ );
(Line 2) and disjointness (Line 3) tests pro-         6           φ ←− QE(T ∗ , φ );
duce proof obligations that can be discharged
                                                              return (safe, B);
thanks to the fact that T has decidable con-
straint satisfiability problem.
     The proof of Proposition 1 consists just
in the observation that, thanks to quantifier elimination in T ⋆ , (3) is a quantifier-free
formula and that a quantifier-free formula is satisfiable in a model of T iff so is it in a
model of T ∗ :
Proposition 1. Suppose that the universal Σ -theory T has decidable constraint sat-
isfiability problem and admits a model completion T ∗ . For every transition system
S = hΣ , T, x, ι , τ i, the backward search algorithm is effective and partially correct for
solving safety problems for S.1                                                                    ⊳
     Despite its simplicity, Proposition 1 is a crucial fact. Notice that it implies decidabil-
ity of the safety problems in some interesting cases: this happens, for instance, when in
T there are only finitely many quantifier-free formulae in which x occur, as in case T
has a purely relational signature or, more generally, T is locally finite2 . Since a theory
is universal iff it is closed under substructures [14] and since a universal locally finite
theory has a model completion iff it has the amalgamation property [48,33], it follows
that Proposition 1 can be used to cover the decidability result stated in Theorem 5 of [7]
(once restricted to transition systems over a first-order definable class of Σ -structures).


4.1 Database Schemata

In this subsection, we provide a new application for the above explained model-
checking techniques [10,12]. The application relates to the verification of integrated
models of business processes and data [9], referred to as artifact systems [47], where
the behavior of the process is influenced by data stored in a relational database (DB)
with constraints. The data contained therein are read-only: they can be queried by the
process and stored in a working memory, which in the context of this paper is consti-
tuted by a set of system variables. In this context, safety amounts to checking whether
the system never reaches an undesired property, irrespectively of what is contained in
the read-only DB.
    We define next the two key notions of (read-only) DB schema and instance, by
relying on an algebraic, functional characterization.
 1 Partial correctness means that, when the algorithm terminates, it gives a correct answer. Ef-

  fectiveness means that all subprocedures in the algorithm can be effectively executed.
 2 We say that T is locally finite iff for every finite tuple of variables x there are only finitely

  many non T -equivalent atoms A(x) involving only the variables x.


                                                 8
Definition 3. A DB schema is a pair hΣ , T i, where: (i) Σ is a DB signature, that is,
a finite multi-sorted signature whose function symbols are all unary; (ii) T is a DB
theory, that is, a set of universal Σ -sentences.                                                   ⊳
We now focus on extensional data conforming to a given DB schema.
Definition 4. A DB instance of DB schema hΣ , T i is a Σ -structure M such that M is
a model of T .3                                                                                     ⊳
    One might be surprised by the fact that signatures in our DB schemata contain unary
function symbols, beside relational symbols. As shown in [10,12], the algebraic, func-
tional characterization of DB schema and instance can be actually reinterpreted in the
classical, relational model so as to reconstruct the requirements posed in [32]. Defi-
nition 3 naturally corresponds to the definition of relational database schema equipped
with single-attribute primary keys and foreign keys. To see this connection, we adopt the
named perspective, where each relation schema is defined by a signature containing a
relation name and a set of typed attribute names. Let hΣ , T i be a DB schema. Each sort
S from Σ corresponds to a dedicated relation RS with the following attributes: (i) one
identifier attribute idS with type S; (ii) one dedicated attribute a f with type S′ for every
function symbol f from Σ of the form f : S −→ S′ .
    The fact that RS is constructed starting from functions in Σ naturally induces cor-
responding functional dependencies within RS , and inclusion dependencies from RS to
other relation schemas. In particular, for each non-id attribute a f of RS , we get a func-
tional dependency from idS to a f . Altogether, such dependencies witness that idS is the
primary key of RS . In addition, for each non-id attribute a f of RS whose corresponding
function symbol f has id sort S′ as image, we get an inclusion dependency from a f to
the id attribute idS′ of RS′ . This captures that a f is a foreign key referencing RS′ .
    Given a DB instance M of hΣ , T i, its corresponding relational instance R[M] is the
minimal set satisfying the following property: for every id sort S from Σ , let f1 , . . . , fn
be all functions in Σ with domain S; then, for every identifier o ∈ SM , R[M] contains
a labeled fact of the form RS (idS : oM , a f1 : f1M (o), . . . , a fn : fnM (o)). In addition, R[M]
contains the tuples from rM , for every relational symbol r from Σ (these relational
symbols represent plain relations, i.e. those not possessing a key).
    We close our discussion by focusing on DB theories. Notice that EUF suffices to
handle the sophisticated setting of database-driven systems from [12] (e.g., key depen-
dencies). The role of a non-empty DB theory is to encode background axioms to express
additional constraints. We illustrate a typical background axiom, required to handle the
possible presence of undefined identifiers/values in the different sorts. This, in turn, is
essential to capture artifact systems whose working memory is initially undefined, in the
style of [17,32]. To accommodate this, we add to every sort S of Σ a constant undefS
(written by abuse of notation just undef from now on), used to specify an undefined
value. Then, for each function symbol f of Σ , we can impose additional constraints
involving undef, for example by adding the following axioms to the DB theory:
                               ∀x (x = undef ↔ f (x) = undef)                                     (4)
 3 One may restrict to models interpreting sorts as finite sets, as customary in database theory.

  Since the theories we are dealing with usually have finite model property for constraint sat-
  isfiability, assuming such restriction turns out to be irrelevant, as far as safety problems are
  concerned (see [10,12] for an accurate discussion).


                                                 9
This axiom states that the application of f to the undefined value produces an undefined
value, and it is the only situation for which f is undefined. A slightly different approach
may handle many undefined values for each sort; the reader is referred to [10,12] for
examples of concrete database instances formalized in our framework. We just point
out that in most cases the kind of axioms that we need for our DB theories T are just
one-variable universal axioms (like Axioms 4), so that they fit the hypotheses of Propo-
sition 2 below.
     We are interested in applying the algorithm of Proposition 1 to what we call simple
artifact systems, i.e. transition systems S = hΣ , T, x, ι (x), τ (x, x′ )i, where hΣ , T i is a
DB schema in the sense of Definition 3. To this aim, it is sufficient to identify a suitable
class of DB theories having a model completion and whose constraint satisfiability
problem is decidable. A first result in this sense is given below. We associate to a DB
signature Σ the edge-labeled graph G(Σ ) whose nodes are the sorts in Σ , and such that
                                   f
G(Σ ) contains a labeled edge S − → S′ if and only if Σ contains a function symbol whose
source sort is S and whose target sort is S′ . We say that Σ is acyclic if G(Σ ) is so.
Proposition 2. A DB theory T has decidable constraint satisfiability problem and ad-
mits a model completion in case it is axiomatized by finitely many universal one-
variable formulae and Σ is acyclic.                                                        ⊳
Proof. First, notice that, in case Σ is acyclic, T has the finite model property. In fact,
if T := 0,/ then congruence closure ensures that the finite model property holds and
decides constraint satisfiability in time O(n log n). Otherwise, we reduce the argument
to the Herbrand Theorem. Indeed, suppose to have a finite set Φ of universal formulae
and let φ (x) be the constraint we want to test for satisfiability. Replace the variables x
with free constants a. Herbrand Theorem states that Φ ∪ {φ (a)} has a model iff the set
of ground Σ a -instances of Φ ∪ {φ (a)} has a model. These ground instances are finitely
many by acyclicity, so we can reduce to the case where T is empty. Hence, the constraint
satisfiability problem for T is decidable.
    To show the existence of a model completion, we freely take inspiration from an
analogous result in [48,33]. We preliminarily show that T is amalgamable. Then, for a
suitable choice of ψ suggested by the acyclicity assumption, the amalgamation property
will be used to prove the validy of the condition (ii) of Lemma 1: this fact (together with
condition (i) of Lemma 1 ) yields that T has a model completion which is axiomatized
by the infinitely many sentences (2).
    Let M1 and M2 two models of T with a submodel M0 of T in common (we sup-
pose for simplicity that |M1 | ∩ |M2 | = |M0 |). We define a T -amalgam M of M1 , M2
over M0 as follows (we use in an essential way the fact that Σ contains only unary
function symbols and n-ary relation symbols). Let the support of M be the set-theoretic
union of the supports of M1 and M2 , i.e. |M| := |M1 | ∪ |M2 |. M has a natural Σ -
structure inherited by the Σ -structures M1 and M2 . For every function symbol f in
Σ , we define, for each mi ∈ |Mi | (i = 1, 2), f M (mi ) := f M1 (mi ), i.e. the interpreta-
tion of f in M is the restriction of the interpretation of f in Mi for every element
mi ∈ |Mi |. This is well-defined since, for every a ∈ |M1 | ∩ |M2 | = |M0 |, we have that
 f M (a) := f M1 (a) = f M0 (a) = f M2 (a). For every n-ry relation symbol R, we let RM
be the union of RM1 ∪ RM2 ; notice that if the tuple a belongs to RM , then we must have
that a ∈ |Mi |n and that a ∈ RMi for either i = 1 or i = 2 (or for both, but this happens

                                              10
just in case a ∈ |M0 |n = |M1 |n ∩ |M2 |n , because M0 is a substructure of M1 and
M2 ). It is clear that M1 and M2 are substructures of M, and their inclusions agree on
M0 .
     We show that the Σ -structure M, as defined above, is a model of T . By hypothesis,
T is axiomatized by universal one-variable formulae: so, we can consider T as a theory
formed by axioms φ which are universal closures of clauses with just one variable, i.e.
φ := ∀x(A1 (x) ∧ ... ∧ An (x) → B1 (x) ∨ ... ∨ Bm (x)), where A j and Bk ( j = 1, ..., n and
k = 1, ..., m) are atoms.
     We show that M satisfies all such formulae φ . In order to do that, suppose that, for
every a ∈ |M|, M |= A j (a) for all j = 1, ..., n. If a ∈ |Mi |, then M |= A j (a) implies
Mi |= A j (a), since A j (a) is a ground formula. Since Mi is model of T and so Mi |= φ ,
we get that Mi |= Bk (a) for some k = 1, ..., m, which means that M |= Bk (a), since
Bk (a) is a ground formula. Thus, M |= φ for every axiom φ of T , i.e. M |= T and,
hence, M is a T -amalgam of M1 , M2 over M0 , as wanted.
     Now, given a primitive formula ∃e φ (e, y), we find a suitable ψ (y) such that con-
ditions (i) and (ii) of Lemma 1 hold. We define ψ (y) as the conjunction of the set of
all quantifier-free χ (y)-formulae such that φ (e, y) → χ (y) is a logical consequences of
T (they are finitely many - up to T -equivalence - because Σ is acyclic). By definition,
clearly we have that (i) of Lemma 1 holds.
     We show that also condition (ii) of Lemma 1 is satisfied. Let M be a model of
T such that M |= ψ (a) for some tuple of elements a from the support of M. Then,
consider the Σ -substructure M[a] of M generated by the elements a: this substructure
is finite (since Σ is acyclic), it is a model of T and we trivially have that M[a] |= ψ (a),
since ψ (a) is a ground formula. In order to prove that there exists an extension N ′
of M[a] such that N |= ∃e φ (e, a), it is sufficient to prove (by the Robinson Diagram
Lemma) that the Σ |M[a]|∪{e} -theory ∆ (M[a]) ∪ {φ (e, a)} is T -consistent. For reduction
to absurdity, suppose that the last theory is T -inconsistent. Then, there are finitely many
literals l1 (a), ..., lm (a) from ∆ (M[a]) (remember that ∆ (M[a]) is a finite set of literals
since M[a] is a finite structure) such that φ (e, a) |=T ¬(l1 (a) ∧ ... ∧ lm (a)). Therefore,
defining A(a) := l1 (a) ∧ ... ∧ lm (a), we get that φ (e, a) |=T ¬A(a), which implies that
¬A(a) is one of the χ (y)-formulae appearing in ψ (a). Since M[a] |= ψ (a), we also
have that M[a] |= ¬A(a), which is a contraddiction: in fact, by definition of diagram,
M[a] |= A(a) must hold. Hence, there exists an extension N ′ of M[a] such that N ′ |=
∃ eφ (e, a). Now, by amalgamation property, there exists a T -amalgam N of M and N ′
over M[a]: clearly, N is an extension of M and, since N ′ ֒→ N and N ′ |= ∃e φ (e, a),
also N |= ∃e φ (e, a) holds, as required.                                                   ⊣
     Since acyclicity of Σ yields local finiteness, we immediately get as a Corollary the
decidability of safety problems for transitions systems based on DB schema satisfying
the hypotheses of the above theorem.


5 Covers via Constrained Superposition

Of course, a model completion may not exist at all; Proposition 2 shows that it exists in
case T is a DB theory axiomatized by universal one-variable formulae and Σ is acyclic.

                                             11
The second hypothesis is unnecessarily restrictive and the algorithm for quantifier elim-
ination suggested by the proof of Proposition 2 is highly impractical: for this reason we
are trying a different approach. In this section, we drop the acyclicity hypothesis and
examine the case where the theory T is empty and the signature Σ may contain function
symbols of any arity. Covers in this context were shown to exist already in [26], using
an algorithm that, very roughly speaking, determines all the conditional equations that
can be derived concerning the nodes of the congruence closure graph. An algorithm for
the generation of interpolants, still relying on congruence closure [29] and similar to
the one presented in [26], is supplied in [30].
     We follow a different plan and we want to produce covers (and show that they ex-
ist) using saturation-based theorem proving. The natural idea to proceed in this sense
is to take the matrix φ (e, y) of the primitive formula ∃e φ (e, y) we want to compute
the cover of: this is a conjunction of literals, so we consider each variable as a free
constant, we saturate the corresponding set of ground literals and finally we output
the literals involving only the y. For saturation, one can use any version of the su-
perposition calculus [42]. This procedure however for our problem is not sufficient.
As a trivial counterexample consider the primitive formula ∃e (R(e, y1 ) ∧ ¬R(e, y2 )):
the set of literals {R(e, y1 ), ¬R(e, y2 )} is saturated (recall that we view e, y1 , y2 as con-
stants), however the formula has a non-trivial cover y1 6= y2 which is not produced
by saturation. If we move to signatures with function symbols, the situation is even
worse: the set of literals { f (e, y1 ) = y′1 , f (e, y2 ) = y′2 } is saturated but the formula
∃e ( f (e, y1 ) = y′1 ∧ f (e, y2 ) = y′2 ) has the conditional equality y1 = y2 → y′1 = y′2 as cover.
Disjunctions of disequations might also arise: the cover of ∃e h(e, y1 , y2 ) 6= h(e, y′1 , y′2 )
(as well as the cover of ∃e f ( f (e, y1 ), y2 ) 6= f ( f (e, y′1 ), y′2 ), see Example 1 below) is
y1 6= y′1 ∨ y2 6= y′2 . 4
     Notice that our problem is different from the problem of producing ordinary
quantifier-free interpolants via saturation based theorem proving [31]: for ordinary
Craig interpolants, we have as input two quantifier-free formulae φ (e, y), φ ′ (y, z) such
that φ (e, y) → φ ′ (y, z) is valid; here we have a single formula φ (e, y) in input and
we are asked to find an interpolant which is good for all possible φ ′ (y, z) such that
φ (e, y) → φ ′ (y, z) is valid. Ordinary interpolants can be extracted from a refutation of
φ (e, y) ∧ ¬φ ′ (y, z), here we are not given any refutation at all (and we are not even
supposed to find one).
     What we are going to show is that, nevertheless, saturation via superposition can
be used to produce covers, if suitably adjusted. In this section we consider signatures
with n-ary function symbols (for all n ≥ 1). For simplicity, we omit n-ary relation sym-
bols (you can easily handle them by rewriting R(t1 , . . . ,tn ) as R(t1 , . . . ,tn ) = true, as
customary in the paramodulation literature [42]).
     We are going to compute the cover of a primitive formula ∃e φ (e, y) to be fixed for
the remainder of this section. We call variables e existential and variables y parameters.
By applying abstraction steps, we can assume that φ is primitive flat. i.e. that it is a
conjunction of e-flat literals, defined below. [By an abstraction step we mean replacing
 4    This example points out a problem that needs to be fixed in the algorithm presented in [26]:
     that algorithm in fact outputs only equalities, conditional equalities and single disequalities, so
     it cannot correctly handle this example.


                                                   12
∃e φ with ∃e ∃e′ (e′ = u ∧ φ ′ ), where e′ is a fresh variable and φ ′ is obtained from φ by
replacing some occurrences of a term u(e, y) by e′ ].
     A term or a formula are said to be e-free iff the existential variables do not occur
in it. An e-flat term is an e-free term t(y) or a variable from e or again it is of the kind
 f (u1 , . . . , un ), where f is a function symbol and u1 , . . . , un are e-free terms or variables
from e. An e-flat literal is a literal of the form
                                                 t = a, a 6= b
where t is an e-flat term and a, b are either e-free terms or variables from e.
     We assume the reader is familiar with standard conventions used in rewriting and
paramodulation literature: in particular s|p denotes the subterm of s in position p and
s[u] p denotes the term obtained from s by replacing s|p with u. We use ≡ to indicate
coincidence of syntactic expressions (as strings) to avoid confusion with equality sym-
bol; when we write equalities like s = t below, we may mean both s = t or t = s (an
equality is seen as a multiset of two terms). For information on reduction ordering, see
for instance [2].
     We first replace variables e = e1 , . . . , en and y = y1 , . . . , ym by free constants - we
keep the names e1 , . . . , en , y1 , . . . , ym for these constants. Choose a reduction ordering >
total for ground terms such that e-flat literals t = a are always oriented from left to right
in the following two cases: (i) t is not e-free and a is e-free; (ii) t is not e-free, it is not
equal to any of the e and a is a variable from e. To obtain such properties, one may for
instance choose a suitable Knuth-Bendix ordering taking weights in some transfinite
ordinal, see [34].
     Given two e-flat terms t, u, we indicate with E(t, u) the following procedure:
• E(t, u) fails if t is e-free and u is not e-free (or vice versa);
• E(t, u) fails if t ≡ ei and (either t ≡ f (t1 , . . . ,tk ) or u ≡ e j for i 6= j);
• E(t, u) = 0/ if t ≡ u;
• E(t, u) = {t = u} if t and u are different but both e-free;
• E(t, u) fails if none of t, u is e-free, t ≡ f (t1 , . . . ,tk ) and u ≡ g(u1 , . . . , ul ) for f 6≡ g;
• E(t, u) = E(t1 , u1 ) ∪ · · · ∪ E(tk , uk ) if none of t, u is e-free, t ≡ f (t1 , . . . ,tk ), u ≡
   f (u1 , . . . , uk ) and none of the E(ti , ui ) fails.
                                                                   V
Notice that, whenever E(t, u) succeeds, the formula E(t, u) → t = u is universally
valid. The definition of E(t, u) is motivated by the next lemma.
Lemma 2. Let R be a convergent (i.e. terminating and confluent) ground rewriting sys-
tem, whose rules consist of e-free terms. Suppose that t and u are e-flat terms with the
same R-normal form. Then E(t, u) does not fail and all pairs from E(t, u) have the same
R-normal form as well.                                                                                    ⊳
Proof. This is due to the fact that if t is not e-free, no R-rewriting is possible at root
position because rules from R are e-free.                                                                 ⊣
     In the following, we handle constrained ground flat literals of the form L kC where
L is a ground flat literal and C is a conjunction of ground equalities among e-free terms.
                                                             V
The logical meaning of L kC is the Horn clause C → L.
     In the literature, various calculi with constrained clauses were considered, starting
e.g. from the non-ground constrained versions of the Superposition Calculus of [4,41].
The calculus we propose here is inspired by such versions and it has close similarities

                                                   13
with a subcase of hierarchic superposition calculus [5], or rather to its ”weak abstrac-
tion” variant from [6] (we thank an anonymous referee for pointing out this connection).
    The rules of our Constrained Superposition Calculus follow; each rule applies pro-
vided the E subprocedure called by it does not fail. The symbol ⊥ indicates the empty
clause. Further explanations and restrictions to the calculus are given in the Remarks
below.
 Superposition Right               l=rkC           s=t kD
                                                                        if l > r and s > t
    (Constrained)                s[r] p = t k C ∪ D ∪ E(s|p , l)
 Superposition Left                    l=rkC            s 6= t k D
                                                                                if l > r and s > t
   (Constrained)                     s[r] p 6= t k C ∪ D ∪ E(s|p , l)
      Reflexion                               t 6= u k C
    (Constrained)                           ⊥ k C ∪ E(t, u)
     Demodulation                       L k C,       l = r kD                  if l > r, L|p ≡ l
     (Constrained)                            L[r] p k C                          and C ⊇ D
Remark 1. The first three rules are inference rules: they are non-deterministically se-
lected for application, until no rule applies anymore. The selection strategy for the rule
to be applied is not relevant for the correctness and completeness of the algorithm (some
variant of a ‘given clause algorithm’ can be applied). An inference rule is not applied
in case one premise is e-free (we have no reason to apply inferences to e-free premises,
since we are not looking for a refutation).                                                       ⊳
Remark 2. The Demodulation rule is a simplification rule: its application not only
adds the conclusion to the current set of constrained literals, but it also removes the first
premise. It is easy to see (e.g., representing literals as multisets of terms and extending
the total reduction ordering to multisets), that one cannot have an infinite sequence of
consecutive applications of Demodulation rules.                                                   ⊳
Remark 3. The calculus takes {Lk0/ | L is a flat literal from the matrix of φ } as the ini-
tial set of constrained literals. It terminates when a saturated set of constrained literals
is reached. We say that S is saturated iff every constrained literal that can be produced
by an inference rule, after being exhaustively simplified via Demodulation, is already in
S (there are more sophisticated notions of ‘saturation up to redundancy’ in the literature,
but we do not need them). When it reaches a saturated set S, the algorithm outputs the
                              V
conjunction of the clauses C → L, varying L kC among the e-free constrained literals
from S.                                                                                           ⊳
We need some rule application policy to ensure termination: without any such policy, a
set like {e = y k 0,
                   / f (e) = ek 0}
                                / may produce by Right Superposition the infinitely many
literals (all oriented from right to left) f (y) = e k 0,
                                                       / f ( f (y)) = e k 0,
                                                                          / f ( f ( f (y))) = e k 0,
                                                                                                  /
etc. The next Remark explains the policy we follow.
Remark 4. First, we apply Demodulation only in case the second premise is of the kind
e j = t(y) kD, where t is e-free. Demodulation rule is applied with higher priority with
respect to the inference rules. Inside all possible applications of Demodulation rule, we
give priority to the applications where both premises have the form e j = t(y) kD (for the
same e j but with possibly different D’s - the D from the second premise being included
in the D of the first). In case we have two constrained literals of the kind e j = t1 (y) kD,
e j = t2 (y) kD inside our current set of constrained literals (notice that the e j ’s and the D’s

                                                14
here are the same), among the two possible applications of the Demodulation rule, we
apply the rule that keeps the smallest ti . Notice that in this way two different constrained
literals cannot simplify each other.                                                        ⊳
    We say that a constrained literal L kC belonging to a set of constrained literals S is
simplifiable in S iff it is possible to apply (according to the above policy) a Demodula-
tion rule removing it. A first effect of our policy is:
Lemma 3. If a constrained literal L kC is simplifiable in S, then after applying to S any
sequence of rules, it remains simplifiable until it gets removed. After being removed, if
it is regenerated, it is still simplifiable and so it is eventually removed again.      ⊳
Proof. Suppose that L kC can be simplified by e = t k D and suppose that a rule is
applied to the current set of constrained literals. Since there are simplifiable constrained
literals, that rule cannot be an inference rule by the priority stated in Remark 4. For
simplification rules, keep in mind again Remark 4. If L kC is simplified, it is removed;
if none of L kC and e = t k D get simplified, the situation does not change; if e = t k D
gets simplified, this can be done by some e = t ′ k D′ , but then L kC is still simplifiable -
although in a different way - using e = t ′ k D′ (we have that D′ is included in D, which is
in turn included in C). Similar observations apply if L kC is removed and re-generated.⊣
     Due to the above Lemma, if we show that a derivation (i.e. a sequence of rule appli-
cations) can produce terms only from a finite set, it is clear that when no new constrained
literal is produced, saturation is reached. First notice that
Lemma 4. Every constrained literal L kC produced during the run of the algorithm is
e-flat.                                                                           ⊳
Proof. The constrained literals from initialization are e-flat. The Demodulation rule,
applied according to Remark 4, produces an e-flat literal out of an e-flat literal. The
same happens for the Superposition rules: in fact, since both the terms s and l from
these rules are e-flat, a Superposition may take place at root position or may rewrite
some l ≡ e j with r ≡ ei or with r ≡ t(y).                                            ⊣
     There are in principle infinitely many e-flat terms that can be generated out of the
e-flat terms occurring in φ (see the above counterexample). We show however that only
finitely many e-flat terms can in fact occur during saturation and that one can determine
in advance the finite set they are taken from.
     To formalize this idea, let us introduce a hierarchy of e-flat terms. Let D0 be the e-
flat terms occurring in φ and let Dk+1 be the set of e-flat terms obtained by simultaneous
                                   S
rewriting of an e-flat term from i≤k S i
                                        D via rewriting rules of the kind e j → t j (y) where
the t j are e-flat e-free terms from i≤k Di . The degree of an e-flat term is the minimum
k such that it belongs to set Dk (it is necessary to take the minimum because the same
term can be obtained in different stages and via different rewritings).5
Lemma 5. Let the e-flat term t ′ be obtained by a rewriting e j → u(y) from the e-flat
term t; then, if t has degree k > 1 and u has degree at most k − 1, we have that t ′ has
degree at most k.                                                                      ⊳

 5    Notice that, in the above definition of degree, constraints (attached to the rewriting rules
     occurring in our calculus) are ignored.


                                                15
Proof. This is clear, because at the k-stage one can directly produce t ′ instead of just t:
in fact, all rewriting producing directly t ′ replace an occurrence of some ei by an e-free
term, so they are all done in parallel positions.                                                ⊣
Proposition 3. The saturation of the initial set of e-flat constrained literals always ter-
minates after finitely many steps.                                                               ⊳
Proof. We show that all e-flat terms that may occur during saturation have at most
degree n (where n is the cardinality of e). This shows that the saturation must terminate,
because only finitely many terms may occur in a derivation (see the above observations).
Let the algorithm during saturation reach the status S; we say that a constraint C allows
the explicit definition of e j in S iff S contains a constrained literal of the kind e j = t(y) kD
with D ⊆ C. Now we show by mutual induction two facts concerning a constrained
literal L kC ∈ S:
(1) if an e-flat term u of degree k occurs in L, then C allows the explicit definition of k
     different e j in S;
(2) if L is of the kind ei = t(y), for an e-flat e-free term t of degree k, then either
     ei = t kC can be simplified in S or C allows the explicit definition of k + 1 different
     e j in S (ei itself is of course included among these e j ).
Notice that (1) is sufficient to exclude that any e-flat term of degree bigger than n can
occur in a constrained literal arising during the saturation process.
     We prove (1) and (2) by induction on the length of the derivation leading to L kC ∈ S.
Notice that it is sufficient to check that (1) and (2) hold for the first time where L kC ∈ S
because if C allows the explicit definition of a certain variable in S, it will continue
to do so in any S′ obtained from S by continuing the derivation (the definition may be
changed by the Demodulation rule, but the fact that ei is explicitly defined is forever).
Also, by Lemma 3, a literal cannot become non simplifiable if it is simplifiable.
     (1) and (2) are evident if S is the initial status. To show (1), suppose that u occurs
for the first time in L kC as the effect of the application of a certain rule: we can freely
assume that u does not occur in the literals from the premisses of the rule (otherwise
induction trivially applies) and that u of degree k is obtained by rewriting in a non-root
position some u′ occurring in a constrained literal L′ k D′ via some e j → t k D. This might
be the effect of a Demodulation or Superposition in a non-root position (Superpositions
in root position do not produce new terms). If u′ has degree k, then by induction D′
contains the required k explicit definitions, and we are done because D′ is included in
C. If u′ has lower degree, then t must have degree at least k − 1 (otherwise u does not
reach degree k by Lemma 5). Then by induction on (2), the constraint D (also included
in C) has (k − 1) + 1 = k explicit definitions (when a constraint e j → t kD is selected
for Superposition or for making Demodulations in a non-root position, it is itself not
simplifiable according to the procedure explained in Remark 4).
     To show (2), we analyze the reasons why the non simplifiable constrained literal
ei = t(y) kC is produced (let k be the degree of t). Suppose it is produced from ei = u′ kC
via Demodulation with e j = u(y) k D (with D ⊆ C) in a non-root position; if u′ has
degree at least k, we apply induction for (1) to ei = u′ kC: by such induction hypotheses,
we get k explicit definitions in C and we can add to them the further explicit definition
ei = t(y) (the explicit definitions from C cannot concern ei because ei = t(y) kC is not
simplifiable). Otherwise, u′ has degree less than k and u has degree at least k − 1 by

                                               16
Lemma 5 (recall that t has degree k): by induction, e j = u k D is not simplifiable (it is
used as the active part of a Demodulation in a non-root position, see Remark 4) and
supplies k explicit definitions, inherited by C ⊇ D. Note that ei cannot have a definition
in D, otherwise ei = t(y) kC would be simplifiable, so with ei = t(y) kC we get the
required k + 1 definitions.
    The remaining case is when ei = t(y) kC is produced via Superposition Right. Such
a Superposition might be at root or at a non-root position. We first analyse the case
of a root position. This might be via e j = ei kC1 and e j = t(y) kC2 (with e j > ei and
C = C1 ∪C2 because E(e j , e j ) = 0),
                                    / but in such a case one can easily apply induction.
Otherwise, we have a different kind of Superposition at root position: ei = t(y) kC is
obtained from s = ei kC1 and s′ = t(y) kC2 , with C = C1 ∪C2 ∪ E(s, s′ ). In this case, by
induction for (1), C2 supplies k explicit definitions, to be inherited by C. Among such
definitions, there cannot be an explicit definition of ei otherwise ei = t(y) kC would be
simplifiable, so again we get the required k + 1 definitions.
    In case of a Superposition at a non root-position, we have that ei = t(y) kC is ob-
tained from u′ = ei kC1 and e j = u(y) kC2 , with C = C1 ∪ C2 ; here t is obtained from
u′ by rewriting e j to u. This case is handled similarly to the case where ei = t(y) kC is
obtained via Demodulation rule.                                                          ⊣
    Having established termination, we now prove that our calculus computes covers; to
this aim, we rely on refutational completeness of unconstrained Superposition Calculus
(thus, our technique resembles the technique used [5,6] in order to prove refutational
completeness of hierarchic superposition, although it is not clear whether Theorem 2
below can be derived from the results concerning hierarchic superposition - we are not
just proving refutational completeness and we need to build proper superstructures):
Theorem 2. Suppose that the above algorithm, taking as input the primitive e-flat for-
mula ∃e φ (e, y), gives as output the quantifier-free formula ψ (y). Then the latter is a
cover of ∃e φ (e, y).                                                                   ⊳
Proof. Let S be the saturated set of constrained literals produced upon termination of
the algorithm; let S = S1 ∪ S2 , where S1 contains the constrained literals in which the
e do not occur and S2 is its complement. Clearly ∃e φ (e, y) turns out to be logically
equivalent to
                         ^ ^                    ^ ^
                              ( C → L) ∧ ∃e          ( C → L)
                         L kC∈S1                   L kC∈S2
so, as a consequence,
            V              V
                              in view of Lemma 1 it is sufficient to show that every model M
satisfying L kC∈S1 ( C → L) via an assignment I to the variables y can be embedded
into a model M′ such thatVfor a suitable     V
                                                  extension I ′ of I to the variables e we have
          ′  ′
that (M , I ) satisfies also L kC∈S2 ( C → L).
    Fix M, I as above. The diagram ∆ (M) of M is obtained as follows. We take one
free constant for each element of the support of M (by Löwenheim-Skolem theorem
you can keep M at most countable, if you like) and we put in ∆ (M) all the literals of
the kind f (c1 , . . . , ck ) = ck+1 and c1 6= c2 which are true in M (here the ci are names
for the elements of the support of M). Let R be the set of ground equalities of the form
yi = ci , where ci is the name of I(yi ). Extend our reduction ordering in the natural way
(so that yi = ci and f (c1 , . . . , ck ) = ck+1 are oriented from left to right). Consider now

                                              17
the set of clauses
                                                   ^
                             ∆ (M) ∪ R ∪ {             C → L | (L kC) ∈ S}                                 (5)
(below, we distinguish the positive and the negative literals of ∆ (M) so that ∆ (M) =
∆ + (M) ∪ ∆ − (M)). We want to saturate the above set in the standard Superposition
Calculus. Clearly the rewriting rules in           V
                                                      R, used as reduction rules, replace everywhere
yi by ci inside the clauses of the kind C → L. At this point, the negative literals from
the equality constraints all disappear: if they are true in M, they ∆ + (M)-normalize to
trivial equalities ci = ci (to be eliminated by standard reduction rules) and if they are
false in M they become part of clauses subsumed by true inequalities from ∆ − (M).
Similarly all the e-free literals not coming from ∆ (M) ∪ R get removed. Let S̃ be the
set of survived literals involving the e (they are not constrained anymore and they are
∆ + (M) ∪ R-normalized): we show that they cannot produce new clauses. Let in fact
(π ) be an inference from the Superposition Calculus [42] applying to them. Since no
superposition with ∆ (M) ∪ R is possible, this inference must involve only literals from
S̃; suppose it produces a literal L̃ from the literals L̃1 , L̃2 (coming via ∆ + (M) ∪ R-
normalization from L1 kC1 ∈ S and L2 kC2 ∈ S) as parent clauses. Then, by Lemma 2,
                                                                                                            V
our constrained inferences produce a constrained literal L kC such that the clause C →
L normalizes to L̃ via ∆ + (M)∪R. Since S is saturated, the constrained literal L kC, after
simplification, belongs to S. Now simplifications via our Constrained Demodulation and
∆ (M)+ ∪ R-normalization commute (they work at parallel positions, see Remark 4), so
the inference (π ) is redundant because L̃ simplifies to a literal already in S̃ ∪ ∆ (M).
       Thus the set of clauses (5) saturates without producing the empty clause. By the
completeness theorem of the Superposition Calculus [28,3,42] it has a model M′ . This
M′ by construction fits our requests by Robinson Diagram Lemma.                                               ⊣
       Theorem 2 also proves the existence of the model completion of (EUF).
Example 1. We compute the cover of the primitive formula ∃e f ( f (e, y1 ), y2 ) 6=
 f ( f (e, y′1 ), y′2 ). Flattening gives the set of literals
           { f (e, y1 ) = e1 , f (e1 , y2 ) = e′1 , f (e, y′1 ) = e2 , f (e2 , y′2 ) = e′2 , e′1 6= e′2 } .
Superposition Right produces the constrained literal e1 = e2 k {y1 = y′1 }; supposing that
we have e1 > e2 , Superposition Right gives first f (e2 , y2 ) = e′1 k {y1 = y′1 } and then also
e′1 = e′2 k {y1 = y′1 , y2 = y′2 }. Superposition Left and Reflexion now produce ⊥ k {y1 =
y′1 , y2 = y′2 }. Thus the clause y1 = y′1 ∧ y2 = y′2 → ⊥ will be part of the output (actually,
this will be the only clause in the output).                                                                  ⊳
Example 2. We add one more example, taken from [26]. We compute the cover of
the primitive formula ∃e (s1 = f (y3 , e) ∧ s2 = f (y4 , e) ∧t = f ( f (y1 , e), f (y2 , e))), where
s1 , s2 ,t are terms in y. This example is taken from [26]. Flattening gives the set of literals
         { f (y3 , e) = s1 , f (y4 , e) = s2 , f (y1 , e) = e1 , f (y2 , e) = e2 , f (e1 , e2 ) = t } .
Suppose that we have e > e1 > e2 > t > s1 > s2 > y1 > y2 > y3 > y4 . Superposition
Right between the 3rd and the 4th clauses produces the constrained 6th clause e1 =
e2 k {y1 = y2 }. From now on, we denote the application of a Superposition Right to the
ith and jth clauses with R(i, j). We list a derivation performed by our calculus:

                         R(3, 4) =⇒ e1 = e2 k {y1 = y2 } (6th clause)

                                                     18
                      R(1, 2) =⇒ s1 = s2 k {y3 = y4 }        (7th clause)
                   R(5, 6) =⇒ f (e2 , e2 ) = t k {y1 = y2 }    (8th clause)
                      R(1, 3) =⇒ e1 = s1 k {y1 = y3 } (9th clause)
                     R(1, 4) =⇒ e2 = s1 k {y2 = y3 } (10th clause)
                     R(2, 3) =⇒ e1 = s2 k {y1 = y4 } (11th clause)
                     R(2, 4) =⇒ e2 = s2 k {y2 = y4 } (12th clause)
                  R(5, 9) =⇒ f (s1 , e2 ) = t k {y1 = y3 }     (13th clause)
                  R(5, 11) =⇒ f (s2 , e2 ) = t k {y1 = y4 }    (14th clause)
                R(6, 9) =⇒ e2 = s1 k {y1 = y3 , y1 = y2 }       (15th clause)
                R(6, 11) =⇒ e2 = s2 k {y1 = y2 , y1 = y4 }         (16th clause)
             R(8, 10) =⇒ f (s1 , s1 ) = t k {y1 = y3 , y2 = y3 }     (17th clause)
             R(8, 12) =⇒ f (s2 , s2 ) = t k {y1 = y4 , y2 = y4 }     (18th clause)
            R(13, 12) =⇒ f (s1 , s2 ) = t k {y1 = y3 , y2 = y4 }      (19th clause)
            R(14, 10) =⇒ f (s2 , s1 ) = t k {y1 = y4 , y2 = y3 }      (20th clause)
                R(9, 11) =⇒ s1 = s2 k {y1 = y3 , y1 = y4 } (21th clause)

The set of clauses above is saturated. The 7th, 17th, 18th, 19th and 20th clauses are
exactly the output clauses of [26]. The non-simplified clauses that do not appear as
output in [26] are redundant and they could be simplified by introducing a Subsumption
rule as an additional simplification rule of our Constrained Superposition Calculus.


6 Complexity Analysis

In the special case where the signature Σ contains only unary function symbols, only
empty constraints can be generated; in case Σ contains also relation symbols of ar-
ity n > 1, the only constrained clauses that can be generated have the form ⊥ k{t1 =
t1′ , . . . ,tn−1 = tn−1
                     ′ }. Also, it is not difficult to see that in a derivation at most one ex-

plicit definition ei = t(y)||0/ can occur for every ei : as soon as this definition is produced,
all occurrences of ei are rewritten to t. This shows that Constrained Superposition com-
putes covers in polynomial time for the empty theory, whenever the signature Σ matches
the restrictions of Definition 3 for DB schemata. We give here a finer complexity anal-
ysis, in order to obtain a quadratic bound.
        In this section, we assume that our signature Σ contains only unary function and
m-ary relation symbols. As we already mentioned, the complexity of the saturation
becomes polynomial in this restricted case. However, in order to attain an optimized
quadratic complexity bound, we need to follow a different strategy in applying the rules
of our constrained superposition calculus (this different strategy would not be correct
for the general case). Thanks to this different strategy, we can make our procedure

                                              19
close to the algorithm of [26]: in fact, such algorithm is correct for the case of unary
functions and requires only a very minor adjustment for the case of unary functions
and m-ary relations (the reason why only a very minor adjustment is sufficient is due
to the fact that the empty clause is the only constrained clause that is generated during
saturation, so that constraints do not become part of a recursive mechanism).
    Since relations play a special role in the present restricted context, we prefer to treat
them as such, i.e. not to rewrite R(t1 , . . . ,tn ) as R(t1 , . . . ,tn ) = true; the consequence is
that we need an additional Constrained Resolution Rule6 . We preliminarily notice that
when function symbols are all unary, the constraints remain all empty during the run of
the saturation procedure, except for the case of the newly introduced Resolution Rule
below. This fact follows from the observation that given two terms u1 and u2 , procedure
E(u1 , u2 ) does not fail iff:
(1) either u1 and u2 are both terms containing only variables from y, or
(2) u1 and u2 are terms that syntactically coincide.
In case (1), E(u1 , u2 ) is {u1 , u2 } and in case (2), E(u1 , u2 ) is 0. / In case (1), Superposition
Rules are not applicable. To show this, suppose that u1 ≡ s|p and u2 ≡ l; then, terms l
and r use only variables from y, and consequently cannot be fed into Superposition
Rules, since Superposition Rules are only applied when variables from e occur in both
premises. Reflexion Rule does not apply too in case (1), because this rule (like any other
rule) cannot be applied to an e-free literal.
    Thus, in the particular case of m-ary relations and unary functions, the rules of the
calculus are the following:
                                        l=r        L
 Superposition                                                          if (i) l > r;
                                            L[r] p
                                                                           (ii) if L ≡ s = t or
                                                                                L ≡ s 6= t, then
                                                                                s > t and p ∈ Pos(s);
                                                                           (iii) E(s|p , l) does not fail.
                         R(t1 , . . . ,tn )      ¬R(s1 , . . . , sn )
  Resolution                                S                           if E(si ,ti ) does not fail
                                     ⊥ k i E(si ,ti )
                                                                           for all i = 1, . . . , n
                                            t 6= u
   Reflexion                                                            if E(t, u) does not fail
                                               ⊥
                                      L l=r
Demodulation                                                if l > r and L|p ≡ l
                                     L[r] p
     We still restrict the use of our rules to the case where all premises are not e-free
literals; again Demodulation is applied only in the case where l = r is of the kind ei =
t(y). For the order of applications of the Rules, Lemma 6 below show that we can apply
(restricted) Superpositions, Demodulations, Reflexions and Resolutions in this order
and then stop.
     An important preliminary observation to obtain such result is that we do not need
to apply Superposition Rules whose left premise l = r is of the kind ei = t(y): this
is because constraints are always empty (unless the constrained clause is the empty
 6 We extend the definition of an e-flat literal so as to include also the literals of the kind

   R(t1 , ..,tn ) and ¬R(t1 , ..,tn ) where the terms ti are either e-free terms or variables from e.


                                                   20
clause), so that a Superposition Rule with the left premise ei = t(y) can be replaced by
a Demodulation Rule. 7 If the left premise of Superposition is not of the kind ei = t(y),
then since our literals are e-flat, it can be either of the kind ei = e j (with ei > e j ) or of the
kind f (ei ) = t. In the latter case t is either ek ∈ e or it is an e-free term; for Superposition
Left (i.e. for Superposition applied to a negative literal), the left premise can only be
ei = e j , because our literals are e-flat and so negative literals L cannot have a position p
such that L|p ≡ f (ei ).
     Let S be a set of e-flat literals with empty constraints; we say that S is RS-closed iff
it is closed under Restricted Superposition Rules, i.e under Superposition Rules whose
left premise is not of the kind ei = t(y). In equivalent terms, as a consequence of the
above discussion, S is RS-closed iff it satisfies the following two conditions:
   – if { f (ei ) = t, f (ei ) = v} ⊆ S, then t = v ∈ S;
   – if {ei = e j , L} ⊆ S and ei > e j and L|p ≡ ei , then L[e j ] p ∈ S.
Since Restricted Superpositions do not introduce essentially new terms (newly intro-
duced terms are just rewritings of variables with variables), it is clear that we can make
a finite set S of e-free literals RS-closed in finitely many steps. This can be naively
done in time quadratic in the size of the formula. As an alternative, we can apply a
congruence closure algorithm to S and produce a set of e-free constraints S′ which is
RS-closed and logically equivalent to S: the latter can be done in O(n · log(n))-time, as
it is well-known from the literature [36,40,29].
Lemma 6. Let S be a RS-closed set of empty-constrained e-flat literals. Then, to satu-
rate S it is sufficient to first exhaustively apply the Demodulation Rule, and then Reflex-
ion and Resolution Rules.                                                                          ⊳
Proof. Let S̃ be the set obtained from S after having exhaustively applied Demodula-
tion. Notice that the final effect of the reiterated application of Demodulation can be
synthetically described by saying that literals in S are rewritten by using some explicit
definitions
                                     ei1 = t1 (y), . . . , eik = tk (y) .                  (6)
These definitions are either in S, or are generated through the Demodulations them-
selves (we can freely assume that Demodulations are done in appropriate order: first
all occurrences of ei1 are rewritten to t1 , then all occurrences of ei2 are rewritten to t2 ,
etc.).8
     Suppose now that a pair L, l = r ∈ S̃ can generate a new literal L[r] p by Superpo-
sition. We know from above that we can limit ourselves to Restricted Superposition,
so l is either of the form e j or of the form f (e j ), where moreover e j is not among the
set {ei1 , . . . , eik } from (6). The literals L and l = r ∈ S̃ happen to have been obtained
from literals L′ and l = r′ belonging to S by applying the rewriting rules (6) (notice that
l cannot have been rewritten). Since such rewritings must have occurred in positions
parallel to p and since S was closed under Restricted Superposition, we must have that
 7 This is not true in the general case where constraints are not empty, because the Demodulation

  Rule does not merge incomparable constraints.
 8 In addition, if we happen to have, say, two different explicit definitions of e as e = t , e = t ′ ,
                                                                                  i1   i1  1 i1    1
  we decide to use just one of them (and always the same one, until the other one is eventually
  removed by Demodulation).


                                                 21
S contained the literal L′ [r′ ] p that rewrites to L[r] p by the rewriting rules (6). This shows
that L[r] p is already in S̃ and proves the lemma, because Reflexion and Resolution can
only produce the empty clause and no rule applies to the empty clause.                          ⊣
Thus the strategy of applying (in this order)
             Restricted Superposition+Demodulation+Reflexion+Resolution
always saturates.
   To produce an output in optimized format, it is convenient to get it in a dag-like
form. This can be simulated via explicit acyclic definitions as follows. When we write
Def (e, y) (where e, y are tuples of distinct variables), we mean any flat formula of the
kind (let e := e1 . . . , en )
                                             ^
                                             n
                                                   ei = ti
                                             i=1
where in the term ti only the variables e1 , . . . , ei−1 , y can occur. We shall supply the
output in the form
                              ∃e′ (Def (e′ , y) ∧ ψ (e′ , y))                            (7)
where the e′ is a subset of the e and ψ is quantifier-free. The dag-format (7) is not
quantifier-free but can be converted to a quantifier-free formula by unravelling the
acyclic definitions of the e′ .
    Thus our procedure for computing a cover in dag-format of a primitive formula
∃e φ (e, y) (in case the function symbols of the signature Σ are all unary) runs by per-
forming the following steps, one after the other. Let OUT be a quantifier-free formula
(initially OUT is ⊤).
(1) We preprocess φ in order to get out of it a RS-closed set S of empty-constrained
     e-flat literals.
(2) We mark the variables e in the following way (initially, all variables are unmarked):
     we scan S and, as soon as we find an equality of the kind ei = t where all variables
     from e occurring in t are marked, we mark ei . This loop is repeated until no more
     variable gets marked.
(3) If Reflexion is applicable, output ⊥ and exit.
(4) Conjoin OUT with all literals where, besides the y, only marked variables occur.
(5) For every literal R(t1 , . . . , e, . . . ,tm ) that contains at least an unmarked e, scan S until
     a literal of the type ¬R(t1 , . . . , e, . . . ,tm ) is found: then, try to apply Resolution and
                                                                              W
     if you succeed getting ⊥ k {u1 = u′1 , . . . , um = u′m } conjoin j u j 6= u′j to OUT .
(6) Prefix to OUT a string of existential quantifiers binding all marked variables and
     output the result.
One remark is in order: when running the subprocedures E(si ,ti ) required by the Reso-
lution Rule in (5) above, you must consider all marked variables as part of the y (thus,
e.g. R(e,t), ¬R(e, v) produces ⊥ k {t = u} if both t and u contain, besides the y, only
marked variables).
Proposition 4. Let T be the theory (EUF) in a signature with unary functions and
m-ary relation symbols. Consider a primitive formula ∃e φ (e, y); then, the above algo-
rithm returns a cover of ∃e φ (e, y) in dag-format in time O(n2 ), where n is the size of
∃e φ (e, y).                                                                                        ⊳


                                                   22
Proof. The preprocessing step (1) requires an abstraction phase for producing e-flat
literals and a second phase in order to get a RS-closed set: the first phase requires linear
time, whereas the second one requires O(n·log(n)) time. All the remaining steps require
linear time, except steps (2) and (5) that requires quadratic time. This is the dominating
cost, thus the entire procedure requires O(n2 ) time.                                     ⊣
     Although we do not deeply investigate the problem here, we conjecture that it might
be possible to further lower down the above complexity to O(n · log(n)).


6.1 An extension

We consider a useful extension of the above algorithm; let us assume that we have a
nonempty theory whose axioms are (4), namely
                           ∀x (x = undef ↔ f (x) = undef)
for every function symbol f .
    One side of the above axiom is equivalent to the ground literal f (undef) = undef
and as such it does not interfer with the completion process (we just add it to our con-
straints from the very beginning).
    To accommodate the other side, we need to modify our Calculus. First, we add to
the Constrained Superposition Calculus of Section 5 the following extra Rule

       Inference Rule Ext(undef)                          f (e j ) = u(y) k D
             (Constrained)                       e j = undefk D ∪ {u(y) = undef}
The Rule is sound because u(y) = undef∧ f (e j ) = u(y) → e j = undef follows from the
axioms (4). For cover comuptation with our new axioms, we need a restricted version
of Paramodulation Rule:

    Paramodulation                  e j = r kC      LkD
                                                        (if e j > r & L|p ≡ e j )
     (Constrained)                      L[r] p kC ∪ D


Notice that we can have e j > r only in case r is either some existential variable ei or it
is an e-free term u(y). Paramodulation Rule (if it is not a Superposition) can only apply
to a right member of an equality and such a right member must be e j itself (because our
literals are flat). Thus the rule cannot introduce new terms and consequently it does not
compromize the termination argument of Proposition 3.
     The proof of Theorem 2 can be easily adjusted as follows. We proceed as in the
proof of Theorem 2, so as to obtain the set ∆ (M) ∪ R ∪ S̃ which is saturated in the
standard (unconstrained) Superposition Calculus . Below, we refer to the general refu-
tational completeness proof of the Superposition Calculus given in [42]. Since we only
have unit literals here, in order to produce a model of ∆ (M) ∪ R ∪ S̃, we can just con-
sider the convergent ground rewriting system → consisting of the oriented equalities
in ∆ + (M) ∪ R ∪ S̃: the support of such model is formed by the →-normal forms of
our ground terms with the obvious interpretation for the function and constant sym-

                                            23
bols. For simplicity, we assume that undef is in normal form. 9 We need to check
that whenever we have10 f (t) →∗ undef then we have also t →∗ undef: we prove
this by induction on the reduction ordering for our ground terms. Let t be a term such
that f (t) →∗ undef: if t is e-free then the claim is trivial (because the axioms (4) are
supposed to hold in M). Suppose also that induction hypothesis applies to all terms
smaller than t. If t is not in normal form, then let t˜ be its normal form; then we have
 f (t) →+ f (t˜) →∗ undef, by the fact that → is convergent. By induction hypothesis,
t˜ → undef, hence t →+ t˜ →∗ undef, as desired. Finally, let us consider the case in
which t is in normal form; since f (t) is reducible in root position by some rule l → r,
our rules l → r are e-flat and t is not e-free, we have that t ≡ e j for some existential
variable e j . Then, we must have that S contains an equality of the kind f (e j ) = u(y) k D
or of the kind f (e j ) = ei k D (the constraint D being true in M under the given as-
signment to the y). The latter case is reduced to the former, since ei →∗ undef (by the
convergence of →∗ ) and since S is closed under Paramodulation. In the former case, by
the rule Ext(undef), we must have that S contains e j = undefk D ∪ {u(y) = undef}.
Now, since f (e j ) = u(y) k D belongs to S and D is true in M, we have that the normal
forms of f (e j ) and of u(y) are the same; since the normal form of f (e j ) is undef, the
normal form of u(y) is undef too, which means that u(y) = undef is true in M. But
e j = undefk D ∪ {u(y) = undef} belongs to S, hence e j = undef belongs to S̃, which
implies e j →∗ undef, as desired.                                                          ⊣


6.2 Remarks on MCMT implementation

As evident from Subsection 4.1, our main motivation for investigating covers originated
from the verification of data-aware processes. Such applications require database (DB)
signatures to contain only unary function symbols (besides relations of every arity).
We observed that computing covers of primitive formulae in such signatures requires
only polynomial time. In addition, if relation symbols are at most binary, the cover of
a primitive formula is a conjunction of literals: this is crucial in applications, because
model checkers like MCMT [22] and CUBICLE [15] represent sets of reachable states
as primitive formulae. This makes cover computations a quite attractive technique in
database-driven model checking.
     Our cover algorithm for DB signatures has been implemented in the model checker
MCMT . The implementation is however still partial, nevertheless the tool is able to com-
pute covers for the EUF-fragment with unary function symbol, unary relations and bi-
nary relations. The optimized procedute of Section 6 has not yet been implemented,
instead MCMT uses a customary Knuth-Bendix completion (in fact, for the above men-
tioned fragments constraints are always trivial and our constrained Superposition Cal-
culus essentially boils down to Knuth-Bendix completion for ground literals in EUF.
     Axioms (4) are also covered in the following way. We assume that constraints of
which we want to compute the cover always contains either the literal e j = undef or the
literal e j 6= undef for every existential variable e j . Whenever a constraint contains the
 9 To be pedantic, according to the definition of ∆ + (M), there should be an equality undef = c
                                                                                                0
   in ∆ + (M) so that c0 is the normal form of undef.
10 We use →∗ for the reflexive-transitive closure of → and →+ for the transitive closure of →.



                                               24
literal e j 6= undef, the completion procedure adds the literal u(yi ) 6= undef whenever
it had produced a literal of the kind f (e j ) = u(yi ).11
      We wonder whether we are justified in assuming that all onstraints of which we
want to compute the cover always contains either the literal e j = undef or the literal
e j 6= undef for every existential variable e j . The answer is the affirmative: according to
the backward search algorithm implemented in array-based systems tools, the variable
e j to be eliminated always comes from the guard of a transition and we can assume
that such a guard contains the literal e j 6= undef (if we need a transition with e j =
undef - for an existentially quantified variable e j - it is possible to write trivially this
condition without using a quantified variable). The MCMT User Manual (available from
the distribution) contains precise instructions on how to write specifications following
the above prescriptions.
      A first experimental evaluation (based on the existing benchmark provided in [32],
which samples 32 real-world BPMN workflows taken from the BPMN official web-
site http://www.bpmn.org/) is described in [10]. The benchmark set is available
as part of the last distribution 2.8 of MCMT http://users.mat.unimi.it/users/
ghilardi/mcmt/ (see the subdirectory /examples/dbdriven of the distribution).
The User Manual, also included in the distribution, contains a dedicated section giv-
ing essential information on how to encode relational artifact systems (comprising both
first order and second order variables) in MCMT specifications and how to produce user-
defined examples in the database driven framework. The first experiments were very en-
couraging: the tool was able to solve in few seconds all the proposed benchmarks and
the cover computations generated automatically during model-checking search were
discharged instantaneously, see [10] for more information about our experiments.


7 Conclusions and Future Work
The above experimental setup motivates new research to extend Proposition 2 to further
theories axiomatizing integrity constraints used in DB applications. Combined cover
algorithms (along the perspectives in [26]) could be crucial also in this setting. Practical
algorithms for the computation of covers in the theories falling under the hypotheses of
Proposition 2 need to be designed: as a little first example, in Subsection 6.1 above
we showed how to handle Axiom (4) by light modifications to our techniques. Symbol
elimination of function and predicate variables should also be combined with cover
computations.
    We consider the present work, together with [10,12], as the starting point for a full
line of research dedicated to SMT-based techniques for the effective verification of data-
aware processes, addressing richer forms of verification beyond safety (such as liveness,
fairness, or full LTL-FO) and richer classes of artifact systems, (e.g., with concrete data
types and arithmetics), while identifying novel decidable classes (e.g., by restricting
the structure of the DB and of transition and state formulae) beyond the ones presented
in [10,12]. Concerning implementation, we plan to further develop our tool to incor-
porate in it the plethora of optimizations and sophisticated search strategies available
11 This is sound because e 6= undef implies f (e) 6= undef according to (4), so u(y ) 6= undef
                                                                                   i
  follows from f (e j ) = u(yi ) and e 6= undef.


                                                   25
in infinite-state SMT-based model checking. Finally, in [11] we tackle more conven-
tional process modeling notations, concerning in particular data-aware extensions of
the de-facto standard BPMN12 : we plan to provide a full-automated translator from the
data-aware BPMN model presented in [11] to the artifact systems setting of [12].


References
 1. F. Baader, S. Ghilardi, and C. Tinelli. A new combination procedure for the word problem
    that generalizes fusion decidability results in modal logics. Inform. and Comput., pages
    1413–1452, 2006.
 2. F. Baader and T. Nipkow. Term Rewriting and All That. Cambridge University Press, United
    Kingdom, 1998.
 3. L. Bachmair and H. Ganzinger. Rewrite-based equational theorem proving with selection
    and simplification. J. Log. Comput., 4(3):217–247, 1994.
 4. L. Bachmair, H. Ganzinger, C. Lynch, and W. Snyder. Basic paramodulation. Inform. and
    Comput., 121(2):172–192, 1995.
 5. L. Bachmair, H. Ganzinger, and U. Waldmann. Refutational theorem proving for hierarchic
    first-order theories. Appl. Algebra Eng. Commun. Comput., 5:193–212, 1994.
 6. P. Baumgartner and U. Waldmann. Hierarchic superposition with weak abstraction. In Proc.
    of CADE, pages 39–57, 2013.
 7. M. Bojańczyk, L. Segoufin, and S. Toruńczyk. Verification of database-driven systems via
    amalgamation. In Proc. of PODS, pages 63–74, 2013.
 8. R. Bruttomesso, S. Ghilardi, and S. Ranise. Quantifier-free interpolation in combinations of
    equality interpolating theories. ACM Trans. Comput. Log., 15(1):5:1–5:34, 2014.
 9. D. Calvanese, G. De Giacomo, and M. Montali. Foundations of data aware process analysis:
    A database theory perspective. In Proc. of PODS, 2013.
10. D. Calvanese, S. Ghilardi, A. Gianola, M. Montali, and A. Rivkin. Verification of data-aware
    processes via array-based systems (extended version). Technical Report arXiv:1806.11459,
    arXiv.org, 2018.
11. D. Calvanese, S. Ghilardi, A. Gianola, M. Montali, and A. Rivkin. Formal modeling and
    SMT-based parameterized verification of data-aware BPMN. In Proc. of BPM, 2019.
12. D. Calvanese, S. Ghilardi, A. Gianola, M. Montali, and A. Rivkin. From model completeness
    to verification of data aware processes. In Description Logic, Theory Combination, and All
    That. Springer, 2019.
13. D. Calvanese, S. Ghilardi, A. Gianola, M. Montali, and A. Rivkin. Model completeness,
    covers and superposition. In Proc. of CADE, 2019.
14. C.-C. Chang and J. H. Keisler. Model Theory. North-Holland Publishing Co., Amsterdam-
    London, third edition, 1990.
15. S. Conchon, A. Goel, S. Krstic, A. Mebsout, and F. Zaı̈di. Cubicle: A parallel smt-based
    model checker for parameterized systems - tool paper. In Proc. of CAV, pages 718–724,
    2012.
16. A. Deutsch, R. Hull, F. Patrizi, and V. Vianu. Automatic verification of data-centric business
    processes. In Proc. of ICDT, pages 252–267, 2009.
17. A. Deutsch, Y. Li, and V. Vianu. Verification of hierarchical artifact systems. In Proc. of
    PODS, pages 179–194. ACM Press, 2016.
18. S. Ghilardi. Model theoretic methods in combined constraint satisfiability. J. Autom. Rea-
    soning, 33(3-4):221–249, 2004.
12 http://www.bpmn.org/



                                               26
19. S. Ghilardi and A. Gianola. Interpolation, amalgamation and combination (the non-disjoint
    signatures case). In Proc. FroCoS, pages 316–332. Springer LNAI, 2017.
20. S. Ghilardi and A. Gianola. Modularity results for interpolation, amalgamation and supera-
    malgamation. Ann. Pure Appl. Logic, 2018.
21. S. Ghilardi, E. Nicolini, and D. Zucchelli. A comprehensive framework for combined deci-
    sion procedures. ACM Trans. Comput. Log., pages 1–54, 2008.
22. S. Ghilardi and S. Ranise. MCMT: A model checker modulo theories. In Proc. of IJCAR,
    pages 22–29, 2010.
23. S. Ghilardi and S. J. van Gool. Monadic second order logic as the model companion of
    temporal logic. In Proc. LICS, pages 417–426, 2016.
24. S. Ghilardi and S. J. van Gool. A model-theoretic characterization of monadic second order
    logic on infinite words. J. Symb. Log., 82(1):62–76, 2017.
25. S. Ghilardi and M. Zawadowski. Sheaves, games, and model completions, volume 14 of
    Trends in Logic—Studia Logica Library. Kluwer Academic Publishers, Dordrecht, 2002. A
    categorical approach to nonclassical propositional logics.
26. S. Gulwani and M. Musuvathi. Cover algorithms and their combination. In Proc. of ESOP,
    Held as Part of ETAPS, pages 193–207, 2008.
27. K. Hoder and N. Bjørner. Generalized property directed reachability. In Proc. of SAT, pages
    157–171, 2012.
28. J. Hsiang and M. Rusinowitch. Proving refutational completeness of theorem-proving strate-
    gies: The transfinite semantic tree method. J. ACM, 38(3):559–587, 1991.
29. D. Kapur. Shostak’s congruence closure as completion. In Rewriting Techniques and Appli-
    cations, 8th International Conference, RTA-97, Sitges, Spain, June 2-5, 1997, Proceedings,
    pages 23–37, 1997.
30. D. Kapur. Nonlinear polynomials, interpolants and invariant generation for system analy-
    sis. In Proc. of the 2nd International Workshop on Satisfiability Checking and Symbolic
    Computation co-located with ISSAC, 2017.
31. L. Kovács and A. Voronkov. Interpolation and symbol elimination. In Proc. of CADE, pages
    199–213, 2009.
32. Y. Li, A. Deutsch, and V. Vianu. VERIFAS: A practical verifier for artifact systems. PVLDB,
    11(3):283–296, 2017.
33. P. Lipparini. Locally finite theories with model companion. In Atti della Accademia
    Nazionale dei Lincei. Classe di Scienze Fisiche, Matematiche e Naturali. Rendiconti, Serie
    8, volume 72. Accademia Nazionale dei Lincei, 1982.
34. M. Ludwig and U. Waldmann. An extension of the Knuth-Bendix ordering with lpo-like
    properties. In Proc. of LPAR, pages 348–362, 2007.
35. K. L. McMillan. Lazy abstraction with interpolants. In Proc. of CAV, pages 123–136, 2006.
36. G. Nelson and D. C. Oppen. Fast decision procedures based on congruence closure. J. ACM,
    27(2):356–364, 1980.
37. E. Nicolini, C. Ringeissen, and M. Rusinowitch. Data structures with arithmetic constraints:
    a non-disjoint combination. In Proc. FroCoS, pages 319–334. Springer LNCS, 2009.
38. E. Nicolini, C. Ringeissen, and M. Rusinowitch. Satisfiability procedures for combination
    of theories sharing integer offsets. In Proc. TACAS. Springer LNCS, 2009.
39. E. Nicolini, C. Ringeissen, and M. Rusinowitch. Combining satisfiability procedures for
    unions of theories with a shared counting operator. Fund. Inform., pages 163–187, 2010.
40. R. Nieuwenhuis and A. Oliveras. Fast congruence closure and extensions. Inf. Comput.,
    205(4):557–580, 2007.
41. R. Nieuwenhuis and A. Rubio. Theorem proving with ordering and equality constrained
    clauses. J. Symb. Comput., 19(4):321–351, 1995.
42. R. Nieuwenhuis and A. Rubio. Paramodulation-based theorem proving. In Handbook of
    Automated Reasoning (in 2 volumes), pages 371–443. MIT Press, 2001.


                                              27
43. A. M. Pitts. On an interpretation of second order quantification in first order intuitionistic
    propositional logic. J. Symb. Log., 57(1):33–52, 1992.
44. T. Rybina and A. Voronkov. A logical reconstruction of reachability. In Perspectives of Sys-
    tems Informatics, 5th International Andrei Ershov Memorial Conference, PSI 2003, Revised
    Papers, pages 222–237, 2003.
45. V. Sofronie-Stokkermans. On interpolation and symbol elimination in theory extensions. In
    Proc. IJCAR, Lecture Notes in Computer Science. Springer, 2016.
46. V. Sofronie-Stokkermans. On interpolation and symbol elimination in theory extensions.
    Log. Methods Comput. Sci., 14(3), 2018.
47. V. Vianu. Automatic verification of database-driven systems: a new frontier. In Proc. of
    ICDT, pages 1–13, 2009.
48. W. H. Wheeler. Model-companions and definability in existentially complete structures.
    Israel J. Math., 25(3-4):305–330, 1976.




                                               28
