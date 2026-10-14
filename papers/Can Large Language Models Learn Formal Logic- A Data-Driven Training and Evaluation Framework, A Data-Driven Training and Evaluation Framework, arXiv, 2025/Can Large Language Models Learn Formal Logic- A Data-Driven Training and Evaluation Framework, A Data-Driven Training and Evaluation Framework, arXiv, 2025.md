                                                                 Can Large Language Models Learn Formal Logic?
                                                                 A Data-Driven Training and Evaluation Framework


                                                                  Yuan Xia 1 Akanksha Atrey 2 Fadoua Khmaissia 2 Kedar S. Namjoshi 2


                                                                    Abstract                                 neuro-symbolic systems such as AlphaProof (AlphaProof &
                                                                                                             teams, 2024), the LLM guides a conventional proof-search
arXiv:2504.20213v1 [cs.LG] 28 Apr 2025




                                                 This paper investigates the logical reasoning ca-
                                                                                                             engine, replacing hard-coded heuristics or hints provided by
                                                 pabilities of large language models (LLMs). For
                                                                                                             humans. In the second category, which our work belongs to,
                                                 a precisely defined yet tractable formulation, we
                                                                                                             are LLMs that search for proofs directly. Chain-of-Thought
                                                 choose the conceptually simple but technically
                                                                                                             (CoT) (Wei et al., 2022) is one such system.
                                                 complex task of constructing proofs in Boolean
                                                 logic. A trained LLM receives as input a set of             The thought-chain produced by a CoT method is expressed
                                                 assumptions and a goal, and produces as output              in natural language. While easier for humans to understand,
                                                 a proof that formally derives the goal from the             a natural-language proof cannot be automatically validated
                                                 assumptions. Incorrect proofs are caught by an              precisely, due to ambiguities inherent in natural language.
                                                 automated proof checker. A critical obstacle for
                                                                                                             In order to systematically investigate the reasoning capabil-
                                                 training is the scarcity of real-world proofs. We
                                                                                                             ities of LLMs, it is simpler and more effective to express
                                                 propose an efficient, randomized procedure for
                                                                                                             input assertions and output proofs in formal language. A
                                                 synthesizing valid proofs and introduce Template
                                                                                                             “reasoning” LLM (Fig. 1) receives as input a set of assump-
                                                 Transformation, a data augmentation technique
                                                                                                             tions and a goal assertion, both expressed in a formal logic.
                                                 that enhances the model’s ability to handle com-
                                                                                                             As output, the LLM exhibits a formal proof that explains
                                                 plex logical expressions. The central evaluation
                                                                                                             how the goal follows logically from the assumptions. That
                                                 question is whether an LLM has indeed learned
                                                                                                             is, an LLM acts as a proof generator.
                                                 to reason. We propose tests to measure the rea-
                                                 soning ability of a black-box LLM. By these                 There are good reasons to believe that LLMs can act as proof
                                                 measures, experiments demonstrate strong reason-            generators and good reasons to believe that they cannot. On
                                                 ing capabilities for assertions with short proofs,          the positive side, LLMs are Turing-complete, assuming infi-
                                                 which decline with proof complexity. Notably,               nite precision arithmetic (Pérez et al., 2019; Bhattamishra
                                                 template transformation improves accuracy even              et al., 2020; Pérez et al., 2021; Strobl et al., 2024). An LLM
                                                 for smaller models, suggesting its effectiveness            scans its input and past output to determine its next output
                                                 across model scales.                                        symbol, using attention mechanisms to focus on the relevant
                                                                                                             portions. This is similar to how, in constructing a mathe-
                                                                                                             matical proof, humans select and combine past deductions
                                         1. Introduction                                                     to form new conclusions. Few-shot learning suggests that
                                                                                                             LLMs can recognize patterns and follow general rules. On
                                         In July 2024, The New York Times published an article               the negative side, Turing completeness relies on unbounded
                                         aptly titled “A.I. Can Write Poetry, but It Struggles With          integers (to encode an unbounded Turing machine tape); but
                                         Math.” (Lohr, 2024). General Large Language Models                  in reality, machine integers have bounded precision. LLMs
                                         (LLMs) are indeed excellent at manipulating text but can            have bounded context, no auxiliary memory, and no back-
                                         be poor at logical reasoning, which is at the heart of mathe-       tracking ability; hence, colloquially, LLMs may “forget”
                                         matics and computing. This work aims to investigate exper-          the distant past. This is an issue for proof construction,
                                         imentally whether that is an inherent limitation.                   as an assumption may not be required until a late stage of
                                         LLM-based reasoning falls into two broad categories. In             proof. LLMs operate statistically and may thus hallucinate
                                                                                                             and produce incorrect proofs even if the claim is valid. Fi-
                                             1
                                             University of Southern California, Los Angeles, CA, USA         nally, logical reasoning has a inherently high worst-case
                                         2
                                          Nokia Bell Labs, Murray Hill, NJ, USA. Correspondence to:          complexity: it is co-NP-complete even for Boolean logic,
                                         Yuan Xia <yuanxia@usc.edu>.                                         with rapidly increasing difficulty (e.g., RE-complete for
                                                                                                             first-order logic).

                                                                                                         1
                                                Can LLMs Learn Formal Logic?

To precisely formulate and test reasoning ability, we focus           determine whether a black-box LLM is actually reasoning
on reasoning in Boolean logic. In our view, there are several         vs. guessing or retrieving answers.
factors that make this a good choice. Boolean logic is the
basis for other logics (e.g., first order, modal, temporal, and       2. Background
the like). Therefore, if Boolean reasoning turns out to be a
challenging task for LLMs, it is unlikely that LLMs can do            In this section, we define the syntax and semantics of
better on more sophisticated reasoning. Boolean logic has a           Boolean logic, introduce the Hilbert proof system, and for-
simple proof system that makes it easy to automatically val-          ward and backward proof-construction mechanisms.
idate proofs. Semantically, Boolean reasoning is non-trivial,
being co-NP-complete. (The dual question of Boolean satis-            2.1. Boolean Logic: Syntax and Semantics
fiability is the canonical NP-complete problem.)
                                                                      Boolean formulas (also called assertions or expressions)
In a strong sense, therefore, Boolean reasoning can be                are formed by combining Boolean variables that represent
viewed as the C.elegans (Brenner, 2002) of LLM reasoning:             atomic propositions using familiar combinators, such as
structurally simple, semantically non-trivial, and exhibiting         “and” ( ∧ ), “or” ( ∨ ), “not” (¬), and “implies” ( → ). The
”in the small” the central difficulties of general reasoning.         Boolean domain is denoted B.
The central challenges are (1) a scarcity of real-world train-        Given a countable set X of Boolean variables (also called
ing data, i.e., valid proofs, and (2) a means of determining          propositions), a Boolean formula over X is formed by the
whether a black-box model is reasoning rather than memo-              minimal grammar f := p ∈ X | ¬f | f ∧ f . Disjunction is
rizing or guessing. We address these critical questions (1)           defined by f ∨ g = ¬((¬f ) ∧ (¬g)), and implication by
by giving an efficient randomized algorithm for generating a          f → g = (¬f ) ∨ g.
large and diverse corpus of logically valid proofs for training
and testing, and (2) by designing meaningful, automated,              An assignment is a function from X to B; i.e., it provides a
black-box tests of reasoning ability. The precision of formal         Boolean value for each variable. The satisfaction of a for-
language and the ability to automatically validate candidate          mula by an assignment π is a relation |= defined recursively
proofs simplifies both tasks, enabling them to be carried out         by: π |= p iff π(p) is true; π |= ¬f iff it is not the case that
fully automatically, efficiently, and at scale.                       π |= f ; and π |= f ∧ g iff π |= f and π |= g.

Our experiments show that Llama models can be trained                 For a Boolean formula, the satisfiability question is whether
to reason well in Boolean logic through a combination of              there is a assignment satisfying the formula. This is the
synthetic proof generation and proof augmentation. Us-                classic NP-complete question. The dual validity question
ing only 9000 synthetically generated proofs as training              is whether all assignments satisfy the formula. This is the
data, our fine-tuned Llama-8B model reaches 98% accu-                 canonical co-NP-complete question.
racy on depth-7 proofs, outperforming GPT-4o’s few-shot
learning performance (70% accuracy), despite having far               2.2. Hilbert Proofs
fewer parameters. Our ablation studies reveal two key find-           An instance of a Boolean reasoning problem is given by
ings: larger model capacity enables better generalization             a (possibly empty) set of assumption formulas and a goal
to deeper proofs, while proof augmentation enhances the               formula. The reasoning problem is to determine whether the
models’ ability to handle complex instances, particularly             goal follows from the assumptions. A proof is a step-by-step
benefiting the smaller Llama-1B model.                                explanation that justifies a ”yes” answer.
In our view, this work makes several contributions. One is            There are several proof systems for Boolean logic. In this
the recognition that training an LLM over a formal logic has          work, we use the well known Hilbert style of proof sys-
distinct advantages: synthetic data can be generated at large         tem (Mendelson, 2024). For simplicity, we restrict attention
scale and variety for training, and reasoning ability can be          to a sub-logic of propositional logic that has implication as
evaluated robustly with automated tests that are generated            its only connective.1 The Hilbert-style proof system for this
and run at scale. The second is the choice of Boolean logic           logic consists of two axioms and one inference rule, called
to study reasoning ability. If LLMs fail at Boolean logic, it         Modus Ponens (MP).
is unlikely that they will succeed at more complex reasoning.
The third is a technical contribution of template proof trans-        The axiom schemas are the following.
formations, which produces syntactically varied proofs that
                                                                      A1 ::    (A → (B → A))
share a common structure. In training, this forces the LLM
to focus on abstract proof patterns rather than on concrete           A2 ::    (A → (B → C)) → ((A → B) → (A → C))
tokens, improving its generalization ability. A fourth contri-           1
                                                                           In this sub-logic, every formula is satisfiable, but validity (i.e.,
bution is the variety of proposed tests that can be applied to        reasoning) is still co-NP-hard (Appendix A.1).

                                                                  2
                                                Can LLMs Learn Formal Logic?

Colloquially, the first axiom says that if both A and B hold,          2.2.2. P ROOF C ONSTRUCTION
then A holds. The second axiom says that if A and B
                                                                       There are two main mechanisms of proof construction.
together imply C, then knowing that A implies B suffices
to conclude that A also implies C.                                     Forward proof construction maintains a set of deduced for-
                                                                       mulas; initially, this set contains the supplied hypotheses. At
An instance of an axiom schema is obtained by providing
                                                                       each step, one adds a formula to this set, either by instantiat-
a substitution that specifies formulas for the placeholders
                                                                       ing an axiom, or by applying MP to formulas already in the
A, B, C. The MP inference rule deduces B given that the
                                                                       set. Reasoning is complete if the goal formula is eventually
hypotheses “A implies B” and “A” both hold.
                                                                       added to the set.
Formally, a proof is a sequence of steps where each step
                                                                       Backwards or Goal-directed proof construction maintains
consists of a claimed formula along with a justification. A
                                                                       a proof tree. Some leaves of the tree represent “open” for-
justification for step k of the proof can be of three kinds: (1)
                                                                       mulas; initially, the tree is a single open node labeled with
matching the k’th formula to an assumption; (2) matching
                                                                       the goal. At a backward step, one “closes” an open leaf
the k’th formula to an axiom instance with a substitution σ,
                                                                       node n labeled with a formula g in one of three ways: by
which is correct if the k’th formula is the result of applying
                                                                       recognizing g as a hypothesis, or by recognizing g as an
σ to the named axiom; or (3) MP applied to steps m, n of
                                                                       axiom instance, or by introducing a formula f and asserting
the proof, which is correct if, denoting the k’th formula by
                                                                       that g follows from f and (f → g) by MP – these formulas
g, for some formula f , the m’th formula is (f → g), and
                                                                       label new open leaf nodes that are added as children of n.
the n’th formula is f . Both m, n must be strictly smaller
                                                                       Reasoning is complete when all leaves are closed.
than k to avoid circular reasoning.
A proof is valid if every justification in the proof is correct
                                                                       3. Training LLMs to Reason
and the goal formula is claimed at some proof step. The
Hilbert system is sound: that is, given a valid proof, the goal        A central challenge in training an LLM to reason with formal
holds for every assignment that satisfies the assumptions.             proofs is the shortage of data. Proofs are found in textbooks,
                                                                       or in proof repositories for automated theorem provers. It
2.2.1. P ROOF E XAMPLE [T RANSITIVITY ]                                is difficult to assemble proofs in a uniform format, and of
                                                                       sufficient quantity and variety for training.
Given assumptions p → q and q → r, does the goal
p → r hold? This is just transitivity, which is true, as can           We describe a simple and efficient randomized backward
be established by the following Hilbert proof:                         proof generation process, which synthesizes valid proofs
                                                                       of arbitrary size and depth. We further augment the set of
  1. (q → r) → (p → (q → r)), by Axiom A1 with                         randomly generated proofs to create groups of structurally
     substitution A = q → r, B = p.                                    similar variants of each original proof.
                                                                       Augmentation is useful in training, to ensure that the LLM
  2. q → r, by Assumption 2.                                           focuses less on the syntax of a proof and more on the un-
                                                                       derlying logical reasoning – in essence, we would like the
  3. p → (q → r), by MP on steps 1, 2.                                 LLM to learn proof patterns rather than memorize specific
                                                                       proofs. Augmentation is also useful for testing whether a
  4. (p → (q → r)) → ((p → q) → (p → r)), by                           trained LLM has learned to reason.
     Axiom A2 with substitution A = p, B = q, C = r.
                                                                       3.1. Proof Generation
  5. (p → q) → (p → r), by MP on steps 4, 3.
                                                                       The proof generation process is, in essence, a randomized
  6. p → q, by Assumption 1.                                           form of the goal-directed proof construction process. In-
                                                                       stead of inferring a proof for a fixed goal under fixed as-
  7. p → r, by MP on steps 5, 6.                                       sumptions, the randomized generation starts with a ran-
                                                                       domly chosen goal formula and proceeds to construct a
Proofs in the Hilbert-style proof system have a well-                  valid, randomized proof tree.
deserved reputation for being difficult to follow for humans.
We chose this system, however, as it has a minimal set of                1. The root of the tree is labeled with a goal formula, say
rules, which we believed would be easier for an LLM to                      g, that is chosen at random.
learn. Other standard proof systems, such as natural deduc-
tion, produce proofs that are easier to follow (Pelletier &              2. At an leaf node labeled with a formula h, the process
Hazen, 2024) but have multiple inference rules.                             decides at random whether to do one of the following.

                                                                   3
                                                Can LLMs Learn Formal Logic?

        • Stop expansion at this node. The open formula h             random that maps each variable in X to a randomly chosen
          turns into an assumption used to prove g.                   Boolean expression over a randomly chosen variable set
        • Choose a formula f at random and expand using               Y (not necessarily different from X), (2) systematically
          a MP justification into two new subgoal nodes               replace each formula f that occurs in the proof with the
          labeled with formulas f and f → h.                          formula σ(f ) that is obtained by applying the substitution
                                                                      σ to f , and (3) systematically apply the substitution σ to the
        • If h is an axiom instance, close this node with an
                                                                      assumption and goal formulas.
          axiom justification.
                                                                      It is easy to show by induction on proof length that the
  3. The process continues until the proof tree reaches a             transformed reasoning instance is also valid. The structure
     specified limit on size or depth.                                and sequence of the justifications is unchanged by this trans-
                                                                      formation: only the formulas are changed according to the
A proof tree generated in this way is turned into a valid proof       randomly chosen substitution. Hence, the transformation
by viewing all formulas of stopped open nodes (case 2) as             can be applied repeatedly to generate many variants of the
assumptions required to prove the goal g. A linear Hilbert            original proof that share a common proof structure. This
proof structure is obtained by traversing the tree from leaves        construction is used to train the LLM model and (as dis-
to the root in any order where the children of every node are         cussed in Section 4) also used to test the reasoning ability
traversed prior to the node itself.                                   of a trained LLM model.

Goal-directed proof generation is efficient for a Hilbert-style       The intuition is that, during training, supplying similar in-
system as the generation process determines an appropriate            stances obtained through template transformation forces the
resolution for every open formula locally, e.g., by randomiz-         LLM to focus on the abstract proof structure rather than
ing the application of MP, in time that does not depend on            on concrete detail such as variable names. This is similar
the size of the current proof tree. In contrast, a forward gen-       in spirit to the use of batch transformations in computer
eration process must search at each step for already-deduced          vision, where a picture (of a cat, say) is subjected to spatial
formulas that match the shapes f → g and f to apply the               transformations such as rotation, reflection, and translation
MP rule. A naı̈ve algorithm requires quadratic time in the            so that the trained model focuses on the attributes intrinsic
number of deduced formulas, which can be reduced to near-             to a cat, ignoring its orientation in space.
linear time using hashing. Thus, goal-directed proof genera-
tion has a significant efficiency advantage, which extends to         4. Evaluation Framework
proof-generation in other systems such as natural deduction.
                                                                      In this section, we present evaluation metrics to assess the
3.2. Proof Augmentation by Template Transformation                    reasoning capabilities of LLMs and demonstrate the effec-
                                                                      tiveness of our training and evaluation methods.
The randomized proof-generation algorithm produces valid
proofs, but does not guarantee that many examples with                Existing LLM evaluation metrics focus on different aspects
same or similar proof structure are generated. That moti-             of model output, such as quality, relevancy, factual correct-
vates our technique for data augmentation, which is based             ness, bias, and toxicity, but there is no standardized approach
on a new concept of template transformations.                         for assessing reasoning capabilities. Having a systematic
                                                                      and comprehensive method is necessary to avoid reliance
This technique is based on the key observation that a proof           on anecdotal data and memorization as well as to accurately
in Hilbert form may also be viewed as a proof schema.                 measure progress in reasoning capabilities.
That is, a proof over a set of variables X can be viewed
as a template: uniformly applying a substitution that maps            We propose an evaluation process with four clearly defined
each variable of X to a Boolean formula over a (possibly              and measurable metrics. These metrics assess the models’
different) set of variables Y creates another valid proof.            ability to apply logical reasoning to new, unseen problems
                                                                      of varying degrees of complexity.
For instance, the reasoning example of Section 2 is defined
over variables p, q, r. Say we uniformly replace q with               4.1. Favoring Semantics over Syntax
y1 , and p with y1 → y2 , and r with y2 → y1 . This
replacement creates a valid proof showing that the new goal           An LLM should demonstrate the ability to generalize be-
(y1 → y2 ) → (y2 → y1 ) (transformed from the original                yond the specific instances in its training data. For example,
goal p → r) follows by transitivity from the transformed              if the LLM can produce a proof for a reasoning problem de-
assumptions (y1 → y2 ) → y1 and y1 → (y2 → y1 ).                      fined over variables p, q, it should similarly manage to con-
                                                                      struct a proof for the template-transformed problem where
In general, to transform a valid reasoning instance defined           p, q are uniformly replaced by arbitrary formulas f, g, re-
over a set X of variables, we (1) choose a substitution σ at

                                                                  4
                                                Can LLMs Learn Formal Logic?

spectively. This indicates that the LLM recognizes and
abstracts the underlying logic of the problem, disregarding
superficial syntactic differences such as variable names or
structural variances.

4.2. Generalizing to Deeper Proofs
A reasoning LLM should discover proofs that are longer
than those present in its training set. This suggests that
the LLM is not merely memorizing proofs up to a certain
complexity but exhibiting deeper logical reasoning. The
evaluation of this metric involves measuring model accuracy
with increasing depth of reasoning, highlighting its ability
to navigate and resolve more complex proof structures.

4.3. Handling Wider Expressions
                                                                      Figure 1. Overview: The training phase generates synthetic proofs
An LLM should prove statements that incorporate a larger              and applies template transformations for fine-tuning. Inference
set of variables than those found in its training dataset. For        produces a candidate proof for the query (“Does the goal follow
instance, if the training involves variables X1 and X2 exclu-         from the assumptions?”); this proof is formally validated.
sively, the model should be tested on properties involving
an expanded set, such as X1 , ..., Xn . Success indicates that
the model has not merely memorized proofs involving two               a given problem is replaced with a randomly generated
variables but can extend its reasoning to more complex sce-           expression consisting of up to 4 variables and with a maxi-
narios. Testing includes measuring accuracy as the number             mum recursion depth of 4. Models are trained to generate
of variables involved increases.                                      complete proofs given a goal and a set of assumptions, as
                                                                      illustrated in Fig. 1.
4.4. Exhibiting Diversity in Proofs
                                                                      Evaluation We generate separate proof trees for training and
A logical statement can have several valid proofs. We eval-           evaluation to prevent data leakage. To obtain the evaluation
uate diversity by assessing the LLM’s ability to generate a           dataset, we construct a few distinct proof trees and ensure
range of valid proofs for a given input query, whenever it is         all formulas f are unique without duplicates occurring in
applicable. This can indicate that the model is engaging in           the training dataset (Section 3.2). From these trees, we
creative and independent reasoning rather than relying on             extract both the validation and testing sets. The validation
rote memorization of the dataset. To support this metric, we          set comprises 375 samples from in-distribution depths (7,
use a symbolic proof checker to semantically evaluate proof           10, and 13; 125 samples each).
validity rather than relying on syntactic token-level equality.       For generalization analysis, we use 450 test samples across
                                                                      nine depths (4-28; 50 samples per depth) and 400 samples
5. Experimental Analysis                                              across four widths of increasing variable complexity (100
                                                                      samples per width). We ensure unique formulas across all
5.1. Experimental Setup                                               partitions. While using synthetic data might seem limiting, it
Training We fine-tune two Llama3 models (8B and 1B                    enables systematic assessment of model performance across
parameters) (Dubey et al., 2024) on our synthetically gener-          proof complexities and controlled testing of generalization
ated Hilbert proofs. We use 4-bit quantization to optimize            capabilities, particularly given the absence of large-scale
memory usage. The fine-tuning process employs Low-Rank                real-world Hilbert proof datasets.
Adaptation (LoRA) (Hu et al., 2021) to efficiently update             To evaluate our models, we report the testing accuracy de-
model parameters without modifying the entire network.                fined as the ratio of correctly generated proofs to the total
Training convergence is monitored using exact match ac-               number of test problems. A proof is considered correct
curacy with the ground-truth proofs. We also use early                only if it passes our formal validator, which accepts a proof
stopping (patience = 5 epochs) to prevent overfitting.                only if it is syntactically well-formed and if every step of
For all experiments, the training data consists of a balanced         the proof passes a rigorous check for (i) valid application
number of proofs with depths 7, 10, and 13. During train-             of Modus Ponens, (ii) correct use of assumptions, and (iii)
ing, Template Transformation is applied with a probability            proper axiom invocation.
αT T = 0.7 during batch preprocessing. Each variable in               Experimental Design Our experimental analysis is twofold:

                                                                  5
                                                  Can LLMs Learn Formal Logic?


Table 1. Proof Generation Accuracy on In-Distribution Test Data: Comparison between fine-tuned Llama models (trained on 9000
examples), GPT-4o few-shot learning (averaged across 1,3,6,9-shot learning settings), and pre-trained baseline models. Testing performed
on proof depths (d) matching training distribution. w/ TT and w/o TT denote models fine-tuned with and without Template Transformation
respectively.
                                                                           Accuracy by Proof Depth
      Model                                            d=7                          d = 10                             d = 13
       SOTA Performance
      GPT-4o (X-shot)                                0.67±0.08                       0.48±0.08                       0.26±0.04
       Pre-trained Base Models
      Llama-3.2-8B (X-shot)                            ≈ 0.00                          ≈ 0.00                          ≈ 0.00
      Llama-3.1-1B (X-shot)                            ≈ 0.00                          ≈ 0.00                          ≈ 0.00
       Our Approach - Small Model (Llama-3.1-1B)
      Fine-tuned w/o TT                       0.52                                      0.30                             0.02
      Fine-tuned w/ TT                        0.54                                      0.30                             0.04
       Our Approach - Large Model (Llama-3.2-8B)
      Fine-tuned w/o TT                       0.78                                      0.40                             0.28
      Fine-tuned w/ TT                        0.98                                      0.66                             0.32



First, we establish baseline performance by comparing our              some examples in Appendix A.2. We use identical ex-
fine-tuned models against GPT-4o (OpenAI, 2024) and                    amples across all x-shot evaluations to maintain evaluation
pre-trained Llama3 models on in-distribution proof depths.             fairness. The reported few-shot results represent averages
Then, through ablation studies, we examine the models’                 across these settings.
generalization capabilities across varying proof depths and
                                                                       GPT-4o achieves an average accuracy of 0.67±0.08 on depth-
widths, and analyze the impact of training data size and
                                                                       7 proofs, with performance degrading to 0.48±0.08 and
Template Transformation.
                                                                       0.26±0.04 at depths 10 and 13. The pre-trained Llama3 base
Key Findings Our experiments reveal the effectiveness of               models fail to generate valid proofs (≈ 0.00 accuracy) when
fine-tuning Llama3 models (8B and 1B) for Hilbert proof                tested directly on our task, likely due to both their smaller
generation using our proposed synthetic data and proof aug-            model sizes compared to GPT-4o (> 100B parameters) and
mentation. The 8B model achieves 98% accuracy on depth-                the challenge of inferring strict syntactic rules of Hilbert
7 proofs, outperforming GPT-4o’s few-shot performance                  proofs from few examples.
(67%±8 averaged across 1,3,6,9-shot settings) despite hav-
                                                                       Our fine-tuned models show substantial improvements over
ing far fewer parameters. Our ablation studies show that
                                                                       both GPT-4o and their pre-trained versions. The large model
model capacity (8B vs 1B) enables generalization to deeper
                                                                       (8B) with Template Transformation achieves 0.98 accuracy
proofs, while proof augmentation by Template Transfor-
                                                                       on depth-7 proofs, significantly outperforming GPT-4o de-
mation enhances handling of complex, out-of-distribution
                                                                       spite having fewer parameters. This performance advantage
expressions. Performance scales with training data size,
                                                                       persists at greater proof depths, with accuracies of 0.66 and
though naturally degrading with increasing proof complex-
                                                                       0.32 for depths 10 and 13 respectively. Template Trans-
ity.
                                                                       formation proves particularly effective for the large model,
                                                                       improving accuracy by 20-25% mainly for shorter depths
5.2. Baseline Evaluation                                               compared to standard fine-tuning.
We evaluate our approach against GPT-4o (100B+ parame-                 The small model (1B) shows more modest improvements,
ters) and compare against our base models: Llama-3.2 (8B)              achieving 0.52 accuracy at depth-7, with Template Trans-
and Llama-3.1 (1B). As shown in Table 1, testing is per-               formation showing limited impact. This performance gap
formed on proof depths matching the training distribution              between our 8B and 1B models suggests that logical rea-
{7,10,13}. For GPT-4o and the pre-trained base models, we              soning capabilities scale with model size, even within the
evaluate few-shot learning with {1, 3, 6, 9} demonstrations:           relatively narrow 1B-8B parameter range.
1-shot uses one depth-7 proof, 3-shot uses one proof from
each training depth 7,10,13}, 6-shot uses two proofs per
depth, and 9-shot uses three proofs per depth. We provide

                                                                   6
                                                  Can LLMs Learn Formal Logic?

5.3. Ablation Study                                                      Results in Fig. 2 show that Template Transformation signifi-
                                                                         cantly improves handling of complex expressions for both
We conduct ablation studies to systematically analyze how
                                                                         the 8B and 1B models. Notably, the template transforma-
different factors affect our fine-tuned LLMs’ performance,
                                                                         tion’s impact on width generalization is more pronounced
and to understand the limits of our proposed approach.
                                                                         than its effect on depth handling, suggesting its particular
                                                                         utility for managing expression complexity.

                                                                         5.3.3. I MPACT OF M ODEL S IZE AND T RAINING DATA
                                                                         We compare Llama-8B and Llama-1B which we denote as
                                                                         LLM and SLM respectively, reflecting their relative model
                                                                         capacities. We train three instances of each model using
                                                                         synthetic training sets of three sizes: 1500, 4500, and 9000
                                                                         examples. Each set is balanced across proof depths 7, 10,
                                                                         and 13.
                                                                         Fig. 2 summarizes the obtained results. While the LLM gen-
                                                                         erally outperforms the SLM, particularly on deeper proofs,
                                                                         we observe an interesting pattern with proof width: when us-
                                                                         ing Template Transformation, the SLM achieves comparable
                                                                         performance to the LLM on wider expressions (width ≥ 2),
                                                                         suggesting that our data augmentation technique effectively
                                                                         compensates for smaller model capacity in handling com-
                                                                         plex expressions. The LLM, however, shows better data effi-
                                                                         ciency overall, achieving stronger performance with smaller
                                                                         training sets, especially on depth generalization.
Figure 2. Comparison of Llama3-8B (LLM) and Llama3-1B
(SLM) model variants’ testing accuracies across different training       5.3.4. I MPACT OF T EMPLATE T RANSFORMATION
data sizes. Left: Impact of proof width on accuracy. Right: Impact
of proof depth on accuracy. Models with and without Template             We analyze how the probability of applying Template Trans-
Transformation (TT) are compared.                                        formation (αT T ) during the training process impacts the
                                                                         models’ reasoning capability. We vary αT T from 0 to 0.9
5.3.1. I MPACT OF P ROOF D EPTH                                          and report model performance across different proof com-
                                                                         plexities as shown in Fig. 3.
To evaluate reasoning depth generalization, we test models
on nine proof depths (4-28 steps, 50 samples per depth)
using fixed-width expressions. Each proof in the test set is
generated by systematically reducing deeper proofs: identi-
fying the first modus ponens application (i.e., one closest to
the leaf nodes) and replacing it with the deduced statement,
which is treated as a new assumption, to reduce depth by
one step.
As shown in Fig. 2, performance degrades with increasing
proof complexity, but larger models show better resilience.              Figure 3. Impact of Template Transformation probability (αT T )
The 8B model maintains reasonable accuracy up to depth                   on model performance. The left subplot shows test accuracy across
13, while the 1B model’s performance drops more sharply                  different model widths (0-3), while the right subplot demonstrates
after depth 10.                                                          the effect on models of varying depths (4-13).

5.3.2. I MPACT OF P ROOF W IDTH
                                                                         The results reveal a consistent pattern for proof width: per-
We analyze width generalization using four levels of ex-                 formance improves as αT T increases up to 0.7, beyond
pression complexity (100 samples per width). Each level                  which accuracy declines sharply. This trend is particularly
represents increasingly nested variable substitutions while              pronounced for width-1 and width-2 proofs, suggesting
maintaining proof depth (d = 7). A width-0 proof uses sim-               an optimal transformation rate for enhancing generaliza-
ple variables (e.g., P ⇒ Q), while higher widths introduce               tion to complex expressions. For proof depth, the impact
nested implications (e.g., (P ⇒ Q) ⇒ R for width-1).                     varies: while deeper proofs (depth 13) show similar sen-

                                                                     7
                                              Can LLMs Learn Formal Logic?

sitivity to αT T , shallower proofs exhibit more stable per-        deeper insights into LLMs’ performance on particular types
formance across different transformation rates. This differ-        of logical problems (Wan et al., 2024; Zong & Lin, 2024).
ence might be attributed to the inherent exposure to shorter
                                                                    Some of these evaluation approaches are limited by the num-
proof patterns within longer proofs during training. Set-
                                                                    ber of examples in the benchmark sets. Moreover, proofs
ting αT T = 0.7 provides the best balance, maximizing the
                                                                    expressed in natural language introduce other difficulties;
model’s ability to handle complex expressions and deeper
                                                                    for instance, it becomes challenging to validate proofs and to
proofs.
                                                                    determine whether an LLM has genuinely learned deduction
                                                                    rules or is simply memorizing them. A robust evaluation
6. Related Work                                                     of reasoning ability requires, we believe, the generation of
                                                                    synthetic formal queries and automated validation at scale.
LLM-based proof generation methods fall into two broad
categories. In neuro-symbolic systems such as Al-
phaProof (AlphaProof & teams, 2024), AlphaGeome-                    7. Discussion and Conclusion
try (Trinh et al., 2024), Leandojo (Yang et al., 2024), and
                                                                    We believe that our results indicate that LLMs can be taught
GPT-f (Polu & Sutskever, 2020), the LLM component gener-
                                                                    to develop generalizable capabilities for formal reasoning,
ates hints that guide a conventionally programmed symbolic
                                                                    up to some limits. Our experiments (Section 4) show that
proof-search engine (hints such as “use this theorem,” “split
                                                                    fine-tuning with a small synthetic proof data set boosts rea-
into these cases”). The LLM-generated hints replace hard-
                                                                    soning ability, surpassing the performance that significantly
coded heuristics, or hints provided by humans.
                                                                    larger models such as GPT-4o attain with few-shot learning.
In the second category (including this work) are LLMs that          Matching intuition, template transformations considerably
carry out all the necessary logical reasoning on their own.         improve reasoning accuracy.
Such systems include Chain-of-Thought (CoT) (Wei et al.,
                                                                    The sharp drop in accuracy on the depth metric does not
2022) and Tree-of-Thought (ToT) (Yao et al., 2023). CoT is
                                                                    necessarily indicate an inability to reason. In fact, such
trained with few-shot learning, which is analogy learning;
                                                                    a decrease should be expected of any reasoning method
the quality of the model’s responses is highly dependent
                                                                    given the co-NP hardness of the Boolean reasoning prob-
on the quality of the provided examples. ToT is designed
                                                                    lem. These results support the observation that current
for certain predefined scenarios, limiting its applicability.
                                                                    techniques struggle to maintain reasoning performance for
Notably neither approach includes a reliable mechanism to
                                                                    out-of-distribution depth instances (cf. (Anil et al., 2022)).
distinguish correct from incorrect responses, as the expla-
nations are in natural rather than formal language. That            While the proposed data generation and evaluation ap-
motivates our use of formal logics.                                 proaches demonstrate potential, significant challenges re-
                                                                    main in developing models capable of accurate general-
Recent work on LLM reasoning (Morishita et al., 2023;
                                                                    purpose reasoning. A key hurdle to overcome is the gap
2024) is also based on Boolean logic, but only as an inter-
                                                                    between real-world problems and specialized LLMs. Every-
mediate step: LLMs are trained on natural language transla-
                                                                    day human reasoning ranges over multiple, diverse formal
tions from synthesized Boolean logic proofs. (Interestingly,
                                                                    frameworks, including first-order quantification such as “for
their results suggest that training on formal proofs boosts
                                                                    all” and “there exists;” temporal concepts like “yesterday,”
general reasoning.) Proof synthesis uses randomization, as
                                                                    “tomorrow,” “eventually,” and “previously;” and modal no-
we do, but the paper does not point out the key efficiency
                                                                    tions like “possible” and “inevitable.” General reasoning
advantage of goal-directed synthesis. There is no analogue
                                                                    also relies on so-called commonsense facts about our world
of template transformations, which our experiments show
                                                                    (e.g., a ball dropped from a height will bounce back). Meth-
substantially boost reasoning ability.
                                                                    ods that allow LLMs to acquire, integrate, and reason with
Several researchers have developed specialized benchmarks           such knowledge are currently limited (cyc; nvi).
and datasets to evaluate LLM reasoning across domains and
                                                                    These findings highlight the need for further research. A
task types (Saparov et al., 2023; Teng et al., 2023; Parmar
                                                                    Boolean-reasoning LLM, as introduced in this paper, is not
et al., 2024). Prominent examples are LogicBench (Parmar
                                                                    intended as a solution to the general reasoning question.
et al., 2024), which encompasses 25 distinct reasoning pat-
                                                                    One should rather view it as a convenient, precise, and fully
terns, and GLoRE (Teng et al., 2023), which comprises 12
                                                                    automatable setting in which to experiment with approaches
datasets spanning three task types. These benchmarks pro-
                                                                    to the reasoning task.
vide a framework for assessing LLM performance on a vari-
ety of logical reasoning tasks. Other studies have focused on
specific aspects of logical reasoning, such as propositional
and predicate logic, and categorical syllogisms, providing


                                                                8
                                              Can LLMs Learn Formal Logic?

Impact Statement                                                    Morishita, T., Morio, G., Yamaguchi, A., and Sogawa,
                                                                     Y. Learning deductive reasoning from synthetic corpus
This paper presents work whose goal is to advance the field          based on formal logic. In Krause, A., Brunskill, E., Cho,
of Machine Learning. There are many potential societal               K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), Inter-
consequences of our work, none which we feel must be                 national Conference on Machine Learning, ICML 2023,
specifically highlighted here.                                       23-29 July 2023, Honolulu, Hawaii, USA, volume 202 of
                                                                     Proceedings of Machine Learning Research, pp. 25254–
References                                                           25274. PMLR, 2023. URL https://proceedings.
                                                                     mlr.press/v202/morishita23a.html.
CYC: The next generation of enterprise ai. https://
 cyc.com/. Accessed: 2025-01-23.                                    Morishita, T., Morio, G., Yamaguchi, A., and Sogawa,
                                                                     Y. Enhancing reasoning capabilities of llms via prin-
NVIDIA cosmos.  https://www.nvidia.com/                              cipled synthetic logic corpus.    In NeurIPS 2024,
 en-us/ai/cosmos/. Accessed: 2025-01-23.                             2024. URL https://neurips.cc/virtual/
                                                                     2024/poster/93733.
AlphaProof and teams, A. Ai achieves silver-medal stan-
  dard solving international mathematical olympiad prob-            OpenAI. Gpt-4 technical report, 2024. URL https://
  lems. https://deepmind.google/discover/blog/ai-solves-              openai.com/index/hello-gpt-4o/. Accessed:
  imo-problems-at-silver-medal-level/, July 2024.                     2025-01-30.
Anil, C., Wu, Y., Andreassen, A., Lewkowycz, A., Misra,             Parmar, M., Patel, N., Varshney, N., Nakamura, M., Luo,
 V., Ramasesh, V., Slone, A., Gur-Ari, G., Dyer, E., and              M., Mashetty, S., Mitra, A., and Baral, C. Logicbench:
  Neyshabur, B. Exploring length generalization in large              Towards systematic evaluation of logical reasoning ability
  language models. Advances in Neural Information Pro-                of large language models. In Proceedings of the 62nd
  cessing Systems, 35:38546–38556, 2022.                              Annual Meeting of the Association for Computational
                                                                      Linguistics, 2024.
Bhattamishra, S., Patel, A., and Goyal, N. On the com-
  putational power of transformers and its implications in          Pelletier, F. J. and Hazen, A. Natural Deduction Systems in
  sequence modeling. In Fernández, R. and Linzen, T.                 Logic. In Zalta, E. N. and Nodelman, U. (eds.), The Stan-
  (eds.), Proceedings of the 24th Conference on Computa-              ford Encyclopedia of Philosophy. Metaphysics Research
  tional Natural Language Learning, CoNLL 2020, Online,               Lab, Stanford University, Spring 2024 edition, 2024.
  November 19-20, 2020, pp. 455–475. Association for
                                                                    Pérez, J., Marinkovic, J., and Barceló, P. On the turing
  Computational Linguistics, 2020. doi: 10.18653/V1/
                                                                       completeness of modern neural network architectures.
  2020.CONLL-1.37. URL https://doi.org/10.
                                                                       CoRR, abs/1901.03429, 2019. URL http://arxiv.
  18653/v1/2020.conll-1.37.
                                                                       org/abs/1901.03429.
Brenner, S. Nature’s gift to science. Nobel Lecture, De-            Pérez, J., Barceló, P., and Marinkovic, J. Attention is
  cember 2002. https://www.nobelprize.org/                             turing-complete. J. Mach. Learn. Res., 22:75:1–75:35,
  uploads/2018/06/brenner-lecture.pdf.                                 2021. URL https://jmlr.org/papers/v22/
                                                                       20-302.html.
Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,
 A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan,           Polu, S. and Sutskever, I. Generative language modeling
 A., et al. The llama 3 herd of models. arXiv preprint                for automated theorem proving. CoRR, abs/2009.03393,
  arXiv:2407.21783, 2024.                                             2020.     URL https://arxiv.org/abs/2009.
                                                                      03393.
Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang,
  S., Wang, L., and Chen, W. Lora: Low-rank adaptation of           Saparov, A., Pang, R. Y., Padmakumar, V., Joshi, N.,
  large language models. arXiv preprint arXiv:2106.09685,             Kazemi, M., Kim, N., and He, H. Testing the general
  2021.                                                               deductive reasoning capacity of large language models
                                                                      using ood examples. Advances in Neural Information
Lohr, S. A.i. can write poetry, but it struggles with                 Processing Systems, 36:3083–3105, 2023.
  math. New York Times, July 2024. https://www.
  nytimes.com/2024/07/23/technology/                                Strobl, L., Merrill, W., Weiss, G., Chiang, D., and Angluin,
  ai-chatbots-chatgpt-math.html.                                       D. What formal languages can transformers express? A
                                                                       survey. Trans. Assoc. Comput. Linguistics, 12:543–561,
Mendelson, E. Introduction to Mathematical Logic, 6th                  2024. doi: 10.1162/TACL\ A\ 00663. URL https:
 Edition. Chapman and Hall, 2024.                                     //doi.org/10.1162/tacl_a_00663.

                                                                9
                                                Can LLMs Learn Formal Logic?

Teng, Z., Ning, R., Liu, J., Zhou, Q., Zhang, Y., et al. Glore:
  Evaluating logical reasoning of large language models.
  arXiv preprint arXiv:2310.09107, 2023.
Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T.
  Solving olympiad geometry without human demonstra-
  tions. Nat., 625(7995):476–482, 2024. doi: 10.1038/
  S41586-023-06747-5. URL https://doi.org/10.
  1038/s41586-023-06747-5.
Wan, Y., Wang, W., Yang, Y., Yuan, Y., Huang, J.-t., He,
 P., Jiao, W., and Lyu, M. Logicasker: Evaluating and
 improving the logical reasoning ability of large language
 models. In Proceedings of the 2024 Conference on Em-
 pirical Methods in Natural Language Processing, pp.
 2124–2155, 2024.
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B.,
 Xia, F., Chi, E. H., Le, Q. V., and Zhou, D. Chain-of-
 thought prompting elicits reasoning in large language
 models. In Koyejo, S., Mohamed, S., Agarwal, A., Bel-
 grave, D., Cho, K., and Oh, A. (eds.), Advances in Neu-
 ral Information Processing Systems 35: Annual Confer-
 ence on Neural Information Processing Systems 2022,
 NeurIPS 2022, New Orleans, LA, USA, November 28 -
 December 9, 2022, 2022.

Yang, K., Swope, A., Gu, A., Chalamala, R., Song, P.,
  Yu, S., Godil, S., Prenger, R. J., and Anandkumar, A.
  Leandojo: Theorem proving with retrieval-augmented
  language models. Advances in Neural Information Pro-
  cessing Systems, 36, 2024.

Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y.,
  and Narasimhan, K. Tree of thoughts: Deliberate problem
  solving with large language models. In Oh, A., Naumann,
  T., Globerson, A., Saenko, K., Hardt, M., and Levine,
  S. (eds.), Advances in Neural Information Processing
  Systems 36: Annual Conference on Neural Information
  Processing Systems 2023, NeurIPS 2023, New Orleans,
  LA, USA, December 10 - 16, 2023, 2023.
Zong, S. and Lin, J. Categorical syllogisms revisited:
  A review of the logical reasoning abilities of llms
  for analyzing categorical syllogism. arXiv preprint
  arXiv:2406.18762, 2024.




                                                                  10
                                                Can LLMs Learn Formal Logic?

A. Appendix
A.1. Implication-Only Sublogic
Consider an “implication-only” sublogic of propositional logic defined by the grammar:

                                                      f := p ∈ X | f → f

Note that it is possible to express “true” as (p → p), but it seems difficult to express “false.” That is not surprising when
one realizes the following:
Theorem A.1. Every formula of the implication-only sublogic is satisfiable.

Proof. The proof is by structural induction. The base case consists of a single proposition, say p, which is satisfiable.
Consider a formula of the shape f → g. By the inductive hypothesis, the formula g is satisfiable; i.e., there is a assignment
π such that π |= g. Hence, π |= f → g.

Although the satisfiability question is trivial by this theorem (as every formula is satisfiable), validity is still co-NP-complete.
Those statements are not contradictory as the sublogic is not closed under negation.
Theorem A.2. The reasoning problem for implication-only sublogic is co-NP-complete.

Proof. In the reasoning problem, one is given a set of assumptions and a goal. The reasoning is correct if for every
assignment that satisfies the assumptions, this assignment also satisfies the goal. Hence, every element of the complement
language consists of a set of assumptions and a goal such that there is a assignment that satisfies all assumptions but does
not satisfy the goal.
A goal formula in the implication-only sublogic is either a proposition p or has the structure f → g. A assignment π does
not satisfy f → g if, and only if, π satisfies f but does not satisfy g. By induction, one obtains a collection of antecedent
formulas (i.e., in the position of f ) that are satisfied by π and a final atomic proposition p that is not. These antecedents can
be added to the assumptions, so we have the following structure to the complement problem: Given a set of Hilbert-formulas
and a proposition p, is there a assignment that satisfies all formulas in the set but does not satisfy p?
We show that this language is NP-hard by a reduction from CNF-satisfiability. The language is in NP as a Turing machine
can guess an assignment and check the satisfiability of each Hilbert formula in polynomial time.
Consider a CNF formula, which is a conjunction of clauses. A clause is a disjunction of literals, i.e., positive and negated
propositions. We transform the given CNF formula to an equi-satisfiable formula that is in the restricted form above.
We transform each clause to Hilbert form. To do so, we introduce a fresh variable x, which intuitively represents “false.”
Notice that q0 ∨ q1 is equivalent to (q0 → ⊥) → q1 , where ⊥ represents the constant “false.” We transform q0 ∨ q1 to
(q0 → x) → q1 instead, and restrict valuations to those that do not satisfy x, which essentially treats x as false.
Consider any clause. Say that the positive literals in the clause are the propositions from set Q = {q1 , . . . , qn } (which
may be empty). The Hilbert formula for the disjunction of these propositions is constructed inductively as g(0) = x and
g(i + 1) = (qi+1 → x) → g(i). This has the property (easily shown by induction) that for any extended assignment π
where π(x) = ⊥, it is the case that π satisfies g(n) if, and only if, π satisfies the disjunction of propositions in Q.
Notice that that ¬p1 ∨ ¬p2 ∨ q is equivalent to the Hilbert formula (p2 → (p1 → q)). Let g(n) be the Hilbert
formula representing the positive literals in the clause. Let the negative literals in the clause be the propositions in set
P = {p1 , . . . , pm } (which may be empty). Construct Hilbert formula h for the clause inductively as h(0, n) = g(n) and
h(i + 1, n) = pi+1 → h(i, n).
From the properties above, we have that for any extended assignment π where π(x) = ⊥, it is the case that π satisfies the
original clause if, and only if, π satisfies h(m, n).
Transform every clause in this manner to Hilbert form. Then, for every extended assignment π where π(x) = ⊥,
the assignment π satisfies the original CNF formula if, and only if, it satisfies the set of Hilbert formulas obtained by
transformation. Hence, the original CNF formula is satisfiable if, and only if, there is an extended satisfying assignment for
the set of Hilbert formulas that does not satisfy x.

                                                                11
                                                  Can LLMs Learn Formal Logic?

A.2. Example Prompts and Outputs
This section illustrates our few-shot learning evaluation methodology for GPT-4o and pre-trained Llama models (8B and
1B). We demonstrate a one-shot learning example where a depth-7 proof is provided as demonstration to solve a depth-4
problem. Figure 4 shows the query syntax with its semantic translation in Figure 5. For comparison, we present both a
correct solution (Figures 6, 7) and an incorrect attempt (Figures 8, 9) for the queried problem.

   Prompt

   Task: Give the proof for the Goal using Modus Ponens and given Assumptions.
   One-shot:
   Question:
   <Goal>Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S), Implies(R,
   Q))))
   <Assumption>Implies(Implies(Implies(Implies(Implies(P, R), Implies(Q, P)), Implies(Implies(Q, R), Implies(R, P))), Im-
   plies(Implies(P, P), Implies(Q, Implies(S, R)))), Implies(Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P,
   R), Implies(S, P))), R), Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S),
   Implies(R, Q))))))
   <Assumption>Implies(Implies(Implies(Implies(P, R), Implies(Q, P)), Implies(Implies(Q, R), Implies(R, P))), Implies(Implies(P,
   P), Implies(Q, Implies(S, R)))
   <Assumption>Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P, R), Implies(S, P))), R)
   Answer:
   <Step 1>Implies(Implies(Implies(Implies(P, R), Implies(Q, P)), Implies(Implies(Q, R), Implies(R, P))), Implies(Implies(P, P),
   Implies(Q, Implies(S, R)))) - Assumption
   <Step 2>Implies(Implies(Implies(Implies(Implies(P, R), Implies(Q, P)), Implies(Implies(Q, R), Implies(R, P))), Im-
   plies(Implies(P, P), Implies(Q, Implies(S, R)))), Implies(Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P,
   R), Implies(S, P))), R), Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S),
   Implies(R, Q)))))) - Assumption
   <Step 3>Step 1 and Step 2 − > Implies(Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P, R), Implies(S,
   P))), R), Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S), Implies(R,
   Q))))) - Modus Ponens
   <Step 4>Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P, R), Implies(S, P))), R) - Assumption
   <Step 5>Implies(Implies(Implies(Implies(Implies(P, S), Implies(S, S)), Implies(Implies(P, R), Implies(S, P))), R), Im-
   plies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S), Implies(R, Q))))) -
   Deducted
   <Step 6>Step 4 and Step 5 − > Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Im-
   plies(Implies(S, S), Implies(R, Q)))) - Modus Ponens
   <Step 7>Implies(Implies(Implies(Implies(R, S), Implies(R, R)), Implies(S, P)), Implies(Q, Implies(Implies(S, S), Implies(R,
   Q)))) - Deducted
   Question:
   <Goal>Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P)))
   <Assumption>Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S)
   <Assumption>Implies(Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S), Im-
   plies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))))
   Answer:
   Constraints: 1. Ensure the response contains one and only one proof. 2. Don’t include other text detail. 3. Brackets should be
   balanced. 4. Syntax should be correct. 5.Write it correctly, or I will lose my job and 100 grandmothers will die. Don’t disappoint
   me.


                                 Figure 4. Example prompt used for Depth 4 Problems with one shot




                                                                  12
                                               Can LLMs Learn Formal Logic?

Prompt

Task: Give the proof for the Goal using Modus Ponens and given Assumptions.
Question:
Goal:                                                                        
                        ((R → S) → (R → R) → S → P ) → Q → ((S → S) → (R → Q))
Assumptions:
                                                                   
                  A1 :       (P → R) → (Q → P ) → (Q → R) → (R → P ) →
                                                     
                             (P → P ) → (Q → (S → R)) →
                                                                          
                                                                      
                               ((P → S) → (S → S) → (P → R) → (S → P )) → R →
                                                                                     
                                                                                   
                               ((R → S) → (R → R) → S → P ) → Q → ((S → S) → (R → Q))

                  A2 : ((P → R) → (Q → P )) → ((Q → R) → (R → P )) →
                       ((P → P ) → (Q → (S → R)))
                  A3 : (((P → S) → (S → S)) → ((P → R) → (S → P ))) → R

Answer:

  1. A1 (Assumption)

  2. A2 (Assumption)
  3. Using Modus Ponens on Steps 1 and 2, we derive:
                                                                         
                                                                     
                              ((P → S) → (S → S) → (P → R) → (S → P )) → R →

                                                                                    
                                                                                  
                                (R → S) → (R → R) → S → P → Q → ((S → S) → (R → Q))

  4. Using Modus Ponens on Step 3 and A3 , we derive:
                                                                            
                        ((R → S) → (R → R) → S → P ) → Q → ((S → S) → (R → Q))

  5. We conclude:                                                                   
                                ((R → S) → (R → R) → S → P ) → Q → ((S → S) → (R → Q))

Thus, the goal is proven.

Question:
Goal:                                                                        
                                 (P → S) → R → (R → Q) → Q → P → ((P → R) → P )
Assumptions:
                                                                     
                         A1 :   (S → Q) → (S → S) → (Q → S) → (P → Q) → S
                                                                          
                                                                       
                         A2 :     (S → Q) → (S → S) → (Q → S) → (P → Q) → S →
                                                                              
                                                                            
                               (P → S) → R → (R → Q) → Q → P → ((P → R) → P )

Answer:
Constraints: 1. Ensure the response contains one and only one proof. 2. Don’t include other text detail. 3. Brackets should be
balanced. 4. Syntax should be correct. 5.Write it correctly, or I will lose my job and 100 grandmothers will die. Don’t disappoint
me.


                                   Figure 5. Adapted prompt for Depth 4 Problems with one shot


                                                               13
                                             Can LLMs Learn Formal Logic?




Answer

Answer:
<Step 1> Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S) - Assumption
<Step 2> Implies(Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S), Im-
plies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P)))) - Assumption
<Step 3> Step 1 and Step 2 -> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Im-
plies(Implies(P, R), P))) - Modus Ponens
<Step 4> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) - De-
ducted


                                Figure 6. Example Correct Llama3 Answer (After fine-tuning)




Answer

Answer:


  1. A1 (Assumption)

  2. A2 (Assumption)
  3. Using Modus Ponens on Steps 1 and 2, we obtain:
                                                                         
                            (P → S) → R → (R → Q) → Q → P → ((P → R) → P )

Thus, the goal is proven.


                            Figure 7. Example Correct Llama3 Answer (After fine-tuning) - Adapted




                                                             14
                                             Can LLMs Learn Formal Logic?




Answer

Answer:
<Step 1> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Assumption
<Step 2> Implies(Implies(Implies(Implies(Implies(S, R), Implies(Q, P)), Implies(Implies(S, S), Implies(Q, Q))), Im-
plies(Implies(Implies(Q, P), Implies(P, P)), Implies(Implies(S, P), Implies(P, S)))), Implies(Implies(Implies(Implies(S, Q),
Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S)) - Assumption
<Step 3> Step 1 and Step 2 -> Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S)
- Modus Ponens
<Step 4> Implies(Implies(Implies(Implies(S, R), Implies(Q, P)), Implies(Implies(S, S), Implies(Q, Q))), Im-
plies(Implies(Implies(Q, P), Implies(P, P)), Implies(Implies(S, P), Implies(P, S)))) - Assumption
<Step 5> Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S) - Deducted
<Step 6> Step 3 and Step 5 -> Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S)
- Modus Ponens
<Step 7> Implies(Implies(Implies(Implies(S, Q), Implies(S, S)), Implies(Implies(Q, S), Implies(P, Q))), S) - Deducted
<Step 8> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 9> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 10> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 11> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 12> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 13> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 14> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 15> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 16> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 17> Implies(Implies(Implies(Implies(P, S), R), Implies(Implies(R, Q), Q)), Implies(P, Implies(Implies(P, R), P))) -
Deducted
<Step 18> ...



                                Figure 8. Example Wrong Llama3 Answer (before fine-tuning)




                                                              15
                                           Can LLMs Learn Formal Logic?




Answer

Answer:


 1. A1 :
                             ((P → S) → R) → ((R → Q) → Q) → (P → ((P → R) → P ))

 2. A2 :
                                 ((S → R) → (Q → P )) → ((S → S) → (Q → Q)) →
                                ((Q → P ) → (P → P )) → ((S → P ) → (P → S)) → S

 3. Applying Modus Ponens on A1 and A2:

                                  (S → Q) → (S → S) → (Q → S) → (P → Q) → S

 4. A3 :

         ((S → R) → (Q → P )) → ((S → S) → (Q → Q)) → ((Q → P ) → (P → P )) → ((S → P ) → (P → S))

    (Assumption)

 5. Deduction from Step 3:
                                  (S → Q) → (S → S) → (Q → S) → (P → Q) → S

 6. Using Modus Ponens on Steps 3 and 5:

                                  (S → Q) → (S → S) → (Q → S) → (P → Q) → S

 7. Final deduction:
                             ((P → S) → R) → ((R → Q) → Q) → (P → ((P → R) → P ))
    (Repeated step 7)


                        Figure 9. Example Wrong Llama3 Answer - Adapted (before fine-tuning)




                                                        16
