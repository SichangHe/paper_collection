                                                  LLM-Assisted Automatic Security Proofs for
                                                  Cryptographic Protocols: How Far Are We?
                                          Tianjian Liu∗∥ , Shicheng Feng† , Jin’ao Shang∗ , Xiaoting Lyu∗ , Bin Wang‡ , Zonghua Zhang§ , Lei Xue¶∥ *, Wei Wang∗ *
                                                                                            ∗ Xi’an Jiaotong University, Xi’an, China

                                                                       {tianjian.liu, jinao s}@stu.xjtu.edu.cn, {xiaoting.lyu, wei.wang}@xjtu.edu.cn
                                                                                                † Tianjin University, Tianjin, China

                                                                                                     fengshicheng@tju.edu.cn
                                                             ‡ Zhejiang Key Laboratory of Artificial Intelligence of Things (AIoT) Network and Data Security

                                                                                                    wangbin02@xidian.edu.cn
                                                                                      § CRSC Research & Design Institute Group Co., Ltd
arXiv:2609.35434v1 [cs.CR] 28 Sep 2026




                                                                                                   zhangzonghua@crscd.com.cn
                                                                                           ¶ Sun Yat-sen University, Guangzhou, China

                                                                                                     xuelei3@mail.sysu.edu.cn
                                                                                        ∥ Shenzhen Loop Area Institute, Shenzhen, China

                                                                                        *Corresponding authors: Lei Xue and Wei Wang.


                                            Abstract—Large language models (LLMs) have shown strong               However, as shown in Figure 1, completing a protocol
                                         potential for assisting software and security analysis tasks, yet     verification typically involves (Step 1) formalizing the cryp-
                                         their effectiveness in cryptographic symbolic protocol verification   tographic protocol, (Step 2) defining security properties, and
                                         remains insufficiently understood.
                                                                                                               (Step 3) analyzing counterexample traces [4]. This process still
                                            In this paper, we conduct the first systematic evaluation of the
                                         capability of state-of-the-art LLMs in cryptographic symbolic         requires substantial expert knowledge and manual effort [2],
                                         protocol verification. To quantify this capability, we propose        [5]–[7]. As reported by the Galois team [8], formally verifying
                                         CRO ST (Coverage Rate of Solve Tree), a proof-based metric            the AES-256-GCM and SHA-384 implementations in AWS
                                         derived from the verifier’s proof skeleton that measures the          LibCrypto required approximately nine person-months of work
                                         similarity between generated lemmas and reference lemmas. We
                                                                                                               by experienced proof engineers.
                                         then establish the rationale of CRO ST through both theoretical
                                         analysis and empirical validation. The evaluation results show
                                         that state-of-the-art models achieve 38.82% coverage on average,            symbolic model                           verified      step 3
                                         with 14.4% of generated lemmas exceeding 80% coverage, indi-             step 1                                                      analyze
                                         cating that LLMs can already generate useful lemmas to a certain           Protocol System                                            proof
                                         extent. However, they still exhibit non-trivial failure modes on                                                     falsified        traces
                                         complex multi-phase protocols, show diminishing returns under                     ?
                                         naive scaling, and incur substantial verification overhead. These                                  formal
                                                                                                                  step 2
                                         findings clarify the practical potential and limitations of LLMs
                                                                                                                  Security Property       verification        timeout
                                         for protocol verification and motivate future work on complex                                       tools
                                         real-world protocols.
                                            Index Terms—LLM, Formal verification, Cryptographic pro-                        Fig. 1. Symbolic model verification pipeline.
                                         tocol, Symbolic model
                                                                                                                  Recent advances in LLMs [9]–[13] suggest a possible
                                                                                                               route for automatically extracting unambiguous and analyz-
                                                                I. I NTRODUCTION                               able specifications, thereby lowering the barrier to applying
                                                                                                               formal methods. Prior work on combining LLMs with sym-
                                            Cryptographic protocols are designed to coordinate security-       bolic model verification tools for cryptographic protocols has
                                         critical interactions and achieve security goals such as se-          mainly studied the translation of natural-language protocol
                                         crecy and authentication. In symbolic models, these goals             descriptions into tool-checkable symbolic models (Step 1)
                                         are formalized as security properties over protocol executions,       [14]. However, the complementary task of specifying security
                                         enabling verification tools to reason about whether an active         properties (Step 2) remains largely manual. Symbolic verifiers
                                         adversary can break them. This style of analysis has proved           require explicit security goals as input, and these goals must be
                                         practically valuable by exposing subtle flaws in widely de-           written as tool-checkable lemmas. Writing and refining such
                                         ployed or standardized protocols, e.g., PCS violations enabled        lemmas requires expert knowledge; it also determines what the
                                         by Signal’s session handling layer [1], multiple confirmed            verifier actually checks and how difficult the subsequent proof
                                         vulnerabilities in Apple/Samsung proximity tracking protocols         search becomes [15]–[18]. We therefore focus on security-
                                         [2], and critical attacks on the EMV payment standard [3].            property specification for already available protocol models,
and study whether LLMs can generate tool-checkable security          symbolic inference rules derived from the algebraic properties
properties in Cryptographic Symbolic Protocol Verification           of cryptographic operators [21].
(CSPV) (Step 2).
                                                                     B. Security Properties
   To answer this question, this paper presents a systematic
empirical study that focuses on two research questions:                 Cryptographic protocols are intended to guarantee security
                                                                     properties such as secrecy, authentication, and sanity. Secrecy
   • What are the capability boundaries of LLMs for
                                                                     captures scenarios in which sensitive data, such as session
      security-property generation in CSPV?
                                                                     keys or private messages, should remain unavailable to the
   • How do LLMs perform across different task types in
                                                                     adversary [16], [22]. Authentication captures scenarios in
      CSPV?
                                                                     which one party’s acceptance should correspond to a genuine
   There are two challenges in answering the above questions.        prior action of its intended peer, rather than to an adversarial
   First, due to the diversity of representations (We will give an   forgery or replay [16], [18], [23]. In protocol analysis, sanity
example in Section III-A) for the same security property, it is      is often used as a basic executability or consistency property,
difficult to measure the similarity between a generated security     checking that the modeled protocol can complete an intended
property and a target correct security property using simple         interaction and that security claims do not hold only vacuously
text-based comparison. To capture deeper features of security        [16].
properties in the verification process, we introduce a proof-
based metric derived from Tamarin’s proof skeleton, which            C. Tamarin Prover
reflects security properties feature at the proof-search layer          In the symbolic verification tool Tamarin Prover [24], [25],
[15], [16]. We further justify the rationale and effectiveness       protocols are specified using multiset rewriting rules of the
of this metric through theoretical analysis and mutation-based       form: [lhs] − [ActionFacts] → [rhs]
empirical validation.                                                   Where lhs and rhs are multisets of facts representing the
   Second, symbolic protocol verification tools such as              current protocol state. A rule can fire when the facts in lhs are
Tamarin use domain-specific specification languages to de-           available; firing the rule consumes the facts on the left and
scribe protocols and their security properties. In such lan-         produces the facts on the right. The bracketed ActionFacts on
guages, security properties often involve temporal semantics,        the arrow are not part of the state; instead, they are recorded
deeply nested logical structures, and protocol-specific con-         as observable events on the execution trace and form the basis
straints. These characteristics make it difficult for LLMs to        for specifying security properties as lemmas. In Figure 2,
generate syntactically correct security properties, even when        the rule Reveal_ltk models long-term key compromise: it
the intended property is conceptually simple [19]. In this work,     reuses a persistent key fact !Ltk(A,ltk), emits the event
we therefore investigate the effect of few-shot prompting on         LtkReveal(A), and outputs the leaked key via Out(ltk).
LLM-based security property generation and evaluate whether
lightweight in-context examples can improve syntactic validity       rule Reveal_ltk:
                                                                       [ !Ltk(A,ltk) ]     // storing long-term key.
and downstream verification performance.                               --[ LtkReveal(A) ]->// Record the reveal event.
   In summary, our contributions are as follows:                       [ Out(ltk) ]        // Output the leaked key.

   • We present the first systematic empirical study of LLM                            Fig. 2. Rewriting rule example.
      capability in CSPV tasks of secrecy, authentication, and          Security properties in Tamarin are expressed as lemmas
      sanity. Our evaluation shows that LLMs exhibit stronger        (Figure 3), which are first-order logic (FOL) with quantifi-
      performance on existential propositions.                       cation over timepoints. Lemmas may quantify universally
   • We propose a solve-level coverage metric named CRoST
                                                                     or existentially over timepoints and action facts, allowing
      (Coverage Rate of Solve Tree) for quantifying security         the specification of both safety and reachability properties.
      properties similarity, and validate its rationality through    Tamarin distinguishes between all-traces lemmas, which
      both theoretical analysis and mutation-based evaluation.       must hold for all possible executions, and exists-trace
   • We unveil the main limitations and failure modes of
                                                                     lemmas, which assert the existence of a witness trace [16].
      mainstream LLMs when they are applied in CSPV tasks.              In this work, we instantiate our evaluation on Tamarin as
      We show that stage-point confusion in complex multi-           the target symbolic verifier for two reasons.
      phase protocols and substantial time overhead are two             First, among symbolic protocol verification tools, Tamarin
      major bottlenecks for using LLMs in CSPV.                      offers particularly strong modeling expressiveness and proof
                      II. BACKGROUND                                 support. It can handle rich equational theories, mutable state,
                                                                     and provides both automatic and interactive proof modes,
A. Symbolic Model                                                    which is important for complex, real-world protocol models
   Symbolic verification [20] of cryptographic protocols is          [26]. Second, Tamarin integrates the SAPIC+ process calcu-
conducted under the Dolev-Yao adversary model. In this               lus [27], a cross-tool modeling layer that can translate SAPIC+
adversary model, cryptographic primitives are treated as ideal       specifications to Tamarin, ProVerif, and DeepSec. This allows
black boxes, and the adversary is allowed to intercept, replay,      protocol models developed in a multi-verifier workflow to be
modify, and inject messages arbitrarily, while being limited to      instantiated as Tamarin theories for our evaluation.
                        III. M ETHODOLOGY                                    exercise a graph-structured behavior space [31]–[33]. From
                                                                             a software testing perspective, a useful coverage criterion
A. Motivation
                                                                             should be measurable, reliable, and predictive. Motivated by
   In this section, we assess how closely LLM-generated                      this principle, we design CRoST as a proof-based coverage
lemmas align with expert-written lemmas in expressing the                    metric over Tamarin proof skeletons.
intended security properties of a protocol. Our benchmark                       Algorithm 1 computes CRO ST in three steps. Lines 1-10
provides, for each protocol theory, a reference lemma set                    define the procedure ExtractPaths, which traverses a proof tree
written by human experts, which we treat as the target spec-                 and records every path. Lines 12-17 apply this procedure to
ification. Based on this comparison, we first derive a metric                all target and generated proof trees to build the path sets P ⋆
CRoST from empirical observations about proof behavior and                   and P . Lines 19-23 then compare each target path against the
generation difficulty, and then justify its rationale in subsection          generated paths and mark it as covered when a match is found.
III-B.                                                                       Finally, Lines 24-27 return the coverage ratio.
   To derive the metric, a key difficulty is that a Tamarin lemma
is a quantified temporal FOL formula over action facts and                     Algorithm 1: CRoST: Coverage Rate of Solve Tree.
their ordering on traces [16], [19]. There is rarely a canonical                Input: Target proof trees T ⋆ , generated proof trees T
lemma form for a given security property: One security                          Output: CRoST score c ∈ [0, 1]
property can be expressed in various forms. For example,                      1 Function ExtractPaths(node, pref ix):
Figure 3 shows that the same secrecy property definition can                  2    P ←∅
be written either as a single overall lemma Secrecy, or                       3    if node is a solve node then
equivalently split into two lemmas Secrecy_split_A and                        4        pref ix′ ← pref ix ∥ ⟨label(node)⟩
Secrecy_split_B that branch on role-specific reveal con-                      5        P ← P ∪ {pref ix′ }
ditions. This poses a challenge for lemma evaluation metrics.                 6    else
                                                                              7        pref ix′ ← pref ix
// Same secrecy property, written in two forms.                               8      foreach child ∈ Children(node) do
lemma Secrecy:
  "All A B m #i.                                                              9          P ← P ∪ ExtractPaths(child, pref ix′ )
     Secret(A,B,m)@#i
     ==> not (Ex #r. K(m)@#r)                                                10      return P
       | (Ex #r. Reveal(A)@#r)
       | (Ex #r. Reveal(B)@#r)"                                              11   P ⋆ ← ∅, P ← ∅
lemma Secrecy_split_A:                                                            // Extract all root-to-solve paths from target lemmas.
  "All A B m #i.                                                             12 foreach tree ∈ T ⋆ do
     Secret(A,B,m)@#i
     & not(Ex #r. Reveal(A)@#r)                                              13     foreach root ∈ Roots(tree) do
     ==> not (Ex #r. K(m)@#r)                                                14         P ⋆ ← P ⋆ ∪ ExtractPaths(root, ⟨ ⟩)
       | (Ex #r. Reveal(B)@#r)"

lemma Secrecy_split_B:                                                            // Extract all root-to-solve paths from generated lemmas.
  "All A B m #i.                                                             15 foreach tree ∈ T do
     Secret(A,B,m)@#i
     & not(Ex #r. Reveal(B)@#r)                                              16     foreach root ∈ Roots(tree) do
     ==> not (Ex #r. K(m)@#r)                                                17         P ← P ∪ ExtractPaths(root, ⟨ ⟩)
       | (Ex #r. Reveal(A)@#r)"
 Fig. 3. Alternative Tamarin specifications for the same secrecy property.   18   covered ← ∅
                                                                                  // Compute covered target paths using subsequence matching
   Text-level similarity metrics such as BLEU [28] are not                         (p ⪯ q).
reliable signals for whether two lemma sets define the same                  19 foreach p ∈ P ⋆ do
security property; metrics based on matching are known to                    20     foreach q ∈ P do
correlate poorly with semantic or functional correctness in                  21         if p ⪯ q then
other generation settings [29]. A seemingly stronger alternative             22             covered ← covered ∪ {p}
is to compare FOL components via truth tables [30]. However,                 23             break
Tamarin lemmas involve quantification over events and time-
points. Truth-table comparison is not applicable in general.                 24 if |P ⋆ | = 0 then
   We therefore adopt a proof-based comparison based on                      25     return c ← 0
Tamarin’s proof artifacts. Given a protocol and a lemma,                     26 else
Tamarin’s automated proof search produces a proof skele-
                                                                             27     return c ← |covered|
                                                                                                   |P ⋆ |
ton (Figure 4) that explicitly records the encountered
solve(...) goals and case distinctions [16] as tree struc-
ture. Intuitively, these solve obligations reflect which parts                  Prior work has shown that proof-based coverage metrics
of the verifier’s reasoning space are exercised by a lemma                   can serve as a practical alternative to mutation-based coverage
specification. This is similar to proof-based criteria in software           in formal verification, while yielding meaningful information
testing, where coverage quantifies how thoroughly executions                 about specification adequacy [31]. In the symbolic verification
of cryptographic protocols scenario, we go one step further by     lift the solve footprint from individual lemmas to the lemma-set
studying whether coverage also correlates with the similarity      level by union:                 [
between generated lemmas and target lemmas.                                               S(L) :=         S(L) ⊆ U.                  (3)
      Goal and proof idea: Our goal is to evaluate an LLM-                                          L∈L
                                                                     Given a target lemma set L⋆ and a candidate generated
generated lemma set by how effectively it reproduces the proof     lemma set L, let
obligations required to establish a target security property               S ⋆ := S(L⋆ ),         S := S(L),       H := S ∩ S ⋆ .    (4)
in Tamarin. We use solve-level coverage to measure how             We write
much of the target lemma’s proof skeleton is covered by the                              n := |S ⋆ |,      k := |H|.                 (5)
generated lemma. In the following, we formalize (i) capability     The solve-level coverage is defined as
as covering a minimal sufficient set of solve obligations,                                    |S(L) ∩ S(L⋆ )|  k
                                                                          Cover(L; L⋆ ) :=                    = = c ∈ [0, 1].        (6)
i.e., a minimal generator of the sufficient-set family, and (ii)                                 |S(L⋆ )|      n
how increasing coverage raises the probability of covering at      Definition 3 (Minimal generators of the sufficient-set family).
least one such minimal generator. We further quantify this         Under fixed P, κ, let F ⊆ 2U be the upward-closed family of
relationship under a simple random-overlap model.                  solve-item sets sufficient for the target outcome. The minimal
                                                                   generators of F are the inclusion-minimal elements of F :
B. Definitions and Assumptions                                                Min(F) := { C ∈ F | ∄C ′ ⊊ C : C ′ ∈ F }.              (7)
     Tool-grounded observables under a fixed proving con-           We write Min(F ) = {C1 , . . . , CM }. Equivalently, for any
figuration: We fix a protocol theory P and a proving con-          X ⊆ U,
figuration κ (Tamarin version, command-line flags, heuristic                 X∈F         ⇐⇒       ∃j ∈ {1, . . . , M } : Cj ⊆ X.     (8)
rules, and resource bounds). For any lemma L, let Skel(L) :=         Each Cj represents a minimal sufficient set of normalized
Autoprove(P, L; κ) denote the proof skeleton produced by           solve-items for the target outcome, i.e., no proper subset of Cj
Tamarin under κ. We view Skel(L) as a finite rooted structure      is sufficient. Typically |Cj | > 1 for all-traces properties, while
whose nodes include solve(c) goals and whose edges reflect         exists-trace properties may admit |Cj | = 1. Figure 4 contrasts
explicit case distinctions in the skeleton output.                 two typical skeleton shapes: exists-trace lemmas succeed by
Definition 1 (Atomic solve-item and solve footprint). Each         finding one witness branch, whereas all-traces lemmas require
solve(c) node contains a goal/constraint term c. We apply          discharging all case splits.
a normalization function Norm(·) that (i) α-renames bound
variables, (ii) erases proof-local indices/counters, and (iii)     Definition 4 (Capability of a lemma generator). Let G be a
canonicalizes commutative constructs. A normalized atomic          lemma generator pipeline. Given a protocol context, G induces
solve-item is u := Norm(c). Let U be the finite universe of        a distribution over finite lemma sets. The generation capability
normalized solve-items observed under the fixed configuration      of G is the probability that the generated lemma set covers at
κ. The solve footprint of lemma L is                               least one minimal generator:          
 S(L) := { Norm(c) ∈ U | solve(c) occurs in Skel(L) } ⊆ U.               Ability(G; F) := Pr S(L) ∈ F
                                                                                         L∼G
                                                         (1)                                                                       (9)
                                                                                       = Pr ∃j ∈ {1, . . . , M } : Cj ⊆ S(L) .
     Proof-skeleton order over solve occurrences: After nor-                                L∼G

malization, each solve(c) node is labeled by an atomic               L ∼ G means L is sampled from distribution induced by G.
solve-item u = Norm(c). For x, y ∈ U, define
          x ⪯κ y   iff   x = y or x is a descendant of y     (2)        Sanity check: If Cover(L; L⋆ ) = 1, then by definition
                                                                       ⋆
                                                                   S(L ) ⊆ S(L). If the target lemma set is sufficient, i.e.,
 This relation captures the solve-reduction structure induced
                                                                   S(L⋆ ) ∈ F, then there exists some minimal generator Cj ⊆
by the proof tree: a node is below another precisely when it
                                                                   S(L⋆ ). Consequently, Cj ⊆ S(L), which implies S(L) ∈ F .
arises from reducing subgoals generated by it.
      Deterministic proof search policy: Under fixed κ,                 (C) A tractable random model: To quantitatively relate
Tamarin’s automated proof search uses a fixed heuristic rank-      solve-level coverage to generation capability, we adopt a
ing to prioritize open constraints and proof methods. Oper-        simplified conditional random model.
ationally, we treat Skel(L) as the deterministic unfolding of      Assumption 1 (Random overlap conditional on coverage). Fix
the proof-search policy induced by κ, yielding a reproducible      a target lemma set L⋆ . In practice, the generated footprint
solve/case structure for a given (P, L).                           S(L) may be correlated with S(L⋆ ) because both are induced
      (B) Lemma-set abstraction for security properties: In        by the same protocol theory and proving configuration. For a
practice, a target security property may be specified by a         tractable analysis, however, we do not assume any favorable
set of Tamarin lemmas rather than a single canonical lemma.        target-specific alignment. Conditioned only on the overlap size
Likewise, an LLM may generate multiple lemmas that jointly         |H| = k, we model H as a uniformly random k-subset of
describe parts of the same intended property. Therefore, we        S(L⋆ ), sampled without replacement.
treat a lemma set as the unit of comparison: multiple lemmas
are abstracted into a property-level solve footprint, obtained
by aggregating their normalized solve footprints.                  C. Predecessor Hits and Minimal-Generator Continuation
Definition 2 (solve-level coverage). For a finite lemma set L           Minimal-generator elements: For each Cj ∈ Min(F), let
under the same protocol P and proving configuration κ, we               Cj = {uj,1 , uj,2 , . . . , uj,mj } ⊆ U,    mj := |Cj |.    (10)
           (a) exists-trace: one successful branch suffices.                             (b) all-traces: all branches must be discharged.
                               Fig. 4. Contrasting proof skeleton for exists-trace vs all-traces lemmas in Tamarin.



    Predecessor sets: Using the proof-skeleton order ⪯κ , for               be the set of solve-items that form singleton minimal gen-
each uj,k ∈ Cj let its target-derived predecessor set be                   erators. For example, Figure 5 illustrates the case where one
        Predκ (uj,k ) := { g ∈ S ⋆ | uj,k ⪯κ g, g ̸= uj,k }.       (11)    such generator is C1 = {u1 }.
 Intuitively, Predκ (uj,k ) contains target solve-items whose
reduction can lead to the solve obligation uj,k .                                    Predκ(u1)={solve(b), solve(c),                             solve(g)
                                                                                          solve(d), solve(e)}
Definition 5 (Predecessor-hit event). For a generated lemma
                                                                                                                                     predecessor hit
set L, let                                                                                       solve(d)      solve(e)

           Hitj,k (L) = 1    iff   H ∩ Predκ (uj,k ) ̸= ∅.         (12)
 That is, the generated lemma set hits at least one target
predecessor of the minimal-generator element uj,k .                                                     solve(b)          solve(c)
                                                                                                                                                possible proof paths

Estimation 1 (Predecessor-to-minimal-generator continuation                                                                                     proof skeleton paths

probability). For each (j,
                       h k), let
                                                                                      C1={solve(a)}
                                                                                                                                                  prove path:
                                             i                                                                 u1=solve(a)              1. solve(d) - solve(b) - solve(a)
            ρj,k := Pr Cj ⊆ H           Hitj,k (L) = 1 .           (13)                                                                 2. solve(e) - solve(b) - solve(a)
                    L∼G                                                                                                                 3. solve(g) - solve(c) - solve(a)

  In our experiments under a fixed κ, we estimate ρj,k from
                                                                           Fig. 5. Exists-trace witness shape with a singleton minimal generator.
repeated runs of G; for example, the average continuation                  The minimal generator is C1 = {solve(a)}; reaching this solve-item along
probability is ρb ≈ 0.513, i.e., conditioned on a predecessor              one witness branch suffices to establish the target outcome.
hit, the full minimal generator is covered about 51.2% of the
time.                                                                      Lemma 1 (Capability equals hitting a singleton minimal
                                                                           generator). In the singleton exists-trace setting, the
      Empirical predecessor-to-generator continuation proba-               capability of G is
bility: A predecessor hit does not fix the remaining proof-                                                           
                                                                                        Ability(G; F) = Pr ∃u ∈ W : u ∈ S(L) .                                              (15)
                                                                                                                          L∼G
search trajectory: the subsequent goal ordering and case splits
may still diverge from the target skeleton. Therefore, even                Lemma 2 (Closed-form capability from coverage in the
under a fixed configuration κ, hitting a predecessor does not              singleton exists-trace case). Define the direct-hit event
guarantee covering the whole minimal generator. The central                                                    A := { H ∩ W ̸= ∅ },                                         (16)
problem in this proof model can be viewed as analogous to                    i.e., the generated footprint directly covers at least one
probabilistic reachability in uncertain graphs [34]: a predeces-           singleton minimal-generator element.
sor hit indicates a possible support path, while ρ estimates the               Under Assumption 1, with k treated as a fixed overlap size,
probability that this path continues to full minimal-generator             we write Prk [·] for the probability induced by drawing H
coverage.                                                                  uniformly from all k-subsets of S ⋆ . Let r := |W |. Then
                                                                                                                                     n−r
                                                                                                                                      k
                                                                                                                Pr[A] = 1 −           n        .                            (17)
D. Exists-trace Situation
                                                                                                                                        
                                                                                                                   k
                                                                                                                                      k
  We first focus on the simplest exists-trace situation,                     Let ρb denote the empirical continuation probability that,
where the target outcome can be witnessed by reaching one                  when no singleton minimal-generator element is directly hit,
solve-item from a singleton minimal generator. Let                         predecessor-supported proof search still continues to full
                W := { u ∈ U | {u} ∈ Min(F) }                      (14)    minimal-generator coverage under fixed configuration κ. Then
the success probability is modeled as                                           A computable lower bound for Pr[Ej ] under random
          Ability(G; F) = Pr[A] + 1 − Pr[A] ρb                              overlap: Under Assumption 1, H is a uniformly random k-
                             k                 k
                                                     n−r
                                                            !
                                                                     (18)   subset of S ⋆ . For each element, define the miss event
                                                      k
                          = ρb + (1 − ρb) 1 −
                                                                                         T Fj,t := { H ∩ Xj,t = ∅ S    }.
                                                      n
                                                                .
                                                      k                     Then Ej = t ¬Fj,t and hence ¬Ej = t Fj,t . By a union
For the special case r = 1, this reduces to                                 bound,
                 Ability(G; F) = ρb + (1 − ρb) c.                    (19)                                             mj
                                                                                                                      X
                                                                                                 Pr[Ej ] ≥ 1 −              Pr[Fj,t ].               (22)
Interpretation. In the singleton exists-trace setting,                                                                t=1
directly covering any singleton minimal-generator element is                 Moreover, each miss probability has a hypergeometric closed
sufficient for success. If the generated footprint instead only             form:                           n−s
                                                                                                                             j,t
reaches predecessor-supported items, ρb models the probability                                        Pr[Fj,t ] =           k
                                                                                                                            n
                                                                                                                                   ,                (23)
that this support continues to full minimal-generator coverage.                                                 a
                                                                                                                           k

When there is only one singleton minimal generator, capability               with the convention that           k     = 0 if a < k. Plugging (23)
                                                                            into (22) yields
increases linearly with coverage c.                                                                                   mj      n−sj,t
                                                                                                                                        
                                                                                                                      X
                                                                                                                                k
                                                                                                 Pr[Ej ] ≥ 1 −                  n
                                                                                                                                           .        (24)
E. All-traces situation                                                                                               t=1       k
                                                                                Coverage-to-capability relation: Combining Lemma 3
   We now consider the typical all-traces situation, where                  and (24), and substituting k = cn, we obtain the following
the target outcome may admit multiple minimal generators and                monotone lower bound: (                      !)  mj        n−sj,t
each minimal generator may contain multiple solve-items.                                                                      X
                                                                                                                                         c·n
                                                                                  Ability(G; F) ≥ max          ρj      1−                 n
                                                                                                                                                .   (25)
      Mixed direct hits and predecessor hits: For each element                                       j∈[M ]
                                                                                                                              t=1        c·n
uj,t ∈ Cj , define its support set as                                       Interpretation. The lower bound is monotone in the solve-
    Xj,t := {uj,t } ∪ Predκ (uj,t ) ⊆ S ⋆ ,   sj,t := |Xj,t |.              level coverage c = Cover(L; L⋆ ). However, the support-set
We say that uj,t is supported by the generated footprint if                 sizes sj,t depend on the target proof-skeleton structure, so
H hits either the element itself or one of its target-derived               the bound cannot in general be reduced to a closed-form
predecessors:                                                               expression purely in terms of c.
                                                                               When analyzing protocol-level coverage over a large lemma
                   Ej,t := { H ∩ Xj,t ̸= ∅ }.                               set, it is natural to have n = |S ⋆ | ≫ sj,t . In this regime, with
Accordingly, a minimal generator Cj is predecessor-supported                k = cn, the combinatorial    term admits the approximation
                                                                                            n−sj,t                    sj,t
                                                                                                  
if all of its elements are supported:
                                                                                                          
                                                                                                                 k
                                mj
                                                                                              k
                                                                                              n
                                                                                                     ≈       1−              = (1 − c)sj,t .        (26)
                                \
                                                                                              k
                                                                                                                 n
                         Ej :=      Ej,t .                                   Substituting (26) into Eq. (25) yields the following coverage-
                                  t=1                                       driven shape:
This definition allows mixed evidence: some elements of Cj                                            (                  mj
                                                                                                                         X
                                                                                                                              !)
may be directly covered by H, while others may only be                           Ability(G; F) ≳ max           ρj     1−    (1 − c)sj,t          .   (27)
                                                                                                     j∈[M ]
supported through predecessor hits.                                                                                           t=1
     Continuation probability for an all-traces minimal gener-               This approximation suggests that capability increases with
ator: Even when Ej holds, the remaining proof-search trajec-                coverage in a concave manner through the terms 1−(1−c)sj,t ,
tory may still diverge from the target skeleton. We therefore               and that larger support sets lead to a faster rise as c increases.
define a minimal-generator-level  continuation  probability:
                                                                                                      IV. E XPERIMENT
                       h                 i
             ρj := Pr Cj ⊆ S(L)           Ej       ∈ [0, 1].         (20)
                   L∼G
                                                                            A. Dataset
Lemma 3 (Capability lower bound via predecessor-supported
                                                                               Our dataset is derived from AUTO SM1 [14], which include
minimal generators). For any j ∈ {1, . . . , M },
                                                                        18 protocols and 90 human-expert-written lemmas from dif-
    Ability(G; F) ≥ Pr Cj ⊆ S(L) ≥ ρj · Pr Ej .                             ferent cryptography scenarios. We have added 54 mutation
                     L∼G                                 L∼G
Consequently,                                                               protocols based on this dataset, which will be explained further
                                                                            in section IV-B.
                                       
           Ability(G; F) ≥ max ρj · Pr Ej .
                                 j∈[M ]    L∼G
                                                                               For each protocol theory P , the dataset includes a reference
Proof. The first inequality holds because                                   lemma set that specifies intended security properties. The
         Ability(G; F) = Pr ∃j ′ : Cj ′ ⊆ S(L) ,                            properties can be classified by secrecy, authentication, and
                                             
                             L∼G                                            sanity.
which dominates any fixed witness j. For the second inequal-
ity, write                                                                  B. Results
     Pr[Cj ⊆ S(L)] = Pr[Cj ⊆ S(L) | Ej ] Pr[Ej ]
                                                                               To answer the two research questions raised in the intro-
                     + Pr[Cj ⊆ S(L) | ¬Ej ] Pr[¬Ej ]                 (21)   duction (section I), we organize the evaluation around the
                   ≥ ρj Pr[Ej ],                                            following five sub-questions.
 using the definition of ρj in (20) and non-negativity of
probabilities.                                                                1 https://github.com/zerrymore/AutoSM
   RQ1. How well do LLMs produce syntactically valid spec-                                                 TABLE I
ifications in CSPV?                                                                            S YNTAX S UCCESS R ATE BY M ODEL .
   RQ2. How effective is CRoST as an evaluation metric?                  Model                              Generated Syntax Success Rate (%)
   RQ3. What are the capability boundaries of LLMs in                    grok-4                                   75                         74                      98.67
CSPV?                                                                    claude-sonnet-4.5                       245                        241                      98.37
   RQ4. How do LLMs perform across different task types in               gpt-5.2-codex                           118                        114                      96.61
CSPV?                                                                    claude-opus-4.5                         166                        155                      93.37
   RQ5. What is the computational cost of using LLMs in                  gemini-3-flash-preview                  95                         86                       90.53
                                                                         gpt-5.2                                 204                        169                      82.84
CSPV?                                                                    claude-haiku-4.5                        290                        230                      79.31
                                                                         qwen-plus                                78                         57                      73.08
   RQ1. How well do LLMs produce syntactically valid                     deepseek-v3.2                           230                        166                      72.17
   specifications in CSPV?                                               gpt-4                                    74                         46                      62.16
                                                                         qwen3.5-plus                            218                        135                      61.93
                                                                         qwen3-coder-plus                        139                         82                      58.99
   Since Tamarin uses a domain-specific specification language
rather than a general-purpose programming language such as               Since real-world cryptographic protocol vulnerabilities are
Python, C, or Java, publicly available examples are relatively        scarce, we adopt mutation testing to assess whether CRO ST
limited [15], [16], [35], [36]. In practice, this challenge of-       is a rational metric [40]. Specifically, we inject a suite of
ten appears first at the syntactic level. LLMs may fail to            simple, explicit flaws into protocol rules (Table II), generated
produce lemma specifications that are well-formed and tool-           with Gemini-3-Pro and manually vetted by human experts.
checkable [19]. We therefore begin by investigating whether           These vulnerabilities are designed as controlled, verification-
LLMs can reliably produce usable lemma specifications, and            relevant fault proxies. Since security properties characterize
whether few-shot prompting (in-context learning) [37], [38]           the intended security behavior of a protocol, any vulnerability
can improve syntactic validity and downstream verification            should violate at least one of them. Therefore, if a lemma
performance by providing a small number of demonstrations             captures the target property well, a local perturbation that
in the form of multiset rewriting rules with 1–4 corresponding        breaks that property should cause the verification result to flip,
lemmas.                                                               allowing us to test whether CRO ST responds appropriately
   We start with a comparison between zero-shot and few-shot          to property-breaking changes. As illustrated in Figure 7, if a
prompting on the same set of rule inputs. The syntax success          lemma is verified on the original protocol but becomes falsified
means that the generated lemmas can be parsed and compiled            on a mutant, we treat the injected vulnerability as detected by
by Tamarin without syntax errors. Figure 6 shows the results          that lemma. We then use the resulting flip rate over mutants
for qwen3-coder-plus. Compared with zero-shot prompting,              to assess the validity of CRO ST.
few-shot prompting improves the syntax success rate by 30.4              What needs to be explained here is mutation testing itself
percentage points. This indicates that few-shot prompting can         can serve as an indicator of lemma-generation capability, but it
significantly improve the syntax success rate.                        has practical limitations [41], [42]. Constructing protocol flaws
                                                                      requires substantial manual effort, and real-world vulnerabili-
                                                                      ties are often covert, making handcrafted mutants unlikely to
                                                                      cover the full spectrum of lemma capability. Moreover, flip-
                                                                      based outcomes provide limited visibility into the verifier’s
                                                                      fine-grained proof search behavior. Therefore, we use mutation
                                                                      testing here only as supporting evidence for the rationality of
Fig. 6. Zero-shot vs. few-shot syntax success for qwen3-coder-plus.   CRO ST, rather than as our primary evaluation metric [43].

   Table I summarizes the syntax success rates across models;                                                                                             Generated
                                                                                                                                                       Security Property
                                                                                           Vulnerability     Mutation                                                        flip !
the majority exceed 70% under few-shot prompting, providing            Protocol Rules
                                                                                            injection      Protocol Rules                               lemma A: verified
                                                                                                                                                        lemma B: falsified
a necessary foundation for the later evaluation that focuses on                                                                            Re-verify
                                                                         Generated                                                                        Generated
proof-search behavior and security property coverage rather           Security Property
                                                                                                                              Formal
                                                                                                                            verification               Security Property
than surface syntax. In all subsequent experiments, we use             lemma A: verified
                                                                       lemma B: verified
                                                                                                                                                        lemma A: verified
                                                                                                                                                        lemma B: verified

few-shot prompting as the default generation setting.
                                                                                           Fig. 7. Mutation test experiment sketch.

   RQ2. How effective is CRoST as an evaluation metric?                 We tested lemmas generated by current state-of-the-art
                                                                      (SOTA) LLMs. Figure 8 shows a strong positive correlation
  In section III, we prove the relationship between CRoST             between CRoST coverage and flip rate (correlation coefficient
and security properties similarity. Furthermore, we designed          = 0.75, p-value = 0.005). This evidence supports the validity
mutation experiments [39] to further prove the rationality of         of CRoST as a fine-grained, tool-grounded indicator for how
CRoST.                                                                well generated lemmas capture security properties.
                            TABLE II
   S IMPLE MODIFICATIONS TO CONSTRUCT VULNERABLE PROTOCOL
                           VARIANTS .

Type                   Operation description
Direct leakage       Add Out(...) to directly release a secret
                     value.
Weak key derivation Modify key-derivation inputs to include pub-
                     lic constants, making the derived key pre-
                     dictable/computable by the adversary.
Removed              Delete signature/MAC verification guards
verification         (e.g., dropping an Eq(verify(...),
                     true)-style check), enabling message
                     forgery.
                                                                            Fig. 9. Lemma count vs. CRO ST. Each point is an LLM.
Weakened binding     Break identity/nonce binding by replacing a
                     bound variable with an unconstrained one.
Missing freshness Remove freshness-related checks so that re-         from 239 to 2672, while CRO ST improves by only about
check                played messages can be accepted without          24 percentage points and largely plateaus after the 8th run.
                     detection.                                       This indicates diminishing returns and coverage saturation:
Incomplete message Remove authentication-critical fields (e.g., a     additional sampling mainly produces redundant or weak vari-
                     nonce) from transmitted messages, prevent-
                     ing the receiver from validating sanity/fresh-
                                                                      ants that contribute little new solve-path coverage. There-
                     ness.                                            fore, improving CSPV performance requires generating more
Broken       message Change message tags/formats so expected          informative lemmas that contribute incremental solve-path
flow                 parsing/transition rules no longer match, dis-   coverage, rather than increasing the raw number of candidates.
                     rupting sanity.
Missing response     Directly delete a required output/response.




                                                                                  Fig. 10. Cumulative sampling and CRO ST.



 Fig. 8. CRoST coverage vs. lemma flip rate under mutation testing.      RQ4. How do LLMs perform across different task
                                                                         types in CSPV?
   RQ3. What are the capability boundaries of LLMs in
                                                                         We treat major security-attribute families as distinct task
   CSPV?
                                                                      types in CSPV (secrecy, authentication, and sanity), and report
                                                                      per-task CRO ST to characterize capability differences and
   With the validity of CRO ST established in RQ2, we next            model biases across tasks.
examine the capability boundary of LLMs in CSPV. A natural               The results in Table III indicate that, on average, SOTA
hypothesis is that higher CRO ST scores may be driven mainly          LLMs perform better on authentication and sanity properties
by generating more lemmas, i.e., stronger models simply               than on secrecy properties. Figure 11 offers a different, lemma-
explore more candidates and thus cover more solve-tree paths          level perspective. The highest-scoring target lemmas are dis-
[44].                                                                 proportionately concentrated in sanity properties. A plausible
   Figure 9 evaluates the relationship between the number of          explanation is that secrecy and authentication properties are
generated lemmas and CRO ST. We observe less correlation              often expressed as all-traces universally quantified lemmas,
with substantial dispersion (p-value = 0.04825). This suggests        whereas sanity properties are more commonly formulated
that CSPV capability differences are not explained primarily          as exists-trace existential lemmas. This suggests that current
by lemma quantity.                                                    LLMs are generally more effective at generating existential
   To further probe the boundary under repeated sampling,             security properties than universally quantified ones.
we run the same pipeline multiple times with a fixed LLM                 To understand the failure modes of SOTA LLMs, we
deepseek-v3.2 and track cumulative statistics (Figure 10).            conduct a focused case study on the top4 LLMs by overall
Across 12 iterations, cumulative generated lemmas increase            CRO ST (claude-sonnet-4.5, claude-opus-4.5, gemini-3-flash-
                                             Fig. 11. Top4 LLMs’ CRO ST on target lemma.



                            TABLE III                                                            TABLE IV
               CRO ST BY S ECURITY P ROPERTY (%).                                      AVERAGE OUTPUT TOKENS PER CALL .

Model                    Overall Secrecy Authentication Sanity                  LLM                          Avg Output Tokens
claude-sonnet-4.5        46.11    30.91        55.85       39.97                claude-sonnet-4.5                  1143
claude-opus-4.5          35.94    42.10        20.02       39.83                claude-opus-4.5                     691
gemini-3-flash-preview   29.36    35.78        24.28       30.74                gemini-3-flash-preview              455
deepseek-v3.2            27.46    20.51        24.25       35.47                deepseek-v3.2                       844
top4 LLMs                38.82    33.90        40.56       39.95
qwen3.5-plus             25.37     9.32        36.48       28.34    AcceptS (phase 1), instead of the target AcceptP (phase 1)
gpt-5.2-codex            24.91    27.50        21.55       20.78
gpt-5.2                  22.60    14.87        25.98       27.44    to AcceptS (phase 1), and forgets the temporal relationship.
claude-haiku-4.5         22.46     8.44        19.90       35.89    This phase mismatch breaks the intended correspondence
grok-4                   15.63    14.87         7.32       22.85    structure.
qwen3-coder-plus         12.46     7.07        21.24        5.37
gpt-4                     6.28     6.67         3.24        3.54              Client                Server
qwen-plus                 5.28     2.54         6.83        6.40
                                                                            AcceptP                AcceptS
                                                                                                                      correct order

preview, and deepseek-v3.2), and analyze representative fail-               AcceptP2              AcceptS2            LLMs failure order

ures on lemma generation.
                                                                      Fig. 12. Example of an LLM failure mode in the basic SSH protocol.

  Case study. Stage point confusion in large protocols.                This issue is particularly damaging for large protocols with
                                                                    many phase-specific action facts induced by multi-round mes-
   To concretely illustrate failure modes of LLMs to generate       sage flows and composed cryptographic primitives. A single
lemma, we present a case study on the multi-phase Au-               stage point mix-up can prevent proof search from reaching the
thenticated Key Exchange (AKE) protocol SSH-R. Its target           target solve-tree paths, resulting in substantial coverage loss
properties are bound to stage-specific action facts.                for the affected lemma family. This case study indicates that
   In SSH-R, client-side authentication proceeds in two stages:     current LLMs often fail to precisely align stage-specific events
the first stage is marked by the action fact AcceptP and cor-       with their temporal constraints, which makes them struggle
responds to transport-layer key exchange plus server authenti-      with CSPV tasks on more complex protocols.
cation, while the second stage is marked by AcceptP2 and
corresponds to user authentication plus final key confirmation.         RQ5. What is the computational cost of using LLMs
Accordingly, the target lemmas are stage-specific rather than           in CSPV?
generic agreement templates: AcceptP (phase 1) is bound to
a prior AcceptS witness, AcceptS2 (phase 2) is bound to                We measure cost from two aspects: (i) LLM token out-
a prior AcceptP2.                                                   put during lemma generation, and (ii) runtime for for-
   We observed that the generated lemmas still demonstrate          mally verifying generated lemmas. All experiments were ex-
a reasonable understanding of the roles of action facts. That       ecuted on Intel(R) Core(TM) i9-14900 (2.00 GHz), 24 cores,
is, LLMs are often able to distinguish whether an action            32GB RAM, with Tamarin configured as +RTS -N -RTS
fact corresponds to key establishment, authentication, or mes-      --auto-sources [16].
sage confirmation, and thus tend to preserve the high-level            For token accounting, we use the Python tiktoken library
functional intent of the protocol. More importantly, however,       for consistent counting across LLMs. The prompt length is
LLMs also exhibit a representative form of stage-point con-         fixed at 1049 tokens for all calls; Table IV reports average
fusion in generated lemmas. In Figure 12, while the LLM             output tokens only.
captures the high-level intent of agreement/authentication, it         For runtime, we report the total time spent verifying gener-
misaligns stage points by relating AcceptP2 (phase 2) to            ated lemmas, and compare it against verifying the original
target lemmas as a baseline. Formal analysis of realistic         Third, for real-world vulnerability discovery, an additional
protocol LLMs can be time- and memory-intensive, making        step is needed to provide counterexample explanation.
verification runtime a key usability factor for CSPV.             Fourth, incorporating richer features of protocols and se-
                                                               curity properties may further improve LLM-based lemma
                            TABLE V
          V ERIFICATION RUNTIME OF GENERATED LEMMAS .
                                                               generation. Our current study is only a preliminary evaluation
                                                               and does not introduce additional protocol-level or property-
Setting                   Lemmas Total Time (s) Mean (s/lemma) level features, leaving this as an important direction for future
Baseline (target lemmas)     91        59.91          0.66     work.
claude-sonnet-4.5           245      1267.76           5.17
claude-opus-4.5             166      1127.33           6.79                            VI. R ELATED W ORK
gemini-3-flash-preview       95       238.24           2.51           Automatic security proofs for cryptographic protocols are
deepseek-v3.2               230      1151.46           5.01
                                                                   not a new research problem [45]. Symbolic protocol verifiers
   Compared to the baseline, verifying generated lemmas in-        provide some basic automation, but it is largely limited to
curs roughly a 4×−21× slowdown. This suggests that, beyond         coarse, pre-defined property templates rather than scenario-
generation cost, the dominant overhead in CSPV can stem            specific, high-level guarantees.
from verification attempts on incorrect or low-utility lemmas.        For example, Scyther [46] can automatically instantiate
Improving lemma quality to reduce wasted verification effort       generic secrecy and authentication claims for protocol vari-
(e.g., by increasing effective coverage gains) is therefore an     ables and locally generated values, enabling basic checks
important direction. The mean per-lemma verification time          without fully hand-writing every claim. But this automation
also increases from 0.66s to 2.51–6.79s, indicating that gen-      is largely confined to generic, coarse-grained security goals
erated lemmas also tend to induce longer formal proof-search       and does not address scenario-specific, complex protocols.
cost per lemma.                                                       Similarly, Tamarin [16] supports automation aimed at proof
                                                                   scalability, such as auto-sources lemmas that are automat-
C. Threats to Validity                                             ically generated to facilitate proving secrecy of protected
   External validity. Our benchmark covers 18 protocols and        subterms (e.g., secrets occurring under hashes/encryptions)
three major property families: secrecy, authentication, and        and to mitigate proof-search blowups due to partial decon-
sanity. However, protocol complexity and property distribution     structions [17], [47]. However, such automation primarily
may affect the observed results, especially in RQ4 where we        targets proof-search scalability and does not resolve the cen-
compare model performance across different security-property       tral property-engineering challenge: deciding which high-level
types. Therefore, the results may not fully generalize to larger   guarantees should be verified in a given scenario and encoding
protocol collections or to property families not covered by our    them precisely as tool-checkable lemmas that are provable or
benchmark.                                                         refutable under the chosen protocol model and verification
   Internal validity. LLM-based lemma generation is sen-           setting.
sitive to prompt design, in-context examples, and decoding            Recent work has begun to combine LLMs with symbolic
randomness. Although we use a unified prompting strategy           protocol verification to reduce the modeling barrier, i.e., gen-
and the same evaluation pipeline across models, the inherent       erating tool-checkable symbolic models directly from natural-
randomness of LLM generation may still introduce variability       language protocol descriptions. [14] studies how to synthesize
in the generated lemmas and the resulting CRoST scores.            symbolic protocol models (centered on SAPIC+ and multiset
                                                                   rewriting rules) from natural-language documents via a staged
                         V. D ISCUSSION
                                                                   pipeline with formally constrained transformations. This line
A. Future work                                                     of work primarily targets the generation of protocol rewrit-
   Our findings suggest several directions for future work.        ing rules (model construction), rather than the generation of
First, CRoST can still produce false positives when proof          security properties/lemmas (property engineering).
paths contain common low-information solve items, such as             CryptoFormalEval [48] provides a simple evaluation of
solve(!KU(x)); an unrelated generated lemma may cover              LLMs in symbolic reasoning. However, they do not provide
the target lemma at such points. Future work can intro-            a method for leveraging LLM capabilities beyond syntax, so
duce stricter constraints into CRoST computation—such as           their results remain at the level of syntax correctness.
semantic-category filtering of solve items, context-consistency       Complementary to those directions, our work focuses on
checks, or minimum-information thresholds—to reduce er-            the setting where the protocol model is already available
roneous matches on common solve items and obtain more              and examines how well LLMs can generate tool-checkable
precise coverage estimates.                                        lemmas.
   Second, scaling CSPV to large, complex protocols requires
addressing stage point confusion: future methods should ex-                             VII. C ONCLUSION
plicitly represent protocol phase structure and constrain gen-        Our work shows that few-shot prompting is often necessary
erated correspondence lemmas to align stage-specific events        to obtain syntactically valid Tamarin lemmas; CRO ST varies
and temporal relations with protocol semantics.                    substantially across LLMs and property families, and complex
multi-phase protocols exhibit recurrent failure modes such as                    [12] J. M. Han, J. Rute, Y. Wu, E. W. Ayers, and S. Polu, “Proof artifact
stage point confusion. Moreover, under fixed prompting and                            co-training for theorem proving with language models,” in The Tenth
                                                                                      International Conference on Learning Representations, ICLR 2022,
pipeline settings, increasing the number of generated lemmas                          Virtual Event, April 25-29, 2022. OpenReview.net, 2022. [Online].
yields diminishing returns and coverage saturation. Finally,                          Available: https://openreview.net/forum?id=rpxJc9j04U
verifying LLM-generated lemmas incurs substantially higher                       [13] A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li,
                                                                                      M. Jamnik, G. Lample, and Y. Wu, “Draft, sketch, and prove:
runtime than verifying baseline target lemmas, highlighting                           Guiding formal theorem provers with informal proofs,” in The Eleventh
verification cost as a practical constraint.                                          International Conference on Learning Representations, ICLR 2023,
                                                                                      Kigali, Rwanda, May 1-5, 2023. OpenReview.net, 2023. [Online].
                                                                                      Available: https://openreview.net/forum?id=SMa9EAovKMC
                         DATA AVAILABILITY                                       [14] Z. Mao, J. Wang, J. Sun, S. Qin, and J. Xiong, “Llm-aided automatic
                                                                                      modeling for security protocol verification,” in Proceedings of the
  The data supporting the results of this paper are publicly                          IEEE/ACM 47th International Conference on Software Engineering,
available at Zenodo2 .                                                                ser. ICSE ’25. IEEE Press, 2025, p. 642–654. [Online]. Available:
                                                                                      https://doi.org/10.1109/ICSE55347.2025.00197
                                                                                 [15] S. Meier, B. Schmidt, C. Cremers, and D. Basin, “The tamarin prover
                              R EFERENCES                                             for the symbolic analysis of security protocols,” in Computer Aided
                                                                                      Verification, N. Sharygina and H. Veith, Eds.        Berlin, Heidelberg:
 [1] C. Cremers, C. Jacomme, and A. Naska, “Formal analysis of session-
                                                                                      Springer Berlin Heidelberg, 2013, pp. 696–701.
     handling in secure messaging: lifting security from sessions to conver-
     sations,” in Proceedings of the 32nd USENIX Conference on Security          [16] The Tamarin Team, Tamarin Prover Manual, Tamarin Prover Project,
     Symposium, ser. SEC ’23. USA: USENIX Association, 2023.                          2024. [Online]. Available: https://tamarin-prover.com/manual/
                                                                                 [17] V. Cortier, S. Delaune, and J. Dreier, “Automatic generation of sources
 [2] X. Liu, C. Zuo, Q. Hou, P. Ren, J. Wu, Q. Zhao, and S. Guo, “A thorough
                                                                                      lemmas in tamarin: Towards automatic proofs of security protocols,” in
     security analysis of ble proximity tracking protocols,” in Proceedings of
                                                                                      Computer Security – ESORICS 2020, L. Chen, N. Li, K. Liang, and
     the 34th USENIX Conference on Security Symposium, ser. SEC ’25.
                                                                                      S. Schneider, Eds. Cham: Springer International Publishing, 2020, pp.
     USA: USENIX Association, 2025.
                                                                                      3–22.
 [3] D. Basin, R. Sasse, and J. Toro-Pozo, “The emv standard: Break, fix,
                                                                                 [18] S. Celi, J. Hoyland, D. Stebila, and T. Wiggers, “A tale of two models:
     verify,” in 2021 IEEE Symposium on Security and Privacy (SP), 2021,
                                                                                      Formal verification of kemtls via tamarin,” in Computer Security –
     pp. 1766–1781.
                                                                                      ESORICS 2022, V. Atluri, R. Di Pietro, C. D. Jensen, and W. Meng,
 [4] S. Andova, C. Cremers, K. Gjøsteen, S. Mauw, S. F. Mjølsnes,
                                                                                      Eds. Cham: Springer Nature Switzerland, 2022, pp. 63–83.
     and S. Radomirović, “A framework for compositional verification of
                                                                                 [19] Z. Ma, C. Wen, Z. Su, X. Liang, C. Tian, S. Qin, and M. Yang, “Bridging
     security protocols,” Inf. Comput., vol. 206, no. 2–4, p. 425–459, Feb.
                                                                                      natural language and formal specification–automated translation of soft-
     2008. [Online]. Available: https://doi.org/10.1016/j.ic.2007.07.002
                                                                                      ware requirements to ltl via hierarchical semantics decomposition using
 [5] C. Cremers, M. Horvat, J. Hoyland, S. Scott, and T. van der Merwe,
                                                                                      llms,” in 2025 40th IEEE/ACM International Conference on Automated
     “A comprehensive symbolic analysis of tls 1.3,” in Proceedings of
                                                                                      Software Engineering (ASE), 2025, pp. 1208–1220.
     the 2017 ACM SIGSAC Conference on Computer and Communications
                                                                                 [20] R. Castaño, V. Braberman, D. Garbervetsky, and S. Uchitel, “Model
     Security, ser. CCS ’17. New York, NY, USA: Association for
                                                                                      checker execution reports,” in 2017 32nd IEEE/ACM International
     Computing Machinery, 2017, p. 1773–1788. [Online]. Available:
                                                                                      Conference on Automated Software Engineering (ASE), 2017, pp. 200–
     https://doi.org/10.1145/3133956.3134063
                                                                                      205.
 [6] J.-K. Zinzindohoué, K. Bhargavan, J. Protzenko, and B. Beurdouche,
                                                                                 [21] D. Dolev and A. Yao, “On the security of public key protocols,” IEEE
     “Hacl*: A verified modern cryptographic library,” in Proceedings of
                                                                                      Trans. Inf. Theor., vol. 29, no. 2, p. 198–208, Sep. 2006. [Online].
     the 2017 ACM SIGSAC Conference on Computer and Communications
                                                                                      Available: https://doi.org/10.1109/TIT.1983.1056650
     Security, ser. CCS ’17. New York, NY, USA: Association for
                                                                                 [22] B. Blanchet, “Security protocol verification: Symbolic and computa-
     Computing Machinery, 2017, p. 1789–1806. [Online]. Available:
                                                                                      tional models,” in Principles of Security and Trust, P. Degano and J. D.
     https://doi.org/10.1145/3133956.3134043
                                                                                      Guttman, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2012,
 [7] C. Cremers, A. Dax, and A. Naska, “Formal analysis of spdm: security
                                                                                      pp. 3–29.
     protocol and data model version 1.2,” in Proceedings of the 32nd
                                                                                 [23] G. Lowe, “A hierarchy of authentication specifications,” in Proceedings
     USENIX Conference on Security Symposium, ser. SEC ’23.              USA:
                                                                                      10th Computer Security Foundations Workshop, 1997, pp. 31–43.
     USENIX Association, 2023.
                                                                                 [24] B. Schmidt, “Formal analysis of key exchange protocols and physical
 [8] M. Dodds, “Formally verifying industry cryptography,” IEEE Security
                                                                                      protocols,” PhD thesis, ETH Zurich, 2012. [Online]. Available:
     & Privacy, vol. 20, no. 3, pp. 65–70, 2022.
                                                                                      https://doi.org/10.3929/ethz-a-009898924
 [9] L. Pan, A. Albalak, X. Wang, and W. Wang, “Logic-LM: Empowering
                                                                                 [25] B. Schmidt, S. Meier, C. Cremers, and D. Basin, “Automated analysis
     large language models with symbolic solvers for faithful logical
                                                                                      of diffie-hellman protocols and advanced security properties,” in 2012
     reasoning,” in Findings of the Association for Computational Linguistics:
                                                                                      IEEE 25th Computer Security Foundations Symposium, 2012, pp. 78–94.
     EMNLP 2023, H. Bouamor, J. Pino, and K. Bali, Eds. Singapore:
                                                                                 [26] C. Cremers. (2024) Security protocol analysis tools. [Online]. Available:
     Association for Computational Linguistics, Dec. 2023, pp. 3806–3824.
                                                                                      https://people.cispa.io/cas.cremers/tools/index.html
     [Online]. Available: https://aclanthology.org/2023.findings-emnlp.248/
                                                                                 [27] V. Cheval, C. Jacomme, S. Kremer, and R. Künnemann, “SAPIC+:
[10] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu,
                                                                                      protocol verifiers of the world, unite!” in 31st USENIX Security
     S. Godil, R. J. Prenger, and A. Anandkumar, “Leandojo: Theorem
                                                                                      Symposium (USENIX Security 22). Boston, MA: USENIX Association,
     proving with retrieval-augmented language models,” in Advances
                                                                                      Aug. 2022, pp. 3935–3952. [Online]. Available: https://www.usenix.
     in Neural Information Processing Systems, A. Oh, T. Naumann,
                                                                                      org/conference/usenixsecurity22/presentation/cheval
     A. Globerson, K. Saenko, M. Hardt, and S. Levine, Eds.,
                                                                                 [28] K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu, “Bleu: a method for
     vol. 36.      Curran Associates, Inc., 2023, pp. 21 573–21 612.
                                                                                      automatic evaluation of machine translation,” in Proceedings of the
     [Online]. Available: https://proceedings.neurips.cc/paper files/paper/
                                                                                      40th Annual Meeting of the Association for Computational Linguistics,
     2023/file/4441469427094f8873d0fecb0c4e1cee-Paper-Datasets and
                                                                                      P. Isabelle, E. Charniak, and D. Lin, Eds. Philadelphia, Pennsylvania,
     Benchmarks.pdf
                                                                                      USA: Association for Computational Linguistics, Jul. 2002, pp.
[11] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
                                                                                      311–318. [Online]. Available: https://aclanthology.org/P02-1040/
     L. Kaiser, and I. Polosukhin, “Attention is all you need,” in Proceedings
                                                                                 [29] M. Evtikhiev, E. Bogomolov, Y. Sokolov, and T. Bryksin, “Out
     of the 31st International Conference on Neural Information Processing
                                                                                      of the bleu: how should we assess quality of the code generation
     Systems, ser. NIPS’17. Red Hook, NY, USA: Curran Associates Inc.,
                                                                                      models?” J. Syst. Softw., vol. 203, p. 111741, 2022. [Online]. Available:
     2017, p. 6000–6010.
                                                                                      https://api.semanticscholar.org/CorpusID:251371647
                                                                                 [30] Y. Yang, S. Xiong, A. Payani, E. Shareghi, and F. Fekri, “Harnessing
  2 https://doi.org/10.5281/zenodo.20996406                                           the power of large language models for natural language to first-order
     logic translation,” in Proceedings of the 62nd Annual Meeting of the      [43] Y. T. Chen, R. Gopinath, A. Tadakamalla, M. D. Ernst, R. Holmes,
     Association for Computational Linguistics (Volume 1: Long Papers),             G. Fraser, P. Ammann, and R. Just, “Revisiting the relationship
     L.-W. Ku, A. Martins, and V. Srikumar, Eds. Bangkok, Thailand:                 between fault detection, test adequacy criteria, and test set size,”
     Association for Computational Linguistics, Aug. 2024, pp. 6942–6959.           in Proceedings of the 35th IEEE/ACM International Conference on
     [Online]. Available: https://aclanthology.org/2024.acl-long.375/               Automated Software Engineering, ser. ASE ’20. New York, NY, USA:
[31] E. Ghassabani, A. Gacek, M. W. Whalen, M. P. E. Heimdahl, and                  Association for Computing Machinery, 2021, p. 237–249. [Online].
     L. Wagner, “Proof-based coverage metrics for formal verification,”             Available: https://doi.org/10.1145/3324884.3416667
     in Proceedings of the 32nd IEEE/ACM International Conference on           [44] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess,
     Automated Software Engineering, ser. ASE ’17. IEEE Press, 2017,                R. Child, S. Gray, A. Radford, J. Wu, and D. Amodei, “Scaling laws for
     p. 194–199.                                                                    neural language models,” ArXiv, vol. abs/2001.08361, 2020. [Online].
[32] N. Tihanyi, Y. Charalambous, R. Jain, M. A. Ferrag, and L. C. Cordeiro,        Available: https://api.semanticscholar.org/CorpusID:210861095
     “A new era in software security: Towards self-healing software via        [45] A. Armando, D. Basin, Y. Boichut, Y. Chevalier, L. Compagna, J. Cuel-
     large language models and formal verification,” in 2025 IEEE/ACM               lar, P. H. Drielsma, P. C. Heám, O. Kouchnarenko, J. Mantovani,
     International Conference on Automation of Software Test (AST), 2025,           S. Mödersheim, D. von Oheimb, M. Rusinowitch, J. Santiago, M. Tu-
     pp. 136–147.                                                                   ruani, L. Viganò, and L. Vigneron, “The avispa tool for the automated
[33] D. Beyer, M. Dangl, D. Dietsch, M. Heizmann, T. Lemberger,                     validation of internet security protocols and applications,” in Computer
     and M. Tautschnig, “Verification witnesses,” ACM Trans. Softw.                 Aided Verification, K. Etessami and S. K. Rajamani, Eds.           Berlin,
     Eng. Methodol., vol. 31, no. 4, Sep. 2022. [Online]. Available:                Heidelberg: Springer Berlin Heidelberg, 2005, pp. 281–285.
     https://doi.org/10.1145/3477579                                           [46] C. J. F. Cremers, “The scyther tool: Verification, falsification, and
[34] X. Ke, A. Khan, and L. L. H. Quan, “An in-depth comparison                     analysis of security protocols,” in Computer Aided Verification, A. Gupta
     of s-t reliability algorithms over uncertain graphs,” Proc. VLDB               and S. Malik, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg,
     Endow., vol. 12, no. 8, p. 864–876, Apr. 2019. [Online]. Available:            2008, pp. 414–418.
     https://doi.org/10.14778/3324301.3324304                                  [47] D. Basin, J. Dreier, and R. Sasse, “Automated symbolic proofs of
[35] G. Tuccio, L. Bulla, M. Madonia, A. Gangemi, and                               observational equivalence,” in Proceedings of the 22nd ACM SIGSAC
     M. Mongiovı̀, “GRAMMAR-LLM: Grammar-constrained natural                        Conference on Computer and Communications Security, ser. CCS ’15.
     language generation,” in Findings of the Association for Computational         New York, NY, USA: Association for Computing Machinery, 2015,
     Linguistics: ACL 2025, W. Che, J. Nabende, E. Shutova,                         p. 1144–1155. [Online]. Available: https://doi.org/10.1145/2810103.
     and M. T. Pilehvar, Eds.            Vienna, Austria: Association for           2813662
     Computational Linguistics, Jul. 2025, pp. 3412–3422. [Online].            [48] C. Curaba, D. Denis, and A. Minisini, “Cryptoformaleval: Integrating
     Available: https://aclanthology.org/2025.findings-acl.177/                     large language models and formal verification for automated
[36] F. Jiao, Z. Teng, B. Ding, Z. Liu, N. Chen, and S. Joty,                       cryptographic protocol vulnerability detection,” in The First Workshop
     “Exploring self-supervised logic-enhanced training for large language          on System-2 Reasoning at Scale, NeurIPS’24, 2024. [Online]. Available:
     models,” in Proceedings of the 2024 Conference of the North                    https://openreview.net/forum?id=hqvJT2pOxu
     American Chapter of the Association for Computational Linguistics:
     Human Language Technologies (Volume 1: Long Papers), K. Duh,
     H. Gomez, and S. Bethard, Eds. Mexico City, Mexico: Association
     for Computational Linguistics, Jun. 2024, pp. 926–941. [Online].
     Available: https://aclanthology.org/2024.naacl-long.53/
[37] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
     A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-
     Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler,
     J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray,
     B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever,
     and D. Amodei, “Language models are few-shot learners,” in Pro-
     ceedings of the 34th International Conference on Neural Information
     Processing Systems, ser. NIPS ’20.        Red Hook, NY, USA: Curran
     Associates Inc., 2020.
[38] S. Min, X. Lyu, A. Holtzman, M. Artetxe, M. Lewis, H. Hajishirzi, and
     L. Zettlemoyer, “Rethinking the role of demonstrations: What makes
     in-context learning work?” in Proceedings of the 2022 Conference
     on Empirical Methods in Natural Language Processing, Y. Goldberg,
     Z. Kozareva, and Y. Zhang, Eds. Abu Dhabi, United Arab Emirates:
     Association for Computational Linguistics, Dec. 2022, pp. 11 048–
     11 064. [Online]. Available: https://aclanthology.org/2022.emnlp-main.
     759/
[39] M. Krichen, “A survey on mutation testing,” in Bio-Inspired Computing,
     V. Sakalauskas, A. Bajaj, A. Abraham, K. R. Madhavi, and P. Manghir-
     malani Mishra, Eds. Cham: Springer Nature Switzerland, 2025, pp.
     210–219.
[40] S. J. Kaufman, R. Featherman, J. Alvin, B. Kurtz, P. Ammann, and
     R. Just, “Prioritizing mutants to guide mutation testing,” in 2022
     IEEE/ACM 44th International Conference on Software Engineering
     (ICSE), 2022, pp. 1743–1754.
[41] R. Just, D. Jalali, L. Inozemtseva, M. D. Ernst, R. Holmes, and
     G. Fraser, “Are mutants a valid substitute for real faults in software
     testing?” in Proceedings of the 22nd ACM SIGSOFT International
     Symposium on Foundations of Software Engineering, ser. FSE 2014.
     New York, NY, USA: Association for Computing Machinery, 2014, p.
     654–665. [Online]. Available: https://doi.org/10.1145/2635868.2635929
[42] M. Papadakis, D. Shin, S. Yoo, and D.-H. Bae, “Are mutation scores
     correlated with real fault detection? a large scale empirical study on
     the relationship between mutants and real faults,” in 2018 IEEE/ACM
     40th International Conference on Software Engineering (ICSE), 2018,
     pp. 537–548.
