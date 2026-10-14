                                                     Bit-Precise CHC Satisfiability Using
                                                         Theory-Modular Reasoning

                                                     Omer Rappoport , Orna Grumberg , and Yakir Vizel

                                                         Technion - Israel Institute of Technology, Haifa, Israel
                                                             {omer.r,orna,yvizel}@cs.technion.ac.il

                                                Abstract. Deciding satisfiability of Constrained Horn Clauses (CHCs)
                                                modulo the theory of fixed-size bit-vectors (TB ) is fundamental to bit-
                                                precise program verification. However, state-of-the-art CHC-solvers often
                                                struggle with TB , limiting scalability in bit-precise reasoning.
                                                We present Mosaic, a theory-modular framework for deciding satisfia-
                                                bility of CHCs modulo TB by combining reasoning in TB and the theory
arXiv:2608.05337v1 [cs.LO] 5 Aug 2026




                                                of Integer Arithmetic (TI ). Given a CHC set modulo TB , Mosaic par-
                                                titions it into two fragments interpreted over TB and TI . Moreover, it
                                                implements an algorithm that reasons about the fragments in a modu-
                                                lar fashion, exchanges information between them via sound translations
                                                across theories, and determines satisfiability w.r.t. the original CHC set.
                                                We implemented a prototype of Mosaic using Z3 and Spacer and eval-
                                                uated it on bit-manipulating benchmarks. Our evaluation shows that
                                                Mosaic significantly outperforms Spacer on these benchmarks.


                                        1     Introduction
                                        Constrained Horn Clauses (CHCs) is a fragment of First Order Logic (FOL) with
                                        many practical applications in Formal Methods [3,17,9]. In particular, program
                                        safety can be reduced to satisfiability of a set of CHCs. Often, the reduction
                                        of program safety to CHCs is done w.r.t. the theory of Integer Arithmetic (TI ).
                                        Since CHC-solvers perform well when Integer Arithmetic is used as a background
                                        theory, this results in efficient program safety verification. However, when pro-
                                        gram operations are required to be represented soundly relative to the low-level
                                        bit representation of data, CHC-solvers do not perform as efficiently.
                                            Encoding program safety verification w.r.t. bit-precise semantics can be nat-
                                        urally achieved through a reduction to CHCs modulo the theory of Fixed-Size
                                        Bit-Vectors (TB ). Alternatively, bit-precision can be modeled using TI despite
                                        the fact that the domain is infinite. This is done by representing bit-precise op-
                                        erations and modular arithmetic via multiplication, division, and modulo con-
                                        straints [19]1 . However, neither approach consistently yields an efficient verifica-
                                        tion procedure. This encoding choice presents a fundamental trade-off: TB for-
                                        mulations often hinder the generalization capabilities of CHC-solvers, whereas
                                        bit-precise TI encodings produce complex constraints that are computationally
                                        expensive to process, particularly in the presence of bit-wise operations.
                                        1
                                            Note that [19] does not consider CHCs. The primary focus of that work is on solving
                                            formulas over QF_BV using a bit-precise encoding w.r.t. QF_IA.
2       O. Rappoport et al.

     In this paper, we present Mosaic, a novel framework designed to efficiently
decide the satisfiability of CHCs modulo TB by leveraging the complementary
strengths of both TB and TI . Given a set of CHCs Π(TB ), Mosaic first parti-
tions the input into two distinct fragments, (ΠB (TB ), ΠI (TI )), each interpreted
under its respective background theory. Mosaic then employs a dual-reasoning
algorithm that processes both sets in a modular fashion to determine the sat-
isfiability of the original Π(TB ). The core intuition behind Mosaic is to exploit
the fact that CHC-solvers handle CHCs modulo TI effectively when limited to
arithmetic operations. By isolating purely arithmetic constraints in ΠI (TI ) while
retaining bit-wise operations in ΠB (TB ), Mosaic bridges the aforementioned gap,
effectively “enjoying the best of both worlds” to achieve superior performance.
     Deciding the satisfiability of Π(TB ) using the decomposed sets (ΠB (TB ), ΠI (TI ))
is a non-trivial task that requires bridging the differences in signatures and se-
mantics of TB and TI through sound transformations. To enable modular rea-
soning, Mosaic integrates three essential components: (i) a theory transformer
to translate formulas and structures between TB and TI ; (ii) an interface to
facilitate communication of reasoning steps between ΠB and ΠI ; and (iii) an al-
gorithm that leverages these components to analyze both fragments and decide
the satisfiability of the original Π(TB ) while ensuring soundness.
     Decomposing Π(TB ) into (ΠB , ΠI ) is done in three steps. First, the set Π is
partitioned into two distinct subsets (ΠB , ΠI ) such that their union is Π. While
the partitioning can be done arbitrarily, in our prototype implementation it is
performed according to the constraints that appear in the body of CHCs in
Π. Specifically, CHCs that include only arithmetic operations are placed in ΠI ,
while CHCs that include bit-wise operations are placed in ΠB . Next, ΠI is re-
encoded w.r.t. TI using a theory transformer, which translates constraints over TB
to constraints over TI . Lastly, ΠB and ΠI share uninterpreted predicate symbols.
For every shared predicate symbol p, two copies, pB and pI , are created. Then,
p is substituted with pB and pI in ΠB and ΠI , respectively. If p is an interface
predicate, namely, w.l.o.g. p appears in the head of a clause in ΠB and in the body
of a clause in ΠI , it is essential to maintain the “logical connection” between ΠB
and ΠI . To achieve that, a set of interface constraints Θ is generated for all such
interface predicates. These constraints ensure consistency w.r.t. interpretations
of the newly created copies of p. The result of these steps is the tuple ΠB|I =
(ΠB , ΠI , Θ), called a theory-modular encoding.
     Reasoning over a theory-modular encoding ΠB|I = (ΠB , ΠI , Θ) is performed
by MosaicSolve. The procedure relies on existing CHC-solvers for TB and TI .
It generates single-theory queries, delegates them to the corresponding CHC-
solvers, and coordinates the exchange of information between fragments as dic-
tated by the interface constraints.
     We implemented a proof-of-concept of Mosaic using Z3 [12] and its CHC-
solver Spacer [11]. For the evaluation, we created a benchmark with several
examples that highlight the benefits of Mosaic over a standard CHC-solver. This
benchmark set consists of small realistic programs that use bit-manipulating, as
well as arithmetic, operations. Our evaluation shows that while Spacer cannot
                 Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                                                  3

                                                        B
                                          Π = { x >s 0 → p(x, 0, 0),
                                                                            B                               B           B
                                                   p(x, a, b), a <s x → p(x, a + 1, b − 1),
                                                                     B
                                                   p(x, a, b), ¬(a <s x) → q(a, b),
1 void f ( int x ) {                                               B    B
                                                   q(a, b), ¬((a ⊕ b) <s 0) → ⊥ }
2   assume (x >0) ;
3   int a =0 , b =0;                                                            (b)
    while (a < x ) {                           ′                ′               I       ′
4                                      ΠI = { x > 0, x ↾B → p (x , 0, 0),
5     a ++;                                    I    ′       ′
                                              p (x , a , b ), a < x
                                                                    ′   ′           ′               I   ′       ′
                                                                                            → p (x , a + 1, b − 1),
                                                                                                                            ′

6     b - -;                                   I    ′       ′       ′           ′               ′       I       ′   ′
                                              p (x , a , b ), ¬(a < x ) → q (a , b ) }
7   }
                                               B                            B               B
8   assert (( a ^ b ) <0) ;            ΠB = { q (a, b), ¬((a ⊕ b) <s 0) → ⊥ }
9 }                                            I        B
                                        Θ={q ⇝q }
                (a)                                                             (c)

    Fig. 1. The opp-signs benchmark. (a) A C function. (b) Its CHC encoding over the
    bit-vector theory (Π). (c) A theory-modular encoding, where arithmetic operations are
    handled in integer arithmetic (ΠI ), while bit-precise operations remain in the bit-vector
    fragment (ΠB ), with the original connections preserved via interface constraints (Θ).
    All variables and constants in Π have sort BV[n] for some n ∈ N+ . Bit-vector constants
    are written using their signed integer values for readability. The term (a ⊕B b) <Bs 0
    evaluates to true if and only if a and b have opposite signs.


    handle these examples, even when considering bit-vectors of a relatively small
    size, Mosaic easily solves these instances for much larger bit-vector sizes.

    Motivating Example. Our motivation comes from program safety verification.
    Assume that the reduction to CHCs is done modulo TB in order to capture
    program safety soundly relative to the low-level bit representation of data. Using
    TB as a background theory, however, limits the kind of programs that can be
    analyzed since CHC-solvers often do not perform well when TB is used.
        Now, consider the set of clauses in Fig. 1(b). It encodes a simple program
    (Fig. 1(a)) that receives an input x greater than 0, and initializes variables a
    and b to 0. Next it performs x iterations of a loop, incrementing a by 1, while
    decrementing b by 1 at each iteration. The property states that the bit-wise XOR
    of a and b is always negative. This bit-wise operation is equivalent to checking
    whether a and b have opposite signs, which clearly holds for this program. When
    encoded using TB (Fig. 1(b)), given a time limit of 2 hours, Spacer can only
    solve it for bit-vectors of width 9. When encoding this problem using bit-precise
    TI [19] Spacer can only solve the resulting CHCs for an encoding that captures
    bit-vectors of size 3, given the same 2 hours time limit.
        Next, consider the Mosaic encoding in Fig. 1(c). The set of clauses is parti-
    tioned into two sets ΠB and ΠI and the encoding is performed w.r.t. T̄ = (TB , TI ).
    The partitioning is not chosen arbitrarily. ΠB includes a bit-precise operation
    (bit-wise XOR), while ΠI includes only arithmetic. As a result, we choose TB
    for ΠB and TI for ΠI . Using this encoding, Mosaic is able to solve this example
    instantly for bit-vectors up to a size of 62, considerably outperforming Spacer.
4       O. Rappoport et al.

1.1   Related Work
To the best of our knowledge, prior work on CHC-SAT has not explored a theory-
modular approach that combines multiple background theories within a single
framework. The work in [16] partitions a set of CHCs based on its structure, but
all subsets are interpreted over the same background theory. In contrast, Mosaic
enables coordinated reasoning across different theories.
    In program verification, several works combine reasoning over TB and TI . For
example, [8] alternates between reasoning in TI and validating in TB , while other
approaches [18,5] rely on abstraction and refinement. In contrast, Mosaic does
not use abstraction and captures the semantics of TB precisely.
    Transforming logical formulas between theories, both syntactically and se-
mantically, is not a new concept. In Institution theory [6,7], such transforma-
tions are formalized via signature and institution morphisms. In the context
of Satisfiability Modulo Theories (SMT), similar translations have been devel-
oped, in particular for TB [14,19,2]. Theory combination in SMT is classically
handled by the Nelson-Oppen framework [13], which assumes stable infiniteness
and thus does not apply to TB , and restricts communication to equalities over
shared variables. More general frameworks based on polite theories [15,10] can
handle TB . In contrast, Mosaic operates in the CHC-SAT setting and, rather
than combining theories within a single formula, decomposes CHCs into frag-
ments interpreted over different theories and coordinates them via the exchange
of general quantifier-free formulas, going beyond equality-based communication.


2     Preliminaries
2.1   Many-Sorted First-Order Logic with Equality
We assume the reader is familiar with first-order logic and satisfiability.

Syntax We fix an infinite set S of sort symbols and an infinite set X of variables,
where each variable is uniquely associated with a sort in S. A signature Σ is a
tuple (S, P, F), where S ⊆ S is a set of sort symbols, and P and F are sets of
predicate and function symbols, respectively. Each predicate symbol p ∈ P (resp.,
function symbol f ∈ F ) is assigned a unique arity n ∈ N and a type σ1 × · · · × σn
(resp., σ1 ×· · ·×σn → σ), where σi , σ ∈ S. Function symbols of arity 0 are called
constant symbols. Σ-terms, Σ-atoms, and Σ-formulas are defined in the standard
way, subject to the requirement that they are well-sorted, i.e., all function and
predicate applications must respect their types. A Σ-sentence is a formula with
no free variables. We write φ[x̄] to denote a formula whose free variables are in
x̄. The constants ⊤ and ⊥ denote the truth values true and false, respectively.

Semantics Given a signature Σ = (S, P, F ), a Σ-structure M maps each sort
σ ∈ S to a non-empty set DM    σ , called the domain of σ in M. It also maps each
predicate symbol p ∈ P of type σ1 × · · · × σn to a relation pM ⊆ DM      p , where
DM
 p  =  DM
        σ1 × · · · × DM
                      σn , and similarly for function symbols. For a variable x∈X
              Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                 5

of sort σ, we write DM           M
                        x for Dσ , and extend this notation to tuples x̄ in the
natural way. When a formula has free variables, satisfiability is defined relative
to a structure and an assignment, i.e., a partial function mapping variables to
elements of their domains. For x̄ = (x1 , . . . , xn ) and ā = (a1 , . . . , an ) ∈ Dx̄M ,
we write {x̄ 7→ ā} for the assignment that maps each xi to ai . The satisfiability
relation is defined in the standard way. We write M, {x̄ 7→ ā} |= φ[x̄] to denote
that M and {x̄ 7→ ā} satisfy φ. If φ is a sentence, we simply write M |= φ.
For a Σ-formula φ with free variables x̄, the semantics of φ with respect to
M, denoted JφKM , is the set of all tuples that satisfy φ under M, that is,
JφKM = { ā ∈ DM x̄ | M, {x̄ 7→ ā} |= φ }. We sometimes extend a signature with
fresh predicate symbols. Let P ′ be disjoint from P, with types over S. We write
Σ ∪ P ′ for the signature (S, P ∪ P ′ , F). For each p′ ∈ P ′ , let Rp′ ⊆ DM       p′ . We
write M{p′ 7→ Rp′ }p′ ∈P ′ for the (Σ ∪ P ′ )-structure that interprets each p′ as
Rp′ and agrees with M on all symbols of Σ.

Theories Theories are used to constrain the interpretation of certain symbols in
a signature. A Σ-theory is a class of Σ-structures, called its models. A structure
M satisfies a Σ-sentence φ modulo T , written M |=T φ, if M is a T -model and
M |= φ. A sentence φ is satisfiable modulo T if some T -model satisfies it, and
valid modulo T , written |=T φ, if all T -models satisfy it. Next, we introduce two
theories, which are the focus of this work.
    The signature ΣB = (SB , PB , FB ) and the theory TB of fixed-size bit-vectors
are defined in SMT-LIB 2 [1].2 The set SB contains all sorts BV[n] for n ∈ N+ ,
where n denotes the bit-width. The set PB includes, for each n, equality =, un-
signed comparisons <Bu , ≤Bu , and signed comparisons <Bs , ≤Bs of type BV[n]×BV[n].3
The set FB includes, for each n ∈ N+ , a constant symbol of type BV[n] for each
bit-vector of width n, represented as a bit-string.4 It also includes arithmetic
operators +B , −B , ·B , divBu , modBu , bitwise operators ∼B , &B , |B , ⊕B , and shift oper-
ators ≪B , ≫B , all of type BV[n] × BV[n] → BV[n] (except ∼B : BV[n] → BV[n]), as
well as extraction [u : l]B : BV[n] → BV[u − l + 1] for 0 ≤ l ≤ u < n, and concate-
nation ◦B : BV[n] × BV[m] → BV[n + m]. The class of quantifier-free ΣB -formulas
is denoted QF_BV. Throughout the paper, we fix a TB -model MB
    The signature ΣI = (SI , PI , FI ) and the theory TI of integer arithmetic are
also defined in SMT-LIB 2. The set SI consists of the single sort Int. The set PI
includes equality = and comparisons <, ≤ of type Int × Int. The set FI includes
a constant symbol of type Int for each integer. It also includes the arithmetic
operators +, −, ·, div, mod of type Int × Int → Int. The class of quantifier-free
ΣI -formulas is denoted QF_IA. Throughout the paper, we fix a TI -model MI .

2.2    Constrained Horn Clauses
Syntax Let Σ = (S, P, F) be a signature, and let P U be a set of fresh predicate
symbols, called uninterpreted predicates, disjoint from P and typed over S.
2
  We use a subset sufficient to express all bit-vector symbols.
3
  Symbols in ΣB are overloaded for each BV[n].
4
  We sometimes refer to a bit-vector constant by its unsigned or signed integer value.
6        O. Rappoport et al.

    A Constrained Horn Clause (CHC ) over Σ ∪ P U is a sentence
                                                             V         of the form
∀x̄. B[x̄] → H[x̄], for which: (i) The body B[x̄] is ϕ[x̄] ∧ i pi (x̄pi ), where ϕ
(the constraint) is a quantifier-free Σ-formula over x̄5 , and each pi (x̄pi ) is an
application of pi ∈ P U with x̄pi ⊆ x̄; and (ii) The head H[x̄] is either h(x̄h ) for
some h ∈ P U with x̄h ⊆ x̄, or ⊥.
    An uninterpreted predicate may appear multiple times in the body with
different arguments. A CHC is a query if its head is ⊥, and a rule otherwise. A
rule is a fact if its body contains no uninterpreted predicates.
    A set of CHCs can encode a safety verification problem for a sequential pro-
gram. In such an encoding, the uninterpreted predicates serve as placeholders for
inductive invariants at specific program locations, while the constraints capture
the program’s transitions between these locations. Facts encode assumptions on
initial states, and queries dually encode assertions.

Semantics Fix a set of CHCs Π over Σ ∪ P U and a Σ-theory T . To define
satisfiability of Π modulo T , we first define the semantics of uninterpreted
predicates. Given a T -model M, an uninterpreted predicate p ∈ P U , and n ∈ N,
the bounded semantics of p w.r.t. M at bound n, denoted JpKM   n , is the set of
tuples in DM p derivable for p from Π by derivations of depth at most n. In the
context of program verification, JpKM
                                    n corresponds to the set of program states
reachable at the location of p by executions inducing derivations of depth at
most n. The bounded semantics is defined inductively on n as follows.
Definition 1 (Bounded Semantics). Let M be a T -model, p ∈ P U an un-
interpreted predicate symbol, and n ∈ N a bound. The bounded semantics of p
with respect to M at bound n, denoted JpKMn , is defined as follows:
                            [                               ′
             JpKM
                n =                  J∃(x̄ \ x̄p ). B[x̄]KM             (1)
                        (∀x̄. B[x̄]→p(x̄p ))∈Π
                                        
                                        M{q 7→ ∅}q∈P U            if n = 0
                        where M′ =
                                        M{q 7→ JqKM }             if n > 0
                                                     n−1 q∈P U

Example 1. Consider the CHC set Π in Fig. 1(b), where all variables have sort
BV[2]. Here we use binary bit-vector notation. Then (01, 00, 00) ∈ JpKM
                                                                      0
                                                                        B
                                                                          (derived
from the first CHC), (01, 01, 11) ∈ JpKM
                                       1
                                         B
                                           (from the second CHC),   and (01, 11) ∈
JqKM
   2
     B
       (from the third CHC).
    Observe that the bounded semantics are defined in a monotonic manner: for
all n ∈ N, JpKM         M
              n ⊆ JpKn+1 . The bounded semantics of all uninterpreted predicates
in Π stabilize at the first limit ordinal ω yielding their (unbounded) semantics [3].
The semantics of p with respect to M, denoted JpKM , is given by n∈N JpKM
                                                                       S
                                                                               n .
    The satisfiability of a CHC set can be defined via the semantics of its uninter-
preted predicates. Every T -model M can be expanded to a (Σ ∪ P U )-structure
M{p 7→ JpKM }p∈P U , which interprets each p by its semantics w.r.t. M. By
5
    For simplicity, we assume all variables in x̄ appear in the constraint.
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning               7

Definition 1, this expansion satisfies all rules in Π. We say that Π is satisfiable
modulo T if there exists a T -model whose expansion also satisfies all queries.

Definition 2 (Satisfiability). Π is satisfiable modulo T if there exists a T -
model M such that M{p 7→ JpKM }p∈P U |= π for every query π ∈ Π.

Definition 3 (The CHC-SAT Problem). Given a CHC set Π over Σ ∪ P U
and a Σ-theory T , determine whether Π is satisfiable modulo T .

    When Π is unsatisfiable modulo T , the bounded semantics can be used to
construct a derivation of ⊥ [4], denoted Π ⊢T ⊥. Such a derivation is called
a refutation. In the context of safety verification, a refutation corresponds to a
finite execution leading to an assertion violation.
    In practice, CHC-SAT algorithms search for interpretations of the unin-
terpreted predicates that over-approximate their semantics while satisfying the
queries. In safety verification, such interpretations correspond to inductive invari-
ants sufficient to prove safety. The search is typically restricted to interpretations
representable by formulas [3]. A Σ-interpretation I assigns to each p ∈ P U of
type σ1 × · · · × σn a Σ-formula I(p) with free variables ȳp = (y1 , . . . , yn ), with yi
of sort σi . For π ∈ Π, we write I(π) for the Σ-formula obtained by replacing each
uninterpreted predicate application p(x̄p ) that occurs in π with I(p)[ȳp 7→ x̄p ].

Definition 4 (Solution). A Σ-interpretation I satisfies Π modulo T , denoted
I |=T Π, if I(π) is valid modulo T for every π ∈ Π. In this case, I is called a
Σ-solution for Π.

   If I is a Σ-solution, then for every T -model M, the expansion M{p 7→
JI(p)KM }p∈P U satisfies all π ∈ Π. Moreover, JpKM ⊆ JI(p)KM for all p ∈ P U .
Thus, if a Σ-solution exists, then Π is satisfiable. The converse, however, does
not necessarily hold due to the limited expressiveness of the class of Σ-formulas.


3    Theory Transformers
As a first step toward our theory-modular approach to deciding the satisfiability
of CHCs modulo TB , we introduce a pair of translation functions, called theory
transformers. The first transformer, denoted τB⇝I , translates bit-vector formulas
into integer arithmetic, while the second transformer, denoted τI⇝B , translates
formulas in the opposite direction. These transformers form the basis of our
approach. Given a set Π of CHCs over ΣB , the transformer τB⇝I is used to
translate a selected fragment of Π to ΣI . Later, when deciding satisfiability of
Π, each fragment is reasoned about in its respective theory, and the transformers
τB⇝I and τI⇝B enable the transfer of information between fragments. Crucially,
this process preserves the semantics of Π, even though the fragments are defined
over different signatures and theories and involve variables of different sorts.
    For the remainder of this section, let Π be a set of CHCs over the signature
ΣB ∪P U , where P U is a set of uninterpreted predicate symbols. We fix a bijective
variable mapping χB⇝I between bit-vector variables (i.e., variables of sort BV[n]
8       O. Rappoport et al.

for some n ∈ N+ ) and integer variables (variables of sort Int). To simplify the
notation, for every bit-vector variable x we write x′ to denote the unique integer
variable such that χB⇝I (x) = x′ . For every tuple x̄ = (x1 , . . . , xm ) of bit-vector
variables, we write x̄′ to denote (x′1 , . . . , x′m ).
    To preserve semantics across theories, for each bit-vector variable x of sort
BV[n] (for some n ∈ N+ ), we relate the domain of x in MB to the domain of
its corresponding integer variable x′ in MI . The domain DM     x
                                                                    B
                                                                       = DMBV[n] is finite
                                                                              B


and consists of all bit-vectors of width n, whereas DM        MI
                                                      x′ = DInt is infinite and
                                                        I


includes the integers. This correspondence is captured by a domain transformer.
Definition 5 (Domain Transformer). Let x be a variable of sort BV[n] for
n ∈ N+ . A domain transformer for x is an injective mapping δB⇝I
                                                             x
                                                                 : DM
                                                                    x
                                                                      B
                                                                        → DM
                                                                           x′ .
                                                                             I



     To ensure consistency, the only restriction on domain transformers is that
all variables appearing in the same argument position of an uninterpreted pred-
icate application in Π must be assigned the same mapping.6 Apart from this
restriction, domain transformers can, in principle, be defined arbitrarily. How-
ever, two natural choices that simplify the translation and yield a more natural
encoding in integer arithmetic are to use either unsigned or signed semantics
for bit-vectors. Let x be a bit-vector variable of sort BV[n] for some n ∈ N+ .
The unsigned domain transformer of x, whose image is [0, 2n − 1] ⊂ DM                     x′ ,
                                                                                            I

                          MB
                                           Pn−1           i
maps each v ∈ Dx to [v]N = i=0 v[i] · 2 . The signed domain transformer
of x, whose image is [−2n−1 , 2n−1 − 1] ⊂ DM             x′ , maps each v ∈ Dx
                                                            I                    MB
                                                                                    to [v]Z =
                     n−1
                             P n−2          i 7
−(v[n − 1]) · 2           + i=0 v[i] · 2 . From now on, the presentation remains ag-
nostic to the concrete choice of domain transformers. The specific instantiation
used in the implementation is discussed in Section 6.
     Let x̄ = (x1 , . . . , xm ) be a tuple of bit-vector variables. For a tuple v̄ =
(v1 , . . . , vm ) ∈ DMx̄
                          B
                            = DM                  MB              x̄
                                x1 × · · · × Dxm , we write δB⇝I (v̄) to denote the tuple
                                   B

   x1                 xm                                                 x̄
(δB⇝I (v1 ), . . . , δB⇝I (vm )). By abuse of notation, we extend δB⇝I        element-wise to
                   MB
subsets of Dx̄ . For the inverse direction, for any integer value v ′ ∈ DM           x′ that
                                                                                        I

                            x                  x     ′
lies in the image of δB⇝I , we write δI⇝B (v ) to denote the unique bit-vector value
v ∈ DM   x
             B              x
               such that δB⇝I  (v) = v ′ . We lift the inverse domain transformer to tuples
and sets analogously. For an uninterpreted predicate p ∈ P U that occurs in Π,
               p                          x̄p
we use δB⇝I         as shorthand for δB⇝I       , where x̄p is a tuple of variables such that
the application p(x̄p ) appears in some CHC in Π. This notation is well defined
due to the consistency requirement, which ensures that variables in the same
argument position of an uninterpreted predicate application in Π are assigned
the same domain transformer.
     Let φ′ be a quantifier-free ΣI -formula with free variables x̄′ . Recall that
   ′ MI
Jφ K         denotes the set of tuples satisfying φ′ under MI . We sometimes restrict
   ′ MI
Jφ K          to elements corresponding to bit-vector values in MB via the domain
transformers. To this end, we define the restriction of Jφ′ KMI to MB .
6
  In CHCs, since all variables are universally quantified, the same variable may appear
  in different contexts. To allow greater flexibility in the choice of domain transformers,
  one may rename variables so that different CHCs use distinct variables.
7
  Signed values are represented using two’s complement.
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                9

Definition 6 (Domain Restriction). Let φ′ ∈ QF_IA with free variables x̄′ .
The restriction of Jφ′ KMI to MB , denoted Jφ′ KMI ↾B , is defined as follows:
                        Jφ′ KMI ↾B = Jφ′ KMI ∩ δB⇝I
                                                x̄
                                                     Dx̄MB
                                                           

Example 2. Let (x, y) be a pair of bit-vector variables of sort BV[2], and assume
      x           y
that δB⇝I   and δB⇝I  are the unsigned domain transformers.
                                    (x,y)
Jx′ < y ′ KMI ↾B = Jx′ < y ′ KMI ∩ δB⇝I DM
                                                
                                             B
                                          (x,y)   =
{(a, b) ∈ (DM  I 2                       2
            Int ) | a < b} ∩ {0, 1, 2, 3} = {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)}

    Restrictions can also be performed syntactically by bounding variable do-
mains. Let x be a bit-vector variable of sort BV[n] for some n ∈ N+ . We write
x′ ↾B to denote the ΣI -constraint enforcing that x′ ranges over the image of
 x
δB⇝I , that is, 0 ≤ x′ ∧ x′ ≤ 2n − 1 for the unsigned domain transformer, and
−2  n−1
        ≤ x′ ∧ x′ ≤ 2n−1 − 1 for the signed domain transformer.
Lemma 1. Let φ′ ∈ QF_IA with free variables x̄′ . The following holds:
                                        ^
                    Jφ′ KMI ↾B = Jφ′ ∧       x′↾B KMI
                                                 x′ ∈x̄′

Example 3. Following Example 2, the formula x′ < y ′ ∧ x′↾B ∧ y ′↾B is equivalent
to x′ < y ′ ∧ (0 ≤ x′ ∧ x′ ≤ 3) ∧ (0 ≤ y ′ ∧ y ′ ≤ 3).
    The restriction operator allows us to compare bit-vector formulas with inte-
ger arithmetic formulas by restricting integer-valued assignments to the domain
induced by bit-vector values. Building on this notion, we now formalize what
it means for a syntactic translation between bit-vector and integer arithmetic
formulas to preserve semantics. Intuitively, an integer arithmetic formula is con-
sidered semantics-preserving with respect to a bit-vector formula if the two for-
mulas agree on this restricted domain. Note that the integer arithmetic formula
may admit additional satisfying assignments outside this domain.
Definition 7 (Theory Transformers). A theory transformer from TB to TI
is a translation function τB⇝I that translates every formula φ ∈ QF_BV with free
variables x̄ into a QF_IA formula τB⇝I (φ) with free variables x̄′ such that:
                         JφKMB = δI⇝B
                                    x̄
                                         JτB⇝I (φ)KMI ↾B
                                                         
                                                                              (2)
   Similarly, a theory transformer from TI to TB is a translation function τI⇝B
that translates every formula φ′ ∈ QF_IA with free variables x̄′ into a QF_BV
formula τI⇝B (φ′ ) with free variables x̄ such that:
                        JτI⇝B (φ′ )KMB = δI⇝Bx̄
                                                 Jφ′ KMI ↾B
                                                            
                                                                             (3)
Example 4. Following Example 2, the ΣI -formula x′ < y ′ preserves the semantics
of the ΣB -formula x <Bu y in the sense of Eqs. 2 and 3. Notably, Jx′ < y ′ KMI is
infinite, whereas Jx <Bu yKMB is finite. The two formulas coincide on the restricted
bit-vector domain up to the domain transformer.
10     O. Rappoport et al.

4     Theory-Modular Encoding of Bit-Precise CHCs

Throughout this section and the next, we fix the following setup. Let Π be a
set of CHCs over the signature ΣB ∪ P U , where P U is a set of uninterpreted
                                                         x
predicate symbols. For each bit-vector variable x, let δB⇝I be a corresponding
domain transformer. Finally, let τB⇝I be a theory transformer from TB to TI , and
let τI⇝B be a theory transformer from TI to TB .


4.1   The Encoding

We now introduce our theory-modular encoding of Π. The encoding is defined
with respect to a partition of Π into two fragments. The first fragment, the
bit-vector fragment, consists of CHCs reasoned about with respect to TB . These
CHCs are left unchanged, except that each uninterpreted predicate p is replaced
by a fresh copy pB . The second fragment, the integer fragment, consists of CHCs
reasoned about with respect to TI . These CHCs are translated into integer arith-
metic formulas using the theory transformer τB⇝I . Concretely, the constraint of
each CHC is translated into a ΣI -formula via τB⇝I , each uninterpreted predicate
p is replaced by a fresh copy pI , and variables are consistently renamed according
to the variable mapping. In addition, the (syntactic) domain restriction opera-
tor is applied to every variable not occurring in a predicate application in the
body, thereby eliminating integer derivations outside the bit-vector domain. The
encoding also introduces interface constraints, which preserve the original depen-
dencies among uninterpreted predicates by relating their copies. The complete
encoding is formalized in the following definition.

Definition 8 (Theory-Modular Encoding). Let ∆B ⊆ Π and ∆I = Π \ ∆B .
The theory-modular encoding of Π induced by (∆B , ∆I ) is a triple ΠB|I =
(ΠB , ΠI , Θ) defined as follows:

 – ΠB , the bit-vector fragment, is the set of CHCs over the signature ΣB ∪ PBU ,
   where PBU = { pB | p ∈ P U }, obtained from ∆B by replacing each uninter-
   preted predicate p ∈ P U with pB .
 – ΠI , the integer fragment, is the set of CHCs over the signature ΣI ∪ PIU ,
   where PIU = { pI | pV ∈ P U }, obtained
                                          from ∆I by transforming each CHC of
   the form ∀x̄. ϕ ∧ j pj (x̄pj ) → h(x̄h ) into
                                    ^                    ^
                ∀x̄′ . τB⇝I (ϕ) ∧       pIj (x̄′pj ) ∧          x′↾B       → hI (x̄′h )
                                                                       
                                    j                    x∈ȳ
                   S
   where ȳ = x̄ \ ( j x̄pj ). If the head is ⊥, it remains unchanged.
 – Θ, the set of interface constraints, is ΘB⇝I ∪ ΘI⇝B , where
    • ΘB⇝I consists of all pairs pB ⇝ pI such that pB is the head predicate of
       some CHC in ΠB and pI occurs in the body of some CHC in ΠI .
    • ΘI⇝B consists of all pairs pI ⇝ pB such that pI is the head predicate of
       some CHC in ΠI and pB occurs in the body of some CHC in ΠB .
               Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning               11

    Note that the partition (∆B , ∆I ) can be chosen arbitrarily, i.e., each CHC
in Π may be assigned to either the bit-vector or the integer fragment. While
different partitioning heuristics may affect performance, all resulting encodings
preserve the semantics of Π (see the following subsection). The partitioning
heuristic used in our implementation is discussed in Section 6.
Example 5. Fig. 1(b) shows a CHC set Π, and Fig. 1(c) shows a theory-modular
encoding of Π in which the query is placed in the bit-vector fragment and all
other CHCs are placed in the integer fragment. The interface constraint q I ⇝ q B
preserves the original dependencies in Π.

4.2   Semantics and Correctness
For clarity, some of the forthcoming definitions reuse notation from the single-
theory case (Section 2.2). Let ΠB|I = (ΠB , ΠI , Θ) be a theory-modular en-
coding of Π. The satisfiability of ΠB|I is defined with respect to both TB and
TI , where each fragment is interpreted in its corresponding theory. We denote
ΣB|I = (ΣB , ΣI ), TB|I = (TB , TI ), and MB|I = (MB , MI ).
     We begin by defining the semantics of the uninterpreted predicates in ΠB|I .
As in the single-theory case, the bounded semantics of a predicate consists of all
tuples derivable through a bounded derivation. In the theory-modular setting,
however, this semantics decomposes into two components: a local component,
denoted → (Eq. 4), which unfolds the definition of the predicate using CHCs
from its own fragment, and an external component, denoted ⇝ (Eq. 5), which
derives tuples from the corresponding predicate copy in the other fragment,
as dictated by the interface constraints. Importantly, the domain restrictions
introduced by the encoding in the integer fragment (see Definition 8) ensure
that only tuples relevant to Π, namely those representing bit-vector tuples, can
be derived in ΠI . The bounded semantics is defined inductively on the bound.
Definition 9 (Bounded Semantics). Let p⋄ ∈ PBU ∪ PIU be an uninterpreted
predicate with ⋄ ∈ {B, I}, and let n ∈ N be a bound. The bounded semantics of
                                                  M                         M
p⋄ with respect to MB|I at bound n, denoted Jp⋄ Kn B|I , is defined as Jp⋄ Kn B|I =
      M                M
(Jp⋄ Kn B|I )→ ∪ (Jp⋄ Kn B|I )⇝ such that:
               M                  [                                        ∗
        (Jp⋄ Kn B|I )→ =                             J∃(x̄ \ x̄p⋄ ). B[x̄]KM⋄              (4)
                        (∀x̄. B[x̄]→p⋄ (x̄p⋄ ))∈Π⋄
                                        
                                        M⋄ {q ⋄ 7→ ∅}q⋄ ∈P⋄U                   if n = 0
                       where M∗⋄ =
                                                                M
                                            M⋄ {q ⋄ 7→ Jq ⋄ Kn−1
                                                               B|I
                                                                   }q⋄ ∈P⋄U     if n > 0
                                        

                             
               M
                             ∅                        if n = 0 or p♦ ⇝ p⋄ ∈
                                                                           / Θ♦⇝⋄
          (Jp⋄ Kn B|I )⇝ =                                                                 (5)
                              p        MB|I 
                              δ♦⇝⋄ Jp♦ Kn−1            if n > 0 and p♦ ⇝ p⋄ ∈ Θ♦⇝⋄
                       where ♦ ∈ {B, I} \ {⋄}
12      O. Rappoport et al.

Example 6. Consider the theory-modular encoding in Fig. 1, where all variables
                                            M
have sort BV[2]. Then (1, 0, 0) ∈ (JpI K0 B|I )→ (first CHC in ΠI ), (1, 1, −1) ∈
      M                                              M
(JpI K1 B|I )→ (second CHC in ΠI ), (1, −1) ∈ (Jq I K2 B|I )→ (third CHC in ΠI ), and
                  M
(01, 11) ∈ (Jq B K3 B|I )⇝ (interface constraint).
                                           p
   Recall the inverse domain transformer δI⇝B  is applied only to integer tuples in
              p
the image of δB⇝I , namely those corresponding to bit-vector tuples. The following
                                        p
lemma states that the application of δI⇝B  in Eq. 5 is well-defined.

Lemma 2. Let p ∈ P U be an uninterpreted predicate that occurs in Π and let
                             M        p
                                          DM
                                               
n ∈ N be a bound. Then, JpI Kn B|I ⊆ δB⇝I  p
                                             B
                                                 .

Proof. By induction on the bound. See Appendix A.
                                                                       M           M
    The bounded semantics are monotonic, i.e., for all n ∈ N, Jp⋄ Kn B|I ⊆ Jp⋄ Kn+1 B|I
                                                                                        .
Taking the union over all bounds yields the (unbounded) semantics of p⋄ . The
                                                                  M
local semantics of p⋄ , denoted (Jp⋄ KMB|I )→ , is n∈N (Jp⋄ Kn B|I )→ . Similarly, the
                                                      S
                                                                    M
external semantics of p⋄ , denoted (Jp⋄ KMB|I )⇝ , is n∈N (Jp⋄ Kn B|I )⇝ . The seman-
                                                        S
tics of p⋄ , denoted Jp⋄ KMB|I , is (Jp⋄ KMB|I )→ ∪ (Jp⋄ KMB|I )⇝ .
    The satisfiability of a theory-modular encoding is defined in terms of the
semantics of its uninterpreted predicates.

Definition 10 (Satisfiability). A theory-modular encoding ΠB|I is satisfiable
modulo TB|I if, for each ⋄ ∈ {B, I} and every query π ∈ Π⋄ , it holds that
M⋄ {p⋄ 7→ Jp⋄ KMB|I }p⋄ ∈P⋄U |= π.

    A key property of a theory-modular encoding is that it preserves the seman-
tics of the uninterpreted predicates of the original set of CHCs. In particular,
the semantics of each uninterpreted predicate p occurring in Π coincides with
the union of the semantics of its copies in the encoding, where the semantics
obtained in the integer fragment are transformed back to the bit-vector domain
via the inverse domain transformer. Intuitively, the encoding preserves derivabil-
ity, up to the domain transformers, at the level of the tuples produced for each
predicate. This is formalized in Lemma 3, which in turn implies Theorem 1.

Lemma 3. Let p ∈ P U be an uninterpreted predicate that occurs in Π. Then,
                                         p
                  JpKMB = JpB KMB|I ∪ δI⇝B   JpI KMB|I
                                                       


Theorem 1. Π is satisfiable modulo TB iff ΠB|I is satisfiable modulo TB|I .

Proof. See Appendix A.

    As in the single-theory setting, our algorithm for checking the satisfiability
of a theory-modular encoding (Section 5) searches for symbolic interpretations
of uninterpreted predicates that over-approximate their semantics while remain-
ing strong enough to satisfy the queries. A ΣB|I -interpretation is a pair IB|I =
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning             13

(IB , II ), where IB is a ΣB -interpretation for ΠB and II is a ΣI -interpretation for
ΠI . Specifically, IB assigns to each uninterpreted predicate symbol pB ∈ PBU of
type BV[n1 ] × · · · × BV[nm ] a ΣB -formula whose free variables are in the tuple
ȳpB = (y1 , . . . , ym ), where each yi has sort BV[ni ]. Analogously, II assigns to each
pI ∈ PIU a ΣI -formula with free variables in the tuple ȳpI = ȳp′ B , all of sort Int.

Definition 11 (Solution). A ΣB|I -interpretation IB|I satisfies ΠB|I modulo TB|I ,
denoted IB|I |=TB|I ΠB|I , if the following conditions hold:

 – Local Satisfaction: For each ⋄ ∈ {B, I} and every CHC π ∈ Π⋄ , the Σ⋄ -
   formula I⋄ (π) is valid modulo T⋄ .
 – Interface Constraint Satisfaction:
     • For every interface constraint pB ⇝ pI ∈ ΘB⇝I , the ΣB -formula
                                                           
         IB|I (pB ⇝ pI ) = ∀ȳpB . IB (pB ) → τI⇝B II (pI ) is valid modulo TB .

      • For every interface constraint pI ⇝ pB ∈ ΘI⇝B , the ΣB -formula
                                                 
          IB|I (pI ⇝ pB ) = ∀ȳpB . τI⇝B II (pI ) → IB (pB ) is valid modulo TB .

In this case, IB|I is called a ΣB|I -solution for ΠB|I .

     Intuitively, local satisfaction ensures that each fragment interpretation sat-
isfies the CHCs of its own fragment in the corresponding theory, while interface
constraint satisfaction enforces consistency between the fragments. For every in-
terface constraint θ ∈ Θ, the formula IB|I (θ) requires that, within the restricted
bit-vector domain, the interpretation of the target predicate includes all tuples
corresponding to those admitted by the interpretation of the source predicate.
Notably, the interpretation of the integer copy of the predicate is allowed to
admit additional tuples outside the restricted domain, and such tuples are dis-
carded when τI⇝B is applied.
     A ΣB|I -solution provides an over-approximation of the semantics of the un-
interpreted predicates. This property is established in Lemma 4.

Lemma 4. Let IB|I be a ΣB|I -solution for ΠB|I , and let p⋄ ∈ PBU ∪ PIU be an
uninterpreted predicate with ⋄ ∈ {B, I}. Then, Jp⋄ KMB|I ⊆ JI⋄ (p⋄ )KM⋄ .

    From Lemma 4, it follows that the existence of a ΣB|I -solution implies the
satisfiability of the theory-modular encoding, as stated formally in Theorem 2.

Theorem 2. If ΠB|I admits a ΣB|I -solution, then ΠB|I is satisfiable modulo TB|I .

   The following theorem establishes a correspondence between solutions of the
encoding and solutions of the original CHCs.

Theorem 3. Π admits a ΣB -solution if and only if ΠB|I admits a ΣB|I -solution.

Proof. See Appendix A.
14      O. Rappoport et al.

Decidability. The encoding does not compromise the decidability of CHC-SAT
modulo TB . Intuitively, although the encoding introduces an integer component,
all tuples that contribute to the semantics of the predicates correspond to values
in the original finite bit-vector domain. Thus, the encoding does not introduce
additional sources of infiniteness that affect decidability.


5    Algorithm

This section presents MosaicSolve, a symbolic procedure for deciding the sat-
isfiability of theory-modular encodings. The procedure relies on two CHC sat-
isfiability oracles: one for the bit-vector fragment modulo TB and one for the
integer fragment modulo TI . At a high level, MosaicSolve generates queries
over a single theory and delegates them to the corresponding oracles, while co-
ordinating the exchange of information between fragments. This coordination is
achieved by propagating constraints soundly across interface constraints using
theory transformers, and by maintaining both under- and over-approximations
of the external semantics of uninterpreted predicates. The under-approximations
are used to search for counterexamples to satisfiability, i.e., derivations leading
to a query violation, while the over-approximations are used to block infeasible
counterexamples and detect convergence.
     The procedure is defined as a transition system with states specified below
and transitions given by the inference rules in Fig. 2. The input to MosaicSolve
is a theory-modular encoding ΠB|I = (ΠB , ΠI , Θ). For convenience, we assume
that ΠB|I contains no query and that a query πq is provided separately. Without     
loss of generality, πq is a ΣB -formula of the form ∀ȳqB . ϕq [ȳqB ] ∧ q B (ȳqB ) → ⊥.
The goal of MosaicSolve is to decide whether (ΠB ∪ {πq }, ΠI , Θ) is satisfiable.
     A state of MosaicSolve is a triple Q ∥ ∆u ∥ ∆o , where Q is a finite set
of proof obligations, ∆u is a set of under-approximation lemmas, and ∆o is a
set of over-approximation lemmas. Each proof obligation has the form ⟨ p⋄ , ϕ ⟩,
where ⋄ ∈ {B, I}, p⋄ ∈ P⋄U is an uninterpreted predicate in the fragment Π⋄ , and
ϕ is a quantifier-free Σ⋄ -formula. A proof obligation ⟨ p⋄ , ϕ ⟩ is generated when
MosaicSolve aims to determine whether the semantics of p⋄ contains a tuple
satisfying ϕ. Intuitively, ϕ characterizes a set of bad tuples, whose presence in the
semantics of p⋄ may witness a counterexample to satisfiability. The sets ∆u and
∆o associate, with each predicate p⋄ that is the target of an interface constraint
p♦ ⇝ p⋄ ∈ Θ (where ⋄ ̸= ♦), a set of learned lemmas. Intuitively, if ⟨ p⋄ , ψ ⟩ is
stored in ∆u (resp. ∆o ), then ψ under- (resp. over-) approximates (Jp⋄ KMB|I )⇝ ,
i.e., the set of tuples derivable for p⋄ via its corresponding predicate copy p♦ in
the other fragment (see Definition 9).
     The procedure MosaicSolve is initialized with a single proof obligation cor-
responding to the input query πq , and with empty lemma sets (rule Init). The
rules NegAnswer, PosAnswer, and Query are then applied repeatedly. Rules
NegAnswer and PosAnswer are applied when a proof obligation in Q can
be resolved using the current over- and under-approximation lemmas in ∆o and
∆u , respectively. Otherwise, if the current approximations are insufficient, rule
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                            15


                                     Init
                                               { ⟨ q B , ϕq ⟩ } ∥ ∅ ∥ ∅

                       Q ∥ ∆u ∥ ∆ o           ⟨ p⋄ , ϕ ⟩ ∈ Q \ { ⟨ q B , ϕq ⟩ }    ⋄ ̸= ♦ ∈ {B, I}
                                              I⋄ |=T⋄ Π⋄o ∪ query(p⋄ , ϕ)
       NegAnswer
                               Q \ {⟨ p⋄ , ϕ ⟩} ∥ ∆u ∥ ∆o ∪ { ⟨ p♦ , τ⋄⇝♦ (I⋄ (p⋄ )) ⟩ }

                       Q ∥ ∆u ∥ ∆ o    ⟨ p⋄ , ϕ ⟩ ∈ Q \ { ⟨ q B , ϕq ⟩ } ⋄ ̸= ♦ ∈ {B, I}
                              Π⋄u ∪ query(p⋄ , ϕ) ⊢T⋄ ⊥ with refutation R
                                        ⟨ p⋄ , ψ ⟩ = child(root(R))
       PosAnswer
                                 Q \ {⟨ p⋄ , ϕ ⟩} ∥ ∆u ∪ { ⟨ p♦ , τ⋄⇝♦ (ψ) ⟩ } ∥ ∆o

                            Q ∥ ∆u ∥ ∆ o        ⟨ p⋄ , ϕ ⟩ ∈ Q     ⋄ ̸= ♦ ∈ {B, I}
                                                      u          ⋄
                                        I⋄ |=T⋄ Π    ⋄ ∪ query(p , ϕ)
                             Π⋄o ∪ query(p⋄ , ϕ) ⊢T⋄ ⊥ with refutation R
                                                   

                               ⟨ r⋄ , ψ ⟩ ∈ leaves(R)        r♦ ⇝ r⋄ ∈ Θ♦⇝⋄
                   Query
                                     Q ∪ {⟨ r♦ , τ⋄⇝♦ (ψ) ⟩} ∥ ∆u ∥ ∆o

                  { ⟨ q B , ϕ q ⟩ } ∥ ∆u ∥ ∆ o                      { ⟨ q B , ϕq ⟩ } ∥ ∆u ∥ ∆o
               IB |=TB ΠBo ∪ query(q B , ϕq )                       ΠBu ∪ query(q B , ϕq ) ⊢TB ⊥
         Sat                                             Unsat
                            SAT                                              UNSAT
                           [                       ^
      Π⋄o = Π⋄ ∪                                         ψ[ȳs⋄ ] ∧ restrict⋄ (ȳs⋄ ) → s⋄ (ȳs⋄ )
                                                                                    
                                         ∀ȳs⋄ .
                     s♦ ⇝s⋄ ∈Θ♦⇝⋄             ⟨ s⋄ ,ψ ⟩∈∆o
                           [                        _
      Π⋄u                                                ψ[ȳs⋄ ] ∧ restrict⋄ (ȳs⋄ ) → s⋄ (ȳs⋄ )
                                                                                    
            = Π⋄ ∪                       ∀ȳs⋄ .
                     s♦ ⇝s⋄ ∈Θ♦⇝⋄              ⟨ s⋄ ,ψ ⟩∈∆u
               ⋄
      query(p , ϕ) = ∀ȳp⋄ . ϕ[ȳp⋄ ] ∧ p⋄ (ȳp⋄ ) ∧ restrict⋄ (ȳp⋄ ) → ⊥
                                                                     
                       (V
                                   ′
                          y ′ ∈ȳ y ↾B if ⋄ = I
      restrict⋄ (ȳ) =
                        ⊤              if ⋄ = B

                       Fig. 2. Inference rules defining MosaicSolve.

Query is applied to generate a new proof obligation in the other fragment. When
the initial proof obligation is resolved using ∆o or ∆u , MosaicSolve terminates
with SAT or UNSAT, respectively (rules Sat and Unsat). We explain the rules
NegAnswer, PosAnswer, and Query below.
NegAnswer discharges a proof obligation ⟨ p⋄ , ϕ ⟩ ∈ Q, other than the initial
one, if it can be answered negatively using the current over-approximation. To
establish this, the CHC satisfiability oracle for T⋄ is invoked Π⋄o ∪ query(p⋄ , ϕ)
(defined at the bottom of Fig. 2). Here, Π⋄o extends Π⋄ with facts that encode,
for each predicate that is the target of an interface constraint, the current over-
approximation of its external semantics by conjoining the corresponding lemmas
in ∆o . The query query(p⋄ , ϕ) asserts that the semantics of p⋄ is disjoint from
the set of tuples satisfying ϕ. If ⋄ = I, syntactic domain restrictions are applied
to ensure that all derivations correspond to the bit-vector domain. If the above
CHC set is satisfiable, the oracle returns a Σ⋄ -solution I⋄ such that I⋄ (p⋄ ) over-
16      O. Rappoport et al.

approximates Jp⋄ KMB|I and |=T⋄ I⋄ (p⋄ ) → ¬ϕ. Consequently, the proof obligation
is discharged and removed from Q. Furthermore, the over-approximation of the
corresponding predicate p♦ in the other fragment is strengthened with a new
lemma obtained by translating I⋄ (p⋄ ) via the appropriate theory transformer.

PosAnswer discharges a proof obligation ⟨ p⋄ , ϕ ⟩ ∈ Q, other than the initial
one, if it can be answered positively using the current under-approximation. To
establish this, the CHC satisfiability oracle for T⋄ is invoked on Π⋄u ∪query(p⋄ , ϕ),
which is constructed as in rule NegAnswer, except that the lemmas in ∆u are
used instead of those in ∆o and are combined disjunctively. If the above CHC
set is unsatisfiable, the oracle returns a refutation R, i.e., a derivation of ⊥. The
child of the root ⊥ in R is a pair ⟨p⋄ , ψ⟩, where ψ is a Σ⋄ -formula that under-
approximates Jp⋄ KMB|I and satisfies ̸|=T⋄ ψ → ¬ϕ. Consequently, the proof obli-
gation is discharged and removed from Q. Furthermore, the under-approximation
of the corresponding predicate p♦ in the other fragment is extended with a new
lemma obtained by translating ψ via the appropriate theory transformer.

Query generates a new proof obligation when an existing proof obligation
⟨ p⋄ , ϕ ⟩ ∈ Q cannot be resolved using the current approximations. In this case,
Π⋄u ∪ query(p⋄ , ϕ) is satisfiable, whereas Π⋄o ∪ query(p⋄ , ϕ) is unsatisfiable. Thus,
the current under-approximation does not witness a counterexample to the proof
obligation, while the current over-approximation does. The CHC satisfiability or-
acle for T⋄ returns a refutation R for Π⋄o ∪query(p⋄ , ϕ). Since R is obtained using
the over-approximation in ∆o , it is not yet clear whether it corresponds to a feasi-
ble derivation of the original encoding ΠB|I . Therefore, a leaf ⟨r⋄ , ψ⟩ of R derived
from a fact contributed by ∆o is selected. Such a leaf must exist, since otherwise
all leaves would be derived from facts in Π⋄ , implying that Π⋄u ∪ query(p⋄ , ϕ)
is unsatisfiable. To determine whether there exists a tuple in (Jr⋄ KMB|I )⇝ that
satisfies ψ, a proof obligation is generated for the corresponding predicate r♦ in
the other fragment by translating ψ via the appropriate theory transformer.

Theorem 4 (Soundness). Let ΠB|I = (ΠB , ΠI , Θ) be a theory-modular en-
coding and πq a ΣB -query. If MosaicSolve returns SAT (resp. UNSAT), then
(ΠB ∪ {πq }, ΠI , Θ) is satisfiable (resp. unsatisfiable).

Proof. By induction on the length of the transition sequence. See Appendix A.

Termination. The presentation of MosaicSolve omits several refinements that
ensure termination. First, when applying rule Query, let ⟨r⋄ , ψ⟩ be the selected
leaf, which induces a new proof obligation. The following two conditions must
hold: (i) the new proof obligation does not overlap with any existing proof obli-
gation, and (ii) no tuple in the current under-approximation of r⋄ satisfies ψ.
These conditions can be checked by examining the existing proof obligations in
Q corresponding to r♦ and the under-approximation lemmas in ∆u correspond-
ing to r⋄ . Second, the procedure follows an iterative deepening strategy, similar
to that of [11], which bounds the exploration of derivations and ensures that all
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning          17

relevant obligations are eventually considered. Under these refinements, and as-
suming each invocation of the underlying CHC satisfiability oracles terminates,
MosaicSolve is guaranteed to terminate.

6    Implementation Details and Experimental Results
This section describes the implementation of the Mosaic framework and its eval-
uation. We present the theory transformers used in our implementation, the
strategy for partitioning a CHC set into theory fragments, and an optimization
applied during the encoding. Our prototype is implemented using Z3 [12] and
Spacer [11], where Spacer serves as the CHC-SAT oracle for both TB and TI .

Theory Transformers. Recall that translations are defined with respect to
domain transformers (Definition 5), which map elements in the domain of each
bit-vector variable to elements in the domain of its corresponding integer vari-
able. Two natural choices are signed and unsigned semantics. In programming
languages, signedness is typically part of a variable’s type (e.g., int vs. unsigned
int in C). In contrast, in ΣB , the sort of a variable depends only on its bit-width,
while signedness is reflected in certain predicates and functions (e.g., <Bu vs. <Bs ).
Consequently, the same variable may appear in both signed and unsigned con-
texts. We adopt the following strategy. For each bit-vector variable, if it occurs
more frequently in unsigned than signed predicate or function applications in Π,
we use the unsigned domain transformer. Otherwise, we use the signed one.
    We now describe the formula transformers τB⇝I and τI⇝B (Definition 7). For
τB⇝I , we use the translation of Zohar et al. [19], which maps QF_BV formulas to
QF_IA formulas and satisfies Eq. 2. Since the translation in [19] assumes unsigned
semantics, we extend it to signed semantics by adjusting domain restrictions and
inserting the appropriate signed-unsigned conversions.
    For τI⇝B , we define a custom transformer based on syntactic substitution.
Arithmetic operators are mapped to their bit-vector counterparts (e.g., + 7→ +B ),
predicates to signed bit-vector predicates (e.g., <7→<Bs ), variables according to
the variable mapping, and each integer constant c to a bit-vector constant whose
signed value is c. However, this substitution alone does not satisfy Eq. 3. For
example, consider the ΣI -formula φ′ = x′ < y ′ + 1, where the corresponding bit-
vector variables x, y have sort BV[2] and use the signed domain transformer. The
syntactic translation yields φ = x <Bs (y +B 01). The assignment x′ 7→ 1, y ′ 7→ 1
satisfies φ′ , but the corresponding assignment x 7→ 01, y 7→ 01 does not satisfy
φ, since 01 +B 01 = 10, whose signed value is −2. This mismatch is caused by
overflow: bit-vector arithmetic is modular and operations may wrap around. To
avoid this, and to obtain a ΣB -formula that agrees with the original ΣI -formula
on the restricted bit-vector domain, we extend variables and constants with extra
bits using sign extension, choosing the minimal width for which no arithmetic
term can overflow. In this example, one extra bit suffices.

Encoding. Given a CHC set Π over ΣB , the partitioning strategy Mosaic ap-
plies (Definition 8) is simple: CHCs whose function applications consist only of
18      O. Rappoport et al.

arithmetic operations (+B , −B , ·B , divBu , modBu ) are placed in the integer frag-
ment, while all other CHCs remain in the bit-vector fragment. The intuition is
that arithmetic constraints are often easier to reason about in TI than in TB ,
whereas bit-precise operations are better handled in TB , since translating them
to TI produces complex terms involving many div and mod operations.
    We apply an additional encoding optimization. The transformer τB⇝I pre-
serves bit-vector modular semantics by introducing modular arithmetic into the
translated integer formulas (e.g., x+B y is translated to (x′ +y ′ ) mod 2n , where n
is the width of x and y). However, for CHCs placed in ΠI , if a term is guaranteed
not to overflow, the modulo operation can be safely omitted. For instance, in the
CHCs of Fig. 1(b), which encode the program in Fig. 1(a), overflow is impossible
along every execution.8 Accordingly, the terms a +B 1 and b −B 1 are translated
simply as a′ + 1 and b′ − 1, without the modulo operation.

Experimental Evaluation. For
                                                             BV         IA         BV+IA
the evaluation, we collected 11 small                      W Time [s] W Time [s] W Time [s]
realistic programs (see Appendix B)         abs-ge         7  693.80 31    0.21 63      0.18
and encoded them as CHCs mod-               abs-sum        6  631.82  3   37.23  6    246.41
ulo TB . These programs use bit-wise        cond-neg       7   76.17  8  506.52 63      0.47
                                            cond-neg-diff  6 1308.05  4 2723.50  8    639.80
operations to implement functions           max-inv        7 5122.19  4    0.05  8   6188.19
such as max and abs for efficiency          opp-signs      9 4358.99  3   13.01 62      0.09
             9                              opp-signs-diff 6  533.03  3  330.25  6    548.96
and security . Experiments were con-        swap           7 2031.24  3   55.68 11 2142.14
ducted on a workstation with AMD            swap-sum       7 2109.57  4  243.96  6    134.21
                                            turn-off-rm    7 1718.30  4  235.95  7    111.17
EPYC 74F3. Every test was given             turn-on-lsb    6  247.10  4  774.95  6    115.98
7200 seconds and 16GB of memory.
Our implementation and the bench- Table 1. Performance of BV, IA, and
marks are publicly available.10         BV+IA. Maximal bit-width (W) and run-
    We evaluate three configurations time. Bold indicates the largest W.
of Mosaic that differ in the partition-
ing strategy: (i) BV, where all CHCs are placed in the bit-vector fragment (equiv-
alent to running Spacer modulo TB ); (ii) IA, where all CHCs are translated to
TI and placed in the integer fragment (equivalent to running Spacer modulo TI
on the translated set); and (iii) BV+IA, our theory-modular approach. For each
configuration, we report the maximal bit-width solved within the timeout and
the runtime at that width (Table 1). Overall, BV+IA achieves the largest bit-
width on most benchmarks, often by a wide margin. In several cases, it scales to
large bit-widths (up to 63), while BV and IA time out at much smaller widths.
When the maximal bit-width is the same, BV+IA typically improves runtime,
sometimes by orders of magnitude. The IA configuration is generally less effec-
tive, despite the arithmetic structure of the benchmarks, due to the translation
of bit-wise operations into complex arithmetic terms involving many div and
mod operations. In contrast, BV often fails to scale to larger bit-widths. Note
8
   This holds for all benchmarks used in our evaluation.
9
   https://graphics.stanford.edu/~seander/bithacks.html
10
   https://doi.org/10.5281/zenodo.21790677
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning          19

that Z3 reports an internal error beyond bit-width 64, limiting the evaluation
range.


7   Conclusion

We presented Mosaic, a theory-modular framework for deciding satisfiability of
CHCs modulo TB . It reduces CHCs into two fragments interpreted over TB and TI ,
connected by interface constraints. We introduced a procedure for determining
satisfiability of such encodings and implemented a prototype. Our evaluation
shows that the approach can significantly outperform state-of-the-art solvers.


References

 1. Barrett, C., Stump, A., Tinelli, C., et al.: The smt-lib standard: Version 2.0. In:
    Proceedings of the 8th international workshop on satisfiability modulo theories
    (Edinburgh, UK). vol. 13, p. 14 (2010)
 2. Barth, M., Heizmann, M.: A bit-vector to integer translation with bv2nat and
    nat2bv. In: Reger, G., Zohar, Y. (eds.) Proceedings of the 22nd International
    Workshop on Satisfiability Modulo Theories co-located with the 36th International
    Conference on Computer Aided Verification (CAV 2024), Montreal, Canada, July,
    22-23, 2024. CEUR Workshop Proceedings, vol. 3725, pp. 53–63. CEUR-WS.org
    (2024), https://ceur-ws.org/Vol-3725/short9.pdf
 3. Bjørner, N.S., Gurfinkel, A., McMillan, K.L., Rybalchenko, A.: Horn clause
    solvers for program verification. In: Beklemishev, L.D., Blass, A., Dershowitz, N.,
    Finkbeiner, B., Schulte, W. (eds.) Fields of Logic and Computation II - Essays
    Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday. Lecture Notes
    in Computer Science, vol. 9300, pp. 24–51. Springer (2015). https://doi.org/10.
    1007/978-3-319-23534-9_2, https://doi.org/10.1007/978-3-319-23534-9_2
 4. Bjørner, N.S., McMillan, K.L., Rybalchenko, A.: On solving universally quanti-
    fied Horn clauses. In: Logozzo, F., Fähndrich, M. (eds.) Static Analysis - 20th
    International Symposium, SAS 2013, Seattle, WA, USA, June 20-22, 2013. Pro-
    ceedings. Lecture Notes in Computer Science, vol. 7935, pp. 105–125. Springer
    (2013). https://doi.org/10.1007/978-3-642-38856-9_8, https://doi.org/10.1007/
    978-3-642-38856-9_8
 5. Fan, G., Chen, L., Yin, B., Zhang, W., Yao, P., Wang, J.: Program analysis com-
    bining generalized bit-level and word-level abstractions. Proc. ACM Softw. Eng.
    2(ISSTA) (Jun 2025). https://doi.org/10.1145/3728905, https://doi.org/10.1145/
    3728905
 6. Goguen, J.A., Burstall, R.M.: Introducing institutions. In: Clarke, E.M., Kozen, D.
    (eds.) Logics of Programs, Workshop, Carnegie Mellon University, Pittsburgh, PA,
    USA, June 6-8, 1983, Proceedings. Lecture Notes in Computer Science, vol. 164,
    pp. 221–256. Springer (1983). https://doi.org/10.1007/3-540-12896-4_366, https:
    //doi.org/10.1007/3-540-12896-4_366
 7. Goguen, J.A., Burstall, R.M.: Institutions: Abstract model theory for specification
    and programming. J. ACM 39(1), 95–146 (1992). https://doi.org/10.1145/147508.
    147524, https://doi.org/10.1145/147508.147524
20      O. Rappoport et al.

 8. Gurfinkel, A., Belov, A., Marques-Silva, J.: Synthesizing safe bit-precise invari-
    ants. In: Ábrahám, E., Havelund, K. (eds.) Tools and Algorithms for the Con-
    struction and Analysis of Systems - 20th International Conference, TACAS 2014,
    Held as Part of the European Joint Conferences on Theory and Practice of Soft-
    ware, ETAPS 2014, Grenoble, France, April 5-13, 2014. Proceedings. Lecture Notes
    in Computer Science, vol. 8413, pp. 93–108. Springer (2014). https://doi.org/10.
    1007/978-3-642-54862-8_7, https://doi.org/10.1007/978-3-642-54862-8_7
 9. Itzhaky, S., Shoham, S., Vizel, Y.: Hyperproperty verification as CHC satisfia-
    bility. In: Weirich, S. (ed.) Programming Languages and Systems - 33rd Euro-
    pean Symposium on Programming, ESOP 2024, Held as Part of the European
    Joint Conferences on Theory and Practice of Software, ETAPS 2024, Luxembourg
    City, Luxembourg, April 6-11, 2024, Proceedings, Part II. Lecture Notes in Com-
    puter Science, vol. 14577, pp. 212–241. Springer (2024). https://doi.org/10.1007/
    978-3-031-57267-8_9, https://doi.org/10.1007/978-3-031-57267-8_9
10. Jovanovic, D., Barrett, C.W.: Polite theories revisited. In: Fermüller, C.G.,
    Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence, and Reason-
    ing - 17th International Conference, LPAR-17, Yogyakarta, Indonesia, October 10-
    15, 2010. Proceedings. pp. 402–416. Lecture Notes in Computer Science, Springer
    (2010). https://doi.org/10.1007/978-3-642-16242-8_29, https://doi.org/10.1007/
    978-3-642-16242-8_29
11. Komuravelli, A., Gurfinkel, A., Chaki, S.: Smt-based model checking for recursive
    programs. Formal Methods Syst. Des. 48(3), 175–205 (2016). https://doi.org/10.
    1007/S10703-016-0249-4, https://doi.org/10.1007/s10703-016-0249-4
12. de Moura, L.M., Bjørner, N.S.: Z3: an efficient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems, 14th International Conference, TACAS 2008, Held as Part of the
    Joint European Conferences on Theory and Practice of Software, ETAPS 2008,
    Budapest, Hungary, March 29-April 6, 2008. Proceedings. Lecture Notes in Com-
    puter Science, vol. 4963, pp. 337–340. Springer (2008). https://doi.org/10.1007/
    978-3-540-78800-3_24, https://doi.org/10.1007/978-3-540-78800-3_24
13. Nelson, G., Oppen, D.C.: Simplification by cooperating decision procedures.
    ACM Trans. Program. Lang. Syst. 1(2), 245–257 (1979). https://doi.org/10.1145/
    357073.357079, https://doi.org/10.1145/357073.357079
14. Okudono, T., King, A.: Mind the gap: Bit-vector interpolation recast over linear in-
    teger arithmetic. In: Biere, A., Parker, D. (eds.) Tools and Algorithms for the Con-
    struction and Analysis of Systems - 26th International Conference, TACAS 2020,
    Held as Part of the European Joint Conferences on Theory and Practice of Soft-
    ware, ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings, Part I. Lecture
    Notes in Computer Science, vol. 12078, pp. 79–96. Springer (2020). https://doi.org/
    10.1007/978-3-030-45190-5_5, https://doi.org/10.1007/978-3-030-45190-5_5
15. Ranise, S., Ringeissen, C., Zarba, C.G.: Combining data structures with nonsta-
    bly infinite theories using many-sorted logic. In: Gramlich, B. (ed.) Frontiers of
    Combining Systems, 5th International Workshop, FroCoS 2005, Vienna, Austria,
    September 19-21, 2005, Proceedings. pp. 48–64. Lecture Notes in Computer Sci-
    ence, Springer (2005). https://doi.org/10.1007/11559306_3, https://doi.org/10.
    1007/11559306_3
16. Rappoport, O., Grumberg, O., Vizel, Y.: Structure-guided solution of constrained
    Horn clauses. In: André, É., Sun, J. (eds.) Automated Technology for Verification
    and Analysis - 21st International Symposium, ATVA 2023, Singapore, October 24-
    27, 2023, Proceedings, Part II. Lecture Notes in Computer Science, vol. 14216, pp.
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning              21

    117–138. Springer (2023). https://doi.org/10.1007/978-3-031-45332-8_6, https://
    doi.org/10.1007/978-3-031-45332-8_6
17. Rothenberg, B., Grumberg, O., Vizel, Y., Singher, E.: Condition synthesis realiz-
    ability via constrained Horn clauses. In: Rozier, K.Y., Chaudhuri, S. (eds.) NASA
    Formal Methods - 15th International Symposium, NFM 2023, Houston, TX, USA,
    May 16-18, 2023, Proceedings. Lecture Notes in Computer Science, vol. 13903, pp.
    380–396. Springer (2023). https://doi.org/10.1007/978-3-031-33170-1_23, https:
    //doi.org/10.1007/978-3-031-33170-1_23
18. Schüssele, F., Bentele, M., Dietsch, D., Heizmann, M., Jiang, X., Klumpp, D.,
    Podelski, A.: Ultimate automizer and the abstraction of bitwise operations - (com-
    petition contribution). In: Finkbeiner, B., Kovács, L. (eds.) Tools and Algorithms
    for the Construction and Analysis of Systems - 30th International Conference,
    TACAS 2024, Held as Part of the European Joint Conferences on Theory and
    Practice of Software, ETAPS 2024, Luxembourg City, Luxembourg, April 6-11,
    2024, Proceedings, Part III. Lecture Notes in Computer Science, vol. 14572, pp.
    418–423. Springer (2024). https://doi.org/10.1007/978-3-031-57256-2_31, https:
    //doi.org/10.1007/978-3-031-57256-2_31
19. Zohar, Y., Irfan, A., Mann, M., Niemetz, A., Nötzli, A., Preiner, M., Reynolds, A.,
    Barrett, C.W., Tinelli, C.: Bit-precise reasoning via int-blasting. In: Finkbeiner, B.,
    Wies, T. (eds.) Verification, Model Checking, and Abstract Interpretation - 23rd
    International Conference, VMCAI 2022, Philadelphia, PA, USA, January 16-18,
    2022, Proceedings. Lecture Notes in Computer Science, vol. 13182, pp. 496–518.
    Springer (2022). https://doi.org/10.1007/978-3-030-94583-1_24, https://doi.org/
    10.1007/978-3-030-94583-1_24
22       O. Rappoport et al.

A      Additional Proofs

Proof of Lemma 2. The claim is proved by induction on the bound. For the
local component, consider a CHC in ΠI with head pI . Any tuple derived us-
ing this CHC assigns to each head variable either (i) a value obtained from an
uninterpreted predicate application in the body, which by the induction hypoth-
esis lies in the image of the corresponding domain transformer, or (ii) a value
satisfying the syntactic domain restriction · ↾B conjoined during the encoding
                                                                       p
(Definition 8). In both cases, the derived tuple lies in the image of δB⇝I . For the
                                                          p
external component, tuples are obtained by applying δB⇝I to tuples derived for
pB , as dictated by the interface constraints. Hence, all externally derived tuples
        p
lie in δB⇝I (DMp ).
                 B
                                                                                   ⊔
                                                                                   ⊓

                                                                 V         
Proof of Lemma 3. Throughout the proof, let π = ∀x̄. φ∧ j pj (x̄pj ) → H[x̄]
range over CHCs in Π, with body B[x̄], and let π B and π I denote its copies per
Definition 8 (when π ∈ ∆B and π ∈ ∆I , respectively), with bodies B B and B I .
Since the body of a CHC is a conjunction of a constraint and uninterpreted
predicate applications, J∃(x̄ \ x̄h ). B[x̄]KM{pj 7→Rj } is monotone in the relations
Rj , for any tuple x̄h ⊆ x̄. We use the following two claims.
                                     p
(A) Let Rj ⊆ DM                 ′          j
                 pj and Rj = δB⇝I (Rj ) for each j, let π ∈ ∆I , and let x̄h ⊆ x̄.
                   B

    Then
                                               I    ′
                                                        
         x̄h
        δI⇝B   J∃(x̄′ \ x̄′h ). B I [x̄′ ]KMI {pj 7→Rj } = J∃(x̄ \ x̄h ). B[x̄]KMB {pj 7→Rj }

    Indeed, every assignment satisfying B I lies in the image ofS           the domain trans-
    formers, since the relations Rj′ constrain the variables j x̄′pj to the im-
    age and the syntactic domain restrictions conjoined by the encoding con-
    strain the remaining variables. Since domain transformers are defined per
    variable (with the consistency requirement guaranteeing that variables in
    the same argument position agree), such an assignment satisfies τB⇝I (φ)
    iff its preimage satisfies φ (Eq. 2), and satisfies pIj (x̄′pj ) under Rj′ iff its
    preimage satisfies pj (x̄pj ) under Rj . Finally, projection onto x̄′h commutes
    with the domain transformers. For π ∈ ∆B , the analogous equality J∃(x̄ \
                        B
    x̄h ). BB [x̄]KMB {pj 7→Rj } = J∃(x̄ \ x̄h ). B[x̄]KMB {pj 7→Rj } is immediate, as π B dif-
    fers from π only in the renaming of its uninterpreted predicates.
(B) Let ⋄ ∈ {B, I} and ♦ ∈ {B, I} \ {⋄}. If p⋄ occurs in the body of some
                                p
    CHC in Π⋄ , then δ♦⇝⋄            Jp♦ KMB|I ⊆ Jp⋄ KMB|I . Indeed, if p♦ is the head
    predicate of some CHC in Π♦ , then p♦ ⇝ p⋄ ∈ Θ♦⇝⋄ by Definition 8, so
      p            M              MB|I ⇝           MB|I
    δ♦⇝⋄    Jp♦ Kn B|I = (Jp⋄ Kn+1     ) ⊆ Jp⋄ Kn+1       for every n (Eq. 5), and the claim
    follows by taking the union over all bounds. Otherwise, (Jp♦ KMB|I )→ = ∅,
                                           p                                              p
    so Jp♦ KMB|I = (Jp♦ KMB|I )⇝ ⊆ δ⋄⇝♦            Jp⋄ KMB|I by Eq. 5, and applying δ♦⇝⋄
                                                        p        p
    yields the claim, since the composition δ♦⇝⋄             ◦ δ⋄⇝♦   is the identity (on DMp
                                                                                              B

                                  I MB|I
    when ⋄ = B, and on Jp K              when ⋄ = I, using Lemma 2).
             Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning               23

                                                                       M
    For the inclusion ⊇, we show by induction on n that JpB Kn B|I ⊆ JpKMB and
 p          M 
δI⇝B   JpI Kn B|I ⊆ JpKMB for every p occurring in Π. For the external com-
                  M            p         MB|I                  p          M
                                                ⊆ JpKMB and δI⇝B
                                                                                   
ponents, (JpB Kn B|I )⇝ ⊆ δI⇝B      JpI Kn−1                         (JpI Kn B|I )⇝ ⊆
 p      p          MB|I           MB|I
                                       ⊆ JpKMB by Eq. 5 and the induction hypoth-
                        
δI⇝B   δB⇝I   JpB Kn−1     = JpB Kn−1
esis. For the local components, consider the contribution of a CHC with head
predicate p. If the CHC is π B ∈ ΠB for some π ∈ ∆B , then by (A), its con-
                                                                MB|I
tribution equals J∃(x̄ \ x̄p ). BKMB {pj 7→Rj } with Rj = JpBj Kn−1  . If the CHC is
                                                        pj      I MB|I
  I
                                                                       
π ∈ ΠI for some π ∈ ∆I , then by (A) with Rj = δI⇝B Jpj Kn−1 (well-defined
                                  p                 M                            p
by Lemma 2, and satisfying δB⇝I      j
                                       (Rj ) = JpIj Kn−1 B|I
                                                             ), the image under δI⇝B  of its
                                        MB {pj 7→Rj }
contribution equals J∃(x̄ \ x̄p ). BK                 . In both cases, Rj ⊆ Jpj KMB by
the induction hypothesis, so by monotonicity, the resulting set is contained in
                               MB
J∃(x̄ \ x̄p ). BKMB {pj 7→Jpj K } , which is contained in JpKMB since the expansion
MB {p 7→ JpKMB }p∈P U satisfies all rules in Π (Section 2.2). The base case n = 0
is subsumed, as facts contain no predicate applications.
    For the inclusion      ⊆, we show by induction on n that JpKM         n
                                                                            B
                                                                              ⊆ JpB KMB|I ∪
  p
       JpI KMB|I . Consider the contribution of a CHC π ∈ Π with head p(x̄p ), in
                 
δI⇝B
which each pj is interpreted as Jpj KM                                      B
                                          n−1 . If π ∈ ∆B , then each pj occurs in the
                                            B

                                                                            MB
body of π ∈ ΠB , so by (B) and the induction hypothesis, Jpj Kn−1 ⊆ JpBj KMB|I .
             B

                                                                      MB          M
Since DM pj is finite, there is a common bound m with Jpj Kn−1 ⊆ Jpj Km
           B                                                                    B    B|I
                                                                                         for
all j, and by (A) and monotonicity, the contribution of π is contained in that
                MB|I →
of π B to (JpB Km+1   ) , hence in JpB KMB|I . If π ∈ ∆I , then each pIj occurs in the
                                  pj
                                        JpBj KMB|I ⊆ JpIj KMB|I , and together with the
           I
                                                  
body of π ∈ ΠI , so by (B), δB⇝I
                                              pj
                                                  Jpj KM            I MB|I
                                                           
induction hypothesis and Lemma 2, δB⇝I                 n−1 ⊆ Jpj K         . By finiteness,
                                                         B

                                     pj          MB
                                                            I M B|I
there is a common bound m with δB⇝I Jpj Kn−1 ⊆ Jpj Km for all j. By (A) with
        pj         M 
Rj = δI⇝B    JpIj Km B|I and monotonicity (note Jpj KM  n−1 ⊆ Rj ), the contribution of
                                                           B

                                   p                                        B|I →  M
π is contained in the image under δI⇝B of the contribution of π I to (JpI Km+1 ) ,
           p
hence in δI⇝B JpI KMB|I .
                        
                                                                                 ⊔
                                                                                 ⊓

Proof of Theorem 1. By Definition 8, the queries of ΠB and ΠI are exactly the
copies π B and π I of the queries π ∈ ∆B and π ∈ ∆I , respectively. By Definitions 2
and 10, it thus suffices to show that, for every query π = ∀x̄. B[x̄] → ⊥ in Π,

        MB {p 7→ JpKMB }p∈P U |= π       iff   M⋄ {p⋄ 7→ Jp⋄ KMB|I }p⋄ ∈P⋄U |= π ⋄

where ⋄ = B if π ∈ ∆B and ⋄ = I if π ∈ ∆I . Let π ∈ ∆B . Each pBj occurs
                    B
in the body of
 pj       I MB|I
                  π ∈B M ΠB , so by (B) (established in the proof of Lemma 3),
δI⇝B Jpj K         ⊆ Jpj K B|I , and Lemma 3 yields Jpj KMB = JpBj KMB|I . Since π B
differs from π only in the renaming of its uninterpreted predicates, the two
expanded structures agree on π, and the equivalence follows.       Let π ∈ ∆I . Each
                                                 pj
                                                     JpBj KMB|I ⊆ JpIj KMB|I . Applying
                                                               
pIj occurs in the body of π I ∈ ΠI , so by (B), δB⇝I
 pj                                                                    pj
                                                                             Jpj KMB =
                                                                                    
δB⇝I   to the equality of Lemma 3 and using Lemma 2, we obtain δB⇝I
JpIj KMB|I . By (A) with Rj = Jpj KMB and x̄h the empty tuple, the body of π is
  24      O. Rappoport et al.

  satisfiable in MB {pj 7→ Jpj KMB } iff the body of π I is satisfiable in MI {pIj 7→
  JpIj KMB|I }, and the equivalence follows.                                        ⊔
                                                                                    ⊓

  Proof of Theorem 3. We say that a formula φ′ ∈ QF_IA with free vari-
  ables x̄′ corresponds  to a formula φ ∈ QF_BV with free variables x̄ if JφKMB =
  δI⇝B Jφ K ↾B , i.e., if φ′ preserves the semantics of φ in the sense of Defini-
           ′ MI
   x̄
                  
                                                          ′
  tion 7. In particular, τB⇝I (φ) corresponds to φ and φV corresponds  to τI⇝B (φ′ )
                                                                ′
  (Eqs. 2 and 3). Moreover, ⊥ corresponds to ⊥, and x′ ∈x̄′ x ↾B corresponds to
  ⊤ by the definition of the syntactic domain restriction. When formulas with free
  variables among a tuple x̄ are combined, their semantics are taken over x̄. We
  use the following two observations.

(O1) Correspondence is preserved under conjunction and under substitution along
     the variable mapping. This holds since domain transformers are defined per
     variable, where the consistency requirement guarantees that substituted vari-
     ables carry the same domain transformers. In addition, by Lemma 1, con-
     joining syntactic domain restrictions to φ′ preserves correspondence.
(O2) Let φ′1 , φ′2 correspond to φ1 , φ2 , respectively, with free variables V among′ x̄
               ′                                                    ′    ′
     (resp.  x̄  ). Then ∀x̄. φ1 →   φ 2 is valid modulo T B iff ∀x̄  . φ1 ∧  x′ ∈x̄′ x ↾B
        → φ′2 is valid modulo TI . Indeed, the former holds iff Jφ1 KMB ⊆ Jφ2 KMB ,
     

             KMI ↾B ⊆ Jφ′2 KMI ↾B by correspondence and the injectivity of δB⇝I
     iff Jφ′1V                                                                   x̄
                                                                                      , iff
         ′            ′   MI       ′ MI
     Jφ1 ∧ x′ ∈x̄′ x ↾B K      ⊆ Jφ2 K    by Lemma 1.

  (⇒) Let I be a ΣB -solution for Π. Define a ΣB|I -interpretation IB|I = (IB , II ) as
  follows. For each uninterpreted predicate p ∈ P U ,
                                                                                    ^
       IB (pB )[ȳpB ] ≜ I(p)[ȳpB ] and II (pI )[ȳp′ B ] ≜ τB⇝I (I(p))[ȳp′ B ] ∧   y ′↾B
                                                                           y ′ ∈ȳp′ B


  We show that IB|I satisfies both conditions of Definition 11. Every CHC π B ∈ ΠB
  is obtained from some π ∈ ∆B by replacing each uninterpreted predicate p with
  pB , so IB (π B ) coincides with I(π) and is valid modulo TBV
                                                              .       
       Next, let π I ∈ ΠI be obtained from π = ∀x̄. φ ∧ j pj (x̄pj ) → H[x̄] in
  ∆I as in Definition 8. By (O1), the body of II (π I ) corresponds to the body of
  I(π): the constraint τB⇝I (φ) corresponds to φ, each conjunct II (pIj )[ȳp′ B 7→ x̄′pj ]
                                                                                     j
  corresponds to I(pj )[ȳpBj 7→ x̄pj ], and the explicit restrictions correspond to
                                     I
  ⊤. Likewise, the head of IV    I (π ) corresponds to the head of I(π). Moreover,
  the body of II (π ) entails x′ ∈x̄S′ x′ ↾B in MI , since the restrictions occurring
                       I

  in the conjuncts II (pIj )[·] cover j x̄′pj and the explicit restrictions cover ȳ =
  x̄ \ ( j x̄pj ). Conjoining x′ ∈x̄′ x′ ↾B to the body of II (π I ) therefore results in
        S                      V
  an equivalent formula, and by (O2), the validity of I(π) modulo TB implies the
  validity of II (π I ) modulo TI .
       Finally, for every p ∈ P U ,
                         ȳpB                    ȳpB
  JτI⇝B (II (pI ))KMB = δI⇝B  JII (pI )KMI ↾B = δI⇝B  JτB⇝I (I(p))KMI ↾B = JI(p)KMB
                                                                       
               Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                25

 by Eq. 3, Lemma 1, and Eq. 2, respectively. Since I(p) = IB (pB ), both ∀ȳpB . IB (pB ) →
 τI⇝B (II (pI )) and its converse are valid modulo TB , so IB|I (θ) is valid modulo TB
 for every interface constraint θ ∈ Θ.
 (⇐) Let IB|I = (IB , II ) be a ΣB|I -solution for ΠB|I . Define a ΣB -interpretation I
 as follows. For each uninterpreted predicate p ∈ P U ,

                                   I(p)[ȳpB ] ≜ φpB ∨ φpI

 where
           (
            IB (pB )[ȳpB ] if pB is the head predicate of some CHC in ΠB
     φpB ≜
            ⊥                otherwise
           (                
            τI⇝B II (pI ) [ȳpB ] if pI is the head predicate of some CHC in ΠI
     φpI ≜
            ⊥                       otherwise

 Note that τI⇝B (II (pI )) is a ΣB -formula with free variables in ȳpB , since ȳpI = ȳp′ B ,
 so I is well-defined.
     We first establish the following claim. For every p ∈ P U :

(C1) If pB occurs in the body of some CHC in ΠB , then ∀ȳpB . I(p) → IB (pB ) is
     valid modulo TB .                                                             
(C2) If pI occurs in the body of some CHC in ΠI , then ∀ȳpB . I(p) → τI⇝B II (pI )
     is valid modulo TB .

 For (C1), the disjunct φpB is either IB (pB ) or ⊥. If φpI ̸= ⊥, then pI is the head
 predicate of some CHC in ΠI and, by the assumption of (C1), pB occurs in the
 body of some CHC in ΠB . By Definition 8, pI ⇝ pB ∈ ΘI⇝B , and interface
 constraint satisfaction (Definition 11) yields the validity modulo TB of φpI →
 IB (pB ). The proof of (C2) is symmetric, using pB ⇝ pI ∈ ΘB⇝I . In addition, by
 construction, if pB (resp. pI ) is the head predicate of some CHC in its fragment,
 then IB (pB ) → I(p) (resp. τI⇝B (II (pI )) → I(p)) is valid modulo TB . We refer to
 these implications as the head bounds. Being validities of universally quantified
 implications, (C1), (C2), and the head bounds also hold under any substitution
 of ȳpB .                                                               V         
     We now show that I(π) is valid modulo TB for every π = ∀x̄. φ∧ j pj (x̄pj ) →
 H[x̄] in Π, i.e., that I is a ΣB -solution for Π (Definition 4).
     Case π ∈ ∆B . Let π B ∈ ΠB be the copy of π. Each pBj occurs in the body of
 π , so by (C1), the body of I(π) implies the body of IB (π B ) modulo TB . By local
  B

 satisfaction, the latter implies ⊥ if H = ⊥, and IB (hB )[ȳhB 7→ x̄h ] if H = h(x̄h ).
 In the latter case, hB is the head predicate of π B ∈ ΠB , so the head bound gives
 IB (hB ) → I(h). Chaining the implications shows that I(π) is valid modulo TB .
     Case π ∈ ∆I . Let π I ∈ ΠI be the translation of π per Definition 8. Each pIj
 occurs in the body of π I , so by (C2), the body of I(π) implies, modulo TB , the
 ΣB -formula                     ^                 
                           φ ∧       τI⇝B II (pIj ) [ȳpBj 7→ x̄pj ]                (6)
                                    j
26      O. Rappoport et al.

By (O1), the body of II (π I ) corresponds to Eq. 6, and the head of II (π I ) cor-
responds to τI⇝B (II (hI ))[ȳhB 7→ x̄h ] if H = h(x̄h ), and to ⊥ if H = ⊥. By local
satisfaction, II (π I ) is V
                           valid modulo TI , and hence so is the formula obtained
from it by conjoining x′ ∈x̄′ x′ ↾B to its body. By (O2), Eq. 6 implies the cor-
responding head modulo TB . If H = ⊥, this shows that I(π) is valid modulo
TB . Otherwise, hI is the head predicate of π I ∈ ΠI , so the head bound gives
τI⇝B (II (hI )) → I(h), and chaining the implications shows that I(π) is valid
modulo TB .                                                                        ⊔
                                                                                   ⊓

Proof of Theorem 4. The proof is by induction on the length of the tran-
sition sequence. We maintain the following invariant. For every ⟨ p⋄ , ψ ⟩ ∈ ∆u ,
the formula ψ under-approximates the external semantics of p⋄ : if ⋄ = B, then
JψKMB ⊆ (JpB KMB|I )⇝ , and if ⋄ = I, then JψKMI ↾B ⊆ (JpI KMB|I )⇝ . Dually, for ev-
ery ⟨ p⋄ , ψ ⟩ ∈ ∆o , the formula ψ over-approximates the external semantics of p⋄ :
if ⋄ = B, then (JpB KMB|I )⇝ ⊆ JψKMB , and if ⋄ = I, then (JpI KMB|I )⇝ ⊆ JψKMI ↾B .
     The invariant holds in the initial state (rule Init), since both lemma sets are
empty. Rule Query preserves it trivially, as it does not modify ∆u or ∆o . Con-
sider rule PosAnswer. Let R be the refutation of Π⋄u ∪ query(p⋄ , ϕ) returned
by the oracle, and let ⟨p⋄ , ψ⟩ be the child of its root. By construction, Π⋄u con-
sists of CHCs from Π⋄ together with facts induced by ∆u . CHCs in Π⋄ are part
of the original encoding ΠB|I , and facts induced by ∆u under-approximate the
corresponding external semantics by the induction hypothesis. Hence Π⋄u under-
approximates the behavior of ΠB|I , in the sense that for every uninterpreted
predicate r⋄ in Π⋄ (and in particular for p⋄ ), its semantics in Π⋄u is contained
in its semantics in ΠB|I . Therefore, R corresponds to a feasible (partial) deriva-
tion in ΠB|I , and ψ under-approximates the semantics of p⋄ in ΠB|I . Finally, by
Definitions 9 and 7, translating ψ across the corresponding interface constraint
yields a formula that under-approximates the external semantics of p♦ . Thus the
invariant is preserved for ∆u .
     Rule NegAnswer is dual. Let I⋄ be the solution of Π⋄o ∪query(p⋄ , ϕ) returned
by the oracle. By construction, Π⋄o consists of CHCs from Π⋄ together with facts
induced by ∆o . CHCs in Π⋄ are part of the original encoding ΠB|I , and facts
induced by ∆o over-approximate the corresponding external semantics by the
induction hypothesis. Hence Π⋄o over-approximates the behavior of ΠB|I , in the
sense that for every uninterpreted predicate r⋄ in Π⋄ (and in particular for
p⋄ ), its semantics in ΠB|I is contained in its semantics in Π⋄o . It follows that
I⋄ (p⋄ ) over-approximates the semantics of p⋄ in ΠB|I . Finally, by Definitions 9
and 7, translating I⋄ (p⋄ ) across the corresponding interface constraint yields a
formula that over-approximates the external semantics of p♦ . Thus the invariant
is preserved for ∆o .
     It follows from the invariant that, throughout the run, Π⋄u under-approximates
the semantics of the corresponding fragment in the theory-modular encoding,
while Π⋄o over-approximates it. Hence, the soundness of rule Unsat follows by
the same reasoning as for rule PosAnswer: a refutation of ΠBu ∪ query(q B , ϕq )
corresponds to a feasible derivation in ΠB|I , and thus witnesses a violation of
the query. Dually, the soundness of rule Sat follows by the same reasoning as
            Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning    27

for rule NegAnswer: a solution of ΠBo ∪ query(q B , ϕq ) over-approximates the
semantics in ΠB|I and proves that no query violation is possible. This concludes
the proof.
    28      O. Rappoport et al.

    B    Benchmarks



                                  Π = { ((x ≥Bs 0, y = (1|B 0) ·B x) ∨ (x <Bs 0, y = (1|B − 1) ·B x)),
1  void f ( int x ) {                                                 x ̸= (1 ≪B (n −B 1)) → p(x, y, 0),
 2   assume ( x !=                         p(x, y, i), i <Bs y → p(x, y, i +B 1),
           INT_MIN ) ;
                                           p(x, y, i), ¬(i <Bs y) → q(x, i),
 3   int y , i ;
 4   if (x >=0) {                          q(x, i), ¬(x ≤Bs i) → ⊥ }
 5      y =(1|0) * x ;
 6   } else {                                                         (b)
 7      y =(1| -1) * x ;
 8   }                            ΠB = { ((x ≥Bs 0, y = (1|B 0) ·B x) ∨ (x <Bs 0, y = (1|B − 1) ·B x)),
 9   i =0;
                                                                       x ̸= (1 ≪B (n −B 1)) → pB (x, y, 0) }
10   while (i < y ) {
11      i ++;                     ΠI = { pI (x′ , y ′ , i′ ), i′ < y ′ → pI (x′ , y ′ , i′ + 1),
12   }
                                           pI (x′ , y ′ , i′ ), ¬(i′ < y ′ ) → q I (x′ , i′ ),
13   assert (x <= i ) ;
14 }                                       q I (x′ , i′ ), ¬(x′ ≤ i′ ) → ⊥ }
                (a)                Θ = { pB ⇝ pI }

                                                                      (c)

    Fig. 3. The abs-ge benchmark. y is initialized to the absolute value of x. All variables
    and constants in Π have sort BV[n] for some n ∈ N+ .
                Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                            29




1  void f ( int x , int y )          Π = { x >Bs 0, y >Bs 0 → p(x, −B y, 0, 0),
         {                                   p(x, y, a, i), i <Bs x → p(x, y, a +B 1, i +B 1),
 2   assume (x >0) ;
 3   assume (y >0) ;                         p(x, y, a, i), ¬(i <Bs x) → q(x, y, a, 0),
 4   int y ’= -y , a =0 , i =0;              q(x, y, a, i), i >Bs y → q(x, y, a −B 1, i −B 1),
 5   int b , c ;                             q(x, y, a, i), ¬(i >Bs y) → r(x, y, a),
 6   while (i < x ) {
 7      a ++;                                r(x, y, a), (a ≥Bs 0),
 8      i ++;                                    ((x ≥Bs 0, b = (1|B 0) ·B x) ∨ (x <Bs 0, b = (1|B − 1) ·B x)),
 9   }
                                                 ((y ≥Bs 0, c = (1|B 0) ·B y) ∨ (y <Bs 0, c = (1|B − 1) ·B y)),
10   i =0;
11   while (i > y ’) {                                                                              ¬(b ≥Bs c) → ⊥ }
12      a - -;
13      i - -;                                                       (b)
14   }
15   if (x >=0) {                    ΠI = { x′ > 0, y ′ > 0, x′↾B , y ′↾B → pI (x′ , −y ′ , 0, 0),
        b =(1|0) * x ;
                                             pI (x′ , y ′ , a′ , i′ ), i′ < x′ → pI (x′ , y ′ , a′ + 1, i′ + 1),
16

17   } else {
18      b =(1| -1) * x ;                     pI (x′ , y ′ , a′ , i′ ), ¬(i′ < x′ ) → q I (x′ , y ′ , a′ , 0),
19   }                                       q I (x′ , y ′ , a′ , i′ ), i′ > y ′ → q I (x′ , y ′ , a′ − 1, i′ − 1),
20   if ( y ’ >=0) {
21      c =(1|0) * y ’;                      q I (x′ , y ′ , a′ , i′ ), ¬(i′ > y ′ ) → rI (x′ , y ′ , a′ ) }
22   } else {                        ΠB = { rB (x, y, a), (a ≥Bs 0),
23      c =(1| -1) * y ’;
24   }                                            ((x ≥Bs 0, b = (1|B 0) ·B x) ∨ (x <Bs 0, b = (1|B − 1) ·B x)),
25   if (a >=0) {                                 ((y ≥Bs 0, c = (1|B 0) ·B y) ∨ (y <Bs 0, c = (1|B − 1) ·B y)),
26      assert (b >= c ) ;
                                                                                                     ¬(b ≥Bs c) → ⊥ }
27   }
28 }
                                      Θ = { rI ⇝ rB }
                 (a)
                                                                     (c)

    Fig. 4. The abs-sum benchmark. All variables and constants in Π have sort BV[n] for
    some n ∈ N+ . Upon termination of the function, the program variables satisfy: a = x
    - y, b = abs(x), and c = abs(y).
    30      O. Rappoport et al.




                                     Π = { x >Bs y, y >Bs 0 → p(x, y, 0),
1  void f ( int x , int y                   p(x, y, i), i <Bs y → p(x, y, i +B 2),
       ) {
 2   assume (x > y ) ;                      p(x, y, i), ¬(i <Bs y) → q(x, i),
 3   assume (y >0) ;                        q(x, i), ((i ≤Bs x, b = 1) ∨ ((i >Bs x, b = 0)),
 4   int i =0 , b ;
                                                      ¬((x ⊕B (−B b)) +B b = −B x)) → ⊥ }
 5   while (i < y ) {
 6      i +=2;                                                     (b)
 7   }
 8   if (i <= x ) {
                                    ΠI = { x′ > y ′ , y ′ > 0, x′↾B , y ′↾B → pI (x′ , y ′ , 0),
 9      b =1;
10   } else {                                pI (x′ , y ′ , i′ ), i′ < y ′ → pI (x′ , y ′ , i′ + 2),
11      b =0;                                pI (x′ , y ′ , i′ ), ¬(i′ < y ′ ) → q I (x′ , i′ ) }
12   }
13   assert (( x ^( - b ) ) +       ΠB = { q B (x, i), ((i ≤Bs x, b = 1) ∨ ((i >Bs x, b = 0)),
           b == - x ) ;
                                                      ¬((x ⊕B (−B b)) +B b = −B x)) → ⊥ }
14 }


                (a)                  Θ = { qI ⇝ qB }

                                                                    (c)

    Fig. 5. The cond-neg benchmark. All variables and constants in Π have sort BV[n] for
    some n ∈ N+ . The term ((x ⊕B (−B b)) +B b) evaluates to −B x if b = 1 and to x if b = 0.
                 Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                           31




                                   Π = { x >Bs y, y >Bs 0 → p(x, y, 0, 0),
1  void f ( int x , int y
                                            p(x, y, a, i), i <Bs x → p(x, y, a −B 1, i +B 1),
        ) {
 2   assume (x > y ) ;                      p(x, y, a, i), ¬(i <Bs x) → q(y, a, 0),
 3   assume (y >0) ;                        q(y, a, i), i <Bs y → q(y, a +B 1, i +B 1),
 4   int i =0 , a =0 , b ;
 5   while (i < x ) {                       q(y, a, i), ¬(i <Bs y), a <Bs 0 → r(a, 1),
 6       a - -;                             q(y, a, i), ¬(i <Bs y), ¬(a <Bs 0) → r(a, 0),
 7       i ++;
                                            r(a, b), ¬((a ⊕B (−B b)) +B b = −B a) → ⊥ }
 8   }
 9   i =0;                                                          (b)
10   while (i < y ) {
11       a ++;
                                ΠI = { x′ > y ′ , y ′ > 0, x′↾B , y ′↾B → pI (x′ , y ′ , 0, 0),
12       i ++;
13   }                                   pI (x′ , y ′ , a′ , i′ ), i′ < x′ → pI (x′ , y ′ , a′ − 1, i′ + 1),
14   if (a <0) {                         pI (x′ , y ′ , a′ , i′ ), ¬(i′ < x′ ) → q I (y ′ , a′ , 0),
15       b =1;
16   } else {                            q I (y ′ , a′ , i′ ), i′ < y ′ → q I (y ′ , a′ + 1, i′ + 1),
17       b =0;                           q I (y ′ , a′ , i′ ), ¬(i′ < y ′ ), a′ < 0 → rI (a′ , 1),
18   }
                                         q I (y ′ , a′ , i′ ), ¬(i′ < y ′ ), ¬(a′ < 0) → rI (a′ , 0) }
19   assert (( a ^( - b ) ) +
            b == - a ) ;        ΠB = { rB (a, b), ¬((a ⊕B (−B b)) +B b = −B a) → ⊥ }
20 }

                                 Θ = { rI ⇝ rB }
                (a)
                                                                    (c)

    Fig. 6. The cond-neg-diff benchmark. All variables and constants in Π have sort BV[n]
    for some n ∈ N+ . The term ((a ⊕B (−B b)) +B b) evaluates to −B a if b = 1 and to a if
    b = 0.
    32      O. Rappoport et al.




1  void f ( unsigned x ,             Π = { x >Bu y, x −B y ≥Bu z → p(y, z, x, 0),
       unsigned y ,                          p(y, z, a, i), i <Bu z → p(y, z, a −B 1, i +B 1),
       unsigned z ) {
                                             p(y, z, a, i), ¬(i <Bu z) → q(y, a),
 2   assume (x > y ) ;
 3   assume (x -y >= z ) ;                   q(y, a), ((a <Bu y, b = −1) ∨ (¬(a <Bu y), b = 0)),
 4   unsigned a = x ;                                       ¬(a = (a ⊕B ((a ⊕B y) &B b))) → ⊥ }
 5   unsigned i =0;
 6   unsigned max =0;                                                  (b)
 7   while (i < z ) {
 8     a - -;                        ΠI = { x′ > y ′ , x′ − y ′ ≥ z ′ , x′↾B , y ′↾B , z ′↾B →
 9     i ++;
10   }                                                                                          pI (y ′ , z ′ , x′ , 0),
11   if (a < y ) {                            pI (y ′ , z ′ , a′ , i′ ), i′ < z ′ → pI (y ′ , z ′ , a′ − 1, i′ + 1),
12     max = a ^(( a ^ y ) & -1) ;
                                              pI (y ′ , z ′ , a′ , i′ ), ¬(i′ < z ′ ) → q I (y ′ , a′ ) }
13   } else {
14     max = a ^(( a ^ y ) &0) ;     ΠB = { q B (y, a), ((a <Bu y, b = −1) ∨ (¬(a <Bu y), b = 0)),
15   }
16   assert ( a == max ) ;                                   ¬(a = (a ⊕B ((a ⊕B y) &B b))) → ⊥ }
17 }
                                      Θ = { qI ⇝ qB }
                 (a)
                                                                       (c)

    Fig. 7. The max-inv benchmark. All variables and constants in Π have sort BV[n] for
    some n ∈ N+ . The term (a ⊕B ((a ⊕B y) &B b)) evaluates to max(a, y), where b = −1 if
    a <Bu y and b = 0 otherwise.
                 Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                              33




                                      Π = { x >Bs y, y >Bs 0 → p(x, y, 0, 0, 0),
1  void f ( int x , int y )                   p(x, y, a, b, i), i <Bs x → p(x, y, a +B 1, b −B 1, i +B 1),
         {                                    p(x, y, a, b, i), ¬(i <Bs x) → q(y, a, b, 0),
 2   assume (x > y ) ;
 3   assume (y >0) ;                          q(y, a, b, i), i <Bs y → q(y, a −B 1, b +B 1, i +B 1),
 4   int a =0 , b =0 , i =0;                  q(y, a, b, i), ¬(i <Bs y) → r(a, b),
 5   while (i < x ) {
                                              r(a, b), ¬((a ⊕B b) <Bs 0) → ⊥ }
 6      a ++;
 7      b - -;                                                         (b)
 8      i ++;
 9   }
                                      ΠI = { x′ > y ′ , y ′ > 0, x′↾B , y ′↾B → pI (x′ , y ′ , 0, 0, 0),
10   i =0;
11   while (i < y ) {                          pI (x′ , y ′ , a′ , b′ , i′ ), i′ < x′ → pI (x′ , y ′ , a′ + 1, b′ − 1, i′ + 1),
12      a - -;                                 pI (x′ , y ′ , a′ , b′ , i′ ), ¬(i′ < x′ ) → q I (y ′ , a′ , b′ , 0),
13      b ++;
14      i ++;                                  q I (y ′ , a′ , b′ , i′ ), i′ < y ′ → q I (y ′ , a′ − 1, b′ + 1, i′ + 1),
15   }                                         q I (y ′ , a′ , b′ , i′ ), ¬(i′ < y ′ ) → rI (a′ , b′ ) }
16   assert (( a ^ b ) <0) ;
17 }                                  ΠB = { rB (a, b), ¬((a ⊕B b) <Bs 0) → ⊥ }

                 (a)                   Θ = { rI ⇝ rB }

                                                                       (c)

    Fig. 8. The opp-signs-diff benchmark. All variables and constants in Π have sort BV[n]
    for some n ∈ N+ . The term (a ⊕B b) <Bs 0 evaluates to true if and only if a and b have
    opposite signs.
    34      O. Rappoport et al.




                                  Π = { x >Bu y, y >Bu 0 → p(x, y, 0, 0),
                                          p(x, y, a, b), b <Bu y → p(x, y, a +B 1, b +B 1),
1  void f ( int x , int y
       ) {                                p(x, y, a, b), ¬(b <Bu y) → q(x, a, b),
 2   assume (x > y ) ;                    q(x, a, b), a <Bu x → q(x, a +B 1, b),
 3   assume (y >0) ;
                                          q(x, a, b), ¬(a <Bu x) → r(a, b),
 4   int a =0 , b =0;
 5   while (b < y ) {                     r(a, b), a1 = a ⊕B b, b1 = b ⊕B a1 , ¬(a1 ⊕B b1 <Bu b1 ) → ⊥ }
 6      a ++;
 7      b ++;                                                          (b)
 8   }
 9   while (a < x ) {             ΠI = { x′ > y ′ , y ′ > 0, x′↾B , y ′↾B → pI (x′ , y ′ , 0, 0),
        a ++;
                                           pI (x′ , y ′ , a′ , b′ ), b′ < y ′ → pI (x′ , y ′ , a′ + 1, b′ + 1),
10

11   }
12   a=a^b;                                pI (x′ , y ′ , a′ , b′ ), ¬(b′ < y ′ ) → q I (x′ , a′ , b′ ),
13   b=b^a;                                q I (x′ , a′ , b′ ), a′ < x′ → q I (x′ , a′ + 1, b′ ),
14   a=a^b;
15   assert (a < b ) ;                     q I (x′ , a′ , b′ ), ¬(a′ < x′ ) → rI (a′ , b′ ) }
16 }
                                  ΠB = { rB (a, b), a1 = a ⊕B b, b1 = b ⊕B a1 , ¬(a1 ⊕B b1 <Bu b1 ) → ⊥ }
                (a)
                                   Θ = { rI ⇝ rB }

                                                                       (c)

    Fig. 9. The swap benchmark. All variables and constants in Π have sort BV[n] for some
    n ∈ N+ . For any a, b, the expressions a1 ⊕B b1 and b1 evaluate to b and a, respectively,
    where a1 = a ⊕B b and b1 = b ⊕B a1 .
                Bit-Precise CHC Satisfiability Using Theory-Modular Reasoning                           35




                               Π = { y ≤Bu (2n − 1) −B x → p(x, y, 0, 0),
1  void f ( int x , int y
        ) {                            p(x, y, a, i), i <Bu x → p(x, y, a +B 1, i +B 1),
 2   assume (y <=                      p(x, y, a, i), ¬(i <Bu x) → q(y, a, 0),
            INT_MAX - x ) ;
 3   assume (y >0) ;                   q(y, a, i), i <Bu y → q(y, a +B 1, i +B 1),
 4   int a =0 , i =0;                  q(y, a, i), ¬(i <Bu y) → r(y, a),
 5   while (i < x ) {
                                       r(y, a), y1 = y ⊕B a, a1 = a ⊕B y1 , ¬(y1 ⊕B a1 ≥Bu a1 ) → ⊥ }
 6       a ++;
 7       i ++;                                                     (b)
 8   }
 9   i =0;
                               ΠI = { y ′ ≤ (2n − 1) − x′ , x′↾B , y ′↾B → pI (x′ , y ′ , 0, 0),
10   while (i < y ) {
11       a ++;                          pI (x′ , y ′ , a′ , i′ ), i′ < x′ → pI (x′ , y ′ , a′ + 1, i′ + 1),
12       i ++;                          pI (x′ , y ′ , a′ , i′ ), ¬(i′ < x′ ) → q I (y ′ , a′ , 0),
13   }
14   y=y^a;                             q I (y ′ , a′ , i′ ), i′ < y ′ → q I (y ′ , a′ + 1, i′ + 1),
15   a=a^y;                             q I (y ′ , a′ , i′ ), ¬(i′ < y ′ ) → rI (y ′ , a′ ) }
16   y=y^a;
17   assert (y >= a ) ;        ΠB = { rB (y, a), y1 = y ⊕B a, a1 = a ⊕B y1 , ¬(y1 ⊕B a1 ≥Bu a1 ) → ⊥ }
18 }
                                Θ = { rI ⇝ rB }
                (a)
                                                                   (c)

    Fig. 10. The swap-sum benchmark. All variables and constants in Π have sort BV[n]
    for some n ∈ N+ . For any y, a, the expressions y1 ⊕B a1 and a1 evaluate to a and y,
    respectively, where y1 = y ⊕B a and a1 = a ⊕B y1 .
    36      O. Rappoport et al.


                                    Π = { x >Bu 0 → p(x, 0, x),
                                            p(x, y, z), y <Bu x −B 1 → p(x, y +B 1, z −B 1),
1 void f ( int x ) {                        p(x, y, z), ¬(y <Bu x −B 1) → q(z),
2   assume (x >0) ;
                                            q(z), ¬((z&B (z −B 1)) = 0) → ⊥ }
3   int y =0 , z = x ;
4   while (y <x -1) {                                               (b)
5     y ++;
6     z - -;
                                  ΠI = { x′ > 0, x′↾B → pI (x′ , 0, x′ ),
7   }
8   assert ( z &( z -1)                   pI (x′ , y ′ , z ′ ), y ′ < x′ − 1 → pI (x′ , y ′ + 1, z ′ − 1),
         ==0) ;                           pI (x′ , y ′ , z ′ ), ¬(y ′ < x′ − 1) → q I (z ′ ) }
9 }

                                  ΠB = { q B (z), ¬((z&B (z −B 1)) = 0) → ⊥ }
                 (a)
                                   Θ = { qI ⇝ qB }

                                                                    (c)

    Fig. 11. The turn-off-rm benchmark. All variables and constants in Π have sort BV[n]
    for some n ∈ N+ . Given a bit-vector z, the expression z&B (z −B 1) clears the rightmost
    1-bit of z, yielding 0 if z contains no 1-bits.


                                  Π = { x >Bs 0 → p(x, 0),
                                         p(x, a), a <Bs x → p(x, a +B 1),
                                         x >Bs 0 → q(x, x, 0),
1  void f ( int x ) {                    q(x, y, b), y >Bs 0 → q(x, y −B 1, b −B 1),
2    assume (x >0) ;
                                         p(x, a), ¬(a <Bs x), q(x, y, b), ¬(y >Bs 0) → r(a, b),
 3   int a =0 , y =x , b =0;
 4   while (a < x ) {                    r(a, b), ¬(((a +B b)|B 1) = 1) → ⊥ }
 5     a ++;
 6   }                                                              (b)
 7   while (y >0) {
 8     y - -;                     ΠI = { x′ > 0, x′↾B → pI (x′ , 0),
       b - -;
                                          pI (x′ , a′ ), a′ < x′ → pI (x′ , a′ + 1),
 9

10   }
11   assert ((( a + b ) |1)               x′ > 0 → q I (x′ , x′ , 0),
          ==1) ;                          q I (x′ , y ′ , b′ ), y ′ > 0 → q I (x′ , y ′ − 1, b′ − 1),
12 }
                                          pI (x′ , a′ ), ¬(a′ < x′ ), q I (x′ , y ′ , b′ ), ¬(y ′ > 0) → rI (a′ , b′ ) }
                 (a)
                                  ΠB = { rB (a, b), ¬(((a +B b)|B 1) = 1) → ⊥ }

                                   Θ = { rI ⇝ rB }

                                                                    (c)

    Fig. 12. The turn-on-lsb benchmark. All variables and constants in Π have sort BV[n]
    for some n ∈ N+ . Given a bit-vector x, the expression x|B 1 sets the least significant bit
    of x to 1.
