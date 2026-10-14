                                                                A Solver-in-the-Loop Framework for Improving LLMs
                                                                on Answer Set Programming for Logic Puzzle Solving
                                                                      Timo Pierre Schrader1,2 , Lukas Lange1 , Tobias Kaminski1 ,
                                                                             Simon Razniewski3 , Annemarie Friedrich2
                                                                                       1
                                                                                           Bosch Center for AI, Renningen, Germany
                                                                                               2
                                                                                                 University of Augsburg, Germany
                                                                                             3
                                                                                               ScaDS.AI & TU Dresden, Germany
                                                                                                  timo.schrader@de.bosch.com

                                                                     Abstract                                    on prompt engineering or create complex planning and rea-
arXiv:2512.17093v1 [cs.AI] 18 Dec 2025




                                                                                                                 soning systems (Yang, Chen, and Tam 2024; Stein et al.
                                           The rise of large language models (LLMs) has sparked inter-
                                           est in coding assistants. While general-purpose programming           2023; Vyas et al. 2024). Yet, for many programming lan-
                                           languages are well supported, generating code for domain-             guages, LLM-based generations remain understudied.
                                           specific languages remains a challenging problem for LLMs.               In this work, we focus on Answer Set Programming (ASP,
                                           In this paper, we focus on the LLM-based generation of code           Gelfond and Lifschitz 1988; Marek and Truszczyński 1999),
                                           for Answer Set Programming (ASP), a particularly effective            which can be used for finding solutions to combinatorial
                                           approach for finding solutions to combinatorial search prob-          search problems. ASP is a well-known and powerful ap-
                                           lems. The effectiveness of LLMs in ASP code generation is             proach for declarative problem solving. It offers an expres-
                                           currently hindered by the limited number of examples seen             sive input language, provides well-optimized solvers, and
                                           during their initial pre-training phase.
                                                                                                                 has been applied to a wide range of industrial problems such
                                           In this paper, we introduce a novel ASP-solver-in-the-loop            as generating software test cases, robotics, and configuration
                                           approach for solver-guided instruction-tuning of LLMs to ad-
                                           dressing the highly complex semantic parsing task inherent
                                                                                                                 problems (Falkner et al. 2018).
                                           in ASP code generation. Our method only requires problem                 ASP is highly suited for solving many real-life problems,
                                           specifications in natural language and their solutions. Specif-       such as scheduling in factory plants, configuring electrical
                                           ically, we sample ASP statements for program continuations            circuits (ECUs), or assignment problems as shown in Fig-
                                           from LLMs for unriddling logic puzzles. Leveraging the spe-           ure 1. These problems and their constraints can often be de-
                                           cial property of declarative ASP programming that partial             scribed by domain experts in natural language. However, do-
                                           encodings increasingly narrow down the solution space, we             main specialists often lack the necessary ASP programming
                                           categorize them into chosen and rejected instances based on           skills. Out-of-the-box LLMs frequently struggle to solve
                                           solver feedback. We then apply supervised fine-tuning to train        these problems using chain-of-thought reasoning, particu-
                                           LLMs on the curated data and further improve robustness
                                           using a solver-guided search that includes best-of-N sam-
                                                                                                                 larly as problem size and complexity grow. Neuro-symbolic
                                           pling. Our experiments demonstrate consistent improvements            solutions that combine LLMs and symbolic solvers are a
                                           in two distinct prompting settings on two datasets.                   promising alternative (Olausson et al. 2023; Schrader et al.
                                                                                                                 2024). These systems translate fine-grained natural language
                                         Code — https://bos.ch/1qzx1jj                                           statements into executable and semantically correct code for
                                                                                                                 which a solver computes the solution.
                                                                                                                    First explorations addressing ASP code generation in-
                                                                 Introduction                                    clude the LLASP dataset (Coppolillo et al. 2024) that pro-
                                         One of the primary productive applications of large language            vides ASP statements only in isolation without a larger con-
                                         models (LLMs) is currently their use as coding assistants               textual problem. Ishay, Yang, and Lee (2023) engineer a
                                         (Jiang et al. 2024; Gu 2023; Ugare et al. 2024), support-               highly specific prompt pipeline for a particular dataset for
                                         ing software developers by taking over tedious and repeti-              commercial GPT-based models only. For processing sensi-
                                         tive programming workflows. However, current systems typ-               tive data on-premise, the use of open-weight LLMs is an
                                         ically target popular and general-purpose programming lan-              alternative. Yet, as we show in this paper, state-of-the-art
                                         guages such as JavaScript, C++, and Python.                             open-weight LLMs still mostly fall short on producing
                                            Many real-life problems, however, require the use of                 correct ASP encodings, even when being provided with
                                         domain-specific programming languages tailored towards                  strong prompt guidance. Our goal is to improve trainable
                                         specific problem types. Various studies on LLM-based code               state-of-the-art LLMs on the task of ASP code generation.
                                         generation have been conducted on programming languages                    In this paper, we present a novel and efficient method that
                                         such as PROLOG or PDDL (planning domain definition lan-                 uses an ASP solver in the loop both for creating high-quality
                                         guage, McDermott et al. (1998)). Existing approaches rely               training data and for guiding the generation process with a
                                         Copyright © 2026, Association for the Advancement of Artificial         solver-based reward. Our ultimate goal is to develop LLMs
                                         Intelligence (www.aaai.org). All rights reserved.                       that excel at ASP coding for assignment problems. We focus
Figure 1: We use the feedback from an ASP solver to assess LLM-generated ASP statements. (1) We take the problem de-
scription and let the LLM output N alternatives for it (generate part of an ASP encoding). We then judge the correctness of
these encodings using an ASP solver which checks for errors as well as for the expected answer size. (2) We incrementally
combine the constraints of the problem into larger inputs to the LLM and obtain longer partial encodings (check part of an
ASP encoding). (3) The ASP solver judges the correctness of each partial encoding containing the base encoding and at least
one constraint. (4a) For training, we select instances from a chosen set that corresponds to instances with positive solver feed-
back. (4b) During inference, where the ground truth is not known, we score every partial encoding using a reward function
that captures errors as well as the number of produced answer sets with preference for a lower number of returned answers.
Additionally, we implement fallback mechanisms that regenerate encodings or backtrack in the graph if all alternatives were
judged with a negative score.


on solving grid-based puzzles as a proxy task since they re-       to rank a set of N alternatives for the same input and triggers
flect assignment problems that are one of the main use cases       fallback mechanisms in case of errors.
of ASP. The LLM-generated ASP encodings are automat-                  We evaluate our trained models with and without reward-
ically evaluated by an ASP solver and classified as either         based inference for solving logic puzzles in two distinct set-
chosen or rejected. Our solver-in-the-loop setup leverages         tings: First, in a few-shot setting, we only provide basic in-
the specific properties of ASP as a declarative approach, i.e.,    structions as well as a few examples in the input prompt.
that the order in which rules and constraints are added does       This reflects a realistic setting in which the type of problem
not alter the semantics of the final encoding. Hence, it al-       and dataset format is not clearly defined beforehand. Sec-
lows for fine-grained evaluation of partial encodings re-          ond, a prompt-engineered setting (Ishay, Yang, and Lee
gardless of the order in which they are added by check-            2023) assumes that everything about the input problem and
ing if the ground truth solution can still be derived from         how it could be generally modeled in ASP is already fully
the partial encoding. We also make use of the fact that ASP        known.
encodings are usually divided into clearly defined generate
                                                                      Our contributions are as follows: (1) We demonstrate
and check parts. This enables us to (re-)combine partial ASP
                                                                   that state-of-the-art open-weight LLMs struggle with ASP
encodings and to verify intermediate generation steps by
                                                                   code generation, even under highly prompt-engineered con-
checking for both syntax errors as well as for a reduction of
                                                                   ditions. (2) We create silver-standard training data by sam-
the answer space after each added constraint. This specific
                                                                   pling partial ASP encodings from an LLM for given com-
ASP property allows for a substantially more fine-grained
                                                                   binatorial problems and filtering them based on feedback
evaluation than evaluating code of other programming lan-
                                                                   from an ASP solver that includes whether the encoding is
guages, e.g., in Python, semantic feedback from the inter-
                                                                   erroneous or whether the ground truth answer can be de-
preter can only be obtained for a full block without being
                                                                   rived from it. (3) We show that applying SFT on the chosen
able to check intermediate steps (Peng et al. 2024).
                                                                   instances improves the performance of open-weight LLMs
  Using the chosen continuations, we apply supervised fine-        of various sizes in generating ASP encodings for grid-based
tuning (SFT) via causal language modeling. Additionally,           puzzles, especially for problems of higher complexity in
we leverage the same solver-in-the-loop setup to further im-       both prompt settings. (4) We demonstrate that the solver can
prove the ASP code generation during test-time. We intro-          steer the ASP generation process successfully during infer-
duce a novel reward function that leverages solver feedback        ence.
             Answer Set Programming                               Task Definition
ASP, a form of declarative programming focusing on dif-           The problems addressed in this paper are grid-based puz-
ficult, primarily NP-hard search problems, is based on the        zle instances of the form I = {D, E, H, S}. D refers to the
stable model semantics proposed by Gelfond and Lifschitz          natural language problem description, E to a set of entities
(1988). Our short introduction follows Lifschitz (2008). The      and their types (e.g., dogs, persons, and times), H to a set
purpose of ASP is to find answer sets consisting of sets of in-   of natural language hints (or clues) that constrain the an-
stantiated first-order atoms (e.g., walk(beagle, eva,             swer space (“Clue: The beagle is walked one hour before the
8)) that satisfy all given rules and constraints. We exem-        poodle.”), and S refers to the correct solution assignment.
plify ASP with the puzzle of matching dogs with their walk-       To solve this, the LLM MASP has to parse the input prob-
ers and times for walking (cf. Figure 1).                         lem {D, E, H} specified as natural language text into a valid
   Rules define if-then statements written in PROLOG-style        ASP encoding Π that contains ASP encodings for entities,
syntax using n-ary predicates. The right-hand side (rule          (choice) rules, and constraints. A solver will then compute
body) is the premise and the left-hand side the conclusion        the solution S given Π. In the following, we stick to the no-
(rule head). “If the beagle is walked by Tom, then the golden     tations of Lifschitz (2008), using Γ to denote a partial ASP
retriever will be walked by Eva at 9 am.” is encoded as:          encoding that contains a proper subset of the ASP code in
   walk(golden, eva, 9) :-                                        Π, i.e., solution(Π = (Γ1 ∪ · · · ∪ Γn )) = S.
                walk(beagle, tom, _).
                                                                  Sampling Trajectories
Constraints eliminate undesired solutions by disallowing
certain combinations of atoms to be true simultaneously.          We define a trajectory T to be an alternating sequence of
They only have a rule body, i.e., no head. A constraint re-       natural language inputs and ASP statements. A trajectory
quires at least 1 atom to evaluate to false. For example,         T starts with a prompt PD,E comprising general informa-
“Anna walks her dog later than Eva.” is encoded as:               tion on ASP,1 the textual problem description D, and the
 :- walk(_, anna, T1), walk(_, eva, T2),                          set of entities E. We feed PD,E into the LLM MS to ob-
    not T1 > T2.                                                  tain ASP code ΓC,E , where C refers to the choice rule that
                                                                  initially generates all potential solutions representing the
Unlike constraints, choice rules generate answer set can-         problem instance, which is then appended to the trajec-
didates instead of filtering them. Assuming that the ASP          tory. Next, a natural language hint hi ∈ H is appended to
program already contains atoms specifying a set of entities       this trajectory and MS is prompted again to obtain a par-
(here: dogs, persons, and times), the following rule states       tial encoding Γi . This results in trajectories of form T =
that “For each time T, some dog D is walked by some person        {PD,E , ΓC,E , h1 , Γ1 , h2 , Γ2 , . . . , hn , Γn } with n being the
P.” The statement dog(beagle;golden;bernese) is                   number of hints of the problem.
an ASP shorthand for dog(beagle). dog(golden).
dog(bernese).                                                     Classification of ASP Encodings
  person(tom;eva;anna).                                           After processing k of the n hints, we obtain a trajectory Tk
  dog(beagle;golden;bernese).
                                                                  that contains k+1 ASP encodings (one for entities and choice
  time(8;9;10).
                                                                  rule and k for hints). We now combine all k+1 ASP encod-
  1 { walk(D, P, T) : dog(D), person(P) } 1                       ings into the partial encoding ΓC,E ∪ Γ1 ∪ . . . Γk and use
     :- time(T).                                                  the solver to compute its solution. We sample 5 completions
                                                                  from MS for each step k simultaneously to get a diverse
Solutions in ASP. An ASP solver calculates all answer sets,       set of ASP encodings for the same input. Preliminary ex-
corresponding to minimal sets of derivable atoms that are         periments showed that a temperature t = 0.8 for sampling
valid interpretations of all rules. More technically, a solu-     provides a good balance between chosen and rejected re-
tion of an ASP program Π is a special truth assignment to         sponses. We then use an ASP solver to evaluate if the partial
all atoms that occur in the grounding of the program, i.e., a     encoding Γk generates a solution that comprises the ground
stable model, and the effect of adding a constraint to a pro-     truth answer set S. We consider Γk as a chosen response to
gram can lead to its elimination, i.e., constraints reduce the    input Tk = {PD,E , ΓC,E , h1 , Γ1 , h2 , Γ2 , . . . , hk } if the solu-
set of solutions monotonically.                                   tion of the partial program ΓC,E ∪ Γ1 ∪ . . . Γk comprises the
                                                                  ground truth solution. If it produces only wrong answer sets,
                                                                  becomes unsatisfiable, or errors and warnings are returned
             Instruction Tuning for ASP                           by the solver, we consider Γk as rejected.
We present a novel instruction-tuning method for ASP code
generation in LLMs. We prompt an LLM MS to generate                  1
                                                                       This includes an instruction of how different variants of logical
ASP code and classify the results into “chosen” and “re-          OR works in ASP, a hint to introduce helper predicates to perform
jected” samples using an ASP solver. The chosen data can be       arithmetics (e.g., on dates), a high-level explanation of the steps
used with causal language modeling to train an ASP-specific       required to solve a grid-based puzzle in ASP as well as a basic
model MASP based on the reference model MS .                      choice rule.
Training Data Generation                                              trade-offs in favor of future rewards (cf. Sutton, Barto et al.
We generate trajectories using depth-first search. At each            (1998)). Similar to creating ASP encodings for training, we
step k, we consider at most two chosen responses. For each            first instruct MASP to generate N alternatives for the par-
of them, we continue at step k+1 recursively until there are          tial encoding ΓC,E that encodes entities and the choice rule.
no hints left. To form pairs from both chosen and rejected            We then select and keep the alternative receiving the high-
responses at each step k, we take the Cartesian product be-           est reward according to fr . We use a special version of fr
tween both sets. To put emphasis on instances that are dif-           for evaluating the ΓC,E encodings, by replacing the recipro-
                                                                                  1
ficult for current LLMs, we keep only instances for which             cal factor M   with a strict check whether the output contains
                                                                           m−1
there are at least one chosen and one rejected alternative. If        (n!)       answer sets for an m×n grid puzzle which is differ-
we have a mix of chosen and rejected responses, we obtain             ent from 1N E in that it is dynamically determined based on
either 1×4 or 2×3 preference pairs in each step. If there are         the size of the input problem. This corresponds to the num-
only chosen or only rejected responses, the trajectory gener-         ber of all theoretically possible answer combinations when
ation is continued at the next step without creating prefer-          disregarding the constraints. Next, for every hint hj ∈ H
ence pairs. If all responses are rejected, the input to the next      in sequential order, we generate N alternatives and append
step becomes {PD,E , ΓC,E , h1 , Γ1 , . . . , hk−1 , Γk−1 , hk+1 },   them to the partial encoding that contains all previously se-
i.e., the rejected response and the hint prompt causing it are        lected encodings and judge all N partial encodings again
removed. This is possible because the hints in grid-based             by fr . At each step, we select the partial encoding with the
puzzles do not refer to each other.                                   highest score and continue until we arrive at the full encod-
                                                                      ing Π. We make use of two recovery mechanisms when all
Model Training                                                        new generations have negative rewards: (1) Re-generation:
The chosen instances can be used to train LLMs using SFT              We let MASP generate 2 × N additional alternatives if all
with causal language modeling. Alternative training meth-             initial N alternatives for the current input were judged neg-
ods, such as DPO, could also be used to perform prefer-               ative by fr . (2) Backtracking: We jump back to the previous
ence alignment using pairs of chosen and rejected instances.          hint with maximum reward that had more than one alterna-
However, our initial experiments showed that SFT works                tive and continue with this as our new partial encoding. We
slightly better than DPO in this context.                             then restart to generate all successive hints.

            Test-Time Sampling for ASP                                                   Experimental Setup
In this section, we explain our best-of-N sampling method             Evaluation Metrics and Datasets
that can be used during test-time on trained and untrained            We report the accuracy of the models based on how often
LLMs. It is based on a novel solver-grounded reward func-             their output exactly matches the correct answer. ASP encod-
tion for LLMs that helps to generate correct ASP encodings            ings that produce more than one solution in the end are con-
more reliably.                                                        sidered wrong in our strict evaluation setup as the consid-
                                                                      ered problems only have unique solutions. One issue when
Reward Function                                                       converting the problem into ASP is the ambiguity of string
The reward function fr maps an encoding Γ and the number              representation in the answer sets and the evaluation with ac-
M ∈ N of answer sets produced by Γ to a floating point                curacy when comparing to the ground truth solution (e.g.,
reward r ∈ R that aims to judge the quality of Γ:                     spaces, underscores, and other ambiguities). To automati-
                                                                      cally evaluate the predicted answer sets, we implement a
                       1                                              Levenshtein heuristic that acts as fallback for fuzzy match-
        fr (Γ, M ) =     − 1E (Γ) − 1U (Γ) − 1N E (Γ)
                       M                                              ing if the answer set does not exactly match the ground truth
   Usually, with every hint in a logic puzzle, the number of          representation.
possible answers is either reduced or stays the same. There-             We work with LogicPuzzles (Mitra and Baral 2015) and
fore, fr rewards stricter generations. 1 are binary indicator         GridPuzzles (Tyagi et al. 2024). LogicPuzzles is a collec-
variables checking Γ for undesired properties. All three con-         tion of 124 grid-based puzzles (50 train and 74 test).2 All
tribute negatively to the reward:                                     puzzles are of size 3×4, i.e., there are 3 entity types, each
   1E indicates whether there are any errors or warnings              with 4 instances (e.g., 4 dogs, 4 owners, 4 countries) where
     when trying to solve Γ.                                          each entity must be assigned once. This results in 4 triples
   1U refers to unsatifiability, i.e., there is no warning or er-     representing a unique solution (e.g., each dog is assigned to a
     ror, but also no answer set.                                     different owner from a different country). GridPuzzles intro-
   1N E indicates that a manually specified maximum num-              duces different puzzle sizes (3×4, 3×5, 4×4, 4×5, 4×6)
     ber of answer sets is exceeded. This avoids out-of-              and difficulty levels (easy, medium, hard). We use this
     memory issues in cases where broken encodings lead               dataset only for evaluation.
     to combinatorial explosions.                                        2
                                                                           We noticed that in the official dataset release, 26 puzzles from
                                                                      the train set are also part of the test set. In order to evaluate the
Sampling Procedure                                                    trained models on unseen data only, we remove these 26 instances
Our test-time method is based on greedy search, i.e., it aims         from our test set. For comparability with prior work, we also report
at maximizing the current reward and does not perform                 the evaluation on the full data in the appendix.
Models                                                               and 1.060 from Qwen. Sampling ASP encodings from the
We train and evaluate four open-weight models from                   8B models did not yield sufficient results as they initially
two model families: Llama-3.3 70B and Llama-3.1 8B3                  lack ASP knowledge and hence do not generate useful re-
(Grattafiori et al. 2024) as well as Qwen3 32B and Qwen3             sponses.
8B (Qwen-Team 2025). We disable the thinking mode in-
troduced in the Qwen3 model family. For the two bigger               Settings
models, we sample distinct training data using our proposed          To test the impact of injecting ASP coding knowledge into
method and fine-tune them separately on their own part. To           LLMs, we compare two settings: First, we use a single-
train the 8B models, we use the SFT data drawn from Llama            prompt two-shot (2S) prompt with limited engineering ef-
3.3 70B as it yields a more diverse range of statements than         fort to generate the ASP program hint-wise as during train-
Qwen3 32B. Additionally, since these smaller models ini-             ing data generation. For this, we provide two dataset-specific
tially possess almost no ASP coding skills, we supplement            examples and explain choice rules and different forms of
the training data by adding the same number of instances             logical OR constructs in ASP. We randomly select parts
from the LLASP dataset (Coppolillo et al. 2024) on top               of two instances for GridPuzzles as there is no training
of our data. The LLASP dataset is a collection of single-            split available. Second, we plug our models into an existing
statement building blocks (e.g., transitive closures).               PromptPipeline (PP) (Ishay, Yang, and Lee 2023) consist-
   We further compare our ASP models to the distilled                ing of 6 prompts specifically tailored to LogicPuzzles. This
variants of DeepSeek-R1 (DeepSeek-AI 2025). They are                 resembles a major prompt engineering effort for tailored
prompted to perform reasoning without making use of ASP.             ASP program generation to a particular dataset. Whereas
We use the prompt setup of Tyagi et al. (2024) to per-               our two-shot setting directly requests the LLM to generate
form reasoning without an ASP solver. While we mainly                ASP encodings for each natural language input, the pipeline
focus on ASP coding skills, we also investigate how our              uses the following six steps: (1) structured generation of
neuro-symbolic method performs compared to reasoning                 constants, (2) formatting constants so that they are suited
language models (RLMs) on these logic reasoning tasks. Fi-           for ASP syntax, (3) generation of predicates that are used
nally, we test our new inference method on one of the latest         to form the relations between the entities, (4) formulation
closed-source models, GPT-4.1-mini (version 2025-04-14)              of the choice rule, (5) rewriting natural language constraints
and show that our best-of-N sampling method also improves            if they contain for example complex logical OR constructs,
closed-source models without the need for prior training.            and (6) translating all natural language constraints into ASP
   We train LoRA adapters (Hu et al. 2022) on top of the             at once. As only the sixth and last step produces one com-
base LLMs. We use 2 to 4 Nvidia H200 GPUs using Deep-                plete ASP encoding, a fine-grained intermediate analysis us-
Speed stage 3 (Rasley et al. 2020). The batch size is set to         ing the solver is not possible.
4 per GPU used during training and the learning rate is set
to 5e−5 for all models, which is a commonly used value                                Results and Analysis
for SFT. The parameters are kept in bfloat16 format. LoRA
rank r and α are both set to 128. All models are trained for         Two-Shot Parsing
at most 10 epochs to keep computation feasible.                      The two upper rows of Table 1 display our main results
   For inference, we use both Nvidia and Intel Gaudi 2 ac-           on LogicPuzzles and GridPuzzles in the single-prompt pars-
celetor cards in combination with vllm (Kwon et al. 2023).           ing setup. All our SFT-trained models outperform their un-
We use clingo v.5.7.1 (Gebser et al. 2017) as ASP solver.            trained counterparts on the task of ASP generation, empha-
We set N = 5 with a temperature of T = 1.0 for the test-             sizing the necessity of fine-tuning current LLMs on under-
time experiments to get a higher variety of outputs. Due to          represented programming languages like ASP. Especially
the higher variety of outputs, we average test-time runs over        the 70B Llama heavily benefits from the training with two-
5 distinct runs in the case of LogicPuzzles. To ensure com-          digit improvements in all settings. For both 8B models,
putational feasibility, we limit the number of backtracking          which do not possess usable ASP skills initially, we observe
steps to 5 for LogicPuzzles and to 1 for GridPuzzles.                a notable increase in performance of approximately 20pp.-
                                                                     25pp. (percentage points) on LogicPuzzles and 10pp. on av-
Training Data Statistics                                             erage on GridPuzzles after SFT-based training on data auto-
We use the train split of LogicPuzzles to generate ASP train-        matically drawn from Llama-3.3 70B. This indicates that our
ing data. We request the LLMs to generate N = 5 alter-               pipeline generates data with qualitative training signals such
natives per input. In the case of Llama-3.3 70B, we get 3.7          that small LLMs can learn the essence of ASP coding as
chosen responses and 1.3 rejected responses on average with          well. Similar performance increases can also be observed for
a standard deviation of 1.82. Qwen3 32B yields 3.3 chosen            the much harder GridPuzzles dataset on which the models
and 1.7 rejected responses on average with a standard devia-         were not specifically trained, i.e., our method demonstrates
tion of 2.04. This indicates that during sampling, Llama pro-        strong transferability to more complex problem settings.
duces a slightly higher number of correct instances, whereas            Effect of Test-time Search. Next, we apply our reward-
Qwen is not yet at the same level of ASP coding skills. Fi-          based search function to all SFT-trained models with N = 5.
nally, we end up with 1.546 training instances from Llama            We observe great improvements for all models over greedy
                                                                     sampling with T = 0.0 (and N = 1). Moreover, our test-
   3
       At the time of publication, there is no Llama-3.3 8B model.   time method leads to competitive performance compared to
   Setup              Llama-3.3 70B         Llama-3.1 8B         Qwen3 32B                          Qwen3 8B                    DeepSeek Variants
             w/o ASP Base SFT +TT Base SFT +TT Base SFT +TT Base SFT +TT                                               Llama 70B Qwen3 32B Llama 8B
2S LogicP.       27.0     31.1 55.4 66.8   0.0   21.6 46.8 17.6 23.0 50.3                         0.0     24.3 43.2      59.5          62.1         24.3
   GridP.        9.1       8.0 16.8 23.7   0.0    8.8 16.8 18.2 21.9 33.9                         0.0     12.4 21.2      21.9          18.2          4.4
PP LogicP.        -       56.8 78.4   -    0.0   0.0    -   51.4 67.6                    -    31.1 24.3           -       -             -             -
   GridP.         -       33.9 55.5   -    0.0   0.0    -   27.7 37.2                    -     9.1 16.1           -       -             -             -

Table 1: Accuracy of all models on both datasets in both the single-prompt parsing (2S) and prompt pipeline (PP) setting. All
test-time methods (TT) are averaged across five runs. Underlined scores denote the best score within the category, bold scores
the overall best results. Every row corresponds to one combination of prompt setting and dataset.


 Model Variant SFT Seq Reg Back N LogicP.                   ∆                            80
                                                                                                                                              Best-of-25
 Llama-3.3 70B                              1    31.0       –                                 Best-of-5                   Best-of-10
 +SFT                 ✓                     1    55.4     0.0




                                                                      Accuracy (%)
  +Seq                ✓   ✓                 5    62.7    +7.3                            60
   +Reg               ✓   ✓    ✓            5    64.6    +9.2                                                                    DS-Llama-70B
   +Back              ✓   ✓           ✓     5    62.7    +7.3                                 SFT
   +Both (TT)         ✓   ✓    ✓      ✓     5    66.8   +11.4
                      ✓   ✓    ✓      ✓    10    65.1    +9.7                            40
                      ✓   ✓    ✓      ✓    25    69.2   +13.8                                           Base
 GPT-4.1-mini                              1     39.2     0.0
  +Seq                    ✓                5     55.4   +16.2                            20
                                                                                              0                2,000     4,000         6,000         8,000
Table 2: Ablation study results on LogicPuzzles. ∆ shows                                                  Number of generated output tokens
improvement over +SFT (Llama) or the base model (GPT).
(Reg = regeneration, Back = backtracking, Seq = best-of-N             Figure 2: Comparison of generated output tokens in relation
w/o regeneration and backtracking)                                    to accuracy on LogicPuzzles between the DeepSeek Llama-
                                                                      70B, the untrained Llama-3.3 70B as well as the SFT-tuned
                                                                      one in combination with reward-based inference.
the state-of-the-art RLMs: ASP-tuned Llama models show
strong performance when compared to their Deepseek coun-
terparts. We also observe similar tendencies for GridPuzzles.         search. This highlights the value of our solver-in-the-loop
   Sampling multiple alternatives with a higher temperature           setup for a wider range of LLMs.
and judging them independently using our reward function                 Cost Comparisons. Figure 2 further provides a calcula-
fr greatly increases the robustness and reduces the number            tion of the generated output tokens per instance on average
                                                 1                    in relation to the accuracy on LogicPuzzles for the RLM
of semantically wrong (captured by the factor M    ) and erro-
neous partial ASP encodings as seen by the increased accu-            DeepSeek Llama 70B compared to the ASP-based setups.4
racy. This improved performance indicates that there is still         First, we can see that our trained Llama 70B outperforms the
insecurity within the model when it comes to ASP coding               untrained base version by 24.4pp. while keeping the same
and that sampling multiple alternatives mitigates this issue.         amount of produced output tokens. Furthermore, the num-
   A detailed study on the different components used in               ber of generated output tokens scales linearly with N . We
our test-time methods is shown in Table 2. Re-generation              conclude that for increasing values of N , the number of pro-
shows slight improvements of 2pp. over basic best-of-5 sam-           duced output tokens is still in a feasible range. Thorough
pling. However, the combination of re-generation and back-            trade-off considerations for inference costs, however, must
tracking demonstrates a robust improvement by over 3pp.               be taken into account for determining the best value for N .
This underlines the necessity of both fallback mechanisms:            Finally, we can see that the number of produced output to-
Sometimes regenerating 2 × N alternatives is already suffi-           kens of the RLM is in the range of our best-of-10 model
cient to recover from errors, whereas backtracking allows for         while performing worse on LogicPuzzles. We can conclude
deeper changes. Table 2 also shows how the number of gen-             that a value of N = 5 provides a good trade-off between
erations N influences our best-of-N sampling method. We               cost efficiency and task performance in our setup.
observe bigger improvements, achieving up to 69% accuracy
for N = 25, which shows that there is a valuable trade-off                           4
                                                                          We use the number of generated output tokens as a general
between inference runtime and accuracy on the problems.               proxy for compute costs, as this greatly influences generation speed
Finally, for the closed-source GPT-4.1-mini without any spe-          and costs - two of the main factors when deciding for LLMs. We
cific fine-tuning for ASP, we still observe a performance             do not count input tokens because this is highly problem-specific
improvement of 16.2pp. when used with our reward-based                and depends mainly on the input prompt.
ASP-tuned Backbones for PromptPipeline                            prompting pipeline for GPT models for solving the Log-
                                                                  icPuzzles dataset (Brown et al. 2020; OpenAI et al. 2024).
The bottom row of Table 1 shows our ASP models plugged
                                                                  Combining this pipeline with our ASP-tuned models outper-
into the 6-step PromptPipeline of Ishay, Yang, and Lee
                                                                  forms prior work on GridPuzzles as well.
(2023) to test instruction-following capabilities. We find that
fine-tuning the models also improves their instruction fol-       Generating data from feedback. Datasets can be labeled
lowing capabilities w.r.t. producing proper ASP encodings.        either manually or in an automated way (Xiao et al. 2024).
This shows that ASP-specific fine-tuning using few-shot           The HelpSteer dataset (Wang et al. 2023; Dong et al.
prompts also generalizes to different settings that follow dif-   2023) is an example for human annotations, while Li et al.
ferent approaches by instructing the model to first perform       (2023) employ GPT-4V to automatically judge the outputs
intermediate rewrite steps before finally producing the ASP       of vision-language models. Lai et al. (2024) use GPT-4 to
encoding.                                                         automatically identify faulty steps in mathematical reason-
                                                                  ing chains. We are not aware of any prior work generating
                                                                  ASP training data from a solver-in-the-loop setup.
Discussion
                                                                  Test-time methods. Recent test-time methods fall into three
One important strength of our method is that it requires no       categories (Dong, Teleki, and Caverlee 2024): Independent
additional human annotations as it samples ASP statements         self-improvement refers to intervening in the generation pro-
from LLMs and automatically computes a reward or cate-            cess of frozen-parameter LLMs (Lu et al. 2022; Ning et al.
gorizes them into chosen and rejected. Yet, this also implies     2024). Context-aware self-improvement describes adapta-
that even the chosen instances might not be perfect. We have      tions to prompts by enriching the input to the model, e.g.,
shown that recent LLMs, despite possessing limited ASP            via chain-of-thought prompting (Wei et al. 2022). Methods
coding skills, are able to produce initial ASP encodings that     using feedback from additional expert (Zeng et al. 2024) or
facilitate our successful self-supervised training data gener-    reward models (Deng and Raffel 2023) are called model-
ation method. Furthermore, our experiments show that best-        aided self-improvement methods. Our approach belongs to
of-N sampling using a solver-in-the-loop setup mitigates sta-     the third category.
bility issues of the ASP generation process with LLMs by
filtering erroneous ASP encodings from a set of N alterna-
tives during inference time.
                                                                                Conclusion and Outlook
                                                                  In this paper, we have presented a novel method for increas-
                      Related Work                                ing the performance of LLMs on the task of ASP code gen-
                                                                  eration. We have shown that an external ASP solver can be
We review related work on neuro-symbolic systems with a           used to generate high-quality training data for instruction
focus on systems in which LLMs generate structured repre-         tuning in a fully automated fashion as well as to provide
sentations and solvers compute solutions (Kautz 2022), ASP        guidance during inference to filter out faulty ASP encodings.
code generation, data generation with feedback incorpora-         We observe consistent improvements for multiple models af-
tion, and test-time methods.                                      ter training in two distinct prompting settings, demonstrating
Semantic parsing in neuro-symbolic systems. Inducing              that our training method integrating solver feedback scales
explicit representations of meaning from text relates to the      to a wider range of LLMs on assignment problems of dif-
task of semantic parsing (Hendrix et al. 1978; Delmonte           ferent sizes and difficulties. Furthermore, we showed that
1990; Baud et al. 1998). Recently, LLMs have been used for        solver feedback incorporated during test-time can further
semantic parsing into logic programming languages. LINC           improve the robustness of the ASP generation process as it
(Olausson et al. 2023) translates natural language premises       is used to find the best combination of partial encodings by
and conclusions into symbolic representations for a theorem       ranking them against each other and allows to recover from
prover. Schrader et al. (2024) and Nafar, Venable, and Ko-        generation errors.
rdjamshidi (2024) extend this idea to probabilistic reason-
ing with numeric probabilities and uncertainty. Pan et al.        Outlook. Potential next steps involve investigating fur-
(2023) create symbolic representations comparable to PRO-         ther training setups. The usage of reinforcement learning-
LOG and first-order logic and fine-tune LLMs based on error       based (RL) training of LLMs has become popular due to
messages from the solver.                                         its promising training results (Ouyang et al. 2022), includ-
ASP code generation with LLMs. Early approaches com-              ing RL with our solver feedback as a training signal (Jha
bining NLP methods with ASP propose ideas for solving             et al. 2024). We propose to extend our reward function fr by
question answering and reasoning tasks (Baral, Gelfond,           introducing weights that rank each error type by its impor-
and Scherl 2004; Nouioua and Nicolas 2006). The L OGI -           tance. It can be further extended to also include signals dur-
CIA system (Mitra and Baral 2015) combines a pairwise             ing training that indicate the correctness based on the ground
Markov network for entity extraction with a maximum en-           truth solution (similar to our sampling procedure).
tropy model for relation classification on the LogicPuz-
zles dataset. Coppolillo et al. (2024) introduce the LLASP                          Acknowledgements
dataset with single-line building blocks of ASP code. We
focus on deriving ASP encodings for solving entire com-           This work was partially supported by the EU Project
plex puzzles. Ishay, Yang, and Lee (2023) create a detailed       SMARTY (GA 101140087).
                       References                                Hendrix, G. G.; Sacerdoti, E. D.; Sagalowicz, D.; and
Baral, C.; Gelfond, M.; and Scherl, R. 2004. Using answer        Slocum, J. 1978. Developing a natural language interface
set programming to answer complex queries. In Proceed-           to complex data. ACM Transactions on Database Systems
ings of the Workshop on Pragmatics of Question Answering         (TODS), 3(2): 105–147.
at HLT-NAACL 2004, 17–22. Boston, Massachusetts, USA:            Hu, E. J.; yelong shen; Wallis, P.; Allen-Zhu, Z.; Li, Y.;
Association for Computational Linguistics.                       Wang, S.; Wang, L.; and Chen, W. 2022. LoRA: Low-Rank
Baud, R. H.; Lovis, C.; Rassinoux, A.-M.; and Scherrer,          Adaptation of Large Language Models. In International
J.-R. 1998. Morpho-semantic parsing of medical expres-           Conference on Learning Representations.
sions. In Proceedings of the AMIA Symposium, 760. Ameri-         Ishay, A.; Yang, Z.; and Lee, J. 2023. Leveraging Large
can Medical Informatics Association.                             Language Models to Generate Answer Set Programs. In
Brown, T. B.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J.;      Proceedings of the International Conference on Principles
Dhariwal, P.; Neelakantan, A.; Shyam, P.; Sastry, G.; Askell,    of Knowledge Representation and Reasoning, volume 19,
A.; Agarwal, S.; Herbert-Voss, A.; Krueger, G.; Henighan,        374–383.
T.; Child, R.; Ramesh, A.; Ziegler, D. M.; Wu, J.; Winter,       Jha, P.; Jana, P.; Suresh, P.; Arora, A.; and Ganesh, V.
C.; Hesse, C.; Chen, M.; Sigler, E.; Litwin, M.; Gray, S.;       2024. RLSF: Reinforcement Learning via Symbolic Feed-
Chess, B.; Clark, J.; Berner, C.; McCandlish, S.; Radford,       back. arXiv preprint arXiv:2405.16661.
A.; Sutskever, I.; and Amodei, D. 2020. Language Models          Jiang, J.; Wang, F.; Shen, J.; Kim, S.; and Kim, S. 2024.
are Few-Shot Learners. arXiv:2005.14165.                         A Survey on Large Language Models for Code Generation.
Coppolillo, E.; Calimeri, F.; Manco, G.; Perri, S.; and Ricca,   arXiv:2406.00515.
F. 2024. LLASP: Fine-tuning Large Language Models for            Kautz, H. 2022. The third ai summer: Aaai robert s. engel-
Answer Set Programming. In Proceedings of the Interna-           more memorial lecture. Ai magazine, 43(1): 105–125.
tional Conference on Principles of Knowledge Representa-
                                                                 Kwon, W.; Li, Z.; Zhuang, S.; Sheng, Y.; Zheng, L.; Yu,
tion and Reasoning, volume 21, 834–844.
                                                                 C. H.; Gonzalez, J. E.; Zhang, H.; and Stoica, I. 2023. Ef-
DeepSeek-AI. 2025. DeepSeek-R1: Incentivizing Rea-               ficient Memory Management for Large Language Model
soning Capability in LLMs via Reinforcement Learning.            Serving with PagedAttention. In Proceedings of the ACM
arXiv:2501.12948.                                                SIGOPS 29th Symposium on Operating Systems Principles.
Delmonte, R. 1990. Semantic parsing with LFG and con-            Lai, X.; Tian, Z.; Chen, Y.; Yang, S.; Peng, X.; and Jia, J.
ceptual representations. Computers and the Humanities, 24:       2024. Step-DPO: Step-wise Preference Optimization for
461–488.                                                         Long-chain Reasoning of LLMs. arXiv:2406.18629.
Deng, H.; and Raffel, C. 2023. Reward-Augmented Decod-           Li, L.; Xie, Z.; Li, M.; Chen, S.; Wang, P.; Chen, L.; Yang,
ing: Efficient Controlled Text Generation With a Unidirec-       Y.; Wang, B.; and Kong, L. 2023. Silkie: Preference Distil-
tional Reward Model. In Bouamor, H.; Pino, J.; and Bali,         lation for Large Visual Language Models.
K., eds., Proceedings of the 2023 Conference on Empirical
Methods in Natural Language Processing, 11781–11791.             Lifschitz, V. 2008. What is answer set programming? In
Singapore: Association for Computational Linguistics.            Proceedings of the 23rd national conference on Artificial
                                                                 intelligence-Volume 3, 1594–1597.
Dong, X.; Teleki, M.; and Caverlee, J. 2024. A Survey
on LLM Inference-Time Self-Improvement. arXiv preprint           Lu, X.; Welleck, S.; West, P.; Jiang, L.; Kasai, J.; Khashabi,
arXiv:2412.14352.                                                D.; Le Bras, R.; Qin, L.; Yu, Y.; Zellers, R.; Smith, N. A.;
                                                                 and Choi, Y. 2022. NeuroLogic A*esque Decoding: Con-
Dong, Y.; Wang, Z.; Sreedhar, M. N.; Wu, X.; and Kuchaiev,       strained Text Generation with Lookahead Heuristics. In
O. 2023. SteerLM: Attribute Conditioned SFT as an (User-         Carpuat, M.; de Marneffe, M.-C.; and Meza Ruiz, I. V., eds.,
Steerable) Alternative to RLHF. arXiv:2310.05344.                Proceedings of the 2022 Conference of the North American
Falkner, A.; Friedrich, G.; Schekotihin, K.; Taupe, R.; and      Chapter of the Association for Computational Linguistics:
Teppan, E. C. 2018. Industrial applications of answer set        Human Language Technologies, 780–799. Seattle, United
programming. KI-Künstliche Intelligenz, 32(2): 165–176.         States: Association for Computational Linguistics.
Gebser, M.; Kaminski, R.; Kaufmann, B.; and Schaub,              Marek, V. W.; and Truszczyński, M. 1999. Stable mod-
T. 2017. Multi-shot ASP solving with clingo. CoRR,               els and an alternative logic programming paradigm. In The
abs/1705.09811.                                                  logic programming paradigm: A 25-year perspective, 375–
Gelfond, M.; and Lifschitz, V. 1988. The stable model se-        398. Springer.
mantics for logic programming. In ICLP/SLP, volume 88,           McDermott, D.; Ghallab, M.; Howe, A. E.; Knoblock, C. A.;
1070–1080. Cambridge, MA.                                        Ram, A.; Veloso, M. M.; Weld, D. S.; and Wilkins, D. E.
Grattafiori, A.; et al. 2024. The Llama 3 Herd of Models.        1998. PDDL-the planning domain definition language. In
arXiv:2407.21783.                                                Proceedings of the Artificial Intelligence Planning Systems
Gu, Q. 2023. Llm-based code generation method for golang         Conference (AIPS-98).
compiler testing. In Proceedings of the 31st ACM Joint Eu-       Mitra, A.; and Baral, C. 2015. Learning to Automatically
ropean Software Engineering Conference and Symposium             Solve Logic Grid Puzzles. In Màrquez, L.; Callison-Burch,
on the Foundations of Software Engineering, 2201–2203.           C.; and Su, J., eds., Proceedings of the 2015 Conference on
Empirical Methods in Natural Language Processing, 1023–          Language Text in Bayesian Reasoning Scenarios. In Al-
1033. Lisbon, Portugal: Association for Computational Lin-       Onaizan, Y.; Bansal, M.; and Chen, Y.-N., eds., Proceedings
guistics.                                                        of the 2024 Conference on Empirical Methods in Natural
Nafar, A.; Venable, K. B.; and Kordjamshidi, P. 2024. Prob-      Language Processing, 2634–2652. Miami, Florida, USA:
abilistic Reasoning in Generative Large Language Models.         Association for Computational Linguistics.
arXiv:2402.09614.                                                Stein, K.; Fišer, D.; Hoffmann, J.; and Koller, A. 2023. Au-
Ning, X.; Lin, Z.; Zhou, Z.; Wang, Z.; Yang, H.; and Wang,       toplanbench: Automatically generating benchmarks for llm
Y. 2024. Skeleton-of-thought: Prompting LLMs for efficient       planners from pddl. arXiv preprint arXiv:2311.09830.
parallel generation. In Proceedings 12th international con-      Sutton, R. S.; Barto, A. G.; et al. 1998. Reinforcement learn-
ference on learning representations-ICLR 2024.                   ing: An introduction, volume 1. MIT press Cambridge.
Nouioua, F.; and Nicolas, P. 2006. Using Answer Set Pro-         Tyagi, N.; Parmar, M.; Kulkarni, M.; Rrv, A.; Patel, N.;
gramming in an inference-based approach to Natural Lan-          Nakamura, M.; Mitra, A.; and Baral, C. 2024. Step-by-Step
guage Semantics. In Bos, J.; and Koller, A., eds., Pro-          Reasoning to Solve Grid Puzzles: Where do LLMs Falter? In
ceedings of the Fifth International Workshop on Inference        Al-Onaizan, Y.; Bansal, M.; and Chen, Y.-N., eds., Proceed-
in Computational Semantics (ICoS-5).                             ings of the 2024 Conference on Empirical Methods in Nat-
Olausson, T.; Gu, A.; Lipkin, B.; Zhang, C.; Solar-Lezama,       ural Language Processing, 19898–19915. Miami, Florida,
A.; Tenenbaum, J.; and Levy, R. 2023. LINC: A Neurosym-          USA: Association for Computational Linguistics.
bolic Approach for Logical Reasoning by Combining Lan-
                                                                 Ugare, S.; Suresh, T.; Kang, H.; Misailovic, S.; and Singh,
guage Models with First-Order Logic Provers. In Bouamor,
                                                                 G. 2024. Improving llm code generation with grammar aug-
H.; Pino, J.; and Bali, K., eds., Proceedings of the 2023 Con-
                                                                 mentation. arXiv preprint arXiv:2403.01632.
ference on Empirical Methods in Natural Language Pro-
cessing, 5153–5176. Singapore: Association for Computa-          Vyas, K.; Graux, D.; Yang, Y.; Montella, S.; Diao, C.; Zhou,
tional Linguistics.                                              W.; Vougiouklis, P.; Lai, R.; Ren, Y.; Li, K.; et al. 2024.
OpenAI; et al. 2024.               GPT-4 Technical Report.       From an LLM Swarm to a PDDL-empowered Hive: Plan-
arXiv:2303.08774.                                                ning Self-executed Instructions in a Multi-modal Jungle.
                                                                 arXiv preprint arXiv:2412.12839.
Ouyang, L.; Wu, J.; Jiang, X.; Almeida, D.; Wainwright,
C. L.; Mishkin, P.; Zhang, C.; Agarwal, S.; Slama, K.; Ray,      Wang, Z.; Dong, Y.; Zeng, J.; Adams, V.; Sreedhar, M. N.;
A.; Schulman, J.; Hilton, J.; Kelton, F.; Miller, L.; Simens,    Egert, D.; Delalleau, O.; Scowcroft, J. P.; Kant, N.; Swope,
M.; Askell, A.; Welinder, P.; Christiano, P.; Leike, J.; and     A.; and Kuchaiev, O. 2023. HelpSteer: Multi-attribute Help-
Lowe, R. 2022. Training language models to follow instruc-       fulness Dataset for SteerLM. arXiv:2311.09528.
tions with human feedback. arXiv:2203.02155.                     Wei, J.; Wang, X.; Schuurmans, D.; Bosma, M.; ichter, b.;
Pan, L.; Albalak, A.; Wang, X.; and Wang, W. 2023. Logic-        Xia, F.; Chi, E.; Le, Q. V.; and Zhou, D. 2022. Chain-of-
LM: Empowering Large Language Models with Symbolic               Thought Prompting Elicits Reasoning in Large Language
Solvers for Faithful Logical Reasoning. In Findings of the       Models. In Koyejo, S.; Mohamed, S.; Agarwal, A.; Bel-
Association for Computational Linguistics: EMNLP 2023,           grave, D.; Cho, K.; and Oh, A., eds., Advances in Neural
3806–3824.                                                       Information Processing Systems, volume 35, 24824–24837.
Peng, Y.; Gotmare, A. D.; Lyu, M.; Xiong, C.; Savarese,          Curran Associates, Inc.
S.; and Sahoo, D. 2024. PerfCodeGen: Improving Perfor-           Xiao, W.; Wang, Z.; Gan, L.; Zhao, S.; He, W.; Tuan, L. A.;
mance of LLM Generated Code with Execution Feedback.             Chen, L.; Jiang, H.; Zhao, Z.; and Wu, F. 2024. A Compre-
arXiv:2412.03578.                                                hensive Survey of Direct Preference Optimization: Datasets,
Qwen-Team. 2025.                 Qwen3 Technical Report.         Theories, Variants, and Applications. arXiv:2410.15595.
arXiv:2505.09388.                                                Yang, X.; Chen, B.; and Tam, Y.-C. 2024. Arithmetic rea-
Rafailov, R.; Sharma, A.; Mitchell, E.; Ermon, S.; Manning,      soning with llm: Prolog generation & permutation. arXiv
C. D.; and Finn, C. 2023. Direct preference optimization:        preprint arXiv:2405.17893.
your language model is secretly a reward model. In Pro-          Zeng, J.; Meng, F.; Yin, Y.; and Zhou, J. 2024. Improving
ceedings of the 37th International Conference on Neural In-      Machine Translation with Large Language Models: A Pre-
formation Processing Systems, NIPS ’23. Red Hook, NY,            liminary Study with Cooperative Decoding. In Ku, L.-W.;
USA: Curran Associates Inc.                                      Martins, A.; and Srikumar, V., eds., Findings of the Asso-
Rasley, J.; Rajbhandari, S.; Ruwase, O.; and He, Y. 2020.        ciation for Computational Linguistics: ACL 2024, 13275–
DeepSpeed: System Optimizations Enable Training Deep             13288. Bangkok, Thailand: Association for Computational
Learning Models with Over 100 Billion Parameters. In Pro-        Linguistics.
ceedings of the 26th ACM SIGKDD International Confer-
ence on Knowledge Discovery & Data Mining, KDD ’20,
3505–3506. New York, NY, USA: Association for Comput-                        Explanatory ASP Encoding
ing Machinery. ISBN 9781450379984.                               In this section, we provide a full step-by-step explanatory
Schrader, T. P.; Lange, L.; Razniewski, S.; and Friedrich,       ASP encoding for one test instance of LogicPuzzles.
A. 2024. QUITE: Quantifying Uncertainty in Natural                 We take instance 17 from the test split:
   Problem Description:                                            so far, it does not exclude that planner Herbert, for ex-
   MVP Events prides itself on planning large-scale par-           ample, is assigned to two different events, only that every
   ties for 50 or more people, anywhere in the United              assignment/3 will refer to a different event/1. There-
   States. This month the company has several different            fore, an addition to the choice rule is required, which is for-
   events to plan. Using only the clues below, match each          mulated as rule:
   event to its number of attendees and the state in which            {E1 = E2; P1 = P2; A1 = A2} = 0
   it will be held, and determine which MVP employee                  :- assignment(E1, P1, A1),
   is handling the logistics.                                            assignment(E2, P2, A2),
   Entities:                                                             (E1, P1, A1) != (E2, P2, A2).
   people: 50, 75, 100, 125.
   planners: Herbert, Joel, Susan, Teresa.                            It reads as follows: “For two assignment/3 that are
   events: Anniversary, Birthday, Graduation, Wedding.             part of the answer set, and the triples (event, planner, at-
   Clues:                                                          tendees) are not exactly the same, there must be zero over-
   1. Of the anniversary event and the event with 100 at-          lap in any of the three entities event, planner, and num-
   tendees, one will be handled by Joel and the other will         ber of attendees.” As we have seen above, there are four
   be handled by Susan.                                            assignment/3 that are part of the answer set. This addi-
   2. Herbert’s assignment will involve 25 fewer people            tion now excludes that two distinct events are, for example,
   than Susan’s assignment.                                        assigned the same planner Herbert.
   3. Of the assignment with 75 attendees and the assign-             Next, we add all rules and constraints based on the hints
   ment with 100 attendees, one will be handled by Susan           provided by the problem instance.
   and the other is the birthday.                                     The first clue is 1. Of the anniversary event and the event
   4. Herbert’s event is either the event with 50 attendees        with 100 attendees, one will be handled by Joel and the other
   or the graduation job.                                          will be handled by Susan. It carries multiple implications:
                                                                   The anniversary event does not have 100 attendees and Joel
   There are three entity types (people, planners, events)         and Susan must plan one of the anniversary event and the
with four subjects each. Hence, it is a 3×4 grid puzzle.           event with 100 attendees. In ASP, this is achieved by the
   We begin each ASP encoding by defining all entities             following encoding:
and constants that are involved in the search problem.
This is, we start by defining the three predicates people,            {E = anniversary; A = 100} = 1
planners/1, and events/1 and assign the 12 entities                   :- assignment(E, joel, A).
to each category respectively:
                                                                     This rule says that if there is an assignment/3 with
   people(50;75;100;125).                                          Joel, it can only have either the anniversary event or the
   planners(herbert;joel;susan;teresa).                            event with 100 attendees.
   events(anniversary;birthday;
                                                                     Likewise for Susan:
          graduation;wedding).
                                                                      {E = anniversary; A = 100} = 1
   We could also encode 4 times people/1 with a differ-               :- assignment(E, susan, A).
ent person inside, but using semi-colons is a much shorter
approach.                                                             The case that both Susan and Joel get the event with 100
   These 12 entities are now hard facts in the encoding, re-       attendees assigned is already excluded by the addition to the
sulting in them being part of every single possible answer         choice rule described above. Same holds for the anniversary
set.                                                               event.
   Next, the problem asks for matching each event to its              The next clue (2. Herbert’s assignment will involve 25
planner and number of attendees. In ASP, this is called gen-       fewer people than Susan’s assignment.) is a constraint that
erate, i.e., generating potential solutions. This is achieved by   excludes a specific condition (as opposed to rules that model
the so-called choice rule:                                         if-else statements). In ASP, this is written as follows:
   1 {assignment(Event, Planner, Attendees)                           :- assignment(_, herbert, A1),
     : planners(Planner), people(Attendees)} 1                        assignment(_, susan, A2),
     :- events(Event).                                                not A1 == A2 - 25.

   The choice rule generates instances of assignment/3                This is a constraint that requires at least one atom to eval-
with triples (event, planner, attendees). The syntax m ...         uate to false. This constraint reads as follows: “Every an-
n says that at least m and at most n grounded instances            swer set that contains one assignment/1 for Herbert and
of assignment/3 must be generated. The semantics of                one for Susan must not allow for Herbert’s number of atten-
this particular choice rule reads as follows: “For every           dees being anything else than the number of Susan’s sub-
event/1 that is part of the answer set, generate exactly           tracted by 25.”
one assignment/3 that contains a single event, a single               The third clue (3. Of the assignment with 75 attendees and
planner, and a single number of attendees.” Since we de-           the assignment with 100 attendees, one will be handled by
fined four distinct events above, the choice rule will gen-        Susan and the other is the birthday.) is modeled in the same
erate four grounded assignment/3 instances. However,               way as clue 1:
                                                                                Levenshtein Heuristics
   {E = birthday; P = susan} = 1                                Since exact string matching to compare ground truth and
   :- assignment(E, P, 75).
                                                                ASP output is often not possible, we implement a Leven-
   {E = birthday; P = susan} = 1                                shtein heuristic that automatically detects whether an ASP
   :- assignment(E, P, 100).                                    output corresponds to the ground truth or not. To achieve
                                                                that, we use the Levenshtein string edit distance that mea-
   Finally, the fourth clue (4. Herbert’s event is either       sures how many atomic string edit operations on a character-
the event with 50 attendees or the graduation job.) is an       level (insert, delete, replace) are necessary to transform one
exclusive-OR (XOR) that is modeled similarly to clues 1 and     string into another.
3:                                                                 We want to explain this using an example first. Con-
   {E = graduation; A = 50} = 1                                 sider the following solution of instance with ID 2 from the
   :- assignment(E, herbert, A).                                test HA split, i.e., the split without explanations of how to
                                                                arrive at the correct solution, of LogicPuzzles:
  The entire encoding looks as follows:                              (2016, ISON-X42, Dr. Golden)
   people(50;75;100;125).                                            (2017, Egert Facility, Dr. Owens)
   planners(herbert;joel;susan;teresa).                              (2018, Zynga Complex, Dr. Weber)
   events(anniversary;birthday;                                      (2019, Bale-Hahn SSC, Dr. Farley)
          graduation;wedding).
                                                                   Running clingo on the ASP encoding parsed by Llama-
   1 {assignment(Event, Planner, Attendees)
   : planners(Planner), people(Attendees)} 1                    3.1 70B yields the following answer sets:
     :- events(Event).                                               assignment(ison_x42,golden,2016)
                                                                     assignment(bale_hahn_ssc,farley,2019)
   {E1 = E2; P1 = P2; A1 = A2} = 0                                   assignment(egert_facility,owens,2017)
   :- assignment(E1, P1, A1),                                        assignment(zynga_complex,weber,2018)
      assignment(E2, P2, A2),
      (E1, P1, A1) != (E2, P2, A2).
                                                                   We can see that the main differences are dashes and
   {E = anniversary; A = 100} = 1                               spaces being converted into underscores, as well as some
   :- assignment(E, joel, A).                                   shortenings such as the prefix “Dr.” being removed. These
                                                                differences make it impossible to perform direct string com-
   {E = anniversary; A = 100} = 1                               parisons. Therefore, for comparing computed output and
   :- assignment(E, susan, A).                                  ground truth, we first transform the ground truth into a rep-
                                                                resentation as it could be used in ASP encodings. However,
   :- assignment(_, susan, A2),                                 if comparison still fails, we apply our Levenshtein heuristics
   not A1 == A2 - 25.                                           to compare both sets. This heuristic applies the following
   {E = birthday; P = susan} = 1
                                                                steps:
   :- assignment(E, P, 75).                                     1. For each computed set of assignments, iterate over each
                                                                    ground truth tuple and every item contained in it and
   {E = birthday; P = susan} = 1                                    compare it to every single item in the computed an-
   :- assignment(E, P, 100).                                        swer sets. In this example, we compare every item out
                                                                    of the 12 ground truth entities to all 12 computed items.
   {E = graduation; A = 50} = 1
   :- assignment(E, herbert, A).
                                                                    This results in a runtime complexity of O(n2 ), with
                                                                    n = 12 in this running example. For example, taking
                                                                    ison x42 and comparing it to (2016, ISON-X42,
  Running clingo on this encoding returns the following             Dr. Golden) results in the following three edit dis-
uniquely determined answer set:                                     tances computed by NLTK’s implementation of Leven-
     planners(herbert) planners(joel)                               shtein:
     planners(susan) planners(teresa)                                    edit_distance("ison_x42",
     people(50) people(75)                                                             "2016") = 8
     people(100) people(125)                                             edit_distance("ison_x42",
     events(anniversary) events(birthday)                                              "ISON-X42") = 6
     events(graduation) events(wedding)                                  edit_distance("ison_x42",
     assignment(anniversary,susan,75)                                                  "Dr. Golden") = 10
     assignment(wedding,herbert,50)
     assignment(birthday,joel,100)                                 After each comparison, we store the index tuple
     assignment(graduation,teresa,125)                             (i, j), i, j ∈ [1, . . . , 4] where i and j refer to the two row
   By comparing all four instances of assignment/3 to              indices where the edit distance was the lowest for i. In
the clues, we can see that this answer set is indeed a stable      the case above, we would have (1, 1) unless there is an-
model of the problem that fulfills all constraints.                other row where ison x42 needs less edits. However,
Figure 3: Matching two types of entities with four subjects      Figure 4: Visualization of an 3 × 4 grid puzzles that requires
each. There are 4 × 3 × 2 × 1 = 4! possibilities to find         2 = 3 − 1 independent matchings with 4! possibilities in
exclusive matchings.                                             each subgraph.


   if there are minimum edit distances, we perform an addi-                      GridPuzzles Example
   tional step that checks whether two strings are contained     GridPuzzles is very similar in its structure to LogicPuzzles.
   in each other or not. If so, this match will be preferred     The main difference is that it goes beyond grid sizes of 3×4
   over the match without overlapping strings.                   by additionally providing problems of sizes 3×5, 4×4, 4×5,
2. To judge whether a computed solution matches its              and 4×6.
   ground truth counterpart, we check if for every item in          The following instance with ID 8526 (note that there are
   ground truth row i the matching row j is the same. Fur-       still 274 instances) is an example for a 4×4 puzzle:
   thermore we require j to be assigned to only one row i.          Problem Description:
   For example, the following Levenshtein matrix indicates          Maurice had several customers in his tattoo parlor to-
   a valid solution for the running example:                        day, each of which requested a simple tattoo of their
        [[(1,1), (1,1), (1,1)],                                     astrological sign. Using only the clues below, match
         [(2,3), (2,3), (2,3)],                                     the prices to the options from customers, colors, and
         [(3,4), (3,4), (3,4)],                                     zodiac signs. Remember, as with all grid-based logic
         [(4,2), (4,2), (4,2)]]                                     puzzles, no option in any category will ever be used
                                                                    more than once.
                                                                    Entities:
 Number of Possible Solutions for Grid-based                        prices: $35, $40, $45, $50.
                  Puzzles                                           customers: Bonita, Carole, Kendra, Neil.
In this section, we want to provide a visual explanation for        colors: black, pink, red, violet.
why the number of possible solutions of an m × n assign-            zodiac signs: Pisces, Sagittarius, Taurus, Virgo.
                                                                    Clues: 1. Bonita was the Taurus.
ment equals to (n!)(m−1) , i.e., for a puzzle with m entity
                                                                    2. Of the person who paid $50 and the Virgo, one got
categories with n entities in each category.
                                                                    the pink tattoo and the other got the violet tattoo.
   Exemplarily, we use a 3 × 4 grid puzzle. That could be
                                                                    3. The Taurus was either the customer who got the red
matching four dogs with four owners and four houses.
                                                                    tattoo or the customer who got the violet tattoo.
   We approach this combinatorial problem as graph as
                                                                    4. Kendra was either the person who paid $50 or the
shown in figure 3. We start by matching the first 4 entities
                                                                    Pisces.
with another 4 entities and only allow for 1 : 1 matchings.
                                                                    5. Of the customer who paid $35 and Neil, one got the
When selecting the first entity of category 1, there are 4 op-
                                                                    red tattoo and the other was the Pisces.
portunities to match it with an entity of category two. After-
                                                                    6. Neil paid 10 dollars more than the customer who
wards, when matching the second entity of category 1, there
                                                                    got the black tattoo.
are only 3 entities left from category 3, resulting in only 3
opportunities. Likewise, the third entity of category 1 has         We approach this dataset in the same way as LogicPuz-
only 2 opportunities left for a matching, while the final one    zles, i.e., we start by defining all the constants:
from category 1 has only a single matching possibility. This
                                                                    price(35;40;45;50).
results in 4 × 3 × 2 × 1 = 4! opportunities. The general            customer(bonita;carole;kendra;neil).
number for n entities per category is therefore n!.                 color(black;pink;red;violet).
   The same holds for the second matching between entities          zodiac_sign(pisces;sagittarius;
from category 2 and category 3. Hence, we get 2 = 3 − 1                           taurus;virgo).
independent matching problems as shown in figure 4. The
general formula hence is m−1. Putting all together results in       Next, we formulate the choice rule. However, we need to
(n!)(m−1) possible solutions for an unconstrained grid puz-      slightly modify it to fit to the 4×4 instance instead of the
zle.                                                             3×4 ones from LogicPuzzles:
                                                                              assignment(_, neil, Co2, _).
   1 {assignment(P, C, CO, Z) :
       price(P), customer(C), color(CO)} 1                            { Z1 = pisces; Z2 = pisces } = 1
       :- zodiac_sign(Z).                                               :- assignment(35, _, _, Z1),
                                                                          assignment(_, neil, _, Z2).
   { P1 = P2; C1 = C2; CO1 = CO2; Z1 = Z2 }
   = 0
       :- assignment(P1, C1, CO1, Z1),                                Finally, the last hint (6. Neil paid 10 dollars more than
       assignment(P2, C2, CO2, Z2),                                the customer who got the black tattoo.) is again an ASP con-
       (P1, C1, CO1, Z1) !=                                        straints that filters all answer sets that do not adhere to this
             (P2, C2, CO2, Z2).                                    constraint:
   The main difference to the choice rule of LogicPuzzles is
                                                                      :- assignment(P1, neil, _, _),
that we now have 4 entity types in the choice rule.                     assignment(P2, _, black, _),
   Next, we look at the first hint: 1. Bonita was the Taurus.           P1 != P2 + 10.
This is a hard fact. However, in ASP, we cannot add facts
with unknown arguments. However, we only know Bonita
being the Taurus, but not how much was paid or what tattoo           In summary, this is the full ASP encoding for this Grid-
color there is. Hence, we need to formulate it as a constraint,    Puzzles instance:
thereby filtering out all answer sets generated by the choice
rule that do not fulfill this constraint:                             price(35;40;45;50).
   :- assignment(_, bonita, _, Z),                                    customer(bonita;carole;kendra;neil).
                 Z != taurus.                                         color(black;pink;red;violet).
                                                                      zodiac_sign(pisces;sagittarius;
                                                                        taurus;virgo).
   The second hint (2. Of the person who paid $50 and the
Virgo, one got the pink tattoo and the other got the violet           1 {assignment(P, C, CO, Z) :
tattoo.) enforces an XOR across two assignments:                        price(P), customer(C), color(CO)} 1
                                                                        :- zodiac_sign(Z).
   { Co1 = pink; Co2 = pink} = 1
                                                                      { P1 = P2; C1 = C2; CO1 = CO2; Z1 = Z2 }
     :- assignment(50, _, Co1, _),
                                                                      = 0
        assignment(_, _, Co2, virgo).
                                                                        :- assignment(P1, C1, CO1, Z1),
   { Co1 = violet; Co2 = violet } = 1
                                                                          assignment(P2, C2, CO2, Z2),
     :- assignment(50, _, Co1, _),
                                                                          (P1, C1, CO1, Z1) !=
        assignment(_, _, Co2, virgo).
                                                                                (P2, C2, CO2, Z2).

   These two statements enforce pink being assigned to ex-            :- assignment(_, bonita, _, Z),
actly one of both (the $50 person and the Virgo), as well as                Z != taurus.
violet being assigned to only one of both. It is not possible
that one gets both red and violet in the answer set as this is        { Co1 = pink; Co2 = pink} = 1
forbidden by the second statement of the choice rule block              :- assignment(50, _, Co1, _),
above.                                                                  assignment(_, _, Co2, virgo).
   The third clue (3. The Taurus was either the customer who          { Co1 = violet; Co2 = violet } = 1
                                                                        :- assignment(50, _, Co1, _),
got the red tattoo or the customer who got the violet tattoo.)          assignment(_, _, Co2, virgo).
is an XOR for one assignment, allowing for only one of two
(Taurus being the customer with red tattoo or violet tattoo)          { Co = red; Co = violet } = 1
to be true:                                                             :- assignment(_, _, Co, taurus).
   { Co = red; Co = violet } = 1
     :- assignment(_, _, Co, taurus).                                 { P = 50; Z = pisces } = 1
                                                                        :- assignment(P, kendra, _, Z).
   Hint 4 (4. Kendra was either the person who paid $50 or            { Co1 = red; Co2 = red} = 1
the Pisces.) is modeled the same way as hint 3:                         :- assignment(35, _, Co1, _),
                                                                        assignment(_, neil, Co2, _).
   { P = 50; Z = pisces } = 1
     :- assignment(P, kendra, _, Z).                                  { Z1 = pisces; Z2 = pisces } = 1
                                                                        :- assignment(35, _, _, Z1),
   Hint 5 (5. Of the customer who paid $35 and Neil, one got            assignment(_, neil, _, Z2).
the red tattoo and the other was the Pisces.) is similar to hint
2:                                                                    :- assignment(P1, neil, _, _),
                                                                        assignment(P2, _, black, _),
   { Co1 = red; Co2 = red} = 1                                          P1 != P2 + 10.
     :- assignment(35, _, Co1, _),
                                                                                                     Results on GridPuzzles per Grid Size
                                                                                     100
                                                                                                                                                    Correct
                                                                                                                                                    Wrong
                                                                                                                                                    Error
                                                                                      80

                            Correct




                                                                    Percentage (%)
                                                                                      60
         Wrong
                              15 30 45                                                40

                            0 Correct - Unique
                                                                                      20



     Unsatisfiable                                                                     0
                                                                                           3x4       3x5              4x4              4x5          4x6
                                                                                                                   Grid Size
        Base
                    Warnings & Errors
        SFT
                                                                  Figure 6: Percentages of correct, wrong, and erroneous cases
                                                                  split by the different grid sizes of GridPuzzles.

                                                                                                   Results on GridPuzzles per Difficulty Level
                                                                                     100
                                                                                                                                                    Correct
Figure 5: Comparison of success and failure types between                                                                                           Wrong
                                                                                                                                                    Error
the base and SFT trained Llama-3.3 70B.                                               80
                                                                  Percentage (%)


                                                                                      60
Evaluation on the Full LogicPuzzles Test Split
As already explained above, there is a slight overlap between                         40
the train split and the two test splits of the LogicPuzzles
dataset. Therefore, in the main text, we report on the cleaned
test split in order to provide a fair evaulation of our models                        20
on unseen data. To also assess the performance of our mod-
els on the full test split, we report the numbers calculated on
                                                                                       0
all 100 dataset instances in Table 3. We observe very similar                               Easy                   Medium                        Hard
tendencies compared to the cleaned test set, indicating that                                                   Grid Difficulty
regardless of the design of the test split, our methods show a
clear improvement in terms of ASP coding capabilities.            Figure 7: Percentages of correct, wrong, and erroneous cases
                                                                  split by the different difficulty levels of GridPuzzles.
       Comparison between DPO and SFT
Our initial idea was to use pairs of chosen and rejected in-       Results on GridPuzzles by Size and Difficulty
stances to perform preference alignment-based training us-        GridPuzzles instances are categorized by two dimensions:
ing DPO (Rafailov et al. 2023). However, as shown in Table        grid size and difficulty. To get a better understanding of how
4, the Llama-3.3 70B model trained with DPO slightly un-          these variables influence the performance of our fine-tuned
derperforms its SFT-trained counterpart by a few percentage       Llama-3.3 70B in combination with reward-based inference,
points on both datasets.                                          we plot the percentage of correct, wrong, and erroneous
                                                                  cases for each size and difficulty level in Figures 6 and 7. We
                 Error Type Analysis                              can observe that the grid size has a bigger influence on the
                                                                  performance of the system than the human-judged difficulty.
Figure 5 shows the success and error types for the base           We interpret this as strength of our neuro-symbolic model
Llama-3.3 70B compared to its SFT trained counterpart on          that it can perform reasoning robustly on even very difficult
LogicPuzzles. We can observe that the untrained Llama es-         problems as long as the ASP semantics is correct. Increasing
pecially struggles with producing non-erroneousness and           grid sizes also lead to increasing search spaces for potential
satisfiable encodings. These cases can be caught especially       solutions, hence requiring much more computational power.
well in our solver-in-the-loop setup. Hence, we observe a         As a result, some of the largest puzzles cannot be solved
great shift towards uniquely and correctly answered cases         due to computational constraints. However, there are strate-
for the SFT trained model.                                        gies for reformulating the uniqueness constraint into n − 1
                      Setup              Llama-3.3 70B            Llama-3.1 8B     Qwen3 32B       Qwen3 8B
                                    w/o ASP Base SFT +TT Base SFT +TT Base SFT +TT Base SFT +TT
                2S   LogicP.          27.0   31.0   55.4 66.8     0.0   21.6 46.8 17.6 23.0 50.3 0.0 24.3 43.2
                2S   LogicP.-Full     22.0   27.0   60.0 68.0     0.0   30.0 54.4 21.0 25.0 55.6 0.0 32.0 50.6
                PP   LogicP.           -     56.8   78.4 -        0.0    0.0  -   51.4 67.6 -    31.1 24.3 -
                PP   LogicP.-Full      -     61.0   80.0 -        0.0    0.0  -   50.0 65.0 -    34.0 28.0 -

    Table 3: The performance of our trained models compared between the cleaned and the full test split of LogicPuzzles.


     Training Setting     LogicPuzzles       GridPuzzles
     SFT                       55.4             16.8
     DPO                       51.4             11.7

Table 4: Performance of Llama-3.3 70B on both datasets
when trained using either SFT or DPO. We can observe a
superior performance of SFT over DPO.


separate statements. Though, in our experiments, the mod-
els failed to grasp the semantics of the alternative uniqueness
constraints. We leave this for future research.
