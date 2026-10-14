                                         ALPS: Measuring Valid Creativity in Large Language Models with Mathematical
                                                                         Construction
                                                                                        Eric Xie, Wenqian Ye, Aidong Zhang
                                                                                                    University of Virginia
                                                                                            {jrg4wx, pvc7hs, aidong}@virginia.edu



                                                                      Abstract                                                             Verifiable         Renewable         Constructive
                                                                                                                                           no subjectivity   no contamination   no set procedure
                                           Large language models produce outputs presented as discov-
                                           eries — new proofs, conjectures, or molecules. Whether such           Static problem sets             ✓                                    ✓
                                           an output that appears creative is truly original and effective is      MATH, code, miniF2F
                                           hard to establish: open-ended outputs require subjective judg-        Synthetic puzzles               ✓                 ✓
                                           ment, the output may replicate something seen in training,              random SAT, ETP
                                                                                                                                                                   ✓                  ✓
arXiv:2608.15979v1 [cs.AI] 17 Aug 2026




                                           or the task may be too simple to need creativity. We present          Open discovery
                                           ALPS (Austin-Law Proof-Synthesis), a benchmark that de-                 hypotheses, molecules
                                           signs a task to measure valid creativity: producing a solution
                                           that is original and can be proven correct. Each instance is a        ALPS (ours)                     ✓                 ✓                  ✓
                                           single equational law, certified to require either the construc-
                                           tion of an infinite mathematical structure satisfying the law, or     Table 1: Each property removes one confound in measur-
                                           a proof that no such structure exists. Submissions are verified       ing valid creativity: verification removes subjective judging,
                                           by automated proof checking with no human involvement, and            renewal removes contamination, and construction removes
                                           a public generator produces new instances without limit, so           solution by any instance-independent method. Each prior
                                           LLMs are never evaluated on problems they may have seen. A            benchmark family (Hendrycks et al. 2021; Chen et al. 2021;
                                           portfolio of eight configurations of leading automated provers        Zheng, Han, and Polu 2021; Selman, Mitchell, and Levesque
                                           resolves 2.2% of the 4,141-law evaluation pool, and a twenty-
                                           fold budget increase adds 0.6%: the obstacle is not compute,
                                                                                                                 1996; Bolan et al. 2025; Gottweis et al. 2026; Jumper et al.
                                           but the absence of any method that produces the tailored struc-       2021) fulfills two of the three, but measuring valid creativity
                                           ture each law requires. Under a fixed protocol, the strongest         requires all three.
                                           reasoning model we test succeeds in 14% of instances on the
                                           proof side, but none on the construction side. The remain-
                                           ing 97.2% of the pool is unresolved at every configuration
                                           and budget we test. We release ALPS in full: the corpus, the          for the task it addresses (Runco and Jaeger 2012). A solu-
                                           generator, and the automated judge.                                   tion that appears creative is not automatically a valid one:
                                                                                                                 apparent novelty may be a repetition of something seen in
                                         Code — https://github.com/EricX22/ALPS                                  training, and apparent effectiveness is unestablished until it is
                                                                                                                 demonstrated. Two conditions must therefore hold: creativity
                                                                                                                 was necessary to solve the problem, and the answer can be
                                                               1    Introduction                                 soundly justified. We call this combination valid creativity.
                                         As large language models (LLMs) begin to take on scientific                Current evaluation methods fail to reliably measure the va-
                                         work in the real world — formalizing and proving theorems               lidity of a creative output. For an evaluation to be effective,
                                         (Yang et al. 2023; Xin et al. 2024), proposing conjectures              the solution must be verifiable, with an answer that can be
                                         (Romera-Paredes et al. 2024; Gottweis et al. 2026; Lu et al.            checked objectively rather than judged. The problem supply
                                         2024), and designing molecules and materials (Jumper et al.             must be renewable; new instances can be generated auto-
                                         2021; Merchant et al. 2023) — AI-for-science has grown                  matically and without limit, so evaluation can always use
                                         increasingly interested in measuring an LLM’s ability to                problems created after any training cutoff. And the task must
                                         reason and produce creative solutions (Chen et al. 2025a).              be constructive, requiring solutions tailored to each instance.
                                         Results within mathematics have shown this interest to be               A benchmark admits a confound for each of the properties it
                                         well-founded. In 2026, a general-purpose reasoning model                lacks. Without renewability and constructiveness, creativity
                                         resolved the roughly eighty-year-old Erdős unit-distance con-           may not have been necessary: the problem could have been
                                         jecture, a long-open question in discrete geometry (OpenAI              answered from memory or by a known general procedure.
                                         2026). Producing such a result requires creativity, defined in          As depicted in Table 1, every prior benchmark family has
                                         the literature by two joint criteria: a creative solution must be       at most two of the three. Synthetic puzzles such as random
                                         original, and it must be effective, meaning it provides value           SAT (Selman, Mitchell, and Levesque 1996) and the Equa-
tional Theories Project (Bolan et al. 2025) are verifiable and                Molecule design              ALPS instance
renewable but can be solved with a general procedure given        Specify     target profile: bind the     a law L the operation
enough compute, so success measures the ability to execute                    pocket, non-toxic, syn-      must satisfy on every as-
a known method. Static corpora such as MATH (Hendrycks                        thesizable                   signment
et al. 2021), coding benchmarks (Chen et al. 2021), and
miniF2F (Zheng, Han, and Polu 2021) ask for constructed,          Construct   propose a structure satis-   propose a magma satis-
                                                                              fying all constraints        fying L
checkable solutions, but draw from fixed sets that eventu-
ally contaminate training data, so a high score may reflect       Verify      synthesis and assay con-     a proof certificate con-
memorization (Xu et al. 2024). Open scientific discovery,                     firm the profile             firms the model
such as hypothesis generation (Gottweis et al. 2026; Lu et al.
2024) and molecule design (Jumper et al. 2021), demands           Table 2: Discovery proceeds by the same three phases in
construction and never exhausts its supply, but its answers       either domain; in ALPS, every phase is machine-checkable.
are judged subjectively, so scores depend on the judge.
   Formal mathematics is the one setting where each of these
three properties can be fulfilled simultaneously. A formal
                                                                  on every assignment of elements, the solver constructs a
proof can be checked automatically, and problems can be gen-
                                                                  magma meeting them, and a proof certificate verifies that it
erated without limit, so verifiability and renewability come
                                                                  does, across the infinitely many cases the solver can never
immediately. Construction is the property that must be estab-
                                                                  check directly. Constructing a mathematical object that prov-
lished by design. Equational theory (Birkhoff 1935) studies
                                                                  ably meets such a specification is itself an act of scientific
magmas: sets with a single binary operation ⋄, and their
                                                                  discovery, and these three phases — specify, construct, and
laws, universally quantified equations such as commutativity
                                                                  verify — recur across the sciences (Table 2). For example, in
x ⋄ y = y ⋄ x (Burris and Sankappanavar 1981; Baader and
                                                                  molecule design, they are a target profile, a proposed struc-
Nipkow 1998). A magma satisfying a law is a model of it. The
                                                                  ture, and a synthesis assay; in ALPS, the law L, a magma,
one-element magma, called the trivial magma, models every
                                                                  and a proof certificate. Because that proof decides both con-
law and carries no information. The substantive question is
                                                                  ditions of valid creativity from the answer alone, a verified
whether a law has a nontrivial model, one with at least two
                                                                  solution is direct evidence that the language model created a
elements. Within a finite carrier, such a model can always
                                                                  novel structure and justified it. The claim is confined to what
be found by search. Some laws, however, have no nontrivial
                                                                  is certifiable: the problem admitted no solution by memory
finite model, yet have a nontrivial model all the same, neces-
                                                                  or routine, and the answer is provably correct — properties
sarily infinite: these are the Austin laws (Kisielewicz 1997;
                                                                  of the problem and of the answer rather than of the process
Bolan et al. 2025). No finite search reaches an infinite model;
                                                                  that produced them.
it must be constructed and then justified.
   We introduce the Austin-Law Proof-Synthesis (ALPS)                We demonstrate empirically that the task ALPS defines is
benchmark. Each instance is a law with no nontrivial fi-          constructive. A portfolio built from eight configurations of
nite model, a property established in advance, which leaves       the strongest automated provers (Kovács and Voronkov 2013;
exactly two possibilities: the law is trivial, collapsing every   Schulz, Cruanes, and Vukmirović 2019; Smallbone 2021)
model so that x = y, or it is Austin, with an infinite model      resolves 2.2% of the 4,141 laws that survive screening, and
that satisfies it. Solving an instance means deciding which       a twentyfold increase in per-prover budget adds 0.6%. The
holds and proving it: a deductive proof on the trivial side, a    remaining laws yield neither a model nor a triviality proof
constructed infinite model on the Austin side. Every answer       under any configuration we test, although each is certified to
is settled by an automatically validated proof certificate, so    have a determinate answer; they are limited by the methods
grading is objective and needs no human judge. The instances      available rather than by the compute allotted to them. In full,
come from a generator that proposes candidate laws without        our contributions are:
limit, then screens each to keep only those with this property,
so ALPS never runs short of fresh, unseen problems.                • a two-sided construction task on Austin laws, with every
   Austin laws sit where AI-for-science and mathematical             instance certified to have a determinate answer;
provers are converging. The Erdős unit-distance conjecture         • a corpus of such laws and a public generator that mints
was settled by a reasoning model through construction within         fresh instances without limit;
an infinite space, at the frontier of what current language
models can do (OpenAI 2026). Computational mathemati-              • an automated judge that certifies submissions through
cal provers approach from the other side with new methods            independent channels — a Lean proof (Moura and Ullrich
of constructing infinite models (Janota, Rawson, and Schulz          2021) for triviality, and an automated-prover certificate
2026). Austin laws are a renewable supply of this challenge:         (Kovács and Voronkov 2013) for constructed models —
each is an infinite-construction problem with a definite an-         with no human in the loop; and
swer, and fresh ones can be generated without limit.
   What ALPS requires of the solver reaches well beyond            • a strong automated baseline that establishes the method-
equational theory. Resolving a law means proposing a new             bound hard tier and, along the way, settles an order-5
mathematical structure and establishing its global properties:       case left open by the Equational Theories Project (ETP)
the law L specifies the conditions the operation must satisfy        (Bolan et al. 2025).
                   2    Related Works                              Twee (Smallbone 2021) implements unfailing Knuth–Bendix
Existing benchmark families each contain two of the three          completion (Knuth and Bendix 1970; Bachmair, Dershowitz,
properties and fall short on the third (Table 1). Static prob-     and Plaisted 1989), orienting equations into rewrite systems.
lem sets span competition mathematics (Cobbe et al. 2021;          When a saturation halts without reaching a contradiction, its
Hendrycks et al. 2021), graduate science (Rein et al. 2023),       accumulated clauses describe a model; Janota, Rawson, and
coding (Chen et al. 2021), and formal proof (Zheng, Han,           Schulz (2026) recently extracted an explicit model from such
and Polu 2021; Azerbayev et al. 2023; Tsoukalas et al. 2024).      a saturation in a case study.
These are scored objectively, but fixed evaluation sets eventu-
ally enter training data, after which performance may reflect               3      The Austin-Law Proof-Synthesis
memorization (Xu et al. 2024; Chen et al. 2025b). Holding                                    Benchmark
problems secret (Glazer et al. 2024) or releasing them over        ALPS is built in three parts: a two-sided task, a corpus gen-
time (White et al. 2025; Jain et al. 2025) delays contamination    erator, and an automated judge. Each part provides one prop-
but remains limited by the rate at which humans author new         erty listed in Table 1: the admissibility certificate makes every
problems. Synthetic puzzles such as random SAT (Selman,            instance a construction problem with a determinate answer,
Mitchell, and Levesque 1996), graph-generated reasoning            the extension engine renews the supply without limit, and the
tasks (Zhu et al. 2024), Sudoku variants (Seely et al. 2025),      judge verifies answers automatically.
and the equational laws of the Equational Theories Project
(Bolan et al. 2025) renew without limit, but the regularity        3.1    Problem Formulation
that makes their problems generable also makes them solv-
able by a known procedure, so success can measure execu-           A magma is a set M , called the carrier, together with a
tion of a method rather than construction of a solution. Open      single binary operation ⋄ : M × M → M and no further
scientific discovery tasks such as hypothesis generation and       axioms. An equational law is a universally quantified identity
molecule or materials design (Lu et al. 2024; Gottweis et al.      between two terms built from variables and ⋄. Its order is the
2026; Alkan et al. 2025; Romera-Paredes et al. 2024; Mer-          number of times the operation appears, so the commutative
chant et al. 2023; Jumper et al. 2021) demand construction         law x ⋄ y = y ⋄ x has order two. A magma satisfies a law
and never exhaust their supply, but their results are validated    when the identity holds under every assignment of carrier
by human expertise or physical experiment, so evaluation           elements to its variables; such a magma is called a model of
is subjective and slow. ALPS combines the strengths of the         the law.
three families: objective scoring, unlimited renewal, and a           Every ALPS instance is a law of the form L : x =
constructive task that no known general procedure solves.          T [x, y, z, . . . ]: a designated variable x, isolated on the left-
   ALPS grades answers by machine verification, made pos-          hand side, equated with a term T of order five or more, where
sible by theorem provers. Lean (Moura and Ullrich 2021)            brackets list variables from which T is built; x may itself re-
is a proof assistant whose kernel mechanically checks each         cur within T . The trivial magma contains only one element,
submitted proof, so a proof it accepts is correct by con-          and is thus a model of every law. A model is nontrivial when
struction. A statement quantified over infinitely many inputs,     its carrier holds at least two distinct elements. The question
such as a law holding under every assignment, is checked           ALPS poses for each L is whether a nontrivial model exists
once, symbolically, rather than case by case. Finding proofs,      at all: either L entails x = y, collapsing every model to a
unlike checking them, is difficult. Classical automated theo-      single value, or some nontrivial magma satisfies it.
rem provers such as Vampire and E (Kovács and Voronkov                A nontrivial model, when one exists, may be finite or infi-
2013; Schulz, Cruanes, and Vukmirović 2019) search for             nite. The finite case is a matter of search: enumerating oper-
first-order proofs by superposition (Bachmair and Ganzinger        ations on carriers of increasing size must eventually find it,
1994), repeatedly deriving consequences of the input until         requiring none of the law-specific creativity the benchmark
a contradiction is reached or no new consequences remain.          aims to measure. We therefore admit a law into the bench-
More recently, language models have been trained to con-           mark only when it carries a machine-checked proof that no
struct proofs in systems such as Lean (Yang et al. 2023; Xin       nontrivial finite model exists, calling such laws admissible.
et al. 2024; Hubert et al. 2026), measured on formal proof         Admissibility forces a dichotomy: every law either entails
benchmarks (Zheng, Han, and Polu 2021).                            x = y or it does not, so each instance has a determinate
   Equational theory studies the identities that operations sat-   answer. Since laws are universally quantified, L |= x = y
isfy and the entailments among them. The Equational Theo-          states that any two elements of any model are equal. For an
ries Project (Bolan et al. 2025) enumerates the implications       admissible law, the two cases are exactly
among thousands of small laws and settles them automati-            L |= x = y        or   |L has an infinite{znontrivial model} . (1)
cally with provers and finite-model finders, singling out the       | {z }
                                                                                                          Austin
                                                                         trivial
Austin laws (Kisielewicz 1997) — those whose only non-
trivial models are infinite — as the hardest to resolve, since     Laws of the second kind are Austin laws (Kisielewicz 1997).
neither a finite-model search nor a short derivation settles          The asymmetry between the two sides of the task is es-
them. Among methods tailored to equational laws, Paradox           sential to what the benchmark measures. Whether L entails
and Mace4 (Claessen and Sörensson 2003; McCune 2003)               x = y is a question of first-order logic, the language of state-
find finite models when they exist, Infinox (Claessen and          ments built from the operation ⋄, equality, logical connec-
Lillieström 2011) proves that no finite model exists, and          tives, and quantifiers ranging over carrier elements (Baader
      Screening stage               Removed     Remaining
      Generated candidates                —         10,474
                                                                                 surj(S) : ∀ȳ ∀u ∃x : S(x, ȳ) = u.              (2)
      Finite-model filter              1,085         9,389             The admissibility query submits both facts to the prover as
      Admissibility prover             1,906         7,483          a single derivation task, written ⊢ in contrast to the entailment
      Admissible pool:                                              |= of Equation (1):
        Proven trivial                               3,080
        Austin classes (262 laws)                      195                              {L, surj(S)} ⊢ x = y.                    (3)
        Unresolved residual                          4,141             A refutation proof of Equation (3) is the admissibility
                                                                    certificate: a derived statement holds in every model of its
Table 3: The screening pipeline. In the top block, each stage       premises, and every finite model of L satisfies both premises,
removes the number of candidates shown and passes the re-           so every finite model of L is trivial. As a result, either L
mainder to the next. The bottom block partitions the certified      entails x = y, or L has a nontrivial model, which must
pool by the proofs screening produced: 3,080 proven trivial,        then be infinite. Admission requires this certificate, and none
262 proven Austin (reported as 195 equivalence classes), and        exists for a law with a nontrivial finite model. When injec-
4,141 unresolved by screening, summing to 7,483.                    tivity cannot be proven, the candidate remains uncertified
                                                                    and is discarded even though it may have been admissible.
                                                                    The screening provers classify the admissible pool into laws
and Nipkow 1998). Proof search within first-order logic is          proven trivial, laws proven Austin, and the residual that the
complete: if the entailment holds, a systematic search will         baseline of the next section attempts.
eventually confirm it. The trivial side is, in principle, settled      Deduplication. Because every law descends from a seed
by deduction. The Austin case admits no such guarantee. A           set, an extension may pose the same problem as its seed or a
search that fails to derive x = y, however long it runs, yields     sibling, defined as when each entails the other:
no model. Because equational entailment is undecidable in                            L1 |= L2     and   L2 |= L1 ,               (4)
general (Baader and Nipkow 1998), no uniform procedure
can be expected to close the gap. Establishing that a law           in which case the two laws have the same models and are
is Austin means inventing an infinite magma tailored to the         called equivalent. A pair is distinct when either direction of
individual law to satisfy it. This synthesis, which deductive       Equation (4) fails, and a failure is witnessed by a separating
search does not supply, is the capability that ALPS isolates.       model: a magma that is a model of L1 but not of L2 shows
                                                                    L1 ̸|= L2 . The models constructed during screening double
3.2   Corpus Construction                                           as these witnesses. Across the 34,191 pairs among the 262
                                                                    laws proved Austin, 33,936 pairs are separated by a model
Generation by extension. Admissible laws are too rare for           found during screening. The prover settles the remainder
random sampling to produce in quantity. We instead grow the         by deriving both directions of Equation (4): 255 pairs are
corpus outward from laws already proven to be Austin: a seed        proved equivalent, and no pair is left undecided. Because
law x = T is extended by selecting any variable v in T and          equivalence is transitive, the 255 proved equivalences chain
replacing one occurrence with v ⋄ w or w ⋄ v for some other         into groups of mutually equivalent laws, each counted as a
variable w. Because a candidate inherits most of the seed’s         single problem. A group of k laws accounts for k(k −1)/2 of
term structure, it often inherits the mechanism that prevents       the proved pairs but only k − 1 duplicates, which is why 255
a finite model, increasing the likelihood of finding new ad-        pairs merge away only 67 laws: the 262 laws collapse to 195
missible laws relative to random sampling. The construction         classes. We report corpus size in classes, so the count reflects
is recursive — laws confirmed Austin at order n seed the            only distinct problems and no solution is credited twice.
round at order n + 1 — so the corpus has no terminal order.
This keeps the supply of new laws renewable: fresh instances        3.3   Answer Verification
can be minted after any training cutoff, so evaluation never
                                                                    Each solved ALPS instance is a machine-verified mathemati-
depends on problems a model may have seen.
                                                                    cal statement. The two sides of the task require different veri-
   Admissibility. Each candidate then enters the screening          fication processes, so the judge issues a certificate through the
pipeline (Table 3). A finite-model filter discards every can-       appropriate channel: a proof checked by the Lean kernel for
didate it can satisfy nontrivially. The survivors face the ad-      the trivial side (Moura and Ullrich 2021), and an automated-
missibility prover, which attempts a proof that no nontrivial       prover certificate for the constructed model (Kovács and
finite model exists. The claim cannot be posed to the prover        Voronkov 2013). Both channels are fully automatic, and a
directly, because finiteness is not expressible in first-order      submission is accepted only if its check succeeds. Verifica-
logic; the proof instead works through a consequence of             tion rests on two trusted checkers, the Lean kernel on the
finiteness: on a finite carrier, an injective map is also surjec-   trivial side and prover saturation on the construction side,
tive. Let S be a subterm of T containing every occurrence of        cross-checkable by a second prover (Smallbone 2021).
x, so that the law reads x = C[ S(x, ȳ) ], where the surround-        The trivial channel. For each law, the judge generates the
ing context C contains no x, and ȳ abbreviates the remaining       proposition
variables. The law itself thus makes C a left inverse of S,
so S is injective in every model. Every finite model of L                  TrivialGoal ≡ ∀M ∀⋄ : M × M → M,
                                                                                                                                 (5)
additionally satisfies the first-order statement                                         Law(⋄) → ∀a, b : M, a = b,
        A toy inadmissible law                                         A hard-tier law
        L0 : x = x ⋄ (y ⋄ y)                                           L : x = y ⋄ (x ⋄ (((w ⋄ y) ⋄ ((y ⋄ z) ⋄ (y ⋄ x))) ⋄ y))


        Sample submission                                              o4-mini’s submission
        E0 : u ⋄ v = u                                                 E1 : y ⋄ (x ⋄ y) = x              E2 : x ⋄ (z ⋄ y) = x ⋄ y
        the operation returns its left argument                        z is universally quantified and may be instantiated at any term


        The two checks                                                 The two checks
        (a) E0 ⊢ L0 : rewriting with u ⋄ v = u (u = x, v = y ⋄ y):     (a) E ⊢ L: instantiating z at the law’s middle subterm,
            x ⋄ (y ⋄ y) = x, so both sides of L0 agree.           ✓                               E
                                                                           y ⋄ (x ⋄ (z ⋄ y)) =2 y ⋄ (x ⋄ y) =1 x
                                                                                                                     E
                                                                                                                                         ✓
        (b) E0 ∪ {a ̸= b} satisfiable: the two-element magma with      (b) E ∪ {a ̸= b} satisfiable: for any t,
            s ⋄ t = s for all s, t satisfies E0 and keeps a ̸= b. ✓      E                 E
                                                                       t =1 y ⋄ (t ⋄ y) =2 y ⋄ y,
        Certified: E0 has a nontrivial model satisfying L0 .
                                                                          so every element equals y ⋄ y: E forces a = b.       ×
                                                                       Rejected at check (b): E admits no model with two distinct
                                                                       elements.

Figure 1: The two checks on two laws. Left: a sample submission on a toy, inadmissible law passes both checks; for admissible
laws, admissibility forces the witnessing model to be infinite. Right: o4-mini’s submission on a hard-tier law passes check (a)
but fails check (b), the “too-strong” failure mode most common across the LLMs we evaluate.


where Law(⋄) asserts that ⋄ satisfies L. In words, Equa-                of E while keeping two elements a and b distinct. The prover
tion (5) states that any magma satisfying L has all of its              answers by saturation: starting from E ∪ {a ̸= b}, it derives
elements equal: it is the trivial side of Equation (1), with            consequences until either a contradiction appears or nothing
the magma quantified inside the statement so that a single              new can be derived, at which point the set is called saturated.
proof covers every carrier and every operation at once. A               A saturated set that contains no contradiction is satisfiable,
submission is a Lean proof of Equation (5). The statement is            provided no inference was skipped along the way, and its
generated by the judge, never written by the submitter: the             accumulated consequences describe a model (Bachmair and
judged file fixes Equation (5) in a header, inserts the submit-         Ganzinger 1994). Provers do skip inferences in some con-
ted proof, and requires it to elaborate at exactly that type, and       figurations, trading completeness for speed, and report when
the proof’s axiom footprint must fall within a fixed allowlist,         they have done so. The judge therefore accepts check (b) only
which blocks declared axioms and placeholder proofs that                when the prover reports that its strategy retained complete-
would allow a solver to postulate what it must prove. Under             ness. A terminating, complete saturation of E ∪{a ̸= b} thus
these constraints, a proof the kernel accepts is correct by             establishes claim (ii). The two checks compose: by (ii) some
construction (Moura and Ullrich 2021). In practice, such a              magma satisfies E with a ̸= b, by (i) that magma satisfies L,
proof formalizes a chain of equalities a = t1 = · · · = tk = b          so L has a nontrivial model, and the admissibility certificate
in which each step applies one instance of L.                           of the previous section forces that model to be infinite. L is
   The construction channel. A model of an Austin law                   therefore Austin. Neither query mentions infinity: both are
has an infinite carrier, but a submission must be a finite              finite first-order tasks, and infinitude enters only through the
object a machine can check. The solver instead submits a                admissibility certificate the instance already carries.
finite presentation E: a finite set of equations over ⋄, whose             Although grading is fully automatic, the checks themselves
models are the magmas satisfying every equation in E. E                 reject any submission that does not encode a genuine con-
must satisfy two claims: (i) every model of E satisfies L,              struction, so a certificate cannot be earned without solving
and (ii) some model of E has two distinct elements. The                 the instance. Submitting the law itself as E gains nothing:
claims constrain E from opposite sides: it must be strong               check (a) becomes immediate, but check (b) reduces to the
enough to entail the law, yet weak enough that its models               saturation of L∪{a ̸= b}, the computation that fails to termi-
do not all collapse to one element. The judge accepts only              nate on these laws. A presentation too strong collapses every
when a prover certifies both. Figure 1 (left) demonstrates this         element and fails check (b) (Figure 1, right); one too weak,
process on a toy law. Formally, the two queries are                     such as the left projection {x ⋄ y = x}, fails check (a). The
                                                                        judge is validated against controls of all three kinds before
                                                                        any evaluation run, and the submission format admits only
  (a) E ⊢ L                   (b) E ∪ { a ̸= b } is satisfiable. (6)
                                                                        unconditional equations, so implications, disequations, and
   Check (a) is a derivation task of the same kind as Equa-             literal restatements of x = y never reach the prover.
tion (3): the prover returns a refutation proof that L is deriv-           A single Lean judge covering both sides is not currently
able from the equations of E, and by the same reasoning                 possible. The model families that are straightforward to for-
as before, every model of E satisfies L, which is claim (i).            malize in Lean are arithmetic. No model of an admissible
Check (b) asks whether some magma satisfies every equation              law is among them, since an arithmetic operation satisfying
the law would yield a nontrivial finite model, contradicting         Budget (s)     New models      New trivial     Unresolved
admissibility. The models that do exist are built from satu-
rations (Janota, Rawson, and Schulz 2026), and formalizing                    30                4             87          4,050
these in Lean awaits a proof of ground confluence. The con-                   60                0              8          4,042
struction side is therefore graded by the prover certificate.                120                0              5          4,037
                                                                             300                0              4          4,033
                                                                             600                0              6          4,027
                    4    Experiments
4.1   The Automated Frontier                                       Table 4: Newly resolved laws at each per-configuration bud-
We establish what automation resolves using a portfolio span-      get over the 4,141-law residual. All models appear at 30
ning eight configurations of leading off-the-shelf provers:        seconds; every later resolution is a triviality proof, and 4,027
Vampire 5.0.1 in five modes (proof search and satura-              laws (97.2%) remain unresolved.
tion, under Knuth–Bendix and lexicographic path orderings)
(Kovács and Voronkov 2013), the E prover in a proof and
a saturation mode (Schulz, Cruanes, and Vukmirović 2019),          4.2   The LLM Frontier
and Twee 2.6.1, an implementation of unfailing completion          Language models enter ALPS on the same terms as the auto-
built for equational reasoning (Smallbone 2021), each run-         mated portfolio: nothing in the task references how an answer
ning over per-prover budgets of up to 600 seconds. A law           is produced, only that it certifies. We evaluate them under a
is resolved if any configuration returns a certificate. Finite-    fixed protocol designed so that failures are attributable. Every
model finders such as Mace4 (McCune 2003) and Paradox              solver receives identical inputs — the law, the task statement,
(Claessen and Sörensson 2003) cannot succeed and are omit-         and a fixed answer format — and may submit to the judge
ted, as our admissibility classification certifies that no non-    up to three times, receiving each verdict as feedback. On the
trivial finite model exists. Saturation and completion are au-     trivial side, the formalization burden is removed. The LLM
tomated methods in the portfolio that can exhibit a model:         emits the entire chain of equalities between two arbitrary
a saturation that terminates without contradiction describes       carrier elements a and b, each step being one application
one (Section 3.3).                                                 of the law, and the autoformalization harness matches each
   Sweeping the portfolio over the admissible pool distin-         step to assemble the Lean proof itself, so the task is focused
guishes two populations. The models of the 262 laws proved         on finding the derivation rather than writing Lean. This as-
Austin during screening are constructed in a median of 0.1         sistance is fixed, and the harness is frozen across LLMs. A
seconds, and sweeping the 4,141-law residual with the full         waypoint lemma is an equality a prover has already derived
portfolio reclassifies a further 114 laws (2.8% of the resid-      from the law. Provided waypoints, the LLM does not need
ual): 110 triviality proofs and 4 completion-only models.          to plan the whole chain at once: it can build a shorter chain
The remaining 4,027 laws resolve under no configuration at         to a waypoint and continue from there. Waypoints cannot
any budget up to 600 seconds and constitute the hard tier,         fix an individual step, since every step the LLM writes must
defined by this gap in the resolution-time distribution. If this   still be a correct application of the law. Comparing runs with
gap were simply a result of insufficient compute, additional       and without waypoints therefore shows where failures lie:
budget would be expected to continue resolving new laws of         in finding chains, which waypoints make easier, or in writ-
both kinds at a comparable rate. Instead, of the 114 residual      ing correct steps, which waypoints do not affect. Saturation
laws the sweep resolves, 91 resolve at the 30-second per-          provers are withheld, since with them a solver could simply
configuration budget. Raising the budget by a factor of 20         re-run the portfolio; the judge and the harness are the tools
resolves only 23 more, each one a triviality proof (Table 4).      available to any solver built on ALPS.
All four models the sweep recovers, together with the 262             We construct one law set for each of the two sides of the
constructed during screening, are identified within the first      task. The certified-easy set tests whether an LLM can pro-
30 seconds.                                                        duce a valid solution under the most favorable conditions the
   The resolved tier contains a result of independent interest.    corpus offers: 63 trivial-tier laws with simple collapse chains
Among the laws the portfolio resolves is an order-five law         a = t1 = · · · = tk = b. Rewriting from both ends until the
and its dual (12857 and 33436 in the ETP numbering) that           two chains meet resolves all 63 in under five seconds, and
the Equational Theories Project recorded as having only triv-      most chains are only three law applications long. The con-
ial finite models, leaving the existence of an infinite model      struction experiment is posed over a sample of 25 of the
open (Bolan et al. 2025). Two independent methods, Vampire         4,027 “hard-tier” laws that no automated configuration re-
saturation and Twee completion, terminate without deriving         solves. These laws are open in both directions so we evaluate
x = y. As established in Section 3.3, a terminating, complete      both channels: the construction channel of Section 3.3, and
run describes a model where x = y fails, and admissibility         the trivial channel without waypoints. Both evaluation sets
forces that model to be infinite. We verify the extracted pre-     contain only laws minted by the extension procedure, and the
sentation, a set of 27 equations, directly: it satisfies the law   generator runs past the released corpus, so future evaluations
and does not force x = y. The model is of the saturation-          can draw instances created after any LLM’s training cutoff.
derived kind described in Section 3.3, so its Lean formaliza-         Table 5 reports the trivial-side results. Without waypoints,
tion awaits the ground-confluence proof noted there; the full      o3 at medium reasoning effort produces six verified solu-
worked example is provided in the Appendix.                        tions on the 63 certified-easy laws (9.5% pass@1), and nine
                Certified-easy (n = 63)         Hard (n = 25)                           5    Discussion
LLM         Default    Waypoints     ↓ Effort    Construction     The solver failures of Section 4.2 reveal weaknesses that
                                                                  are not specific to mathematical reasoning. Trivial-side fail-
GPT-4.1        0           0            —              0          ures concentrate in step validity rather than planning, which
o4-mini        0           0            0              0          self-verification at each step could address. Construction-
o3             6           9            0              0          side submissions fail as too strong or too weak, with the
                                                                  judge reporting which. Passing both checks requires balanc-
Table 5: Verified LLM solves under the fixed protocol. Way-       ing two opposing requirements: satisfying a global specifi-
points are prover-derived lemmas included in the prompt.          cation without collapsing into a degenerate solution. Both
Reasoning effort is medium except where marked ↓, which           weaknesses concern creative generation under constraints, a
denotes low effort; GPT-4.1 has no effort setting.                requirement of general scientific problem-solving, not just
                                                                  equational theory. These patterns point to a verify-and-refine
                                                                  loop, one that drafts a structure to satisfy global constraints,
                                                                  reads a verdict, and revises accordingly. If these weaknesses
(14%) with waypoints. GPT-4.1 and o4-mini produce none            generalize, other domains should have arrived at the same
even with waypoints, and setting o3’s reasoning effort to low     remedy independently; software synthesis did, standardizing
reduces its solves to zero. The verified chains are three to      it as counterexample-guided inductive synthesis (CEGIS)
four law applications long, most are accepted on the second       (Solar-Lezama et al. 2006), the architecture underlying pro-
or third feedback round, and a solved law costs a median of       gram sketching (Solar-Lezama 2013), syntax-guided syn-
roughly 50,000 completion tokens. Failures share one dom-         thesis (Alur et al. 2013), and invariant discovery (Garg et al.
inant pattern at every setting: the submitted chains contain      2014).
steps that are not applications of the law — no substitution         ALPS differs from those settings in one step. There, a
instance of either side of L rewrites one term into the next      human supplies the candidate space, as a sketch or a gram-
— and the harness rejects the chain at the matching stage.        mar; in ALPS, no candidate space is known (Section 3.3), so
   Solve events are stochastic. A second run using o3 under       the proposal must come from the solver. That proposal step
identical settings reproduces one of the nine solves. Single-     is the construct phase of the specify–construct–verify cycle
run counts are therefore pass@1 samples rather than a fixed       (Table 2), so the capability ALPS motivates extends wher-
solved set. The stable signals are binary: o3 produces verified   ever a specification can be stated and a solution checked.
solves in every run, GPT-4.1 and o4-mini in none, and low         Because each run leaves a certified failure profile and the cor-
reasoning effort in none. The variation is expected: each run     pus renews, evaluation, analysis, and redesign can continue
samples a fresh reasoning trace, and the harness provides         without exhausting the benchmark. The Appendix gives the
minimal guidance beyond the three feedback rounds, so these       full protocol prompts, per-configuration sweep results, and
results are a lower bound on language-model performance.          the complete failure classification.
The waypoint comparison sits within this variation: given the
low reproduction rate, the difference between six and nine is                          6    Conclusion
not distinguishable from run noise, and we treat the effect of
                                                                  We presented ALPS (Austin-Law Proof-Synthesis), a bench-
waypoints as suggestive. Its smallness is consistent with the
                                                                  mark that measures valid creativity in language models:
dominant failure mode: rejected chains fail on invalid steps,
                                                                  solving problems for which creativity is necessary, with an-
which waypoints do not repair.
                                                                  swers that are soundly justified. Each instance asks the solver
   o3, o4-mini, and GPT-4.1 each attempt the 25 hard-tier         to construct an infinite mathematical structure satisfying a
laws over three feedback rounds, and no submission passes         freshly minted law, or to prove that no such structure ex-
both checks. On the same laws, the trivial channel without        ists, and each is certified in advance to ensure finite search
waypoints also produces no verified solution, so every sam-       cannot settle it. Creativity is necessary because renewability
pled law remains open in both directions. Classifying each        and constructiveness remove the confounds: instances minted
law by its final-round submission, 23 of o3’s 25 presenta-        past any training cutoff cannot be answered from memory,
tions are overly strong: they entail the law but admit only       and a task automation rarely resolves — eight configurations
one-element models, passing check (a) and failing check (b).      of provers resolve 2.2% of the 4,141-law pool, and a twen-
The remaining two are too weak, maintaining two distinct          tyfold budget increase adds 23 triviality proofs and no new
elements but failing to entail the law. o4-mini divides into      models — cannot be answered by routine. Justification is se-
11 that are too strong, 4 that are too weak, and 10 that fail     cured by verifiability: acceptance is decided by the machine-
both checks; GPT-4.1 divides into 10, 11, and 4. Figure 1         checked certificate alone. The strongest LLM we test verifies
(right) shows one such submission. On final submissions, o3       14% of the certified-easy set and constructs nothing on the
clears exactly one check on all 25 laws, GPT-4.1 on 21, and       hard tier, where it satisfies one of the two checks on every
o4-mini on 15. The failure profile distinguishes the LLMs         law and weaker LLMs sometimes satisfy neither. That failure
despite all submissions failing: o3’s failures concentrate in a   profile specifies the verifier-guided solvers the benchmark re-
single mode, while the weaker LLMs spread across all three.       wards. We therefore release ALPS — corpus, generator, and
Producing a presentation that is neither too strong nor too       automated judge — with 97.2% of the evaluation pool unre-
weak is the capability the construction side tests.               solved by every configuration we test.
                         References                                  et al. 2021. Training verifiers to solve math word problems.
Alkan, A. K.; Sourav, S.; Jablonska, M.; Astarita, S.;               arXiv preprint arXiv:2110.14168.
Chakrabarty, R.; Garuda, N.; Khetarpal, P.; Pióro, M.; Tanog-        Garg, P.; Löding, C.; Madhusudan, P.; and Neider, D. 2014.
lidis, D.; Iyer, K. G.; et al. 2025. A survey on hypothesis gen-     ICE: A robust framework for learning invariants. In Interna-
eration for scientific discovery in the era of large language        tional Conference on Computer Aided Verification, 69–87.
models. arXiv preprint arXiv:2504.05496.                             Springer.
Alur, R.; Bodik, R.; Juniwal, G.; Martin, M. M.;                     Glazer, E.; Erdil, E.; Besiroglu, T.; Chicharro, D.; Chen, E.;
Raghothaman, M.; Seshia, S. A.; Singh, R.; Solar-Lezama,             Gunning, A.; Olsson, C. F.; Denain, J.-S.; Ho, A.; Santos, E.
A.; Torlak, E.; and Udupa, A. 2013. Syntax-guided synthe-            d. O.; et al. 2024. Frontiermath: A benchmark for evaluat-
sis. In 2013 Formal Methods in Computer-Aided Design,                ing advanced mathematical reasoning in ai. arXiv preprint
1–8. IEEE.                                                           arXiv:2411.04872.
Azerbayev, Z.; Piotrowski, B.; Schoelkopf, H.; Ayers, E. W.;         Gottweis, J.; Weng, W.-H.; Daryin, A.; Tu, T.; Sirkovic, P.;
Radev, D.; and Avigad, J. 2023. Proofnet: Autoformaliz-              Myaskovsky, A.; Glowaty, G.; Weissenberger, F.; Orlandi, A.;
ing and formally proving undergraduate-level mathematics.            Popovici, D.; et al. 2026. Accelerating scientific discovery
arXiv preprint arXiv:2302.12433.                                     with Co-Scientist. Nature, 1–3.
Baader, F.; and Nipkow, T. 1998. Term rewriting and all that.        Hendrycks, D.; Burns, C.; Kadavath, S.; Arora, A.; Basart,
Cambridge university press.                                          S.; Tang, E.; Song, D.; and Steinhardt, J. 2021. Measuring
Bachmair, L.; Dershowitz, N.; and Plaisted, D. A. 1989.              mathematical problem solving with the math dataset. arXiv
Completion without failure. In Rewriting Techniques, 1–30.           preprint arXiv:2103.03874.
Elsevier.                                                            Hubert, T.; Mehta, R.; Sartran, L.; Horváth, M. Z.; Žužić, G.;
Bachmair, L.; and Ganzinger, H. 1994. Rewrite-based equa-            Wieser, E.; Huang, A.; Schrittwieser, J.; Schroecker, Y.; Ma-
tional theorem proving with selection and simplification.            soom, H.; et al. 2026. Olympiad-level formal mathematical
Journal of Logic and Computation, 4(3): 217–247.                     reasoning with reinforcement learning. Nature, 651(8106):
                                                                     607–613.
Birkhoff, G. 1935. On the structure of abstract algebras. In
Mathematical proceedings of the Cambridge philosophical              Jain, N.; Gu, A.; Li, W.-D.; Yan, F.; Zhang, T.; Wang,
society, volume 31, 433–454. Cambridge University Press.             S.; Solar-Lezama, A.; Sen, K.; and Stoica, I. 2025. Live-
                                                                     codebench: Holistic and contamination free evaluation of
Bolan, M.; Breitner, J.; Brox, J.; Carlini, N.; Carneiro, M.;        large language models for code. In International Conference
van Doorn, F.; Dvorak, M.; Goens, A.; Hill, A.; Husum, H.;           on Learning Representations, volume 2025, 58791–58831.
et al. 2025. The Equational Theories Project: Advancing
collaborative mathematical research at scale. arXiv preprint         Janota, M.; Rawson, M.; and Schulz, S. 2026. Case Study:
arXiv:2512.07087.                                                    Saturations as Explicit Models in Equational Theories. arXiv
                                                                     preprint arXiv:2602.16324.
Burris, S.; and Sankappanavar, H. P. 1981. A course in
universal algebra, volume 78. Springer.                              Jumper, J.; Evans, R.; Pritzel, A.; Green, T.; Figurnov, M.;
                                                                     Ronneberger, O.; Tunyasuvunakool, K.; Bates, R.; Žídek, A.;
Chen, M.; Tworek, J.; Jun, H.; Yuan, Q.; Pinto, H. P. D. O.;         Potapenko, A.; et al. 2021. Highly accurate protein structure
Kaplan, J.; Edwards, H.; Burda, Y.; Joseph, N.; Brockman,            prediction with AlphaFold. Nature, 596(7873): 583–589.
G.; et al. 2021. Evaluating large language models trained on
code. arXiv preprint arXiv:2107.03374.                               Kisielewicz, A. 1997. Austin identities. Algebra Universalis,
                                                                     38(3): 324–328.
Chen, Q.; Yang, M.; Qin, L.; Liu, J.; Yan, Z.; Guan, J.; Peng,
D.; Ji, Y.; Li, H.; Hu, M.; et al. 2025a. Ai4research: A survey      Knuth, D. E.; and Bendix, P. B. 1970. Simple word problems
of artificial intelligence for scientific research. arXiv preprint   in universal algebras. In Computational problems in abstract
arXiv:2507.01903.                                                    algebra, 263–297. Elsevier.
Chen, S.; Chen, Y.; Li, Z.; Jiang, Y.; Wan, Z.; He, Y.; Ran,         Kovács, L.; and Voronkov, A. 2013. First-order theorem
D.; Gu, T.; Li, H.; Xie, T.; et al. 2025b. Recent advances           proving and Vampire. In International Conference on Com-
in large langauge model benchmarks against data contami-             puter Aided Verification, 1–35. Springer.
nation: From static to dynamic evaluation. arXiv preprint            Lu, C.; Lu, C.; Lange, R. T.; Foerster, J.; Clune, J.; and Ha, D.
arXiv:2502.17521.                                                    2024. The ai scientist: Towards fully automated open-ended
Claessen, K.; and Lillieström, A. 2011. Automated inference          scientific discovery. arXiv preprint arXiv:2408.06292.
of finite unsatisfiability. Journal of Automated Reasoning,          McCune, W. 2003. Mace4 reference manual and guide. arXiv
47(2): 111–132.                                                      preprint cs/0310055.
Claessen, K.; and Sörensson, N. 2003. New techniques that            Merchant, A.; Batzner, S.; Schoenholz, S. S.; Aykol, M.;
improve MACE-style finite model finding. In Proceedings              Cheon, G.; and Cubuk, E. D. 2023. Scaling deep learning
of the CADE-19 Workshop: Model Computation-Principles,               for materials discovery. Nature, 624(7990): 80–85.
Algorithms, Applications, 11–27.                                     Moura, L. d.; and Ullrich, S. 2021. The lean 4 theorem prover
Cobbe, K.; Kosaraju, V.; Bavarian, M.; Chen, M.; Jun, H.;            and programming language. In International Conference on
Kaiser, L.; Plappert, M.; Tworek, J.; Hilton, J.; Nakano, R.;        Automated Deduction, 625–635. Springer.
OpenAI. 2026. An OpenAI Model Has Disproved a Central              Zheng, K.; Han, J. M.; and Polu, S. 2021. Minif2f: a cross-
Conjecture in Discrete Geometry. https://openai.com/index/         system benchmark for formal olympiad-level mathematics.
model-disproves-discrete-geometry-conjecture/.                     arXiv preprint arXiv:2109.00110.
Rein, D.; Hou, B. L.; Stickland, A. C.; Petty, J.; Pang, R. Y.;    Zhu, K.; Chen, J.; Wang, J.; Gong, N.; Yang, D.; and Xie, X.
Dirani, J.; Michael, J.; and Bowman, S. R. 2023. Gpqa: A           2024. Dyval: Dynamic evaluation of large language models
graduate-level google-proof q&a benchmark. arXiv preprint          for reasoning tasks. In International Conference on Learning
arXiv:2311.12022.                                                  Representations, volume 2024, 18091–18128.
Romera-Paredes, B.; Barekatain, M.; Novikov, A.; Balog,
M.; Kumar, M. P.; Dupont, E.; Ruiz, F. J.; Ellenberg, J. S.;
Wang, P.; Fawzi, O.; et al. 2024. Mathematical discoveries
from program search with large language models. Nature,
625(7995): 468–475.
Runco, M. A.; and Jaeger, G. J. 2012. The standard definition
of creativity. Creativity research journal, 24(1): 92–96.
Schulz, S.; Cruanes, S.; and Vukmirović, P. 2019. Faster,
higher, stronger: E 2.3. In International Conference on Au-
tomated Deduction, 495–507. Springer.
Seely, J.; Imajuku, Y.; Zhao, T.; Cetin, E.; and Jones, L. 2025.
Sudoku-Bench: Evaluating creative reasoning with Sudoku
variants. arXiv preprint arXiv:2505.16135.
Selman, B.; Mitchell, D. G.; and Levesque, H. J. 1996. Gen-
erating hard satisfiability problems. Artificial intelligence,
81(1-2): 17–29.
Smallbone, N. 2021. Twee: an equational theorem prover.
In International Conference on Automated Deduction, 602–
613. Springer.
Solar-Lezama, A. 2013. Program sketching. International
Journal on Software Tools for Technology Transfer, 15(5):
475–495.
Solar-Lezama, A.; Tancau, L.; Bodik, R.; Seshia, S.; and
Saraswat, V. 2006. Combinatorial sketching for finite pro-
grams. In Proceedings of the 12th international conference
on Architectural support for programming languages and
operating systems, 404–415.
Tsoukalas, G.; Lee, J.; Jennings, J.; Xin, J.; Ding, M.; Jen-
nings, M.; Thakur, A.; and Chaudhuri, S. 2024. Putnam-
bench: Evaluating neural theorem-provers on the putnam
mathematical competition. Advances in Neural Information
Processing Systems, 37: 11545–11569.
White, C.; Dooley, S.; Roberts, M.; Pal, A.; Feuer, B.; Jain,
S.; Shwartz-Ziv, R.; Jain, N.; Saifullah, K.; Dey, S.; et al.
2025. Livebench: A challenging, contamination-limited llm
benchmark. In International Conference on Learning Rep-
resentations, volume 2025, 91595–91631.
Xin, H.; Guo, D.; Shao, Z.; Ren, Z.; Zhu, Q.; Liu, B.; Ruan,
C.; Li, W.; and Liang, X. 2024. Deepseek-prover: Advancing
theorem proving in llms through large-scale synthetic data.
arXiv preprint arXiv:2405.14333.
Xu, C.; Guan, S.; Greene, D.; Kechadi, M.; et al. 2024.
Benchmark data contamination of large language models:
A survey. arXiv preprint arXiv:2406.04244.
Yang, K.; Swope, A.; Gu, A.; Chalamala, R.; Song, P.; Yu,
S.; Godil, S.; Prenger, R. J.; and Anandkumar, A. 2023.
Leandojo: Theorem proving with retrieval-augmented lan-
guage models. Advances in Neural Information Processing
Systems, 36: 21573–21612.
                 Appendix                                          2021). Of the 357 equations, a substantial minority carry a
                                                                   free variable on each side, so they cannot be oriented into
 A    Worked Example: Laws 12857 and 33436                         rewrite rules in the usual sense.
Among the laws the portfolio resolves is a pair the Equational        That is a constraint on printing the system, not on the
Theories Project (Bolan et al. 2025) recorded as having only       construction. The model rewrites a ground term whenever the
trivial finite models, with the existence of an infinite model     ground instance strictly decreases, and a variable unbound
left unresolved. In the ETP numbering they are laws 12857          on the other side of an equation may be mapped to any
and 33436:                                                         ground term that makes the instance decrease — in practice
       L12857 :    x = y ⋄ ((x ⋄ (y ⋄ (z ⋄ z))) ⋄ y),              the smallest constant. Every equation is therefore usable, in
       L33436 :    x = ((y ⋄ (((z ⋄ z) ⋄ y) ⋄ x)) ⋄ y).            whichever direction decreases the instance. Termination is
                                                                   immediate because the ordering is well founded on ground
The two are duals: reversing the arguments of every occur-         terms, and ground confluence is inherited from saturation
rence of ⋄ in one yields the other. A magma satisfies one          under unfailing completion.
exactly when its opposite magma satisfies the other, so the           What is missing is an off-the-shelf certifier. Tools such as
pair is a single open case up to duality, and resolving either     CSI and TTT2 check plain rewriting systems, and the object
resolves both.                                                     here is an ordered one. A Lean formalization of this model
                                                                   therefore awaits a machine-checked ground confluence proof.
A.1    Two independent certificates                                Models of the algebraic kind, by contrast, are Lean-checkable
Both laws were resolved twice, by methods that share no            today; no admissible law admits one, for the reason given in
search strategy.                                                   Section 3.3.
   Vampire 5.0.1 (Kovács and Voronkov 2013) was run
in ordered saturation mode (-sa otter, default Knuth–                B    LLM Evaluation Protocol and Prompts
Bendix ordering) on the law together with the assertion that
two elements are distinct. It terminated with SZS status           B.1   The fixed protocol
Satisfiable in 7.95 seconds and 126 MB of memory,
                                                                   Every solver receives the same three inputs: the law, the task
printing an active set of 357 unit equations. A terminating,
                                                                   statement, and a fixed answer format. A submission may
complete saturation containing no contradiction describes
                                                                   be sent to the judge up to three times, and each verdict is
a model, as set out in Section 3.3; here the model is one
                                                                   returned verbatim as feedback before the next attempt. No
in which x = y fails, and the admissibility certificate the
                                                                   solver receives a hint that is not derived mechanically from
instance already carries forces that model to be infinite.
                                                                   the law itself, and the harness is frozen across all language
   Twee 2.6.1 (Smallbone 2021) was run indepen-
                                                                   models, so differences in outcome are attributable to the
dently on both laws and returned SZS status
                                                                   model rather than to the scaffolding.
CounterSatisfiable for each, deriving 55 rules for
12857 and 54 for 33436. Unfailing completion is complete              Saturation provers are withheld from the language-model
by construction, so this is a second certificate for the same      setting. With access to them a solver could re-run the au-
conclusion by a different route.                                   tomated portfolio of Section 4.1 rather than construct any-
                                                                   thing; the judge and the autoformalization harness are the
A.2    Verifying the presentation                                  tools available to any solver built on ALPS.
                                                                      All LLM calls use provider-default sampling through a
The saturated presentation is checked directly rather than
                                                                   single API gateway. The APIs expose no seed parameter,
taken on the prover’s word. Three properties are confirmed.
                                                                   and the reasoning LLMs are nondeterministic at any setting,
The ordering check verifies that the ordering used to evaluate
                                                                   so bitwise reproduction of a run is not available. Run-to-
the presentation matches the one recorded in the certificate
                                                                   run variation is therefore measured rather than controlled:
header, which is necessary because ground confluence is
                                                                   the reproduction run of Section 4.2 repeats the nine solved
inherited from the saturation only with respect to the ordering
                                                                   and five matched unsolved laws under the identical frozen
the prover saturated under; every pre-ordered equation is
                                                                   harness. The released result files record every attempt; the
comparable under that ordering. The law then holds on every
                                                                   submitted chain is withheld from solved rows, since a verified
ground instance tested, 27 of 27, and rewrites fire in all of
                                                                   chain is a solution to a certified-easy law, and every reported
them, so the model is not satisfying the law vacuously. Finally
                                                                   count is reproducible from the retained fields.
the two Skolem constants of the distinctness axiom normalise
to different terms, which establishes that the carrier has at
least two elements.                                                B.2   The trivial channel
   The presentation is too large to reproduce here; the certifi-   On the trivial side the formalization burden is removed. The
cate exists in the released code, and ordered_model.py             model emits a chain of equalities between two arbitrary car-
reproduces all three checks from it.                               rier elements a and b, each step being one application of the
                                                                   law, and returns it as JSON. The harness matches each step
A.3    Why this model is not Lean-checkable today                  against the law, bridges gaps of at most three single applica-
The presentation is not an off-the-shelf term rewriting sys-       tions automatically, and assembles the Lean proof itself. The
tem, which is why this model is graded by the prover cer-          model therefore searches for a derivation rather than writing
tificate rather than by the Lean kernel (Moura and Ullrich         Lean.
   A step is accepted only when some substitution instance                      D   LLM Failure Analysis
of one side of the law rewrites one term into the next at        Each language model attempts all 25 hard-tier laws over three
exactly one position, with everything outside that position      feedback rounds, and no submission from any model passes
unchanged. Two rejections are absolute: relating a and b         both checks. Because a run ends either in acceptance or after
directly, and any jump the bridging search cannot close.         three rejections, every law leaves a final-round submission,
   A waypoint lemma is an equality a prover has already de-      and Table A2 classifies all 75 of them by which of the two
rived from the law, supplied in the prompt. Waypoints shorten    checks that final submission satisfies.
planning — the model can build a chain to a waypoint and            The three classes partition the outcomes. A presentation
continue from there — but they cannot repair an individual       is too strong when it entails the law but admits only one-
step, since every step the model writes must still be a cor-     element models: check (a) succeeds and check (b) fails. It
rect application of the law. Comparing runs with and without     is too weak when it keeps two elements distinct but does
waypoints therefore separates failures of chain-finding from     not entail the law: check (b) succeeds and check (a) fails. A
failures of step validity.                                       submission failing both satisfies neither condition. The final
                                                                 column, counting laws on which the model clears exactly one
B.3   The construction channel                                   check, is therefore 25 minus the both-fail count.
On the construction side the model proposes a finite presen-        The trivial-side failures follow one dominant pattern at ev-
tation E: a set of unconditional equations over ⋄, returned      ery setting, and it is a different kind of failure. The submitted
as JSON. The submission format admits only unconditional         chains contain steps that are not applications of the law: no
equations, so implications, disequations and literal restate-    substitution instance of either side rewrites one term into the
ments of x = y never reach the prover. The judge then runs       next, so the harness rejects the chain at the matching stage
the two checks of Equation (6).                                  rather than at the prover. The failure is in executing individual
                                                                 steps soundly, not in planning a route between a and b.
B.4   Prompts
Figure A1 gives the trivial-channel prompt and Figure A2
                                                                          E    Corpus Yield and Renewability
the construction-channel prompt, both verbatim. Braces           Section 3.2 claims that the corpus has no terminal order
marked {law} and {hint_block} are substituted at call            and that fresh instances can therefore be minted after any
time; the hint block is empty in the no-waypoint condition       training cutoff. That claim is worth checking against yield:
and lists the prover-derived waypoint lemmas otherwise.          a generator whose output thins as the order grows would
On a rejected submission the harness appends the judge’s         eventually stop supplying instances, whatever the recursion
reason to the next round’s prompt: Your previous                 permits in principle.
chain was REJECTED: {feedback} on the triv-                         Table A3 gives the yield of the screening pipeline bro-
ial side, and Your previous proposal failed                      ken down by the order of the candidate law, over all 10,474
to certify: {feedback} followed by Try a                         candidates screened.
different presentation. on the construction side.                   Yield must be read as a density rather than a count. The
                                                                 raw number of Austin laws dips from 117 at order 7 to 105
  C    Automated Baseline: Per-Configuration                     at order 8, but fewer order-8 candidates were screened, so
                                                                 the dip measures how much was generated rather than how
                     Results                                     much was there. Normalised to admissible laws per thousand
The portfolio spans eight configurations: Vampire 5.0.1 in       screened candidates, the yield rises across every order the
five modes, E 3.3.5 (Schulz, Cruanes, and Vukmirović 2019)       extension engine produces: 20.5 at order 6, 24.4 at order 7,
in two, and Twee 2.6.1. Table A1 reports how many distinct       and 25.4 at order 8. Order 5 is excluded from the comparison
laws each configuration resolves at each per-configuration       because those laws are ETP’s curated enumeration rather
budget, over the 4,141-law residual. The counts overlap, since   than a uniform draw from the generator, which is why its
several configurations resolve the same law, so the column       density is several times higher.
totals exceed the 114 laws resolved overall.                        Counting only laws that open a new equivalence class
   Two features of the table bear on the main paper’s claims.    gives 16.9, 19.4 and 16.2 per thousand across the same three
First, every configuration concentrates its resolutions at the   orders. That density does not fall, so the corpus continues to
30-second rung; no configuration shows a profile in which        produce genuinely distinct problems rather than variations
added budget yields resolutions at a steady rate. Second, all    on classes it has already covered; unlike the overall yield, it
four models the submitted sweep recovers come from a single      is not monotonic, and we do not claim it is rising.
configuration, twee/complete. The Vampire saturation
modes resolve 14 laws each, all by proving triviality. The            F       Validation of the Automated Judge
construction side of the portfolio therefore rested on one       Both channels of the judge run a control suite before any
configuration.                                                   evaluation. The suites are part of the released code and can
   The sweep exits a law’s ladder as soon as any configura-      be re-run with --selftest.
tion resolves it, so the number of laws reaching each rung
declines: 4,141 at 30 seconds, then 4,050, 4,042, 4,037 and      The trivial channel. A submission is a Lean proof of a
4,033.                                                           proposition the judge generates, and two things must hold:
 1   You are proving a magma law forces triviality. You will NOT write Lean --you
 2   give only a sequence of terms, and a theorem prover checks each step.
 3
 4   Law: {law}
 5   Read it as a rewrite rule. Write the law as L = R, where L is the single
 6   variable on the left and R is the big right-hand term. ONE step does exactly
 7   one of:
 8     •pick any subterm ‘e‘ of the current term and replace that ONE occurrence
 9       with R, taking L := e (so ‘e‘ becomes R with the law’s left variable set
10       to ‘e‘); OR
11     •the reverse --replace a subterm that exactly matches an instance of R by
12       the corresponding ‘e‘.
13   Everything OUTSIDE that one chosen subterm stays byte-for-byte identical.
14
15   Goal: build a = t1 = t2 = ... = b. Adjacent terms should be only a FEW (1-3)
16   such steps apart --you may skip intermediate terms and the checker will fill
17   short gaps automatically, so give WAYPOINTS, not necessarily every atomic
18   step. Prefer smaller jumps.
19
20   HARD RULES --a jump breaking any of these is rejected, so self-check each one
21   before writing it:
22     •You may NOT write "a = b" or otherwise relate a and b directly. They are
23       opaque atoms; the only way to connect them is through the law.
24     •Each jump must be a GENUINE short derivation --at most ~3 single law
25       applications apart. A leap between unrelated terms cannot be bridged and
26       is rejected.
27     •Every application is a REAL instance: a subterm ‘e →R[L:=e]‘ (or its
28       reverse) for some choice of the law’s other variables. If you can’t name
29       that instance, the step is invalid.
30
31   STRATEGY: rewrite FORWARD from ‘a‘ (each rewrite grows the term via the law)
32   toward a term the law forces to collapse --these laws let you derive
33   ‘op(_, _) = (any element)‘; once both ‘a‘ and ‘b‘ reduce to a common term, the
34   chain closes.{hint_block}
35
36   Return ONLY JSON: {"chain": ["a", "<term>", ..., "b"]} first "a", last "b";
37   use only a, b, ⋄, ().
38   Example (toy law x = y ⋄y): {"chain": ["a", "(a ⋄a)", "b"]}
39     step 1: ‘a‘ →‘(a ⋄a)‘ --the law with x:=a, y:=a gives a = a⋄a. ✓
40     step 2: ‘(a ⋄a)‘ →‘b‘ --reverse: the law with x:=b, y:=a gives b = a⋄a,
41       so a⋄a = b. ✓
42   Only write steps you can justify this way.

     Figure A1: The trivial-channel prompt, verbatim. The model returns a chain of terms as JSON; the harness matches each step
     against the law, bridges gaps of at most three single applications, and assembles the Lean proof.


     the proof must elaborate at exactly the generated type, and        answer passes the scan and compiles with an allowed foot-
     its axiom footprint must lie within the allowlist {propext,        print.
     Quot.sound, Classical.choice}. Anything outside
     that set is a failure, and sorryAx, Lean.ofReduceBool              The construction channel. Three controls cover the three
     and Lean.trustCompiler are named explicitly as for-                ways a presentation can fail to encode a construction, match-
     bidden. The footprint is an allowlist rather than a blocklist so   ing the cases discussed in Section 3.3. Submitting the law
     that an unanticipated axiom fails closed.                          itself serves as the positive control: it certifies exactly when
        Seven negative controls exercise the ways a submitter           bare saturation of L ∪ { a ̸= b } terminates, which screening
     could avoid proving anything, and each is rejected by a textual    has already established for the seed law used here. On the
     scan that runs before Lean is invoked, since several of them       hard tier the same submission diverges at check (b), so echo-
     would otherwise subvert Lean itself: a sorry; a declared ax-       ing the law back does not produce a certificate there. The left
     iom asserting the goal; two forms of namespace shadowing;          projection {x ⋄ y = x} is too weak: it admits models with
     redefining the law predicate as True; native_decide;               distinct elements but does not entail the law, so check (a)
     and naming the submitted theorem anything other than the           fails. The collapse {x = y} is too strong: it entails the law
     identifier the judged file elaborates. A positive control con-     but admits only one-element models, so check (b) fails. The
     firms the suite is not simply rejecting everything: a reference    suite passes only when the first certifies and the other two do
 1   You are constructing an infinite model for a magma law, to be checked by an
 2   automated theorem prover.
 3
 4   The law is: {law}
 5   (the binary magma operation is written with the diamond; the law holds for all
 6   inputs.)
 7
 8   This law has NO nontrivial FINITE model, so its model is necessarily infinite,
 9   and it CANNOT be an arithmetic formula (any polynomial op over the integers
10   would descend to a finite model). Instead, propose a finite set of DEFINING
11   EQUATIONS for the operation --a presentation of the model --from which the law
12   follows and which is consistent with the carrier having two distinct elements.
13
14   Think of it as the completed rewrite system a Knuth-Bendix procedure would
15   converge to: a handful of equations that (a) entail the law, and (b) do not
16   force all elements equal.
17
18   Return ONLY a JSON object, nothing else:
19     {"E": ["<equation>", "<equation>", ...]}
20   Each equation uses variables x,y,z,w and the diamond operator, in the form
21   LHS = RHS .
22   Example shape (NOT a solution):
23     {"E": ["x ⋄(y ⋄x) = y", "(x ⋄x) ⋄x = x ⋄x"]}
24   Do NOT just restate the law, and do NOT write ‘x = y‘.

     Figure A2: The construction-channel prompt, verbatim. The model returns a finite presentation E as JSON, which the judge
     submits to the two checks of Equation (6).

                                 Configuration             30   60    120   300   600     Total   Models
                                 twee/complete             69     5     4     3      5      86           4
                                 eprover/triv/auto         64     2     2     1      1      70           0
                                 vampire/triv/casc+lpo     30     1     1     1      0      33           0
                                 vampire/triv/casc         24     1     0     1      0      26           0
                                 vampire/triv/discount     22     0     0     0      0      22           0
                                 vampire/sat/otter+lpo     13     1     0     0      0      14           0
                                 vampire/sat/otter+kbo     12     1     1     0      0      14           0
                                 eprover/sat/satauto        0     0     0     0      0       0           0

     Table A1: Distinct laws resolved by each configuration at each per-configuration budget in seconds, over the 4,141-law residual.
     Counts overlap across configurations. “Models” counts laws resolved by exhibiting a nontrivial model rather than by proving
     triviality.


     LLM        Too strong     Too weak     Both fail    One check          G     Diversity of the Constructed Models
     o3                  23            2           0            25      Section 3.2 reports corpus size in equivalence classes, so
     o4-mini             11            4          10            15      that laws posing the same problem are not counted twice.
     GPT-4.1             10           11           4            21      Logical equivalence is the natural criterion, but it leaves a
                                                                        question open: two laws that are not equivalent may still be
     Table A2: Final-round classification of all 25 hard-tier con-      satisfied by essentially the same construction, in which case
     struction submissions per LLM. “Too strong” entails the law        the class count would overstate how many distinct problems
     but admits only one-element models (passes check (a), fails        the corpus contains.
     (b)); “too weak” maintains two distinct elements but fails to         We test this directly, without a prover, by asking which laws
     entail the law (passes (b), fails (a)). The last column counts     each constructed model satisfies. Every model built during
     laws on which the LLM clears exactly one of the two checks.        screening is evaluated against every one of the 262 laws
                                                                        proved Austin, giving 68,382 ordered pairs and no missing
                                                                        models. A model transfers to a law when it satisfies that law
                                                                        as well as its own.
                                                                           The result is that construction classes and logical classes
                                                                        coincide exactly: both number 195. The pairs on which trans-
     not.                                                               fer runs in both directions number 255, precisely the 255 pairs
      Order     Screened     Austin    Austin per 1,000
           5          115        11                95.7‡
           6        1,418        29                 20.5
           7        4,803       117                 24.4
           8        4,138       105                 25.4

Table A3: Admissible-law yield by order, over all 10,474
screened candidates. Density rises monotonically across the
orders the extension engine generates, so the supply does not
thin as the corpus grows. ‡ Order 5 is excluded from the trend:
those laws come from ETP’s curated enumeration rather than
a uniform draw from the generator.


the prover proved equivalent, so mutual model-satisfaction
and logical equivalence pick out the same relation — a cross-
check on the deduplication of Section 3.2 by a method that
shares none of its machinery. Transfer across class bound-
aries is rare and one-directional: 173 of 68,382 ordered pairs,
or 0.25%. A typical model satisfies only the law it was built      Run                             Records    Completion        Prompt
for, with a median coverage of one law, a mean of 3.67 and         o3 cert-63, waypoints               127      3,094,531       164,044
a maximum of 19. No cell is undecided, and every model             o3 cert-63, no waypoints             99      3,289,573       130,963
satisfies its own law.                                             o3 low effort                         9        152,309        20,724
   The 195 classes are therefore construction-distinct and not     o3 reproduction                      14        575,997        59,653
merely logically distinct. The models do not collapse onto         o4-mini cert-63                      63        974,972       147,300
a shared construction that a solver could learn once and           GPT-4.1 cert-63, waypoints           63         61,670       149,538
reapply.                                                           GPT-4.1 cert-63, no waypoints        63         71,736       139,620
                                                                   GPT-4.1 early run (95 laws)         100        192,466       269,443
    H     Computing Infrastructure and Cost                        GPT-4.1 pilot (10 laws)              10          9,234        31,870
All prover experiments ran on a dual-socket AMD EPYC               o3 trivial, hard-25                  25      1,226,978        53,475
7313 machine — 2 sockets × 16 cores with SMT dis-                  o3 construct, hard-25                25      1,120,628       144,122
abled, giving 32 physical cores — with 503 GB of RAM un-           o4-mini construct                    25        554,835        24,818
der Ubuntu 22.04.5 LTS. The portfolio sweep was sharded            GPT-4.1 construct                    46          6,605        45,755
32 ways, one shard per physical core, so no configuration          Total                               669     11,331,534   1,381,325
competed with a sibling hyperthread for its time budget.
Language-model experiments were run through the Open-              Table A4: Token usage across all reported language-model
Router API.                                                        runs. A solved certified-easy law costs a median of 49,221
   Table A4 reports token usage for every language-model           completion tokens.
run described in the paper. The two certified-easy runs ac-
count for more than half of the total, because each of the 63
laws may consume up to three feedback rounds and because
reasoning traces on that set are long: a solved law costs a me-
dian of 49,221 completion tokens. The construction runs are
cheaper per law despite resolving nothing, since a presenta-
tion is a short object to emit. GPT-4.1’s totals are an order of
magnitude below the reasoning models’ at comparable call
counts, which reflects the absence of a reasoning trace rather
than a shorter answer.
   Files with more than 63 records contain repeated passes
under identical settings, appended in run order. The no-
waypoint o3 file holds a first pass over all 63 laws, on which
four chains certify, followed by a second pass over the 36 laws
then unsolved, which adds two more; the six no-waypoint
solutions reported in the main text are the union of the two
passes. The waypoint o3 file holds a first pass over all 63
laws, on which nine chains certify, followed by two further
passes over 32 of the unsolved laws, which add none. The
reproduction run is a separate file.
