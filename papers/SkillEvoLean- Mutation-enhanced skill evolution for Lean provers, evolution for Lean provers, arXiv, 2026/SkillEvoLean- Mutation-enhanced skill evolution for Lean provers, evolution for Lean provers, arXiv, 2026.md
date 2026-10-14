                                        SkillEvoLean: Mutation-enhanced skill
                                        evolution for Lean provers

                                         Kuo Zhou                     Zixiong Yang                             Lu Zhang
                                         Peking University            Peking University                        Peking University
                                         zhoukuo@pku.edu.cn           yangzixiong26@stu.pku.edu.cn             zhanglu@sei.pku.edu.cn




                                                                                    A BSTRACT
arXiv:2610.01799v2 [cs.LG] 6 Oct 2026




                                                 Skill evolution offers a promising way to improve large language model agents
                                                 without updating their parameters, but its use in formal theorem proving re-
                                                 mains underexplored. Existing methods mainly target natural-language reason-
                                                 ing, improving skills by analyzing successful and failed trajectories and incre-
                                                 mentally revising solving strategies. Although the Lean verifier provides reliable
                                                 execution feedback, when all sampled trajectories fail, existing skill evolution
                                                 methods lack successful trajectories from which to infer effective update direc-
                                                 tions. Furthermore, these methods also focus mainly on the root instruction file,
                                                 thus underexploring the evolution of reference knowledge including mathemati-
                                                 cal concepts and proving techniques. To address these limitations, we propose
                                                 a mutation-enhanced skill self-evolution framework for building skill-augmented
                                                 Lean provers. The framework jointly evolves a high-level solving policy and its
                                                 reference knowledge through progressive and mutation-based updates. Progres-
                                                 sive evolution derives local improvements from successful and failed trajectories,
                                                 while mutation is triggered when no complete proof can be generated, sampling
                                                 mathematical concepts to produce and select new skill candidates under veri-
                                                 fier feedback. We evaluate our method on MiniF2F, PutnamBench, the 2025
                                                 International Mathematical Olympiad (IMO 2025), and the 2026 USA Mathe-
                                                 matical Olympiad (USAMO 2026). Under the same backbone model, trajectory-
                                                 sampling budget, and test-time compute, our method achieves proof success rates
                                                 of 100.0%, 90.6%, 4/6, and 4/6, respectively, with GPT-5.5, outperforming the
                                                 baseline methods. Further analysis shows that concept-guided mutation outper-
                                                 forms random-text-guided mutation by 6.9 and 8.2 percentage points on MiniF2F
                                                 and PutnamBench, respectively, while solving one additional problem on both
                                                 IMO 2025 and USAMO 2026. Removing the mutation module reduces perfor-
                                                 mance by 16.1 and 18.3 percentage points on MiniF2F and PutnamBench, respec-
                                                 tively, and reduces the number of solved problems to 0/6 on both competition-level
                                                 benchmarks.


                                        1   I NTRODUCTION

                                        Large language models have recently driven rapid progress in formal theorem proving (Polu &
                                        Sutskever, 2020; Polu et al., 2023; Yang et al., 2023; Xin et al., 2024a; Lin et al., 2025a). Ex-
                                        isting approaches improve proof generation through tactic prediction and increasingly powerful
                                        proof-search procedures, enabling models to interact with Lean and iteratively construct machine-
                                        checkable proofs (Jiang et al., 2022; Yang et al., 2023; Song et al., 2024; Xin et al., 2024b). Build-
                                        ing on these advances, agentic Lean provers integrate language-model reasoning with multi-step
                                        search and tool interaction, and have achieved strong performance on challenging formal mathemat-
                                        ics benchmarks (Thakur et al., 2024; Wang et al., 2024; Lin et al., 2025b; Baba et al., 2025; Chung
                                        et al., 2026).
                                        Improving agents through external skills offers a promising alternative to updating model parame-
                                        ters (Ding et al., 2026; Yang et al., 2026b). A skill represents reusable procedural knowledge that
                                        guides reasoning and action, enabling an agent to acquire task-specific capabilities without addi-
                                        tional model training (Liu et al., 2026; Ni et al., 2026; Zhou et al., 2026a). Since skills are explicit


                                                                                           1
and editable, they can also be iteratively refined from execution experience (Zhang et al., 2026; Ni
et al., 2026; Zhou et al., 2026b). However, despite growing interest in skill evolution for general-
purpose agents (Ding et al., 2026; Zhang et al., 2026; Zhou et al., 2026a), its application to formal
theorem proving remains largely unexplored.
Existing studies on skill evolution focus on general-purpose reasoning and tool-use tasks rather
than mathematical problem solving. Typically, these approaches adopt progressive skill evolution,
following a three-step pipeline: collecting execution trajectories, summarizing reusable experience
into a textual patch, and updating the current skill accordingly. However, this update paradigm does
not fully account for the distinctive requirements of formal theorem proving. In particular, when all
sampled trajectories fail, no successful behavior is available to provide an effective update direction.
The skill therefore cannot be meaningfully revised, causing the evolution process to stagnate on
challenging theorem-proving problems.
To overcome this stagnation, we introduce mutation-based evolution into skill optimization, inspired
by the role of mutation in genetic algorithms. Conventional mutation operators, such as swap, in-
sertion, and inversion, cannot be directly applied to skills because arbitrary modifications to natural-
language instructions may disrupt their syntactic coherence and semantic structure. We therefore
propose Concept-Guided Skill Refinement (CGSR), a semantic mutation mechanism specifically de-
signed for skill evolution. The core idea of CGSR is to use large language models to establish two
semantic transformations between the text space and the concept space. As illustrated in Figure 1,
the current skill is first mapped from natural-language instructions to a compact set of concepts that
characterize its underlying reasoning strategies and procedural knowledge. Random perturbations
are then applied to this concept set by adding, removing, or replacing selected concepts. Finally,
the perturbed concepts are mapped back into the text space to generate a structurally coherent but
behaviorally different skill, thereby realizing semantic mutation without directly manipulating the
surface form of the original instructions.
In summary, our contributions are threefold. First, we formulate skill evolution for formal theorem
proving and identify a fundamental limitation of existing trajectory-based progressive evolution:
the update process can stagnate when all sampled proof trajectories fail. Second, we propose a
concept-guided mutation mechanism that introduces mathematically meaningful semantic perturba-
tions while preserving the structural coherence of natural-language skills, enabling broader explo-
ration of the skill space beyond locally derived updates. Third, we develop a unified skill-evolution
framework that combines progressive refinement with mutation-based exploration and validate its
effectiveness on multiple challenging Lean theorem-proving benchmarks, demonstrating consistent
improvements over existing skill-construction and skill-evolution baselines.



2   M ETHOD

We propose a mutation-enhanced skill evolution framework for Lean theorem proving, as illustrated
in Figure 2. Starting from an initial skill, the framework iteratively improves it through two com-
plementary mechanisms. Progressive evolution exploits execution trajectories and verifier feedback
to perform stable, local refinement, while mutation-based evolution is activated when encountering
difficult problems that are completely unsolvable under the current skill, meaning that all generated
trajectories fail, aiming to explore new regions of the skill space via concept-guided perturbation.
Candidate skills are evaluated by the Lean verifier, and effective updates are retained for subse-
quent iterations. The following sections describe the skill representation, initialization, progressive
evolution, and mutation-based refinement in detail.


LLM-Based Operators. Optimization in textual skill space differs fundamentally from optimiza-
tion in continuous model parameter space. Because textual skills are discrete and non-differentiable,
they are optimized using LLM-based operators that perform structured transformations of natural-
language instructions. Throughout this section, operators prefixed with LLM denote prompted in-
vocations of a shared backbone model with operator-specific prompts, inputs, and output formats.
Their functions are summarized in Table 1, with detailed prompt templates provided in the Supple-
mentary Material.


                                                   2
        Concept-Guided Skill Refinement (CGSR)
                                     Original Skill (Text Space)
                                                                                                                                         Overview of Skill Evolution
        1                 Solve the problem step by step.
                          Consider different cases carefully.                                                                                                     Training set D train
                          Ensure the conclusion follows logically.
                                                                                                                    Progressive
                                                                                                                                                                                                                          Mutation-Based
                                                                                                                     Evolution                                                                                              Evolution
        2                           LLM-based Text-to-Concept Mapping
                                                                                                           Execution Trajectories                                                                                  Stagnation

                                           Concept Space                                                                                          S0            S1          S2                     S*
        3                     backward reasoning                                                                                                                                         ...
                              case analysis                                                                                                       </>           </>         </>                    </>             Concept Sampling from
                                                                                                          Successful / Failed Trials
                              contradiction                                                                                                                                                                          Method Dictionary
                              goal decomposition                                                                                        ...                   Skill evolution over time                                    • Problem Decomposition
                                                                                                                                                                                                                           • Analogy
                                                                                                                                                                                                                           • Case Analysis
                                                                                                                                                                                                                           • Backward Reasoning
                                Random Concept Perturbation                                                   Local Feedback
        4                                                                                                                                                                                                                  • Simplification
                    backward reasoning      −         backward reasoning                                             • Error messages
                                                                                                                                                                                                                           • Auxiliary Lemma


                    case analysis       − remove                                                                     • Counterexamples
                                                                                                                                                                                                                   Semantic Mutation
                                                                                                                     • Hints
                    contradiction                replace             induction
                    goal decomposition        + add                  lemma first                             Local Refinement
                                                                                                                                                                                                                   LLM Refinement

                                         Mutated Concept Set
        5                     backward reasoning                                                              </>              </>
                                                                                                                                                                                                                                        </>


                              induction                                                                                                                                                                                  Candidate Skills
                              contradiction                                                                                                                                                                        C1      C2     C3          Cn
                              lemma first                                                                                                                                                                                              ...
                                                                                                                                                                                                                   </>     </>   </>          </>


        6                           LLM-based Concept-to-Text Mapping
                                                                                                                                                          Lean Verifier / Lean Feedback
                                    Mutated Skill (Text Space)
        7            Work backward from the goal to identify key steps.                                                                   </>   </>     </>                λ                               ...

                     Use induction and generalization to handle cases.                                                                  Updated skills /           Lean Compiler        Proof success / failure
                     State helpful lemmas first, then derive the conclusion.                                                            Candidate skills            and Checker        Feedback (errors, traces)


   CGSR performs semantic mutation by perturbing concepts instead of directly editing surface text.                                                                       retain better skill




Figure 1: The CGSR-based mutation algorithm,                                                              Figure 2: Overview of the proposed skill evolu-
which maps a skill into the concept space, per-                                                           tion framework with progressive refinement and
turbs its concept representation, and maps the                                                            mutation-based exploration.
mutated concepts back into the text space.

                            Table 1: Summary of the LLM-based operators used in our framework.

  Operator                                                                         Function
  LLMInitialize                                                                    Generates the initial high-level solving policy stored in SKILL.md.
  LLMConsolidate                                                                   Merges, deduplicates, and filters candidate proof patterns.
  LLMCompare                                                                       Compares successful and failed trajectories to identify behavioral dif-
                                                                                   ferences and possible causes of failure.
  LLMLocate                                                                        Locates the skill component or reference entry that should be up-
                                                                                   dated.
  LLMSuggest                                                                       Generates concrete modification suggestions from trajectory analysis
                                                                                   and verifier feedback.
  LLMRewrite                                                                       Rewrites the current skill according to the generated suggestions
                                                                                   while preserving its overall structure.


Skill Definition. A skill sk is a structured and reusable procedural knowledge artifact made avail-
able to an agent before execution. We define a skill as
                                                                                          sk := (M, R, E),                                                                                                                                    (1)
where M denotes the root natural-language policy stored in SKILL.md, R denotes a collection of
associated reference resources, and E denotes a collection of representative examples.

2.1      P ROGRESSIVE S KILL E VOLUTION

Skill Initialization. The initial skill consists of a root policy M0 and a reference collection R0 .
The root policy is generated through a manually designed prompt:
                                                                                   M0 ← LLMInitialize (pinit ) ,                                                                                                                              (2)
where pinit specifies the Lean theorem-proving task, the expected proof workflow, and the protocol
for interacting with the Lean language server, including submitting proof actions, inspecting proof


                                                                                                      3
Algorithm 1: Progressive Skill Evolution
Require: A family of trajectory sets DT = {T1 , T2 , . . . , TN }, where each Ti contains multiple
    trajectories for the same problem, including both successful and failed trajectories, and the
    current skill S
Ensure: Updated skill Snew
 1: PS ← ExtractPositionTree (S)
 2: D∆S ← ∅
 3: for i = 1 to N do
 4:    Ti+ ← CollectSuccessful (Ti )
 5:    Ti− ← CollectFailed (Ti )
       (Ci , Wi ) ← LLMCompare Ti+ , Ti−
                                           
 6:
 7:    Pi ← LLMLocate (PS , Ci , Wi )
 8:    Ai ← LLMSuggest (Pi , Ci , Wi )
 9:    δSi ← (Pi , Ai ) , D∆S ← D∆S ∪ {δSi }
10: end for
11: S (0) ← S
12: for i = 1 to N do
13:    (Pi , Ai ) ← δSi              
14:    Ciloc ← Retrieve S (i−1) , Pi
                                      
15:    Cei ← LLMRewrite C loc , Ai
                             i          
16:    S (i) ← Replace S (i−1) , Pi , C
                                      ei
17: end for
18: Snew ← S (N )
19: return Snew



states and compiler feedback. Due to space constraints, the detailed skill initialization procedure is
provided in the Supplementary Material.
We progressively refine procedural knowledge by contrasting successful and failed trajectories for
the same problem. Localized updates are generated for relevant positions in the skill directory and
then merged across problems to produce the new skill, as shown in Algorithm 1.

Position Tree Extraction.     We represent the editable structure of a skill as a position tree:

                                  PS = ExtractPositionTree(S).                                     (3)

The tree organizes SKILL.md, references, and examples into uniquely addressed nodes correspond-
ing to files, sections, or entries. Its structure is provided to the skill-updating LLM, allowing it to
locate and modify only the relevant component instead of rewriting the entire skill.

Local Skill Update Generation.        For each problem i, the trajectory set Ti is first divided into
successful and failed subsets:

                    Ti+ = CollectSuccessful(Ti ),        Ti− = CollectFailed(Ti ).                 (4)

We then use LLMCompare to contrast the two subsets and identify effective behaviors Ci from
successful trajectories and failure patterns Wi from failed trajectories:

                               (Ci , Wi ) = LLMCompare Ti+ , Ti− .
                                                                      
                                                                                         (5)

Based on the extracted evidence, we first locate a relevant position Pi in the position tree PS and
then generate a corresponding local update instruction Ai . We represent the resulting local update
as
                                         δSi = (Pi , Ai ).                                       (6)
Finally, we collect the local updates generated for all problems to form the update set D∆S .


                                                   4
Algorithm 2: Random-Concept-Guided Skill Mutation
Require: Initial skill S0 , data set Dtrain , concept dictionary C = {c1 , c2 , . . . , cN }, maximum num-
    ber of evolution iterations Imax , number of mutation candidates M , and concept retrieval size
    K
Ensure: Evolved skill SImax
 1: for i = 1 to Imax do
 2:   Si ← Si−1
 3:   ri ← Evaluate (Si−1 , Dtrain )
 4:   Zi ← Φ (Si−1 ) = LLMConceptualize (Si−1 )
 5:   for j = 1 to M do
             (j)
 6:       ∆Zi ← LLMRetrieve (Zi , C, K)
           (j)              (j)
 7:      Zi      ← Zi ∪ ∆Zi (j) 
          remove
 8:      Zi,j    ← LLMPrune Z i
 9:      Ze(j) ← Z (j)
                   i \ Z
                          remove
            i             i,j                
            (j)       e(j) = LLMRealize Ze(j)
10:      Sei ← Ψ Z     i                  i
                                   
           (j)                 (j)
11:      rei ← Evaluate Si , Dtrain
                              e
              (j)
12:      if rei > ri then
                    (j)        (j)
13:          Si ← Sei , ri ← rei
14:      end if
15:   end for
16: end for
17: return SImax



2.2   M UTATIONAL S KILL E VOLUTION

Progressive skill evolution relies on behavioral differences between successful and failed trajecto-
ries. However, when the current skill fails on all trajectories of a set of difficult problems, no suc-
cessful behavior is available for contrastive analysis. In this case, local updates derived solely from
existing trajectories may repeatedly reinforce the current strategy and fail to explore qualitatively
different solution procedures. To address this limitation, we introduce mutational skill evolution,
which injects randomized external concepts into the skill refinement process. The overall procedure
is presented in Algorithm 2.

Motivation. The design of CGSR is inspired by cognitive psychology research on the organization
of knowledge around deep principles (Chi et al., 1981) and representational change in problem
solving (Knoblich et al., 1999). We hypothesize that, when search under the current skill stagnates,
perturbations at the level of abstract reasoning strategies can help generate alternative problem-
solving procedures. We test this hypothesis through controlled comparisons between concept-guided
mutation and alternative mutation strategies.
Let S denote the textual skill space and C the concept space. Since instructions in a skill are seman-
tically interdependent, directly inserting or deleting sentences in S may break logical consistency or
disrupt the overall workflow. We therefore introduce a skill conceptualization mapping Φ : S → C
and a skill realization mapping Ψ : C → S. Given a skill St , we first map it to its concept repre-
sentation, apply a random perturbation in C, and then realize the perturbed representation as a new
skill:
                                    St+1 = Ψ (Perturb (Φ(St ))) .                                  (7)
This formulation enables semantic-level mutation while maintaining the coherence of the generated
skill.

Concept Space.      We define the concept space as
                                         C = {c1 , c2 , . . . , cN },                                 (8)


                                                      5
Table 2: Planning scenario, not measured results. Provisional success-rate targets and baseline
assumptions across agent backbone models. MiniF2F and PutnamBench entries are percentages;
competition entries are solved problems out of six. The planned comparison uses the same Claude
Code harness, Lean environment, and inference limits within each backbone.

     Backbone Model       Method        MiniF2F       PutnamBench    IMO 2025     USAMO 2026
                          No Skill        61.5            55.3         0/6           0/6
                          Human Skill     82.0            58.2         1/6           1/6
                          LLM Skill      70.5             51.8         0/6           0/6
     DeepSeek-V4-flash
                          Trace2Skill     77.0            55.3         0/6           0/6
                          SkillOpt       77.9             58.8         0/6           1/6
                          Ours            94.7            77.1         2/6           3/6
                          No Skill        68.9            61.2         0/6           0/6
                          Human Skill     82.4            64.1         1/6           1/6
                          LLM Skill      77.5             58.2         0/6           1/6
     DeepSeek-V4-pro
                          Trace2Skill     81.1            61.8         0/6           1/6
                          SkillOpt       84.8             66.5         1/6           1/6
                          Ours            98.4            81.8         2/6           3/6
                          No Skill        89.3            78.2         1/6           1/6
                          Human Skill     91.0            82.9         1/6           1/6
                          LLM Skill      90.6             79.4         2/6           1/6
     GPT-5.5
                          Trace2Skill     93.4            82.4         1/6           1/6
                          SkillOpt       90.2             85.3         2/6           2/6
                          Ours           100.0            90.6         4/6           4/6


where each concept represents a general reasoning principle or problem-solving operation, such as
decomposition, analogy, case analysis, or backward reasoning. For a skill St ∈ S, the conceptual-
ization mapping extracts its concept representation:
                                     Zt = Φ(St ),       Zt ⊆ C.                                   (9)
Compared with raw textual instructions, Zt provides a structured semantic representation of the
strategies encoded in the skill.

Random Concept Perturbation. To introduce alternative reasoning behaviors, we employ a
stochastic LLM-based concept retriever to select new concepts from the concept dictionary C. Given
the current concept representation Zt and a predefined retrieval size K, the retriever produces a set
of concepts that are not already contained in Zt :
                                ∆Zt = LLMRetrieve (Zt , C, K) ,
                                                                                                (10)
                                ∆Zt ⊆ C \ Zt , |∆Zt | = K.
The stochasticity of the LLM retriever allows different concept sets to be obtained across mutation
attempts. The retrieved concepts are first incorporated into the current representation by set union:
                                         Z t = Zt ∪ ∆Zt .                                       (11)
Because the newly retrieved concepts may conflict with existing concepts or introduce semantically
redundant information, we employ an LLM-based pruning operator to identify concepts that should
be removed:
                                   Ztremove = LLMPrune Z t .
                                                              
                                                                                               (12)
The final perturbed concept representation is then obtained by removing these conflicting or redun-
dant concepts:
                               Zet = Perturb(Zt ) = Z t \ Ztremove .                           (13)

Skill–Concept Mappings. We implement both mappings using few-shot prompting with a shared
backbone LLM. The demonstrations consist of human-authored skill documents paired with their
key concepts, providing examples of how concrete textual instructions correspond to abstract rea-
soning strategies. Based on these demonstrations, the skill conceptualization mapping Φ : S → C
extracts the concepts encoded in a textual skill:
                             Zt = Φ(St ) = LLMConceptualize(St ).                               (14)


                                                  6
Conversely, the skill realization mapping Ψ : C → S converts a perturbed concept representation
into a coherent textual skill:
                                 St′ = Ψ(Zet ) = LLMRealize(Zet ).                                 (15)
These mappings are semantic transformations rather than exact inverses: Φ abstracts concrete in-
structions into concepts, whereas Ψ instantiates concepts as executable solving strategies and work-
flows.
Overall, mutational skill evolution is formulated as
                                        Φ       Perturb        Ψ
                                 Si−1 −−→ Zi −−−−−−→ Zei −−→ Sei ,                                 (16)
where Φ denotes the skill conceptualization mapping, which abstracts the procedural knowledge
and reasoning strategies encoded in the current skill Si−1 into a concept representation Zi . The
perturbation operator modifies Zi by introducing randomly sampled concepts, producing the per-
turbed representation Zei . Finally, Ψ denotes the skill realization mapping, which converts Zei into a
coherent textual skill Si through holistic rewriting.
                       e

Evaluation.    A candidate that passes the interpretation stage is evaluated on the evaluation task set:
                                                                  
                                   (t)                  (t)
                                 rei,j = Evaluate sk i,j , Dtrain .
                                                     f                                             (17)

The mutation is accepted only when it improves upon the best score obtained in the current evolution
iteration:
                                              (t)
                                            rei,j > ri .                                        (18)
Otherwise, the candidate is discarded and the current skill is preserved. Repeating this process over
multiple concept lists and evolution iterations yields a stochastic search over qualitatively different
skill variants while ensuring that only empirically beneficial mutations are retained.
Acceptance based on an aggregate score does not guarantee that every previously solved problem
remains solvable. We therefore examine problem-level regressions and retention in Section 3.4.
Unlike progressive evolution, which exploits trajectory-level differences to produce localized up-
dates, mutational evolution emphasizes exploration through randomized conceptual perturbations.
The two mechanisms are therefore complementary: progressive evolution refines effective behaviors
when informative successful trajectories are available, whereas mutational evolution helps the skill
escape stagnant strategies when the current policy completely fails on difficult problems.

3   E XPERIMENTS
Benchmarks. We evaluate our method on these Lean benchmarks: 1) MiniF2F-test contains
high-school competition problems covering algebra, number theory, inequalities, and related topics.
2) PutnamBench consists of Lean formalizations of undergraduate-level Putnam problems span-
ning analysis, algebra, combinatorics, and number theory. 3) IMO 2025 contains recent olympiad
problems at the highest pre-university competition level. 4) USAMO 2026 contains high-difficulty
olympiad problems. We formalize these problems with the assistance of GPT-5.5.

Baselines. We compare our method against these baselines: No Skill, which runs the frozen target
model with the default system prompt; Human Skill, an expert-written skill document manually
designed for Lean theorem proving; LLM Skill, which is generated once from a high-level task
description and remains fixed throughout evaluation; Trace2Skill Ni et al. (2026), which distills
reusable skills from execution trajectories; and SkillOpt Yang et al. (2026a), which iteratively op-
timizes a natural-language skill using execution feedback. All methods use the same target model,
test set, Lean environment, and inference budget.

Implementation Details. We use DeepSeek-V4-Pro to initialize skills and implement all LLM-
based operations in skill evolution, including attribution, merging, refinement, and mutation, with
task-specific prompts. All training problems are drawn from FormalMath (Yu et al., 2025) and


                                                   7
Figure 3: Progressive evolution converges without mutation. Without mutation-based exploration,
progressive updates gradually saturate.

Table 3: Planning scenario, not measured results. Component ablation targets with DeepSeek-
V4-Pro. P ROG . and M UT. denote progressive and mutation-based evolution. All variants are to use
the same initial skill and evaluation limits.

                         Variant    MiniF2F PutnamBench IMO USAMO
                         Full Method 98.4       81.8     2/6  3/6
                         w/o Prog.   92.1       74.5     1/6  2/6
                         w/o Mut     82.3       63.5     0/6  0/6


are disjoint from the evaluation benchmarks. During evaluation, Claude Code serves as the agent
harness, while DeepSeek-V4-Pro, DeepSeek-V4-Flash, and GPT-5.5 are used as frozen backbones
to execute skills and interact with Lean. For IMO and USAMO, GPT-5.5 first generates natural-
language solutions, and verified solutions are inserted as comments into the corresponding Lean
files; this step is omitted for the other datasets. For Algorithm 2, we set the maximum number of
evolution iterations Imax = 5, the number of mutation candidates per iteration = 20, and the concept
retrieval = 3 . All experiments use mathlib v4.30.0.

3.1   M AIN R ESULTS

Table 2 compares our method with different skill construction and optimization approaches across
three backbone models. Our method consistently achieves the best performance on all four bench-
marks, demonstrating that the proposed skill evolution framework generalizes across backbone mod-
els with substantially different baseline capabilities. With DeepSeek-V4-flash, our method achieves
94.7% on MiniF2F-test and 77.1% on PutnamBench, outperforming the strongest baseline by 12.7
and 18.3 percentage points, respectively. Similar improvements are observed with DeepSeek-V4-
pro, where our method improves the best baseline from 84.8% to 98.4% on MiniF2F-test and from
66.5% to 81.8% on PutnamBench. The gains remain substantial with the stronger GPT-5.5 back-
bone. Our method solves all problems in MiniF2F-test and achieves 90.6% on PutnamBench, ex-
ceeding the strongest baselines by 6.6 and 5.3 percentage points, respectively. Moreover, it solves
4/6 problems on both IMO 2025 and USAMO 2026, whereas the strongest baseline solves at most
2/6 problems on either benchmark. These results indicate that skill evolution provides improve-
ments beyond those obtained by simply using a stronger backbone, particularly on difficult problems
that require qualitatively different proof strategies rather than local refinements of existing solution
behaviors. Overall, the improvements are particularly pronounced for the weaker DeepSeek-V4-


                                                   8
Table 4: Planning scenario, not measured results. Mutation-guidance targets with DeepSeek-V4-
Pro under matched evaluation limits.

                        Strategy  MiniF2F PutnamBench IMO USAMO
                        UM         83.7       62.4     0/6  1/6
                        RTGM       91.5       73.6     1/6  2/6
                        CGM (Ours) 98.4       81.8     2/6  3/6


flash and DeepSeek-V4-pro backbones, suggesting that evolved skills can partially compensate for
limitations in the underlying model. Meanwhile, the consistent gains obtained with GPT-5.5 show
that the proposed framework remains effective even when the backbone already exhibits strong
theorem-proving capabilities.
Static skill construction yields less consistent improvements across backbones and benchmarks. For
instance, LLM Skill underperforms No Skill on PutnamBench with both DeepSeek-V4-flash and
DeepSeek-V4-pro, while Human Skill provides only moderate gains. Trace2Skill and SkillOpt gen-
erally outperform directly generated skills, but their benefits vary across models. In contrast, our
method consistently surpasses both static skills and existing optimization methods, demonstrating
the value of iterative refinement from execution feedback. The results also show that backbone
capability and skill evolution are complementary. Stronger backbones achieve higher No Skill per-
formance, leaving less room for improvement on saturated benchmarks such as MiniF2F-test. Nev-
ertheless, our method improves GPT-5.5 from 89.3% to 100.0% on MiniF2F-test and from 78.2%
to 90.6% on PutnamBench. Thus, skill evolution not only compensates for weaker models but also
improves the reasoning and proof-construction behavior of strong backbones. This trend extends
to competition-level problems. Most baselines solve at most one problem with the DeepSeek back-
bones and two with GPT-5.5. Our method solves 2/6 IMO 2025 and 3/6 USAMO 2026 problems
with both DeepSeek variants, and reaches 4/6 on both benchmarks with GPT-5.5. Despite the small
benchmark sizes, these consistent gains suggest that evolved skills transfer beyond standard distri-
butions and provide useful guidance for difficult proofs.

3.2   A BLATION S TUDIES

We conduct ablation studies to answer two questions. First, we examine whether progressive evolu-
tion and mutation are both necessary for effective skill evolution. Second, we investigate whether the
effectiveness of mutation comes from mathematical concept guidance rather than arbitrary pertur-
bations. For a fair comparison, all variants use DeepSeek-V4-Pro as the backbone model, together
with the same initial skill and training problems.

C OMPONENT A BLATION .
Table 3 shows that both progressive evolution and mutation are important to overall performance.
The full method achieves 98.4% on MiniF2F-test and 81.8% on PutnamBench. Removing pro-
gressive evolution reduces the results to 92.1% and 74.5%, while the numbers of solved problems
decrease from 2/6 to 1/6 on IMO 2025 and from 3/6 to 2/6 on USAMO 2026. This indicates that pro-
gressive evolution enables stable, trajectory-driven refinement. Removing mutation causes a larger
degradation, reducing accuracy to 82.3% on MiniF2F-test and 63.5% on PutnamBench, with no
problems solved on either IMO 2025 or USAMO 2026. This supports our motivation that progres-
sive updates alone are insufficient when the current skill cannot produce successful trajectories. As
shown in Figure 3, performance improves rapidly during the first four evolution cycles and gradu-
ally saturates after the fifth, demonstrating the convergence of progressive skill evolution. Overall,
mutation expands the search space with qualitatively different proof strategies, whereas progressive
evolution consolidates effective behaviors through stable local refinement. Their complementary
effects explain the consistent advantage of the full method across all four benchmarks.

E FFECT OF M UTATION G UIDANCE .
We further investigate whether the effectiveness of mutation arises merely from introducing arbitrary
perturbations or from using task-relevant mathematical concepts as semantic guidance. Under the
same backbone model, initial skill, evolution budget, and evaluation budget, we compare the follow-


                                                  9
Table 5: Planning targets, not measured results. Proof success and inference cost on Putnam-
Bench with DeepSeek-V4-Pro. Success rates match the provisional main table. Cost targets con-
cern test-time execution after skills have been finalized and frozen. Per-problem averages include
successful, failed, and timed-out attempts. Tokens per solved problem divide total test tokens by the
number of solved problems. K denotes thousands of tokens. No token usage, timing, or variability
has been measured for this scenario.

               Success    Input tokens Output tokens Lean calls      Time       Tokens/solved
Method        rate (%) ↑ (K/problem) ↓ (K/problem) ↓ /problem ↓ (min/problem) ↓ problem (K) ↓
No Skill        61.2          80.0            20.0          10.0           20.0            163.4
Human Skill     64.1          88.0            18.0           9.0           19.5            165.4
LLM Skill       58.2          92.0            22.0          11.0           22.0            195.9
Trace2Skill     61.8          90.0            18.0           9.5           20.0            174.8
SkillOpt        66.5          84.0            17.0           8.5           18.0            151.9
Ours            81.8          82.0            14.0           8.0           17.0            117.4



ing three mutation strategies: Unguided Mutation (UM) directly modifies the current skill without
additional semantic guidance. Random-Text-Guided Mutation (RTGM) uses randomly sampled
task-irrelevant text to guide skill mutation. Concept-Guided Mutation (CGM) uses mathematical
concepts to guide the generation of diverse and task-relevant skill variants. As shown in Table 4,
UM achieves the weakest performance, obtaining 83.7% on MiniF2F and 62.4% on PutnamBench,
while solving 0/6 IMO 2025 problems and 1/6 USAMO 2026 problems. RTGM improves the re-
sults to 91.5% and 73.6%, respectively, and solves 1/6 IMO 2025 problems and 2/6 USAMO 2026
problems. This suggests that external perturbations can encourage more diverse skill updates, even
when the guidance itself is not directly relevant to theorem proving. Nevertheless, CGM consis-
tently outperforms both alternatives, achieving 98.4% on MiniF2F and 81.8% on PutnamBench,
while solving 2/6 IMO 2025 problems and 3/6 USAMO 2026 problems. Compared with RTGM,
CGM yields additional gains of 6.9 percentage points on MiniF2F and 8.2 percentage points on
PutnamBench, while solving one additional problem on each competition benchmark. These results
indicate that the benefit of mutation does not come solely from arbitrary variation. Mathematical
concepts provide structured semantic directions that promote exploration while preserving relevance
to the theorem-proving task, resulting in more effective skill mutations.

3.3   I NFERENCE C OST A NALYSIS

Evaluation Protocol. We plan to evaluate the recurring inference cost of reusing final, frozen
skills across theorem-proving tasks. Skill construction and evolution costs are outside the scope of
this analysis. Table 5 provides the comparison for the six methods in our main experiments, us-
ing DeepSeek-V4-Pro on PutnamBench. The comparison uses the same test problems, per-problem
attempt and token limits, timeout, stopping rule, and execution concurrency. Actual resource con-
sumption must be measured under these limits; the present entries are design targets and baseline
assumptions.

Cost Accounting. Test-time input and output tokens are accumulated over all attempts for each
problem and averaged over the complete test set. Input tokens include loaded skill content, reference
resources, and interaction history; output tokens include reasoning tokens when reported by the
API, without double counting. Lean calls count verification invocations, and time measures elapsed
execution time per problem, including tool execution and failed attempts. These quantities measure
computational usage; token counts alone do not represent monetary cost.
To account for the resources spent on unsuccessful proofs, we also report the test-time token cost
per solved problem:
                                          PNtest in           
                                                   Ti + Tiout
                                Tsolved = i=1PNtest             ,                             (19)
                                                   i=1 yi
where yi = 1 if at least one attempt yields a verified proof for problem i, and yi = 0 otherwise. The
numerator includes all test attempts, including failures. The metric is undefined when no problem is
solved. It therefore differs from averaging token usage only over successful problems.


                                                 10
Table 6: Planning targets, not measured results. Forgetting and retention with DeepSeek-V4-Pro.
Retained, gained, and lost are normalized per 100 audit problems, not raw counts. The initial skill is
assumed to match the LLM Skill row in the main table; retained plus gained matches the component-
ablation targets. Historical forgetting includes problems first solved at intermediate checkpoints.
The frozen control allows sampling losses without an update. pp denotes percentage points. No
standard deviations are assumed; independent runs must supply them.

                       Retained      Gained         Lost       Retention   Net gain      Historical
  Method               (per 100)   (per 100) ↑   (per 100) ↓    (%) ↑       (pp) ↑    forgetting (%) ↓
   MiniF2F-test (initial success assumption: 77.5%)
  Frozen S0 (control)      76.5        1.0            1.0        98.7         0.0           3.1
  w/o Prog.                73.5        18.6           4.0        94.8        14.6           5.6
  w/o Mut.                 76.0         6.3           1.5        98.1         4.8           2.9
  Full Method              76.5        21.9           1.0        98.7        20.9           1.4
   PutnamBench (initial success assumption: 58.2%)
  Frozen S0 (control)    56.7        1.5           1.5           97.4         0.0           4.9
  w/o Prog.              53.2        21.3          5.0           91.4        16.3           9.7
  w/o Mut.               56.2         7.3          2.0           96.6         5.3           5.2
  Full Method            56.7        25.1          1.5           97.4        23.6           3.5


Target Success–Cost Trade-off. In this planning scenario, the full method targets an 81.8% suc-
cess rate, 15.3 percentage points above the assumed SkillOpt baseline. Average total tokens de-
crease modestly from 101K to 96K per problem (5.0%), while tokens per solved problem decrease
from 151.9K to 117.4K (22.7%, computed before rounding). The intended benefit is higher verified
coverage at approximately the same token budget. These differences are planning arithmetic, not
observed improvements or evidence that the method will reach the targets.

Target Interaction Overhead. Relative to the assumed SkillOpt baseline, the targets reduce input
tokens from 84K to 82K, output tokens from 17K to 14K, and Lean calls from 8.5 to 8.0 per problem.
The time target changes from 18 to 17 minutes (5.6%). Input usage remains above the No Skill
assumption of 80K, allowing for skill-loading overhead. A practical first milestone is at least 20%
fewer tokens per solved problem without reduced proof success under matched limits. The absolute
token and time values require calibration in a pilot; they are neither runtime predictions nor monetary
estimates.

3.4   F ORGETTING AND K NOWLEDGE R ETENTION

Higher aggregate proof success can conceal regressions on previously solved problems. We plan to
examine whether skill evolution preserves earlier capabilities while acquiring new ones, including
capabilities first acquired at intermediate checkpoints and subsequently lost.

Evaluation Protocol. We plan to compare the full method with its progressive-only and mutation-
only variants, starting from the same initial skill S0 . The audit uses MiniF2F-test and PutnamBench
separately, with DeepSeek-V4-Pro and identical per-problem sampling limits, tool settings, and
stopping rules. Checkpoints are selected according to a predefined schedule, including S0 and the
final skill ST . Audit problems are disjoint from the evolution data, and audit outcomes are never used
to generate, accept, or select skill updates. The final checkpoint is fixed by the evolution protocol,
rather than selected by its audit performance. The planning table normalizes counts by audit-set size
to avoid assuming an unrecorded benchmark subset. Measured results should also report the actual
audit size and raw counts for each run.

Retention Metrics. Within one run, let At be the set of audit problems solved by at least one
verified proof under the fixed attempt budget with skill St . For an audit set Daudit , the initial-to-
final transitions are
                                         K = A0 ∩ AT ,
                                          G = AT \ A0 ,                                           (20)
                                          L = A0 \ AT ,

                                                   11
where K, G, and L contain retained, gained, and lost problems, respectively. Retention is
100|K|/|A0 |, and the net change in success rate is 100(|G| − |L|)/|Daudit | percentage points. An
initially solved problem that is lost and later recovered is retained in this endpoint comparison; its
temporary regression remains visible in the checkpoint-level transitions.
To include capabilities acquired after initialization, we also measure
                                                 −1
                                                T[
                                          H=           At ,
                                                t=0                                               (21)
                                                   |H \ AT |
                                       Fhist = 100           .
                                                     |H|
Here H contains all problems solved at any audited checkpoint before the final one. Historical
forgetting is the fraction of these problems no longer solved at the final checkpoint. Ratios with
empty denominators are reported as undefined, not zero. We compute each metric within each run
before averaging; successful problems are not pooled across independent runs.

Sampling Variability. Observed success-to-failure transitions under a finite sampling budget do
not by themselves establish persistent forgetting. We therefore repeat independent evolution and au-
dit runs and apply the same checkpoint schedule and evaluation budget to an unchanged S0 control.
The control estimates apparent losses from repeated stochastic execution. Historical forgetting is
compared under the same number of audited checkpoints, since additional checkpoints create more
opportunities to observe a transient success. Claims of persistent regression require fresh reevalua-
tion of affected problems with both the earlier and later skills.

Target Acquisition and Retention. Per 100 MiniF2F-test problems, the full-method scenario re-
tains 76.5, gains 21.9, and loses 1.0, giving 98.7% retention and a 20.9-point net gain. On Putnam-
Bench, the corresponding targets are 56.7, 25.1, and 1.5, giving 97.4% retention and a 23.6-point
net gain. Retained plus gained recovers the respective 98.4% and 81.8% stretch success targets. A
practical first milestone is at least 95% retention with positive net gain on both benchmarks. The
nonzero losses explicitly allow some regressions; aggregate improvement alone is not evidence of
complete retention.

Target Forgetting Across Checkpoints. The full-method historical-forgetting targets are 1.4%
on MiniF2F-test and 3.5% on PutnamBench, compared with assumed frozen-control values of 3.1%
and 4.9%. The mutation-only scenarios allow larger losses (5.6% and 9.7%); the progressive-only
scenarios use 2.9% and 5.2%. Historical forgetting is specified from hypothetical checkpoint unions,
not inferred from endpoint counts. These assumptions express a retention hypothesis to test. No
independent reevaluation or causal attribution to either module has yet been established by these
target values.

4     R ELATED W ORK
4.1   S KILL E VOLUTION

Recent studies have explored skill evolution as a way to improve language-model agents through
explicit and editable procedural knowledge rather than parameter updates. Approaches most rele-
vant to our work mainly derive skill updates from execution feedback or trajectory analysis (Ding
et al., 2026). Execution-feedback methods revise skills using runtime errors, environment observa-
tions, unmet requirements, or verifier responses, enabling agents to correct ineffective instructions
through interaction (Liu et al., 2026; Zhang et al., 2026; Yang et al., 2026b). Trajectory-distillation
methods instead analyze complete execution traces to extract reusable strategies from successful
behaviors and recurring failure patterns. For example, Trace2Skill contrasts successful and failed
trajectories to generate targeted skill patches and consolidates repeated modifications into reusable
instructions (Ni et al., 2026). Similarly, some methods convert execution experience into persis-
tent procedural knowledge for future tasks (Zhou et al., 2026b;a). Despite their effectiveness, these
approaches remain feedback-driven and depend on sufficiently informative trajectories. Execution-
based refinement becomes ineffective when feedback is sparse or only indicates final correctness,


                                                  12
while trajectory distillation requires successful or partially successful behaviors from which useful
update directions can be inferred (Ding et al., 2026). This limitation is especially pronounced in
formal theorem proving. Although Lean can reliably reject invalid proofs, when all sampled trajec-
tories fail, it provides little evidence about which high-level strategy should replace the current one.
Consequently, trajectory-based progressive evolution may stagnate on difficult problems.

4.2   LLM-BASED L EAN P ROVERS .

Existing Lean provers mainly improve formal proof generation through tactic prediction, proof
search, and model training. Early representative systems include PACT (Han et al., 2022), which
uses proof-artifact co-training; HyperTree Proof Search (Lample et al., 2022), which combines neu-
ral tactic prediction with structured search; and LeanDojo/ReProver (Yang et al., 2023), which intro-
duces retrieval-augmented proving in an interactive Lean environment. Later methods incorporate
explicit reasoning, expert iteration, reinforcement learning, and verifier feedback, including Lean-
STaR (Lin et al., 2024), InternLM2.5-StepProver (Wu et al., 2024), and DeepSeek-Prover-V1.5 (Xin
et al., 2024b). More recent systems further explore large-scale proof synthesis, subgoal decom-
position, self-correction, and deeper Lean interaction, such as Goedel-Prover (Lin et al., 2025a),
DeepSeek-Prover-V2 (Ren et al., 2025), Kimina-Prover (Wang et al., 2025), Goedel-Prover-V2 (Lin
et al., 2025b), and Seed-Prover (Chen et al., 2025). These advances demonstrate the effectiveness
of combining language-model reasoning with formal verification, structured search, and iterative
proof refinement. However, existing agentic provers generally do not explicitly focus on external
skills. Consequently, useful problem-solving techniques discovered during proof construction are
often limited to individual trajectories and cannot be effectively reused to guide subsequent prob-
lems. Skill evolution (including our work) addresses this limitation by treating skills as evolving
procedural knowledge, allowing effective strategies and recurring failure patterns to be progres-
sively integrated, refined, and leveraged across problems. In fact, it is feasible to combine advances
in both directions to further boost formal theorem proving.


5     C ONCLUSION & D ISCUSSION

We presented SkillEvoLean, a mutation-enhanced skill evolution framework for Lean theorem prov-
ing. It combines progressive evolution for trajectory-based local refinement with concept-guided
mutation for exploring new strategies when refinement stagnates. Experiments on MiniF2F, Put-
namBench, IMO 2025, and USAMO 2026 show consistent improvements across multiple backbone
models over static and existing skill optimization baselines. Ablation studies further demonstrate the
complementary roles of progressive evolution and mutation, as well as the effectiveness of mathe-
matical concept guidance. These results highlight self-evolving skills as a promising direction to
improving formal theorem provers without additional parameter training.
Beyond the empirical gains, our findings suggest that skill evolution can serve as a mechanism for
accumulating and reusing procedural knowledge across theorem-proving tasks. Progressive refine-
ment helps consolidate effective behaviors observed in proof trajectories, while mutation broad-
ens the search space beyond locally derived updates. Their combination therefore supports both
knowledge exploitation and strategy exploration. Nevertheless, the quality of evolved skills re-
mains dependent on the diversity of training problems, the informativeness of proof trajectories, and
the reliability of skill evaluation. Future work may investigate more compact skill representations,
mechanisms for resolving redundant or conflicting instructions, and transfer across different formal
libraries, theorem domains, and interactive theorem provers.


R EFERENCES
Kaito Baba, Chaoran Liu, Shuhei Kurita, and Akiyoshi Sannai. Prover Agent: An agent-based
  framework for formal mathematical proofs, 2025.
Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin,
  Xing Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei Shen, Wenlei Shi, Tong Sun, He Sun,
  Jiahui Wang, Siran Wang, Zhihong Wang, Chenrui Wei, Shufa Wei, Yonghui Wu, Yuchen Wu,
  Yihang Xia, Huajian Xin, Fan Yang, Huaiyuan Ying, Hongyi Yuan, Zheng Yuan, Tianyang Zhan,


                                                  13
  Chi Zhang, Yue Zhang, Ge Zhang, Tianyun Zhao, Jianqiu Zhao, Yichi Zhou, and Thomas Hanwen
  Zhu. Seed-Prover: Deep and broad reasoning for automated theorem proving, 2025.
Michelene T. H. Chi, Paul J. Feltovich, and Robert Glaser. Categorization and representation of
 physics problems by experts and novices. Cognitive Science, 5(2):121–152, 1981. doi: 10.1207/
 s15516709cog0502 2.
Jui-Hui Chung, Ziyang Cai, Zihao Li, Qishuo Yin, Rohit Agarwal, Simon Park, Rodrigo Porto,
  Narutatsu Ri, Ziran Yang, Shange Tang, Xingyu Dang, Hongzhou Lin, Mengdi Wang, Danqi
  Chen, Chi Jin, Liam H. Fowl, and Sanjeev Arora. Goedel-Architect: Streamlining formal theorem
  proving with blueprint generation and refinement, 2026.
Kexin Ding, Yang Zhou, Can Jin, Feng Tong, Mu Zhou, and Dimitris N. Metaxas. Agent skill
  evaluation and evolution: Frameworks and benchmarks, 2026.
Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W. Ayers, and Stanislas Polu. Proof artifact
  co-training for theorem proving with language models. In International Conference on Learning
  Representations, 2022.
Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz
  Odrzyg’o’zd’z, Piotr Miło’s, Yuhuai Wu, and Mateja Jamnik. Thor: Wielding hammers to in-
  tegrate language models and automated theorem provers. In Advances in Neural Information
  Processing Systems, volume 35, 2022.
Günther Knoblich, Stellan Ohlsson, Hilde Haider, and Detlef Rhenius. Constraint relaxation and
  chunk decomposition in insight problem solving. Journal of Experimental Psychology: Learning,
  Memory, and Cognition, 25(6):1534–1555, 1999. doi: 10.1037/0278-7393.25.6.1534.
Guillaume Lample, Timoth’ee Lacroix, Marie-Anne Lachaux, Aur’elien Rodriguez, Amaury Hayat,
  Thibaut Lavril, Gabriel Ebner, and Xavier Martinet. HyperTree proof search for neural theorem
  proving. In Advances in Neural Information Processing Systems, volume 35, pp. 26337–26349.
  Curran Associates, Inc., 2022.
Haohan Lin, Zhiqing Sun, Yiming Yang, and Sean Welleck. Lean-STaR: Learning to interleave
  thinking and proving, 2024.
Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
  Xia, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover: A frontier model for open-source
  automated theorem proving, 2025a.
Yong Lin, Shange Tang, Bohan Lyu, Ziran Yang, Jui-Hui Chung, Haoyu Zhao, Lai Jiang, Yihan
  Geng, Jiawei Ge, Jingruo Sun, Jiayun Wu, Jiri Gesi, Ximing Lu, David Acuna, Kaiyu Yang,
  Hongzhou Lin, Yejin Choi, Danqi Chen, Sanjeev Arora, and Chi Jin. Goedel-Prover-V2: Scaling
  formal theorem proving with scaffolded data synthesis and self-correction, 2025b.
Xingyan Liu, Xiyue Luo, Linyu Li, Ganghong Huang, Jianfeng Liu, and Honglin Qiao. SkillForge:
  Forging domain-specific, self-evolving agent skills in cloud technical support. In Proceedings
  of the 49th International ACM SIGIR Conference on Research and Development in Information
  Retrieval, pp. 4763–4768. Association for Computing Machinery, 2026.
Jingwei Ni, Yihao Liu, Xinpeng Liu, Yutao Sun, Mengyu Zhou, Pengyu Cheng, Dexin Wang, Er-
   chao Zhao, Xiaoxi Jiang, and Guanjun Jiang. Trace2Skill: Distill trajectory-local lessons into
   transferable agent skills, 2026.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving,
  2020.
Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor Babuschkin, and Ilya
  Sutskever. Formal mathematics statement curriculum learning. In International Conference on
  Learning Representations, 2023.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang,
   Zhe Fu, Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yux-
   uan Liu, Wenjun Gao, Daya Guo, and Chong Ruan. DeepSeek-Prover-V2: Advancing formal
   mathematical reasoning via reinforcement learning for subgoal decomposition, 2025.
Peiyang Song, Kaiyu Yang, and Anima Anandkumar. Lean Copilot: Large language models as
  copilots for theorem proving in Lean, 2024.


                                               14
Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri. An in-
 context learning agent for formal theorem-proving. In Conference on Language Modeling, 2024.
Haiming Wang, Huajian Xin, Chuanyang Zheng, Zhengying Liu, Qingxing Cao, Yinya Huang, Jing
  Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and Xiaodan Liang. LEGO-Prover: Neural the-
  orem proving with growing libraries. In International Conference on Learning Representations,
  2024.
Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood
  Sung, Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxc’e, Bolton Bailey,
  Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang, Frederick Pu, Han Zhu, Jiawei Liu,
  Jonas Bayer, Julien Michel, Longhui Yu, L’eo Dreyfus-Schmidt, Lewis Tunstall, Luigi Pagani,
  Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer, Wen-Ding
  Li, Yazhe Niu, Yann Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying
  Liu, and Jia Li. Kimina-Prover Preview: Towards large formal reasoning models with reinforce-
  ment learning, 2025.
Zijian Wu, Suozhi Huang, Zhejian Zhou, Huaiyuan Ying, Jiayu Wang, Dahua Lin, and Kai Chen.
  InternLM2.5-StepProver: Advancing automated theorem proving via expert iteration on large-
  scale LEAN problems, 2024.
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li,
  and Xiaodan Liang. DeepSeek-Prover: Advancing theorem proving in LLMs through large-scale
  synthetic data, 2024a.
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao, Wanjia Zhao, Haocheng Wang, Bo Liu,
  Liyue Zhang, Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, Dejian Yang, Zhibin Gou, Z. F.
  Wu, Fuli Luo, and Chong Ruan. DeepSeek-Prover-V1.5: Harnessing proof assistant feedback for
  reinforcement learning and monte-carlo tree search, 2024b.
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan J. Prenger, and Animashree Anandkumar. LeanDojo: Theorem proving with retrieval-
  augmented language models. In Advances in Neural Information Processing Systems, volume 36,
  pp. 21573–21612. Curran Associates, Inc., 2023.
Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei
  Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, and Chong Luo.
  SkillOpt: Executive strategy for self-evolving agent skills, 2026a.
Yutao Yang, Junsong Li, Qianjun Pan, Bihao Zhan, Yuxuan Cai, Lin Du, Jie Zhou, Kai Chen, Qin
  Chen, Xin Li, Bo Zhang, and Liang He. AutoSkill: Experience-driven lifelong learning via skill
  self-evolution, 2026b.
Zhouliang Yu, Ruotian Peng, Keyi Ding, Yizhe Li, Zhongyuan Peng, Minghao Liu, Yifan Zhang,
  Zheng Yuan, Huajian Xin, Wenhao Huang, Yandong Wen, Ge Zhang, and Weiyang Liu. Formal-
  MATH: Benchmarking formal mathematical reasoning of large language models, 2025.
Hanrong Zhang, Shicheng Fan, Henry Peng Zou, Yankai Chen, Zhenting Wang, Jiayu Zhou,
  Chengze Li, Wei-Chieh Huang, Yifei Yao, Kening Zheng, Xue Liu, Xiaoxiao Li, and Philip S.
  Yu. CoEvoSkills: Self-evolving agent skills via co-evolutionary verification, 2026.
Huichi Zhou, Siyuan Guo, Anjie Liu, Zhongwei Yu, Ziqin Gong, Bowen Zhao, Zhixun Chen, Men-
  glong Zhang, Yihang Chen, Jinsong Li, Runyu Yang, Qiangbin Liu, Xinlei Yu, Jianmin Zhou,
  Na Wang, Chunyang Sun, and Jun Wang. Memento-Skills: Let agents design agents, 2026a.
Yang Zhou, Zihan Dong, Zhenting Wang, Can Jin, Shiyu Zhao, Bangwei Guo, Difei Gu, Linjun
  Zhang, Mu Zhou, and Dimitris N. Metaxas. Evidence over plans: Online trajectory verification
  for skill distillation, 2026b.




                                              15
