                                          Not All Invariants Are Equal: Curating Training Data to Accelerate Program
                                                                    Verification with SLMs


                                                          Ido Pinto 1 Yizhak Yisrael Elboher 1 Haoze Wu 2 3 Nina Narodytska 3 Guy Katz 1


                                                                    Abstract                                 enough to prove the program’s correctness. Despite decades
                                                                                                             of research into symbolic methods such as Craig interpola-
                                              The synthesis of inductive loop invariants remains
                                                                                                             tion (McMillan, 2003) and constraint solving (Colón et al.,
arXiv:2603.15510v2 [cs.LG] 23 Jun 2026




                                              a critical bottleneck in automated program veri-
                                                                                                             2003; Gupta & Rybalchenko, 2009), finding inductive in-
                                              fication. While Large Language Models (LLMs)
                                                                                                             variants remains a challenging problem, and a practical
                                              show promise in mitigating this issue, they often
                                                                                                             bottleneck for modern verifiers.
                                              fail on complex programs, producing invariants
                                              that are invalid or computationally ineffective. Al-           The advent of Large Language Models (LLMs) has intro-
                                              though fine-tuning is a natural strategy to address            duced a new paradigm: generate-and-verify. Models such
                                              these limitations, obtaining high-quality training             as GPT-4 (OpenAI, 2023) and Claude (Anthropic, 2024)
                                              data remains an open challenge. We first for-                  have demonstrated an ability to hypothesize loop invari-
                                              malize the properties required for a high-quality              ants (Pei et al., 2023). Recent tools such as Loopy (Kamath
                                              training invariant, and then present W ONDA, a                 et al., 2024), Lemur (Wu et al., 2024b) and ACInv (Liu et al.,
                                              rigorous data curation pipeline that extracts such             2025) leverage this capability, wrapping LLMs in iterative
                                              invariants from raw verifier output via AST-based              refinement strategies that filter hallucinations using SMT
                                              normalization followed by LLM-driven semantic                  solvers.
                                              rewriting and augmentation with provable quality
                                                                                                             Despite this progress, a significant gap remains. As ob-
                                              guarantees. Fine-tuning Small Language Mod-
                                                                                                             served by Wei et al. (2025), while LLM-based verifiers
                                              els (SLMs) on W ONDA-curated data yields con-
                                                                                                             represent a promising direction, they do not yet offer a sig-
                                              sistent gains across the Qwen3, Llama-3.1, and
                                                                                                             nificant advantage over state-of-the-art symbolic tools, such
                                              Mistral families: the 4B and 8B Qwen3 models
                                                                                                             as UAutomizer, which do not leverage LLMs.
                                              nearly double invariant correctness and double
                                              speedup rates, while Llama-3.1-8B triples both.                Given these limitations, the natural question arises: can we
                                              On the challenging InvBench suite, the same 4B                 train an LLM that specializes in the task of invariant gen-
                                              model outperforms an off-the-shelf model 20× its               eration? Such specialization is standard practice in many
                                              size and matches the end-to-end verification time              domains and has proven successful. Indeed, within the
                                              of GPT-OSS-120B, while a 14B Qwen3 model                       program verification literature, this specific problem has
                                              matches that of the frontier model GPT-5.2, all                received increasing attention (Pei et al., 2023; Wei et al.,
                                              without test-time compute overhead. Our code is                2025). However, the success of these training efforts has
                                              publicly available on GitHub.                                  only been partial. Recent work on fine-tuning invariant
                                                                                                             generation models reports improvements on easy verifica-
                                                                                                             tion problems, yet achieving significant speedups on hard
                                         1. Introduction                                                     benchmarks remains elusive (Wei et al., 2025). We argue
                                                                                                             that data quality, rather than model scale alone, is the key
                                         Automated program verification is a powerful technique for          bottleneck for current neural invariant synthesizers. Exist-
                                         ensuring the reliability of critical software infrastructure.       ing datasets (Wei et al., 2025) rely on raw outputs from
                                         At the core of deductive verification lies the challenge of         symbolic tools (e.g., UAutomizer (Heizmann et al., 2013)),
                                         loop invariant synthesis: identifying a logical property that       which suffer from two limitations:
                                         is preserved across every iteration of a loop and is strong
                                             1
                                               Hebrew University of Jerusalem, Israel 2 Amherst Col-           1. Low Pedagogical Value: Solver-generated invariants
                                         lege, USA 3 VMware Research by Broadcom, USA. Correspon-                 are often technically correct but structurally obfuscated
                                         dence to: Ido Pinto <ido.pinto@mail.huji.ac.il>, Guy Katz
                                         <g.katz@mail.huji.ac.il>.                                                (see Figure 1), and each output reflects only one valid
                                                                                                                  choice among many for the same program. As a result,
                                         Preprint. June 24, 2026.                                                 models may learn verifier-specific artifacts, rather than

                                                                                                         1
                                                  Not All Invariants Are Equal

     the underlying program logic or the broader space of              ((((((((((((((((((( 1 <= weight1 ) && (((( long long
     useful invariants.                                                ) weight1 + weight2 ) + 1 ) <= max threshold )) && (
                                                                       weight2 <= 10 )) && ( 20 <= (( int128 ) (( long long )
                                                                       weight1 * 14 ) + cumulative weight )))) && ( weight1 <=
  2. Dependence on Solver Outputs: When training relies                10 ) && ( count <= 4 )) && ( 1 <= weight2 )) && (( long
     heavily on solver-generated data, the model may inherit           long ) weight1 + weight2 <= cumulative weight )) || ...
                                                                       || (((((((( 1 <= weight1 ) && (((( long long ) weight1 +
     the solver’s biases, making it harder to improve beyond           weight2 ) + 1 ) <= max threshold )) && ( count <= 5 ) &&
     the current symbolic state-of-the-art.                            ( weight2 <= 10 )) && ( weight1 <= 10 )) && ( 20 <= ((
                                                                        int128 ) cumulative weight + (( long long ) weight1 *
                                                                       13 )))) && ( 1 <= weight2 )) && (( long long ) weight1 +
To mitigate these limitations, we introduce W ONDA, a rig-             weight2 <= cumulative weight )))

orous data curation pipeline. Instead of directly training                            3084 chars, 75 conjuncts, 11 disjuncts
on verifier-generated invariants, W ONDA explicitly opti-
mizes for learnability. We employ Abstract Syntax Tree                Figure 1. Example of a raw verbose invariant generated by UAu-
(AST) normalization to clean the structural representation            tomizer. W ONDA transforms such outputs into more compact,
                                                                      learnable forms.
of invariants. We further implement an LLM-driven se-
mantic rewriting and augmentation engine that transforms
obscure machine-generated invariants into concise, inter-
pretable forms, simplifying their logical semantics while             loop invariants from proofs of unsatisfiability in bounded
maintaining soundness. Augmentation generates multiple                model checking traces. Tools like UAutomizer (Heizmann
candidate rewrites per input, so the model is not limited             et al., 2013) and Eldarica (Hojjat & Rümmer, 2018) build
to the single invariant the solver originally produced. To            on these approaches. A separate line of work casts invari-
ensure soundness, we use a formal verification tool to val-           ant generation as a constraint-satisfaction problem solved
idate invariants after any transformation step that may not           with off-the-shelf solvers (Colón et al., 2003; Gupta & Ry-
preserve correctness.                                                 balchenko, 2009; Fedyukovich & Bodı́k, 2018). Finally,
                                                                      dynamic analysis tools like Daikon (Ernst et al., 2007) in-
Our Contributions.                                                    fer likely invariants by observing program execution traces;
                                                                      while efficient, dynamic methods are unsound, as they can
  1. We demonstrate that directly fine-tuning invariants gen-         only guarantee correctness for the observed executions.
     erated by symbolic solvers does not reliably improve             Learning-based Invariant Synthesis. Early techniques for
     model performance and can even degrade it.                       data-driven invariant synthesis relied on decision trees (Garg
  2. We propose W ONDA, a rigorous data curation frame-               et al., 2016), algebraic inference (Sharma et al., 2013), and
     work that combines AST normalization with LLM-                   Horn-ICE learning (Ezudheen et al., 2018). Pei et al. (2023)
     driven semantic rewriting and augmentation, transform-           explored fine-tuning LLMs for invariant prediction, train-
     ing raw, obfuscated symbolic outputs into high-quality           ing on Daikon (Ernst et al., 2007) outputs. With the rise
     training signals while preserving soundness.                     of code-capable LLMs, more recent frameworks employ
                                                                      iterative generate-and-verify loops, using symbolic solvers
  3. We present a thorough experimental evaluation across             to filter or refine LLM proposals: Loopy (Kamath et al.,
     the Qwen3, Llama-3.1, and Mistral model families,                2024) applies Houdini-based filtering of LLM-generated
     showing that W ONDA-curated data lets small fine-                candidates, LaM4Inv (Wu et al., 2024a) iteratively queries
     tuned models match much larger and frontier mod-                 the LLM and uses BMC to filter and reassemble candidate
     els on end-to-end verification time, without test-time           predicates across rounds, LEMUR (Wu et al., 2024b) in-
     compute overhead.                                                troduces backtracking to repair invalid invariants. Related
                                                                      directions include contrastive ranking (Chakraborty et al.,
                                                                      2023), C++ class invariants (Sun et al., 2025), and complex
2. Related Work                                                       loop structures (Liu et al., 2025).
Traditional Invariant Synthesis. Invariant synthesis has              Fine-tuning for Invariant Synthesis. Fine-tuning LLMs to
been extensively studied through various formalisms. Ab-              propose a single invariant, subsequently verified by a sym-
stract Interpretation (Cousot & Cousot, 1977) gave rise               bolic solver, has received increasing attention. Unlike Pei
to techniques for discovering specific classes of invari-             et al. (2023), who train on Daikon outputs without formal
ants, such as affine relationships (Karr, 1976) and linear            verification of the generated invariants, Wei et al. (2025)
restraints (Cousot & Halbwachs, 1978) among variables.                introduce a one-shot setting using UAutomizer-generated
Model Checking (Clarke et al., 2018) and Predicate Abstrac-           training data, which is formally correct but, as we show,
tion (Flanagan & Qadeer, 2002; Lahiri & Bryant, 2007) infer           structurally noisy (see Figure 1). We adopt the same evalua-
invariants by refining abstract states based on a set of predi-       tion framework and focus on improving training data quality
cates, while Craig Interpolation (McMillan, 2003) generates           and diversity, producing more compact and generalizable

                                                                  2
                                                    Not All Invariants Are Equal

   Input Query: ⟨A, P, q⟩ where A = {p}
                                                                    Baseline: V(A, P, q)
   int x = 0;
                                                            int x = 0;
   int y = 100;
                                                            int y = 100;
   assume(x == 0 && y == 100); ▷ p
                                                            assume(x == 0 && y == 100); ▷ p
   while (y > 0) {
                                                            while (y > 0) {                                         tb
     // Location l
                                                              x += 3;
     x += 3;
                                                              y -= 5;
     y -= 5;
                                                            }
   }
                                                            assert(x > y); ▷ q
   assert(x > y); ▷ q




                                    Correctness Check: V1 = V(A, P, I)      Sufficiency Check: V2 = V(A ∪ {I}, P, q)
                  LLM      tm

         I = (l, 5x + 3y == 300)
                                                                               int x = 0;
                                   int x = 0;
                                                                               int y = 100;
                                   int y = 100;
                                                                               assume(x == 0 && y == 100); ▷ p
                                   assume(x == 0 && y == 100); ▷ p
                                                                               while (y > 0) {
                                   while (y > 0) {
                                                                                 assume(5*x + 3*y == 300); ▷ I           t2
                                     assert(5*x + 3*y == 300); ▷ I
                                                                                 x += 3;
                                                                                                                               VBS
                                     x += 3;
                                                                                 y -= 5;
                                     y -= 5;
                                                                               }
                                   }
                                                                               assert(x > y); ▷ q



                                                                                   t1

Figure 2. Illustration of the VBS metric. Given a query ⟨A, P, q⟩, the LLM proposes invariant I = (l, φ) with inference latency tm .
V1 and V2 run in parallel alongside the baseline V(A, P, q), with tv = max(t1 , t2 ). VBS selects min(tv , tb ) if I is correct and the
decomposed checks yield a conclusive result (per Table 1), and falls back to tb otherwise. For the end-to-end metric VBPE2E , tm is added
to tv for sufficient instances.


invariants. The one-shot and iterative directions are com-             correctness and use the terms interchangeably; if the predi-
plementary: while iterative tools such as Lemur (Wu et al.,            cate additionally satisfies sufficiency, it constitutes a formal
2024b) and Loopy (Kamath et al., 2024) refine invariants               proof of the postcondition q.
over multiple LLM calls, a stronger one-shot generator pro-
vides better initialization for such loops.                            Running Example. We illustrate these concepts using the
                                                                       program shown in Figure 2 (top-left block). The program
3. Preliminaries                                                       initializes x = 0 and y = 100 (the precondition p), then
                                                                       repeatedly increments x by 3 and decrements y by 5 until
We ground our approach in Hoare logic (Hoare, 1969), a                 y ≤ 0. The verification goal is to prove the postcondition
seminal framework for reasoning about program correctness.             q ≡ x > y. We claim that the candidate invariant I ≡
A Hoare triple {p} S {q} asserts that if precondition p holds          5x+3y = 300 satisfies these criteria. It is inductive because
before executing statement S, then postcondition q holds               it holds initially (5(0) + 3(100) = 300) and is preserved
afterward. While sequential statements are straightforward             by the loop body updates: assuming I holds, the new state
to compose, loops pose a fundamental challenge: they may               satisfies 5(x + 3) + 3(y − 5) = 5x + 15 + 3y − 15 =
execute for an unbounded number of iterations, requiring               5x+3y = 300. Furthermore, the invariant is sufficient: upon
an auxiliary predicate, a loop invariant, to enable finite             loop termination, ¬B ≡ y ≤ 0 combined with I implies
reasoning.                                                             5x+3y = 300∧y ≤ 0. Substituting, 5x = 300−3y ≥ 300
                                                                       (since −3y ≥ 0), so x ≥ 60. As x ≥ 60 > 0 ≥ y, the
For a loop while B do S with precondition p and post-
                                                                       postcondition q ≡ x > y follows.
condition q, a valid invariant I must satisfy: (i) Initia-
tion: p ⇒ I, meaning the invariant holds upon loop en-
try; (ii) Consecution: {I ∧ B} S {I}, meaning the invari-              3.1. Program Verification
ant is preserved by each iteration; and (iii) Sufficiency:             Let P denote a program, let Loc(P ) denote its set of pro-
I ∧ ¬B ⇒ q, meaning that upon termination, the invari-                 gram locations, and let L(P ) ⊆ Loc(P ) denote its loop
ant implies the postcondition. A predicate satisfying both             entry locations.
initiation and consecution is termed an inductive invari-
                                                                       Definition 3.1 (Property). A property is a pair (l, φ), where
ant. Throughout this paper, we refer to this property as
                                                                       l ∈ Loc(P ) and φ is a predicate over the variables of pro-

                                                                   3
                                                  Not All Invariants Are Equal

gram P . For a given execution of P , a property holds, or is         guaranteed to be correct (Wei et al., 2025). This approach
satisfied, if φ holds, whenever P reaches line l.                     augments the verification problem with new knowledge that
Definition 3.2 (Verification Query). A verification query             can be useful to prove the desired property. The correctness
is a triple ⟨A, P, q⟩ where P is a program, q is a property           and sufficiency checks are independent and can therefore be
(the postcondition), and A is a set of properties representing        performed in parallel, and in the case where both queries are
preconditions.                                                        simpler than the original query, the wall-clock verification
                                                                      time is reduced.
Definition 3.3 (Verification Query Validity). A verification
query ⟨A, P, q⟩ is valid if every execution of P that sat-            Table 1. Decision procedure for verification queries using a candi-
isfies the (precondition) properties in A also satisfies the          date invariant. Note that a FALSE outcome in the sufficiency check
postcondition q.                                                      implies the original query is invalid regardless of the invariant’s
                                                                      correctness.
Definition 3.4 (Verification Oracle). A verification oracle
V takes a verification query ⟨A, P, r⟩ and returns:                         V1 (Correctness)     V2 (Sufficiency)     Outcome
                                                                                  T RUE               T RUE            T RUE
        V(A, P, r) ∈ {T RUE, FALSE, U NKNOWN}                                       ∗                 FALSE            FALSE
                                                                                          otherwise                  U NKNOWN
where T RUE indicates the query is valid, FALSE indicates
a counterexample exists, and U NKNOWN indicates the or-
acle could not determine the result (e.g., due to timeout or          An illustration of the approach appears in Figure 2. Instead
inherent incompleteness). Here, we consider only sound                of directly verifying the query (Baseline block, top-right),
oracles: if V(A, P, r) = T RUE, then the query is valid; if           we can use the invariant I = (l, 5x + 3y = 300) and verify
V(A, P, r) = FALSE, then a counterexample exists.                     its correctness (Correctness Check block, bottom-left) and
                                                                      sufficiency (Sufficiency Check block, bottom-right). When
Verification queries use assume(φ) and assert(φ)                      the verifier returns T RUE for both of these queries, we can
statements. assume(φ) at line l restricts traces to                   immediately deduce the safety of the program.
those satisfying φ (equivalent to if (¬φ) halt), while
                                                                      Generating Invariants. The effectiveness of the aforemen-
assert(φ) jumps to ERROR if violated (equivalent to if
                                                                      tioned techniques is conditional upon our ability to generate
(¬φ) goto ERROR). For query ⟨A, P, q⟩, we annotate
                                                                      useful invariant candidates, i.e., candidates that will allow us
P with assume(φ) for each (l, φ) ∈ A and assert(φ)
                                                                      to reach a T RUE/FALSE outcome, as per Table 1. We define
where q = (l, φ). P is safe with respect to the verification
                                                                      the invariant generation task, which is the primary focus of
query if and only if ERROR is unreachable.
                                                                      this work, as follows: given a verification query ⟨A, P, q⟩, a
                                                                      verification oracle V, and a designated loop entry l ∈ L(P ),
3.2. Program Verification using Invariants
                                                                      the objective is to synthesize a predicate φ such that the
Given a verification query ⟨A, P, q⟩, the task can be                 resulting property I = (l, φ) satisfies the correctness and
addressed through a direct invocation of the verifier:                sufficiency checks; i.e., V returns T RUE for the correspond-
V(A, P, q). Alternatively, we can break the problem into              ing correctness and sufficiency queries. We also regard a
sub-problems, by introducing a candidate invariant prop-              correct candidate whose sufficiency check returns FALSE as
erty I = (l, φ), where l ∈ L(P ). This approach splits the            desirable, since this witnesses a genuine bug in P .
verification task into two distinct queries:
                                                                      4. Methodology
  1. Correctness Check (V1 ): Verify that the property I
     is correct (inductive) within the program P given A:             The main component of the generate-and-verify paradigm
     V1 := V(A, P, I)                                                 is the LLM that performs invariant synthesis. In practice,
                                                                      off-the-shelf LLMs are not very effective at this task and
  2. Sufficiency Check (V2 ): Verify that the target postcondi-       need to be fine-tuned for the invariant generation domain.
     tion q holds, assuming the correctness of the candidate          Somewhat counterintuitively, fine-tuning on data produced
     invariant I: V2 := V(A ∪ {I}, P, q)                              by modern verification tools does not show a performance
                                                                      boost on challenging problems (Wei et al., 2025). We ar-
We denote by tb the wall-clock time of direct verification            gue that fine-tuning can in fact be quite useful, provided
V(A, P, q), and by tv = max(t1 , t2 ) the parallel execution          the training data is of high quality. To this end, we investi-
time of the correctness and sufficiency checks, where t1 and          gate two research questions: (a) how to define high-quality
t2 are their respective solving times.                                training data in this context; and (b) how to produce it.
The final outcome is determined by Table 1. This proce-               Given a verification query ⟨A, P, q⟩, a verification oracle
dure is sound; conclusive outcomes (T RUE or FALSE) are               V and loop locations L(P ), our goal is to produce training

                                                                  4
                                                    Not All Invariants Are Equal

         V0 : Raw Verifier Output
                                                           V1 : Normalized
  (((((((((((((((((((((( 36 <= y )
  && ( 36 <= x ))                                    36 <= y && 36 <= x                                              V2 : Simplified
    || (( 21 <= y ) && ( 45 <= x )))                 || 21 <= y && 45 <= x
    || (( 21 <= x ) && ( 65 <= y )))                 || 21 <= x && 65 <= y
    || (( 42 <= x ) && ( 26 <= y )))    normalize    || 42 <= x && 26 <= y                            simplify
    || (( 12 <= x ) && ( 80 <= y )))                 || 12 <= x && 80 <= y                  LLM                  5*x + 3*y == 300
    || (( 11 <= y ) && ( 51 <= x )))                   .
                                                       .
    .                                                  .
    .
    .                                                || 16 <= y && 48 <= x                                           18 chars, 1 equation
    || (( 16 <= y ) && ( 48 <= x )))
                                                           441 chars, 21 disjuncts
            603 chars, 21 disjuncts


Figure 3. W ONDA pipeline. The raw verifier output (V0 ) is normalized (V1 ), then an LLM simplifies it to a compact closed-form
expression (V2 ): 5x + 3y = 300, achieving a 2x verification speedup.


samples that pair programs with high-quality loop invariants.             4.1. Invariant Normalization
We claim that a good invariant I = (l, φ) should satisfy the
                                                                          Raw invariants from automated verifiers are often clut-
following characteristics:
                                                                          tered with syntactic noise that obscures underlying program
  1. Non-Degeneracy: we exclude trivial invariants φ ∈                    logic. This noise typically manifests as: (i) tautological
     {FALSE, T RUE}.                                                      clauses (e.g., n <= n); (ii) redundant parenthesization,
                                                                          and (iii) excessive integral type casts (e.g., int128 and
  2. Correctness: invariant φ holds at location l on all exe-             long long) used for bit-precise semantics. In rare cases,
     cutions, i.e., V(A, P, I) = T RUE.                                   verifiers may even produce contradictions within unreach-
  3. Usefulness: using I expedites verification times. This               able or dead-code paths, such as (x > x), which can
     entails sufficiency, i.e., V2 = T RUE, and that tv < tb ,            confuse models during training.
     where tv and tb are as defined in Section 3.2.                       We apply a semantic-preserving AST normalization, N OR -
                                                                          MALIZE, which performs a single bottom-up traversal using
  4. Compactness: invariant I has a succinct syntactic form,
     which we hypothesize facilitates learning and improves               the rules in Table 2. It also strips the invariants of any unnec-
     generalization.                                                      essary parentheses, based on standard C operator precedence
                                                                          rules.
Grounding to Verifier-Generated Invariants. Following
                                                                          Table 2. Rewrite rules applied during AST normalization. e
Wei et al. (2025), we initialize our curation process using
                                                                          represents a numeric variable, φ a predicate, c a constant, and
invariants extracted from UAutomizer. When UAutomizer                     ▷◁∈ {≤, ≥, =, <, >, ̸=} a relational operator.
proves a verification query ⟨{p}, P, q⟩, it emits discovered
invariants {(l, φraw )} as part of its proof. These invariants                Rule             Transformation
satisfy correctness by construction. However, they are not                    Tautology Elimination
guaranteed to be useful (they may not provide speedup) or                     TAUT C ONJ       φ ∧ true or true ∧ φ −→ φ
compact (they often contain tool-specific artifacts). Figure 1                TAUT R EFL       e ▷◁ e −→ true for ▷◁∈ {≤, ≥, =}
depicts an example: while correct, the raw invariant is clut-                 TAUT C ONST      c1 ▷◁ c2 −→ true if c1 ▷◁ c2 holds
tered with type casts and verbose structure, making it a poor                 Contradiction Propagation
training target.                                                              C ONTRAC ONJ φ ∧ false or false ∧ φ −→ false
                                                                              C ONTRA D ISJ    φ ∨ false or false ∨ φ −→ φ
We address these issues with a two-stage pipeline:                            C ONTRA R EFL e ▷◁ e −→ false for ▷◁∈ {<, >, ̸=}

  1. Invariant Normalization (§4.1): AST-based rewriting
     that removes tautologies, contradictions, minimizes                  Proposition 4.1 (Normalization Soundness). For any predi-
     parentheses and strips redundant type casts.                         cate φ, the normalized predicate φ′ = N ORMALIZE(φ) is
                                                                          semantically equivalent to the original (φ′ ≡ φ).
  2. LLM-Based Simplification (§4.2): A data augmentation
     step where an LLM generalizes verbose invariants into
     compact candidates, each verified for correctness and                Proof. The rewrite rules implement standard first-order
     usefulness.                                                          logic identities applied inductively via bottom-up AST
                                                                          traversal. The parenthesis minimization follows the C op-
Figure 3 illustrates output produced by our pipeline. An-                 erator precedence while preserving associativity and bind-
other example appears in Figure 6 (Appendix A).                           ing.

                                                                     5
                                                      Not All Invariants Are Equal

As an additional optimization step, we eliminate integral                   Overall, our strategy encourages semantic abstraction over
casts to reduce clutter. While stripping casts can break                    syntactic rewriting; for the full prompt, see Appendix B.2.
soundness (e.g., under certain overflow conditions), we pri-                Definition 4.2 (Quality Grade G). To measure the utility
oritize logical clarity for model training and formally verify              of a candidate φ′ with respect to a verification query Q =
the final generated invariants against the original program                 ⟨A, P, q⟩ and baseline time tb , we define a grading function
to ensure correctness is maintained.                                        G(φ′ , Q, tb ) ∈ {0, 1, 2, 3} based on V1 , V2 checks defined
                                                                            in §3.2.
4.2. LLM-Based Invariant Simplification
                                                                                             
                                                                                               0 V1 ̸= T RUE
AST normalization removes syntactic noise, but many invari-                                  
                                                                                             
                                                                                             
                                                                                             1 V = T RUE ∧ V ̸= T RUE
ants remain verbose due to semantic complexity: enumer-                     G(φ′ , Q, tb ) =
                                                                                                      1              2
ated cases, redundant bounds, or overly strong constraints.                                  
                                                                                             
                                                                                              2    V 1 =  T RUE ∧ V 2 = T RUE ∧ tv ≥ tb
These patterns require reasoning beyond local rewrites. To                                   
                                                                                               3 V1 = T RUE ∧ V2 = T RUE ∧ tv < tb
bridge this gap, we employ an LLM as a simplification
function fθ : Φ → ΦN , where Φ is the set of possible predi-                where tv = max(t1 , t2 ) and tb are as defined in Section 3.2.
cates and N is the number of generated candidates. Unlike                   The full grading procedure is given in Algorithm 1 (Ap-
the rules in Table 2, fθ is not guaranteed to be semantics-                 pendix C). Syntactically invalid candidates are discarded
preserving (fθ (φ) ̸≡ φ). Instead, we leverage the LLM’s                    before grading. We retain candidates with G(φ′ , Q, tb ) ≥ 2
ability to perform abstraction, aiming for candidates that are              as “golden” training samples.
more compact yet still sufficient to prove property q. The
resulting predicate can be equivalent, stronger, weaker or                  The simplification procedure is given in Algorithm 2
incomparable with the original predicate; this does not jeop-               (Appendix C). It first discards degenerate invariants, i.e.,
ardize soundness, as we later invoke the verifier to ensure                 φnorm ∈ {FALSE, T RUE}. Otherwise, if the invariant is
the correctness and sufficiency of the rewritten predicates.                deemed verbose (in our implementation, if |φnorm | > η for
                                                                            a threshold η > 0), an LLM generates N candidates. These
                                                                            candidates are deduplicated by exact match, filtered again
Simplification Procedure. To guide the LLM toward                           for degeneracy, and each is graded using Algorithm 1; we
high-quality invariants, we provide a prompt context C =                    retain those with grade g ≥ 2 as pairs (φ, g). If no candidate
⟨P, φ, G⟩ containing the program P , the reference invariant                qualifies (or if φnorm is not verbose), we instead grade φnorm
φ, and a set of transformation goals G. The following trans-                itself.
formation goals capture our main insights for achieving the
desired characteristics of compactness and usefulness.                      Proposition 4.3 (Pipeline Soundness). If the pipeline out-
                                                                            puts (l, φ∗ ), then φ∗ is a correct loop invariant sufficient to
Range generalization. We observed that a large number                       prove q.
of raw invariants
           Wk       have a case-enumeration structure; for
example, i=1 (x = i) might come from a loop that runs                       Proof. By construction, φ∗ is returned only if it passes
for k steps. We prompt an LLM to simplify such invariants                   the formal verifier’s correctness check (V1 = T RUE) and
into a more compact range invariant, 1 ≤ x ≤ k, which is                    sufficiency check (V2 = T RUE).
easier to learn than the enumeration representation.
Constraint factoring. Some invariants form Boolean expres-                  5. Experimental Setup
sions that have unnecessarily complex logical structure, e.g.,
(a ∧ b1 ) ∨ . . . ∨ (a ∧ bk ). We encourage an LLM to perform               Training Dataset. We fine-tune on raw verifier-generated
logical simplification, e.g., rewrite this as a ∧ (b1 ∨ . . . ∨ bk ).       invariants extracted from training programs released by Wei
                                                                            et al. (2025). We run UAutomizer to verify each program
Closed-form discovery. Often, we would like to generalize                   and collect loop invariants from its output; we denote this
the normalized invariant to replace case enumerations with                  raw collection V0. AST-based normalization yields V1,
arithmetic relations, where linear expressions are preferred                and LLM-driven simplification (Kimi K2 Thinking (Team
for solver efficiency, though non-linear closed forms are                   et al., 2025), N =4 candidates per verbose invariant, where
also possible. This gives us compact, reusable invariants                   η = 20 characters) followed by verifier filtering yields V2.
                                      Pn
that are easier to learn; for example, i=1 i → n(n+1)
                                                    2   .                   Retaining only g ≥ 2 candidates for fine-tuning yields 7,284
Redundancy removal. Some expressions are implied by                         samples, partitioned 80/20 into train and validation. Full
program semantics and hold throughout the program, e.g.,                    pipeline yield and dataset statistics are in Appendix D.
preconditions or variables with fixed values. To simplify
them, we can remove these redundant clauses to obtain more
compact and easier-to-learn invariants.

                                                                        6
                                                      Not All Invariants Are Equal

Evaluation Dataset. For evaluation, we use InvBench,                   set. We also define the speedup factor:
a benchmark of C verification queries derived from SV-                                (i) (i)
COMP (Beyer & Strejcek, 2025), released by Wei et al.                                tb /tv
                                                                                                 if C ORRECT(i) ∧
(2025). Starting from 219 programs, we expand multi-loop                     S(i) =                  Di ∈ {T RUE, FALSE}
programs into per-loop instances, yielding 362 total. We par-                        
                                                                                     
                                                                                        1         otherwise
tition these into Easy (n = 239, 66%) and Hard (n = 123,
34%) using a 15-second UAutomizer baseline threshold,
focusing on Hard instances where invariants provide mean-              We report S̄>1 as the mean speedup factor among instances
ingful speedup; 20 Hard instances time out (Appendix E).               with S PEEDUP(i) = 1.
                                            (i)
Each instance in D = {(pi , Pi , qi , li , tb )}ni=1 comprises a       Virtual Best Solver. The verification procedure described
precondition pi , program Pi , postcondition qi , loop loca-           in Section 3.2 is designed to run as part of a portfolio, in
                                                   (i)
tion li ∈ L(Pi ), and median baseline time tb over k = 3               parallel to direct verification: the LLM proposes an invariant
runs. Models are prompted with a structured JSON format                while the baseline verifier runs concurrently, and whichever
(Appendix B.1); syntactically invalid, ill-formed, or outputs          finishes first determines the outcome. The Virtual Best
using side-effect operators (e.g., ++, + =, =) receive ver-            Solver (VBS) metric captures this by selecting the faster
dict U NKNOWN. UAutomizer configuration, and hardware                  strategy per instance (cf. Figure 2):
used for evaluation are detailed in Appendix G.
                                                                                                (i) (i)
                                                                                      
Models. We evaluate three open model families. From                                   min(tv , tb ) if C ORRECT(i) ∧
                                                                                      
Qwen3 (Yang et al., 2025) we use Qwen3-0.6B, Qwen3-                      VBS(i) =                            Di ∈ {T RUE, FALSE}
4B-Instruct-2507, Qwen3-8B, and Qwen3-14B (referred                                    (i)
                                                                                      
                                                                                        tb                 otherwise
to as Qwen3-0.6B/4B/8B/14B); we also use Llama-3.1-8B-
Instruct (Grattafiori et al., 2024) and Mistral-7B-Instruct-
                                                                       The Virtual Best Performance VBP = n1 i VBS(i) mea-
                                                                                                                 P
v0.3 (Jiang et al., 2023), referred to as Llama-3.1-8B and
Mistral-7B. All models are fully fine-tuned except Qwen3-              sures the average verification time achievable by optimally
8B, which uses LoRA (Hu et al., 2022) (Appendix F). As                 combining LLM invariants with baseline direct verification.
off-the-shelf baselines, we compare against Qwen3-Next-                Note on Model Latency. Our primary metrics (Rspeedup ,
80B-A3B-Instruct (referred to as Qwen3-80B), GPT-OSS-                                                                 (i)
                                                                       S̄>1 , and VBP) exclude inference latency tm to isolate
120B (Agarwal et al., 2025), and GPT-5.2 (OpenAI, 2025).               model capability from deployment factors. For end-to-end
The Qwen3-0.6B, 8B, and 14B models are trained and eval-                                                                  (i)    (i)
                                                                       cost, we additionally report VBPE2E , which adds tm to tv
uated in non-thinking mode.                                                                                          (i)   (i) (i)
                                                                       for sufficient instances. : VBSE2E (i) = min(tv +tm , tb ).
Decision Procedure. For valid candidates, we apply the
procedure from §3.2, executing two queries in parallel:

    (i)                                                                6. Results and Analysis
  V1 = V({pi }, Pi , (li , φ̂i ))         (Correctness Check)
    (i)                                                                Benefits of W ONDA. Table 3 depicts our main results
  V2 = V({pi , (li , φ̂i )}, Pi , qi )    (Sufficiency Check)          on the hard split. Across all open-model scales, V2 cura-
                                                                       tion significantly boosts performance relative to the corre-
                          (i)       (i)
with wall-clock times t1 and t2 , respectively. Since both             sponding base. Qwen3-4B-V2 more than doubles its base
                                                       (i)
queries execute in parallel, the verification time is tv =             model’s speedup rate and nearly doubles its correctness,
      (i) (i)                                                          with VBPE2E falling from 185.7 s to 165.7 s. Qwen3-8B-
max(t1 , t2 ). The outcome Di is determined by Table 1.
                                                                       V2 shows the same pattern, Llama-3.1-8B-V2 triples base
Evaluation Metrics. We define binary indicators for each               correctness (14.9% → 45.5%), and Mistral-7B-V2 more
instance i:                                                            than doubles its speedup rate (7.3% → 16.0%). Qwen3-
                                                                       14B-V2 achieves the best VBP among our models (162.1 s),
  1. VALID(i) = 1 iff syntactic validation passes;                     matching GPT-5.2 on VBPE2E (162.9 s vs. 163.4 s). VBP
                                                                       improves by up to 16.0% (∼31 s) over direct verification
                                                (i)
  2. C ORRECT(i) = 1 iff VALID(i) and V1 = T RUE;                      alone across all families. All fine-tuned Qwen3 models
                                                                       at 4B parameters and above, as well as Llama-3.1-8B-V2,
                                                                       outperform the off-the-shelf Qwen3-80B on both correct-
  3. S PEEDUP(i) = 1 iff C ORRECT(i),
                               (i)    (i)                              ness and VBPE2E , with Qwen3-4B-V2 the most notable
     Di ∈ {T RUE, FALSE}, and tv < tb .                                given it is ∼20× smaller; it also matches GPT-OSS-120B
                                                                       on VBPE2E (165.7 s vs. 167.6 s). Figure 4 summarizes
We report the mean of each indicator across the evaluation             these comparisons visually.

                                                                   7
                                                                        Not All Invariants Are Equal

Table 3. Main results on the Hard instances (n = 123). Results shown as mean ± std. across three runs. Rvalid/correct/speedup : indicator rates
(%). S̄>1 : mean speedup among accelerated instances. VBP: Virtual Best Performance in seconds (verifier-only baseline VBP: 193s).
Solved: baseline timeouts (of 20) resolved per run. Bold: indicates best per model scale.

                   Model                            Rvalid (%)       Rcorrect (%)    Rspeedup (%)    S̄>1 (x)   VBP ↓ (s)   VBPE2E ↓ (s)   Solved
                   GPT-5.2                           94.0±1.7          72.4±2.2        37.1±1.2     10.7±0.4    155.6±3.0     163.4±3.0     3, 2, 3
                   GPT-OSS-120B                      92.1±1.2          58.0±1.2        27.4±2.9      7.0±1.4    165.8±5.6     167.6±5.7     3, 2, 1
                   Qwen3-80B                         97.8±0.5          38.8±1.7        21.4±1.2      9.5±1.0    169.5±2.1     169.7±2.1     4, 3, 3
                   Qwen3-14B                        96.5±0.5           36.3±1.9        13.6±2.0      7.6±0.9    183.2±1.2     183.6±1.1     1, 2, 1
                   Qwen3-14B-V2 (Ours)             100.0±0.0           43.4±4.9        18.4±4.2     16.0±3.3    162.1±8.3     162.9±8.1     4, 4, 2
                   Qwen3-8B (Base)                  89.4±7.8           23.8±3.1        10.8±0.5      8.5±5.2    181.6±4.3     181.7±4.2     0, 0, 3
                   Qwen3-8B-V2 (Ours)              100.0±0.0           42.8±4.6        21.7±1.7     10.7±2.3    166.5±4.3     166.7±4.3     2, 1, 4
                   Qwen3-4B (Base)                  99.2±0.0           22.8±2.2        11.1±0.9      8.9±2.5    185.6±2.4     185.7±2.4     1, 0, 1
                   Qwen3-4B-V2 (Ours)              100.0±0.0           44.4±2.3        24.7±1.2     12.4±2.2    165.5±3.2     165.7±3.2     3, 2, 2
                   Qwen3-0.6B (Base)                 88.3±0.5          28.5±2.8        12.2±2.2      5.3±3.3    182.9±5.7     183.0±5.7     2, 0, 1
                   Qwen3-0.6B-V2 (Ours)              99.7±0.5          27.9±0.5        14.1±2.5      8.5±3.1    174.0±5.6     174.1±5.6     2, 2, 1
                   Llama3.1-8B (Base)                96.2±1.2          14.9±1.7         5.4±2.0      3.7±1.4    186.3±5.1     186.4±5.1     1, 0, 2
                   Llama3.1-8B-V2 (Ours)             99.7±0.5          45.5±1.4        18.4±2.5     11.3±2.1    168.9±7.6     169.2±7.5     3, 2, 4
                   Mistral-7B (Base)                 93.8±0.9          18.4±2.0         7.3±1.4      6.7±3.6    186.7±1.5     186.9±1.5     0, 0, 0
                   Mistral-7B-V2 (Ours)              99.5±0.9          31.4±0.5        16.0±0.5     17.0±0.9    169.0±4.3     169.4±4.3     2, 1, 4



                                  GPT-5.2    GPT-OSS-120B        Qwen3-80B                  rect invariant need not accelerate verification; Table 3 sepa-
                         Qwen3-0.6B         Qwen3-8B                Mistral-7B              rates Rcorrect from Rspeedup and VBPE2E for this reason.
                         Qwen3-0.6B-V2      Qwen3-8B-V2 (LoRA)      Mistral-7B-V2           Qwen3-0.6B illustrates the decoupling most clearly: base
                         Qwen3-4B           Qwen3-14B               Llama3.1-8B
                         Qwen3-4B-V2        Qwen3-14B-V2            Llama3.1-8B-V2          and V2 achieve similar Rcorrect (28.5% vs. 27.9%), yet
                                                                                            V2 yields higher Rspeedup (14.1% vs. 12.2%), larger S̄>1
                        baseline (193s)                                                     (8.5× vs. 5.3×), and lower VBPE2E (174.1 s vs. 183.0 s).
                                                                                            W ONDA targets this gap by curating invariants that are not
             190                                                                            only correct but also practically beneficial to the verifier.

             185
                                                                                            Timeouts remain a challenge. Resolving baseline time-
VBPE2E (s)




                                                                                            outs remains an open problem: even the strongest models
             180                                                                            clear only a small fraction of the 20 hard-split instances that
                                                                                            timed out (Table 3, Solved). Still, V2 makes measurable
             175                                                                            progress. Qwen3-14B-V2 averages ∼3.3 resolved per run,
                                                                                            the highest among all models and above GPT-5.2 (∼2.7);
             170                                                                            Llama-3.1-8B-V2 also exceeds GPT-5.2 at ∼3.0. Mistral-
                                                                                            7B base stays at 0, while Mistral-7B-V2 averages ∼2.3 (up
             165                                                                            to 4). The consistent base→V2 improvement across fami-
             163                                                                            lies suggests that W ONDA teaches invariants that help the
                    0        10       20     30      40      50        60      70           verifier resolve previously intractable instances.
                                              Rcorrect (%)
                                                                                            Ablation Analysis. Table 4 traces V0→V1→V2 on Qwen3-
Figure 4. Correctness vs. VBPE2E on hard split (n=123; mean                                 4B/8B, Llama-3.1-8B, and Mistral-7B. V0 fine-tuning
over three runs). Dashed line: baseline VBP (193 s); better is                              on raw verifier-generated invariants often lowers Rvalid
bottom-right. V2 improves both axes across most of the models;                              (e.g., Qwen3-4B 99.2% → 81.3%; Mistral-7B 93.8% →
Qwen3-4/8B-V2 match GPT-OSS-120B on VBPE2E , with Qwen3-                                    65.0%); V1 normalization restores syntax but yields only
14B-V2 matching GPT-5.2, despite lower correctness rate.
                                                                                            modest gains. V2 brings the largest improvements across
                                                                                            all families: correctness and speedup rates nearly double on
                                                                                            Qwen3-4B and 8B, Llama-3.1-8B-V2 reaches the highest
Invariant Correctness vs. Verification Speedup. Fig-                                        Rcorrect in the table (45.5%), and Mistral-7B recovers from
ure 4 summarizes the joint improvement in correctness and                                   the V0 drop. Only the full W ONDA pipeline consistently de-
VBPE2E across families: in most cases, V2 (squares) im-                                     livers both syntactic reliability and meaningful verification
proves over base (circles) on both axes. However, a cor-                                    speedup. This trend is illustrated concretely in Figure 5 in

                                                                                        8
                                                     Not All Invariants Are Equal

Table 4. W ONDA ablation study on the hard split (n=123; mean ± std. over three runs). V0: raw UAutomizer invariants; V1: AST-
normalized; V2: full pipeline. Bold: best per model family.

             Model                      Rvalid (%)    Rcorrect (%)   Rspeedup (%)     S̄>1 (x)   VBP ↓ (s)   VBPE2E ↓ (s)
             Qwen3-8B (Base)             89.4±7.8       23.8±3.1         10.8±0.5     8.5±5.2    181.6±4.3     181.7±4.2
             Qwen3-8B-V0                 88.1±3.9       29.9±3.4         11.5±1.9     9.4±2.6    180.0±2.7     180.6±2.7
             Qwen3-8B-V1                 97.0±0.9       30.1±0.8         13.0±2.2     9.1±1.9    175.3±3.2     175.5±3.2
             Qwen3-8B-V2 (Ours)         100.0±0.0       42.8±4.6         21.7±1.7    10.7±2.3    166.5±4.3     166.7±4.3
             Qwen3-4B (Base)             99.2±0.0       22.8±2.2         11.1±0.9     8.9±2.5    185.6±2.4     185.7±2.4
             Qwen3-4B-V0                 81.3±0.8       29.3±3.5         13.6±1.9    10.1±1.5    177.5±1.5     177.7±1.5
             Qwen3-4B-V1                 97.6±1.4       33.1±2.3         12.7±2.3    11.4±2.9    174.2±4.7     174.4±4.7
             Qwen3-4B-V2 (Ours)         100.0±0.0       44.4±2.3         24.7±1.2    12.4±2.2    165.5±3.2     165.7±3.2
             Qwen3-0.6B (Base)           88.3±0.5       28.5±2.8         12.2±2.2     5.3±3.3    182.9±5.7     183.0±5.7
             Qwen3-0.6B-V0               85.9±2.6       18.7±0.8          8.9±0.8    11.7±9.4    178.0±2.7     178.1±2.7
             Qwen3-0.6B-V1               97.6±1.4       23.3±1.2          9.8±2.2    15.3±0.9    174.4±4.4     174.5±4.4
             Qwen3-0.6B-V2 (Ours)        99.7±0.5       27.9±0.5         14.1±2.5     8.5±3.1    174.0±5.6     174.1±5.6
             Llama3.1-8B (Base)          96.2±1.2       14.9±1.7          5.4±2.0     3.7±1.4    186.3±5.1     186.4±5.1
             Llama3.1-8B-V0              88.9±0.5       31.2±2.0         14.9±0.9     9.3±3.1    175.0±2.5     175.4±2.5
             Llama3.1-8B-V1              99.7±0.5       36.3±5.4         14.1±3.7    15.3±3.4    170.0±3.5     170.4±3.5
             Llama3.1-8B-V2 (Ours)       99.7±0.5       45.5±1.4         18.4±2.5    11.3±2.1    168.9±7.6     169.2±7.5
             Mistral-7B (Base)           93.8±0.9       18.4±2.0          7.3±1.4     6.7±3.6    186.7±1.5     186.9±1.5
             Mistral-7B-V0               68.8±2.0       17.1±4.3          6.5±2.8    16.8±2.3    179.1±7.7     179.4±7.7
             Mistral-7B-V1               95.9±1.6       24.9±0.9         10.0±3.8    14.3±2.8    175.4±6.4     175.9±6.2
             Mistral-7B-V2 (Ours)        99.5±0.9       31.4±0.5         16.0±0.5    17.0±0.9    169.0±4.3     169.4±4.3


Appendix A on a concrete example, where UAutomizer it-                   7. Limitations & Future Work
self, the base model, and the V0/V1 stages produce verbose
or incorrect invariants, while V2 discovers a compact, cor-              W ONDA currently relies on UAutomizer as its sole source
rect, and sufficient invariant yielding a 39.75× end-to-end              of training invariants, limiting coverage to solver-verifiable
speedup.                                                                 programs and risking inheriting the solver’s biases. Ex-
                                                                         tending W ONDA to additional backend verifiers is a natural
                                                                         next step. Beyond the training data itself, our current setup
Table 5. Ablation results on the Easy Split (n = 239). Bold: best
per model family.                                                        neither exposes intermediate reasoning steps nor leverages
                                                                         verifier feedback. Promising directions include chain-of-
     Model                        Rvalid (%)    Rcorrect (%)             thought supervision, reinforcement learning driven by veri-
     Qwen3-4B (Base)             100.0±0.0        42.3±1.1               fication outcomes, and integrating W ONDA-trained models
     Qwen3-4B-V0                  85.1±2.5        26.9±3.8               into iterative, counterexample-guided refinement loops.
     Qwen3-4B-V1                  99.0±0.6        34.5±1.5
     Qwen3-4B-V2 (Ours)          100.0±0.0        50.8±0.9
                                                                         8. Conclusion
     Mistral-7B (Base)            96.5±0.6        25.8±3.1
     Mistral-7B-V0                78.0±1.7        19.5±0.4               We introduced W ONDA, a novel data curation pipeline that
     Mistral-7B-V1                98.2±0.2        34.6±1.3               transforms raw verifier-generated invariants into compact,
     Mistral-7B-V2 (Ours)         99.7±0.2        41.7±1.7
                                                                         high-quality training signals with provable quality guaran-
     Llama3.1-8B (Base)           99.2±0.4        13.4±0.4               tees. Our results show that data quality, not model scale
     Llama3.1-8B-V0               91.1±1.5        31.2±2.7
     Llama3.1-8B-V1               99.7±0.2        41.3±1.7
                                                                         alone, is a key bottleneck for neural invariant generation:
     Llama3.1-8B-V2 (Ours)        99.7±0.2        57.6±2.1               fine-tuning small models on W ONDA-curated data substan-
                                                                         tially improves both invariant correctness and verification
                                                                         speedup across the Qwen3, Llama-3.1, and Mistral fam-
                                                                         ilies. Most notably, a 4B model surpasses a 20× larger
Easy split. Table 5 shows easy-split results. V2 lifts cor-              model, and our best 14B model matches frontier models
rectness across all families, with Llama-3.1-8B-V2 reaching              such as GPT-5.2 on end-to-end verification time, without
57.6% and Qwen3-4B-V2 reaching 50.8%. The V0 drop                        test-time compute overhead. These findings suggest that
and V1 partial recovery pattern is consistent across all three           careful data curation is a practical path to integrating small
families, matching the hard split. We report only validation             language models into traditional verifiers, making program
and correctness here as the average direct verification time             verification faster and more accessible.
is already very short (∼6.15 s) on this split.

                                                                     9
                                                Not All Invariants Are Equal

Impact Statement                                                      Conf. on Principles of Programming Languages (POPL),
                                                                      pp. 238–252, 1977.
This work contributes to our understanding of how to curate
training data for improving model performance on logical            Cousot, P. and Halbwachs, N. Automatic Discovery of
reasoning tasks. In addition, this work helps make formal             Linear Restraints Among Variables of a Program. In Proc.
verification more practical in high-stakes domains where              5th Int. Conf. on Principles of Programming Languages
the reliability of the software system is important. We do           (POPL), pp. 84–96, 1978.
not anticipate significant negative societal impacts arising
from this work.                                                     Ernst, M. D., Perkins, J. H., Guo, P. J., McCamant, S.,
                                                                      Pacheco, C., Tschantz, M. S., and Xiao, C. The Daikon
                                                                      System for Dynamic Detection of Likely Invariants. Sci-
Acknowledgments                                                       ence of Computer Programming, 69(1-3):35–45, 2007.
The work of Pinto, Elboher and Katz was partially funded            Ezudheen, P., Neider, D., D’Souza, D., Garg, P., and Mad-
by the European Union (RobustifAI project, ID 101212818).             husudan, P. Horn-ICE Learning for Synthesizing Invari-
Views and opinions expressed are however those of the                 ants and Contracts. Proceedings of the ACM on Program-
author(s) only and do not necessarily reflect those of the            ming Languages, 2(OOPSLA):131:1–131:25, 2018.
European Union or the European Health and Digital Ex-
ecutive Agency (HADEA). Neither the European Union                  Fedyukovich, G. and Bodı́k, R. Accelerating Syntax-Guided
nor the granting authority can be held responsible for them.          Invariant Synthesis. In Proc. 24th Int. Conf. on Tools and
The work of Wu is partially supported by a gift from the              Algorithms for the Construction and Analysis of Systems
VMware University Research Fund.                                      (TACAS), pp. 251–269, 2018.
                                                                    Flanagan, C. and Qadeer, S. Predicate Abstraction for Soft-
References                                                            ware Verification. In Proc. 29th Int. Conf. on Principles
                                                                      of Programming Languages (POPL), pp. 191–202, 2002.
Agarwal, S., Ahmad, L., Ai, J., Altman, S., et al. GPT-OSS-
 120B & GPT-OSS-20B Model Card, 2025. Technical Re-                 Garg, P., Neider, D., Madhusudan, P., and Roth, D. Learning
  port. https://arxiv.org/abs/2508.10925.                             Invariants Using Decision Trees and Implication Coun-
                                                                      terexamples. ACM Sigplan Notices, 51(1):499–512, 2016.
Anthropic. The Claude 3 Model Family: Opus, Sonnet,
  Haiku, 2024. Technical Report. https://arxiv.                     Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian,
  org/abs/2403.05530.                                                 A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A.,
                                                                      et al. The Llama 3 Herd of Models, 2024. Technical Re-
Beyer, D. and Strejcek, J. Improvements in Software Ver-              port. https://arxiv.org/abs/2407.21783.
  ification and Witness Validation: SV-COMP 2025. In
  Proc. 31st Int. Conf. on Tools and Algorithms for the             Gupta, A. and Rybalchenko, A. InvGen: An Efficient In-
  Construction and Analysis of Systems (TACAS), 2025.                variant Generator. In Proc. 21st Int. Conf. on Computer
                                                                     Aided Verification (CAV), pp. 634–640, 2009.
Chakraborty, S., Lahiri, S., Fakhoury, S., Lal, A., Musu-
                                                                    Heizmann, M., Christ, J., Dietsch, D., Ermis, E., Hoenicke,
  vathi, M., Rastogi, A., Senthilnathan, A., Sharma, R., and
                                                                      J., Lindenmann, M., Nutz, A., Schilling, C., and Podelski,
  Swamy, N. Ranking LLM-Generated Loop Invariants for
                                                                      A. Ultimate Automizer with SMTInterpol: (Competition
  Program Verification. In Proc. 28th Int. Conf. on Empiri-
                                                                      Contribution). In Proc. 19th Int. Conf. on Tools and
  cal Methods in Natural Language Processing (EMNLP),
                                                                     Algorithms for the Construction and Analysis of Systems
  pp. 9164–9175, 2023.
                                                                     (TACAS), pp. 641–643, 2013.
Clarke, E. M., Henzinger, T. A., and Veith, H. Introduction         Hoare, C. A. R. An Axiomatic Basis for Computer Program-
  to Model Checking. In Handbook of Model Checking, pp.               ming. Communications of the ACM, 12(10):576–580,
  1–26. Springer, 2018.                                              1969.
Colón, M., Sankaranarayanan, S., and Sipma, H. Linear In-          Hojjat, H. and Rümmer, P. The ELDARICA Horn Solver.
  variant Generation Using Non-Linear Constraint Solving.             In Proc. 18th Int. Conf. on Formal Methods in Computer-
  In Proc. 15th Int. Conf. on Computer Aided Verification            Aided Design (FMCAD), pp. 1–7, 2018.
  (CAV), pp. 420–432, 2003.
                                                                    Hu, J. E., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,
Cousot, P. and Cousot, R. Abstract Interpretation: A Unified          S., and Chen, W. LoRA: Low-Rank Adaptation of Large
  Lattice Model for Static Analysis of Programs by Con-               Language Models. In Proc. 10th Int. Conf. on Learning
  struction or Approximation of Fixpoints. In Proc. 4th Int.         Representations (ICLR), 2022.

                                                               10
                                                  Not All Invariants Are Equal

Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C.,               Wei, A., Suresh, T., Sun, T., Wu, H., Wang, K., and
   Chaplot, D. S., de las Casas, D., Bressand, F., Lengyel,             Aiken, A. InvBench: Can LLMs Accelerate Program
   G., Lample, G., Saulnier, L., Lavaud, L. R., Lachaux, M.-            Verification with Invariant Synthesis?, 2025. https:
   A., Stock, P., Le Scao, T., Lavril, T., Wang, T., Lacroix,           //arxiv.org/abs/2509.21629v1.
   T., and El Sayed, W. Mistral 7B, 2023. Technical Report.
   https://arxiv.org/abs/2310.06825.                                   Wu, G., Cao, W., Yao, Y., Wei, H., Chen, T., and Ma, X.
                                                                        LLM Meets Bounded Model Checking: Neuro-symbolic
Kamath, A., Mohammed, N., Senthilnathan, A.,                            Loop Invariant Inference. In Proc. 39th Int. Conf. on
  Chakraborty, S., Deligiannis, P., Lahiri, S. K., Lal,                 Automated Software Engineering (ASE), pp. 406–417,
  A., Rastogi, A., Roy, S., and Sharma, R. Leveraging                   2024a.
  LLMs for Program Verification. In Proc. 24th Int.
                                                                       Wu, H., Barrett, C., and Narodytska, N. Lemur: Integrating
  Conf. on Formal Methods in Computer-Aided Design
                                                                        Large Language Models in Automated Program Verifica-
 (FMCAD), pp. 107–118, 2024.
                                                                        tion. In Proc. 12th Int. Conf. on Learning Representations
Karr, M. Affine Relationships Among Variables of a Pro-                 (ICLR), 2024b.
  gram. Acta Informatica, 6(2):133–151, 1976.
                                                                       Yang, A., Li, A., Yang, B., Zhang, B., Hui, B., Zheng, B.,
Lahiri, S. K. and Bryant, R. E. Predicate Abstraction with               Yu, B., Gao, C., Huang, C., Lv, C., Zheng, C., Liu, D.,
  Indexed Predicates. ACM Transactions on Computational                  Zhou, F., Huang, F., Hu, F., Ge, H., Wei, H., Lin, H.,
  Logic (TOCL), 9(1):4–es, 2007.                                         Tang, J., Yang, J., Tu, J., Zhang, J., Yang, J., Yang, J.,
                                                                         Zhou, J., Zhou, J., Lin, J., Dang, K., Bao, K., Yang, K.-P.,
Liu, R., Chen, M., Wu, L.-I., Ke, J., and Li, G. Enhanc-                 Yu, L., Deng, L.-C., Li, M., Xue, M., Li, M., Zhang, P.,
  ing Automated Loop Invariant Generation for Complex                    Wang, P., Zhu, Q., Men, R., Gao, R., Liu, S.-Q., Luo, S.,
  Programs with Large Language Models. Science of Com-                   Li, T., Tang, T., Yin, W., Ren, X., Wang, X., Zhang, X.,
  puter Programming, 243:103387, 2025.                                   Ren, X., Fan, Y., Su, Y., Zhang, Y.-C., Zhang, Y., Wan, Y.,
                                                                         Liu, Y., Wang, Z., Cui, Z., Zhang, Z., Zhou, Z., and Qiu,
McMillan, K. L. Interpolation and SAT-Based Model Check-                 Z. Qwen3 Technical Report, 2025. Technical Report.
 ing. In Proc. 15th Int. Conf. on Computer Aided Verifica-               https://arxiv.org/abs/2505.09388.
 tion (CAV), pp. 1–13, 2003.

OpenAI. GPT-4 Technical Report, 2023. Technical Report.
  https://arxiv.org/abs/2303.08774.

OpenAI. Update to GPT-5 System Card: GPT-5.2, 2025.
 Technical Report. https://openai.com/index/
  gpt-5-system-card-update-gpt-5-2/.

Pei, K., Bieber, D., Shi, K., Sutton, C., and Yin, P. Can Large
  Language Models Reason About Program Invariants? In
  Proc. 40th Int. Conf. on Machine Learning (ICML), pp.
  27496–27520, 2023.

Sharma, R., Gupta, S., Hariharan, B., Aiken, A., Liang, P.,
  and Nori, A. V. A Data Driven Approach for Algebraic
  Loop Invariants. In Proc. 22nd Int. Conf. on European
  Symposium on Programming (ESOP), pp. 574–592, 2013.

Sun, C., Agashe, V., Chakraborty, S., Taneja, J., Barrett,
  C., Dill, D., Qiu, X., and Lahiri, S. K. ClassInvGen:
  Class Invariant Synthesis Using Large Language Models.
  In Proc. 2nd Symposium on AI Verification (SAIV), pp.
  64–96, 2025.

Team, K., Bai, Y., Bao, Y., Chen, G., Chen, J., Chen, N.,
  Chen, R., Chen, Y., Chen, Y., Chen, Y., et al. Kimi
  K2: Open Agentic Intelligence, 2025. Technical Report.
  https://arxiv.org/abs/2507.20534.

                                                                  11
                                                       Not All Invariants Are Equal

Appendix
A. Additional Examples

       cohendiv ll valuebound50 6.c            Baseline: 214.28 s
       void assert(int cond) {
         if (!(cond)) { ERROR: reach error(); }
       }
       void assume(int cond) {
         if (!cond) { abort(); }
       }
                                                                                     UAutomizer Generated Invariant          18 disjuncts
       int main() {
         int x, y;                                                                   (((long long) y * 4) == b) &&
         long long q, r, a, b;                                                        (( int128) r + 293) <=
         x = VERIFIER nondet int();                                                    (( int128) b * 1024))
         assume((x >= 0) && (x <= 50));                                               && ((r < (((long long) y * 8) + 1))
         y = VERIFIER nondet int();                                                    || (r < (((long long) 2 * y) + 1))))
         assume((y >= 0) && (y <= 50));                                               && (y <= b)) && (a == 4))
         assume(y >= 1);                                                             || (((r <= 50) && (1 <= y))
         q = 0; r = x;                                                                 && (b == ((long long) 16 * y)))
         a = 0; b = 0;                                                                 && (16 == a))
         while (1) {                                                                 || ((((b == ((long long) 16 * y))
           if (!(r >= y)) break;                                                       && ((16 + (16 * ((r >= 0)
           a = 1; b = y;                                                                ? (r / 32) : ((r / 32) - 1))))
           while (1) {                                                                 <= b)) && (16 == a))
              // Location l ← target                                                  && (( int128) 1998 + r)
             if (!(r >= (2 * b))) break;                                               <= (( int128) b * 1024)))
             assert(r >= ((2 * y) * a));                                             .
             a = 2 * a;                                                              .
                                                                                     .                               (15 more disjuncts)
             b = 2 * b;
           }
           r = r - b;
           q = q + a;
         }
         return 0;
       }


                                      ((((( int128) (((long long) a * 2)
                                      * y) + ( int128) 2 * ((( int128)
                                      ((long long) a * y * 2) * a))) == (b
                                      + ( int128) ((long long) b * 2))))
                                      || ((((( int128) ((long long) a *
                                      y * 2) + (long long) a * y) == (b +
       (r >= (2 * y) * a) &&          ( int128) ((long long) b * 3))) &&
                                                                                               a == 0 || b < y + 1                 a * y == b
       (b == (2ˆ(a / 2)))             ((( int128) ((long long) b * 4) +
                                      b) + ((( int128) ((long long) a *
                                      y * 2) * a)))))) || (((((a >= 0) ?                           Qwen3-8B-V1
              Qwen3-8B Base           (a % 2) : ((a % 2) + 2)) != 0) &&
                                      ((( int128) ((long long) a * y * 2)                                                          Qwen3-8B-V2
                                                                                                      Incorrect
                   Incorrect          < (b + ((( int128) ((long long) a *
                                      y * 2) * a)))))))                                                                       Correct, Sufficient (39.75×)


                                                      Qwen3-8B-V0

                                                         Incorrect

Figure 5. Inference-time invariant predictions on cohendiv ll valuebound50 6.c. The task is to synthesize an inductive invariant
at the inner loop entry point (// Location l). The UAutomizer-generated invariant (top right) enumerates 18 disjuncts, each encoding
b == k*y and a == k for specific powers of two; the compact closed-form a*y == b captures all of them. V2 discovers this
generalization, reducing verification from 214.28 s to 5.39 s (39.75× speedup including LLM inference), while earlier stages produce
incorrect or obfuscated invariants.


         V0 : Raw Verifier Output                           V1 : Normalized
                                                                                                                                     V2 : Simplified
   ((((((((7 <= i) && (N <= 10))                   7 <= i && N <= 10
     || ((2 == i) && (N <= 10)))                   || 2 == i && N <= 10
     || ((5 == i) && (N <= 10)))                   || 5 == i && N <= 10
     || ((i == 1) && (N <= 10)))
                                       normalize
                                                   || i == 1 && N <= 10                                  LLM
                                                                                                                  simplify       1 <= i && i <=
     || ((3 == i) && (N <= 10)))                   || 3 == i && N <= 10                                                           N && N <= 10
     || ((i == 4) && (N <= 10)))                   || i == 4 && N <= 10
     || ((6 <= i) && (N <= 10)))                   || 6 <= i && N <= 10
                                                                                                                                     30 chars, Grade 3
             239 chars, 7 disjuncts                         147 chars, 7 disjuncts


Figure 6. W ONDA pipeline. The LLM factors out the common constraint N <= 10 and reduces case enumeration into a compact range,
achieving a 3.47x verification speedup.


                                                                          12
                                               Not All Invariants Are Equal

B. Prompts
B.1. Prompt for training and evaluation
We provide here the system and user prompts for loop invariant generation task, used for both training and evaluation.
System:
   You are an expert C programmer and highly proficient
   in generating strong loop invariants
   for C programs that accelerate traditional verifiers’ verification process.

    ## Input format
    - A C program instrumented with loop markers of the form:
     ‘‘‘c
     INVARIANT_MARKER_k(); // appears at the *start of each loop body*
     ‘‘‘
     - The program contains a single target property as an assertion of the form:
     ‘‘‘c
     assert(<target_property>);
     ‘‘‘
    - A target loop marker (e.g., "INVARIANT_MARKER_1")

    ## Task
    - Propose ONE loop invariant that is intended to hold specifically at the target loop
        marker.
    - The invariant should help prove the target property and be inductive if possible.

    ## Output format
    - Output MUST be a single JSON object on one line wrapped in ‘‘‘json‘‘‘ tags and
        nothing else.
    - The JSON MUST have exactly these keys:
     - "marker": MUST be exactly the target loop marker (e.g., "INVARIANT_MARKER_1")
     - "content": ONLY a valid C boolean expression for the invariant.

    ## Output format example
    ‘‘‘json
    {"marker":"<target_marker>","content":"<content>"}
    ‘‘‘

User:
  ## User Input
  ### C Program
  ‘‘‘c
  {program}
  ‘‘‘
  ### Target Loop Marker
  {target_marker}




                                                           13
                                              Not All Invariants Are Equal

B.2. Prompt for Invariant Simplification
We provide here the full system and user prompts used for the simplification step in the W ONDA pipeline.
System:
   ## Task
   Given the C program and the invariant, your task is to simplify the
   invariant to a more compact and general form.

      ## Output format
      - Output MUST be a single JSON object.
      - The JSON MUST have exactly these keys:
       - "simplified_invariant": A single compact, inductive, C boolean
         expression, nothing else.
       - "rationale": A short explanation of why you simplified the
         invariant to the given form.
      ## Output format example
      {"simplified_invariant":"<simplified_invariant>",
         "rationale":"<rationale>"}

      ## Guidelines
      - The simplified invariant should be logically weaker than (or
       equivalent to) the original, but still inductive and strong enough
       to prove the target property.
      - Prefer LINEAR arithmetic expressions (the verifier struggles with
       non-linear math like x*y)
      - Prefer mathematical relationships over case enumeration
      - Look for patterns across disjuncts (e.g., repeated structure with
       varying constants)
      - Generalize enumerated values to ranges (e.g., "i == 1 || i == 2
       || i == 3" -> "1 <= i && i <= 3")
      - Remove tautological constraints (e.g., "a == a", "n <= n",
       "0 <= 0", "a + 0 == a", "true", "1")
      - Remove constraints on constant variables (variables initialized
       but never modified in loops)
      - Replace redundant constraints with simpler equivalents (e.g.,
       "a <= b && b <= a" -> "a == b")
      - Ensure the simplified invariant is still inductive (holds before
       loop and preserved by each iteration)
      - Use the program context to understand variable semantics and
       loop structure
      - Use ONLY plain ASCII characters in your output (no Unicode symbols)

User:
   Simplify the following invariant for the given C program and marker.
   c_program:
   ‘‘‘c
   {program}
   ‘‘‘
   invariant:
   ‘‘‘c
   {invariant}
   ‘‘‘

      marker:
      ‘‘‘c
      {marker}
‘‘‘




                                                           14
                                               Not All Invariants Are Equal

C. Algorithms


Algorithm 1 Candidate Invariant Grading                            Algorithm 2 Invariant Simplification
 1: Input: Verification query ⟨A, P, q⟩, location l, candi-         1: Input: Verification query ⟨A, P, q⟩, location l, normal-
    date predicate φ, baseline time tb                                 ized invariant φnorm , baseline time tb , N candidates,
 2: Output: Quality grade g ∈ {0, 1, 2, 3}                             minimum character length η
 3:                                                                 2: Output: Set R of qualifying simplified invariants with
 4: if not S YNTAX VALID(φ) then                                       their corresponding grades.
 5:    return 0 {Invalid syntax}                                    3: R ← ∅
 6: end if                                                          4: if φnorm ∈ {0, 1} then
 7:                                                                 5:     return R
 8: I ← (l, φ)                                                      6: end if
 9: {Parallel execution (cf. Figure 2)}                             7: if |φnorm | > η then
10: (V1 , t1 ) ← V(A, P, I) {Correctness Check}                     8:     C ← LLM(P, φnorm , l, N )
11: (V2 , t2 ) ← V(A ∪ {I}, P, q) {Sufficiency Check}               9:     C ← D EDUPLICATE(C)
12: tv ← max(t1 , t2 ) {Total wall-clock time}                     10:     for each φ ∈ C do
13:                                                                11:        if φ ∈ {0, 1} then
14: if V1 ̸= T RUE then                                            12:           continue
15:    return 0 {Incorrect (not inductive)}                        13:        end if
16: else if V2 ̸= T RUE then                                       14:        g ← G RADE C ANDIDATE(⟨A, P, q⟩, l, φ, tb ) {via
17:    return 1 {Correct but not sufficient}                                  Alg. 1}
18: else if tv ≥ tb then                                           15:        if g ≥ 2 then
19:    return 2 {Correct and sufficient, but no speedup}           16:           R ← R ∪ {(φ, g)}
20: else                                                           17:        end if
21:    return 3 {Correct, sufficient, and provides speedup}        18:     end for
22: end if                                                         19: end if
                                                                   20: if R = ∅ then
                                                                   21:     g ← G RADE C ANDIDATE(⟨A, P, q⟩, l, φnorm , tb )
                                                                   22:     if g ≥ 2 then
                                                                   23:        R ← {(φnorm , g)}
                                                                   24:     end if
                                                                   25: end if
                                                                   26: return R




                                                              15
                                                                                                  Not All Invariants Are Equal

D. Training Data Statistics
Pipeline Yield. We applied W ONDA to 4,000 raw verifier-generated invariants. Of these, 3,932 (98.3%) produced at least
one accepted candidate (G(φ) > 0); only 68 (1.7%) yielded an empty set. Of the 2,995 verbose invariants (|φnorm | ≥ 20),
the LLM simplification stage generated 11,980 candidates (N =4), retaining 6,584 (55.0%) with G(φ) ≥ 2, along with 187
G(φ)=1 and 39 normalized fallbacks. The remaining 1,005 compact invariants were verified as-is; 983 (97.8%) yielded a
G(φ) ≥ 2 candidate. The pipeline produces 7,763 curated rows in total; restricting to G(φ) ≥ 2 and dropping examples
whose full prompt-completion sequence (after applying the chat template) exceeds 1,024 tokens gives the final V2 set of
7,284 samples.

Dataset Statistics. As shown in Figure 7, the V2 set is partitioned 80/20 into 5,827 training and 1,457 validation samples,
comprising two quality tiers: Correct and Sufficient (G(φ) = 2, 4,516 samples) and Provides Speedup (G(φ) = 3, 2,768
samples). The mean sequence length is 518 tokens; generated invariants are highly concise at 15.8 tokens on average.
The G(φ) = 3 subset achieves a mean speedup of 2.13× with peaks up to 41.39×, demonstrating that W ONDA-curated
invariants offer significant computational advantages for the formal solver.

                                                              Correct and Sufficient          Provides Speedup                                                      Mean Speedup (All)            Mean Speedup (>1x)
                                                              Grade Distribution (V2 Dataset)                                                                       Mean Speedup Performance (V2)
                                                       4516                                                                                                         2.13x                 2.13x                    2.14x
                                                                                                                                           2.00
                                               4000
                                                                             3601                                                          1.75
                           Number of Samples




                                               3000
                                                                                                                          Speedup Factor   1.50
                                                              2768                                                                                          1.21x                 1.22x                    1.21x
                                                                                                                                           1.25
                                                                                       2224
                                               2000                                                                                        1.00
                                                                                                                                           0.75
                                               1000                                                  915                                   0.50
                                                                                                            544                            0.25
                                                  0                                                                                        0.00
                                                          Full                   Train               Validation                                                 Full                 Train                  Validation

                                                  Figure 7. Statistical distribution of the V2 curated dataset across the 80/20 train-validation split.



E. Hard Split Evaluation
To quantify the difficulty of the hard cases, we evaluate the baseline verifier on this subset 3 times and use the median
timing among them. Figure 8 (Left) reports the verifier’s performance on the 123 selected hard instances. The verifier fails
to solve 16.3% of these cases (compared to 5.5% across all instances), confirming that these represent substantially more
challenging verification problems. Figure 8 (Right) shows the runtime distribution of the baseline verifier on the 123 hard
cases. Execution times range from 15.5 s to the 600 s timeout, with a median of 112.2 s and a mean of 193.0 s.

                                                                                                                 Hard Split

                           Baseline Decision Distribution (n=123)                                                                                                      Baseline Time Distribution (n=123)
                                                                                                                                                       20                                                                  Median (112.2s)
                      80                                                                                                                                                                                                   Mean (193.0s)
Number of Instances




                                                                                                                                 Number of Instances




                                                                                                                                                       15
                      60
                                 81
                      40       (65.9%)                                                                                                                 10
                                                                    22                           20
                                                                  (17.9%)                      (16.3%)
                      20                                                                                                                                5

                       0                                                                                                                                0
                                 TRUE                             FALSE                       TIMEOUT                                                                                                102
                                                      Baseline Verifier Decision                                                                                                Baseline time (s, log scale)
Figure 8. Hard evaluation split baseline characterization. 72 programs expanded to 123 per-loop instances (median timing>15 s).
(a) Baseline verifier decisions (n=123 instances). (b) Baseline time distribution (n=123; instance-level baseline VBP).


                                                                                                                     16
                                                                   Not All Invariants Are Equal

E.1. Benchmark Characterization
The hard evaluation split comprises 72 SV-COMP programs (which expands to 123 per-loop instances). Figure 9 summarizes
the code structure:

                                          Program Size                                                        Loop Nesting Depth
                         42                                                                    60   60
           40                                                      mean=63.9                                                                  mean=1.2
                                                                                               50
           30
                                                                                               40
Programs




                                                                                    Programs
           20                                                                                  30
                    16
                                                                                               20
           10                  9
                                                                                               10                       10
                                                        2                3                                                                    2
            0                                                                                   0
                                                                                                    1                    2                    3
                   0
                 30
                 60
                 90
                   0
                   0
                   0
                   0
                   0
                   0
                   0
                   0
                   0
                   0
                   0
                   0                                                                                      Max Loop Nesting Depth
                12
                15
                18
                21
                24
                27
                30
                33
                36
                39
                42
                45
                                          Lines of Code
                                         Variable Count                                                   Nonlinear Arithmetic
           50                 50                                                                         44
                                                                    mean=8.1                                     Nonlinear = var*var, var/var, or var%var
                                                                                               40
           40
                                                                                               30                                        28
Programs




                                                                                    Programs

           30
                                                                                               20
           20

           10                                                                                  10
                     6             5      6
                                                               2        3
            0                                                                                   0
                                                                                                         No                             Yes
                0
                    4
                              8
                                   12
                                         16
                                              20
                                                   24
                                                        28
                                                             32
                                                                   36
                                                                        40




                                       Variable Declarations                                             Has Nonlinear Arithmetic

                                   Figure 9. Benchmark characterization on hard programs (n=72 unique C programs).



E.2. Post-hoc Timeout Sweep
We performed a post-hoc timeout sweep (T ∈ {15, 30, . . . , 600} s), shown in Figure 10. At each T , rates count only
instances that finish within T .
W ONDA-V2 dominates its base counterpart at every timeout on all three panels. Rcorrect and Rspeedup rise with T for both,
but V2 climbs faster and plateaus substantially higher; gains are already visible at short timeouts. VBPE2E stays lower for
V2 throughout, while base models remain near the ∼193 s verifier baseline.




                                                                               17
                                                                                  Not All Invariants Are Equal

                                                              Qwen3-8B            Qwen3-8B-V2 (LoRA)        Qwen3-4B   Qwen3-4B-V2

                (a) Rcorrect                                                       (b) Rspeedup                                                            (c) VBPE2E
           40
                                                                                                                                                     195     baseline (193 s)
           35                                                                25
                                                                                                                                                     190
           30
                                                                             20                                                                      185
           25
                                                                                                                                                     180




                                                                                                                                        VBPE2E (s)
                                                                             15
Rate (%)




                                                                  Rate (%)
           20
                                                                                                                                                     175
           15                                                                10                                                                      170
           10                                                                                                                                        165
                                                                              5
            5                                                                                                                                        160
            0                                                                 0                                                                      155
                 15       30       60 90 120 180 300 450600                        15       30     60 90 120 180 300 450600                                15        30         60 90 120 180 300 450600
                                   Timeout (s)                                                         Timeout (s)                                                              Timeout (s)
 Figure 10. Post-hoc timeout sweep on hard instances (n=123; T ∈ {15, 30, . . . , 600} s). (a) Rcorrect , (b) Rspeedup , and (c) VBPE2E
 vs. T for Qwen3-4B/8B base (circles, dashed) and W ONDA-V2 (squares, solid; 8B-V2 uses LoRA). Dashed line in (c): solver baseline
 (≈193 s).


  F. Model training details
                               Table 6. Full SFT hyperparameters for all other fine-tuned models on invariant generation (no-think mode).

                                                                             Qwen3-0.6B /                      Mistral-7B /
                                      Hyperparameter                             4B                            Llama3.1-8B                     Qwen3-14B
                                                                                          −4                             −5
                                      Learning Rate                 1 × 10                                        2 × 10                  5 × 10−5
                                                               cosine with min lr                                                    cosine with min lr
                                      LR Scheduler                (min ratio: 0.1)                                cosine                (min ratio: 0.1)
                                      Warmup Ratio                     0.03                                         0.05                     0.03
                                      Epochs                             2                                            3                        3
                                      Effective Batch Size              32                                           32                       32
                                      Max Seq. Length                  1024                                        1024                      1024



           Table 7. Supervised Fine-Tuning (SFT) Hyperparameters for Qwen3-8B-V2 on invariant generation with LoRA (Hu et al., 2022).

                               Category             Hyperparameter                      Value / Setting
                               Optimizer & LR       Learning Rate                       5 × 10−4
                                                    LR Scheduler                        cosine with min lr (min ratio: 0.1)
                                                    Warmup Ratio                        0.03
                               Batch Config         Epochs                              2
                                                    Effective Batch Size                32
                                                    Max Seq. Length                     1024 tokens
                               LoRA (PEFT)          Rank (r)                            128
                                                    Alpha (α)                           64
                                                    Dropout                             0.05
                                                    Target Modules                      All linear layers + embed tokens




                                                                                                       18
                                                    Not All Invariants Are Equal

           (a) Qwen3 non-think models (0.6B–14B).                        (b) Mistral-7B-Instruct-v0.3 and Llama-3.1-8B-Instruct.

                 Hyperparameter          Value                              Hyperparameter       Mistral-7B    Llama-3.1-8B
                                                                                                  Instruct        Instruct
                 Max New Tokens          1024
                 Temperature             0.7                                Max New Tokens         1024            1024
                 Top-p                   0.8                                Temperature             0.6             0.6
                 Top-k                   20                                 Top-p                   0.9             0.9
                 Min-p                   0
                 Repetition Penalty      1.1
                                        Table 8. Sampling hyperparameters used for each model.



G. Hardware, UAutomizer Release & Configuration
We used UAutomizer release for SVCOMP-2025 (Heizmann et al., 2013) with the configuration shown in Table 9.

                                                  Table 9. UAutomizer Configuration

               Parameter                 Value
               Version                   0.3.0-dev-d790fec1 (Java 21, jdk-21.0.1)
               Property                  unreach-call.prp
               Property specification    CHECK( init(main()), LTL(G ! call(reach error())) )
               Architecture              32-bit
               Memory limit              16 GB (enforced via runlim2 )
               Timeout                   600 s per verification task


Hardware. Experiments ran on a Linux SLURM cluster node with 8 AMD EPYC 9354 cores, 256 GB RAM, and one
NVIDIA L40S GPU. The verifier was memory-limited to 16 GB using runlim.




   1
       https://zenodo.org/records/14209043
   2
       https://github.com/arminbiere/runlim

                                                                 19
