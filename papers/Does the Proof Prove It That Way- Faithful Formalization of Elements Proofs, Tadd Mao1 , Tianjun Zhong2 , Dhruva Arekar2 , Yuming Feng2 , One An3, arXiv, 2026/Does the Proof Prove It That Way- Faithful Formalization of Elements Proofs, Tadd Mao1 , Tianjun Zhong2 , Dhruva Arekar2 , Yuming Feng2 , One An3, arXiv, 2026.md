                                            Does the Proof Prove It That Way? Faithful Formalization of Elements Proofs
                                                               Tadd Mao1 , Tianjun Zhong2 , Dhruva Arekar2 , Yuming Feng2 , One An3 ,
                                                                               Jiani Huang3 , Xujie Si1∗ , Ziyang Li2∗†
                                                                                                     1
                                                                                                       University of Toronto
                                                                                                   2
                                                                                                    Johns Hopkins University
                                                                                                  3
                                                                                                    University of Pennsylvania
                                                                                                       ziyang@cs.jhu.edu


                                                                       Abstract                                    et al. 2022; de Moura and Ullrich 2021). Most work targets
                                                                                                                   the formalization of statements (Li et al. 2024; Azerbayev
                                           In formal verification, both the autoformalization of state-            et al. 2023), yet the formalization of proofs is often left
                                           ments and automated proof search have been studied exten-
                                                                                                                   to automated proof search, which hunts for a sequence of
                                           sively. While automated proof search can produce a formal
                                           proof that compiles, the generated proof does not necessar-             proof tactics that closes the goal. As a result, proof faithful-
                                           ily reflect how the natural-language argument arrives at its            ness, whether the formal proof reflects how the NL argument
                                           conclusion—a property we refer to as faithfulness. With faith-          reaches its conclusion (Avigad, Dean, and Mumma 2009;
arXiv:2608.15432v1 [cs.AI] 15 Aug 2026




                                           fully formalized proofs, one can check the reasoning behind             Cabral et al. 2025), is largely overlooked.
                                           a human- or AI-written argument, and assist mathematicians                 Faithfulness is not a stylistic nicety; it is what makes a
                                           in formalizing their proof sketches. However, it is particularly        formal proof useful beyond a yes or no verdict. A faithful
                                           challenging due to misalignment of formal proof tactics and             formalization lets us check correctness at the level of the ar-
                                           natural language reasoning. In this work, we rigorously de-             gument, certifying that the reasoning as written in NL is valid.
                                           scribe a set of five necessary conditions a faithful formal proof
                                           must satisfy, and introduce Pistis, an agentic, oracle-guided
                                                                                                                   When the argument has a hole, a faithful attempt localizes
                                           proof search that produces formal Lean proofs that satisfy              it rather than silently papering over it with proof automa-
                                           them. At its core is a novel faithfulness-preserving divide-            tion, letting us validate or refute a given NL proof. It helps
                                           and-conquer search, which we name OrderDecompose, that                  mathematicians turn informal sketches into formal artifacts
                                           tracks citation dependencies and blocks unfaithful shortcuts,           that still resemble what they wrote, and it keeps those arti-
                                           paired with a refutation search, that surfaces gaps and er-             facts legible for study and teaching, since each NL reasoning
                                           rors in the natural language proof source. OrderDecompose               step maps directly to a formal step. For a proof to contribute
                                           completes proofs that baselines cannot close even within a 12-          to the broader field, legibility is only the starting point; the
                                           hour budget, and its artifacts compile over 33× as fast as prior        community must also recognize, digest, and build upon its
                                           work’s. We apply Pistis on the first three books of Euclid’s            argument. A human author can convey the insights behind a
                                           Elements, producing high-quality artifacts containing faithful
                                           formal proofs. Under a blinded human study and an LLM-as-
                                                                                                                   proof, while current AI tools remain black boxes (Tao 2026).
                                           a-judge protocol on rigorous rubrics, Pistis-generated proofs              Achieving faithfulness is hard for three reasons. First, the
                                           are favored over prior works—2.89× and 5.2× as often by                 target is intrinsically misaligned with the source: a proof
                                           human reviewers and the LLM judge, respectively. It further             assistant like Lean or Rocq advances by tactics, which trans-
                                           uncovers gaps in Euclid’s proofs and their translation, and can         form proof states, whereas an NL proof advances by sen-
                                           accept or refute natural language proofs written by humans              tences of mathematical reasoning. Second, NL proofs may
                                           or AI, demonstrating that faithful formalization is useful as a         omit steps a human finds obvious but the formal system
                                           proof-checking tool.                                                    explicitly demands, so a faithful proof must fill these gaps
                                                                                                                   without altering mathematical proof structures. Third, the
                                                                 1   Introduction                                  field lacks a precise, checkable notion of what proof faith-
                                                                                                                   fulness is (Murphy et al. 2024; Cabral et al. 2025): prior
                                            We are not trying to meet some abstract production quota               evaluations lean on coarse proxies such as LLM-as-a-judge
                                            of definitions, theorems and proofs. The measure of our
                                                                                                                   semantic matching (Lu et al. 2024; Poiroux et al. 2025; Yu
                                            success is whether what we do enables people to understand
                                            and think more clearly and effectively about mathematics.              et al. 2025), which cannot serve as a certification.
                                                                                                                      In this work we introduce Pistis1 , a framework that for-
                                                  On Proof and Progress in Mathematics (Thurston 1994)             malizes an NL proof into a faithful Lean proof, which we
                                         Autoformalization translates natural-language (NL) mathe-                 demonstrate in Euclidean geometry. Our key insight is that
                                         matics into the formal language of a proof assistant such as              faithfulness becomes tractable once the proof is segmented:
                                         Lean or Rocq, where it can be checked mechanically (Wu                    rather than searching for a single proof term that closes the
                                                                                                                   whole theorem, we split the NL proof into structural formal
                                            ∗
                                                These authors contributed equally.
                                                                                                                      1
                                            †
                                                Corresponding author.                                                     From the Greek pistis (πίστ ις), meaning “faith” or “trust.”
 Euclid, Elements I-6                              Formal statement in Lean (given)
 Statement. If a triangle has two angles           theorem proposition_6 : ∀ (a b c : Point) (AB BC AC : Line),
 equal to one another then the sides subtend-        formTriangle a b c AB BC AC ∧ (∠ a:b:c = ∠ a:c:b) → |(a–b)| = |(a–c)|
 ing the equal angles will also be equal to
 one another. Let ABC be a triangle having
                                                   Unfaithful             Partly faithful              Faithful (ours)
 the angle ABC equal to the angle ACB. I
 say that side AB is also equal to side AC.        by                     by euclid_intros             by euclid_intros
                                                    euclid_intros          by_contra           1 2      have habsurd:                   1 2
 Proof. For if AB is unequal to AC then             euclid_apply           by_cases                      ¬(|(a–b)|̸=|(a–c)|) := . . .
 one of them is greater. 1 Let AB be                 (superposition          |(a–b)| > |(a–c)|           wlog gt: |(a–b)| > |(a–c)|
 greater. 2 And let DB, equal to the lesser             a b c a c b        · -- the first case            generalizing b c AB BC AC
 AC, have been cut off from the greater AB              AB BC AC AC)         euclid_apply        3        with Hsym
  Proposition I-3 . 3 Therefore, . . . , and the     as                       (prop_3 . . . ) as d       · . . . -- prove symmetry gap
                                                     (b’,c’,BC’,AC’)         euclid_apply                · have s3: between b d a          3
 angle DBC is equal to the angle ACB. 6                                       (line d c) as DC                ∧ |(b–d)|=|(a–c)| := . . .
                                                    euclid_finish
 Thus, the base DC is equal to the base                                      euclid_apply                   . . . -- steps 4-5
 AB, 7 and the triangle DBC will be                                           prop_4 . . .                  have s6: ∠d:b:c = ∠a:c:b 6
                                                                                                            . . . -- steps 7-9        10 – 11
 equal to the triangle ACB Proposition I-4 ,                 A               euclid_finish
                                                                           · -- the second case         have s10: ¬(|(a–b)|̸=|(a–c)|)
 the lesser to the greater. 8 The very no-                                   euclid_apply                := by exact habsurd
 tion (is) absurd Common Notion 5 . 9 Thus,              D
                                                                              (prop_3 . . . ) as d      have s11: |(a–b)| = |(a–c)|
 AB is not unequal to AC. 10 Thus, (it is)                                   ...                         := by_contra . . .
 equal. 11 Thus, if a triangle has. . . 12    □      B           C           euclid_finish              exact s11


Figure 1: Motivating example (Book I, Prop. 6). Left: Euclid’s statement and natural-language proof, its sentences marked 1 – 12
at the points where our method splits them; citations appear as pills (e.g. Proposition I-3 ); the accompanied diagram illustrates
the corresponding geometric constructions. Top right: the formal statement we are given in Lean. Bottom right: three ways
to fill the proof, from unfaithful to faithful. Left: a single superposition that discards Euclid’s argument; middle: prior
work (Murphy et al. 2024), where one euclid_finish collapses many of Euclid’s sentences; and right: our faithful proof,
where each NL sentence maps to exactly one formal step matching k on the left.


sub-goals. This process is accomplished by the Map Stage                  gaps and refutes erroneous NL proofs, including 2 genuine
of Pistis, where an agent works with an oracle to ensure the              citation mistakes in the Elements translated text.
faithfulness of the mathematical proof structure.
                                                                          Contributions.        In summary, we contribute:
   After mapping a faithful proof structure, Pistis invokes
                                                                           • new Lean artifacts of faithfully formalized proofs for
a Fill Stage algorithm, OrderDecompose, which is a novel
                                                                             Books I–III of Euclid’s Elements;
proof search backed by LLM agents. Its key component is
an ordered, hierarchical decomposition that closes stratified              • a taxonomy of five necessary conditions of faithfulness a
sub-goals individually rather than the theorem as a whole,                   formal proof must satisfy;
giving both efficient compilation and a tight feedback loop.               • Pistis, an oracle-guided methodology for faithful proof
This is further accompanied by 1) a proof-structure preser-                  formalization, built on the OrderDecompose search;
vation mechanism that guards against the rewriting of the                  • a thorough evaluation on faithfulness, cost efficiency, and
top-level faithful structure, 2) agentic tools that enforce faith-           compilation time, including a double-blind human expert
ful citation dependencies so each supporting proposition is                  review, showing improvements over prior methods; and
applied exactly where the argument invokes it, and 3) when a
                                                                           • the identification of at least 52 gaps in Elements proofs
sub-goal will not close, refutation techniques such as proving
                                                                             including 2 genuine mistakes in the translation.
the negated sub-goal or searching for a counterexample.
   We evaluate Pistis on the first three books of Euclid’s                                  2   Motivating Example
Elements (92 propositions), producing new Lean artifacts.                 Consider Proposition 6 of Book I (I-6): if a triangle has two
Beyond extending the previously formalized single book of                 equal angles, the sides subtending them are equal (Fig. 1).
LeanEuclid (Murphy et al. 2024), we argue our artifact is                 Problem-wise, we are given its natural-language (NL) proof
of higher quality. They compile at least 33× as fast, and on              as a string and its statement already formalized in Lean; our
four criteria across 127 blinded reviews, human evaluators                task is to fill in the formal proof. It appears early in Euclid’s
favor Pistis-generated proofs 2.89× as often as the already               Elements and reads as a short, simple argument. However,
faithfulness-claiming LeanEuclid. An LLM-as-a-judge pro-                  formalizing it faithfully already forces us to discharge an
tocol scoring a rigorous five-dimension rubric agrees, fa-                implicit without-loss-of-generality step and several unstated
voring Pistis over LeanEuclid by a 26:5 win–loss ratio on                 deductions, difficulties that compound in later propositions.
Book I. An ablation shows that OrderDecompose finishes
within a fixed budget, produces 2.5× as many completed                    Faithfulness. Lean’s kernel enforces proof irrelevance:
proofs as a state-of-the-art LLM-agent baseline while being               any two proofs of the same proposition are definitionally
80% more cost-effective. Finally, Pistis faithfully surfaces              equal (Carneiro 2019), so Lean accepts any term whose type
Table 1: Conditions Pistis guarantees; all notation is defined in the Problem Definition. Faithfulness comprises the five necessary
conditions of faithfulness; Soundness is separate. A free variable si ranges over all sentences s1 , . . . , sn . script checks are
automated (no M), oracle checks are by human experts, and Soundness is checked by Lean.

Name                       Condition                                                                                          Checked by
Coverage                   s1 , . . . , sn concatenate, in order, to the NL proof PNL                                         Script
Atomicity                  si has a single assertion assert(si ), with assumptions assumps(si )                               Oracle
Atomic Faithfulness        ∀a ∈ assumps(si ), formal(a) is faithful, and formal(assert(si )) is faithful                      Oracle
Order                      (formal(assert(s1 )), . . . , formal(assert(sn ))) is a subsequence of (ϕ1 , . . . , ϕN )          Script
Citation                   Given formal(assert(si )) = ϕk , every (NL) prop. p cited in si has formal(p) ∈ {ϕj : j < k}       Script
Soundness                  formal(PNL ) compiles in Lean with no sorry                                                        Lean


is the stated proposition. Therefore, all three proofs in Fig. 1         as a named subgoal with have (stepK, shown sK in the
are treated as interchangeable. Yet they differ sharply in how,          figure), so sentences 3 and 6 map exactly. Finally, mirroring
and whether, they follow Euclid. We call a formal proof faith-           Euclid’s conclusion in sentences 10 and 11 , we discharge
ful when it mirrors the NL proof step by step, each formal               habsurd and close the proof with exact.
step corresponding to a specific NL sentence, in the same                   As we show later, the same faithful formalization, applied
order, under the assumptions that sentence actually invokes.             across the corpus, further lets us identify gaps in the Ele-
                                                                         ments and its translations (such as a reference to the wrong
What a faithful proof for I-6 must capture. Euclid ar-                   proposition), produce proofs that human readers prefer, and
gues by contradiction. A faithful formalization must therefore           produce proofs that compile faster than automation-heavy
(a) follow this contradiction path, including the construction           alternatives.
of D; (b) apply each cited proposition exactly where Euclid
applies it, e.g. Proposition I-3 for the construction and I-4
for the triangle congruence; (c) discharge the gaps Euclid
                                                                                              3    Methodology
leaves implicit, in particular the without-loss-of-generality            In this section, we describe the problem definition of faith-
(WLOG) step his “one of them is greater. 1 Let AB be                     ful formalization of NL proofs, including one taxonomy of
greater. 2 ” leaves unstated; and (d) justify each step from             necessary faithful conditions (Sec. 3.1). We then present the
precisely the claims that step is entitled to use.                       overview of Pistis, including its map stage, fill stage, and the
                                                                         main OrderDecomposition algorithm (Sec. 3.2).
Unfaithful and partly faithful proofs. The leftmost proof
(unfaithful) reflects triangle ABC across the axis through A,            3.1   Problem Definition
producing a copy that is congruent, whence AB = AC. This                 We begin by explaining what Pistis takes as input, what it
is a valid proof, but it proves by symmetry and reconstructs             produces as output, and what conditions these satisfy.
none of his steps. The middle proof (partly faithful), pre-
sented in prior work (Murphy et al. 2024), recovers the high-            Input. Pistis takes as input ⟨PNL , formal(PNL ), FNL , ∆⟩,
level shape, but three problems remain. First, where Euclid              where PNL is an NL proposition, formal(PNL ) is its formal-
reasons WLOG, it instead proves both cases directly. Second,             ization in Lean, and FNL is an NL proof of PNL . Specifically,
many sentences have no formal counterpart: sentence 6 , for              formal(PNL ) is of the form α → β, which reads “given the
instance, is absent, and one can only guess the correspon-               hypotheses α, the theorem concludes β.” We may also write
dence by inspecting the referenced symbols. Third, it may                α = α1 ∧ ... ∧ αm to separate the larger formula of hypothe-
hide NL reasoning steps in a black-box euclid_finish                     ses into the individual hypothesis formulas α1 , . . . , αm , and
tactic, which might take a different route than Euclid’s inten-          free variables in α are referred to as v1 , ..., vk ; the Appendix
tion and is non-deterministic.                                           explains why these occur, and concrete examples in Lean.
                                                                         Additionally, the set of System E (Avigad, Dean, and Mumma
A faithful proof. Our proof (faithful, right) follows the NL             2009) axioms is denoted ∆ and is also part of the input.
reasoning line by line. Reading Euclid’s “the very notion
is absurd” 9 , we recognize an argument by contradiction                 Output. While general proof search algorithms only output
and name the negated goal habsurd. Euclid never states                   an arbitrary sound formal proof formal(FNL ), we argue that
WLOG; we infer it from “one of them is greater. 1 Let AB be              to ensure faithfulness, the output requires more than just the
greater. 2 ” and make it explicit with the wlog tactic, proving          formal proof itself. In this work, we enforce a faithful proof to
the required symmetry rather than expanding both cases2 .                capture: (i) knowing each step of the formal proof ϕ1 , ..., ϕN
This discharges the symmetry gap Euclid leaves implicit;                 (rather than the whole proof as one object ϕ) so we can match
had that symmetry been false, the attempt would instead                  these formal steps to the NL steps, (ii) what we even mean
expose the gap or refute the proof outright (Sec. 4.5). We then          by an NL step and how the NL proof is segmented into steps,
proceed sentence by sentence, introducing each assertion                 (iii) what is the structure within an NL step, and finally (iv)
                                                                         which NL step maps to which formal step.
   2
     Without-loss-of-generality (WLOG) is a well-known source of            Therefore, to address the above requirements, the output
subtle errors, since the appealed-to symmetry is not always genuine.     of Pistis is a tuple ⟨ϕ̄, s̄, assumps(·), assert(·), formal(·)⟩
where: (1) ϕ̄ = {ϕi }N    1 = formal(FNL ) which is a sequence                      Algorithm 1: OrderDecompose
of formal steps, with each ϕi derivable from the System E                           Require: Hypothesis τ , Subgoals ψ1 , . . . , ψn and conclusion γ
axioms ∆, hypotheses α and ϕ1 , . . . , ϕi−1 . Formally ϕ̄ is a                         s.t. ∆ ∪ {τ, ψ1 , . . . , ψn } ⊢ γ; LLM M
proof that ∆ ∪ {α} ⊢ β; (2) an NL partition of FNL into steps                       Returns: Bool — whether the proof search succeeded
s̄ = {s1 , . . . , sn }, where each NL step si is referred to as a                   1: for i = 1, . . . , m do           ▷ prove each subgoal ψi in order
segment; (3) two mappings assumps(·) and assert(·), send-                            2:      repeat              ▷ re-attempt ψi until it passes every check
ing each segment si to a set of substrings of si in assumps(si )                     3:         if GiveUp(τ, ψi , M) then return False
and a single substring of si in assert(si ), respectively. For ex-                   4:         (η1 , ...,Vηm ) ← CreateHypothesis(τ, ψi , M)
ample, consider si = “since P and Q, therefore R” we have                            5:         SP ← j InContext(ηj )                           ▷ suppliable
assumps(si ) = {P, Q} and assert(si ) = R; (4) a mapping                             6:         P ← Decomp((η1 , ..., ηm ), ψi , M)             ▷ soundness
formal(·) that sends each assertion assert(si ) to some ϕj                           7:      until SP ∧ P ∧Citation(ψi ) ∧ UnChanged(M \ {ϕ̄′ })
                                                                                     8: end for
and each assumption in assumps(si ) to some ϕk .                                     9: return True                      ▷ all subgoals proven, so γ follows
Conditions. Whereas a typical proof search need only
soundness, i.e., Lean compilation, faithfulness demands                             10: function Decomp((η1 , ..., ηn ), ν, M) : Bool
                                                                                    11:    repeat                  ▷ close ν directly, else decompose it
more, and we present these additional conditions in Tab. 1.
                                                                                    12:        if ∆ ∪ {∪j {ηj }} ⊢SMT-30s ν then return True
They are necessary but not sufficient: they constrain the                           13:        if GiveUp(η̄, ν, M) then return False
proof’s structure while leaving aspects such as author’s im-                        14:        repeat ▷ search lemmas until sufficient & suppliable
plicit intent uncaptured. Complete faithfulness is, we argue,                       15:            (h(j) → ω (j) ) ← CreateLemmas(η̄, ν, M)
unattainable: since a formal proof must fill gaps the NL proof                      16:            SF ← (∆∪{∪k ηk ∪j ω (j) } ⊢SMT-30s ν) ▷ sufficient
omits, a formalization mirroring the NL proof exactly would
                                                                                    17:
                                                                                                         (j)       (j)
                                                                                                   ∀j, (h1 , ..., hlj ) ← h(j)
leave those gaps and hence be unsound. We therefore aim to
be more faithful than prior work rather than perfectly faithful,                    18:            SP ← j,i InContext(hi )                   ▷ suppliable
                                                                                                          V                    (j)

and leave this gap to future work.                                                  19:        until SF ∧ SP
                                                                                    20:        allHelpersClosed ← j Decomp((h(j) ), ω (j) , M)
                                                                                                                       V

3.2     Approach Overview                                                           21:    until allHelpersClosed
                                                                                    22:    return True          ▷ all helper lemmas proved, so ν holds
In order to produce a faithful formal proof satisfying the                          23: end function
aforementioned conditions, Pistis uses a two-stage approach:
a map stage, which creates a faithful and formal template with
sorry placeholders, and a fill stage, which uses OrderDe-                           “cheating”, and agentic tools to aid in the proof search (details
compose to close the formal goal.                                                   in the Appendix).
Map Stage. M := ⟨ϕ̄′ , s̄, assumps(·), assert(·), formal(·)⟩                           The core of OrderDecompose is the recursive Decomp
are produced by the map stage, where ϕ̄′ is intended to                             function (Alg. 1, line 10), which proves a subgoal ν from hy-
be a subsequence of the (eventual) formal proof ϕ̄. These                           potheses η1 , ..., ηn under a 30-second SMT budget, denoted
outputs are created by LLM agents to ensure every condition                         ∆ ∪ {∪j ηj } ⊢SMT-30s ν; the tight budget keeps the feedback
in Tab. 1 except for Soundness, and Citation, and are                               loop fast. When a direct SMT search fails, Decomp asks the
checked by an oracle or a script. Details of the LLM-agent                          LLM to propose intermediate lemmas h(j) → ω (j) , keeps
and its prompting strategies are described in the Appendix.                         them only if they are sufficient (SF) to close ν and suppli-
   If the conditions the oracle is assigned to check are not                        able (SP) from the current context, and recurses on each. In
satisfied, the oracle prompts the LLM to fix the output, and                        both CreateLemmas and CreateHypothesis, the lemma
this process repeats until the oracle is satisfied.                                 search is aided by agentic tools. Finally, because the map
                                                                                    stage leaves Soundness (P) and Citation unverified, Or-
Fill stage. The fill stage proves each ϕ′i since they were left                     derDecompose checks both, and also that map stage objects
unproven (sorry) in the map stage. By “proves“ we mean for                          were unchanged (line 7).
each ϕ′i , create a sequence of steps κ1 , ..., κt s.t. Lean com-                      If OrderDecompose returns False, either: (1) LLM is
piler is able to check that ∆ ∪ {α, ϕ′1 , ..., ϕ′i−1 , κ1 , ..., κt } ⊢             incapable (2) The oracle made a map stage mistake (3) Sys-
ϕ′i . When the check succeeds, κ1 , ..., κt are added to the                        tem E implementation limitations (4) Euclid made a mistake
proof: (ϕ′1 , ..., ϕ′N ′ ) ← (ϕ′1 , ..., ϕ′i−1 , κ1 , ..., κt , ϕ′i , ...ϕ′N ′ ).   or (5) The translated text made a mistake. First, OrderDe-
This process is done using OrderDecompose (Alg. 1).                                 compose’s purpose is to mitigate LLM limitations. Second,
    OrderDecompose takes in hypotheses α, subgoals ϕ̄′ , and                        if the oracle makes a mistake, they fix it and resume Or-
conclusion β, along with an LLM M. It returns either True                           derDecompose (details in the Appendix), and finally, (4)
if it successfully proves all subgoals ϕ′i , or False if M                          and (5) are formally addressed in the next section.
decides to GiveUp. The main structure of OrderDecompose
is to prove ϕ′1 , then ϕ′2 , until ϕ′N ′ in order (Alg. 1, line 1–9),               Acceptance, Refute, and Gaps. To address issues (4) and
and for each ϕ′i , does a recursive, divide-and-conquer search                      (5), Pistis can refute a proof or identify its gaps; we define
by decomposing it into further sub-lemmas (line 14–19) until                        these notions precisely. To refute a proof is to derive a logical
each sub-lemma, is proven, resulting in ϕ′i to be proven. LLM                       contradiction from it. A gap is a missing step that does not
executes and follows OrderDecompose in practice through                             itself create a contradiction, and whether an omission is large
skill files for general instructions, agentic hooks to prevent                      enough to count as a gap is inherently subjective. To accept
    Step Fidelity (0–5)                         LeanEuclid       Tie         Ours                 Step Transp Repr Pref         Step Transp Repr Pref
               4.52                                                                    Prop I-1                                                         Prop I-25
5                                                                                      Prop I-2                                                         Prop I-27
      3.68                Mathematical                                                 Prop I-6                                                         Prop I-28
                          transparency         31%                63%
4                                                                                      Prop I-7                                                         Prop I-30
                                                                                       Prop I-8                                                         Prop I-32
3                              Textbook                                                Prop I-9                                                         Prop I-33
                          representation 17%                    73%                   Prop I-11                                                         Prop I-35
2                                                                                     Prop I-12                                                         Prop I-36
1                                Overall                                              Prop I-13                                                         Prop I-37
                              preference       29%                62%                 Prop I-14                                                         Prop I-38
0                                                                                     Prop I-15                                                         Prop I-39
                                           0     20      40     60      80    100     Prop I-16                                                         Prop I-40
                                                                                      Prop I-17                                                         Prop I-42
    LeanEuclid Ours                               Preferred Responses (%)             Prop I-20                                                         Prop I-43
                                                                                      Prop I-23                                                         Prop I-46

Figure 2: Human expert review results. Left: mean step-                                LeanEuclid                         Tie                           Ours
fidelity ratings with standard error over all rated items. Right:
preference judgments by reviewers on three dimensions.                              Figure 3: Per-proposition human evaluation on Book I, each
                                                                                    cell scored on the [−3, 3] scale: blue favors LeanEuclid, white
                                                                                    a tie, and gold favors ours.
a proof is to certify that it contains no contradiction, and is
therefore valid, though it may still contain gaps.
    Pistis identifies gaps in two ways. First, during the fill stage                source Fitzpatrick (2007), and treat it as the source we for-
the LLM may flag a suspected gap by returning False;                                malize faithfully. A small number of Book III propositions
if the oracle agrees, we mark it (details on how we mark                            are omitted as they lie beyond the scope of the current System
in the Appendix). Second, Pistis detects assumption gaps                            E implementation.
automatically, in an optional stage between mapping and                             Model and Agent. All proofs are generated with Claude
filling. A script materializes each formal assumption as a                          Code (version 2.1.168), driving Claude Opus 4.8.
have statement and tries to close it with automated tactics,
including SMT search; any unclosed assumption becomes a                             Machine configuration. Proofs are checked with Lean 4
gap, marked with a sorry and added to the sequence (ϕ′i )i to                       (v4.8.0-rc2), using SMT solvers Z3 4.15.4 and
be discharged. We treat an unclosed assumption as a reliable                        cvc5 1.3.4. In the Lean compile-time experiments, the SMT
gap because assumptions should already be provable, so                              solvers run uncapped, so the only cutoff is a wall-clock limit.
these tactics should close them.                                                    Experiments were generally run on a Linux SLURM cluster
    Pistis refutes a proof by formally exhibiting one of two                        whose compute nodes are Intel Xeon Platinum 8480+ (Sap-
failures at a step. The first is that an asserted step is false under               phire Rapids), with each job allocated 32 cores and 128 GB.
premises, ∃i, ∆ ∪ {α} ⊢ ¬ formal(assert(si )): the axioms
                                                                                    Baselines and Metrics. We compare against LeanEu-
and hypotheses together disprove what the proof claims at si .
                                                                                    clid (Murphy et al. 2024) (Book I only), which claims to
The second is that an asserted step does not follow from the
                                                                                    already provide faithful formalizations, and vanilla LLM-
premises, ∃i, ∆ ⊢ ∃v1 , ..., vk ¬(α → formal(assert(si ))):
                                                                                    agent based baselines. We report faithfulness (detailed in
there is a concrete configuration of the geometric objects
                                                                                    RQ1), wall-clock time, monetary cost, and other relevant
v1 , ..., vk (the free variables of α) that satisfies the hypotheses
                                                                                    metrics detailed in the following sections.
yet violates assert(si ). Either failure yields a contradiction
that certifies the proof is wrong; we further detail how this is                    4.2   RQ1: Faithfulness of Generated Proofs
derived in the Appendix, and give examples in Sec. 4.5.
                                                                                    Double-blind Human Evaluation. We randomly sampled
                          4      Evaluation                                         30 of the 48 Book I propositions for human review. Each
                                                                                    reviewer was assigned 10 random propositions and saw the
We conduct systematic evaluations of our method to answer                           textbook theorem and proof, two anonymized formalizations,
the following four research questions:                                              and an interactive Lean server for inspecting the proof state at
RQ1. How faithful are the Pistis-generated formal proofs                            each line. The formalizations were shown in randomized or-
     compared to LeanEuclid (Murphy et al. 2024)?                                   der, and method-identifying nonmathematical artifacts were
RQ2. Is OrderDecompose necessary, or can a bare LLM                                 removed. Reviewers were 14 formal-methods researchers and
     complete the fill stage on its own?                                            students familiar with Lean and geometry, who were indepen-
                                                                                    dent of the author team. The study produced 127 completed
RQ3. How does the compilation speed of Pistis-generated                             assignments, with 4.2 final annotations per proposition on
     proofs compare to LeanEuclid?                                                  average, covering 254 step-fidelity ratings and 381 pairwise
RQ4. Qualitatively, how does Pistis refute proofs and iden-                         preference judgments. The review rubric and interface are
     tify gaps, including those in the textbook translations?                       detailed and summarized in the Appendix.
                                                                                       Figure 2 summarizes the aggregate human scores and pref-
4.1     Evaluation Setups                                                           erences, while Figure 3 shows the proposition-level pattern.
Targets. We target Euclid’s Elements, Books I–III, com-                             The human ratings favor our method across all evaluated di-
prising 92 propositions in total (48 in Book I, 14 in Book II,                      mensions. Figure 2 shows a higher mean step-fidelity score
30 in Book III). We take the natural-language proof text                            for our formalizations than for LeanEuclid (4.52 vs. 3.68).
(including its bracketed proposition references) from open                          Reviewers also preferred proofs generated by our method in
       Pistis (Ours)         Baseline (LeanEuclid)     Baseline (Claude Code)                                    Baseline      Pistis (Ours)          Baseline failed
            OC                        OC                     OC




                                                                                                                                      Timeout (12h)
                                                                                     Prop I-3
 ASC                   PSC   ASC               PSC   ASC             PSC             Prop I-6
                                                                                  Prop I-12
                                                                                  Prop I-18
                                                                                  Prop I-20
                                                                                  Prop I-27
 CDF                   PSF   CDF              PSF    CDF            PSF
                                                                                  Prop I-30
   n = 48, scale 3–5           n = 14, scale 0–5      n = 30, scale 0–5
                                                                                  Prop I-36
       (a) Book I                (b) Book II           (c) Book III               Prop I-45
                                                                                  Prop II-3
Figure 4: LLM-as-judge faithfulness by book over five sub-
categories, OC (object correspondence), PSC (proof step                          Prop II-12

coverage), PSF (proof structure fidelity), CDF (cited depen-                     Prop III-6
dency fidelity), ASC (assumption & side condition). Book I                      Prop III-11
compares Pistis against the LeanEuclid baseline, while                          Prop III-25
Book II compares against LLM-agent-generated proofs.                            Prop III-36

                                                                                                               10−1     100       101                       101             101.5
Metric                         OrderDecompose LLM-only Factor
                                                                                           (a) Synthesis wall-clock (hr)                              (b) Compile time (s)
coverage (pass@k) ↑                15/15 (100%)      6/15 (40%) 2.5×
total cost / success ($) ↓             15.6             28.8    1.8×
                                                                                Figure 5: Fill Stage ablation over Books I–III (all 3 runs
                                                                                shown as separate bars). (a) Synthesis wall-clock per propo-
      Table 2: Fill Stage ablation (N =15, k=3 runs each).                      sition; baseline runs that reach the 12h cap fail, while every
                                                                                run of Pistis finishes within ∼3.5h. (b) Compile time of the
                                                                                proof each arm produced, timed by recompiling only that
63.0% of mathematical-transparency comparisons, 73.2% of                        proof’s own files from a warm cited-dependency cache.
textbook-representation comparisons, and 62.2% of overall-
                                                                                                                                                                        ?
preference comparisons. The proposition-level heatmaps in
                                                                                                                      Pistis (Ours) – Run 1
Figure 3 show that these gains are broadly distributed rather                                                                                                 Timeout (1 Hour)
                                                                                                                      Pistis (Ours) – Run 2
than driven by a small number of propositions.
                                                                                  Compile Time (s)




                                                                                                     103
                                                                                                                      Pistis (Ours) – Run 3
                                                                                                                      Baseline (LeanEuclid) – Run 1
LLM-as-Judge Evaluation. We also assess faithfulness                                                                  Baseline (LeanEuclid) – Run 2
with an LLM-as-judge protocol. As shown in Fig. 4, our                                               102
                                                                                                                      Baseline (LeanEuclid) – Run 3
method consistently outperforms the baselines while staying
consistent throughout the three books. Specifically, faithful-                                       101
ness evaluation was done with a 5 point scale rubric across
5 different subcategories: object correspondence, proof step                                               0            10          20                30           40
coverage, proof structure fidelity, cited dependency fidelity,                                                         Number of Propositions Compiled
and assumption and side conditions. We prompted open and
closed LLMs (Opus 4.6 shown, GLM-5 in Appendix) to                              Figure 6: Cactus plot of cold-compile time on a log scale, all
perform assessment with a strict rubric, detailed in the Ap-                    3 runs drawn per world. Our decomposed proofs compile all
pendix. On Book I, Pistis is favored 5.2× as often as Lea-                      48 propositions, while the original baseline compiles 41.
nEuclid (26 wins, 17 ties, 5 losses).

4.3     RQ2: Filling Stage Ablation Study                                       Findings. As shown in Table 2, and a more detailed view in
We compare Pistis (full pipeline) against an ablated bare-                      Fig. 5, Pistis solves all 15 propositions (45/45 runs succeed),
LLM baseline that receives the same agentic framework and                       whereas the baseline solves 6 and fails to finish the remaining
model but with our skills, scripts, hooks, and persistent mem-                  9 within the 12-hour budget (29/45 runs time out). Pistis is
ory removed. Both arms start in the same state, where the                       also cheaper per successful proof ($15.6 vs. $28.8), since the
map stage has just been completed. Further, they are given                      baseline pays for many long runs that never complete.
the same citation instructions, are graded once at the end by
an identical script checking Soundness, Citation (Tab. 1),                      4.4                  RQ3: Lean Compile Performance
and that none of the objects created in the map stage were                      Some LeanEuclid proofs compile very slowly (over an hour)
altered. They run under a 12-hour wall-clock budget per at-                     or not at all, due to heavy SMT reliance. A key design
tempt, and we evaluate 15 propositions across Books I–III                       decision of OrderDecompose is to ensure proofs compile
with 3 repeated runs each (90 total runs).                                      quickly, so here we compare Pistis generated proofs against
 Prop I-9. To cut a given rectilinear angle in half. Let BAC be the given recti. . .                          5    Related Work
 Prop I-10. To cut a given finite straight-line in half. Let AB be the given finite. . .
                                                                                           Autoformalization and Euclidean Geometry. Autofor-
                                                                                           malization in Lean (de Moura and Ullrich 2021) grew from
 NL Source                                     Faithful formalization                      landmark formalizations and libraries (Gonthier 2008; Hales
 Prop III-1. To find the center of a given     theorem p1: ∀(ABC: Circle),                 et al. 2017; mathlib Community 2020) into an area driven by
 circle. Let ABC be the given circle. . .       ∃f: Point, f.isCentre ABC                  language models (Wu et al. 2022; Li et al. 2024). Most work
                                                := by . . .
 Proof. Let some straight-line AB be
                                                 euclid_apply prop_10 . . .                asks what systems can formalize, at growing scales: compe-
 drawn through (ABC), at random 1 ,
 and let (AB) be cut in half at point D
                                                 -- @suppress_deps_check                   tition and textbook statements (Zheng, Han, and Polu 2022;
                                                 have s2: between a d b 2
  Proposition I-9 2 . . . .                      ∧ |(a–d)|=|(d–b)|:= by. . .               Azerbayev et al. 2023), repositories and long contexts (Yang
                                                                                           et al. 2023; Hu, Zhu, and Welleck 2025), corpora and theo-
Figure 7: A citation gap unveiled in the proof of Prop. III-1.                             ries (Min et al. 2026; Feng et al. 2026), progress measured
Fitzpatrick brackets “cut AB in half” as Proposition I-9 , but I-9                         by compilation. Attention has recently turned to how a proof
is about angles, not straight lines, and it should be Prop I-10.                           closes. Euclid has drawn the most: Avigad et al. (Avigad,
                                                                                           Dean, and Mumma 2009) give system E as a faithful model
                                                                                           of his proofs, Beeson et al. (Beeson, Narboux, and Wiedijk
 NL Source                                     Formal refutation                           2018) machine-check Book I, and LeanEuclid (Murphy et al.
 Prop I-5. For isosceles triangles, the        theorem p5: ∀(a b c. . . ) . . .            2024) implements E in Lean with SMT for diagrams. Else-
 angles at the base are equal to one an-        → (∠c:b:d=∠b:c:e) := by                    where informal sketches guide proof search (Jiang et al. 2023;
 other. and if the equal sides are. . .          have s3 : ∠ c:b:d = ⌞                     Zheng et al. 2024), but only heuristically.
 Proof. Since the side AB is equal to             := by sorry                  3
                                                 have refute_s3 :
 the side AC, the base angles are equal
                                                  ¬(∠ c:b:d = ⌞) := by                     Neurosymbolic and Agentic Approaches. Neurosym-
 to one another. . . Now the angle CBD
 is itself a right-angle 3 ,. . . Which is
                                                   . . . ; euclid_finish                   bolic programming (Huang et al. 2021; Li, Huang, and
                                                 have contra : False :=
 the very thing required to show.                 refute_s3 s3
                                                                                           Naik 2023; Manhaeve et al. 2018) supplies neural facts to
                                                                                           declarative programs reasoned over symbolically; agentic
Figure 8: Formal refutation of an LLM-generated proof. Left:                               coding frameworks (Wang et al. 2025) establish the tool-
excerpt from an LLM-generated proof with false claim s3 .                                  equipped-agent pattern. Closest are hierarchical decompo-
Right: we prove ¬ formal(assert(s3 )).                                                     sition searches (Lample et al. 2022; Li et al. 2026), which
                                                                                           split a goal into independently closed subgoals chosen for
                                                                                           tractability: any that closes the theorem will do, none con-
                                                                                           strained by the source argument.
the original LeanEuclid proofs (Murphy et al. 2024) in terms
of compilation speed on Book I. We wipe all built artifacts                                Faithfulness. Statement-level faithfulness means seman-
and compile3 every proposition from cold, one at a time, with                              tic equivalence with the source, via type-checking, back-
a one-hour per-proposition wall timeout, and repeat this over                              translation, or logical equivalence (Poiroux et al. 2025; Lu
three runs. As Fig. 6 shows, Pistis compiles all 48 proposi-                               et al. 2024). Such equivalence never constrains the proof:
tions, whereas LeanEuclid compiles only 41. Further, Pistis                                the kernel accepts any well-typed term inhabiting the goal,
compiles all of Book I in 13.3 minutes of wall-clock, more                                 so a faithful statement admits proofs the source never gave.
than 33× as fast as LeanEuclid (7.3+ hours).                                               Proof-level evaluation is weaker: LeanEuclid (Murphy et al.
                                                                                           2024) measures only whether Lean accepts the proof and
                                                                                           its edit distance to a hand repair. ProofFlow (Cabral et al.
4.5     RQ4: Qual. Analysis of Refutations and Gaps                                        2025) preserves a dependency graph but validates only well-
                                                                                           formedness, not whether each step’s tactics use its declared
We now illustrate how Pistis identifies gaps in Euclid’s El-                               premises. The informal analogue asks whether a chain of
ements and its translations, or refutes NL proofs such as                                  thought reflects its computation (Turpin et al. 2023).
those generated by AI. Across the corpus of Books I–III,
we mark 33 assumption gaps, 2 confirmed citation mistakes,                                         6    Conclusion and Future Works
and 17 other generic gaps. We hereby illustrate a citation gap                             We introduced Pistis, an oracle-guided proof search that for-
found by Pistis arising from the edition rather than Euclid:                               malizes a natural-language proof into a Lean proof satisfying
Fig. 7 shows a source that brackets “let AB be cut in half”                                five necessary conditions of faithfulness. Across three books
as [Prop. I-9], though I-9 bisects an angle whereas bisect-                                of Euclid’s Elements, Pistis produces proofs that are more
ing a straight-line is I-10. Another example, an AI-generated                              faithful than prior work and compile faster, and it accepts
proof refuted by our method, is presented in Fig. 8, where                                 or refutes human- and AI-written arguments, surfacing gen-
the sentence s3 of a proof of Book I, Prop. 5 claims that                                  uine errors. We plan to extend faithful formalization beyond
angle CBD is a right angle, which we formally refute. To-                                  Euclidean geometry and reduce its reliance on supervision.
gether, these demonstrate that Pistis is capable of checking
NL proofs while surfacing gaps and refuting errors.                                        Limitations. Our study is limited to Euclidean geometry
                                                                                           in System E, which cannot express a handful of Elements
                                                                                           propositions. Moreover, Pistis relies on a human or LLM
  3
    Compile-time experiments were run on a single exclusive                                oracle to certify faithfulness, and our conditions, while nec-
AMD EPYC 9634 (Zen 4, 84 cores) in this specific experiment                                essary, are not sufficient to capture an author’s full intent.
                  Acknowledgements                                 Lample, G.; Lachaux, M.-A.; Lavril, T.; Martinet, X.; Hayat,
We thank the anonymous reviewers who participated in our           A.; Ebner, G.; Rodriguez, A.; and Lacroix, T. 2022. Hy-
human evaluation study. Research reported in this publica-         perTree Proof Search for Neural Theorem Proving. arXiv
tion was supported by an Amazon Research Award, Fall               preprint.
2025, and by the 2026 Amazon Nova AI Challenge: Trusted            Li, Z.; Huang, J.; and Naik, M. 2023. Scallop: A Language
Software Agents; Tadd Mao acknowledges support from an             for Neurosymbolic Programming. Proceedings of the ACM
NSERC Undergraduate Student Research Award. The views              on Programming Languages (PLDI), 7.
and conclusions contained herein are those of the authors          Li, Z.; Sun, J.; Murphy, L.; Su, Q.; Li, Z.; Zhang, X.; Yang,
and should not be interpreted as necessarily representing the      K.; and Si, X. 2024. A Survey on Deep Learning for Theorem
official policies of the supporting sponsors.                      Proving. arXiv preprint.
                                                                   Li, Z.; Yang, Z.; He, D.; Zhao, H.; Zhao, A.; Tang, S.; Yang,
                        References                                 K.; Gupta, A.; Su, Z.; and Jin, C. 2026. Goedel-Code-Prover:
Avigad, J.; Dean, E.; and Mumma, J. 2009. A Formal System          Hierarchical Proof Search for Open State-of-the-Art Code
for Euclid’s Elements. The Review of Symbolic Logic, 2(4):         Verification. arXiv:2603.19329.
700–768.                                                           Lu, J.; Wan, Y.; Huang, Y.; Xiong, J.; Liu, Z.; and Guo, Z.
Azerbayev, Z.; Piotrowski, B.; Schoelkopf, H.; Ayers, E. W.;       2024. FormalAlign: Automated Alignment Evaluation for
Radev, D.; and Avigad, J. 2023. ProofNet: Autoformaliz-            Autoformalization. arXiv preprint.
ing and Formally Proving Undergraduate-Level Mathemat-             Manhaeve, R.; Dumancic, S.; Kimmig, A.; Demeester, T.;
ics. arXiv preprint.                                               and De Raedt, L. 2018. DeepProbLog: Neural Probabilistic
Beeson, M.; Narboux, J.; and Wiedijk, F. 2018. Proof-              Logic Programming. In Advances in Neural Information
checking Euclid. arXiv:1710.00787.                                 Processing Systems (NeurIPS).
Cabral, R.; Do, T. M.; Yu, X.; Tai, W. M.; Feng, Z.; and           mathlib Community, T. 2020. The lean mathematical li-
Shen, X. 2025. ProofFlow: A Dependency Graph Approach              brary. In Proceedings of the 9th ACM SIGPLAN Interna-
to Faithful Proof Autoformalization. arXiv:2510.15981.             tional Conference on Certified Programs and Proofs, CPP
Carneiro, M. 2019. The Type Theory of Lean. Master’s thesis,       ’20, 367–381. ACM.
Carnegie Mellon University. https://github.com/digama0/            Min, M. J.; Gao, Y.; Sy, W.; Li, Z.; Si, X.; and Bastani, O.
lean-type-theory.                                                  2026. Divide and Abstract: Autoformalization via Decompo-
de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theo-               sition and Abstraction Learning. In International Conference
rem Prover and Programming Language. In Platzer, A.; and           on Learning Representations (ICLR).
Sutcliffe, G., eds., Automated Deduction (CADE 28), vol-           Murphy, L.; Yang, K.; Sun, J.; Li, Z.; Anandkumar, A.;
ume 12699 of Lecture Notes in Computer Science, 625–635.           and Si, X. 2024. Autoformalizing Euclidean Geometry.
Berlin, Heidelberg: Springer.                                      ArXiv:2405.17216 [cs.LG].
Feng, Y.; Pu, F.; An, O.; Bastani, O.; Zhang, L.; Huang, J.;       Poiroux, A.; Weiss, G.; Kunčak, V.; and Bosselut, A. 2025.
Si, X.; and Li, Z. 2026. Theory-Scale Auto-Formalization of        Reliable Evaluation and Benchmarks for Statement Autofor-
Logics for Computer Science. arXiv:2606.26525.                     malization. In Conference on Empirical Methods in Natural
Fitzpatrick, R. 2007. Euclid’s Elements of Geometry                Language Processing (EMNLP).
(Greek/English edition). https://github.com/rfitzp/Elements.       Tao, T. 2026. Mathematics in the Age of AI. Public lecture,
Greek text after J. L. Heiberg (1883–1885); commit 5a6699e,        International Congress of Mathematicians.
accessed 2026-07-28.                                               Thurston, W. P. 1994. On Proof and Progress in Mathematics.
Gonthier, G. 2008. Formal Proof—The Four-Color Theo-               Bulletin of the American Mathematical Society, 30(2): 161–
rem. Notices of the American Mathematical Society, 55(11):         177.
1382–1393.                                                         Turpin, M.; Michael, J.; Perez, E.; and Bowman, S. R. 2023.
Hales, T.; Adams, M.; Bauer, G.; Dang, T. D.; Harrison, J.;        Language Models Don’t Always Say What They Think:
Hoang, L. T.; Kaliszyk, C.; Magron, V.; McLaughlin, S.;            Unfaithful Explanations in Chain-of-Thought Prompting.
Nguyen, T. T.; et al. 2017. A Formal Proof of the Kepler           arXiv:2305.04388.
Conjecture. Forum of Mathematics, Pi, 5: e2.                       Wang, X.; Li, B.; Song, Y.; Xu, F. F.; Tang, X.; Zhuge,
Hu, J.; Zhu, T.; and Welleck, S. 2025. miniCTX: Neural             M.; Pan, J.; Song, Y.; Li, B.; Singh, J.; Tran, H. H.; Li, F.;
Theorem Proving with (Long-)Contexts. arXiv:2408.03350.            Ma, R.; Zheng, M.; Qian, B.; Shao, Y.; Muennighoff, N.;
Huang, J.; Li, Z.; Chen, B.; Samel, K.; Naik, M.; Song,            Zhang, Y.; Hui, B.; Lin, J.; Brennan, R.; Peng, H.; Ji, H.;
L.; and Si, X. 2021. Scallop: From Probabilistic Deductive         and Neubig, G. 2025. OpenHands: An Open Platform for AI
Databases to Scalable Differentiable Reasoning. In Advances        Software Developers as Generalist Agents. In International
in Neural Information Processing Systems (NeurIPS).                Conference on Learning Representations (ICLR).
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Li, W.; Liu, J.; Jamnik,   Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M. N.; Staats, C.; Jamnik,
M.; Lacroix, T.; Wu, Y.; and Lample, G. 2023. Draft, Sketch,       M.; and Szegedy, C. 2022. Autoformalization with Large
and Prove: Guiding Formal Theorem Provers with Informal            Language Models. In Advances in Neural Information Pro-
Proofs. arXiv:2210.12283.                                          cessing Systems (NeurIPS).
Yang, K.; Swope, A. M.; Gu, A.; Chalamala, R.; Song, P.; Yu,
S.; Godil, S.; Prenger, R.; and Anandkumar, A. 2023. Le-
anDojo: Theorem Proving with Retrieval-Augmented Lan-
guage Models. In Advances in Neural Information Process-
ing Systems (NeurIPS) Datasets and Benchmarks Track.
Yu, X.; Zhong, J.; Feng, Z.; Zhai, P.; Yousefzadeh, R.; Ng,
W. C.; Liu, H.; Shou, Z.; Xiong, J.; Zhou, Y.; Ong, C. B.;
Sugiarto, A. J.; Zhang, Y.; Tai, W. M.; Cao, H.; Lu, D.;
Sun, J.; Xu, Q.; Xin, S.; and Li, Z. 2025. Mathesis: To-
wards Formal Theorem Proving from Natural Languages.
arXiv:2506.07047.
Zheng, C.; Wang, H.; Xie, E.; Liu, Z.; Sun, J.; Xin, H.; Shen,
J.; Li, Z.; and Li, Y. 2024. Lyra: Orchestrating Dual Correc-
tion in Automated Theorem Proving. arXiv:2309.15806.
Zheng, K.; Han, J. M.; and Polu, S. 2022. MiniF2F: a cross-
system benchmark for formal Olympiad-level mathematics.
In International Conference on Learning Representations
(ICLR).
         A    Pistis Implementation Details                              • ϕ̄′ , the sequence of subgoals the fill stage will close, which
This section is intended to clarify the connection between                 consists of both the sentence steps formal(assert(si ))
what the main paper describes abstractly in the methodol-                  and the additional helper have ...:= by sorry
ogy to how it is implemented. Examples of such questions                   steps the map stage inserts to bridge them (e.g. swapfig
we answer include: what does the mapping formal(·) look                    in Fig. 10).
like in the code? How do we enforce that the agent follows             Alongside euclid_sentence, three sibling tactics han-
OrderDecompose?                                                        dle Euclid’s non-assertive sentences. These still record the
                                                                       text (so Coverage can tile the full proof) but emits no have,
A.1    How Objects are Implemented                                     carries no claim, and leaves the proof term and context un-
Input Objects. Recall (Sec. 3) that Pistis takes as input the          changed. The three differ only by what role they mark:
tuple ⟨PNL , formal(PNL ), FNL , ∆⟩. Fig. 9 instantiates every           • euclid_intro_sentence: this is just PNL
component verbatim from the released artifact on Book I,                 • euclid_conclude_sentence: the closing restate-
Prop. 6 (I-6), the running example of Fig. 1, so a reader can              ment of PNL , which Euclid always writes
locate each object in the codebase directly. The figure shows
                                                                         • euclid_wts: a mid-proof “I say that X” (last line of
every input object, as well as further details such as what the
                                                                           Fig. 10) that announces the goal X the following sen-
free variables are, and how formal(PNL ) is broken down into
                                                                           tences will establish, rather than asserting X is already
α → β.
                                                                           proven.
Free Variables. We explain why there are free variables                Because a structural sentence asserts nothing, for it
rather than having the variables quantified with ∀.                    assert(si ) is the empty string, assumps(si ) = ∅, and
   Usually, theorems never have any free variables, and they           formal(assert(si )) = True.
are all quantified with either ∀ or ∃. However the way we
write theorems in Lean, when we prove a theorem, we are                Fill Stage Objects. The fill stage proves each ϕ′i that
not proving the one with ∀ quantifiers, and rather the one             the map stage left as sorry: for each it produces a se-
with free variables. Take for example the theorem statement            quence of steps κ1 , . . . , κt such that Lean checks ∆ ∪
∀x ∈ C, P (x) → Q(x). In Lean this theorem statement is                {α, ϕ′1 , . . . , ϕ′i−1 , κ1 , . . . , κt } ⊢ ϕ′i (Sec. 3.2). Fig. 11 shows
                                                                       an example of how this happens concretely.
 theorem prop : (x : C), P(x) → Q(x) :=
                                                                       Output Objects. Fig. 12 gives a bird’s-eye view of a fully
This is a function, where x ∈ C is already given and fixed.            completed proposition, showing an example of what the full
The proof, that is the stuff after :=, is really a proof that          output looks like in practice.
∆ ∪ {x ∈ C} ⊢ P (x) → Q(x). Here, x is a free variable not
quantified with ∀. Another subtlety, is in this case, we would         A.2     Map Stage Details
consider P (x) as the hypothesis, and because we use the               This section explains how the map stage is executed in the
intro tactic, we are really proving ∆ ∪ {x ∈ C, P (x)} ⊢               code.
Q(x). Hence in this example, α = α1 ∧ α2 = x ∈ C ∧ P (x),                 The map stage runs as skills (Tab. 3) which are prompt
while β = Q(x), with the proof being that of ∆ ∪ {x ∈                  files. The first skill ran is (1) faithful-split, which
C, P (x)} ⊢ Q(x).                                                      gets the LLM to read the proposition’s English text and
  As a final note, even though Lean only directly proves               splits it into an ordered list of NL segments satisfy-
∆ ∪ {x ∈ C, P (x)} ⊢ Q(x), this directly implies ∆ ⊢ x ∈               ing Atomicity and Coverage, and finally written to a
C → (P (x) → Q(x)), which further implies ∆ ⊢ ∀x ∈                     file split.json. A script (check_faithful.py
C, (P (x) → Q(x))                                                      --split) then confirms this partition tiles the source
Map Phase Objects. The map stage produces the tuple                    text byte-for-byte, enforcing Coverage before any Lean
M = ⟨ϕ̄′ , s̄, assumps(·), assert(·), formal(·)⟩ (Sec. 3.2) as         is written. Then (2) faithful-map turns that split
a single Lean file, and Fig. 10 shows this artifact concretely         into Main.lean. It first stamps a placeholder file,
for Prop. 6 in its pre-fill state, where every step body is still      a        euclid_sentence "Book#.Prop#.Step#"
:= by sorry. The euclid_sentence tactic is what                        "NL segment" (stepN : True) := by sorry
constructs these objects, and each output-tuple component is           per entry, using the faithful_map_assemble.py
pinpointed in the figure. Each tuple object is implemented             --placeholders script, which copies each sentence’s
as:                                                                    "NL segment" and locator directly from split.json.
                                                                       Then the agent replaces each True with (what the agent
  • s̄ = {s1 , . . . , sn }, the ordered NL string literals, one per
                                                                       thinks) is the sentence’s real claim formal(assert(si ))
    euclid_sentence, appearing top-to-bottom so the
                                                                       and each placeholder tag with a real @assumption
    Order condition holds by construction;
                                                                       ("text", type).
  • formal(assert(si )), the type annotation τ of (stepi : τ )            At the end check_faithful.py re-checks Coverage
    in each sentence. Also, the assertion assert(si ) is the part      and Order, while the oracle checks Atomicity and Atomic
    of si that is not an assumption;                                   Faithfulness.
  • For each a ∈ assumps(si ), a and formal(a) are defined                One may wonder how Order is possible to check. After
    by the -- @assumption ("text", type) com-                          all, the definition in Tab. 1 references ϕ̄ the final proof, which
    ment tags above the sentence, one per assumption a;                does not yet exist. Recall that the fill stage is only allowed
-- ============ formal(P_NL) : the Lean theorem (Book1/Prop06/Main.lean) ============
theorem proposition_6 : ∀ (a b c : Point) (AB BC AC : Line),
  formTriangle a b c AB BC AC ∧ (∠ a:b:c = ∠ a:c:b)    -- hypothesis α = α1 ∧ ...
  → |(a-b)| = |(a-c)|                                   -- conclusion β
--   free variables v1 ..vk : a b c, AB BC AC

-- ============ P_NL : the natural-language proposition ============
-- "If a triangle has two angles equal to one another then the sides subtending
-- the equal angles will also be equal to one another."

-- ============ F_NL : the natural-language proof that gets segmented ============
-- "Let ABC be a triangle having the angle ABC equal to the angle ACB. I say that
-- side AB is also equal to side AC. For if AB is unequal to AC then one of them
-- is greater. Let AB be greater. And let DB, equal to the lesser AC, have been
-- cut off from the greater AB [Prop. 1.3]. And let DC have been joined [Post. 1].
-- Therefore, since DB is equal to AC, and BC (is) common, the two sides DB, BC are
-- equal to the two sides AC, CB, respectively, and the angle DBC is equal to the
-- angle ACB. Thus, the base DC is equal to the base AB, and the triangle DBC will
-- be equal to the triangle ACB [Prop. 1.4], the lesser to the greater. The very
-- notion (is) absurd [C.N. 5]. Thus, AB is not unequal to AC. Thus, (it is) equal."

-- ============ ∆ : the fixed System E axiom set (SystemE/Theory/**), e.g. ============
axiom two_points_determine_line : ∀ (a b : Point) (L M : Line),
  distinctPointsOnLine a b L ∧ (a.onLine M) ∧ (b.onLine M) → L = M
axiom segment_symmetric : ∀ (a b : Point), |(a-b)| = |(b-a)|
axiom angle_symm : ∀ (a b c : Point), (a ̸= b) ∧ (b ̸= c) → ((∠ a:b:c) = (∠ c:b:a))
axiom superposition : ∀ (a b c d g h : Point) (AB BC AC L : Line), . . .
-- . . .

Figure 9: The input tuple ⟨PNL , formal(PNL ), FNL , ∆⟩ instantiated on Book I, Prop. 6. Every component is reproduced verbatim
from the released artifact.


to insert formulae κ in between two existing ϕ′i , ϕ′j . This is    in isolation as it was proved.
enforced in practice by telling the LLM, and script checkers
such as check_faithful.py. Thus checking the order                  Resume. check_step.py records which steps are al-
is correct in the map stage guarantees the order stays correct      ready proven. Because the agent proves the steps in order,
in the fill stage.                                                  if it stops after finishing ϕ′i−1 it simply continues from ϕ′i
    Once the oracle approves all checks in the end,                 rather than starting over. This is correct because each ϕ′i is
check_steps.py --save saves these objects so the                    proved using only α, ϕ′1 , . . . , ϕ′i−1 , so it can never depend
fill stage cannot silently alter them (the LLM agent is denied      on a later step; the steps already proven stay valid, and if the
write access).                                                      oracle later fixes a map-stage mistake only that step and the
                                                                    ones after it need re-proving.
A.3    Fill Stage (OrderDecompose) Details
                                                                                B    Accept, Refute, and Gaps
Similar to how map stage is implemented, the fill stage re-
lies on skills, but also relies on hooks, and tools to follow       In this section, we validate our formal refutation methods,
OrderDecompose.                                                     then go into more detail on gaps.
   It starts by calling the faithful-prove skill (Tab. 3),
which contains the core instructions of OrderDecompose.             B.1    Why Refutation Creates a Logical
During the algorithm, a set of tools (Tab. 4) help the agent in            Contradiction
the proof search process, and hooks/settings make the agent         This section goes into detail how we are able to prove a
actually follow the algorithm rather than merely being told         logical contradiction if either of the following are true:
to. One example of a setting to enforce good behavior, is           A ∃i, ∆ ∪ {α} ⊢ ¬ formal(assert(si ))
that the agent is denied raw lake build, and can only
build using one of the tools, so all its build commands can         B ∃i, ∆ ⊢ ∃v1 , ..., vk , ¬(α → formal(assert(si ))), where
be checked.                                                           v1 , ..., vk are all the free variables occurring in α
   An example of a hook, is that we hard-deny the agent from        We begin by assuming that System E axioms cannot prove
writing any stepN.lean that is past the latest step checked,        the contradiction, denoted False in Lean, and nor can the
so it physically cannot skip ahead or prove a later step before     hypotheses ( ∆∪{α} ⊬ False). Recall that if, Pistis is able
an earlier one is certified, enforcing the in-order iteration of    to accept the proof, then a proof (ϕ1 , ...., ϕN ) of ∆∪{α} ⊢ β,
line 1 of Alg. 1. Routing every build through these scripts         is outputted. A property of this proof, is that for every ϕi ,
likewise forces the SF/SP/P (sufficiency, suppliability, and        ∆ ∪ {α} ⊢ ϕi (according to first order logic). Also, recall
provability) discipline on each new lemma: it is first checked      that every formal(assert(si )) = ϕk for some k (output 4 of
for sufficiency (line 16), then suppliability (line 18), and only   Sec. 3).
then proven (line 20). A final check_step.py --all                     If A is true, then ∆ ∪ {α} ⊢ ¬ϕk , but because ϕ̄ is a proof
certifies the whole proof end-to-end; in practice it rarely         of ∆ ∪ {α} ⊢ β, ∆ ∪ {α} ⊢ ϕk hence we prove False. We
surfaces anything new, since each step was already certified        assumed we cannot prove False so this is a contradiction.
theorem proposition_6 : ∀ (a b c : Point) (AB BC AC : Line),
  formTriangle a b c AB BC AC ∧ (∠ a:b:c = ∠ a:c:b) → |(a-b)| = |(a-c)| := by
  euclid_intros
  have habsurd : ¬ (|(a-b)| ̸= |(a-c)|) := by
    intro hne
    -- s1 = "For if AB is unequal to AC then one of them is greater."
    -- assert(s1 ) = "one of them is greater"
    -- formal(assert(s1 )) = |(a-b)| > |(a-c)| ∨ |(a-c)| > |(a-b)|
    -- assumptions(s1 ) = { "AB is unequal to AC" },
    -- formal(a) = |(a-b)| ̸= |(a-c)|, where a is the one element in assumptions(s1 )
    -- @assumption ("AB is unequal to AC", |(a-b)| ̸= |(a-c)|)
    have step1_assumption1 : |(a-b)| ̸= |(a-c)| := by assumption -- materialized assumption
    euclid_sentence "1.6.1" "For if AB is unequal to AC then one of them is greater."
       (step1 : |(a-b)| > |(a-c)| ∨ |(a-c)| > |(a-b)|) := by sorry
    wlog hgt : |(a-b)| > |(a-c)| generalizing b c AB BC AC with Hsym
    · have swapfig :                               -- another helper ‘have‘ in ϕ
           (∠ a:c:b = ∠ a:b:c) ∧ (a ̸= c) ∧ (AC ̸= BC) ∧ (BC ̸= AB) ∧ (AB ̸= AC)
           ∧ (|(a-c)| ̸= |(a-b)|) ∧ (|(a-c)| > |(a-b)| ∨ |(a-b)| > |(a-c)|)
           ∧ (|(a-c)| > |(a-b)|) := by sorry
       obtain ⟨. . . ⟩ := swapfig
       exact Hsym c b AC BC AB . . .
    · euclid_sentence "1.6.2" "Let AB be greater."
         (step2 : |(a-b)| > |(a-c)|) := by sorry
       .
       .
       .
       euclid_sentence "1.6.9" "The very notion (is) absurd [C.N. 5]."
         (step9 : False) := by sorry
       exact step9
  euclid_sentence "1.6.10" "Thus, AB is not unequal to AC."
    (step10 : ¬ (|(a-b)| ̸= |(a-c)|)) := by sorry
  euclid_sentence "1.6.11" "Thus, (it is) equal."
    (step11 : |(a-b)| = |(a-c)|) := by sorry
  exact step11

-- ----------- separately, a mid-proof "what-to-show" sentence (Book I Prop. 19) -----------
-- euclid_wts announces a goal instead of asserting a fact, so:
--   assert(si ) = "" (empty), assumptions(si ) = ∅, formal(assert(si )) = True
  euclid_wts "1.19.2" "In fact, AC is not equal to AB."

Figure 10: Example of artifact at the end of map-stage, M = ⟨ϕ̄′ , s̄, assumps(·), assert(·), formal(·)⟩. The
euclid_sentence tactic is the mapping-object constructor: it emits the ordered NL partition s̄ = {s1 , . . . , sn }, and
for each si its type (stepi : τ ) is formal(assert(si )) while the -- @assumption tags above it pinpoint assumps(si )
together with each formal(a). Each @assumption is also materialized as a have (e.g. step1_assumption1) by the
assumption stage (Sec. B.2). A euclid_wts is also shown at the end. The way to know if it is “wts“ or not is by context of
what is around it.


  If B is true, we show that it will also lead to a contradiction.   tions are notions that should already be proven, not new
Like case A, ∆ ∪ {α} ⊢ ϕk , and therefore ∆ ⊢ α → ϕk ,               steps to prove, and we believe these automated tactics are
which implies that for variables v1 , ..., vk occurring free in      generous (they are already powerful), so if they claim there
α: ∆ ⊢ ∀v1 , ..., vk , (α → ϕk ). But by assumption B, ∆ ⊢           is an assumption gap, then it is trustworthy.
∃v1 , ..., vk , ¬(α → ϕk ), so ∆ ⊢ ¬(∀v1 , ..., vk , (α → ϕk ))         Across our 92 proofs, the stage materializes 311 assump-
hence we prove False.                                                tions in total, of which 33 are marked as gaps and passed to
                                                                     the fill stage (11, 5, and 17 in Books I, II, and III respectively).
B.2    Assumption Gap Implementation Details
Recall the (optional) assumption gap tagging stage, which            B.3    Citation Gap
tries automated tactics to close the assumption. This section
goes into more detail, such as explaining the exact tactics to       A citation gap is a cited [Prop. B.N] that
close the assumption.                                                the Citation check cannot satisfy. We mark it
   The exact automated tactics tried are: rfl,                       with a -- @suppress_deps_check "reason" line
assumption, simp, linarith, nlinarith,                               above the sentence, which tells the checker script
euclid_finish, where euclid_finish is essen-                         (check_faithful.py) to skip that one citation. This
tially an SMT solver. These are tried one at a time in the           is needed in two cases: the citation is an actual mistake in the
order listed, and if none of them close the assumption, we           source edition (as explained in the main text), or it points to
mark it as a gap (@assumption_gap) and leave a sorry                 a proposition we skipped (one of the Book III propositions
placeholder.                                                         we leave out of scope; see Sec. H). We use 7 such tags across
   We justify this choice of measuring gaps since assump-            Book III.
-- BEFORE (map stage): step9 is left as ‘sorry‘ -- the missing κ1 ,. . . ,κt
  euclid_sentence "1.6.9" "The very notion (is) absurd [C.N. 5]."
    (step9 : False) := by sorry

-- AFTER (fill stage): the sorry is replaced by a call to the backing lemma, which supplies κ1 ,. . . ,κt .
  euclid_sentence "1.6.9" "The very notion (is) absurd [C.N. 5]."
    (step9 : False) := by euclid_apply (helper_1_6_step9 a b c d AB BC AC . . . )

theorem helper_1_6_step9 (a b c d : Point) (AB BC AC : Line)
    (hbda : between b d a) (hbdac : |(b-d)| = |(a-c)|)
    (hdbc_acb : ∠ d:b:c = ∠ a:c:b)
    (harea : Triangle.area △d:b:c = Triangle.area △a:c:b) . . . :
    False := by
  have hoff : ¬ c.onLine AB := by euclid_finish                                 -- one of the κi
  have hdec : Triangle.area △a:d:c + Triangle.area △c:d:b
                 = Triangle.area △a:c:b := by euclid_apply (sum_areas_if a b d c AB); assumption
  have hpos : 0 < Triangle.area △a:d:c := by euclid_finish
  have hsymm : Triangle.area △c:d:b = Triangle.area △d:b:c := by euclid_finish
  linarith

Figure 11: The fill stage on sentence 1.6.9 of Prop. 6. Before, the map stage leaves step9 as sorry, the placeholder for
the missing steps κ1 , . . . , κt . After, the body after being filled becomes := by euclid_apply (helper_1_6_step9
...)

      Skill                 Role                                           Example instruction (verbatim excerpt)
      faithful-split        Map stage, part 1: split the NL proof into     “Your ONLY job: take the raw English text of a Euclid
                            atomic assertions                              proposition and split it into atomic assertions. [. . . ] You do
                                                                           NOT translate to Lean, you do NOT look at any .lean
                                                                           file.”
      faithful-map          Map stage, part 2: turn each assertion into    “Your job: fill . . . a Lean claim type per sentence . . . one
                            a Lean claim type                              sentence at a time. [. . . ] RULE 0: THE SENTENCE IS
                                                                           THE CLAIM. [. . . ]”
      faithful-prove        Fill stage: main instructions to follow Or-    “prove each Euclid sentence’s step, IN ISOLATION, using
                            derDecompose                                   the recursive... . . . the SCRIPT does all wiring . . . you only
                                                                           ever write proof bodies and add have+backing-file decom-
                                                                           positions.”

Table 3: The agent skills (prompt files under .claude/skills/) and a verbatim excerpt of each one’s core instruction. The
map stage runs faithful-split then faithful-map; the fill stage then runs faithful-prove.


B.4    Generic Gap Implementation Details                                 these are simply what we judged to be a gap.
A generic gap is a gap in Euclid’s reasoning itself, distinct
from an assumption and citation gap. These surface when                             C     Human Evaluation Protocol
OrderDecompose cannot close a step and returns False:                     Reviewers used a custom web interface to evaluate
if the oracle agrees the step is a genuine gap rather than an M           anonymized pairs of formalizations. The interface supported
or mapping failure, we mark it with a -- @euclid_gap:                     the full review workflow, from an interactive tutorial to step-
<why> comment.                                                            fidelity scoring and final pairwise preferences. The review
    For example, Book III Prop. 35 says that if two straight-             itself proceeded in two stages.
lines AC and BD in a circle cut one another at E, the
                                                                          1. They rated the step fidelity of each formalization inde-
rectangle on the two pieces of AC equals the rectangle on
                                                                              pendently.
the two pieces of BD. Euclid proves two cases: both lines
pass through the centre, and neither line passes through the              2. They answered pairwise preference questions comparing
centre. He does not treat the remaining case, where one line                  the two anonymized formalizations.
passes through the centre and the other does not, even though                To ensure fairness, we compare only the for-
his hypotheses allow it. We add this missing case and tag the             mal Lean proofs, and remove any non-essential
site -- @euclid_gap. Across Book III we mark 17 such                      objects. That is, out of the output objects
generic gaps. None were marked in Book II and we do not                   ⟨ϕ̄, s̄, assumps(·), assert(·), formal(·)⟩ that Pistis cre-
claim any gaps in Book I as these were already found by                   ates, we remove s̄, assumps(·), assert(·), formal(·) from
(Murphy et al. 2024).                                                     the Lean file of our version, so we are only compar-
    Note ordinary System-E plumbing should not be consid-                 ing the proof ϕ̄. We do this in practice by replacing
ered a gap, and what truly constitutes a gap is subjective so             euclid_sentence with have and removing comments.
Figure 12: Bird’s-eye view of the completed Book I Prop. 6 artifact. In the codebase, these are interactive html artifacts
(map.html).


C.1    Step Fidelity                                              then reported pairwise preferences for mathematical trans-
The first rubric item reviewers were asked to rate is step        parency, textbook representation, and overall preference.
fidelity. This was rated on a 0–5 scale for each formalization.
Reviewers were asked to assess how well the Lean proof                                        D   LLM as a Judge
preserves the mathematical route of the textbook proof. The       Complementing the human study, we assess faithfulness with
full scoring rubric is shown in Tab. 5.                           an LLM-as-judge protocol using two judges: a closed model,
                                                                  Claude Opus 4.6 (whose radar is Fig. 4 in the main text), and
C.2    Pairwise Preferences                                       an open model, GLM-5 (Fig. 14). For each proposition the
For each proposition, reviewers answered three seven-tier         judge scores the formalization on five independent 0–5 di-
pairwise preference questions. The interface did not show         mensions, each defined by a strict rubric (Tab. 7): object cor-
numeric values: the center choice indicated no preference,        respondence, proof-step coverage, proof-structure fidelity,
and choices farther to either side indicated stronger prefer-     cited-dependency fidelity, and assumption/side-condition fi-
ence for one anonymized method. Tab. 6 summarizes the             delity.
three pairwise criteria.                                                      Pistis (Ours)       Baseline (LeanEuclid)     Baseline (Claude Code)

                                                                           OC                                OC                             OC
C.3    Evaluation Interface
                                                                  ASC                PSC           ASC                PSC         ASC                PSC
Fig. 13 illustrates the website used for the human-expert eval-
uation. Reviewers first completed an interactive tutorial that
introduced the task, the anonymized presentation, and the
available controls. For each proposition, the interface showed
                                                                   CDF               PSF            CDF             PSF            CDF               PSF
the textbook theorem and proof beside one formalization at
                                                                        (a) Book I                      (b) Book II                    (c) Book III
a time, so reviewers could compare the formal proof against
the natural-language argument without seeing the method           Figure 14: GLM-5 LLM-as-judge faithfulness by book (axes
identity. A live Lean server was available for querying proof     as in Fig. 4).
states and inspecting what each line establishes. After exam-
ining each formalization, reviewers assigned a step-fidelity        The full prompt given to each judge, which embeds the
score using the detailed 0–5 rubric shown in the interface,       shared five-dimension rubric of Tab. 7, is:
     Tool                              Purpose and Role in Faithfulness
     check_step.py                     The agent’s only build tool in Phase B. Implements SF/SP/P checks for each ϕ′i .
     check_step --context              Dumps exact hypotheses available at a proof node, showing context ∆ ∪ {ϕ′1 , . . . , ϕ′i−1 } for
                                       proving ϕ′i . Operationalizes InContext predicate (Alg. 1, line 5).
     find.py                           Declarative query interface over indexed database of System E axioms, definitions, and previously
                                       proven propositions. Agent uses it during CreateLemmas (Alg. 1) to locate relevant axioms,
                                       or propositions. An example is that agents can search for all formal statements that conclude a
                                       specific property.
     scaffold_step.py                  Generates boilerplate backing files for each ϕ′i left as sorry after mapping stage.

                    Table 4: Examples of custom Python tools provided to LLM agents during the filling stage.


  Score     Description                                                           textbook.
    0       The Lean proof does not represent the textbook                  Formal encoding overhead -- such as extra
            proof’s mathematical content.                                       type parameters (e.g.
    1       Only isolated textbook-like facts appear.                       requiring a Line object where the textbook
    2       Some essential steps are present, but important ob-                  just names two points),
            jects, constructions, dependencies, or conclusions              additional binders for type-checking,
            are missing or hidden.                                              imported helper lemmas whose
    3       The main route is recognizable, but there are notable           internals are not shown, or sentence-level
            omissions, compression, ordering issues, or unclear                  annotations -- is a routine
            automation.                                                     artifact of formalization in a proof
    4       The essential steps and dependencies are represented                assistant. Do not penalize a
            with only minor formal differences.                             formalization for these formal necessities
    5       The formalization closely preserves the textbook’s                  . Evaluate only whether the
            mathematical route in a readable and recoverable                mathematical content (objects, claims,
            way.                                                                proof steps, dependencies,
                                                                            assumptions) is faithful to the textbook.
        Table 5: Step-fidelity rubric shown to reviewers.
                                                                            You will score the formalization on 5
                                                                                independent metrics, each on a
 Metric                   Question                                          0-5 scale, using the rubric below.
 Mathematical trans-      Which formalization makes the mathe-
 parency                  matical argument more transparent and             [ RUBRIC -- the five-dimension scoring
                          easier to follow?                                     rubric ]
 Textbook representa-     Which formalization better represents
 tion                     the textbook proof?                               For each of the 5 metrics, provide a brief
 Overall preference       Which formalization is preferred over-                 justification (2-4
                          all for the proposition?                          sentences) citing specific parts of the
                                                                                Lean code and textbook proof.
                                                                            After all justifications, output your
Table 6: Pairwise preference criteria used in the human eval-                   final scores as five integers
uation.                                                                     (0-5) in angle brackets in the following
                                                                                order:
                                                                            <object_correspondence,
  You are an expert in Euclidean geometry,                                      proof_step_coverage,
      mathematical logic, and                                                   proof_structure_fidelity,
  formal verification in Lean 4.                                             cited_dependency_fidelity,
                                                                                 assumption_side_condition_fidelity>
  Your task is to evaluate how faithfully a                                 For example: <4, 3, 5, 4, 3>
      Lean formalization                                                    You MUST end your response with exactly
  represents the mathematical content of a                                      one set of angle brackets
      textbook proposition and                                              containing the five scores.
  proof from Euclid’s Elements. The textbook
       is the reference standard.                                           --- EVALUATION DATA ---
  You should not evaluate general elegance,                                 TEXTBOOK PROOF:      [ natural-language
      maintainability, proof                                                    proof ]
  brevity, annotation quality, or code style                                LEAN FORMALIZATION (Main file):      [
       except insofar as these                                                  Main.lean ]
  affect mathematical faithfulness to the                                   HELPER LEMMA FILES (backing proofs for
       each sentence-level step):                                           F    Compile Performance Details
        [ each stepN.lean, separated by --- ]                      The compile-time benchmark measures, per proposition,
                                                                   the wall-clock time to compile the faithful decom-
             E     Ablation Study Details                          posed proof (Book1/PropN) against the original proof
This section details precisely how the ablation experiment         (OldBook1/PropN) done by Murphy et al. (2024); both
was done. We compared the ablated arm, and full arm                prove the same proposition_N and differ only in struc-
(OrderDecompose) using the same model Opus 4.8.                    ture. The procedure is: (1) wipe .lake/build (the cached
Isolation: two worktrees, one arm at a time. Each                  Mathlib packages are left untouched, so Mathlib is never re-
arm runs in its own git worktree on its own branch, be-            built); (2) build SystemE once, untimed; (3) compile each
cause the arms require different repo contents: The ablated        proposition cold, one at a time, and record its wall-clock time,
branch removes the tools, hooks, and skills the full method        with a per-proposition 1-hour cap. SMT is left uncapped
(OrderDecompose) relies on, so the two cannot share a              (systemE.solverTime raised to 100000) so the 1-hour
working tree. We also never run the two arms concurrently          wall is the only cutoff, and both experiments were ran on
since models may update a memory file, so simultaneous runs        the same exclusive node (one after the other, not at the same
could cross-contaminate. Memory is wiped before every run          time). All runs used a single exclusive AMD EPYC 9634
and runs execute one arm at a time.                                (84-core) node.
                                                                      The ablation compile-time companion which eval-
Prevent Cheating. The answers (fully proven proposi-               uates the artifacts the ablated, and OrderDecompose
tions) exist in the git history, so agents could cheat. We could   created (Fig. 5b) follows the same procedure on an
deny the raw usage of git in settings.json, but there are          AMD EPYC 9754 (128-core) node. The drivers, hard-
ways an agent can get around this, so instead we tell the agent    ware metadata, and result CSVs are in the archive under
what it is not allowed to do, and check suspicious behavior        reproducable_experiments/compile_time/
after the agent is done.                                           (and /ablation_study/compile_time/).
   We specifically tell the agent that reading anything out-
side the repository or under the experiment folder, the eval               G     Further Refutation Examples
harness, or any use of git, auto-fails the attempt.                The main paper showed one example of a refuta-
The prompts, and why the comparison is fair. Crucially,            tion. The released code contains further examples under
the ablated arm is not handicapped by ignorance of what            LeanEuclidF/accept_refute/1.5/. Importantly,
it must produce: its prompt spells specifies how to output         it also contains a type B refutation example (only type A
things, and what it is or is not allowed to do (for example that   was shown in the main text).
it cannot change the original formal claim).                          Further, this folder contains example proofs that we accept
   The two task prompts are:                                       that differ from Euclid’s own proof, showcasing that there
  FULL (--my-method):                                              are various ways to proove the same statement, to which our
    Prove LeanEuclidF/<prop>/Main.lean end                         methodology can figure out which one to accept or refute
        to end using the                                           formally.
    /faithful-prove skill...

  ABLATED (--ablated):
                                                                                   H     Limitation Details
    Prove LeanEuclidF/<prop>/Main.lean --                          Skipped propositions. We complete 30 of the 37 proposi-
        fill every ’:= by sorry’ so                                tions of Book III. The remaining 7 (Props. 24, 26–31) each
    it builds with ZERO sorry. Do NOT change                       require extending the current implementation of System E
         the theorem statement, the                                with a new primitive: an arc-length (circumference) measure
    ’(stepN : ...)’ claim types, or the ’--                        for Props. 26–30, a circle-superposition rule for Prop. 24, and
        @assumption (...)’ lines.                                  a horn angle for Prop. 31. System E is prior work (Avigad,
    Anything Euclid cites must be cited in
        Lean too...
                                                                   Dean, and Mumma 2009), implemented in Lean by Murphy
                                                                   et al. (2024), and adding such primitives was decided to be
  SHARED (both arms):                                              out of scope.
    Do NOT read anything outside this                              Reliance on the oracle. Pistis is oracle-guided: a human
        repository, or under
    reproducable_experiments/. Do NOT use
                                                                   (or automated) oracle validates the Atomicity and Atomic
        git in any way. Either                                     Faithfulness of the map stage. While LLM oracle is a valid
    DISQUALIFIES the attempt -- AUTO-FAILED.                       option, the quality of proofs may degrade compared to using
         No gaming the eval.                                       a human oracle, which is a limitation of the current system.
                                                                   However, our methodology still minimizes human-oracle ef-
What the transcripts show. The ablated arm characteris-            fort so it is better than having the oracle complete the proof
tically fails by attempting the whole proof at once, running       fully. Nonetheless, reducing oracle use is a natural direction
a massive lake build, then rewriting files and re-firing           for future work.
another massive build. The full method instead decomposes
into small step lemmas built in fast scoped batches, making
steady in-order progress.
                          (a) Tutorial                                             (b) Textbook proof and formalization




                      (c) Live Lean query                                                (d) Step-fidelity scoring




                                                       (e) Pairwise preferences

Figure 13: Human-evaluation interface. Reviewers complete a tutorial, inspect each anonymized formalization against the
textbook proof, query a live Lean server, score step fidelity with the rubric available in the interface, and finally record pairwise
preferences across the three preference criteria.
 Score    Description
 (a) Object Correspondence
   0     Object mapping invalid. The main objects are mapped incorrectly, making the formalization about different geometric entities
         than the textbook.
   1     Major object-role errors. Several important objects or roles are confused, omitted, or swapped in ways that materially change
         the proposition or proof.
   2     Partial object correspondence. The principal objects are identifiable, but important constructed objects, incidences, angle
         vertices, side correspondences, or role assignments are wrong or ambiguous.
   3     Mostly correct object correspondence with notable issues. Most objects are mapped correctly, but there are nontrivial local
         mismatches, such as an incorrect orientation, a missing constructed object, or a questionable side/angle correspondence.
   4     Faithful object correspondence with minor formal differences. All central objects and roles match the textbook. Minor discrep-
         ancies are limited to harmless naming, orientation conventions, or formal encodings that preserve the mathematical content.
   5     Fully faithful object correspondence. Every relevant textbook object, including constructed objects and their roles, is represented
         by the corresponding Lean object or relation with no substantive mismatch.
 (b) Proof-Step Coverage
   0      Textbook proof not represented. The Lean proof does not contain the textbook’s essential proof strategy or steps, even if it proves
          a related result.
   1      Minimal overlap with textbook proof. Only isolated pieces of the textbook argument appear; most essential proof moves are
          absent or replaced by unrelated reasoning.
   2      Some central proof steps are present, but multiple essential steps are missing, bypassed, or replaced by substantially different
          mathematical arguments.
   3      Mostly covered with significant gaps. The Lean proof includes the main proof strategy and several essential steps, but one or
          more important steps are absent, compressed beyond recoverability, or only indirectly represented.
   4      Nearly complete step coverage. All essential textbook steps are present, with only minor omissions or compressions that do not
          change the mathematical proof strategy.
   5      Every essential mathematical step of the textbook proof is represented in the Lean proof, allowing for routine formal elaboration
          and harmless decomposition into sublemmas.
 (c) Proof-Structure Fidelity
   0      Incompatible proof structure. The formal proof follows a fundamentally different dependency structure from the textbook proof.
   1      Severe structural mismatch. The proof contains some textbook-like steps but combines or orders them in a way that changes the
          argument’s mathematical logic.
   2      Partial structural fidelity. The broad strategy is recognizable, but important dependencies, branches, or contradiction structure
          are missing, reversed, or replaced.
   3      Mostly faithful structure with notable deviations. The proof follows the textbook’s main dependency pattern, but one or more
          significant structural components are altered, hidden, or not justified in the same way.
   4      Faithful structure with minor formal differences. The proof preserves the textbook’s dependency structure. Differences are
          limited to formal necessities, such as making implicit cases explicit or splitting bundled steps into lemmas.
   5      Fully faithful structure. The proof’s mathematical dependencies match the textbook argument closely, including construction
          order, use of intermediate facts, branching, contradiction structure, and final conclusion.
 (d) Cited-Dependency Fidelity
   0      Cited dependencies ignored or replaced wholesale. The formal proof does not use the textbook’s cited mathematical dependencies
          or equivalent principles, and instead relies on unrelated results.
   1      Major dependency mismatch. Most important cited dependencies are absent, replaced by stronger later results, or used in ways
          that do not correspond to the textbook.
   2      Partial dependency fidelity. Some cited dependencies are represented, but several important ones are missing, mismatched, or
          replaced by non-equivalent principles.
   3      Mostly faithful dependencies with significant caveats. The main cited dependencies are present, but at least one important
          dependency is replaced by a stronger or less directly corresponding formal result.
   4      Faithful dependencies with minor formal substitutions. The proof uses formal analogues of the cited dependencies. Any
          substitutions are mathematically equivalent or are unavoidable due to the formal library’s organization.
   5      Fully faithful dependencies. Each cited textbook dependency is represented by a direct formal analogue or a clearly equivalent
          formal principle used at the corresponding mathematical point in the proof.
 (e) Assumption and Side-Condition Fidelity
   0     Unjustified assumptions central to the proof. The proof relies on assumptions or side conditions that are not in the textbook, not
         implied by the setup, and materially affect the result.
   1     Major assumption problems. Several important side conditions are unjustified, too strong, or inconsistent with the textbook
         configuration.
   2     Partial assumption fidelity. Some side conditions are justified, but important assumptions remain unsupported, stronger than
         what the textbook permits, or mathematically unclear.
   3     Mostly justified assumptions with notable concerns. Most added formal obligations follow from the textbook setup, but at least
         one nontrivial side condition is unjustified, uncertain, or requires a stronger reading of the textbook than warranted.
   4     Faithful assumptions with minor gaps. Added assumptions and side conditions are justified by the textbook setup or standard
         Euclidean background. Remaining issues are minor, local, or evidentially uncertain without threatening the proof’s mathematical
         faithfulness.
   5     Fully faithful assumptions and side conditions. Every formal side condition used by the proof is justified by the textbook
         statement, the constructed configuration, prior established facts, or accepted Euclidean background principles. This score is
         compatible with automation when the automated obligations are mathematically justified.

Table 7: The five-dimension rubric shown to the LLM judge. Each dimension is scored independently on the same 0–5 scale.
