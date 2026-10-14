                                                 ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis


                                            Mantas Bakšys 1 2 Stefan Zetzsche 2 Olivier Bouissou 3 Remi Delmas 3 Soonho Kong 4 Sean B. Holden 1


                                                                 Abstract
                                             Large language models have become proficient
                                             at generating functional code, but ensuring the
                                             output truly matches the programmer’s intent
arXiv:2512.10173v2 [cs.SE] 2 Feb 2026




                                             remains difficult. Testing improves trust, yet
                                             for safety-critical applications, formal verifica-
                                             tion provides the only true guarantees through
                                             machine-checked proofs. However, verified code
                                             remains scarce compared to mainstream lan-
                                             guages or mathematical theorem proving, limit-
                                             ing LLM capabilities in this domain. We present
                                             ATLAS, an automated pipeline that synthesizes
                                             verified programs to address this data bottleneck.
                                             Applied to the TACO dataset of Python solu-
                                             tions to LeetCode-style problems, ATLAS gen-
                                             erates 2.7K verified Dafny programs, each with
                                             high-quality specifications and machine-checked
                                             proofs. Through task decomposition, we extract
                                             19K training examples. Fine-tuning Qwen 2.5 7B
                                             Coder on this data improves performance from
                                             32.4% to 56.9% on DafnyBench and from 15.8%
                                             to 65.8% on DafnySynthesis, demonstrating that
                                             synthetic data generation is a viable path to scal-                       Figure 1. An overview of the ATLAS pipeline.
                                             ing LLM capabilities for formal verification.
                                                                                                               even high-quality generated code comes without guaran-
                                                                                                               tees—there is no systematic way to ensure the output truly
                                        1. Introduction                                                        matches the user’s intent. Unit tests and property-based
                                                                                                               testing can improve trust, and for most applications this is
                                        Large language models (LLMs) have transformed software                 sufficient.
                                        engineering, demonstrating impressive capabilities in code
                                                                                                               In safety-critical domains such as cryptographic libraries,
                                        generation, completion, and debugging. On mainstream
                                                                                                               medical devices, or aerospace systems, however, "probably
                                        languages like Python, JavaScript, and Java (Chen et al.,
                                                                                                               correct" is not enough. Formal verification addresses this
                                        2021; Cassano et al., 2023; Kocetkov et al., 2022), mod-
                                                                                                               gap: by requiring precise specifications of intended behavior
                                        els routinely produce functional, semantically meaningful
                                                                                                               and mathematically proving implementations satisfy them,
                                        code that solves the task at hand. Yet in typical workflows,
                                                                                                               verified software eliminates entire classes of bugs by con-
                                            Mantas Bakšys worked on this project during an internship at       struction. Producing verified code today, however, demands
                                        Amazon Web Services in London, UK.                                     substantial expertise—developers must craft not only the
                                        ATLAS - Automated Toolkit for LArge-Scale Verified Code                implementation but also specifications and the annotations
                                        Synthesis 1 University of Cambridge, Cambridge, UK 2 Amazon
                                        Web Services, London, UK 3 Amazon Web Services, Boston, USA            that guide automated reasoning toward a proof.
                                        4
                                          Amazon Web Services Santa Clara, CA, US. Correspondence              Formal verification tools span a spectrum. Interactive theo-
                                        to: Mantas Bakšys <mb2412@cam.ac.uk>, Stefan Zetzsche <ste-
                                        fanze@amazon.co.uk>.                                                   rem provers (ITPs) like Lean and Isabelle require users to
                                                                                                               construct proofs step-by-step and have seen the most suc-
                                        Preprint. February 3, 2026.                                            cess in mathematical domains. AI-assisted theorem proving

                                                                                                           1
                             ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

in ITPs has advanced rapidly—multiple systems recently
achieved gold medal performance on IMO 2025 with formal
proofs (Chen et al., 2025; Achim et al., 2025). For software
verification, auto-active tools like Dafny (Leino, 2010), F∗
(F* Development Team, 2025), Viper (Müller et al., 2016),
and Verus (Lattuada et al., 2023) offer a different tradeoff:
users annotate code with specifications and proof hints, and
an SMT solver automatically discharges the verification con-
ditions. This automation handles routine reasoning, letting
human effort focus on the hard parts. We focus on Dafny              Figure 2. Evaluation of our fine-tuned Qwen 2.5 7B Coder on
                                                                     DafnyBench and DafnySynthesis, compared with results reported
and provide further background in Section 2.                         in (Loughridge et al., 2024) and (Misu et al., 2024b) at the time of
Can similar AI-driven progress be achieved for auto-active           their release.
verification as has been seen in ITPs? A key obstacle is data
scarcity. While code in mainstream languages is abundant,            method Max(a: int, b: int) returns (m: int)
verified code remains rare—Dafny repositories on GitHub                requires true
are orders of magnitude fewer, and many contain incom-                 ensures m >= a && m >= b
plete proofs. The Lean community addressed analogous                   ensures m == a || m == b
                                                                     {
challenges through synthetic data: autoformalized theorem              if a >= b { m := a; } else { m := b; }
statements have successfully trained models for theorem              }
proving (Polu et al., 2022; Ying et al., 2025). Inspired
by these successes, we tackle the data scarcity problem
for Dafny—though our challenge differs: rather than auto-                 Figure 3. A simple Dafny method with specifications.
formalizing mathematical statements, we must synthesize
entire verified programs comprising implementations, speci-
                                                                     on DafnySynthesis (Misu et al., 2024b), which evaluates
fications, and proof annotations.
                                                                     generating verified programs from scratch (Figure 2).
To this end, we introduce ATLAS, a pipeline for automati-
                                                                     To sum up, our contributions are the following:
cally generating verified programs at scale (Figure 1). Given
a natural language problem description, a reference imple-
mentation in a mainstream language (e.g., Python), and test             • We present ATLAS, an automated pipeline for synthe-
cases, ATLAS synthesizes a corresponding program in a                     sizing verified programs from algorithmic problems
verification-aware language, complete with formal specifi-                with reference implementations and test cases.
cations and proof annotations. The pipeline works through
                                                                        • We define soundness and completeness criteria that
iterative refinement, alternating between verifier feedback
                                                                          leverage test cases to ensure specification quality, fil-
and LLM-driven repair. To ensure specification quality, we
                                                                          tering degenerate solutions.
verify that specifications are consistent with test cases and,
ideally, strong enough to uniquely determine the expected               • We demonstrate a data decomposition strategy that
output for each test input. While the pipeline could be                   extracts multiple training tasks per verified program,
adapted to other input datasets and target languages (e.g.,               achieving 7× data expansion.
Verus, F∗ ) with modest effort, we instantiate it on the TACO-
verified dataset (Li et al., 2023)—LeetCode-style problems              • We show empirically that fine-tuning on our synthe-
with Python solutions and unit tests—targeting Dafny.                     sized data yields substantial improvements on Dafny-
                                                                          Bench and DafnySynthesis.
This yields 2.7K verified Dafny programs, each with high-
quality specifications and machine-checked proofs of cor-
rectness. By decomposing each into specialized training              2. The Dafny Language
tasks—such as synthesizing code and specifications from              Dafny is a verification-aware programming language based
natural language, inferring implementations from specifi-            on Floyd-Hoare logic (Hoare, 1969). Programs are an-
cations, and repairing specifications, implementations, and          notated with specifications in the form of Hoare triples
proofs—we achieve 7× data expansion for ≈19K training                {P } s {Q}, where P is a precondition (requires), Q
examples (Table 1). Fine-tuning Qwen 2.5 7B Coder on this            is a postcondition (ensures), and s is the program body.
data improves performance from 32.4% to 56.9% on Dafny-              Figure 3 shows a simple example.
Bench (Loughridge et al., 2024), which evaluates proof an-
notation of existing Dafny code, and from 15.8% to 65.8%             The verification mechanism relies on weakest precondition
                                                                     calculus. Dafny translates code and specifications into an

                                                                 2
                              ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

intermediate representation (Boogie (Barnett et al., 2005)),          To address these requirements, we designed ATLAS, a multi-
which computes the weakest precondition wp(s, Q)—the                  phase pipeline that decouples problem statement generation
necessary and sufficient condition for s to terminate in a            from verified solution synthesis. The complete process is
state satisfying Q. The system then generates a verifica-             shown in Figure 1.
tion condition of the form P =⇒ wp(s, Q), which is
dispatched to the Z3 SMT solver (De Moura & Bjørner,                  3.1. Overview
2008). If Z3 determines the condition is valid, the program
is verified.                                                          We seed the synthesis pipeline with a dataset of program-
                                                                      ming contest problems paired with solutions in a general-
When Z3 cannot verify a program automatically, users pro-             purpose language. This ensures each program has a self-
vide ghost code—annotations that guide the solver without             contained implementation and reference solution with input-
affecting runtime behavior. Common forms include asser-               output test cases. We use TACO-verified (Li et al., 2023),
tions (assert P) that establish intermediate facts, loop in-          which contains 12.8K programming contest problems with
variants that characterize state at each iteration, lemmas that       Python reference solutions. We selected TACO-verified
encapsulate reusable proof steps, and calculational proofs            for its breadth—covering problems from LeetCode, Code-
(calc) that break complex equalities into transitive steps.           Forces, HackerRank, and others—its unified and rich meta-
Unlike interactive theorem provers where users construct              data, and its permissive licensing. Other datasets that could
explicit proof terms step-by-step, Dafny’s SMT solver han-            potentially be used for this task include APPS (Hendrycks
dles low-level reasoning automatically while users focus on           et al., 2021) and CodeContests (Li et al., 2022), which offer
high-level proof structure.                                           similar problem-solution pairs. However, they may lack the
Dafny has enabled large-scale verification efforts across in-         same high-quality metadata and strict test-case quality that
dustry and academia, including AWS’s Cedar authorization              TACO-verified provides.
engine (Hicks, 2023b), the AWS Cryptographic Material
Providers Library (Hicks, 2023a), VMware’s VeriBetrFS                 3.1.1. C ONTRACT G ENERATION
file system (Hance et al., 2020), Microsoft’s IronFleet dis-          The first stage generates a sound and complete formal con-
tributed systems (Hawblitzel et al., 2017), and ConsenSys’s           tract—consisting of a method signature, strong pre- and
Ethereum Virtual Machine specification (ConsenSys, 2023).             postconditions, and executable test cases—that serves as the
Notably, AWS rewrote and verified its policy authorization            immutable problem statement for implementation.
engine in Dafny, which is invoked 1 billion times per second
(Chakarov et al., 2025).                                              Method Signatures. We extract a reference solution from
                                                                      the dataset and prompt an LLM to generate the correspond-
3. ATLAS                                                              ing Dafny method signature. We use a generative approach
                                                                      to accommodate type system differences between Python
Synthesizing formally verified code poses challenges be-              and Dafny, a design choice validated by high task adherence
yond standard code generation. A robust pipeline must                 rates.
produce both an implementation and the correctness speci-
fication it satisfies. Drawing from formal theorem proving            Specifications and Tests. Given the method signature,
principles, we identify three key requirements:                       we synthesize specifications as requires and ensures
                                                                      clauses, which may reference auxiliary functions or pred-
   • Strong Specifications. The pipeline must generate                icates. In parallel, we generate test cases from the input-
     strong, semantically meaningful specifications that              output examples in TACO-verified, supplemented with ad-
     fully capture the program’s intended logic—not merely            ditional test cases generated by the agent to ensure broad
     safety properties like non-null outputs or range con-            coverage.
     straints.
   • Test Cases. The pipeline must generate executable test           Iterative Refinement. The Dafny compiler verifies gen-
     cases within the formal language to ground specifica-            erated specifications and tests for syntax errors. On failure,
     tions in concrete examples.                                      compiler errors are formatted and passed to an LLM judge,
                                                                      which provides corrective feedback for the next generation
   • Problem Freezing. Once defined, the problem state-               attempt. This iterative refinement loop continues until syn-
     ment must remain fixed to prevent the model from                 tactically valid specifications and test cases are produced or
     weakening specifications or trivializing test cases. This        the error-correction budget is exhausted. Beyond syntactic
     mirrors mathematical theorem proving, where a proof              correctness, we apply soundness and completeness checks
     attempt cannot alter the theorem statement once final-           that significantly improve compatibility between test cases
     ized.                                                            and specifications (detailed in Section 3.2).

                                                                  3
                            ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis


predicate isStringPalindrome(s: string)
                                                                   lemmas that provably satisfy the contract.
  ensures isStringPalindrome(s) <==> forall
     i :: 0 <= i < |s| / 2 ==> s[i] == s[|s                        Code and Proofs. We prompt an LLM with the specifi-
    | - 1 - i]                                                     cation and test cases to generate an implementation. We
  ensures |s| <= 1 ==> isStringPalindrome(s
    )
                                                                   observe that in practice, frontier models struggle to output
{                                                                  only implementations and assertions when specifications
  forall i :: 0 <= i < |s| / 2 ==> s[i] ==                         contain multiple functions or predicates. We therefore allow
    s[|s| - 1 - i]                                                 the model to regenerate specifications during implemen-
}                                                                  tation, provided they satisfy strict adherence constraints
function reverseString(s: string): string
                                                                   defined in the next validation step.
  ensures |reverseString(s)| == |s|
  ensures forall i :: 0 <= i < |s| ==>                             Validation. We enforce three checks to ensure correctness.
    reverseString(s)[i] == s[|s| - 1 - i]                          First, we verify contract adherence: each predicate,
  ensures isStringPalindrome(s) <==> s ==
    reverseString(s)
                                                                   function, and method must have exactly the original
{                                                                  requires clauses and a superset of the original ensures
  if |s| == 0 then "" else reverseString(s                         clauses. Second, we verify that the complete Dafny pro-
    [1..]) + [s[0]]                                                gram satisfies the specification. Third, we compile the pro-
}                                                                  gram and confirm that it passes all test cases in the Test()
method IsPalindrome(s: string) returns (
                                                                   method.
    isPalindrome: bool)                                            An example of a program that successfully passed both
  ensures isPalindrome ==
    isStringPalindrome(s)
                                                                   phases is shown in Figure 4.
  ensures |s| <= 1 ==> isPalindrome
{                                                                  3.2. Soundness and Completeness
  isPalindrome := true;
  var i := 0;                                                      During specification generation, we observe that synthe-
  while i < |s| / 2                                                sized specifications commonly exhibit insufficient strength,
    invariant 0 <= i <= |s| / 2                                    particularly in postconditions. This weakness is exacerbated
    invariant isPalindrome == forall j :: 0
     <= j < i ==> s[j] == s[|s| - 1 - j]
                                                                   by iterative error corrections, which progressively weaken
  {                                                                postconditions rather than strengthen them. To address this,
    if s[i] != s[|s| - 1 - i] {                                    we develop a framework that systematically relates specifi-
      isPalindrome := false;                                       cations and test cases through verification lemmas.
      return;
    }                                                              We construct three types of verification lemmas from test
    i := i + 1;                                                    case input-output pairs:
  }
}
                                                                   Soundness Lemmas These lemmas evaluate whether the
method Test() {                                                    contract is consistent with test cases by checking if it holds
  // Test case 1 [TACO]                                            pointwise for concrete instantiations. The intuition is that if
  var result1 := IsPalindrome("aba");                              a specification correctly captures the intended behavior, the
  expect result1 == true;
  ...                                                              contract should be satisfied when instantiated with known
  // Test case 8 [GENERATED]                                       correct examples. For each test case, we construct a lemma
  var result8 := IsPalindrome("                                    that asserts the concrete input and output values, then ver-
    fnjzxnxnjplfwzowfdrk");                                        ifies whether the contract holds (Figure 5). If this lemma
  expect result8 == false;                                         verifies successfully, it confirms that the contract is consis-
}
                                                                   tent with the test case. Conversely, if a soundness lemma
                                                                   fails, it reveals an inconsistency—the contract cannot be sat-
Figure 4. A verified Dafny program synthesized by ATLAS, in-       isfied by this known correct example, indicating it is either
cluding specification, implementation, and test cases.             too restrictive or incorrectly specified.

                                                                   Completeness Lemmas (Contradiction) These lemmas
                                                                   evaluate whether the postconditions uniquely determine out-
3.1.2. I MPLEMENTATION G ENERATION
                                                                   puts for given inputs by attempting to derive a contradiction
Once a valid formal contract is generated and frozen, the          from alternative outputs. The intuition is that if a specifi-
second stage synthesizes implementations, assertions, and          cation is sufficiently complete, assuming a different output

                                                               4
                             ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

                                                                     Difficulty        Total    Success    Success   Avg. Success   Avg. Fail
lemma Soundness(s: string, isPalindrome:                                             Samples   Samples    Rate (%)        Length     Length
     bool)                                                           EASY               5456      2572       47.14          3848        6531
   requires s == "aba" // Test input                                 MEDIUM             1353       338       24.98          4902        6879
   requires isPalindrome == true // Test                             MEDIUM HARD        1801       451       25.04          5226        6929
     output                                                          HARD               1256       260       20.70          5692        7270
                                                                     VERY HARD           537       107       19.93          5637        7102
   ensures isPalindrome ==
     isStringPalindrome(s)                                           UNKNOWN            2000       689       34.45          4559        6929
   ensures |s| <= 1 ==> isPalindrome
                                                                    Figure 6. ATLAS pipeline success rate by TACO-verified difficulty
{}
                                                                    ratings.
lemma CompletenessContr(s: string,
     isPalindrome: bool)
   requires s == "aba" // Test input
   requires isPalindrome != true // Test
     output negated
   requires isPalindrome ==
     isStringPalindrome(s)
   requires |s| <= 1 ==> isPalindrome
   ensures false
{}

lemma CompletenessPerturb(s: string,
     isPalindrome: bool)
   requires s == "aba" // Test input                                Figure 7. ATLAS pipeline success rate by TACO-verified difficulty
   requires isPalindrome == false // Test                           skill types.
     output perturbed
   ensures isPalindrome ==
     isStringPalindrome(s)
   ensures |s| <= 1 ==> isPalindrome                                be rejected. Conversely, if the perturbed output fails ver-
{}                                                                  ification, it suggests the postconditions are appropriately
                                                                    restrictive. This approach trades formal completeness guar-
                                                                    antees for practical automated verification.
Figure 5. Soundness and completeness lemmas constructed from
the first test case in Figure 4.                                    We leverage Dafny’s auto-active verification to obtain prover
                                                                    feedback on these lemmas without explicit proof construc-
                                                                    tion. The verification results inform the LLM judge follow-
while maintaining the contract should lead to an inconsis-          ing specification generation, enabling accurate evaluation
tency. For each test case, we construct a lemma that assumes        of specification strength and consistency. Failed soundness
the preconditions, postconditions, and negation of the ex-          lemmas indicate inconsistent or overly restrictive contracts,
pected output, then attempts to derive false (Figure 5). If         while successful perturbation lemmas reveal incomplete
this lemma proves successfully, it confirms no other output         specifications. While this approach is limited by the base
can satisfy the postconditions for the given input. However,        prover’s capabilities, it significantly improves specification
such proofs often exceed automated theorem provers capa-            quality by detecting weaknesses that would otherwise pass
bilities without guidance, motivating our perturbation-based        syntactic validation alone.
alternative described in the next paragraph.
                                                                    3.3. Analysis
Completeness Lemmas (Perturbation) These lemmas
                                                                    Applied to TACO-verified, ATLAS successfully generates
provide a practical alternative for evaluating specification
                                                                    2,751 verified Dafny programs, each with specifications and
completeness by directly testing whether the postconditions
                                                                    machine-checked proofs. We analyze pipeline performance
accept incorrect outputs. While the contradiction approach
                                                                    across difficulty levels and problem types.
attempts to prove that alternative outputs are impossible—a
task often too complex for automated provers—the pertur-
                                                                    3.3.1. D IFFICULTY R ATINGS
bation approach simply checks whether modified outputs
satisfy the contract. For each test case, we systematically         To evaluate the robustness of our ATLAS pipeline, we an-
perturb the output by structurally prompting an LLM while           alyzed its performance against the difficulty ratings pro-
maintaining fixed inputs, then verify whether the contract          vided by the TACO-verified dataset. The dataset classifies
still holds (Figure 5). If a lemma verifies successfully with       problems into five tiers—EASY, MEDIUM, MEDIUM HARD,
a perturbed output, it reveals that the postconditions have         HARD, and VERY HARD—enabling us to measure success
insufficient constraints—they accept behavior that should           rate and output characteristics as a function of problem

                                                                5
                              ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

complexity. Results are shown in Figure 6                                    Table 1. Multi-task SFT dataset produced by ATLAS.

The data shows a clear inverse correlation between problem            Task                                         Count      (%)
difficulty and success rate. Success rate is highest for EASY
problems at 47.1% and decreases systematically with com-              NL-to-Code Synthesis                         2,751     14.19
plexity, reaching approximately 20% for HARD and VERY
                                                                      NL-to-Spec Synthesis                         5,225     14.19
HARD problems. This validates that difficulty ratings mean-
ingfully reflect synthesis and verification challenge.                Spec-to-Code Synthesis                       2,751     14.19
The average length of successful programs increases con-              Specification Repair                         2,353     12.14
sistently with difficulty, growing from 3,848 characters for
EASY problems to over 5,600 for the hardest categories,               Implementation Repair                        4,562     23.53
suggesting that complex problems require more elaborate
                                                                      Proof Infilling                              1,743      8.99
code and proof structures. Conversely, failed attempts re-
main consistently long across all categories, indicating that
                                                                      Total                                        19,385 100.00
failures stem from complex, verbose, but ultimately incor-
rect generations rather than trivial attempts. These patterns
confirm the rational behavior of our synthesis pipeline.
                                                                      implementation, and correction. We therefore train not only
3.3.2. S KILL S ET                                                    on the final verified Dafny programs ATLAS produces, but
                                                                      also on its execution traces, including intermediate failed at-
TACO-verified provides skill set tags for many problems, en-          tempts. This approach significantly increases the per-sample
abling granular analysis of synthesis capabilities presented          efficiency of each verified program.
in Figure 7. Among tagged problems, data structure prob-
lems achieve the highest success rate at 14.1%, followed              The curated dataset includes: the initial natural language
by search problems at 13.1%. The pipeline struggles more              prompt, all intermediate generation attempts for specifica-
with sorting and range query problems (6.1% and 4.4%,                 tions and implementations, LLM-as-a-Judge feedback, and
respectively). Range query problems involve efficiently an-           the final verified program. As shown in Table 1, this enables
swering queries about intervals of objects (e.g., determining         us to extract multiple training tasks from each pipeline run:
the maximum sum of a contiguous subarray of fixed length k            direct implementation (NL-to-Code Synthesis), specifica-
within a given array), whereas higher-success problem types           tion formalization (NL-to-Spec Synthesis), implementation
typically require manipulation of individual elements (e.g.,          from specifications (Spec-to-Code Synthesis), assertion syn-
finding the closest-valued node with exactly k descendants).          thesis (Proof Infilling), and correction tasks. Correction
This pattern suggests that formally verifying operations on           tasks comprise over 35% of our dataset (Specification Re-
groups of objects presents a greater challenge than verify-           pair and Implementation Repair combined), transforming
ing discrete element manipulations, though comprehensive              typically discarded failed attempts into valuable learning
studies would be necessary to substantiate this observation.          opportunities. The Proof Infilling task further leverages suc-
                                                                      cessful verifications by teaching the model to reconstruct
                                                                      essential proof annotations such as loop invariants and auxil-
4. Supervised Fine-Tuning                                             iary lemmas. These examples are created by stripping proof
The verified programs produced by ATLAS provide a foun-               hints from verified programs. Of the 2.7K verified programs
dation for training models on formal verification. Rather             produced by ATLAS, approximately 1K verify automati-
than using only final outputs, we extract multiple training           cally without hints, yielding 1.7K training examples.
tasks from each pipeline run—including intermediate at-               This multi-task decomposition yields over 7 training exam-
tempts and repairs—to maximize data efficiency. We de-                ples per verified program on average, significantly amplify-
scribe our dataset curation, training procedure, and evalua-          ing the utility of each successful pipeline run.
tion on two Dafny benchmarks.
                                                                      4.1.2. E XECUTION
4.1. Training
                                                                      This multi-task approach structures our pipeline output into
4.1.1. DATASET C URATION                                              a curriculum for learning formal verification. We fine-tune
We hypothesize that fine-tuning for formal verification re-           Qwen 2.5 7B Coder, an open-source LLM for general cod-
quires a dataset that teaches more than final answers (Wei            ing that has limited knowledge of verification-aware lan-
et al., 2023). For agentic applications, the training data must       guages and syntax. We perform LoRA (Hu et al., 2021)
capture the process of problem decomposition, specification,          supervised fine-tuning using the Hugging Face TRL library
                                                                      (von Werra et al., 2020) on an AWS EC2 instance with 8

                                                                  6
                               ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis




Model                           Pass@1      Pass@5      Pass@10         Model                            Pass@1      Pass@3       Pass@5
                 1                                                      Qwen 2.5 Coder 7B                     7.5        13.2       15.8
Claude 4.1 Opus                        –           –        89.2
GPT-51                                 –           –        72.0        GPT-41                               33.1        49.4       53.4
Gemini 2.5 Pro1                        –           –        75.3        ATLAS Qwen 2.5 Coder 7B              39.0        57.0       65.8
                                                                          w/o s&c                            36.4        52.2       58.4
Claude 3 Opus2                      53.8        65.0        67.8          w/o test cases                     32.6        51.7       59.6
CodeLlama 7B2                       27.4        28.0        28.0
Dafny Verification (No LLM)         26.9        26.9        26.9                Figure 9. Evaluation results on DafnySynthesis.
Qwen 2.5 Coder 7B                   31.8        32.4        32.4
ATLAS Qwen 2.5 Coder 7B             55.8        56.9        56.9
  w/o s&c                           52.2        56.4        56.4
  w/o test cases                    54.9        56.4        56.5        from multiple attempts—Claude 3 Opus improves from
                                                                        53.8% to 67.8%. Recent frontier models have established
          Figure 8. Evaluation results on DafnyBench.                   higher performance (Bursuc et al., 2025), with Opus 4.1
                                                                        achieving 89.2% at Pass@10 (Bursuc et al., 2025), suggest-
                                                                        ing our approach may be constrained by the 7B parameter
NVIDIA H100 GPUs. The model trains for up to 10 epochs                  scale of our base model.
using standard cross-entropy loss with gradient clipping.
We evaluate on two downstream Dafny benchmarks to as-                   Ablation studies reveal that removing specification and com-
sess whether the ATLAS dataset enhances verified code                   pleteness checks or test cases has minimal impact on Dafny-
synthesis capabilities.                                                 Bench performance, with Pass@10 scores remaining around
                                                                        56%. This is expected, as DafnyBench primarily focuses on
                                                                        implementing pre-defined contracts rather than open-ended
                                                                        synthesis tasks where these verification components typi-
                                                                        cally prove more valuable (see Section 4.2.2). The bench-
4.2. Evaluation                                                         mark’s nature—having ground-truth specifications and not
4.2.1. DAFNY B ENCH                                                     requiring test case generation—likely undermines the perfor-
                                                                        mance boost of soundness and completeness (s&c) checks
To assess generalization, we evaluate our fine-tuned model              and test case generation compared to open-ended synthesis
on DafnyBench (Loughridge et al., 2024), a widely rec-                  tasks. The substantial improvement over the base model
ognized benchmark for Dafny proof hint generation. The                  Qwen 2.5 Coder 7B (32.4% at Pass@10) and size-matched
benchmark comprises 782 problems requiring assertions                   CodeLlama 7B (28.0% at Pass@10) demonstrates that our
and invariants to be filled into ground-truth implementations           ATLAS dataset successfully induces verification-aware ca-
with specifications.                                                    pabilities, even if scaling limitations prevent matching larger
As shown in Figure 8, ATLAS-enhanced Qwen 2.5 Coder                     frontier models.
7B achieves strong single-shot performance at 55.8%
Pass@1, surpassing Claude 3 Opus (53.8%), the state-of-                 4.2.2. DAFNY S YNTHESIS
the-art at the benchmark’s release (Loughridge et al., 2024).           To evaluate our model on Dafny code synthesis, we use the
However, performance plateaus at Pass@5 (56.9%), show-                  DafnySynthesis benchmark (Misu et al., 2024a), which con-
ing minimal improvement with additional attempts. This                  sists of 228 programming tasks adapted for Dafny verifica-
contrasts with Claude models, which benefit significantly               tion split into a test set of 178 tasks and 50 tasks for training.
   1
   As reported in (Bursuc et al., 2025).                                This dataset derives from the sanitized MBPP (Mostly Basic
   2
   As reported in (Loughridge et al., 2024) at the time of bench-       Python Programming) dataset (Austin et al., 2021), curated
mark release.                                                           to exclude problems requiring Python-specific features or ex-

                                                                    7
                               ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

ternal libraries incompatible with Dafny’s standard libraries.           et al., 2025) in Lean represent progress in this direction.
Each problem includes a natural language description of the
                                                                         Second, while reinforcement learning has shown success in
task, Dafny method signature, and 3 test cases. The evalua-
                                                                         mathematical theorem proving (Wang et al., 2025; Lin et al.,
tion of the benchmark considers a response successful if it
                                                                         2025), its application to verification-aware code generation
verifies without errors and contains non-trivial specifications
                                                                         remains underexplored due to lack of well-defined reward
of the functions or methods synthesized.
                                                                         structures. Future work should investigate combining com-
We evaluate our model using the signature prompt format                  piler feedback, complexity analysis, and proof resource
from (Misu et al., 2024a), which combines the problem de-                allocation as reward signals.
scription with its method signature and test cases. While
                                                                         Finally, recent advances in agentic theorem proving, includ-
(Misu et al., 2024a) explored contextless and Chain of
                                                                         ing HILBERT (Varambally et al., 2025) and SeedProver
Thought (CoT) prompting, we selected the signature format
                                                                         (Chen et al., 2025), suggest promising directions. These
as it provides a standardized and practical assessment of
                                                                         approaches demonstrate how agentic interaction with verifi-
verification-aware programming, balancing realistic context
                                                                         cation frameworks can augment model capabilities through
with minimal scaffolding.
                                                                         iterative refinement and guided exploration, with potential
Results are shown in Figure 9. ATLAS-trained Qwen 2.5                    for practical co-pilot and agent tools.
Coder 7B achieves 65.8% verification success at Pass@5,
surpassing GPT-4 (53.4%) by 12.4 percentage points, which                6. Conclusion
was the best performing model at benchmark release. The
substantial improvement over the baseline model Qwen 2.5                 Our work ATLAS, an automated pipeline for synthesizing
Coder 7B (15.8% at Pass@5) demonstrates the effective-                   verified Dafny programs from algorithmic problems with
ness of the ATLAS dataset in inducing verification-aware                 reference implementations. By introducing soundness and
programming capabilities.                                                completeness checks that leverage test cases, ATLAS en-
                                                                         sures specification quality and filters degenerate solutions.
Ablation studies reveal the contributions of different com-
                                                                         Applied to TACO-verified, the pipeline produces 2.7K veri-
ponents to ATLAS performance. Removing soundness and
                                                                         fied programs, which we decompose into 19K training ex-
completeness checks (s&c) degrades Pass@5 to 58.4%, in-
                                                                         amples spanning synthesis, repair, and proof infilling tasks.
dicating these components are crucial for guiding the model
                                                                         Fine-tuning Qwen 2.5 7B Coder on this data yields substan-
toward formally verified solutions. Similarly, removing test
                                                                         tial improvements on both DafnyBench (32.4% to 56.9%)
cases from fine-tuning yields 59.6% at Pass@5, demonstrat-
                                                                         and DafnySynthesis (15.8% to 65.8%), demonstrating that
ing the value of concrete examples in the synthesis process.
                                                                         synthetic data generation is a viable path to scaling LLM
                                                                         capabilities for formal verification. Our results suggest that
5. Related and Future Work                                               the data scarcity bottleneck for verification-aware languages
                                                                         can be addressed through automated synthesis pipelines,
Complementary to our work, dafny-annotator (Poesia et al.,
                                                                         opening opportunities for broader adoption of formal meth-
2024) targets automated annotation generation by bootstrap-
                                                                         ods in software development.
ping from existing Dafny programs. In contrast, ATLAS
employs a stage-wise approach that generates specifications
before implementations without requiring Dafny code as                   Impact Statement
input. While dafny-annotator evaluates on a test split of
                                                                         This paper presents work whose goal is to advance the field
DafnyBench after using the remainder for synthesis and
                                                                         of Machine Learning. There are many potential societal
training, ATLAS achieves strong performance on Dafny-
                                                                         consequences of our work, none which we feel must be
Bench without in-distribution training, demonstrating that
                                                                         specifically highlighted here.
general-purpose synthesis can effectively support special-
ized verification tasks.
                                                                         References
Several promising research directions remain unexplored.
First, while current benchmarks evaluate free-form synthe-               Achim, T., Best, A., Der, K., Fédérico, M., Gukov, S.,
sis or specialized tasks like proof hint infilling, there is a             Halpern-Leister, D., Henningsgard, K., Kudryashov,
need for benchmarks emphasizing end-to-end synthesis for                  Y., Meiburg, A., Michelsen, M., et al. Aristotle:
complete specifications. Recent work such as (Bursuc et al.,               Imo-level automated theorem proving. arXiv preprint
2025), VERINA (Ye et al., 2025), and CLEVER (Thakur                        arXiv:2510.01346, 2025.
    1
      As reported in (Misu et al., 2024a) at the time of benchmark
release.                                                                 Austin, J., Odena, A., Nye, M., Bosma, M., Michalewski,
                                                                           H., Dohan, D., Jiang, E., Cai, C., Terry, M., Le, Q., and

                                                                     8
                             ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

  Sutton, C. Program synthesis with large language models,           De Moura, L. and Bjørner, N. Z3: an efficient smt
  2021. URL https://arxiv.org/abs/2108.0                               solver. In Proceedings of the Theory and Practice of
  7732.                                                                Software, 14th International Conference on Tools and
                                                                      Algorithms for the Construction and Analysis of Systems,
Barnett, M., Chang, B.-Y. E., DeLine, R., Jacobs, B., and              TACAS’08/ETAPS’08, pp. 337–340, Berlin, Heidelberg,
  Leino, K. R. M. Boogie: a modular reusable verifier                  2008. Springer-Verlag. ISBN 3540787992.
  for object-oriented programs. In Proceedings of the 4th
  International Conference on Formal Methods for Com-                F* Development Team. F*: A General-Purpose Proof-
  ponents and Objects, FMCO’05, pp. 364–387, Berlin,                   Oriented Programming Language. https://fsta
  Heidelberg, 2005. Springer-Verlag. ISBN 3540367497.                  r-lang.org/, 2025. Accessed: 2025-10-06.
  doi: 10.1007/11804192_17. URL https://doi.or                       Hance, T., Lattuada, A., Hawblitzel, C., Howell, J., Johnson,
  g/10.1007/11804192_17.                                               R., and Parno, B. Storage systems are distributed systems
                                                                       (so verify them that way!). In Proceedings of the 14th
Bursuc, S., Ehrenborg, T., Lin, S., Astefanoaei, L., Chiosa,
                                                                       USENIX Conference on Operating Systems Design and
  I. E., Kukovec, J., Singh, A., Butterley, O., Bizid, A.,
                                                                       Implementation, OSDI’20, USA, 2020. USENIX Associ-
  Dougherty, Q., Zhao, M., Tan, M., and Tegmark, M. A
                                                                       ation. ISBN 978-1-939133-19-9.
  benchmark for vericoding: formally verified program
  synthesis, 2025. URL https://arxiv.org/abs/                        Hawblitzel, C., Howell, J., Kapritsos, M., Lorch, J. R.,
  2509.22908.                                                          Parno, B., Roberts, M. L., Setty, S., and Zill, B. Ironfleet:
                                                                       proving safety and liveness of practical distributed sys-
Cassano, F., Gouwar, J., Nguyen, D., et al. Multipl-e: A scal-         tems. Commun. ACM, 60(7):83–92, June 2017. ISSN
  able and polyglot approach to benchmarking neural code               0001-0782. doi: 10.1145/3068608. URL https:
  generation. IEEE Transactions on Software Engineering,              //doi.org/10.1145/3068608.
  2023.
                                                                     Hendrycks, D., Basart, S., Kadavath, S., Mazeika, M., Arora,
Chakarov, A., Geldenhuys, J., Heck, M., Hicks, M., Huang,              A., Guo, E., Burns, C., Puranik, S., He, H., Song, D. X.,
  S., Jaloyan, G. A., Joshi, A., Leino, R., Mayer, M.,                 and Steinhardt, J. Measuring coding challenge compe-
  McLaughlin, S., Mritunjai, A., Claudel, C. P., Porn-                 tence with apps. ArXiv, abs/2105.09938, 2021. URL
  charoenwase, S., Rabe, F., Rapoport, M., Reger, G., Roux,            https://api.semanticscholar.org/Corp
  C., Rungta, N., Salkeld, R., Schlaipfer, M., Schoepe, D.,            usID:234790100.
  Schwartzentruber, J., Tasiran, S., Tomb, A., Torlak, E.,
                                                                     Hicks, M. AWS cryptographic material providers library,
  Tristan, J., Wagner, L., Whalen, M., Willems, R., Xiang,
                                                                       2023a. URL https://github.com/aws/aws-c
  J., Byun, T. J., Cohen, J., Wang, R., Jang, J., Rath, J.,
                                                                       ryptographic-material-providers-libra
  Syeda, H. T., Wagner, D., and Yuan, Y. Formally verified
                                                                       ry-dafny. Accessed: 2026-01-28.
  cloud-scale authorization. 2025. URL https://www.
  amazon.science/publications/formally                               Hicks, M. How we built Cedar with automated reasoning
 -verified-cloud-scale-authorization.                                  and differential testing, 2023b. URL https://www.
                                                                       amazon.science/blog/how-we-built-ced
Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie,                ar-with-automated-reasoning-and-diffe
  A., Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J.,             rential-testing. Accessed: 2026-01-28.
  Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang,
  Z., Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H.,            Hoare, C. A. R. An axiomatic basis for computer program-
  Yang, F., Ying, H., Yuan, H., Yuan, Z., Zhan, T., Zhang,             ming. Communications of the ACM, 12(10):576–580,
  C., Zhang, Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y.,             1969. doi: 10.1145/363235.363259.
  and Zhu, T. H. Seed-prover: Deep and broad reasoning
                                                                     Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,
  for automated theorem proving, 2025. URL https:
                                                                       S., Wang, L., and Chen, W. Lora: Low-rank adaptation
  //arxiv.org/abs/2507.23726.
                                                                       of large language models, 2021. URL https://arxi
Chen, M., Tworek, J., Jun, H., et al. Evaluating large                v.org/abs/2106.09685.
  language models trained on code. arXiv preprint                    Kocetkov, D., Li, R., Allal, L. B., et al. The stack: 3 tb
  arXiv:2107.03374, 2021.                                              of permissively licensed source code. arXiv preprint
                                                                       arXiv:2211.15533, 2022.
ConsenSys. evm-dafny, 2023. URL https://github
  .com/Consensys/evm-dafny. Accessed: 2026-                          Lattuada, A. et al. Verus: Verified rust for low-level systems
  01-28.                                                               code. In OSDI, 2023.

                                                                 9
                            ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

Leino, K. R. M. Dafny: an automatic program veri-                  Poesia, G., Loughridge, C., and Amin, N. dafny-annotator:
  fier for functional correctness. In Proceedings of the             Ai-assisted verification of dafny programs, 2024. URL
  16th International Conference on Logic for Program-                https://arxiv.org/abs/2411.15143.
  ming, Artificial Intelligence, and Reasoning, LPAR’10,
  pp. 348–370, Berlin, Heidelberg, 2010. Springer-Verlag.          Polu, S., Han, J. M., Zheng, K., Baksys, M., Babuschkin, I.,
  ISBN 3642175104.                                                   and Sutskever, I. Formal mathematics statement curricu-
                                                                     lum learning, 2022. URL https://arxiv.org/ab
Li, R., Fu, J., Zhang, B.-W., Huang, T., Sun, Z., Lyu, C.,           s/2202.01344.
  Liu, G., Jin, Z., and Li, G. Taco: Topics in algorithmic
                                                                   Thakur, A., Lee, J., Tsoukalas, G., Sistla, M., Zhao, M.,
  code generation dataset, 2023. URL https://arxiv.
                                                                     Zetzsche, S., Durrett, G., Yue, Y., and Chaudhuri, S.
  org/abs/2312.14852.
                                                                     Clever: A curated benchmark for formally verified code
Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser,             generation, 2025. URL https://arxiv.org/abs/
  J., Leblond, R., Eccles, T., Keeling, J., Gimeno, F.,              2505.13938.
  Dal Lago, A., Hubert, T., Choy, P., de Masson d’Autume,
                                                                   Varambally, S., Voice, T., Sun, Y., Chen, Z., Yu, R., and
  C., Babuschkin, I., Chen, X., Huang, P.-S., Welbl, J.,
                                                                     Ye, K. Hilbert: Recursively building formal proofs with
  Gowal, S., Cherepanov, A., Molloy, J., Mankowitz,
                                                                     informal reasoning, 2025. URL https://arxiv.or
  D. J., Sutherland Robson, E., Kohli, P., de Freitas, N.,
                                                                     g/abs/2509.22819.
  Kavukcuoglu, K., and Vinyals, O. Competition-level
  code generation with alphacode. Science, 378(6624):              von Werra, L., Belkada, Y., Tunstall, L., Beeching, E.,
  1092–1097, December 2022. ISSN 1095-9203. doi:                     Thrush, T., Lambert, N., Huang, S., Rasul, K., and Gal-
  10.1126/science.abq1158. URL http://dx.doi.o                       louédec, Q. Trl: Transformer reinforcement learning.
  rg/10.1126/science.abq1158.                                        https://github.com/huggingface/trl,
                                                                     2020.
Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li,
  J., Xia, M., Chen, D., Arora, S., and Jin, C. Goedel-            Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., San-
  prover: A frontier model for open-source automated theo-          tos, M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z.,
  rem proving, 2025. URL https://arxiv.org/ab                       Lu, J., de Saxcé, H., Bailey, B., Song, C., Xiao, C.,
  s/2502.07640.                                                     Zhang, D., Zhang, E., Pu, F., Zhu, H., Liu, J., Bayer,
                                                                    J., Michel, J., Yu, L., Dreyfus-Schmidt, L., Tunstall,
Loughridge, C., Sun, Q., Ahrenbach, S., Cassano, F., Sun,           L., Pagani, L., Machado, M., Bourigault, P., Wang, R.,
  C., Sheng, Y., Mudide, A., Misu, M. R. H., Amin, N.,              Polu, S., Barroyer, T., Li, W.-D., Niu, Y., Fleureau, Y.,
  and Tegmark, M. Dafnybench: A benchmark for formal                Hu, Y., Yu, Z., Wang, Z., Yang, Z., Liu, Z., and Li, J.
  software verification, 2024. URL https://arxiv.                   Kimina-prover preview: Towards large formal reason-
  org/abs/2406.08467.                                               ing models with reinforcement learning, 2025. URL
                                                                    https://arxiv.org/abs/2504.11354.
Misu, M. R. H., Lopes, C. V., Ma, I., and Noble, J. To-
 wards ai-assisted synthesis of verified dafny methods.            Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
 Proceedings of the ACM on Software Engineering, 1                  Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-thought
 (FSE):812–835, July 2024a. ISSN 2994-970X. doi:                    prompting elicits reasoning in large language models,
 10.1145/3643763. URL http://dx.doi.org/10.                         2023. URL https://arxiv.org/abs/2201.1
 1145/3643763.                                                      1903.
Misu, M. R. H., Lopes, C. V., Ma, I., and Noble, J. Towards        Ye, Z., Yan, Z., He, J., Kasriel, T., Yang, K., and Song, D.
 ai-assisted synthesis of verified dafny methods. Proceed-           Verina: Benchmarking verifiable code generation, 2025.
 ings of the ACM on Software Engineering, 1(FSE):812–                URL https://arxiv.org/abs/2505.23135.
 835, 2024b.
                                                                   Ying, H., Wu, Z., Geng, Y., Yuan, Z., Lin, D., and Chen, K.
Müller, P., Schwerhoff, M., and Summers, A. J. Viper: A              Lean workbook: A large-scale lean problem set formal-
 verification infrastructure for permission-based reasoning.         ized from natural language math problems, 2025. URL
 In Proceedings of the 17th International Conference on              https://arxiv.org/abs/2406.03847.
 Verification, Model Checking, and Abstract Interpretation
 - Volume 9583, VMCAI 2016, pp. 41–62, Berlin, Heidel-
 berg, 2016. Springer-Verlag. ISBN 9783662491218. doi:
 10.1007/978-3-662-49122-5_2. URL https://doi.
 org/10.1007/978-3-662-49122-5_2.

                                                              10
                             ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis

A. Appendix
Code Examples
Incomplete Specification and Implementation
The listing below demonstrates a naive implementation of an arithmetic progression checker produced by ATLAS without
soundness and completeness checks. While syntactically correct, it lacks crucial specification properties. The implementation
only checks consecutive differences, missing ensures clauses specifying the relationship between all pairs of adjacent
elements.

method ArithmeticProgression(sequence: seq<int>)
  returns (hasSamePattern: bool)
    requires |sequence| >= 3
{
    var diff := sequence[1] - sequence[0];
    hasSamePattern := (forall i :: 0 <= i < |sequence|-1 ==>
        sequence[i+1] - sequence[i] == diff);
    return;
}



Complete Specification and Implementation using Soundness and Completeness checks
The addition of soundness and completeness checks results in output, which demonstrates robust and complete specifications.
In the below listing, the solution introduces two auxiliary functions: IsArithmeticSequence establishes the core
property that all adjacent differences must be equal, while IsArithmeticProgression adds the size requirement and
connects to the main implementation.

function IsArithmeticSequence(sequence: seq<int>): bool
  requires |sequence| >= 2
  ensures IsArithmeticSequence(sequence) <==>
    forall i, j :: 0 <= i < j < |sequence|-1 ==>
      (sequence[i+1] - sequence[i] ==
       sequence[j+1] - sequence[j])
{
  if |sequence| < 2 then false
  else
    var diff := sequence[1] - sequence[0];
    forall i :: 0 <= i < |sequence|-1 ==>
        sequence[i+1] - sequence[i] == diff
}

function IsArithmeticProgression(
    sequence: seq<int>): bool
  requires |sequence| >= 3
  ensures IsArithmeticProgression(sequence) <==>
    (|sequence| >= 3) &&
    IsArithmeticSequence(sequence)
{
  |sequence| >= 3 && IsArithmeticSequence(sequence)
}

method ArithmeticProgression(sequence: seq<int>)
    returns (hasSamePattern: bool)
  requires |sequence| >= 3
  ensures hasSamePattern <==>
    IsArithmeticProgression(sequence)
{
  var diff := sequence[1] - sequence[0];
  var i := 1;
  hasSamePattern := true;


                                                             11
                              ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis


    while i < |sequence| - 1
      invariant 1 <= i <= |sequence| - 1
      invariant hasSamePattern <==>
        (forall k :: 0 <= k < i ==>
          sequence[k+1] - sequence[k] == diff)
    {
      if sequence[i+1] - sequence[i] != diff {
        hasSamePattern := false;
        return;
      }
      i := i + 1;
    }
}



Soundness and Completeness Lemma Generation
Algorithm 1 presents the procedure for constructing verification lemmas that evaluate specification quality. The algorithm
takes as input a method m with its signature σ, pre-conditions R, post-conditions E, and a test suite T containing n test
cases. Each test case (ai , oi , Γi ) comprises input arguments ai , expected output oi , and input variable bindings Γi that map
method parameters to concrete values.

Soundness Lemmas. We instantiate the contract with concrete test inputs and outputs as preconditions, then verify that
the postconditions hold. Verification failure indicates the specification is inconsistent with known correct behavior.

Contradiction Lemmas. We assume the contract holds with a negated output and attempt to derive false. Success proves
the postconditions uniquely determine the output, though such proofs often exceed automated prover capabilities.

Perturbation Lemmas. We substitute LLM-generated incorrect outputs—such as negated booleans, offset integers, or
sequences with swapped elements—and check if the contract still holds. Successful verification reveals the specification
admits incorrect behavior and requires strengthening.

Feedback Integration. The complete lemma set L is submitted to the Dafny verifier. Verification results are parsed and
formatted into structured feedback:

Soundness Check Results:
  Test 1: PASS (contract consistent with test case)
  Test 2: FAIL (contract rejects valid input-output pair)

Completeness Check Results:
  Test 1: PASS (perturbed output correctly rejected)
  Test 2: FAIL (perturbed output incorrectly accepted)


This feedback is provided to the LLM Judge, which synthesizes actionable recommendations for specification refinement.
Common remediation patterns include strengthening postconditions with additional constraints, introducing auxiliary
predicates to capture invariant properties, and adding quantified assertions over collection elements.




                                                               12
                             ATLAS: Automated Toolkit for Large-Scale Verified Code Synthesis




Algorithm 1 Soundness and Completeness Lemma Generation
 1: Input: Method m, signature σ, pre-conditions R, post-conditions E, test cases T = {(ai , oi , Γi )}n
                                                                                                       i=1 (ai : inputs, oi :
    outputs, Γi : input variable bindings)
 2: Output: Set of verification lemmas L
 3: L ← ∅
 4: for i = 1 to n do
 5:   (ai , oi , Γi ) ← Ti
 6:   // Soundness lemma
 7:   Ri ← R ∪ Γi ∪ {σ = ai } ∪ {vout = oi }
 8:   ℓsound
        i     ← ConstructLemma(σ, vout , Ri , E)
 9:   L ← L ∪ {ℓsound i   }
10:   // Completeness lemma (contradiction)
11:   Ri ← R ∪ Γi ∪ {σ = ai } ∪ {vout ̸= oi } ∪ E
12:   ℓcontra
        i      ← ConstructLemma(σ, vout , Ri , {⊥})
13:   L ← L ∪ {ℓcontrai    }
14:   // Completeness lemma (perturbation)
15:   pi ← Perturbation(oi , E)
16:   Ri ← R ∪ Γi ∪ {σ = ai } ∪ {vout = pi }
17:   ℓperturb
        i       ← ConstructLemma(σ, vout , Ri , E)
18:   L ← L ∪ {ℓperturb
                      i     }
19: end for
20: return L




                                                            13
