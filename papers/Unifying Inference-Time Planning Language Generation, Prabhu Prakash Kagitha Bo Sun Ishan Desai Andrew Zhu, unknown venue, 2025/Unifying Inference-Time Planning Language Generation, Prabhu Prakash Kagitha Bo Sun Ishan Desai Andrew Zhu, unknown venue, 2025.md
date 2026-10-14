                                                         Unifying Inference-Time Planning Language Generation

                                                  Prabhu Prakash Kagitha        Bo Sun     Ishan Desai         Andrew Zhu
                                                       Cassie Huang        Manling Li    Ziyang Li        Li Zhang
                                                                 Drexel University     University of Pennsylvania
                                                              Northwestern University    Johns Hopkins University
                                                               {prabhuprakash.k,harry.zhang}@drexel.edu



                                                                  Abstract                             program in languages such as the Planning Do-
                                                                                                       main Definition Language (PDDL). Such a pro-
                                                A line of work in planning uses LLM not to             gram is input into a formal solver to deterministi-
arXiv:2505.14763v2 [cs.CL] 7 Oct 2025




                                                generate a plan, but to generate a formal repre-       cally search for a plan (Tantakoun et al., 2025).
                                                sentation in some planning language, which can
                                                                                                       The LLM-as-formalizer methodology (Figure 1)
                                                be input into a symbolic solver to deterministi-
                                                cally find a plan. While showing improved trust        has been widely advocated in literature due to its re-
                                                and promising performance, dozens of recent            portedly better performance and formal guarantees
                                                publications have proposed scattered methods           compared to LLM-as-planner (Liu et al., 2023).
                                                on a variety of benchmarks under different ex-         However, the success of LLM-as-formalizer in pre-
                                                perimental settings. We attempt to unify the           vious work has primarily been tied to closed-source
                                                inference-time LLM-as-formalizer methodol-             LLMs that are likely huge in terms of parameters
                                                ogy for classical planning by proposing a unify-
                                                                                                       and esoteric in terms of engineering. In contrast,
                                                ing framework based on intermediate represen-
                                                tations. We thus systematically evaluate more
                                                                                                       preliminary experiments on open-source, smaller
                                                than a dozen pipelines that subsume most ex-           LLMs have been shown to exhibit much lower
                                                isting work, while proposing novel ones that           performance (Huang and Zhang, 2025), severely
                                                involve syntactically similar but high resource        hindering the accessibility and democratization of
                                                intermediate languages (such as a Python wrap-         LLM-assisted planning. Moreover, most if not all
                                                per of PDDL). We provide recipes for planning          past work has employed unsystematic designs of
                                                language generation pipelines, draw a series of        pipelines of piecemeal techniques, hence the direc-
                                                conclusions showing the efficacy of their vari-
                                                                                                       tion of improvement remains unclear.
                                                ous components, and evidence their robustness
                                                against problem complexity.1                              In this work, we attempt to unify the
                                                                                                       LLM-as-formalizer methodology for classical plan-
                                                                                                       ning. We first propose a theoretical framework
                                        1       Introduction                                           based on the number and interplay of interme-
                                                                                                       diate representations (IR). This framework sub-
                                        Large language models (LLMs) have been exten-                  sumes most if not all prior work on planning lan-
                                        sively applied to classical planning, an important             guage generation while opening new paths for ex-
                                        step for complex problem solving in artificial in-             perimentation. Concretely, we propose the use
                                        telligence. Given a textual description of the do-             of a high-resource but syntactically similar IR,
                                        main and problem of an environment, LLMs of-                   namely a Python wrapper of PDDL, to achieve
                                        ten directly generate a sequence of actions in an              competitive performance. We systematically in-
                                        end-to-end manner (Wei et al., 2025). Despite                  stantiate and evaluate pipelines that subsume most
                                        much better domain adaptation ability than sym-                prior work and validate the challenge for open-
                                        bolic methods, the LLM-as-planner methodology                  source, mid-sized LLMs no more than 32B pa-
                                        is not verifiable and interpretable by nature, in              rameters. On 4 standard benchmarks (IPC, 1998),
                                        addition to underperforming complex problems                   we show that IR and revision by solver feed-
                                        (Valmeekam et al., 2023a). Alternatively, a re-                back are the keys ingredients of a successful
                                        cent line of work re-imagines the role of LLMs                 LLM-as-formalizer pipeline, which consistently
                                        not to generate the plan, but to generate a formal             outperforms LLM-as-formalizer especially when
                                            Our code and data are at https://github.com/
                                            1                                                          the problem complexity increases. Even so, other
                                        prakashkagitha/llm-pddl-gen.                                   intuitive methods such as constrained decoding by

                                                                                                   1
                                                                        LLM-as-planner

Domain                                             Formalization in PDDL                                                  Plan




                                                                                                                 Solver
 You can move one block at                                                                                                unstack(red, blue)
                                                   Domain File (DF)                   Problem File (PF)                   put_down(red)




                               LLM-as-formalizer
 once. You can only pick up
                                                                                                                          pick_up(blue)
 a block from this table                           (define (domain blocksworld)        (define (problem
                                                                                                                          stack(blue, red)
 only if there’s nothing on                          (:predicate                           reverse-two-blocks)
                                                       (on ?x ?y) (ontable ?x)           (:domain blocksworld)
 top of it and put it down                             (clear ?x) (holding ?x) …)        (:objects red blue)
 on the table. You can also                          (:action pick-up                    (:init
 unstack or stack a block on                           :parameters (?x)                    (on red blue)                     Evaluator
 another block.                                        :precondition (and                  (ontable blue)
                                                         (ontable ?x) (clear ?x) …)        (clear red) …)
Problem                                                :effect (and (holding ?x)         (:goal (and                      Gold PDDL
                                                         (not (ontable ?x)) …)             (on blue red)
                                                     (:action put-down …)                  (ontable red)                  (define   (define
 You see a red block on a                                                                                                  (domai    (:doma
                                                     (:action unstack …)                   (clear blue)))
 blue block on the table.                            (:action stack …))                )                                    (:pre     (:obj
 You’d like to reverse them.                                                                                                (:act     (:ini



Figure 1: An illustration of using LLM as a planner or a formalizer in classical planning. While LLM-as-planner
generates a plan directly, LLM-as-formalizer formalizes a PDDL domain file and problem which evoke a solver to
find a plan. The plan is evaluated against ground-truth PDDL that simulates the environment.


grammar or a natural language IR resembling chain-                               pre-conditions of each action, and (ii) constitutes
of-thought do not improve performance over end-                                  a successful transition from the initial states and
to-end PDDL generation. We pose this work as                                     goal states.
a building block to greatly accelerate progress in                                  The domain file DF is defined by three main
LLM-as-formalizer and planning.                                                  components: types (T ), predicates (R), and action
                                                                                 semantics (am , ap , ae ):
2    Task Formulation                                                            1. Types: T = t1 , . . . , tn is the set of entity types
We will first formally define the classical planning                                present in the environment.
task in line with established literature of STRIPS                               2. Predicates: R = r1 , . . . , rn is the set of rela-
(Fikes and Nilsson, 1971) and recent conventions in                                 tional predicates, each in the form of r(t̄), where
the natural language processing community (Huang                                    t̄ is a tuple of types that participate in relation r.
and Zhang, 2025), before introducing our theoretic                               3. Action semantics: given an action a ∈ A, am ,
framework for LLM-as-formalizer.                                                    ap and ae are its parameters, pre-conditions
   Formally, the input I of a classical planning task                               and effects. The parameters am are a set of
consists of a triplet (Dd , Dp , DFG′ ), where:                                     types t̄ that participate in this action. The pre-
1. Dd is a textual description of the domain, speci-                                conditions ap are a set of predicates r̄ that must
   fying the types (the type system for entities e),                                hold true for this action to be executed. The
   predicates (in relation to the types), and actions                               effects ae are a set of new predicates r̄′ of which
   A including pre-conditions and effects (parame-                                  the new state takes the value after the execution
   terized by conjunctive logical formulas over the                                 of this action.
   the predicates).                                                                 The problem file PF is defined by three main
2. Dp is a textual description of the problem, spec-                             components: objects (E), the initial state (s0 ), and
   ifying the objects, initial states and goal states                            the goal state (ψgoal ):
   in terms of predicates;                                                       1. Objects: E = e1 , . . . , en is the set of named
3. DFG′ is the header of the ground-truth PDDL do-                                  entities present in the environment. Each object
   main file DFG that only provides the names and                                   is an instance of an entity type defined in DFG′ .
   parameters of the actions. This is required so                                2. Initial State: s0 ∈ S is a set of relational facts
   that the eventual plan is grounded to an existing                                of the form r(ē), where r ∈ R is a relational
   ontology and can be evaluated fairly.                                            predicate defined in D; ē is a tuple of entities
   The final objective is a plan L                 =                                from E that participate in relation r.
[a1 (ē1 ), . . . , am (ēm )], where each ai ∈ A is                             3. Goal State: ψgoal : S → B is a boolean formula
an action provided by DFG′ , and each ēi is a                                      over relational facts, where S is the state space
tuple of grounded entities corresponding to the                                     and B = {True, False}. When ψgoal (s∗ ) =
parameters of ai . The plan L, when executed in                                     True, state s∗ achieves the problem goal.
the environment expressed by a ground-truth DFG                                     Here, the state space S comprises all possible
and PFG , must (i) be executable, fulfilling the                                 configurations of relational facts over the object

                                                                             2
set E with the predicates R. Each state s ∈ S is                is too distant from the generation target while
a set of instantiated facts r(ē), describing which             PDDL itself is too low-resource. We draw inspira-
relations hold among the objects. Successfully ex-              tion from related work in program synthesis that
ecuting a plan L from the initial state s0 yields a             suggests high-resource languages (Cassano et al.,
sequence of intermediate states s1 , s2 , . . . , s∗ such       2024; Zhang et al., 2025) may be effect IRs for
that the goal formula ψgoal (s∗ ) evaluates to True.            generating low-resource languages like PDDL. We
   While an end-to-end LLM-as-planner pipeline                  also note from previous work that the rigid and par-
maps the input triplet I directly to a plan L, in this          ticular syntax of PDDL calls for a syntax alignment
work we focus on LLM-as-formalizer pipelines                    with an IR. Based on these criteria, we additionally
which instead generate the domain file DFP and                  propose two fully formal IRs:
PFP before inputting them into a PDDL solver to                 3. Python simulator, where the LLM is instructed
search for a plan.                                                 to generate a Python code that simulates the
                                                                   domain and the problem. We place minimal
3   Framework and Related Work                                     requirement on the structure of the code to
We propose a theoretical framework for LLM-                        leverage the coding ability of high-resource pro-
based classical planning revolving around levels of                gramming languages. We require the generated
intermediate representations (IR), where the num-                  Python code to be directly executable to return
bering of levels corresponds to the number of IRs                  a plan, though in this work treat it as an IR that
involved.                                                          we transpile to PDDL to take advantage of the
• Level 0: I → L                                                   optimized planners.
• Level 1: I → PDDL ; L                                         4. PyPDDL, where the LLM is instructed to gener-
• Level 2: I → IR → PDDL ; L                                       ate Python code in a specific wrapper for PDDL
• Level 3: I → IR → IR → PDDL ; L                                  referred to as PyPDDL2 . The documentation for
• Level 4: . . .                                                   PyPDDL is provided in the prompt along with
   Level 0 is essentially LLM-as-planner, mapping                  a domain-agnostic example. While the library
the input I to the plan L. While it is possible to                 does not provide a solver, implementing one is
involve IR in this level as a chain-of-thought, we do              feasible as the language is fully formal. Even
not discuss it as our focus is on LLM-as-formalizer                so, in this work we again transpile the PyPDDL
represented by the other levels, where PDDL is                     code to PDDL either deterministically with tools
always the final IR before the plan. We can thus                   from the library or with an LLM.
increase the level of complexity of a pipeline with                Examples of IRs are shown in Appendix C.
more IRs. To instantiate a pipeline with the formu-             Choice of Modules I → L: In general plan-
lation above, we will first discuss the choice of IRs           ning tasks, there exists much prior work of
before the choice of modules.                                   LLM-as-planner that generates plans in an end-to-
Choice of IR IRs used in past work include:                     end manner (Valmeekam et al., 2023a,b, 2025).
                                                                This line of work commonly involves LLM agents.
1. A natural language, where the LLM converts
                                                                Common techniques include reasoning before plan-
   the input description into a free-form representa-
                                                                ning (Yao et al., 2023), task decomposition (Prasad
   tion that facilitate later PDDL generation. This
                                                                et al., 2024), reflection after planning (Majumder
   representation can range from loose sentences
                                                                et al., 2024), continuous learning (Wang et al.,
   (Zhang et al., 2024; Hu et al., 2025) to a semi-
                                                                2024), and so on. As a complete survey exists (Wei
   formal data structure (Wong et al., 2024; Hao
                                                                et al., 2025), we do not dive into more discussions.
   et al., 2025), but in any case cannot be executed
   by an external solver. Such a conversion can in-                I → PDDL: In PDDL-based classical plan-
   volve information extraction, chain-of-thought,              ning, most existing work of LLM-as-formalizer
   or summarization.                                            generates various parts of the PDDL without in-
2. Another PDDL, where the module that takes                    volving additional IR. The generation target in-
   one PDDL as input and outputs another is a                   cludes the goal states (Xie et al., 2023), problem
   revision module discussed in details below.                  file (Liu et al., 2023; Zuo et al., 2025), action
                                                                semantics (Zhang et al., 2024; Zhu et al., 2025;
   We will show in later discussions that neither of
                                                                Hu et al., 2025), domain file (Guan et al., 2023;
these two IRs are sufficiently effective for open-
source, mid-size LLMs generating PDDL, as one                      2
                                                                       https://github.com/remykarem/Py2PDDL


                                                            3
Wong et al., 2024), and complete PDDL (Huang                  revise them without indication if their correctness.
and Zhang, 2025; Gong et al., 2025) like us. Fol-                IR → PDDL: Overall, higher-order chaining of
lowing cited work, we do not consider methods                 general purpose IRs (e.g., natural language, JSON)
that require supervised training due to the extreme           has proven effective for non-PDDL planning lan-
low-resource nature of PDDL. Common inference                 guage generation (Wong et al., 2024; Hao et al.,
techniques include basic few-shot prompting (e.g.,            2025). In our work, we specifically propose IRs
Xie et al. (2023)), where the LLM is prompted via             with high syntax alignment with PDDL. To tran-
in-context learning with some exemplars to trans-             spile an IR to PDDL, we rely on either (i) a de-
late the natural language Dd and/or Dp into PDDL              terministic rule-based transpiler or (ii) an LLM.
DF and/or PF. We do this by default with a                    We default to the latter following cited work and
prompt that introduces the basic structure of PDDL            discuss the former in a later ablation study.
with a domain-agnostic example. Other techniques
include sequential generation (e.g., Gong et al.              Non-PDDL Planning Languages Even in plan-
(2025)), where the LLM generates DF and/or PF                 ning, LLM-as-formalizer is a general methodology
sequentially instead of at once with distinctive              that can be instantiated with many planning lan-
prompts, or retrieval of documentation (e.g., Wang            guages other than PDDL, including satisfiability
and Zhang (2025)), where the LLM retrieves the                modulo theories (SMT) (Guo et al., 2024; Hao
documentation of the PDDL language along with                 et al., 2025), linear temporal logic (LTL) (Yang
examples before generation. We consider those                 et al., 2023; Li et al., 2024), Answer Set Program-
contemporaneous techniques out of scope.                      ming (Lin et al., 2024), action languages (AL)
                                                              (Ishay and Lee, 2025), and so on. While our work is
   We additionally apply decoding by grammar
                                                              largely applicable to any planning language (except
technique (denoted →GD ) to PDDL generation
                                                              for IRs requiring affinity to a particular language),
based on grammar (Wang et al., 2023) and con-
                                                              we only study PDDL which is widely used in lit-
strained decoding (Scholak et al., 2021) favorable
                                                              erature and also the language that underlies many
in the program synthesis community. We translate
                                                              classical planning benchmarks.
the formal BNF definition of PDDL 3.13 into a
LALR(1)-compatible EBNF grammar used to limit                 4   Experimental Setup
LLMs’ decoding to trivially syntactically correct
PDDL, but may degrade semantics.                              Datasets. We consider 4 simulated planning envi-
   PDDL ; L: All cited work above use a sym-                  ronments highly common in cited literature. First,
bolic PDDL solver such as Fast Downward planner               we have BlocksWorld, Logistics, and Sokoban
(Helmert, 2006), as do we. Another strand of work             from the International Planning Competition (IPC,
has used LLMs in lieu of such solvers to take PDDL            1998). These domains represent object manipula-
as input and outputs a plan (Stein et al., 2025), or to       tion and range from 4 actions to 12 actions. We use
generate programs that emulate such solvers (Silver           the moderately templated version of the datasets
et al., 2024; Chen et al., 2025).                             from Huang and Zhang (2025). Next, we have Co-
   PDDL →   − ∗ PDDL: This represents a revision              inCollector (Yuan et al., 2019), a partially observ-
module, where the LLM first generates an initial              able navigation domain, which convert to be fully
PDDL, before revising it multiple times (−    →∗ ). In        observable just as the other three. The dataset of
conjunction with the PDDL solver, the validity of             each environment comes with 100 tuples of domain
the predicted PDDL along with syntax error mes-               description, problem description, ground-truth do-
sages are typically provided to the LLM for re-               main and problem files. Examples are shown in
generation, denoted as →FB (Zhu et al., 2025; Hu              Appendix B.
et al., 2025). It is also possible to revise PDDL             Metrics. We use syntactic and semantic accuracy
solely based on LLMs’ own feedback without in-                to assess the generated PDDL. Syntactic accuracy
voking the solver.                                            is the percentage where no syntax error are re-
                                                              turned by the planning solver.Plan accuracy is the
   IR →− ∗ IR: A generated IR can also be revised
                                                              percentage where a plan is not only found by the
similarly. However, not all IRs can work with a
                                                              solver but also correct based on validation. We use
formal solver, so we rely on the LLM to optionally
                                                              the dual-bfws-ffparser planner (Muise, 2016)
   3
    Kovacs, 2011: http://pddl4j.imag.fr/repository/           to solve for the plan and VAL (Howey et al., 2004)
wiki/BNF-PDDL-3.1.pdf                                         to validate the plan against the ground-truth PDDL.

                                                          4
    Lv.   Input   1st IR      2nd IR           3rd IR         Output    Description
    0       I                                                   →L      LLM-as-planner (ϕ)
            I     → PDDL                                        ;L      PDDL-base: directly generating PDDL.
    1
                                                                        PDDL-grammar† the above plus constraining
            I     →GD PDDL                                      ;L
                                                                        LLM decoding with grammar.
                                                                        Generating an NL description of the actions
            I     → NL        → PDDL                            ;L
                                                                        and entity states before PDDL
                                                                        †
                                                                         Transpiling a PyPDDL program to PDDL ei-
            I     → PyPDDL    → | ; PDDL                        ;L
                                                                        ther with Py2PDDL (;) or by an LLM (→).
    2                                                                   †
                                                                         Generating a Python-based simulator before
            I     → PySim     → PDDL                            ;L
                                                                        translating to PDDL.
                                                                        Refining the generated PDDL once (with or
            I     → PDDL      →FB? PDDL                         ;L
                                                                        without the solver feedback).
                                                                        †
                                                                         Generating a PyPDDL wrapper before gener-
            I     → PyPDDL    → PDDL           → PDDL           ;L
                                                                        ating PDDL that receives one revision.
                                                                        †
                                                                         Revising the PyPDDL representation once be-
            I     → PyPDDL    → PyPDDL         → PDDL           ;L
                                                                        fore generating PDDL.
    3                                                                   †
                                                                         Marching through three IRs to emulate a
            I     → NL        → PyPDDL         → PDDL           ;L
                                                                        loose-to-formal transpilation process.
                                                                        Iteratively refining the PDDL program twice
            I     → PDDL      →FB? PDDL        →FB? PDDL        ;L
                                                                        (with or without solver feedback).

Table 1: Pipelines that we evaluate in this work, ranging from level 0 to level 3. For each pipeline, we specify the
IRs before reaching the final plan (L). Pipelines marked with † are newly introduced in this work. Straight arrows
(→) denote procedures involving LLMs, with superscripts indicating special variants—GD for grammar-guided
decoding and FB for solver feedback. Wavy arrows (;) represent purely symbolic solving or compilation processes.


Pipelines. We instantiate an array of pipelines              assisted planning focusing on PDDL generation.
based on our previously introduced framework. Re-
call that we define the level of a pipeline as the           5.1   The Best Pipeline
number of IRs (including PDDL) it involves. We
notate each pipeline as the intermediate IRs in-             Figure 2 shows the performance of 4 LLMs and
volves, excluding the input description I and the            12 pipelines on BlocksWorld and Logistics. The
output plan L. For example, PDDL → PDDL de-                  results of Sokoban and CoinCollector are shown in
notes a pipeline I → PDDL → PDDL ; L. The                    Appendix A. We focus on the first two due to space
evaluated pipelines are illustrated in Table 1, rang-        limitation and relatively consistent findings. Over-
ing from level 0 to level 3. We do not consider level        all, the highest plan accuracy is achieved by a Level
4 onward pipelines.                                          3 pipeline, involving 3 IRs, in 6 out of 8 LLM-
                                                             domain combinations. Among those, pipeline that
Models. We evaluate 4 recent and best performing
                                                             involves PyPDDL as an IR (PyPDDL → PyPDDL
open-source LLMs, QwQ-32B, Qwen3-32B, gpt-
                                                             or PDDL →FB PDDL) performs the best most
oss-120b (total 117B with 5.1B active parameters),
                                                             frequently, while that only involving revisions of
and GLM-4.5-Air-FP8 (total 106B with 12B active
                                                             PDDL (PyPDDL → PDDL →FB PDDL) comes as
parameters) We use vLLM (Kwon et al., 2023) to
                                                             a second. Generally, our finding recommends a
speed up inference and set temperature of 0.4 for
                                                             higher level pipeline that involves IRs and revi-
each of our experiments on one H100 GPU. We
                                                             sions, for the LLM-as-formalizer methodology.
report mean of three runs and their standard devia-
tion is shown as error bars. Examples of prompts                However, as real-life planning applications can-
are shown in Appendix D.                                     not assume unlimited computational resource.
                                                             Therefore, we now consider the most resource-
5       Results and Discussions                              constrained case of Level 0 and Level 1 pipelines
                                                             where the most costly step, an LLM genera-
With our unifying framework, we present a com-               tion, happens once. The comparison between
prehensive evaluation for inference-time LLM-                the vanilla LLM-as-planner (ϕ) and LLM-as-

                                                         5
                                                           BlocksWorld: Syntactic and Plan Accuracy by Model & Pipeline (grouped by Level)
                                                              Qwen/QwQ-32B                                                                                                 Qwen/Qwen3-32B
                           Level 0   Level 1                   Level 2                               Level 3                   1.2       Level 0   Level 1                   Level 2                               Level 3
                1.0
                                                                                                                               1.0

                0.8
                                                                                                                               0.8

                0.6                                                                                                            0.6

                0.4                                                                                                            0.4

                0.2                                                                                                            0.2

                0.0                     l           l       l     ) l   )     l            l   l      l    ) l                 0.0                       l         l       l     ) l   )     l            l   l      l    ) l
                        ner          pdd         pdd pdd ddl pdd ack pdd                pdd pdd pdd back pdd                           ner         pdd          pdd pdd ddl pdd ack pdd                pdd pdd pdd back pdd
                   plan
                 as-                         nl nsim h py2ppddl feedb pddl        ddl ddl ddl eed ddl                             plan
                                                                                                                                as-                         nl nsim h py2ppddl feedb pddl        ddl ddl ddl eed ddl
            llm-                           y th o (wit py (w/o
                                                  l                         l pyp l pyp ddl p (w/o f ddl p                 llm-                           y t ho (wit py (w/o
                                                                                                                                                                 l                         l pyp l pyp ddl p (w/o f ddl p
                                          p pdd               ddl          n pdd pyp ddl p                                                               p pdd               ddl          n pdd pyp ddl p
                                         ddl              l p               py
                                                                                       ddl
                                                                                           p
                                                                                                                                                        ddl              l p               py
                                                                                                                                                                                                      ddl
                                                                                                                                                                                                          p
                                      pyp             pdd                                                                                           pyp              pdd
 Accuracy




                                                                                   l p                                                                                                            l p
                                                                               pdd                                                                                                            pdd
                                                           openai/gpt-oss-120b                                                                                          zai-org/GLM-4.5-Air-FP8
                           Level 0   Level 1                   Level 2                               Level 3                             Level 0   Level 1                   Level 2                               Level 3
                1.0                                                                                                            1.0

                0.8                                                                                                            0.8

                0.6                                                                                                            0.6

                0.4                                                                                                            0.4

                0.2                                                                                                            0.2

                0.0                     l           l       l     ) l   )     l            l   l      l    )    l              0.0                       l   l       l     ) l   )     l            l   l      l    ) l
                        ner          pdd         pdd pdd ddl pdd ack pdd                pdd pdd pdd back pdd                           ner         pdd    pdd pdd ddl pdd ack pdd                pdd pdd pdd back pdd
                   plan
                 as-                         nl nsim h py2ppddl feedb pddl        ddl ddl ddl eed ddl                             plan
                                                                                                                                as-                   nl nsim h py2ppddl feedb pddl        ddl ddl ddl eed ddl
            llm-                           y th o (wit py (w/o
                                                  l                         l pyp l pyp ddl p (w/o f ddl p                 llm-                     y t ho (wit py (w/o
                                                                                                                                                           l                         l pyp l pyp ddl p (w/o f ddl p
                                          p pdd               ddl          n pdd pyp ddl p                                                         p pdd               ddl          n pdd pyp ddl p
                                         ddl              l p               py
                                                                                       ddl
                                                                                           p
                                                                                                                                                  ddl              l p               py
                                                                                                                                                                                                ddl
                                                                                                                                                                                                    p
                                      pyp             pdd                          l p                                                        pyp              pdd                          l p
                                                                               pdd                  Plan accuracy            Syntactic accuracy                                         pdd

                                                              Logistics: Syntactic and Plan Accuracy by Model & Pipeline (grouped by Level)
                                                              Qwen/QwQ-32B                                                                                                 Qwen/Qwen3-32B
                           Level 0   Level 1                   Level 2                               Level 3                             Level 0   Level 1                   Level 2                               Level 3
                1.0                                                                                                            1.0

                0.8                                                                                                            0.8

                0.6                                                                                                            0.6

                0.4                                                                                                            0.4

                0.2                                                                                                            0.2

                 0.0                    l           l        l             l      l                                             0.0
                          ann
                              er     pdd
                                                                     )
                                                 pdd pdd ddl pdd ack pdd
                                                                             )               ddl ddl ddl ck) ddl                        ann
                                                                                                                                           er      pdd
                                                                                                                                                         l         l        l       )
                                                                                                                                                               pdd pdd ddl pdd ack pdd
                                                                                                                                                                                          l )    l          ddl ddl ddl ck) ddl
                     s-pl                    nl nsim h py2ppddl feedb pddl               l p l p l p dba l p                       s-pl                     nl nsim h py2ppddl feedb pddl               l p l p l p dba l p
               m - a                          h o      i t     p y     / o        p y pdd pypdd l pdd /o fee l pdd            m - a                          ho       i t     p y     / o        p y pdd pypdd l pdd /o fee l pdd
            ll                            pyt pddl (w           ddl
                                                                    (w         nl pddl pypdd ddl (w pdd                    ll                            pyt pddl (w           ddl
                                                                                                                                                                                   (w         nl pddl pypdd ddl (w pdd
                                         ddl               l p                  py
                                                                                           ddl
                                                                                               p
                                                                                                                                                        ddl               l p                  py
                                                                                                                                                                                                          ddl
                                                                                                                                                                                                              p
                                      pyp             pdd                                                                                           pyp              pdd
 Accuracy




                                                                                       l p                                                                                                            l p
                                                                                   pdd                                                                                                            pdd
                                                           openai/gpt-oss-120b                                                                                          zai-org/GLM-4.5-Air-FP8
                           Level 0   Level 1                   Level 2                               Level 3                             Level 0   Level 1                   Level 2                               Level 3
                1.0                                                                                                            1.0


                0.8                                                                                                            0.8


                0.6                                                                                                            0.6


                0.4                                                                                                            0.4


                0.2                                                                                                            0.2

                0.0                     l           l        l       )     l )    l             l    l      l   )  l           0.0                       l         l        l       )     l )    l             l    l      l   )  l
                           er        pdd        pdd pdd ddl pdd ack pdd                      pdd pdd pdd back pdd                        er        pdd         pdd pdd ddl pdd ack pdd                      pdd pdd pdd back pdd
                       ann                   nl nsim h py2ppddl feedb pddl                                                            ann                   nl nsim h py2ppddl feedb pddl
                 as-pl                                                                p ddl ypddl pddl o feed pddl              as-p
                                                                                                                                     l
                                                                                                                                                                                                     p ddl ypddl pddl o feed pddl
            llm-                               o
                                          pythpddl (w
                                                       i t     p y
                                                                    (w / o        p y     p       l
                                                                               nl pddl pypdd ddl (w pdd
                                                                                                       /      l            llm-                               o
                                                                                                                                                         pythpddl (w
                                                                                                                                                                      i t     p y
                                                                                                                                                                                   (w / o        p y     p       l
                                                                                                                                                                                              nl pddl pypdd ddl (w pdd
                                                                                                                                                                                                                      /      l
                                                                ddl                                                                                                            ddl
                                         ddl               l p                  py
                                                                                            ddl
                                                                                                p
                                                                                                                                                        ddl               l p                  py
                                                                                                                                                                                                           ddl
                                                                                                                                                                                                               p
                                      pyp             pdd                               l p                                                         pyp              pdd                               l p
                                                                                   pdd               Plan accuracy           Syntactic accuracy                                                   pdd


Figure 2: Syntactic accuracy and plan accuracy of various methods grouped by levels and LLMs on BlocksWorld
and Logistics. Error bars shows the standard deviation over 3 runs.



                                                                                                                       6
                                              Domain Description                                                Problem Description                                                                       PDDL                                                            P
scription                                                                                                                                                                        (define (domain blocksworld)
                                    I am playing with a set of blocks… Here are the                       As initial conditions I have that, block 2 is
                                                                                                                                                                                  (:action putdown                                                       (define (domain blo
                                    actions I can do: Pick up a block, Unstack a block                    clear, block 9 is clear, … the hand is empty,                                             Missing predicate
                                                                                                                                                                                    :parameters (?ob) arm-empty                                            (:requirements :s
                                    from on top of another block…                                         block 1 is on top of block 5, block 2 is on top                           :precondition ((holding ?ob) …)                                      (:predicates (clear
                                    I have the following restrictions on my actions: 1)                                                                                                                                                                             (on-table ?
                                                                                                          of block 1, block 10 is on top of block 4,                                :effect (and (clear ?ob)                                             …
                                    I can only pick up/ unstack one block at a time. 2)
                                                                                                          block 11 is on top of block 14, block 12 is on                              (on-table ?ob)                                                     (:action pickup …
                                    I can only pick up a block if the block is on the
                                                                                                          top of block 13, block 3 is on the table, block                             (not (holding ?ob))) …)                                            (:action putdown
                                    table and the block is clear. Once I pick up, I am                                                                                                                                                                     :parameters (?ob
                                    holding the block.                                                    4 is on the table, block 5 is on the table,                                                                                                      :precondition (hol
                                                                                                                                                                                 (define (problem …)                                                       :effect (and (clear
                                    I can only put down a block that I am holding.                        block 7 is on the table, block 5 is on the
                                                                                                                                                                                  (:domain blocks)                                                                   (not (hold
                                    ;; Action Heads                                                       table, block 7 is on the table, …                                       (:objects 1 2 3 4 5 6 7 8 9 10 11                                      …
                                                                                                                                                                                                                                                         (define (problem b
                                    pickup (?b          - block)                                          My goal is to have that block 1 is on top of                           12 13 14 - block)                                                           (:domain blocks
                                    unstack (?b ?under - block) …                                                                                                                                        Solver:
                                                                                                          block 9, block 2 is on top of block 5, …,                               (:init … ) …)                                                              (:objects
                                                                                                                                                                                                       Syntax error                                              1234567
ve that, block 2 is clear,                                                                                                                                                                                                                                   (:init …) …
 and is empty, block 1 is on
  on top of block 1, block 10
 k 11 is on top of block 14,
 ck 13, block 3 is on the                            Plan           Executed                    NL-PDDL                                                PyPDDL                                           PDDL (Revised)
able, block 5 is on the table,
block 5 is on the table, block
                                  (unstack block2 block1)                           BlockStackingDomain                          class BlocksWorldDomain(Domain):                              (define                                             (define (domain b
                                                                                                                                  Block = create_type("block")                                  (domain blocksworld)
                                  (putdown block2)                                  Entity Types:
                                                                                                                                                   Missing predicate                                                                                 (:predicate
                                                                                                                                  @action(Block)                                                (:action putdown
block 1 is on top of block 9,     (stack block1 block9)                             - block: Physical objects…
                                                                                                                                  def pickup(self, b):~clear(b)                                                                                        (on ?x ?y) (o
                                                                                    - hand: A single robotic hand…                 precond = [self.handempty(),...]
                                                                                                                                                                                                 :parameters    (?ob)                                  (clear ?x) (h
k 5, …, block 3 is on the         (pickup block2)                                                                                                                                                      Mistake not  corrected
able, block 5 is on the table,                                                      Predicates: clear: True when…                  effect = [~self.handempty(),                                  :precondition     (
                                                                                                                                                                                                           after revision                            (:action pick-u
                                  (stack block2 block5)                                                                                                                                             (holding ?ob) …)
and block 7 is on the table …                                                       Actions:                                        ~self.ontable(b), self.holding(b)]                                                                                 :parameters (
                                  (unstack block11 block14)                         - pickup: parameters: ?b - block               return precond, effect                                        :effect (and (clear ?ob)                              :precondition
                                                Failure:
                                  (stack block11  block1)
                                             block5 not clear
                                                                                     - Preconditions:                                                                                               (on-table ?ob)                                       (ontable ?x
                                                                                                                                 class BlocksWorldProblem(...):
                                  (unstack block12 block13)                            - Positive: on-table(?b),                                                                                    (not (holding ?ob))))                              :effect (and
                                                                                                                                  def __init__(self): …
                                  (stack block12 block2)                                  empty-hand()                             self.blocks=Block.create_objs(                               … )                                                      (not (ontab
                                  (pickup block14)
                                                                                       - Negative: holding(?b)                      [1,2,3,4,5,...,12,13,14], ...)                                          Successfully                             (:action put-do
                                                                                     - Effects: Missing predicate                 @init                                                        (define (problem  …) issue                            (:action unstac
                                  (stack block14 block12)                                              clear                      def init(self):
                                                                                                                                                  Cannot find obj;                                         fixed the
                                                                                       - Add: holding(?b)
                                                                                                                                                (should be b[“b2”])                             (:domain blocks)                                     (:action stack
                                  (pickup block9)                                                                                  b = self.blocks
                                                                                                                                   return [self.clear(b[2]),
                                                                                                                                                                                                (:objects b1 b2 b3 b4 …
                                  (stack block9 block14)                            BlockStackingProblem                                                                                       b12 b13 b14 - block)
                                                                                                                                    self.clear(b[4]),
                                  …                                                 Objects: block: b1, b2, b3, …                   self.clear(b[6]), …]                                        (:init … ) …)



                                 Figure 3: Qualitative examples of a same problem in BlocksWorld, juxtaposing different IRs generated including
                                 NL, PyPDDL, PDDL, before generating the final PDDL (Level 2). Also included is a revised PDDL based on solver
                                 feedback  and a directly generated
                                        Plan               NL-PDDL  plan (Level 0).   PyPDDL                      Revised PDDL
                                       (unstack block2 block1)           BlockStackingDomain                        class BlocksWorldDomain(Domain):                                (define (domain blocksworld)
                                     (putdown block2)      Executed   Entity Types:
                                 formalizer           (PDDL-base)
                                     (stack block1 block9)                           hasobjects
                                                                      - block: Physical       no… clear winner                  (3            5.2 The Best IR (:predicates
                                                                                                                     Block = create_type("block")                                       (:requirements :strips)
                                                                                                                                                                                                      (clear ?x)
                                     (pickup block2)                  - hand: A single robotic hand ..                                                                                           (on-table ?x)
                                 against       5
                                     (stack block2  in
                                                   block5)8    LLM-domain
                                                                      Predicates:            combinations),                 cor-
                                                                                                                     @predicate(Block, Block)
                                                                                                                                                                                      …
                                     (unstack block11
                                                        Failed.       - clear(?b - block): True when
                                                                                                                     def on(self, b1, b2):
                                                                                                                                              Having demonstrated
                                                                                                                        """block b1 is on block b2"""                                 (:action the
                                                                                                                                                                                                 pickupeffectiveness
                                                                                                                                                                                                         …                            of IR in
                                 roborating
                                     block14)
                                                     similar
                                                      Block5 not    claims
                                                                      block ?b hasin      recent
                                                                                     no blocks  on top ofwork
                                                                                                         it     that … eval-                                                          (:action putdown
                                     (stack block11 block1)
                                     (unstack block12
                                                         clear        and is not being held.                         @action(Block)           planning               language        generation
                                                                                                                                                                                        :parameters (?ob) and justified our IR-
                                 uated      reasoning LLMs
                                     block13)
                                                                      …
                                                                                 with inference-time                      scal- b):
                                                                                                                     def pickup(self,                                                   :precondition (holding ?ob)
                                     (stack block12 block2)
                                                                      Actions:
                                                                      Action: pickup
                                                                                                                                              based
                                                                                                                        precond = [self.handempty(),           framework,
                                                                                                                                                         self.clear(b),               we:effect zoom            onto
                                                                                                                                                                                                 (and (clear ?ob)  (on-tableLevel
                                                                                                                                                                                                                            ?ob)          2 with
                                 ing(pickup
                                        (Huang
                                             block14)     and Zhang,  Parameters: 2025;
                                                                                     ?b - block     Amonkarself.ontable(b)]
                                                                                                                       et     al.,                                                                 (not (holding ?ob))))
                                     (stack block14 block12)          Preconditions:                              self.holding(b)]
                                                                                                                                              one additional IR before
                                                                                                                        effect = [~self.handempty(), ~self.ontable(b),                (:action unstack
                                                                                                                                                                                      …
                                                                                                                                                                                                        the final            PDDL to be
                                                                                                                                                                                                                    Mistake not corrected
                                 2025).
                                     (pickup Applicable
                                             block9)               for-empty-hand()
                                                                          all levels,
                                                                        Positive:  on-table(?b),we evaluate PDDL-       return precond, effect
                                     (stack block9 block14)
                                                                                                                     …                        generated.                  Our
                                                                                                                                                        ~self.clear(?b) omitted   pipelines            are      instantiated              with 4
                                 grammar           with constrained
                                     (unstack block6 block8)
                                                                                        decoding
                                                                                           clear(?b) omitted as a drop-in
                                                                      - Negative: holding(?b)                                                                                         (define (problem blocks-problem)
                                     (putdown block6)
                                     (unstack block8 block10)
                                                                      Effects:
                                                                      - Add: holding(?b)
                                                                                                                                              types of IR: NL, Python
                                                                                                                  class BlocksWorldProblem(BlocksWorldDomain):                          (:domain   Simulator,
                                                                                                                                                                                                    blocks)                PyPDDL, and
                                                                                                                                                                                                                      Syntax corrected
                                 replacement             for standard
                                     (stack block8 block6)                          decoding in PDDL-base            def __init__(self):
                                                                                                                        super().__init__() PDDL. Compared tob1Level
                                                                                                                                                                                        (:objects
                                     (unstack block10 block4)         BlockStackingProblem                                                                                                                  1,    NL        as an IR con-
                                                                                                                                                                                               b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12
                                                                                                                                                                                      b13 b14 - block)
                                 pipeline.
                                     (stack block10Although
                                                    block3)             performance on BlockWorld
                                                                      Objects:
                                                                                                                        self.blocks=
                                                                                                                                                                                        (:init
                                     (pickup block13)                 - block: b1, b2, b3, …                                                  sistently
                                                                                                                  BlocksWorldDomain.Block.create_objs(
                                                                                                                                                                    hurts
                                                                                                                           [1,2,3,4,5,6,7,8,9,10,11,12,13,14], prefix="b")
                                                                                                                                                                                 performance.
                                                                                                                                                                                          (clear b2) (clear b9) (clear b6) …)Simulator is
                                                                                                                                                                                                              Python
                                 domain        is comparable
                                     (stack block13 block7)
                                                                           (38%
                                                                      Initial State:    for PDDL-grammar             @init      vs                                                      (:goal (and
                                                                      - on(b1, b5), on(b2, b1), on(b6,               def init(self):          similar            yet sometimes(on improves      b1 b9) (on b2 b5) (onperformance.
                                                                                                                                                                                                                       b7 b14) (ontable       In
                                 36% for PDDL-base),                          the performance on Logis-
                                                                      b8), on(b8, b10), on(b10, b4),                    b = self.blocks
                                                                                                                                                      Should be b[“b4”]               b5) (ontable b3) …
                                                                      Goal Conditions:
                                                                      …
                                                                                                                        return [              contrast,             PyPDDL           and))      PDDL            as    IRs      consistently
                                 tics domain is zero. Constrained                                 decoding …,showed        self.clear(b[2]), self.clear(b[4]), self.clear(b[6]),      )
                                                                                                                                              improves performance. Notably, PyPDDL →
                                 an hit or miss behaviour; either performing com-
                                                                                                                                              PDDL and PDDL →FB PDDL out-performs each
                                 parable to standard decoding or catastrophically
                                                                                                                                              other in half of the 8 LLM-domain combinations.
                                 making similar mistakes in all the problems. We
                                                                                                                                              Without the solver feedback but with the LLM feed-
                                 defer comprehensive evaluation of constrained de-
                                                                                                                                              back, the PDDL → PDDL pipeline loses its advan-
                                 coding to future work while suggesting for robust
                                                                                                                                              tage of revision. Whenever invoking the solver
                                 decoding techniques. With one more IR, the best
                                                                                                                                              may be costly, this finding presents the commu-
                                 Level 2 LLM-as-formalizer pipeline always out-
                                                                                                                                              nity an alternative to revision with solver feedback:
                                 performs LLM-as-planner and also the Level 1
                                                                                                                                              transpilation from a syntax-aligned IR to the target
                                 pipelines in all 8 out of 8 cases. This finding cau-
                                                                                                                                              language. Figure 3 shows qualitative examples of
                                 tions against generating planning languages with
                                                                                                                                              different IRs and their typical mistakes.
                                 merely one LLM call.
                                                                                                                                                    For any pipeline that involves PyPDDL →
                                                                                                                                              PDDL, recall that PyPDDL is a formal language
                                                                                                                                              where a solver could be defined in situ (though, this

                                                                                                                                      7
Figure 4: The performance of two LLMs and four methods including usage as planners and as formalizers on
BlocksWorld problems with an increasing entity space.


is a non-trivial effort) yet is not provided by the        pipelines including PDDL (Level 1), PyPDDL →
library we use, so we default to using the LLM             PDDL, and PDDL → PDDL (Level 2).
to transpile PyPDDL to PDDL to leverage the                   Figure 4, clearly shows that while all methods
PDDL solver. As an ablation study, we also attempt         degrade with complexity, LLM-as-formalizer is
to perform transpilation deterministically using           much more robust than LLM-as-planner. We
Py2PDDL library (denoted as PyPDDL ; PDDL).                observe that, as the number of blocks approaches
One may expect such a deterministic transpilation          20, the performance of LLM-as-planner halves
to outperform LLM generating PDDL, consider-               compared to 10; approaching 50, its performance
ing Python is much higher-resource than PDDL.              drops to zero. In contrast, all LLM-as-formalizer
Transpilation with Py2PDDL performs much worse             pipelines are more robust to increased entity-space
than LLM-based transpilation. For instance, with           complexity despite reduction in performance. No-
accuracy 16% vs 68% for QwQ-32B model in                   tably, directly generating PDDL (Level 1) loses no
BlocksWorld. The generated PyPDDL tends to                 more than 20% plan accuracy as the number of
not follow non-trivial way of representing different       entities increases from 10 to 50. In comparison, the
PDDL components. As shown in Figure 3, a set               Level 2 pipelines perform better with less entities,
of blocks created by create_objs is mistakenly             but degrade more severely with more entities.
treated as a List instead of a Dict.                          Situated among recent studies, our findings cor-
                                                           roborate the claim that even reasoning LLMs with
5.3   Robustness against Complexity                        inference-time scaling are not robust to problem
                                                           complexity. Moreover, we are the first to evi-
Recent work has cast doubt on the ability of LLM,
                                                           dence and advocate for the robustness of LLM-
both as a planner and as a formalizer, to scale
                                                           as-formalizer in planning. For more multi-IR
with the problem complexity (Shojaee et al., 2025;
                                                           pipelines of higher levels, we also caution against
Lin et al., 2025; Amonkar et al., 2025). For ex-
                                                           the tradeoff between performance and robustness
ample, the BlocksWorld dataset evaluated in this
                                                           against complexity.
work ranges from 2 to 15 blocks, while other cited
previous work often relied on datasets with even           6   Conclusion
smaller entity space. In real-life applications such
as robotics or logistics, current benchmarks do            We propose a unifying framework of inference-
not help understand LLMs’ robustness in plan-              time planning language generation. Based on
ning for complex problems, either as planners or as        the interplay of IR, our framework not only sub-
formalizers. Therefore, we specifically construct          sumes most prior work involving multi-stage LLM
BlocksWorld problems with increasing number of             pipelines but also inspires novel pipelines, such
entities (blocks), ranging from 10 to 50, with an          as those involving a high-resource, syntactically
increment of 10 and 10 problems per bucket. We             similar IR to the target language. In addition to
evaluate the robustness of some of the most com-           providing immediately applicable recipes for high-
monly used and best-performing pipelines LLM-              performing planning methods, our work opens up
as-planner (Level 0) and three LLM-as-formalizer           promising directions of research in designing ef-

                                                       8
ficient LLM pipelines that outreaches to alterna-              Weihang Guo, Zachary Kingston, and Lydia E. Kavraki.
tive planning languages (e.g., LTL) and even non-                2024. Castl: Constraints as specifications through
                                                                 llm translation for long-horizon task and motion plan-
planning domain-specific languages (e.g., SMT).
                                                                 ning. Preprint, arXiv:2410.22225.
7   Limitations                                                Yilun Hao, Yang Zhang, and Chuchu Fan. 2025. Plan-
                                                                 ning anything with rigor: General-purpose zero-shot
We work with moderately templated descriptions                   planning with llm-based formalized programming.
for domain and problem as input. This is easier                  Preprint, arXiv:2410.12112.
than more natural version of the data. While we
                                                               Malte Helmert. 2006. The fast downward planning
observe increased performance with some of the                  system. J. Artif. Int. Res., 26(1):191–246.
techniques implemented, it is not clear whether we
same performance gains with natural data which is              R. Howey, D. Long, and M. Fox. 2004. Val: auto-
                                                                 matic plan validation, continuous effects and mixed
more applicable to the real world.                               initiative planning using pddl. In 16th IEEE Inter-
   We only consider pipelines with three levels i.e.             national Conference on Tools with Artificial Intelli-
three IRs for planning language generation. Some                 gence, pages 294–301.
of the existing work already have more than three
                                                               Mengkang Hu, Tianxing Chen, Yude Zou, Yuheng Lei,
IRs in their pipelines (Hao et al., 2025; Ishay and             Qiguang Chen, Ming Li, Yao Mu, Hongyuan Zhang,
Lee, 2025). Thus, instantiation of our framework                Wenqi Shao, and Ping Luo. 2025. Text2World:
presented here is still limited in all possible insights        Benchmarking large language models for symbolic
applicable to contemporary work. We defer this to               world model generation. In Findings of the Asso-
                                                                ciation for Computational Linguistics: ACL 2025,
future work.                                                    pages 26043–26066, Vienna, Austria. Association
                                                                for Computational Linguistics.

References                                                     Cassie Huang and Li Zhang. 2025. On the limit of
                                                                 language models as planning formalizers. In Pro-
Rikhil Amonkar, May Lai, Ronan Le Bras, and                      ceedings of the 63rd Annual Meeting of the Associa-
  Li Zhang. 2025. Are llms better formalizers                    tion for Computational Linguistics (Volume 1: Long
  than solvers on complex problems?  Preprint,                   Papers), pages 4880–4904, Vienna, Austria. Associa-
  arXiv:2505.13252.                                              tion for Computational Linguistics.
Federico Cassano, John Gouwar, Francesca Lucchetti,            IPC. 1998. International planning competition. https:
  Claire Schlesinger, Anders Freeman, Carolyn Jane               //www.icaps-conference.org/competitions.
  Anderson, Molly Q Feldman, Michael Greenberg,
  Abhinav Jangda, and Arjun Guha. 2024. Knowl-                 Adam Ishay and Joohyung Lee. 2025. Llm+al: Bridg-
  edge transfer from high-resource to low-resource               ing large language models and action languages
  programming languages for code llms. Preprint,                 for complex reasoning about actions. Preprint,
  arXiv:2308.09895.                                              arXiv:2501.00830.
Yongchao Chen, Yilun Hao, Yang Zhang, and Chuchu               Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  Fan. 2025. Code-as-symbolic-planner: Foundation               Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
  model-based robot planning via symbolic code gen-             Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
  eration. Preprint, arXiv:2503.01700.                          cient memory management for large language model
                                                                serving with pagedattention. In Proceedings of the
Richard E. Fikes and Nils J. Nilsson. 1971. Strips: a           ACM SIGOPS 29th Symposium on Operating Systems
  new approach to the application of theorem proving            Principles.
  to problem solving. In Proceedings of the 2nd Inter-
  national Joint Conference on Artificial Intelligence,        Manling Li, Shiyu Zhao, Qineng Wang, Kangrui Wang,
  IJCAI’71, page 608–620, San Francisco, CA, USA.               Yu Zhou, Sanjana Srivastava, Cem Gokmen, Tony
  Morgan Kaufmann Publishers Inc.                               Lee, Li Erran Li, Ruohan Zhang, et al. 2024. Embod-
                                                                ied agent interface: Benchmarking llms for embodied
Liancheng Gong, Wang Zhu, Jesse Thomason, and                   decision making. arXiv preprint arXiv:2410.07166.
  Li Zhang. 2025. Zero-shot iterative formalization
  and planning in partially observable environments.           Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson,
  Preprint, arXiv:2505.13126.                                    Ashish Sabharwal, Radha Poovendran, Peter Clark,
                                                                 and Yejin Choi. 2025. Zebralogic: On the scaling lim-
Lin Guan, Karthik Valmeekam, Sarath Sreedharan,                  its of LLMs for logical reasoning. In Forty-second
  and Subbarao Kambhampati. 2023. Leveraging pre-                International Conference on Machine Learning.
  trained large language models to construct and uti-
  lize world models for model-based task planning.             Xinrui Lin, Yangfan Wu, Huanyu Yang, Yu Zhang,
  In Thirty-seventh Conference on Neural Information             Yanyong Zhang, and Jianmin Ji. 2024. Clmasp:
  Processing Systems.                                            Coupling large language models with answer set


                                                           9
  programming for robotic task planning. Preprint,                leveraging large language models to construct auto-
  arXiv:2406.03367.                                               mated planning models. In Findings of the Asso-
                                                                  ciation for Computational Linguistics: ACL 2025,
Bo Liu, Yuqian Jiang, Xiaohan Zhang, Qiang Liu,                   pages 25167–25188, Vienna, Austria. Association
  Shiqi Zhang, Joydeep Biswas, and Peter Stone.                   for Computational Linguistics.
  2023. Llm+ p: Empowering large language mod-
  els with optimal planning proficiency. arXiv preprint         Karthik Valmeekam, Matthew Marquez, Alberto Olmo,
  arXiv:2304.11477.                                               Sarath Sreedharan, and Subbarao Kambhampati.
                                                                  2023a. Planbench: An extensible benchmark for
Bodhisattwa Prasad Majumder, Bhavana Dalvi Mishra,                evaluating large language models on planning and
  Peter Jansen, Oyvind Tafjord, Niket Tandon,                     reasoning about change. Advances in Neural Infor-
  Li Zhang, Chris Callison-Burch, and Peter Clark.                mation Processing Systems, 36:38975–38987.
  2024. CLIN: A continually learning language agent
  for rapid task adaptation and generalization. In First        Karthik Valmeekam, Matthew Marquez, Sarath Sreed-
  Conference on Language Modeling.                                haran, and Subbarao Kambhampati. 2023b. On the
                                                                  planning abilities of large language models: a critical
Christian Muise. 2016. Planning.Domains. In The                   investigation. In Proceedings of the 37th Interna-
  26th International Conference on Automated Plan-                tional Conference on Neural Information Processing
  ning and Scheduling - Demonstrations.                           Systems, NIPS ’23, Red Hook, NY, USA. Curran
                                                                  Associates Inc.
Archiki Prasad, Alexander Koller, Mareike Hartmann,
  Peter Clark, Ashish Sabharwal, Mohit Bansal, and              Karthik Valmeekam, Kaya Stechly, Atharva Gundawar,
  Tushar Khot. 2024. ADaPT: As-needed decompo-                    and Subbarao Kambhampati. 2025. A systematic
  sition and planning with language models. In Find-              evaluation of the planning and scheduling abilities of
  ings of the Association for Computational Linguis-              the reasoning model o1. Transactions on Machine
  tics: NAACL 2024, pages 4226–4252, Mexico City,                 Learning Research.
  Mexico. Association for Computational Linguistics.
                                                                Bailin Wang, Zi Wang, Xuezhi Wang, Yuan Cao, Rif A.
Torsten Scholak, Nathan Schucher, and Dzmitry Bah-                Saurous, and Yoon Kim. 2023. Grammar prompting
  danau. 2021. PICARD: Parsing incrementally for                  for domain-specific language generation with large
  constrained auto-regressive decoding from language              language models. In Proceedings of the 37th Interna-
  models. In Proceedings of the 2021 Conference on                tional Conference on Neural Information Processing
  Empirical Methods in Natural Language Processing,               Systems, NIPS ’23, Red Hook, NY, USA. Curran
  pages 9895–9901, Online and Punta Cana, Domini-                 Associates Inc.
  can Republic. Association for Computational Lin-
  guistics.                                                     Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Man-
                                                                  dlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh,                  Anima Anandkumar. 2024. Voyager: An open-ended
  Maxwell Horton, Samy Bengio, and Mehrdad Fara-                  embodied agent with large language models. Trans-
  jtabar. 2025. The illusion of thinking: Understand-             actions on Machine Learning Research.
  ing the strengths and limitations of reasoning mod-
  els via the lens of problem complexity. Preprint,             Renxiang Wang and Li Zhang. 2025. Documenta-
  arXiv:2506.06941.                                               tion retrieval improves planning language generation.
                                                                  Preprint, arXiv:2509.19931.
Tom Silver, Soham Dan, Kavitha Srinivas, Joshua B.
  Tenenbaum, Leslie Kaelbling, and Michael Katz.                Hui Wei, Zihao Zhang, Shenghua He, Tian Xia, Shijia
  2024. Generalized planning in pddl domains with                 Pan, and Fei Liu. 2025. PlanGenLLMs: A modern
  pretrained large language models. In Proceedings                survey of LLM planning capabilities. In Proceedings
  of the Thirty-Eighth AAAI Conference on Artificial              of the 63rd Annual Meeting of the Association for
  Intelligence and Thirty-Sixth Conference on Inno-               Computational Linguistics (Volume 1: Long Papers),
  vative Applications of Artificial Intelligence and              pages 19497–19521, Vienna, Austria. Association
  Fourteenth Symposium on Educational Advances in                 for Computational Linguistics.
  Artificial Intelligence, AAAI’24/IAAI’24/EAAI’24.
  AAAI Press.                                                   Lionel Wong, Jiayuan Mao, Pratyusha Sharma,
                                                                  Zachary S. Siegel, Jiahai Feng, Noa Korneev,
Katharina Stein, Daniel Fišer, Jörg Hoffmann, and                 Joshua B. Tenenbaum, and Jacob Andreas. 2024.
  Alexander Koller. 2025. Automating the generation               Learning adaptive planning representations with nat-
  of prompts for llm-based action choice in pddl plan-            ural language guidance. In International Conference
  ning. In Proceedings of the Workshop on Bridging                on Learning Representations (ICLR).
  the Gap Between AI Planning and Reinforcement
  Learning (PRL) at ICAPS.                                      Yaqi Xie, Chen Yu, Tongyao Zhu, Jinbin Bai, Ze Gong,
                                                                  and Harold Soh. 2023. Translating natural lan-
Marcus Tantakoun, Christian Muise, and Xiaodan Zhu.               guage to planning goals with large-language models.
 2025. LLMs as planning formalizers: A survey for                 Preprint, arXiv:2302.05128.


                                                           10
Ziyi Yang, Shreyas S. Raman, Ankit Shah, and Stefanie          main file (df; Listing 8), problem file (pf; Listing 9),
  Tellex. 2023. Plug in the safety chip: Enforcing             and plan (plan; Listing 10).
  constraints for llm-driven robot agents. Preprint,
  arXiv:2309.09919.                                            B.2    Logistics
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak               Logistics. Find the domain description (dd; List-
  Shafran, Karthik Narasimhan, and Yuan Cao. 2023.
  React: Synergizing reasoning and acting in language          ing 11), problem description (pd; Listing 12), do-
  models. Preprint, arXiv:2210.03629.                          main file (df; Listings 13 and 14), problem file (pf;
                                                               Listing 15), and plan (plan; Listing 16).
Xingdi Yuan, Marc-Alexandre Côté, Alessandro Sor-
  doni, Romain Laroche, Remi Tachet des Combes,                B.3    CoinCollector
  Matthew Hausknecht, and Adam Trischler. 2019.
  Counting to explore and generalize in text-based             CoinCollector. Find the domain description (dd;
  games. Preprint, arXiv:1806.11525.                           Listing 17), problem description (pd; Listing 18),
Jipeng Zhang, Jianshu Zhang, Yuanzhe Li, Renjie Pi,            domain file (df; Listing 19), problem file (pf; List-
   Rui Pan, Runtao Liu, Zheng Ziqiang, and Tong                ing 20), and plan (plan; Listing 21).
   Zhang. 2025. Bridge-coder: Transferring model ca-
   pabilities from high-resource to low-resource pro-          B.4    Sokoban
   gramming language. In Findings of the Association
   for Computational Linguistics: ACL 2025, pages              Sokoban. Find the domain description (dd; List-
   10865–10882, Vienna, Austria. Association for Com-          ing 22), problem description (pd; Listing 23), do-
   putational Linguistics.                                     main file (df; Listings 24 and 25), problem file (pf;
Tianyi Zhang, Li Zhang, Zhaoyi Hou, Ziyu Wang, Yul-            Listing 26), and plan (plan; Listing 27).
   ing Gu, Peter Clark, Chris Callison-Burch, and Niket
  Tandon. 2024. PROC2PDDL: Open-domain plan-                   C     Examples of IRs
   ning representations from texts. In Proceedings of
   the 2nd Workshop on Natural Language Reasoning              C.1    NL→PDDL (nl_pddl)
   and Structured Explanations (@ACL 2024), pages
  13–24, Bangkok, Thailand. Association for Compu-             Listing 28 and Listing 29 present NL-PDDL IR
   tational Linguistics.                                       Example.
Wang Bill Zhu, Ishika Singh, Robin Jia, and Jesse              C.2    PythonSim→PDDL (pythonsim_pddl)
 Thomason. 2025. Language models can infer action
 semantics for symbolic planners from environment              Listings 30–32 and Listing 33 present the Python-
 feedback. In Proceedings of the 2025 Conference               Sim IR example.
 of the Nations of the Americas Chapter of the Asso-
 ciation for Computational Linguistics: Human Lan-             C.3    PyPDDL→PDDL (pypddl_pddl)
 guage Technologies (Volume 1: Long Papers), pages
 8751–8773, Albuquerque, New Mexico. Association               Listings 34–35 and Listing 36 present PyPDDL IR
 for Computational Linguistics.                                example.
Max Zuo, Francisco Piedrahita Velez, Xiaochen Li,
 Michael Littman, and Stephen Bach. 2025. Plan-                C.4    PDDL→PDDL (pddl_pddl)
 etarium: A rigorous benchmark for translating text            Listing 37 and Listing 38 present PDDL IR exam-
 to structured planning languages. In Proceedings
 of the 2025 Conference of the Nations of the Amer-            ple.
 icas Chapter of the Association for Computational
 Linguistics: Human Language Technologies (Volume              D     Examples of Prompts
 1: Long Papers), pages 11223–11240, Albuquerque,
 New Mexico. Association for Computational Linguis-            D.1    Base Prompts
 tics.

A     Additional Results                                       D.2    Plan Generation (plan_gen)
                                                               Uses plan_instruction together with the natural-
The experimental results for Sokoban and CoinCol-
                                                               language domain and problem descriptions for di-
lector are shown in Table 5.
                                                               rect plan synthesis.
B     Examples of Input and Output
                                                               D.3    Single-Stage PDDL (pddl)
B.1    BlocksWorld                                             Uses only_pddl_instruction before asking for
Blocksworld. Find the domain description (dd;                  domain and problem files grounded in the original
Listing 6), problem description (pd; Listing 7), do-           descriptions.

                                                          11
                                                              Sokoban: Syntactic and Plan Accuracy by Model & Pipeline (grouped by Level)
                                                              Qwen/QwQ-32B                                                                                                    Qwen/Qwen3-32B
                          Level 0   Level 1                    Level 2                                Level 3                              Level 0   Level 1                    Level 2                                 Level 3
                1.0                                                                                                              1.0

                0.8                                                                                                              0.8

                0.6                                                                                                              0.6

                0.4                                                                                                              0.4

                0.2                                                                                                              0.2

                0.0                    l              l       l       ) l )    l            l    l     l     ) l                 0.0                    l              l       l       ) l )    l            l    l     l     ) l
                            er      pdd           pdd pdd ddl pdd ack pdd                pdd pdd pdd ack pdd                                 er      pdd           pdd pdd ddl pdd ack pdd                pdd pdd pdd ack pdd
                       lann                  nl nsim h py2ppddl feedb pddl           dl dl dl edb dl                                    lann                  nl nsim h py2ppddl feedb pddl           dl dl dl edb dl
                  as-p                                                           ypd pypd dl pd w/o fe dl pd                       as-p                                                           ypd pypd dl pd w/o fe dl pd
             llm-                            t h
                                          py pddl
                                                 o  ( w  it py w/o
                                                                    (          p
                                                                            nl pddl pypd ddl pd(                              llm-                            t h
                                                                                                                                                           py pddl
                                                                                                                                                                  o  ( w  i t py w/o
                                                                                                                                                                                     (          p
                                                                                                                                                                                             nl pddl pypd ddl pd(
                                                                ddl                                                                                                              ddl
                                         ddl                l p              py
                                                                                        ddl
                                                                                            p
                                                                                                                                                          ddl                l p              py
                                                                                                                                                                                                         ddl
                                                                                                                                                                                                             p
                                     pyp                pdd                                                                                           pyp                pdd
  Accuracy




                                                                                    l p                                                                                                              l p
                                                                                pdd                                                                                                              pdd
                                                           openai/gpt-oss-120b                                                                                             zai-org/GLM-4.5-Air-FP8
                          Level 0   Level 1                    Level 2                                Level 3                    1.0       Level 0   Level 1                    Level 2                                 Level 3
                1.0
                                                                                                                                 0.8
                0.8

                                                                                                                                 0.6
                0.6

                0.4                                                                                                              0.4


                0.2                                                                                                              0.2


                 0.0                   l              l         l             l      l                                            0.0
                         ann
                             er     pdd
                                                                        )
                                                   pdd pdd ddl pdd ack pdd
                                                                                )               ddl ddl ddl ck) ddl                       ann
                                                                                                                                              er     pdd
                                                                                                                                                        l              l          l       )
                                                                                                                                                                    pdd pdd ddl pdd ack pdd
                                                                                                                                                                                                l )    l          ddl ddl ddl ck) ddl
                    s-pl                       nl nsim h py2ppddl feedb pddl                l p l p l p dba l p                      s-pl                       nl nsim h py2ppddl feedb pddl                 l p l p l p dba l p
                                                                                         pdd pypdd l pdd /o fee l pdd                                                                                      pdd pypdd l pdd /o fee l pdd
             ll m-a                             h o
                                           pyt pddl ( w  it       p y
                                                                       (w / o        p y
                                                                                  nl pddl pypdd ddl (w pdd                    ll m-a                             h o
                                                                                                                                                            pyt pddl ( w  i t       p y
                                                                                                                                                                                         (w / o        p y
                                                                                                                                                                                                    nl pddl pypdd ddl (w pdd
                                                                   ddl                                                                                                               ddl
                                          d dl            d d l p                  py
                                                                                              ddl
                                                                                                  p
                                                                                                                                                           d dl            d  d l p                  py
                                                                                                                                                                                                                ddl
                                                                                                                                                                                                                    p
                                     py p               p                                 l p                                                         py p               p                                  l p
                                                                                      pdd              Plan accuracy            Syntactic accuracy                                                      pdd

                                                          CoinCollector: Syntactic and Plan Accuracy by Model & Pipeline (grouped by Level)
                                                              Qwen/QwQ-32B                                                                                                    Qwen/Qwen3-32B
                          Level 0   Level 1                    Level 2                                Level 3
                                                                                                                                 1.4       Level 0   Level 1                    Level 2                                 Level 3
                1.0
                                                                                                                                 1.2

                0.8                                                                                                              1.0

                                                                                                                                 0.8
                0.6
                                                                                                                                 0.6
                0.4
                                                                                                                                 0.4
                0.2
                                                                                                                                 0.2

                0.0                    l              l       l       ) l )    l            l    l     l     ) l                 0.0                    l              l       l       ) l )    l            l    l     l     ) l
                            er      pdd           pdd pdd ddl pdd ack pdd                pdd pdd pdd ack pdd                                 er      pdd           pdd pdd ddl pdd ack pdd                pdd pdd pdd ack pdd
                       lann                  nl nsim h py2ppddl feedb pddl           dl dl dl edb dl                                    lann                  nl nsim h py2ppddl feedb pddl           dl dl dl edb dl
                  as-p                                                           ypd pypd dl pd w/o fe dl pd                       as-p                                                           ypd pypd dl pd w/o fe dl pd
             llm-                            t h
                                          py pddl
                                                 o  ( w  it py w/o
                                                                    (          p
                                                                            nl pddl pypd ddl pd(                              llm-                            t h
                                                                                                                                                           py pddl
                                                                                                                                                                  o  ( w  i t py w/o
                                                                                                                                                                                     (          p
                                                                                                                                                                                             nl pddl pypd ddl pd(
                                                                ddl                                                                                                              ddl
                                         ddl                l p              py
                                                                                        ddl
                                                                                            p
                                                                                                                                                          ddl                l p              py
                                                                                                                                                                                                         ddl
                                                                                                                                                                                                             p
                                     pyp                pdd                                                                                           pyp                pdd
  Accuracy




                                                                                    l p                                                                                                              l p
                                                                                pdd                                                                                                              pdd
                                                           openai/gpt-oss-120b                                                                                             zai-org/GLM-4.5-Air-FP8
                          Level 0   Level 1                    Level 2                                Level 3                              Level 0   Level 1                    Level 2                                 Level 3
                                                                                                                                 1.0
                1.0

                0.8                                                                                                              0.8


                0.6                                                                                                              0.6


                0.4                                                                                                              0.4


                0.2                                                                                                              0.2

                 0.0                   l               l        l              l      l                                           0.0
                         ann
                             er     pdd
                                                                         )
                                                    pdd pdd ddl pdd ack pdd
                                                                                 )               ddl ddl ddl ck) ddl                      ann
                                                                                                                                              er     pdd
                                                                                                                                                        l               l         l        )
                                                                                                                                                                     pdd pdd ddl pdd ack pdd
                                                                                                                                                                                                 l )    l          ddl ddl ddl ck) ddl
                    s-pl                       nl nsim h py2ppddl feedb pddl                 l p l p l p dba l p                     s-pl                       nl nsim h py2ppddl feedb pddl                  l p l p l p dba l p
                                                                                          pdd pypdd l pdd /o fee l pdd                                                                                      pdd pypdd l pdd /o fee l pdd
             ll m-a                            t h o
                                           py pddl (   w  it      p y
                                                                      l( w / o        p y
                                                                                   nl pddl pypdd ddl (w pdd                   ll m-a                            t h o
                                                                                                                                                            py pddl (   w  i t      p y
                                                                                                                                                                                        l( w / o        p y
                                                                                                                                                                                                     nl pddl pypdd ddl (w pdd
                                            dl                  pdd                 py             p                                                         dl                   pdd                 py             p
                                        p d              p d dl                                ddl                                                       p d                d  dl                                ddl
                                     py                                                    l p                                                        py                  p                                  l p
                                                                                       pdd             Plan accuracy            Syntactic accuracy                                                       pdd


Figure 5: Syntactic accuracy and plan accuracy of various methods grouped by levels and LLMs on Sokoban and
CoinCollector. Error bars shows the standard deviation over 3 runs.




                                                                                                                         12
I am playing with a set of blocks where I need to arrange the blocks into stacks .
Here are the actions I can do

      Pick up a block
      Unstack a block from on top of another block
      Put down a block
      Stack a block on top of another block

   I have the following restrictions on my actions :
   I can only pick up or unstack one block at a time .
   I can only pick up or unstack a block if my hand is empty .
   I can only pick up a block if the block is on the table and the block is clear .
A block is clear if the block has no other blocks on top of it and if the block is
not picked up .
   I can only unstack a block from on top of another block if the block I am
unstacking was really on top of the other block .
   I can only unstack a block from on top of another block if the block I am
unstacking is clear .
   Once I pick up or unstack a block , I am holding the block .
   I can only put down a block that I am holding .
   I can only stack a block on top of another block if I am holding the block being
stacked .
   I can only stack a block on top of another block if the block onto which I am
stacking the block is clear .
   Once I put down or stack a block , my hand becomes empty .
   Once you stack a block on top of a second block , the second block is no longer
clear .

;; Action Heads
pickup      (? b               -    block )
unstack     (? b ? under       -    block )
putdown     (? b               -    block )
stack       (? b ? under       -    block )


                                   Figure 6: Blocksworld Domain Description

As initial conditions I       have that , block1 is clear , block2 is clear , block3 is
clear , block5 is clear ,     the hand is empty , block5 is on top of block4 , block1 is on
the table , block2 is on      the table , block3 is on the table , and block4 is on the
table .
My goal is to have that       block4 is on top of block5 , block1 is on the table , block2
is on the table , block3      is on the table , and block5 is on the table .


                                Figure 7: Blocksworld Problem Description


D.4    NL→PDDL (nl_pddl)                                   only_pddl_instruction plus the generated
                                                           program.
Stage one converts natural language to a structured
prose specification using nl_instruction; stage            D.7   PDDL→PDDL with Feedback
two calls only_pddl_instruction to emit PDDL                     (pddl_pddl)
from the summary plus original descriptions.
                                                           Stage one uses pddl_instruction for direct
D.5    PythonSim→PDDL (pythonsim_pddl)                     PDDL; stage two revises the files using solver feed-
                                                           back from the first attempt.
Stage one gathers a Python simulator via
python_sim_instruction; stage two invokes                  D.8   PDDL→PDDL→PDDL
only_pddl_instruction with the simulator                         (pddl_pddl_pddl)
alongside the original descriptions.                       Applies pddl_instruction across three solver-
                                                           informed revisions.
D.6    PyPDDL→PDDL (pypddl_pddl)
Stage one elicits PyPDDL code with
pypddl_instruction; stage two relies on

                                                      13
( define ( domain blocksworld )
   (: requirements : strips )
(: predicates ( clear ?x)
               (on - table ?x)
               ( arm - empty )
               ( holding ?x)
               ( on ?x ?y))

(: action pickup
   : parameters (? ob )
   : precondition ( and ( clear ? ob ) (on - table ? ob ) ( arm - empty ))
   : effect ( and ( holding ? ob ) ( not ( clear ? ob )) ( not (on - table ? ob ))
                  ( not ( arm - empty ))))

(: action putdown
   : parameters (? ob )
   : precondition ( holding ? ob )
   : effect ( and ( clear ? ob ) ( arm - empty ) (on - table ? ob )
                  ( not ( holding ? ob ))))

(: action stack
   : parameters (? ob ? underob )
   : precondition ( and ( clear ? underob ) ( holding ? ob ))
   : effect ( and ( arm - empty ) ( clear ? ob ) ( on ? ob ? underob )
                  ( not ( clear ? underob )) ( not ( holding ? ob ))))

(: action unstack
   : parameters (? ob ? underob )
   : precondition ( and ( on ? ob ? underob ) ( clear ? ob ) ( arm - empty ))
   : effect ( and ( holding ? ob ) ( clear ? underob )
                  ( not ( on ? ob ? underob )) ( not ( clear ? ob )) ( not ( arm - empty )))))


                                   Figure 8: Blocksworld Domain PDDL

( define ( problem blocksworld - p02 )
   (: domain blocksworld )
   (: objects block1 block2 block3 block4 block5 )
   (: init
      ( on - table block1 )
      ( clear block1 )
      ( on - table block3 )
      ( clear block3 )
      ( on - table block2 )
      ( clear block2 )
      ( on - table block4 )
      ( on block5 block4 )
      ( clear block5 )
      ( arm - empty )
   )
   (: goal ( and
      ( on - table block3 )
      ( on - table block5 )
      ( on block4 block5 )
      ( on - table block2 )
      ( on - table block1 )
   ))
)


                                   Figure 9: Blocksworld Problem PDDL

1.   ( unstack block5 block4 )
2.   ( putdown block5 )
3.   ( pickup block4 )
4.   ( stack block4 block5 )


                                       Figure 10: Blocksworld Plan


                                                    14
I need to move packages between locations . Here are the actions I can do

    Load an package onto a truck at a location ( load - truck package truck location )
    Load an package onto an airplane at a location ( load - airplane package airplane
location )
    Unload an package from a truck at a location ( unload - truck package truck
location )
    Unload an package from an airplane at a location ( unload - airplane package
airplane location )
    Drive a truck from location1 to location2 in a city ( drive - truck truck
location1 location2 city )
    Fly an airplane from airport1 to airport2 ( fly - airplane airplane airport1
airport2 )

I have the following restrictions on my actions :
    I can only load a package onto a truck or airplane if both the package and
airplane are at the location .
    Once I load the package in the truck or airplane , it is no longer at the
location .
    I can only unload a package from a truck or airplane if the truck or airplane
is at the location and the package is in the truck or airplane .
    Once I unload the truck or airplane , the object is at the location and no
longer in the truck or airplane .
    I can only drive a truck between locations if the truck is at the first
location and both the first and second locations are in the same city . Once I drive
a truck , the truck is in the second city and no longer in the first city .
    I can only fly an airplane between two airports and the airplane is at the
first airport .
    Once I fly an airplane , the airplane is at the second airport and no longer at
the first airport .

;; Action Heads
load - truck        (? obj - package     ? truck - truck       ? loc - location )
load - airplane     (? obj - package     ? airplane - airplane ? loc - airport )
unload - truck      (? obj - package     ? truck - truck       ? loc - location )
unload - airplane   (? obj - package     ? airplane - airplane ? loc - airport )
drive - truck       (? truck - truck     ? loc - from - location ? loc - to - location     ? city
- city )
fly - airplane      (? airplane - airplane     ? loc - from - airport   ? loc - to - airport )


                             Figure 11: Logistics Domain Description




As initial conditions , I have that , obj11 is a package , obj12 is a package , obj13
is a package , obj21 is a package , obj22 is a package , obj23 is a package , tru1 is a
truck , tru2 is a truck , cit1 is a city , cit2 is a city , pos1 is a location , apt1 is
a location , pos2 is a location , apt2 is a location , apt1 is an airport , apt2 is an
airport , apn1 is an airplane , apn1 is at apt2 , tru1 is at pos1 , obj11 is at pos1 ,
obj12 is at pos1 , obj13 is at pos1 , tru2 is at pos2 , obj21 is at pos2 , obj22 is at
pos2 , obj23 is at pos2 , pos1 is in cit1 , apt1 is in cit1 , pos2 is in cit2 , and apt2
is in cit2 .
My goal is to have that obj12 is at pos1 , obj23 is at pos1 , obj11 is at apt1 , obj22
is at apt1 , obj13 is at pos2 , and obj21 is at pos2 .


                             Figure 12: Logistics Problem Description




                                               15
;; logistics domain
;;

( define ( domain logistics )
   (: requirements : strips )
   (: predicates ( package ? obj )
              ( truck ? truck )
      ( airplane ? airplane )
                      ( airport ? airport )
                         ( location ? loc )
      ( in - city ? obj ? city )
                      ( city ? city )
      ( at ? obj ? loc )
      ( in ? obj ? obj ))


(: action load - truck
   : parameters
     (? obj
       ? truck
       ? loc )
   : precondition
     ( and ( package ? obj ) ( truck ? truck ) ( location ? loc )
     ( at ? truck ? loc ) ( at ? obj ? loc ))
   : effect
     ( and ( not ( at ? obj ? loc )) ( in ? obj ? truck )))

(: action load - airplane
   : parameters
     (? obj
       ? airplane
       ? loc )
   : precondition
     ( and ( package ? obj ) ( airplane ? airplane ) ( location ? loc )
     ( at ? obj ? loc ) ( at ? airplane ? loc ))
   : effect
     ( and ( not ( at ? obj ? loc )) ( in ? obj ? airplane )))

(: action unload - truck
   : parameters
     (? obj
       ? truck
       ? loc )
   : precondition
     ( and ( package ? obj ) ( truck ? truck ) ( location ? loc )
             ( at ? truck ? loc ) ( in ? obj ? truck ))
   : effect
     ( and ( not ( in ? obj ? truck )) ( at ? obj ? loc )))

(: action unload - airplane
   : parameters
     (? obj
       ? airplane
       ? loc )
   : precondition
     ( and ( package ? obj ) ( airplane ? airplane ) ( location ? loc )
             ( in ? obj ? airplane ) ( at ? airplane ? loc ))
   : effect
     ( and ( not ( in ? obj ? airplane )) ( at ? obj ? loc )))


                                Figure 13: Logistics Domain PDDL (Part 1)




                                                   16
; Logistics domain ( continued )

(: action drive - truck
   : parameters
     (? truck
       ? loc - from
       ? loc - to
       ? city )
   : precondition
     ( and ( truck ? truck ) ( location ? loc - from ) ( location ? loc - to ) ( city ? city )
     ( at ? truck ? loc - from )
     ( in - city ? loc - from ? city )
     ( in - city ? loc - to ? city ))
   : effect
     ( and ( not ( at ? truck ? loc - from )) ( at ? truck ? loc - to )))

(: action fly - airplane
   : parameters
     (? airplane
       ? loc - from
       ? loc - to )
   : precondition
     ( and ( airplane ? airplane ) ( airport ? loc - from ) ( airport ? loc - to )
   ( at ? airplane ? loc - from ))
   : effect
     ( and ( not ( at ? airplane ? loc - from )) ( at ? airplane ? loc - to )))
)


                                Figure 14: Logistics Domain PDDL (Part 2)




( define ( problem logistics -6 -9)
(: domain logistics )
(: objects apn1 apt2 pos2 apt1 pos1 cit2 cit1 tru2 tru1 obj23 obj22 obj21 obj13
obj12 obj11 )
(: init ( package obj11 ) ( package obj12 ) ( package obj13 ) ( package obj21 )
  ( package obj22 ) ( package obj23 ) ( truck tru1 ) ( truck tru2 ) ( city cit1 ) ( city cit2 )
  ( location pos1 ) ( location apt1 ) ( location pos2 ) ( location apt2 ) ( airport apt1 )
  ( airport apt2 ) ( airplane apn1 ) ( at apn1 apt2 ) ( at tru1 pos1 ) ( at obj11 pos1 )
  ( at obj12 pos1 ) ( at obj13 pos1 ) ( at tru2 pos2 ) ( at obj21 pos2 ) ( at obj22 pos2 )
  ( at obj23 pos2 ) (in - city pos1 cit1 ) (in - city apt1 cit1 ) (in - city pos2 cit2 )
  ( in - city apt2 cit2 ))
(: goal ( and ( at obj12 pos1 ) ( at obj23 pos1 ) ( at obj11 apt1 ) ( at obj22 apt1 )
                ( at obj13 pos2 ) ( at obj21 pos2 )))
)


                                   Figure 15: Logistics Problem PDDL




                                                   17
1. ( load - truck obj11 tru1 pos1 )
2. ( load - truck obj13 tru1 pos1 )
3. ( drive - truck tru1 pos1 apt1 cit1 )
4. ( unload - truck obj11 tru1 apt1 )
5. ( unload - truck obj13 tru1 apt1 )
6. ( load - truck obj22 tru2 pos2 )
7. ( load - truck obj23 tru2 pos2 )
8. ( drive - truck tru2 pos2 apt2 cit2 )
9. ( unload - truck obj22 tru2 apt2 )
10. ( unload - truck obj23 tru2 apt2 )
11. ( load - airplane obj22 apn1 apt2 )
12. ( load - airplane obj23 apn1 apt2 )
13. ( fly - airplane apn1 apt2 apt1 )
14. ( unload - airplane obj22 apn1 apt1 )
15. ( unload - airplane obj23 apn1 apt1 )
16. ( load - airplane obj13 apn1 apt1 )
17. ( fly - airplane apn1 apt1 apt2 )
18. ( unload - airplane obj13 apn1 apt2 )
19. ( load - truck obj13 tru2 apt2 )
20. ( drive - truck tru2 apt2 pos2 cit2 )
21. ( unload - truck obj13 tru2 pos2 )
22. ( load - truck obj23 tru1 apt1 )
23. ( drive - truck tru1 apt1 pos1 cit1 )
24. ( unload - truck obj23 tru1 pos1 )


                                      Figure 16: Logistics Plan




I ' m exploring a grid of rooms to collect items . Doors may block passage between
rooms until I open them . Here are the actions I can do :

       Move from one room to an adjacent room in a given direction
       Open a closed door between two rooms ( which then allows travel both ways )
       Take ( pick up ) an item that 's in the same room as me

I have the following restrictions on my actions :

     I can move only if there is an open connection from my current room to the
target room in the intended direction .
     If a door between two rooms is closed , I must open it before I can move through
it .
     To open a door , I must be in one of the two rooms the door connects , and I must
know both the direction I 'm opening in and its reverse (e.g., east / west ,
north / south ).
     Opening the door removes the " closed " state and creates connections in both
directions .
     I can only take an item if I am in the same room as the item and the item
hasn ' t already been taken .
     Once I take an item , it is considered collected ( no longer present in the room ) .

;; Action Heads

move     (? room1 - room ? room2 - room ? direction - direction )
open     (? room1 - room ? room2 - room ? direction - direction ? reverse - direction )
take     (? item - item ? room - room )


                             Figure 17: CoinCollector Domain Description




                                                 18
As initial conditions , I have that , kitchen is a room , corridor is a room , pantry
is a room , north is a direction , south is a direction , east is a direction , west is
a direction , coin is an item , I am at kitchen , there is an open connection from
kitchen to corridor going north , there is an open connection from corridor to
kitchen going south , there is a closed door from kitchen to pantry going east ,
there is a closed door from pantry to kitchen going west , coin is in corridor ,
direction north is reverse of south , direction south is reverse of north , direction
east is reverse of west , and direction west is reverse of east .
My goal is to have that coin is taken .


                               Figure 18: CoinCollector Problem Description




( define ( domain coin - collector )
   (: requirements : strips : typing )
   (: types
      room
      direction
      item
   )
   (: predicates
      ( at ? room - room )
      ( connected ? room1 - room ? room2 - room ? direction - direction )
      ( closed - door ? room1 - room ? room2 - room ? direction - direction )
      ( location ? item - item ? room - room )
      ( taken ? item - item )
      ( is - reverse ? direction - direction ? reverse - direction )
   )

    (: action move
       : parameters (? room1 - room ? room2 - room ? direction - direction )
       : precondition ( and ( at ? room1 ) ( connected ? room1 ? room2 ? direction ))
       : effect ( and ( not ( at ? room1 )) ( at ? room2 ))
    )

   (: action open
       : parameters (? room1 - room ? room2 - room ? direction - direction ? reverse -
direction )
       : precondition ( and ( at ? room1 ) ( closed - door ? room1 ? room2 ? direction )
( is - reverse ? direction ? reverse ))
       : effect ( and ( not ( closed - door ? room1 ? room2 ? direction )) ( not ( closed - door
? room2 ? room1 ? reverse )) ( connected ? room1 ? room2 ? direction ) ( connected ? room2
? room1 ? reverse ))
   )

    (: action take
       : parameters (? item - item ? room - room )
       : precondition ( and ( at ? room ) ( location ? item ? room ) ( not ( taken ? item )))
       : effect ( and ( taken ? item ) ( not ( location ? item ? room )))
    )
)


                                 Figure 19: CoinCollector Domain PDDL




                                                   19
( define ( problem coin_collector_numLocations3_numDistractorItems0_seed54 )
   (: domain coin - collector )
   (: objects
      kitchen corridor pantry - room
      north south east west - direction
      coin - item
   )
   (: init
      ( at kitchen )
      ( connected kitchen corridor north )
      ( closed - door kitchen pantry east )
      ( connected corridor kitchen south )
      ( closed - door pantry kitchen west )
      ( location coin corridor )
      ( is - reverse north south )
      ( is - reverse south north )
      ( is - reverse east west )
      ( is - reverse west east )
   )
   (: goal
      ( taken coin )
   )
)


                            Figure 20: CoinCollector Problem PDDL




1. ( move kitchen corridor north )
2. ( take coin corridor )


                                Figure 21: CoinCollector Plan




                                             20
I am playing a Sokoban puzzle where a player pushes stone crates onto goal squares .
Here are the actions I can do

   Move the player into an adjacent clear square
   Push a stone into an adjacent goal square
   Push a stone into an adjacent non - goal square

   I have the following restrictions on my actions :
   I can only move if I choose one of the four cardinal directions , I am the
player , I am at the from - square , the destination square is clear , and the two
squares are aligned with that direction .
   When I move , I leave my previous square clear and occupy the destination square .
   I can only push a stone toward a goal square if I am the player , the object is a
stone , I stand directly behind the stone in the chosen direction , the target square
is clear , that target square is marked as a goal , and both adjacency relations
match the direction of push .
   After pushing a stone toward a goal square , I advance into the stone 's former
square , the stone moves into the goal square , the goal square is no longer clear ,
my previous square becomes clear , and the stone is marked as being on a goal square .
   I can only push a stone toward a non - goal square if I am the player , the object
is a stone , I stand behind the stone in the direction of push , the destination
square is clear , that destination square is marked as a normal square , and the
adjacency relations match the direction of push .
   After pushing a stone toward a non - goal square , I move into the stone 's former
square , the stone shifts forward , the destination square is no longer clear , and my
previous square becomes clear while the stone is marked as not being on a goal
square .

;; Action Heads
move                (? p - thing ? from - location ? to - location ? dir - direction )
push - to - goal    (? p - thing ?s - thing ? ppos - location ? from - location ? to -
location ? dir - direction )
push - to - nongoal (? p - thing ?s - thing ? ppos - location ? from - location ? to -
location ? dir - direction )


                              Figure 22: Sokoban Domain Description




As initial conditions I have that , player -01 is at pos -1 -1 , stone -01 is at pos -1 -2 ,
pos -1 -3 is clear , pos -1 -3 is a goal square , pos -1 -1 is a normal square , pos -1 -2 is
a normal square , player -01 is the player , stone -01 is a stone , dir - right is an
available move direction , dir - left is an available move direction , dir - up is an
available move direction , dir - down is an available move direction , moving from
pos -1 -1 to pos -1 -2 uses dir - right , moving from pos -1 -2 to pos -1 -1 uses dir - left ,
moving from pos -1 -2 to pos -1 -3 uses dir - right , and moving from pos -1 -3 to pos -1 -2
uses dir - left .
My goal is to have that stone -01 is at a goal square .


                              Figure 23: Sokoban Problem Description




                                               21
( define ( domain sokoban )
   (: requirements : typing )
   (: types thing location direction )
   (: predicates ( move - dir ? v0 - location ? v1 - location ? v2 - direction )
   ( is - nongoal ? v0 - location )
   ( clear ? v0 - location )
   ( is - stone ? v0 - thing )
   ( at ? v0 - thing ? v1 - location )
   ( is - player ? v0 - thing )
   ( at - goal ? v0 - thing )
   ( move ? v0 - direction )
   ( is - goal ? v0 - location )
   )

  ; (: actions move )



  (: action move
     : parameters (? p - thing ? from - location ? to - location ? dir - direction )
     : precondition ( and ( move ? dir )
        ( is - player ?p)
        ( at ?p ? from )
        ( clear ? to )
        ( move - dir ? from ? to ? dir ))
     : effect ( and
        ( not ( at ?p ? from ))
        ( not ( clear ? to ))
        ( at ?p ? to )
        ( clear ? from ))
  )


                             Figure 24: Sokoban Domain PDDL (Part 1)




                                               22
; Sokoban domain ( continued )

  (: action push -to - goal
     : parameters (? p - thing ?s - thing ? ppos - location ? from - location ? to -
location ? dir - direction )
     : precondition ( and ( move ? dir )
        ( is - player ?p)
        ( is - stone ?s)
        ( at ?p ? ppos )
        ( at ?s ? from )
        ( clear ? to )
        ( move - dir ? ppos ? from ? dir )
        ( move - dir ? from ? to ? dir )
        ( is - goal ? to ))
     : effect ( and
        ( not ( at ?p ? ppos ))
        ( not ( at ?s ? from ))
        ( not ( clear ? to ))
        ( at ?p ? from )
        ( at ?s ? to )
        ( clear ? ppos )
        ( at - goal ?s))
  )


  (: action push -to - nongoal
     : parameters (? p - thing ?s - thing ? ppos - location ? from - location ? to -
location ? dir - direction )
     : precondition ( and ( move ? dir )
        ( is - player ?p)
        ( is - stone ?s)
        ( at ?p ? ppos )
        ( at ?s ? from )
        ( clear ? to )
        ( move - dir ? ppos ? from ? dir )
        ( move - dir ? from ? to ? dir )
        ( is - nongoal ? to ))
     : effect ( and
        ( not ( at ?p ? ppos ))
        ( not ( at ?s ? from ))
        ( not ( clear ? to ))
        ( at ?p ? from )
        ( at ?s ? to )
        ( clear ? ppos )
        ( not (at - goal ?s)))
  )

)


                           Figure 25: Sokoban Domain PDDL (Part 2)




                                             23
( define ( problem sokoban - small )
   (: domain sokoban )
   (: objects
      dir - down - direction
      dir - left - direction
      dir - right - direction
      dir - up - direction
      player -01 - thing
      stone -01 - thing
      pos -1 -1 - location
      pos -1 -2 - location
      pos -1 -3 - location
   )
   (: goal ( and (at - goal stone -01) ))
   (: init
      ( at player -01 pos -1 -1)
      ( at stone -01 pos -1 -2)
      ( clear pos -1 -3)
      ( is - goal pos -1 -3)
      ( is - nongoal pos -1 -1)
      ( is - nongoal pos -1 -2)
      ( move dir - down )
      ( move dir - left )
      ( move dir - right )
      ( move dir - up )
      ( is - player player -01)
      ( is - stone stone -01)
      ( move - dir pos -1 -1 pos -1 -2 dir - right )
      ( move - dir pos -1 -2 pos -1 -1 dir - left )
      ( move - dir pos -1 -2 pos -1 -3 dir - right )
      ( move - dir pos -1 -3 pos -1 -2 dir - left )
   )
)


                                     Figure 26: Sokoban Problem PDDL




1. ( push - to - goal player -01 stone -01 pos -1 -1 pos -1 -2 pos -1 -3 dir - right )


                                          Figure 27: Sokoban Plan




                                                       24
Domain Specification BlockStacking
Overview : Arrange blocks into stacks using actions that pick up , unstack , put down ,
or stack blocks , adhering to constraints on hand state and block clarity .

Entity Types :
- block : Represents individual blocks that can be manipulated .

Predicates :
- HandEmpty : True when no block is being held .
- Holding ( b: block ): True when block b is in the hand .
- Clear ( b : block ): True when block b has no blocks on top of it and is not being
held .
- OnTable ( b: block ): True when block b is directly on the table .
- On ( b : block , under : block ): True when block b is immediately on top of block
under .

Actions :
Action : Pickup
Intent : Lift a single block from the table into the hand .
Parameters : b ( block )
Preconditions :
- Positive : Clear (b) , OnTable ( b) , HandEmpty
- Negative : None
Effects :
- Add : Holding (b)
- Delete : HandEmpty , OnTable (b) , Clear (b)
- Conditional : None

Action : Unstack
Intent : Remove a block from on top of another block and hold it .
Parameters : b ( block ) , under ( block )
Preconditions :
- Positive : Clear (b) , On (b , under ) , HandEmpty
- Negative : None
Effects :
- Add : Holding (b) , Clear ( under )
- Delete : On (b , under ) , HandEmpty , Clear (b)
- Conditional : None

Action : Putdown
Intent : Place a held block onto the table .
Parameters : b ( block )
Preconditions :
- Positive : Holding (b)
- Negative : None
Effects :
- Add : OnTable (b) , Clear (b) , HandEmpty
- Delete : Holding (b)
- Conditional : None

Action : Stack
Intent : Place a held block onto another block .
Parameters : b ( block ) , under ( block )
Preconditions :
- Positive : Holding (b) , Clear ( under )
- Negative : None
Effects :
- Add : On (b , under ) , Clear (b) , HandEmpty
- Delete : Holding (b) , Clear ( under )
- Conditional : None


                      Figure 28: NL-PDDL IR from the NL→PDDL pipeline.




                                            25
Problem Specification BlockArrangement
Context : Rearrange the blocks from their initial configuration to a specified goal
state involving multiple stacks and table placements .

Objects :
- block : 1 , 2, 3, 4, 5, 6, 7, 8, 9 , 10 , 11

Initial State :
- Clear (1) holds
- Clear (2) holds
- Clear (3) holds
- Clear (8) holds
- Clear (9) holds
- Clear (10) holds
- HandEmpty holds
- OnTable (1) holds
- OnTable (2) holds
- OnTable (4) holds
- OnTable (6) holds
- OnTable (8) holds
- OnTable (11) holds
- On (3 , 6) holds
- On (5 , 4) holds
- On (7 , 11) holds
- On (9 , 5) holds
- On (10 , 7) holds
- Note : Blocks not explicitly listed as On or OnTable (e.g., block 5) are not on
the table unless stated . For example , OnTable (5) is false because it is on block 4.

Goal Conditions :
- On (1 , 8) must hold
- On (2 , 4) must hold
- On (6 , 1) must hold
- On (9 , 6) must hold
- OnTable (3) must hold
- OnTable (4) must hold
- OnTable (5) must hold
- OnTable (7) must hold
- OnTable (8) must hold
- OnTable (10) must hold
- OnTable (11) must hold


                       Figure 29: NL-PDDL IR from the NL→PDDL pipeline.




                                             26
from dataclasses import dataclass , field
from typing import Dict , Set , Optional , Union , Tuple , List , Iterable , frozenset

@dataclass ( frozen = True )
class State :
    on : Dict [ int , Union [ str , int ]] # block -> ' table ', another block , or ' held '
    clear : frozenset [ int ] # blocks that are clear ( no blocks on top and not held )
    held : Optional [ int ] # the block being held , or None

class Action :
    def __init__ ( self , name : str , params : Tuple ):
        self . name = name
        self . params = params

    def is_applicable ( self , state : State ) -> bool :
        raise NotImplementedError

    def apply ( self , state : State ) -> State :
        raise NotImplementedError

class PickupAction ( Action ):
    def __init__ ( self , block : int ):
        super () . __init__ (" pickup " , ( block ,) )
        self . block = block

    def is_applicable ( self , state : State ) -> bool :
        b = self . block
        return ( state . on [b] == ' table ' and
                 b in state . clear and
                 state . held is None )

    def apply ( self , state : State ) -> State :
        new_on = state . on . copy ()
        new_on [ self . block ] = ' held '

         new_clear = set ( state . clear )
         new_clear . remove ( self . block )
         new_clear = frozenset ( new_clear )

         new_held = self . block

         return State ( new_on , new_clear , new_held )

class UnstackAction ( Action ):
    def __init__ ( self , block : int , under : int ):
        super () . __init__ (" unstack " , ( block , under ))
        self . block = block
        self . under = under

    def is_applicable ( self , state : State ) -> bool :
        return ( state . on [ self . block ] == self . under and
                 self . block in state . clear and
                 state . held is None )

    def apply ( self , state : State ) -> State :
        new_on = state . on . copy ()
        new_on [ self . block ] = ' held '

         new_clear = set ( state . clear )
         new_clear . remove ( self . block )


                Figure 30: PythonSim IR from the PythonSim→PDDL pipeline (Part 1 of 3).




                                                  27
         new_clear . add ( self . under )
         new_clear = frozenset ( new_clear )

         new_held = self . block

         return State ( new_on , new_clear , new_held )

class PutdownAction ( Action ):
    def __init__ ( self , block : int ):
        super () . __init__ (" putdown " , ( block ,) )
        self . block = block

    def is_applicable ( self , state : State ) -> bool :
        return state . held == self . block

    def apply ( self , state : State ) -> State :
        new_on = state . on . copy ()
        new_on [ self . block ] = ' table '

         new_clear = set ( state . clear )
         new_clear . add ( self . block )
         new_clear = frozenset ( new_clear )

         new_held = None

         return State ( new_on , new_clear , new_held )

class StackAction ( Action ):
    def __init__ ( self , block : int , under : int ):
        super () . __init__ (" stack " , ( block , under ))
        self . block = block
        self . under = under

    def is_applicable ( self , state : State ) -> bool :
        return ( state . held == self . block and
                 self . under in state . clear and
                 self . block != self . under )

    def apply ( self , state : State ) -> State :
        new_on = state . on . copy ()
        new_on [ self . block ] = self . under

         new_clear = set ( state . clear )
         new_clear . remove ( self . under )
         new_clear . add ( self . block )
         new_clear = frozenset ( new_clear )

         new_held = None

         return State ( new_on , new_clear , new_held )

def available_actions ( state : State ) -> Iterable [ Action ]:
    actions = []

    # Pickup
    for b in state . on :
        if state . on [b] == ' table ' and b in state . clear and state . held is None :
             actions . append ( PickupAction (b))

    # Unstack


                Figure 31: PythonSim IR from the PythonSim→PDDL pipeline (Part 2 of 3).




                                                  28
    for b in state . on :
        if state . on [b] not in ( ' table ', ' held '):
            under = state . on [b]
            if b in state . clear and state . held is None :
                 actions . append ( UnstackAction (b , under ))

    # Putdown
    if state . held is not None :
        actions . append ( PutdownAction ( state . held ))

    # Stack
    if state . held is not None :
        b = state . held
        for under in state . clear :
             if under != b:
                  actions . append ( StackAction (b , under ))

    return actions

def execute ( action : Action , state : State ) -> State :
    return action . apply ( state )


               Figure 32: PythonSim IR from the PythonSim→PDDL pipeline (Part 3 of 3).




                                                 29
from typing import List , Tuple

def initial_state () -> State :
    on = {
        1: ' table ',
        2: ' table ',
        3: 6,
        4: ' table ',
        5: 4,
        6: ' table ',
        7: 11 ,
        8: ' table ',
        9: 5,
        10: 7,
        11: ' table '
    }
    clear = frozenset ({1 , 2, 3, 8, 9, 10})
    held = None
    return State (on , clear , held )

def is_goal ( state : State ) -> bool :
    return ( state . held is None and
              state . on [1] == 8 and
              state . on [2] == 4 and
              state . on [6] == 1 and
              state . on [9] == 6 and
              state . on [3] == ' table ' and
              state . on [4] == ' table ' and
              state . on [5] == ' table ' and
              state . on [7] == ' table ' and
              state . on [8] == ' table ' and
              state . on [10] == ' table ' and
              state . on [11] == ' table ')

def solve ( limit : int = 1024) -> List [ Action ]:
    from collections import deque

    frontier = deque ()
    frontier . append (( initial_state () , []) )
    visited = set ()

    while frontier and len ( frontier ) < limit :
        state , plan = frontier . popleft ()
        if is_goal ( state ):
            return plan
        if state in visited :
            continue
        visited . add ( state )
        for action in available_actions ( state ):
            next_state = execute ( action , state )
            frontier . append (( next_state , plan + [ action ]) )
    return []


                     Figure 33: PythonSim IR from the PythonSim→PDDL pipeline.




                                                 30
from py2pddl import Domain , create_type
from py2pddl import predicate , action

class BlocksWorldDomain ( Domain ):
    Block = create_type (" block ")

    @predicate ( Block )
    def clear ( self , b):
        " " " Block is clear ( no blocks on top and not held )"""

    @predicate ( Block , Block )
    def on ( self , b , under ):
        " " " Block b is on top of block under """

    @predicate ( Block )
    def on_table ( self , b):
        " " " Block is on the table """

    @predicate ( Block )
    def holding ( self , b):
        " " " Block is being held """

    @predicate ()
    def hand_empty ( self ):
        " " " Hand is empty """

    @action ( Block )
    def pickup ( self , b):
        precond = [
              self . hand_empty () ,
              self . clear (b) ,
              self . on_table (b)
        ]
        effect = [
              ~ self . hand_empty () ,
              self . holding (b) ,
              ~ self . on_table (b) ,
              ~ self . clear (b)
        ]
        return precond , effect

    @action ( Block , Block )
    def unstack ( self , b , under ):
        precond = [
              self . hand_empty () ,
              self . clear (b) ,
              self . on (b , under )
        ]
        effect = [
              ~ self . hand_empty () ,
              self . holding (b) ,
              ~ self . on (b , under ) ,
              ~ self . clear (b) ,
              self . clear ( under )
        ]
        return precond , effect

    @action ( Block )
    def putdown ( self , b):
        precond = [


                  Figure 34: PyPDDL IR from the PyPDDL→PDDL pipeline (Part 1 of 2).




                                                 31
         self . holding (b)
     ]
     effect = [
         ~ self . holding (b) ,
         self . hand_empty () ,
         self . on_table (b) ,
         self . clear (b)
     ]
     return precond , effect

@action ( Block , Block )
def stack ( self , b , under ):
    precond = [
          self . holding (b) ,
          self . clear ( under )
    ]
    effect = [
          ~ self . holding (b) ,
          self . hand_empty () ,
          self . on (b , under ) ,
          ~ self . clear ( under ) ,
          self . clear (b) ,
          ~ self . on_table (b)
    ]
    return precond , effect


              Figure 35: PyPDDL IR from the PyPDDL→PDDL pipeline (Part 2 of 2).




                                             32
from py2pddl import init , goal

class BlocksWorldProblem ( BlocksWorldDomain ):
    def __init__ ( self ):
        super () . __init__ ()
        self . blocks = self . Block . create_objs ( range (1 , 12) , prefix =" block ")

    @init
    def init ( self ):
        clear = [
             self . clear ( self . blocks [0]) ,     #   block1
             self . clear ( self . blocks [1]) ,     #   block2
             self . clear ( self . blocks [2]) ,     #   block3
             self . clear ( self . blocks [7]) ,     #   block8
             self . clear ( self . blocks [8]) ,     #   block9
             self . clear ( self . blocks [9]) ,     #   block10
        ]

         hand_empty = [ self . hand_empty () ]

         on_relations = [
             self . on ( self . blocks [2] ,   self . blocks [5]) , #     block3 on block6
             self . on ( self . blocks [4] ,   self . blocks [3]) , #     block5 on block4
             self . on ( self . blocks [6] ,   self . blocks [10]) , #    block7 on block11
             self . on ( self . blocks [8] ,   self . blocks [4]) , #     block9 on block5
             self . on ( self . blocks [9] ,   self . blocks [6]) , #     block10 on block7
         ]

         on_table = [
             self . on_table ( self . blocks [0]) , #       block1
             self . on_table ( self . blocks [1]) , #       block2
             self . on_table ( self . blocks [3]) , #       block4
             self . on_table ( self . blocks [5]) , #       block6
             self . on_table ( self . blocks [7]) , #       block8
             self . on_table ( self . blocks [10]) , #      block11
         ]

         return clear + hand_empty + on_relations + on_table

    @goal
    def goal ( self ):
        goals = [
             self . on ( self . blocks [0] , self . blocks [7]) ,     #   block1 on block8
             self . on ( self . blocks [1] , self . blocks [3]) ,     #   block2 on block4
             self . on ( self . blocks [5] , self . blocks [0]) ,     #   block6 on block1
             self . on ( self . blocks [8] , self . blocks [5]) ,     #   block9 on block6
             self . on_table ( self . blocks [2]) ,                   #   block3 on table
             self . on_table ( self . blocks [3]) ,                   #   block4 on table
             self . on_table ( self . blocks [4]) ,                   #   block5 on table
             self . on_table ( self . blocks [6]) ,                   #   block7 on table
             self . on_table ( self . blocks [7]) ,                   #   block8 on table
             self . on_table ( self . blocks [9]) ,                   #   block10 on table
             self . on_table ( self . blocks [10]) ,                  #   block11 on table
        ]
        return goals


                        Figure 36: PyPDDL IR from the PyPDDL→PDDL pipeline.




                                                     33
( define
   ( domain blocks-world )
   (: requirements : strips : typing )
   (: types block )
   (: predicates
      ( clear ?b - block )
      ( on ? b - block ?x - block )
      ( ontable ?b - block )
      ( holding ?b - block )
      ( handempty )
   )
   (: action pickup
      : parameters (? b - block )
      : precondition ( and ( clear ?b) ( ontable ?b) ( handempty ))
      : effect ( and ( holding ?b) ( not ( clear ?b)) ( not ( handempty )) ( not ( ontable ?b)) )
   )
   (: action unstack
      : parameters (? b ? under - block )
      : precondition ( and ( clear ?b) ( on ?b ? under ) ( handempty ))
      : effect ( and ( holding ?b) ( clear ? under ) ( not ( on ?b ? under )) ( not ( handempty ))
( not ( clear ?b)))
   )
   (: action putdown
      : parameters (? b - block )
      : precondition ( holding ?b)
      : effect ( and ( ontable ?b) ( handempty ) ( clear ?b) ( not ( holding ?b)))
   )
   (: action stack
      : parameters (? b ? under - block )
      : precondition ( and ( holding ?b) ( clear ? under ))
      : effect ( and ( on ?b ? under ) ( handempty ) ( not ( clear ? under )) ( not ( holding ?b))
( not ( ontable ?b)))
   )
)


                         Figure 37: PDDL IR from the PDDL→PDDL pipeline.




( define
   ( problem block_problem )
   (: domain blocks-world )
   (: objects block1 block2 block3 block4 block5 block6 block7 block8 block9 block10
block11 - block )
   (: init
      ( clear block1 ) ( clear block2 ) ( clear block3 ) ( clear block8 ) ( clear block9 )
( clear block10 )
      ( on block3 block6 ) ( on block5 block4 ) ( on block7 block11 ) ( on block9 block5 )
( on block10 block7 )
      ( ontable block1 ) ( ontable block2 ) ( ontable block4 ) ( ontable block6 ) ( ontable
block8 ) ( ontable block11 )
      ( handempty )
   )
   (: goal
      ( and
         ( on block1 block8 ) ( on block2 block4 ) ( on block6 block1 ) ( on block9 block6 )
         ( ontable block3 ) ( ontable block4 ) ( ontable block5 ) ( ontable block7 ) ( ontable
block8 ) ( ontable block10 ) ( ontable block11 )
      )
   )
)


                         Figure 38: PDDL IR from the PDDL→PDDL pipeline.




                                               34
You are an expert automated planner . Your task is to read a natural - language domain description and a
corresponding problem description , reason through the objects , actions , and goals , and output a valid plan .

Recall the distinctions :
- The ** domain description ** explains the general world : available action schemas , predicates , and object
types .
- The ** problem description ** gives the concrete instance : specific objects , the initial state , and the
goals for this planning episode .

Planning output requirements :
- Think aloud inside < think >... </ think > to lay out objects , preconditions , effects , and progress toward the
goals .
- Produce the final plan inside < plan >... </ plan >. Each action must be on its own line in classical PDDL
plan syntax , e . g . `( move robot1 roomA roomB ) `.
- Maintain the execution order from top to bottom . Do not include step numbers , timestamps , or
probabilities .
- Only emit actions that are applicable given the initial state and that eventually achieve the goals .
- After the closing </ plan > tag , do not add extra commentary .

Example format ( replace names with the task - specific details ) :
< think >
... reasoning about applicable actions ...
</ think >
<plan >
( pick - up block1 hand )
( stack block1 block2 )
( move robot room1 room2 )
</ plan >

Follow this template for every problem . EOF


                                 Figure 39: Base instruction plan_instruction.




                                                         35
PDDL domain file contains domain name , requirements , types of objects in the domain , predicates , and
actions .
Based on the natural language domain description , identify the actions that are possible .
Identify action sematics i . e . understand the preconditions under which that action could be done and the
effects of the action .
Then identify appropriate predicates that could enable action semantics i . e . preconditions and effects .
PDDL domain file has a definitive syntax that must be followed for any domain . An abstract example PDDL
domain file is given below :

< domain_file >
( define
   ( domain domain_name )
   (: requirements : strips : typing )
   (: types
      type1
      type2
   )
   (: predicates
      ( predicate1 ? arg1 - type1 ? arg2 - type2 )
      ( predicate2 ? arg1 - type1 ? arg2 - type2 )
   )
   (: action action1
      : parameters (? arg1 - type1 ? arg2 - type2 ? arg3 - type2 )
      : precondition ( predicate1 ? arg1 ? arg2 )
      : effect ( and ( predicate1 ? arg1 ? arg2 ) ( predicate2 ? arg1 ? arg3 ) )
   )
   (: action action2
      : parameters (? arg1 - type1 ? arg2 - type2 ? arg3 - type2 )
      : precondition ( and ( predicate1 ? arg1 ? arg2 ) ( predicate2 ? arg1 ? arg3 ) )
      : effect ( predicate2 ? arg1 ? arg3 )
   )
)
</ domain_file >

Notes for generating domain file :
- type1 & type2 are only representative and should be replaced with appropriate types . There could be any
number of types .
- predicate1 & predicate2 are only representative and should be replaced with appropriate predicates . There
could be any number of predicates .
- action1 & action2 are only representative and should be replaced with appropriate actions . There could be
any number of actions .
- arg1 & arg2 are only representative and should be replaced with appropriate arguments for predicates and
in preconditions and effects .
- predicates with proper arguments could be combined to combine complex boolean expression to represent
predicondition and effect
The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the arguments to any : precondition or : effect of an action should be declared in : parameters as input
arguments


PDDL problem file contains problem name , domain name , objects in this problem instance , init state of
objects , and goal state of objects .
Based on the natural language problem description , identify the relevant objects for this problems with
their names and types .
Represent the initial state with the appropriate predicates and object arguments . Represent the goal state
with the appropriate predicates and object arguments .
PDDL problem file has a definitive syntax that must be followed for any problem . An abstract example PDDL
problem file is given below .

< problem_file >
( define
   ( problem problem_name )
   (: domain domain_name )
   (: objects
      obj1 obj2 - type1
      obj3 , obj4 - type2
   )
   (: init ( predicate1 obj1 obj3 ) ( predicate2 obj2 obj3 ) )
   (: goal ( and ( predicate1 obj1 obj4 ) ( predicate2 obj2 obj3 ) ) )
)
</ problem_file >

Notes for generating problem file :
- obj1 , obj2 , ... are only representative and should be replaced with appropriate objects . There could be
any number of obects with their types .
- init state with predicate1 & predicate2 is only representative and should be replaced with appropriate
predicates that define init state
- goal state with predicate1 & predicate2 is only representative and should be replaced with appropriate
predicates that define goal state
- predicates with proper arguments could be combined to combine complex boolean expression to represent
init and goal states
- The braces should be balanced for each section of the PDDL program
- Use predicates with arguments of the right type as declared in domain file
- All the objects that would be arguments of predicates in init and goal states should be declared in
: objects


                                 Figure 40: Base instruction only_pddl_instruction.
                                                              36
Natural language planning specifications serve as a blueprint for generating the exact PDDL domain and
problem files . Write in clear prose , but ensure every detail required for a faithful PDDL reconstruction is
present and testable .

Overall guidance :
- Organize the specification with labeled sections so the structure is obvious without PDDL syntax .
- Use precise terminology and consistent naming ; anything omitted here cannot appear in the final PDDL .
- State facts , conditions , and effects explicitly . Avoid implication , ambiguity , or narrative fluff .

Domain description must include :
- Domain title and a one - sentence overview of the scenario .
- Complete list of entity types , subtyping relations when relevant , and the role each type plays .
- Exhaustive catalog of predicates . For each predicate , name every parameter , state its type , and clarify
exactly what the predicate means when true .
- Exhaustive catalog of actions . For each action , provide :
  * Action title and concise intent .
  * Parameter list with names and types , including any constraints or distinctness requirements .
  * Preconditions broken out as positive conditions ( facts that must hold ) and negative conditions ( facts
that must not hold ) , both referencing the predicates above .
  * Effects split into add effects ( facts that become true ) and delete effects ( facts that cease to hold ) .
Mention conditional effects separately if they exist .
  * Any invariants or notes needed to enforce the same logical behavior as PDDL .

Problem description must include :
- Problem title and one - sentence context linking it to the domain .
- Exhaustive list of objects , grouped by type , using the exact type names from the domain section .
- Initial state described as bullet points or sentences , each mapping directly to a predicate instance that
should hold initially . Include explicit mention of facts that are false if the domain relies on them .
- Goal conditions stated explicitly , each tied to predicate instances . Distinguish between conjunctive and
disjunctive goals if applicable .

Formatting conventions :
- Stick to full sentences or crisp bullet points - no raw PDDL , no code blocks , no decorative markup .
- Maintain consistent vocabulary between domain and problem sections so predicates , actions , and objects
align exactly .
- If numeric fluents , temporal elements , or other advanced PDDL features are present , describe their roles ,
bounds , and update rules explicitly .
- The specification must be sufficient for a separate model to regenerate the original PDDL without
guessing .

Abstract example ( replace placeholders with the concrete content for the task at hand ) :
Domain Specification - DomainName
Overview : A single sentence summarizing the planning scenario .
Entity Types :
- Type1 : Explanation of entities of this type and any subtype relationships .
- Type2 : Explanation of entities of this type .
Predicates :
- predicate1 ( entity1 : Type1 , entity2 : Type2 ) : Meaning of the fact when true .
- predicate2 ( entity : Type2 ) : Meaning of the fact when true .
Actions :
Action : Action1
Intent : Brief purpose of the action .
Parameters : entity1 : Type1 , entity2 : Type2 ( include distinctness constraints if required ) .
Preconditions :
- Positive : predicate1 ( entity1 , entity2 ) must hold .
- Negative : predicate2 ( entity2 ) must not hold .
Effects :
- Add : predicate2 ( entity2 ) becomes true .
- Delete : predicate1 ( entity1 , entity2 ) ceases to hold .
- Conditional : Describe any conditional effects explicitly , including their triggering conditions .
Action : Action2
Intent : Another representative action with its parameters , preconditions , and effects fully spelled out .

Problem Specification - ProblemName
Context : One sentence linking the problem to the domain .
Objects :
- Type1 : obj1 , obj2 ( brief descriptions optional ) .
- Type2 : obj3 , obj4 .
Initial State :
- predicate1 ( obj1 , obj3 ) holds because ...
- predicate2 ( obj4 ) is false ( state explicitly if the domain depends on this ) .
Goal Conditions :
- Conjunctive goal requiring predicate2 ( obj3 ) and predicate2 ( obj4 ) to hold .
- Note disjunctions or temporal ordering if the problem includes them .


                                  Figure 41: Base instruction nl_instruction.




                                                         37
{{ plan_instruction }}

### Domain description
{{ domain_description }}

### Problem description
{{ problem_description }}
Generate the plan for this instance following the required format .


                              Figure 42: Prompt template for plan_gen plan generation.




{{ only_pddl_instruction }}

You are an expert PDDL engineer .
Create syntactically correct and mutually consistent domain and problem files using the information below .

### Original domain description
{{ domain_description }}

### Original problem description
{{ problem_description }}

Wrap only the final domain PDDL in < domain_file >... </ domain_file > and the final problem PDDL in
< problem_file >... </ problem_file >.


                                        Figure 43: Prompt template for pddl.




{{ nl_instruction }}

Use the following natural - language descriptions to craft a complete planning specification in prose . Follow
the layout described above .

### Original domain description
{{ domain_description }}

### Original problem description
{{ problem_description }}

Wrap the final structured prose in < nl_summary >... </ nl_summary >. Begin your reasoning with < think > so we
can inspect the chain of thought .
Do not emit any PDDL or code yet .


                                     Figure 44: Stage-one prompt for nl_pddl.




{{ only_pddl_instruction }}

You are an expert PDDL engineer .
Leverage the structured natural - language planning specification , along with the original descriptions , to
produce consistent domain and problem files . Always ground your final answer in the original domain and
problem descriptions shown below .

### Original domain description
{{ domain_description }}

### Original problem description
{{ problem_description }}

### Natural - language planning specification
{{ nl_summary }}

Output syntactically correct PDDL . Wrap only the domain file in < domain_file >... </ domain_file > and the
problem file in < problem_file >... </ problem_file >.


                                     Figure 45: Stage-two prompt for nl_pddl.



                                                        38
{{ python_sim_instruction }}

### Domain description
{{ domain_description }}

### Problem description
{{ problem_description }}

Synthesise the Python planning simulator . Wrap the reusable domain code in < domain_file >... </ domain_file >
and the problem - specific code in < problem_file >... </ problem_file >.


                               Figure 46: Stage-one prompt for pythonsim_pddl.

{{ only_pddl_instruction }}

You are an expert PDDL engineer . Using the natural - language descriptions and the Python simulator below ,
produce syntactically correct and mutually consistent domain / problem PDDL files . Your answer must stay
aligned with the original domain and problem descriptions referenced above .

### Original domain description
{{ domain_description }}

### Original problem description
{{ problem_description }}

### Python simulator \ - domain module
``` python
{{ python_domain_module }}
```

### Python simulator \ - problem module
``` python
{{ python_problem_module }}
```

Wrap only the final domain PDDL in < domain_file >... </ domain_file > and the final problem PDDL in
< problem_file >... </ problem_file >.


                               Figure 47: Stage-two prompt for pythonsim_pddl.

{{ pypddl_instruction }}

### Domain description
{{ domain_description }}

### Problem description
{{ problem_description }}

Write the PyPDDL domain and problem classes . Wrap the domain in < domain_file >... </ domain_file > and the
problem in < problem_file >... </ problem_file >.


                                  Figure 48: Stage-one prompt for pypddl_pddl.

{{ only_pddl_instruction }}

You are an expert PDDL engineer . Using the natural - language descriptions and the PyPDDL program below ,
produce syntactically correct , mutually consistent domain and problem PDDL files . Keep the original
descriptions in mind throughout your answer .

### Original domain description
{{ domain_description }}

### Original problem description
{{ problem_description }}

### PyPDDL domain class
``` python
{{ pypddl_domain_code }}
```

### PyPDDL problem class
``` python
{{ pypddl_problem_code }}
```

Wrap only the final domain PDDL in < domain_file >... </ domain_file > and the final problem PDDL in
< problem_file >... </ problem_file >.


                                  Figure 49: Stage-two prompt for pypddl_pddl.


                                                        39
{{ pddl_instruction }}

Domain description :
{{ domain_description }}

Problem description :
{{ problem_description }}
Write the domain and problem files in minimal PDDL .

Wrap the domain inside < domain_file >... </ domain_file > and the problem inside
< problem_file >... </ problem_file >.


                                    Figure 50: Stage-one prompt for pddl_pddl.

{{ pddl_instruction }}

Domain description :
{{ domain_description }}

Problem description :
{{ problem_description }}
Write the domain and problem files in minimal PDDL .

To aid the revision , the original natural - language descriptions are repeated above .
------ Previous attempt start ------
[ DOMAIN FILE ]
{{ stage1_domain_file }}

[ PROBLEM FILE ]
{{ stage1_problem_file }}
------ Previous attempt end --------

Feedback from the planning solver :
{{ stage1_solver_feedback }}

Revise the domain and problem to fix the issues . Output only the new domain wrapped in
< domain_file >... </ domain_file > and the new problem wrapped in < problem_file >... </ problem_file >.


                                    Figure 51: Stage-two prompt for pddl_pddl.

{{ pddl_instruction }}

Domain description :
{{ domain_description }}

Problem description :
{{ problem_description }}
Write the domain and problem files in minimal PDDL .

Wrap the domain inside < domain_file >... </ domain_file > and the problem inside
< problem_file >... </ problem_file >.


                                Figure 52: Stage-one prompt for pddl_pddl_pddl.

{{ pddl_instruction }}

Domain description :
{{ domain_description }}

Problem description :
{{ problem_description }}
Write the domain and problem files in minimal PDDL .

To aid the revision , the original natural - language descriptions are repeated above .
------ Previous attempt start ------
[ DOMAIN FILE ]
{{ stage1_domain_file }}

[ PROBLEM FILE ]
{{ stage1_problem_file }}
------ Previous attempt end --------

Solver feedback :
{{ stage1_solver_feedback }}

Revise the domain and problem to fix the issues . Output only the new domain wrapped in
< domain_file >... </ domain_file > and the new problem wrapped in < problem_file >... </ problem_file >.


                                Figure 53: Stage-two prompt for pddl_pddl_pddl.


                                                          40
{{ pddl_instruction }}

Domain description :
{{ domain_description }}

Problem description :
{{ problem_description }}
Write the domain and problem files in minimal PDDL .

Review the latest PDDL below together with the solver feedback and produce a final corrected version .

### Previous domain . pddl
``` pddl
{{ stage2_domain_file }}
```

### Previous problem . pddl
``` pddl
{{ stage2_problem_file }}
```

### Solver feedback
{{ stage2_solver_feedback }}

Wrap the refined domain in < domain_file >... </ domain_file > and the refined problem in
< problem_file >... </ problem_file >.


                               Figure 54: Stage-three prompt for pddl_pddl_pddl.




                                                        41
