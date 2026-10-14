             Enumerating Choice Terms in
           Model-Based Quantifier Instantiation

                    Lydia Kondylidou1 , Andrew Reynolds2 ,
                    Jasmin Blanchette1 , and Cesare Tinelli2
           1
               Ludwig-Maximilians-Universität München, Munich, Germany
                  l.kondylidou@lmu.de, jasmin.blanchette@lmu.de
                  2
                    The University of Iowa, Iowa City, United States
               andrew-reynolds@uiowa.edu, cesare-tinelli@uiowa.edu



       Abstract. Satisfiability modulo theories (SMT) solvers are widely used
       for determining the satisfiability of logical formulas with respect to back-
       ground theories. SMT solvers are traditionally based on first-order logic,
       but some also support higher-order logic. Recently, Kondylidou et al.
       introduced model-based quantifier instantiation with fast enumeration
       (MBQI-Enum), a quantifier instantiation strategy that works for both
       logics. A weakness of MBQI-Enum is that it does not find refutations
       when Hilbert choice terms are necessary. In this work, we present an
       extension of MBQI-Enum that enables it to reason effectively about
       Hilbert’s choice operator. The extended strategy substantially increases
       the success rate of the SMT solver cvc5 on higher-order benchmarks.


1   Introduction
Satisfiability modulo theories (SMT) solvers combine a Boolean satisfiability
(SAT) solver with decision procedures for interpreted theories. They work by
refutation: They assume the negation of the conjecture as an axiom and try to
establish the unsatisfiability (i.e., provability) of the input problem. Several SMT
solvers, including Bitwuzla [25], Boolector [26], CVC4 [5], cvc5 [3], veriT [8], and
Z3 [23], support quantifiers via Skolemization and instantiation.
    Most SMT solvers are based on first-order logic, but a few support higher-
order logic. Specifically, CVC4, its successor cvc5, and a prototype version of
veriT have been extended to parse and solve higher-order problems [4]. In prin-
ciple, higher-order logic is often more convenient than first-order logic for ex-
pressing problems, particularly those involving binders (e.g., λx, i , i , x ).
    A crucial aspect of higher-order SMT solvers is their use of quantifier instan-
tiation strategies. Barbosa et al. [4] partly extended the first-order E-matching
strategy [22] to a higher-order setting. Recently, Kondylidou et al. [19] introduced
model-based quantifier i nstantiation w ith f ast e numeration ( MBQI-Enum), a
strategy that extends model-based quantifier i nstantiation ( MBQI) [ 15] with
syntax-guided synthesis (SyGuS) [27] techniques. While traditional MBQI relies
only on ground terms from the MBQI model to instantiate quantified variables,
MBQI-Enum broadens this approach by generating a wider range of candidate

© The Author(s) 2026
S. Junges and G. Katz (Eds.): TACAS 2026, LNCS 16505, pp. 295–314, 2026.
https://doi.org/10.1007/978-3-032-22752-2_15
296     L. Kondylidou et al.

instantiations. It does so by enumerating terms guided by a SyGuS grammar,
which enables it to construct more complex instantiations involving, for instance,
identity functions and uninterpreted symbols. MBQI-Enum was found to be the
most successful strategy [19, Sect. 5] for solving higher-order problems from the
TPTP [39] library.
    A weakness of MBQI-Enum is that it does not attempt instantiations con-
taining Hilbert’s choice operator. A Hilbert choice expression has the form εx. φ,
where variable x is bound in formula φ. The entire expression denotes some value
of x that satisfies φ, if such a value exists; otherwise, it denotes an arbitrary value
from the type of x. Sometimes the ε operator occurs in the input problem, in
which case the SMT solver must reason about it. Even if ε is absent, an ε term
might be useful in quantifier instantiations. The ε operator is reputed to be
difficult to reason about because it is characterized by a higher-order axiom.
    In this paper, we extend MBQI-Enum so that it instantiates quantifiers with
terms that include Hilbert’s choice operator. This extension requires three main
modifications to MBQI-Enum. First, we augment the SyGuS grammar to in-
clude ε terms. Second, we introduce fresh Skolem symbols that represent these
ε terms, since this is simpler than implementing ε terms throughout the SMT
solver. Finally, we generate lemmas corresponding to instances of ε’s character-
istic axiom and add them to the solver.

Example 1. We compare our extended MBQI-Enum with the original on
TPTP benchmark SEV431^1. Let u be an uninterpreted sort, and let f be an
uninterpreted symbol of type u → u. Consider the second-order problem con-
sisting of the injectivity axiom ∀x, y. f x = f y =⇒ x = y for f and the negated
conjecture ∀g. ∃z. g (f z) ̸= z, where g has type u → u and x, y, z have type u.
MBQI-Enum generates the instantiations λy. y, λy. f y, λy. f (f y), . . . for g. As
a result, the SMT solver does not terminate. By contrast, our strategy instanti-
ates g with the term λy. εx. y = f x using the grammar. This term denotes the
left inverse of f. Then the strategy introduces a fresh Skolem symbol h that rep-
resents this term. The lemma ∀y. ¬ (∃x. y = f x) ∨ y = f (h y) characterizing h is
added to the problem. After instantiating g with h, the solver can derive a con-
tradiction with the injectivity axiom. This implies that the unnegated conjecture
∃g. ∀z. g (f z) = z is entailed by the axiom.

    We implemented the extended MBQI-Enum strategy in the cvc5 solver. We
evaluated it on the higher-order benchmarks of the TPTP library [39]. The re-
sults show that Hilbert’s choice is often useful for establishing the unsatisfiability
of an input problem without introducing much overhead in problems where it is
not needed. Remarkably, our extension solves a strict superset of the problems
solved by the original MBQI-Enum.
    We also compare our approach with other cvc5 strategies and find that it
outperforms them. Finally, we compare cvc5 equipped with our strategy with
the provers Satallax [10], Vampire [7], and Zipperposition [40], representing the
state of the art in higher-order automated theorem proving, and find that it is
highly competitive. The raw evaluation data are available online [21]. Our source
        Enumerating Choice Terms in Model-Based Quantifier Instantiation                      297

code, along with instructions for reproducing the experiments, is also available
online [20].

2    Preliminaries
Our approach builds on higher-order logic with Hilbert’s choice, SMT with quan-
tifiers, and MBQI-Enum. Below, we briefly introduce these concepts.

Higher-Order Logic with Hilbert’s Choice. Monomorphic higher-order
logic [1, 16], also called simple type theory [11], generalizes classical first-order
logic by allowing quantification over functions. The syntax distinguishes between
types and terms. Types τ are either base types, or sorts, κ or applications of
the function type constructor → to two types: τ1 → τ2 . The type of Booleans is
denoted by o.
     The term language is based on the simply typed λ-calculus, where terms
t, e, . . . are inductively defined as variables g, x, y, z, . . . , symbols a, b, f, h, p, r . . .
(possibly of function type), term applications t t′ , and λ-abstractions λx. t,
where x is the bound variable and t is the abstraction’s body. A variable is free
in a term if it is not bound by an enclosing λ-abstraction. Terms are syntactically
equal modulo α-, β-, and η-conversion, meaning, for example, that (λx. f x x) c
is syntactically equal to f c c. Terms of type τ1 → · · · → τn → o are called
predicates. A term of type o is called a formula.
     A common extension of higher-order logic is Hilbert’s choice operator ε [17,18,
37]: If x is a variable of type τ and φ is a formula that contains x, then ε (λx. φ),
abbreviated as εx. φ, is a term of type τ . Intuitively, the term εx. φ denotes some
element x of type τ for which the formula φ holds if such an element exists. If no
such element exists, it denotes an arbitrary element of type τ . Unlike existential
quantification, which only asserts the existence of such an element, the choice
operator yields the element. Hilbert’s choice operator is characterized by the
higher-order axiom ∀y. (∃x. y x) =⇒ y (εx. y x). The operator makes it possible
to denote functions that exist according to the standard semantics of higher-order
logic but that otherwise cannot be expressed (cf. Example 1). Some treatments
of Hilbert’s choice include an axiom ∀y, z. y = z =⇒ (εx. y x) = (εx. z x), but
this is a special case of congruence, which is built into higher-order logic.

Quantifier Instantiation in SMT. To reason about the satisfiability of quan-
tified formulas, SMT solvers typically rely on a combination of Skolemization and
heuristic instantiation: Universal quantifiers occurring positively in a formula are
instantiated, while those occurring negatively are Skolemized. Dually, existential
quantifiers occurring positively are Skolemized, whereas those occurring nega-
tively are instantiated.
     Let T be a theory, or combination of theories, over a set of interpreted sym-
bols, and let F be a (conjunctively understood) set of formulas, or problem,
over the signature of T . To determine the satisfiability of F in T , typical SMT
solvers rely on a quantifier-free subsolver for reasoning about quantifier-free for-
mulas and an instantiation module for reasoning about quantified formulas. The
298     L. Kondylidou et al.

former, which combines a SAT solver and a specialized solver for the theory T ,
enumerates potential models of an abstraction of F in which quantified subfor-
mulas are treated as propositional variables. The SAT solver proposes candidate
models for F at the propositional level—truth assignments to atomic formulas
in F that propositionally satisfy F —while the theory solvers check these models
for theory-specific conflicts. If all candidate models generate conflicts, F is de-
clared unsatisfiable. Otherwise, the instantiation module handles the quantified
subformulas in F by generating selected instances of them and adding them to
F . The added instances preserve the satisfiability of F . Instances with quanti-
fiers will be possibly instantiated further, whereas those with no quantifiers will
be directly processed by the quantified-free subsolver.
    Instantiation is performed following user-selectable strategies that compute
substitutions σ for the top-level variables in quantified formulas of F , mapping
those variables to ground (i.e., variable-free) terms. More precisely, for selected
quantified formulas q of the form ∀x1 , . . . , xn . ψ in F and selected substitutions σ
that map each variable xi to a ground term ti , the instantiation module produces
lemmas of the form q =⇒ ψ{x1 → t1 , . . . , xn → tn } that are then added to the
set F . Existentially quantified formulas in F are instantiated by Skolemization:
for each selected formula q of the form ∃x1 , . . . , xn . ψ in F , n fresh Skolem
symbols sk1 , . . . , skn are introduced and a corresponding lemma of the form
q =⇒ ψ{x1 → sk1 , . . . , xn → skn } is added to F . The main SMT loop is then
reentered with the new F .
    This iterative process continues until the SMT solver finds a model for F
with respect to T (which is itself a difficult task given the presence in F of
quantified formulas [14, 15, 32, 34]) or the quantifier-free subsolver determines F
to be unsatisfiable in T . Of course, at any point, the SMT solver may run out
of time or memory.
    To generate relevant ground terms for instantiating universal quantifiers,
SMT solvers rely on instantiation strategies. For first-order logic with theories,
some strategies are refutationally complete and enable SMT solvers to offer semi-
decision procedures: They will find a proof of unsatisfiability if one exists, but
they may not terminate otherwise. Higher-order logic—which allows terms to in-
clude functions as arguments, λ-abstractions, and partial applications—remains
semidecidable under Henkin semantics but is more challenging to support in
practice than first-order logic. The strategies implemented in CVC4, cvc5, and
veriT are pragmatic and do not seek refutational completeness [4, 19].
    For higher-order logic, cvc5 initially supported only an extension of the E-
matching [22] instantiation strategy. New strategies that also partly work on
higher-order problems were later added to the solver. Specifically, MBQI [15]
is a strategy that iteratively refines a candidate model constructed from the
quantifier-free part of the problem and then attempts to refute the model by
generating ground instances of the quantified formulas that may be falsified
by the model. It has been used on higher-order benchmarks and has proved
somewhat effective on these [19, Sect. 5]. Common techniques such as conflict-
guided instantiation [35], enumerative instantiation [30], and counterexample-
      Enumerating Choice Terms in Model-Based Quantifier Instantiation          299

guided instantiation [33] can also be used on higher-order problems, but they
have generally proved less effective [19, Sect. 5], which is unsurprising given
that they were originally designed for first-order reasoning. SyQI [27], a syntax-
guided synthesis approach, works well on some higher-order problems since it
can generate terms by synthesizing candidate expressions with the help of a
grammar [19, Sect. 5].

MBQI-Enum. MBQI-Enum [19] is a recent addition to cvc5 that integrates a
SyGuS-based enumerator directly into MBQI. For each quantified variable in the
formula, MBQI-Enum first constructs a grammar. It then iteratively enumerates
candidate terms generated from the grammar and checks each resulting instance
against the current model. If one instance refutes the current model, the strategy
builds a substitution by mapping the quantified variable to the current enumer-
ated term. If the instance fails to refute the model, the enumerator proceeds to
the next candidate term. If all candidates are exhausted without success, the
strategy reverts to standard MBQI. This fallback mechanism guarantees that
MBQI-Enum can, in principle, solve any problem that MBQI can solve.
    A key aspect of MBQI-Enum is the construction of the SyGuS grammar
that guides the enumeration. The grammar is created from a set of symbols
including uninterpreted symbols extracted from the entire formula and bound
variables that have not yet been instantiated. For higher-order variables, the
grammar incorporates rules for generating λ-abstractions. The enumerator then
systematically constructs λ-expressions by generating terms over the abstrac-
tions’ argument variables.

Example 2. We consider a modified version of the TPTP benchmark SYO288^5,
which is over the theory T of equality with uninterpreted sorts and functions.
Let u be an uninterpreted sort. Let f be a function symbol f : u → u and consider
the second-order conjecture ∃y. ∀z. y z = f z, where y is a variable of type u → u
and z is a variable of type u. To prove its validity in T , we ask the SMT solver to
prove the unsatisfiability of its negation, or, equivalently, of the input problem:

                              F = {∀y. ∃z. y z ̸= f z}

MBQI-Enum first constructs a SyGuS grammar for y to guide the enumeration
process. The set of symbols is empty. The grammar consists of the rules

                g0 ::= λx. g1
                g1 ::= x | f g1 | ite(g2 , g1 , g1 )
                g2 ::= true | false | g1 = g1 | ¬ g2 | g2 ∧ g2 | g2 ∨ g2

In the first iteration, MBQI-Enum enumerates terms generated by the gram-
mar and tries them in sequence. When the enumeration reaches the term λx. x,
MBQI-Enum generates the substitution σ = {y → λx. x}. The strategy then
determines whether the instantiation of the quantified formula, obtained by ap-
plying σ to the subformula ∃z. y z ̸= f z, refutes the current model. This is
300      L. Kondylidou et al.

achieved by checking whether the negation of that subformula, under the cur-
rent substitution σ, is T -satisfiable. Now, if we negate the subformula, instantiate
y with λx. x in it and β-reduce, we obtain a formula equivalent to ∀z. z = f z,
which is satisfiable in T since in that theory the symbol f can be interpreted as
the identity function. The substitution σ is then returned.
    Back in the SMT loop, the instantiation lemma (∀y. ∃z. y z =           ̸ f z) =⇒
∃z. z ̸= f z is then added to F . In essence, this causes the solver to also add
the propositionally entailed formula ∃z. z =   ̸ f z to F . Since that formula has an
existential quantifier prefix, it is Skolemized into sk1 ≠ f sk1 where sk1 is a fresh
symbol of type u. Then, the Skolemization lemma (∃z. z =        ̸ f z) =⇒ sk1 ̸= f sk1
added to F .
    In the next iteration, MBQI-Enum tries the term λx. f x generated by the
grammar and produces the substitution σ = {y → λx. f x}, leading to the
addition of the instantiation lemma (∀y. ∃z. y z =    ̸ f z) =⇒ ∃z. f z ̸= f z to F .
Then, the formula ∃z. f z = ̸ f z is Skolemized, with variable z replaced by a fresh
Skolem symbol sk2 , and the Skolemization lemma (∃z. f z ̸= f z) =⇒ f sk2 =           ̸
f sk2 is added to F . Now, from the formulas ∀y. ∃z. y z =       ̸ f z, (∀y. ∃z. y z ̸=
f z) =⇒ ∃z. f z ≠ f z, and (∃z. f z ̸= f z) =⇒ f sk2 ̸= f sk2 in F , the quantifier-
free subsolver deduces the propositionally entailed formula f sk2 ̸= f sk2 , which
it then determines to be unsatisfiable. The SMT solver then concludes that the
original F is unsatisfiable in T , and hence that the conjecture is valid.


3      The Extended Strategy
Our strategy is based on MBQI-Enum, which has proved effective for higher-
order reasoning. It adds three main ingredients:
    • the grammar guiding the enumeration is augmented to include ε terms;
    • fresh Skolem symbols are introduced to represent these terms; and
    • term filtering is applied to eliminate redundant or invalid candidate terms
      during enumeration.
In addition to these extensions, our strategy generalizes MBQI-Enum by return-
ing not only a substitution but also a set of lemmas. These lemmas are added
to the input problem F , extending it iteratively.
     The generalized strategy is detailed in Algorithm 3. It takes as input a quan-
tified formula q of the form ∀y1 , . . . , ym . ψ occurring in F , where ψ does not
start with a universal quantifier. It starts by computing an initial substitution σ
from the model (line 3). If no such substitution exists, it returns the empty set,
indicating that no instantiation could be found.
     After computing σ, the strategy iterates over the quantified variables y1 , . . . ,
ym in the formula q to instantiate. For each yi where i ∈ {1, . . . , m}, it constructs
a SyGuS grammar Gi based on uninterpreted symbols appearing in the entire
input formula (line 7). The grammar is further augmented to include terms of
the form εx. φ, where x is a variable whose type is the return type of yi and
φ is a formula over x and other free variables and symbols from the formula q.
      Enumerating Choice Terms in Model-Based Quantifier Instantiation       301

Algorithm 3 Generalized MBQI-Enum
 1: function mbqi_enum_with_choice(q)
 2:    assume q is ∀y1 , . . . , yn . ψ
 3:    let σ ← insts_mbqi(q)
 4:    if σ does not exist then
 5:        return ∅
 6:    for each i ∈ {1, . . . , n} do
 7:        let Gi ← make_grammar(q, yi )
 8:        for each j ∈ {1, 2, . . . } do
 9:            let e ← get_enum_term(Gi , j)
10:            if e does not exist then
11:                break
12:            σ ′ ← σ[yi → e]
13:            if ¬ ψσ ′ is satisfiable then
14:                σ ← σ′
15:                break
16:    return get_lemmas(σ)



This grammar guides the enumeration of candidate terms that may be used to
instantiate yi . As a result, the SyGuS enumerator generates both ε and non-ε
terms as potential substitutions for yi .
     For each candidate term e generated by the enumerator, a new substitution
σ ′ is formed by mapping yi to the current term e in the initial substitution σ
(line 12). The strategy then checks whether the negation of the body of the
quantified formula under σ ′ is satisfiable in the current model (line 13). This
satisfiability check serves as a semantic filter, pruning out terms that do not
yield counterexamples. If the check succeeds, σ is updated and the enumeration
process proceeds to the next quantified variable. Otherwise, it continues with
the next candidate term. Once all quantified variables have been considered, our
strategy returns both the final substitution σ and a set of lemmas, which include
those introduced during the handling of ε terms and quantifier instantiations.
These lemmas are subsequently added to the input formula F , extending it
iteratively.

Augmented Grammar. Our strategy augments the base grammar used for
term enumeration in MBQI-Enum by incorporating ε terms, allowing the gen-
eration of arbitrary formulas. Our approach is detailed in Algorithm 4.
   MBQI-Enum constructs a base grammar for each universally quantified vari-
able yi in the formula q using a set of symbols S from the entire input formula,
such as uninterpreted symbols and bound variables (line 4). A grammar G is
a triple (g0 , G, RG ), where g0 is the initial symbol, G is a set of nonterminal
symbols with g0 ∈ G, and RG is a set of production rules. Each rule has the
form g ::= t, where g ∈ G and t is a term built from symbols in the set S, non-
terminals in G, free variables, and symbols from the signature of a background
theory T . The symbols in S, along with the free variables and the theory sym-
bols from T , act as terminal symbols in the grammar. Each grammar generates
302    L. Kondylidou et al.

Algorithm 4 Augmented grammar
 1: function make_grammar(q, yi )
 2:    let F be the input formula
 3:    S ← symbols(F ) ∪ symbols(q) ∪ {yi+1 , . . . , yn }
 4:    let (g0 , G, RG ) ← make_base_grammar(S, yi )
 5:    if choice is enabled then
 6:        let x be a variable of type τ
 7:        (p0 , P, RP ) ← make_predicate_grammar(S, x, yi )
 8:        extend G ← G ∪ P
 9:        extend RG ← {g0 ← εx. p0 } ∪ RG ∪ RP
10:    return (g0 , G, RG )
11: function make_predicate_grammar(S, x, yi )
12:    S ← S ∪ {x}
13:    let z¯ ← bound variables in yi
14:    define p0 nonterminals
15:    let P ← {z̄} ∪ S ∪ {true, false, =, ¬, ∧}
16:    define RP ← production rules
17:    return (p0 , P, RP )



terms whose type matches the return type τ of yi . For higher-order variables,
the grammars include rules for generating λ-abstractions. In this case, the initial
symbol g0 expands to λ-terms. Whereas earlier versions of MBQI-Enum consid-
ered only terms in η-long β-normal form [19], the current cvc5 implementation
allows partial application. The variables bound by λ-abstractions are terminal
symbols in the grammar that generates the abstraction’s body. For example, if
yi is a function variable of arity n whose arguments and result are all of the
same type, the grammar includes rules such as

              g0 ::= λx1 , . . . , xn . g1             g1 ::= x1 | · · · | xn

    To include ε terms of the form εx. φ, our strategy extends the grammar as
follows. For the nonterminal g1 in the base grammar corresponding to yi ’s return
type τ , a variable x of type τ is introduced (line 6) and added to the symbol set
S (line 12). A new grammar is then built to generate Boolean formulas over the
extended symbol set S ∪ {x} (line 7). This predicate grammar is defined as the
triple (p0 , P, RP ), where p0 is the initial nonterminal symbols and P is a set of
nonterminal symbols that includes p0 . The set RP contains production rules of
the form p ::= t, where p ∈ P and t is a term. Each term t is built from symbols
in S, nonterminals in P , variables that were bound in yi but now appear free, and
symbols from the signature of the Boolean background theory (line 15). These
elements act as terminal symbols in the grammar. The new grammar includes
the rules

      p0 ::= true | false | p1 = p1 | ¬ p0 | p0 ∧ p0        p1 ::= x1 | · · · | xn | x

The nonterminal p0 directly defines the body of the ε term. We define a new
production rule of the form g1 ::= εx. p0 . The resulting grammar is con-
       Enumerating Choice Terms in Model-Based Quantifier Instantiation                         303

structed by extending the base grammar (g0 , G, RG ) with the predicate grammar
(p0 , P, RP ) and the new production rule (lines 8–9). The final grammar is defined
as (p0 , G ∪ P, {g1 ::= εx. p0 } ∪ RG ∪ RP ). It can be used to enumerate both ε
and non-ε terms and is thus more expressive than the original grammar. For our
example, the final grammar consists of the rules

     g0 ::= λx1 , . . . , xn . g1                             g1 ::= εx. p0 | x1 | · · · | xn
     p0 ::= true | false | p1 = p1 | ¬ p0 | p0 ∧ p0           p1 ::= x1 | · · · | xn | x

Skolem Symbols. The most important part of the strategy is where we take
formulas containing ε terms generated by the grammar, abstract these terms
into fresh Skolem symbols, and generate corresponding lemmas with triggers to
guide efficient higher-order quantifier instantiation. Our approach is detailed in
Algorithm 5.


Algorithm 5 Lemmas for Skolem symbols
 1: function get_lemmas(σ)
 2:    let L ← ∅
 3:    let ψ ′ ← ψ
 4:    for all i ∈ {1, . . . , m} do
 5:        assume yi σ = λ(x1 , . . . , xn ). t              ▷ yi is the variable being instantiated
 6:        let t′ ← t
 7:        for all subterms e of t of the form εx : τ. φ(z̄, x) do
 8:            let z¯ = (z1 : τ1 , . . . , zk : τk ) ⊆ {x1 , . . . , xn } be φ’s free variables
 9:            let h : (τ1 , . . . , τk ) → τ be a fresh Skolem symbol
10:            let lemma ← ∀¯        z. ¬ (∃x. φ(z̄, x)) ∨ φ(z̄, h z̄)
11:            extend L ← L ∪ {lemma}
12:            replace e in t′ with h z¯
13:        ψ ′ ← ψ ′ {yi → λ(x1 , . . . , xn ). t′ }
14:    let inst_lemma ← (∀y1 , . . . , ym . ψ) =⇒ ψ ′
15:    extend L ← L ∪ {inst_lemma}
16:    return L



    Our strategy generalizes MBQI-Enum by iterating over the variables in
∀y1 , . . . , ym . ψ and incrementally building a fully instantiated formula before
generating the instantiation lemmas. It then returns the set of generated lem-
mas L instead of only the substitutions.
    Given a substitution σ = {yi → λx1 , . . . , xn . t} for each variable yi , consider
any subterm e of t of the form εx : τ. φ(z̄, x), where z¯ = (z1 : τ1 , . . . , zk : τk ),
the free variables of e, are included in {x1 , . . . , xn }. We replace all occurrences
of e in t with an application of a fresh Skolem symbol h to the variables z¯ (lines
5–10). In other words, the subterm εx. φ(z̄, x) is converted to h z̄, where h has
type τ1 → · · · → τk → τ . The introduction of these Skolems abstracts the ε
binder into symbols understood by the rest of the SMT solver. Our strategy
constructs the lemma ∀¯      z. ¬ (∃x. φ(z̄, x)) ∨ φ(z̄, h z̄) (line 10) and adds it to the
304     L. Kondylidou et al.

lemma set L. When later added to the set F , this lemma makes the strategy less
incomplete while preserving F ’s satisfiability. It guarantees that if there exists
an x satisfying φ(z̄, x), then h z¯ satisfies φ as well.
    Additionally, we mark the Skolem application h z¯ as a trigger [12, 13] in the
lemma. This trigger guides E-matching, ensuring that instantiations are driven
by terms that match the structure of the Skolem application, which is applied
to exactly the same set of variables as in the original quantified formula.
    After all ε-subterms in t have been abstracted, the modified substitution
yi → λx1 , . . . , xn . t′ , where t′ is obtained by replacing the ε-subterms of t with
the corresponding Skolem applications h z¯ (line 12), is applied to the partially
instantiated body ψ of the formula q (line 13). This procedure is repeated for
each variable yi , yielding a fully instantiated formula ψ ′ in which all substitutions
have been applied to the universally quantified variables and all Skolem symbols
have been introduced. Finally, the instantiation lemma (∀y1 , . . . , ym . ψ) =⇒ ψ ′
is generated (line 14) and added to the lemma set L. The complete set L is
eventually returned and merged with the current set F .

Filtering. To avoid redundant instantiations, term filtering is applied during
enumeration. Enumerated terms already present in the set of candidate terms
are discarded, ensuring that terms equivalent under rewriting are considered only
once. For terms of the form εx. φ, the bound variable x must occur in the body φ.
Terms in which x does not occur are excluded, to prevent the introduction of
trivial instantiations. Since cvc5 already performs extensive theory-specific fil-
tering by default, no additional filtering is required in our setting.

Example 6. We return to Example 1 and present it in more detail. Let T be
the same theory as in the previous examples. Let u be an uninterpreted sort and
let f be an uninterpreted function of type u → u. Consider the conjecture

                (∀x, y. f x = f y =⇒ x = y) =⇒ ∃g. ∀z. g (f z) = z

where g has type u → u and x, y, z have type u. The formula states that if f
is injective, then it has a left inverse. We prove that the formula holds in T by
contradiction. That is, we negate it, obtaining the following input problem

              F = {∀x, y. f x = f y =⇒ x = y, ∀g. ∃z. g (f z) =
                                                              ̸ z} ,

and prove that F is unsatisfiable in T .
   MBQI-Enum generates a grammar for g using the set of symbols S = {f}.
The grammar consists of the rules

                   g0 ::= λy. g1                    g1 ::= y | f g1

Based on this grammar, MBQI-Enum generates the substitutions {g → λy. y},
{g → λy. f y}, {g → λy. f (f y)}, . . . for g. Since this enumeration does not
capture inverse functions, the SMT solver does not terminate.
       Enumerating Choice Terms in Model-Based Quantifier Instantiation            305

    Our strategy addresses this challenge by constructing a richer grammar. We
introduce a variable x of type u and extend the symbol set to S ∪ {x}. We then
define the following grammar:

       p0 ::= true | false | p1 = p1 | ¬ p0 | p0 ∧ p0        p1 ::= y | x | f p1

We extend the MBQI-Enum grammar by adding a rule to produce εx. p0 . The
result consists of the rules for p0 and p1 above and the following rules:

                g0 ::= λy. g1                  g1 ::= εx. p0 | y | f g1

Using this grammar, our strategy generates the term λy. εx. y = f x, which
denotes a left inverse of f, leading to the substitution {g → λy. εx. y = f x}.
   Corresponding to this term, we introduce a fresh Skolem symbol h : u → u.
Our strategy asserts the following lemma:

                         ∀y. ¬ (∃x. y = f x) ∨ y = f (h y)                         (ℓ1 )

The lemma states that for any y, if there exists an x such that y = f x (i.e., y is
in the image of f), then applying f to h y must yield y. The original enumerated
term λy. εx. y = f x is thus rewritten to the term λy. h y. The substitution
σ = {g → λy. h y} is considered. Next, the instantiation lemma

                     (∀g. ∃z. g (f z) ̸= z) =⇒ ∃z. h (f z) ̸= z                    (ℓ2 )

is generated by applying the substitution σ followed by β-reduction. The set of
lemmas L = {(ℓ1 ), (ℓ2 )} is constructed. Each lemma in L is then added to set
F . After that, Skolemization introduces a fresh symbol sk corresponding to the
existentially quantified variable z. The lemma

                        (∃z. h (f z) ̸= z) =⇒ h (f sk) ̸= sk                       (ℓ3 )

is also added to F .
    The strategy proceeds to instantiate the universally quantified formulas in
F . Quantified variables of type u are instantiated using terms from F . First, the
strategy instantiates x and y in ∀x, y. f x = f y =⇒ x = y with sk and h (f sk),
respectively. Then it instantiates x and y in the lemma ∀y. ¬ (∃x. y = f x) ∨ y =
f (h y) with sk and f sk, respectively. These instantiations arise from E-matching,
which matches each lemma’s pattern against the terms already present in the
equivalence classes maintained by the SMT solver. The instantiation lemmas

    (∀y. ¬ (∃x. y = f x) ∨ y = f (h y)) =⇒ f sk ̸= f sk ∨ f sk = f (h (f sk))      (ℓ4 )
    (∀x, y. f x = f y =⇒ x = y) =⇒ f sk ̸= f (h (f sk)) ∨ sk = h (f sk)            (ℓ5 )

are then added to F . At this point, the quantifier-free subsolver finds F unsatis-
fiable in T by determining that the conclusions of the lemmas ℓ3 , ℓ4 , and ℓ5 are
jointly unsatisfiable in T . This implies that the conjecture is valid.
306    L. Kondylidou et al.

Example 7. We consider a simplified version of TPTP benchmark SYO268^5.
Let u1 , u2 be uninterpreted sorts, and let r be a function symbol of type u1 →
u2 → o. Consider the conjecture

                       (∀x. ∃y. r x y) =⇒ ∃g. ∀x. r x (g x)

where g has type u1 → u2 , x has type u1 , and y has type u2 . The formula states
that for every total relation r on u1 × u2 , there exists a corresponding function
from u1 to u2 . To prove the formula by contradiction, we negate it and obtain
the input problem F = {∀x. ∃y. r x y, ∀g. ∃x. ¬ r x (g x)}.
   MBQI-Enum generates a grammar for g using the set of symbols S = {r}.
The grammar consists of the rules

                    g0 ::= λy. g1                         g1 ::= t

Based on this grammar, MBQI-Enum generates the substitution {g → λy. t},
where t is a ground term of type u2 . As a result, the SMT solver terminates with
an unknown status.
    By contrast, with our extension, the solver behaves as follows. Let x be a
variable of type u2 . We extend the symbol set to S ∪ {x}. Consider the rules

          p0 ::= true | false | p1 = p1 | p2 = p2 | r p1 p2 | ¬ p2 | p2 ∧ p2
          p1 ::= y
          p2 ::= x

We augment the MBQI-Enum grammar by adding a rule to produce εx. p0 . The
resulting grammar consists of the rules for p0 , p1 , and p2 above together with

                 g0 ::= λy. g1                      g1 ::= εx. p0 | t

Using this grammar, our strategy generates the term λy. εx. r y x, leading to
the substitution {g → λy. εx. r y x}.
   Corresponding to this term, we introduce a fresh Skolem symbol h : u1 → u2 .
Our strategy asserts the following lemma:

                              ∀y. ¬ (∃x. r y x) ∨ r y (h y)                    (ℓ1 )

The original enumerated term λy. εx. r y x is thus rewritten to the term λy. h y.
The substitution σ = {y → λy. h y} is considered. Next, the instantiation lemma

                     (∀g. ∃x. ¬ r x (g x)) =⇒ ∃x. ¬ r x (h x)                  (ℓ2 )

is generated by applying the substitution σ followed by β-reduction. The set
of lemmas L = {(ℓ1 ), (ℓ2 )} is constructed and then merged with F . Afterward,
Skolemization introduces a fresh symbol sk corresponding to the existentially
quantified variable x. The lemma

                        (∃x. ¬ r x (h x)) =⇒ ¬ r sk (h sk)                     (ℓ3 )
        Enumerating Choice Terms in Model-Based Quantifier Instantiation        307

is added to F .
    The strategy proceeds to instantiate the universally quantified formulas of
F . Quantified variables of nonfunction type are instantiated using terms from
F . First, the strategy instantiates x and y in the lemma ∀y. ¬ (∃x. r y x) ∨
r y (h y) with h sk and sk, respectively. Then it instantiates x and y in the axiom
∀x. ∃y. r x y with sk, and h sk, respectively. These instantiations arise from E-
matching, which matches each lemma’s pattern against the terms already present
in the equivalence classes maintained by the solver. The instantiation lemmas

           (∀y. ¬ (∃x. r y x) ∨ r y (h y)) =⇒ ¬ r sk (h sk) ∨ r sk (h sk)       (ℓ4 )
           (∀x. ∃y. r x y) =⇒ r sk (h sk)                                       (ℓ5 )

are added to F . At this point, the quantifier-free subsolver finds F unsatisfiable.
Hence the conjecture is valid.


4   Implementation

We developed our strategy as an extension of cvc5’s implementation of MBQI-
Enum. Our extension refines the selection of grammars for term enumeration,
introduces a mechanism for managing choice terms generated by these grammars,
and incorporates a filtering step to discard redundant or unsuitable terms.
    For each quantified variable, MBQI-Enum constructs a SyGuS grammar that
specifies the space of candidate instantiations (Algorithm 4, line 4). Our imple-
mentation augments these grammars with terminal rules for generating choice
terms. Specifically, for each nonterminal type that qualifies, we add a correspond-
ing expression of the form εx. φ, which selects a value satisfying a predicate over
that type (lines 5–9). This allows the enumerator to synthesize Skolem-style
instantiations directly from the grammar.
    We use the existing implementation of the fast SyGuS-based enumerator for
term generation. This enumerator considers only terms that are unique up to
rewriting [31]. During the enumeration process, ε terms are constructed within
cvc5’s internal abstract syntax tree representation, thereby exploiting cvc5’s
built-in rewriter. For example, εx. x = t, where x does not occur free in t,
is rewritten to t.
    Beyond these rewrite-based simplifications, our implementation applies ad-
ditional heuristics for filtering ε terms. In particular, it explicitly discards any
term of the form εx. φ, where x does not occur free in φ. These heuristics are
implemented via a callback from the SyGuS enumerator.
    The enumerator constructs ε terms that are immediately purified by our
implementation. Recall that each ε term is replaced with a fresh Skolem symbol,
and an accompanying lemma is generated to relate the Skolem to the original ε
term (Algorithm 5, lines 6–10). For example, given a term εx. φ, the procedure
introduces a fresh Skolem h and asserts that either φ(h) holds or the quantified
condition that motivated the ε term is already satisfied. An important heuristic
is that our approach designates the Skolem application itself as a trigger for the
308       L. Kondylidou et al.

generated quantified formula, thereby ensuring that instantiations during solving
are guided by the intended terms.
    During instantiation, terms containing ε terms are first normalized through
the purification and filtering procedures described above before being considered
as candidate substitutions. The generalized strategy, shown in Algorithm 3, iter-
atively builds substitutions by enumerating terms from the augmented grammars
(lines 6–12), tests them in the current model (line 13), and commits suitable as-
signments (line 14). Notably, unlike the standard MBQI-Enum procedure, our
strategy returns not only substitutions but also auxiliary lemmas (line 16).


5      Evaluation

We extensively evaluated our cvc5 implementation of the extended MBQI-Enum
on higher-order benchmarks.
   Since the publication of Kondylidou et al. [19], MBQI-Enum has been devel-
oped further independently of our work on choice. In our evaluation, by “original
MBQI-Enum” we mean the most recent version of the strategy excluding our
modifications related to ε. This strategy includes the following enhancements
over Kondylidou et al.:

    • MBQI-Enum now supports partial applications, allowing the strategy to con-
      sider candidate terms that partially apply functions during enumeration.
    • Timeouts have been added to subsolver invocations used for checking candi-
      date instantiations, preventing individual candidates from stalling the overall
      SMT loop. In addition, there is an option that completely prohibits nested
      MBQI calls, which avoids potential nontermination caused by nested sub-
      solver invocations.
    • MBQI-Enum now incorporates a guess-and-test loop with a progress-aware
      instantiation cache: When a proposed instantiation fails to refute the current
      model, it is cached to avoid rechecking the same substitution later, thereby
      ensuring that the strategy always makes progress.
    • We now incorporate a lookahead approach that preemptively considers
      Skolem symbols for quantified formulas that are not introduced during pre-
      processing. These symbols are incorporated into the SyGuS grammars, thus
      enriching the set of terms we consider for instantiation with MBQI-Enum.

Setup. We denote our configuration of MBQI-Enum extended with choice
by cvc5[C]. We compare our strategy against several established quantifier
instantiation strategies in cvc5: cvc5[s], which uses SyQI [27]; cvc5[m], which im-
plements MBQI [15]; cvc5[M], which implements the original MBQI-Enum [19];
cvc5[hoelim], which eagerly rewrites higher-order constraints into first-order
form and applies full quantifier saturation; and cvc5[foinst], which relies on
exhaustive first-order-style instantiation and axiomatic handling of higher-order
applications.
       Enumerating Choice Terms in Model-Based Quantifier Instantiation       309

   Table 1. Extended MBQI-Enum vs. other provers on TPTP TH0 benchmarks

                           Satallax   Vampire   Zipperposition   cvc5[C]
           Satisfiable       196         14            0           204
           Unsatisfiable    2162       2303         2083          2178
           Total            2358       2317         2083          2382
           Unknown            15         16            0           154
           Timeouts         1384       1424         1674          1221



   We also include a comparison with the state-of-the-art provers Satallax [10],
Vampire [7], and Zipperposition [40]. Satallax was run with its default settings.
Vampire was run in portfolio mode, as its higher-order reasoning configuration
automatically enables this mode and disabling it makes the prover much less
competitive. For Zipperposition, we enabled several options that were extensively
evaluated by Bozec and Blanchette [9] and shown to achieve the best overall
performance on higher-order benchmarks.
   All experiments were conducted on a machine with a 40-core Intel Xeon Silver
4114 CPU running at 2.20 GHz, equipped with 192 GB of RAM and running
Debian 12 (Bookworm). Each benchmark was executed with a timeout of 60
seconds.

Benchmarks. The experiments were carried out on monomorphic higher-order
problems (TH0) from version 9.1.0 of the TPTP library [39]. The benchmark
set consists of 3757 problems. From the 3962 TH0 problems, we excluded 205
benchmarks that one or more systems could not parse (e.g., because of the use
of interpreted arithmetic).
    To support reasoning with choice, we implemented external parser support
for the TPTP operators for ε and the definite description operator ι. Although
the TPTP library contains very few problems with ε and ι, they might arise in
users’ problems.

Results. The results are shown in Tables 1 and 2, where bold indicates the
most successful system. Notably, our approach achieves the highest total count
of solved benchmarks, surpassing the nearest competitor by 24 solved problems
and the baseline MBQI-Enum by 23.
    Table 1 compares our strategy (cvc5[C]) with external state-of-the-art prov-
ers. Our approach achieves the highest total number of solved benchmarks, with
2382 problems, surpassing Satallax, Vampire, and Zipperposition. It outperforms
the nearest competitor by 24 benchmarks. In particular, our strategy solves 204
satisfiable problems, while Satallax solves 196, Vampire solves 14, and Zipperpo-
sition solves none. For unsatisfiable problems, Vampire performs the best, solving
2303 benchmarks, whereas our strategy solves 2178, Satallax 2162, and Zipper-
position 2083. Overall, our strategy demonstrates strong performance across
310           L. Kondylidou et al.

Table 2. Extended MBQI-Enum vs. other cvc5 strategies on TPTP TH0 benchmarks

                       cvc5[hoelim]   cvc5[foinst]   cvc5[s]   cvc5[m]   cvc5[M]   cvc5[C]
      Satisfiable            14            37           88       188       204       204
      Unsatisfiable        2082          2126         1657      2074      2155      2178
      Total                2096          2163         1745      2262      2359      2382
      Unknown                 0           125           45       289       158       154
      Timeouts             1661          1469         1967      1206      1240      1221



both satisfiable and unsatisfiable problems compared with the state-of-the-art
provers.
    Table 2 compares cvc5[C] with other cvc5 quantifier instantiation strategies.
Our configuration solves 23 unsatisfiable benchmarks that the baseline MBQI-
Enum cannot, with no benchmarks lost, while solving the same number of satis-
fiable problems (204). This shows that extending MBQI-Enum with choice con-
sistently improves solver performance. Overall, when compared against all other
available quantifier instantiation strategies, our strategy achieves the strongest
performance, demonstrating that it is considerably more effective on higher-order
benchmarks than any other individual technique in cvc5. It may seem as though
23 additional benchmarks are not that many; however, we should bear in mind
that the vast majority of higher-order TPTP benchmarks do not contain choice
and can likely be solved without reasoning about choice.
    In addition, our technique solves several problems not solved by its competi-
tors: 143 problems not solved by Vampire, 296 not solved by Zipperposition, 235
not solved by Satallax, and 21 not solved by any other cvc5 strategy. When con-
sidering all systems, cvc5[C] solves exactly one benchmark that no other system
can solve.


6      Related Work
Besides MBQI-Enum, other quantifier instantiation strategies work on higher-
order problems, notably E-matching, MBQI, and SyQI. In higher-order E-
matching, quantified variables are instantiated by matching their patterns
against ground terms available in the current context—that is, the set of ground
terms introduced during proof search. This technique has been extended to sup-
port higher-order features, such as functional arguments [3]. Higher-order MBQI
constructs candidate models that provide interpretations for functions. This en-
ables the solver to generate ground instantiations of quantified formulas in an
attempt to refute the current model [15]. Higher-order SyQI further improves the
instantiation process by selecting candidate terms using syntactic templates and
heuristics derived from the problem’s structure, guided by a fixed grammar [27].
None of these approaches provides special support for Hilbert’s choice.
    Other higher-order provers support Hilbert’s choice in various ways. Satal-
lax implements specialized tableau inference rules that directly reason about ε
       Enumerating Choice Terms in Model-Based Quantifier Instantiation        311

terms in a sound and refutationally complete way [2]. Leo-III integrates ε into its
extensional higher-order paramodulation calculus and supports Henkin seman-
tics with choice [38]. Zipperposition includes a dedicated choice axiom within
its higher-order superposition calculus, allowing it to reason about ε terms as
needed [6]. Vampire supports Hilbert’s choice either through a Leo-III-style in-
ference or by introducing the choice axiom [7].
    Hilbert’s choice is also present in proof assistants such as Isabelle/HOL [28],
Lean [24], and Rocq [36] (formerly known as Coq). In Isabelle/HOL, the choice
operator is introduced as an axiom as part of the system’s core libraries. In
systems based on dependent type theory, such as Lean and Rocq, choice is intro-
duced via classical axioms, which should be avoided in constructive definitions
and proofs. Even in Isabelle/HOL, some users, such as Paulson [29], prefer to
avoid choice:
    Pragmatists may argue that in verification nobody cares whether choice
    is used or not. However, pragmatists should be concerned that reasoning
    about ε-terms is tricky.
Reasoning about choice is indeed tricky, but cvc5 can do it reasonably well now.


7   Conclusion
We presented an SMT quantifier instantiation strategy that extends the MBQI-
Enum strategy so as to reason natively about Hilbert’s choice operator. It can
be used to solve problems that contain Hilbert’s choice but also problems that
do not (cf. Example 1). We implemented the approach in the SMT solver cvc5.
The empirical results on higher-order TPTP benchmarks show that our strategy
is clearly superior to the original MBQI-Enum.
    We believe there is potential for further improving the strategy. We noticed
that the ε terms we need often occur too late in the term enumeration (which is
by increasing term size), since they tend to be relatively complex. Better term
enumeration heuristics and term filtering could help the SMT solver generate
the desired terms earlier—before the timeout.

Acknowledgments. We thank Mark Summerfield and the anonymous review-
ers for their helpful comments. We also thank Haniel Barbosa, who provided
many comments on an earlier draft.
    This research was cofunded by the European Union (ERC, Nekoka,
101083038). Views and opinions expressed are however those of the authors only
and do not necessarily reflect those of the European Union or the European
Research Council. Neither the European Union nor the granting authority can
be held responsible for them.
    This research was also partially funded by the Defense Advanced Research
Projects Agency (DARPA) under contract FA8750-24-2-1001. Any opinions,
findings, and conclusions or recommendations expressed here are those of the
authors and do not necessarily reflect the views of DARPA.
312     L. Kondylidou et al.

Data-Availability Statement. The artifact associated with this paper, in-
cluding the software and scripts used for experiments, is publicly available on
Zenodo [20]. The raw evaluation data are also available on Zenodo [21]. The
instructions on the first Zenodo page [20] explain how to reproduce the experi-
mental evaluation.


References
 1. Andrews, B.: An Introduction to Mathematical Logic and Type Theory: To Truth
    Through Proof, APLS, vol. 27. Springer (2022)
 2. Backes, J., Brown, C.E.: Analytic tableaux for higher-order logic with choice. Jour-
    nal of Automated Reasoning 47, 451–479 (2011)
 3. Barbosa, H., Barrett, C., Brain, M., Kremer, G., Lachnitt, H., Mann, M., Mo-
    hamed, A., Mohamed, M., Niemetz, A., Nötzli, A., Ozdemir, A., Preiner, M.,
    Reynolds, A., Sheng, Y., Tinelli, C., Zohar, Y.: cvc5: A versatile and industrial-
    strength SMT solver. In: Fishman, D., Rosu, G. (eds.) TACAS 2022. LNCS, vol.
    13243, pp. 415–442. Springer (2022)
 4. Barbosa, H., Reynolds, A., Ouraoui, D.E., Tinelli, C., Barrett, C.: Extending SMT
    solvers to higher-order logic. In: Fontaine, P. (ed.) CADE 2019. LNCS, vol. 11716,
    pp. 35–54. Springer (2019)
 5. Barrett, C.W., Conway, C.L., Deters, M., Hadarean, L., Jovanovic, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: Gopalakrishnan, G., Qadeer, S. (eds.) CAV
    2011. LNCS, vol. 6806, pp. 171–177. Springer (2011)
 6. Bentkamp, A., Blanchette, J., Tourret, S., Vukmirović, P.: Superposition for higher-
    order logic. Journal of Automated Reasoning 67 (2023)
 7. Bhayat, A., Suda, M.: A higher-order Vampire (short paper). In: Benzmüller, C.,
    Heule, M.J.H., Schmidt, R.A. (eds.) IJCAR 2024. LNCS, vol. 14739, pp. 75–85.
    Springer (2024)
 8. Bouton, T., de Oliveira, D.C.B., Déharbe, D., Fontaine, P.: veriT: An open,
    trustable and efficient SMT-solver. In: Schmidt, R.A. (ed.) CADE 2009. LNCS,
    vol. 5663, pp. 151–156. Springer (2009)
 9. Bozec, T., Blanchette, J.: Iterative monomorphisation. In: Thiemann, R., Weiden-
    bach, C. (eds.) FroCoS 2025. LNCS, vol. 15979, pp. 269–286. Springer (2025)
10. Brown, C.E.: Satallax: An automatic higher-order prover. Journal of Automated
    Reasoning 7364, 111–117 (2012)
11. Church, A.: A formulation of the simple theory of types. Journal of Symbolic Logic
    5, 56–68 (1940)
12. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: A theorem prover for program check-
    ing. Journal of the ACM 52(3), 365–473 (2005)
13. Dross, C., Conchon, S., Paskevic, A.: Reasoning with triggers. In: Fontaine, P.,
    Goel, A. (eds.) SMT 2012. EPiC Series in Computing, vol. 20, pp. 22–31 (2012)
14. Ge, Y., Barrett, C.W., Tinelli, C.: Solving quantified verification conditions using
    satisfiability modulo theories. Annals of Mathematics and Artificial Intelligence
    55(1-2), 101–122 (2009)
15. Ge, Y., de Moura, L.: Complete instantiation for quantified formulas in satisfi-
    abiliby modulo theories. In: Bouajjani, A., Maler, O. (eds.) CAV 2009. LNCS,
    vol. 5643, pp. 306–320. Springer (2009)
16. Gordon, M.J.C.: Introduction to the HOL system. In: Archer, M., Joyce, J.J.,
    Levitt, K.N., Windley, P.J. (eds.) HOL 1991. pp. 2–3. IEEE (1991)
        Enumerating Choice Terms in Model-Based Quantifier Instantiation              313

17. Hilbert, D., Ackermann, W.: Grundzüge der Theoretischen Logik, Grundlehren der
    mathematischen Wissenschaften, vol. 27. Springer (1928)
18. Hilbert, D., Bernays, P.: Grundlagen der Mathematik I, Grundlehren der mathe-
    matischen Wissenschaften, vol. 40. Springer (1934)
19. Kondylidou, L., Reynolds, A., Blanchette, J.: Augmenting model-based instantia-
    tion with fast enumeration. In: Gurfinkel, A., Heule, M. (eds.) TACAS 2025. LNCS,
    vol. 15696, pp. 85–103. Springer (2025)
20. Kondylidou, L., Reynolds, A., Blanchette, J., Tinelli, C.: Artifact for paper “Enu-
    merating choice terms in model-based quantifier instantiation”. In: TACAS 2026.
    Zenodo (2026), https://doi.org/10.5281/zenodo.18304537
21. Kondylidou, L., Reynolds, A., Blanchette, J., Tinelli, C.: Enumerating choice terms
    in model-based quantifier instantiation [data set]. In: TACAS 2026. Zenodo (2026),
    https://doi.org/10.5281/zenodo.18212605
22. de Moura, L., Bjørner, N.: Efficient E-matching for SMT solvers. In: Pfenning, F.
    (ed.) CADE 2007. LNCS, vol. 4603, pp. 183–198. Springer (2007)
23. de Moura, L., Bjørner, N.: Z3: An efficient SMT solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) TACAS 2008. LNCS, vol. 4963, pp. 337–340. Springer (2008)
24. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming language.
    In: Platzer, A., Sutcliffe, G. (eds.) CADE 2021. LNCS, vol. 12699, pp. 625–635.
    Springer (2021)
25. Niemetz, A., Preiner, M.: Bitwuzla. In: Enea, C., Lal, A. (eds.) CAV 2023. LNCS,
    vol. 13965, pp. 3–17. Springer (2023)
26. Niemetz, A., Preiner, M., Biere, A.: Boolector 2.0. Journal on Satisfiability, Boolean
    Modeling and Computation 9, 53–58 (2014)
27. Niemetz, A., Preiner, M., Reynolds, A., Barrett, C., Tinelli, C.: Syntax-guided
    quantifier instantiation. In: Groote, J.F., Larsen, K.G. (eds.) TACAS 2021. LNCS,
    vol. 12652, pp. 145–163. Springer (2021)
28. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL: A Proof Assistant for
    Higher-Order Logic, LNCS, vol. 2283. Springer (2002)
29. Paulson, L.C.: Defining functions on equivalence classes. In: Guruswami, V.,
    Glazener, T. (eds.) CoRR 2019. vol. 7, pp. 658–675. Association for Computing
    Machinery (2019)
30. Reynolds, A., Barbosa, H., Fontaine, P.: Revisiting enumerative instantiation. In:
    Beyer, D. (ed.) TACAS 2018. LNCS, vol. 10806, pp. 112–131. Springer (2018)
31. Reynolds, A., Barbosa, H., NÖtzli, A., Barrett, C.W., Tinelli, C.: cvc4sy: Smart
    and fast term enumeration for syntax-guided synthesis. In: Dillig, I., Tasiran, S.
    (eds.) CAV 2019, Part II. LNCS, vol. 11562, pp. 74–83. Springer (2019)
32. Reynolds, A., Blanchette, J.C., Cruanes, S., Tinelli, C.: Model finding for recursive
    functions in SMT. In: Olivetti, N., Tiwari, A. (eds.) IJCAR 2016. LNCS, vol. 9706,
    pp. 133–151. Springer (2016)
33. Reynolds, A., Deters, M., Kuncak, V., Tinelli, C., Barrett, C.: Counterexample-
    guided quantifier instantiation for synthesis in SMT. In: Kroening, D., Păsăreanu,
    C.S. (eds.) CAV 2015. LNCS, vol. 9207, pp. 198–216. Springer (2015)
34. Reynolds, A., Tinelli, C., Goel, A., Krstić, S.: Finite model finding in SMT. In:
    Sharygina, N., Veith, H. (eds.) CAV 2013. LNCS, vol. 8044, pp. 640–655. Springer
    (2013)
35. Reynolds, A., Tinelli, C., de Moura, L.: Finding conflicting instances of quantified
    formulas in SMT. In: FMCAD 2014. pp. 195–202. IEEE (2014)
36. Rocq Development Team: Rocq Prover. https://zenodo.org/records/15149629
    (2025), Zenodo
314     L. Kondylidou et al.

37. Simpson, S.G.: The epsilon calculus and conservative extensions. Notre Dame Jour-
    nal of Formal Logic 25(3), 193–202 (1984)
38. Steen, A.: Extensional Paramodulation for Higher-Order Logic and its Effective
    Implementation Leo-III. Ph.D. thesis, Freie Universität Berlin (2020)
39. Sutcliffe, G.: The TPTP problem library and associated infrastructure—from CNF
    to TH0, TPTP v6.4.0. Journal of Automated Reasoning 59, 483–502 (2017)
40. Vukmirović, P., Bentkamp, A., Blanchette, J., Cruanes, S., Nummelin, V., Tourret,
    S.: Making higher-order superposition work. Journal of Automated Reasoning 66,
    541–564 (2022)




Open Access. This chapter is licensed under the terms of the Creative Com-
mons Attribution-NonCommercial-NoDerivatives 4.0 International License (http://
creativecommons.org/licenses/by-nc-nd/4.0/), which permits any noncommercial use,
sharing, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the
Creative Commons license and indicate if you modified the licensed material. You do
not have permission under this license to share adapted material derived from this
chapter or parts of it.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
