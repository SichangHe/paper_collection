                                         M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                                         M AGENTA : C LOSING THE L OOP B ETWEEN M ATHE -
                                         MATICAL R EASONING AND L EAN V ERIFICATION

                                          Joshua Ong Jun Leang1,2 , Haonan Li1 , Zheng Zhao3 , Xinyi Shang4
                                          Wenda Li3 , Zhengzhong Liu1 , Eric Xing1 , Shay B. Cohen3 , Eleonora Giunchiglia2
                                          1
                                           Institute of Foundation Models, 2 Imperial College London
                                          3
                                           University of Edinburgh, 4 University College London
                                          {Joshua.Ong,Haonan.Li}@mbzuai.ac.ae
arXiv:2609.11319v2 [cs.AI] 21 Sep 2026




                                                                                    A BSTRACT
                                                  Most of mathematical knowledge has been communicated through so-called in-
                                                  formal use of mathematics and natural language. With large language models
                                                  (LLMs) being highly adept in using natural language, they achieve strong perfor-
                                                  mance, yet not perfect, in informal mathematical reasoning. Restraining LLMs to
                                                  informal reasoning misses out on the opportunity to use the discrete verification
                                                  abilities that machines offer through machine-checkable proofs. In this paper, we
                                                  bridge the gap between informal and formal reasoning by integrating Lean sig-
                                                  nals into the informal reasoning process. We introduce M AGENTA, a training-free
                                                  agentic pipeline that, given only a natural-language problem, produces an answer,
                                                  expresses it as a Lean 4 statement, and constructs a machine-checked proof. A
                                                  statement judge verifies whether the formalisation preserves the original prob-
                                                  lem, while an error-attribution judge routes failed attempts either to mathematical
                                                  re-derivation or local Lean repair. M AGENTA achieves 100% accuracy across all
                                                  evaluated olympiad benchmarks, including AIME 2025, AIME 2026, and HMMT
                                                  February 2026. When paired with the open-weight K2-H ORIZON -7B reasoner, it
                                                  solves all six IMO 2026 problems. Our analysis shows that statement adjudication
                                                  is essential for preventing false certificates and that feedback-guided correction
                                                  outperforms independent resampling on difficult problems.


                                         1    I NTRODUCTION
                                         LLMs have become increasingly capable mathematical problem solvers (OpenAI, 2026; Anthropic,
                                         2026; Qwen Team, 2026), solving International Mathematical Olympiad (IMO) problems (Huang &
                                         Yang, 2025) and beginning to contribute to mathematical research (Chen & Jiang, 2026; Jiang et al.,
                                         2026). Much of this progress relies on chain-of-thought (CoT) reasoning (Wei et al., 2022) and test-
                                         time scaling (Muennighoff et al., 2025), where models generate long reasoning traces. Yet longer
                                         reasoning does not make correctness easier to guarantee: such traces routinely contain errors and
                                         dead ends (Leang et al., 2025a; Lyu et al., 2023). LLM judges (Li et al., 2026) and process reward
                                         models (Guan et al., 2025; Zhang et al., 2025c) provide useful supervision over such traces, but
                                         ultimately remain learned proxies for correctness: they reproduce the failure modes of the models
                                         they evaluate and score plausible-but-incorrect reasoning (Yosef et al., 2026; Guan et al., 2025).
                                         Interactive theorem provers and proof assistants such as Lean 4 (Moura & Ullrich, 2021), Is-
                                         abelle (Paulson, 1994) and Rocq (Coquand & Huet, 1988) offer a different form of supervision:
                                         once a theorem is stated, a proof accepted by them provides a certificate of correctness. Systems
                                         built on this foundation have reached gold-medal level at the IMO (Chen et al., 2025) and solve
                                         99.2% of miniF2F (Zheng et al., 2022) and 70.0% of PutnamBench (Tsoukalas et al., 2024; Varam-
                                         bally et al., 2026). However, the models used are closed-source, or require parameter counts and
                                         search budgets beyond ordinary reach (Chen et al., 2025; Wang et al., 2026). In addition, the re-
                                         sults stated above largely address proof search after formalisation. Such benchmarks provide the
                                         system with a human-written formal statement and evaluate whether it can prove that statement (Lin
                                         et al., 2026; Xin et al., 2024). They therefore assume away a central part of mathematical problem
                                         solving: determining precisely what the natural-language problem asks to prove. Extending formal
                                         verification to natural-language mathematics consequently requires more than stronger proof search.


                                                                                          1
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                                       1. Reasoning & Answer            2. Formal Statement Generation,          3. Formal Proof Generation
                                                                                                                                                     4. Error attribution
                                             Generation                    Verification & Adjudication                  & Verification
                                               Reasoner (𝑹)                            Formaliser (𝑭)                         Prover (𝑷)                   Proof Verifier (𝑽𝒑 )
                                               LLM Reasoner                         LLM Formaliser                            LLM Lean Prover                Lean Verifier
           Problem Input (𝓠)         I/O: 𝒬 × ℱ!"#$ → Δ(𝒞 × 𝒜)                    I/O: 𝒬 × 𝒜 → Δ 𝒮                                                      I/O: 𝒮 × 𝒫 → T ∪ 𝜀%
                                                                                                                     I/O: 𝒬 × 𝒞 × 𝒮 × 𝜀% → Δ 𝒫
                                     Informal Reasoning Chain (𝒞)              Formal Statement 𝒮
         Natural Language                                                                                               Formal Proof (𝒫)                                 Final
                                             & Answer 𝒜                   theorem problem_1 :                                                       Success
          Math Problem              It means that the seventh                           …                        import Mathlib                                       Answer (𝒂)
                                    iterate of π is the identity map:
     Example (𝒒):                                π! = id" .                                                      open Equiv                                     Failure
     Find the number of             Hence the order of π must divide              Statement Verifier (𝑽𝒔 )
     functions 𝜋 mapping the        7. Since 7 is prime, the only
     set 𝐴 = {1,2,3,4,5,6} onto 𝐴   possible orders are 1 and 7. A                 I/O: 𝒮 → T ∪ 𝜀%               theorem problem_1 :
     such that for every 𝑎 ∈ 𝐴,     permutation of a set of size 6                                               Nat . card {π : Equiv . Perm
                                    can have order at most 6 (the            Failure            Success          (Fin 6) | ∀ a : Fin 6, (π ˆ              Error Judge 𝑱𝒆
     𝜋 𝜋 𝜋 𝜋 𝜋 𝜋 𝑎          =𝑎      maximum occurs for a 6-cycle).                                               7) a = a} = 1 := by
                                    Thus a permutation of order 7
                                    cannot exist on a set of six                                                                                          I/O: 𝒬 × 𝒞 × 𝒜 × 𝒮
                                    elements. Consequently the only               Statement Judge 𝑱𝒔             have h_set_eq : {π : Equiv .
                                                                                                                                                          × 𝒫 × 𝜀% → Δ 𝑙
                                    function satisfying is the                                                   Perm (Fin 6) | ∀ a : Fin 6,
                                    identity permutation.
                                                                            I/O: 𝓠 × 𝒜 × 𝒮 → Δ {0, 1}            (π ˆ 7) a = a} = {1} := by
                                                                                                                               …                 Syntax Error        Math Error
                                                                             No                 Yes

                                                                                                Compiler Error as Feedback (𝝋 ∈ ℱ4567 )



Figure 1: Overview of M AGENTA. The pipeline maps a natural-language problem to an informal
solution and candidate answer, a faithfully adjudicated Lean 4 statement, and a machine-checked
proof. The illustrated example is taken from AIME 2026, where the initial reasoning incorrectly
derives π 7 instead of the correct expression π 6 . Rejected formal statements are resampled, while
failed proof attempts are classified as either L EAN or M ATH errors. L EAN errors trigger local proof
regeneration, whereas M ATH errors, such as the π 7 versus π 6 mistake shown here, are returned to
the reasoner for mathematical re-derivation using verification feedback.
To address these issues, we introduce M AGENTA, an end-to-end agentic pipeline, as shown in Fig-
ure 1. Given a natural-language problem, M AGENTA produces a reasoning chain and candidate
answer, converts them into a Lean 4 statement, and constructs a machine-checked proof. M AGENTA
separates these tasks across four roles: A reasoner derives an informal solution and commits to
a candidate answer; a formaliser converts the problem and that answer into a Lean 4 statement;
a statement judge explicitly checks whether that statement preserves the semantics of the original
question and answer, rejecting omitted hypotheses, altered constants, and trivialising assumptions;
and a prover uses the informal reasoning as a proof plan. The Lean kernel can certify only that a
proof establishes the generated formal statement; it cannot determine whether that statement faith-
fully represents the original natural-language problem. This semantic gap is therefore the central
reliability risk in our setting, and the statement judge mitigates it by checking their alignment be-
fore proof generation. In addition, M AGENTA, in contrast to previous work, treats each certification
failure as an attribution problem, introducing an error judge that labels it S YNTAX or MATH and
reroutes the pipeline based on that.
M AGENTA verifies every problem on AIME 2025, AIME 2026, and HMMT February 2026 with
four different reasoners, which indicates that these benchmarks are saturated under our evaluation
setting. Paired with K2-H ORIZON -7B, M AGENTA solves all six IMO 2026 problems, surpassing
frontier closed models (OpenAI, 2026) and reasoners over two orders of magnitude larger (Team,
2026). To our knowledge, this is the smallest reported reasoner to solve all six problems. Since per-
fect scores may raise concerns of contamination, we further test whether the results can be explained
by one-shot recall: many problems reach a verified solution only after verification-guided self-
correction, and we additionally re-evaluate the pipeline on answer-preserving paraphrases. Stan-
dalone reasoners degrade under such perturbations (Mirzadeh et al., 2025; Leang et al., 2025a),
whereas M AGENTA remains robust. In summary, our contributions are as follows:
• We introduce M AGENTA, a training-free agentic pipeline that bridges informal mathematical rea-
  soning and formal verification, jointly producing an answer, a Lean 4 formalisation of the problem
  and answer, and a machine-checked proof through verification-guided self-correction.
• We further evaluate robustness to paraphrasing, characterise how verified performance scales with
  formalisation and proof-repair budgets, and ablate the two mechanisms that distinguish M AGENTA
  from a simple retry loop.


2   M ETHODOLOGY

M AGENTA combines natural-language reasoning with verification in Lean. The reasoner proposes
solutions but cannot guarantee their correctness, while Lean verifies proofs but cannot determine
whether an error is due to an incorrect mathematical solution or a wrong formal implementation.
M AGENTA closes this gap by attributing verification failures to the responsible component and rout-


                                                                                            2
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




ing the resulting feedback accordingly. Figure 1 gives an overview and Appendix A states the
notation and algorithm.

2.1   C OMPONENTS
M AGENTA contains five components, each implemented by a prompted language model except for
the deterministic verifier. To describe them, we first define the spaces over which they operate.
Let Q, C, A, S and P denote, respectively, the spaces of natural-language mathematics problems,
informal reasoning chains, candidate answers, Lean 4 theorem statements and Lean 4 proof scripts.
Let Ep and Es denote the space of Lean diagnostics produced when a proof fails verification and
when a statement fails to elaborate, respectively. Let ∅ ∈ Es ∩ Ep denote the absence of diagnostics,
as occurs on the first iteration before any call to the Lean verifier. Let Fmath = (C × A × S ×
P × Ep ) ∪ {∅} denote the space of all correction feedback signals that get generated in case of a
mathematical mistake, where ∅ denotes the absence of feedback. Given a set B, we denote by ∆(B)
the set of distributions over B, and by x ∼ P a sample x ∈ B from a distribution P ∈ ∆(B).
Reasoner R. The reasoner R : Q×Fmath → ∆(C ×A) maps a problem q ∈ Q and a mathematical-
correction signal φ ∈ Fmath to a distribution over pairs (c, a), where c ∈ C is an informal reasoning
chain and a ∈ A is a candidate answer. We write (c, a) ∼ R(q, φ) for a sample from the reasoner
model obtained by inserting q and φ into its prompt and extracting c and a from the generated
output. On the initial attempt, φ = ∅; a non-empty φ arises only after the error judge returns MATH,
indicating that the previous reasoning chain contains a mathematical error.
Formaliser F . The formaliser F : Q × A → ∆(S) maps a problem q ∈ Q and candidate answer
a ∈ A to a distribution over the space S of Lean 4 theorem statements. We write s ∼ F (q, a) for a
sample from the formaliser model obtained by inserting q and a into its prompt and extracting the
generated Lean statement. Conditioning on a makes the statement assert the proposed answer rather
than pose an open-ended existential goal. The resulting statement remains a candidate until it passes
both Lean elaboration and semantic adjudication.
Prover P . The prover P : Q × C × S × Ep → ∆(P) maps a problem q ∈ Q, an informal chain
c ∈ C, an accepted formal statement s ∈ S and an optional diagnostic to a proof script ϵ ∈ Ep to a
distribution over the space P of Lean 4 proof scripts. We write π ∼ P (q, c, s, ϵ), for a sample from
the prover model obtained by inserting q, c, s and ϵ into its prompt. On the first attempt ϵ = ∅, after
a S YNTAX error the next attempt receives the latest diagnostic while c, a and s remain fixed.
Verifier V . The verifier is the deterministic Lean 4 checking environment augmented with SafeVer-
ify, a certification wrapper that rejects a submission whenever the declared theorem differs from the
accepted statement or the script uses a forbidden construct such as sorry, admit, a new axiom or
native decide (Appendix B.2). The verifier consists of two deterministic checks: the statement
verifier Vs : S → {⊤} ∪ Es and the proof verifier Vp : S × P → {⊤} ∪ Ep , where ⊤ denotes a
successful check. The verifier Vs checks that a generated statement is closed and elaborates in Lean,
which is a well-formedness check and does not establish that the statement is true or faithful to the
problem. The verifier Vp checks that π is a complete, policy-compliant Lean proof of the unchanged
statement s; otherwise, the verifier returns a diagnostic ϵ ∈ Ep .
Judge J. A single language model, prompted in two distinct ways, implements two distinct judging
functions. The statement judge Js : Q × A × S → ∆({0, 1}) maps a problem q ∈ Q, candidate
answer a ∈ A, and Lean 4 statement s ∈ S to a distribution over acceptance decisions. Acceptance
denotes that the Lean 4 statement faithfully represents the original problem and candidate answer.
The error judge Je : Q × C × A × S × P × Ep → ∆({MATH, S YNTAX}), maps the complete
context of a failed proof attempt to a distribution over error labels. We write ℓ ∼ Je (q, c, a, s, π, ϵ),
where ℓ = MATH indicates that the mathematical reasoning should be revised, while ℓ = S YNTAX
indicates that the error lies in the formal implementation. Thus, Js determines whether the generated
statement faithfully represents the intended claim, whereas Je determines which component should
be revised after proof verification fails.

2.2   T HE M AGENTA PROCEDURE
M AGENTA is an iterative verification-guided refinement procedure in which Lean 4 feedback is used
to identify and correct errors in the reasoner’s proposed solution. Verification failures are attributed
either to the mathematical reasoning or to its formal implementation, allowing the pipeline to revise


                                                    3
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




only the component responsible for the failure. Below we describe each step of the procedure, while
the pseudocode can be found in Appendix A.2.
Step 1: Reasoning & Answer Generation (Reasoner R). Let T be a user-defined upper bound
on the number of calls to the reasoner, and let t = 0, . . . , T − 1 index these calls. At iteration t, the
reasoner samples (ct , at ) ∼ R(q, φt ), where φ0 = ∅. For t > 0, the reasoner is invoked only after
the error judge Je classifies the previous failed proof attempt as MATH; in this case, φt ∈ Fmath
is constructed from the failed attempt and the corresponding verifier diagnostic. Thus, each MATH
error triggers a new reasoning chain and candidate answer, while statement resampling and proof
repair leave the current pair (ct , at ) unchanged. The procedure terminates if a proof is verified or if
the budget of T reasoner calls is exhausted.
Step 2.a: Formal Statement Generation (Formaliser F ). Let M be a user-defined upper bound
on the number of statement samples drawn for a fixed candidate answer, and let m = 0, . . . , M − 1
index these samples. At sample m, the formaliser draws sm t ∼ F (q, at ), whose hypotheses encode
the conditions of q and the final answer provided by at .
Step 2.b: Formal Statement Verification (Statement Verifier Vs ). Each candidate statement
sm                                                        m
 t is first submitted to the Lean 4 verifier. If Vs (st ) ̸= ⊤, the statement is discarded and the
                                         m
formaliser F is resampled. Otherwise, st proceeds to statement adjudication. This verification step
is restarted for every new reasoning pair (ct , at ) and repeated within the same reasoning iteration
until a statement passes verification, while (ct , at ) remains fixed.
Step 2.c: Formal Statement Adjudication (Statement Judge Js ). Given a candidate statement
sm                 m                                                        m
 t such that Vs (st ) = ⊤, the statement judge samples b ∼ Js (q, at , st ). The judge is tasked
           m
to accept st only if it faithfully represents the original problem q and assert the candidate answer
at . If b = 0, the candidate is discarded and control returns to step 2, where the formaliser F is
resampled under the same statement budget M . If b = 1, the candidate is accepted, denoted st ,
and passed to the prover. A failure at either step 2.1 or step 2.2 does not trigger a new call to the
reasoner; hence, statement resampling leaves the current reasoning pair (ct , at ) unchanged. The
statement judge therefore determines what the pipeline attempts to prove, and is the component that
connects Lean’s guarantee about the accepted formal statement st to the corresponding claim about
the original problem q; §2.3 discusses the resulting guarantee in detail.
Step 3: Formal Proof Generation (Prover P ). Let K be a user-defined upper bound on the
number of proof attempts for an accepted statement, and let k = 0, . . . , K − 1 index these attempts.
At attempt k = 0, the prover samples πtk ∼ P (q, ct , st , ϵk ), where ϵ0 = ∅ and the informal solution
ct acts as a proof plan.
Step 4.a: Proof Verification (Proof Verifier Vp ). Each candidate proof πtk is submitted to the
proof verifier Vp . If Vp (st , πtk ) = ⊤, then the Lean 4 verifier has accepted the proof, and the
pipeline terminates and returns (st , at , ct , πtk ). The associated informal solution ct and candidate
answer at are retained as the final reasoning chain and answer. Otherwise, Vp (st , πtk ) = ϵkt , i.e., the
verifier has returned an error, which gets passed to the error judge.
Step 4.b: Error attribution (Error Judge Je ). Each candidate proof πtk that failed the verifier
check is submitted together with its corresponding error trace ϵkt to the error judge Je , which returns
ℓ ∼ Je (q, ct , at , st , πtk , ϵkt ). If ℓ = S YNTAX then the algorithm loops back to step 3 a new candidate
proof πtk+1 is sampled from the prover. Thus, each S YNTAX error triggers a repair of the proof
script alone, while ct , at and st remain fixed. If ℓ = MATH the informal solution is deemed false or
insufficient, and the pipeline builds φt ∈ Fmath from the failed attempt and returns to step 1. Only
a MATH label may revise the reasoning and answer.


2.3   ROLE OF THE J UDGE AND S COPE OF THE G UARANTEE

Why is statement adjudication necessary? Lean verifies a proof only relative to the generated
statement: Vp (s, π) = ⊤ entails that π is a valid proof of s, but this does not imply that s faithfully
represents the original problem q and answer a. We refer to this as the autoformalisation gap,
which is due to the nature of LLMs and use of natural language. The statement judge prevents
these false certificates, working under the assumption that it is an easier task to confirm alignment
between formal and informal statements compared to the generation of the formal statement. As this
semantic check is performed by a learned judge rather than the Lean kernel, the final output is a soft


                                                     4
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




certificate: formally sound with respect to s, but only as relevant to q as the generated statement is
faithful. Further ablation study of Statement Judge can be referred to §4.3.
Why is error attribution necessary? When proof verification fails, Vp identifies where Lean
failed. However, the same rejection may arise because the informal mathematics is false or insuffi-
cient, or because a correct argument has been implemented incorrectly in Lean. These cases require
varying actions: the former requires a new mathematical derivation, or the latter requires proof re-
pair at fixed mathematical content. The error judge supplies this decision: ℓ ∼ Je (q, c, a, s, π, e),
where ℓ ∈ {MATH,S YNTAX}. The resulting label determines the correction path:
           ℓ = S YNTAX =⇒ π ′ ∼ P (q, c, s, e),       ℓ = MATH =⇒ (c′ , a′ ) ∼ R(q, φ).            (1)
A S YNTAX label preserves (c, a, s) and uses the diagnostic to repair the Lean proof, whereas a MATH
label constructs φ ∈ Fmath and returns control to the reasoner. Without Je , the closed-loop pipeline
is underdetermined: a failed verification provides no basis for choosing between proof repair and
mathematical re-derivation.
A mistake-bound perspective Given a question q ∈ Q, let A(q) be the possible answers (correct
or not) that an LLM could provide for it. We might ask the question, in terms of the mistake-bound
model of learning (Cesa-Bianchi & Lugosi, 2006), what is the maximal number of “mistakes” M (q)
(verifier returning 0),1 our pipeline, or an improved one, would make before we find a verified
answer? If the LLM does not loop in its answer (and the verifier provides a significant feedback),
and the context length is limited (hence, the answer too), then this “dimension” of Q (over all
questions, see also the Littlestone dimension in online learning; Littlestone 1987) is finite.
A simple result speaks about this dimension in terms of the feedback loop removing a fraction
γ ∈ (0, 1) of potential (mistaken) answers left at each step shows that M (q) ≤ log1/(1−γ) |A(q)|.
For example, if at each point we remove half of the possible answers from the LLM prediction based
on our verifier feedback, then M (q) ≤ log2 |A(q)|. Given the complexity of LLM inference, it is
difficult to point and prove an exact value of γ or M (q), but we believe the mistake-bound model
is a promising learning model to analyse such pipelines and we leave it for future work to estimate
γ in our case on a larger set of answers and questions. We provide further empirical analysis of the
number of mistakes our pipeline makes in §3.2.

3     E XPERIMENTS
3.1    E XPERIMENTAL S ETUP
Models. We vary R across both open-weight and proprietary families: K2-Horizon-7B and 375B,
Qwen3.8-27B and GPT-5.6-Sol (Codex). All other components are held fixed unless stated oth-
erwise: Goedel-Formaliser-32B as F , DeepSeek-V4-Flash for both judge roles, and Leanstral-1.5
as the prover P . This provides an entirely open weight pipeline. §4.1 substitutes GPT-5.6-Sol for
F and for P . Proofs are checked with Lean v4.29.1 and M ATHLIB under SafeVerify; decoding
settings and the budgets T , M , K are provided in Appendix B.2.
Datasets. We evaluate on AIME 2025, AIME 2026 and HMMT February 2026: natural-language
competition problems with a numerical answer and no accompanying formal statement. We addi-
tionally evaluate our smallest reasoner K2-H ORIZON -7B with M AGENTA on IMO 2026 problems.
Baselines. We compare against state-of-the-art baselines: Claude Opus 5, Gemini 3.7 Flash, and
Kimi K3. We let each baseline only generate one answer (i.e., pass@1 rate).
3.2    E XPERIMENTAL R ESULTS
M AGENTA is robust to model choice. As shown in Table 1, M AGENTA’s performance is not
tied to a particular base model used as reasoner. The average gain across the three tasks over the
corresponding standalone reasoner ranges from 8.6 points for Qwen3.8-27B to 25.8 points for K2-
H ORIZON -7B. In order to show that generalist closed models can be used instead of specialised
open source models as formaliser and prover, we replace both of them with GPT-5.6-Sol (Codex).
This once again yields the perfect scores shown in Table 1. Consistency across reasoner, formaliser
and prover configurations suggests the gains arise from the verification-guided pipeline rather than
from any single model; §4.1 analyses what these configurations cost.
   1
     We note the term “mistake” is referring to lack of verifiability, not correctness, due to the autoformalisation
gap that remains unpreventable with current techniques


                                                         5
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




Table 1: Accuracy (%) on competition-level mathematics benchmarks, covering 93 problems in
total. Light-grey rows denote results obtained with M AGENTA. Green values in parentheses report
absolute improvements over the corresponding base reasoner in percentage points.

      Model                 AIME 2025          AIME 2026                                  HMMT Feb. 2026       Overall
      Claude Opus 5         100.00             100.00                                        96.97              98.92
      Gemini 3.7 Flash      100.00             100.00                                        90.91              96.77
      Kimi K3                93.33              90.00                                        78.79              87.10
      K2-Horizon-7B          83.33              80.00                                        60.61              74.19
        + M AGENTA          100.00 (↑ 16.67)   100.00 (↑ 20.00)                             100.00 (↑ 39.39)   100.00 (↑ 25.81)
      K2-Horizon-375B        93.33              90.00                                        72.73              84.95
        + M AGENTA          100.00 (↑ 6.67)    100.00 (↑ 10.00)                             100.00 (↑ 27.27)   100.00 (↑ 15.05)
      Qwen3.8-27B           100.00              86.67                                        87.88              91.40
        + M AGENTA          100.00             100.00 (↑ 13.33)                             100.00 (↑ 12.12)   100.00 (↑ 8.60)
      GPT-5.6-Sol (Codex)    90.00              86.67                                        78.79              84.95
        + M AGENTA          100.00 (↑ 10.00)   100.00 (↑ 13.33)                             100.00 (↑ 21.21)   100.00 (↑ 15.05)


K2-H ORIZON -7B+M AGENTA solves all IMO 2026 problems. Coupled with M AGENTA, K2-
H ORIZON -7B solves all six IMO 2026 problems. To our knowledge, this is the smallest reported
reasoner to score perfectly on this task. Unlike answer-only benchmarks, IMO solutions are inher-
ently multi-step: they require answering a sequence of intermediate subproblems, whose results are
then composed to obtain the final answer. Despite perfect final answer accuracy and formal veri-
fication we observe a residual gap between the informal explanation and the formal statement and
proof. We therefore append a final alignment judge, instantiated with K2-H ORIZON -375B, which
returns incomplete proof when the two do not support the same conclusion (Appendix F);
its feedback yields substantially more complete reasoning chains in our qualitative analysis. For-
mal correctness is thus attainable with a compact reasoner, whereas a fully aligned, communicable
informal derivation remains a separate challenge.
Verification-guided correction trades test-time                                20
                                                             Number of self-corrections




                                                            20
computation for model scale. Most reasoners do
not solve every problem first time, but their verified      15
solve rates rise consistently across correction rounds.
                                                            10                                8
On AIME 2026, K2-H ORIZON -7B needs an average
of 5 correction rounds to reach a verified solution          5            3
against 2 for K2-H ORIZON -375B. Both ultimately                                        2  1
                                                                   0
attain perfect accuracy, but the larger reasoner gets        0
                                                                  P1     P2    P3      P4 P5 P6
there with fewer feedback cycles while the 7B model                             Problem
closes the gap by spending additional verification-
guided computation. On the more complex IMO 2026, Figure 2: Self-corrections required by K2-
K2-H ORIZON -7B needs an average of 5.7 rounds, H ORIZON -7B+M AGENTA on IMO 2026.
with per-problem trajectories in Figure 2. These averages count only revisions triggered by
mathematical errors; compiler-level errors require further repair iterations (§4.1).

4      A NALYSIS
4.1     S CALING A NALYSIS
We analyse how test-time computation is distributed across the two stages of M AGENTA. We first
examine how the choice of formaliser affects the number of samples required to obtain an accepted
statement, and then compare the cost of different proof backends.

4.1.1     F ORMAL S TATEMENT G ENERATION
The formaliser governs how quickly the pipeline reaches a faithful, provable statement. C ODEX
succeeds on its first call for approximately 66% of AIME 2026 problems against 42% for Goedel,
and covers the benchmark within 6 calls rather than approximately 120 (Figure 3); at a six-call
budget Goedel covers only about 68%. The distributions differ in shape, not merely location:

                                                     6
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




C ODEX is compact, and indeed M = 6 represents a                                                 100




                                                                      Cumulative pass rate (%)
very small number of calls, whereas the Goedel curve
spans two orders of magnitude and any practical M                                                 80
truncates it. Truncation is not a correctness failure—
adjudication rejects unfaithful statements before proof
effort is spent—but an exhausted statement budget for-                                            60
                                                                                                                                                        Goedel
feits the problem, thus a long formalisation tail converts                                                                                              Codex
directly into lost coverage.                                                                      40
                                                                                                         1                       10                           100
                                                                                                             Formal-statement generation calls (log scale)
4.1.2    F ORMAL P ROOF G ENERATION
Both prover backends verify 100% of AIME 2026, thus Figure 3: Cumulative pass rate against
accuracy by itself cannot separate them. Reporting ac- formal-statement generation calls on
curacy as a function of a budget rather than at a single AIME 2026.
operating point is standard practice in agent evaluation (Kapoor et al., 2025) and in the test-time-
scaling literature (Muennighoff et al., 2025; Snell et al., 2025). To make claims about self-repair
meaningful, we report the cumulative pass rate:
                                        1 X
                         Passu (β) =           1[Ver(q) = 1 ∧ u(q) ≤ β] ,                        (2)
                                       |D|
                                           q∈D
where u(q) measures measures the number of to-                                          100
kens necessary to produce the proof, Ver(q) indicates

                                                             Cumulative pass rate (%)
                                                                                            80
whether the proposed resolution of q passes indepen-
dent verification, and β represents the tokens budget.                                      60
A single cost axis is not well defined across backends:
                                                                                            40
L EANSTRAL runs as a multi-turn agent, thus one in-
vocation can hide hundreds of compiler queries, while                                       20
a C ODEX CLI call reports one call regardless of what                                                                                                 Leanstral
                                                                                                 0
it does internally. We therefore count a cost as exter-                                              1               10               100             1,000
nal when a failure survives the prover’s own repair at-                                                            Internal model calls (log scale)
tempts and returns to the error judge, and internal when
incurred inside a single invocation. External costs are          Figure 4: Internal L EANSTRAL agent
defined identically for both backends; internal costs are        calls on the winning trajectory. This mea-
observable only for L EANSTRAL (Figure 4), and are               sure has no C ODEX counterpart, as its CLI
paid on local hardware rather than billed per request.           does not expose per-invocation turns.
Measured externally, L EANSTRAL reaches the shared ceiling more cheaply: it solves 42% of prob-
lems with no failed external verification round against 17% for C ODEX (Figure 5b), reaches full
coverage on approximately 6 × 104 reasoner tokens versus 9 × 105 (Figure 5c), and produces veri-
fied proofs roughly half as long, 1.1 × 104 against 2 × 104 tokens (Figure 5d).
This efficiency is bought with computation inside L EANSTRAL’s agentic loop: its winning trajec-
tories consume approximately 3 × 102 internal calls at median coverage and up to 3 × 103 at full
coverage (Figure 4), and once these are counted the ordering reverses (Figure 5a). The claim is
therefore not that the open-weight prover is cheaper outright, but that at equal verified accuracy it
moves cost from metered rounds into local computation one controls. Since C ODEX performs an
unknown amount of internal work, its external measurements is only a lower-bound on its true com-
pute. Attribution matters mainly in the remaining tail: an external failure reaches the router on 58%
of problems with L EANSTRAL against 83% with C ODEX.

4.2     ROBUSTNESS TO A NSWER -P RESERVING PARAPHRASE
To control for possible data leakage, we Table 2: Accuracy (%) on original and para-
use DeepSeek-V4-Flash to paraphrase every phrased AIME 2026. ∆ is the % decrease.
AIME 2026 problem while preserving its quantities,
hypotheses, goal and reference answer, check Model               Original Paraphrased    ∆
each paraphrase before use using C ODEX, and K2-Horizon-375B         90.0        86.7  -3.3
measure the robustness gap ∆ between original and    + M AGENTA     100.0       100.0   0.0
paraphrased accuracy. Prior work (Mirzadeh et al., K2-Horizon-7B     80.0        70.0 -10.0
2025) shows that standalone reasoners are sensitive  + M AGENTA     100.0       100.0   0.0
to such answer-preserving changes, and Table 2


                                                  7
    M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                           100                                                                                        100



Cumulative pass rate (%)




                                                                                           Cumulative pass rate (%)
                            80                                                                                         80

                            60
                                                                                                                       60

                            40
                                                                                                                       40
                            20                                               Leanstral                                                                                   Leanstral
                                                                             Codex                                     20                                                Codex
                             0
                                 1          10              100              1,000                                          0    1   2      5    10    20       50    100     200     400
                                          Total recorded calls (log scale)                                                  Failed external Lean/code-verification rounds (log scale)

                                         (a) Total recorded calls                                                       (b) Failed external Lean verification rounds
                           100                                                                                        100
Cumulative pass rate (%)




                                                                                           Cumulative pass rate (%)
                            80                                                                                         80

                            60                                                                                         60

                            40                                                                                         40

                            20                                          Leanstral                                      20                                                   Leanstral
                                                                        Codex                                                                                               Codex
                             0                                                                                          0
                              103             104                 105                106                                 100                      1,000                      10,000
                                     K2-Horizon-Reasoner tokens (log scale)                                                      Final verified Lean-code tokens (log scale)
                                 (c) Reasoner (K2-H ORIZON -7B) tokens                                                          (d) Final verified Lean-code length

    Figure 5: Cumulative pass rate against four cost measures on AIME 2026 (Equation 2). Both
    backends reach 100%, so the curves separate on budget, not on ceiling. Panels (b)–(d) are external
    measures, defined identically for both backends, and L EANSTRAL is left-shifted on each.

    reproduces this: paraphrasing costs K2-H ORIZON -375B 3.3 points and K2-H ORIZON -7B 10.0
    points, whereas both retain 100% with M AGENTA (∆ = 0). Perturbing the numerical quantities,
    so that the reference answer itself changes, would be the stronger test; we therefore read this as
    necessary rather than sufficient evidence against contamination.

    4.3                          A BLATION S TUDY

    We ablate the two mechanisms that distinguish M AGENTA from a generic retry loop: the statement
    judge Js , which decides what is proved, and the error judge Je , which decides how a failed attempt
    is retried. Both rerun the same harness with one component disabled, and the rest as in §3.1.
    Statement adjudication. A certificate is Table 3: Effect of statement adjudication with
    meaningful only when the proved statement Goedel formaliser on AIME 2026.
    preserves the original problem, so we separate
    two outcomes. Let Ver be the fraction of prob-         Setting       Ver ↑ VerCor ↑ FCR ↓
    lems for which the pipeline returns a verified
    proof and VerCor the fraction for which it does        With Js      63.3%      63.3%      0.0%
                                                           Without Js 36.7%        20.0% 45.5%
    so and the certified answer matches the ref-
    erence. The false certification rate FCR =
    1 − VerCor/Ver is then the fraction of returned certificates whose answer is nonetheless wrong.
    Since the verifier V is sound, FCR > 0 is possible only through an unfaithful formalisation, which
    makes it a direct measurement of the residual gap identified in §2.3. We disable Js by accepting the
    first elaborated statement unconditionally. Table 3 reports the result.
    Without the judge Ver falls from 63.3% to 36.7% even though every first-sampled formalisation
    is now accepted. The judge, therefore, acts as an additional filter on the formal statement beyond
    semantically aligning it with the informal one. The effect on correctness is larger still: VerCor
    falls 43.3 points to 20.0% and FCR rises to 45.5%, so nearly half the surviving certificates prove
    something other than the problem asked, but not necessarily contradictory (Appendix E.1).


                                                                                           8
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




Resampling versus diagnostic-conditioned self-correction. We next replace diagnostic-
conditioned self-correction with independent resampling, which discards compiler feedback and
draws a fresh proof each attempt. This baseline is stronger than it may appear: for a problem with
single-shot success probability p > 0, after n parallelisable attempts of using V as a sound selec-
tor, the probability is increased to 1 − (1 − p)n ≥ 1 − e−np . On AIME 2026 resampling with
K2-H ORIZON -7B solves 29/30 (96.7%) against 30/30 for self-correction; in the single failure the
initial answer is wrong, so the statement is unprovable and further proof samples cannot recover it.
The gap widens on IMO 2026, where, despite 8–16 independent generations per problem, resam-
pling verifies only 1/6 (16.7%) while self-correction verifies all six, so p is effectively zero under
our budget for most IMO problems. Conditioning on a diagnostic moves probability mass onto
proofs the unconditioned distribution does not reach. The benefit in error attribution (M ATH versus
S YNTAX) is routing the next attempt to the right component based on the previous attempt.

5   R ELATED W ORK
LLMs for Mathematical Reasoning. LLMs have achieved strong performance in competition
mathematics through CoT reasoning (Wei et al., 2022) and test-time scaling (Albalak et al., 2025;
Shao et al., 2024; Zhang et al., 2025b). As plausible reasoning traces may still lead to incorrect so-
lution, prior work applies LLM judges (Yosef et al., 2026), process reward models (Liu et al., 2024),
and related scoring or selection methods (Ospanov et al., 2026; Leang et al., 2026a). These sig-
nals remain learned proxies that may share the models’ failure modes (Leang et al., 2026a; 2025a).
M AGENTA instead uses Lean as a deterministic verifier of the generated formal proof.
Theorem Proving and Autoformalisation. LLM-based theorem proving has advanced rapidly,
with specialised proving models such as Pythagoras-Prover (Leang et al., 2026b), Goedel-
Prover (Lin et al., 2026), and others (Ma et al., 2026; Wang et al., 2026), together with agentic
closed-source models (Liu et al., 2026; Xu et al., 2026), have rapidly advanced LLM theorem prov-
ing, albeit often through substantial test-time scaling (Varambally et al., 2026; Klingner et al., 2026;
Chen et al., 2025; Lin et al., 2026). However, current benchmarking assume an accurate formal
statement as the input. Producing faithful formal statements remains challenging: an incorrect for-
malisation may admit a valid proof without certifying the original problem (Cornish et al., 2026).
Formal–Informal Distillation. Previous work has explored connections between informal rea-
soning and formal proof (Varambally et al., 2026; Quan et al., 2025), but often relying solely on
closed-source models, and underperforms state-of-the-art mathematical reasoners (Liu et al., 2025;
Zhou et al., 2024; Yao et al., 2025; Zhang et al., 2025a). Carefully curated formal–informal pipelines
can improve reliability (Sazonova et al., 2026), while Theorem Prover as a Judge uses GPT-4o and
formal verification to validate informal traces during synthetic-data generation (Leang et al., 2025b).
Tsoukalas et al. (2026), on the other hand, applies formal-informal distillation on solving mathemat-
ical research problems, but rely heavily on closed-source models with large parameter scale. Often,
current methods assume that a formal goal is already available (Yao et al., 2025; Varambally et al.,
2026; Bourigault et al., 2026). These systems use formal verification as a selection or certification
signal, rather than for error attribution.

6   C ONCLUSION
We introduced M AGENTA, a training-free agentic pipeline that couples informal mathematical rea-
soning with formal verification. Given only a natural-language problem, it produces a reasoning
chain and candidate answer, formalises them as a Lean 4 statement, and generates a checked proof,
with a statement judge deciding whether the formalisation preserves the original problem and an
error judge routing failed attempts to re-derivation or local repair. M AGENTA verifies every prob-
lem on AIME 2025, AIME 2026 and HMMT February 2026 with four reasoners, and with K2-
H ORIZON -7B solves all six IMO 2026 problems. Our ablation experimental results show that ad-
judication is what keeps a certificate meaningful and that diagnostic-conditioned correction reaches
proofs independent resampling does not. Because the pipeline writes the statement it proves, verifi-
cation guarantees correctness only relative to the generated formalisation, not unconditionally with
respect to the original problem. Closing that gap is a question of better autoformalisation rather
than better proof search, which we regard as the main remaining obstacle to Lean-guided natural
language reasoning.


                                                   9
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




R EFERENCES
Alon Albalak, Duy Phung, Nathan Lile, Rafael Rafailov, Kanishk Gandhi, Louis Castricato, Anikait
  Singh, Chase Blagden, Violet Xiang, Dakota Mahan, and Nick Haber. Big-math: A large-scale,
  high-quality math dataset for reinforcement learning in language models, 2025. URL https:
  //arxiv.org/abs/2502.17387.
Anthropic.  System Card: Claude Opus                  4.6.       https://anthropic.com/
  claude-opus-4-6-system-card, 2026.
Pauline Bourigault, Xiaotong Ji, Matthieu Zimmer, Rasul Tutunov, and Haitham Bou Ammar. Risk-
  controlled lean-as-judge for natural-language mathematical reasoning, 2026. URL https://
  arxiv.org/abs/2605.28365.
Nicolo Cesa-Bianchi and Gabor Lugosi. Prediction, Learning, and Games. Cambridge University
  Press, 2006.
Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
   Jin, Chenggang Li, Wenlei Shi, et al. Seed-prover 1.5: Mastering undergraduate-level theorem
   proving via learning from experience. arXiv preprint arXiv:2512.17260, 2025.
Xiaoyang Chen and Xiang Jiang. Moonshine: An autonomous mathematical research agent centered
  on conjecture generation, 2026. URL https://arxiv.org/abs/2606.10806.
Thierry Coquand and Gérard Huet. The Calculus of Constructions. Information and Computation,
  76(2–3):95–120, 1988. URL https://doi.org/10.1016/0890-5401(88)90005-3.
Rob Cornish, Iacopo Ghinassi, Po-Hung Yeh, Shuqi Liu, Qiyuan Xu, Haoxuan Yin, Dominik Wag-
  ner, Wenda Li, Yee Whye Teh, and Luke Ong. Faithformbench: Benchmarking faithfulness of
  mathematical chain-of-thought autoformalisation. arXiv preprint arXiv:2608.10916, 2026.
Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang, and Mao Yang.
  rStar-math: Small LLMs can master math reasoning with self-evolved deep thinking. In Aarti
  Singh, Maryam Fazel, Daniel Hsu, Simon Lacoste-Julien, Felix Berkenkamp, Tegan Maharaj,
  Kiri Wagstaff, and Jerry Zhu (eds.), Proceedings of the 42nd International Conference on Ma-
  chine Learning, volume 267 of Proceedings of Machine Learning Research, pp. 20640–20661.
  PMLR, 13–19 Jul 2025. URL https://proceedings.mlr.press/v267/guan25f.
  html.
Yichen Huang and Lin F. Yang. Winning gold at imo 2025 with a model-agnostic verification-and-
  refinement pipeline, 2025. URL https://arxiv.org/abs/2507.15855.
Eric Jiang, Xiao Liang, Yikai Zhang, Yingjia Wan, Mengting Li, Haikang Deng, Alexander K.
  Taylor, Justin Baker, Rushil Raghavan, Junyi Zhang, Ying Nian Wu, Andrea L. Bertozzi, Kai-
  Wei Chang, Raghu Meka, Matthew Sottile, Nanyun Peng, Amit Sahai, Terence Tao, and Wei
  Wang. From solvers to research: Large language model-driven formal mathematics at the research
  frontier, 2026. URL https://arxiv.org/abs/2607.07779.
Sayash Kapoor, Benedikt Stroebl, Zachary S Siegel, Nitya Nadgir, and Arvind Narayanan. AI
  agents that matter. Transactions on Machine Learning Research, 2025. ISSN 2835-8856. URL
  https://openreview.net/forum?id=Zy4uFzMviZ.
Tyson Klingner, Drew Bladek, Escher Crawford, Bohao Chen, Ariel Fu, Kaira Nair, Jarod Alper,
  Giovanni Inchiostro, and Vasily Ilin. Evaluation of LLMs for mathematical formalization in Lean,
  2026. URL https://arxiv.org/abs/2606.05632.
Joshua Ong Jun Leang, Aryo Pradipta Gema, and Shay B Cohen. CoMAT: Chain of Mathemat-
  ically Annotated Thought Improves Mathematical Reasoning. In Christos Christodoulopoulos,
  Tanmoy Chakraborty, Carolyn Rose, and Violet Peng (eds.), Proceedings of the 2025 Con-
  ference on Empirical Methods in Natural Language Processing, pp. 20245–20274, Suzhou,
  China, November 2025a. Association for Computational Linguistics. ISBN 979-8-89176-332-
  6. doi: 10.18653/v1/2025.emnlp-main.1024. URL https://aclanthology.org/2025.
  emnlp-main.1024/.


                                               10
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




Joshua Ong Jun Leang, Giwon Hong, Wenda Li, and Shay B Cohen. Theorem Prover as a Judge
  for Synthetic Data Generation. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mo-
  hammad Taher Pilehvar (eds.), Proceedings of the 63rd Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers), pp. 29941–29977, Vienna, Austria, July
  2025b. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/
  2025.acl-long.1448. URL https://aclanthology.org/2025.acl-long.1448/.
Joshua Ong Jun Leang, Zheng Zhao, Aryo Pradipta Gema, Sohee Yang, Wai-Chung Kwan, Xuanli
  He, Wenda Li, Pasquale Minervini, Eleonora Giunchiglia, and Shay B Cohen. PiCSAR: Prob-
  abilistic confidence selection and ranking for reasoning chains. In Maria Liakata, Viviane P.
  Moreira, Jiajun Zhang, and David Jurgens (eds.), Findings of the Association for Computa-
  tional Linguistics: ACL 2026, pp. 31511–31544, San Diego, California, United States, July
  2026a. Association for Computational Linguistics. ISBN 979-8-89176-395-1. doi: 10.18653/v1/
  2026.findings-acl.1577. URL https://aclanthology.org/2026.findings-acl.
  1577/.
Joshua Ong Jun Leang, Zheng Zhao, Mihaela Cătălina Stoian, Qiyuan Xu, Haonan Li, Wenda
  Li, Shay B. Cohen, and Eleonora Giunchiglia. Pythagoras-prover: Advancing efficient formal
  proving via augmented lean formalisation, 2026b. URL https://arxiv.org/abs/2606.
  12594.
Zhuochun Li, Yong Zhang, Ming Li, Yuelyu Ji, Yiming Zeng, Ning Cheng, Yun Zhu, Yanmeng
  Wang, Shaojun Wang, Jing Xiao, and Daqing He. Rethinking LLM-as-a-judge: Representation-
  as-a-judge with small language models via semantic capacity asymmetry. In The Fourteenth
  International Conference on Learning Representations, 2026. URL https://openreview.
  net/forum?id=VAISvCsrvG.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
  Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
  Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover-V2: Scaling
  Formal Theorem Proving with Scaffolded Data Synthesis and Self-Correction. In The Fourteenth
  International Conference on Learning Representations, 2026. URL https://openreview.
  net/forum?id=j4C0nALrgK.
Nick Littlestone. Learning quickly when irrelevant attributes abound: A new linear-threshold algo-
  rithm. In 28th Annual Symposium on Foundations of Computer Science (sfcs 1987), pp. 68–77,
  1987. doi: 10.1109/SFCS.1987.37.
Chengwu Liu, Ye Yuan, Yichun Yin, Yan Xu, Xin Xu, Zaoyu Chen, Yasheng Wang, Lifeng Shang,
  Qun Liu, and Ming Zhang. Safe: Enhancing mathematical reasoning in large language mod-
  els via retrospective step-aware formal verification. In Wanxiang Che, Joyce Nabende, Ekate-
  rina Shutova, and Mohammad Taher Pilehvar (eds.), Proceedings of the 63rd Annual Meeting
  of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 12171–12186,
  Vienna, Austria, July 2025. Association for Computational Linguistics. ISBN 979-8-89176-
  251-0. doi: 10.18653/v1/2025.acl-long.594. URL https://aclanthology.org/2025.
  acl-long.594/.
Chris Yuhao Liu, Liang Zeng, Jiacai Liu, Rui Yan, Jujie He, Chaojie Wang, Shuicheng Yan, Yang
  Liu, and Yahui Zhou. Skywork-reward: Bag of tricks for reward modeling in LLMs, 2024. URL
  https://arxiv.org/abs/2410.18451.
Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, jiawei liu, Yunzhou Xie, Junqiao
  Zhao, Qiufeng Wang, Lihong Zhi, Jia LI, and Wenda Li. Numina-lean-agent: An open and general
  agentic reasoning system for formal mathematics. In Forty-third International Conference on
  Machine Learning, 2026. URL https://openreview.net/forum?id=0bTEd4LpQr.
Qing Lyu, Shreya Havaldar, Adam Stein, Li Zhang, Delip Rao, Eric Wong, Marianna Apidi-
  anaki, and Chris Callison-Burch. Faithful Chain-of-Thought Reasoning. In Jong C. Park,
  Yuki Arase, Baotian Hu, Wei Lu, Derry Wijaya, Ayu Purwarianti, and Adila Alfa Krisnadhi
  (eds.), Proceedings of the 13th International Joint Conference on Natural Language Process-
  ing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational

                                               11
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




  Linguistics (Volume 1: Long Papers), pp. 305–329, Nusa Dua, Bali, November 2023. Asso-
  ciation for Computational Linguistics. doi: 10.18653/v1/2023.ijcnlp-main.20. URL https:
  //aclanthology.org/2023.ijcnlp-main.20/.

David Ma, Kaijing Ma, Shawn Guo, Yunfeng Shi, Enduo Zhao, Jiajun Shi, Zhaoxiang Zhang, Gavin
  Cheung, Jiaheng Liu, and Zili Wang. OProver: A unified framework for agentic formal theorem
  proving, 2026. URL https://arxiv.org/abs/2605.17283.

Iman Mirzadeh, Keivan Alizadeh, Hooman Shahrokhi, Oncel Tuzel, Samy Bengio, and Mehrdad
  Farajtabar. GSM-Symbolic: Understanding the Limitations of Mathematical Reasoning in
  Large Language Models. In The Thirteenth International Conference on Learning Represen-
  tations, ICLR 2025, Singapore, April 24-28, 2025. OpenReview.net, 2025. URL https:
  //openreview.net/forum?id=AjXkRZIvjB.

Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and programming language.
  In Automated Deduction – CADE 28: 28th International Conference on Automated Deduction,
  Virtual Event, July 12–15, 2021, Proceedings, pp. 625–635, Berlin, Heidelberg, 2021. Springer-
  Verlag. ISBN 978-3-030-79875-8. doi: 10.1007/978-3-030-79876-5 37. URL https://doi.
  org/10.1007/978-3-030-79876-5_37.

Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei, Hannaneh Hajishirzi,
  Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori Hashimoto. s1: Simple test-
  time scaling. In Christos Christodoulopoulos, Tanmoy Chakraborty, Carolyn Rose, and Violet
  Peng (eds.), Proceedings of the 2025 Conference on Empirical Methods in Natural Language
  Processing, pp. 20275–20321, Suzhou, China, November 2025. Association for Computational
  Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.1025. URL https:
  //aclanthology.org/2025.emnlp-main.1025/.

OpenAI. OpenAI GPT-5 System Card, 2026. URL https://arxiv.org/abs/2601.03267.

Azim Ospanov, Zijin Feng, Jiacheng Sun, Haoli Bai, SHEN XIN, and Farzan Farnia. HERMES:
  Towards efficient and verifiable mathematical reasoning in LLMs. In Forty-third International
  Conference on Machine Learning, 2026. URL https://openreview.net/forum?id=
  w7BZcUc0fJ.

Lawrence C. Paulson. Isabelle - A Generic Theorem Prover (with a contribution by T. Nipkow),
  volume 828 of Lecture Notes in Computer Science. Springer, 1994. ISBN 3-540-58244-4. doi:
  10.1007/BFB0030541. URL https://doi.org/10.1007/BFb0030541.

Xin Quan, Marco Valentino, Louise A. Dennis, and Andre Freitas. Faithful and robust LLM-driven
  theorem proving for NLI explanations. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and
  Mohammad Taher Pilehvar (eds.), Proceedings of the 63rd Annual Meeting of the Association for
  Computational Linguistics (Volume 1: Long Papers), pp. 17734–17755, Vienna, Austria, July
  2025. Association for Computational Linguistics. ISBN 979-8-89176-251-0. doi: 10.18653/v1/
  2025.acl-long.867. URL https://aclanthology.org/2025.acl-long.867/.

Qwen Team. Qwen3.6-27B: Flagship-Level Coding in a 27B Dense Model, April 2026. URL
 https://qwen.ai/blog?id=qwen3.6-27b.

Subham Sekhar Sahoo, Marianne Arriola, Yair Schiff, Aaron Gokaslan, Edgar Marroquin,
  Justin T Chiu, Alexander Rush, and Volodymyr Kuleshov. Simple and Effective Masked
  Diffusion Language Models. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Pa-
  quet, J. Tomczak, and C. Zhang (eds.), Advances in Neural Information Processing Sys-
  tems, volume 37, pp. 130136–130184. Curran Associates, Inc., 2024. doi: 10.52202/
  079017-4135. URL https://proceedings.neurips.cc/paper_files/paper/
  2024/file/eb0b13cc515724ab8015bc978fdde0ad-Paper-Conference.pdf.

Varvara Sazonova, Dmitri Shmelkin, Stanislav Kikot, and Vasily Motolygin. Pipeline for verify-
  ing LLM-generated mathematical solutions, 2026. URL https://arxiv.org/abs/2602.
  20770.


                                              12
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
  Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of mathe-
  matical reasoning in open language models, 2024. URL https://arxiv.org/abs/2402.
  03300.

Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar. Scaling LLM test-time compute
  optimally can be more effective than scaling parameters for reasoning. In The Thirteenth Interna-
  tional Conference on Learning Representations, 2025. URL https://openreview.net/
  forum?id=4FWAwZtd2n.

Kimi Team. Kimi K3: open frontier intelligence, 2026. URL https://arxiv.org/abs/
  2607.24653.

George Tsoukalas, Jasper Lee, John Jennings, Jimmy Xin, Michelle Ding, Michael Jennings,
  Amitayush Thakur, and Swarat Chaudhuri. PutnamBench: Evaluating Neural Theorem-Provers
  on the Putnam Mathematical Competition. In A. Globerson, L. Mackey, D. Belgrave, A. Fan,
  U. Paquet, J. Tomczak, and C. Zhang (eds.), Advances in Neural Information Processing Systems,
  volume 37, pp. 11545–11569. Curran Associates, Inc., 2024. doi: 10.52202/079017-0368.
  URL https://proceedings.neurips.cc/paper_files/paper/2024/file/
  1582eaf9e0cf349e1e5a6ee453100aa1-Paper-Datasets_and_Benchmarks_
  Track.pdf.

George Tsoukalas, Anton Kovsharov, Sergey Shirobokov, Anja Surina, Moritz Firsching, Gergely
  Bérczi, Francisco JR Ruiz, Arun Suggala, Adam Zsolt Wagner, Eric Wieser, et al. Advancing
  mathematics research with ai-driven formal proof search. arXiv preprint arXiv:2605.22763, 2026.

Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert:
  Recursively building formal proofs with informal reasoning. In The Fourteenth International
  Conference on Learning Representations, 2026. URL https://openreview.net/forum?
  id=GN8OdkTo3B.

Jianing Wang, Jianfei Zhang, Qi Guo, Linsen Guo, Rumei Li, Chao Zhang, Chong Peng, Cunguang
   Wang, Dengchang Zhao, Jiarong Shi, Jingang Wang, et al. Longcat-flash-prover: Advancing
   native formal reasoning via agentic tool-integrated reinforcement learning, 2026. URL https:
   //arxiv.org/abs/2603.21065.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, brian ichter, Fei Xia, Ed Chi, Quoc V
  Le, and Denny Zhou. Chain-of-Thought Prompting Elicits Reasoning in Large Language Mod-
  els. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), Advances in
  Neural Information Processing Systems, volume 35, pp. 24824–24837. Curran Associates, Inc.,
  2022. URL https://proceedings.neurips.cc/paper_files/paper/2022/
  file/9d5609613524ecf4f15af0f7b31abca4-Paper-Conference.pdf.

Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-
  Scale Synthetic Data, 2024. URL https://arxiv.org/abs/2405.14333.

Qiyuan Xu, Joshua Ong Jun Leang, Renxi Wang, Wenda Li, Haonan Li, Luke Ong, and Conrad
  Watt. AoA: Theorem proving agent over abstract syntax tree of redesigned language, 2026. URL
  https://arxiv.org/abs/2607.16372.

Jiarui Yao, Ruida Wang, and Tong Zhang. FANS: Formal answer selection for LLM natural lan-
   guage math reasoning using Lean4. In Christos Christodoulopoulos, Tanmoy Chakraborty, Car-
   olyn Rose, and Violet Peng (eds.), Proceedings of the 2025 Conference on Empirical Methods in
   Natural Language Processing, pp. 3181–3200, Suzhou, China, November 2025. Association for
   Computational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.158.
   URL https://aclanthology.org/2025.emnlp-main.158/.

Erez Yosef, Oron Anschel, Shunit Haviv Hakimi, Asaf Gendler, Adam Botach, Nimrod Berman, and
  Igor Kviatkovsky. Rethinking math reasoning evaluation: A robust LLM-as-a-judge framework
  beyond symbolic rigidity, 2026. URL https://arxiv.org/abs/2604.22597.


                                                13
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




Lan Zhang, Marco Valentino, and Andre Freitas. Autoformalization in the wild: Assessing LLMs
  on real-world mathematical definitions. In Christos Christodoulopoulos, Tanmoy Chakraborty,
  Carolyn Rose, and Violet Peng (eds.), Proceedings of the 2025 Conference on Empirical Methods
  in Natural Language Processing, pp. 1720–1738, Suzhou, China, November 2025a. Association
  for Computational Linguistics. ISBN 979-8-89176-332-6. doi: 10.18653/v1/2025.emnlp-main.
  90. URL https://aclanthology.org/2025.emnlp-main.90/.
Qiyuan Zhang, Fuyuan Lyu, Zexu Sun, Lei Wang, Weixu Zhang, Wenyue Hua, Haolun Wu, Zhihan
  Guo, Yufei Wang, Niklas Muennighoff, Irwin King, Xue Liu, and Chen Ma. A survey on test-
  time scaling in large language models: What, how, where, and how well?, 2025b. URL https:
  //arxiv.org/abs/2503.24235.
Zhenru Zhang, Chujie Zheng, Yangzhen Wu, Beichen Zhang, Runji Lin, Bowen Yu, Dayiheng Liu,
  Jingren Zhou, and Junyang Lin. The lessons of developing process reward models in mathematical
  reasoning. In Wanxiang Che, Joyce Nabende, Ekaterina Shutova, and Mohammad Taher Pilehvar
  (eds.), Findings of the Association for Computational Linguistics: ACL 2025, pp. 10495–10516,
  Vienna, Austria, July 2025c. Association for Computational Linguistics. ISBN 979-8-89176-256-
  5. doi: 10.18653/v1/2025.findings-acl.547. URL https://aclanthology.org/2025.
  findings-acl.547/.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. MiniF2F: a cross-system benchmark for
  formal Olympiad-level mathematics. In International Conference on Learning Representations,
  2022. URL https://openreview.net/forum?id=9ZPegFuFTFv.
Jin Peng Zhou, Charles Staats, Wenda Li, Christian Szegedy, Kilian Q. Weinberger, and Yuhuai
   Wu. Don’t trust: Verify – grounding LLM quantitative reasoning with autoformalization. In
   The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria,
   May 7-11, 2024. OpenReview.net, 2024. URL https://openreview.net/forum?id=
   V5tdi14ple.




                                              14
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




A        A LGORITHM

A.1         N OTATION S UMMARY

Table 4 summarises the notation used throughout the description and analysis of M AGENTA.


                    Table 4: Summary of the principal notation used in M AGENTA.

    Symbol                Domain or type         Description
    Problems and generated artefacts
    Q, q               q∈Q                       Natural-language mathematics problems, and an in-
                                                 dividual problem.
    A, at                 at ∈ A                 Candidate answers, and the answer proposed by the
                                                 reasoner at round t.
    a⋆ , â               ∈A                     Reference answer, used only for evaluation and never
                                                 shown to the pipeline; and the answer finally re-
                                                 turned.
    C, ct                 ct ∈ C                 Informal reasoning chains, and the chain generated at
                                                 round t.
    S, s                  s∈S                    Lean 4 theorem statements, and a generated state-
                                                 ment.
    P, π                  π∈P                    Lean 4 proof scripts, and a candidate proof.
    Es                    Diagnostic space       Statement-elaboration diagnostics returned by Vs .
    Ep , e                e ∈ Ep                 Proof-verification diagnostics returned by Vp , and the
                                                 diagnostic from a failed attempt.
    Fmath , φt            φt ∈ Fmath             Mathematical-correction feedback built from a failed
                                                 attempt, (ct , at , s, π, e). Constructed only when Je
                                                 returns MATH.
    ∅                     Empty signal           Absence of feedback: φ = ∅ on the first reasoning
                                                 round, ϵ = ∅ on the first proof attempt.
    Pipeline components
    R                     Q × Fmath → C × A      Reasoner: produces an informal chain and candidate
                                                 answer.
    F                     Q×A→S                  Formaliser: renders the problem and candidate an-
                                                 swer as a Lean 4 statement.
    P                     Q × C × S × Ep → P     Prover: generates or repairs a Lean 4 proof script.
    Vs                    S → {⊤} ∪ Es           Statement checker: elaborates s in Lean (well-
                                                 formedness only).
    Vp                    S × P → {⊤} ∪ Ep       Proof checker: Lean kernel plus SafeVerify on the
                                                 unchanged statement.
    Js , b                b ∈ {0, 1}             Statement judge and its verdict; b = 1 accepts the
                                                 formalisation.
    Je , ℓ                ℓ ∈ {MATH, S YNTAX}    Error judge and its label, routing a failed attempt to
                                                 re-derivation or to local Lean repair.
    ⊤                     Success verdict        A check passed: elaboration for Vs , kernel and
                                                 SafeVerify acceptance for Vp .
    Budgets and evaluation
    T, M, K             ∈N                       Maximum reasoner attempts, formalisation samples
                                                 per candidate answer, and proof attempts per ac-
                                                 cepted statement.
    D                     Set of problems        The evaluation benchmark.
    Ver(q)                ∈ {0, 1}               Indicator that q terminated with an adjudicated state-
                                                 ment and a kernel-accepted proof.
    u, β                  u : D → R≥0            A per-problem cost measure and a budget on it, used
                                                 in Equation 2.


                                                15
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




A.2    F ULL D ETAILS
Algorithm 1 specifies the complete inference procedure using the notation of §2.1. The budgets T ,
M and K bound reasoner attempts, formal-statement samples for a fixed answer, and proof attempts
for an accepted statement, respectively. The procedure returns the verified reasoning chain, answer,
statement and proof (c, a, s, π), or UNCERTIFIED if an applicable budget is exhausted. Per problem
it issues at most T reasoner calls, T M formaliser and statement-judge calls, and T K prover, verifier
and error-judge calls, so adjudication is cheap relative to proof search whenever M ≪ K, which is
the regime we operate in and the reason adjudication precedes proving.

                                    Algorithm 1: M AGENTA inference.

Require: problem q; components R, F, P, Vs , Vp , Js , Je ; budgets T, M, K
Ensure: verified output (c, a, s, π), or UNCERTIFIED
  1: φ ← ∅                                                                            ▷ reasoner feedback state
  2: for t = 1, . . . , T do
  3:    (ct , at ) ∼ R(q, φ)                                            ▷ Phase 1: natural-language reasoning
  4:    zs ← 0                                                                      ▷ no accepted statement yet
  5:    for m = 1, . . . , M do                                          ▷ Steps 1–2: formalise and adjudicate
  6:        sm ∼ F (q, at )
  7:        um ← Vs (sm )
  8:        if um ̸= ⊤ then continue                                        ▷ resample an ill-formed statement
  9:        bm ∼ Js (q, at , sm )
 10:        if bm = 1 then s ← sm ; zs ← 1; break
 11:    if zs = 0 then return UNCERTIFIED
 12:    ϵ←∅
 13:    zmath ← 0
 14:    for k = 1, . . . , K do                                                       ▷ Step 3: prove and verify
 15:        π ∼ P (q, ct , s, ϵ)
 16:        e ← Vp (s, π)
 17:        if e = ⊤ then return (ct , at , s, π)                                       ▷ Step 5: verified output
 18:        ℓ ∼ Je (q, ct , at , s, π, e)                                             ▷ Step 4: error attribution
 19:        if ℓ = MATH then
 20:            φ ← (ct , at , s, π, e); zmath ← 1; break                        ▷ construct feedback in Fmath
 21:        ϵ←e                                                           ▷ S YNTAX: repair the proof in place
 22:    if zmath = 0 then return UNCERTIFIED
 23: return UNCERTIFIED                                                            ▷ reasoner budget exhausted


Algorithms 2–4 decompose the same procedure into its controller, statement-search and proof-search
routines. Statement search resamples F whenever Vs rejects an ill-formed statement or Js rejects an
unfaithful one; neither failure changes (c, a) or returns control to R. Once a statement is accepted
it remains fixed throughout proof search. A S YNTAX label returns the verifier diagnostic to P for
local proof repair, whereas only a MATH label constructs feedback in Fmath and invokes R again.




                                                       16
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                          Algorithm 2: End-to-end controller for M AGENTA.

Require: problem q; components R, F, P, Vs , Vp , Js , Je ; budgets T, M, K
Ensure: verified output (c, a, s, π), or UNCERTIFIED
  1: φ ← ∅
  2: for t = 1, . . . , T do                                                    ▷ mathematical-revision loop
  3:    (ct , at ) ∼ R(q, φ)
  4:    (zs , s) ← StatementSearch(q, at ; F, Vs , Js , M )
  5:    if zs = REJECTED then return UNCERTIFIED
  6:    (zp , π, e) ← ProofSearch(q, ct , at , s; P, Vp , Je , K)
  7:    if zp = CERTIFIED then return (ct , at , s, π)
  8:    if zp = MATH - ERROR then
  9:        φ ← (ct , at , s, π, e); continue                                  ▷ construct feedback in Fmath
 10:    if zp = REPAIR - EXHAUSTED then return UNCERTIFIED
 11: return UNCERTIFIED                                                          ▷ reasoner budget exhausted




                             Algorithm 3: Faithful formal-statement search.

Require: problem q; candidate answer a; formaliser F ; statement verifier Vs ; statement judge Js ; budget M
Ensure: (ACCEPTED, s) or (REJECTED, ∅)
  1: for m = 1, . . . , M do
  2:    sm ∼ F (q, a)                                    ▷ generate a closed answer-carrying Lean signature
  3:    um ← Vs (sm )                                                        ▷ elaborate the statement in Lean
  4:    if um ̸= ⊤ then continue                                                            ▷ resample from F
  5:    bm ∼ Js (q, a, sm )
  6:                                                 ▷ check the problem structure and the proposed answer
  7:    if bm = 1 then return (ACCEPTED, sm )
  8: return (REJECTED, ∅)




                    Algorithm 4: Syntax-guided proof repair and error attribution.

Require: problem q; chain c; answer a; immutable statement s; prover P ; proof verifier Vp ; error judge Je ;
budget K
Ensure: status in {CERTIFIED, MATH - ERROR, REPAIR - EXHAUSTED}, proof, diagnostic
  1: ϵ ← ∅; πlast ← ∅; elast ← ∅
  2: for k = 1, . . . , K do
  3:    πk ∼ P (q, c, s, ϵ)                                   ▷ preserve q, c, s; repair only the Lean body
  4:    πlast ← πk
  5:    ek ← Vp (s, πk )                                                   ▷ Lean and SafeVerify checking
  6:    if ek = ⊤ then return (CERTIFIED, πk , ∅)
  7:    elast ← ek
  8:    ℓk ∼ Je (q, c, a, s, πk , ek )
  9:    if ℓk = MATH then
 10:        return (MATH - ERROR, πk , ek )                                          ▷ route to the reasoner
 11:    ϵ ← ek                                                 ▷ S YNTAX: condition the next local repair
 12: return (REPAIR - EXHAUSTED, πlast , elast )



For IMO 2026, a final completeness judge is applied only after Algorithm 4 returns CERTIFIED. It
compares (q, c, a) with (s, π) and returns incomplete proof when the formal certificate omits
or misaligns a substantive part of the informal solution. This is an additional acceptance filter; it
does not replace Lean or alter the feedback routing above.


                                                     17
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




B     I MPLEMENTATION D ETAILS FOR M AGENTA

B.1   P ROMPT TEMPLATES

The templates below are reproduced verbatim from the experimental harness.
 K2 informal-reasoner prompt
 You are an expert mathematical problem solver. Solve the problem carefully and show enough
 ,→ reasoning to make the solution understandable. End with the final answer in the exact
 ,→ form \boxed{answer}. Do not put anything after the boxed answer.

 {original_problem}


 K2 mathematical self-correction prompt
 Solve the original mathematics problem again and produce a complete corrected mathematical
 ,→ solution.

 A downstream formal-verification audit classified the previous mathematical reasoning as
 ,→ defective.

 Use the latest Lean code and exact verifier diagnostic below only as evidence locating the
 ,→ mathematical defect.

 Do not focus on Lean syntax or tactics. Re-derive the mathematics, correct the answer if
 ,→ necessary, and provide a self-contained solution.

 End with one clear final answer in \boxed{...}.

 Closed-loop regeneration cycle: {cycle}

 Original problem:

 {original_problem}

 Previous mathematical solution:

 {previous_mathematical_solution}

 Immutable Lean target generated from that solution:

 {immutable_lean_target}

 Latest Lean proof attempt:

 {latest_lean_proof_attempt}

 Exact Lean/SafeVerify diagnostic:

 {lean_or_safeverify_diagnostic}


 Goedel formaliser prompt
 Please autoformalize the following natural language problem statement in Lean 4.

 The natural language statement is:

 {informal_statement_content}

 Think before you provide the lean statement.


 DeepSeek statement-alignment judge prompt
 Judge whether the candidate Lean 4 theorem statement faithfully formalizes the supplied
 ,→ question together with the generator's proposed final answer.

 This is a statement-alignment judgment only. Do not write a proof and do not repair or
 ,→ rewrite the statement.

 Do not independently solve the problem, recompute the answer, correct the generator's
 ,→ mathematics, or prefer your own conclusion. A mathematically wrong proposed answer
 ,→ must still be judged right when the Lean statement faithfully encodes that answer and
 ,→ the original task structure.




                                                18
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 The original question controls domains, hypotheses, quantifiers, constraints, and the
 ,→ requested quantity.

 The proposed answer controls the concrete claimed result. Do not silently replace it with
 ,→ a different answer.

 Return verdict right only when the candidate preserves both sources without missing
 ,→ assumptions, extra assumptions, weakened conclusions, strengthened conclusions,
 ,→ hard-coded loopholes, or a changed answer.

 Return verdict wrong otherwise and precisely describe the mismatch.

 Return only one strict JSON object with exactly these string fields: verdict, rationale,
 ,→ mismatch_details. verdict must be right or wrong. mismatch_details must be empty when
 ,→ right and nonempty when wrong.

 Exact appended question passed to the formalizer:

 {answer_appended_question}

 Original natural-language question:

 {original_question}

 Generator's proposed final answer:

 {proposed_answer}

 Candidate Lean 4 theorem statement:

 {candidate_lean4_theorem_statement}


 Leanstral proof-generation prompt
 Produce a complete Lean 4 proof of the supplied theorem signature.

 1. This is a formal translation and verification task, not an independent mathematics
 ,→ attempt.
 2. Copy the theorem signature verbatim and do not weaken, strengthen, rename, or otherwise
 ,→ alter it.
 3. Formalize the supplied K2 solution's reasoning and claimed conclusion without
 ,→ correcting, replacing, or bypassing its mathematics. Add only Lean-specific
 ,→ bookkeeping needed to express the same steps.
 4. Do not substitute an independent proof strategy merely because it proves the statement.
 ,→ Do not use `native_decide` or another exhaustive computation unless the supplied
 ,→ solution itself explicitly used that strategy.
 5. If the supplied mathematics is false or insufficient, do not invent assumptions or
 ,→ silently repair it.
 6. Use the available Lean compiler and lean-lsp-mcp tools to inspect errors and
 ,→ iteratively repair only the Lean implementation.
 7. Edit `Main.lean` in the current working directory. It must import Mathlib and must not
 ,→ use `sorry`, `admit`, axioms, unsafe declarations, fabricated assumptions, or the
 ,→ conclusion as a hypothesis.
 8. Before editing the final code, provide a detailed Lean-oriented proof plan covering the
 ,→ main steps, intermediate lemmas, and tactics.

 Original informal problem (authoritative for task structure):
 {original_question}

 Answer-appended question supplied to K2 (the answer is parsed from the K2 solution, not
 ,→ from ground truth):
 {answer_appended_question}

 Supplied K2 final mathematical solution (content after the private thinking marker;
 ,→ authoritative for the reasoning and claimed conclusion):
 {k2_final_mathematical_solution}

 Lean 4 theorem signature that must be preserved verbatim:
 {immutable_lean4_theorem_signature}

 Current `Main.lean`:
 ```lean4
 {current_Main_lean}
 ```




                                             19
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 DeepSeek error-classification prompt
 Classify the root cause of this failed Lean 4 proof attempt.

 This is a routing-only classification task. Do not repair the Lean code, do not suggest
 ,→ tactics, and do not provide feedback for the prover.

 Return math_error only when the supplied mathematical reasoning or claimed answer is
 ,→ itself false or insufficient, and the verifier evidence materially exposes that
 ,→ mathematical defect.

 Return code_error for syntax, elaboration, typing, tactic, missing-lemma, namespace,
 ,→ coercion, timeout, forbidden-token, changed-target, SafeVerify protocol, or
 ,→ incomplete-proof failures that could be fixed while preserving the same mathematics.

 A difficult or currently unsolved proof is code_error. SafeVerify rejection caused by
 ,→ changing the theorem is code_error.

 When evidence is ambiguous, return code_error. Do not independently replace the proposed
 ,→ answer.

 Return only one strict JSON object with exactly these string fields: classification,
 ,→ rationale, evidence.

 classification must be code_error or math_error. Keep rationale and evidence concise.

 Original problem:

 {original_question}

 proposed answer:

 {proposed_answer}

 mathematical solution:

 {mathematical_solution}

 Immutable Lean theorem target:

 {immutable_lean_theorem_target}

 Latest Lean candidate:

 {latest_lean_candidate}

 Verifier stage:

 {verifier_stage}

 Exact Lean/SafeVerify diagnostic:

 {exact_lean_or_safeverify_diagnostic}



B.2   H YPERPARAMETER S ETTINGS
      1. Budgets. For all the experiments, we use T = 32 reasoner attempts, M = 512 formal-
         statement samples per candidate answer and K = 4096 proof attempts per accepted state-
         ment. For computational efficiency, the ablations of §4.3, run the pipeline in batched mode
         with a batch size 32 .
      2. Reasoner. We use temperature 0.6, top p = 0.95, a maximum output length of 64,000
         tokens (128,000 for IMO 2026), and thinking=auto. The random seed is 42 for the
         main evaluation. The reasoner is served with a 524,288-token context window. During
         self-correction, incomplete responses are resampled if they reach the token limit without
         emitting the post-thinking marker (this counts toward the budget T ). In practice, this never
         occurred in our experiments.
      3. Goedel formaliser. We use temperature 0.9, top k = 20, top p = 0.95, a maximum
         output length of 16,384 tokens, and seed 42. The model is served with a 40,960-token
         context window. Each extracted theorem statement is checked in Lean with a temporary
         sorry proof.
      4. DeepSeek statement-alignment judge. We use temperature 1.0, top p = 1.0, a max-
         imum output length of 32,000 tokens, and reasoning effort max. Only statements that
         have already passed Lean elaboration are submitted to this judge. The model is served


                                                 20
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




         with a 65,536-token context window, tensor parallelism 8, pipeline parallelism 1, GPU-
         memory utilisation 0.90, FP8 KV cache, block size 256, prefix caching and expert paral-
         lelism. DS PARK speculative decoding is enabled with seven speculative tokens and greedy
         draft sampling.
     5. DeepSeek error-attribution judge. The error-attribution judge uses the same checkpoint
        and hyperparameters as the statement-alignment judge but is issued as a separate call, and
        returns either code error or math error.
     6. Leanstral proof agent. We use mistralai/Leanstral-1.5-119B-A6B through
        Mistral Vibe 2.18.4, with decoding temperature 1.0, thinking level high and reasoning ef-
        fort high. The served context length is 200,000 tokens and automatic context compaction
        is triggered at 168,000 tokens. Compaction preserves the trajectory, and the cumulative
        token counter is not reset after compaction. The server permits at most 80,000 newly gen-
        erated tokens per request, while the experimental wrapper applies a stricter 32,000-token
        per-call output limit. The cumulative output-token budget is 4,000,000 tokens per proof
        trajectory.
     7. Lean tools and final certification. The proof environment uses Lean v4.29.1. A result
        is accepted only when the theorem statement is unchanged, Lean returns exit code zero,
        SafeVerify returns exit code zero, neither verifier times out, and the proof contains no
        forbidden constructs such as sorry, admit, new axioms, unsafe or native decide.
     8. Codex comparator and fallback. The C ODEX formaliser and proof backend use
        gpt-5.6-sol with reasoning effort ultra.

C    R EFINEMENT ROUNDS ACROSS M ODELS AND DATASETS

Table 5: Reported average and maximum rounds required across models and datasets, counting the
initial attempt as round 1. Average counts are rounded.

                                      K2-Horizon-7B         K2-Horizon-375B
                     Dataset       Average    Maximum      Average   Maximum
                     AIME2025             1            3         1            1
                     AIME2026             2            5         1            2
                     HMMT2026             3           10         1            2

Table 5 shows that refinement effort varies across both models and datasets. K2-Horizon-7B requires
approximately one, two and three rounds on average for AIME2025, AIME2026 and HMMT2026,
respectively. Its maximum increases from three to five and ten rounds, showing that some in-
stances require substantially more refinement than the dataset average. K2-Horizon-375B requires
approximately one round on average across all three datasets, with at most one additional round on
AIME2026 and HMMT2026.
The shorter trajectories of K2-Horizon-375B are consistent with its reported tendency to produce
correct answers on the first attempt. For K2-Horizon-7B, the increasing refinement effort suggests
that AIME2026 and HMMT2026 pose greater difficulty within this workflow. Lower initial accu-
racy leaves more instances requiring subsequent correction, providing a possible explanation for the
additional rounds. However, the relationship between initial accuracy and round count should be
assessed using the corresponding first-attempt results; round counts alone measure refinement effort
rather than establish a model-independent ranking of dataset difficulty.




                                                21
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




D    AIME2026 F ORMAL AND I NFORMAL P ROOF E XAMPLE
We reproduce a complete audited trajectory for an AIME 2026 problem (see also Figure 1), in
which the initial informal solution is wrong, the error is attributed to the mathematics rather than to
the Lean implementation, and the pipeline recovers. Boxes 1–5 are the failed cycle and boxes 6–9
the corrected one.
  Input question
  Find the number of functions π mapping the set A = {1, 2, 3, 4, 5, 6} onto A such that for every
  a ∈ A,
                                  π(π(π(π(π(π(a)))))) = a.

                                                  ⇓
  1. Informal reasoner — initial generation
  The condition
                            π(π(π(π(π(π(a)))))) = a          for all a ∈ A
  means that the seventh iterate of π is the identity map:
                                             π 7 = idA .
  Hence the order of π must divide 7. Since 7 is prime, the only possible orders are 1 and 7.
  A permutation of a set of size 6 can have order at most 6 (the maximum occurs for a 6-cycle).
  Thus a permutation of order 7 cannot exist on a set of six elements.
  Consequently the only function satisfying π 7 = idA is the identity permutation.

                                                  1

                                                  ⇓
  2. Goedel formaliser — initial generation
  theorem problem_1 :
    Nat.card {π : Equiv.Perm (Fin 6) | ∀ a : Fin 6, (π ˆ 6) a = a} = 1

                                                  ⇓
  3. DeepSeek statement judge

                                             right
                                               ⇓
  4. Leanstral — initial proof generation
  import Mathlib

  open Equiv

  theorem problem_1 :
    Nat.card {π : Equiv.Perm (Fin 6) | ∀ a : Fin 6, (π ˆ 7) a = a} = 1 := by
    have h_set_eq : {π : Equiv.Perm (Fin 6) | ∀ a : Fin 6, (π ˆ 7) a = a} = {1} := by
      ext π
      constructor
      · intro h
        have h_all : ∀ a : Fin 6, (π ˆ 7) a = a := h
        have h_pow : (π ˆ 7) = 1 := by
          apply Equiv.ext
          intro a
          simpa using h_all a
        have h_order_dvd_7 : orderOf π | 7 := orderOf_dvd_of_pow_eq_one h_pow
        have h_prime_7 : Nat.Prime 7 := Nat.prime_seven
        have h_order_cases : orderOf π = 1 ∨ orderOf π = 7 :=
          h_prime_7.eq_one_or_self_of_dvd (orderOf π) h_order_dvd_7
        rcases h_order_cases with (h_order | h_order)
        · have h_one : π = 1 := (orderOf_eq_one_iff.mp h_order)
          simp [h_one]
        · have h_card : Fintype.card (Equiv.Perm (Fin 6)) = 720 := by
            rw [Fintype.card_perm, Fintype.card_fin]




                                                  22
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




           norm_num
         have h_order_dvd_card : orderOf π | Fintype.card (Equiv.Perm (Fin 6)) :=
         ,→ orderOf_dvd_card
         rw [h_card] at h_order_dvd_card
         rw [h_order] at h_order_dvd_card
         have h_7_not_dvd_720 : ¬ (7 : N) | 720 := by
           have h_mod : 720 %
           intro h_dvd
           have h_mod_zero : 720 %
           rw [h_mod] at h_mod_zero
           linarith
         exact absurd h_order_dvd_card h_7_not_dvd_720
     · intro h
       have h_one : π = 1 := by simpa using h
       rw [h_one]
       intro a
       simp
   rw [h_set_eq]
   simp


                                                  ⇓
 5. DeepSeek error attribution
                                          math error
                                                  ⇓
 6. Informal reasoner — corrected generation
 The condition π(π(π(π(π(π(a)))))) = a for all a ∈ A means that the sixth iterate of π is
 the identity, i.e., π 6 = idA . Since π maps A onto A and A is finite, π is a bijection, hence a
 permutation of A. The order of π divides 6, so we must count the permutations in S6 whose
 order divides 6.
 The order of a permutation is the least common multiple of its cycle lengths. Thus the order
 divides 6 if and only if all cycle lengths belong to {1, 2, 3, 6} (cycles of length 4 or 5 would give
 orders 4 or 5, which do not divide 6). We count the permutations by their cycle types:
        • One 6-cycle: (6 − 1)! = 120
        • Two 3-cycles: 326!·2! = 720
                                   18 = 40
                                                   6!
        • One 3-cycle, one 2-cycle, one 1-cycle: 3·2·1 = 720
                                                          6 = 120
        • One 3-cycle, three 1-cycles: 3·16!3 ·3! = 720
                                                    18 = 40
        • Three 2-cycles: 236!·3! = 720
                                     48 = 15
                                           6!         720
        • Two 2-cycles, two 1-cycles: 22 ·2!·12 ·2! = 16 = 45


        • One 2-cycle, four 1-cycles: 2·16!4 ·4! = 720
                                                    48 = 15
        • Six 1-cycles (identity): 1
 Summing these gives 120 + 40 + 120 + 40 + 15 + 45 + 15 + 1 = 396.

                                                 396

                                                  ⇓
 7. Goedel formaliser — corrected generation
 theorem problem_1 :
   Set.ncard {π : Equiv.Perm (Fin 6) | ∀ a, (πˆ[6]) a = a} = 396


                                                  ⇓
 8. DeepSeek statement judge
                                                yes
                                                  ⇓

                                                  23
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




    9. Leanstral — corrected proof generation
    import Mathlib

    set_option maxRecDepth 10000000
    set_option maxHeartbeats 2000000

    theorem problem_1 :
      Set.ncard {π : Equiv.Perm (Fin 6) | ∀ a, (πˆ[6]) a = a} = 396 := by
      have h_eq : {π : Equiv.Perm (Fin 6) | ∀ a, (πˆ[6]) a = a} = {π | π ˆ 6 = 1} := by
        ext π
        constructor
        · intro h
          ext a
          have ha := h a
          have ha1 : (π ˆ 6) a = a := by
             simpa [Equiv.Perm.iterate_eq_pow π 6] using ha
          simpa [ha1]
        · intro h a
          have h' := congrArg (λ f : Equiv.Perm (Fin 6) => f a) h
          simpa [Equiv.Perm.iterate_eq_pow π 6] using h'
      rw [h_eq]
      have h_fin : Set.Finite {π : Equiv.Perm (Fin 6) | π ˆ 6 = 1} := by
        exact Set.finite_coe_iff.mp inferInstance
      have h_card : Set.ncard {π : Equiv.Perm (Fin 6) | π ˆ 6 = 1} =
          Finset.card ((Finset.univ : Finset (Equiv.Perm (Fin 6))).filter (λ π => π ˆ 6 = 1))
          ,→ := by
        rw [Set.ncard_eq_toFinset_card _ h_fin]
        congr
        ext π
        simp
      rw [h_card]
      decide




E     E RROR A NALYSIS

E.1     F ORMAL S TATEMENT E RROR A NALYSIS


Table 6: Formal-statement generation and adjudication errors (%) across all 30 AIME 2026 prob-
lems. Generated percentages are normalised over all Goedel statements. Conditional percentages
are normalised over the statements reaching the relevant stage: all pre-judge rejections for the error
categories and all Lean-passing statements for the DeepSeek outcomes.

                     Outcome or first failure category          Generated   Conditional
                     All-30 Goedel generation outcomes
                     Lean elaborated                                66.55            –
                     Lean compiler error                            33.08            –
                     Statement extraction failure                    0.22            –
                     Input context overflow                          0.16            –
                     First cause among rejected all-30 statements
                     Type, coercion, or projection mismatch         17.47         52.23
                     Typeclass or instance synthesis                 7.85         23.46
                     Parser or notation syntax                       4.78         14.28
                     Unknown name or API misuse                      2.73          8.17
                     Statement extraction failure                    0.22          0.66
                     Input context overflow                          0.16          0.47
                     Metavariables or underspecified binders         0.13          0.38
                     Pattern, binder, or match elaboration           0.10          0.31
                     Tactic failure or open goal                     0.01          0.02
                     Resource timeout                                0.01          0.02
                     All-30 compiler-to-DeepSeek outcomes
                     Rejected before judge: Lean error              33.08             –
                     Rejected before judge: extraction error         0.22             –
                     Rejected before judge: context overflow         0.16             –
                     DeepSeek semantic rejection                    44.64         67.08
                     DeepSeek semantic acceptance                   21.91         32.92


                                                      24
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




We generate a full grid of candidate answers and Goedel formalisations for each of the 30
AIME 2026 problems. The audit in Table 6 shows that formal-statement failure is primarily an
elaboration problem rather than a parsing problem. Type, coercion and projection mismatches ac-
count for more than half of rejected statements, and typeclass synthesis for almost a quarter; together
these two categories explain over three quarters of pre-proof rejection. Syntax errors form a much
smaller share, and extraction, context, tactic and timeout failures are negligible. The main obstacle
is therefore expressing the intended mathematics with Lean-compatible types and interfaces, not
producing superficially valid Lean syntax.
The DeepSeek audit exposes a separate semantic bottleneck. Even after the compiler and extractor
filter malformed statements, the judge rejects 67.08% of the statements it sees and accepts 32.92%;
relative to all generated statements these correspond to 44.64% rejected and 21.91% accepted. Com-
pilation is therefore a weak proxy for faithfulness: semantic adjudication removes substantially more
compilable-but-misaligned statements than Lean removes malformed ones. Among falsely certified
statements in the no-Js ablation of §4.3, the dominant failure mode is a weakened or answer-baked
surrogate goal: three of five certificates prove such surrogates, one drops an essential part of the
problem and one mistranslates the underlying geometry; none succeeds through a contradictory
context.



E.2   P ROOF E RROR A NALYSIS

L EANSTRAL exposes proof errors at two different levels: 54.73% of its de-duplicated internal
Lean/LSP results contain an error diagnostic or tool failure, spanning tactic failures, API misuse,
protocol failures, syntax, typing, and resource limits (Table 7). By the time a trajectory reaches the
external verifier, however, failures are concentrated in unsolved proof obligations and SafeVerify
policy violations. This shift shows that Leanstral’s agentic inner loop absorbs many local elabora-
tion and implementation errors before they reach the outer correction loop.


Table 7: Proof-error distributions (%) across all 30 AIME 2026 problems. Leanstral internal is
normalized over error-bearing Lean/LSP results; the external columns are normalized over failed
outer rounds. One category is assigned per result or round, with policy violations taking priority;
“–” denotes no assigned error.

           Primary error category                 Leanstral int.   Leanstral ext.   Codex ext.
           Tactic failure or open goals                   42.70            63.78        30.28
           Forbidden token or policy                          –            26.77            –
           Unknown name or API misuse                     15.19                –        15.31
           Tool, protocol, or runtime failure             13.68                –         2.16
           Parser or syntax error                          8.18             0.79         0.67
           Type or coercion mismatch                       6.70                –        45.92
           Resource limit or timeout                       5.72             8.66         2.66
           Other Lean diagnostic                           5.23                –            –
           Typeclass or instance synthesis                 2.60                –         1.83
           Metavariables or invalid declaration               –                –         0.83
           Noncomputable definition                           –                –         0.33




Compared with L EANSTRAL, C ODEX exposes a different external failure profile: type and coercion
mismatches dominate, followed by tactic failures and API misuse, whereas L EANSTRAL’s external
failures are dominated by proof search and policy enforcement. Parser errors are negligible for both,
showing that syntactic Lean generation is not the main bottleneck. The important distinction is
therefore where debugging occurs: L EANSTRAL resolves a broader range of implementation errors
internally, while Codex returns more of them to the pipeline. External rounds are consequently
not interchangeable units of proof effort, and error attribution should account for both the prover
backend and the level at which the error is observed.


                                                    25
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




E.3      R EASONER E RROR A NALYSIS


Table 8: Root causes of the 14 mathematical errors attributed to K2-H ORIZON -7B by the error
judge while solving the AIME 2026 problems.

      Cause                                                                                            Percent (%)
      Input interpretation or transcription                                                                      28.6
      Unsupported logical or proof step                                                                          28.6
      Arithmetic, algebra, or cardinality                                                                        21.4
      Escalation after repeated Lean repair could not preserve the contract                                      14.3
      Invalid construction or counterexample                                                                      7.1


As Table 8 shows, the dominant failures arise less from routine calculation than from preserving
the problem statement and justifying key proof steps. Representative examples include changing
17017 to 107017, solving the problem for N = 1000 instead of N = 10000, reading 39 as 3
or as 39 , interpreting six iterates as seven (Appendix D), and relying on unsupported geometric
or combinatorial reductions. These cases show why compiler feedback alone is insufficient: error
attribution must sometimes return control to the reasoner to reconstruct the mathematics rather than
continue repairing its Lean implementation.

F      D ETAILS OF IMO 2026

F.1     E XPERIMENTAL S ETUP
For IMO 2026 we retain the same pipeline and add a final judge after formal verification to assess
whether the formal certificate covers the complete informal solution. The judge compares the orig-
inal problem and informal reasoning with the generated Lean statement and proof. If it detects a
substantive mismatch, or an argument that is present informally but absent from the formal certifi-
cate, it returns incomplete proof. We count a solution as complete only when it passes both
Lean/SafeVerify and this final formal–informal alignment check.

F.2     E VALUATION
We evaluate our IMO 2026 solutions under two complementary protocols. First, we use C ODEX
as an automated judge, supplying it with several publicly available reference solutions, including
those from the Art of Problem Solving forums and from Kimi K3, and asking it to score each
generated solution against the official marking scheme. Second, for a more robust assessment, we
ask a former IMO medallist with access to national IMO score predictions to mark the same solutions
independently.

F.3     V ERIFICATION -G UIDED T EST-T IME S CALING
Figure 6 shows that M AGENTA adaptively allocates
                                                                                              858K
more inference-time computation to more difficult          800K
problems. Problems 3 and 6 consume the largest to-
                                                                 Output tokens




                                                           600K
ken budgets and require more self-correction, consis-                                                              380K
                                                           400K
tent with their higher level of difficulty. Rather than                                234K
relying on a single fixed generation, M AGENTA uses        200K
                                                                                                     72K   82K
                                                                                 36K
formal-verification feedback to guide subsequent at-          0
                                                                P1   P2     P3        P4   P5 P6
tempts, allowing the reasoner to revise unsuccessful                      IMO 2026 problem

arguments and devote additional computation where it
is most needed. This reflects the principle of test-time Figure 6: Total reasoner-token usage of
scaling (Sahoo et al., 2024), with verification provid- K2-H ORIZON -7B with M AGENTA across
ing a targeted signal for how that additional computa- the six IMO 2026 problems.
tion should be used. Through this verification-guided
scaling process, K2-H ORIZON -7B ultimately solves all six problems on IMO 2026.


                                                        26
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4     G ENERATED S OLUTIONS

F.4.1    IMO P ROBLEM 1

 Question
 There are 2026 integers greater than 1 written on a blackboard, not necessarily distinct. In one
 move, Confucius chooses two integers m > 1 and n > 1, written in different positions, and
 replaces them by
                                                       lcm(m, n)
                              gcd(m, n)       and                 .
                                                       gcd(m, n)
 He continues making moves for as long as a move is possible.
        (a) Prove that, regardless of his choices, the process terminates after finitely many moves
            with exactly one integer M > 1 on the board.
        (b) Prove that the value of M is independent of all choices made during the process.

 K2-Horizon-7B generation
 Let the initial integers be a1 , a2 , . . . , a2026 with ai > 1 for all i. We regard the board as a
 function f : {1, 2, . . . , 2026} → N>1 . A move consists of choosing two distinct positions i, j
 with m = f (i) > 1 and n = f (j) > 1, and replacing them by
                                                       lcm(m, n)
                               g = gcd(m, n),          h=         .
                                                       gcd(m, n)
 All other positions stay unchanged. The process continues as long as such a move is possible.

 ( A ) T ERMINATION AND THE FINAL BOARD
 For any board b (a function from {1, . . . , 2026} to positive integers) define
                                                                      2026
                                                                      Y
                          N (b) = #{ i | b(i) > 1 },        P (b) =          b(i).
                                                                      i=1
 Because every b(i) is a positive integer, P (b) is a positive integer.
 Lemma 1. After a move b → c we have N (c) ≤ N (b), and if N (c) = N (b) then P (c) < P (b).
 Proof. Let the move act on positions i, j with m = b(i) > 1, n = b(j) > 1. Set g = gcd(m, n)
 and h = lcm(m, n)/g; then c(i) = g, c(j) = h and c(k) = b(k) for k ̸= i, j.
 For k ∈/ {i, j} the contribution to N and P is unchanged, so we only compare the two changed
 positions.
 Case 1: g = 1. Then h = lcm(m, n) = mn (since gcd(m, n) = 1). Because m, n > 1, we
 have h > 1. Thus we replace two numbers > 1 by one number > 1 (namely h) and one number
 1 (namely g). Hence N (c) = N (b) − 1. Moreover
                                       gh            1 · mn
                           P (c) = P (b) · = P (b) ·          = P (b).
                                      mn               mn
 Case 2: g > 1. Write m = g m′ , n = g n′ with gcd(m′ , n′ ) = 1. Then
                                   lcm(m, n)    g m ′ n′
                                h=            =          = m′ n′ .
                                       g           g
 Subcase 2a: h = 1. Then m′ = n′ = 1, so m = n = g. We replace two equal numbers > 1 by
 g > 1 and 1; therefore N (c) = N (b) − 1. Also
                                 g·1     P (b)
                       P (c) = P (b) ·=        < P (b) (since g > 1).
                                 g·g       g
 Subcase 2b: h > 1. Then we replace two numbers > 1 by two numbers > 1 (g > 1, h > 1);
 hence N (c) = N (b). Moreover


                                                  27
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                               gh            g (m′ n′ )   P (b)
            P (c) = P (b) ·        = P (b) ·            =        < P (b) (since g > 1).
                              mn              g m′ g n′     g
 In every situation N (c) ≤ N (b), and when N (c) = N (b) we are in subcase 2b, which gives
 P (c) < P (b).                                                                                  □
 The lexicographic order on N × N is well-founded (because N is well-ordered). Lemma 1 shows
 that the pair (N, P ) strictly decreases lexicographically at each move. Hence the process cannot
 continue indefinitely; it must terminate after finitely many moves.
 Let b be a terminal board, i.e. no move is possible. Then there are no two distinct positions with
 values > 1; consequently at most one position contains a number > 1. We claim that exactly
 one such position exists.
 Suppose, for contradiction, that all b(i) = 1. Then N (b) = 0. The initial board has N = 2026.
 Each move can decrease N by at most one (Lemma 1). To reach N = 0 from N = 2026 we
 would need at least 2026 moves that each reduce N by one. However, a move that reduces N
 from 1 to 0 is impossible because a move requires two numbers > 1. More precisely, if at some
 stage N = 1, no move can be performed, so the process would have stopped earlier. Thus the
 process can never reach a state with N = 0. Therefore the final board must have N = 1.
 Hence there is a unique index i with b(i) > 1, and for all j ̸= i we have b(j) = 1. Set M = b(i);
 then M > 1. This proves part (a).

 ( B ) I NDEPENDENCE OF THE FINAL VALUE M
 For a prime p and a positive integer x let vp (x) be the exponent of p in the prime factorisation
 of x (with vp (1) = 0). For a board b define

                              Gp (b) = gcd{ vp (b(i)) | i = 1, . . . , 2026 }.
 (If the set consists only of zeros we take the gcd to be 0.)
 Lemma 2. Gp (b) is invariant under moves.
 Proof. Consider a move on positions i, j with m = b(i), n = b(j). Put a = vp (m), b = vp (n).
 Then

                  vp (gcd(m, n)) = min(a, b),            vp (lcm(m, n)) = max(a, b).
 Since h = lcm(m, n)/ gcd(m, n),

         vp (h) = vp (lcm(m, n)) − vp (gcd(m, n)) = max(a, b) − min(a, b) = |a − b|.
 Thus the multiset of p-adic valuations changes from {a, b} to {min(a, b), |a − b|}. Let R be the
 multiset of valuations of the other 2024 positions. Then
                                                                   
                            gcd {a, b} ∪ R = gcd gcd(a, b), gcd(R) ,
                                                                                   
             gcd {min(a, b), |a − b|} ∪ R = gcd gcd(min(a, b), |a − b|), gcd(R) .
 Hence it suffices to prove

                                 gcd(min(a, b), |a − b|) = gcd(a, b).                             (*)
 Assume without loss of generality that a ≥ b. Then min(a, b) = b and |a − b| = a − b. If d
 divides both b and a − b, then d divides b + (a − b) = a; conversely, if d divides both b and
 a, then d divides a − b. Thus the sets of common divisors of {b, a − b} and {a, b} coincide, so
 their greatest common divisors are equal. Hence (∗) holds, and the gcd of the whole multiset is
 unchanged.                                                                                         □
 Now look at the terminal board: it contains one number M > 1 and the remaining 2025 numbers
 equal to 1. The multiset of valuations is {vp (M )} ∪ {0, 0, . . . , 0} (2025 zeros). The gcd of this
 set is vp (M ) because gcd(vp (M ), 0) = vp (M ). Therefore

                                          Gp (final) = vp (M ).
 By Lemma 2, Gp (final) = Gp (initial) for every prime p. Consequently

                              vp (M ) = Gp (initial)       for all primes p.



                                                    28
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 The prime factorisation of an integer is unique, so
                                              Y
                                      M=           p Gp (initial) .
                                                p prime

 Since the right-hand side depends only on the initial multiset, the value of M is independent of
 the choices made during the process.                                                          □

            The process terminates with exactly one integer M > 1 on the board, and
                            Y
                               p gp ,
                                                                               
                     M=                  gp = gcd vp (a1 ), . . . , vp (a2026 ) ,
                                p

                                    which is independent of the choices.




                                                     29
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4.2   IMO P ROBLEM 2




 Question
 Let ABC be a triangle, and let M and N be the midpoints of AB and AC, respectively. Let K
 and L be chosen strictly inside triangles BM C and BN C, respectively, such that K lies strictly
 inside ∠LBA, L lies strictly inside ∠ACK, and
              ∠KBA = ∠ACL,              ∠LBK = ∠LN C,                ∠LCK = ∠BM K.
 If O is the circumcentre of triangle AKL, prove that OM = ON .

 K2-Horizon-7B generation
 Place triangle ABC in the plane with A at the origin. Let B = (b1 , b2 ) and C = (c1 , c2 ). Since
 △ABC is non-degenerate, the vectors B and C are linearly independent. Define

                 D = det(B, C) = b1 c2 − b2 c1 ̸= 0,           r = |B|2 = b21 + b22 ,
                  s = B ·C = b1 c1 + b2 c2 ,                   t = |C|2 = c21 + c22 .
 For any points P, Q we write P − Q for the vector from Q to P , and for vectors u, v we denote
 by det(u, v) the determinant (cross product) and by u·v the dot product.

 1. C OORDINATES OF K AND L
 Because K lies inside △BM C there exist positive numbers α, β, γ with α + β + γ = 1 such
 that

                                      K = αB + βM + γC.
 The midpoint M of AB is M = 21 (A + B) = 21 B; hence
                                            β
                                      K = α+    B + γC.
                                             2
 Set
                                        β
                                      x=α+,    y = γ.
                                        2
 Then K = xB + yC. From α, β, γ > 0 and α + β + γ = 1 we obtain
                                                           β              β
              0 < x < 1,        0 < y < 1,       x+y =α+      + γ = 1 − < 1.
                                                           2              2
 Similarly, L lies inside △BN C. Its midpoint N is N = 12 C; thus there exist positive α′ , β ′ , γ ′
 with α′ + β ′ + γ ′ = 1 such that
                                                               β′        
                         L = α′ B + β ′ N + γ ′ C = α′ B +           + γ ′ C.
                                                                2
 Set
                                                        β′
                                     p = α′ ,     q=       + γ′.
                                                        2
 Then L = pB + qC and
                                                                        β′
                      0 < p < 1,       0 < q < 1,        p+q =1−           < 1.
                                                                        2



                                                 30
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 2. T HE CONDITIONS “K INSIDE ∠LBA” AND “L INSIDE ∠ACK”
 K inside ∠LBA means that the ray BK lies between BA and BL. With A = 0 this is equivalent
 to the existence of positive numbers u, v such that

                     K − B = u(L − B) + v(A − B) = u(L − B) − vB.                            (*)
 Write K − B = (x − 1)B + yC and L − B = (p − 1)B + qC. Substituting into (∗) gives
                                                             
          (x − 1)B + yC = u (p − 1)B + qC − vB = u(p − 1) − v B + uqC.
 Because B and C are independent, we equate coefficients:

                               y = uq,        x − 1 = u(p − 1) − v.                          (1)
 From the first equation u = y/q > 0. Then
                                           y                     y(p − 1) − q(x − 1)
            v = u(p − 1) − (x − 1) =         (p − 1) − (x − 1) =                     .
                                           q                              q
 Define

                                     d = q(1 − x) − y(1 − p).
 A short calculation shows y(p − 1) − q(x − 1) = d; hence v = d/q. Since v > 0 and q > 0,

                                                d > 0.                                       (2)
 Similarly, L inside ∠ACK means there exist positive u′ , v ′ such that

                   L − C = u′ (A − C) + v ′ (K − C) = −u′ C + v ′ (K − C).                 (**)
 Write L − C = pB + (q − 1)C and K − C = xB + (y − 1)C. Substituting into (∗∗) gives

        pB + (q − 1)C = v ′ xB + (y − 1)C − u′ C = (v ′ x)B + v ′ (y − 1) − u′ C.
                                                                           

 Equating coefficients:

                              p = v ′ x,      q − 1 = v ′ (y − 1) − u′ .                     (3)
                          ′
 From the first equation v = p/x > 0. Then
                                           p                     p(y − 1) − x(q − 1)
           u′ = v ′ (y − 1) − (q − 1) =      (y − 1) − (q − 1) =                     .
                                           x                              x
 Define

                                 e = x(1 − q) − p(1 − y).
 Again p(y − 1) − x(q − 1) = e; hence u′ = e/x. Since u′ > 0 and x > 0,

                                                e > 0.                                       (4)

 3. A LEMMA ON ANGLE EQUALITIES
 Lemma. Let u, v, u′ , v ′ be non-zero vectors in the plane. If the (undirected) angle between u
 and v equals the angle between u′ and v ′ and det(u, v) det(u′ , v ′ ) > 0, then

                              det(u, v) (u′ ·v ′ ) = det(u′ , v ′ ) (u·v).                   (*)
 Proof. Equality of the undirected angles gives equality of the cosines:
                                         u·v      u′ ·v ′
                                               = ′ ′ .
                                       |u||v|    |u ||v |
 The absolute values of the determinants satisfy




                                                  31
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                                 | det(u, v)|   | det(u′ , v ′ )|
                                              =                   .
                                    |u||v|         |u′ ||v ′ |
 Because the determinants have the same sign,
                                     det(u, v)   det(u′ , v ′ )
                                               =                .
                                       |u||v|     |u′ ||v ′ |
 Multiplying the two equalities yields ⋆.                                                 □

 4. T RANSLATING THE ANGLE EQUALITIES
 We apply the lemma to each given angle equality. First we compute the relevant determinants
 and dot products.
 ∠KBA = ∠ACL. Take u = K − B, v = A − B = −B, u′ = A − C = −C, v ′ = L − C.
 Then

                      det(K − B, −B) = yD,              det(−C, L − C) = pD.
 Since y > 0, p > 0 and D ̸= 0, the product is positive. The dot products are

            (K − B)·(−B) = (1 − x)r − ys,               (−C)·(L − C) = t(1 − q) − ps.
 Lemma ⋆ gives
                                                               
                             yD t(1 − q) − ps = pD (1 − x)r − ys .
 Cancelling D and simplifying we obtain

                                       rp(1 − x) = ty(1 − q).                            (I)
                                                          ′           ′
 ∠LBK = ∠LN C. Take u = L − B, v = K − B, u = L − N, v = C − N . Then
                                                                              p
                  det(L − B, K − B) = dD,              det(L − N, C − N ) =     D.
                                                                              2
 Since d > 0, p > 0 the product is positive. The dot products are
                      (L − B)·(K − B) = r(1 − p)(1 − x)
                                                                    
                                             − s (1 − p)y + q(1 − x) + tqy,
                                              sp + t(q − 12 )
                     (L − N )·(C − N ) =                      .
                                                    2
 Lemma ⋆ yields

                          sp + t(q − 12 )  p   h
                   dD ·                   = D · r(1 − p)(1 − x)
                                2          2                                i
                                                                      
                                               − s (1 − p)y + q(1 − x) + tqy .
 Cancelling D and multiplying by 2 we get
                                       h
                 d sp + t(q − 12 ) = p r(1 − p)(1 − x)
                                  

                                                                         i             (II)
                                             − s (1 − p)y + q(1 − x) + tqy .
 ∠LCK = ∠BM K. Take u = L − C, v = K − C, u′ = B − M, v ′ = K − M . Then
                                                                              y
                  det(L − C, K − C) = eD,              det(B − M, K − M ) =     D.
                                                                              2
 Since e > 0, y > 0 the product is positive. The dot products are




                                                  32
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                                                                          
                        (L − C)·(K − C) = rpx − s p(1 − y) + x(1 − q)
                                            + t(1 − q)(1 − y),
                                            r(x − 12 ) + sy
                    (B − M )·(K − M ) =                     .
                                                  2
 Lemma ⋆ gives

                        r(x − 12 ) + sy  y   h                            
                 eD ·                   = D · rpx − s p(1 − y) + x(1 − q)
                              2          2                 i
                                           + t(1 − q)(1 − y) .
 Cancelling D and multiplying by 2 we obtain
                                         h
                   e r(x − 12 ) + sy = y rpx − s p(1 − y) + x(1 − q)
                                                                    
                                                            i                             (III)
                                           + t(1 − q)(1 − y) .


 5. A CRUCIAL ALGEBRAIC IDENTITY
 Set
           E1 = rp(1 − x) − ty(1 − q) = 0                         (from (I)),
                                                              
           E2 = p r(1 − p)(1 − x) − s (1 − p)y + q(1 − x) + tqy
                − d sp + t(q − 21 ) = 0
                                   
                                                                  (from (II)),
                                                              
           E3 = y rpx − s p(1 − y) + x(1 − q) + t(1 − q)(1 − y)
                − e r(x − 21 ) + sy = 0
                                   
                                                                  (from (III)).
 Define

                          c1 = (x + y)(p + 2q − 1) − (p + q)(1 − x).
 Consider the linear combination

                    F = c1 E1 + 2(x + y)(1 − q)E2 − 2(p + q)(1 − x)E3 .
 Since E1 , E2 , E3 are zero, we have F = 0. Now we expand F . Substituting the expressions for
 d and e,

                   d = q(1 − x) − y(1 − p),        e = x(1 − q) − p(1 − y),
 and expanding, we obtain after collecting terms:
                                  h
             F = (1 − x)(1 − q) r 2(p + q)x2 − 2(x + y)p2 − (xq − yp)
                                                                      
                                                                
                                    + s 4(p + q)xy − 4(x + y)pq
                                                                             i
                                    + t 2(p + q)y 2 − 2(x + y)q 2 + (xq − yp) .
 Because 0 < x < 1 and 0 < q < 1, we have (1 − x)(1 − q) ̸= 0. Hence the bracket must vanish,
 which gives

                    2(p + q)(rx2 + 2sxy + ty 2 )
                                                                                          (IV)
                        − 2(x + y)(rp2 + 2spq + tq 2 ) = (xq − yp)(r − t).




                                              33
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 6. T HE CIRCUMCENTER O OF △AKL
 Since A is the origin, the condition OA = OK = OL is equivalent to

                                     |O|2 = |O − K|2 = |O − L|2 .
 Expanding the squares gives

                                2 O·K = |K|2 ,          2 O·L = |L|2 .
 Using K = xB + yC and L = pB + qC,

                                               rx2 + 2sxy + ty 2
                            x (O·B) + y (O·C) =                   ,                         (5)
                                                        2
                                               rp2 + 2spq + tq 2
                       p (O·B) + q (O·C) =                       .                          (6)
                                                        2
 Let u = O·B and v = O·C. Then (5) and (6) are a linear system for u, v.
 We must prove OM = ON . Because M = 21 B and N = 12 C,
                                                        r
                         OM 2 = |O − 12 B|2 = |O|2 − u + ,
                                                        4
                              2       1   2       2     t
                         ON = |O − 2 C| = |O| − v + .
                                                        4
 Thus OM = ON is equivalent to OM 2 = ON 2 , i.e.
                                                  t−r
                                            v−u=      .                                     (7)
                                                    4
 To obtain (7) from (5) and (6), eliminate u and v. Multiply (5) by p + q and (6) by x + y and
 subtract:
                              (p + q)(xu + yv) − (x + y)(pu + qv)
                                    1h
                                 = (p + q)(rx2 + 2sxy + ty 2 )
                                    2                           i
                                        − (x + y)(rp2 + 2spq + tq 2 ) .
 The left-hand side simplifies to

                                          (py − xq)(v − u).
 Hence
                                            1h
                    (py − xq)(v − u) =        (p + q)(rx2 + 2sxy + ty 2 )
                                            2                                 i             (8)
                                                 − (x + y)(rp2 + 2spq + tq 2 ) .
 Now use (IV). Dividing (IV) by 2 gives

                      (p + q)(rx2 + 2sxy + ty 2 )
                                                              (xq − yp)(r − t)
                         − (x + y)(rp2 + 2spq + tq 2 ) =                       .
                                                                     2
 Substituting this into (8) yields
                                                       (xq − yp)(r − t)
                              (py − xq)(v − u) =                        .
                                                              4
 Since py − xq = −(xq − yp), we have
                                                       (xq − yp)(r − t)
                             −(xq − yp)(v − u) =                        .
                                                              4



                                                  34
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 The triangle AKL is non-degenerate (its circumcenter O exists), therefore K and L are not
 collinear with A. In our coordinates this means

                                det(K, L) = (xq − yp)D ̸= 0,
 and because D ̸= 0 we have xq − yp ̸= 0. Cancelling this non-zero factor gives
                                     r−t                       t−r
                         −(v − u) =           =⇒ v − u =             ,
                                      4                          4
 which is exactly (7). Hence OM 2 = ON 2 , and since distances are non-negative, OM = ON .
                                                                                        □




                                              35
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4.3    IMO P ROBLEM 3

 Question
 Let n be a positive integer. Liu Bang and Xiang Yu have a stick of length 1. First Liu Bang marks
 at most n points on the stick, and then Xiang Yu marks at most n further points; all marked points
 are distinct. The stick is cut at every marked point. The players then alternately claim unclaimed
 pieces, with Liu Bang moving first, and each player seeks to maximize the total length of the
 pieces he claims. Determine the largest number c that Liu Bang can guarantee, regardless of
 Xiang Yu’s play.

 K2-Horizon-7B generation
 Let the stick be the interval [0, 1]. Liu marks at most n points, then Xiang marks at most n
 further points; all marked points are distinct. The stick is cut at every marked point, producing
 pieces. The players then alternately claim unclaimed pieces, Liu moving first, each maximizing
 total length.
 Lemma 1 (Optimal play). Let the pieces be sorted in non-increasing order y1 ≥ y2 ≥ · · · ≥
 ym > 0. Under optimal play Liu obtains the pieces at odd positions and Xiang the pieces at even
 positions. Consequently Liu’s total is 1+D
                                          2 where
                                             X        X
                                       D=        yi −      yi .
                                                         i odd          i even

 Liu wants to maximise D, Xiang to minimise it.
 Proof. We prove by induction on m that the player whose turn it is always takes the largest
 remaining piece. For m = 1 this is trivial. Assume the statement holds for m − 1 pieces. For m
 pieces, suppose it is the current player’s turn. If the player takes yj (j > 1), the remaining pieces
 are sorted descending with yj removed. By induction the opponent will obtain the odd-indexed
 pieces in that sorted list. Let Gj be the opponent’s total if the current player takes yj . For j = 1,
 G1 = y2 + y4 + · · ·. For j > 1, removing yj shifts the parity of indices for elements after j; the
 opponent takes yi for i < j with i odd, and for i > j with i even. Hence
                                              X            X
                                       Gj =        yi +        yi .
                                                         i<j               i>j
                                                         i odd            i even

 Then                                                 X               X           X
                                 Gj − G1 =                      yi +            yi −  yi .
                                                        i<j             i>j            i even
                                                        i odd          i even
         P               P                                                         P
 Write     i even yi =    i<j yi + (yj if j is even else 0) +                       i>j yi . Thus
                         i even                                                    i even
                             X              X                                                   X              X
             Gj − G1 =               yi −            yi − (yj if j is even else 0) =                    yi −            yi .
                             i<j             i<j                                                i<j             i≤j
                             i odd          i even                                              i odd          i even
                                                      P
 Now consider the cases. • If j = 2h is even, then i<2h,i odd yi = y1 + y3 + · · · + y2h−1 =
 Ph              P                                              Ph
         y2r−1 ,   i≤2h,i even yi = y2 + y4 + · · · + y2h =           y2r . Hence Gj − G1 =
 Pr=1 h                                                          Pr=1
         (y
      r=1 2r−1   − y2r ) ≥   0.   • If j = 2h + 1  is odd,  then   i<2h+1,i odd yi = y1 + y3 +
                   Ph              P                                           Ph
 · · · + y2h−1 = r=1 y2r−1 , i≤2h+1,i even yi = y2 + y4 + · · · + y2h = r=1 y2r . Hence
                 Ph
 Gj − G1 = r=1 (y2r−1 − y2r ) ≥ 0. In both cases Gj ≥ G1 , so taking y1 minimises the
 opponent’s total and maximises the current player’s total.                                   □
 Lemma 2 (Pairs-plus-one). Let S be a multiset of positive real numbers. Suppose S consists
 of some number of equal pairs (each pair consists of two equal numbers) plus possibly one extra
 element r > 0. (If r = 0 we may ignore it.) Then when S is sorted in non-increasing order, the
 alternating sum                            X         X
                                         D=     si −       si
                                                          odd i          even i




                                                                  36
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 equals r.
 Proof. Sort S descending. Group the elements by their values. Since all numbers except possibly
 r appear in pairs, every value block (except possibly the block containing r) has even size. The
 block containing r has odd size. The number of elements before this block is the sum of the
 sizes of the previous blocks, which are all even, so it is even. In the alternating sum, each block
 of even size contributes 0 (the alternating sum of an even number of equal terms cancels). The
 block containing r starts at an odd position (because the number of preceding elements is even),
 so its terms alternate signs starting with +. The sum of an odd number of equal terms with
 alternating signs starting with + is the value itself. Hence the contribution of this block is r. All
 other blocks contribute 0. Thus D = r. If r = 0 then D = 0.                                        □

 1. L OWER BOUND – L IU CAN GUARANTEE D ≥ δ
              1
 Set δ = n+1       . Liu marks the points (2k − 1)δ for k = 1, 2, . . . , n. The stick is divided into
         2      −1
 n + 1 intervals
                     Ik = (2k−1 − 1)δ, (2k − 1)δ ,
                                                  
                                                          k = 1, . . . , n + 1,
 with lengths lk = 2 k−1 δ. Their sum is δ(2n+1 − 1) = 1.
 Xiang marks at most n further points. The stick is cut at every marked point, producing pieces.
 Let m be the number of positive pieces. Since there are at most 2n marks, m ≤ 2n + 1.
 Sort the pieces in non-increasing order and pad with zeros to obtain a list of length 2n + 2 (if
 m < 2n + 1 add zeros; if m = 2n + 1 add one zero). Pair the list as (a1 , b1 ), . . . , (an+1 , bn+1 )
 with ai ≥ bi ≥ 0. Associate each piece with its parent interval Ik ; zero pieces are associated
 with a dummy vertex D.
 Construct a directed multigraph G: vertices are I1 , . . . , In+1 and D. For each pair (ai , bi ) draw
 a directed edge from the parent of ai to the parent of bi . Thus G has V = n + 2 vertices and
 E = n + 1 edges. Every Ik contains at least one piece, and D is incident to at least one zero
 piece (since exactly 2n + 2 − m ≥ 1 zeros were added), so every vertex has degree ≥ 1.
 Consider the undirected version of G. For any connected component C, we have EC ≥ VC − 1
 (a connected graph has at least VC −1 edges). Summing over all components, E ≥ V −c, where
 c is the number of components. Since E = V − 1, we get V − 1 ≥ V − c, hence c ≥ 1. If every
 component satisfied EC ≥ VC , then E ≥ V , contradicting E = V − 1. Therefore there exists at
 least one component T with ET = VT − 1. Because every vertex has degree ≥ 1, T contains at
 least two vertices. A connected multigraph with ET = VT − 1 has no cycles (any cycle requires
 at least VT edges), so T is a tree (acyclic, simple). Bipartition this tree T into U ∪ W . Both U
 and W are non-empty.
 Define P = {k : Ik ∈ U } and Q = {k : Ik ∈ W }. The tree has at least two vertices and only
 one can be the dummy D, so P ∪ Q is nonempty. For a directed edge e = (A, B) in T (where
 A is the parent of ai , B is the parent of bi ), define sgn(e) = +1 if A ∈ U, B ∈ W and −1 if
 A ∈ W, B ∈ U . Let de = ai − bi (so de ≥ 0). For a vertex v let L(v) be the total length of
 pieces from v (all pieces from v are incident to edges in T , because v belongs to T ).
 We claim                      X                  X             X
                                   sgn(e) de =        L(v) −        L(v).
                              e∈T               v∈U           v∈W
 Indeed, for an edge e = (A, B) the contribution is sgn(e)(ai − bi ). If A ∈ U, B ∈ W this is
 ai − bi ; if A ∈ W, B ∈ U it is bi − ai . In both cases the piece from the U -endpoint receives +1
 and the piece from the W -endpoint receives −1. Summing over all edges in T , each piece from
 v ∈ U is counted +1 and each from v ∈ W is counted −1. Hence the identity holds.
 Now L(Ik ) = lk = 2 k−1 δ for k = 1, . . . , n + 1 and L(D) = 0. The difference U L − W L
                                                                                   P         P
 is a sum of some lk with coefficients ±1. Since the lk are distinct powers of two times δ,
 any
 P suchk−1   sum isP a multiple of δ. Moreover, P and Q are disjoint and P ∪ Q is nonempty. If
    k∈P 2       = k∈Q 2k−1 , uniqueness of binary expansion gives P = Q; disjointness then
 gives P = Q = ∅, contradicting P ∪ Q nonempty. Therefore the signed sum is nonzero and its
 absolute value
              Pn+1is at least δ. P
 Now D = i=1 (ai − bi ) = e∈E de . Since de ≥ 0, we have
                               X       X                   X         X
                         D≥      de ≥       sgn(e) de =         L−      L ≥ δ.
                            e∈T        e∈T                  U        W




                                                  37
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 Thus Liu’s total is at least 1+δ
                               2 .

 2. U PPER BOUND – X IANG CAN FORCE D ≤ δ
 If Liu marks fewer than n points, he creates at most n intervals. Xiang bisects each interval
 (using at most n cuts); then all pieces come in equal pairs, so D = 0 ≤ δ.
 Assume
 P          Liu marks exactly n points, creating n + 1 intervals of lengths a0 , a1 , . . . , an > 0 with
     ai = 1.
 Consider all subsets of {0, 1, . . . , n}. There are 2 n+1 subset sums (counted with multiplicity),
 all in [0, 1], including 0 and 1. Sort them: s1 ≤ s2 ≤ · · · ≤ s2 n+1 . The 2 n+1 − 1 consecutive
                                                                              1
 gaps are non-negative and telescope to 1, so one gap is at most 2 n+1          −1 = δ. The two entries
 bounding this gap come from two distinct subsets (if the gap P      is zero the
                                                                              Psubsets are still distinct).
 Hence there exist distinct subsets X, Y ⊆ {0, . . . , n} with | X − Y | ≤ δ.
 Among
 P         all such pairs, choose one that minimises
           P                                            P     |X|
                                                               P + |Y |. Let A = X, B = Y with
     A ≥ B (swap if necessary) and set r = A − B; then 0 ≤ r ≤ δ.
 Claim 1. P  A ∩ B =P∅. Proof. If Z = A ∩ B ̸= ∅, let A′ = A \ Z, B ′ = B \ Z. Then A′ , B ′ are
 distinct, | A′ − B ′ | = r ≤ δ, and |A′ | + |B ′ | = |A| + |B| − 2|Z| < |A| + |B|, contradicting
 minimality.                                                                                               □
 Thus A, B are disjoint. Let p = |A|, q = |B|.        P
 Case 1: B = ∅. Then A is non-empty and P                A = r ≤ δ. Minimality forces |A| = 1. Indeed,
 if |A| ≥ 2, choose a singleton {i} ⊂ A. Then {i} = ai ≤ r ≤ δ and |{i}|+|∅| = 1 < |A|,
 contradicting minimality. Thus A = {k} for some k and r = ak ≤ δ. Xiang leaves Ik uncut and
 bisects all other n intervals (using n cuts). The pieces are one piece of length r and 2n pieces
 forming n equal pairs. By Lemma 2, D = r ≤ δ.
 Case 2: B ̸= ∅. Then q ≥ 1. We have A, B disjoint. Order the intervals in A byPtheir positions
 on the stick: lengths α1 , . . . , αp , cumulative
                                                P sums A0 = 0, A1 = α1 , . . . , Ap =           A. Similarly
 for B: β1 , . . . , βq , B0 = 0, . . . , Bq =     B.     P                        P                     P
 Claim 2. For all k with 1 ≤ k < p, Ak ≤                     B. Proof. Suppose       B < Ak <              A
 for
 P    some P k   <   p.   Let T be   the   set of indices of A corresponding   to {αk+1 , . . . , α p }. Then
  PT = PA − AkP< r ≤ δ and |T | = p − k < p + q (since q ≥ 1). The pair (T, ∅) is disjoint,
 | T − ∅| =           P T ≤ δ, and |T | + 0 = p − k < p + q, contradicting minimality.                     □
 Hence Ap−1 ≤             B ≤ Ap .
 Now we construct Xiang’s marks. The cumulative numbers Aj and Bj are coordinates in two
 separate abstract concatenations, not positions on the original stick. Order the actual selected        P
 A-intervals left-to-right and translate them end-to-end, preserving lengths, to virtual [0, A],
 where actual P  interval αj represents virtual [Aj−1 , Aj ]. Separately translate the actual B-intervals
 to virtual [0, B].                                                                             P
 Retain Claim 2 and the common sorted boundary union 0 = t0 < t1 < · · · < ts =                     B, where
                            S = {0} ∪ {A1 , . . . , Ap−1 } ∪ {B1 , . . . , Bq }.
                   P                                  P                    P
 (Recall Ap−1 ≤ B, so all Aj for j < p are ≤ B, and Bq =                      B.)
 For each B-boundary Bj (1 ≤ j ≤ q) strictly inside a virtual A-cell [Ak−1 , Ak ], mark the
 corresponding actual A-interval at distance Bj −Ak−1 from its actual left endpoint. For each A-
 boundary Aj (1 ≤ j ≤ p−1) strictly inside a virtual B-cell [Bk−1 , Bk ], mark the corresponding
 actual B-interval at distance Aj − Bk−1 from its actual left endpoint. Equal boundaries need
 no cuts. Thus overlay cuts ≤ p + q − 1, and all marks are legal and distinct.
 Because A and B are disjoint, the A-intervals and B-intervals are distinct intervals on the
                                                                                           P stick.
 The two abstract concatenations now have the same refinement boundary list up to             B, so
 their resulting physical pieces have paired equal lengths ti − ti−1 ; they need not be at the same
 physical locations. P                               P P
 Because Ap−1 ≤         B ≤ Ap , the virtual tail [ B, A] corresponds to one tail in the last
 actual A-interval, of length r; when r = 0 it is absent.
 Bisect all intervals not in A or B; there are n + 1 − p − q of them, using n + 1 − p − q cuts.
 Total cuts used is at most (p + q − 1) + (n + 1 − p − q) = n. Hence Xiang can use at most n
 cuts.
 The final pieces consist of: • equal pairs from the overlay construction, • equal pairs from the
 bisected intervals, • one extra piece of length r (if r > 0).
 By Lemma 2, the alternating sum D equals r (or 0 if r = 0). Since r ≤ δ, we have D ≤ δ.



                                                     38
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 3. C ONCLUSION
 Liu can guarantee at least 1+δ                           1+δ
                             2 and Xiang can force at most 2 . Therefore the largest number c
 Liu Bang can guarantee is
                                                  1
                                1+δ   1 + 2 n+1 −1    2n
                           c=       =              = n+1    .
                                 2         2        2    −1

                                             2n
                                          2n+1 − 1




                                             39
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4.4   IMO P ROBLEM 4

 Question
 Shan-Yu and Mulan are playing a game. Let θ be an angle satisfying
                                          0◦ < θ < 180◦ ,
 known to both players. Initially, Shan-Yu constructs a paper triangle T with measurements of
 his choice. They then repeatedly perform the following steps:
        1. If T has at least one angle measuring exactly θ, the game ends and Mulan wins.
        2. Otherwise, Mulan chooses a point P on the perimeter of T , distinct from its three
           vertices.
        3. She makes a straight cut from P to the opposite vertex of T , dividing T into two
           triangles.
        4. Shan-Yu discards one of the two triangles, and the remaining triangle becomes the new
           T.
 For which real values of θ can Mulan guarantee victory in finitely many steps, regardless of how
 Shan-Yu plays?

 K2-Horizon-7B generation
 Let θ be an angle with 0◦ < θ < 180◦ . A triangle is determined by its three positive angles
 A, B, C with A + B + C = 180◦ . A cut at vertex A (with angles A, B, C) means choosing
 a point P on side BC (different from B, C) and drawing segment AP . This splits the triangle
 into two triangles with angles

             (x, B, 180◦ − x − B)          and      (A − x, C, 180◦ − (A − x) − C)
 for some x with 0 < x < A. (The angles at B and C remain unchanged, and the new angles at
 A are x and A − x; the third angles are forced by the sum 180◦ .)
 We determine for which θ Mulan has a strategy that guarantees victory in finitely many steps,
 no matter how Shan-Yu plays.

 1. N ECESSITY: IF θ DOES NOT DIVIDE 180◦ , M ULAN CANNOT FORCE A WIN .
 Assume θ ∤ 180◦ ; then there is no integer k with 180◦ = kθ.
 Lemma 1. Let T be a triangle with angles A, B, C, none of which is an integer multiple of
 θ. For any cut of T , at most one of the two resulting triangles has an angle that is an integer
 multiple of θ.
 Proof. Suppose we cut at vertex A, splitting A into x and A − x (0 < x < A). The two triangles
 are

           T1 = (x, B, 180◦ − x − B),            T2 = (A − x, C, 180◦ − (A − x) − C).
 Assume, for contradiction, that both T1 and T2 contain an angle that is an integer multiple of θ.
 We examine the possibilities.
 • If T1 ’s multiple is B or T2 ’s multiple is C, then T itself has a multiple, contradicting the
 hypothesis. • If T1 ’s multiple is x and T2 ’s multiple is A − x, then A = x + (A − x) is a multiple
 of θ, contradiction. • If T1 ’s multiple is x and T2 ’s multiple is the third angle 180◦ −(A−x)−C,
 then
                  180◦ − (A − x) − C = B + x              (since A + B + C = 180◦ ).
 Hence B + x is a multiple of θ; because x is a multiple of θ, B is also a multiple of θ, contra-
 diction. • If T1 ’s multiple is the third angle 180◦ − x − B and T2 ’s multiple is A − x, then
              180◦ − x − B = (A − x) + C            (again using A + B + C = 180◦ ),
 so C is a multiple of θ, contradiction. • If both multiples are the third angles, then
           (180◦ − x − B) + (180◦ − (A − x) − C) = 360◦ − (A + B + C) = 180◦ ,


                                                  40
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 which gives (p + q)θ = 180◦ for some integers p, q; this contradicts θ ∤ 180◦ .
 All cases lead to a contradiction, so at most one of T1 , T2 can have a multiple of θ.            □
 Shan-Yu’s strategy. Choose an initial triangle with no angle a multiple of θ; for instance the
 equilateral triangle with angles 60◦ , 60◦ , 60◦ . (If 60◦ were a multiple of θ, then 180◦ = 3 · 60◦
 would be a multiple of θ, contradicting θ ∤ 180◦ .)
 Whenever Mulan makes a cut, Shan-Yu discards the triangle that contains a multiple of θ (if
 such a triangle exists); otherwise he discards arbitrarily. By Lemma 1 the remaining triangle has
 no multiple of θ. Hence the game never produces an angle equal to θ, and Mulan never wins.
 Thus Mulan cannot guarantee victory when θ ∤ 180◦ .

 2. S UFFICIENCY: IF θ DIVIDES 180◦ , M ULAN HAS A WINNING STRATEGY.
 Now assume 180◦ = mθ for some integer m ≥ 2 (because θ < 180◦ gives m > 1). We describe
 Mulan’s strategy.
 Strategy. Given the current triangle T with angles A, B, C.
 • If any angle equals θ, Mulan wins immediately. • Otherwise, we distinguish two cases.
 Case 1. T has an angle that is a positive integer multiple of θ, say A = qθ with q ≥ 2. Mulan
 cuts at vertex A, splitting it into θ and (q − 1)θ. The two resulting triangles are

                   T1 = (θ, B, A + C − θ),            T2 = ((q − 1)θ, C, B + θ).
 (One checks that A + C − θ = 180 − B − θ and B + θ = 180◦ − C − (q − 1)θ, so the angles
                                      ◦

 sum to 180◦ in each triangle.) T1 contains θ, so Shan-Yu will discard T1 . The remaining triangle
 is T2 . If q = 2, then T2 contains θ and Mulan wins. If q > 2, then T2 has an angle (q − 1)θ
 which is a positive integer multiple of θ; we are back to Case 1 with a smaller multiple. Hence
 after at most q − 1 moves Mulan wins.
 Case 2. T has no angle that is a positive integer multiple of θ. Mulan performs a special cut to
 create two triangles that both have a multiple of θ.
 Lemma 2. There exist a vertex i ∈ {0, 1, 2} and a positive integer p such that

                   T (i + 1) < pθ < T (i) + T (i + 1)        (indices modulo 3).
 Proof of Lemma 2. Suppose first that there is a vertex i with T (i) > θ. Let p be the smallest
 positive integer with pθ > T (i + 1) (such p exists because T (i + 1) < 180◦ = mθ). Then
 (p − 1)θ ≤ T (i + 1) < pθ. Since T (i) > θ,

                              pθ ≤ T (i + 1) + θ < T (i + 1) + T (i),
 so pθ < T (i) + T (i + 1). The inequality T (i + 1) < pθ holds by construction.
 If, on the other hand, every angle satisfies T (i) ≤ θ, then because no angle equals θ we have
 T (i) < θ for all i. Pick i = 0. Then T (1) < θ. Moreover,
          T (0) + T (1) = 180◦ − T (2) > 180◦ − θ = (m − 1)θ ≥ θ           (since m ≥ 2).
 Hence T (1) < θ < T (0) + T (1), and we may take p = 1.                                   □
 Now let i and p be as in Lemma 2. Set x = pθ − T (i + 1). Then 0 < x < T (i). Mulan cuts at
 vertex i, splitting the angle T (i) into x and T (i) − x. The two resulting triangles are

              L = (x, T (i + 1), (m − p)θ),           R = (T (i) − x, T (i + 2), pθ).
 (One verifies the third angles using A + B + C = 180◦ and 180◦ = mθ.)
 Both L and R have an angle that is a positive integer multiple of θ. Shan-Yu discards one of
 them. The remaining triangle has an angle that is a positive integer multiple of θ. If that multiple
 is θ, Mulan wins immediately. If it is larger, say qθ with q ≥ 2, Mulan proceeds to Case 1,
 which will finish in at most q − 1 moves. Because p ≤ m − 1 and the remaining multiple is
 either p or m − p, we have q ≤ m − 1. Thus after the initial cut Mulan wins in at most m − 1
 further moves, i.e. in at most m moves altogether.
 This completes the description of Mulan’s strategy.




                                                 41
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 3. C ONCLUSION
 Mulan can guarantee her victory in finitely many steps if and only if θ divides 180◦ , i.e.

                                    180◦
                               θ=           for some integer k ≥ 2 .
                                     k




                                                 42
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4.5   IMO P ROBLEM 5

 Question
                                                          p
 Determine all functions f : R>0 → R>0 such that
 p                                                            (x2 + f (y)2 )/2 ≥ (f (x) + y)/2 ≥
   xf (y) for every x, y ∈ R>0 .

 K2-Horizon-7B generation
 Let f : (0, ∞) → (0, ∞) satisfy
                   r
                      x2 + f (y)2       f (x) + y     p
                                    ≥              ≥     x f (y)     (∀x, y > 0).
                            2               2
 All quantities are positive, so squaring preserves the order. The left inequality becomes

                x2 + f (y)2     f (x) + y 2
                             ≥                ⇐⇒ 2x2 + 2f (y)2 ≥ (f (x) + y)2 ,
                     2               2
 and the right inequality becomes
                      f (x) + y 2
                                      ≥ x f (y) ⇐⇒ (f (x) + y)2 ≥ 4x f (y).
                            2
 Thus for all x, y > 0

                            2x2 + 2f (y)2 ≥ (f (x) + y)2 ≥ 4x f (y).                         (1)

 1. A FUNCTIONAL EQUATION
 Put x = f (y) in (1). Because f (y) > 0,

                          2f (y)2 + 2f (y)2 ≥ (f (f (y)) + y)2 ≥ 4f (y)2 ,
 hence (f (f (y)) + y)2 = 4f (y)2 . Since f (f (y)) + y > 0,

                                f (f (y)) + y = 2f (y)     (∀y > 0),
 or

                                       f (f (y)) = 2f (y) − y.                               (2)

 2. I NTRODUCING g
 Define g(y) = f (y) − y for y > 0; then f (y) = y + g(y). From (2),

             g(f (y)) = f (f (y)) − f (y) = (2f (y) − y) − f (y) = f (y) − y = g(y).         (3)

 3. I TERATION AND NON - NEGATIVITY OF g
 We prove by induction that for every y > 0 and every n ∈ N,

                         g(y + n g(y)) = g(y)      and      y + n g(y) > 0.                  (4)
 Base n = 0: g(y) = g(y) and y > 0. Inductive step: Assume (4) holds for some n. Then

              f (y + n g(y)) = (y + n g(y)) + g(y + n g(y)) = y + (n + 1)g(y).
 Because y + n g(y) > 0, the hypothesis f (z) > 0 for z > 0 gives f (y + n g(y)) > 0; hence
 y + (n + 1)g(y) > 0. Moreover,
                                                    
              g(y + (n + 1)g(y)) = g f (y + n g(y)) = g(y + n g(y)) = g(y),
 where we used (3) and the induction hypothesis. Thus (4) holds for n + 1.


                                                 43
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




                                                                                             y
 Now suppose g(y) < 0 for some y > 0. Then −g(y) > 0. Choose n ∈ N with n >                       .
                                                                                            −g(y)
 Then

                                   y + n g(y) = y − n(−g(y)) < 0,
 contradicting the second part of (4). Therefore

                                        g(y) ≥ 0          (∀y > 0).                             (5)
 Consequently f (y) = y + g(y) ≥ y for all y > 0.

 4. A KEY INEQUALITY
 For arbitrary x, y > 0 set ∆ = g(x) − g(y). Expanding the two parts of (1) gives

              2x2 + 2f (y)2 − (f (x) + y)2 = (x − f (y))2 − 2∆ (x + f (y)) − ∆2 ,

                    (f (x) + y)2 − 4x f (y) = (x − f (y))2 + 2∆ (x + f (y)) + ∆2 .
 Hence (1) yields

                             (x − f (y))2 − 2∆ (x + f (y)) − ∆2 ≥ 0,                            (6)
                                          2                           2
                             (x − f (y)) + 2∆ (x + f (y)) + ∆ ≥ 0.                              (7)
 Now observe that
                                              2
             4f (y)∆ + (x − f (y)) + ∆             = (x − f (y))2 + 2∆ (x + f (y)) + ∆2 .
 Thus (6) and (7) are exactly the two parts of
                                                              2
          0 ≤ 4f (y) g(x) − g(y) + (x − f (y)) + (g(x) − g(y)) ≤ 2(x − f (y))2 .
                                   
                                                                                                (8)
 So (8) holds for all x, y > 0.

 5. B OUNDING THE DIFFERENCE OF g
 Let u, v > 0. We prove

                              4 min(u, v) |g(u) − g(v)| ≤ (u − v)2 .                            (9)
 Assume first that g(v) ≤ g(u). Put x = f (u), y = v in (8). Using (3),
                                                   
                         0 ≤ 4f (v) g(f (u)) − g(v)
                                                                     2
                              + (f (u) − f (v)) + (g(f (u)) − g(v))
                                  ≤ 2(f (u) − f (v))2 .
 Since g(f (u)) = g(u) and f (v) = v + g(v), the right-hand inequality becomes
                             4(v + g(v))(g(u) − g(v))
                                                                   2
                                  + (f (u) − f (v)) + (g(u) − g(v))
                                  ≤ 2(f (u) − f (v))2 .
 Now f (u) = u + g(u), f (v) = v + g(v), so

                             f (u) − f (v) = (u − v) + (g(u) − g(v)).
 Let ∆ = g(u) − g(v) ≥ 0. Then

             f (u) − f (v) = (u − v) + ∆,            (f (u) − f (v)) + ∆ = (u − v) + 2∆.
 Substituting these into the inequality and expanding gives

        4v∆ + 4g(v)∆ + (u − v)2 + 4∆(u − v) + 4∆2 ≤ 2(u − v)2 + 4∆(u − v) + 2∆2 ,



                                                     44
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 which simplifies to

                                 4v∆ + 4g(v)∆ + 2∆2 ≤ (u − v)2 .
 Because g(v) ≥ 0 and ∆ ≥ 0, we have

                       4v∆ ≤ 4(v + g(v))∆ ≤ (u − v)2 − 2∆2 ≤ (u − v)2 .
 Thus

                                      4v (g(u) − g(v)) ≤ (u − v)2 .                       (10)
 If instead g(u) ≤ g(v), we interchange the roles of u and v (use x = f (v), y = u in (8)) and
 obtain

                                      4u (g(v) − g(u)) ≤ (u − v)2 .                       (11)
 In either case (9) follows.

 6. g IS CONSTANT
 Suppose there exist p, q > 0 with g(p) ̸= g(q). Without loss of generality, assume p < q. Put
 E = |g(q) − g(p)| > 0. Choose a natural number n such that

                                                   (q − p)2
                                              n>            .                             (12)
                                                     4pE
         q−p
 Set d =        > 0 and define zk = p + kd for k = 0, 1, . . . , n. Then zn = q, and for each k
           n
 we have zk > 0 and min(zk+1 , zk ) = zk ≥ p.
 Applying (9) to the pair (zk+1 , zk ) yields

                            4zk |g(zk+1 ) − g(zk )| ≤ (zk+1 − zk )2 = d2 .
 Since zk ≥ p,

                        4p |g(zk+1 ) − g(zk )| ≤ 4zk |g(zk+1 ) − g(zk )| ≤ d2 .
 Summing these inequalities for k = 0, 1, . . . , n − 1 gives
                                n−1
                                X                                   (q − p)2
                           4p         |g(zk+1 ) − g(zk )| ≤ nd2 =            .
                                                                       n
                                k=0
 By the triangle inequality,
                 n−1
                 X
                       |g(zk+1 ) − g(zk )| ≥ |g(zn ) − g(z0 )| = |g(q) − g(p)| = E.
                 k=0
 Consequently

                                                    (q − p)2
                                            4pE ≤            .
                                                       n
                    (q − p)2
 But (12) implies            < 4pE, a contradiction. Hence our assumption was false, and g(p) =
                       n
 g(q) for all p, q > 0. Therefore g is constant.




                                                    45
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 7. D ETERMINING f
 Let g(y) = c for all y > 0. Then f (y) = y + c. The condition f (y) > 0 for all y > 0 forces
 c ≥ 0. (If c < 0, then for y = −c/2 > 0 we would have f (y) = c/2 < 0, impossible.)
 Conversely, if c ≥ 0 and f (x) = x + c, then for any x, y > 0,
                         r
                            x2 + (y + c)2      x+y+c          p
                                           ≥               ≥    x(y + c).
                                  2                2
 Indeed, the right inequality is equivalent to (x + y + c)2 ≥ 4x(y + c), which simplifies to
 (x − y − c)2 ≥ 0; the left inequality is equivalent to 2(x2 + (y + c)2 ) ≥ (x + y + c)2 , which
 simplifies to (x − (y + c))2 ≥ 0. Both are true.

                         f (x) = x + c   for an arbitrary constant c ≥ 0




                                               46
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




F.4.6   IMO P ROBLEM 6

 Question
 Let a1 , a2 , a3 , . . . be an infinite sequence of positive integers greater than 1. Suppose that,
 for every positive integer n, the number an+1 is the smallest integer greater than an such that
 gcd(an+1 , ai ) > 1 for every 1 ≤ i ≤ n. Prove that there exist positive integers T and L such
 that an+T = an + L for every positive integer n.

 K2-Horizon-7B generation
 Let (an )n≥1 be the given sequence of integers > 1. Define a positive integer x > 1 to be good
 if gcd(x, ai ) > 1 for every i ≥ 1.
 Lemma 1. For all m, n ≥ 1, gcd(am , an ) > 1. Proof. If m = n then am > 1 so
 gcd(am , am ) = am > 1. If m < n, then by the definition of an (the smallest integer > an−1
 with gcd(an , ai ) > 1 for all i ≤ n − 1) we have m ≤ n − 1 and hence gcd(an , am ) > 1. If
 m > n the same argument with roles reversed gives gcd(am , an ) > 1.                             □
 Consequently every term an is good: for any i, if i < n then gcd(an , ai ) > 1 by the above; if
 i > n then gcd(ai , an ) > 1; and if i = n then an > 1.
 Lemma 2. The sequence is strictly increasing and an ≥ a1 + n − 1 for all n ≥ 1. Proof. The
 hypothesis gives an+1 > an . By induction, an ≥ a1 + n − 1.                                      □
 Lemma 3. The set of good numbers that are ≥ a1 is exactly {an : n ≥ 1}. Proof. By Lemma 1
 every an is good and an ≥ a1 . Conversely, let x be good with x ≥ a1 . If x = a1 we are done.
 If x > a1 , then by Lemma 2 the sequence is unbounded, so there exists a smallest N ≥ 2 such
 that aN ≥ x. Then aN −1 < x ≤ aN . If x = aN we are done. If x < aN , then by the definition
 of aN there exists i ≤ N − 1 with gcd(x, ai ) = 1, contradicting that x is good. Hence x = aN .
 □
 Lemma 4. Any two good numbers are not coprime. Proof. Let x, y be good. Set z = y a1 +1 .
 Because y > 1 and a1 ≥ 2, we have z > a1 . For any i, since y is good there is a prime p | y
 and p | ai ; then p | z. Thus gcd(z, ai ) ≥ p > 1 for all i, so z is good. By Lemma 3, z = aN
 for some N . Since x is good, gcd(x, aN ) > 1, hence gcd(x, z) > 1. If gcd(x, y) = 1, then
 gcd(x, y a1 +1 ) = 1, a contradiction. Therefore gcd(x, y) > 1.                                  □
 Lemma 5. Let B = a1a1 +1 + a1 + 2. For every good number x and every i ≥ 1 there exists a
 prime p < B such that p | x and p | ai . Proof. We first establish some auxiliary facts.
 Witness Lemma. If k > a1 is not good, then there exists an index j ≥ 1 with aj < k and
 gcd(k, aj ) = 1. Proof. Since an → ∞, choose N with aN > k. Let n be the largest integer
 with an < k (so an < k < an+1 or k = an+1 ). Because k is not good, k ̸= an+1 ; thus
 an < k < an+1 . By the definition of an+1 there is i ≤ n with gcd(k, ai ) = 1. Take j = i; then
 aj ≤ an < k and gcd(k, aj ) = 1.                                                                 □
 Core numbers. A positive integer d > 1 is called a core if d is good and for every good divisor
 f of d we have d ≤ f (i.e., d has no proper good divisor). Every good number x possesses a
 core divisor: let d be the smallest good divisor of x. Then d is good, d | x, and if f is a good
 divisor of d, then f is a good divisor of x, so by minimality d ≤ f . Hence d is core.
 Claim. For every core d, all prime factors of d are < B. Proof by strong induction on d. Base
 case: d is prime. Since d is good, gcd(d, a1 ) > 1; because d is prime, d | a1 , so d ≤ a1 < B.
 The only prime factor is d itself, which is < B. Inductive step: Assume d is composite and the
 claim holds for all core d′ < d. Let p be a prime divisor of d and write d = p e with e > 1.
 Because d is core, e is not good (otherwise e would be a smaller good divisor of d). Also e < d.
 We distinguish two cases.
 Case 1: e > a1 . Since e is not good and e > a1 , the Witness Lemma gives an index j with
 aj < e and gcd(e, aj ) = 1. Let c be the smallest good divisor of aj . Then c is good, c | aj ,
 c ≤ aj < e < d, and c is core. Moreover gcd(e, c) = 1 because c | aj and gcd(e, aj ) = 1.
 Now c and d are both good, so by Lemma 4, gcd(c, d) > 1. Choose a prime q | gcd(c, d). Then
 q | d = p e, so q | p or q | e. Since gcd(e, c) = 1, q ∤ e; hence q | p. As p is prime, q = p. Thus
 p | c. Now c is a core number with c < d. By the induction hypothesis, all prime factors of c are
 < B; in particular p < B.
 Case 2: e ≤ a1 . Consider k = e a1 +1 . Because e > 1 and a1 ≥ 2, we have k > a1 and
 k ≤ a1a1 +1 < B. Also e | k. We claim k is not good. Indeed, if k were good then for every i,


                                                 47
M AGENTA: Closing the Loop Between Mathematical Reasoning and Formal Verification




 gcd(k, ai ) > 1; every prime divisor of k divides e, so gcd(e, ai ) > 1 for all i, making e good –
 a contradiction. Hence k is not good and k > a1 . By the Witness Lemma there exists an index
 j with aj < k and gcd(k, aj ) = 1. (Note that k is not a term, so the lemma applies.) Let c be
 the smallest good divisor of aj . Then c is good, c | aj , c ≤ aj < k, and c is core. Moreover
 gcd(e, c) = 1 because e | k and gcd(k, aj ) = 1. Again, c and d are good, so gcd(c, d) > 1. Let
 q be a prime dividing gcd(c, d). Then q | p e, and since gcd(e, c) = 1, q | p; thus q = p. Hence
 p | c. Now c < k ≤ a1a1 +1 < B. Consequently p ≤ c < B.
 In both cases we obtain p < B. This completes the induction.                                     □
 Now return to the original statement. Let x be good and i ≥ 1. Take d to be the smallest good
 divisor of x; then d is core. By the Claim, every prime factor of d is < B. Since d is good,
 gcd(d, ai ) > 1; pick a prime p | gcd(d, ai ). Then p | d | x and p | ai and p < B.              □
 Lemma 6. Let L = B! (the factorial of B). For every x > 1 we have good(x) ⇐⇒ good(x +
 L). Proof. If good(x), then for any i Lemma 5 gives a prime p < B with p | x and p | ai .
 Because p < B, p | L, so p | x + L. Hence gcd(x + L, ai ) ≥ p > 1 and x + L > 1; thus
 good(x + L). Conversely, suppose good(x + L). Then for any i, Lemma 5 applied to x + L
 gives a prime p < B with p | x + L and p | ai . Since p | L, we have p | (x + L) − L = x. Thus
 p | x and p | ai . Also x > 1: if x ≤ 1 then x = 1 (since x is a positive integer), but then p | 1,
 impossible. Therefore gcd(x, ai ) > 1 for all i, so good(x).                                     □
 Construction of T and L. Since a1 is good, Lemma 6 yields good(a1 + L). By Lemma 3,
 a1 + L ≥ a1 is a term of the sequence; let N be the index with aN = a1 + L. Because L > 0
 and the sequence is strictly increasing, N > 1. Define
                                    T = N − 1,         L = B!.
 Then T > 0 and a1+T = a1 + L.
 Lemma 7. For every n ≥ 1 we have an+T = an + L. Proof by induction on n. Base case
 n = 1: a1+T = a1 + L by construction. Inductive step. Assume an+T = an + L. Because the
 sequence is strictly increasing, an+1 is good, so by Lemma 6, an+1 + L is good. Moreover
                                  an+T = an + L < an+1 + L.
 Since an+T +1 is the smallest good number larger than an+T , we obtain
                                      an+T +1 ≤ an+1 + L.
 Suppose for contradiction that an+T +1 < an+1 + L. Set x = an+T +1 − L. Then
                                         an < x < an+1 .
 By the definition of an+1 (or the contrapositive of its minimality) there exists i ≤ n with
 gcd(x, ai ) = 1. On the other hand, an+T +1 is a term, hence good. Lemma 6 gives good(x)
 because good(x + L) holds. Therefore gcd(x, ai ) > 1 for all i, contradicting gcd(x, ai ) = 1.
 Hence an+T +1 = an+1 + L, which is exactly a(n+1)+T = an+1 + L.                             □
 Conclusion. We have exhibited positive integers T and L (depending only on a1 ) such that
 an+T = an + L for every n ≥ 1.

                          There exist positive integers T and L such that
                                 an+T = an + L for all n ≥ 1.




                                                 48
