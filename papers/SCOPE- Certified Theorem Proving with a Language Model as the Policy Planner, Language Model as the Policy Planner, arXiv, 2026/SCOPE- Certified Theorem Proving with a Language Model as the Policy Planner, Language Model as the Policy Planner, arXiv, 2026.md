                                                    SCOPE: Certified Theorem Proving with a
                                                     Language Model as the Policy Planner
                                                                                              Hanchao Zhou and Jialei Li



                                           Abstract—In proof assistants such as Lean, a generated proof              long proof is the conjunction of all its numeric content. If the
                                        must pass machine compilation checks, so evaluation needs no                 model writes each content element correctly with probability
                                        human scoring. Direct generation fails on multi-step numeric                 p and a proof contains k elements, the pass rate of direct
                                        propositions: a proof is valid only if every content integer is
                                        correct, so the pass rate is bounded by the k-th power of the per-           generation is bounded above by pk . When k grows with
                                        integer accuracy. Controlled corruption across 2,617 reference               problem difficulty, any fixed p below one drives the pass rate
                                        proofs confirms this power law. SCOPE (State-Conditioned                     down exponentially. Our experiments support this analysis and
arXiv:2610.08319v1 [cs.AI] 6 Oct 2026




                                        Operator Planning and Execution) enforces the natural division               fold the countermeasure into the same architectural frame:
                                        of labor: the model plans over an operator vocabulary, a                     if the analysis holds, the rational architectural response is
                                        symbolic engine executes the numerics, and a compiler renders
                                        the proof. On a 218-problem suite it certifies 191/218 (87.6%) with          to narrow the model’s role to policy planning free of nu-
                                        a 135M backbone; the 7B DeepSeek-Prover-V1.5-RL certifies                    meric generation, hand numeric computation to a symbolic
                                        18/218 at 27.5 times the tokens and 37.5 times the wall-clock,               tool, and hand proof text to template compilation. In human
                                        and DeepSeek-Prover-V2-7B certifies zero on a bidirectional dual             mathematical practice, the core competence of solving lies
                                        suite. Multi-step thinking costs 6.12 discrete decision actions              to a large extent in perceiving and choosing tools: judging
                                        per problem and produces no natural-language thinking text.
                                        Replacing the lagged engine state in the decision frame with                 which theorem, which lemma, which transformation, or which
                                        the current one lifts the pass rate from 117/218 to 191/218,                 algorithm applies to the proposition at hand. Carrying out the
                                        while up-weighting the chain-end loss hurts. On the public Lean-             computation is comparatively mechanical and has always been
                                        Workbook library, 2,132 of 3,536 gradeable admissible problems               done precisely by external procedures. We therefore test a
                                        certify (60.29%) with zero regression on the main suite. All                 division-of-labor hypothesis: let the language model supply
                                        readings come from a version-frozen review with independent
                                        rechecks and reverse verification. Restricting free generation and           the connection between problem and tool, and let a symbolic
                                        keeping decision-time information visible is a more direct route             computing component execute the numerics; then examine
                                        than enlarging the model.                                                    whether this division supports long-chain, multi-step, exact
                                           Index Terms—Automated theorem proving, formal verification,               reasoning. Specifically, on three families of constructively
                                        large language models, Lean, neuro-symbolic systems.                         generated discrete-mathematics problems (induction, inequal-
                                                                                                                     ities, and number theory), we build a complete system called
                                                                I. I NTRODUCTION                                     SCOPE (State-Conditioned Operator Planning and Execution).
                                                                                                                     The backbone is the 135M-parameter SmolLM2 [2], fitted with
                                           Automatic generation of formal proofs has long been a hard                an operator-selection head and an argument-prediction head
                                        problem at the intersection of artificial intelligence and formal            that produce a solution chain step by step inside a vocabulary
                                        verification. Proof assistants such as Lean [1] bring propo-                 of 194 operators; the numerics of each step are computed by a
                                        sitions, proofs, and the checking process into one machine-                  symbolic execution engine that returns the state; the proof text
                                        verifiable framework: a candidate proof is accepted only if                  is generated by a compiler from the chain and the engine’s
                                        the compiler confirms that every step is legal and that no                   results, and is finally reviewed by the Lean compiler. On
                                        unproven assumption is used. This property makes theorem                     this architecture we run a set of experiments that isolate one
                                        proving a suitable testbed for studying the reasoning ability                variable at a time, plus an external-model comparison. The
                                        of language models: evaluation involves no human scoring,                    main results follow. When complete proof text is generated
                                        and surface fluency earns no credit. In recent years, language               directly, token-level accuracy and certified pass rate diverge
                                        models ranging from hundreds of millions to tens of billions                 sharply: the model’s token accuracy on a held-out set from
                                        of parameters have made a series of advances in this direction,              the training distribution is 0.9637, yet certified passes on the
                                        yet certified pass rates on propositions that require multi-                 218-problem suite number 0/218; a same-distribution control
                                        step numeric derivation remain low. Failed samples show                      set (20 problems) yields one pass, matching the power-law
                                        a consistent pattern: the proof is structurally conventional                 prediction of about 0.031 computed from the number of
                                        (it uses standard tactics such as induction, rewriting, and                  content elements per proof (about 14.9). The 7B DeepSeek-
                                        normalization) but breaks at concrete numeric values and ends                Prover-V1.5-RL [3] passes 18/218 on the same suite, with 177
                                        with an unsolved goal (sorry in Lean). The pattern suggests                  outputs terminating in sorry, the same pattern. Once proof text
                                        that the bottleneck may lie not in the choice of proof steps                 is produced by the compiler instead, the pass rate of the same
                                        but in generating the numeric content one item at a time. The                model on the same suite rises from 1/218 to 117/218. The
                                        division of labor can be stated quantitatively: the validity of a            compiler reproduces the reference proofs byte for byte on all
                                          Jialei Li (e-mail: gayly0414@163.com). Corresponding author: Hanchao       2,399 corpus rows and certifies 218/218 when fed the reference
                                        Zhou (e-mail: zhouhanchao6@gmail.com).                                       chains of the test suite, so this stage contributes no precision

                                                                                                                 1
loss. Analysis of the remaining errors further localizes the             paradigm: the model produces proof text or tactic sequences
failure to the final step of the chain: all 101 first errors among       itself. Its failure mode on multi-step numeric propositions is
the 101 errors occur at the last step. The residual class read           the subject of our first empirical law. Open environments such
off the final step stands in a fully determined correspondence           as LeanDojo [5] provide the evaluation infrastructure for this
with the engine’s residual value (799/799 on the corpus and              line of work. Another line couples learning with symbolic
181/181 on the test suite), but the decision frame carries a state       search: HyperTree Proof Search [9] explores proof trees under
that lags one step behind. A 2 × 2 factorial experiment (state           a transformer guide, Magnushammer [10] replaces hand-tuned
shifted or not, crossed with chain-end loss weight) shows:               premise selection with a learned retriever, Draft-Sketch-Prove
shifting the state raises the pass rate from 117/218 to 191/218;         [11] turns an informal draft into a formal sketch that smaller
up-weighting the loss lowers it (117 to 110; with the state              provers complete, AlphaGeometry [12] pairs a language model
shifted, 191 to 172). In resource terms, this architecture emits         with a symbolic deduction engine, and AlphaProof [13] carries
6.12 decision actions per problem on average, takes 0.53 s               the recipe to competition-level problems. Assistant-style tools
per problem, and peaks at 833 MiB of inference memory; the               bring models inside proof assistants: Baldur [14] generates
comparison model emits 168.0 generated tokens, takes 19.88               and repairs whole Isabelle proofs from failure feedback, and
s, and peaks at 8,567 MiB. The two systems differ in interface           Lean Copilot [15] serves tactic suggestions natively in Lean
conditions: the comparison model has no execution engine or              4; in both, the model remains in the role of producing proof
compiler and must generate the complete proof as free text.              text. Learned neuro-symbolic models of this broad family are
We use this comparison as evidence on the structure of the               an established design space in this journal [16]. What the
output channel. The contributions of this paper are as follows.          proof-producing systems above do not provide is a controlled
We give, in a controllable domain, the error-product structure           analysis of the failure mechanism that concerns us here, the
of direct long-proof generation and verify it quantitatively.            conjunction structure of long numeric derivations. Research
We propose and implement SCOPE, an architecture in which                 on tool-augmented language models shows that delegating
the language model serves as the policy planner, a symbolic              numeric computation or code execution to external tools
engine serves as the computing component, and a compiler                 improves reliability on the corresponding tasks; representa-
serves as the text-generation component, reaching an 87.6%               tive work includes program-aided language modeling [17]
certified pass rate on the test suite. The model’s multi-step            and code-interpreter invocation [18], and documented failures
thinking is endogenous to the architecture and enabled by                of language models on fine-grained character- and symbol-
default: it happens in the latent decision space over operator           level manipulation [19] sharpen the case for delegation. The
chains, produces no natural-language thinking text, and costs            difference here is that tool calls are not wholesale delegation
6.12 decision actions per problem on average. Thinking never             (generate a program once, then run it) but are embedded in the
passes through the output channel, yet the system is not a black         step-by-step decision process, with every decision conditioned
box: per-step decision distributions and engine states can be            on the state the tool returns; the tool state itself enters training
read out directly. A factorial experiment attributes the main            and inference as model input, and we examine the link
information bottleneck of chain decisions to state visibility at         between state visibility and decision correctness on that basis.
decision time rather than to loss allocation. For all readings           Curriculum learning [20] and constructive data synthesis are
we establish a validity pipeline of version-frozen review plus           widely used in mathematical-reasoning training; the distinc-
independent recheck plus reverse verification. We complete               tive property of our corpus engineering is auditability: every
a domain-extension validation on a public problem library:               training row carries an executable reference chain and has
the admissible domain is determined by mechanical checks                 passed a mechanically executed leakage check. Work related
and disclosed layer by layer, model-independent readings are             to our error analysis includes exposure bias and its remedies
reported separately from system readings, and an independent             in sequence generation [21], [22], error compounding that
final audit verifies the numbers. Code, corpus, and review               deepens with derivation length in compositional tasks [23],
programs will be released.                                               and step-level verification of reasoning chains [24], with chain-
                                                                         of-thought prompting [25] as the common substrate. Most of
                                                                         these works observe the phenomenon indirectly, through end-
                     II. R ELATED W ORK
                                                                         to-end metrics on natural-language reasoning tasks; we reduce
   The use of language models for theorem proving has                    it, in a certified setting, to a computable structure, namely a
evolved from tactic-level prediction to complete proof gen-              Boolean conjunction of proof validity over content elements,
eration. GPT-f [4] and follow-up work train tactic-prediction            which yields a definite power-law relation between pass rate
models in the Lean and Metamath environments; ReProver                   and per-element accuracy and admits direct examination under
[5] and related retrieval-augmented methods improve proof                controlled conditions.
search with premise selection; the DeepSeek-Prover line [6],
[3] trains proof-specialized models on Lean 4 from large-scale
                                                                                                   III. M ETHOD
synthetic data, with proof-assistant feedback reinforcement
learning entering at V1.5 and evaluation centered on bench-                This section describes the components of SCOPE. The
marks such as miniF2F [7] and Lean-Workbook [8]; its V1.5                system takes a mathematical proposition written in a domain-
release is the comparison model of this paper. The common                specific language as input and outputs a proof certified by
form of these methods is what we call the direct-generation              the Lean compiler. Processing has four parts: the discrete

                                                                     2
representation of propositions and the operator vocabulary                               argument structure and state-update form. The model never
(Section III-A), the symbolic execution engine (Section III-                             touches Lean tactic names; the correspondence at tactic level is
B), the chain-planning model (Section III-C), and the proof                              handled by the compiler. For later reference, we fix the formal
compiler (Section III-D); the review protocol is given in                                notation as follows. Definition 1 (problem state): a problem
Section III-E.                                                                           state is an integer vector with a fixed field structure,



                                                                                                             s = (x1 , . . . , xd ) ∈ Zd               (1)


                                                                                         where the fields correspond to the objects of the proposition
                                                                                         (variables, polynomial coefficients, moduli), and one problem-
                                                                                         type family shares one field structure. Definition 2 (operators
                                                                                         and solution chains): the legal operators form a finite vocab-
                                                                                         ulary O (194 initially, 220 after the public-library extension);
                                                                                         each operator o ∈ O carries an argument vector a of operator-
                                                                                         specific shape; one decision is the pair (o, a). A solution chain
                                                                                         is a finite sequence


                                                                                                                                               
                                                                                                          τ = (o1 , a1 ), . . . , (oT , aT )           (2)



Fig. 1. The SCOPE architecture and data flow. A mathematical proposition                 where T is the chain length, and the chain terminates with an
enters a latent decision loop through discrete encoding: the chain planner, with         end symbol. Definition 3 (execution engine and certification):
its operator and argument heads, handles perception and routing and commits
to one decision per step inside the operator vocabulary, which supplies both             the execution engine is a deterministic map E : (s, o, a) 7→
operator semantics and rendering templates; the symbolic engine executes                 (s′ , cert) that returns a unique state s′ and an execution
each step exactly, and the state frame, after the state shift, feeds back into the       certificate cert for identical inputs. Write acc(π) = 1 if proof
decision loop, so multi-step thinking is carried endogenously by the loop with
zero generated tokens (the Zero-token thinking label in the figure). The chain           text π passes certification, i.e., it compiles in Lean and the
and its arguments go to the proof compiler, which renders Lean text from the             compiled result depends on no unproven assumption; every
templates; the Lean compiler reviews it, a frozen review program performs an             certified pass rate reported in this paper is the mean of acc
independent recheck and reverse verification, and a certified proof is output.
                                                                                         over the corresponding problem set. Definitions 1 to 3 fix the
                                                                                         formal objects of the system, and the solving goal can now
A. Task Definition and Operator Vocabulary                                               be stated: given a problem state s, find a solution chain whose
                                                                                         compiled proof passes certification, i.e.,
   The problem domain covers three families of elemen-
tary discrete mathematics: induction identities, polynomial in-
equalities, and elementary number-theoretic divisibility. Each                                                                     
proposition is produced constructively by a parameterized                                              find τ such that acc C(τ, s) = 1                (3)
generator together with a reference solution chain and a
reference proof; generation guarantees solvability, and the
reference solution is verifiable by mechanical execution. A                              where C is the proof compiler (Section III-D, formalized in
proposition is given as a state: the objects it mentions (vari-                          (12)) and acc is the certification indicator of Definition 3.
ables, polynomial coefficients, moduli) appear as a fixed field                          This search cannot be carried out by enumerating chains: the
structure rather than as natural language. Solving is modeled                            number of candidate combinations per step is the product
as an operator chain, where each step consists of an operator                            of the vocabulary size and the value-space size (220 and
identifier and a list of concrete arguments, and the chain ends                          352 in our configuration), chains run 5 to 9 steps, and the
with an explicit terminator. All legal operators form a finite                           chain space exceeds the fifth power of that product. The role
vocabulary; the initial release contains 194 operators, extended                         of the chain-planning model (Section III-C) is to locate the
to 220 for the public library (Section X). The vocabulary                                correct chain in this space, step by step, under a learned
grows in successive batches: each new batch of operator rows                             conditional distribution. Table I maps the problem-domain
receives only incremental training, with zero regression on                              layers onto the composition of the vocabulary. The vocabulary
existing capability as the acceptance gate. Every operator has                           grows in batches, each covering a problem type or one domain
an executable semantics in the engine. The vocabulary is                                 extension; every batch has executable semantics in the engine
organized by problem family, for example the nested-induction                            (Section III-B), and the vocabulary carries a per-operator
family, the multi-lemma-combination family, and the sum-of-                              admissibility matrix over multiplier rows that restricts the legal
squares decomposition family; operators of one family share                              argument set of each decision.

                                                                                     3
                               TABLE I                                               This correspondence holds for every problem in the corpus and
 P ROBLEM - DOMAIN LAYERS AND THE COMPOSITION OF THE OPERATOR                        the test suite (799/799 and 181/181) and underlies the factorial
    VOCABULARY. T HE INITIAL RELEASE HAS 194 ROWS ( FIRST FOUR
 SEGMENTS ) AND THE PUBLIC - LIBRARY EXTENSION RAISES THE COUNT                      analysis of Section VIII. Two design constraints govern the
TO 220 (S ECTION X); PER - SEGMENT COUNTS ARE MEASURED FROM THE                      engine-model interface. First, the arguments fed to the engine
                 SYSTEM ’ S VOCABULARY REGISTRY.                                     take reference values during training and model predictions
                                                                                     at inference; if a predicted argument is illegal (for example,
      Vocabulary       Rows   Covered problem types and introduction
       segment                               batch                                   outside its domain), the engine rejects execution and the step
     Base segment      161    Core operators and skeleton rows of the
                                                                                     is scored as an error. Second, the engine returns a fixed-
                                    initial three domains (induction                 dimensional state for every operator, so the states of different
                                  identities, polynomial inequalities,               operators can be concatenated within one frame structure. For
                                      number-theoretic divisibility)
      Deep-chain        17    Closed-form operators of the deep-chain
                                                                                     the mainstay operator of the sum-of-squares family (single-
       extension                 corpus: sum-of-squares closed forms,                variable block absorption), executing (4) inside the engine
        segment               geometric and summation closed forms,                  must satisfy an exact absorption criterion: one square com-
                                  block closing, partial fractions, and
                                        high-tower combinations
                                                                                     ponent is removed if and only if the residual decomposes into
     Construction-      7       Three construction curricula: induction              that square term and a remainder that contains no nonzero
      curriculum              recursion, ring identities, sum-of-squares             term in any variable supporting the removed linear form, i.e.,
       segment                   decomposition, divisibility witnesses
      Deep-chain        9         Nested-induction chain construction                           Rin = m ℓ2 + Rout ,
    family segment               (difference-equation solving, folding,
                               telescoping check, closed-form closing)                              and the coefficients of the variables         (6)
                                and sum-of-squares chain construction
                                 (single-variable blocks, cross blocks,                               of ℓ in Rout are all zero
                                           three closing types)
    Substitution and    4     Algebraic evaluation, modular evaluation,              The two conditions together make the removal exact; argu-
      evaluation                        and variable substitution                    ments that fail the criterion (for instance m not a positive
       segment
    Routing segment     9        Route operators from public-library
                                                                                     integer, or a remainder that still contains terms in variables
                               problem statements to existing families               supporting ℓ) are rejected by the engine. The criterion is
       Extension        13       Nine extension families: goal-shape                 verified mechanically on a finite test grid:
        segment                   splitting, quantifier introduction,
                              existence witnesses, predicate unfolding,                         Rin (k) = m ℓ(k)2 + Rout (k),
                                     radical reduction, symbolic                                                                                  (7)
                               exponentiation, factorials, library-name                                for all k on the verification grid
                                     entry, and chained relations
         Total         220                        —                                  The grid is determined by the variable domains and a degree
                                                                                     bound; passing the verification issues the execution certificate
B. Symbolic Execution Engine                                                         of the step, which is written to disk together with the chain
   The execution engine is a set of deterministic symbolic-                          (Section III-G). Table II lists representative operators of each
computation programs, one execution function per operator.                           problem family and their execution logic. Operator names
Given the current state and the arguments, the function per-                         are the identifiers of the implementation (family-prefixed in
forms the computation and returns two things: the numeric                            the released code); for each family we show one or two
intermediate result, and a mechanically checkable execution                          operators that carry its main computation; full specifications
certificate (for example, an algebraic identity check that                           of all operators ship with the code.
passed). Taking the sum-of-squares decomposition family as
an example, each step removes one square component from                              C. Chain-Planning Model
the goal expression and returns what remains, which we call
the residual; its update rule is                                                        The planning model uses SmolLM2-135M [2], a trans-
                                                                                     former decoder [26], as the backbone and adds two output
                        Rout = Rin − m ℓ2                                  (4)       heads: the operator-selection head gives, over the vocabu-
where Rin and Rout are the residuals before and after the                            lary, the distribution of the next operator, and the argument-
step, m is the coefficient of the removed square term, and ℓ is                      prediction head gives that operator’s arguments, predicted in a
the corresponding linear form. The residual enters the model’s                       discretized value space (352 candidates). Writing the problem
state frame as an eight-dimensional numeric vector (Section                          state as s and the representation of the executed steps as
III-C). All engine computation uses exact integer and rational                       h1 , . . . , ht−1 , the decision at step t is
arithmetic and contains no floating-point error; the engine is
implemented in C++/CUDA, is bit-aligned with the training-                                           (ot , at ) = fθ (s, h1 , . . . , ht−1 )      (8)
side reference implementation, and runs more than five times
                                                              where ot is the operator choice, at the arguments, and θ the
faster than it. The final step of a chain must classify the final
                                                              model parameters. Decisions proceed autoregressively until the
residual ρ :
                                                              model emits the terminator or the step budget is reached. The
c(ρ) = 0 (ρ = 0); c(ρ) = square (ρ ∈ {4, 9, 16, 25, 36, 49}); two output heads expand fθ into discrete distributions. Write
c(ρ) = other (otherwise)                                      the decision frame as Ft = (s, h1 , . . . , ht−1 ) (consistent with
                                                         (5) Algorithm 2); the operator head gives a distribution over the

                                                                                 4
                                                 TABLE II
  EXECUTION LOGIC OF REPRESENTATIVE OPERATORS. THE EXECUTION SEMANTICS AND CERTIFICATES ARE THE ACTUAL
CHECKING PROCEDURES INSIDE THE ENGINE; THE RENDERED TACTICS ARE THE LEAN TACTICS THE COMPILER EXPANDS FOR
                                                THAT STEP.

      Operator (family)                          Execution semantics                                           Execution certificate                      Rendered tactics
           sos block           Deducts one single-variable square component from the            Grid identity (7) plus absorption criterion (6); m a          positivity
       (sum-of-squares)                          current residual per (4)                                         positive integer
         sos tail other        Classifies the final residual per (5) and closes the chain       Closed-chain identity: the goal equals the sum of       norm num, nlinarith
       (sum-of-squares)                                                                              deducted squares plus the final residual                    only
      nest solve (nested      Solves one difference equation from increment and initial            Quadruple check: exact degree, initial value,         rw and ring inside
           induction)                  value, yielding a polynomial closed form                           telescoping grid, degree ladder                      induction
      nest delta (nested                 Verifies that the closed form satisfies                 Pointwise identity of the forward-difference grid     Certificate-level check;
           induction)                        F (k + 1) − F (k) = S(k)                                                                                   emits no tactic lines
       s poly (routing)         Recognizes the statement as a polynomial identity and                        Ring-law recomputation                               ring
                                              invokes ring-law verification
       s eval (routing)          Recognizes the statement as numeric evaluation and                      Exact arithmetic recomputation                      norm num
                                                 computes step by step
      sqrt iso (extension      Gives exact values for radicals of perfect-square closed                   Grid check of side conditions                rw (radical equivalence
           families)           forms; squares one-sided radical inequalities under side                                                                       theorems)
                                                        conditions
    intro binder (extension   Strips the leading universally quantified binder and passes                        Structural check                               intro
           families)                           the body to existing routes




vocabulary O, and the argument head a distribution over the                                 Algorithm 1 Training the chain-planning model
value space V with |V | = 352:                                                              Require: deep-chain corpus D (with reference chains (o∗ , a∗ )
                                                                                                and per-step ground-truth engine states); batch-order file;
                                                                                               6000 training steps; batch size 6; learning rate 4 × 10−5 .
                     P (ot = o | Ft ) ∝ exp zo (o) ,                                            Convention: during training, the state and arguments in
                                                                                (9)
                                                                                                the decision frame take reference values (Section III-B).
                                                    
                  P (at = v | ot , Ft ) ∝ exp za (v)
                                                                                             1: initialize parameters θ (SmolLM2-135M backbone plus
                                                                                                operator-selection and argument-prediction heads)
where zo and za are the logits of the two heads on the decision                              2: for step = 1 to 6000 do
frame, and the legal value set of each operator is restricted by                             3:    draw a mini-batch {(s, o∗ , a∗ )} ⊂ D following the
the admissibility matrix carried with the vocabulary (Table I).                                    batch-order file
At inference, the highest-probability item is taken at every                                 4:    for each sample, read the decision frame step by step
step. The training objective is the cross-entropy of operator                                      (19); compute (ot , at ) ← fθ (·)
selection and argument prediction, supervised by the reference                               5:    L ← Lop (ot , o∗t ) + (1/24) Lval (at , a∗t ) {(10)}
chain (o∗t , a∗t ):                                                                          6:    if end-step weighting enabled (Exp. 4B/C, λ = 5): L ←
                                                                                                   L + (λ − 1) 1[t = T ] Lop {(11)}
                                                                                             7:    θ ← update(θ, ∇L)
                  L = Lop (ot , o∗t ) + 24
                                         1
                                           Lval (at , a∗t )                    (10)          8: end for
                                                                                            Ensure: trained parameters θ and the training log (steps,
                                                                                                losses, and checksums).
where the argument term is scaled by the total number of
value slots (24). The chain-end weighting configuration gives
the operator cross-entropy at the terminating step (t = T ) an                              D. Proof Compiler
extra weight, bringing its total weight to λ(Experiment 4 uses                                 Proof text is produced by a compiler: given an operator
λ = 5):                                                                                     chain, the compiler expands each step into Lean tactic se-
                                                                                            quences under the operator’s template rules, and every number
                                                                                            in the output comes from the engine’s actual computation.
                   LW = L + (λ − 1) 1[t = T ] Lop                              (11)
                                                                                            The compiler calls no language model and reads no reference
                                                                                            proof text. Its correctness rests on two verifications: on all
                                                                                            2,399 corpus rows, the compiled output matches the reference
All experiments share one training configuration: 6,000 steps,
                                                                                            proof byte for byte (2,399/2,399); on the test suite, feeding
batch size 6, learning rate 4×10−5 , random seed 20260923,
                                                                                            the reference chains yields proofs that all certify (218/218).
and the same batch-order file (whose checksum is identical
                                                                                            Consequently, whenever the model’s chain is correct, the
across configurations), so that any difference between con-
                                                                                            compiled proof certifies, and the certified pass rate of the
figurations is attributable to a single variable. The training
                                                                                            system is determined entirely by the quality of chain deci-
dynamics of the final configuration (loss components and
                                                                                            sions. Compilation is a deterministic map. Writing E(τ , s)
gradient norms over the 6,000 steps) appear in Fig. A1. An
                                                                                            for the step-by-step execution results (the state and certificate
earlier version of the model also carried a proof-text generation
                                                                                            sequence) of chain τ started from state s, the proof text is
head (used in Experiments 1 and 2 of Section VI); it was                                                                             
removed following the findings of Section VII.                                                                    π = C τ, E(τ, s)                       (12)

                                                                                      5
The map C has no free parameters and calls no language                  and returns the numeric state plus a mechanically checkable
model: template rules fix the tactic skeleton, and all num-             execution certificate; for example, the correspondence between
bers come from the actual computation in E(τ , s). Since C              the final class and the residual value holds row by row on
reproduces the reference proofs byte for byte on the corpus             the corpus and the test suite (799/799 and 181/181), so the
(2,399/2,399), the search problem of (3) reduces entirely to            correctness of this stage can be verified independently of the
the chain-decision problem.                                             model. Proof text is generated by the compiler from templates;
                                                                        it matches the reference proofs byte for byte on all 2,399
Algorithm 2 SCOPE solving one problem                                   corpus rows and certifies on all 218 test problems given
Require: problem state s; operator vocabulary O; execution              the reference chains, showing that the text stage contains
    engine E; proof compiler C; step budget Tmax .                      no free parameters. Auditability at the review layer rests
 1: h ← ∅; t ← 1                                                        on three mechanisms: the review program is version-frozen
 2: while t ≤ Tmax do                                                   (MD5-anchored, checked before and after grading in every
                                                         (t−1)
 3:    read decision frame Ft = (s, h1 , . . . , ht−1 , Rout )          experiment); accepted samples are re-reviewed through an
       {(19)}                                                           independent path in strata (66/66 zero discrepancies, repli-
 4:    (ot , at ) ← fθ (Ft ) {(8)}                                      cated across two configurations); reverse verification rejects all
 5:    if ot is the terminator then break                               corrupted proofs (12/12 for both truncation and substitution).
 6:    (s, cert) ← E(s, ot , at ); ht ← (ot , at ) {(4)}                Two zero-capability controls (the untuned backbone and a
 7:    t←t+1                                                            rule-based solver, 1,080 applicable problems each with zero
 8: end while                                                           passes) further rule out earning certified scores by guessing or
 9: τ ← (h1 , . . . , ht−1 ); π ← C(τ )                                 pattern matching. Auditability at the experiment layer takes
Ensure: the operator chain τ , the proof text π, and per-step           the form of configuration control and record completeness: all
    records (decision distributions, arguments, engine states,          configurations share the batch-order file (identical checksums)
    and certificates).                                                  and random seeds; the differing variable of each configuration
                                                                        is registered in the design file in advance; every results file
                                                                        carries a checksum ledger. A direct payoff of auditability is
E. Review Protocol                                                      error analysis at decision-step granularity: the 101 first errors
   Review is performed by an independent automatic program:             of Section VIII all localize to the final step of the chain, which
a candidate proof is compiled in the Lean environment, and              presupposes the symbolic decision sequence; attribution at this
the compiled result is checked to depend on no unproven                 granularity cannot be obtained directly from free-text output.
assumption (no sorry and no corresponding axioms). The
program stayed version-frozen for the entire experimental               G. Process Auditability and Observability of Latent Thinking
period (anchored by an MD5 checksum, given in Appendix
B), and every experiment was checksummed once before and                   The intermediate process consists of explicit symbolic struc-
once after review. To rule out bias introduced by review                tures and can be inspected item by item. For every problem,
itself, a dual-protocol recheck is executed: at least 60 accepted       the system writes to disk: the model’s complete operator
proofs, drawn in strata, are re-reviewed one by one through             chain, the arguments of every step, the residual and execution
an independent path; in the reverse direction, 12 corrupted             certificate returned by the engine, the proof text produced by
proofs of each of two kinds (final segments truncated; proofs           the compiler, and the review program’s verdict with its reason
of other problems substituted) are submitted, and the program           (the compilation result and the axiom dependencies). Errors
is required to reject them. Across all experiments the two              can therefore be pinned to specific steps: Section VIII localizes
protocols show zero discrepancies, and reverse verification             all 101 errors to the final step of the chain and reports the
rejects all cases.                                                      predicted probability at each erroneous step (55 of them at 0.9
                                                                        or above). Step-level analysis of this kind lacks an operational
                                                                        counterpart in the free-text generation paradigm: text output
F. Auditability                                                         offers only an aggregate right-or-wrong signal and surface
   The design makes the entire solving process inspectable step         statistics. In the final configuration of this paper, multi-step
by step. The model’s output is not free text but an operator            thinking is the default behavior granted directly by the training
chain inside a restricted vocabulary: each step consists of an          objective; no prompt or mode switch triggers it. The entire
operator identifier and concrete arguments, whose legality can          solving process consists of step-by-step decisions over the op-
be checked one item at a time against the engine’s semantics.           erator chain and produces no natural-language output: on av-
This property forms the contrast with the direct-generation             erage 6.12 discrete decision actions per problem (Section IX),
paradigm: the intermediate steps of a free-text proof admit             with the proof text compiled separately. Because the carrier of
no mechanical inspection, and evaluation must rely on the               decision is a discrete symbolic structure, the thinking process
final compilation result. In this architecture, any output can          is observable from outside, and the observation does not rely
be replayed as a complete decision sequence, and an error               on the model’s self-report: the operator-selection distribution,
can be pinned to a specific step. Auditability at the computing         the predicted arguments, and the engine-returned state of every
layer comes from the determinism of the engine. The engine              step can be read and tallied directly. The hidden state of
executes every step in exact integer and rational arithmetic            the decision frame is equally readable: in low-dimensional

                                                                    6
projection it organizes by problem family (nearest-neighbor              proof is a two-layer induction structure: an induction first
purity 0.999), the frames of one problem advance continuously            establishes the closed form of the inner recurrence, then an
along the chain (Fig. 2), and the projected vectors are frame-           induction on the outer goal uses the previous step’s result, and
for-frame identical to the hidden states that the output heads           ring normalization finishes the proof. The proof was certified
actually consume. By comparison, the observability of chain-             by the review program. The two public-library examples come
of-thought comes at the price of generated tokens, and natural           from the Lean-Workbook final exam. For the algebraic identity
language produced as an explanation can disagree with the                x5 −y 5 = (x−y)(x4 +x3 y+x2 y 2 +xy 3 +y 4 ), the chain has two
model’s actual reasons for deciding; what we observe here is             steps: a routing reduction into the polynomial route, rendered
the decision itself. Every stage of the system can be re-verified        as the two tactics norm num1 and ring. For the number-theory
by a third party. The review program is version-frozen and               evaluation (29 × 31 + 37 − 41) mod 4 = 3, the chain has the
carries a checksum; accepted samples are re-reviewed through             same two-step shape into the evaluation route, rendered as a
an independent path (stratified sampling, zero discrepancies);           single line of norm num. Both problems certify. Full records
reverse-constructed corrupted proofs are all rejected (Section           of all four examples (per-step decision distributions, engine
III-E); training configurations, batch order, and random seeds           states, and certificates) ship with the code.
are registered together with the checksums of all reading files,
so any reading can be recomputed from the released material;                               IV. E XPERIMENTAL S ETUP
proof compilation is deterministic and fully replayable from
the operator chain (2,399/2,399 byte-identical on the corpus,            A. Pre-Control on the Carrier of Latent Thinking
Section III-D); the isolation check between corpus and test                 A precondition of this architecture concerns the form the
suite is a two-level mechanical scan whose program ships                 carrier of thinking takes inside the latent space: if the inter-
with the code. Auditability also makes controlled intervention           mediate states of multi-step reasoning are passed between the
possible. The factorial experiment of Section VIII directly              model’s hidden states as continuous vectors, can later steps
edits the state quantity inside the decision frame and retrains          read them out reliably? Latent-carrier designs of this kind have
comparison configurations, thereby attributing a 74-problem              recently been explored as alternatives to token-level reasoning
change in pass rate to a single variable; frame-level interven-          chains [28], [29]; whether the carrier survives across steps
tion of this kind presupposes a structured process. We will              is a property to be tested rather than assumed. A controlled
release the code, corpus, review programs, and per-problem               experiment under a unified protocol (same backbone, same
records (including per-step decision distributions), so that all         number of training steps, two random seeds) answers no for
experimental readings can be re-checked outside the system.              continuous feedback. As Table IV shows, pure hidden-state
                                                                         feedback reaches a readout accuracy of only 0.01 to 0.06
                                                                         beyond two hops; the continuous-register scheme averages
H. Worked Examples: From Problem State to Certified Proof                0.0246 over all depths; value-format discretization manages
   This section presents the input, the decision chain, and the          only 10% to 15%. The only configuration that reads out fully
output of the system on four real problems. Two come from                at a depth of 16 hops is key-token discretization combined with
the main suite (the configuration of Section VIII) and two               curriculum training, which scores 1.0000 at every depth k = 1
from the public-library final exam (Section X); the chains and           to 16 on formal evaluation. Neither ingredient suffices alone:
proof texts are the system’s actual records on disk, unedited.           curriculum by itself reads out at roughly zero, and key format
The sum-of-squares example shows the residual mechanism                  alone needs roughly three to four times the training volume to
in full. The problem is the multivariate polynomial inequality           bootstrap. The external-judge reference group (0.973 to 0.984)
v 2 + 2u2 + 2w2 + z 2 − 2yv + y 2 + 2x2 + 4v − 12u − 4w −                shows that the discrimination step itself is feasible; the failure
4z − 4y − 8x + 57 ≥ −7. The model’s chain has six steps:                 lies in the carrier, not the judge. The comparison readings of
cross-block absorption handles the square containing the cross           Table IV come from the discretization line of latent chain-
term −2yv; four single-variable block absorptions remove four            of-thought, whose main configuration (v15 in our notation)
square terms in succession; and the closing step classifies              is decomposed in Table V. That line uses a dynamic multi-
the final residual. Table III lists, step by step, the square            hop task as its carrier: given one member of an operator
component removed at each step and the proof line rendered               family (orthogonal, permutation, or cyclic matrix families), the
from it. The final residual is 28, of the other class per (5); the       model applies it to a latent state step by step and reads out
closing accordingly emits a constant-nonnegativity proof line            the terminal state after T steps. The depth curriculum of v15
and then closes all goals with a nonlinear-arithmetic tactic.            advances as a ladder: the depth measured by the gate probe
The proof was certified by the review program. The nested-               rises monotonically from 1 to 16, with all fifteen openings
induction example is a closed-form problem: the proposition              falling between training steps 11,000 and 17,500 (Fig. A2),
is ∀n : N, f n = 4 − 12n + n2 + 12n3 + 4n4 , with f                      and the opening of the depth gate was independently re-
defined by a difference recurrence. The model’s five-step chain          verified. Depth sampling of training episodes stayed shallower
solves the inner difference equation for the inner closed form,          than the gate depth throughout this window (the vast majority
folds it into the outer increment, solves the outer difference           of episodes remain at T = 1), so the ladder curve measures the
equation, runs a telescoping check confirming that the closed            trajectory of the gate, not the training distribution itself. After
form matches the increment pointwise (Table II), and closes              the ladder was fully traversed from T = 1 to 16, the discrete
with the closed form together with its class. The rendered               decision carrier of all subsequent experiments in this paper was

                                                                     7
Fig. 2. Low-dimensional projection of decision-frame hidden states (218 problems, 1,552 frames, UMAP [27]). The states organize by problem family
(nearest-neighbor purity 0.999 against a random baseline of 0.659); frames of the same problem advance along the chain (adjacent-frame cosine similarity
0.607 versus 0.154 for random frame pairs); the projected vectors are frame-for-frame identical to the hidden states consumed by the output heads (maximum
deviation 0). Thinking rides on a discrete decision sequence whose internal state can be read out directly, without relying on the model’s self-report.

                                                  TABLE III
   STEP-BY-STEP COMPUTATION OF A SUM-OF-SQUARES PROBLEM (ACTUAL RECORD ON DISK). EACH STEP REMOVES ONE
 SQUARE COMPONENT PER (4); EVERY NUMBER IN THE RENDERED LINE COMES FROM ENGINE COMPUTATION; THE CLOSING
                            ROW GIVES THE FINAL RESIDUAL 28 (OTHER CLASS, PER (5)).

            Step          Operator            Component removed, m ℓ2 per (4)                Rendered proof line (engine-computed values)
              1    sos cross (cross block)           1 (−v + y − 2)2                 have h1 : (0:Q) ≤ 1 * (- v + y - 2) ˆ 2 := by
                                                                                                       positivity
              2          sos block                      2 (w − 1)2                      have h2 : (0:Q) ≤ 2 * (w - 1) ˆ 2 := by
                                                                                                       positivity
              3          sos block                      2 (u − 3)2                      have h3 : (0:Q) ≤ 2 * (u - 3) ˆ 2 := by
                                                                                                       positivity
              4          sos block                      1 (z − 2)2                      have h4 : (0:Q) ≤ 1 * (z - 2) ˆ 2 := by
                                                                                                       positivity
              5          sos block                      2 (x − 2)2                      have h5 : (0:Q) ≤ 2 * (x - 2) ˆ 2 := by
                                                                                                       positivity
              6    sos tail other (closing)              ρ = 28                       have hrho : (0:Q) ≤ (28:Q) := by norm_num;
                                                                                       nlinarith only [h1, h2, h3, h4, h5, hrho]




in place; the comparison readings in the table share the unified                    (chain length 5), the lemma-tower family (chain length 9),
protocol of Table IV. This set of comparisons establishes                           and the sum-of-squares decomposition family (chain length 5
the necessary condition behind all subsequent design: multi-                        to 7); the overall chain-length distribution is 1,136 rows at 5
step state in latent space must be pinned to discrete symbols                       steps, 330 at 6, 133 at 7, and 800 at 9, averaging 6.58 steps.
(keys in token format) to survive across steps. The operator                        The deep-chain corpus is designed so that multi-step planning
vocabulary, the engine state frame, and the compiler rendering                      genuinely occurs during training: the average chain of the
of Sections III-A to III-D all presuppose it. A bandwidth                           early shallow corpus is only about 1.77 steps, too short to
estimate (about 6 bits per step) together with the measured                         support a study of multi-step behavior. All data carry per-step
depth of 16 hops indicates that the carrier does not bottleneck                     ground-truth engine states (15,791/15,791 steps nonzero) and
the task depths of this paper.                                                      position annotations of the content integers of reference proofs
                                                                                    (100% coverage); the latter serve the error analysis of Section
B. Training Corpus                                                                  VI. Isolation between corpus and test suites uses a two-
                                                                                    level check: identifier level (exact matching of problem names
   The training corpus has two layers. The shallow corpus
                                                                                    and statement text, required to yield zero hits) and semantic
contains 9,366 proposition-proof pairs with chains of one to
                                                                                    level (an identity check after algebraic normalization, plus
three steps, covering the early problem families. The deep
                                                                                    a statement-text four-gram overlap check; rows with overlap
corpus contains 2,399 proposition-proof rows built by three
                                                                                    of 0.9 or above are removed from the training set). This
deep-chain generator families: the nested-induction family

                                                                                8
                              TABLE IV                                                                     TABLE V
   C ARRIER COMPARISON FOR MULTI - HOP READOUT IN LATENT SPACE                  M ECHANISM DECOMPOSITION OF THE DISCRETIZATION EXPERIMENT
( UNIFIED PROTOCOL : SAME S MOL LM2-135M BACKBONE , SAME NUMBER             ( V 15 CONFIGURATION ). T HE DISCRETIZATION OF KEYS AND VALUES , THE
   OF TRAINING STEPS , TWO RANDOM SEEDS ; READINGS ARE READOUT                 FEEDBACK CHANNEL , AND THE DEPTH PROTOCOL ARE INDEPENDENT
                             ACCURACY ).                                    AND MUTUALLY SUPPORTING ; THE CONTROL READINGS COME FROM ARM
                                                                             COMPARISONS UNDER THE UNIFIED PROTOCOL ( SAME SOURCE AS TABLE

    Carrier configuration       Readout accuracy          Verdict                                             IV).

      Pure hidden-state        0.01–0.06 beyond two       Failure              Mechanism             Treatment in v15              Related control
    feedback (continuous      hops (tail mean 0.0223)                          component                                              readings
           vectors)
        Value-format                0.10–0.15             Failure                 Task        Dynamic multi-hop: one operator              —
        discretization                                                           carrier    family (orthogonal, permutation, or
     (ground-truth keys)                                                                     cyclic matrices) acts on the latent
   Curriculum training (no           About 0              Failure                          state step by step; the terminal state
         key format)                                                                               is read out after T steps
   Key-token discretization   Slow bootstrap; needs       Partial              Value dis-    Codebook quantization: the latent Continuous-vector
       (no curriculum)          roughly 3–4× the                               cretization state snaps to the nearest codeword;        feedback:
                                 training volume                                             readout and feedback both use the 0.01–0.06 beyond
    Continuous registers      Mean 0.0246 over all        Failure                                   dequantized codeword               two hops
                                      depths                                    Key dis-              Keys represented in         Values discretized
        External judge             0.973–0.984        Judge feasible;          cretization        token-vocabulary format            without keys:
   references (markov/gru)                              no carrier                                                                     0.10–0.15
                                                        specificity              Depth     Curriculum ladder: training depth T        Key format
   Key-token discretization 1.0000 at every depth k = Full readout at           protocol        rises stepwise from 1 to 16,            without
    + curriculum training             1–16               16 hops                           advancing after each level passes the      curriculum:
                                                                                                         readout gate             roughly 3–4× the
                                                                                                                                   training volume
                                                                                 Depth      Ladder fully traversed from T = 1         Continuous
                                                                                outcome     to 16; gate openings independently      registers: mean
                                                                                                          re-verified                    0.0246

procedure once detected content-level overlaps when several
corpus versions were merged and removed them all; the final                 D. Configuration Overview
training set and test sets share zero problems.                               The main configurations reported in this paper share the
                                                                            same backbone, training hyperparameters, batch order, and
                                                                            random seed; they differ only in the variables listed in Table
                                                                            VI: how proof text is produced, the chain-end loss weight,
                                                                            and the state timing of the decision frame. Experiments 1 to
                                                                            3 isolate one factor at a time: Experiment 1 examines direct
                                                                            generation; Experiment 2 adds structured numeric output on
                                                                            top of it; Experiment 3 switches proof text to the compiler.
                                                                            Experiment 4 is a 2 × 2 factorial design. Experiment 5 is the
                                                                            external-model comparison.
C. Test Suite
                                                                            E. Review Validity
                                                                              The main proportional readings carry Wilson 95% confi-
                                                                            dence intervals [30], where n is the number of graded problems
   The deep-chain test suite is produced from the generator                 and z = 1.96:
candidate pool by a triple screen: unsolvable by the rule-based                                           p
                                                                                        p̂ + z 2 /(2n) ± z p̂(1 − p̂)/n + z 2 /(4n2 )
solver working from the statement text (so pattern matching                   CI(p̂) =                                                 (13)
                                                                                                          1 + z 2 /n
cannot answer it), in possession of a reference proof, and
passing the overlap check against the training corpus. Of 338               The interval is solved from the√ pivot of ap
                                                                                                                       binomial proportion:
candidates, 218 survive overlap filtering (the four text-domain             by the central limit theorem, n (p̂−p)/ p(1 − p) converges
overlap counts are 7, 120, 217, and 326 problems; the stricter              in distribution to the standard normal, pand the interval end-
count was adopted to avoid potential contamination, removing                points solve the inequality |p̂ − p| ≤ z p(1 − p)/n. Squaring
120 problems): 13 nested-induction problems, 24 lemma-tower                 both sides and rearranging gives the quadratic inequality in p
problems, and 181 sum-of-squares problems. A shallow-chain
                                                                                      (1 + z 2 /n) p2 − 2 (p̂ + z 2 /(2n)) p + p̂2 ≤ 0;
suite (1,083 problems, chains of one to three steps) serves for
evaluating early configurations and as the baseline reference               taking the two roots by the quadratic formula, with (p̂ +
of this paper. Both zero-capability controls score zero on the              z 2 /(2n))2 − (1 + z 2 /n)p̂2 = z 2 p̂(1 − p̂)/n + z 4 /(4n2 ) under
shallow suite: the untuned backbone and the rule-based solver               the radical, yields the endpoint expression of (13). Beyond the
each have 1,080 applicable problems and fail all of them (3                 dual-protocol recheck of Section III-E, the following discipline
inapplicable problems excluded), showing that certified scores              applies to all readings. Every score states the number of graded
cannot be obtained by guessing or pattern matching.                         problems and the total; unexecuted reviews are never counted

                                                                        9
                                                             TABLE VI
 M AIN EXPERIMENTAL CONFIGURATIONS . E XPERIMENTS 1 TO 4 SHARE THE BACKBONE (S MOL LM2-135M), TRAINING HYPERPARAMETERS , BATCH
ORDER , AND RANDOM SEED ; THE FOUR CONFIGURATIONS OF E XPERIMENT 4 DIFFER ONLY IN THE LISTED VARIABLES . E XPERIMENT 5 IS AN EXTERNAL
                                     COMPARISON MODEL AND IS NOT SUBJECT TO THESE CONTROLS .


                ID            Proof-text production         Chain-end loss          Decision-frame state                     Purpose
                                                               weight
              Exp. 1            Model-generated                  1.0            Original (lagged by one step)        Direct-generation baseline
              Exp. 2     Model-generated + value slotting        1.0                       Original               Isolates the numeric-generation
                                                                                                                                mode
              Exp. 3           Compiler-generated                1.0                      Original                  Isolates the text-production
                                                                                                                                mode
             Exp. 4A           Compiler-generated                1.0                      Original                Factorial baseline (same as Exp.
                                                                                                                                  3)
             Exp. 4B           Compiler-generated                5.0                      Original                    Factorial: loss weighting
             Exp. 4C           Compiler-generated                5.0               Shifted to current state         Factorial: weighting + state
             Exp. 4D           Compiler-generated                1.0               Shifted to current state             Factorial: state (final
                                                                                                                            configuration)
              Exp. 5     DeepSeek-Prover-V1.5-RL direct          —                           —                            External control
                                  generation




as zero; stratified recheck samples below the planned size are                most consequential reading of this paper. Experiment 1 evalu-
marked as such. Wherever rendering accuracy serves as the                     ates direct generation: the model plans the solution chain step
metric, a zero-parameter mode baseline (outputting the most                   by step, and a text-generation head writes the complete proof;
frequent answer in the training set) is reported alongside: on                certified passes number 0/218. The zero does not come from
the shallow-chain suite the final configuration reaches 0.9755                failed chain decisions: the first-operator hit rate is 218/218
against 0.6276 for the baseline, a net gain of 34.8 percentage                and the exact whole-chain hit rate is 117/218 (53.7%), with
points, which rules out inflation from templated data. The zero               the nested-induction family 13/13 and the lemma-tower family
scores of the two zero-capability controls (untuned backbone                  24/24 all correct. Meanwhile, the model’s token accuracy on a
and rule-based solver), together with reverse verification (all               held-out set from the training distribution is 0.9637, in sharp
corrupted proofs rejected), show that the review program                      contrast to the zero pass rate. Decomposing the generated text
rejects wrong proofs and passes reference proofs.                             identifies the cause of failure. Counting the content integers
                                                                              (coefficients, exponents, constants) of each proof individually:
      V. BASELINES AND N EGATIVE R ESULTS IN THE                              on the training-distribution control set (20 problems), the per-
                S HALLOW-C HAIN E RA                                          digit accuracy of a single content integer is about 0.79, and
   With the curriculum corpus in place, the shallow-chain                     each proof carries about 14.9 content integers on average.
suite (1,083 problems, chains of one to three steps) produced                 Writing the content integers of a proof as X1 , . . . , Xk , with
the first baseline: the formal configuration certifies 180/1083               digit i written correctly with independent probability pi, proof
(16.6%), while the two zero-capability controls, the untuned                  validity requires every digit to be correct:
backbone and the rule-based solver, each have 1,080 applicable                                                           k
problems and score zero, so certified scores cannot come                                                        Pass =
                                                                                                                         Y
                                                                                                                               pi                    (14)
from guessing or pattern matching. Rendering accuracy is                                                                 i=1
0.9755 against 0.6276 for the zero-parameter mode baseline,
a net gain of 34.8 percentage points; inflation from templated                When all digits share the accuracy p, the expression equals pk ;
data is excluded. The first mechanism-level ablation was                      taking p as an upper bound on every digit gives the power-law
run in the same period: adding step-level attention to the                    bound:
chain planner (a first-generation implementation) cost a net                                                     Pass ≤ pk                           (15)
62 problems over the full suite (118/1083 against 180/1083,
same suite, seed, and batch order). This negative result points               Proposition 1 (product law and power-law bound): suppose a
in the same direction as the state-injection ablation of Section              proof contains k content integers, digit i is written correctly
IX: the bottleneck does not lie in the expressive power of                    with independent probability pi, and certification requires all
the decision mechanism. Shallow-chain tasks are solvable,                     digits to be correct; then the pass rate is given by (14), and if
but chains of one to three steps cannot examine multi-step                    no digit exceeds accuracy p, the bound of (15) holds. Proof:
behavior. The deep-chain corpus and the 218-problem deep-                     the certification event is the intersection of the k events that
chain exam (Section IV-B) then moved the examination ground                   digit i is correct; by independence, its probability is the product
to a qualitative change; the narrative of the next section starts             of the per-digit probabilities, which is (14). If every digit’s
from the first deep-chain exam.                                               accuracy is at most p, each factor of the product is at most p,
                                                                              so the product is at most pk , which is (15).           ■ Corollary
  VI. C OLLAPSE : T HE E RROR -P RODUCT S TRUCTURE OF                         (load correction): let S ⊆ {1, . . . , k} be the set of load-bearing
          D IRECT L ONG -P ROOF G ENERATION                                   integers determined mechanically by the controlled-corruption
  The first deep-chain exam, run once the deep-chain corpus                   experiment; changing the value of an integer outside S does
and the 218-problem suite were in place, produced the single                  not change the certification outcome. The product therefore

                                                                         10
                                       Q
only needs its factors in S, Pass = i∈S pi ; when all load-               in one configuration the slot ground truth is supplied by the
bearing digits share the accuracy p, this is (17). Substituting           execution engine. The results: slots with engine supply pass
p = 0.7919 and k = 14.9 gives a pass rate of about 0.031,                 1/218, slots filled by the model pass 0/218, and the original
i.e., less than one expected pass in 20 problems; the measured            baseline 0/218. After slotting, the model’s fill-in accuracy
one pass matches the prediction (Fig. 3(a)). On the test suite,           reaches 94.5% (39.6% of rows fully correct), yet whole-
the per-digit accuracy of the inequality family is only 0.0911;           problem certification stays near zero; the gap between high
the same computation puts the pass rate near zero, consistent             fill-in accuracy and failure under autoregression comes from
with the measured 0/181. In other words, the validity of a                the cumulative effect of earlier errors on later conditions in
long proof is the conjunction of all its content elements,                autoregressive generation. The result shows that local improve-
and when per-element accuracy is insufficient the pass rate               ments in numeric generation (raising per-element accuracy)
falls exponentially with the element count; token-level metrics           cannot offset the exponential loss of the conjunctive structure;
do not reflect this structure and therefore do not constitute             the free-generation stage itself must be removed.
a valid performance measure in this setting. Enlarging the
thinking budget does not help the structure either: in the budget           VII. R EVERSAL : C OMPILER -G ENERATED P ROOF T EXT
comparison on a synthetic task, doubling the multi-step budget
                                                                             The contrast between 53.7% chain navigation and 0/218
left accuracy flat across levels (about 0.974), showing that the
                                                                          certified direct generation pinpoints the text-generation stage.
bottleneck is the conjunctive structure of the output channel,
                                                                          Experiment 3 changes the production of proof text to the
not the computational budget. The product structure admits a
                                                                          compiler (Section III-D); the model outputs only the operator
direct test that does not depend on the model. For the annotated
                                                                          chain, and the text loss leaves the training objective. On
content-integer positions in the reference-proof pool (218 test
                                                                          the same suite, the certified pass rate rises from 1/218 to
problems plus 2,399 corpus rows, 2,617 proofs in total), each
                                                                          117/218 (53.7%). Moreover, the chains of the existing model
integer is independently replaced, with probability 1 − p, by a
                                                                          (produced by the Experiment 2 configuration), when compiled,
random value of the same magnitude (excluding the original
                                                                          certify 121/218, matching the exact hit rate of those chains;
value; the sign is kept), and the corrupted proofs are graded
                                                                          the retrained pure-planning model gives 117/218, within four
by the same review program. The design crosses six values
                                                                          problems of the 121/218 obtained from the existing chains,
of p from 0.99 to 0.50 with bins of the per-problem content-
                                                                          essentially the same. These readings show that once free-text
integer count (bin means 10.4, 15.1, 20.0, and 30.0), for 3,570
                                                                          generation is removed, the certified pass rate of the system
sampling runs and 1,680 corrupted units graded (0 review
                                                                          is determined entirely by chain-decision quality and the text
anomalies). The theoretical mean weights the actual sampling
                                                                          stage no longer costs anything; the same chain set under the
structure of the per-problem integer counts and the six values
                                                                          two text-production modes yields 1/218 versus 121/218, which
of p:
                                    N                                     directly quantifies the cost of the free-generation stage. Given
                                 1 X kj                                   that compilation is a deterministic map, verified twice over
                        T (p) =        p                     (16)
                                N j=1                                     (byte-identical reproduction on 2,399 corpus rows and 218/218
                                                                          on reference chains), the certified pass rate of the system
The measured pass rate over the full pool is 0.558, slightly
                                                                          equals the correctness rate of the chains the model produces:
above the theoretical value of 0.530, a relative excess of
about 5% (Fig. 3(b)). The source of the deviation can be                                    Pass = P (chain correct),                (18)
located slot by slot: no corrupted unit at coefficient or exponent
positions survives (0/432), and all 1,164 corrupted units of               where chain correctness is measured by exact whole-chain
the nested-induction and lemma-tower families are rejected                match. The equality removes the text stage from the perfor-
by review; every instance of tolerance occurs at multiplier and           mance variables and leaves chain-decision quality as the only
linear-form constant positions of the sum-of-squares family. In           performance variable of the system: the 117/218 of Experiment
that family’s proofs the multiplier appears only as a positive            3 equals the exact chain hit rate, and the 121/218 of the
scalar, which the nonlinear-arithmetic tactic can absorb, so              Experiment 2 chains under compilation matches their hit rate
replacing the number leaves the proof valid (25/25 single-slot            as well. The product structure of Section VI is precisely the
corruptions survive; tolerance occurs only at such positions              form that the right-hand side of this equality takes under the
of this family and is a property of the proof template).                  free-text paradigm.
Accordingly, write S ⊆ {1, . . . , k} for the set of load-bearing
integers (determined by the proof template, |S| ≤ k); a more                   VIII. ATTRIBUTION : A FACTORIAL A NALYSIS OF
precise statement of the pass rate is:                                               D ECISION -T IME S TATE I NFORMATION
                                                                             Compilation exposes all remaining errors at the final step of
                          Pass ≈ p|S|                        (17)
                                                                          the chain. Localizing the 101 errors of Experiment 3 problem
The controlled-corruption experiment also provides a mechan-              by problem and step by step: all 101 first errors occur at the
ical way to measure the load-bearing status of each digit                 last step of the chain, with no mid-chain errors, no premature
position. On this baseline, Experiment 2 changes the numeric              termination, and no budget exhaustion; 55 of the erroneous
output to structured slots: the content-integer positions of the          steps carry predicted probability 0.9 or above, i.e., the model
proof template are predicted by the model in a discrete value             is highly confident in its wrong judgments. Combined with
space instead of being generated freely by the text head, and             (5), the final class is fully determined by the residual value;

                                                                     11
Fig. 3. Quantitative tests of Law 1. (a) The pass rate of direct generation decays as a power law in the number k of content integers (p = 0.79), with measured
points overlaid (control 1/20, deep-chain suite 0/218, comparison model 18/218). (b) Measured pass rate under controlled integer corruption (0.558) against
the independent-assumption theory (0.530), bin by bin.



the residual needed for the verdict is already available after the                  0.876. The difference between the two configurations, 218 ×
execution of step T −1, whereas the original decision frame                         (0.876 − 0.537) = 74 problems, matches the measurement, so
carries the value from before the previous step, a one-step lag.                    the gain comes from improved conditional quality at the final
Experiment 4 tests this hypothesis with a 2×2 factorial design:                     step; prefix quality is not a loss term in either configuration.
factor one is whether the state frame replaces the lagged value
with the current one (the state shift below); factor two is                                                     TABLE VII
the cross-entropy loss weight at the chain’s final step (1.0 or                     FACTORIAL RESULTS ( N = 218). T HE SIMPLE EFFECT OF THE STATE SHIFT
                                                                                       IS +74 PROBLEMS ; THE SIMPLE EFFECT OF LOSS WEIGHTING IS −7
5.0). The four configurations are otherwise identical (same                             ( AVERAGE MAIN EFFECTS +68 AND −13), AND WEIGHTING STILL
batch order, same random seed). Table VII reports the results.                             LOWERS THE PASS RATE ON TOP OF THE SHIFT (191 TO 172).
Mathematically, the state shift augments the conditioning of
(8):                                                                                   Configuration   State    End-step    Certified passes (n    ∆ vs.
                                                     (t−1)                                            shift     weight           = 218)          baseline
             (ot , at ) = fθ s, h1 , . . . , ht−1 , Rout     (19)
                                                                                      Baseline (Exp.    No         1.0             117               —
       (t−1)                                                                                3)
where Rout is the residual after the execution of step t−1                              Weighted        No         5.0             110              −7
per (4), computed before the decision and placed into the state                        Weighted +       Yes        5.0             172              +55
                             (T −1)                                                        shift
frame; for the final step, Rout     is exactly the final residual
                                                                                       Shift (final     Yes        1.0             191              +74
needed for the verdict. Separating final-step quality from prefix                     configuration)
quality yields a two-factor decomposition of the pass rate.
Proposition 2 (final-step conditional decomposition): let B be
                                                                                       These results show that adding information does far more
the problem set whose first T −1 steps are all correct, and C
                                                                                    than reallocating loss: correcting the state timing alone lifts
the set whose whole chain is correct; then
                                                                                    the pass rate from 53.7% to 87.6%, whereas up-weighting
                          Pass = AT −1 · qT ,                           (20)        the loss at the site where errors concentrate is negative under
                                                                                    both states and raises confidently wrong decisions from 55
where AT −1 = P(B) is the prefix accuracy and qT = P(C —                            to 69. Weighting adds no decision-relevant information; it
B) the conditional accuracy of the final step. Proof: a fully                       only shifts the tendency of the class prior. The migration
correct chain implies a correct prefix, i.e., C ⊆ B, so P (C) =                     of error composition tracks the completeness of state in-
P (B) · P (C | B), which is the claim.                            ■                 formation (Figs. 4(a) and 4(b)): the final configuration’s 27
On Experiment 3 the decomposition takes concrete values: the                        errors all sit at the final step and all are confusions between
101 first errors all sit at step T, so the prefix accuracy is (117+                 the square class and the other class (zero-residual verdicts
101)/218 = 1.000 and the conditional final-step accuracy is                         are all correct, 31/31; zero-class-related confusions fall from
qT = 117/218 = 0.537; after the state shift it is 191/218 =                         36 to 0; confidently wrong decisions fall from 55 to 12).

                                                                               12
The zero-residual case can be read directly off the residual              outputs almost all terminate in unsolved goals; generation-
value, while the square verdict requires the model to look up             capacity triggers account for 77/218 and 177/500, and the
one of six squares, a representation-learning problem under               problems that did not hit the cap (141 and 323) also all fail,
information already in hand rather than missing information.              so the zeros cannot be attributed to the generation budget.
Per-step decision entropy quantifies this structure: early-chain          If the zeros simply reflected a domain mismatch, the model
decisions are near-deterministic (entropy below 0.001 nats)               should do clearly better on the stratified suite close to its own
and real uncertainty concentrates in the last three steps; failing        problem sources; the measurement says otherwise. The preset
problems have seven times the entropy of passing problems                 failure decomposition (correlation of content-integer count
at the first divergent step (0.191 versus 0.027 nats), while the          with correctness) degenerates because both arms are constant
top-1 probability at that step still reaches 0.918 (Fig. 4(c)), so        at zero, and yields no readable quantity. This configuration
measurable extra uncertainty and high-confidence error hold               generates 5,255 tokens per problem on average (3,919 of
at once. Two further pieces of parameter-side evidence appear             them in the thinking segment), takes 286 s, and peaks at
in the appendix: the parameter geometry of the operator head              11,649 MiB; both generation volume and wall-clock are an
separates backbone operators from added operators rather than             order of magnitude above V1.5-RL. The readings of the two
clustering by problem family (Fig. A3); the two-dimensional               generations on the same main suite (18/218 and 0/218) with
loss cross-section at the training convergence point is a wide,           consistent interruption patterns show that the iteration did not
shallow basin, with corner loss 15.2 times the convergence-               change the fate of the direct-generation paradigm on this class
point loss (Fig. A4); complete versions of the first-error                of propositions. All verdicts came from the version-frozen
probability and the along-chain entropy appear in Figs. A5                review program, with matching checksums before and after
and A6.                                                                   grading. Both ratios can be explained by the cost structures
                                                                          at the two ends. Per problem, the number of model forward
                                                                          passes and of engine calls each equals the number of decision
      IX. C ROSS -M ODEL E XAMINATION AND S CALE
                                                                          steps T; the text is compiled from templates and never enters
                    D ECOMPOSITION
                                                                          the generation sampling loop, so the per-problem cost of this
   Once the two laws closed on the same exam, two questions               architecture is
followed: is the collapse specific to small models, and what are
the separate contributions of the architectural change and of                           Csc = T (cfwd + cexec ) + ccompile ,          (21)
model scale? Experiment 5 evaluates DeepSeek-Prover-V1.5-
RL [3] (7B parameters, int8 quantization, greedy decoding,
zero-shot prompting, single generation) on the same 218-                  where cfwd is the cost of one forward pass, cexec the cost of one
problem suite. Certified passes: 18/218 (8.3%); 177 outputs               engine execution, and ccompile the cost of expanding the whole
contain an unsolved goal (sorry), and 23 are rejected by the              chain from templates; all three are deterministic and do not
review program. By family: nested induction 0/13, lemma                   fluctuate with sampling. The direct-generation paradigm must
tower 0/24, and every pass belongs to the sum-of-squares                  generate every content integer digit by digit; its per-problem
family (18/181). The final configuration of this paper reaches            cost is
191/218 on the same suite (Fig. 5(a)). The distribution of
decision steps per problem appears in Fig. A7 (mean 6.12,                                        Cdir = Ngen ctok ,                   (22)
chains of 5 to 9 steps; the two synthetic families have rigid
chain lengths, and in the final configuration every remaining             where ctok is the cost of one generated token, and the
failure sits in the sum-of-squares family, Section VIII). This            measured mean of Ngen is 168.0 (V1.5-RL) and 5,254.6 (V2,
comparison must be read with the interface difference in view:            including the thinking segment). The two cost expressions
the comparison model has no execution engine or compiler and              count different things: our corpus chains run 5 to 9 steps
must generate the complete proof as free text, so its failure             (mean 6.58), while the comparison models average 168.0 and
mode matches the direct-generation experiments of Section                 5,254.6 generated tokens; the measured ratios of Table VIII
VI; the suite demands more correctly written content integers             agree with this difference in counts (Fig. 5(b)). Injecting the
than the model can produce. We therefore read this comparison             same step-by-step state information as our system into the
as evidence on the structure of the output channel, not as                external comparison model gives pass rates of 18, 14, and 13
a ranking of the two models’ reasoning ability. Table VIII                out of 218, no improvement. A three-configuration comparison
gives the resource comparison. A cross-generation recheck                 gives a preliminary separation of the effect of scale alone: the
of the comparison uses a bidirectional dual suite: DeepSeek-              inherited-head 135M, the new-head 1B, and the same-loadout
Prover-V2-7B [31] (int4 quantization, greedy decoding, single             new-head 135M reach 191, 170, and 180 out of 218; loadout
generation capped at 8,192 tokens) answers both the main                  migration and backbone scale each contribute about half the
suite of this paper (218 problems) and a stratified suite of 500          difference (−11 and −10 problems), and the two factors act on
rows drawn from the public library Lean-Workbook [8], with                disjoint problem sets. Together with the attention ablation of
problem sources and style close to that model family, so that             the shallow-chain era (Section V), these two groups of results
a favorable skew of the exam cannot explain the comparison                say: the collapse is not limited to small models, mechanism
result. Both suites yield zero certified passes (0/218 and 0/500;         upgrades do not move the pass rate, and information visibility
Wilson 95% upper bounds 0.017 and 0.008), and failing                     is the decisive variable.

                                                                     13
Fig. 4. Composition, confidence, and uncertainty of final-step errors. (a) All 101 baseline first errors sit at the chain’s final step, and the 27 remaining errors
of the final configuration are all table-lookup confusions between the square class and the other class, with all zero-residual verdicts correct (31/31). (b)
Distributions of top-1 probability at the first erroneous decision step: the two configurations’ shapes nearly coincide, and confidently wrong decisions fall from
55 to 12; the state shift changes the number of errors, not their confidence. (c) Decision entropy along the chain: early steps are near-deterministic (below
0.001 nats), real uncertainty concentrates in the last three steps, and failing problems have seven times the entropy of passing problems at the first divergent
step (0.191 versus 0.027 nats).

                                                             TABLE VIII
R ESOURCE COMPARISON ( N = 218). V1.5-RL AND V2 DENOTE D EEP S EEK -P ROVER -V1.5-RL AND D EEP S EEK -P ROVER -V2-7B; THE RATIO COLUMN IS
   EACH GENERATION AGAINST THIS ARCHITECTURE ; THE V2 COLUMN IS UNDER INT 4 QUANTIZATION WITH SINGLE GENERATION CAPPED AT 8,192
TOKENS . T HIS ARCHITECTURE PRODUCES NO NATURAL - LANGUAGE THINKING TEXT; 6.12 IS THE MEAN NUMBER OF DECISION ACTIONS PER PROBLEM .


                 Metric           This architecture (135M)           V1.5-RL (7B)                           V2-7B (int4)                 Ratio (V1.5 / V2)
             Certified passes         191/218 (87.6%)                18/218 (8.3%)                             0/218                          —
           Generated tokens per     6.12 (decision steps)     168.0 (output); 156.6 (input)    5254.6 (output, incl. 3918.8 thinking);   27.5× / 858×
                 problem                                                                                   217.6 (input)
             Wall-clock per                0.53 s                       19.88 s                               285.9 s                    37.5× / 539×
                 problem
             Peak inference              833 MiB                       8567 MiB                             11,649 MiB                   10.3× / 14.0×
                 memory




    X. D OMAIN E XTENSION : VALIDATION ON A P UBLIC                                    exist for 3,536 rows, which enter review, and 2,132 certify
                  P ROBLEM L IBRARY                                                    (60.29%, Wilson 95% interval 58.67 to 61.89); the reference
                                                                                       arm of the existing operator families stands at 73.04%, and
   All experiments so far ran inside the proposition domain                            the type-tree chains of the nine extension families at 44.07%.
constructed by this paper and on the 218-problem main suite.                           Rows outside the admissible domain are listed separately and
To examine whether the recipe transfers and what the admis-                            do not enter the score. This coverage boundary is set by
sible domain actually covers, we extend the operator library                           mechanical checks: which problems lie inside the capability
and the corpus to the public library Lean-Workbook (139,826                            domain, which do not, and why, are themselves outputs the
problems) [8]. The extension follows the same discipline as                            system can produce. Part of the chains behind these whole-
the main suite: training data are synthesized by problem-                              library readings comes from the fixture and the type trees. To
family generalization, and every library problem is checked                            isolate the model’s independent contribution, we run a model-
for leakage against problem name, statement text, and constant                         independent chain-walking exam on 1,535 certifiable rows
vector; the checking program itself is validated by injection                          of the nine extension families, none of which intersects the
experiments; the exams always use one deterministic renderer,                          training corpus. The model decides autonomously throughout,
and every problem is graded by the same frozen review                                  including the terminator; on the 623 rows whose chains are
program. On Lean-Workbook, 7,448 rows shipped with the                                 renderable, 281 certify (45.10%, Wilson 41.24 to 49.03), the
library cannot be parsed, matching the exclusion count in the                          same level as the type-tree chains at 44.07% (Fig. 5(d)). Of
library’s documentation; they do not enter the denominator,                            these, 331 rows match the fixture’s reference chains exactly,
and the remaining 132,378 rows form the full denominator.                              and the rendered text of these rows matches the fixture
Structural triage produces three tiers: 48,106 rows admissible                         rendering line for line by checksum (331/331), ruling out
under our operator system; 84,267 rows parseable but without                           systematic drift in the rendering channel. The deep-exam
a matching problem family; and 5 rows failing to parse (Fig.                           reading of 191/218 (87.6%) holds under the same-distribution
5(c)). Within the admissible domain, fixture-renderable chains

                                                                                  14
Fig. 5. Main results. (a) Certified pass-rate ladder of the main configurations: 0/218 (direct generation), 1/218 (slotting), 117/218 (compilation), 191/218
(state shift), with the shallow-chain reference 180/1083 and the comparison model 18/218 marked. (b) Resource comparison (log axis): generated tokens per
problem (6.12 versus 168.0), wall-clock per problem (0.53 s versus 19.88 s), and peak memory (833 MiB versus 8,567 MiB); the comparison model runs one
to two orders of magnitude higher on all three. (c) The three-tier triage funnel over the full Lean-Workbook library (132,378 → 48,106 → 3,536, with 2,132
certified). (d) End-to-end comparison of model-independent chain walking against type-tree chains over the nine extension families (45.10% versus 44.07%).



condition: domain-extension training causes zero regression on                   One negative result is reported in full. Merging the corpus
existing capability, and the difference against the re-measured                  of the existing routing families into training, so that routing
starting model is −5 problems; the discordant pairs b = 4 (the                   problems enter the model’s capability domain, fails the zero-
re-measurement passes while the new configuration fails) and                     regression gate in all three mixing ratios (176, 184, and 172
c = 9 (the reverse) give the exact binomial test                                 out of 218, all below 191), with degradation not monotone in
                                                                               the ratio; we register this as a sensitivity of corpus mixing to
                                   min(b,c)      
                                     X        b+c                               the training trajectory, and model-level inclusion of the routing
           p = min1, 2 1−(b+c)                            (23)
                                               i                                 domain is left to future methodological work. In the whole-
                                     i=0
                                                                                 library readings, this domain’s score comes from the fixture
Substituting gives p = 0.267; the difference is not statistically                reference arm and is labeled as such. All readings additionally
significant. The construction of the formula: under the null                     passed an independent final audit: stratified re-grading by
hypothesis (equal pass rates), the directions of the b + c                       independent judges with zero discrepancies, and item-by-item
discordant pairs are independent and equiprobable, so the                        reconciliation of discordant rows and denominator scope.
null distribution of the smaller-side count X = min(b, c)
is binomial B(b + c, 1/2); the two-sided exact probability is                                         XI. D ISCUSSION
2 P (X ≤ min(b, c)), capped
                        P4 at 1. With b = 4 and c = 9 there                        The two empirical laws merge into one design principle:
are 13 discordant pairs: i=0 13 i = 1+13+78+286+715 =                            for multi-step numeric derivation, restrict the model’s free-
1,093, so p = 2 × 1093/213 = 0.267, consistent with (23).                        generation range and make the tool state needed for the verdict

                                                                            15
available at decision time. The first law says that when numeric         reliability guarantees, this property has value independent of
content is generated freely, the required accuracy grows ex-             the pass rate; formal verification of neural networks is an
ponentially with the length of the proposition, and improving            established line in this journal [33], [34], and auditability
per-element accuracy cannot compensate; the second says that             extends the same concern from the network to the process that
inside a restricted decision space, information visibility rather        generates its outputs. The structured process also changes how
than loss allocation decides correctness. The experimental               evaluation and scrutiny work. When the smallest unit of model
results agree with the division-of-labor hypothesis of the               behavior is an executable operator decision, a failure sample
introduction, and the architecture choice both point to is: the          no longer offers only an aggregate signal but decomposes into
model handles policy (choosing steps and arguments), the                 position (which step failed), content (which argument or class
symbolic tool handles computation, and template compilation              failed), and confidence (the decision distribution); the error
handles text. The analysis of the error structure also carries           localization and attribution of Section VIII are built on this
independent evaluation significance. Token-level accuracy and            decomposition. For applications that presuppose reliability,
the surface correctness of chain-of-thought intermediate steps           this property matters as much as the pass rate itself: it allows
can badly overestimate ability on long-derivation tasks; in              mechanical enumeration and statistics of failure modes before
settings where proof validity is a Boolean conjunction, per-             deployment, without human sampling of generated text. Unlike
content-element accuracy and the element count are the quan-             chain-of-thought, this observability costs no natural-language
tities directly tied to the pass rate; the controlled-corruption         output: the final configuration completes the entire solution
experiment further shows that the load-bearing integer count             within 6.12 discrete decision actions per problem on average,
is what matters: when non-load-bearing numbers are present               and the model generates no text to explain itself.
(which depends on the proof template), the measured pass
rate runs above the value computed from the surface count.                                    XII. L IMITATIONS
This analysis also offers a way to read the failure samples
                                                                            This paper has several main limitations. The problem do-
of other direct-generation systems: the interruption patterns of
                                                                         main consists of constructively generated discrete-mathematics
the two comparison generations on this suite match our direct-
                                                                         problems in three families (induction, inequalities, number
generation experiments (177 sorry interruptions for V1.5-RL;
                                                                         theory); the conclusions do not transfer directly to open
near-total sorry interruptions for V2-7B on both suites) and are
                                                                         domains or to propositions requiring complex lemma rewrit-
explained by the conjunctive requirement on content elements,
                                                                         ing. The main test suite has 218 problems and comes from
without assuming insufficient model scale. For tool-augmented
                                                                         our own generators; although zero-capability controls, seman-
methods, our results emphasize the timing and content of
                                                                         tic overlap filtering, and stating graded counts with every
tool-state feedback, beyond the availability of tools. In our
                                                                         reading are in place, and the domain-extension validation
factorial experiment the tool, the execution engine, is available
                                                                         on the public library (Section X) adds external readings,
in every configuration; the only difference is the computation
                                                                         most rows of Lean-Workbook (84,267 of 132,378) lie outside
timing of the state inside the decision frame, and that single
                                                                         the admissible domain of our operator system, and further
difference moves the pass rate by 74 problems. This suggests
                                                                         extension of that domain is constrained by corpus-mixing
that in settings with step-by-step tool calls, the design of
                                                                         sensitivity (the negative result at the end of Section X).
state feedback should be evaluated as an independent design
                                                                         Experiments use SmolLM2-135M as the main backbone; the
variable. The separate effect of scale has been separated in
                                                                         three-configuration comparison on the 1B backbone (Section
a first approximation by the three-configuration comparison:
                                                                         IX) gives a preliminary split of loadout migration and scale at
loadout migration and backbone scale each contribute about
                                                                         roughly half each, and systematic validation at larger scale is
half the difference (−11 and −10 problems, Section IX),
                                                                         still pending. Review verdicts are bound to our frozen review
whereas within this domain the combined effect of removing
                                                                         program and Lean version; changing the proof assistant or the
free generation and completing state information (from near
                                                                         version requires redoing the dual-protocol recheck. Finally,
zero to 87.6%) far exceeds the parameter gap between the
                                                                         the external models in the comparison experiments are not
two backbones in the comparison; this contrast in magnitude
                                                                         connected to our toolchain; the comparison speaks to the
is the substance of our claim. Replication on larger backbones
                                                                         difference in output-channel structure and cannot be read as a
and transfer of the recipe to more problem families remain
                                                                         same-interface comparison of the two models’ ability.
future work. The auditability of this architecture is not a
bolted-on engineering measure but a direct consequence of
separating responsibilities: the model’s output is restricted                                 XIII. C ONCLUSION
to symbolic decisions, computation lives in a deterministic                 This paper examined the failure mechanism of long-chain
engine, and text comes from template compilation; each can               generation in language-model automated theorem proving
be checked independently. This makes both the failures and               inside a fully auditable discrete-mathematics domain, and
the successes of the system explainable down to specific                 proposed SCOPE, an architecture with the model as policy
stages; our localization of the error structure (Section VI)             planner. The main results follow. Under direct generation of
and of state timing (Section VIII) both rest on this property.           complete proofs, the pass rate is bounded by a power law in the
Extracting human-readable symbolic accounts from trained                 accuracy of single content elements, and token-level accuracy
networks is an active direction [32]; here the symbolic ac-              diverges from the pass rate (token accuracy 0.9637 with
count is native to the architecture. For applications that need          0/218 passing; the control-set pass rate matches the power-law

                                                                    16
prediction, and the controlled-corruption experiment verifies              repository; drawing notes are in writing/FIGURES PLAN.md;
the constraint on 2,617 reference proofs, with load-bearing                every number can be exported directly from the raw files
corruption surviving 0/432). Replacing free-text generation                of the results and gen44 directories. The eight tables are
with a compiler raises the pass rate from 1/218 to 117/218, and            numbered in order of appearance: Table I, problem-domain
the text stage stops costing anything. A factorial experiment              layers and the operator vocabulary; Table II, execution logic
on final-step decisions shows that the state timing of the                 of representative operators; Table III, step-by-step computation
decision frame alone determines a 74-problem difference in                 of a sum-of-squares problem; Table IV, carrier comparison for
pass rate (117/218 versus 191/218), while loss weighting is                multi-hop latent readout; Table V, mechanism decomposition
negative. On the same suite, the 135M configuration with                   of the discretization experiment; Table VI, main experimental
the toolchain attached reaches an 87.6% certified pass rate                configurations; Table VII, factorial results; Table VIII, re-
at one to three orders of magnitude lower resource cost than               source comparison. Data sources as above.
two generations of 7B proof-specialized direct generators,
and the cross-generation recheck points the same way (V2-                                       A PPENDIX B
7B certifies zero on both the main suite and the public-                         R EVIEW P ROGRAM AND K EY-F ILE C HECKSUMS
library stratified suite, including the problems that never hit the           The review program source is drct common.py,
generation cap). All multi-step thinking happens in the discrete           version-frozen for the entire experimental period, MD5
decision sequence, with no natural-language thinking text.                 7c31b58da9d7228cee31b9be581fe5dd. The raw reading files
We conclude that in multi-step numeric derivation, output-                 of every experiment (per-problem records, stratified rechecks,
channel structure and decision-information visibility are more             and reverse-verification results) and their checksums are
direct improvement variables than model scale. On the public               listed in MANIFEST.md and the results directory of the
library, domain extension reaches a 60.29% certified pass rate             code repository; training configurations and batch-order
on gradeable problems inside the admissible domain with                    checksums are recorded in the report file of each experiment.
zero regression on the old domain, and model-independent                   The key files of the domain-extension and public-library
pass rates on the extension families match the fixture chains;             validation (the final experiment report, the literal-scope
systematic validation on larger backbones is future work.                  full re-grading summary, the final-exam model checkpoint,
                                                                           and the final-audit report) and their checksums are in the
                    A PPENDIX A                                            gen44 directory; the key files of the cross-model dual-suite
  F IGURE AND TABLE I NVENTORY WITH DATA S OURCES                          comparison (the experiment report, the grading summary, and
                                                                           the failure-decomposition artifacts) and their checksums are
   The five main figures are numbered in order of appearance.              in the gen45 directory.
Fig. 1, the SCOPE architecture and data flow (division of
labor among the three components, the zero-token thinking
label, and the main readings); Fig. 2, the low-dimensional
projection of decision-frame hidden states (the measured fam-
ily organization and chain progression); Fig. 3, quantitative
tests of Law 1 (the power-law curve with measured points,
and the two controlled-corruption panels); Fig. 4, composition,
confidence, and per-step entropy of final-step errors (three
panels); Fig. 5, the main results grid (configuration pass-rate
ladder, resource comparison, the Lean-Workbook triage fun-
nel, and the nine-family end-to-end comparison). The carrier-
comparison readings of multi-hop latent readout are carried
by Table IV and the text of Section IV-A and are not given
a separate figure. Seven appendix figures follow: Fig. A1,
training dynamics of the final configuration (loss compo-
nents and gradient norms, 6,000 steps); Fig. A2, the depth-
curriculum ladder of the discretization experiment (gate-probe
trajectory, Section IV-A); Fig. A3, the vocabulary geometry
of the operator-selection head (separation of backbone and
added operators, not family clustering); Fig. A4, the filtered-
direction loss cross-section at the training convergence point
(51 × 51 grid, a wide shallow basin); Fig. A5, complete
two-configuration distributions of first-error probability (the
full version of Fig. 4(b)); Fig. A6, the complete along-chain
decision-entropy curves (the full version of Fig. 4(c)); Fig. A7,
decision-step counts and per-family pass rates (Section IX).
Per-figure data files for every figure (with source paths and
checksums) live in writing/figures/llm analysis/ of the code

                                                                      17
Fig. A1. Training dynamics of the final configuration (6,000 steps). (a) Total objective with the chain and slot components (log axis). (b) Clipped gradient
norm and held-out operator top-1 accuracy; the latter saturates from step 50 onward, so training progress is read from the loss.




Fig. A2. The depth-curriculum ladder of the discretization experiment (v15). (a) The gate-probe measured depth rises monotonically from 1 to 16, with all
fifteen openings between training steps 11,000 and 17,500; the shading shows depth sampling of training episodes. (b) Probe and training error curves. (c)
Depth sampling of training episodes.




                                                                            18
Fig. A3. Low-dimensional projection of the operator-selection head’s output vectors (220 rows). The head encodes the boundary between backbone and added
operators (0.969 within-backbone nearest-neighbor share), not a seven-segment clustering by problem family.




Fig. A4. Filtered-direction loss cross-section at the training convergence point (51 × 51 grid). The floor is 0.235 nats; the corners reach 5.34 nats, 15.2 times
the loss at the convergence point (0.351 nats), forming a wide, shallow basin.




                                                                              19
Fig. A5. Empirical distributions and counts of top-1 probability at the first erroneous decision step in the two configurations (baseline n = 101, final
configuration n = 27; counts at the 0.9 threshold: 55 and 12); the full version of Fig. 4(b).




Fig. A6. Operator-decision entropy along the chain (log vertical axis; certified passes versus failures), the full version of Fig. 4(c); at t = 4 the two groups
read 0.027 and 0.191 nats.




                                                                              20
Fig. A7. Step-count distribution of the 218 gold operator chains (stacked by problem family, mean 6.12), and the compile-grade pass rate of each family for
the Experiment 2 chains under compilation (121/218: nested induction 13/13, lemma tower 24/24, sum-of-squares 84/181).




                                                                           21
                            R EFERENCES                                                 for formal olympiad-level mathematics,” in Proc. Int. Conf. Learning
                                                                                        Representations (ICLR), 2022.
                                                                                    [8] H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen, “Lean
                                                                                        workbook: A large-scale Lean problem set formalized from natural
                                                                                        language math problems,” arXiv preprint arXiv:2406.03847, 2024.
                                                                                    [9] G. Lample et al., “HyperTree proof search for neural theorem proving,”
                                                                                        in Advances in Neural Information Processing Systems (NeurIPS), 2022.
                                                                                   [10] M. Mikuła et al., “Magnushammer: A transformer-based approach to
                                                                                        premise selection,” in Proc. Int. Conf. Learning Representations (ICLR),
                                                                                        2024.
                                                                                   [11] A. Q. Jiang et al., “Draft, sketch, and prove: Guiding formal theorem
                                                                                        provers with informal proofs,” in Proc. Int. Conf. Learning Representa-
                                                                                        tions (ICLR), 2023.
                                                                                   [12] T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong, “Solving olympiad
                                                                                        geometry without human demonstrations,” Nature, vol. 625, no. 7995,
                                                                                        pp. 476–482, 2024.
                                                                                   [13] T. Hubert et al., “Olympiad-level formal mathematical reasoning with
                                                                                        reinforcement learning,” Nature, vol. 651, no. 8106, pp. 607–613, 2025.
                                                                                   [14] E. First, M. N. Rabe, T. Ringer, and Y. Brun, “Baldur: Whole-proof gen-
                                                                                        eration and repair with large language models,” in Proc. 31st ACM Joint
                                                                                        European Software Engineering Conf. and Symp. on the Foundations of
                                                                                        Software Engineering (ESEC/FSE), 2023, pp. 1229–1241.
                                                                                   [15] P. Song, K. Yang, and A. Anandkumar, “Lean Copilot: Large language
                                                                                        models as copilots for theorem proving in Lean,” in Proc. Int. Conf.
                                                                                        Neuro-Symbolic Systems (NeuS), PMLR vol. 288, 2025, pp. 144–169.
                                                                                   [16] K. Su, H. Su, C. Li, J. Zhu, and B. Zhang, “Probabilistic neural–symbolic
                                                                                        models with inductive posterior constraints,” IEEE Trans. Neural Netw.
                                                                                        Learn. Syst., vol. 35, no. 2, pp. 2667–2679, 2024.
                                                                                   [17] L. Gao et al., “PAL: Program-aided language models,” in Proc. Int. Conf.
                                                                                        Machine Learning (ICML), 2023.
                                                                                   [18] T. Schick et al., “Toolformer: Language models can teach themselves
                                                                                        to use tools,” in Advances in Neural Information Processing Systems
                                                                                        (NeurIPS), 2023.
                                                                                   [19] Y. Zhang, Z. He, and G. G. Yen, “Uncovering large language model
                                                                                        weaknesses in character and word understanding and manipulating,”
                                                                                        IEEE Trans. Neural Netw. Learn. Syst., vol. 36, no. 10, pp. 17570–
                                                                                        17584, 2025.
                                                                                   [20] Y. Bengio, J. Louradour, R. Collobert, and J. Weston, “Curriculum
                                                                                        learning,” in Proc. Int. Conf. Machine Learning (ICML), 2009, pp. 41–
                                                                                        48.
                                                                                   [21] S. Bengio, O. Vinyals, N. Jaitly, and N. Shazeer, “Scheduled sampling
[1] L. de Moura and S. Ullrich, “The Lean 4 theorem prover and program-                 for sequence prediction with recurrent neural networks,” in Advances in
    ming language,” in Proc. 28th Int. Conf. Automated Deduction (CADE),                Neural Information Processing Systems (NeurIPS), 2015.
    Lecture Notes in Computer Science, vol. 12699, 2021, pp. 625–635.              [22] M. Ranzato, S. Chopra, M. Auli, and W. Zaremba, “Sequence level
                                                                                        training with recurrent neural networks,” in Proc. Int. Conf. Learning
                                                                                        Representations (ICLR), 2016.
                                                                                   [23] N. Dziri et al., “Faith and fate: Limits of transformers on compositional-
                                                                                        ity,” in Advances in Neural Information Processing Systems (NeurIPS),
[2] L. B. Allal et al., “SmolLM2: When smol goes big: Data-centric training             2023.
    of a small language model,” arXiv preprint arXiv:2502.02737, 2025.             [24] H. Lightman et al., “Let’s verify step by step,” in Proc. Int. Conf.
                                                                                        Learning Representations (ICLR), 2024.
                                                                                   [25] J. Wei et al., “Chain-of-thought prompting elicits reasoning in large lan-
                                                                                        guage models,” in Advances in Neural Information Processing Systems
[3] H. Xin et al., “DeepSeek-Prover-V1.5: Harnessing proof assistant feed-              (NeurIPS), 2022.
    back for reinforcement learning and Monte-Carlo tree search,” arXiv            [26] A. Vaswani et al., “Attention is all you need,” in Advances in Neural
    preprint arXiv:2408.08152, 2024.                                                    Information Processing Systems (NeurIPS), 2017.
                                                                                   [27] L. McInnes, J. Healy, and J. Melville, “UMAP: Uniform manifold
                                                                                        approximation and projection for dimension reduction,” arXiv preprint
                                                                                        arXiv:1802.03426, 2018.
                                                                                   [28] S. Hao et al., “Training large language models to reason in a continuous
[4] S. Polu and I. Sutskever, “Generative language modeling for automated               latent space,” in Proc. Conf. on Language Modeling (COLM), 2025.
    theorem proving,” arXiv preprint arXiv:2009.03393, 2020.                       [29] J. Geiping et al., “Scaling up test-time compute with latent reasoning:
                                                                                        A recurrent depth approach,” in Advances in Neural Information Pro-
                                                                                        cessing Systems (NeurIPS), 2025.
                                                                                   [30] E. B. Wilson, “Probable inference, the law of succession, and statistical
                                                                                        inference,” J. Amer. Statist. Assoc., vol. 22, no. 158, pp. 209–212, 1927.
[5] K. Yang et al., “LeanDojo: Theorem proving with retrieval-augmented            [31] DeepSeek-AI, “DeepSeek-Prover-V2: Advancing formal mathematical
    language models,” in Advances in Neural Information Processing Sys-                 reasoning via reinforcement learning for subgoal decomposition,” arXiv
    tems (NeurIPS), 2023.                                                               preprint arXiv:2504.21801, 2025.
                                                                                   [32] J. Townsend, T. Chaton, and J. M. Monteiro, “Extracting relational
                                                                                        explanations from deep neural networks: A survey from a neural-
                                                                                        symbolic perspective,” IEEE Trans. Neural Netw. Learn. Syst., vol. 31,
[6] H. Xin et al., “DeepSeek-Prover: Advancing theorem proving in LLMs                  no. 9, pp. 3456–3470, 2020.
    through large-scale synthetic data,” arXiv preprint arXiv:2405.14333,          [33] W. Xiang, H.-D. Tran, and T. T. Johnson, “Output reachable set
    2024.                                                                               estimation and verification for multilayer neural networks,” IEEE Trans.
                                                                                        Neural Netw. Learn. Syst., vol. 29, no. 11, pp. 5777–5783, 2018.
                                                                                   [34] F. Boudardara, A. Boussif, P.-J. Meyer, and M. Ghazel, “INNAbstract:
                                                                                        An INN-based abstraction method for large-scale neural network veri-
                                                                                        fication,” IEEE Trans. Neural Netw. Learn. Syst., vol. 35, no. 12, pp.
[7] K. Zheng, J. M. Han, and S. Polu, “MiniF2F: A cross-system benchmark                18455–18469, 2024.


                                                                              22
