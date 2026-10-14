                                         A Probabilistic Separation Logic

                                         GILLES BARTHE, MPI for Security and Privacy, Germany and IMDEA Software Institute, Spain
                                         JUSTIN HSU, University of Wisconsin–Madison, USA
                                         KEVIN LIAO, MPI for Security and Privacy, Germany and University of Illinois Urbana-Champaign, USA
arXiv:1907.10708v4 [cs.PL] 17 Jul 2020




                                         Probabilistic independence is a useful concept for describing the result of random sampling—a basic operation
                                         in all probabilistic languages—and for reasoning about groups of random variables. Nevertheless, existing
                                         verification methods handle independence poorly, if at all. We propose a probabilistic separation logic PSL,
                                         where separation models probabilistic independence. We first give a new, probabilistic model of the logic of
                                         bunched implications (BI). We then build a program logic based on these assertions, and prove soundness
                                         of the proof system. We demonstrate our logic by verifying information-theoretic security of cryptographic
                                         constructions for several well-known tasks, including private information retrieval, oblivious transfer, secure
                                         multi-party addition, and simple oblivious RAM. Our proofs reason purely in terms of high-level properties,
                                         like independence and uniformity.
                                         CCS Concepts: • Security and privacy → Logic and verification; • Theory of computation → Separa-
                                         tion logic.
                                         Additional Key Words and Phrases: probabilistic independence, separation logic, verified cryptography
                                         ACM Reference Format:
                                         Gilles Barthe, Justin Hsu, and Kevin Liao. 2020. A Probabilistic Separation Logic. Proc. ACM Program. Lang. 4,
                                         POPL, Article 55 (January 2020), 41 pages. https://doi.org/10.1145/3371123

                                         1     INTRODUCTION
                                         Probabilistic programs have important applications in many domains, including information secu-
                                         rity and machine learning. As the impact of these areas continues to grow, probabilistic programming
                                         languages (PPLs) are receiving renewed attention from formal verification. While the mathematical
                                         semantics of PPLs has been well-studied, starting from Kozen [1981]; Saheb-Djahromi [1980] and
                                         continuing up to today [Ehrhard et al. 2018; Vákár et al. 2019], deductive program verification
                                         for PPLs remains challenging. Establishing simple properties can involve tedious arguments, and
                                         scaling formal proofs up to verify target properties of randomized algorithms is often difficult.

                                         1.1    Probabilistic Independence
                                         A basic property that is poorly handled by existing verification techniques is independence. Roughly
                                         speaking, two random variables are probabilistically independent if they are uncorrelated: in-
                                         formation about one quantity yields no information about the other. In probabilistic programs,
                                         independence usually arises when variables are derived from separate randomness—e.g., from the
                                         results of two different coin flips—but independence can also hold when variables share randomness
                                         in just the right way.
                                            Although it is usually not the target property of interest, probabilistic independence often serves
                                         as an intermediate assertion in pen-and-paper proofs of randomized algorithms. From a verification
                                         perspective, independence is useful for several reasons.
                                         Authors’ addresses: Gilles Barthe, MPI for Security and Privacy, Germany and IMDEA Software Institute, Spain; Justin
                                         Hsu, University of Wisconsin–Madison, USA; Kevin Liao, MPI for Security and Privacy, Germany and University of Illinois
                                                                                                                                                                             55
                                         Urbana-Champaign, USA.

                                         © 2020 Copyright held by the owner/author(s).
                                         This is the author’s version of the work. It is posted here for your personal use. Not for redistribution. The definitive Version
                                         of Record was published in Proceedings of the ACM on Programming Languages, https://doi.org/10.1145/3371123.



                                                                            Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:2                                                                           Gilles Barthe, Justin Hsu, and Kevin Liao


   Independence simplifies reasoning about groups of random variables. Probabilistic programs often
manipulate multiple random variables. If a group of random variables are independent, then their
joint distribution is precisely described by the distribution of each variable in isolation. As a result,
formal reasoning can focus on one variable at a time, without losing information.

   Independence characterizes the result of random sampling. All PPLs have built-in constructs to
draw random samples from primitive distributions (e.g., drawing a random boolean from a coin-flip
distribution). These basic operations produce a “fresh” random quantity that is independent from
the rest of the program state, at least when the primitive distribution does not depend on the state.

  Independence is preserved under local operations. Like standard programs, probabilistic programs
typically manipulate only a few variables at a time. To ease formal reasoning, properties about
unmodified variables should be preserved as much as possible. Independence is preserved under
local modifications: if x and y are independent and x is updated to x ′ = x + 1, then x ′ and y
remain independent. In this way, probabilistic independence seemingly flows through a program,
continuing to hold far beyond the original sampling instructions.

   Independence is compatible with conditioning. Probabilistic programs can have randomized control
flow, for example branching on a randomized boolean. Semantically, this kind of branch is modeled
by conditioning, an operation that transforms an input distribution into two conditional distributions,
one where the guard is true and one where the guard is false.
   While conditioning is well-understood mathematically, it poses problems for formal reasoning.
Conditioning on a variable x—say, when branching on x > 0—can alter the distribution over other
variables. If x is independent of y, however, conditioning on x will have no effect on the distribution
over y. As a result, properties of variables that are syntactically separate from the variable x are
preserved when conditioning on the guard x > 0, a highly useful reasoning principle.

1.2    Example Applications of Independence
To ground our investigation in applications, we focus on security properties from cryptography.
We first encode target cryptographic protocols as probabilistic programs of type A × A → O × A,
where the first input represents the secret input, the second input represents the public input, and
the first and second output represents the observer’s view and computation output, respectively. In
many cases the two outputs coincide, but this need not be the case in general.
   Then, we establish security properties by proving properties of these programs in our logic.
Defining precisely what it means for a construction to be secure is surprisingly subtle; cryptogra-
phers have proposed many definitions capturing different assumptions and guarantees. Baseline,
information-theoretic security of many schemes, including private information retrieval [Chor
et al. 1995], oblivious transfer [Rivest 1999], multi-party computation [Cramer et al. 2015], and
oblivious RAM [Chung and Pass 2013], can be stated in terms of the following definitions.

  Uniformity. A natural way to define security is to require that the observer’s view is the same,
no matter what the private input is; this is a probabilistic form of non-interference. For instance, it
suffices to show that the observer’s view is always uniformly distributed over a fixed set: no matter
what the private inputs are, the observer’s view is the same.

  Input Independence. Another way to define security is to model the secret input as drawn from
some distribution, and then argue that the distribution of the observer’s view is probabilistically
independent of the secret input. This formulation captures security through an intuitive reading
of independence: the observer’s view reveals no information about the secret input. Though

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                      55:3


this definition looks quite different from probabilistic non-interference, the two definitions are
equivalent in many settings. Their proofs, however, may be quite different.

1.3    Contributions and Plan of the Paper
After introducing mathematical preliminaries in Section 2, we begin working towards the main
goal of this paper: a probabilistic program logic where independence is the central concept. Our
logic is a probabilistic variant of separation logic, a highly successful technique for reasoning about
heap-manipulating programs [Ishtiaq and O’Hearn 2001; O’Hearn et al. 2001]. To model sharing
and separation, separation logic uses assertions from the logic of bunched implications (BI), a
substructural logic. For instance, the separating conjunction models separation of heaps: ϕ ∗ ψ
states that the heap can be split into two disjoint parts satisfying ϕ and ψ , respectively.
    While separation logic was originally designed for heaps, separation is a useful concept in many
verification settings. A notable line of work extends separation logic to the concurrent setting,
where separation models exclusive ownership of resources [Brookes 2007; O’Hearn 2007]. More
generally, the resource semantics of BI [Pym et al. 2004] gives a powerful way to generalize BI to
new notions of separation.
    Inspired by this perspective, our first contribution is a new interpretation of BI where the separat-
ing conjunction models probabilistic independence. Roughly speaking, ϕ ∗ ψ holds in a distribution
µ over program memories if µ can be factored into two distributions µ 1 and µ 2 satisfying ϕ and
ψ , respectively. Splitting a distribution amounts to finding two disjoint sets of program variables
X and Y such that every distribution in the support of µ is defined precisely on X ∪ Y , with the
factors µ 1 and µ 2 obtained by projecting µ along X and Y respectively. This intuitive interpretation
gives rise to a probabilistic model of BI. Our model can smoothly incorporate useful primitive
assertions about distributions, including probabilistic equality and uniformity. We present our
model in Section 3.
    Leveraging this probabilistic version of BI as an assertion logic, our second contribution is a
program logic PSL for a simple probabilistic programming language, similar to pWhile. Our logic
bears a strong resemblance to separation logic: there are proof rules for local and global reasoning,
there is a version of the Frame rule, and whereas separation logic distinguishes between store and
heap, our logic distinguishes between deterministic and probabilistic variables. However, there are
also notable differences in the probabilistic setting. We present the proof system of PSL and prove
soundness in Section 4.
    As our third contribution, we demonstrate our program logic by formalizing security of several
well-known constructions from cryptography, including a simple oblivious RAM, a private informa-
tion retrieval algorithm, a simple three-party computation algorithm for addition, and an oblivious
transfer algorithm. We prove two different forms of information-theoretic security: uniformity of
outputs (which implies probabilistic non-interference), and input independence. We present these
examples in Section 5.
    We survey related work in Section 6 and discuss potential future directions in Section 7.

2     PRELIMINARIES
2.1    Probabilities and Distributions
A (discrete) probability distribution over a countable set A is a function µ : A → [0, 1] such that the
total weight is one: a ∈A µ(a) = 1; we write D(A) for the set of all distributions over A. Intuitively,
                     Í
µ(a) represents the probability of drawing a from the distribution µ. Likewise, the probability of
drawing some element in S ⊆ A is µ(S) ≜ a ∈S µ(a). The support of a distribution is the set of
                                               Í
elements with non-zero probability: supp(µ) = {a ∈ A | µ(a) > 0}.

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:4                                                                                Gilles Barthe, Justin Hsu, and Kevin Liao


   We will use two standard constructions on probability distributions. First, the distribution unit
unit : A → D(A) associates each element a ∈ A with the Dirac distribution δ a centered at a. This
distribution is simply defined as δ a (x) ≜ 1 if x = a and δ a (x) ≜ 0 otherwise; intuitively, the Dirac
distribution deterministically yields a. Second, the distribution bind bind : D(A) → (A → D(B)) →
D(B) is defined by:
                                                    Õ
                                  bind(µ, f )(b) ≜      µ(a) · f (a)(b)
                                                             a ∈A
Intuitively, bind sequences a distribution with a continuation. Together, unit and bind make D a
monad [Giry 1982]; these operations are commonly used to model randomized programs.
  Given our focus on independence, we will be particularly interested in distributions over products
and products of distributions. The distribution product ⊗ : D(A) × D(B) → D(A × B) is defined by:
                                        (µ A ⊗ µ B )(a, b) ≜ µ A (a) · µ B (b).
We can extract component distributions out of any distribution over a product using the projections
π1 : D(A × B) → D(A) and π 2 : D(A × B) → D(B):
                                  Õ                              Õ
                     π 1 (µ)(a) ≜    µ(a, b) and π2 (µ)(b) ≜         µ(a, b).
                                         b ∈B                                      a ∈A

We call µ ∈ D(A × B) a product distribution if it can be factored as µ = π1 (µ) ⊗ π 2 (µ); in this case,
we say that the components of µ are (probabilistically) independent.
  Finally, will need conditioning and convex combination operations on distributions to model
control flow splits and merges, respectively. Let S ⊆ A be any event. If S has non-zero probability
under µ ∈ D(A), then the conditional distribution µ | S ∈ D(A) is defined as:
                                                                 µ(S ∩ E)
                                                (µ | S)(E) ≜              .
                                                                   µ(S)
Intuitively, the conditional distribution represents the relative probabilities of elements restricted
to S. Conditioning is not defined when µ(S) = 0.
   To join output distributions from two branches, we define the convex combination of distributions.
Let ρ ∈ [0, 1] and let µ 1 , µ 2 ∈ D(A). The convex combination µ 1 ⊕ρ µ 2 ∈ D(A) is defined as:

                                  (µ 1 ⊕ρ µ 2 )(S) ≜ ρ · µ 1 (S) + (1 − ρ) · µ 2 (S).

We define µ 1 ⊕0 µ 2 ≜ µ 2 and µ 1 ⊕1 µ 2 ≜ µ 1 , even when µ 1 or µ 2 may be undefined. Conditioning
and taking convex combination yields the original distribution: µ = (µ | S) ⊕µ(S ) (µ | S).

2.2    Probabilistic Memories
Distributions over program memories are naturally modeled by distributions over products. We
fix a countable set RV of random variables and a countable set Val of values. For any subset of
variables S ⊆ RV, we let RanM[S] ≜ S → Val be the set of memories with domain S; we write
RanM ≜ RanM[RV]. When S is empty, there is precisely one map 0 : ∅ → Val and so D(RanM[∅])
contains just the Dirac distribution δ 0 . Given a distribution µ ∈ D(RanM[S]), we write dom(µ) ≜ S
for the domain.
   Viewing RanM[S] as a product indexed by S, we can adapt the general constructions for dis-
tributions over products to distributions over RanM[S]. Given disjoint variables S, S ′ ⊆ RV, for
instance, we define the product ⊗ : D(RanM[S]) × D(RanM[S ′]) → D(RanM[S ∪ S ′]) to be
                                       (µ S ⊗ µ S ′ )(m) ≜ µ S (m S ) · µ S ′ (m S ′ )

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                      55:5


where m S ∈ RanM[S] and m S ′ ∈ RanM[S ′] restrict m to S and S ′ respectively. The Dirac distribution
δ 0 is the identity of this operation: µ ⊗ δ 0 = δ 0 ⊗ µ = µ. When µ ∈ D(RanM[S]) can be factored as
µ = µ 1 ⊗ µ 2 for µ i ∈ D(RanM[Si ]), we say that S 1 and S 2 are (probabilistically) independent in µ.
    Likewise, we can project a distribution over RanM[S] to a distribution over RanM[S ′] for S ′ ⊆ S
using the projection πS,S ′ : D(RanM[S]) → D(RanM[S ′]), defined as:
                                                         Õ
                              πS,S ′ (µ)(m S ′ ) ≜                    µ(m S ),
                                                      m S ∈RanM[S ]:pS ′ (m S )=m S ′

where pS ′ restricts the range of the memory to S ′. For example, πS,S is the identity, while πS, ∅ maps
all distributions to δ 0 . We will abbreviate πS,S ′ by πS ′ (or just π ) when the domains are clear from
the context.

2.3    Probabilistic Programs
We will work with a variant of the basic probabilistic imperative language pWhile. We enforce a
clear separation between deterministic and probabilistic data using simple syntactic conditions,
though more sophisticated techniques (e.g., dataflow analysis) could be also used. Let DV be a
countable set of deterministic variables disjoint from RV, and let DetM ≜ DV → Val be the set
of deterministic memories, or stores. The expression language is largely standard:
                            DE ∋ ed ::= DV | DE + DE | DE ∧ DE | · · ·
                             RE ∋ er ::= DE | RV | RE + RE | RE ∧ RE | · · ·
We assume that expressions are typed using a simple type system, and we only work with well-
typed expressions. We interpret deterministic expressions as maps Jed K : DetM → Val. Randomized
expressions are interpreted as maps Jer K : DetM × RanM[S] → Val, where S ⊆ RV contains all
randomized variables in er ; if er mentions variables outside of S, then the interpretation is not
defined. It is also straightforward to lift this interpretation to interpret randomized expressions in
distributions over randomized memories: Jer K : DetM × D(RanM[S]) → D(Val).
   Next, we consider the commands. RC commands appearing under a randomized guard—so they
cannot assign to deterministic variables—while C commands are general.
        RC ∋ c ::= skip | RV ← RE | RV ←
                                       $ U | RC ; RC
                                          S
                  | if D DE then RC else RC | if R RE then RC else RC | while DE do RC
           C ∋ c ::= skip | DV ← DE | RV ← RE | RV ←
                                                   $ U | C ; C
                                                      S
                  | if D DE then C else C | if R RE then RC else RC | while DE do C
The main probabilistic command is sampling: RV ←       $ U takes a uniform sample from a finite,
                                                            S
non-empty set S and assigns it to a variable.
  Our grammar separates commands for assignments to deterministic variables and randomized
variables, and separates commands for deterministic and probabilistic conditionals (we require
loop guards to be deterministic). These distinctions will be important when we introduce our proof
system. We will also use a few standard variants of commands:
                      for i = 1, . . . , N do c ≜ i ← 1 ; while i ≤ N do (c ; i ← i + 1)
           if D b then c ≜ if D b then c else skip                if R b then c ≜ if R b then c else skip
We interpret programs using a restricted version of the standard semantics due to Kozen [1981],
assuming additionally that programs terminate on all inputs—notions like product distribution
and probabilistic independence are poorly behaved when programs may diverge with positive

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:6                                                                                 Gilles Barthe, Justin Hsu, and Kevin Liao



                            JskipK(σ , µ) ≜ (σ , µ)
                       Jxd ← ed K(σ , µ) ≜ (σ [xd 7→ Jed Kσ ], µ)
                       Jx r ← er K(σ , µ) ≜ (σ , bind(µ, m 7→ unit(m[x r 7→ Jer K(σ , m)])))
                           $ U K(σ , µ) ≜ (σ , bind(µ, m 7→ bind(Unif , u 7→ unit(m[x 7→ u]))))
                      Jx r ←  S                                      S               r
                         Jc ; c ′K(σ , µ) ≜ Jc ′K(JcK(σ , µ))
                                            (
                                              JcK(σ , µ) : JbKσ = true
         Jif D b then c else c K(σ , µ) ≜
                                ′
                                              Jc ′K(σ , µ) : JbKσ = false
          Jif R b then c else c ′K(σ , µ) ≜ JcK(σ , µ | JbKσ = true) ⊕ρ Jc ′K(σ , µ | JbKσ = false)
                                                        where ρ = µ(JbKσ = true)
                  Jwhile b do cK(σ , µ) ≜ Jc ; · · · ; c K(σ , µ)
                                           | {z }
                                                       N (σ )≜ #steps until Jb K=false


                                               Fig. 1. Program semantics


probability. Technically, programs transform configurations, pairs of a deterministic memory σ and
a distribution µ over randomized memories:
                               JcK : (DetM × D(RanM)) → (DetM × D(RanM)).
Figure 1 presents the program semantics; UnifS ∈ D(S) is the uniform distribution over a finite,
non-empty set S, which assigns probability 1/|S | to every element s ∈ S. The semantics of random
conditionals uses convex combination lifted to configurations; this is defined since the output stores
are equal because branches under random guards may not modify deterministic variables.

3      A PROBABILISTIC MODEL OF BI
Assertions in separation logic are based on the logic of bunched implications (BI) [O’Hearn and
Pym 1999; Pym 1999]. We first review the syntax and semantics of this logic, then introduce a
probabilistic interpretation that will enable BI formulas to describe probabilistic states.

3.1     The Syntax and (Resource) Semantics of BI, in Brief
The logic of bunched implications (BI) is a substructural logic with the following formulas:1
                     ϕ,ψ ::= p ∈ AP | ⊤ | ⊥ | ϕ ∧ ψ | ϕ ∨ ψ | ϕ → ψ | ϕ ∗ ψ | ϕ −∗ ψ
Throughout, p ranges over a set of atomic propositions AP. Negation ¬ϕ is defined as ϕ → ⊥.
Intuitively, BI combines standard propositional logic with a substructural fragment consisting of
the separating conjunction ∗ and the separating implication (“magic wand”) −∗. In the standard heap
model of BI underlying separation logic, atomic propositions describe the contents of particular
heap locations, separating conjunction combines assertions describing disjoint portions of the heap,
and separating implication describes the result of adjoining the current heap with a disjoint portion.
   BI can be given several kinds of semantics. We follow the resource semantics, as developed by
David Pym and others [Pym et al. 2004]. The basic idea is to define a Kripke semantics where the
set of possible worlds forms a partial, pre-ordered commutative monoid M = (M, ◦, e, ⊑).
1 We do not need the multiplicative identity I from BI, since it will be equivalent to ⊤ in our setting.



Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                       55:7


Definition 1 (Galmiche et al. [2005]). A (partial) Kripke resource monoid consists of a set M of
possible worlds, a partial binary operation ◦ : M × M ⇀ M, an element e ∈ M, and a pre-order ⊑ on
M such that the monoid operation
    • has identity e: for all x ∈ M, we have e ◦ x = x ◦ e = x;
    • is associative: x ◦ (y ◦ z) = (x ◦ y) ◦ x, where both sides are either defined and equal, or both
      undefined; and
    • is compatible with the pre-order: if x ⊑ y and x ′ ⊑ y ′ and if both x ◦ x ′ and y ◦ y ′ are defined,
      then x ◦ x ′ ⊑ y ◦ y ′.

   Under the resource interpretation of BI, possible worlds are collections of resources, the monoid
operation ◦ combines sets of resources, and the identity e represents the lack of resources. The
monoid operation may fail to be defined when combining two incompatible sets of resources; this
is useful for modeling resources that should not be duplicated, such as heap addresses. We write
(m ◦ m ′) ↓ when the combination is defined.

Definition 2. Let (M, ◦, e, ⊑) be a partial Kripke resource monoid and let J−K : AP → 2M be a
Kripke resource interpretation of atomic formulas: if m ∈ JpK and m ⊑ m ′, then m ′ ∈ JpK. Then the
corresponding Kripke resource model of BI can be defined as follows:

 m |= p               iff m ∈ JpK
 m |= ⊤               always
 m |= ⊥               never
 m |= ϕ ∧ ψ           iff m |= ϕ and m |= ψ
 m |= ϕ ∨ ψ           iff m |= ϕ or m |= ψ
 m |= ϕ → ψ           iff for all m ⊑ m ′, m ′ |= ϕ implies m ′ |= ψ
 m |= ϕ ∗ ψ           iff exist m 1 , m 2 with (m 1 ◦ m 2 ) ↓ and m 1 ◦ m 2 ⊑ m such that m 1 |= ϕ and m 2 |= ψ
 m |= ϕ −∗ ψ          iff for all m ′ such that m ′ |= ϕ, (m ◦ m ′) ↓ implies m ◦ m ′ |= ψ

All formulas satisfy the Kripke monotonicity property: if m |= ϕ and m ⊑ m ′, then m ′ |= ϕ as well.
We write |= ϕ when ϕ is valid, i.e., when ϕ holds in all worlds.

  BI enjoys good metatheoretic properties and a rich proof theory. Many models are known beyond
heaps, including doubly closed categories (DCCs), presheafs, and Petri nets. There are also complete
proof systems for BI. The interested reader should consult Pym [2002] or Docherty [2019] for a
detailed treatment of BI’s proof theory, and Galmiche et al. [2005] for more information about the
partial monoid semantics we use here.

3.2 A Probabilistic Version of BI
By leveraging the resource semantics of BI, we can give a probabilistic interpretation of BI formulas.

Definition 3. Let M be the set of program configurations DetM[S] × D(RanM[T ]) where S ranges
over subsets of DV and T ranges over subsets of RV. Let ◦ be a partial binary operation defined as:
                          (
                              (σ ∪ σ ′, µ ⊗ µ ′) : σ = σ ′ on dom(σ ) ∩ dom(σ ′) and dom(µ) ∩ dom(µ ′) = ∅
 (σ , µ) ◦ (σ , µ ) ≜
              ′   ′
                              undefined          : otherwise.

                                    Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:8                                                                             Gilles Barthe, Justin Hsu, and Kevin Liao


Let e be the empty deterministic memory paired with the Dirac distribution over the empty probabilistic
memory, and let ⊑ be the following partial order:
                                     (
                                        dom(σ ) ⊆ dom(σ ′) and σ = σ ′ on dom(σ )
              (σ , µ) ⊑ (σ , µ ) iff
                          ′ ′
                                        dom(µ) ⊆ dom(µ ′) and µ = πdom(µ ′ ),dom(µ) (µ ′).
Then (M, ◦, e, ⊑) is a Kripke resource monoid.
   To describe basic properties of configurations, we take the following atomic formulas.
                     AP ∋ p ::= US [RE] | RE ∼ RE | DE = DE | DE ≤ DE | · · ·
We will fix a base theory E of program expressions, enough to interpret the necessary arithmetic
operations (+, ·) and relations (=, ≤), and we write |=E ϕ if ϕ when ϕ is valid. For example |=E
e + e ′ = e ′ + e holds for any two expressions, randomized or not.
   Validity for atomic formulas of deterministic expressions is defined as expected: these formulas
can be interpreted as subsets of DetM. More formally, for any deterministic proposition pd we
write σ |=E pd if pd holds in σ , and we define:
                                               (σ , µ) |= pd iff σ |=E pd
The more interesting cases are the atomic formulas for randomized expressions.
Definition 4. For a nonempty finite set S and a randomized expression er ∈ RE, we define JUS [er ]K to
be the set of configurations (σ , µ) where FV (er ) ⊆ dom(σ ) ∪ dom(µ), and Jer K(σ , µ) assigns probability
1/|S | to each element of S; we omit S when it is clear from the context.
   We define Jer ∼ er′ K to be the set of configurations (σ , µ) where FV (er ) ∪ FV (er′ ) ⊆ dom(σ ) ∪ dom(µ)
and Jer K(σ , m) = Jer′ K(σ , m) for m ∈ supp(µ). This formula asserts equality between randomized
expressions; we use ∼ to avoid confusion with equality between deterministic expressions. We abbreviate
D[e] ≜ e ∼ e. Explicitly, JD[e]K contains all configurations (σ , µ) where FV (e) ⊆ dom(σ ) ∪ dom(µ).
   Since the interpretation of atomic assertions is monotonic, our configurations are a Kripke
resource model of BI. An important feature of the resulting semantics is that validity only depends
on the variables in the formula. (We defer proofs to Appendix B.)
Lemma 1 (Restriction). Let (σ , µ) be any configuration and let ϕ be a BI formula. Then:
                                      (σ , µ) |= ϕ ⇐⇒ (σ , πFV (ϕ) (µ)) |= ϕ.
   One useful consequence is the following property, which allows a ∧ conjunct to be pulled into a
∗ conjunct covering all of the formula’s free random variables.
Lemma 2 (Extrusion). If |= ϕ → D[FV (η) ∩ RV], then |= (ϕ ∗ ψ ) ∧ η → (ϕ ∧ η) ∗ ψ .
   An easy and useful consequence follows when η does not mention any random variables.2
   Corollary 1. Let pd be a deterministic proposition. The following axiom is sound:
                                                 |= ψ ∧ pd → ψ ∗ pd
 Proof. Since ⊤ is the unit for ∗ in our semantics, ψ ∧ pd implies (⊤ ∗ ψ ) ∧ pd . Since pd does not
mention any random variables, Lemma 2 implies (⊤ ∧ pd ) ∗ ψ . Symmetry of ∗ gives ψ ∗ pd .        □
   We briefly mention two other important features of our semantics. First, the semantics is intu-
itionistic: ϕ ∨ ¬ϕ is not valid. Second, our semantics admits weakening:
                                                  |= ϕ ∗ ψ → ϕ ∧ ψ
We will use repeatedly this property to pull out facts about specific variables from a larger assertion.
2 For readers familiar with separation logic, deterministic propositions resemble pure assertions in the heap model of BI.



Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                      55:9


3.3     Axiom Schema for Atomic Formulas
Next, we present our axioms for atomic formulas. Much like the situation for atomic formulas in the
“pointer logic” underlying standard separation logic, these axioms are not complete. Nevertheless,
they are already sufficient to reason about many interesting probabilistic programs.
   We begin with axioms for formulas with ∼. The main difference between ∼ and standard equality
is that since ∼ is interpreted in a randomized configuration—which might not have all of RV in its
domain—replacing expressions by equal expressions must not introduce new random variables.
Lemma 3. The following axiom schema are valid:
            |= er ∼ er′ → er′ ∼ er                                                                                   (S1)
            |= er ∼ er′ ∧ er′ ∼ er′′ → er ∼ er′′                                                                     (S2)
            |= er ∼ er′ → er ∼ er′′ whenever |=E er′ = er′′ and FV (er′′) ∩ RV ⊆ FV (er′ ) ∩ RV                      (S3)
            |= er ∼ er → er′ ∼ er′ whenever FV (er′ ) ∩ RV ⊆ FV (er ) ∩ RV                                           (S4)
 Note that |= er ∼ er is not an axiom—it is not sound, since it may not hold in a randomized
memory D(RanM[∅]) with empty domain. We also have axioms for uniformity propositions.
Lemma 4. The following axiom schema are valid:
      |= er ∼ er′ ∧ US [er ] → US [er′ ]                                                                            (U1)
      |= US [er ] → er ∼ er                                                                                         (U2)
      |= US [er ] → US [f (er )] for any bijection Jf K : S → S and FV (f ) ∩ RV ⊆ FV (er ) ∩ RV                    (U3)

3.4     Comparison with Typical Models of BI
This subsection contains a more detailed comparison with other models of BI; readers who are
primarily interested in the separation logic can safely skip ahead to Section 4.
   Our model of BI is strongly inspired by the standard heap model. There, worlds are partial maps
from heap locations to values and the main atomic assertion e 7→ e ′ (“points-to”) indicates that in
the current heap, the location stored in expression e holds the value denoted by e ′ in the current
store. A separating conjunction of two points-to assertions e 7→ e ′ ∗ f 7→ f ′ indicates that the
addresses held in e and f do not alias. This separation property cannot be deduced syntactically—
two expressions mentioning different variables may refer to the same heap location in the current
store—but it is crucial for local reasoning in the presence of aliasing.
   Our probabilistic model is designed to capture a fundamentally different notion of separation
that is natural to the probabilistic setting. The randomized portion of the program state plays the
role of the heap in the heap model, but randomized variables are not heap-allocated. Accordingly,
the names of randomized variables are fixed and it is possible to syntactically determine when two
assertions refer to the same variable. However, it is not always possible to determine when two
assertions refer to probabilistically independent variables—for instance, the assertion U[x] ∧ U[y]
holds in any memory where x and y are uniform, but x and y may be correlated. The stronger
property of probabilistic independence—the notion of non-aliasing that probabilistic BI is designed
to model—is captured by the assertion U[x] ∗ U[y].
   As we have noted, our semantics is intuitionistic. This aspect stems from our choice of a non-
trivial partial order ⊑ over worlds. If this order is taken to be discrete, relating only identical
elements, and atomic formulas are interpreted exactly, referring to the entire memory rather than a
fragment, we would arrive at a classical or Boolean semantics for probabilistic BI. This situation is
mirrored in heap models of BI, where the classical logic BBI has a semantics with a discrete order.

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:10                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


                                                                                ⊢ {ϕ} c {ψ }         ⊢ {ψ } c ′ {η}
    DAssn                                       Skip                     Seqn
            ⊢ {ψ [ed /xd ]} xd ← ed {ψ }               ⊢ {ϕ} skip {ϕ}                     ⊢ {ϕ} c ; c ′ {η}

                   ⊢ {ϕ ∧ b = tt} c {ψ }
                   ⊢ {ϕ ∧ b = ff } c ′ {ψ }                             ⊢ {ϕ ∧ b = tt} c {ϕ}
      DCond                                              DLoop
              ⊢ {ϕ} if D b then c else c {ψ }
                                            ′
                                                                 ⊢ {ϕ} while b do c {ϕ ∧ b = ff }

                                   Fig. 2. Proof rules: deterministic constructs


    For heap models, BBI is more precise than BI—it supports atomic assertions that are not preserved
under heap extension, like emp for empty heap, and BI formulas ϕ can be recovered by BBI formulas
ϕ ∗ ⊤. In the probabilistic setting, however, a classical logic seems to run into trouble. For instance,
it is not the case that a formula ϕ valid in (σ , µ) under our semantics can be directly translated into
a classical semantics: (σ , µ) |= ϕ ∗ ⊤ would state that the domain of the distribution modeling ϕ
is probabilistically independent of all other variables, which does not follow from (σ , µ) |= ϕ. We
leave the development of a classical version of probabilistic BI for future work.

4     A PROBABILISTIC SEPARATION LOGIC
We now have all the ingredients needed for our separation logic PSL. First, the judgments.

4.1     Judgments and Validity
Definition 5. PSL judgments have the form {ϕ} c {ψ } where ϕ and ψ are probabilistic BI formulas.
Such a judgment is valid, denoted |= {ϕ} c {ψ }, if for all configurations (σ , µ) ∈ DetM[DV] ×
D(RanM[RV]) satisfying (σ , µ) |= ϕ, we have JcK(σ , µ) |= ψ .
  We have defined validity to quantify over only input states with all variables in the domain.
Unlike in separation logic, programs do not allocate variables and memory faults are not possible,
so there is no reason to consider behaviors from partial configurations in the program logic.

4.2     Proof Rules: Deterministic Constructs
We introduce the proof system of PSL in three stages. First, we consider the deterministic constructs
in Fig. 2. The rule DAssn is the usual Hoare rule for assignments, but it is only sound for assignments
to deterministic variables. Otherwise, the rules are as expected.
   When proving judgments of for-loops, we will use the following derived rule:
                                ⊢ {ϕ} c {ϕ[i + 1/i]}          FV (N ) ∩ MV (c) = ∅
                        DFor
                               ⊢ {ϕ[1/i]} for i = 1, . . . , N do c {ϕ[N + 1/i]}
MV (c) is the set of variables that may be modified by c; we defer the formal definition to Definition 7,
when we discuss the frame rule.

4.3     Proof Rules: Probabilistic Constructs
Fig. 3 presents the proof rules for randomized operations. RAssn and RSamp are for randomized
assignment and random sampling, respectively; in contrast to DAssn, these rules reason forwards.
Both rules are presented in their “local” form, where the pre-condition is trivial. We will soon
derive “global” variants, with general pre-conditions, from the structural rules.
  There are two rules for randomized conditionals. RDCond resembles DCond, with a side-
condition to ensure that the randomized guard b is deterministic. RCond applies when the guard

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:11


                            x r < FV (er )
           RAssn                                             RSamp
                    ⊢ {⊤} x r ← er {x r ∼ er }                        ⊢ {⊤} x r ←
                                                                                $ U {U [x ]}
                                                                                   S  S r


             ⊢ {ϕ ∧ b ∼ tt} c {ψ }            ⊢ {ϕ ∧ b ∼ ff } c ′ {ψ }        |= ϕ → (b ∼ tt ∨ b ∼ ff )
  RDCond
                                           ⊢ {ϕ} if R b then c else c {ψ }
                                                                         ′


              ⊢ {ϕ ∗ b ∼ tt} c {ψ ∗ b ∼ tt}             ⊢ {ϕ ∗ b ∼ ff } c ′ {ψ ∗ b ∼ ff }         ψ ∈ SP
    RCond
                                   ⊢ {ϕ ∗ D[b]} if R b then c else c {ψ ∗ D[b]}
                                                                         ′



                                      Fig. 3. Proof rules: probabilistic constructs


is truly probabilistic, and it has two unusual aspects. First, the pre-condition in the conclusion
requires the guard to be separated from the rest of the pre-condition; that is, the guard must be
probabilistically independent of the portion of the randomized memory satisfying ϕ. This separation
is crucial for ϕ to be soundly used as a pre-condition in each branch: the input distribution to each
branch is obtained by conditioning on the value of the guard expression in the input distribution.
This operation may not preserve ϕ, even if ϕ and the guard have no variables in common—this is a
particular feature of the probabilistic setting.
Example 1. Suppose that x, y, z are randomized boolean variables, and let µ be the output of:
                                            x←
                                             $ U ;y $ U ;z ← x ∨ y
                                                B  ← B
In words, x and y store the results of two fair coin flips, and z stores the value of x ∨y. Then x and y are
independent in µ, i.e., D[x] ∗ D[y] holds in µ. However, if S ⊆ RanM[RV] is the set of all randomized
memories where z = tt, representing the event that z is true, then D[x] ∗ D[y] does not hold in µ | S.
Intuitively, if we know z = tt, then x and y are correlated: if one is false, then the other must be true.
   RCond also shows that the guard remains independent of the branch post-condition assuming
the branches do not modify the guard, and the branch post-condition determines a unique portion
of the distribution over randomized memories. Formally, we adapt the following class of assertions
from separation logic [Reynolds 2008].
Definition 6. A formula ϕ is supported (SP) if for any deterministic memory σ , there exists a
randomized memory µ such that if (σ , µ ′) |= ϕ, then µ ⊑ µ ′.
   The following syntactic conditions ensure SP.
Lemma 5. The following assertions are SP:
                                      η ::= pd | RV ∼ DE | US [RV] | η ∗ η
  Proof. By induction on η. The base cases are immediate: pd holds in the unique randomized
memory with empty domain, while x ∼ e and US [x] hold in unique randomized memories with
domain {x }. The inductive case is also straightforward.                                  □
Example 2 (Non-SP assertions). A simple example of an assertion that is not covered by Lemma 5
is ϕ ≜ D[x], where x ∈ RV is a boolean randomized variable. It is easy to see that ϕ is not SP; for
instance, ϕ holds in two incomparable distributions δ (x 7→tt) and δ (x 7→ff ) . Indeed, allowing ϕ as a branch
post-condition in RCond would be unsound. Consider the following program:
                                        c ≜ if R b then x ← tt else x ← ff

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:12                                                                             Gilles Barthe, Justin Hsu, and Kevin Liao


                       ⊢ {ϕ} c {ψ }         |= ϕ ′ → ϕ ∧ ψ → ψ ′
             Weak                                                              True
                                      ⊢ {ϕ ′ } c {ψ ′ }                                  ⊢ {⊤} c {⊤}

                ⊢ {ϕ 1 } c {ψ 1 }     ⊢ {ϕ 2 } c {ψ 2 }              ⊢ {ϕ 1 } c {ψ 1 }      ⊢ {ϕ 2 } c {ψ 2 }
        Conj                                                  Case
                     ⊢ {ϕ 1 ∧ ϕ 2 } c {ψ 1 ∧ ψ 2 }                         ⊢ {ϕ 1 ∨ ϕ 2 } c {ψ 1 ∨ ψ 2 }

                ⊢ {ϕ ∗ b ∼ tt} c {ψ ∗ b ∼ tt}             ⊢ {ϕ ∗ b ∼ ff } c {ψ ∗ b ∼ ff }          ψ ∈ SP
        RCase
                                              ⊢ {ϕ ∗ D[b]} c {ψ ∗ D[b]}

                                        ⊢ {ϕ} c {ψ }         FV (η) ∩ MV (c) = ∅
                               Const
                                                     ⊢ {ϕ ∧ η} c {ψ ∧ η}

          ⊢ {ϕ} c {ψ }          FV (η) ∩ MV (c) = ∅           FV (ψ ) ⊆ T ∪ RV (c) ∪ WV (c)                |= ϕ → D[T ∪ RV (c)]
Frame
                                                           ⊢ {ϕ ∗ η} c {ψ ∗ η}

                                                  Fig. 4. Structural rules


Clearly, ϕ ∗ b ∼ tt and ϕ ∗ b ∼ ff are sound post-conditions for the two branches. But c is semantically
equal to x ← b, and D[x] ∗ D[b] is not a sound post-condition.
  In Appendix A, we consider a variant of RCond that proves a weaker post-condition, but relaxes
the requirement on ψ and allows the branches to modify the guard.

4.4     Structural Rules
Fig. 4 collects the final group of rules, the structural rules. Weak, True, Conj, and Case are
standard; RCase is an analog of RCond. The last two rules are more interesting. Const is the
rule of constancy from Hoare logic, which states that formulas η that do not mention any of c’s
modified variables MV (c) may be conjoined to the pre- and post-condition. This rule is not sound
in standard separation logic—motivating the separating conjunction and the frame rule—but it is
sound in PSL: writes cannot invalidate assertions about other variables.
   But, the post-condition in Const does not ensure that ψ and η refer to probabilistically indepen-
dent variables. For this stronger guarantee, we need Frame. The side conditions mention several
classes of variables. Roughly speaking, RV (c) is the set of variables that c may read from, while
WV (c) is the set of variables that c must write to (before possibly reading from). MV (c) is the set of
variables that c may write to, so WV (c) is a subset of MV (c).
   We can approximate these sets using a simple syntactic condition.
Definition 7. RV , WV , MV are defined as follows:
   RV (x r ← er ) ≜ FV (er )                     $ U ) ≜ ∅
                                         RV (x r ←  S                  RV (c ; c ′) ≜ RV (c) ∪ (RV (c ′) \ WV (c))

         RV (if R b then c else c ′) ≜ FV (b) ∪ RV (c) ∪ RV (c ′)                  RV (while b do c) ≜ RV (c)

                     WV (x r ← er ) ≜ {x r } \ FV (er )                              $ U ) ≜ {x }
                                                                             WV (x r ←  S      r

WV (c ; c ′) ≜ WV (c) ∪ (WV (c ′) \ RV (c))               WV (if R b then c else c ′) ≜ (WV (c) ∩ WV (c ′)) \ FV (b)


Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:13




      MV (x r ← e) ≜ {x r }                       $ U ) ≜ {x }
                                          MV (x r ←  S      r                  MV (c ; c ′) ≜ MV (c) ∪ MV (c ′)

          MV (if R b then c else c ′) ≜ MV (c) ∪ MV (c ′)                    MV (while b do c) ≜ MV (c)
  Other analyses are possible, so long as non-modified variables are preserved from input to output,
and output modified variables depend only on input read variables.
Lemma 6 (Soundness for RV , WV , MV ). Let (σ ′, µ ′) = JcK(σ , µ), and let Sr = RV (c), Sw =
WV (c), Sc = RV \ MV (c). Then:
  (1) Variables outside of MV (c) are not modified: πSc (µ ′) = πSc (µ).
  (2) The sets Sr and Sw are disjoint.
  (3) There exists F : RanM[Sr ] → D(RanM[MV (c)]) such that µ ′ = bind(µ, m 7→ F (πSr (m)) ⊗
      unit(πSc (m))).
   Returning to Frame, we consider the side-conditions one by one. The first side-condition is as
in Const; the framing condition η cannot mention any possibly-modified variables. The second
condition states that the post-condition ψ can only mention variables that are (i) in the footprint of ϕ,
or (ii) written by c. The last condition states that any portion of the randomized memory satisfying
ϕ must have a footprint containing T and all variables read by c. Intuitively, these side-conditions
ensure that if the framing condition (i) does not mention modified variables and (ii) is initially
independent of all read variables, then it is independent of all variables in ϕ as well as all written
variables—these variables can only depend on read variables, which were initially all independent
from the framing condition.
Example 3. Using Const, we can derive the following global version of RAssn:
                                                     x r < FV (ϕ, er )
                                   RAssn*
                                            ⊢ {ϕ} x r ← er {ϕ ∧ x r ∼ er }
The set of modified variables is {x r }.
Example 4. Using Frame, we can derive the following global version of RSamp:
                                                      x r < FV (ϕ)
                                   RSamp*
                                            ⊢ {ϕ} x r ←
                                                      $ U {ϕ ∗ U [x ]}
                                                         S      S r

There are no read variables, and the modified and written variables are both {x r }.

4.5    Soundness
As expected, the proof system is sound.
Theorem 2 (Soundness). If ⊢ {ϕ} c {ψ } is derivable, then it is valid: |= {ϕ} c {ψ }.
   We discuss other meta-theoretical properties in Section 7.

5 EXAMPLES: CRYPTOGRAPHIC SECURITY
We demonstrate our logic by proving security for several cryptographic schemes. As we will see,
our logic can express and prove two distinct forms of information-theoretic security properties. For
more convenient encoding of the protocols, we will work with an extended language with arrays,
which can be indexed or assigned to via x[i], and finite tuples, which can be indexed or assigned to
via x .1, x .2, etc. To write compact assertions about arrays, our assertions will use big versions of
                                                      ∗
the conjunctions, written i ∈p(i) ϕ(i) and i ∈p(i) ϕ(i) where i is a fresh logical variable and p is
                               Ó


                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:14                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


deterministic and holds for at most finitely many indices. In some examples we use assignments
of the form x ← e where x ∈ FV (e). Since our assignment rule Rassn does not apply here, these
assignments are short for x f ← e; x ← x f , where x f is a fresh temporary variable. We give proof
sketches in this section; details can be found in Appendix C.
   We will need axioms relating uniformity assertions, pairing, and modular arithmetic, the main
arithmetic operation in our examples. In general, axioms are strongly dependent on the equational
theory of expressions, and it is not clear how to give a complete axiomatization even for just the
modular addition operator; we give axioms schema that are broadly useful for our examples.
Lemma 7. Let q ≥ 2 be any integer, and let {x i } be any finite set of distinct variables. The following
axiom schema are sound.
   |= US1 [x 1 ] ∗ · · · ∗ USn [x n ] ↔ US1 ×···×Sn [(x 1 , . . . , x n )]
   |= UZq [x 1 ] ∗ D[x 2 ] ∗ · · · ∗ D[x n ] ∧ x 0 ∼ x 1 + · · · + x n mod q → UZq [x 0 ] ∗ D[x 2 ] ∗ · · · ∗ D[x n ]
In particular, we will use two derived axioms (writing ⊕ for xor, addition modulo 2):
   |= UZ2 [x 1 ] ∗ D[x 2 ] ∧ x 0 ∼ x 1 ⊕ x 2 → UZ2 [x 0 ] ∗ D[x 2 ]                                               (U4)
   |= UZq [x 1 ] ∗ D[x 2 ] ∗ D[x 3 ] ∧ x 0 ∼ x 1 + x 2 + x 3 mod q → UZq [x 0 ] ∗ D[x 2 ] ∗ D[x 3 ]               (U5)
These axioms also hold for expressions with at most one free variables.

5.1     Warming Up: The One-Time Pad
The one-time pad (OTP) is a simple encryption scheme [Katz and Lindell 2014] enjoying a strong
property called perfect secrecy. The OTP is a triple of algorithms (Gen, Enc, Dec) parameterized by
n ∈ N, which determines the key space K, message space M, and ciphertext space C, each equal
to {0, 1}n :
    • Gen: Select a key k ∈ K uniformly at random.
    • Enck (m): Given a key k ∈ K and message m ∈ M, output the ciphertext c = m ⊕ k.
    • Deck (c): Given a key k ∈ K and ciphertext c ∈ C, output the message m = c ⊕ k.
We model Gen and Enc with the following code, where m is a deterministic input variable:
                                                  $ {0, 1}n ; c ← m ⊕ k
                                                 k←
But why is the OTP perfectly secret, and what does that mean in the first place? A natural way to
define secrecy is to say that “the ciphertext reveals nothing about the plaintext.” We can formalize
this intuitive notion in two ways. One variant requires that an observer’s view is uniformly
distributed for all private inputs.
Definition 8 (Perfect Secrecy as Probabilistic Non-Interference). An encryption scheme Π : M →
D(C) is perfectly secret if for every pair of messages m, m ′ ∈ M and every ciphertext c ∈ C, we have:
                                            Pr[Π(m) = c] = Pr[Π(m ′) = c].
This notion can be seen as probabilistic non-interference, a generalization of a standard information
flow property to the probabilistic setting. As previously noted, perfect secrecy follows from unifor-
mity: if we can show that the output distribution is uniformly distributed, an observer’s view is the
same for all private inputs since the uniform distribution is unique. In other words, it suffices to
show U[c] as a post-condition, where c denotes the (probabilistic) output of Enck (m).
   Another way to define security is to treat the secret input—here, the message—as drawn from a
distribution, and then require the observer’s view to be probabilistically independent of the input
for every distribution on inputs. This formulation captures security through an intuitive reading of
independence: the public output reveals no new information about the secret input.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:15


Definition 9 (Perfect Secrecy as Input Independence). Let M be the message space and let C be the
ciphertext space. Regarding an encryption scheme Π : M → D(C) as the map Π̃ : D(M) → D(M ×C)
that preserves the input distribution, Π is perfectly secret if the random variables M and C are
independent in Π̃(µ) for every input distribution µ over M.
Again, we are done if we can show that the output distribution is independent from the input
distribution. In other words, it suffices to show D[m] ∗ D[c] as a post-condition, where m denotes
the secret input and c denotes the (probabilistic) output of Enck (m).
   Although it turns out that these two formulations of perfect secrecy are equivalent [Katz and
Lindell 2014], the proofs of these properties differ. To demonstrate, we show that the OTP is perfectly
secret according to both definitions by establishing U[c] and D[m] ∗ D[c] as post-conditions.
5.1.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition Ψ ≜ U[c]. Perfect secrecy then follows from Definition 8. We start by adjoining
the random sample for k according to RSamp:
                                                          U[k].
Then, by RAssn*, assigning to c gives
                                                  U[k] ∧ c ∼ m ⊕ k.
The xor axiom (U4) gives the desired post-condition:
                                                       Ψ ≜ U[c].
5.1.2 Proof of Input Independence. Starting from the pre-condition Φ1 ≜ D[m], we would like
to prove the post-condition Ψ ≜ D[m] ∗ U[c], now treating m as a randomized variable; perfect
secrecy then follows from Definition 9. We start by using RSamp* to adjoin the sample k:
                                                      D[m] ∗ U[k].
By RAssn*, assigning to c then gives
                                             D[m] ∗ U[k] ∧ c ∼ m ⊕ k.
Finally, applying the xor axiom (U4) gives
                                                      D[m] ∗ U[c],
which implies the desired post-condition:
                                                   Ψ ≜ D[m] ∗ D[c].
   We now prove both properties for several other constructions.

5.2    Private Information Retrieval
Private information retrieval (PIR) enables a user to retrieve an item from a database server without
the server learning which item was requested [Chor et al. 1995]. For instance, one (highly inefficient)
scheme just has the server send the entire database to the user. When multiple copies of the database
are held by multiple servers, however, significantly more efficient PIR schemes are possible.
   We consider the following single-bit two-server PIR scheme by Chor et al. [1995]. Two non-
colluding servers S0 , S1 store the same N -bit database D. A client C wishes to access the i-th bit of
D, denoted D[i], without either server learning any information about i. To achieve this, C first

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:16                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


uniformly samples an N -bit string q 0 . Then, C sends q 0 to S0 and sends q 1 = q 0 ⊕ I to S1 , where
I ∈ {0, 1} N has value 1 at index i and value 0 everywhere else. Server S0 computes a response r 0 as
                                               Ê
                                                      D[j].
                                                 1≤j ≤N :q 0 [j]=1

Similarly, server S1 computes a response r 1 as
                                             Ê
                                                                     D[j].
                                                 1≤j ≤N :q 1 [j]=1

Finally, C computes r 0 ⊕ r 1 = D[i]. Since it is
                                                          1        q0 ← $ {0, 1} N ;
assumed that S0 and S1 do not collude, the fact
that the queries q 0 and q 1 are each uniformly dis-      2        q1 ← q0 ⊕ I ;
tributed ensure that no information about the             3        for i = 1, . . . , N do
index i is leaked. The fact that q 0 and q 1 are          4           if R q 0 [i] = 1 then a 0 [i] ← D[i];
not independent, however, means that the pro-             5           if R q 1 [i] = 1 then a 1 [i] ← D[i];
                                                                   r0 ←                    a [j];
                                                                           É
tocol does not ensure secrecy in the presence of          6
collusion—information about i may (and in this                             Éj ∈[1, N ] 0
                                                          7        r1 ←         j ∈[1, N ] a 1 [j];
case, does) leak out through different correlations
                                                          8        v ← r0 ⊕ r1;
between q 0 and q 1 .
   The combined program in Fig. 5 models this
                                                       Fig. 5. Private information retrieval (PIR) scheme
protocol (arrays a 0 , a 1 initialized with 0). We es-
tablish security by proving two different properties of the program in our logic: uniformity and
input independence. While both properties amount to the same security property, their proofs are
different and demonstrate our logic’s flexibility.
5.2.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition
                                       Ψ ≜ U[q 0 ] ∧ U[q 1 ] .
                                            |{z} |{z}
                                                     S0 ’s view S1 ’s view
This says that the views of S0 and S1 (q 0 and q 1 , respectively) are uniformly random bitstrings.
  By RSamp, adjoining the sampling for q 0 (line 1) gives
                                                        U[q 0 ].
Since I is a deterministic variable, we can adjoin D[I ]:
                                                    U[q 0 ] ∗ D[I ].
By RAssn*, assigning to q 1 (line 2) gives
                                           U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I .
Next, we can pull out U[q 0 ] like so:
                                    U[q 0 ] ∧ (U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I ).
We then apply the xor axiom (U4) to the right conjunct, giving the desired post-condition:
                                               Ψ ≜ U[q 0 ] ∧ U[q 1 ].
Since q 0 and q 1 are unmodified in the remainder of the program, we can preserve Ψ through to the
end using Const and True.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:17


 1     r0, r1 ←$ {0, 1}k ;

 2     d←  $ {0, 1};

 3     if R d = 0 then rd ← r 0 ; r 1−d ← r 1 else rd ← r 1 ; r 1−d ← r 0 ;
 4     e ← c ⊕ d;
 5     if R e = 0 then f 0 ← m 0 ⊕ r 0 ; f 1 ← m 1 ⊕ r 1 else f 0 ← m 0 ⊕ r 1 ; f 1 ← m 1 ⊕ r 0 ;
 6     if D c = 0 then mc ← f 0 ⊕ rd ; f 1−c ← m 1 ⊕ r 1−d else mc ← f 1 ⊕ rd ; f 1−c ← m 0 ⊕ r 1−d ;

                                        Fig. 6. Oblivious transfer (OT) scheme


5.2.2 Proof of Input Independence. Starting from the pre-condition Φ1 ≜ D[I ], now treating I as a
randomized variable, we would like to prove the post-condition
                                       Ψ ≜ D[I ] ∗ D[q 0 ] ∧ D[I ] ∗ D[q 1 ] .
                                           |{z} |{z} |{z} |{z}
                                              Index   S0 ’s view   Index   S1 ’s view

This says that the views of S0 and S1 (q 0 and q 1 , respectively) are independent of secret index I .
  By RSamp*, adjoining the sampling for q 0 (line 1) gives
                                                      U[q 0 ] ∗ D[I ].
By RAssn*, assigning to q 1 (line 2) gives
                                             U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I .
Next, we can pull out D[I ] ∗ U[q 0 ] like so:
                                   D[I ] ∗ U[q 0 ] ∧ (U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I ).
We then apply the xor axiom (U4) to the right conjunct, giving
                                            D[I ] ∗ U[q 0 ] ∧ D[I ] ∗ U[q 1 ],
which implies the desired post-condition:
                                         Ψ ≜ D[I ] ∗ D[q 0 ] ∧ D[I ] ∗ D[q 1 ].
Since q 0 and q 1 are unmodified in the remainder of the program, we can preserve Ψ through to the
end using Const and True.

5.3    Oblivious Transfer
Oblivious transfer (OT) is a common building block in many cryptographic protocols [Rabin 2005].
It involves two parties: a sender S holding two secrets m 0 , m 1 and a receiver R holding a choice bit
c ∈ {0, 1}. Through the protocol, R learns the secret mc but nothing about m 1−c , while S learns
nothing about c. If the setup can be performed by a trusted third party T , the following simple
protocol implements OT [Rivest 1999]:
   (1) T sends S two random k-bit strings r 0 , r 1 .
   (2) T sends R a random bit d and the string rd .
   (3) R sends S the value e = c ⊕ d.
   (4) S sends R the values f 0 = m 0 ⊕ r e and f 1 = m 1 ⊕ r 1−e .
   (5) R computes mc = fc ⊕ rd .

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:18                                                                           Gilles Barthe, Justin Hsu, and Kevin Liao


As part of the trusted setup in steps 1 and 2, T essentially hands S and R one-time pad keys to
encrypt their secrets. R uses d to encrypt its choice c (step 3), S uses r 0 , r 1 to encrypt its secrets
m 0 , m 1 using R’s message to pick which key to use for which message (step 4), and finally R uses
rd to decrypt one of the secrets (step 5).
   The protocol ensures perfect secrecy for R’s choice c, since e is an encryption of c under the
OTP with key d, which is kept secret from S. The protocol ensures perfect secrecy for one of S’s
secrets m 0 , m 1 , since f 0 , f 1 are encryptions of m 0 , m 1 under the OTP with keys r e , r 1−e , and the fact
that R is given one of the keys (rd ) means that it can decrypt exactly one of f 0 or f 1 .
   The combined program in Fig. 6 models the OT protocol. Stating security for S requires a bit of
work. We first instrument the program with ghost code, shown in gray. Intuitively, the ghost code
computes the encrypted version of the wrong message, i.e., the one that R did not request—the
combined view of R should then be uniform.

5.3.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition

                          Ψ ≜ (Uk×k [(r 0 , r 1 )] ∗ U[e]) ∧ (U[d] ∗ Uk ×k [(rd , f 1−c )]) .
                              |          {z             } |             {z               }
                                         S’s view                       R’s “view”

To establish R ′s secrecy, we need to consider the view of S, which consists of r 0 , r 1 , and e. For R’s
choice c to be kept secret, it is required that Uk ×k [(r 0 , r 1 )] ∗ U[e], i.e., S’s combined view is uniform.
Note that it is not enough to establish that the individual components of S’s view are uniform. To
see why, suppose T also sends S the random bit d, which reveals c = e ⊕ d. Although the individual
components of S’s view would indeed be uniform, i.e., Uk [r 0 ] ∧ Uk [r 1 ] ∧ U[e] ∧ U[d], R’s secrecy
is clearly violated. The stronger post-condition establishes that S’s combined view is uniform.
    To establish S ′s (one-sided) secrecy, we need to consider the view of R, which consists of d,
rd , and one of f 0 or f 1 . In particular, the fi to be considered corresponds to the encryption of the
“wrong” message, which we assign to the ghost variable f 1−c (which is, in turn, computed using the
ghost variable r 1−d ). Similar to R’s secrecy, it is then required that U[d] ∗ Uk ×k [(rd , f 1−c )], i.e., R’s
combined view is uniform.
    We first show R’s secrecy, followed by S’s secrecy, and then combine the results using Conj. By
RSamp and RSamp*, we can adjoin the random samplings for r 0 , r 1 , d (lines 1–2), giving

                                             Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].

Since the free variables of this formula are unmodified in the conditional (line 3), we can preserve
the formula using Const and True. Since c is a deterministic variable we can adjoin D[c], giving

                                         D[c] ∗ Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].

For the assignment to e (line 4), we start from the local pre-condition

                                                    D[c] ∗ U[d].

By RAssn*, assigning to e gives

                                           (D[c] ∗ U[d]) ∧ e ∼ c ⊕ d.

Applying the xor axiom (U4) leaves
                                                        U[e].

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:19


Then, we can frame as follows:
         ⊢ {ϕ} c ′ {ψ }      FV (η) ∩ MV (c ′) = ∅          FV (ψ ) ⊆ FV (ϕ) ∪ WV (c ′)          |= ϕ → D[RV (c ′)]
Frame
                   ⊢ {D[c] ∗ U[d] ∗ Uk [r 0 ] ∗ Uk [r 1 ]} e ← c ⊕ d { U[e] ∗ Uk [r 0 ] ∗ Uk [r 1 ]}
                      | {z } |               {z       } | {z } |{z} |                  {z       }
                             ϕ                     η                   c′         ψ              η                      .
The post-condition implies
                                             Uk ×k [(r 0 , r 1 )] ∗ U[e],
which establishes R’s secrecy. Since r 0 , r 1 , and e are unmodified in the remainder of the program,
we can preserve Uk ×k [(r 0 , r 1 )] ∗ U[e] through to the end using Const.
   Next, we show S’s secrecy. Again, by RSamp and RSamp*, we can adjoin the random samplings
for r 0 , r 1 , d (lines 1–2), giving
                                            Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].
We go through the conditional (line 3) with RCond, which gives pre-condition
                                            Uk [r 0 ] ∗ Uk [r 1 ] ∗ d = 0 ∼ tt.
To go through the first assignment, we start from the local pre-condition
                                                         Uk [r 0 ].
By RAssn*, assigning to rd gives
                                                   Uk [r 0 ] ∧ rd ∼ r 0 .
Transferring the distribution law gives
                                                Uk [rd ].
We can then frame in Uk [r 1 ] ∗ d = 0 ∼ tt giving
                                            Uk [rd ] ∗ Uk [r 1 ] ∗ d = 0 ∼ tt.
The second assignment follows similarly, this time starting from the local pre-condition
                                                          Uk [r 1 ]
and giving the following post-condition in the true branch
                                           Uk [rd ] ∗ Uk [r 1−d ] ∗ d = 0 ∼ tt.
The false branch yields the same post-condition, which, by RCond, brings us to the post-condition
                                              Uk [rd ] ∗ Uk [r 1−d ] ∗ U[d].
Since the free variables of this formula are unmodified in lines 4–5, we can preserve this formula
through using Const and True. Next, we go through the deterministic conditional (line 6) using
DCond. In the true branch, we start with pre-condition
                                     Uk [rd ] ∗ Uk [r 1−d ] ∗ U[d] ∧ (c = 0) = tt.
Dropping the right conjunct, we can adjoin D[m 1 ] like so
                                         Uk [rd ] ∗ D[m 1 ] ∗ Uk [r 1−d ] ∗ U[d],
since m 1 is a deterministic variable. We preserve this formula through the first assignment to mc
using Const and True, and then go through the second assignment to f 1−c starting from the local
pre-condition
                                         D[m 1 ] ∗ Uk [r 1−d ].
Applying RAssn* and the xor axiom (U4) gives
                                                        Uk [f 1−c ].

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:20                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


Framing in Uk [rd ] ∗ U[d] gives the following post-condition in the true branch
                                             Uk [rd ] ∗ Uk [f 1−c ] ∗ U[d].
The false branch yields the same post-condition. Then, we can merge Uk [rd ] ∗ Uk [f 1−c ] and
rearrange like so
                                  U[d] ∗ Uk ×k [(rd , f 1−c )].
This establishes S’s secrecy. Combining the formulas establishing R’s secrecy and S’s secrecy
using Conj gives the desired post-condition.
5.3.2 Proof Attempt: Input Independence. Again, we can try to prove security via input indepen-
dence instead of uniformity. Starting from the pre-condition
                                         Φ1 ≜ D[c] ∧ D[m 0 ] ∧ D[m 1 ],
we would like to prove the post-condition
        Ψ ≜ ( D[c] ∗ (D[r 0 ] ∧ D[r 1 ] ∧ D[e])) ∧ (D[m 1−c ] ∗ (D[d] ∧ D[rd ] ∧ D[f 0 ] ∧ D[f 1 ])).
             |{z} |             {z           }      | {z } |                  {z                 }
          R’s secret choice       S’s view            S’s unselected secret               R’s view

To establish R ′s secrecy, we need to show that the secret choice c is independent from S’s view.
Similarly, to establish S’s (one-sided) secrecy, we need to show that the unselected secret, which
we assign to the ghost variable m 1−c is independent from R’s view.
  However, here we run into difficulties—it does not seem possible to prove this judgment in our
logic, and even sketching a proof on paper is not easy. In general, stating and proving perfect
security as input independence is trickier when there are multiple parties, like in OT. Investigating
how to prove this kind of property is an interesting direction for further work.

5.4     Multi-Party Computation
Secure multi-party computation (MPC) allows
mutually untrusting parties to jointly com- 1                     for i = 1, . . . , 3 do
pute a function of their private inputs with-             2         r [i].1 ←
                                                                            $ Z ;
                                                                                   p
out revealing them [Goldreich et al. 1987; Yao            3         r [i].2 $ Z ;
                                                                            ← p
1986]. The parties agree on a function f and 4                      r [i].3 ← x[i] − r [i].1 − r [i].2 mod p;
then use an MPC protocol to securely com- 5                       for i = 1, . . . , 3 do
pute v = f (x 1 , . . . , x n ), where x i is party Pi ’s 6         s[i] ← r [1].i + r [2].i + r [3].i mod p;
private input. MPC guarantees that parties 7                     v ← s[1] + s[2] + s[3] mod p;
learn v, and nothing more.
    As an example, we consider secure com-                  Fig. 7. Three-party secure addition protocol
putation of addition,   Ín       i.e., of the function
f (x 1 , . . . , x n ) = i=1 x i [Cramer et al. 2015]. This simple function turns out to be surprisingly
useful, for example, for privately totaling salaries of employees in a company or votes in secure
electronic voting. Secure addition can be achieved by the following simple protocol with inputs
x i ∈ Zp , where p is a fixed prime number agreed upon in advance. We describe the three-party case
for simplicity, but the protocol easily extends to n parties.
  (1) Each Pi encodes their input as three secret shares by choosing r i,1 , r i,2 uniformly at random
      in Zp and setting r i,3 = x i − r i,1 − r i,2 mod p.
  (2) Each Pi sends r i,2 , r i,3 to P1 , r i,1 , r i,3 to P2 , and r i,1 , r i,2 to P3 .
  (3) Each P j computes the sum s ℓ = r 1, ℓ + r 2, ℓ + r 3, ℓ mod p for ℓ , j and sends s ℓ to all parties.
  (4) All parties compute the result v = s 1 + s 2 + s 3 mod p.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                     55:21


The end-to-end security of the protocol, i.e., that parties learn no new information beyond the
output v, is subtle to prove. In a nutshell, the security of the protocol is usually established by
simulation [Lindell 2017], a proof technique that is pervasive in cryptography but does not have a
clean translation to our logic. The interested reader should see the monograph by Cramer et al.
[2015].
   The security of secret sharing, however, is expressible in our logic. Informally, the protocol splits
each secret into three pieces (“shares”), and the security property ensures that knowing at most
two of the three shares reveals no information about the secret. In step (1), each party generates
shares of their secret input x i by selecting r i,1 , r i,2 , r i,3 uniformly at random from Zp , subject to the
constraint that the shares add up to x i . In step (2), each party distributes secret shares in such a way
that no other party learns any information about their secret input. For concreteness, consider P 2 ’s
view: It knows the values r i,1 and r i,3 , and that x i = r i,1 + r i,2 + r i,3 mod p, but since r i,2 is chosen
uniformly from Zp , any value of x i is equally likely. Thus, no information about x i is leaked.
   The combined program in Fig. 7 models the secure addition protocol; the secret sharing steps
correspond to lines 1–4. Like in our previous examples, we prove the security of secret sharing in
two ways: by establishing uniformity and input independence.

5.4.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition
            Û                               Û                              Û
     Ψ≜             U[(r [α].2, r [α].3)] ∧        U[(r [α].1, r [α].3)] ∧        U[(r [α].1, r [α].2)] .
          α ∈ {2,3}
                    |       {z         } α ∈ {1,3} |       {z         } α ∈ {1,2} |       {z         }
                        P1 ’s view from P α                 P2 ’s view from P α               P 3 ’s view from P α

This says that each party’s view from the other parties is uniform and independent.
  To prove this post-condition, we take the following for-loop invariant:

                     ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                   α ∈[1,i)

By RSamp*, adjoining the random samplings for r [i].1 and r [i].2 (lines 2 and 3) gives

     U[r [i].1] ∗ U[r [i].2] ∗       ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                                   α ∈[1,i)

To go through the assignment to r [i].3 (line 4), we start from the local pre-condition
                                                 U[r [i].1] ∗ U[r [i].2].
By RAssn*, assigning to r [i].3 gives
                       U[r [i].1] ∗ U[r [i].2] ∧ r [i].3 ∼ x[i] − r [i].1 − r [i].2       mod p.
Applying the modular addition axiom (U5) and merging pairwise independent assertions gives
                          U[(r [i].1, r [i].2)] ∧ U[(r [i].2, r [i].3)] ∧ U[(r [i].1, r [i].3)].
Framing in the invariant for the earlier iterations establishes the loop invariant in DFor, giving:

                     ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                   α ∈[1,3]

After rearranging and dropping terms, this formula implies the desired post-condition Ψ. Since the
free variables of Ψ are unmodified in the remainder of the program, we can preserve it through to
the end using Const and True, establishing uniformity.

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:22                                                                                   Gilles Barthe, Justin Hsu, and Kevin Liao


5.4.2   Proof of Input Independence. Starting from the pre-condition
                                               Û
                                        Φ1 ≜        D[x[α]],
                                                        α ∈[1,3]

we would like to prove the post-condition
               Û                                         Û
       Ψ≜              D[x[α]] ∗ D[(r [α].2, r [α].3)] ∧        D[x[α]] ∗ D[(r [α].1, r [α].3)] ∧
             α ∈ {2,3}
                       | {z } |          {z         } α ∈ {1,3} | {z } |         {z          }
                         P α ’s input   P1 ’s view from P α                    P α ’s input   P2 ’s view from P α
                                                                     Û
                                                                               D[x[α]] ∗ D[(r [α].1, r [α].2)] .
                                                                   α ∈ {1,2}
                                                                               | {z } |          {z         }
                                                                               P α ’s input     P3 ’s view from P α

This says that, for each party, the secret input of each other party is independent from the view
they generate. We defer details of this proof to Appendix C.

5.5     Simple Oblivious RAM
Consider a core programming language defined by the following syntax:
                                P ::= ϵ | i; P   where i ::= read(x) | write(x, v)
with x ranging over a set X of registers and v ranging over integers Z. A simple execution model
for this language is random access memory (RAM). Informally, a RAM machine maintains a partial
mapping from registers to integers, a program counter that tracks which instruction is to be
executed next, and reads and updates the mapping according to the program instructions.
   Oblivious RAM (ORAM) [Goldreich 1987; Goldreich and Ostrovsky 1996] is a probabilistic
execution model guaranteeing that an adversary who observes the sequence of accessed memory
locations—but not their contents—only learns the length of the program. The basic idea of ORAM is
to maintain a mapping from logical addresses accessed by the client program to physical addresses
where data is stored; this mapping is re-scrambled after each read and write. We consider a simple
and idealized variant of ORAM inspired by Chung and Pass [2013], and use our logic to prove its
security.
5.5.1 Definition of Simple ORAM. ORAM assumes a memory model split into two parts: an external,
insecure bulk memory where accesses are visible to the adversary, and an internal, secure memory
with a small number of registers where accesses are not visible to the adversary. In our variant, the
internal memory stores a so-called position map, while the external memory is organized into a tree
where values can be read and written. We treat the external memory a as a map from addresses
to buckets. Addresses are bitstrings of length at most n; they are partially ordered by the prefix
relation, and are thus structured as a tree. Leaf addresses are bitstrings of length exactly n. Each
node of the tree stores a bucket a list of triples of the form (x, v, l), where x ∈ X is a register, v ∈ Z
is an integer, and l ∈ {0, 1}n is a leaf address. One key invariant of the ORAM scheme is that (x, v, l)
will be stored in some bucket along the path from root address ϵ to leaf address l, i.e. in a bucket
a[i] at some address i that is a prefix of l. The position map p is a mapping from registers x ∈ X to
leaf addresses; this mapping ensures obliviousness by introducing a level of indirection.
   We briefly describe the semantics of the read(x) instruction; Fig. 8 illustrates an example. To
retrieve the value of x, we read p[x] from the position map and then search through all buckets
along the path from ϵ to p[x] for a triple of the form (x, u, p[x]) (Fig. 8 (a)). Once the triple is found, it
is removed from its bucket. In order to guarantee obliviousness, it is necessary to read all addresses
along the path to the leaf, regardless of where the target entry is found. Once the leaf is reached,
we sample a fresh bitstring l of length n, add (x, u, l) to the bucket a[ϵ], and then update p[x] to

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                                   55:23


                      ... 01 ... ...                            ... 11 ... ...                        ... 11 ... ...


          ( , , 01)                                            [ ]               ( , , 11)                             ( , , 11)

                 0                     1                   0                      1               0                     1
           [0]                                                                                               [1]

            00           01 10             11         00             01 10            11     00          01 10              11




                      (a) read(x)                          (b) Update p[x]                            (c) flush

                                                      Fig. 8. Simple ORAM


hold l (Fig. 8 (b)). The semantics of the write(x, v) instruction is similar, except that the updated
entry (x, v, l) is added to the bucket a[ϵ].
   While the operations so far ensure obliviousness, all triples will accumulate at the root of the
tree, i.e., in the bucket a[ϵ]. To better balance the buckets, each read or write operation is followed
by a flush operation, which samples another bitstring l of length n and then traverses the tree from
root ϵ to leaf l while pushing every triple (x, v, l ′) along its path as far down as possible, namely, to
bucket a[lcp(l, l ′)] where lcp(l, l ′) is the longest common prefix of l and l ′ (Fig. 8 (c)).
   Fig. 9 defines the oblivious semantics of core language programs by compilation to pWhile. To
model the adversary’s view of the accesses, the compilation instruments the code to store leakage
information in the variable ℓ, as explained below. We briefly comment on the notation and operators.
We use [] for the empty list, :: for adding an element to a list, and + for concatenating two lists.
Given a bitstring i of length n and k ≤ n, we let i[1, . . . , k] be the bitstring of length k consisting of
the first k bits of i; we let i[1, . . . , 0] = ϵ denote the empty bitstring. The operator split {(x,v,l )|ϕ }
iterates over a list of triples and returns two sublists of elements satisfying ϕ and elements not
satisfying ϕ respectively, where ϕ can mention (x, v, l).
5.5.2 Security of Simple ORAM. Informally, the leakage of a program is the sequence of internal
memory accesses performed during program execution. Formally, we introduce the events r a[i]
and w a[i] for reading and writing address i; note that reading or writing an internal address does
not leak any information. Leakage is then defined as a sequence of events. For instance, the leakage
for instructions read(x) or write(x, v) is the sequence:
                 r a[ϵ], w a[ϵ], r a[p[x][1]], w a[p[x][1]], . . . , r a[p[x]], w a[p[x]], w a[ϵ].
The leakage of a program is the concatenation of the leakage of its instructions. Obliviousness
states that executing two different programs with the same number of instructions induce the same
leakage, and that the leakage does not depend on the initial contents of the ORAM.
   Our proof uses an equivalent definition of obliviousness that is more convenient for our purposes.
Concretely, we encode the leakage of instructions read(x) and write(x, v) by p[x]. Redefining the
leakage in this way does not affect the definition of obliviousness, but the advantage is that we
can show obliviousness by proving that the leakage of a program P of length k is uniform over
bitstrings of length 2 · n · k.3 Our compilation adds ghost code to record this leakage in an array ℓ
indexed by the program counter c, which tracks the index of the current instruction. Concretely, we

3 In contrast, using the straightforward definition of leakage would require proving that a block of memory accesses is

uniform over paths from root to leaf. Although this can also be done in our logic, the proof becomes more cumbersome.


                                       Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:24                                                                            Gilles Barthe, Justin Hsu, and Kevin Liao

                  Compilation of read                                          Compilation of write
 C(read(x)) =                                                  C(write(x, v)) =
  1    ℓ[c].1 ← p[x];                                           1    ℓ[c].1 ← p[x];
  2    w ← [];                                                  2    w ← [];
  3    for j = 1, . . . , n do                                  3    for j = 1, . . . , n do
  4       (w ′, a[p[x][1, . . . , j]]) ←                        4       (w ′, a[p[x][1, . . . , j]]) ←
  5          split {(y,−,−) |x =y } (a[p[x][1, . . . , j]]);    5          split {(y,−,−)|x =y } (a[p[x][1, . . . , j]]);
  6       w ← w + w ′;                                          6       w ← w + w ′;
  7    (y, u, l) ← head(w);                                     7    (y, u, l) ← head(w);
  8    p[x] ←  $ {0, 1}n ;                                      8    p[x] ←  $ {0, 1}n ;

  9    a[ϵ] ← (x, u, p[x]) :: a[ϵ]                              9    a[ϵ] ← (x, v, p[x]) :: a[ϵ]
                      Flush operation                                       Compilation of programs
 flush =                                                                 C(i; P) = C(i) ; flush ; c ← c + 1 ; C(P)
  1     l←$ {0, 1}n ;                                                    C(ϵ) = skip
  2     ℓ[c].2 ← l;
  3     w ← [];
  4     for j = 1, . . . , n do
  5        (a[l[1, . . . , j]], w) ← split {(−,−,l ′ ) |lcp(l,l ′ )=l [1, ...,i]} (a[l[1, . . . , j]] + w)

            Fig. 9. Compiling programs. Grayed instructions is ghost code used to record leakage.


add an assignment ℓ[c].1 ← p[x] at the beginning of each instruction (line 1 in both read and write
compilation), and an assignment ℓ[c].2 ← l in corresponding flush operations (line 2 in flush).
  Under our encoding, proving security of the ORAM scheme reduces to showing that for every
program P of length k in our core language, the leakages (ℓ[1].1, ℓ[1].2), . . . , (ℓ[k].1, ℓ[k].2) are
independently and uniformly distributed in the post-condition of the compiled version of P.
  We sketch how to formalize this property as a uniformity property in our logic; details are in
Appendix C. The overall strategy is to show that after each instruction-flush pair, the entries of the
position map and the leakage are uniform and mutually independent. We establish two judgments
                                {Φ(j)} C(read(x)) ; flush ; c ← c + 1 {Φ(j + 1)}
                              {Φ(j)} C(write(x, v)) ; flush ; c ← c + 1 {Φ(j + 1)}
for every j, where the invariant is defined to be
                           Φ(j) ≜ c = j ∧       ∗ U[(ℓ[β].1, ℓ[β].2)] ∗ ∗ U[p[α]].
                                              β ∈[1,c)                          α ∈X

Starting from the pre-condition Φ1 ≜ Φ(1), which asserts that the position map is initialized
uniformly and independently, repeatedly applying Seqn establishes
                                               {Φ(1)} C(P) {Φ(k + 1)}.
The post-condition implies our desired assertion:
                                           Ψ≜      ∗ U[(ℓ[β].1, ℓ[β].2)],
                                                 β ∈[1,k ]

which says that the distribution of instruction-flush leakage pairs is uniform and independent.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:25


   Discussion. The ORAM scheme by Chung and Pass [2013] has several additional wrinkles. First,
they define a recursive ORAM, which uses a hierarchy of trees to reduce the internal memory; this
construction can be encoded in our language, and we conjecture that our proof can be extended
to this more complex setting. Moreover, Chung and Pass [2013] initialize the position map lazily,
i.e. for every instruction write(x, v), the ORAM checks whether the position map for x is already
defined, and samples a fresh bitstring and extends the position map otherwise. This lazy version
can be modeled using conditionals, and our proof can be adapted to this variant.
   Chung and Pass [2013] also assume that buckets have a maximal size. As a consequence, execution
may fail if buckets overflow. Formalizing this variant requires care. One option would be to prove
that the leakage trace is uniform conditioned on execution not failing, and that the probability of
failing is small. However, dealing with conditional uniformity is challenging. A better solution may
be to compare the distributions induced by executing the program with finite buckets and with
infinite buckets, showing that these distributions are close.

6   RELATED WORK
The intersection of programming languages and security is broad; we limit our attention to the
most directly relevant work.

   Probabilistic independence. Our logic is the first program logic where probabilistic independence
is the central concept, but previous systems have also touched on independence. Darais et al. [2020]
define a type and effect system for proving properties of probabilistic computations. Their effect
system is based on a new notion of probabilistic region, which they use to track probabilistic
dependencies. Their type system uses affine typing to ensure that random variables are used at most
once. They show the expressiveness of their type and effect system with examples of simple ORAM
and tree-based ORAM. Although the two approaches have some similarities, it seems challenging
to compare the expressiveness of their type and effect system and of our logic. One advantage of
our logic is that it admits an intuitive interpretation based on bunched logics.
   Barthe et al. [2009] define probabilistic Relational Hoare Logic (pRHL), a program logic for
proving relational specifications of probabilistic programs. Their logic provides a flexible framework
for proving information flow properties of programs. These approaches are able to deal with
Private Information Retrieval, Multi-Party Computation, but are otherwise incomparable to ours.
In particular, it seems difficult to use their approaches for proving security of ORAM in pRHL,
without using an additional proof technique called Eager/Lazy Sampling. On the other hand, they
can prove that von Neumann’s trick, an algorithm to simulate a fair coin using a biased coin, yields
a uniform distribution, which appears out of reach of our current proof system. Barthe et al. [2017]
also show how to use this logic to prove uniformity and independence for probabilistic programs,
but these assertions can only be established at the end of the program.
   PSL is also related to Ellora, a program logic for probabilistic programs [Barthe et al. 2018].
Ellora works with a more standard assertion logic based on first order logic, and allows assertions
to directly describe probabilities of events. This expressivity means that it is possible to reason
about independence as a defined assertion. Barthe et al. [2018] propose an “independence logic” as a
subsystem, but the rules are limited (e.g., it is not possible to reason about probabilistic control flow).
In contrast, probabilistic independence in PSL is handled implicitly by means of a substructural logic.
While this kind of logic is a bit exotic, we find that it makes it possible to represent independence
assertions more compactly and integrate with mathematical axioms more smoothly.
   In more specialized contexts, Smith [2003] and Hoang et al. [2015] develop type systems for
proving computational security of modes of operation and authenticated encryption schemes. Their
type system enforces a strong invariant probabilistic independence between different expressions,

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:26                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


although the type system in itself does not feature any specific judgment for probabilistic inde-
pendence. It would be very interesting to understand whether their results could be emulated and
generalized in our program logic. In a similar spirit, Barthe et al. [2015] develop a proof system for
proving that programs are protected against power side-channels. Their proof system makes an
implicit but critical use of independence.
   On the more foundational side, Ackerman et al. [2019] study computability issues for (conditional)
independence. Their work is partially motivated by exchangeable sequences, which are closely
related to independence. Language-based investigations of exchangeable sequences can be found
for instance in Staton et al. [2018]. It would be interesting to investigate how to reason about
exchangeable sequences in our logic.
   Separation logics for probabilistic programs. There have been two recent proposals for probabilistic
separation logics. Batz et al. [2019] developed a logic QSL for reasoning about probabilistic, heap-
manipulating programs. There, the connectives in BI are interpreted as acting on expectations,
real-valued analogs of state predicates. Tassarotti and Harper [2019] have also developed a relational
separation program logic for reasoning about concurrent probabilistic programs. Both of these
logics leverage standard notions of separation, from heap separation logic and concurrent separation
logic, respectively.
   BI and separation logics. Our work builds on fruitful lines of research on bunched implications
and separation logic. On the bunched implications side, our model uses the resource interpretation
of BI [Pym et al. 2004]; readers should consult Pym [2002] or Docherty [2019] for more information.
The idea of using separation to model probabilistic independence has been considered before [Lozes
2010],4 but we are not aware of concrete results in this area. From a different point of view,
Simpson [2018] develops categorical structures for independence and conditional independence,
encompassing independence in heaps, nominal sets, and probability distributions. On the separation
logic side, by varying the notion of separation our work is another instance of separation logic,
alongside heap separation logic [Ishtiaq and O’Hearn 2001; O’Hearn et al. 2001] and concurrent
separation logic [Brookes 2007; O’Hearn 2007]. These areas are too vast to survey here; the draft
notes by Reynolds [2008] are a good place to start.

7 CONCLUSION AND FUTURE DIRECTIONS
We have presented a novel separation logic for probabilistic programs, using a probabilistic variant
of the logic BI where separation models probabilistic independence. Proofs in the separation
logic reason in terms of higher-level properties like independence and uniformity, and we have
demonstrated our logic to prove two forms of cryptographic security for a number of interesting
protocols. We see many possible directions for interesting future work.
   Completeness and decidability. Our logic is not complete: there are semantically valid judgments
that are not provable from our proof rules. There are several sources of incompleteness. First, the
proof rules for randomized conditionals is incomplete: it only allows parts of the pre-condition that
are independent of all variables in the guard expression to be carried into the branches, while a
finer analysis could allow more general pre-conditions to be preserved or modified in a controlled
way. Another source of incompleteness is the interplay between uniformity, independence, and the
equational theory of the expression language; even with just the xor operator, it is not clear how to
give a complete axiomatization.
   On the positive side, our logic may be relatively complete under the following provisos: expres-
sions are variables (i.e., the expression language has no operators); programs are straightline code
4 Peter O’Hearn and David Pym, personal communication.



Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:27


(i.e., sequences of assignments); and assertions are regular or separating conjunctions of uniformity
and equality predicates. In this specific case, it could be possible to reflect a complete dependency
analysis into the program logic; since entailment between our restricted set of assertions is decidable,
this fragment of the logic may also be decidable.
    Decidability of entailment for larger classes of assertions is also an interesting open problem. The
formulas in our logic bear a superficial resemblance to the “pointer logic” underlying heap separation
logic. Decidability for some restricted fragments follows from a small model property [Yang 2001].
Unlike heap models of BI, our probabilistic model works with a fixed collection of locations; however,
our setting has probabilistic correlations. We conjecture that fragments of our logic may also enjoy
a small model property, perhaps by tracking which subsets of variables are mutually independent.

   Enriching the assertion logic. The assertion logic we have presented is based on intuitionistic,
propositional BI. We have found this logic to be convenient to work with, but other choices are
certainly possible. One natural alternative is to work with a classical logic instead of an intuitionistic
one; in standard separation logic, a classical logic supports a useful, backwards style of reasoning
through the “magic wand” connective. In the probabilistic setting, a classical logic runs into trouble
because probabilistic separation seems too strong—we cannot freely assume that a variable is
independent of the rest of the random variables. However, it may be possible to weaken the
notion of separation to allow randomness to be shared in tightly controlled ways; we are currently
investigating a non-commutative version of BI for this purpose.
   There are also natural extensions to our intuitionistic logic. Developing a probabilistic model
of predicate BI [Pym 1999] would allow substantially richer assertions. In particular, the lack of
existential quantifiers in our logic complicates our proofs and seems to be an obstacle to defining a
strongest post-condition calculus. Extending the logic to support reasoning about conditioning
would also help make the proof rules more precise.

   Supporting quantitative reasoning. While the assertions in our logic describe probability distribu-
tions, our logic notably does not support quantitative reasoning: it is not possible to describe the
probability of an event, or the expected value of a function. This stands in sharp contrast to other
deductive techniques for probabilistic programs, such as PPDL [Kozen 1985] and pGCL [Morgan
et al. 1996]. Incorporating some of these tools for reasoning about numeric probabilities could
extend the reach of our logic. One possibility is to make an approximate version of the logic with
judgments of the form ⊢ϵ {ϕ} c {ψ }, stating that the output distribution is at distance at most ϵ of a
distribution satisfying ψ . Such a logic could be obtained by combining ideas of PSL with the union
bound logic of Barthe et al. [2016], and could be used to reason about more advanced versions of
our examples and further examples from the cryptographic literature (e.g., the PRF/PRP Switching
Lemma of Impagliazzo and Rudich [1988]).

   Modeling more advanced properties and cryptographic constructions. We have focused on basic,
information-theoretic security properties from cryptography in this paper. It would be interesting
to understand whether our logic can be used to capture other properties (e.g., active security).
Similarly, it would be interesting to explore potential applications of our logic to other constructions,
including more complex variants of the constructions we have considered, e.g., Tree ORAM [Gentry
et al. 2013; Shi et al. 2011], Path ORAM [Stefanov et al. 2013], Multi-Server ORAM [Chan et al.
2018] as well as other constructions, such as history independent data structures [Micciancio 1997;
Naor and Teague 2001; Wang et al. 2014]. More speculatively, it would be interesting to understand
whether our logic could be used for reasoning about computational security, or approximate notions
of independence and uniformity.

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:28                                                                              Gilles Barthe, Justin Hsu, and Kevin Liao


ACKNOWLEDGMENTS
We thank the anonymous reviewers and our shepherd Ohad Kammar for their close reading and
useful suggestions. The present work was sparked during a workshop at McGill University’s
Bellairs Research Institute. This work was also partially supported by Office of Naval Research
under projects N00014-12-1-0914, N00014-15-1-2750, and N00014-19-1-2292, the University of
Wisconsin, a Facebook TAV grant, an NSF Graduate Research Fellowship, and the Max Planck
Institute for Software-Systems for hosting some of the authors.


REFERENCES
Nathanael L. Ackerman, Jeremy Avigad, Cameron E. Freer, Daniel M. Roy, and Jason M. Rute. 2019. On the computability of
   graphons. In IEEE Symposium on Logic in Computer Science (LICS), Vancouver, British Columbia.
Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Benjamin Grégoire, and Pierre-Yves Strub. 2015.
   Verified Proofs of Higher-Order Masking. In IACR International Conference on the Theory and Applications of Cryptographic
   Techniques (EUROCRYPT), Sofia, Bulgaria (Lecture Notes in Computer Science), Vol. 9056. Springer-Verlag, 457–485.
   https://doi.org/10.1007/978-3-662-46800-5_18
Gilles Barthe, Thomas Espitau, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2018. An Assertion-
   Based Program Logic for Probabilistic Programs. In European Symposium on Programming (ESOP), Thessaloniki, Greece.
   arXiv:cs.LO/1803.05535 https://arxiv.org/abs/1803.05535
Gilles Barthe, Thomas Espitau, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2017. Proving uniformity and
   independence by self-composition and coupling. In International Conference on Logic for Programming, Artificial Intelligence
   and Reasoning (LPAR), Maun, Botswana (EPiC Series in Computing), Vol. 46. 385–403. http://www.easychair.org/
   publications/paper/340344
Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves Strub. 2016. A Program Logic for Union
   Bounds. In International Colloquium on Automata, Languages and Programming (ICALP), Rome, Italy (Leibniz International
   Proceedings in Informatics), Vol. 55. Schloss Dagstuhl–Leibniz Center for Informatics, 107:1–107:15. https://doi.org/10.
   4230/LIPIcs.ICALP.2016.107 arXiv:cs.LO/1602.05681
Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. 2009. Formal certification of code-based cryptographic
   proofs. In ACM SIGPLAN–SIGACT Symposium on Principles of Programming Languages (POPL), Savannah, Georgia. 90–101.
   https://doi.org/10.1145/1480881.1480894
Gilles Barthe, Justin Hsu, and Kevin Liao. 2020. A Probabilistic Separation Logic. Proceedings of the ACM on Programming
   Languages 4, POPL (Jan. 2020). arXiv:cs.PL/1907.10708 https://arxiv.org/abs/1907.10708
Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Thomas Noll. 2019. Quantitative
   separation logic: a logic for reasoning about probabilistic pointer programs. Proceedings of the ACM on Programming
   Languages 3, POPL (2019), 34:1–34:29. https://doi.org/10.1145/3290347
Stephen Brookes. 2007. A semantics for concurrent separation logic. Theoretical Computer Science 375, 1–3 (2007), 227–270.
   https://doi.org/10.1016/j.tcs.2006.12.034
T.-H. Hubert Chan, Jonathan Katz, Kartik Nayak, Antigoni Polychroniadou, and Elaine Shi. 2018. More is Less: Perfectly
   Secure Oblivious Algorithms in the Multi-server Setting. In International Conference on the Theory and Application of
   Cryptology and Information Security (ASIACRYPT), Brisbane, Australia (Lecture Notes in Computer Science), Thomas Peyrin
   and Steven D. Galbraith (Eds.), Vol. 11274. Springer-Verlag, 158–188. https://doi.org/10.1007/978-3-030-03332-3_7
Benny Chor, Oded Goldreich, Eyal Kushilevitz, and Madhu Sudan. 1995. Private information retrieval. In IEEE Symposium
   on Foundations of Computer Science (FOCS), Milwaukee, Wisconsin. 41–50.
Kai-Min Chung and Rafael Pass. 2013. A Simple ORAM. IACR Cryptology ePrint Archive 2013 (2013), 243. http://eprint.iacr.
   org/2013/243
Ronald Cramer, Ivan Bjerre Damgård, and Jesper Buus Nielsen. 2015. Secure Multiparty Computation. Cambridge University
   Press.
David Darais, Chang Liu, Ian Sweet, and Michael Hicks. 2020. A Language for Probabilistically Oblivious Computation.
   Proceedings of the ACM on Programming Languages 4, POPL (Jan. 2020). http://arxiv.org/abs/1711.09305
Simon Docherty. 2019. Bunched Logics: A Uniform Approach. Ph.D. Dissertation. University College London.
Thomas Ehrhard, Michele Pagani, and Christine Tasson. 2018. Measurable cones and stable, measurable functions: a
   model for probabilistic higher-order programming. Proceedings of the ACM on Programming Languages 2, POPL (2018),
   59:1–59:28. https://doi.org/10.1145/3158147
Didier Galmiche, Daniel Méry, and David J. Pym. 2005. The semantics of BI and resource tableaux. Mathematical Structures
   in Computer Science 15, 6 (2005), 1033–1088. https://doi.org/10.1017/S0960129505004858


Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                        55:29


Craig Gentry, Kenny A. Goldman, Shai Halevi, Charanjit S. Jutla, Mariana Raykova, and Daniel Wichs. 2013. Optimizing
   ORAM and Using It Efficiently for Secure Computation. In International Symposium on Privacy Enhancing Technologies
   (PETS), Bloomington, Indiana (Lecture Notes in Computer Science), Vol. 7981. Springer-Verlag, 1–18. https://doi.org/10.
   1007/978-3-642-39077-7_1
Michèle Giry. 1982. A categorical approach to probability theory. In Categorical Aspects of Topology and Analysis. Springer
   Berlin Heidelberg, Berlin, Heidelberg, 68–85.
Oded Goldreich. 1987. Towards a Theory of Software Protection and Simulation by Oblivious RAMs. In ACM SIGACT
   Symposium on Theory of Computing (STOC), New York, New York, Alfred V. Aho (Ed.). 182–194. https://doi.org/10.1145/
   28395.28416
Oded Goldreich, Silvio Micali, and Avi Wigderson. 1987. How to play any mental game. In ACM SIGACT Symposium on
   Theory of Computing (STOC), New York, New York. 218–229.
Oded Goldreich and Rafail Ostrovsky. 1996. Software Protection and Simulation on Oblivious RAMs. Journal of the ACM 43,
   3 (1996), 431–473. https://doi.org/10.1145/233551.233553
Viet Tung Hoang, Jonathan Katz, and Alex J. Malozemoff. 2015. Automated Analysis and Synthesis of Authenticated
   Encryption Schemes. IACR Cryptology ePrint Archive 2015 (2015), 624. http://eprint.iacr.org/2015/624
Russell Impagliazzo and Steven Rudich. 1988. Limits on the Provable Consequences of One-way Permutations. In IACR
   International Cryptology Conference (CRYPTO), Santa Barbara, California (Lecture Notes in Computer Science), Vol. 403.
   Springer, 8–26. https://doi.org/10.1007/0-387-34799-2_2
Samin S. Ishtiaq and Peter W. O’Hearn. 2001. BI as an assertion language for mutable data structures. In ACM SIGPLAN–
   SIGACT Symposium on Principles of Programming Languages (POPL), London, England. 14–26. https://dl.acm.org/citation.
   cfm?id=375719
Jonathan Katz and Yehuda Lindell. 2014. Introduction to Modern Cryptography. Chapman and Hall/CRC.
Dexter Kozen. 1981. Semantics of Probabilistic Programs. J. Comput. System Sci. 22, 3 (1981), 328–350. https://doi.org/10.
   1016/0022-0000(81)90036-2
Dexter Kozen. 1985. A Probabilistic PDL. J. Comput. System Sci. 30, 2 (1985). https://doi.org/10.1016/0022-0000(85)90012-1
Yehuda Lindell. 2017. How to simulate it–a tutorial on the simulation proof technique. In Tutorials on the Foundations of
   Cryptography. Springer-Verlag, 277–346.
Étienne Lozes. 2010. Towards information as resource in separation logic. Draft presented at FCS-PrivMod, Edinburgh.
Daniele Micciancio. 1997. Oblivious Data Structures: Applications to Cryptography. In ACM SIGACT Symposium on Theory
   of Computing (STOC), El Paso, Texas. 456–464. https://doi.org/10.1145/258533.258638
Carroll Morgan, Annabelle McIver, and Karen Seidel. 1996. Probabilistic Predicate Transformers. ACM Transactions on
   Programming Languages and Systems 18, 3 (1996), 325–353. https://doi.org/10.1145/229542.229547
Moni Naor and Vanessa Teague. 2001. Anti-presistence: history independent data structures. In Proceedings on 33rd
   Annual ACM Symposium on Theory of Computing, July 6-8, 2001, Heraklion, Crete, Greece. ACM, 492–501. https:
   //doi.org/10.1145/380752.380844
Peter W. O’Hearn. 2007. Resources, concurrency, and local reasoning. Theoretical Computer Science 375, 1–3 (2007), 271–307.
   https://doi.org/10.1016/j.tcs.2006.12.035
Peter W. O’Hearn and David J. Pym. 1999. The logic of bunched implications. Bulletin of Symbolic Logic 5, 2 (1999), 215–244.
   http://www.math.ucla.edu/%7Easl/bsl/0502/0502-003.ps
Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local Reasoning about Programs that Alter Data Structures.
   In International Workshop on Computer Science Logic (CSL), Paris, France (Lecture Notes in Computer Science), Vol. 2142.
   Springer-Verlag, 1–19. https://doi.org/10.1007/3-540-44802-0_1
David J. Pym. 1999. On Bunched Predicate Logic. In IEEE Symposium on Logic in Computer Science (LICS), Trento, Italy.
   183–192. https://doi.org/10.1109/LICS.1999.782614
D. J. Pym. 2002. The Semantics and Proof Theory of the Logic of Bunched Implications. Applied Logic Series, Vol. 26. Kluwer
   Academic Publishers. Errata and Remarks maintained at: http://www.cantab.net/users/david.pym/BI-monograph-
   errata.pdf.
David J. Pym, Peter W. O’Hearn, and Hongseok Yang. 2004. Possible worlds and resources: the semantics of BI. Theoretical
   Computer Science 315, 1 (2004), 257–305. https://doi.org/10.1016/j.tcs.2003.11.020
Michael O. Rabin. 2005. How To Exchange Secrets with Oblivious Transfer. IACR Cryptology ePrint Archive 2005 (2005), 187.
John C. Reynolds. 2008. An Introduction to Separation Logic (Preliminary Draft). Technical Report. ITU University, Copenhagen.
   https://www.cs.cmu.edu/~jcr/copenhagen08.pdf
Ronald Rivest. 1999. Unconditionally secure commitment and oblivious transfer schemes using private channels and a
   trusted initializer. (1999).
N. Saheb-Djahromi. 1980. CPO’s of Measures for Nondeterminism. Theoretical Computer Science 12 (1980), 19–37. https:
   //doi.org/10.1016/0304-3975(80)90003-1



                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:30                                                                             Gilles Barthe, Justin Hsu, and Kevin Liao


Elaine Shi, T.-H. Hubert Chan, Emil Stefanov, and Mingfei Li. 2011. Oblivious RAM with O ((log N )3 ) Worst-Case Cost. In
   International Conference on the Theory and Application of Cryptology and Information Security (ASIACRYPT), Seoul, South
   Korea (Lecture Notes in Computer Science), Vol. 7073. Springer, 197–214. https://doi.org/10.1007/978-3-642-25385-0_11
Alex Simpson. 2018. Category-theoretic Structure for Independence and Conditional Independence. Electronic Notes in
   Theoretical Computer Science 336 (2018), 281–297. https://doi.org/10.1016/j.entcs.2018.03.028
Geoffrey Smith. 2003. Probabilistic Noninterference through Weak Probabilistic Bisimulation. In IEEE Computer Security
   Foundations Workshop (CSFW), Pacific Grove, California. 3–13. https://doi.org/10.1109/CSFW.2003.1212701
Sam Staton, Dario Stein, Hongseok Yang, Nathanael L. Ackerman, Cameron E. Freer, and Daniel M. Roy. 2018. The Beta-
   Bernoulli process and algebraic effects. In International Colloquium on Automata, Languages and Programming (ICALP),
   Prague, Czech Republic (Leibniz International Proceedings in Informatics), Vol. 107. Schloss Dagstuhl–Leibniz Center for
   Informatics, 141:1–141:15. https://doi.org/10.4230/LIPIcs.ICALP.2018.141
Emil Stefanov, Marten van Dijk, Elaine Shi, Christopher W. Fletcher, Ling Ren, Xiangyao Yu, and Srinivas Devadas. 2013.
   Path ORAM: an extremely simple oblivious RAM protocol. In ACM SIGSAC Conference on Computer and Communications
   Security (CCS), Berlin, Germany. 299–310. https://doi.org/10.1145/2508859.2516660
Joseph Tassarotti and Robert Harper. 2019. A separation logic for concurrent randomized programs. Proceedings of the ACM
   on Programming Languages 3, POPL (2019), 64:1–64:30. https://doi.org/10.1145/3290377
Matthijs Vákár, Ohad Kammar, and Sam Staton. 2019. A domain theory for statistical probabilistic programming. Proceedings
   of the ACM on Programming Languages 3, POPL (2019), 36:1–36:29. https://dl.acm.org/citation.cfm?id=3290349
Xiao Shaun Wang, Kartik Nayak, Chang Liu, T.-H. Hubert Chan, Elaine Shi, Emil Stefanov, and Yan Huang. 2014. Oblivious
   Data Structures. In ACM SIGSAC Conference on Computer and Communications Security (CCS), Scottsdale, Arizona. 215–226.
   https://doi.org/10.1145/2660267.2660314
Hongseok Yang. 2001. Local Reasoning for Stateful Programs. Ph.D. Dissertation. Champaign, IL, USA. AAI3023240.
Andrew Chi-Chih Yao. 1986. How to generate and exchange secrets. In IEEE Symposium on Foundations of Computer Science
   (FOCS), Toronto, Ontario. 162–167.

A       ALTERNATIVE PROOF RULE FOR CONDITIONALS
When the branches of a conditional may modify the guard, rule RCond does not apply. We consider
an alternative version:
                    ⊢ {ϕ ∗ b ∼ tt} c {ψ } ⊢ {ϕ ∗ b ∼ ff } c ′ {ψ } ψ ∈ CM
          RCondCM
                                      ⊢ {ϕ ∗ D[b]} if R b then c else c ′ {ψ }
In this case we are not able to show that the guard remains independent of the post-condition—since
it may have been modified—but we are still able to show that branch post-conditions are preserved.
In fact, we may relax the side-condition on the branch post-condition.
Definition 10. A formula ϕ is closed under mixtures (CM) if whenever µ, µ ′ have the same domain
and (σ , µ) |= ϕ and (σ , µ ′) |= ϕ, then ϕ is preserved under convex combinations: for every ρ ∈ [0, 1],
we have:
                                            (σ , µ) ⊕ρ (σ , µ ′) |= ϕ
  Intuitively, the final distribution after the conditional is a mixture of two output distributions,
one from each branch. Each component distribution satisfies ψ , but the CM condition is needed to
ensure that the mixture also satisfies ψ . The following syntactic conditions ensure CM.
Lemma 8. The following assertions are CM, where η is SP:
                                               γ ::= pd | γ ∧ γ ′ | η ∗ γ
   Proof. First, we can show |= γ → D[FV (γ )] by induction on γ . The main lemma then follows
by induction on γ . The only interesting case is the last one, when γ = η ∗ γ ′ where η is SP and γ ′ is
CM.
   Suppose that (σ , µ) |= η ∗ γ ′ and (σ , µ ′) |= η ∗ γ ′. By validity there are (σ , ν 1 ) |= η and
(σ , ν 2 ) |= γ ′ separate such that (σ , ν 1 ) ◦ (σ , ν 2 ) ⊑ (σ , µ), and (σ , ν 1′ ) |= η and (σ , ν 2′ ) |= γ ′ separate
such that (σ , ν 1′ ) ◦ (σ , ν 2′ ) ⊑ (σ , µ ′); since η is SP we may assume that ν 1 = ν 1′ , and by restriction we

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                                   55:31


may assume that dom(ν 2 ) = dom(ν 2′ ) = FV (γ ′) since |= γ ′ → D[FV (γ ′)]. So for any ρ ∈ [0, 1], we
have:
           ((σ , ν 1 ) ⊕ρ (σ , ν 1′ )) ◦ ((σ , ν 2 ) ⊕ρ (σ , ν 2′ )) = (σ , ν 1 ) ◦ ((σ , ν 2 ) ⊕ρ (σ , ν 2′ ))
                                                                    = (((σ , ν 1 ) ◦ (σ , ν 2 )) ⊕ρ ((σ , ν 1 ) ◦ (σ , ν 2′ )))
                                                                    = (((σ , ν 1 ) ◦ (σ , ν 2 )) ⊕ρ ((σ , ν 1′ ) ◦ (σ , ν 2′ )))
                                                                    ⊑ (σ , µ) ⊕ρ (σ , µ ′).
We can conclude, since (σ , ν 1 ) ⊕ρ (σ , ν 1′ ) = (σ , ν 1 ) |= η and (σ , ν 2 ) ⊕ρ (σ , ν 2′ ) = (σ , ν 2 ) |= γ ′ by
induction on γ ′.                                                                                                     □
Example 5 (Non-CM assertions). A simple example of an assertion that is not covered by Lemma 8 is
ϕ ≜ D[x] ∗ D[y], where x, y ∈ RV are randomized variables. In fact, ϕ is not CM. To see why, suppose
that x and y are both boolean and consider the distributions µ 1 ≜ δ (x 7→tt,y7→tt) and µ 2 ≜ δ (x 7→ff ,y7→ff ) .
Then ϕ holds in µ 1 and µ 2 —in these distributions x and y are deterministic, hence independent—but ϕ
does not hold in µ 1 ⊕p µ 2 for any p ∈ (0, 1).
  Indeed, allowing ϕ as a post-condition in RCondCM would not be sound. Consider the following
program:
                                   c ≜ if R x then y ← x else y ← x .
Then ϕ would be a sound post-condition for each branch, since x and y are deterministic and hence
independent. But c is semantically equal to y ← x, and ϕ is clearly not a sound post-condition.
    All SP assertions are CM, but some CM assertions are not SP.
Example 6 (Non-SP assertions). The formula ϕ = U[x] ∧ U[y] is CM by Lemma 8, but not SP: the
following programs have ϕ as a post-condition, but have incomparable output distributions.
                                                    c1 ≜ x ←
                                                           $ U ;y ← x
                                                              B
                                                    c2 ≜ x ←
                                                           $ U ; y ← ¬x
                                                              B

B    OMITTED PROOFS
Lemma 1 (Restriction). Let (σ , µ) be any configuration and let ϕ be a BI formula. Then:
                                           (σ , µ) |= ϕ ⇐⇒ (σ , πFV (ϕ) (µ)) |= ϕ.
  Proof. The reverse direction follows by the Kripke monotonicity. The forward direction follows
by induction on ϕ.
    • ϕ ≡ ⊤, ⊥, and atomic propositions p. Trivial.
    • ϕ ≡ ϕ 1 ∧ ϕ 2 . By induction, we have
                                  (σ , πFV (ϕ1 ) (µ)) |= ϕ 1      and      (σ , π FV (ϕ2 ) (µ)) |= ϕ 2 .
       By Kripke monotonicity, we have
                               (σ , πFV (ϕ1,ϕ2 ) (µ)) |= ϕ 1      and (σ , πFV (ϕ1,ϕ2 ) (µ)) |= ϕ 2
       so (σ , π FV (ϕ1 ∧ϕ2 ) (µ)) |= ϕ 1 ∧ ϕ 2 .
     • ϕ ≡ ϕ 1 ∨ ϕ 2 . By induction, we have (σ , π FV (ϕi ) (µ)) |= ϕ i for i = 1 or i = 2. By Kripke
       monotonicity, we have (σ , πFV (ϕ1,ϕ2 ) (µ)) |= ϕ i so (σ , πFV (ϕ1 ∧ϕ2 ) (µ)) |= ϕ 1 ∨ ϕ 2 .
     • ϕ ≡ ϕ 1 → ϕ 2 . Take any (σ ′, µ ′) ⊒ (σ , πFV (ϕ1,ϕ2 ) (µ)) such that (σ ′, µ ′) |= ϕ 1 . There exists a dis-
       tribution µ ′′ such that dom(µ ′′) = dom(µ) ∪ dom(µ ′), and π dom(µ) (µ ′′) = µ and πdom(µ ′ ) (µ ′′) =
       µ ′. In particular, (σ ′, µ ′′) ⊒ (σ , µ). By Kripke monotonicity, we have (σ ′, µ ′′) |= ϕ 1 and by

                                     Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:32                                                                             Gilles Barthe, Justin Hsu, and Kevin Liao


      validity, we have (σ ′, µ ′′) |= ϕ 2 . By induction, (σ ′, πFV (ϕ2 ) (µ ′′)) |= ϕ 2 . Since (σ ′, πFV (ϕ2 ) (µ ′′)) ⊑
      (σ ′, µ ′), Kripke monotonicity gives (σ ′, µ ′) |= ϕ 2 . So, (σ , πFV (ϕ1 →ϕ2 ) (µ)) |= ϕ 1 → ϕ 2 as desired.
    • ϕ ≡ ϕ 1 ∗ ϕ 2 . There exists (σ1 , µ 1 ) and (σ2 , µ 2 ) with (σ1 , µ 1 ) ◦ (σ2 , µ 2 ) ⊑ (σ , µ) and (σ1 , µ 1 ) |= ϕ 1
      and (σ2 , µ 2 ) |= ϕ 2 . By induction, we have (σ1 , π FV (ϕ1 ) (µ 1 )) |= ϕ 1 and (σ2 , πFV (ϕ2 ) (µ 2 )) |= ϕ 2 .
      By Kripke monotonicity, we have (σ1 , πFV (ϕ1 ∗ϕ2 ) (µ 1 )) |= ϕ 1 and (σ2 , πFV (ϕ1 ∗ϕ2 ) (µ 2 )) |= ϕ 2 .
      Now, it is not hard to show that since (σ1 , µ 1 ) ◦ (σ2 , µ 2 ) is defined, (σ1 , πFV (ϕ1 ∗ϕ2 ) (µ 1 )) ◦
      (σ2 , πFV (ϕ1 ∗ϕ2 ) (µ 2 )) ⊑ (σ , πFV (ϕ1 ∗ϕ2 ) (µ)) is defined as well. So, (σ , πFV (ϕ1 ∗ϕ2 ) (µ)) |= ϕ 1 ∗ ϕ 2 as
      desired.
    • ϕ ≡ ϕ 1 −∗ ϕ 2 . Take any (σ ′, µ ′) such that (σ ′, µ ′) ◦ (σ , πFV (ϕ1 −∗ϕ2 ) (µ)) ↓ and (σ ′, µ ′) |= ϕ 1 .
      If (σ ′, µ ′) ◦ (σ , µ) ↓, then (σ ′, µ ′) ◦ (σ , µ) |= ϕ 2 and by induction, (σ ′, πFV (ϕ1 −∗ϕ2 ) (µ ′)) ◦
      (σ , πFV (ϕ1 −∗ϕ2 ) (µ)) |= ϕ 2 . Kripke monotonicity gives (σ ′, µ ′) ◦ (σ , πFV (ϕ1 −∗ϕ2 ) (µ)) |= ϕ 2 .
      Otherwise, suppose that (σ ′, µ ′) ◦ (σ , µ) is not defined. Since (σ ′, µ ′) ◦ (σ , πFV (ϕ1 −∗ϕ2 ) (µ)) ↓,
      it must be the case that ∅ , dom(µ ′) ∩ dom(µ) ⊆ RV \ FV (ϕ 1 −∗ ϕ 2 ). Accordingly,
      (σ ′, πFV (ϕ1 ) (µ ′))◦(σ , µ) ↓. By induction, (σ ′, πFV (ϕ1 ) (µ ′)) |= ϕ 1 and so (σ ′, πFV (ϕ1 ) (µ ′))◦(σ , µ) |=
      ϕ 2 . By induction again, (σ ′, πFV (ϕ1 )∩FV (ϕ2 ) (µ ′)) ◦ (σ , πFV (ϕ2 ) (µ)) |= ϕ 2 . By Kripke monotonicity
      and the fact that the extension is defined, we have (σ ′, µ ′) ◦ (σ , π FV (ϕ1 −∗ϕ2 ) (µ)) |= ϕ 2 . So,
      (σ , πFV (ϕ1 −∗ϕ2 ) (µ)) |= ϕ 1 −∗ ϕ 2 as desired.
                                                                                                                            □
Lemma 2 (Extrusion). If |= ϕ → D[FV (η) ∩ RV], then |= (ϕ ∗ ψ ) ∧ η → (ϕ ∧ η) ∗ ψ .
   Proof. Let (σ , µ) |= (ϕ ∗ ψ )∧η. By validity of the first conjunct, there exists separate (σ1 , µ 1 ) |= ϕ
and (σ2 , µ 2 ) |= ψ . Since |= ϕ → D[FV (η)], we have FV (η) ⊆ dom(µ 1 ). By restriction (Lemma 1)
and the fact that η is valid in (σ , µ), we have (σ1 , µ 1 ) |= η. Thus (σ , µ) |= (ϕ ∧ η) ∗ ψ and so
|= (ϕ ∗ ψ ) ∧ η → (ϕ ∧ η) ∗ ψ , as desired.                                                                  □
Lemma 3. The following axiom schema are valid:
           |= er ∼ er′ → er′ ∼ er                                                                                       (S1)
           |= er ∼ er′ ∧ er′ ∼ er′′ → er ∼ er′′                                                                         (S2)
           |= er ∼ er′ → er ∼ er′′ whenever |=E er′ = er′′ and FV (er′′) ∩ RV ⊆ FV (er′ ) ∩ RV                          (S3)
           |= er ∼ er → er′ ∼ er′ whenever FV (er′ ) ∩ RV ⊆ FV (er ) ∩ RV                                               (S4)
   Proof. Almost immediate from the definitions; we show (S3). Suppose that (σ , µ) is a config-
uration, and let (σ ′, µ ′) ⊒ (σ , µ) be any larger configuration. If (σ ′, µ ′) |= er ∼ er′ , then then free
variables of er and er′ are contained in dom(µ ′), and so are the free variables of er′′. Now for all
m ∈ supp(µ ′), we have Jer K(σ ′, m) = Jer′ K(σ ′, m) = Jer′′K(σ ′, m), where the last equality follows
from |=E er′ = er′′. Hence (σ ′, µ ′) |= er ∼ er′′, as desired.                                             □
Lemma 4. The following axiom schema are valid:
    |= er ∼ er′ ∧ US [er ] → US [er′ ]                                                                                  (U1)
    |= US [er ] → er ∼ er                                                                                               (U2)
    |= US [er ] → US [f (er )] for any bijection Jf K : S → S and FV (f ) ∩ RV ⊆ FV (er ) ∩ RV                          (U3)
   Proof. Almost immediate from definitions; axiom (U3) follows from the fact that the uniform
distribution is preserved under bijections of its domain.                                    □
Theorem 2 (Soundness). If ⊢ {ϕ} c {ψ } is derivable, then it is valid: |= {ϕ} c {ψ }.
   Proof. By induction on the derivation. Let (σ , µ) satisfy the pre-condition of the conclusion.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:33


DAssn. By induction on ψ .
Skip. Trivial.
Seqn. By induction hypothesis.
DCond. By induction hypothesis and case analysis.
DLoop. Since the guard is deterministic and the loop is assumed to terminate on all inputs, the
     number of iterations is a function of the deterministic input store and we have:

                            Jwhile b do cK(σ , µ) = Jc N (σ ) K(σ , µ) = JcKN (σ ) (σ , µ)

    where c k ≜ c ; · · · ;c is the k-fold sequential composition of c. Soundness follows by repeatedly
    applying the induction hypothesis from c.
RAssn. Trivial.
RSamp. Trivial.
RDCond. Since (σ , µ) |= ϕ, either (σ , µ) |= b ∼ tt or (σ , µ) |= b ∼ ff . Note that exactly one
    case holds, since |= b ∼ tt → ¬(b ∼ ff ) and vice versa. If (σ , µ) |= b ∼ tt holds, then
    (σ , µ) |= ϕ ∧ b ∼ tt and since Jif R b then c else c ′K(σ , µ) = JcK(σ , µ), we can conclude by
    induction. The case (σ , µ) |= b ∼ ff is similar.
RCondCM. There exist µ 1 , µ 2 such that µ 1 ◦ µ 2 ⊑ µ, and (σ , µ 1 ) |= ϕ and (σ , µ 2 ) |= D[b]. Let ρ be
    the probability Jb = ttK(σ , µ 2 ). We may assume that ρ ∈ (0, 1); if ρ is equal to zero or one
    then we can conclude by induction.
    By the semantics of commands, we have

                     Jif R b then c else c ′K(σ , µ) = ρ · JcK(σ , µ t ) + (1 − ρ) · Jc ′K(σ , µ f )

       where µ t is the distribution µ conditioned on b = tt, and µ f is the distribution µ conditioned
       on b = ff . Note that the final deterministic states must be equal to the initial deterministic
       state σ in both branches, due to the syntactic restriction.
       Furthermore since µ 1 and µ 2 are independent, we can decompose µ 1 ◦ µ 2,t ⊑ µ t and µ 1 ◦ µ 2, f ⊑
       µ f such that (σ , µ 2,t ) |= b ∼ tt and (σ , µ 2, f ) |= b ∼ ff . Since (σ , µ 1 ) |= ϕ, we know that
       (σ , µ t ) |= ϕ ∗ b ∼ tt and (σ , µ f ) |= ϕ ∗ b ∼ ff so the induction hypothesis gives:

                                        JcK(σ , µ t ) |= ψ and Jc ′K(σ , µ f ) |= ψ .

       Since ψ is CM, we can conclude

                   Jif R b then c else c ′K(σ , µ) = ρ · JcK(σ , µ) + (1 − ρ) · Jc ′K(σ , µ) |= ψ

    so the post-condition holds.
RCond. The proof goes much like the proof of RCondCM; let µ t , µ f , ρ be as before. Recall that by
    the induction hypothesis, we have:

                            JcK(σ , µ t ) |= ψ ∗ b ∼ tt and Jc ′K(σ , µ f ) |= ψ ∗ b ∼ ff .

       Since the top-level command is a randomized conditional, the final deterministic state must
       be the same for both branches; call it σ ′. We can decompose the output states into

                      (σ ′, ν ) ◦ (σ ′, νt ) ⊑ JcK(σ , µ t ) and (σ ′, ν ) ◦ (σ ′, ν f ) ⊑ JcK(σ , µ f )

       such that
                           (σ ′, ν ) |= ψ and (σ ′, νt ) |= b ∼ tt and (σ ′, ν f ) |= b ∼ ff

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:34                                                                              Gilles Barthe, Justin Hsu, and Kevin Liao


        noting that ν can be taken to be the same in both branches since ψ ∈ SP; by Lemma 1, we
        may also assume that dom(νt ) = dom(ν f ). Thus, we have:
         ρ · (σ ′, ν ) ◦ (σ ′, νt ) + (1 − ρ) · (σ ′, ν ) ◦ (σ ′, ν f ) = (σ ′, ρ · (ν ⊗ νt ) + (1 − ρ) · (ν ⊗ ν f ))
                                                                    = (σ ′, ν ⊗ (νt ⊕ρ ν f ))
                                                                    = (σ ′, ν ) ◦ (σ ′, (νt ⊕ρ ν f ))
                                                                    ⊑ Jif R b then c else c ′K(σ , µ),
     and we can conclude since (σ ′, ν ) |= ψ and (σ ′, (νt ⊕ρ ν f )) |= D[b].
Weak. By induction hypothesis and semantics of implication.
True. Trivial.
Conj. By induction hypothesis and semantics of conjunction.
Case. By case analysis.
RCase. Essentially the same as RCond.
Const. The fact that JcK(σ , µ) |= ψ follows by induction. To show JcK(σ , µ) |= η, by the restriction
     property we have (σ , π FV (η) (µ)) |= η initially, and since the free variables of η are disjoint
     from the modified variables of c, we have (JcKσ , πFV (η) (JcKµ)) |= η as well. Thus, there is
     restriction of the output where η holds, thus JcK(σ , µ) |= η as desired.
Frame. There exist µ 1 , µ 2 such that µ 1 ◦ µ 2 ⊑ µ, and (σ , µ 1 ) |= ϕ and (σ , µ 2 ) |= η; let S 1 ≜ dom(µ 1 ),
     and note that T ∪ RV (c) ⊆ S 1 by the last side-condition.
     By the restriction property we have (σ , πFV (η) (µ 2 )) |= η; let S 2 ≜ dom(µ 2 ) ∩ FV (η) and note
     that S 1 and S 2 are disjoint. Let S 3 be the set of all variables not contained in S 1 or S 2 . Since
     WV (c) is disjoint from S 2 by the first side-condition, we must have WV (c) ⊆ S 1 ∪ S 3 .
     By induction, we have JcK(σ , µ) |= ψ . The restriction property gives (JcKσ , π FV (ψ ) (JcKµ)) |= ψ .
     By the third side-condition, RV (c) ⊆ S 1 . By soundness of RV and WV , all variables in
     WV (c) must be written to before they are read and there is a function F : RanM[S 1 ] →
     D(RanM[WV (c) ∪ S 1 ]) such that:
                         (JcKσ , πWV (c)∪S1 (JcKµ)) = (JcKσ , bind(µ, m 7→ F (πS1 (m)))).
        Since S 2 ⊆ FV (η), variables in S 2 are not in MV (c) by the first side-condition, and S 2 is disjoint
        from WV (c) ∪ S 1 . By soundness of MV , we have:
    (JcKσ , π(WV (c)∪S1 )∪S2 (JcKµ)) = (JcKσ , bind(π(WV (c)∪S1 )∪S2 (µ), (m 1 , m 2 ) 7→ F (m 1 ) ⊗ unit(m 2 ))).
        Since S 1 and S 2 are independent in µ, we know that S 1 ∪ WV (c) and S 2 are independent in
        JcK(σ , µ) as well. Hence:
                          (JcKσ , JcKµ) ⊒ (JcKσ , πS1 ∪WV (c) (JcKµ)) ◦ (JcKσ , πS2 (JcKµ)).
        We know that FV (ψ ) ⊆ T ∪ WV (c) ⊆ S 1 ∪ WV (c) so since ψ is valid in JcK(σ , µ), it is
        valid in the first conjunct by the restriction property and the second side-condition. Since
        πS2 (JcKµ) = πS2 (µ), and η does not depend on modified deterministic variables, η is valid in
        the second conjunct. Thus, we can conclude:
                                                   JcK(σ , µ) |= ψ ∗ η.                                                        □
   The proof of the last case relies on the following useful fact connecting independence and
distribution bind.
Lemma 9. Let A1 , A2 be disjoint and let B 1 , B 2 be disjoint, and consider functions Fi : Ai →
D(RanM[Bi ]) for i = 1, 2. For any two distributions µ i ∈ D(RanM[Ai ]), we have:
  bind(µ 1 ⊗ µ 2 , (m 1 , m 2 ) 7→ F 1 (m 1 ) ⊗ F 2 (m 2 )) = bind(µ 1 , m 1 7→ F 1 (m 1 )) ⊗ bind(µ 2 , m 2 7→ F 2 (m 2 )).

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                          55:35


    Proof. By direct calculation.                                                                                            □
Lemma 7. Let q ≥ 2 be any integer, and let {x i } be any finite set of distinct variables. The following
axiom schema are sound.
    |= US1 [x 1 ] ∗ · · · ∗ USn [x n ] ↔ US1 ×···×Sn [(x 1 , . . . , x n )]
    |= UZq [x 1 ] ∗ D[x 2 ] ∗ · · · ∗ D[x n ] ∧ x 0 ∼ x 1 + · · · + x n mod q → UZq [x 0 ] ∗ D[x 2 ] ∗ · · · ∗ D[x n ]
In particular, we will use two derived axioms (writing ⊕ for xor, addition modulo 2):
    |= UZ2 [x 1 ] ∗ D[x 2 ] ∧ x 0 ∼ x 1 ⊕ x 2 → UZ2 [x 0 ] ∗ D[x 2 ]                                                      (U4)
    |= UZq [x 1 ] ∗ D[x 2 ] ∗ D[x 3 ] ∧ x 0 ∼ x 1 + x 2 + x 3 mod q → UZq [x 0 ] ∗ D[x 2 ] ∗ D[x 3 ]                      (U5)
These axioms also hold for expressions with at most one free variables.
   Proof. We prove the slightly more general version with a finite set of expressions {ei } each
with a single random variable x i , and {x i } are distinct. Let (σ , µ) be any configuration.
   For the first axiom, by validity of the left-hand side the configuration can be decomposed into
a sequence of independent products: (σ , µ 1 ) ◦ · · · ◦ (σ , µ n ) ⊑ (σ , µ) such that x i ∈ dom(µ i ) and
(σ , µ i ) |= USi [ei ]. By the restriction property, we may assume that dom(µ i ) = FV (e) = {x i }. Now
the tuple (e 1 , . . . , en ) is uniform in (σ , µ 1 ) ◦ · · · ◦ (σ , µ n ), and so US1 ×···×Sn [(e 1 , . . . , en )] holds in a
restriction of (σ , µ). The other direction is similar.
   For the second axiom, suppose that
                    (σ , µ) |= UZq [e 1 ] ∗ D[e 2 ] ∗ · · · ∗ D[en ] ∧ e 0 ∼ e 1 + · · · + en     mod q.
By validity and restriction, we can again decompose (σ , µ 1 ) ◦ · · · ◦ (σ , µ n ) ⊑ (σ , µ) such that
(σ , µ 1 ) |= UZq [e 1 ] and (σ , µ i ) |= D[ei ] for i > 1, and dom(µ i ) = FV (ei ) = {x i }. Now, e 1 + · · · + en
mod q is distributed uniformly in µ, since for any realization of e 2 , . . . , en and any z ∈ Zq , there
is exactly one value of e 1 that will make e 1 + · · · + en = z mod q and e 1 is uniformly distributed,
so each z has equal probability. For the same reason, e 1 + · · · + en is independent of the joint
distribution of (e 2 , . . . , en ) in µ. Thus, we have:
                                           (σ , µ) |= UZq [e 0 ] ∗ D[(e 2 , . . . , en )].
Since (σ , µ) |= D[e 2 ] ∗ · · · ∗ D[en ], extrusion gives
                                        (σ , µ) |= UZq [e 0 ] ∗ D[e 2 ] ∗ · · · ∗ D[en ]
as desired.                                                                                                                  □

C     EXAMPLES: ADDITIONAL DETAILS
C.1     Private Information Retrieval
C.1.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition
                                       Ψ ≜ U[q 0 ] ∧ U[q 1 ] .
                                           |{z} |{z}
                                                          S0 ’s view S1 ’s view
This says that the views of S0 and S1 (q 0 and q 1 , respectively) are uniformly random bitstrings.
  By RSamp, adjoining the sampling for q 0 (line 1) gives
                                                              U[q 0 ].
Since I is a deterministic variable, we can adjoin D[I ], giving
                                                         U[q 0 ] ∗ D[I ].

                                    Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:36                                                                          Gilles Barthe, Justin Hsu, and Kevin Liao


By RAssn*, assigning to q 1 (line 2) gives
                                           U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I .
Next, we can pull out U[q 0 ] like so
                                    U[q 0 ] ∧ (U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I ).
and apply the xor axiom (U4) to the right conjunct, which gives the desired post-condition
                                               Ψ ≜ U[q 0 ] ∧ U[q 1 ].
Since q 0 and q 1 are unmodified in the remainder of the program, we can preserve Ψ through to the
end using Const and True.
C.1.2 Proof of Input Independence. Starting from the pre-condition Φ1 ≜ D[I ], we would like to
prove the post-condition
                             Ψ ≜ D[I ] ∗ U[q 0 ] ∧ D[I ] ∗ U[q 1 ] .
                                 |{z} |{z} |{z} |{z}
                                            Index   S0 ’s view   Index   S1 ’s view
This says that the views of S0 and S1 (q 0 and q 1 , respectively) are independent of secret index I .
  By RSamp*, adjoining the sampling for q 0 (line 1) gives
                                                    U[q 0 ] ∗ D[I ].
By RAssn*, assigning to q 1 (line 2) gives
                                           U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I .
Next, we can pull out D[I ] ∗ U[q 0 ] like so
                                 D[I ] ∗ U[q 0 ] ∧ (U[q 0 ] ∗ D[I ] ∧ q 1 ∼ q 0 ⊕ I )
and apply the xor axiom (U4) to the right conjunct, giving
                                          D[I ] ∗ U[q 0 ] ∧ D[I ] ∗ U[q 1 ],
which implies the desired post-condition
                                       Ψ ≜ D[I ] ∗ U[q 0 ] ∧ D[I ] ∗ U[q 1 ].
Since q 0 and q 1 are unmodified in the remainder of the program, we can preserve Ψ through to the
end using Const and True.

C.2     Oblivious Transfer
C.2.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition
                          Ψ ≜ (Uk×k [(r 0 , r 1 )] ∗ U[e]) ∧ (U[d] ∗ Uk ×k [(rd , f 1−c )]) .
                              |          {z             } |             {z               }
                                         S’s view                        R’s “view”

Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove the post-condition
                          Ψ ≜ (Uk×k [(r 0 , r 1 )] ∗ U[e]) ∧ (U[d] ∗ Uk ×k [(rd , f 1−c )]) .
                              |          {z             } |             {z               }
                                  S’s view                  R’s “view”
To establish R s secrecy, we need to consider the view of S, which consists of r 0 , r 1 , and e. For R’s
              ′

choice c to be kept secret, it is required that Uk ×k [(r 0 , r 1 )] ∗ U[e], i.e., S’s combined view is uniform.
Note that it is not enough to establish that the individual components of S’s view are uniform. To
see why, suppose T also sends S the random bit d, which reveals c = e ⊕ d. Although the individual

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:37


components of S’s view would indeed be uniform, i.e., Uk [r 0 ] ∧ Uk [r 1 ] ∧ U[e] ∧ U[d], R’s secrecy
is clearly violated. Thus, the stronger post-condition is needed to establish that S’s combined view
is uniform.
    To establish S ′s (one-sided) secrecy, we need to consider the view of R, which consists of d,
rd , and one of f 0 or f 1 . In particular, the fi to be considered corresponds to the encryption of the
“wrong” message, which we assign to the ghost variable f 1−c (which is, in turn, computed using the
ghost variable r 1−d ). Similar to R’s secrecy, it is then required that U[d] ∗ Uk ×k [(rd , f 1−c )], i.e., R’s
combined view is uniform.
    We first show R’s secrecy, followed by S’s secrecy, and then combine the results using Conj. By
RSamp and RSamp*, we can adjoin the random samplings for r 0 , r 1 , d (lines 1–2), giving
                                               Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].
Since the free variables of this formula are unmodified in the conditional (line 3), we can preserve
the formula using Const and True. Since c is a deterministic variable we can adjoin D[c], giving
                                           D[c] ∗ Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].
For the assignment to e (line 4), we start from the local pre-condition
                                                       D[c] ∗ U[d].
By RAssn*, assigning to e gives
                                             (D[c] ∗ U[d]) ∧ e ∼ c ⊕ d.
Applying the xor axiom (U4) leaves
                                                          U[e].
Then, we can frame as follows:
         ⊢ {ϕ} c ′ {ψ }      FV (η) ∩ MV (c ′) = ∅          FV (ψ ) ⊆ FV (ϕ) ∪ WV (c ′)          |= ϕ → D[RV (c ′)]
Frame
                   ⊢ {D[c] ∗ U[d] ∗ Uk [r 0 ] ∗ Uk [r 1 ]} e ← c ⊕ d { U[e] ∗ Uk [r 0 ] ∗ Uk [r 1 ]}
                      | {z } |               {z       } | {z } |{z} |                  {z       }
                             ϕ                     η                  c′          ψ              η                      .
The post-condition implies
                                             Uk ×k [(r 0 , r 1 )] ∗ U[e],
which establishes R’s secrecy. Since r 0 , r 1 , and e are unmodified in the remainder of the program,
we can preserve Uk ×k [(r 0 , r 1 )] ∗ U[e] through to the end using Const.
   Next, we show S’s secrecy. Again, by RSamp and RSamp*, we can adjoin the random samplings
for r 0 , r 1 , d (lines 1–2), giving
                                            Uk [r 0 ] ∗ Uk [r 1 ] ∗ U[d].
We go through the conditional (line 3) with RCond, which gives pre-condition
                                            Uk [r 0 ] ∗ Uk [r 1 ] ∗ d = 0 ∼ tt.
To go through the first assignment, we start from the local pre-condition
                                                         Uk [r 0 ].
By RAssn*, assigning to rd gives
                                                   Uk [r 0 ] ∧ rd ∼ r 0 .
Transferring the distribution law gives
                                                Uk [rd ].
We can then frame in Uk [r 1 ] ∗ d = 0 ∼ tt giving
                                            Uk [rd ] ∗ Uk [r 1 ] ∗ d = 0 ∼ tt.

                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:38                                                                                 Gilles Barthe, Justin Hsu, and Kevin Liao


Going through the second assignment follows similarly, this time starting from the local pre-
condition
                                             Uk [r 1 ]
and giving the following post-condition in the true branch
                                               Uk [rd ] ∗ Uk [r 1−d ] ∗ d = 0 ∼ tt.
The false branch yields the same post-condition, which, by RCond, brings us to the post-condition
                                                  Uk [rd ] ∗ Uk [r 1−d ] ∗ U[d].
Since the free variables of this formula are unmodified in lines 4–5, we can preserve this formula
through using Const and True. Next, we go through the deterministic conditional (line 6) using
DCond. In the true branch, we start with pre-condition
                                       Uk [rd ] ∗ Uk [r 1−d ] ∗ U[d] ∧ (c = 0) = tt.
Dropping the right conjunct, we can adjoin D[m 1 ] like so
                                           Uk [rd ] ∗ D[m 1 ] ∗ Uk [r 1−d ] ∗ U[d],
since m 1 is a deterministic variable. We preserve this formula through the first assignment to mc
using Const and True, and then go through the second assignment to f 1−c starting from the local
pre-condition
                                         D[m 1 ] ∗ Uk [r 1−d ].
Applying RAssn* and the xor axiom (U4) gives
                                                           Uk [f 1−c ].
Framing in Uk [rd ] ∗ U[d] gives the following post-condition in the true branch
                                                  Uk [rd ] ∗ Uk [f 1−c ] ∗ U[d].
The false branch yields the same post-condition. Then, we can merge Uk [rd ] ∗ Uk [f 1−c ] and
rearrange like so
                                    U[d] ∗ Uk ×k [(rd , f 1−c )].
This establishes S’s secrecy. Combining the formulas for R’s secrecy and S’s secrecy using Conj
gives the desired post-condition.

C.3       Multi-Party Computation
C.3.1 Proof of Uniformity. Starting from the trivial pre-condition Φ1 ≜ ⊤, we would like to prove
the post-condition
            Û                               Û                              Û
     Ψ≜             U[(r [α].2, r [α].3)] ∧        U[(r [α].1, r [α].3)] ∧        U[(r [α].1, r [α].2)] .
          α ∈ {2,3}
                    |       {z         } α ∈ {1,3} |       {z         } α ∈ {1,2} |       {z         }
                         P1 ’s view from P α                   P2 ’s view from P α                 P 3 ’s view from P α
This says that each party’s view from the other parties is uniform and independent.
  To prove this post-condition, we take the following for-loop invariant:
                      ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                    α ∈[1,i)

By RSamp*, adjoining the random samplings for r [i].1 and r [i].2 (lines 2 and 3) gives
        U[r [i].1] ∗ U[r [i].2] ∗     ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                                    α ∈[1,i)

To go through the assignment to r [i].3 (line 4), we start from the local pre-condition
                                                     U[r [i].1] ∗ U[r [i].2].

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                               55:39


By RAssn*, assigning to r [i].3 gives
                          U[r [i].1] ∗ U[r [i].2] ∧ r [i].3 ∼ x[i] − r [i].1 − r [i].2                 mod p.
Applying the modular addition axiom (U5) gives
                    U[r [i].1] ∗ U[r [i].2] ∧ U[r [i].2] ∗ U[r [i].3] ∧ U[r [i].1] ∗ U[r [i].3].
Then, we can merge pairwise independent distributions like so
                             U[(r [i].1, r [i].2)] ∧ U[(r [i].2, r [i].3)] ∧ U[(r [i].1, r [i].3)].
Then, we can frame as follows
         ⊢ {ϕ} c {ψ }               FV (η) ∩ MV (c) = ∅     FV (ψ ) ⊆ FV (ϕ) ∪ WV (c)                            |= ϕ → D[RV (c)]
 Frame                                             n                           o
                                                 ⊢ U[r [i].1] ∗ U[r [i].2] ∗ η
                                                     |       {z         }
                                                                     ϕ

                             n              c ≜ r [i].3 ← x[i] − r [i].1 − r [i].2              mod p                o
                                 U[(r [i].1, r [i].2)] ∧ U[(r [i].2, r [i].3)] ∧ U[(r [i].1, r [i].3)] ∗ η
                                 |                               {z                                 }
                                                                    ψ                                                               ,
where
                η≜         ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                         α ∈[1,i)
We can reassociate the post-condition like so
                     ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                  α ∈[1,i+1)

The for-loop post-condition from DFor implies
                     ∗ U[(r [α].1, r [α].2)] ∧ U[(r [α].2, r [α].3)] ∧ U[(r [α].1, r [α].3)].
                   α ∈[1,3]

After rearranging and dropping terms, this implies the desired post-condition
            Û                            Û                           Û
      Ψ≜         U[(r [α].2, r [α].3)] ∧     U[(r [α].1, r [α].3)] ∧    U[(r [α].1, r [α].2)].
             α ∈ {2,3}                               α ∈ {1,3}                                  α ∈ {1,2}

Since the free variables of Ψ are unmodified in the remainder of the program, we can preserve Ψ
through to the end using Const and True.
C.3.2    Proof of Input Independence. Starting from the pre-condition
                                                Û
                                        Φ1 ≜        D[x[α]],
                                                              α ∈[1,3]

we would like to prove the post-condition
               Û                                         Û
       Ψ≜              D[x[α]] ∗ D[(r [α].2, r [α].3)] ∧        D[x[α]] ∗ D[(r [α].1, r [α].3)] ∧
             α ∈ {2,3}
                       | {z } |          {z         } α ∈ {1,3} | {z } |         {z          }
                             P α ’s input     P1 ’s view from P α                    P α ’s input    P2 ’s view from P α
                                                                           Û
                                                                                     D[x[α]] ∗ D[(r [α].1, r [α].2)] .
                                                                         α ∈ {1,2}
                                                                                     | {z } |          {z         }
                                                                                     P α ’s input     P3 ’s view from P α

This says that, for each party, the secret input of each other party is independent from the view
they generate. Throughout, let
Φ2 ≜ D[x[α]] ∗ U[(r [α].1, r [α].2)] ∧ D[x[α]] ∗ U[(r [α].2, r [α].3)] ∧ D[x[α]] ∗ U[(r [α].1, r [α].3)].

                                      Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
55:40                                                                                Gilles Barthe, Justin Hsu, and Kevin Liao


First, we take the following for-loop invariant
                                      Û              Û
                                           D[x[α]] ∧   Φ2 .
                                           α ∈[1,3]               α ∈[1,i)

To go through the assignments in lines 2–4, we start from the local pre-condition
                                                        D[x[i]].
By RSamp*, adjoining the random samplings for r [i].1 and r [i].2 gives
                                         D[x[i]] ∗ U[r [i].1] ∗ U[r [i].2].
By rule RAssn*, assigning to r [i].3 gives
                (D[x[i]] ∗ U[r [i].1] ∗ U[r [i].2]) ∧ r [i].3 ∼ x[i] − r [i].1 − r [i].2            mod p.
Applying the modular arithmetic axiom (U5) gives
 D[x[i]] ∗ U[r [i].1] ∗ U[r [i].2] ∧ D[x[i]] ∗ U[r [i].2] ∗ U[r [i].3] ∧ D[x[i]] ∗ U[r [i].1] ∗ U[r [i].3].
We can then merge the pairwise independent distributions of secret shares like so
    Φ3 ≜ D[x[i]] ∗ U[(r [i].1, r [i].2)] ∧ D[x[i]] ∗ U[(r [i].2, r [i].3)] ∧ D[x[i]] ∗ U[(r [i].1, r [i].3)].
Then, we can carry in unused conjuncts as follows
                                    ⊢ {ϕ} c {ψ }    FV (η) ∩ MV (c) = ∅
        Const                      n             Û                 Û         o
                                  ⊢ D[x[i]] ∧          D[x[i]] ∧          Φ2
                                     | {z } α ∈[1,3]\i           α ∈[1,i)
                                        ϕ      |          {z               }
                                                                     η
                c ≜ r [i].1 ←
                            $ Z ; r [i].2 $ Z ; r [i].3 ← x[i] − r [i].1 − r [i].2
                               pn        ← Û p                Û         o                          mod p
                                      Φ3 ∧           D[x[i]] ∧          Φ2
                                     |{z} α ∈[1,3]\i           α ∈[1,i)
                                       ψ   |            {z               }
                                                                 η                                           .
Reassociating the post-condition gives
                                    Û                                Û
                                                     D[x[i]] ∧                Φ2 .
                                          α ∈[1,3]               α ∈[1,i+1)

Thus, the for-loop invariant is preserved. By DFor, the post-condition of the conclusion is
                                      Û               Û
                                           D[x[i]] ∧      Φ2 ,
                                            α ∈[1,3]              α ∈[1,4)

which implies the desired post-condition Ψ
            Û                                      Û
                 D[x[α]] ∗ D[(r [α].2, r [α].3)] ∧   D[x[α]] ∗ D[(r [α].1, r [α].3)] ∧
             α ∈ {2,3}                                      α ∈ {1,3}
                                                                 Û
                                                                         D[x[α]] ∗ D[(r [α].1, r [α].2)].
                                                            α ∈ {1,2}

Because the free variables of Ψ are unmodified in the rest of the program, we can frame Ψ through
to the end using Const and True.

Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
A Probabilistic Separation Logic                                                                                    55:41


C.4    Simple Oblivious RAM
Starting from the pre-condition
                                                   Φ1 ≜       ∗ U[p[α]],
                                                              α ∈X
which says that the position map is initialized uniformly and independently, we would like to prove
the post-condition
                                  Ψ≜                ∗
                                                U[(ℓ[β].1, ℓ[β].2)],
                                                  β ∈[1,k ]
which says that the product distribution for each instruction-flush leakage pair is uniform and
independent.
  Starting from the local pre-condition
                                            U[p[x]],
the assignment to ℓ[j].1 (using RAssn*) gives
                                               U[p[x]] ∧ ℓ[1].1 ∼ p[x].
Transferring the distribution law gives
                                                         U[ℓ[1].1].
Then, we can frame as follows
       ⊢ {ϕ} c {ψ }      FV (η) ∩ MV (c) = ∅    FV (ψ ) ⊆ FV (ϕ) ∪ WV (c)  |= ϕ → D[RV (c)]
 Frame
                                        ∗                                                   ∗
                  n                         o              n                       o
                ⊢ U[p[x]] ∗         U[p[α]] ℓ[1].1 ← p[x] U[ℓ[i].1] ∗      U[p[α]]
                    | {z } α ∈X\x             |   {z      } | {z } α ∈X\x
                       ϕ
                              |    {z     }         c           ψ      |  {z    }
                                              η                                                   η

We can preserve this post-condition through lines 4–8 up until the random sampling for p[x] using
Const and True. By RSamp*, the random sampling for p[x] gives
                                               U[ℓ[1].1] ∗       ∗ U[p[α]].
                                                                α ∈X
Again, we can frame this formula through the last assignment in the read instruction using Const
and True. For the flush instruction, we first adjoin the random sampling for l
                                           U[ℓ[1].1] ∗ U[l] ∗          ∗ U[p[α]].
                                                                     α ∈X
Assigning to ℓ[1].2 gives
                                        U[ℓ[1].1] ∗ U[ℓ[1].2] ∗          ∗ U[p[α]].
                                                                        α ∈X
Then, we can merge U[ℓ[1].1] ∗ U[ℓ[1].2] like so
                                          U[(ℓ[1].1, ℓ[1].2)] ∗        ∗ U[p[α]].
                                                                       α ∈X
Then, we preserve through rest of the flush instruction using Const and True. We proceed through
the remaining k − 1 compiled instructions similarly, giving the desired post-condition
                                           Ψ≜       ∗ U[(ℓ[β].1, ℓ[β].2)].
                                                  β ∈[1,k ]




                                   Proc. ACM Program. Lang., Vol. 4, No. POPL, Article 55. Publication date: January 2020.
