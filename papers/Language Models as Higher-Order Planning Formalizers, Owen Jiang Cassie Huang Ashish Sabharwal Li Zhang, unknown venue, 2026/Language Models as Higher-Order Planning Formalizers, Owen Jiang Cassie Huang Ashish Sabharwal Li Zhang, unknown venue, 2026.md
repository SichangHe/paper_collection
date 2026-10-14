                                                         Language Models as Higher-Order Planning Formalizers


                                                     Owen Jiang            Cassie Huang      Ashish Sabharwal       Li Zhang
                                                                           Drexel University Allen Institute for AI
                                                                    owenjiang669@gmail.com | harry.zhang@drexel.edu




                                                                   Abstract
                                                Recent work provides overwhelming evidence
arXiv:2603.23844v2 [cs.CL] 4 Jul 2026




                                                that LLMs, even those trained to scale their
                                                reasoning trace, quickly deteriorate at planning
                                                as problems become more complex. LLM-as-
                                                Formalizers aim to address this by employing
                                                LLMs as a bridge to translate natural language
                                                descriptions into structured planning represen-
                                                tations such as PDDL, which are then fed to a
                                                programmatic solver. We observe that its suc-
                                                cess may be overstated because planning prob-
                                                lem descriptions in standard benchmarks often
                                                have a one-to-one mapping to PDDL, which
                                                departs from real use cases. To address this,
                                                we introduce the notion of unraveling prob-
                                                lems where a natural yet succinct description          Figure 1: On an unraveling problem where the input
                                                translates into a very large PDDL representa-          description is short but the denoted planning instance is
                                                tion. Using unraveling variants of four standard       large, an LLM-as-Formalizer must explicitly enumerate
                                                planning domains, we demonstrate that LLM              many grounded fluents, while an LLM-as-Higher-Order-
                                                Formalizers also do not always scale. We tackle        Formalizer generates a compact program that captures
                                                this challenge by introducing a new paradigm,          the same logic and can be expanded downstream.
                                                LLM-as-Higher-Order-Formalizer, where the
                                                LLM generates a high-level program that cap-
                                                tures the recurrent logic within the description       lack verifiability and interpretability. An alterna-
                                                and in turn generates the larger PDDL repre-           tive paradigm, called LLM-as-Formalizer, has been
                                                sentation. This decouples token output from            introduced as a remedy that employs the LLM as a
                                                the combinatorial explosion of the underlying          bridge to translate natural language (NL) descrip-
                                                formalization and search space, leading to im-         tions into structured formal representations like
                                                proved performance for complex problems.1
                                                                                                       the Planning Domain Definition Language (PDDL)
                                        1       Introduction                                           (McDermott et al., 1998; Huang and Zhang, 2025).
                                                                                                       The output is then fed to a programmatic planner
                                        Recent large language models (LLMs) have been                  to derive a plan. This provides built-in verifiability
                                        advocated to be able to plan, or to be trained to plan.        and is effective on standard benchmarks (Huang
                                        The most intuitive paradigm, LLM-as-Planner, gen-              et al., 2025; Kagitha et al., 2025a).
                                        erates action sequences directly from domain and                  However, we observe that the success of the For-
                                        problem specifications in an end-to-end fashion.               malizer paradigm may be overstated due to an unre-
                                        However, recent work provides overwhelming evi-                alistic design of standard benchmarks, namely that
                                        dence that LLMs, even those trained to scale their             the natural language problem description and the
                                        reasoning trace (LRMs), collapse when solving                  ground-truth PDDL code often have a one-to-one
                                        planning problems beyond a certain complexity                  mapping. In industrial uses cases, succinct prob-
                                        (Valmeekam et al., 2024; Shojaee et al., 2025; Lin             lem descriptions often describe large problems. In
                                        et al., 2025; Varela et al., 2025). Additionally, they         Figure 1, the description “There are 10,000 blocks,
                                            1
                                                Code and data attached with the submission.            of which all even-numbered ones are in one stack.”

                                                                                                   1
naturally translates to tens thousands of lines of           2.1      In Theory
PDDL. This is not reflected in any current bench-            Let Dn denote a natural-language description of a
mark.                                                        planning problem with n objects.
   To remedy this, we first introduce the concept            Definition 1. Let
of unraveling problems where a single line of de-
                                                                    In = U (Dn ) = ⟨On , R, Fn , An , In , Gn ⟩
scription corresponds to arbitrarily many lines in
PDDL. We propose the             benchmark based on          be the symbolic planning instance denoted by the
4 classical planning domains that significantly chal-        natural-language description Dn , where:
lenges even the Formalizers that perform perfectly              • On is a set of objects;
on standard benchmarks. Our results reveal that                 • R is a finite set of predicate symbols;
Formalizers also do not always scale. How, then,                • Fn is the set of ground fluents induced by On
can we design a LLM-based planning method that                    and R;
scale more reliably? To tackle this challenge, we               • An is the set of grounded actions;
introduce a new planning paradigm called LLM-                   • In ⊆ Fn is the initial state;
as-Higher-Order-Formalizer. Here the LLM’s                      • Gn is the goal condition.
job is to translate the natural language problem de-         A state is a subset s ⊆ Fn . A plan is a finite action
scription into a high-level program (e.g., in Python),       sequence π = (a1 , a2 , . . . , aL ),   ai ∈ An that
which in turn generates the PDDL representation,             transforms In into a state satisfying Gn .
which is then fed to a programmatic planner. Im-                Therefore, the task of planning involves:
portantly, this high-level program is expected to                    Dn →
                                                                        − In = ⟨On , Fn , An , In , Gn ⟩ →
                                                                                                         − π.
roughly be in a one-to-one correspondence with the
natural language description, capturing its recursive        Spaces Induced by Planning Instances. A sym-
nature, and drastically shortening the token output          bolic planning instance In induces several distinct
of the LLM on compactly described problems. We               spaces described next and not to be conflated:
find that under this new paradigm, frontier models                  Fn ,        An , Sn ,               Tn , ALn  .
                                                                   |{z}        |{z}  |{z}              |{z}
such as Gemini 3 Flash and DeepSeek-V4-Flash
                                                                                                             |{z}
                                                              fluent space action space state space search space plan space
scale nearly perfectly on         , while open models
                                                                The fluent space Fn is a set of ground predicates
such as Qwen2.5-32B achieve notably improved
                                                             forming the symbolic vocabulary over which states
performance in most cases.
                                                             are described. The state space Sn is the set of legal
    As LLMs become increasingly adept at coding,             world configurations (where each world configura-
it is only natural to try to leverage this ability for       tion is a state s ⊆ Fn is the subset of fluents that are
planning. The earlier Formalizer paradigm can be             true in that state). The action space An contains
seen as relying on an LLM’s code execution (rather           grounded actions that map states to other states.
than code generation) ability to output the grounded         Actions are described by schemas, e.g., transport
PDDL representation. Code execution, however,                package 5 from location 10 to location 15. The
requires state tracking, making it more demanding            search space Tn is the transition graph induced by
than code generation (Merrill et al., 2026). On the          states and actions Tn = (Sn , En ), where an edge
                                                                a
other hand, the H-O Formalizer paradigm directly             s−→ s′ exists if action a ∈ An is applicable in state
leverages LLMs’ code generation skills, along with           s ∈ Sn and produces successor state s′ ∈ Sn . The
structured representations and traditional planners,         plan space AL  n contains candidate action sequences
in order to solve complex, large-scale planning              of length L. A valid plan is a path in Tn from the
problems with natural succinct descriptions.                 initial state In to a state satisfying the goal Gn .
                                                                For a given planning domain, if r is the fluent
                                                             predicate arity and ℓ the action-schema arity,2 then
2   LLM Planning and Scaling
                                                                          |Fn | = Θ(nr ), |An | = Θ(nℓ ).
                                                             Thus the grounded fluent and action vocabularies
We start with theoretical discussions of the input,          are of size polynomial in n. In contrast, the state
output, and semantic spaces an LLM navigates in              space is exponential in the fluent vocabulary,
different planning paradigms. We then present em-                                                        r

pirical results about how these paradigms fare when                             |Sn | = 2|Fn | = 2Θ(n ) ,
                                                                2
scaling problem size.                                               For ease of exposition, we assume fixed arity for both.


                                                         2
                                                                 ing changes the amount of search performed, not
                                                                 the nature of the search problem.

                                                                 LLM-as-Formalizer. The Formalizer does not
                                                                 directly navigate the search space. Instead, given
                                                                 a fixed domain, it navigates the space of ground
                                                                 fluents Fn , which scales polynomially in n. The
                                                                 combinatorial plan search is delegated to a sym-
                                                                 bolic planner. See Figure 2.

                                                                 2.2   In Practice
                                                                 We follow Huang and Zhang (2025) for the con-
                                                                 crete task formulation: given a domain specifica-
                                                                 tion (describes actions and their pre-conditions and
                                                                 effects) both in NL and PDDL and a problem de-
                                                                 scription (describes initial and goal states of enti-
                                                                 ties), a system outputs a plan (a sequence of ac-
                                                                 tions) which is validated via a ground-truth simu-
                                                                 lation. Planner does so in an end-to-end manner,
                                                                 while Formalizer does so by generating a PDDL
                                                                 problem file which a programmatic planner takes
                                                                 in and produces a plan. We assume the domain file
                                                                 as given, following works like Zuo et al. (2025) as
Figure 2: An illustration of the nature of combinatorial         we only consider the scaling of problem complex-
explosion in the BlocksWorld domain. Under different             ity, where the domain remains constant. We nor-
paradigms, LLMs generate tokens tantamount to the                mally use the dual-bfws-ffparser planner im-
complexity of different spaces.                                  plemented by Muise (2016) as the programmatic
                                                                 planner and VAL (Howey et al., 2004) as the val-
                                                                 idator. However, since the programmatic planner
and the plan space of length L is exponential in L
                                                                 times-out as problems grow in complexity, we write
             |AL          L
               n | = |An | = Θ(n
                                ℓ·L
                                    ).                           our own parsers to compare the LLM-generated
The search space is the transition graph constrained             PDDL problem files with the ground-truth prob-
by action applicability and goal satisfaction, which             lem files for differences. Since BlocksWorld guar-
we approximate as                                                anties solvability, if the parser shows that the LLM-
                |Tn | ≈ Θ(|Sn | |An |).                          generated problem files perfectly match the ground-
                                                                 truths, we count that as providing a valid plan. We
LLM-as-Planner. An LLM may directly map                          report the plan accuracy, the percentage that can
the natural-language description to a plan by gener-             be executed to achieve the goal state.
ating just the plan Dn 7→ πb. The generated output
π
b is a token sequence, but a direct planner must                 Benchmark. We focus on the arguably most used
implicitly perform two tasks: translate Dn to the                planning domains in the community, BlocksWorld
planning instance In and navigate the search space               (IPC, 1998) based on object manipulation to re-
Tn , which is often infeasible for an inference pass             arrange stacks of blocks on a table. We extend
that runs in time O(n2 ) for a transformer LLM.                  an existing dataset from Huang and Zhang (2025)
                                                                 with “moderately templated” descriptions but cre-
LLM-as-Planner with Inference-Time Scaling.                      ate problems with much higher complexity than
Inference-time scaling gives the LLM a larger bud-               existing work (see Appendix D). Examples of the
get to explore candidate outputs π
                                 b1 , π
                                      b2 , . . . , π
                                                   bB . At       NL domain and problem descriptions, the Planner
the token level, this expands the explored gener-                and Formalizer prompts, and the PDDL domain
ation space. At the semantic level, these outputs                and problem files are shown in the Appendix start-
correspond to candidate paths within the same un-                ing Listing 4. The resulting BlocksWorld-XXL
derlying space Tn . Therefore, inference-time scal-              dataset includes 200 problems ranging from 5 to

                                                             3
100 blocks. We use the size of the object space as           to formalize (Hales et al., 2015).
a proxy of problem complexity.
                                                             3.1   Definition
Models. We consider Gemini 3 Flash (G3F) as a                We call a planning problem an unraveling prob-
representative, state-of-the-art, closed-source LRM,         lem when the natural language description Dn is
DeepSeek-V4-Flash (DS-V4) (DeepSeek-AI, 2026)                succinct, but the denoted planning instance
as an open-source LRM, and Qwen2.5-Coder-32B-
Instruct (Q25) (Hui et al., 2024) as an open-source                U (Dn ) = In = ⟨On , Fn , An , In , Gn ⟩
LLM. Open models are run using KANI (Zhu et al.,             is significantly larger (|Dn | ≪ |In |). This creates
2023) with default temperature on 1 H100 GPU.                a distinct scaling challenge for a Formalizer that
                                                             must still explicitly emit polynomially many facts
Scaling Performance. Figure 5a shows the scal-               from the compact description.
ing performance of 3 models as both Planners                    To address this compression gap, we intro-
and Formalizers on BlocksWorld-XXL. We con-                  duce the paradigm of LLM-as-Higher-Order-
clusively corroborate previous work that Planners            Formalizer. Instead of directly outputting the fully
do not scale with problem complexity. All models             grounded instance In , the model outputs a higher-
including the LRMs trained to scale reasoning to-            order generator program first:
ken degrade to 20% accuracy or worse as Planners
                                                                               Dn 7→ Rn 7→ In ,
at merely 30 blocks, while both LRMs display a
“spark” of planning ability at only 5 blocks. In con-        where Rn compactly describes (e.g., in Python)
trast, Formalizers scale much better with problem            how to emit the objects and fluents of the instance.
complexity. The performance of G3F remains 100%              A downstream compiler, interpreter, or lifted plan-
up to 100 blocks, while that of the non-reasoning            ner then expands this higher-order representation
Q25 remains above 70% until 80 blocks but sharply            into a grounded planning instance. While a regu-
degrades thereafter. Error analysis on Q25’s outputs         lar Formalizer navigates the ground fluent space
shows 14% have missing initial conditions, 64%               Fn , an H-O Formalizer instead navigates a com-
have extra initial conditions, 57% have missing              pact program space; its generated text can remain
goals, and 21% have extra goals.                             small even when the denoted instance is large
   To show weaker models’ inability to formalize             (|Rn | ≪ |Fn |). This shifts Formalizer’s burden
long statements, we propose a divide-and-conquer             from enumerating large grounded fluent sets to pro-
(D&C) technique. We prompt an LLM to first gen-              ducing a compact generation rule of them.
erate the problem file headers with one call, in-
                                                             3.2   Unraveling Datasets
cluding problem name, domain name, and objects.
Next, the input problem description is segmented             We create a benchmark of unraveling problems
into sentences. Provided one sentence at a time              coined         containing 4 classical planning do-
plus the domain specification to avoid context over-         mains: BlocksWorld, OpenStacks (IPC, 2011),
load, the LLM generates only one line of PDDL                Transport (IPC, 2008), and ChildSnack (IPC, 2014).
code. Since each generated line is grounded in the           Our data creation process can be extended to any
domain file and thus independent of each other, the          similar planning domain.
lines are later consolidated. Figure 5a shows that
                                                             Unraveling Problems Layout. In unraveling
D&C addresses the context overloading problem
                                                             problems, the most important distinction is that we
for weaker models, increasing Q25 performance as
                                                             no longer describe problems line-by-line, but with
Formalizer from 30% to 100% at 100 blocks.
                                                             compact language that portrays the overall prop-
3   Uraveling Problems                                       erties and relations of the objects in the domains,
                                                             effectively compressing the problem descriptions
In all existing planning benchmarks juxtaposing              (Figure 1). As an example from ChildSnack, an
NL and PDDL, the problem descriptions Dn and                 enumerative description like ‘There are child 1,
problem files (On , Fn , Gn ) are aligned as a one-to-       child 2, child 3, child 4, child 5, tray 1, tray 2, tray
one, line-to-line mapping, so that formalizing them          3, bread portion 1, bread portion 2, bread portion
may be oversimplifying real-life problems. As an             3, . . .’ turns into a compressed, higher-level de-
extreme example in theorem proving, the Kepler               scription ‘There are n children numbered 1 to 5,
conjecture is a single statement that took 11 years          bread portions numbered 1 to 3, . . .’. However, in-

                                                         4
spired by the observation that symmetric initial and
goal states, while enabling efficient search, limit
the scope of problems that are created (Sabharwal,
2005), we still randomize and enumerate the goal
states to maintain solution complexity.

Creating Unraveling Problems. We create prob-
lem descriptions by picturing a realistic scenario
with an easily describable pattern for each domain.
For example, in ChildSnack, we use a controlled
serving scenario in which children are partitioned
into groups waiting at fixed places, with one tray
serving each group. Unlike standard ChildSnack in-
stances, where the distribution of children, ingredi-
ents, trays, and dietary requirements can vary more
freely, our instances assign each child a correspond-
ing bread portion, content portion, and sandwich
placeholder, and use a deterministic regular/gluten-
free dietary pattern with matching gluten-free ingre-
dients. The goal is to prepare and serve one appro-
                                                            Figure 3: An illustration of how we set different vari-
priate sandwich to every child. We refer to this sce-       ables in ChildSnack and how the variables form an ex-
nario as ‘single sandwich line’ because each child          ample problem description.
appears in exactly one serving line, although an
instance may contain multiple tray-specific lines.
                                                            like ceil(n/3) can still lead to identical problems
Choosing Main-Varying versus Fixed Parame-                  within a batch. For example, in the n = 5 batch of
ters. All domains except BlocksWorld have mul-              ChildSnack, there are only five unique child-tray
tiple variable parameters, such as the number of            assignments if we only use a primitive partition
children, trays, and content portions in ChildSnack.        formula children group = ceil(n/3). In a prob-
Theoretically, we could randomly vary all param-            lem with five children, the second five problems
eters to create distinct problems. However, that            will repeat the partitions of the first five. To solve
makes it impossible to systematically study how             this, we first introduce a "hyperparameter" local_k
LLMs’ performance changes for more or less com-             that is equivalent to the problem index within a
plex problems. Therefore, we choose a main pa-              batch. This hyperparameter helps determine the
rameter in each domain to vary and fix other param-         partition shift for each problem within the batch
eters at a low-medium-level difficulty based on the         using shif t = ((local_k − 1)//2) % n. Further-
original competitions. For example, in ChildSnack,          more, we add an assignment order rule where odd
we choose the number of children as the main pa-            problems use forward child order and even prob-
rameter and fix the numbers of trays to 3 versus            lems use backward child order. These designs help
a maximum of 4 in the original competition. The             eliminate identical problems within a given batch.
main and fixed parameters for Transport and Open-           Figure 4 provides an example of combining rules
Stacks are shown in Appendix B. Figure 3 shows              to create distinct problems.
an example of setting parameters for ChildSnack.
                                                            Unraveling       Problems        Statistics. The
Ensuring Distinct Within-Batch Problems. We                 Domains-Unravel dataset contains 280 problem
create 10 problems for each n per domain. We                descriptions and PDDL files for four domains,
call each 10-problem group a batch. To create               including problem descriptions and PDDL files
distinct problems within each batch, we rotate              ranging from 5 to 100 blocks for BlocksWorld,
the way the main-varying parameters are matched             from 5 to 100 orders for OpenStacks, from 10 to
with the fixed parameters. For example, we ro-              100 locations for Transport, and from 5 to 100
tate the trays that the children are assigned in            children for ChildSnack. The dataset enables us
ChildSnack. However, a simple partition, such               to draw convincing conclusions, while it can be
as grouping children using a fixed division rule            expanded without costs by adjusting the numerical

                                                        5
                                                                that they just wrote for the first prompt before fi-
                                                                nalizing the Python programs, especially paying
                                                                attention to possible errors in the way problem
                                                                descriptions translate to repeating patterns. This
                                                                two-stage prompting method is distinct from the
                                                                single-stage prompting in Planner and Formalizer.

                                                                4   Results
                                                                Figure 5:b-e shows that the unraveling problems
                                                                in        almost zero-out Planner performance, ex-
                                                                cept for G3F and DS-V4 in OpenStacks. To under-
                                                                stand why this outlier occurs, we analyze the plans
                                                                written by the two models and find that they mainly
                                                                employ a brute-force approach in which they first
                                                                ensure opening sufficient stacks for all orders, then
                                                                bulk start working on the orders, and finally bulk
                                                                ship all orders without meaningful optimizations,
                                                                especially for the complex-end of the problems.
                                                                This helps G3F and DS-V4 achieve nearly perfect
                                                                performance in Planner in OpenStacks.
                                                                   Figure 5:b-e also indicates that when comparing
                                                                Formalizer and H-O Formalizer, Formalizer fluc-
                                                                tuates or degrades in BlocksWorld and Transport
                                                                while H-O Formalizer outperforms Formalizer in
Figure 4: Using a combination of rules to create distinct       those two domains. Furthermore, in OpenStacks
within-batch problems in ChildSnack.                            and ChildSnack, Formalizer with frontier models
                                                                G3F and DS-V4 remains robust while H-O Formal-
                                                                izer matches Formalizer performance. Why can
expressions like n. Note that as we scale up                    Formalizer with frontier models keep robust? Is
problem complexity (both entity space and fluent                it because of true scalability or because the spe-
space), the initial statement portion of the input              cific problems are simply too easy? To test this,
size of the unraveling problems remains constant.               we extend the problems to 300 and 1000 orders in
                                                                OpenStacks, as well as 300 and 1000 children in
3.3   Implementing H-O Formalizers                              ChildSnack. For the 300-batch in OpenStacks, G3F
                                                                and DS-V4 still maintain 90% and 100% accuracy,
We conduct comprehensive experiments for all
                                                                respectively. For the 300-batch in ChildSnack, G3F
domains and pipelines. In H-O Formalizer, we
                                                                and DS-V4 achieve 80% and 90%, respectively. For
provide LLMs with NL domain and problem de-
                                                                the 1000-batch, only DS-V4 completes the Open-
scriptions, proprietary H-O Formalizer prompts,
                                                                Stacks problems, with 70% accuracy. Although per-
and ground-truth PDDL domain files and ask the
                                                                formance starts to decline slightly as the problems
LLMs to generate Python programs that produce
                                                                become extremely large, this brief extension study
PDDL problem files upon execution. Examples
                                                                suggests that the key reason for the observed For-
of the domain and problem descriptions, H-O For-
                                                                malizer robustness is likely true scalability. Overall,
malizer prompts, PDDL domain and problem files
                                                                our results show that H-O Formalizer matches or
are shown in Appendix starting from Listing 25.
                                                                outperforms Formalizer in nearly all cases.
Like in Formalizer, we also use our own parsers
to perform differences checking. In H-O Formal-                 5   Discussion
izer, inspired by the fact that the LLMs naturally
needed to write code for repeating patterns such                Ablation Study with Q25. To demonstrate the
as object types appending and loops to formalize                effectiveness of H-O Formalizer, we conduct an
the problems, we use two-stage prompts where we                 ablation study using Q25 on OpenStacks, Transport,
ask the LLMs to reflect on the repeating patterns               and ChildSnack in which we do not ask Q25 to

                                                            6
                                                              (a) BlocksWorld-XXL
                     As Planner                               As Formalizer                         As D&C Formalizer
100%

 80%

 60%

 40%

 20%

  0%
       5


                30


                          50


                                    75



                                           0




                                                     5


                                                          30


                                                                  50


                                                                            75



                                                                                        0




                                                                                               5


                                                                                                     30


                                                                                                              50


                                                                                                                        75



                                                                                                                                   0
                                          10




                                                                                      10




                                                                                                                                  10
                                                         (b) BlocksWorld-Unravel
                     As Planner                                As Formalizer                             As H-O Formalizer
100%

 80%

 60%

 40%

 20%

  0%
    0

           20


                     40


                               60


                                     80


                                           0




                                                    0

                                                         20


                                                                40


                                                                       60


                                                                                 80


                                                                                        0




                                                                                               0

                                                                                                    20


                                                                                                            40


                                                                                                                   60


                                                                                                                             80


                                                                                                                                   0
                                          10




                                                                                      10




                                                                                                                                  10
                                                          (c) OpenStacks-Unravel
                     As Planner                               As Formalizer                          As H-O Formalizer
100%

 80%

 60%

 40%

 20%

  0%
       10
       15
       20
       25
       30


                      50




                                           0




                                                    10
                                                    15
                                                    20
                                                    25
                                                    30


                                                                 50




                                                                                       0




                                                                                               10
                                                                                               15
                                                                                               20
                                                                                               25
                                                                                               30


                                                                                                             50




                                                                                                                                   0
                                          10




                                                                                      10




                                                                                                                                  10
                                                              (d) Transport-Unravel
                     As Planner                                As Formalizer                             As H-O Formalizer
100%

 80%

 60%

 40%

 20%

  0%
   10
   15
   20
   25
   30


                      50




                                           0




                                                    10
                                                    15
                                                    20
                                                    25
                                                    30


                                                                  50




                                                                                           0




                                                                                               10
                                                                                               15
                                                                                               20
                                                                                               25
                                                                                               30


                                                                                                              50




                                                                                                                                       0
                                          10




                                                                                       10




                                                                                                                                   10




                                                          (e) ChildSnack-Unravel
                     As Planner                                As Formalizer                             As H-O Formalizer
100%

 80%

 60%

 40%

 20%

  0%
     5
    10
    15
    20
    25
    30


                      50




                                           0




                                                     5
                                                    10
                                                    15
                                                    20
                                                    25
                                                    30


                                                                  50




                                                                                        0




                                                                                                5
                                                                                               10
                                                                                               15
                                                                                               20
                                                                                               25
                                                                                               30


                                                                                                              50




                                                                                                                                   0
                                          10




                                                                                      10




                                                                                                                                  10




                Gemini 3 Flash                 Qwen2.5-32B             Qwen2.5-32B Pattern Review            DeepSeek-V4-Flash

Figure 5: a. Performance of state-of-the-art LLM Planners and Formalizers, on BlocksWorld with increasing
problem complexity quantified by entity space size. For the divide-and-conquer (D&C) technique, we omit Gemini
3 Flash and DeepSeek-V4-Flash due to their already high accuracy as regular formalizers; b–e. Performance of
state-of-the-art LLMs Planners, Formalizers, and H-O Formalizers on        across four classical planning domains
with increasing problem complexity quantified by input size.




                                                                            7
                   100                                                       2023; Liu et al., 2023; Zhang et al., 2024a,b; Zhu
                           Q25                       87%
                           Q25 Pattern Review                                et al., 2024). While Planner is intuitive and strong
                    80
                                            66%                              on small problems, Formalizer promises verifiabil-
    Accuracy (%)


                    60         55%                                           ity and scalability, which we show does not always
                         45%                                                 hold. Therefore, we only focus on works involving
                                                                  41%
                    40
                                                                             scaling complexity in planning and beyond.
                                                            23%
                    20
                                                                             Scaling Complexity. Prior work has demon-
                     0                                                       strated degraded performance as models plan with
                         OpenStacks             Transport   ChildSnack
                                                                             larger and more complex problems (Valmeekam
Figure 6: The pattern review method improves Q25                             et al., 2024; Shojaee et al., 2025; Lin et al., 2025).
performance on all scheduling domains.                                       Varela et al. (2025); Shi et al. (2023) reveal that
                                                                             diminishing performance may be due to large text
reflect on repeating patterns code, and we perform                           size and irrelevant context added to the problem.
error analysis on Q25’s code by domains under the                            Kagitha et al. (2025b) demonstrates potential scal-
ablated prompting. For each domain, we randomly                              ing ability for Formalizer, while Huang et al. (2025)
pick two batches of problems and manually analyze                            shows that both methodologies struggle when con-
at most 10 errors in those batches.                                          straints are added to larger problems. However, no
   In OpenStacks, 90% of the errors occur in a loop,                         work has been done on unraveling problems, the
and 80% are about the ‘(includes order product)’                             focus of this paper, except Li et al. (2026) which
loop. Listing 1 shows an example of the latter.                              discusses description compression from an infor-
Listing 1: Correct vs. Qwen’s Code for ‘Includes’ Facts                      mation theoretic angle. We are unobliged to discuss
                                                                             this work preprinted in Feb 2026.
Correct code:
for i in range(1, num_orders + 1):
    for j in range(3):
                                                                             Code Generation. Using H-O Formalizer relies
        product = ((i + j + 4 - 1) % num_products                            on LLMs’ ability to generate code. LLMs have
            ) + 1                                                            been used for writing and debugging programs
        init_facts.append(f"(includes o{i} p{
            product})")
                                                                             (Jiang et al., 2026) and generating code as inter-
                                                                             mediate representations for PDDL formalization
Qwen writes:                                                                 (Kagitha et al., 2025b). Related to H-O Formalizer,
for i in range(1, num_orders + 1):
    for j in range(3):                                                       LLMs have also been used to generate solver code
        product = (i + j + 5) % num_products + 1                             to produce plans (Stein et al., 2026; Silver et al.,
        init_facts.append(f"(includes o{i} p{                                2023). However, different from prior work, we
            product})")
                                                                             generate code that will be used to formalize the
   In Transport, 50% of errors occur in appending                            environment, rather than generate a plan.
object types, and 50% occur in either the loop as-
signing packages to location or the loop assigning                           7   Conclusion
capacities to trucks. An example of an object ap-                            We revisit the scalability of LLM-based planning
pending error is shown in Listing 3. Finally, in                             and argue that prior evaluations overestimate the
ChildSnack, 100% of errors occur in the ‘waiting’                            robustness of Formalizer due to unrealistic one-to-
loop assigning children to wait for sandwiches at                            one NL-PDDL mappings in existing benchmarks.
different places. An example of such an error is                             To address this, we introduce unraveling prob-
shown in Listing 2. The overall performance boost                            lems, where compact descriptions expand into large
from pattern review is shown in Figure 6.                                    grounded planning instances. Our experiments
                                                                             across four planning domains show that standard
6           Related Work
                                                                             Formalizers also degrade under this setting. We
Wei et al. (2025) and Tantakoun et al. (2025) are re-                        further propose H-O Formalizer, which leverages
cent surveys on the Planner and Formalizer method-                           LLMs’ code-generation ability to produce compact
ologies. In essence, LLMs have been tasked to gen-                           generator programs instead of explicit grounded
erate plans directly (Sel et al., 2025; Verma et al.,                        representations. This paradigm improves scalabil-
2025; Bohnet et al., 2025) or generate a formal                              ity, particularly on large and highly compressed
language to interface a symbolic solver (Xie et al.,                         planning problems.

                                                                         8
8   Limitations                                               Cassie Huang and Li Zhang. 2025. On the limit of
                                                                language models as planning formalizers. In Pro-
We discuss a few important limitations of our                   ceedings of the 63rd Annual Meeting of the Associa-
method. First, although we evaluate four planning               tion for Computational Linguistics (Volume 1: Long
domains with different structures and parameteri-               Papers), pages 4880–4904, Vienna, Austria. Associa-
                                                                tion for Computational Linguistics.
zations, our experiments are still limited to classi-
cal symbolic planning settings with fixed domain              Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Day-
specifications. Future work may extend unravel-                 iheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang,
ing problems to broader planning environments,                  Bowen Yu, Kai Dang, et al. 2024. Qwen2. 5-coder
                                                                technical report. arXiv preprint arXiv:2409.12186.
such as partially observable, stochastic, temporal,
or multi-agent domains, where compact natural-                IPC. 1998. International planning competition. https:
language descriptions may induce even more com-                 //www.icaps-conference.org/competitions.
plex grounded representations and execution con-              IPC. 2008. International planning competition. https:
straints.                                                       //www.icaps-conference.org/competitions.
   Second, our implementation of H-O Formal-
                                                              IPC. 2011. International planning competition. https:
izer relies on Python-based generator programs                  //www.icaps-conference.org/competitions.
and handcrafted prompting strategies, including
the pattern-reflection stage. While this design               IPC. 2014. International planning competition. https:
demonstrates strong empirical scalability, it does              //www.icaps-conference.org/competitions.
not yet explore whether the generated higher-order            Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and
representations are optimal, minimal, or transfer-              Sunghun Kim. 2026. A survey on large language
able across domains. Future research may investi-               models for code generation. ACM Transactions on
                                                                Software Engineering and Methodology, 35(2):1–72.
gate more principled intermediate representations,
learned compilation strategies, or tighter integra-           Prabhu Prakash Kagitha, Bo Sun, Ishan Desai, An-
tion between higher-order formalization and lifted              drew Zhu, Cassie Huang, Manling Li, Ziyang Li, and
planning systems.                                               Li Zhang. 2025a. Unifying inference-time planning
                                                                language generation. Preprint, arXiv:2505.14763.

                                                              Prabhu Prakash Kagitha, Andrew Zhu, and Li Zhang.
References                                                      2025b. Addressing the challenges of planning lan-
Bernd Bohnet, Pierre-Alexandre Kamienny, Hanie                  guage generation. Preprint, arXiv:2505.14763.
  Sedghi, Dilan Gorur, Pranjal Awasthi, Aaron Parisi,
                                                              Zhong Li, Hongliang Lu, Tao Wei, Wenyu Liu, Yuxuan
  Kevin Swersky, Rosanne Liu, Azade Nova, and
                                                                Chen, Yuan Lan, Fan Zhang, and Zaiwen Wen. 2026.
  Noah Fiedel. 2025. Enhancing llm planning ca-
                                                                Constructing industrial-scale optimization modeling
  pabilities through intrinsic self-critique. Preprint,
                                                                benchmark. Preprint, arXiv:2602.10450.
  arXiv:2512.24103.
DeepSeek-AI. 2026. DeepSeek-V4: Towards highly                Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson,
  efficient million-token context intelligence.                 Ashish Sabharwal, Radha Poovendran, Peter Clark,
                                                                and Yejin Choi. 2025. Zebralogic: On the scaling lim-
Thomas Hales, Mark Adams, Gertrud Bauer, Dat Tat                its of LLMs for logical reasoning. In Forty-second
  Dang, John Harrison, Truong Le Hoang, Cezary                  International Conference on Machine Learning.
  Kaliszyk, Victor Magron, Sean McLaughlin,
  Thang Tat Nguyen, Truong Quang Nguyen, Tobias               Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu,
  Nipkow, Steven Obua, Joseph Pleso, Jason Rute,                Shiqi Zhang, Joydeep Biswas, and Peter Stone.
  Alexey Solovyev, An Hoai Thi Ta, Trung Nam Tran,              2023. Llm+ p: Empowering large language mod-
  Diep Thi Trieu, Josef Urban, Ky Khac Vu, and                  els with optimal planning proficiency. arXiv preprint
  Roland Zumkeller. 2015. A formal proof of the ke-             arXiv:2304.11477.
  pler conjecture. Preprint, arXiv:1501.02155.
                                                              Drew McDermott, Malik Ghallab, Adele Howe, Craig
R. Howey, D. Long, and M. Fox. 2004. Val: auto-                 Knoblock, Ashwin Ram, Manuela Veloso, Daniel
  matic plan validation, continuous effects and mixed           Weld, and David Wilkins. 1998. PDDL - the planning
  initiative planning using pddl. In 16th IEEE Inter-           domain definition language. Technical Report CVC-
  national Conference on Tools with Artificial Intelli-         TR-98-003 / YaleU/DCS/TR-1165, Yale Center for
  gence, pages 294–301.                                         Computational Vision and Control.

Cassie Huang, Stuti Mohan, Ziyi Yang, Stefanie Tellex,        William Merrill, Yanhong Li, Tyler Romero, Anej Svete,
  and Li Zhang. 2025. Language model as plan-                   Caia Costello, Pradeep Dasigi, Dirk Groeneveld,
  ner and formalizer under constraints. Preprint,               David Heineman, Bailey Kuehl, Nathan Lambert, Ja-
  arXiv:2510.05486.                                             cob Morrison, Luca Soldaini, Finbarr Timbers, Pete


                                                          9
  Walsh, Noah A. Smith, Hanna Hajishirzi, and Ashish               Hui Wei, Zihao Zhang, Shenghua He, Tian Xia, Shijia
  Sabharwal. 2026. Olmo Hybrid: From theory to                       Pan, and Fei Liu. 2025. PlanGenLLMs: A modern
  practice and back. arXiv preprint arXiv:2604.03444.                survey of LLM planning capabilities. In Proceedings
                                                                     of the 63rd Annual Meeting of the Association for
Christian Muise. 2016. Planning.Domains. In The                      Computational Linguistics (Volume 1: Long Papers),
  26th International Conference on Automated Plan-                   pages 19497–19521, Vienna, Austria. Association
  ning and Scheduling - Demonstrations.                              for Computational Linguistics.
Ashish Sabharwal. 2005. SymChaff: A structure-aware                Yaqi Xie, Chen Yu, Tongyao Zhu, Jinbin Bai, Ze Gong,
  satisfiability solver. In AAAI, pages 467–474, Pitts-              and Harold Soh. 2023. Translating natural language
  burgh, PA.                                                         to planning goals with large-language models. arXiv
                                                                     preprint arXiv:2302.05128.
Bilgehan Sel, Ruoxi Jia, and Ming Jin. 2025. LLMs can
   plan only if we tell them. In The Thirteenth Interna-           Li Zhang, Peter Jansen, Tianyi Zhang, Peter Clark,
   tional Conference on Learning Representations.                    Chris Callison-Burch, and Niket Tandon. 2024a.
Freda Shi, Xinyun Chen, Kanishka Misra, Nathan                       PDDLEGO: Iterative planning in textual environ-
  Scales, David Dohan, Ed Chi, Nathanael Schärli,                    ments. In Proceedings of the 13th Joint Conference
  and Denny Zhou. 2023. Large language models can                    on Lexical and Computational Semantics (*SEM
  be easily distracted by irrelevant context. Preprint,              2024), pages 212–221, Mexico City, Mexico. As-
  arXiv:2302.00093.                                                  sociation for Computational Linguistics.

Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh,                   Tianyi Zhang, Li Zhang, Zhaoyi Hou, Ziyu Wang, Yul-
  Maxwell Horton, Samy Bengio, and Mehrdad Fara-                      ing Gu, Peter Clark, Chris Callison-Burch, and Niket
  jtabar. 2025. The illusion of thinking: Understand-                Tandon. 2024b. PROC2PDDL: Open-domain plan-
  ing the strengths and limitations of reasoning mod-                 ning representations from texts. In Proceedings of
  els via the lens of problem complexity. Preprint,                   the 2nd Workshop on Natural Language Reasoning
  arXiv:2506.06941.                                                   and Structured Explanations (@ACL 2024), pages
                                                                     13–24, Bangkok, Thailand. Association for Compu-
Tom Silver, Soham Dan, Kavitha Srinivas, Joshua B.                    tational Linguistics.
  Tenenbaum, Leslie Pack Kaelbling, and Michael
  Katz. 2023. Generalized planning in pddl domains                 Andrew Zhu, Liam Dugan, Alyssa Hwang, and Chris
  with pretrained large language models. Preprint,                   Callison-Burch. 2023. Kani: A lightweight and
  arXiv:2305.11014.                                                  highly hackable framework for building language
                                                                     model applications. In Proceedings of the 3rd Work-
Katharina Stein, Nils Hodel, Daniel Fišer, Jörg                      shop for Natural Language Processing Open Source
  Hoffmann, Michael Katz, and Alexander Koller.                      Software (NLP-OSS 2023), pages 65–77, Singapore.
  2026. Improved generalized planning with llms                      Association for Computational Linguistics.
  through strategy refinement and reflection. Preprint,
  arXiv:2508.13876.                                                Wang Zhu, Ishika Singh, Robin Jia, and Jesse Thoma-
                                                                    son. 2024. Language models can infer action seman-
Marcus Tantakoun, Christian Muise, and Xiaodan Zhu.                 tics for classical planners from environment feedback.
 2025. LLMs as planning formalizers: A survey for                   arXiv preprint arXiv:2406.02791.
 leveraging large language models to construct auto-
 mated planning models. In Findings of the Asso-                   Max Zuo, Francisco Piedrahita Velez, Xiaochen Li,
 ciation for Computational Linguistics: ACL 2025,                   Michael Littman, and Stephen Bach. 2025. Plan-
 pages 25167–25188, Vienna, Austria. Association                    etarium: A rigorous benchmark for translating text
 for Computational Linguistics.                                     to structured planning languages. In Proceedings
                                                                    of the 2025 Conference of the Nations of the Amer-
Karthik Valmeekam, Kaya Stechly, and Subbarao Kamb-                 icas Chapter of the Association for Computational
  hampati. 2024. Llms still can’t plan; can lrms? a                 Linguistics: Human Language Technologies (Volume
  preliminary evaluation of openai’s o1 on planbench.               1: Long Papers), pages 11223–11240, Albuquerque,
  Preprint, arXiv:2409.13373.                                       New Mexico. Association for Computational Linguis-
                                                                    tics.
Iñaki Dellibarda Varela, Pablo Romero-Sorozabal, Ed-
   uardo Rocon, and Manuel Cebrian. 2025. Rethink-
   ing the illusion of thinking. In Artificial Intelligence        A    Example Errors
  XLII: 45th SGAI International Conference on Artifi-
   cial Intelligence, AI 2025, Cambridge, UK, Decem-
   ber 16-18, 2025, Proceedings, Part I, page 116–129,             Listing 2: Correct vs. Qwen’s Code for ‘Waiting’ Facts
   Berlin, Heidelberg. Springer-Verlag.                            Correct code:
                                                                   for i, child in enumerate(children, start=1):
Pulkit Verma, Ngoc La, Anthony Favier, Swaroop                         if i % 3 == 0:
  Mishra, and Julie A. Shah. 2025. Teaching llms                           init_facts.append(f"(allergic_gluten {
  to plan: Logical chain-of-thought instruction tuning                         child})")
  for symbolic planning. Preprint, arXiv:2509.13351.                   else:


                                                              10
                                                                                         BlocksWorld-XXL
         init_facts.append(f"(not_allergic_gluten
             {child})")                                                                    Average Plan length
                                                                                 200

    if child_num == 1 or child_num >= 22:                                        150
           table = "table3"
    elif child_num <= 11:                                                        100
           table = "table1"
    else:                                                                         50

           table = "table2"
                                                                                   0
    init_facts.append(f"(waiting {child} {tables[                                      0     20 40 60 80 100
        table_index]})")                                                Gemini 3 Flash             Qwen3-32B     Qwen2.5-32B

Qwen writes:
for i, child in enumerate(children, start=1):                    Figure 7: Average plan length increases with number
    if i % 3 == 0:                                               of blocks under LLM-as-formalizer pipeline, indicating
        init_facts.append(f"(allergic_gluten {                   growing solution complexity with increasing input com-
             child})")
    else:                                                        plexity.
        init_facts.append(f"(not_allergic_gluten
             {child})")
    table_index = (i - 1) // children_per_tray                   C    Problem Size and Plan Length Relation
    init_facts.append(f"(waiting {child} {tables[
         table_index]})")
                                                                 To better consider the linear relationship between
                                                                 the natural language inputs and the resulting solv-
                                                                 ing process under PDDL formulation, we plot num-
Listing 3: Correct vs. Qwen’s Code for Appending                 ber of blocks and the resulting plan length (in lines
Objects Types Facts                                              of text file) (Figure 7).
Correct code:
lines.append(" (:objects")                                       D    BlocksWorld-XXL Dataset
lines.append(f" {' '.join(locations)} - location                      Construction
    ")
lines.append(f" {' '.join(vehicles)} - vehicle")                 Problems were generated following the procedure
lines.append(f" {' '.join(packages)} - package")
lines.append(f" {' '.join(capacities)} -                         in (Huang and Zhang, 2025). For BlocksWorld-
    capacity-number")                                            XXL, we first randomly generate the initial stacks
lines.append(" )")
                                                                 and goal stacks given the number of blocks, then
Qwen writes:                                                     use a template to automatically generate the prob-
objects = locations + packages + vehicles + [f"                  lem descriptions. As mentioned in Section 3 the
    capacity-{i}" for i in range(max_capacity +
    1)]                                                          initial stacks were artificially set. Listings 4-20
                                                                 display example PDDL and natural language de-
                                                                 scriptions for BlocksWorld-XXL, BlocksWorld-
                                                                 Unravel. ChildSnack, OpenStacks and Transport.
B    Main and Fixed Parameters in
     Transport and OpenStacks                                    E   Experimental Details
                                                                 During evaluation of formalizers, due to the large
                                                                 problem sizes in our dataset, the solver often
Domain      Varied           Fixed            Ours Max           crashes before completion, so we implement a
                             Packages          10    30          parser to compare the differences between the
Transport   Locations        Vehicles          3     11          LLM-generated and ground-truth problem files.
                             Capacity          4      –
                                                                 Knowing our domains’ problems are always solv-
                             Products          12   250          able, we regard a perfect match for all of the objects,
OpenStacks Orders
                             Prod./order        3    –
                                                                 initial, and goal states between the two problem
Table 1: Main (varied) and fixed parameters in the unrav-
                                                                 files implies a valid plan, and any mismatch means
eling problems of Transport and OpenStacks. Dashes               invalid plan.
indicate that there are no directly comparable maxi-                Listings 21-34 display the full prompts that we
mum in the original competition settings, and we set the         use to generate the outputs, including plans and
values in our problems to create controlled, structured          problem files. Outputs were parsed using a parser
problem templates.                                               that takes in an output .txt file.

                                                            11
F   Potential Risks
Although LLM-as-formalizer and LLM-as-higher-
order-formalizer have much higher accuracy than
LLM-as-planner, it is important to note that for-
malizer methods may still experience issues like
hallucination, especially if they are applied in the
real world.

G    Personally Identifying Information
The data used in this project is synthetic and does
not contain personally identifying information or
offensive content.

H    Descriptive Statistics
All statistics for experimental results are in percent-
ages. Each experiment is run once, as each result
only takes extreme values of either 0% or 100%.

I   Artifacts Licenses and Use
Our use of artifacts is completely for academic re-
search and fit the intended licenses or use purposes.




                                                          12
                  Listing 4: Domain File for BlocksWorld-XXL and BlocksWorld-Unravel
(define (domain blocksworld)
  (:requirements :strips)
(:predicates (clear ?x)
            (on-table ?x)
            (arm-empty)
            (holding ?x)
            (on ?x ?y))

(:action pickup
  :parameters (?ob)
  :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
  :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob))
              (not (arm-empty))))

(:action putdown
  :parameters (?ob)
  :precondition (holding ?ob)
  :effect (and (clear ?ob) (arm-empty) (on-table ?ob)
              (not (holding ?ob))))

(:action stack
  :parameters (?ob ?underob)
  :precondition (and (clear ?underob) (holding ?ob))
  :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
              (not (clear ?underob)) (not (holding ?ob))))

(:action unstack
  :parameters (?ob ?underob)
  :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
  :effect (and (holding ?ob) (clear ?underob)
              (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty)))))


          Listing 5: Domain Description for an Example 100-Block Problem in BlocksWorld-XXL
I am playing with a set of blocks where I need to arrange the blocks into stacks. Here are the
    actions I can do

Pick up a block
Unstack a block from on top of another block
Put down a block
Stack a block on top of another block

I have the following restrictions on my actions:
I can only pick up or unstack one block at a time.
I can only pick up or unstack a block if my hand is empty.
I can only pick up a block if the block is on the table and the block is clear. A block is clear if
    the block has no other blocks on top of it and if the block is not picked up.
I can only unstack a block from on top of another block if the block I am unstacking was really on
    top of the other block.
I can only unstack a block from on top of another block if the block I am unstacking is clear.
Once I pick up or unstack a block, I am holding the block.
I can only put down a block that I am holding.
I can only stack a block on top of another block if I am holding the block being stacked.
I can only stack a block on top of another block if the block onto which I am stacking the block is
    clear.
Once I put down or stack a block, my hand becomes empty.
Once you stack a block on top of a second block, the second block is no longer clear.


           Listing 6: Problem Description for an Example 5-Block Problem in BlocksWorld-XXL
As initial conditions I have that, block 1 is clear, the hand is empty, block 1 is on top of block 3,
     block 3 is on top of block 5, block 4 is on top of block 2, block 5 is on top of block 4, and
    block 2 is on the table.
My goal is to have that block 1 is on the table, block 2 is on the table, block 3 is on the table,
    block 4 is on the table, and block 5 is on the table.



                                                 13
          Listing 7: Problem Description for an Example 100-Block Problem in BlocksWorld-XXL
As initial conditions I have that,
block 1 is clear, block 2 is clear, block 3 is clear, block 4 is clear,
block 5 is clear, block 6 is clear, block 7 is clear, block 8 is clear,
block 9 is clear, block 10 is clear, block 11 is clear,
block 12 is clear, block 14 is clear, block 15 is clear,
block 16 is clear, block 18 is clear, block 19 is clear,
block 20 is clear, block 23 is clear, block 24 is clear,
block 25 is clear, block 26 is clear, block 27 is clear,
block 28 is clear, block 29 is clear, block 30 is clear,
block 31 is clear, block 33 is clear, block 36 is clear,
block 38 is clear, block 39 is clear, block 40 is clear,
block 41 is clear, block 42 is clear, block 43 is clear,
block 44 is clear, block 46 is clear, block 47 is clear,
block 48 is clear, block 50 is clear, block 51 is clear,
block 52 is clear, block 53 is clear, block 54 is clear,
block 56 is clear, block 57 is clear, block 58 is clear,
block 59 is clear, block 60 is clear, block 61 is clear,
block 62 is clear, block 63 is clear, block 64 is clear,
block 65 is clear, block 68 is clear, block 69 is clear,
block 73 is clear, block 74 is clear, block 75 is clear,
block 76 is clear, block 77 is clear, block 78 is clear,
block 80 is clear, block 81 is clear, block 83 is clear,
block 84 is clear, block 85 is clear, block 86 is clear,
block 87 is clear, block 88 is clear, block 90 is clear,
block 93 is clear, block 94 is clear, block 95 is clear,
block 96 is clear, block 97 is clear, block 98 is clear,
block 100 is clear, the hand is empty, block 8 is on top of block 35,
block 12 is on top of block 82, block 14 is on top of block 32,
block 15 is on top of block 92, block 16 is on top of block 72,
block 18 is on top of block 67, block 19 is on top of block 37,
block 20 is on top of block 34, block 24 is on top of block 49,
block 27 is on top of block 13, block 28 is on top of block 66,
block 32 is on top of block 17, block 34 is on top of block 91,
block 35 is on top of block 22, block 47 is on top of block 89,
block 59 is on top of block 79, block 67 is on top of block 71,
block 69 is on top of block 70, block 79 is on top of block 55,
block 81 is on top of block 99, block 89 is on top of block 45,
block 94 is on top of block 21, block 1 is on the table,
block 2 is on the table, block 3 is on the table,
block 4 is on the table, block 5 is on the table,
block 6 is on the table, block 7 is on the table,
block 9 is on the table, block 10 is on the table,
block 11 is on the table, block 13 is on the table,
block 17 is on the table, block 21 is on the table,
block 22 is on the table, block 23 is on the table,
block 25 is on the table, block 26 is on the table,
block 29 is on the table, block 30 is on the table,
block 31 is on the table, block 33 is on the table,
block 36 is on the table, block 37 is on the table,
block 38 is on the table, block 39 is on the table,
block 40 is on the table, block 41 is on the table,
block 42 is on the table, block 43 is on the table,
block 44 is on the table, block 45 is on the table,
block 46 is on the table, block 48 is on the table,
block 49 is on the table, block 50 is on the table,
block 51 is on the table, block 52 is on the table,
block 53 is on the table, block 54 is on the table,
block 55 is on the table, block 56 is on the table,
block 57 is on the table, block 58 is on the table,
block 60 is on the table, block 61 is on the table,
block 62 is on the table, block 63 is on the table,
block 64 is on the table, block 65 is on the table,
block 66 is on the table, block 68 is on the table,
block 70 is on the table, block 71 is on the table,
block 72 is on the table, block 73 is on the table,
block 74 is on the table, block 75 is on the table,
block 76 is on the table, block 77 is on the table,
block 78 is on the table, block 80 is on the table,


                                                 14
block 82 is on the table, block 83 is on the table,
block 84 is on the table, block 85 is on the table,
block 86 is on the table, block 87 is on the table,
block 88 is on the table, block 90 is on the table,
block 91 is on the table, block 92 is on the table,
block 93 is on the table, block 95 is on the table,
block 96 is on the table, block 97 is on the table,
block 98 is on the table, block 99 is on the table,
and block 100 is on the table.
My goal is to have that,
block 2 is on top of block 39, block 8 is on top of block 42,
block 10 is on top of block 92, block 12 is on top of block 10,
block 15 is on top of block 56, block 16 is on top of block 14,
block 19 is on top of block 20, block 20 is on top of block 25,
block 31 is on top of block 64, block 32 is on top of block 90,
block 33 is on top of block 67, block 40 is on top of block 62,
block 41 is on top of block 22, block 42 is on top of block 60,
block 43 is on top of block 12, block 46 is on top of block 3,
block 55 is on top of block 57, block 57 is on top of block 71,
block 58 is on top of block 63, block 62 is on top of block 4,
block 66 is on top of block 36, block 68 is on top of block 74,
block 69 is on top of block 82, block 70 is on top of block 34,
block 71 is on top of block 77, block 73 is on top of block 27,
block 78 is on top of block 21, block 79 is on top of block 44,
block 80 is on top of block 58, block 81 is on top of block 91,
block 82 is on top of block 7, block 83 is on top of block 18,
block 84 is on top of block 68, block 86 is on top of block 40,
block 88 is on top of block 1, block 91 is on top of block 48,
block 93 is on top of block 51, block 1 is on the table,
block 3 is on the table, block 4 is on the table,
block 5 is on the table, block 6 is on the table,
block 7 is on the table, block 9 is on the table,
block 11 is on the table, block 13 is on the table,
block 14 is on the table, block 17 is on the table,
block 18 is on the table, block 21 is on the table,
block 22 is on the table, block 23 is on the table,
block 24 is on the table, block 25 is on the table,
block 26 is on the table, block 27 is on the table,
block 28 is on the table, block 29 is on the table,
block 30 is on the table, block 34 is on the table,
block 35 is on the table, block 36 is on the table,
block 37 is on the table, block 38 is on the table,
block 39 is on the table, block 44 is on the table,
block 45 is on the table, block 47 is on the table,
block 48 is on the table, block 49 is on the table,
block 50 is on the table, block 51 is on the table,
block 52 is on the table, block 53 is on the table,
block 54 is on the table, block 56 is on the table,
block 59 is on the table, block 60 is on the table,
block 61 is on the table, block 63 is on the table,
block 64 is on the table, block 65 is on the table,
block 67 is on the table, block 72 is on the table,
block 74 is on the table, block 75 is on the table,
block 76 is on the table, block 77 is on the table,
block 85 is on the table, block 87 is on the table,
block 89 is on the table, block 90 is on the table,
block 92 is on the table, block 94 is on the table,
block 95 is on the table, block 96 is on the table,
block 97 is on the table, block 98 is on the table,
block 99 is on the table, and block 100 is on the table.


         Listing 8: Problem Description for an Example 100-Block Problem in BlocksWorld-Unravel
As initial conditions I have 100 blocks numbered 1 to 100. All the odd numbered blocks are on one
    stack, with increasing numbering from top to bottom. Same for the even numbered blocks on
    another stack.
My goal is to have that block 1 is on top of block 74, block 2 is on top of block 47, block 3 is on
    top of block 36, block 4 is on top of block 6, block 5 is on top of block 93, block 6 is on top
    of block 9, block 7 is on top of block 1, block 8 is on top of block 83, block 9 is on top of


                                                  15
    block 77, block 10 is on top of block 44, block 11 is on top of block 34, block 12 is on top of
    block 63, block 14 is on top of block 8, block 15 is on top of block 65, block 16 is on top of
    block 14, block 17 is on top of block 92, block 18 is on top of block 32, block 19 is on top of
    block 7, block 20 is on top of block 26, block 21 is on top of block 84, block 23 is on top of
    block 40, block 24 is on top of block 37, block 25 is on top of block 15, block 26 is on top of
    block 48, block 27 is on top of block 95, block 28 is on top of block 59, block 29 is on top of
    block 35, block 30 is on top of block 90, block 31 is on top of block 17, block 32 is on top of
    block 55, block 33 is on top of block 91, block 34 is on top of block 85, block 35 is on top of
    block 46, block 36 is on top of block 97, block 37 is on top of block 11, block 38 is on top of
    block 82, block 39 is on top of block 71, block 40 is on top of block 81, block 41 is on top of
    block 75, block 42 is on top of block 73, block 43 is on top of block 87, block 44 is on top of
    block 22, block 45 is on top of block 66, block 46 is on top of block 80, block 47 is on top of
    block 96, block 48 is on top of block 50, block 49 is on top of block 89, block 50 is on top of
    block 4, block 51 is on top of block 21, block 52 is on top of block 99, block 53 is on top of
    block 64, block 54 is on top of block 88, block 55 is on top of block 25, block 56 is on top of
    block 45, block 57 is on top of block 62, block 58 is on top of block 67, block 59 is on top of
    block 98, block 60 is on top of block 18, block 61 is on top of block 20, block 62 is on top of
    block 100, block 63 is on top of block 43, block 64 is on top of block 31, block 65 is on top of
     block 27, block 66 is on top of block 12, block 67 is on top of block 42, block 68 is on top of
     block 94, block 69 is on top of block 41, block 71 is on top of block 10, block 72 is on top of
     block 33, block 73 is on top of block 79, block 74 is on top of block 53, block 75 is on top of
     block 39, block 76 is on top of block 58, block 77 is on top of block 78, block 78 is on top of
     block 38, block 79 is on top of block 13, block 80 is on top of block 57, block 81 is on top of
     block 61, block 82 is on top of block 24, block 83 is on top of block 56, block 84 is on top of
     block 5, block 85 is on top of block 69, block 86 is on top of block 52, block 87 is on top of
    block 70, block 88 is on top of block 29, block 89 is on top of block 16, block 90 is on top of
    block 72, block 91 is on top of block 28, block 92 is on top of block 51, block 93 is on top of
    block 3, block 94 is on top of block 60, block 95 is on top of block 54, block 97 is on top of
    block 23, block 98 is on top of block 49, block 99 is on top of block 19, block 100 is on top of
     block 30, block 13 is on the table, block 22 is on the table, block 70 is on the table, and
    block 96 is on the table.


                                 Listing 9: Domain File for ChildSnack
(define (domain child-snack)
(:requirements :typing :equality)
(:types child bread-portion content-portion sandwich tray place)
(:constants kitchen - place)

(:predicates (at_kitchen_bread ?b - bread-portion)
      (at_kitchen_content ?c - content-portion)
          (at_kitchen_sandwich ?s - sandwich)
          (no_gluten_bread ?b - bread-portion)
            (no_gluten_content ?c - content-portion)
            (ontray ?s - sandwich ?t - tray)
            (no_gluten_sandwich ?s - sandwich)
      (allergic_gluten ?c - child)
          (not_allergic_gluten ?c - child)
      (served ?c - child)
      (waiting ?c - child ?p - place)
            (at ?t - tray ?p - place)
      (notexist ?s - sandwich)
  )

(:action make_sandwich_no_gluten
   :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
   :precondition (and (at_kitchen_bread ?b)
          (at_kitchen_content ?c)
          (no_gluten_bread ?b)
          (no_gluten_content ?c)
          (notexist ?s))
   :effect (and
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
       (at_kitchen_sandwich ?s)
       (no_gluten_sandwich ?s)
                  (not (notexist ?s))
       ))



                                                  16
(:action make_sandwich
   :parameters (?s - sandwich ?b - bread-portion ?c - content-portion)
   :precondition (and (at_kitchen_bread ?b)
          (at_kitchen_content ?c)
                          (notexist ?s)
          )
   :effect (and
       (not (at_kitchen_bread ?b))
       (not (at_kitchen_content ?c))
       (at_kitchen_sandwich ?s)
                  (not (notexist ?s))
       ))


(:action put_on_tray
   :parameters (?s - sandwich ?t - tray)
   :precondition (and (at_kitchen_sandwich ?s)
           (at ?t kitchen))
   :effect (and
       (not (at_kitchen_sandwich ?s))
       (ontray ?s ?t)))


(:action serve_sandwich_no_gluten
  :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
  :precondition (and
          (allergic_gluten ?c)
          (ontray ?s ?t)
          (waiting ?c ?p)
          (no_gluten_sandwich ?s)
                     (at ?t ?p)
          )
  :effect (and (not (ontray ?s ?t))
        (served ?c)))

(:action serve_sandwich
  :parameters (?s - sandwich ?c - child ?t - tray ?p - place)
  :precondition (and (not_allergic_gluten ?c)
                   (waiting ?c ?p)
        (ontray ?s ?t)
        (at ?t ?p))
  :effect (and (not (ontray ?s ?t))
        (served ?c)))

(:action move_tray
   :parameters (?t - tray ?p1 ?p2 - place)
   :precondition (and (at ?t ?p1))
   :effect (and (not (at ?t ?p1))
         (at ?t ?p2)))


)


                            Listing 10: Example Problem File for ChildSnack
(define (problem p01)
  (:domain child-snack)
  (:objects
    child1 child2 child3 child4 child5 - child
    bread1 bread2 bread3 bread4 bread5 - bread-portion
    content1 content2 content3 content4 content5 - content-portion
    tray1 tray2 tray3 - tray
    table1 table2 table3 - place
    sandw1 sandw2 sandw3 sandw4 sandw5 - sandwich
  )
  (:init
    (at tray1 kitchen)
    (at tray2 kitchen)


                                                  17
     (at tray3 kitchen)
     (at_kitchen_bread bread1)
     (at_kitchen_bread bread2)
     (at_kitchen_bread bread3)
     (at_kitchen_bread bread4)
     (at_kitchen_bread bread5)
     (at_kitchen_content content1)
     (at_kitchen_content content2)
     (at_kitchen_content content3)
     (at_kitchen_content content4)
     (at_kitchen_content content5)
     (no_gluten_bread bread1)
     (no_gluten_content content1)
     (allergic_gluten child1)
     (not_allergic_gluten child2)
     (not_allergic_gluten child3)
     (no_gluten_bread bread4)
     (no_gluten_content content4)
     (allergic_gluten child4)
     (not_allergic_gluten child5)
     (waiting child1 table1)
     (waiting child2 table1)
     (waiting child3 table2)
     (waiting child4 table2)
     (waiting child5 table3)
     (notexist sandw1)
     (notexist sandw2)
     (notexist sandw3)
     (notexist sandw4)
     (notexist sandw5)
    )
    (:goal
      (and
        (served child1)
        (served child2)
        (served child3)
        (served child4)
        (served child5)
      )
    )
)


                          Listing 11: Example Domain Description for ChildSnack
     I am preparing and serving sandwiches to children. Here are the actions I can do

Make a sandwich
Make a gluten-free sandwich
Put a sandwich on a tray
Move a tray from one place to another
Serve a sandwich to a child
Serve a gluten-free sandwich to a child

I have the following restrictions on my actions:
I can only make a sandwich if the required bread portion and content portion are both available in
    the kitchen.
I can only make a gluten-free sandwich if the bread portion and content portion are both gluten-free
    and available in the kitchen.
I can only use a sandwich object that does not already exist.
Once I make a sandwich, the corresponding bread and content portions are no longer available in the
    kitchen.
I can only put a sandwich on a tray if the sandwich is in the kitchen and the tray is in the kitchen.
I can only serve a sandwich to a child if the tray holding the sandwich is at the same place where
    the child is waiting.
I can only serve a regular sandwich to a child who is not allergic to gluten.
I can only serve a gluten-free sandwich to a child who is allergic to gluten.
I can move a tray from one place to another at any time.




                                                   18
                         Listing 12: Example Problem Description for ChildSnack
    As initial conditions I have 5 children numbered 1 to 5, 3 trays numbered 1 to 3, 5 bread
         portions numbered 1 to 5, 5 content portions numbered 1 to 5, and 5 sandwich placeholders
         numbered 1 to 5. The children assigned to tray 1 are child 1, child 2, the children assigned
         to tray 2 are child 3, child 4, and the remaining child are assigned to tray 3. Every 3rd
         child starting from child 1 must receive a gluten-free sandwich, and all other children can
         receive a regular sandwich. The bread portions whose numbers match the children that need
         gluten-free sandwiches are gluten-free, and the content portions whose numbers match the
         children that need gluten-free sandwiches are gluten-free. All trays start in the kitchen,
         all bread portions and content portions start in the kitchen, and all sandwiches still need
         to be prepared and served.
My goal is to have that child 1 has been served a sandwich, child 2 has been served a sandwich, child
      3 has been served a sandwich, child 4 has been served a sandwich, and child 5 has been served a
      sandwich.



                                 Listing 13: Domain File for OpenStacks
    (define (domain openstacks-sequencedstrips-nonADL)
(:requirements :typing :action-costs)
(:types order product count)
(:constants
 p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 - product
 o1 o2 o3 o4 o5 - order
)

(:predicates
  (includes ?o - order ?p - product)
  (waiting ?o - order)
  (started ?o - order)
  (shipped ?o - order)
  (made ?p - product)
  (stacks-avail ?s - count)
  (next-count ?s ?ns - count)
)

(:functions
(total-cost)
)

(:action open-new-stack
:parameters (?open ?new-open - count)
:precondition (and (stacks-avail ?open)(next-count ?open ?new-open))
:effect (and (not (stacks-avail ?open))(stacks-avail ?new-open) (increase (total-cost) 1))
)

(:action start-order
:parameters (?o - order ?avail ?new-avail - count)
:precondition (and (waiting ?o)(stacks-avail ?avail)(next-count ?new-avail ?avail))
:effect (and (not (waiting ?o))(started ?o)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

(:action make-product-p1
:parameters ()
:precondition (and (not (made p1))(started o1))
:effect (and (made p1))
)

(:action make-product-p2
:parameters ()
:precondition (and (not (made p2))(started o1)(started o2))
:effect (and (made p2))
)

(:action make-product-p3
:parameters ()
:precondition (and (not (made p3))(started o1)(started o2)(started o3))
:effect (and (made p3))
)


                                                  19
(:action make-product-p4
:parameters ()
:precondition (and (not (made p4))(started o2)(started o3)(started o4))
:effect (and (made p4))
)

(:action make-product-p5
:parameters ()
:precondition (and (not (made p5))(started o3)(started o4)(started o5))
:effect (and (made p5))
)

(:action make-product-p6
:parameters ()
:precondition (and (not (made p6))(started o4)(started o5))
:effect (and (made p6))
)

(:action make-product-p7
:parameters ()
:precondition (and (not (made p7))(started o5))
:effect (and (made p7))
)

(:action make-product-p8
:parameters ()
:precondition (and (not (made p8)))
:effect (and (made p8))
)

(:action make-product-p9
:parameters ()
:precondition (and (not (made p9)))
:effect (and (made p9))
)

(:action make-product-p10
:parameters ()
:precondition (and (not (made p10)))
:effect (and (made p10))
)

(:action make-product-p11
:parameters ()
:precondition (and (not (made p11)))
:effect (and (made p11))
)

(:action make-product-p12
:parameters ()
:precondition (and (not (made p12)))
:effect (and (made p12))
)

(:action ship-order-o1
:parameters (?avail ?new-avail - count)
:precondition (and (started o1)(made p1)(made p2)(made p3)(stacks-avail ?avail)(next-count ?avail ?
    new-avail))
:effect (and (not (started o1))(shipped o1)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

(:action ship-order-o2
:parameters (?avail ?new-avail - count)
:precondition (and (started o2)(made p2)(made p3)(made p4)(stacks-avail ?avail)(next-count ?avail ?
    new-avail))
:effect (and (not (started o2))(shipped o2)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

(:action ship-order-o3


                                                  20
:parameters (?avail ?new-avail - count)
:precondition (and (started o3)(made p3)(made p4)(made p5)(stacks-avail ?avail)(next-count ?avail ?
    new-avail))
:effect (and (not (started o3))(shipped o3)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

(:action ship-order-o4
:parameters (?avail ?new-avail - count)
:precondition (and (started o4)(made p4)(made p5)(made p6)(stacks-avail ?avail)(next-count ?avail ?
    new-avail))
:effect (and (not (started o4))(shipped o4)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

(:action ship-order-o5
:parameters (?avail ?new-avail - count)
:precondition (and (started o5)(made p5)(made p6)(made p7)(stacks-avail ?avail)(next-count ?avail ?
    new-avail))
:effect (and (not (started o5))(shipped o5)(not (stacks-avail ?avail))(stacks-avail ?new-avail))
)

)



                            Listing 14: Example Problem File for OpenStacks
    (define (problem p01)
(:domain openstacks-sequencedstrips-nonADL)
(:objects
 n0 n1 n2 n3 n4 n5 n6 n7 n8 n9 n10 n11 n12 - count
)

(:init
(next-count n0 n1) (next-count n1 n2) (next-count n2 n3) (next-count n3 n4) (next-count n4 n5) (
    next-count n5 n6) (next-count n6 n7) (next-count n7 n8) (next-count n8 n9) (next-count n9 n10) (
    next-count n10 n11) (next-count n11 n12)
(stacks-avail n0)

(waiting o1)
(includes o1 p1)(includes o1 p2)(includes o1 p3)

(waiting o2)
(includes o2 p2)(includes o2 p3)(includes o2 p4)

(waiting o3)
(includes o3 p3)(includes o3 p4)(includes o3 p5)

(waiting o4)
(includes o4 p4)(includes o4 p5)(includes o4 p6)

(waiting o5)
(includes o5 p5)(includes o5 p6)(includes o5 p7)

(= (total-cost) 0)
)
(:goal
(and
(shipped o1)
(shipped o2)
(shipped o3)
(shipped o4)
(shipped o5)
))
(:metric minimize (total-cost))

)



                         Listing 15: Example Domain Description for OpenStacks



                                                   21
   I am managing a factory that produces products to fulfill customer orders. Here are the actions I
        can do

Open a new stack
Start an order
Make a product
Ship an order

I have the following restrictions on my actions:
I can only start an order if that order is still waiting to be started.
I can only start an order if there is at least one available stack.
Once I start an order, that order becomes active and uses one available stack.
I can only make a product if that product has not already been made.
I can only make a product if every active order that requires that product has already been started.
Once I make a product, that product is available for all orders that require it.
I can only ship an order if that order has already been started.
I can only ship an order if all products required by that order have already been made.
Once I ship an order, that order is completed and its stack becomes available again.
Opening a new stack increases the total cost by 1.


                          Listing 16: Example Problem Description for OpenStacks
    As initial conditions I have 5 customer orders numbered 1 to 5, and 12 products numbered 1 to 12.
          Every order requires exactly 3 products. For this problem, the sliding window starts at
         product 1. Order 1 requires products 1, 2, and 3; order 2 requires products 2, 3, and 4;
         order 3 requires products 3, 4, and 5; and in general each next order shifts the required
         product window forward by one product. When the numbering reaches product 12, it wraps around
          to product 1 again. All orders are initially waiting, no products have been made yet, and
         zero stacks are open initially.
My goal is to have that order 1 is completed, order 2 is completed, order 3 is completed, order 4 is
     completed, and order 5 is completed.


                                   Listing 17: Domain File for Transport
;; Transport sequential
;;

(define (domain transport)
  (:requirements :typing :action-costs)
  (:types
       location target locatable - object
       vehicle package - locatable
       capacity-number - object
  )

 (:predicates
    (road ?l1 ?l2 - location)
    (at ?x - locatable ?v - location)
    (in ?x - package ?v - vehicle)
    (capacity ?v - vehicle ?s1 - capacity-number)
    (capacity-predecessor ?s1 ?s2 - capacity-number)
 )

 (:functions
    (road-length ?l1 ?l2 - location) - number
    (total-cost) - number
 )

 (:action drive
   :parameters (?v - vehicle ?l1 ?l2 - location)
   :precondition (and
       (at ?v ?l1)
       (road ?l1 ?l2)
     )
   :effect (and
       (not (at ?v ?l1))
       (at ?v ?l2)
       (increase (total-cost) (road-length ?l1 ?l2))


                                                    22
        )
    )

(:action pick-up
   :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity-number)
   :precondition (and
       (at ?v ?l)
       (at ?p ?l)
       (capacity-predecessor ?s1 ?s2)
       (capacity ?v ?s2)
     )
   :effect (and
       (not (at ?p ?l))
       (in ?p ?v)
       (capacity ?v ?s1)
       (not (capacity ?v ?s2))
       (increase (total-cost) 1)
     )
 )

    (:action drop
      :parameters (?v - vehicle ?l - location ?p - package ?s1 ?s2 - capacity-number)
      :precondition (and
          (at ?v ?l)
          (in ?p ?v)
          (capacity-predecessor ?s1 ?s2)
          (capacity ?v ?s1)
        )
      :effect (and
          (not (in ?p ?v))
          (at ?p ?l)
          (capacity ?v ?s2)
          (not (capacity ?v ?s1))
          (increase (total-cost) 1)
        )
    )

)


                            Listing 18: Example Problem Description for Transport
   (define (problem p01)
(:domain transport)
(:objects
 location-1 - location
 location-2 - location
 location-3 - location
 location-4 - location
 location-5 - location
 location-6 - location
 location-7 - location
 location-8 - location
 location-9 - location
 location-10 - location
 truck-1 - vehicle
 truck-2 - vehicle
 truck-3 - vehicle
 package-1 - package
 package-2 - package
 package-3 - package
 package-4 - package
 package-5 - package
 package-6 - package
 package-7 - package
 package-8 - package
 package-9 - package
 package-10 - package
 capacity-0 - capacity-number
 capacity-1 - capacity-number


                                                     23
 capacity-2 - capacity-number
 capacity-3 - capacity-number
 capacity-4 - capacity-number
)
(:init
 (= (total-cost) 0)
 (capacity-predecessor capacity-0 capacity-1)
 (capacity-predecessor capacity-1 capacity-2)
 (capacity-predecessor capacity-2 capacity-3)
 (capacity-predecessor capacity-3 capacity-4)
 (road location-1 location-2)
 (= (road-length location-1 location-2) 1)
 (road location-1 location-3)
 (= (road-length location-1 location-3) 1)
 (road location-1 location-4)
 (= (road-length location-1 location-4) 1)
 (road location-1 location-5)
 (= (road-length location-1 location-5) 1)
 (road location-1 location-6)
 (= (road-length location-1 location-6) 1)
 (road location-1 location-7)
 (= (road-length location-1 location-7) 1)
 (road location-1 location-8)
 (= (road-length location-1 location-8) 1)
 (road location-1 location-9)
 (= (road-length location-1 location-9) 1)
 (road location-1 location-10)
 (= (road-length location-1 location-10) 1)
 (road location-2 location-1)
 (= (road-length location-2 location-1) 1)
 (road location-2 location-3)
 (= (road-length location-2 location-3) 1)
 (road location-2 location-4)
 (= (road-length location-2 location-4) 1)
 (road location-2 location-5)
 (= (road-length location-2 location-5) 1)
 (road location-2 location-6)
 (= (road-length location-2 location-6) 1)
 (road location-2 location-7)
 (= (road-length location-2 location-7) 1)
 (road location-2 location-8)
 (= (road-length location-2 location-8) 1)
 (road location-2 location-9)
 (= (road-length location-2 location-9) 1)
 (road location-2 location-10)
 (= (road-length location-2 location-10) 1)
 (road location-3 location-1)
 (= (road-length location-3 location-1) 1)
 (road location-3 location-2)
 (= (road-length location-3 location-2) 1)
 (road location-3 location-4)
 (= (road-length location-3 location-4) 1)
 (road location-3 location-5)
 (= (road-length location-3 location-5) 1)
 (road location-3 location-6)
 (= (road-length location-3 location-6) 1)
 (road location-3 location-7)
 (= (road-length location-3 location-7) 1)
 (road location-3 location-8)
 (= (road-length location-3 location-8) 1)
 (road location-3 location-9)
 (= (road-length location-3 location-9) 1)
 (road location-3 location-10)
 (= (road-length location-3 location-10) 1)
 (road location-4 location-1)
 (= (road-length location-4 location-1) 1)
 (road location-4 location-2)
 (= (road-length location-4 location-2) 1)
 (road location-4 location-3)
 (= (road-length location-4 location-3) 1)


                                                24
(road location-4 location-5)
(= (road-length location-4 location-5) 1)
(road location-4 location-6)
(= (road-length location-4 location-6) 1)
(road location-4 location-7)
(= (road-length location-4 location-7) 1)
(road location-4 location-8)
(= (road-length location-4 location-8) 1)
(road location-4 location-9)
(= (road-length location-4 location-9) 1)
(road location-4 location-10)
(= (road-length location-4 location-10) 1)
(road location-5 location-1)
(= (road-length location-5 location-1) 1)
(road location-5 location-2)
(= (road-length location-5 location-2) 1)
(road location-5 location-3)
(= (road-length location-5 location-3) 1)
(road location-5 location-4)
(= (road-length location-5 location-4) 1)
(road location-5 location-6)
(= (road-length location-5 location-6) 1)
(road location-5 location-7)
(= (road-length location-5 location-7) 1)
(road location-5 location-8)
(= (road-length location-5 location-8) 1)
(road location-5 location-9)
(= (road-length location-5 location-9) 1)
(road location-5 location-10)
(= (road-length location-5 location-10) 1)
(road location-6 location-1)
(= (road-length location-6 location-1) 1)
(road location-6 location-2)
(= (road-length location-6 location-2) 1)
(road location-6 location-3)
(= (road-length location-6 location-3) 1)
(road location-6 location-4)
(= (road-length location-6 location-4) 1)
(road location-6 location-5)
(= (road-length location-6 location-5) 1)
(road location-6 location-7)
(= (road-length location-6 location-7) 1)
(road location-6 location-8)
(= (road-length location-6 location-8) 1)
(road location-6 location-9)
(= (road-length location-6 location-9) 1)
(road location-6 location-10)
(= (road-length location-6 location-10) 1)
(road location-7 location-1)
(= (road-length location-7 location-1) 1)
(road location-7 location-2)
(= (road-length location-7 location-2) 1)
(road location-7 location-3)
(= (road-length location-7 location-3) 1)
(road location-7 location-4)
(= (road-length location-7 location-4) 1)
(road location-7 location-5)
(= (road-length location-7 location-5) 1)
(road location-7 location-6)
(= (road-length location-7 location-6) 1)
(road location-7 location-8)
(= (road-length location-7 location-8) 1)
(road location-7 location-9)
(= (road-length location-7 location-9) 1)
(road location-7 location-10)
(= (road-length location-7 location-10) 1)
(road location-8 location-1)
(= (road-length location-8 location-1) 1)
(road location-8 location-2)
(= (road-length location-8 location-2) 1)


                                             25
 (road location-8 location-3)
 (= (road-length location-8 location-3) 1)
 (road location-8 location-4)
 (= (road-length location-8 location-4) 1)
 (road location-8 location-5)
 (= (road-length location-8 location-5) 1)
 (road location-8 location-6)
 (= (road-length location-8 location-6) 1)
 (road location-8 location-7)
 (= (road-length location-8 location-7) 1)
 (road location-8 location-9)
 (= (road-length location-8 location-9) 1)
 (road location-8 location-10)
 (= (road-length location-8 location-10) 1)
 (road location-9 location-1)
 (= (road-length location-9 location-1) 1)
 (road location-9 location-2)
 (= (road-length location-9 location-2) 1)
 (road location-9 location-3)
 (= (road-length location-9 location-3) 1)
 (road location-9 location-4)
 (= (road-length location-9 location-4) 1)
 (road location-9 location-5)
 (= (road-length location-9 location-5) 1)
 (road location-9 location-6)
 (= (road-length location-9 location-6) 1)
 (road location-9 location-7)
 (= (road-length location-9 location-7) 1)
 (road location-9 location-8)
 (= (road-length location-9 location-8) 1)
 (road location-9 location-10)
 (= (road-length location-9 location-10) 1)
 (road location-10 location-1)
 (= (road-length location-10 location-1) 1)
 (road location-10 location-2)
 (= (road-length location-10 location-2) 1)
 (road location-10 location-3)
 (= (road-length location-10 location-3) 1)
 (road location-10 location-4)
 (= (road-length location-10 location-4) 1)
 (road location-10 location-5)
 (= (road-length location-10 location-5) 1)
 (road location-10 location-6)
 (= (road-length location-10 location-6) 1)
 (road location-10 location-7)
 (= (road-length location-10 location-7) 1)
 (road location-10 location-8)
 (= (road-length location-10 location-8) 1)
 (road location-10 location-9)
 (= (road-length location-10 location-9) 1)
 (at truck-1 location-1)
 (capacity truck-1 capacity-4)
 (at truck-2 location-2)
 (capacity truck-2 capacity-4)
 (at truck-3 location-3)
 (capacity truck-3 capacity-4)
 (at package-1 location-1)
 (at package-2 location-1)
 (at package-3 location-1)
 (at package-4 location-1)
 (at package-5 location-2)
 (at package-6 location-2)
 (at package-7 location-2)
 (at package-8 location-3)
 (at package-9 location-3)
 (at package-10 location-3)
)
(:goal
 (and
   (at package-1 location-1)


                                              26
   (at package-2 location-4)
   (at package-3 location-8)
   (at package-4 location-5)
   (at package-5 location-3)
   (at package-6 location-2)
   (at package-7 location-6)
   (at package-8 location-9)
   (at package-9 location-7)
   (at package-10 location-10)
  )
 )
 (:metric minimize (total-cost))
)


                           Listing 19: Example Domain Description for Transport
   I am moving packages between locations using vehicles. Here are the actions I can do

Drive a vehicle from one location to another
Pick up a package with a vehicle
Drop a package from a vehicle at a location

I have the following restrictions on my actions:
I can only drive a vehicle from one location to another if there is a road connecting the two
    locations.
I can only pick up a package if the vehicle and the package are at the same location.
I can only pick up a package if the vehicle has enough remaining carrying capacity.
Once I pick up a package, the package is inside the vehicle and is no longer at the location.
I can only drop a package if the package is currently inside the vehicle.
I can only drop a package at the location where the vehicle currently is.
Once I drop a package, the package is at that location and is no longer inside the vehicle.
Driving a vehicle has a cost that depends on the road length.
Picking up and dropping a package each have a cost of 1.


                           Listing 20: Example Problem Description for Transport
    As initial conditions I have 10 locations numbered 1 to 10, 10 packages numbered 1 to 10, and 3
         vehicles numbered 1 to 3. The locations form one fully connected road network, so every
         location is directly connected to every other location in both directions. Vehicle 1 starts
         at location 1, vehicle 2 starts at location 2, and vehicle 3 starts at location 3. Packages 1
          through 4 are initially at location 1, packages 5 through 7 are initially at location 2, and
          packages 8 through 10 are initially at location 3. All 3 vehicles have carrying capacity 4,
         and every road has length 1.
My goal is to have that package 1 is at location 1, package 2 is at location 4, package 3 is at
     location 8, package 4 is at location 5, package 5 is at location 3, package 6 is at location 2,
     package 7 is at location 6, package 8 is at location 9, package 9 is at location 7, and package
     10 is at location 10.


                            Listing 21: Prompt for Regular LLM-as-Formalizer
PDDL problem file contains problem name, domain name, objects in this problem instance, init state of
     objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types.
Represent the initial state with the appropriate predicates and object arguments. Represent the goal
    state with the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
    PDDL problem file is given below.

<problem_file>
(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )


                                                    27
 (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
 (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)
</problem_file>

Notes for generating problem file:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- init state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define init state
- goal state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define goal state
- predicates with proper arguments could be combined to combine complex boolean expression to
    represent init and goal states
- The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the objects that would be arguments of predicates in init and goal states should be declared in
     :objects


Additional strict constraints for large instances (55-100 blocks):
- Output only one complete problem PDDL wrapped in <problem_file>...</problem_file>. Do not output
    any domain file.
- Include every block mentioned in the problem description exactly once in :objects, and do not
    include undeclared objects.
- Use only predicates and action-relevant symbols that are valid for the provided domain PDDL.
- In :init, ensure each block appears in exactly one support relation: either (on-table blockX) or (
    on blockX blockY), but not both.
- In :init, include (clear blockX) if and only if blockX has no block on top of it.
- In :init, include exactly one (arm-empty).
- Ensure there are no self-relations such as (on blockX blockX).
- In :goal, use only declared objects and valid predicates, and avoid contradictory goals.
- Ensure parentheses are balanced and PDDL syntax is valid.


                             Listing 22: Prompt for Regular LLM-as-Planner
You are an expert automated planner. Your task is to read a natural-language domain description, the
    corresponding problem description, and the provided ground-truth domain PDDL, reason through the
     objects, actions, and goals, and output a valid plan.

Recall the distinctions:
- The domain description explains the general world: available action schemas, predicates, and object
     types.
- The problem description gives the concrete instance: specific objects, the initial state, and the
    goals for this planning episode.
- The ground-truth domain PDDL provides the formal acton schema and predicate definitions that your
    plan must follow exactly.

Planning output requirements:
- Produce the final plan inside <plan>...</plan>. Each action must be on its own line in classical
    PDDL plan syntax, e.g. ,(move robot1 roomA roomB).
- Maintain the execution order from top to bottom. Do not include step numbers, timestamps, or
    probabilities.
- Only emit actions that are applicable given the initial state and that eventually achieve the goals
    .
- After the closing </plan> tag, do not add extra commentary.

Example format (replace names with the task-specific details):
<plan>
(pick-up block1 hand)
(stack block1 block2)
(move robot room1 room2)
</plan>

Follow this template for every problem. EOF


                            Listing 23: Prompt for D&C Problem File Header



                                                  28
PDDL problem file's header parts contain problem name, domain name, and objects in this problem
    instance.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types..
PDDL problem file header has a definitive syntax that must be followed for any problem. An abstract
    example PDDL problem file header is given below.

<header>
(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
)
</header>

Notes for generating problem file header:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- The braces should be balanced for each section of the PDDL program header
- All the objects should be declared in :objects


Additional strict constraints for all instances (5-100 blocks):
- Output only one complete problem PDDL header wrapped in <header>...</header>. Do not output any
    domain file.
- Include every block mentioned in the problem description exactly once in :objects, and do not
    include undeclared objects.
- Only write for the header parts.
- Do not write anything for :init.
- Do not write anything for :goal.
- Ensure parentheses are balanced and PDDL syntax is valid.


                           Listing 24: Prompt for D&C Problem File Main Body
PDDL problem file fact states contains init state of objects, and goal state of objects.
Based on the natural language problem description, identify the relevant init and goal states for
    this problem ONE-BY-ONE.
Represent the initial state with the appropriate predicates and object arguments. Represent the goal
    state with the appropriate predicates and object arguments.
PDDL problem file fact state has a definitive syntax that must be followed for any problem. An few
    abstract examples PDDL problem file fact state is given below.

<fact>
(predicate1 obj1 obj3) (predicate2 obj2 obj3))
</fact>
for init state

OR

<fact>
(and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
</fact>
for goal state


Notes for generating problem file fact state:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- init state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define init state.
- goal state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define goal state.
- predicates with proper arguments could be combined to combine complex boolean expression to
    represent init and goal states.
- The braces should be balanced for each fact state of the PDDL program.
- Use predicates with arguments of the right type as declared in domain file.


                                                  29
Additional strict constraints for ALL instances (5-100 blocks):
- Output only one problem PDDL fact state wrapped in <fact>...</fact>. Do not output any domain file.
- DO NOT WRITE ANY :init or :goal inside <fact>...</fact>!!!
- Use only predicates and action-relevant symbols that are valid for the provided domain PDDL.
- Section headers :init and :goal are only produced once.
- For init, ensure the one fact is a correct translation of the corresponding fact in the natural
    language problem description.
- For init, write (clear blockX) if and only if blockX is clear.
- For init, write (arm-empty) if and only if the hand is empty.
- If a fact belongs to section :init, output one init fact atom.
- Ensure there are no self-relations such as (on blockX blockX).
- For goal, use only declared objects and valid predicates, and avoid contradictory goals.
- If a fact belongs to section :goal, output one goal fact atom.
- Ensure parentheses are balanced and PDDL syntax is valid.

Important examples for incorrect and correct atomic fact:
- INVALID: (:init (clear blockX))
- INVALID: (:goal (on-table blockX))
- Valid: (clear blockX)
- Valid: (on-table blockX)


                         Listing 25: Prompt for LLM-as-Higher-Order-Formalizer
;; Original prompt
PDDL problem file contains problem name, domain name, objects in this problem instance, init state of
     objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types.
In a formal PDDL problem file, initial state have the appropriate predicates and object arguments.
In a formal PDDL problem file, goal state also have the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
    PDDL problem file is given below.

(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
  (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
  (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)

You MUST generate a PYTHON SCRIPT that, upon execution, generates the PDDL problem file that matches
    the natural language problem description:
<generator>
the python script code...
</generator>

EXAMPLE executable generator style (generalized):

<generator>
def build_init_from_unraveling_rule(n):
  blocks = [f"block{i}" for i in range(1, n + 1)]

 # Odd and even stacks are TOP -> BOTTOM with increasing numbering
 odd_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 1]
 even_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 0]

 init_facts = []

 # Convert one stack (top->bottom) to on/on-table/clear facts
 def emit_stack(stack):
     if not stack:
         return
     for idx, block in enumerate(stack):


                                                    30
         if idx == len(stack) - 1:
             init_facts.append(f"(on-table {block})")
         else:
             under = stack[idx + 1]
             init_facts.append(f"(on {block} {under})")
         if idx == 0:
             init_facts.append(f"(clear {block})")

 emit_stack(odd_stack)
 emit_stack(even_stack)

 init_facts.append("(arm-empty)")
 return blocks, init_facts


def build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts):
  lines = []
  lines.append(f"(define (problem {problem_name})")
  lines.append(f" (:domain {domain_name})")
  lines.append(f" (:objects {' '.join(blocks)})")
  lines.append(" (:init")
  for fact in init_facts:
      lines.append(f" {fact}")
  lines.append(" )")
  lines.append(" (:goal (and")
  for fact in goal_facts:
      lines.append(f" {fact}")
  lines.append(" ))")
  lines.append(")")
  return "\n".join(lines) + "\n"


def main():
  # n should be inferred from the given NL problem description in the real task
  n = 10
  problem_name = "example_problem"
  domain_name = "blocksworld"

 blocks, init_facts = build_init_from_unraveling_rule(n)

 # Goal extraction can be abstracted; replace with parsed goal facts from the given NL problem
 goal_facts = [
     "(on block1 block5)",
     "(on block2 block1)",
     "(on-table block4)"
 ]

 pddl_text = build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts)

 with open("problem.pddl", "w", encoding="utf-8") as f:
     f.write(pddl_text)


if __name__ == "__main__":
  main()
</generator>


Notes for generating the python script:
- The Python script is ONLY TRANSLATING the natural language problem description to the formal PDDL
    problem file.
- The Python script is ABSOLUTELY NOT SOLVING the BlocksWorld problem


Additional strict constraints for all instances (5-100 blocks):
- Output only one complete Python script wrapped in <generator>...</generator>. Do not output any
    domain file.
- The script MUST derive init/goal facts algorithmically from compact structure, not hardcoded full
    fact lists.
- Disallowed: manually listing full init_state/goal_state facts as constants.


                                                 31
- Required: at least one loop that constructs predicates (e.g., on/on-table/clear) from computed
    stacks or parsed patterns.
- Required: compute object list from inferred block count (do not hardcode all object names manually)
    .
- The Python script, upon execution, need to produce a complete PDDL problem file that includes every
      block mentioned in the problem description exactly once in :objects and do not include
    undeclared objects.
- The Python script, upon execution, need to produce a complete PDDL problem file that uses only
    predicates and action-relevant symbols that are valid for the provided domain PDDL.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    ensures each block appears in exactly one support relation: either (on-table blockX) or (on
    blockX blockY), but not both.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    include (clear blockX) if and only if blockX has no block on top of it.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    include exactly one (arm-empty).
- The Python script, upon execution, need to produce a complete PDDL problem file that ensures there
    are no self-relations such as (on blockX blockX).
- The Python script, upon execution, need to produce a complete PDDL problem file that in :goal, use
    only declared objects and valid predicates, and avoid contradictory goals.
- The Python script, upon execution, need to produce a complete PDDL problem file that ensures
    parentheses are balanced and PDDL syntax is valid.

;; Second stage LLM-as-Higher-Order-Formalizer Prompt for BlocksWorld
You generated a first draft of generator.py. Now review the loops in that script carefully before
    producing the final answer. Focus on whether the generator will exactly reproduce the target
    OpenStacks problem PDDL when executed. Regenerate the complete generator.py script now. Use the
    same original task prompt again below as the specification. Output only one <generator>...</
    generator> block, with only raw Python source code inside it.

Original task prompt:
{original_prompt}


                         Listing 26: Prompt for LLM-as-Planner for ChildSnack
   You are an expert automated planner. Your task is to read a natural-language domain description,
       the corresponding problem description, and the provided ground-truth domain PDDL, reason
       through the objects, actions, and goals, and output a valid plan.

Recall the distinctions:
- The domain description explains the general world: available action schemas, predicates, and object
     types.
- The problem description gives the concrete instance: specific objects, the initial state, and the
    goals for this planning episode.
- The ground-truth domain PDDL provides the formal acton schema and predicate definitions that your
    plan must follow exactly.

Planning output requirements:
- Produce the final plan inside <plan>...</plan>. Each action must be on its own line in classical
    PDDL plan syntax, e.g. `(move robot1 roomA roomB)`.
- Maintain the execution order from top to bottom. Do not include step numbers, timestamps, or
    probabilities.
- Only emit actions that are applicable given the initial state and that eventually achieve the goals
    .
- After the closing </plan> tag, do not add extra commentary.

Example format (replace names with the task-specific details):
<plan>
(make_sandwich_no_gluten sandw1 bread1 content1)
(put_on_tray sandw1 tray1)
(move_tray tray1 kitchen table1)
(serve_sandwich_no_gluten sandw1 child1 tray1 table1)
</plan>

Follow this template for every problem. EOF


                        Listing 27: Prompt for LLM-as-Formalizer for ChildSnack



                                                  32
    PDDL problem file contains problem name, domain name, objects in this problem instance, init
         state of objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
     with their names and types.
Represent the initial state with the appropriate predicates and object arguments. Represent the goal
     state with the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
     PDDL problem file is given below.

<problem_file>
(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
  (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
  (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)
</problem_file>

Notes for generating problem file:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- init state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define init state
- goal state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define goal state
- predicates with proper arguments could be combined to combine complex boolean expression to
    represent init and goal states
- The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the objects that would be arguments of predicates in init and goal states should be declared in
     :objects


Additional strict constraints for large instances (5-30 children):
- Output only one complete problem PDDL wrapped in <problem_file>...</problem_file>. Do not output
    any domain file.
- Include every required problem object exactly once in :objects, and do not include undeclared or
    duplicate objects.
- Use only predicates and action-relevant symbols that are valid for the provided domain PDDL.
- In this ChildSnack formulation, declare all required children, bread-portion objects,
    content-portion objects, sandwich objects, tray objects, and place objects exactly once using
    valid names and valid types from the problem description.
- Do not declare the kitchen as a problem object if it is already provided as a domain constant; use
    it only where valid predicates require it.
- In :init, include the required at facts for trays, the required at_kitchen_bread facts for bread
    portions, the required at_kitchen_content facts for content portions, and the required notexist
    facts for sandwich objects using only declared objects and valid predicates.
- In :init, assign each child exactly one valid gluten-status predicate, and include the required
    no_gluten_bread and no_gluten_content facts exactly for the intended gluten-free ingredients.
- In :init, include exactly one valid waiting fact for each child at the intended place, using only
    declared objects and valid predicates.
- In :goal, include the required served facts for all and only the intended children, using only
    declared objects and valid predicates, and avoid contradictory goals.
- Ensure parentheses are balanced and PDDL syntax is valid.


                  Listing 28: Prompt for LLM-as-Higher-Order-Formalizer for ChildSnack
;; Original Prompt
PDDL problem file contains problem name, domain name, objects in this problem instance, init state of
     objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types.
In a formal PDDL problem file, initial state have the appropriate predicates and object arguments.
In a formal PDDL problem file, goal state also have the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example


                                                  33
    PDDL problem file is given below.

(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
  (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
  (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)

You MUST generate a PYTHON SCRIPT that, upon execution, generates the PDDL problem file that matches
    the natural language problem description:
<generator>
the python script code...
</generator>

EXAMPLE executable generator style from another domain (generalized):

<generator>
def build_init_from_unraveling_rule(n):
  blocks = [f"block{i}" for i in range(1, n + 1)]

 # Odd and even stacks are TOP -> BOTTOM with increasing numbering
 odd_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 1]
 even_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 0]

 init_facts = []

 # Convert one stack (top->bottom) to on/on-table/clear facts
 def emit_stack(stack):
     if not stack:
         return
     for idx, block in enumerate(stack):
         if idx == len(stack) - 1:
             init_facts.append(f"(on-table {block})")
         else:
             under = stack[idx + 1]
             init_facts.append(f"(on {block} {under})")
         if idx == 0:
             init_facts.append(f"(clear {block})")

 emit_stack(odd_stack)
 emit_stack(even_stack)

 init_facts.append("(arm-empty)")
 return blocks, init_facts


def build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts):
  lines = []
  lines.append(f"(define (problem {problem_name})")
  lines.append(f" (:domain {domain_name})")
  lines.append(f" (:objects {' '.join(blocks)})")
  lines.append(" (:init")
  for fact in init_facts:
      lines.append(f" {fact}")
  lines.append(" )")
  lines.append(" (:goal (and")
  for fact in goal_facts:
      lines.append(f" {fact}")
  lines.append(" ))")
  lines.append(")")
  return "\n".join(lines) + "\n"


def main():
  # n should be inferred from the given NL problem description in the real task


                                                    34
 n = 10
 problem_name = "example_problem"
 domain_name = "xxx"

 blocks, init_facts = build_init_from_unraveling_rule(n)

 # Goal extraction can be abstracted; replace with parsed goal facts from the given NL problem
 goal_facts = [
     "(on block1 block5)",
     "(on block2 block1)",
     "(on-table block4)"
 ]

 pddl_text = build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts)

 with open("problem.pddl", "w", encoding="utf-8") as f:
     f.write(pddl_text)


if __name__ == "__main__":
  main()
</generator>


Notes for generating the python script:
- The Python script is ONLY TRANSLATING the natural language problem description to the formal PDDL
    problem file.
- The Python script is ABSOLUTELY NOT SOLVING the ChildSnack problem


Additional strict constraints for all instances (5-30 children):
- Output only one complete Python script wrapped in <generator>...</generator>. Do not output any
    domain file.
- The script MUST derive init/goal facts algorithmically from compact structure, not hardcoded full
    fact lists.
- Disallowed: manually listing full init_state/goal_state facts as constants.
- Required: at least one loop that constructs predicates (e.g., waiting/at_kitchen_bread/served) from
     parsed patterns.
- Required: compute object list from inferred child count and the fixed template counts for breads,
    contents, sandwiches, trays, and tables (do not hardcode all object names manually).
- The Python script, upon execution, need to produce a complete PDDL problem file that includes every
     required child, bread-portion, content-portion, tray, table, and sandwich object exactly once
    in :objects and does not include undeclared problem objects.
- The Python script, upon execution, need to produce a complete PDDL problem file that uses only
    predicates and object arguments that are valid for the provided ChildSnack domain PDDL.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    places every tray at exactly one valid place, with the kitchen referenced only as the domain
    constant kitchen and not redeclared in :objects.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    places every bread portion exactly once with at_kitchen_bread and every content portion exactly
    once with at_kitchen_content.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    marks each sandwich placeholder with notexist exactly once and does not also place that sandwich
     at the kitchen or on a tray initially.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    assigns each child exactly one gluten-status fact, either allergic_gluten or not_allergic_gluten,
     but not both.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    assigns no_gluten_bread and no_gluten_content exactly to the portions required by the described
    template pattern, without adding those facts to regular portions.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    places every child in exactly one waiting fact at exactly one valid table according to the
    described tray-assignment pattern.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :goal,
    includes exactly the served facts for all described children and avoids contradictory or
    undeclared goals.
- The Python script, upon execution, need to produce a complete PDDL problem file that ensures
    parentheses are balanced and PDDL syntax is valid.

;; Second stage prompt


                                                 35
You generated a first draft of generator.py. Now review the loops and regenerated facts carefully
    before producing the final answer.

================================================================================
MOST IMPORTANT OVERARCHING LESSON FROM YOUR PREVIOUS GENERATION:
For larger ChildSnack instances, do NOT summarize, compress, or reconstruct the instance-specific
    patterns from intuition. Your main failure mode is inventing compact formulas for gluten/
allergy residue classes or child-to-table waiting assignments instead of preserving the exact facts
    specified by the original prompt. A small off-by-one modulo error or a guessed table
chunking rule will scale into many missing and extra init facts. Treat the exact residue class and
    exact waiting assignments as data to preserve, not as patterns to guess.
================================================================================

Focus on whether the generator will exactly reproduce the target ChildSnack problem PDDL when
    executed. In particular, check:
- The waiting child-to-table loop must match the problem-specific child/table assignment exactly.
- Do not assume children are assigned sequentially to tables in fixed blocks unless the problem
    explicitly says so; assignments may be shifted, reversed, or cyclic.
- Keep table/place assignment logic independent from allergy/gluten logic.
- Check the gluten/allergy/no-gluten pattern separately, including the correct modulo offset for
    children, bread portions, and content portions.
- Check that object loops create all children, breads, contents, sandwiches, trays, and table/place
    objects with valid PDDL names and types.

Regenerate the complete generator.py script now. Use the same original task prompt again below as the
     specification. Output only one <generator>...</generator> block, with only raw Python
source code inside it.

Original task prompt:
{original_prompt}


                         Listing 29: Prompt for LLM-as-Planner for OpenStacks
    You are an expert automated planner. Your task is to read a natural-language domain description,
         the corresponding problem description, and the provided ground-truth domain PDDL, reason
         through the objects, actions, and goals, and output a valid plan.
Recall the distinctions:
- The domain description explains the general world: available action schemas, predicates, and object
      types.
- The problem description gives the concrete instance: specific objects, the initial state, and the
     goals for this planning episode.
- The ground-truth domain PDDL provides the formal acton schema and predicate definitions that your
     plan must follow exactly.

Planning output requirements:
- Produce the final plan inside <plan>...</plan>. Each action must be on its own line in classical
    PDDL plan syntax, e.g. `(move robot1 roomA roomB)`.
- Maintain the execution order from top to bottom. Do not include step numbers, timestamps, or
    probabilities.
- Only emit actions that are applicable given the initial state and that eventually achieve the goals
    .
- After the closing </plan> tag, do not add extra commentary.

Example format (replace names with the task-specific details):
<plan>
(start-order o1 n0 n1)
(make-product p1)
(ship-order o1 n1 n0)
</plan>

Follow this template for every problem. EOF


                        Listing 30: Prompt for LLM-as-Formalizer for OpenStacks
    PDDL problem file contains problem name, domain name, objects in this problem instance, init
         state of objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
     with their names and types.


                                                  36
Represent the initial state with the appropriate predicates and object arguments. Represent the goal
    state with the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
    PDDL problem file is given below.

<problem_file>
(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
  (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
  (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)
</problem_file>

Notes for generating problem file:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- init state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define init state
- goal state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define goal state
- predicates with proper arguments could be combined to combine complex boolean expression to
    represent init and goal states
- The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the objects that would be arguments of predicates in init and goal states should be declared in
     :objects


Additional strict constraints for large instances (5-30 customer orders):
- Output only one complete problem PDDL wrapped in <problem_file>...</problem_file>. Do not output
    any domain file.
- Include every required problem object exactly once in :objects, and do not include undeclared or
    duplicate objects.
- Use only predicates and action-relevant symbols that are valid for the provided domain PDDL.
- In this OpenStacks formulation, include only the count objects in :objects exactly once each, and
    ensure the count objects run from n0 up to nM where M = max(number of orders, number of products
    ).
- In :init, include exactly one (stacks-avail n0).
- In :init, include the full next-count chain from (next-count n0 n1) through (next-count n{M-1} nM),
     using only declared count objects.
- In :init, include every waiting order exactly once with the valid waiting predicate.
- In :init, include every required includes relation between orders and products exactly as specified
     by the problem description, using only declared objects and valid predicates.
- In :goal, include the required shipped facts for all and only the intended orders, using only
    declared objects and valid predicates, and avoid contradictory goals.
- Ensure parentheses are balanced and PDDL syntax is valid.


                  Listing 31: Prompt for LLM-as-Higher-Order-Formalizer for OpenStacks
;; Original Prompt
PDDL problem file contains problem name, domain name, objects in this problem instance, init state of
     objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types.
In a formal PDDL problem file, initial state have the appropriate predicates and object arguments.
In a formal PDDL problem file, goal state also have the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
    PDDL problem file is given below.

(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1


                                                  37
      obj3, obj4 - type2
    )
    (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
    (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)

You MUST generate a PYTHON SCRIPT that, upon execution, generates the PDDL problem file that matches
    the natural language problem description:
<generator>
the python script code...
</generator>

EXAMPLE executable generator style from another domain (generalized):

<generator>
def build_init_from_unraveling_rule(n):
  blocks = [f"block{i}" for i in range(1, n + 1)]

    # Odd and even stacks are TOP -> BOTTOM with increasing numbering
    odd_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 1]
    even_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 0]

    init_facts = []

    # Convert one stack (top->bottom) to on/on-table/clear facts
    def emit_stack(stack):
        if not stack:
            return
        for idx, block in enumerate(stack):
            if idx == len(stack) - 1:
                init_facts.append(f"(on-table {block})")
            else:
                under = stack[idx + 1]
                init_facts.append(f"(on {block} {under})")
            if idx == 0:
                init_facts.append(f"(clear {block})")

    emit_stack(odd_stack)
    emit_stack(even_stack)

    init_facts.append("(arm-empty)")
    return blocks, init_facts


def build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts):
  lines = []
  lines.append(f"(define (problem {problem_name})")
  lines.append(f" (:domain {domain_name})")
  lines.append(f" (:objects {' '.join(blocks)})")
  lines.append(" (:init")
  for fact in init_facts:
      lines.append(f" {fact}")
  lines.append(" )")
  lines.append(" (:goal (and")
  for fact in goal_facts:
      lines.append(f" {fact}")
  lines.append(" ))")
  lines.append(")")
  return "\n".join(lines) + "\n"


def main():
  # n should be inferred from the given NL problem description in the real task
  n = 10
  problem_name = "example_problem"
  domain_name = "xxx"

    blocks, init_facts = build_init_from_unraveling_rule(n)

    # Goal extraction can be abstracted; replace with parsed goal facts from the given NL problem


                                                    38
 goal_facts = [
     "(on block1 block5)",
     "(on block2 block1)",
     "(on-table block4)"
 ]

 pddl_text = build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts)

 with open("problem.pddl", "w", encoding="utf-8") as f:
     f.write(pddl_text)


if __name__ == "__main__":
  main()
</generator>


Notes for generating the python script:
- The Python script is ONLY TRANSLATING the natural language problem description to the formal PDDL
    problem file.
- The Python script is ABSOLUTELY NOT SOLVING the Openstacks problem


Additional strict constraints for all instances (5-30 orders):
- Output only one complete Python script wrapped in <generator>...</generator>. Do not output any
    domain file.
- The script MUST derive init/goal facts algorithmically from compact structure, not hardcoded full
    fact lists.
- Disallowed: manually listing full init_state/goal_state facts as constants.
- Required: at least one loop that constructs predicates (e.g., waiting/includes/next-count) from
    parsed patterns.
- Required: compute the count-object list from the inferred maximum count needed by the instance (do
    not hardcode all object names manually).
- For this OpenStacks formulation, the count objects and the next-count chain must run from n0 up to
    nM where M = max(number of orders, number of products), not just the number of orders.
- The Python script, upon execution, need to produce a complete PDDL problem file that includes every
     required count object exactly once in :objects, and uses only order and product symbols that
    are valid for the generated domain file.
- The Python script, upon execution, need to produce a complete PDDL problem file that uses only
    predicates and action-relevant symbols that are valid for the provided domain PDDL.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    includes a valid next-count chain over the declared count objects, with no missing links or
    invalid count references.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    includes exactly one initial stacks-avail fact, and that fact must use a declared count object.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    includes exactly one waiting fact for each order described in the natural language problem
    description, and does not include undeclared orders.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    derives the includes facts algorithmically from the compact order-product pattern in the natural
     language problem description, and uses only valid order/product symbols from the generated
    domain file.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :goal,
    includes exactly the shipped facts required by the natural language problem description, uses
    only valid order symbols, and avoids contradictory goals.
- The Python script, upon execution, need to produce a complete PDDL problem file that ensures
    parentheses are balanced and PDDL syntax is valid.


HIGHLY IMPORTANT additional requirements for all instances (5-30 customer orders):
- In this OpenStacks formulation, only the count objects n0 ... nM belong in :objects. Do not declare
     order symbols (such as o1, o2, ...) or product symbols (such as p1, p2, ...) in :objects.
- Do not place order or product symbols in the same typed object list as the count objects. Only the
    n-symbols should appear before "- count".
- Do not assign order symbols or product symbols the type count or any other type in :objects.
- The next-count relation must be a simple forward chain only: (next-count n0 n1), (next-count n1 n2)
    , ..., (next-count n{M-1} nM).
- Do not add any wraparound, backward, or extra next-count fact. In particular, do not add a fact
    like (next-count nM n0).
- Do not invent extra structural facts beyond those implied by the problem description and the


                                                 39
    required OpenStacks chain/count structure.

;; Second stage prompt
You generated a first draft of generator.py. Now review the loops in that script carefully before
    producing the final answer.

Focus on whether the generator will exactly reproduce the target OpenStacks problem PDDL when
    executed. In particular, check:
- The count-object and next-count loops cover exactly the required n0..nM objects and full chain.
- The waiting-order loop covers every order exactly once.
- The includes/product-window loop uses the correct sliding-window start and wraparound over products
     p1..p12.
- The generated PDDL facts are complete, valid parenthesized facts with correct object names and
    types.

Regenerate the complete generator.py script now. Use the same original task prompt again below as the
     specification. Output only one <generator>...</generator> block, with only raw Python source
    code inside it.

Original task prompt:
{original_prompt}


                            Listing 32: Prompt for LLM-as-Planner for Transport
   You are an expert automated planner. Your task is to read a natural-language domain description,
       the corresponding problem description, and the provided ground-truth domain PDDL, reason
       through the objects, actions, and goals, and output a valid plan.

Recall the distinctions:
- The domain description explains the general world: available action schemas, predicates, and object
     types.
- The problem description gives the concrete instance: specific objects, the initial state, and the
    goals for this planning episode.
- The ground-truth domain PDDL provides the formal acton schema and predicate definitions that your
    plan must follow exactly.

Planning output requirements:
- Produce the final plan inside <plan>...</plan>. Each action must be on its own line in classical
    PDDL plan syntax, e.g. `(move robot1 roomA roomB)`.
- Maintain the execution order from top to bottom. Do not include step numbers, timestamps, or
    probabilities.
- Only emit actions that are applicable given the initial state and that eventually achieve the goals
    .
- After the closing </plan> tag, do not add extra commentary.

Example format (replace names with the task-specific details):
<plan>
(pick-up truck-1 location-1 package-1 capacity-3 capacity-4)
(drive truck-1 location-1 location-2)
(drop truck-1 location-2 package-1 capacity-3 capacity-4)
</plan>

Follow this template for every problem. EOF


                           Listing 33: Prompt for LLM-as-Formalizer for Transport
    PDDL problem file contains problem name, domain name, objects in this problem instance, init
         state of objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
     with their names and types.
Represent the initial state with the appropriate predicates and object arguments. Represent the goal
     state with the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
     PDDL problem file is given below.

<problem_file>
(define
  (problem problem_name)


                                                    40
 (:domain domain_name)
 (:objects
   obj1 obj2 - type1
   obj3, obj4 - type2
 )
 (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
 (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)
</problem_file>

Notes for generating problem file:
- obj1, obj2, ... are only representative and should be replaced with appropriate objects. There
    could be any number of objects with their types.
- init state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define init state
- goal state with predicate1 & predicate2 is only representative and should be replaced with
    appropriate predicates that define goal state
- predicates with proper arguments could be combined to combine complex boolean expression to
    represent init and goal states
- The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the objects that would be arguments of predicates in init and goal states should be declared in
     :objects


Additional strict constraints for large instances (10-30 locations):
- Output only one complete problem PDDL wrapped in <problem_file>...</problem_file>. Do not output
    any domain file.
- Include every required problem object exactly once in :objects, and do not include undeclared or
    duplicate objects.
- Use only predicates and action-relevant symbols that are valid for the provided domain PDDL.
- In this Transport formulation, declare all locations, vehicles, packages, and capacity-number
    objects exactly once using valid names and valid types from the problem description.
- In :init, include the full capacity-predecessor chain using only declared capacity-number objects
    and valid predicates.
- In :init, include the complete fully connected bidirectional road network between all distinct
    locations, and include the corresponding road-length facts exactly as required by the problem
    description.
- In :init, place each vehicle at exactly one valid starting location and assign each vehicle the
    correct carrying capacity using only declared objects and valid predicates.
- In :init, place each package at exactly one valid starting location, and do not place the same
    package at multiple locations or simultaneously inside a vehicle unless the problem description
    requires it.
- In :goal, include the required package destination facts for all and only the intended packages,
    using only declared objects and valid predicates, and avoid contradictory goals.
- Ensure parentheses are balanced and PDDL syntax is valid.


                  Listing 34: Prompt for LLM-as-Higher-Order-Formalizer for Transport
;; Original Prompt
PDDL problem file contains problem name, domain name, objects in this problem instance, init state of
     objects, and goal state of objects.
Based on the natural language problem description, identify the relevant objects for this problem
    with their names and types.
In a formal PDDL problem file, initial state have the appropriate predicates and object arguments.
In a formal PDDL problem file, goal state also have the appropriate predicates and object arguments.
PDDL problem file has a definitive syntax that must be followed for any problem. An abstract example
    PDDL problem file is given below.

(define
  (problem problem_name)
  (:domain domain_name)
  (:objects
    obj1 obj2 - type1
    obj3, obj4 - type2
  )
  (:init (predicate1 obj1 obj3) (predicate2 obj2 obj3))
  (:goal (and (predicate1 obj1 obj4) (predicate2 obj2 obj3)))
)


                                                  41
You MUST generate a PYTHON SCRIPT that, upon execution, generates the PDDL problem file that matches
    the natural language problem description:
<generator>
the python script code...
</generator>

EXAMPLE executable generator style from another domain (generalized):

<generator>
def build_init_from_unraveling_rule(n):
  blocks = [f"block{i}" for i in range(1, n + 1)]

 # Odd and even stacks are TOP -> BOTTOM with increasing numbering
 odd_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 1]
 even_stack = [b for i, b in enumerate(blocks, start=1) if i % 2 == 0]

 init_facts = []

 # Convert one stack (top->bottom) to on/on-table/clear facts
 def emit_stack(stack):
     if not stack:
         return
     for idx, block in enumerate(stack):
         if idx == len(stack) - 1:
             init_facts.append(f"(on-table {block})")
         else:
             under = stack[idx + 1]
             init_facts.append(f"(on {block} {under})")
         if idx == 0:
             init_facts.append(f"(clear {block})")

 emit_stack(odd_stack)
 emit_stack(even_stack)

 init_facts.append("(arm-empty)")
 return blocks, init_facts


def build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts):
  lines = []
  lines.append(f"(define (problem {problem_name})")
  lines.append(f" (:domain {domain_name})")
  lines.append(f" (:objects {' '.join(blocks)})")
  lines.append(" (:init")
  for fact in init_facts:
      lines.append(f" {fact}")
  lines.append(" )")
  lines.append(" (:goal (and")
  for fact in goal_facts:
      lines.append(f" {fact}")
  lines.append(" ))")
  lines.append(")")
  return "\n".join(lines) + "\n"


def main():
  # n should be inferred from the given NL problem description in the real task
  n = 10
  problem_name = "example_problem"
  domain_name = "xxx"

 blocks, init_facts = build_init_from_unraveling_rule(n)

 # Goal extraction can be abstracted; replace with parsed goal facts from the given NL problem
 goal_facts = [
     "(on block1 block5)",
     "(on block2 block1)",
     "(on-table block4)"
 ]


                                                    42
 pddl_text = build_problem_pddl(problem_name, domain_name, blocks, init_facts, goal_facts)

 with open("problem.pddl", "w", encoding="utf-8") as f:
     f.write(pddl_text)


if __name__ == "__main__":
  main()
</generator>


Notes for generating the python script:
- The Python script is ONLY TRANSLATING the natural language problem description to the formal PDDL
    problem file.
- The Python script is ABSOLUTELY NOT SOLVING the Transport problem


Additional strict constraints for all instances (10-30 locations):
- Output only one complete Python script wrapped in <generator>...</generator>. Do not output any
    domain file.
- The script MUST derive init/goal facts algorithmically from compact structure, not hardcoded full
    fact lists.
- Disallowed: manually listing full init\_state/goal\_state facts as constants.
- Required: at least one loop that constructs predicates (e.g., road/location/at/at-package/capacity)
     from computed patterns.
- Required: compute object lists from inferred location count, package count, and vehicle count (do
    not hardcode all object names manually).
- The Python script, upon execution, need to produce a complete PDDL problem file that includes every
     location, package, and vehicle mentioned in the problem description exactly once in :objects
    and do not include undeclared objects.
- The Python script, upon execution, need to produce a complete PDDL problem file that uses only
    predicates and action-relevant symbols that are valid for the provided domain PDDL.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    places each vehicle at exactly one declared location and each package at exactly one declared
    location.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    assigns the fixed carrying capacity to every vehicle using only valid capacity-related symbols
    from the provided domain PDDL.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :init,
    derives the bidirectional road connectivity facts algorithmically from the described fully
    connected transport network and avoids invalid self-connections unless they are explicitly
    described.
- The Python script, upon execution, need to produce a complete PDDL problem file that in :goal,
    assigns each package to exactly one declared destination location, uses only declared objects
    and valid predicates, and avoids contradictory goals.
- The Python script, upon execution, need to produce a complete PDDL problem file that ensures
    parentheses are balanced and PDDL syntax is valid.

;; Second stage prompt
You generated a first draft of generator.py. Now review the loops, object construction, and generated
     facts carefully before producing the final answer.

Focus on whether the generator will exactly reproduce the target Transport problem PDDL when executed
    . In particular, check:
- The :objects section must be typed into separate groups: locations - location, packages - package,
    trucks - vehicle, and capacity numbers - capacity-number.
- Do not flatten typed object groups into one untyped list/string, and do not pass a pre-joined
    object string to code that joins it again.
- The initial package locations must match the Transport pattern exactly: package-1..package-4 at
    location-1, package-5..package-7 at location-2, and package-8..package-10 at location-3.
- Each truck starts at its matching location: truck-1 at location-1, truck-2 at location-2, truck-3
    at location-3, and each truck has exactly capacity-4.
- The capacity-predecessor chain must include capacity-0->capacity-1, capacity-1->capacity-2,
    capacity-2->capacity-3, and capacity-3->capacity-4.
- The road network must contain every directed road between distinct locations, with a valid
    parenthesized (= (road-length A B) 1) fact for every directed road.
- Keep package goal facts exactly problem-specific; do not infer or reorder them unless the prompt
    specifies that mapping.



                                                 43
Regenerate the complete generator.py script now. Use the same original task prompt again below as the
     specification. Output only one <generator>...</generator> block, with only raw Python source
    code inside it.

Original task prompt:
{original_prompt}




                                                 44
