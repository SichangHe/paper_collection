                                                Completeness for a First-order Abstract
                                                          Separation Logic

                                                                       Zhé Hóu and Alwen Tiu
arXiv:1608.06729v1 [cs.LO] 24 Aug 2016




                                                             Nanyang Technological University, Singapore
                                                              zhe.hou@ntu.edu.sg, atiu@ntu.edu.sg


                                                Abstract. Existing work on theorem proving for the assertion language
                                                of separation logic (SL) either focuses on abstract semantics which are
                                                not readily availabe in most applications of program verification, or on
                                                concrete models for which completeness is not possible. An important
                                                element in concrete SL is the points-to predicate which denotes a sin-
                                                gleton heap. SL with the points-to predicate has been shown to be non-
                                                recursively enumerable. In this paper, we develop a first-order SL, called
                                                FOASL, with an abstracted version of the points-to predicate. We prove
                                                that FOASL is sound and complete with respect to an abstract seman-
                                                tics, of which the standard SL semantics is an instance. We also show
                                                that some reasoning principles involving the points-to predicate can be
                                                approximated as FOASL theories, thus allowing our logic to be used for
                                                reasoning about concrete program verification problems. We give some
                                                example theories that are sound with respect to different variants of
                                                separation logics from the literature, including those that are incompat-
                                                ible with Reynolds’s semantics. In the experiment we demonstrate our
                                                FOASL based theorem prover which is able to handle a large fragment of
                                                separation logic with heap semantics as well as non-standard semantics.


                                         1    Introduction
                                         Separation Logic (SL) is widely used in program verification and reasoning about
                                         memory models [28,30]. SL extends the traditional Hoare Logic with logical con-
                                         nectives ∗, −∗ from the logic of Bunched Implications (BI). These new connec-
                                         tives in BI provide an elegant way to reason about resources locally, enabling
                                         analyses of large scale programs. Current work on SL can be divided into two
                                         categories: one on the abstract separation logics and the other on the concrete
                                         ones. On the abstract side there has been study on BI and its Boolean variant
                                         BBI [27,22]. Closely related are abstract separation logic and its neighbours [9,21].
                                         Abstract separation logics lack the interpretation of the points-to predicate 7→,
                                         which represents a single memory cell. In this setting, the semantics is just an ex-
                                         tension of commutative monoids with certain properties usually called separation
                                         theory [13,8]. On the concrete side there have been developments along several di-
                                         rections, such as proof methods for SL with memory model semantics [15,17,24],
                                         and symbolic heaps [2,1,26,6]. There have been numerous modifications of SL,
                                         e.g., Fictional Separation Logic [18], Rely/Guarantee [34], Concurrent Separa-
                                         tion Logic [4].
     To support reasoning about Hoare triples, it is essential to have proof meth-
ods for the assertion logic. In the reminder of this paper we focus on the assertion
logic of separation logic. Although theorem proving for propositional abstract
separation logics (PASLs) is undecidable [22,7], there have been semi-decision
procedures for those logics [5,29,16,8,23]. However, since PASLs do not impose
a concrete semantic model, they usually cannot be directly used in program
verification. The situation is more intriguing for separation logic with memory
model semantics. Calcagno et al. showed that the full logic is not recursively
enumerable [10], thus it is not possible to have a sound and complete finite proof
system for the full separation logic. Interestingly, their result uses only an exten-
sion of first-order logic, without function symbols, but with a two-field points-to
predicate, i.e., predicates of the form [a 7→ c, d], which represents a memory cell
with a record of two fields. Recent study also shows that the points-to predicate
7→ is a source of undecidability. For example, restricting the record field (i.e.,
 right hand side) of 7→ to one variable and allowing only one quantified variable
 reduces the satisfiability of SL to PSPACE-complete [12]. The above work in-
 dicates that directly handling the points-to predicate in the logic may not be
 easy. Section 4 of [17] details related issues on various proof systems for separa-
 tion logic with memory model. Another complicating factor in designing a proof
 system for separation logic is the “magic wand” −∗ connective. The separation
conjunction ∗ can be encoded using −∗ , but not the other way around [3,11].
 Consequently, most proof methods for SL with concrete semantics are restricted
 to fragments of SL, typically omitting −∗ . The connective −∗ , however, has
 found many applications, such as tail-recursion [25], iterators [19], “septraction”
 in rely/guarantee [34], amongst other motivating examples discussed in the in-
 troduction of [24].
    Since completeness with respect to Reynolds’s model is not possible, an in-
teresting question arises as to what properties of points-to (−∗ is not so crucial
in terms of the completeness property) one should formalize in the system, and
what kind of semantics the resulting proof system captures. There have been at
least a couple of attempts at designing a proof system that features both −∗ and
points-to; one by Lee and Park [24] and the other by Hou et al. [17]. In [24], Lee
and Park claimed incorrectly that their proof system is complete with respect
to Reynolds’s semantics, though this claim was later retracted.1 In [17], Hou et
al. give a proof system LSSL that is sound with respect to Reynolds’s semantics,
but no alternative semantics was proposed nor any completeness result stated.
It is also not clear in general what proof rules one should include in the proof
system such as that in [17]. This has led to the introduction of various ad hoc
proof rules in [17], which are often complex and unintuitive, in order to cap-
ture specific properties of the underlying concrete separation logic models (e.g.,
Reynolds’s model), resulting in a complex proof system, which is both hard to
implement and hard to reason about.

1
     See http://pl.postech.ac.kr/SL/ for the revised version of their proof system,
    which is sound but not complete w.r.t. Reynolds’s semantics.
     In this paper, we revisit our previous work [17] in order to provide an abstract
semantics and a sound and complete proof system with respect to that abstract
semantics, that are useful for reasoning about the meta-theory of the proof sys-
tem, and easy to extend to support reasoning about various concrete models of
separation logic. Our point of departure is to try to give a minimal proof system
and encode as many properties of points-to as possible using logical theories,
rather than proof rules, and to formalize as inference rules only those properties
that cannot be easily encoded as theories. This led us to keep only two proof
rules for the points-to predicate from [17] (see the rules 1 and 2 in Figure 1
in Section 3). Semantically, these two rules are justified by a new semantics of
an abstract version of the points-to predicate (notationally represented by
here, to distinguish it from the points-to predicate 7→ in the concrete SL), that
is, it is a function that constructs a heap from a tuple of values. In particular,
we do not assume that the constructed heap from a tuple is a singleton heap, so
a points-to predicate such as [a      b, c] in our semantics denotes a heap, but not
necessarily a singleton heap mapping a to a two-field record (b, c). Reasoning
in the concrete models, such as Reynolds’s SL, which may require properties of
singleton heaps, can be approximated by adding theories to restrict the interpre-
tation of points-to (see e.g., Section 5.1). Obviously one would not be able to
completely restrict the interpretation of       to singleton heaps via a finite theory,
as one would then run into the same incompleteness problem as shown in [10].
    The proof system for the first-order abstract separation logic that we intro-
duce here, called LSF OASL , is based on the proof system LSP ASL for proposi-
tional abstract separation logic (PASL) [16], which is a labelled sequent calculus.
We choose labelled calculi as the framework to formalize our logic since it has
been shown to be a good framework for proof search automation for abstract
separation logics [17,23]. Formulas in a labelled sequent in LSP ASL are inter-
preted relative to the interpretation of the labels they are attached to, so a
labelled formula such as h : F , where h is a label and F is a formula, denotes
the truth value of F when evaluated against the heap h. In extending PASL
to the first-order case, especially when formulating theories for specific concrete
models, it turns out that we need to be able to assert that some formulas hold
universally for all heaps, or that they hold in some unspecified heap, both of
which are not expressible in PASL. To get around this limitation, we introduce
modal operators to allow one to state properties that hold globally in all heaps
or in some heap. Section 5 shows some examples of uses of these modal operators
in theories approximating concrete models of separation logics.
    The semantics of FOASL is formally defined in Section 2. In Section 3 we
present the proof system LSF OASL , which is an extension of LSP ASL with rules
for first-order quantifiers, the points-to predicate and modal operators. In Sec-
tion 4, we prove soundness and completeness of LSF OASL with respect to the
semantics described in Section 2. The completeness proof is done via a counter-
model construction similar to that in [20,16] for the propositional case, but our
proof is significantly more complicated as we have to deal with the first-order
language and the construction of the model for the points-to predicate, which
requires a novel proof technique. We show in Section 5 that all the inference
rules for points-to in the labelled sequent calculus LSSL [17] can be derived us-
ing theories in our logic, except one rule called HC, which is not used in the
current program verification tools. Our theories for points-to cover the widely-
used symbolic heap fragment of SL, thus our logic can be used in many existing
program verification methods. Furthermore, we can also prove many formulae
that are valid in SL but which cannot be proved by most existing tools. An
implementation is discussed in Section 6, we show that our prover can reason
about the standard heap semantics and the non-standard ones.


2    First-order Abstract Separation Logic
This section introduces First-order Abstract Separation Logic (FOASL). The
formulae of FOASL are parameterized by a first order signature Σ = (R, C),
consisting of a set of predicate symbols R and a set of constants C. Constants
are ranged by a, b and c, and predicate symbols by p and q (possibly with
subscripts). We also assume an infinite set V of first-order variables, ranged over
by x, y, z. A term is either a constant or a variable, and is denoted by e, s and t.
We assume that R includes a symbol =, denoting the equality predicate, and a
finite collection of abstract points-to predicates. We shall use the notation n to
denote an abstract points-to predicate of arity n. We use an infix notation when
writing the abstract points-to predicates. For an abstract points-to predicate of
arity k, taking arguments t1 , . . . , tk , we write it in the form:
                                           k
                                     t1        t2 , . . . , t k .
We shall omit the superscript k when the arity of      is not important or can
be inferred from the context of discussion. Note that the abstract points-to
is not the points-to predicate in SL, but is a weaker version whose properties
will be discussed later. To simplify presentation, we do not consider function
symbols in our language, but it is straightforward to add them. In any case,
the incompleteness result for concrete SL of [10] holds even in the absence of
function symbols, so the omission of function symbols from our logic does not
make the completeness proof for our logic conceptually easier.
    The formulae of FOASL are given by the following grammar:
           F ::= ⊤∗ | ⊥ | p(t1 , . . . , tk ) | s t1 , . . . , t l | s = t | F → F |
                 F ∗ F | F −∗ F | ♦F | ∃x.F
The logical constant ⊥, the connective → and the quantifer ∃ are the usual logical
 operators from first-order logic. The operator ♦ is a modal operator (denoting
“possibility”). Classical negation ¬F is defined as F → ⊥. Other operators, i.e.,
 ⊤, ∨, ∧, ∀, and , can be defined via classical negation, e.g., A = ♦(A →
 ⊥) → ⊥. The connectives ∗ and −∗ correspond to separation conjunction and
the “magic wand” from separation logic [30], and ⊤∗ is the multiplicative truth.
    The semantics of FOASL is defined based on a separation algebra, i.e., a
 commutative monoid (H, ◦, ǫ) where H is a non-empty set, ◦ is a partial binary
M, v, h    p(t1 , · · · , tn ) iff (tM               M
                                        1 , · · · , tn ) ∈ p
                                                             I
                                                                      M, v, h ⊤∗ iff h = ǫ
M, v, h    A→B                   iff M, v, h 6 A or M, v, h B         M, v, h ⊥ iff never
M, v, h     A ∗ B iff h1 ◦ h2 = h and M, v, h1 A and M, v, h2 B for some h1 and h2
M, v, h     A−∗ B iff for all h1 and h2 , if h ◦ h1 = h2 and M, v, h1 A, then M, v, h2 B.
M, v, h    ∃x.A(x) iff ∃d ∈ D.M, v[d/x], h A(x)
M, v, h    ♦A                       iff ∃h1 ∈ H.M, v, h1 A
M, v, h    t1 = t2                  iff tM            M
                                         1 and t2 are the same element in D.
M, v, h    t1      t2 , . . . , tk iff fk (t1 , . . . , tM
                                             M
                                                         k ) = h.

                         Table 1. The semantics of FOASL.


function H × H ⇀ H written infix, and ǫ ∈ H is the unit. This separation
algebra satisfies the following conditions, where ‘=’ is interpreted as ‘both sides
undefined, or both sides defined and equal’:

identity: ∀h ∈ H. h ◦ ǫ = h.
commutativity: ∀h1 , h2 ∈ H. h1 ◦ h2 = h2 ◦ h1 .
associativity: ∀h1 , h2 , h3 ∈ H. h1 ◦ (h2 ◦ h3 ) = (h1 ◦ h2 ) ◦ h3 .
cancellativity: ∀h1 , h2 , h3 , h4 ∈ H. if h1 ◦ h2 = h3 and h1 ◦ h4 = h3 then
    h2 = h4 .
indivisible unit: if h1 ◦ h2 = ǫ then h1 = ǫ.
disjointness: ∀h1 , h2 ∈ H. if h1 ◦ h1 = h2 then h1 = ǫ.
cross-split: if h1 ◦ h2 = h0 and h3 ◦ h4 = h0 , then ∃h13 , h14 , h23 , h24 ∈ H such
    that h13 ◦ h14 = h1 , h23 ◦ h24 = h2 , h13 ◦ h23 = h3 , and h14 ◦ h24 = h4 .

Note that partial-determinism is assumed since ◦ is a partial function: for any
h1 , h2 , h3 , h4 ∈ H, if h1 ◦ h2 = h3 and h1 ◦ h2 = h4 then h3 = h4 .
     A FOASL model is a tuple M = (D, I, v, F , H, ◦, ǫ) where D is a non-empty
domain, I is an interpretation function mapping constant symbols to elements
of D, and predicate symbols, other than = and , to relations. The function v
is a valuation function mapping variables to D. We use a set F of functions to
interpret the abstract points-to predicates. To each abstract points-to predicate
of arity n, we associate an n-argument total function fn : D × · · · × D 7→ H ∈
F . The tuple (H, ◦, ǫ) is a separation algebra. For a predicate symbol p and
a constant symbol c, we write pI and cI , respectively, for their interpretations
under I. We write tM for the interpretation of term t in the model M. For a
variable x, xM = v(x). A term t is closed if it has no variables, and we write tI
for the interpretation of t since it is independent of the valuation function v.
     A separation algebra (H, ◦, ǫ) can be seen as a Kripke frame, where H is the
set of worlds and the (ternary) accessibility relation R is defined as: R(h1 , h2 , h3 )
iff h1 ◦ h2 = h3 . Modal operators are thus a natural extension to FOASL.
     The semantics of FOASL formulae are defined via Kripke style notations in
Table 1, where M = (D, I, v, F , H, ◦, ǫ) is a FOASL model, and h, h1 , h2 ∈ H.
In the table, we write v[c/x] to denote the valuation function that may differ
from v only in the mapping of x, i.e., v[c/x](x) = c and v[c/x](y) = v(y) if
y 6= x. A FOASL formula A is true at h in the model M = (D, I, v, F , H, ◦, ǫ)
if M, v, h A. It is true in M if it is true at some h in H. A formula is valid
if it is true in all models; a formula is satisfiable if it is true in some model. A
formula is called a sentence if it has no free variables.
     Besides the first-order language, FOASL has two main extensions over PASL:
the abstract points-to predicate          and the modality ♦. We explain their intu-
itions here. In the concrete SL models, the points-to predicate [a 7→ b] is true
only in a singleton heap that maps a to b. In our abstract semantics for [a           b],
we drop the requirement that the heap must be singleton. Instead, we generalize
this by parameterizing the semantics with a function (the function f discussed
earlier) that associates values to (possibily non-singleton) heaps. The predicate
[a     b] is true in a world h iff h is the image of f2 (a, b). As a consequence of this
interpretation of , we have the following properties where ~t is a list of fields:

 – (Injectivity) If s ~t holds in both h1 and h2 , then h1 = h2 .
 – (Totality) For any s and ~t, there is some h such that s ~t holds in h.

The latter in particular is a consequence of the fact that functions in F are
total functions. We do not impose any other properties on . For example, we
do not assume an invalid address nil such that nil 7→ ~t must be false. The
reason we cannot disprove nil       ~t is partly because we do not insist on a fixed
interpretation of nil in our logic. This does not mean that nil        ~t is valid in our
logic; it is only satisfiable. We can strengthen       by adding more theories to it,
including a formula to force nil       ~t to be unsatisfiable. See Section 5 and 6 for
details.
    To motivate the need for the modal operators, consider an example to approx-
imate, in our framework, a separation logic where the points-to relation maps an
address to a multiset of addresses. In the binary case, one could formalize this
as:

                        F = ∀x, y, z.(x 7→ y, z) → (x 7→ z, y)

We can encode this property as a rule in a labelled sequent calculus as shown
below left. When generalising this to points-to of (n + 1)-arities, we will have to
consider adding many variants of rules that permute the right hand side of 7→,
which is what we are trying to avoid. Alternatively, we can add the formula F
to the antecedent of the sequent, and attach a label l to F , and do a forward-
chaining on l : F , as shown below right, where Γ, ∆ are sets of labelled formulae:

           Γ ; l : (a 7→ c, b) ⊢ ∆       ···        Γ, l : F, l : (a 7→ c, b) ⊢ ∆
           Γ ; l : (a 7→ b, c) ⊢ ∆             Γ, l : F, l : (a 7→ b, c) ⊢ ∆
where the · · · are the instantiation of x, y, z with a, b, c respectively, and the
discharge of the assumption (x 7→ y, z) of F . However, if (a 7→ b, c) in the
conclusion is attached to another label (world) m, we then have to add m : F to
the sequent. In effect, we would have to add an infinite set of labelled formulae
of the form k : F to the sequent to achieve the same effect of the inference rule.
With modalities, we can simply use l : F , which would then allow F to be used
at any world in the antecedent of the sequent.
Example 1. Consider Reynolds’s semantics for separation logic [30], with an ab-
stract points-to predicate of arity two. This can be shown to be an instance
of our abstract semantics, where the domain D is the set of integers, H is the
set of heaps (i.e., finite partial maps from integers to integers), ǫ denotes the
empty heap, and the function f2 is defined as f2 (a, b) = [a 7→ b] where [a 7→ b]
is the singleton heap, mapping a to b. The operation ◦ on H is defined as heap
composition. It can be shown that (H, ◦, ǫ) forms a separation algebra. Note
that if we relax the interpretation of H to allow infinite heaps, (H, ◦, ǫ) is still
a separation algebra, which shows that our semantics may admit non-standard
interpretations of separation logic.


3    LSF OASL : A Labelled Calculus for FOASL
Let LVar be an infinite set of label variables, the set L of labels is LVar ∪ {ǫ},
where ǫ 6∈ LVar is a label constant. We overload the notation and write h with
subscripts as labels. A function ρ : L → H from labels to worlds is a label
mapping iff it satisfies ρ(ǫ) = ǫ, mapping the label constant ǫ to the identity
world of H. A labelled formula is a pair consisting of a label and a formula. We
write a labelled formula as h : A, when h is the label and A is the formula of
the labelled formula. A relational atom is an expression of the form (h1 , h2 ⊲ h3 ),
where h1 , h2 and h3 are labels, this corresponds to h1 ◦ h2 = h3 in the semantics.
A relational atom is not a formula; rather it can be thought of as a structural
component of a sequent. A sequent takes the form G; Γ ⊢ ∆ where G is a set
of relational atoms, Γ, ∆ are sets of labelled formulae, and ; denotes set union.
Thus Γ ; h : A is the union of Γ and {h : A}. The left hand side of a sequent is
the antecedent and the right hand side is the succedent.
    We call our labelled proof system LSF OASL . The logical rules of LSF OASL
are shown in Figure 1, structural rules are in Figure 2. To simplify some rules,
we introduce the notation h1 ∼ h2 as an abbreviation of (ǫ, h1 ⊲ h2 ). We use the
notation [t/x] to denote a variable substitution, and similarly [h′ /h] for a label
substitution, where h is a label variable. The equality rules, for terms (=1 and
=2 ) and labels (∼1 and ∼2 ), are the usual equality rules (see e.g., [33]). These
rules allow one to replace a term (label) with its equal anywhere in the sequent.
Note that in those rules, the replacement of terms (labels) need not be done for
all occurrences of equal terms; one can replace just one occurrence or more. For
example, below left is a valid instance of =2 . This is because both the premise
and the conclusion of the rules are instances of the sequent below right:
    h : s = t; h1 : p(t, s) ⊢ h2 : q(s, s)   =2   h : s = t; h1 : p(x, s) ⊢ h2 : q(s, s)
    h : s = t; h1 : p(s, s) ⊢ h2 : q(s, s)
i.e., the premise sequent is obtained from the above sequent with substitution
[t/x], and the conclusion sequent with [s/x]. A similar remark applies for label
replacements in sequents affected via ∼2 . The rules 1 and 2 respectively
capture the injectivity and the totality properties of the underlying semantic
function interpreting .
                           id                             ⊥L          G; h ∼ ǫ; Γ ⊢ ∆                                          ⊤∗ R
 G; Γ ; h : A ⊢ h : A; ∆              G; Γ ; h : ⊥ ⊢ ∆                                       ⊤∗ L       G; Γ ⊢ ǫ : ⊤∗ ; ∆
                                                                     G; Γ ; h : ⊤∗ ⊢ ∆

                G; Γ ; h : A ⊢ h : B; ∆                       G; Γ ⊢ h : A; ∆         G; Γ ; h : B ⊢ ∆
                                               →R                                                           →L
                 G; Γ ⊢ h : A → B; ∆                                   G; Γ ; h : A → B ⊢ ∆

        (h1 , h2 ⊲ h0 ); G; Γ ; h1 : A; h2 : B ⊢ ∆                   (h1 , h0 ⊲ h2 ); G; Γ ; h1 : A ⊢ h2 : B; ∆
                                                         ∗L                                                        −∗ R
                 G; Γ ; h0 : A ∗ B ⊢ ∆                                        G; Γ ⊢ h0 : A−∗ B; ∆

        (h1 , h2 ⊲ h0 ); G; Γ ⊢ h1 : A; h0 : A ∗ B; ∆             (h1 , h2 ⊲ h0 ); G; Γ ⊢ h2 : B; h0 : A ∗ B; ∆
                                                                                                                        ∗R
                                         (h1 , h2 ⊲ h0 ); G; Γ ⊢ h0 : A ∗ B; ∆

      (h1 , h0 ⊲ h2 ); G; Γ ; h0 : A−∗ B ⊢ h1 : A; ∆             (h1 , h0 ⊲ h2 ); G; Γ ; h0 : A−∗ B; h2 : B ⊢ ∆
                                                                                                                        −∗ L
                                        (h1 , h0 ⊲ h2 ); G; Γ ; h0 : A−∗ B ⊢ ∆

        G; Γ ; h : A(y) ⊢ ∆                    G; Γ ⊢ h : A(t); h : ∃x.A(x); ∆                      G; Γ ; h′ : A ⊢ ∆
                                  ∃L                                                 ∃R                                  ♦L
      G; Γ ; h : ∃x.A(x) ⊢ ∆                        G; Γ ⊢ h : ∃x.A(x); ∆                           G; Γ ; h : ♦A ⊢ ∆

       G; Γ ; h : t = t ⊢ ∆
                                 =1
                                            G; h : s = t; Γ [t/x] ⊢ ∆[t/x]
                                                                              =2
                                                                                           G; Γ ⊢ h′ : A; h : ♦A; ∆
                                                                                                                        ♦R
            G; Γ ⊢ ∆                      G; h : s = t; Γ [s/x] ⊢ ∆[s/x]                      G; Γ ⊢ h : ♦A; ∆

                  G; Γ ; h : s        ~
                                      t⊢∆              G; h1 ∼ h2 ; Γ ; h1 : s      ~
                                                                                    t; h2 : s       ~
                                                                                                    t⊢∆
                                                1                                                            2
                        G; Γ ⊢ ∆                              G; Γ ; h1 : s   ~
                                                                              t ; h2 : s      ~
                                                                                              t⊢∆

Side conditions:
In ∗L and −∗ R, the labels h1 and h2 do not occur in the conclusion.
In ∃L, y is not free in the conclusion.               In ♦L, h′ does not occur in the conclusion.
In   1 , h does not occur in the conclusion.


                                  Fig. 1. Logical rules in LSF OASL.


    An extended model (M, ρ) is a FOASL model M equipped with a label
mapping ρ. A sequent G; Γ ⊢ ∆ is falsifiable in an extended model if: (1) every
relational atom (h1 , h2 ⊲ h3 ) ∈ G is true, i.e., ρ(h1 ) ◦ ρ(h2 ) = ρ(h3 ); (2) every
labelled formula h : A ∈ Γ is true, i.e., M, v, ρ(h) A; (3) every labelled formula
h′ : B ∈ ∆ is false, i.e., M, v, ρ(h′ ) 6 B. A sequent is falsifiable if it is falsifiable
in some extended model.
    To prove a formula F , we start from the sequent ⊢ h : F with an arbitrary
label h 6= ǫ, and try to derive a closed derivation by applying inference rules
backwards from this sequent. A derivation is closed if every branch can be closed
by a rule with no premises. The soundness of LSF OASL can be proved by arguing
that each rule preserves falsifiability upwards. The proof is given in Appendix A.

Theorem 1 (Soundness). For every FOASL formula F , if ⊢ h : F is derivable
in LSF OASL for any label h, then F is a valid FOASL formula.


4    Counter-model Construction

We now give a counter-model construction for LSF OASL to show that LSF OASL
is complete w.r.t. FOASL. The proof here is motivated by the completeness proof
of the labelled sequent calculus and labelled tableaux for PASL [16,20], but this
                  h ∼ h; G; Γ ⊢ ∆                    h1 ∼ h2 ; G[h2 /h]; Γ [h2 /h] ⊢ ∆[h2 /h]
                                       ∼1                                                           ∼2
                      G; Γ ⊢ ∆                       h1 ∼ h2 ; G[h1 /h]; Γ [h1 /h] ⊢ ∆[h1 /h]

           (h2 , h1 ⊲ h0 ); (h1 , h2 ⊲ h0 ); G; Γ ⊢ ∆                (h1 , h1 ⊲ h2 ); h1 ∼ ǫ; G; Γ ⊢ ∆
                                                          E                                                 D
                   (h1 , h2 ⊲ h0 ); G; Γ ⊢ ∆                              (h1 , h1 ⊲ h2 ); G; Γ ⊢ ∆

                    (h3 , h5 ⊲ h0 ); (h2 , h4 ⊲ h5 ); (h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h1 ); G; Γ ⊢ ∆
                                                                                                   A
                                    (h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h1 ); G; Γ ⊢ ∆

           (h1 , h2 ⊲ h0 ); h0 ∼ h3 ; G; Γ ⊢ ∆                       (h1 ,h2 ⊲ h0 ); h2 ∼ h3 ; G; Γ ⊢ ∆
                                                      P                                                         C
        (h1 , h2 ⊲ h0 ); (h1 , h2 ⊲ h3 ); G; Γ ⊢ ∆                (h1 ,h2 ⊲ h0 ); (h1 , h3 ⊲ h0 ); G; Γ ⊢ ∆

   (h5 , h6 ⊲ h1 ); (h7 , h8 ⊲ h2 ); (h5 , h7 ⊲ h3 ); (h6 , h8 ⊲ h4 ); (h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h0 ); G; Γ ⊢ ∆
                                                                                                                    CS
                                   (h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h0 ); G; Γ ⊢ ∆


 Side conditions:
 In A, the label h5 does not occur in the conclusion.
 In CS, the labels h5 , h6 , h7 , h8 do not occur in the conclusion.

                                 Fig. 2. Structural rules in LSF OASL .


proof is significantly more complex, as can be seen in the definition of Hintikka
sequent below, which has almost twice as many cases as the previous work. The
constructed model extends the non-classical logic model in the previous work
with a Herbrand model as in first-order logic. For space reasons we only set up
the stage here and delay the full proofs to Appendix B.
   We define a notion of saturated sequent, i.e., Hintikka sequent, on which all
possible rule instances in LSF OASL have been applied. In the following, we
denote with R a relational atom or a labelled formula.

Definition 1 (Hintikka sequent). Let L be a FOASL language and let T be
the set of closed terms in L. A labelled sequent G; Γ ⊢ ∆, where Γ, ∆ are sets of
labelled sentences, is a Hintikka sequent w.r.t. L if it satisfies the following condi-
tions for any sentences A, B, any terms t, t′ , and any labels h, h0 , h1 , h2 , h3 , h4 , h5 , h6 , h7 :
 1. If h1 : A ∈ Γ and h2 : A ∈ ∆ then h1 ∼ h2 6∈ G.
 2. h : ⊥ 6∈ Γ .
 3. If h : ⊤∗ ∈ Γ then h ∼ ǫ ∈ G.
 4. If h : ⊤∗ ∈ ∆ then h ∼ ǫ 6∈ G.
 5. If h : A → B ∈ Γ then h : A ∈ ∆ or h : B ∈ Γ.
 6. If h : A → B ∈ ∆ then h : A ∈ Γ and h : B ∈ ∆.
 7. If h0 : A ∗ B ∈ Γ then ∃h1 , h2 ∈ L s.t. (h1 , h2 ⊲ h0 ) ∈ G, h1 : A ∈ Γ and h2 : B ∈ Γ.
 8. If h3 : A ∗ B ∈ ∆ then ∀h0 , h1 , h2 ∈ L if (h1 , h2 ⊲ h0 ) ∈ G and h0 ∼ h3 ∈ G then
    h1 : A ∈ ∆ or h2 : B ∈ ∆.
 9. If h3 : A−∗ B ∈ Γ then ∀h0 , h1 , h2 ∈ L if (h1 , h2 ⊲ h0 ) ∈ G and h2 ∼ h3 ∈ G, then
    h1 : A ∈ ∆ or h0 : B ∈ Γ.
10. If h2 : A−∗ B ∈ ∆ then ∃h0 , h1 ∈ L s.t. (h1 , h2 ⊲ h0 ) ∈ G, h1 : A ∈ Γ and
    h0 : B ∈ ∆.
11. If h : ∃x.A(x) ∈ Γ then h : A(t) ∈ Γ for some t ∈ T .
12. If h : ∃x.A(x) ∈ ∆ then h : A(t) ∈ ∆ for every t ∈ T .
13. If h : ♦A ∈ Γ then ∃h1 ∈ L s.t. h1 : A ∈ Γ .
14. If h : ♦A ∈ ∆ then ∀h1 ∈ L, h1 : A ∈ ∆.
15. For any t ∈ T , ∃h ∈ L s.t. h : t = t ∈ Γ .
16. If h1 : t = t′ ∈ Γ and h2 : A[t/x] ∈ Γ (h2 : A[t/x] ∈ ∆) then h2 : A[t′ /x] ∈ Γ
    (resp. h2 : A[t′ /x] ∈ ∆).
17. For any label h ∈ L, h ∼ h ∈ G.
18. If h1 ∼ h2 ∈ G and a relational atom or a labelled formula R[h1 /h] ∈ G ∪ Γ (resp.
    R[h1 /h] ∈ ∆), then R[h2 /h] ∈ G ∪ Γ (resp. R[h2 /h] ∈ ∆).
19. If (h1 , h2 ⊲ h0 ) ∈ G then (h2 , h1 ⊲ h0 ) ∈ G.
20. If {(h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h6 ); h1 ∼ h6 } ⊆ G then ∃h5 ∈ L. {(h3 , h5 ⊲ h0 ), (h2 , h4 ⊲
    h5 )} ⊆ G.
21. If {(h1 , h2 ⊲ h0 ); (h3 , h4 ⊲ h9 ); h0 ∼ h9 } ⊆ G then ∃h5 , h6 , h7 , h8 ∈ L s.t. {(h5 , h6 ⊲
    h1 ), (h7 , h8 ⊲ h2 ), (h5 , h7 ⊲ h3 ), (h6 , h8 ⊲ h4 )} ⊆ G.
22. For every abstract points-to predicate k in the language and for any t1 , . . . , t′k ∈ T ,
    ∃h ∈ L s.t. h : t1 k t2 , . . . , tk ∈ Γ .
23. If {h1 : s      ~t, h2 : s    ~t} ⊆ Γ then h1 ∼ h2 ∈ G.
24. If {(h1 , h3 ⊲ h2 ), h1 ∼ h3 } ⊆ G then h1 ∼ ǫ ∈ G.
25. If {(h1 , h2 ⊲ h0 ), (h4 , h5 ⊲ h3 ), h1 ∼ h4 , h2 ∼ h5 } ⊆ G then h0 ∼ h3 ∈ G.
26. If {(h1 ,h2 ⊲ h0 ), (h4 , h5 ⊲ h3 ), h1 ∼ h4 , h0 ∼ h3 } ⊆ G then h2 ∼ h5 ∈ G.

    The next lemma shows that we can build an extended FOASL model (M, ρ)
where M = (D, I, v, F , H, ◦, ǫ) that falsifies the Hintikka sequent G; Γ ⊢ ∆.
The D, I part is a Herbrand model as in first-order logic. The construction of
the monoid (H, ◦, ǫ) is similar to the one for PASL [16], where H is the set of
equivalent classes of labels in the sequent. The interpretation of the predicate
    is defined based the set of functions F . For each n-ary predicate n , there
is a function fn ∈ F defined as below:

         fn (t1 , · · · , tn ) = [h]G iff h′ : t1   n
                                                        t2 , · · · , tn ∈ Γ and h ∼ h′ ∈ G.

where [h]G is the class of labels equivalent to h in G. F is the set of all such
functions. By Condition 22 and 23 of the Hintikka sequent, each function in F
must be a total function. The full proof is in Appendix B.

Lemma 1 (Hintikka’s Lemma). Suppose L is a FOASL language with a non-
empty set of closed terms. Every Hintikka sequent w.r.t. L is falsifiable.

   Then we show how to construct a Hintikka sequent for an unprovable for-
mula using the proof system LSF OASL . Unlike the usual procedure, we have to
consider the rules with no (or more than one) principal formulae. To this end,
we define a notion of extended formulae as in the previous work [16]:

  ExF ::= F | ≡1 | ≡2 | 7→1 | 7→2 | E | A | CS | ≈1 | ≈2 |
              P | C | D

Here, F is a FOASL formula, the other symbols correspond to the special rules in
LSF OASL . For example, ≡1 and ≡2 correspond to rules =1 and =2 ; 7→1 and 7→2
correspond to 1 and 2 ; ≈1 and ≈2 correspond to ∼1 and ∼2 . The saturation
procedure is performed according to a schedule, which is defined below.
Definition 2 (Schedule). A rule instance is a tuple (O, h, ExF, R, S, n), where
O is either 0 (left) or 1 (right), h is a label, ExF is an extended formula, R is
a set of relational atoms such that |R| ≤ 2, S is a set of labelled formulae with
|S| ≤ 2, and n is a natural number. Let I denote the set of all rule instances. A
schedule is a function from natural numbers N to I. A schedule φ is fair if for
every rule instance I, the set {i | φ(i) = I} is infinite.
    It is easy to verify that a fair schedule must exist. This is proved by checking
that I is a countable set [20], which follows from the fact that I is a finite product
of countable sets. We fix a fair schedule φ for the following proofs. We assume
the set L of labels is totally ordered and can be enumerated as h0 , h1 , h2 , · · · ,
where h0 = ǫ. Similarly, we assume an infinite set of closed terms which can
be enumerated as t0 , t1 , t2 , · · · , all of which are disjoint from the terms in F .
Suppose F is an unprovable formula, we start from the sequent ⊢ h1 : F and
construct an underivable sequent as below.

Definition 3. Let F be a formula which is not provable in LSF OASL . We as-
sume that every variable in F is bounded, otherwise we can rewrite F so that
unbounded variables are universally quantified. We construct a series of finite
sequents hGi ; Γi ⊢ ∆i ii∈N from F where G1 = Γ1 = ∅ and ∆1 = a1 : F . Suppose
Gi ; Γi ⊢ ∆i has been defined, we define Gi+1 ; Γi+1 ⊢ ∆i+1 in the sequel. Suppose
φ(i) = (Oi , hi , ExFi , Ri , Si , ni ). When we use ni to select a term (resp. label) in
a formula (resp. relational atom), we assume the terms (resp. labels) are ordered
from left to right. If ni is greater than the number of terms in the formula (labels
in the relational atom), then no effect is taken. We only show a few cases here,
and display this rather involved construction in Appendix B.

 – If Oi = 0, ExFi is a FOASL formula Ci = F1 ∗ F2 and hi : Ci ∈ Γi , then
   Gi+1 = Gi ∪ {(h4i , h4i+1 ⊲ hi )}, Γi+1 = Γi ∪ {h4i : F1 , h4i+1 : F2 }, ∆i+1 = ∆i .
 – If ExFi is ≡1 and Si = {hi : tn = tn }, where n ≤ i + 1, then Gi+1 = Gi ,
   Γi+1 = Γi ∪ {hi : tn = tn }, and ∆i+1 = ∆i .
 – If ExFi is ≡2 and Si = {h : t = t′ , h′ : A[t/x]} ⊆ Γi , where x is the ni th
   term in A, then Gi+1 = Gi , Γi+1 = Γi ∪ {h′ : A[t′ /x]}, and ∆i+1 = ∆i .
 – If ExFi is ≡2 and Si = {h : t = t′ , h′ : A[t/x]} where h : t = t′ ∈ Γi ,
   h′ : A[t/x] ∈ ∆i , and x is the ni th term in A. Then Gi+1 = Gi , Γi+1 = Γi ,
   and ∆i+1 = ∆i ∪ {h′ : A[t′ /x]}.

    The first rule shows how to use the ∗L rule and how to deal with fresh vari-
ables. The indexing of labels guarantees that the choice of h4i , h4i+1 , h4i+2 , h4i+3
are always fresh for the sequent Gi ; Γi ⊢ ∆i . Similarly, the term ti+1 does not
occur in the sequent Gi ; Γi ⊢ ∆i . The second rule generates an identity equality
relation for the term tn . The last two rules find a formula h′ : A in the an-
tecedent and succedent respectively, and replace t with t′ in A. The construction
in Definition 3 non-trivially extends a similar construction of Hintikka CSS due
to Larchey-Wendling [20] and a similar one in [16].
    We also borrow the notions of consistency and finite-consistency from Larchey-
Wendling’s work [20]. We say G ′ ; Γ ′ ⊢ ∆′ ⊆ G; Γ ⊢ ∆ iff G ′ ⊆ G, Γ ′ ⊆ Γ
and ∆′ ⊆ ∆. A sequent G; Γ ⊢ ∆ is finite if G, Γ, ∆ are finite sets. Define
G ′ ; Γ ′ ⊢ ∆′ ⊆f G; Γ ⊢ ∆ iff G ′ ; Γ ′ ⊢ ∆′ ⊆ G; Γ ⊢ ∆ and G ′ ; Γ ′ ⊢ ∆′ is finite. If
G; Γ ⊢ ∆ is a finite sequent, it is consistent iff it does not have a derivation in
LSF OASL . A (possibly infinite) sequent G; Γ ⊢ ∆ is finitely-consistent iff every
G ′ ; Γ ′ ⊢ ∆′ ⊆f G; Γ ⊢ ∆ is consistent.
      We write Li for the set of labels occurring in the sequent Gi ; Γi ⊢ ∆i , and
write Di for the set of terms which are disjoint from those in F in that sequent.
Thus L1 = {a1 } and D1 = ∅. The following lemma states some properties of the
construction of the sequents Gi ; Γi ⊢ ∆i .
Lemma 2. For any i ∈ N , the following properties hold:

 1. Gi ; Γi ⊢ ∆i has no derivation            3. Di ⊆ {t0 , t1 , · · · , ti }
 2. Li ⊆ {a0 , a1 , · · · , a4i−1 }           4. Gi ; Γi ⊢ ∆i ⊆f Gi+1 ; Γi+1 ⊢ ∆i+1

   Given the construction of the series of sequents in Definition 3, we define a
notion of a limit sequent as the union of every sequent in the series.

Definition 4 (Limit sequent). Let F be a formula unprovable in    S LSF OASL .
                                         ω     ω    ω         ω
The limit sequent for F is the sequent G   ; Γ   ⊢ ∆  where G   =  i∈N Gi and
Γ ω = i∈N Γi and ∆ω = i∈N ∆i and where Gi ; Γi ⊢ ∆i is as defined in Def.3.
      S                  S

   The last step is to show that the limit sequent is a Hintikka sequent, which
gives rise to a counter-model of the formula that cannot be proved.

Lemma 3. If F is a formula unprovable in LSF OASL , then the limit sequent
for F is a Hintikka sequent.

    Now we can finish the completeness theorem: whenever a FOASL formula
has no derivation in LSF OASL , there is an infinite counter-model. The theorem
states the contraposition.

Theorem 2 (Completeness). If F is valid in FOASL, then F is provable in
LSF OASL .


5     Theories for 7→ in Separation Logics
Our predicate      admits more interpretations than the standard 7→ predicate in
SL heap model semantics. We can, however, approximate the behaviors of 7→ by
formulating additional properties of 7→ as logical theories. We show next some
of the theories for 7→ arising in various SL semantics.

5.1    Reynolds’s semantics
The 7→ predicate in Reynolds’s semantics can be formalized as follows, where
the store s is a total function from variables to values, and the heap h is a finite
partial function from addresses to values:
                                                                       7→ L1
                                            G; Γ ; ǫ : e1 7→ e2 ⊢ ∆


             (ǫ, h0 ⊲ h0 ); G[ǫ/h1 , h0 /h2 ]; Γ [ǫ/h1 , h0 /h2 ]; h0 : e1 7→ e2 ⊢ ∆[ǫ/h1 , h0 /h2 ]
             (h0 , ǫ ⊲ h0 ); G[ǫ/h2 , h0 /h1 ]; Γ [ǫ/h2 , h0 /h1 ]; h0 : e1 7→ e2 ⊢ ∆[ǫ/h2 , h0 /h1 ]
                                                                                                        7→ L2
                                   (h1 , h2 ⊲ h0 ); G; Γ ; h0 : e1 7→ e2 ⊢ ∆

                                                            7→ L3              G; Γ θ; h : e1 θ 7→ e2 θ ⊢ ∆θ
                                                                                                                   7→ L4
 (h1 , h2 ⊲ h0 ); G; Γ ; h1 : e 7→ e1 ; h2 : e 7→ e2 ⊢ ∆                 G; Γ ; h : e1 7→ e2 ; h : e3 7→ e4 ⊢ ∆


  G[h1 /h2 ]; Γ [h1 /h2 ]; h1 : e1 7→ e2 ⊢ ∆[h1 /h2 ]                  (h1 , h0 ⊲ h2 ); G; Γ ; h1 : e1 7→ e2 ⊢ ∆
                                                           7→ L5                                                      HE
       G; Γ ; h1 : e1 7→ e2 ; h2 : e1 7→ e2 ⊢ ∆                                         G; Γ ⊢ ∆
Side conditions:
Each label being substituted cannot be ǫ.                             In 7→ L4 , θ = mgu({(e1 , e3 ), (e2 , e4 )}).
In HE, h0 occurs in conclusion, h1 , h2 , e1 are fresh.

                                   Fig. 3. Points-to rules in LSSL .


                  s, h      x 7→ y iff dom(h) = {s(x)} and h(s(x)) = s(y).

   Here we tackle the problem indirectly from the abstract separation logic angle.
We give the following theories to approximate the semantics of 7→ in SL:

 1. ∀e1 , e2 .(e1 7→ e2 )∧⊤∗ → ⊥                 2. ∀e1 , e2 .(e1 7→ e2 ) → ¬(¬⊤∗ ∗ ¬⊤∗ )
 3. ∀e1 , e2 , e3 , e4 .(e1 7→ e2 ) ∗ (e3 7→ e4 ) → ¬(e1 = e3 )
 4. ∀e1 , e2 , e3 , e4 .(e1 7→ e2 ) ∧ (e3 7→ e4 ) → (e1 = e3 ) ∧ (e2 = e4 )
 5. ∃e1 ∀e2 .¬((e1 7→ e2 )−∗ ⊥)                  6. ∀e1 , e2 .(e1 7→ e2 ) → (e1  e2 )

Note that the opposite direction (e1      e2 ) → (e1 7→ e2 ) does not necessarily
hold because      is weaker than 7→. The above theories intend to capture the
inference rules for 7→ in LSSL [17], the captured rules are given in Figure 3.
The first five formulae simulate the rules 7→ L1 , 7→ L2 , 7→ L3 , 7→ L4 , and HE
respectively. The rule 7→ L5 can be derived by 2 and Formula 6.

Lemma 4. The inference rules in Figure 3 are admissible in LSF OASL when
Formula 1 ∼ 6 are assumed true.

   The validity of Formula 1 to 6 w.r.t. Reynolds’s SL model is easy to check,
the rationale is similar to the soundness of corresponding rules in LSSL [17].
Therefore Reynolds’s SL is an instance of our logic.

Lemma 5. Formula 1 ∼ 6 are valid in Reynolds’s SL semantics.

   The rules in Figure 3 cover most of the rules for 7→ in LSSL [17], but we have
not found a way to handle the following rule (with two premises):
                                       (h1 , h2 ⊲ h0 ); G; Γ ⊢ ∆
          (h3 , h4 ⊲ h1 ); (h5 , h6 ⊲ h2 ); G; Γ ; h3 : e1 7→ e2 ; h5 : e1 7→ e3 ⊢ ∆
                                                                                     HC
                                            G; Γ ⊢ ∆
The rule HC effectively picks two arbitrary heaps h1 and h2 , and does a case
split of whether they can be combined or not. This rule seems to require more
expressiveness than our logic. However, the above formulae cover most of prop-
erties about 7→ that existing tools for SL can handle, including the treatments
in [17] and those for symbolic heaps [2].


5.2     Vafeiadis and Parkinson’s SL

Vafeiadis and Parkinson’s SL [34] is almost the same as Reynolds’s definition,
but they only consider values as addresses. This is a common setting in many
applications, such as [14]. In this setting, the following formula is valid: ⊤∗ →
¬((e1 7→ e2 )−∗ ¬(e1 7→ e2 )). This formula, however, is invalid in Reynolds’s SL.
Obviously Formula 1 to 6 are valid in Vafeiadis and Parkinson’s SL, thus their
logic is also an instance of our abstract logic. To cater for the special feature, we
propose a formula for “total addressability”:

 7. ∀e1 , e2 .♦(e1 7→ e2 )

    This formula ensures that there must exist a heap (e1 7→ e2 ) no matter what
values e1 , e2 have. This is sound because in Vafeiadis and Parkinson’s SL, e1
must denote a valid address, thus h with dom(h) = {s(e1 )} and h(s(e1 )) = s(e2 ),
where s is the store, must be a legitimate function, which by definition is a heap.


5.3     Lee et al.’s SL

Lee et al.’s proof system for SL corresponds to a non-standard semantics (al-
though they used Reynolds’s semantics in their paper) [24]. While there is not a
reference of a formal definition of their non-standard semantics, their inference
rule −∗ Disj suggests that they forbid “incompatible heaps”. For example, if
there exists a heap e1 7→ e2 , then there shall not exist another heap (e1 7→ e3 ),
where e2 6= e3 . Their −∗ Disj rule can help derive the following formula, which
is invalid in Reynolds’s SL:

   (((e1 7→ e2 ) ∗ ⊤)−∗ ⊥) ∨ (((e1 7→ e3 ) ∗ ⊤)−∗ ¬((e1 7→ e2 )−∗ ⊥)) ∨ (e2 = e3 )

   If we assume that the above non-standard semantics conform with Reynolds’s
SL in other aspects (as validated by Formula 1 to 6), then it can be seen as a
special instance of our abstract logic. The compatibility property can then be
formulated as follows:

 8. ∀e1 , e2 .♦(e1 7→ e2 ) → ¬(∃e3 .¬(e2 = e3 ) ∧ ♦(e1 7→ e3 ))

      With Formula 8 we can prove the invalid formula above.
5.4   Thakur et al.’s SL

There are SL variants that forbid heaps with cyclic lists, for example, the one
defined by Thakur et al. [32]. Consequently, the following two formulae are un-
satisfiable in their SL:

                       e1 7→ e1                e1 7→ e2 ∗ e2 7→ e1

To formulate this property, we first define a notion of a path:

        ∀e1 , e2 .(path(e1 , e2 ) ≡ e1 7→ e2 ∨ (∃e3 .(e1 7→ e3 ) ∗ path(e3 , e2 )))

where ≡ denotes logical equivalence (bi-implication). Now the property of “acy-
clism” can be formulated as

 9. ∀e1 , e2 .(path(e1 , e2 ) → e1 6= e2 )

which renders cyclic paths unsatisfiable in our logic, too. Note that since our
proof system does not support inductive definitions, we cannot force the in-
terpretation of path to be the least fixed point of its definition. We leave the
incorporation of inductive definitions to future work.


6     Implementation and Experiment

Our theorem prover for FOASL extends our previous prover for Reynolds’s
SL [17] with the ability to handle (non-inductive) predicates and modalities. To
speed up proof search, instead of implementing =2 and ∼2 , we use the following
rules:
                 G; Γ [s/t] ⊢ ∆[s/t] ′               Gθ; Γ θ ⊢ ∆θ
                                     =2                              ∼′2
                 G; h : s = t; Γ ⊢ ∆              h1 ∼ h2 ; G; Γ ⊢ ∆

              where θ = [h1 /h2 ] if h2 6= ǫ and θ = [h2 /h1 ] otherwise.

These two rules can be shown to be interchangeable with =2 and ∼2 . One di-
rection, i.e., showing that =′2 and ∼′2 can be derived in FOASL, is straightfor-
ward. The other direction requires some further justification. Let LSF′ OASL be
LSF OASL with =2 and ∼2 replaced by =′2 and ∼′2 respectively, we then need to
show that =2 and ∼2 are admissible in LSF′ OASL . To prove this, we follow a sim-
ilar proof for free-equality rules for first-order terms by Schroeder-Heister [31].
The key part in that proof is in showing that provability is closed under sub-
stitutions. In our setting, we need to show that LSF′ OASL is closed under both
term substitutions and label substitutions, which are stated below.

Lemma 6. If G; Γ ⊢ ∆ is derivable in LSF′ OASL , then so is G; Γ [s/t] ⊢ ∆[s/t]
for any terms s and t.

Lemma 7. If G; Γ ⊢ ∆ is derivable in LSF′ OASL , then so is G[h1 /h2 ]; Γ [h1 /h2 ] ⊢
∆[h1 /h2 ] for any label h1 and label variable h2 .
        Formula                                                               Time
   1    ((⊤−∗ (((k 7→ c, d)−∗ (l 7→ a, b)) → (l 7→ a, b))) → (l 7→ a, b))     < 0.001s
   2    ((∃x2 .((∃x1 .((x2 7→ x1 , b) → ⊥)) → ⊥)) → (∃x3 .(x3 7→ a, b)))      < 0.001s
   3    (((⊤∗ → ⊥) → ⊥) → ((∃x1 .((x1 7→ a, b) ∗ ⊤)) → ⊥))                    < 0.001s
   4    ((∃x3 x2 x1 .(((x3 7→ a, x2 ) ∗ (x1 7→ c, d)) ∧ x2 = x1 )) →
        (∃x5 x4 .((x4 7→ c, d) ∗ (x5 7→ a, x4 ))))                            < 0.001s
   5    ((((e1 7→ e2 ) ∗ ⊤) ∧ (((e3 7→ e4 ) ∗ ⊤)∧
        (((e5 7→ e6 ) ∗ ⊤) ∧ (¬(e1 = e3 ) ∧ (¬(e1 = e5 ) ∧ ¬(e3 = e5 )))))) →
        (((e1 7→ e2 ) ∗ ((e3 7→ e4 ) ∗ (e5 7→ e6 ))) ∗ ⊤))                    0.9s
   6    ((((e1 7→ e2 ) ∗ ¬((e3 7→ e4 ) ∗ ⊤)) ∧ ((e3 7→ e4 ) ∗ ⊤)) → e1 = e3 ) < 0.001s
   7    ¬((¬⊤∗ ∗ ¬⊤∗ )−∗ ⊥)                                                   0.0015s
   8    ((¬(((l1 7→ p) ∗ (l2 7→ q))−∗ (¬(l3 7→ r)))) →
        (¬((l1 7→ p)−∗ (¬(¬((l2 7→ q)−∗ (¬(l3 7→ r))))))))                    < 0.001s
   9    ((¬((l1 7→ p)−∗ (¬(¬((l2 7→ q)−∗ (¬(l3 7→ r))))))) →
        (¬(((l1 7→ p) ∗ (l2 7→ q))−∗ (¬(l3 7→ r)))))                          < 0.001s
   10   ((¬((lx 7→ ly)−∗ (¬((l1 7→ p) ∗ (l2 7→ q))))) →
        (¬((¬((¬((lx 7→ ly)−∗ (¬(l1 7→ p)))) ∗ ((l2 7→ q)∧
        (¬(∃x1 .((lx 7→ x1 ) ∗ ⊤)))))) ∧ (¬((¬((lx 7→ ly)−∗
        (¬(l2 7→ q)))) ∗ ((l1 7→ p) ∧ (¬(∃x2 .((lx 7→ x2 ) ∗ ⊤)))))))))       < 0.001s
   11   ((∀x2 x1 .♦(x2 7→ x1 )) → (⊤∗ → ¬((e1 7→ e2 )−∗ ¬(e1 7→ e2 ))))       < 0.001s
   12   ((∀x3 x2 .(♦(x3 7→ x2 ) → ¬(∃x1 .(¬(x2 = x1) ∧ ♦(x3 7→ x1 ))))) →
        ((((e1 7→ e2 ) ∗ ⊤)−∗ ⊥) ∨ ((((e1 7→ e3 ) ∗ ⊤)−∗ ¬((e1 7→ e2 )−∗ ⊥))
        ∨e2 = e3 )))                                                          0.0025s

                     Table 2. Experiment on selected formulae.

    Note that by restricting h2 to a label variable, we forbid ǫ to be substituted
in the above lemma. These two lemmas require induction on the height of deriva-
tions, and routine checks confirm that they both hold. Then it is a corollary that
=2 and ∼2 are admissible in LSF′ OASL .
    Since the heap model is widely used, our prover also includes useful rules
to reason in the heap model, such as the derived rules in Figure 3. But we
currently have not included the HC rule in our proof search procedure. Since
many applications of SL involve reasoning about invalid addresses, such as nil,
we also add a theory to capture a simple aspect of the invalid address nil:

10. ∀~e.(nil 7→ ~e) → ⊥

Since the current prover is an extension of our previous prover, it builds in the
inference rules for linked lists and binary trees for reasoning about the symbolic
heap fragment of SL. It is also capable of proving theorems used in verification
of a tail-recursive append function [25], as shown in [17]. However, we do not
exploit these aspects here.
    We illustrate a list of formulae provable by our prover in Table 2. Formulae
1 to 4 are examples drawn from Galmiche and Méry’s work on resource graph
tableaux for SL [15]. Formula 5 is a property about overlaid data structures: if
the current heap contains (e1 7→ e2 ) and (e3 7→ e4 ) and (e5 7→ e6 ), and they are
pairwise distinct, then the current heap contains the combination of the three
heaps. Formula 6 says that if the current heap can be split into two parts, one is
(e1 7→ e2 ) and the other part does not contain (e3 7→ e4 ), and the current heap
contains (e3 7→ e4 ), then we deduce that (e3 7→ e4 ) and (e1 7→ e2 ) must be the
same heap, therefore e1 = e3 . Formula 7 says that any heap can be combined with
a composite heap. We give a derivation of formula 7 in Appendix C. Formulae
8 to 10 are properties of “septraction” in SL with Rely-Guarantee [34]. Finally,
formulae 11 and 12 show that our prover can easily support reasoning about
Vafeiadis and Parkinson’s SL (cf. Section 5.2) and Lee et al.’s SL (cf. Section 5.3)
by simply adding the corresponding theories as assumptions. This is a great
advantage over our previous work where new rules have to be implemented to
extend the ability of the prover. To our knowledge most existing provers for
SL cannot prove the formulae in Table 2. Examples of larger formulae used in
program verification can be found in the experiment of our previous prover [17],
upon which this prover is built.


7    Conclusion
This paper presents a first-order abstract separation logic with modalities. This
logic is rich enough to express formulae in real-world applications such as pro-
gram verification. We give a sound and complete labelled sequent calculus for
this logic. The completeness of the finite calculus implies that our logic is recur-
sively enumerable. To deal with 7→, we give a set of formulae to approximate the
semantics of memory model. Of course, we cannot fully simulate 7→, but we can
handle most properties about 7→ compared with existing tools for SL. Moreover,
we can prove numerous formulae that many existing tools for SL cannot handle.
The techniques discussed in this paper are demonstrated in a rather flexible theo-
rem prover which supports automated reasoning in different SL variants without
any change to the implementation. With this foundation, one can simply add
formulae as “assumption”, and prove theorems that cannot be proved in the
base logic.


Acknowledgments
This research is supported by the National Research Foundation, Prime Minis-
ter’s Office, Singapore under its National Cybersecurity R&D Program (Award
No. NRF2014NCR-NCR001-30) and administered by the National Cybersecurity
R&D Directorate.


References
 1. Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Smallfoot: Modular
    automatic assertion checking with separation logic. In FMCO, pages 115–137.
    Springer, 2005.
 2. Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic execution
    with separation logic. In APLAS, volume 3780, pages 52–68, 2005.
 3. Rémi Brochenin, Stphane Demri, and Etienne Lozes. On the almighty wand. In-
    form. and Comput., 211:106–137, 2012.
 4. Stephen Brookes. A semantics for concurrent separation logic. Theor. Comput.
    Sci., 375(1-3):227–270, April 2007.
 5. James Brotherston. A unified display proof theory for bunched logic. ENTCS,
    265:197–211, September 2010.
 6. James Brotherston, Dino Distefano, and Rasmus Lerchedahl Petersen. Automated
    cyclic entailment proofs in separation logic. In CADE, pages 131–146, 2011.
 7. James Brotherston and Max Kanovich. Undecidability of propositional separation
    logic and its neighbours. Journal of ACM, 2014.
 8. James Brotherston and Jules Villard. Parametric completeness for separation the-
    ories. In POPL, pages 453–464. ACM, 2014.
 9. Cristiano Calcagno, Peter W. O’Hearn, and Hongseok Yang. Local action and
    abstract separation logic. In LICS, pages 366–378. IEEE, 2007.
10. Cristiano Calcagno, Hongseok Yang, and Peter W. O’Hearn. Computability and
    complexity results for a spatial assertion language for data structures. In FSTTCS,
    volume 2245 of LNCS, pages 108–119, 2001.
11. Stéphane Demri and Morgan Deters. Expressive completeness of separation logic
    with two variables and no separating conjunction. In CSL/LICS, 2014.
12. Stéphane Demri, Didier Galmiche, Dominique Larchey-Wendling, and Daniel Mèry.
    Separation logic with one quantified variable. In CSR. LNCS 8476, 2014.
13. Robert Dockins, Aquinas Hobor, and Andrew W. Appel. A fresh look at separation
    algebras and share accounting. In APLAS, volume 5904, pages 161–177, 2009.
14. Dider Galmiche, Daniel Méry, and David Pym. The semantics of BI and resource
    tableaux. MSCS, 15(6):1033–1088, December 2005.
15. Didier Galmiche and Daniel Méry. Tableaux and resource graphs for separation
    logic. J. Logic Comput., 20(1):189–231, 2010.
16. Zhé Hóu, Ranald Clouston, Rajeev Goré, and Alwen Tiu. Proof search for propo-
    sitional abstract separation logics via labelled sequents. In POPL, 2014.
17. Zhé Hóu, Rajeev Goré, and Alwen Tiu. Automated theorem proving for assertions
    in separation logic with all connectives. In CADE, 2015.
18. Jonas B. Jensen and Lars Birkedal. Fictional separation logic. In ESOP, volume
    7211 of LNCS, pages 377–396, 2012.
19. Neelakantan R. Krishnaswami. Reasoning about iterators with separation logic. In
    SAVCBS, pages 83–86. ACM, 2006.
20. Dominique Larchey-Wendling. The formal strong completeness of partial monoidal
    Boolean BI. JLC, 2014.
21. Dominique Larchey-Wendling and Didier Galmiche. Exploring the relation between
    intuitionistic BI and Boolean BI: An unexpected embedding. MSCS, 19(3):435–500,
    2009.
22. Dominique Larchey-Wendling and Didier Galmiche. The undecidability of Boolean
    BI through phase semantics. LICS, 0:140–149, 2010.
23. Dominique Larchey-Wendling and Didier Galmiche. Looking at separation algebras
    with Boolean BI-eyes. TCS, 2014.
24. Wonyeol Lee and Sungwoo Park. A proof system for separation logic with magic
    wand. In POPL, pages 477–490. ACM, 2014.
25. Toshiyuki Maeda, Haruki Sato, and Akinori Yonezawa. Extended alias type system
    using separating implication. In TLDI, pages 29–42. ACM, 2011.
26. Juan Antonio Navarro Pérez and Andrey Rybalchenko. Separation logic + super-
    position calculus = heap theorem prover. In PLDI. ACM, 2011.
27. Peter W. O’Hearn and David J. Pym. The logic of bunched implications. BSL,
    5(2):215–244, 1999.
28. Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. Local reasoning about
    programs that alter data structures. In CSL, pages 1–19, 2001.
29. Jonghyun Park, Jeongbong Seo, and Sungwoo Park. A theorem prover for Boolean
    BI. In POPL, POPL ’13, pages 219–232, New York, NY, USA, 2013.
30. John C. Reynolds. Separation logic: A logic for shared mutable data structures.
    In LICS, pages 55–74. IEEE, 2002.
31. Peter Schroeder-Heister. Definitional reflection and the completion, pages 333–347.
    Springer, 1994.
32. Aditya Thakur, Jason Breck, and Thomas Reps. Satisfiability modulo abstraction
    for separation logic with linked lists. SPIN 2014, pages 58–67, 2014.
33. Anne S. Troelstra and Helmut Schwichtenberg. Basic Proof Theory. 1996.
34. Viktor Vafeiadis and Matthew Parkinson. A marriage of rely/guarantee and sepa-
    ration logic. In CONCUR, volume 4703 of LNCS, 2007.
A    Soundness of LSF OASL

Theorem 1. For every FOASL formula F , if ⊢ h : F is derivable in LSF OASL
for any label h, then F is a valid FOASL formula.

Proof. The soundness of most rules in LSF OASL is analogous to the same rules
in LSP ASL [16]. Here we only show the rules ∃L, ∃R, ♦L, ♦R, 1 , and 2 . We
prove the soundness of the rules by showing that if the conclusion is falsifiable,
then at least one premise is falsifiable.

∃L: Assume the conclusion is falsifiable in an extended model (M, ρ), we have
     M, v, ρ(h)      ∃x.A. So there is an element in D such that by mapping x
     to that element, A is true at h. However, our valuation function v may not
     mention this element at all. We pick y as that element, and let v map x to
     y. Since y does not occur in the conclusion, this does not affect any existing
     mappings in v. Thus the mapping for all other variables remain the same,
     and the truth value of the reminder of the sequent does not change. With
     the extended valuation, A[y/x] is true at ρ(h), and the premise is falsifiable.
∃R: Assume the conclusion is falsifiable in an extended model (M, ρ), then h :
     ∃x.A is false. That is, M, v, ρ(h) 6 ∃x.A, which means M, v, ρ(h) ∀x.¬A.
     So there are no elements in D that could possibly make A true at ρ(h).
     Therefore no matter what y is, A[y/x] is false at ρ(h). So M, v, ρ(h) 6 A[y/x].
     Hence the premise is falsifiable.
♦L: If the conclusion is falsifiable in some extended model (M, ρ), we have
     M, v, ρ(h)      ♦A. Thus there exists a world in H such that A under the
     valuation of v is true at that world. Let ρ be extended with a fresh label h′
     that maps to that world. This will not change the existing label mappings.
     Then we have M, v, ρ(h′ ) A. Thus the premise is falsifiable.
♦R: If the conclusion is falsifiable in some extended model (M, ρ), then M, v, ρ(h) 6
     ♦A. This is equivalent to ∀w ∈ H.M, v, w 6 A. So for any mapping ρ and
     any label h′ , M, v, ρ(h′ ) 6 A. We have that h′ : A is false in the premise,
     thus the premise is falsifiable.
  1 : Suppose the conclusion is falsifiable in some extended model (M, ρ). Sup-
     pose f is the semantic function associated with . Since f is a total function,
     and the domain is non-empty, for any terms s, ~t, there exists h′ ∈ H such
     that f(sM , ~tM ) = h′ . Let ρ′ be a label mapping such that ρ′ (h) = h′ and
     ρ′ (h1 ) = ρ(h1 ) for any h1 6= h. Since h does not occur in the conclusion
     sequent, we have that (M, ρ′ ) satisfies all labelled formulae and relational
     atoms in the antecedent of the premise, and falsifies every formula in the
     succedent of the premise. Hence the premise is also fasifiable.
  2 If the conclusion is falsifiable in some extended model (M, ρ), then both
    :
     M, v, ρ(h1 ) s       ~t and M, v, ρ(h2 ) s     ~t hold. By the semantics of ,
     we have ρ(h1 ) = ρ(h2 ). Thus ǫ ◦ ρ(h1 ) = ρ(h2 ) holds, and (M, ρ) satisfies
     h1 ∼ h2 . So the premise is also falsifiable.                                ⊓
                                                                                  ⊔
B    Completeness of LSF OASL

Lemma 1. Suppose L is a FOASL language with a non-empty set of closed
terms. Every Hintikka sequent w.r.t. L is falsifiable.

Proof. Let G; Γ ⊢ ∆ be a Hintikka sequent w.r.t. L. We construct an extended
model (M, ρ) where M = (D, I, v, F , H, ◦, ǫ).
   The first order component (D, I) is a Herbrand model. That is,

 – D is exactly the non-empty set of closed terms of L.
 – For each constant symbol c in L, cI = c.

It is then easy to verify that for each closed term t, tI = t. As in the first order
logic convention, the reminder of this proof will be confined to sentences and
closed terms, so the valuation function v does not matter here.
    The interpretation of the equality symbol = is as follows:
                      (
                         is true if h : t1 = t2 ∈ Γ for some h ∈ L;
              t1 = t2
                         is false otherwise.

We show that = is indeed an equivalence relation:

Reflexivity: For any closed term t ∈ D, by condition 15 of Definition 1, ∃h ∈ L
   such that h : t = t ∈ Γ . Thus t = t.
Symmetry: Suppose t1 = t2 holds, then there is some h ∈ L such that h : t1 =
   t2 ∈ Γ . By reflexivity, t1 = t1 holds, and h′ : t1 = t1 ∈ Γ for some h′ ∈ L.
   Consider h′ : t1 = t1 as an instance of h′ : x = t1 [t1 /x], Condition 16 in
   Definition 1 guarantees that h′ : t2 = t1 ∈ Γ . Thus t2 = t1 .
Transitivity: Suppose t1 = t2 and t2 = t3 both hold. There must be some
   h, h′ ∈ L such that {h : t1 = t2 , h′ : t2 = t3 } ⊆ Γ . Since h : t1 = t2 is an
   instance of h : t1 = x[t2 /x], by condition 16 in Definition 1, h : t1 = t3 ∈ Γ ,
   thus t1 = t3 .

    Similarly, the relation ∼ on labels is also an equivalence relation. Given a set
of relational atoms G, the relation ∼ partitions the set L of labels into equivalence
classes [h]G for each label a ∈ L:

                               [h]G = {h′ ∈ L | h ∼ h′ ∈ G}.

    The other components of the extended model are defined as:

 – H = {[h]G | h ∈ L}.
 – [h1 ]G ◦ [h2 ]G = [h0 ]G iff ∃h′0 , h′1 , h′2 s.t. {(h′1 , h′2 ⊲ h′0 ); h0 ∼ h′0 ; h1 ∼ h′1 ; h2 ∼
   h′2 } ⊆ G.
 – ǫ = [ǫ]G .
 – ρ(h) = [h]G for every h ∈ L.
    The interpretation of the predicate    is defined based the set of functions
F . For each n-ary predicate n , there is a function fn ∈ F defined as below:

                    fn (t1 , · · · , tn ) = [h]G iff h′ : t1 n t2 , · · · tn ∈ Γ
                                                      and h ∼ h′ ∈ G.

F is the set of all such functions. By Condition 22 and 23, each function in F
must be a total function.
   Finally, the interpretation for the other relation symbols are given below:
 – For each n-ary relation symbol R in L and n closed terms t1 , · · · , tn in D,
   RI (t1 , · · · , tn ) holds in the world [h]G ∈ H iff h′ : R(t1 , · · · , tn ) ∈ Γ and
   h ∼ h′ ∈ G.
    In the following we will drop the subscript G in [h]G for readability. It can be
checked that conditions 17, 19, 20, 21 in Definition 1 ensure identity, commuta-
tivity, associativity, and cross-split respectively in the semantics. Furthermore,
disjointness, partial-determinism, cancellativity are covered by Condition 24, 25,
26 respectively. Condition 24 also implies indivisible unit. A similar proof to
these can be found in [16]. Here we give three cases that are not considered in
the previous work.
Cross-split: Assume [h1 ] ◦ [h2 ] = [h0 ] and [h3 ] ◦ [h4 ] = [h0 ] hold. By the above
   construction, there must be some (h′1 , h′2 ⊲ h′0 ) ∈ G and (h′3 , h′4 ⊲ h′′0 ) ∈ G
   such that [h1 ] = [h′1 ], [h2 ] = [h′2 ], [h3 ] = [h′3 ], [h3 ] = [h′4 ], and [h0 ] = [h′0 ] =
   [h′′0 ] hold. This means that h′0 ∼ h′′0 ∈ G. By condition 21 in Definition 1,
   there exist h5 , h6 , h7 , h8 ∈ L such that {(h5 , h6 ⊲ h′1 ), (h7 , h8 ⊲ h′2 ), (h5 , h7 ⊲
   h′3 ), (h6 , h8 ⊲ h′4 )} ⊆ G. Again, by construction of the model, we have [h5 ] ◦
   [h6 ] = [h′1 ], [h7 ] ◦ [h8 ] = [h′2 ], [h5 ] ◦ [h7 ] = [h′3 ], [h6 ] ◦ [h8 ] = [h′4 ], from which
   we obtain the cross-split property in the semantics.
Disjointness: For any two worlds [h1 ], [h2 ] ∈ H, if [h1 ] ◦ [h1 ] = [h2 ], then there
   must be some (h′1 , h′′1 ⊲ h′2 ) ∈ G such that [h1 ] = [h′1 ] = [h′′1 ] and [h2 ] = [h′2 ],
   hence h′1 ∼ h′′1 ∈ G. By Condition 24, h′1 ∼ ǫ ∈ G. Since ∼ is an equivalence
   relation, we have h1 ∼ ǫ.
Indivisible unit: This is a direct consequence of disjointness [23].

    Therefore the (H, ◦, ǫ) part of the extended model is indeed a separation
algebra as defined in Section 2. The reminder of this proof shows that the Hin-
tikka sequent G; Γ ⊢ ∆ is falsifiable in the constructed model, this includes the
following:

 – If (h1 , h2 , ⊲h0 ) ∈ G then [h1 ] ◦ [h2 ] = [h0 ].
 – If h : A ∈ Γ then M, v, [h] A.
 – If h : A ∈ ∆ then M, v, [h] 6 A.
The first item follows from the construction of the model. In the sequel we show
the last two items simultaneously by induction on the size of sentence A.
Base cases:
 – Suppose an atomic labelled formula h : R(t1 , · · · , tn ) is in Γ . We must show
   that (tM                 M      I
               1 , · · · , tn ) ∈ R in the world [h]. Since R(t1 , · · · , tn ) is a sentence,
   t1 , · · · , tn are closed terms. Thus each tM     i   is actually tIi , which equals ti .
                                              I
   By the definition of our model, R (t1 , · · · , tn ) holds in the world [h]. So
   M, v, [h] R(t1 , · · · , tn ) regardless of the valuation function v.
 – Suppose h : R(t1 , · · · , tn ) ∈ ∆, we show that M, v, h 6 R(t1 , · · · , tn ). As-
   sume the opposite, i.e., RI (t1 , · · · , tn ) is true in [h], then there must be some
   h′ : R(t1 , · · · , tn ) ∈ Γ and h ∼ h′ ∈ G. But this contradicts condition 1 in
   Definition 1. Thus M, v, h 6 R(t1 , · · · , tn ).

    Note that the cases for       are just special cases of the above by the definition
    of f ∈ F .
Inductive cases: We do a case analysis on the main connective/quantifier/modality
of the sentence A. The cases for connectives in propositional abstract separation
logic are proved in [16]. Here we show the cases for ∃, ♦, which correspond to
conditions 11, 12, 13, 14 respectively in Definition 1.
 – If h : ∃x.A(x) ∈ Γ , then h : A(t) ∈ Γ for some closed term t in L. Since
   D is the set of closed terms in L, there exists some t ∈ D such that when
   the valuation function v maps x to t, we have M, v[t/x], [h] A(x) by the
   induction hypothesis. Thus M, v, [h] ∃x.A(x).
 – If h : ∃x.A(x) ∈ ∆, then h : A(t) ∈ ∆ for every closed term t ∈ L. Since
   D is the set of closed terms in L, for any t ∈ D, if the valuation function
   v maps x to t, we have M, v[t/x], [h] 6 A(x) by the induction hypothesis.
   Thus M, v, [h] 6 ∃x.A(x).
 – If h : ♦A ∈ Γ , then ∃h′ ∈ L such that h′ : A ∈ Γ . By the induction hypothe-
   sis, there is some [h′ ] ∈ H such that M, v, [h′ ] A. Therefore M, v, [h] ♦A.
 – If h : ♦A ∈ ∆, then ∀h′ ∈ L, h′ : A ∈ ∆. By the induction hypothesis,
   M, v, [h′ ] 6 A for any [h′ ] ∈ H. So M, v, [h] 6 ♦A.                      ⊓
                                                                              ⊔


Definition 3. Let F be a formula which is not provable in LSF OASL . We as-
sume that every variable in F is bounded, otherwise we can rewrite F so that
unbounded variables are universally quantified. It can be checked that this will
not affect the validity of the formula. We construct a series of finite sequents
hGi ; Γi ⊢ ∆i ii∈N from F where G1 = Γ1 = ∅ and ∆1 = a1 : F . Suppose
Gi ; Γi ⊢ ∆i has been defined, we define Gi+1 ; Γi+1 ⊢ ∆i+1 in the sequel. Sup-
pose φ(i) = (Oi , hi , ExFi , Ri , Si , ni ). When we use ni to select a term (resp.
label) in a formula (resp. relational atom), we assume the terms (resp. labels)
are ordered from left to right. If ni is greater than the number of terms in the
formula (labels in the relational atom), then no effect is taken.

 – If Oi = 0, ExFi is a FOASL formula Ci and hi : Ci ∈ Γi :
     • If Ci = F1 → F2 . If there is no derivation for Gi ; Γi ⊢ hi : F1 ; ∆i then
       Γi+1 = Γi , ∆i+1 = ∆i ∪ {hi : F1 }. Otherwise Γi+1 = Γi ∪ {hi : F2 },
       ∆i+1 = ∆i . In both cases, Gi+1 = Gi .
    • If Ci = ⊤∗ , then Gi+1 = Gi ∪ {(ǫ, hi ⊲ ǫ)}, Γi+1 = Γi , ∆i+1 = ∆i .
    • If Ci = F1 ∗ F2 , then Gi+1 = Gi ∪ {(h4i , h4i+1 ⊲ hi )}, Γi+1 = Γi ∪ {h4i :
      F1 , h4i+1 : F2 }, ∆i+1 = ∆i .
    • If Ci = F1 −∗ F2 and Ri = {(h, hi ⊲ h′′ )} ⊆ Gi . If Gi ; Γi ⊢ h : F1 ; ∆i
      has no derivation, then Γi+1 = Γi , ∆i+1 = ∆i ∪ {h : F1 }. Otherwise
      Γi+1 = Γi ∪ {h′′ : F2 }, ∆i+1 = ∆i . In both cases, Gi+1 = Gi .
    • If Ci = ∃x.F (x), then Gi+1 = Gi , Γi+1 = Γi ∪ {hi : F (ti+1 )}, and
      ∆i+1 = ∆i .
    • If Ci = ♦F , then Gi+1 = Gi , Γi+1 = Γi ∪ {h4i : F }, and ∆i+1 = ∆i .
– If Oi = 1, ExFi is a FOASL formula Ci , and hi : Ci ∈ ∆:
    • If Ci = F1 → F2 , then Γi+1 = Γ ∪ {hi : F1 }, ∆i+1 = ∆i ∪ {hi : F2 }, and
      Gi+1 = Gi .
    • Ci = F1 ∗ F2 and Ri = {(h, h′ ⊲ hi )} ⊆ Gi . If Gi ; Γi ⊢ h : F1 ; ∆i has no
      derivation, then ∆i+1 = ∆i ∪ {h : F1 }. Otherwise ∆i+1 = ∆i ∪ {h′ : F2 }.
      In both cases, Gi+1 = Gi and Γi+1 = Γi .
    • If Ci = F1 −∗ F2 , then Gi+1 = Gi ∪ {(h4i , hi ⊲ h4i+1 )}, Γi+1 = Γi ∪ {h4i :
      F1 }, and ∆i+1 = ∆i ∪ {h4i+1 : F2 }.
    • If Ci = ∃x.F (x) and Si = {hi : tn = tn }, where n ≤ i+1, then Gi+1 = Gi ,
      Γi+1 = Γi , ∆i+1 = ∆i ∪ {hi : F (tn )}.
    • If Ci = ♦F and Ri = {(hn , ǫ ⊲ hn )}, where n ≤ 4i + 3, then Gi+1 = Gi ,
      Γi+1 = Γi , and ∆i+1 = ∆i ∪ {hn : F }.
– If ExFi ∈ {≡1 , ≡2 , 7→1 , 7→2 , E, A, CS, ≈1 , ≈2 , P, C, D}, we proceed as follows:
    • If ExFi is ≡1 and Si = {hi : tn = tn }, where n ≤ i + 1, then Gi+1 = Gi ,
      Γi+1 = Γi ∪ {hi : tn = tn }, and ∆i+1 = ∆i .
    • If ExFi is ≡2 and Si = {h : t = t′ , h′ : A[t/x]} ⊆ Γi , where x is the ni th
      term in A, then Gi+1 = Gi , Γi+1 = Γi ∪ {h′ : A[t′ /x]}, and ∆i+1 = ∆i .
    • If ExFi is ≡2 and Si = {h : t = t′ , h′ : A[t/x]} where h : t = t′ ∈ Γi ,
      h′ : A[t/x] ∈ ∆i , and x is the ni th term in A. Then Gi+1 = Gi , Γi+1 = Γi ,
      and ∆i+1 = ∆i ∪ {h′ : A[t′ /x]}.
    • If ExFi is 7→1 and Si = {hi : e1              ~e} where {e1 , ~e} ⊆ {t1 , · · · , ti+1 }.
      Then Gi+1 = Gi , Γi+1 = Γi ∪ {h4i : e1            ~e}, and ∆i+1 = ∆i .
    • If ExFi is 7→2 and Si = {h : s              ~e, h′ : s     ~e} ⊆ Γi , then Gi+1 =
      Gi ∪ {h ∼ h′ }, Γi+1 = Γi and ∆i+1 = ∆i .
    • If ExFi = E, Ri = {(h, h′ ⊲ h′′ )} ⊆ Gi , then Gi+1 = Gi ∪ {(h′ , h ⊲ h′′ )},
      Γi+1 = Γi , ∆i+1 = ∆i .
    • If ExFi = A, Ri = {(h, h′ ⊲ h′′ ), (w, w′ ⊲ h)} ⊆ Gi , then Gi+1 = Gi ∪
      {(w, h4i ⊲ h′′ ), (h′ , w′ ⊲ h4i )}, Γi+1 = Γi , ∆i+1 = ∆i .
    • If ExFi = CS, Ri = {(h, h′ ⊲ h′′ ), (w, w′ ⊲ h′′ )} ⊆ Gi , then Gi+1 =
      Gi ∪{(h4i , h4i+1 ⊲h), (h4i , h4i+2 ⊲w), (h4i+2 , h4i+3 ⊲h′ ), (h4i+1 , h4i+3 ⊲w′ )},
      Γi+1 = Γi , ∆i+1 = ∆i .
    • If ExFi is ≈1 , Ri = {(ǫ, hn ⊲ hn )}, where n ≤ 4i + 3, then Gi+1 =
      Gi ∪ {hn ∼ hn }, Γi+1 = Γi , ∆i+1 = ∆i .
    • If ExFi is ≈2 and Ri = {h′ ∼ h′′ , R[h′ /h]} ⊆ Gi , where h is the ni th
      label in R. Then Gi+1 = Gi ∪ {R[h′′ /h]}, Γi+1 = Γi , and ∆i+1 = ∆i .
    • If ExFi is ≈2 , Ri = {h ∼ h′ } ⊆ Gi , and Si = {w : A[h/w]} ⊆ Γi . Then
      Gi+1 = Gi , Γi+1 = Γi ∪ {w : A[h′ /w]}, and ∆i+1 = ∆i .
     • If ExFi is ≈2 , Ri = {h ∼ h′ } ⊆ Gi , and Si = {w : A[h/w]} ⊆ ∆i . Then
       Gi+1 = Gi , Γi+1 = Γi , and ∆i+1 = ∆i ∪ {w : A[h′ /w]}.
     • If ExFi = P and Ri = {(h′′ , h′ ⊲ h), (h′′ , h′ ⊲ w)} ⊆ Gi , then Gi+1 =
       Gi ∪ {h ∼ w}, Γi+1 = Γi and ∆i+1 = ∆i .
     • If ExFi = C and Ri = {(h′′ , h′ ⊲ h), (h′′ , w ⊲ h)} ⊆ Gi , then Gi+1 =
       Gi ∪ {h′ ∼ w}, Γi+1 = Γi and ∆i+1 = ∆i .
     • If ExFi = D and Ri = {(h, h ⊲ h′ )} ⊆ Gi , then Gi+1 = Gi ∪ {h ∼ ǫ},
       Γi+1 = Γi , and ∆i+1 = ∆i .
 – In all other cases, Gi+1 = Gi , Γi+1 = Γi and ∆i+1 = ∆i .


Lemma 3. If F is a formula unprovable in LSF OASL , then the limit sequent for
F is a Hintikka sequent.

Proof. Let G ω ; Γ ω ⊢ ∆ω be the limit sequent. First we show that G ω ; Γ ω ⊢ ∆ω
is finitely-consistent. Consider any G; Γ ⊢ ∆ ⊆f G ω ; Γ ω ⊢ ∆ω , we show that
G; Γ ⊢ ∆ has no derivation. Since G, Γ, ∆ are finite sets, there exists i ∈ N s.t.
G ⊆ Gi , Γ ⊆ Γi , and ∆ ⊆ ∆i . Moreover, Gi ; Γi ⊢ ∆i is not provable in LSF OASL ,
thus G; Γ ⊢ ∆ ⊆f Gi ; Γi ⊢ ∆i cannot be provable either. So condition 1, 2, and
4 in Definition 1 hold for the limit sequent, for otherwise we would be able to
construct a provable finite labelled sequent from the limit sequent.
     In some rules (thus also in the construction of the limit sequent), e.g., ∗R, a
label may occur multiple times in the principal relational atoms/formulae. In the
corresponding condition for the Hintikka sequent, we use distinct labels instead.
This causes no problems since the rule ∼2 (Condition 18 of Hintikka sequent)
ensures that any formula/relational atom, in which a label is substituted with
an equivalent one, must also be in the sequent. We explain this using ∗R as an
example:
     Suppose h′′′ : A ∗ B ∈ ∆ω and {(h, h′ ⊲ h′′ ), h′′ ∼ h′′′ } ⊆ G ω . There must
be some i ∈ N such that h′′′ : A ∗ B ∈ ∆i and {(h, h′ ⊲ h′′ ), h′′ ∼ h′′′ } ⊆ Gi .
There must also be some j > i with φ(j) = ( , , ≈2 , {(h, h′ ⊲ w)[h′′ /w], h′′ ∼
h′′′ }, {}, 3). By the first construction clause of ≈2 in Definition 3, Gj+1 contains
(h, h′ ⊲ w)[h′′′ /w], which is (h, h′ ⊲ h′′′ ). Now, there must be some k > j such that
φk = (1, h′′′ , A ∗ B, {h, h′ ⊲ h′′′ }, , ). By Definition 3, either ∆k+1 = ∆k ∪ {h : A}
or ∆k+1 = ∆k ∪ {h′ : B}, whichever is not derivable. Thus Condition 8 of
Hintikka sequent is met.
     With the above technique, most of other conditions in Definition 1 can be
checked in a similar way as the proof in [16], here we give some cases that do
not appear in the previous work. The following cases are numbered according to
items in Definition 1.
11. If h : ∃x.A(x) ∈ Γ ω , then there is some i ∈ N such that h : ∃x.A(x) ∈ Γi . And
    there is some j > i such that φ(j) = (0, h, ∃x.A(x), , , ). By Definition 3,
    h : A(tj+1 ) ∈ Γj+1 , thus h : A(tj+1 ) ∈ Γ ω .
12. If h : ∃x.A(x) ∈ ∆ω , then there is some i ∈ N such that h : ∃x.A(x) ∈ ∆i . For
    each tn ∈ D, there is some j > max(i, n) with φ(j) = (1, h, ∃x.A(x), , {h :
    tn = tn }, ). By Definition 3, h : A(tn ) ∈ ∆j+1 , thus h : A(tn ) ∈ ∆ω .
The other conditions can be shown similarly.                                                                     ⊓
                                                                                                                 ⊔




Theorem 2. If F is valid in FOASL, then F is provable in LSF OASL .




Proof. We construct a limit sequent G ω ; Γ ω ⊢ ∆ω for F following Definition 4.
Note that by the construction of the limit sequent, we have h1 : F ∈ ∆ω . By
Lemma 3, this limit sequent is a Hintikka sequent, and therefore by Lemma 1,
G ω ; Γ ω ⊢ ∆ω is falsifiable. This means there exists an extended model (M, ρ)
that satisfies every item in G ω and Γ ω and falsifies every item in ∆ω , including
h1 : F . Therefore F is false at world ρ(h1 ) in that model. Thus F is not valid.
Note that the limit sequent corresponds to a Hintikka sequent with an infinite
set of closed terms. In case that the target language only has a finite set of closed
terms and constants, we can just ignore the interpretations for the redundant
ones.                                                                               ⊓
                                                                                    ⊔




C      An example derivation




We sometimes write r × n when it is obvious that the rule r is applied n times.
We omit some formulae to save space.




                                       ⊤∗ R                                                     id
 · · · ; ǫ : e3 7→ e4 ⊢ ǫ : ⊤∗ · · ·               · · · ; ǫ : e3 7→ e4 ⊢ ǫ : e3 7→ e4 ; · · ·
                                                                                                    ∧R                                          ⊥L
                     · · · ; ǫ : e3 7→ e4 ⊢ ǫ : (e3 7→ e4 ) ∧ ⊤∗ ; · · ·                                  · · · ; ǫ : ⊥; ǫ : e3 7→ e4 ⊢ · · ·
                                                                                                                                                →L
                                                                                     ∗
                                                  · · · ; ǫ : ((e3 7→ e4 ) ∧ ⊤ ) → ⊥; ǫ : e3 7→ e4 ⊢ · · ·
                                                                                                                         ∀L × 2
                                            · · · ; ǫ : ∀e1 , e2 .((e1 7→ e2 ) ∧ ⊤∗ ) → ⊥; ǫ : e3 7→ e4 ⊢ · · ·
                                                                                                                         L on Formula 1
                                                                       · · · ; ǫ : e3 7→ e4 ⊢ · · ·
                                                                                                         Eq1
                                                              (ǫ, h3 ⊲ ǫ); · · · ; h3 : e3 7→ e4 ⊢ · · ·
                                                                                                         ⊤∗ L
                                                               · · · ; h3 : e3 7→ e4 ; h3 : ⊤∗ ⊢ · · ·
                                                                                                         ¬R
                                                              · · · ; h3 : e3 7→ e4 ⊢ h3 : ¬⊤∗ ; · · ·
                                                                                     Π2
                                                                                 Π1          Π2
                              ⊥L                                                                                                    ∗R
    · · · ; h4 : ⊥ ⊢ · · ·                 (h3 , h1 ⊲ h5 ); · · · ; h1 : e1 7→ e2 ; h3 : e3 7→ e4 ⊢ h5 : ((¬⊤∗ ) ∗ (¬⊤∗ )); · · ·
                                                                                                                                    −∗ L
       (h5 , h0 ⊲ h4 ); (h3 , h1 ⊲ h5 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ); h3 : (e3 7→ e4 ) ⊢ · · ·
                                                                                                                                  E
       (h0 , h5 ⊲ h4 ); (h3 , h1 ⊲ h5 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ); h3 : (e3 7→ e4 ) ⊢ · · ·
                                                                                                                                  A
       (h0 , h1 ⊲ h2 ); (h2 , h3 ⊲ h4 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ); h3 : (e3 7→ e4 ) ⊢ · · ·
                                                                                                                                        E×2
(h1 , h0 ⊲ h2 ); (h3 , h2 ⊲ h4 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ); h3 : (e3 7→ e4 ) ⊢ h4 : ⊥; h2 : ⊥
                                                                                                                                        −∗ R
            (h1 , h0 ⊲ h2 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ) ⊢ h2 : (e3 7→ e4 )−∗ ⊥; h2 : ⊥
                                                                                                                                ¬L
         (h1 , h0 ⊲ h2 ); · · · ; h2 : ¬((e3 7→ e4 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ) ⊢ h2 : ⊥
                                                                                                                                   ∀L
     (h1 , h0 ⊲ h2 ); · · · ; h2 : ∀e2 .¬((e3 7→ e2 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ) ⊢ h2 : ⊥
                                                                                                                                     ∃L
  (h1 , h0 ⊲ h2 ); · · · ; h2 : ∃e1 ∀e2 .¬((e1 7→ e2 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ) ⊢ h2 : ⊥
                                                                                                                                     L on Formula 5
                        (h1 , h0 ⊲ h2 ); · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥; h1 : (e1 7→ e2 ) ⊢ h2 : ⊥
                                                                                                                 −∗ R
                                     · · · ; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥ ⊢ h0 : (e1 7→ e2 )−∗ ⊥
                                                                                                           ¬L
                                  · · · ; h0 : ¬((e1 7→ e2 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥ ⊢
                                                                                                             ∀L
                              · · · ; h0 : ∀e2 .¬((e1 7→ e2 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥ ⊢
                                                                                                               ∃L
                           · · · ; h0 : ∃e1 ∀e2 .¬((e1 7→ e2 )−∗ ⊥); h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥ ⊢
                                                                                                               L on Formula 5
                                                 ; h0 : A; h0 : ((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥ ⊢
                                                                                                  ¬R
                                               ; h0 : A ⊢ h0 : ¬(((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥)
                                                                                                  → R
                                                ; ⊢ h0 : A → ¬(((¬⊤∗ ) ∗ (¬⊤∗ ))−∗ ⊥)

                         N.B. The sub-derivation Π1 is similar to Π2 .
