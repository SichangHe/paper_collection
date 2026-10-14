                                                 N EURO S YMBOLIC R EASONING FOR P LANNING :
                                            C OUNTEREXAMPLE G UIDED I NDUCTIVE S YNTHESIS USING
                                            L ARGE L ANGUAGE M ODELS AND S ATISFIABILITY S OLVING


                                                      Sumit Kumar Jha                        Susmit Jha                         Patrick Lincoln
                                              Computer Science Department            Computer Science Laboratory           Computer Science Laboratory
arXiv:2309.16436v1 [cs.AI] 28 Sep 2023




                                              Florida International University           SRI International                      SRI International
                                                   sumit.jha@fiu.edu                   susmit.jha@sri.com                  patrick.lincoln@sri.com

                                                             Nathaniel D. Bastian                                    Alvaro Velasquez
                                                            Army Cyber Institute                              Department of Computer Science
                                                       United States Military Academy                         University of Colorado Boulder
                                                    nathaniel.bastian@westpoint.edu                         alvaro.velasquez@colorado.edu

                                                                 Rickard Ewetz                                         Sandeep Neema
                                                      Electrical and Computer Engineering                   Electrical and Computer Engineering
                                                          University of Central Florida                             Vanderbilt University
                                                           rickard.ewetz@ucf.edu                            sandeep.neema@vanderbilt.edu




                                                                                            A BSTRACT
                                                 Generative large language models (LLMs) with instruct training such as GPT-4 can follow human-
                                                 provided instruction prompts and generate human-like responses to these prompts. Apart from natural
                                                 language responses, they have also been found to be effective at generating formal artifacts such
                                                 as code, plans, and logical specifications from natural language prompts. Despite their remarkably
                                                 improved accuracy, these models are still known to produce factually incorrect or contextually inap-
                                                 propriate results despite their syntactic coherence – a phenomenon often referred to as hallucinations.
                                                 This limitation makes it difficult to use these models to synthesize formal artifacts that are used
                                                 in safety-critical applications. Unlike tasks such as text summarization and question-answering,
                                                 bugs in code, plan, and other formal artifacts produced by LLMs can be catastrophic. We posit
                                                 that we can use the satisfiability modulo theory (SMT) solvers as deductive reasoning engines to
                                                 analyze the generated solutions from the LLMs, produce counterexamples when the solutions are
                                                 incorrect, and provide that feedback to the LLMs exploiting the dialog capability of instruct-trained
                                                 LLMs. This interaction between inductive LLMs and deductive SMT solvers can iteratively steer
                                                 the LLM to generate the correct response. In our experiments, we use planning over the domain of
                                                 blocks as our synthesis task for evaluating our approach. We use GPT-4, GPT3.5 Turbo, Davinci,
                                                 Curie, Babbage, and Ada as the LLMs and Z3 as the SMT solver. Our method allows the user to
                                                 communicate the planning problem in natural language; even the formulation of queries to SMT
                                                 solvers is automatically generated from natural language. Thus, the proposed technique can enable
                                                 non-expert users to describe their problems in natural language, and the combination of LLMs and
                                                 SMT solvers can produce provably correct solutions.




                                         Keywords Robust Learning · Planning · Program Synthesis · Large Language Model · Decision Procedures ·
                                         Satisfiability Solving
                                     Planning using Neuro Symbolic Reasoning


1   Introduction
Many safety-critical applications such as communication protocols, adaptive software-defined radio, autonomous
vehicles, and assistive robots need to operate in the presence of uncertainty and have the capability to adapt to an
evolving non-stationary environment. This need for generalization and adaptation has fueled the adoption of artificial
intelligence (AI) for such applications. We can categorize these AI components into two categories - inductive learning-
based methods that generalize well but do not provide any guarantees on their output, and deductive automated reasoning
methods that require significant user expertise but provide guarantees on their outputs. Examples of inductive learning
methods include decision trees [Kot13], support vector machines [HDO+ 98], deep learning models [GBC16], the more
recent class of large language models (LLMs), and, more generally, foundation models [BHA+ 21] that generalize
across tasks and domains. Examples of deductive symbolic reasoning methods include propositional satisfiability
(SAT) solvers [BHvM09], satisfiability modulo theory (SMT) solvers [BT18], program synthesizers [JGST10], and
proof assistants [NWP02]. While inductive learning techniques have been typically used for tasks such as perception
requiring decisions over very high-dimensional inputs [JJJJ18], the deductive AI methods have been successfully used
to solve complex tasks such as automated planning, program reverse engineering, code repair, and protocol design. The
remarkable success of LLMs has made it feasible to use them even for these complex tasks, and several recent results
have demonstrated that LLMs can be used for program synthesis and planning [CTJ+ 21, SWW+ 22]. More generally,
the LLMs exhibit limited symbolic reasoning capability making them applicable to problems that traditionally required
symbolic AI reasoning methods such as SAT and SMT solving.
Despite the reasoning capability of LLMs being extremely limited compared to symbolic reasoning methods, they
overcome one key hindrance that has limited the widespread use of formal methods and automated reasoning: the
need for deep expertise in formalizing and specifying problems to these tools. LLMs only require natural language
specification of the problem and have been shown to be capable of automated formalization. Further, the output of
the LLMs can be accompanied with easy to understand natural language explanations. This ease of interaction with
LLMs as reasoning engines can enable non-expert users to pose planning or program synthesis prompts to them and
obtain a solution that is easy to understand. However, LLMs are prone to generating factually incorrect or contextually
inappropriate responses, also referred to as hallucinations [MNBM20, RDG+ 20, CDC22, JLF+ 22, JRE+ 21, KJR+ 22].
The lossy encoding of knowledge in LLMs and the memory distortion that accompanies knowledge generalization
naturally lead to inaccurate retrieval of knowledge even from training data. Thus, simply scaling data and models is not
sufficient to resolve this problem.

2   Related Work
The use of large language models for tasks such as planning and code generation has been an area of active research
in recent years, and numerous techniques have been developed to exploit the capabilities of these models in these
domains. Large language models have been used to generate plans for complex tasks [SWW+ 22, HAPM22] and for
code generation [CTJ+ 21, WWJH21, NPH+ 22]. Several efforts to improve the performance of large language models
in code generation and planning have been recently made through the use of specialized training techniques such
as a combination of contrastive learning and fine-tuning [LWX+ 23], incorporation of external feedback in the form
of success detection and human interaction through internal monologue [HXX+ 22], and decomposition of plans to
sub-plans using LLMs followed by mapping to admissible actions using demonstrations [HAPM22]. Despite these
advancements, several challenges remain in the application of large language models in planning and code generation.
Notably, the model’s ability to handle edge cases, produce consistent outputs, and understand the precise semantics
of the generated code or plan is very limited [VSM+ 23, VOSK22]. The lack of world knowledge and contextual
understanding is another limitation of large language models in planning. These models struggle to consider real-world
constraints and commonsense reasoning in their planning process, which often leads to the generation of unrealistic or
unfeasible plans [Mar20]. Further, the opacity of the decision-making process in large language models is a crucial
limitation for the use of the LLM-produced programs or plans.
In order to address this problem and make the LLM outputs more consistent and robust, and consequently less
prone to errors and hallucinations, fine-tuning has been proposed to adapt to specific tasks or domains [LCK19].
But for many domains, it is not obvious what a sufficient size of the domain-specific dataset needs to be used for
fine-tuning, and continuously monitoring and fine-tuning LLMs is not practical. Failure of fine-tuning to improve LLM
performance has been reported in literature [BIK22]. Further, fine-tuning [WSL+ 22] adversely impacts the model’s
fluency, conversational capability, and in-context learning ability, which is critical to its response to prompts.
Another approach is to connect LLMs to knowledge graphs [WMWG17], which represent knowledge as a graph of
interconnected entities and relationships. Knowledge graphs can encode a wide range of structured and unstructured
knowledge, including facts, concepts, and relationships. Methods have been developed to infuse structured knowledge


                                                           2
                                        Planning using Neuro Symbolic Reasoning


into LLMs by training models on factual triples of knowledge graphs (KGs), and such models pre-trained on knowledge
graphs have been shown to outperform baselines [MDAJ22]. But this requires a well-curated and complete knowledge
base, building which is a time-consuming and expensive endeavor. Maintaining these knowledge bases with consistent
and up-to-date information over time is also challenging.
Yet another possibility is to encode external relevant knowledge into a key-value memory that exploits the fast maximum
inner product search for memory querying. These memory slots can then be integrated with language models [WZH+ 22]
for relatively smaller models, such as T5. Such a memory augmentation has been shown to improve the performance of
the deep learning model on knowledge-intensive tasks. More recently, recurrent memory transformer (RMT) has been
shown to be computationally efficient for large prompts with a million or more tokens [BKB23].
But for tasks such as programming or plan generation, the space of possible queries is very large and can have many
syntactic variations. Some of these simple syntactic variations could be superfluous with respect to the actual task, and
not be relevant to the planning problem. It has been recently shown that LLMs are very sensitive to such irrelevant
variations [JEVJ22]. Hence, improving accuracy via expensive fine-tuning or explicit curation of knowledge graphs
in such a context would be unrealistic as it would require not just creating variations relevant to the domain but also
considering changes irrelevant to the core search problem. We also aim to avoid making significant changes to the deep
learning model’s architecture, such as memory augmentation, which can cause a significant decline in the scalability
and accuracy of these models.
Our approach to generating trustworthy formal artifacts using LLMs is based on formal synthesis [Jha11, JS17, JGST10,
SLTB+ 06]. Formal synthesis generates a program, a plan, or a protocol satisfying a high-level formal specification. In
particular, we use the paradigm of counterexample-guided inductive synthesis [SLTB+ 06] - an instance of oracle-guided
inductive synthesis [JS17], wherein the oracle is a verifier, and the feedback provided to the learning engine is in the
form of counterexamples. These formal approaches to synthesis blend induction and deduction in the sense that even
as they generalize from examples, deductive procedures are used in the process of generalization. Formal inductive
synthesis and machine learning fields have the same high-level goal: to develop algorithmic techniques for synthesizing
a concept from observations. However, there are also important differences in the problem formulations and techniques
used in both fields. First, the concept classes in machine learning tend to use optimization-friendly representations
such as deep neural networks, convex polytopes, or half-spaces. In the case of formal synthesis, the target of learning
includes general programs, protocols, or automata. Secondly, the learning process in formal synthesis often incorporates
combinatorial search methods such as satisfiability solving [BHvM09], and hence, are much less scalable compared to
purely learning techniques. But these approaches provide formal guarantees on the produced artifacts, which is lacking
in learning-based approaches. This paper combines counterexample-guided inductive synthesis with LLMs for the
scalable yet trusted synthesis of plans and programs.


3    Technical Approach

We begin by defining some basic terms and notations motivated by the literature on formal synthesis [JS17]. Following
standard terminology in the machine learning theory community [Ang88], we define a concept c as a set of examples
drawn from a domain of examples E. In other words, c ⊆ E. For example, when learning to produce plans, the E
could be the sequence of all possible state evolutions of the world, and the plan could be the subset of evolutions that
correspond to the correct action sequence. The set of all possible concepts is termed the concept class, denoted by C.
Thus, C ⊆ 2E . Depending on the application domain, E can be finite or infinite. The concept class C can also be finite
or infinite. Note that it is possible to place (syntactic) restrictions on concepts so that C is finite even when E is infinite.
Unlike machine learning, one distinguishing characteristic of our problem formulation is the presence of an explicit
formal specification. This is crucial for an unambiguous definition of correct output.
While the complete specification is infeasible, many domains, such as planning and program synthesis, admit properties
that characterize the target plan or program requirements. Thus, a specification Φ can be thought to represent a set
of “correct” concepts, i.e., Φ ⊆ C ⊆ 2E . Any example x ∈ E such that there is a concept c ∈ Φ where x ∈ c is
called a positive example or witness. Likewise, an example x that is not contained in any c ∈ Φ is a negative example
or counterexample. Given a concept c ∈ C we say that c satisfies Φ iff c ∈ Φ. If we have a complete specification,
it means that Φ is a singleton set comprising only a single allowed concept. In general, Φ is likely to be a partial
specification that allows for multiple correct concepts.
Since we use LLMs for learning, the subsets of examples can be provided as part of the prompts and used for in-context
learning by the LLMs. Using only the witnesses is common in machine learning, but the presence of deductive reasoning
engines and formal verification methods can enable a richer set of inputs, such as counterexamples obtained from
verifying whether the artifact produced from the LLM satisfies the given specification. In general, we can model the
availability of this richer set of inputs that can access the specification Φ as an oracle interface. An oracle interface O


                                                               3
                                       Planning using Neuro Symbolic Reasoning




Figure 1: The technical approach in this paper wraps the generative capability of the large language models in a formal
synthesis loop inspired from counterexample-guided inductive synthesis [SLTB+ 06] and more generally, oracle-guided
inductive synthesis [JS17]. The learning oracle in our approach is the conversation large language model, and the
verification engine serves as the oracle. In particular, we use SMT solvers [DMB08] for verification. The initial query
defines the concept class (plans over a given set of actions), the set of possible behaviors (state space and the evolution
of the environment state), and the specification. The verifier complements this initial query by adding counterexamples
— behaviors of the produced incorrect plans by the LLM that are not consistent with the specification (∼ denotes
symmetric set difference). The final output is the candidate produced by the LLM that is formally verified to be
consistent with the given specification.


is a subset of Q × R where Q is a set of query types, R is a corresponding set of response types, and O defines which
pairs of query and response types are semantically well-formed. A simple instance of an oracle interface is one with a
single query type that returns positive examples from E. Another instance is an oracle that has access to a verification
engine and can return counterexamples. Implementations of the oracle interface can be nondeterministic algorithms
that exhibit nondeterministic choices in the stream of queries and responses. Consider a concept class C, a domain of
examples E, a specification Φ, and an oracle interface O. Our goal is to find a target concept c ∈ C that satisfies Φ,
given only O and C. In other words, E and Φ can be accessed only through O.
We restrict the oracle to be a verifier that can produce counterexamples, and thus, our approach becomes an instance of
counterexample-guided inductive synthesis (CEGIS). It was originally proposed as an algorithmic method for program
synthesis where the specification is given as a reference program and the concept class is defined using a partial program,
also referred to as a “sketch” [SLTB+ 06]. In CEGIS, the learner (synthesizer) interacts with a “verifier" that can take in
a candidate plan or a program and a specification, and try to find a counterexample showing that the candidate program
does not satisfy the specification. In CEGIS, the learner is typically implemented on top of a general-purpose decision
procedure such as a satisfiability solver, satisfiability modulo theory solver, or model checker. The oracle (verifier) is
also implemented similarly. In contrast, we use the LLMs as the learner in our work and a formal verification engine as
the oracle.
Thus, we adopt the CEGIS architecture and locate the LLM as a scalable learner within it. This enables us to scale
synthesis and, at the same time, produce plans or programs that are formally verified against the given specifications.
This proposed approach extends our recent work-in-progress report on improving the trust of LLMs [JJL+ 23], and
exploits the following characteristics of the LLMs and the satisfiability solvers as verification engines. First, the LLMs
can be prompted to generate well-structured outputs that can be easily parsed by a formal verification engine. The
inclusion of a large corpus of code in their training data is perhaps responsible for this characteristic. We successfully
use this to ensure the output of LLMs can be ingested by the verifier. We also use LLMs to derive the queries to the
verifier, automatically checking for the correctness specification. Second, the formal verifiers are very fast at checking
the correctness of a single solution for a task such as planning, as compared to solving the planning problem using
combinatorial search and finding a valid plan. Formal verification techniques can also be used to localize the part of the
solution that violates the specification and to provide informative feedback to the LLMs that rule out not just a single
incorrect solution but a whole class of incorrect solutions. A large body of work on verification, fault isolation, and
explanation generation can be leveraged using this architecture. This would expand the query types and response types
(Q, R) in the formal synthesis framework. Further, LLMs demonstrate remarkable in-context learning, and adding


                                                             4
                                      Planning using Neuro Symbolic Reasoning


counterexamples and explanations to the prompt steers them away from incorrect responses and eventually drives
them to a correct solution that is accepted by the verifier. The context length used to train LLMs has been rapidly
growing. Models such as GPT-4 can take a context length of 32K tokens, while other generative models with 100K
tokens have also been developed. This larger context length enables LLMs to stay consistent with provided prompts.
This increasing context length enables being able to support more number of counterexamples in the prompt. Thus, the
current direction of improvement in LLMs supports more number of iterations of the presented architecture. Finally,
the use of formal methods for tasks such as planning requires tedious modeling into existing solvers and verifiers. The
responses of these formal engines also need to be translated back into more easily interpretable forms to be used by
engineers and developers who are not experts in formal methods. The use of LLM in the above architecture also serves
as a human-friendly front end and, thus, partially alleviates the challenge of making formal synthesis engines more
accessible to non-expert users.
In the rest of the paper, we evaluate the proposed approach using automated planning as the synthesis domain and
using SMT solver [DMB08] as the verification engine. We first describe a case study in detail and then present the
quantitative results.

4   Experiments
We use block-world planning [GN92] traditionally used in the traditional planning literature for our experiments. This
standard benchmark allows us to test scalability and accuracy across different problem sizes and using different LLMs.
We specify the high-level predicates that capture the state of the world, such as BlockOn, OnTable, and Holding,
and their evolution. We describe the permitted operations/actions and the initial state. We provide a final state and ask
the LLM to produce a valid plan. The LLMs take a few iterations with the verifier to produce the correct result. We
consider responses where the verifier appends the incorrect sequences to the prompt only stating that these sequences
are not valid or provides a richer response as a prefix of the invalid plan such that any completion would be incorrect.
This iteration continues till the response of the LLM is verified to be correct.
The final response from the LLM provides a human-readable justification in addition to the final plan. We use one
example of a block-world problem to demonstrate our proposed approach before presenting quantitative results that
compare different LLMs, such as GPT4, GPT3.5 Turbo, Davinci, Curie, Babbage, and Ada, and also consider planning
problems of varying scale.
Illustrative Example We consider the block world planning problem. The natural language specification of the plan in
the BLOCKWORLD problem is also translated into formal (first-order) constraints using the LLM. We provide the
details for that step in the appendix and focus here on the iterative refinement of the prompt to steer LLM toward a
correct response using the formal verifier as the guiding oracle. We provide two examples in our prompt to assist the
LLMs to inductively reason about a new problem and respond with its plan.
One of the two examples is listed below.
    Given the block world problem OLDPROB1:
    (define (problem BW-sample-0)
    (:domain blocksworld-4ops)
    (:objects b1 b2 b3 b4 b5 b6 )

    (:init
    (arm-empty)
    (on b1 b2)
    (on b2 b3)
    (on b3 b4)
    (on b4 b5)
    (on b5 b6)
    (on-table b6)
    (clear b1)
    (clear b2)
    (clear b3)
    (clear b4)
    (clear b5)
    (clear b6)
    )

    (:goal
    (and
    (on b6 b5)
    (on b5 b4)
    (on b4 b3)
    (on b3 b2)
    (on b2 b1)
    (on-table b1)
    )))



                                                           5
                                      Planning using Neuro Symbolic Reasoning


We first list the problem, as shown above, and then a plan for the planning problem.
    The solution for the problem OLDPROB1 is:
    START-PLAN
    1. unstack b1 b2
    2. put-down b1
    3. unstack b2 b3
    4. put-down b2
    5. unstack b3 b4
    6. put-down b3
    7. unstack b4 b5
    8. put-down b4
    9. unstack b5 b6
    10. put-down b5
    11. pick-up b6
    12. stack b6 b5
    13. pick-up b5
    14. stack b5 b4
    15. pick-up b4
    16. stack b4 b3
    17. pick-up b3
    18. stack b3 b2
    19. pick-up b2
    20. stack b2 b1
    END-PLAN


Now, given a new block world problem NEWPROB, the LLM may produce an incorrect response:
    (define (problem BW-rand-6)
    (:domain blocksworld-4ops)
    (:objects b1 b2 b3 b4 b5 b6 )
    (:init
    (arm-empty)
    (on b1 b6)
    (on b2 b3)
    (on-table b3)
    (on b4 b1)
    (on-table b5)
    (on-table b6)
    (clear b2)
    (clear b4)
    (clear b5)
    )
    (:goal
    (and
    (on b1 b2)
    (on b5 b3)
    (on b6 b4))
    )
    )


The incorrect solution from the problem NEWPROB is:
    START-PLAN
    1. unstack b4 b1
    2. put-down b4
    3. unstack b1 b6
    4. put-down b1
    5. pick-up b2
    6. stack b2 b3
    7. pick-up b1
    8. stack b1 b2
    9. pick-up b5
    10. stack b5 b3
    11. pick-up b6
    12. stack b6 b4
    END-PLAN


The SMT solver identifies the following as an infeasible subset of the plan and generates a new prompt including the
statement that “Any plan with the following prefix is not correct”:
    START-PLAN
    1. unstack b4 b1
    2. put-down b4
    3. unstack b1 b6
    4. put-down b1
    5. pick-up b2


Using this information, the LLM produces a new response that is verified to be correct by the decision procedure.


                                                          6
                                                                             Planning using Neuro Symbolic Reasoning



    START-PLAN
    1. unstack b4 b1
    2. put-down b4
    3. unstack b1 b6
    4. put-down b1
    5. unstack b2 b3
    6. put-down b2
    7. pick-up b5
    8. stack b5 b3
    9. pick-up b6
    10. stack b6 b4
    11. pick-up b1
    12. stack b1 b2
    END-PLAN



Quantitative Results We analyze the performance of different GPT on 20 random problems with 3 blocks in Fig. 2.


                                                                 20                              19
                                 Number of Successful Plans




                                                                 15
                                                                                                             12
                                                                 10


                                                                                 5
                                                                                                                          2         2         2
                                                                                                                                                           0
                                                                                 0
                                                                                                                                            e
                                                                                                         -4


                                                                                                          o

                                                                                                          ci

                                                                                                                                rie




                                                                                                                                                       da
                                                                                                                                          ag
                                                                                                        rb

                                                                                                       in
                                                                                                      PT




                                                                                                                                                     A
                                                                                                                              Cu

                                                                                                                                        bb
                                                                                                    Tu

                                                                                                    av
                                                                                                    G




                                                                                                                                    Ba
                                                                                                  D
                                                                                                 .5
                                                                                               -3
                                                                                             PT
                                                                                            G




                   Figure 2: The performance of different GPT models on problems with 3 blocks.

GPT-4 is the most successful model and we analyze its performance with with 3, 4, 5 and 6 blocks. In Fig. 3, we
observe that it is only able to solve 2 out of the 20 problems with 10 blocks even though it could solve 19 out of the
20 problem with 3 blocks. We also study the performance of the second best model, that is, GPT 3.5 with a different
number of blocks, and the results are shown in Fig. 4.


                                                                                            20        19
                                                              Number of Correct Solutions




                                                                                            15
                                                                                                                  11          11
                                                                                            10                                            9


                                                                                             5
                                                                                                                                                       2
                                                                                             0
                                                                                                  ks


                                                                                                                  s


                                                                                                                          ks


                                                                                                                                        ks


                                                                                                                                                     s
                                                                                                             ck




                                                                                                                                                  ck
                                                                                                 oc




                                                                                                                         oc


                                                                                                                                     oc
                                                                                                              o




                                                                                                                                                 o
                                                                                             Bl


                                                                                                           Bl


                                                                                                                       Bl


                                                                                                                                   Bl


                                                                                                                                              Bl
                                                                                            3


                                                                                                       4


                                                                                                                      5


                                                                                                                                6


                                                                                                                                          10




                       Figure 3: The performance of GPT-4 on problems with multiple blocks.



                                                                                                                          7
                                                                                                          Planning using Neuro Symbolic Reasoning



                                                                                                                    12




                                                                       Number of Correct Solutions
                                                                                                      10


                                                                                                                                                                                    6
                                                                                                          5                                   4

                                                                                                                                                                                                         1
                                                                                                          0



                                                                                                                ks



                                                                                                                                         ks



                                                                                                                                                                                   s



                                                                                                                                                                                                      ks
                                                                                                                                                                                k
                                                                                                             oc



                                                                                                                                      oc



                                                                                                                                                                             oc



                                                                                                                                                                                                   oc
                                                                                                           Bl



                                                                                                                                   Bl



                                                                                                                                                                          Bl



                                                                                                                                                                                                Bl
                                                                                                          3



                                                                                                                              4



                                                                                                                                                              5



                                                                                                                                                                                            6
                                                    Figure 4: The performance of GPT-3.5 on problems with multiple blocks.


We study how LLMs are improved by adding verification in the loop and report the number of iterations taken by our
approach to produce the correct result. In Fig. 5, we analyze the number of iterations of counterexamples need by
GPT-4 and GPT-3.5 on 20 random problems involving 3 and 4 blocks.


                       10                                                                                                                                                 10


                       9                                                                                                                                                   9


                       8                                                                                                                                                   8


                       7                                                                                                                                                   7
    Number of Trials




                                                                                                                                                       Number of Trials




                       6                                                                                                                                                   6


                       5                                                                                                                                                   5


                       4                                                                                                                                                   4


                       3                                                                                                                                                   3


                       2                                                                                                                                                   2


                       1                                                                                                                                                   1


                       0                                                                                                                                                   0
                            0

                                1

                                    2

                                        3

                                            4

                                                5

                                                    6

                                                        7

                                                            8

                                                                  9

                                                                       10

                                                                                                     11

                                                                                                          12

                                                                                                               13

                                                                                                                    14

                                                                                                                         15

                                                                                                                              16

                                                                                                                                    17

                                                                                                                                         18

                                                                                                                                              19




                                                                                                                                                                               0

                                                                                                                                                                                   1

                                                                                                                                                                                        2

                                                                                                                                                                                            3

                                                                                                                                                                                                 4

                                                                                                                                                                                                     5

                                                                                                                                                                                                           6

                                                                                                                                                                                                               7

                                                                                                                                                                                                                   8

                                                                                                                                                                                                                         9

                                                                                                                                                                                                                              10

                                                                                                                                                                                                                                   11

                                                                                                                                                                                                                                        12

                                                                                                                                                                                                                                             13

                                                                                                                                                                                                                                                  14

                                                                                                                                                                                                                                                       15

                                                                                                                                                                                                                                                            16

                                                                                                                                                                                                                                                                 17

                                                                                                                                                                                                                                                                      18
                                                            Problem Number                                                                                                                                         Problem Number                                          19



                                                                   GPT-4                                                                                                                                                  GPT-4
                                                                GPT-3.5 Turbo                                                                                                                                          GPT-3.5 Turbo




                                                     Figure 5: Number of iterations required by GPT-4 and GPT-3.5 Turbo.


5                      Conclusions

We present a novel approach to addressing the challenge of the trustworthy generation of formal artifacts such as plans
and programs from LLMs. Our technique uses the paradigm of counterexample-guided inductive synthesis wherein the
learner is implemented using the LLM and the verifier uses SMT solver. Our approach can be viewed as an adversarial
variant [JRF+ 19] of the in-context learning approach, wherein we use formal verification to detect incorrect responses
and include the generated counterexamples as a part of the prompt in the dialog with the LLM. The initial experiments
reported over the planning task in this paper are encouraging and indicate that the proposed combination of LLMs
and formal verifiers can be an effective approach to using LLMs in applications where the generated artifact must be
verified.


                                                                                                                                                   8
                                   Planning using Neuro Symbolic Reasoning


References
[Ang88]      Dana Angluin. Queries and concept learning. Machine learning, 2:319–342, 1988.
[BHA+ 21]    Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, et al. On the opportunities
             and risks of foundation models. arXiv preprint arXiv:2108.07258, 2021.
[BHvM09]     Armin Biere, Marijn Heule, and Hans van Maaren. Handbook of satisfiability, volume 185. IOS press,
             2009.
[BIK22]      Michael Bommarito II and Daniel Martin Katz. GPT takes the bar exam. arXiv preprint arXiv:2212.14402,
             2022.
[BKB23]      Aydar Bulatov, Yuri Kuratov, and Mikhail S Burtsev. Scaling transformer to 1m tokens and beyond with
             rmt. arXiv preprint arXiv:2304.11062, 2023.
[BT18]       Clark Barrett and Cesare Tinelli. Satisfiability modulo theories. Springer, 2018.
[CDC22]      Meng Cao, Yue Dong, and Jackie Chi Kit Cheung. Hallucinated but factual! inspecting the factuality of
             hallucinations in abstractive summarization. In Proceedings of the ACL (Volume 1: Long Papers), 2022.
[CTJ+ 21]    Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan,
             Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large language models
             trained on code. arXiv:2107.03374, 2021.
[DMB08]      Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In TACAS, pages 337–340.
             Springer, 2008.
[GBC16]      Ian Goodfellow, Yoshua Bengio, and Aaron Courville. Deep learning. MIT press, 2016.
[GN92]       Naresh Gupta and Dana S Nau. On the complexity of blocks-world planning. Artificial Intelligence,
             56(2-3):223–254, 1992.
[HAPM22]     Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot
             planners: Extracting actionable knowledge for embodied agents. In International Conference on Machine
             Learning, pages 9118–9147. PMLR, 2022.
[HDO+ 98]    Marti A. Hearst, Susan T Dumais, Edgar Osuna, John Platt, and Bernhard Scholkopf. Support vector
             machines. IEEE Intelligent Systems and their applications, 13(4):18–28, 1998.
[HXX+ 22]    Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan
             Tompson, Igor Mordatch, Yevgen Chebotar, et al. Inner monologue: Embodied reasoning through
             planning with language models. arXiv preprint arXiv:2207.05608, 2022.
[JEVJ22]     Sumit Kumar Jha, Rickard Ewetz, Alvaro Velasquez, and Susmit Jha. Responsible reasoning with large
             language models and the impact of proper nouns. In Workshop on Trustworthy and Socially Responsible
             ML, NeurIPS, 2022.
[JGST10]     Susmit Jha, Sumit Gulwani, Sanjit A Seshia, and Ashish Tiwari. Oracle-guided component-based program
             synthesis. In Proceedings of the 32nd ACM/IEEE International Conference on Software Engineering,
             2010.
[Jha11]      Susmit Kumar Jha. Towards automated system synthesis using sciduction. University of California,
             Berkeley, 2011.
[JJJJ18]     Susmit Jha, Uyeong Jang, Somesh Jha, and Brian Jalaian. Detecting adversarial examples using data
             manifolds. In MILCOM 2018-2018 IEEE Military Communications Conference (MILCOM), pages
             547–552. IEEE, 2018.
[JJL+ 23]    Susmit Jha, Sumit Kumar Jha, Patrick Lincoln, Nathaniel D. Bastian, Alvaro Velasquez, and Sandeep
             Neema. Dehallucinating large language models using formal methods guided iterative prompting. In
             IEEE International Conference on Assured Autonomy, 2023.
[JLF+ 22]    Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Yejin Bang, Andrea
             Madotto, and Pascale Fung. Survey of hallucination in natural language generation. ACM Computing
             Surveys, 2022.
[JRE+ 21]    Sumit Kumar Jha, Arvind Ramanathan, Rickard Ewetz, Alvaro Velasquez, and Susmit Jha. Protein
             folding neural networks are not robust. arXiv preprint arXiv:2109.04460, 2021.
[JRF+ 19]    Susmit Jha, Sunny Raj, Steven Lawrence Fernandes, Sumit Kumar Jha, Somesh Jha, Gunjan Verma,
             Brian Jalaian, and Ananthram Swami. Attribution-driven causal analysis for detection of adversarial
             examples. arXiv preprint arXiv:1903.05821, 2019.


                                                       9
                                    Planning using Neuro Symbolic Reasoning


[JS17]     Susmit Jha and Sanjit A Seshia. A theory of formal synthesis via inductive learning. Acta Informatica,
           54:693–726, 2017.
[KJR+ 22]  Ramneet Kaur, Susmit Jha, Anirban Roy, Sangdon Park, Edgar Dobriban, Oleg Sokolsky, and Insup Lee.
           idecode: In-distribution equivariance for conformal out-of-distribution detection. In Proceedings of the
           AAAI Conference on Artificial Intelligence, volume 36, pages 7104–7114, 2022.
[Kot13]    Sotiris B Kotsiantis. Decision trees: a recent overview. Artificial Intelligence Review, 39:261–283, 2013.
[LCK19]    Cheolhyoung Lee, Kyunghyun Cho, and Wanmo Kang. Mixout: Effective regularization to finetune
           large-scale pretrained language models. arXiv preprint arXiv:1909.11299, 2019.
     +
[LWX 23] Shangqing Liu, Bozhi Wu, Xiaofei Xie, Guozhu Meng, and Yang Liu. Contrabert: Enhancing code
           pre-trained models via contrastive learning. arXiv preprint arXiv:2301.09072, 2023.
[Mar20]    Gary Marcus. The next decade in ai: four steps towards robust artificial intelligence. arXiv preprint
           arXiv:2002.06177, 2020.
[MDAJ22] Fedor Moiseev, Zhe Dong, Enrique Alfonseca, and Martin Jaggi. Skill: Structured knowledge infusion
           for large language models. arXiv preprint arXiv:2205.08184, 2022.
[MNBM20] Joshua Maynez, Shashi Narayan, Bernd Bohnet, and Ryan McDonald. On faithfulness and factuality in
           abstractive summarization. arXiv preprint arXiv:2005.00661, 2020.
     +
[NPH 22] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and
           Caiming Xiong. Codegen: An open large language model for code with multi-turn program synthesis.
           arXiv preprint arXiv:2203.13474, 2022.
[NWP02]    Tobias Nipkow, Markus Wenzel, and Lawrence C Paulson. Isabelle/HOL: a proof assistant for higher-
           order logic. Springer, 2002.
[RDG+ 20] Stephen Roller, Emily Dinan, Naman Goyal, Da Ju, Mary Williamson, Yinhan Liu, Jing Xu, Myle
           Ott, Kurt Shuster, Eric M Smith, et al. Recipes for building an open-domain chatbot. arXiv preprint
           arXiv:2004.13637, 2020.
[SLTB+ 06] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay Saraswat. Combinatorial
           sketching for finite programs. In ASPLOS, 2006.
      +
[SWW 22] Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M Sadler, Wei-Lun Chao, and Yu Su. Llm-
           planner: Few-shot grounded planning for embodied agents with large language models. arXiv preprint
           arXiv:2212.04088, 2022.
[VOSK22] Karthik Valmeekam, Alberto Olmo, Sarath Sreedharan, and Subbarao Kambhampati. Large language
           models still can’t plan (a benchmark for llms on planning and reasoning about change). arXiv:2206.10498,
           2022.
     +
[VSM 23] Karthik Valmeekam, Sarath Sreedharan, Matthew Marquez, Alberto Olmo, and Subbarao Kambhampati.
           On the planning abilities of large language models (a critical investigation with a proposed benchmark).
           arXiv:2302.06706, 2023.
[WMWG17] Quan Wang, Zhendong Mao, Bin Wang, and Li Guo. Knowledge graph embedding: A survey of
           approaches and applications. IEEE Transactions on Knowledge and Data Engineering, 29(12):2724–
           2743, 2017.
     +
[WSL 22] Yihan Wang, Si Si, Daliang Li, Michal Lukasik, Felix Yu, Cho-Jui Hsieh, Inderjit S Dhillon, and Sanjiv
           Kumar. Preserving in-context learning ability in large language model fine-tuning. arXiv preprint
           arXiv:2211.00635, 2022.
[WWJH21] Yue Wang, Weishi Wang, Shafiq Joty, and Steven CH Hoi. Codet5: Identifier-aware unified pre-trained
           encoder-decoder models for code understanding and generation. arXiv preprint arXiv:2109.00859, 2021.
      +
[WZH 22] Yuxiang Wu, Yu Zhao, Baotian Hu, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel.
           An efficient memory-augmented transformer for knowledge-intensive nlp tasks. arXiv preprint
           arXiv:2210.16773, 2022.




                                                        10
                                         Planning using Neuro Symbolic Reasoning


A    Experimental Details
The natural language specification of the plan in the BLOCKWORLD problem is also translated into formal ( first
order ) constraints using the LLM. For this, we specify the key predicates and then use the prompt “Translate the
following into first-order logic using the formatting of Z3 Python API and the following state information:” to enable
the translation and obtain the corresponding Z3 API code that we then deploy in our deductive reasoning engine. The
state information given to the LLM is as follows:
 1   class State:
 2       def __init__(self, name):
 3           self.table = Function(f'{name}_table', IntSort(), BoolSort())
 4           self.hand = Function(f'{name}_hand', IntSort(), BoolSort())
 5           self.stacked = Function(f'{name}_stacked', IntSort(), IntSort(), BoolSort()
                 )
 6           self.clear = Function(f'{name}_clear', IntSort(), BoolSort())
 7           self.handsfree = Function(f'{name}_handsfree', IntSort(), BoolSort())

The informal specification for the Pick-up operation in the planning problem is given by:

          The block must be clear and on the table in state s1. The block must not be in the hand in state s1. The block
          must be in the hand in state s2. The block must not be on the table in state s2 and must not be clear. For all
          other blocks x, the state of the hand, table, and clear should remain the same between s1 and s2. For all blocks
          x, y, the state of the stacked should remain the same between s1 and s2.


The corresponding produced formal constraints by the LLM are:


          # Constraint 1: The block must be clear and on the table in state s1
          constraint1 = And(s1.table(the_block), s1.clear(the_block))
          # Constraint 2: The block must not be in the hand in state s1
          constraint2 = Not(s1.hand(the_block))
          # Constraint 3: The block must be in the hand in state s2
          constraint3 = s2.hand(the_block)
          # Constraint 4: The block must not be on the table in state s2 and must
          ,→  not be clear
          constraint4 = And(Not(s2.table(the_block)), Not(s2.clear(the_block)))
          # Constraint 5: For all other blocks x, the state of the hand, table, and
          ,→  clear should remain the same between s1 and s2
          x = Int('x')
          constraint5 = ForAll([x], And(s1.table(x) == s2.table(x), s1.hand(x) ==
          ,→  s2.hand(x), s1.clear(x) == s2.clear(x)), patterns=[x != the_block])
          # Constraint 6: For all blocks x, y, the state of the stacked should
          ,→  remain the same between s1 and s2
          x = Int('x')
          y = Int('y')
          constraint6 = ForAll([x, y], s1.stacked(x, y) == s2.stacked(x, y))
          # Combine all constraints
          constraints = And(constraint1, constraint2, constraint3, constraint4,
          ,→  constraint5, constraint6)


We query the LLM to translate the following constraint into first order logic for the Put-down operation in the planning
problem:

          The block must not be in the hand in state s2. The block must be on the table in state s2 and must be clear. For
          all other blocks x, the state of the hand, table, and clear should remain the same between s1 and s2. For all
          blocks x, y, the state of the stacked should remain the same between s1 and s2.



                                                                11
                                        Planning using Neuro Symbolic Reasoning


Similarly, we use the following query to the LLM to translate the stack operation into first-order logic:


         In all cases, the following should be true when executing the stack(block1, block2) operation. For all other
         blocks x other than these two blocks, the state of the hand, table, and clear should remain the same between
         the states s1 and s2. For all blocks x, y, where neither x is block1, nor y is block2, the state of being stacked
         should remain the same between s1 and s2.
         There are two cases: either a block is stacked from the table or a block is stacked from the hand.
         If the block1 is being stacked from the table, then the following is true: The block1 must be on the table in
         state s1. Neither block1 nor block2 should be stacked on each other in state s1. Both block1 and block2 must
         be clear, i.e., not having any block on them, in state s1. The agent’s hand should be free in state s1. The block1
         must not be in the agent’s hand nor on the table in state s2. The block1 must be stacked on block2 in state s2.
         The block1 must be clear, while block2 must not be clear in state s2. The agent’s hand should be free in state
         s2.
         If the block1 is being stacked from the hand, then the following is true: The block1 must be in the agent’s hand
         in state s1. Neither block1 nor block2 should be stacked on each other in state s1. The block2 must be clear in
         state s1. The agent’s hand should not be free in state s1. The block1 must not be in the agent’s hand nor on the
         table in state s2. The block1 must be stacked on block2 in state s2. The block1 must be clear, while block2
         must not be clear in state s2. The agent’s hand should be free in state s2.



The LLM produces the following first order logic formula using the flavored syntax of Z3 Python API.



           constraints.append(ForAll(x, Implies(And(x != block1, x != block2),
           ,→  And(s1.hand(x) == s2.hand(x), s1.table(x) == s2.table(x), s1.clear(x) ==
           ,→  s2.clear(x)))))

           constraints.append(ForAll([x, y], Implies(And(x != block1, y != block2),
           ,→  s1.stacked(x, y) == s2.stacked(x, y))))

           constraints.append(Or(
           And(
           # If the block1 is being stacked from the table
           s1.table(block1),      # The block1 is on the table in state s1
           Not(s1.stacked(block1, block2)), # Neither block1 nor block2 are stacked on each
           ,→  other in state s1
           s1.clear(block1),      # Block1 is clear in state s1
           s1.clear(block2),      # Block2 is clear in state s1
           s1.handsfree(),        # The agent's hand is free in state s1
           Not(s2.table(block1)), # Block1 is not on the table in state s2
           Not(s2.hand(block1)),    # Block1 is not in the agent's hand in state s2
           s2.stacked(block1, block2), # Block1 is stacked on block2 in state s2
           s2.clear(block1),      # Block1 is clear in state s2
           Not(s2.clear(block2)), # Block2 is not clear in state s2
           s2.handsfree()         # The agent's hand is free in state s2
           ),
           And(
           # If the block1 is being stacked from the hand
           s1.hand(block1),       # The block1 is in the agent's hand in state s1
           Not(s1.stacked(block1, block2)), # Neither block1 nor block2 are stacked on each
           ,→  other in state s1
           s1.clear(block2),      # Block2 is clear in state s1
           Not(s1.handsfree()), # The agent's hand is not free in state s1
           Not(s2.table(block1)), # Block1 is not on the table in state s2
           Not(s2.hand(block1)),    # Block1 is not in the agent's hand in state s2
           s2.stacked(block1, block2), # Block1 is stacked on block2 in state s2
           s2.clear(block1),      # Block1 is clear in state s2
           Not(s2.clear(block2)), # Block2 is not clear in state s2
           s2.handsfree()         # The agent's hand is free in state s2
           )
           ))



                                                                12
                                                        Planning using Neuro Symbolic Reasoning



           In all cases, the following should be true when executing the unstack(block1, block2) operation. For
           all other blocks x other than these two blocks, the state of the hand, table, and clear should remain
           the same between the states s1 and s2. For all blocks x and y, where neither x is block1, nor y is
           block2, the state of being stacked should stay the same between s1 and s2.
           There are two cases: either a block is unstacked to the table or a block is unstacked to the hand.
           If the block1 is being unstacked from the block2 to the table, then the following must be true: The
           blocks block1 and block2 must be stacked in state s1, with block1 clear and the agent’s hand free. In
           state s2, block1 should not be stacked on block2 but should be on the table. In state 2, both block1
           and block2 should be clear, and the agent’s hand should be free.
           If the block1 is being unstacked from the block2 to the hand, then the following must be true: The
           blocks block1 and block2 must be stacked in state s1, with block1 clear and the agent’s hand free.
           In state s2, block1 should not be stacked on block2 but should be in the agent’s hand. The block2
           should be clear, but block1 should not be clear, and the agent’s hand should not be free.


A.1     Number of iterations with GPT-4 and GPT-3.5

A.1.1    GPT-4 and GPT-3.5 Turbo with 5 blocks

We analyze the number of iterations of computerexamples needed by GPT-4 and GPT-3.5 on 20 random problems with
5 blocks.



                                   10


                                    9


                                    8


                                    7
                Number of Trials




                                    6


                                    5


                                    4


                                    3


                                    2


                                    1


                                    0
                                        0

                                            1

                                                2

                                                    3

                                                         4

                                                             5

                                                                 6

                                                                     7

                                                                         8

                                                                               9

                                                                                    10

                                                                                         11

                                                                                              12

                                                                                                   13

                                                                                                        14

                                                                                                             15

                                                                                                                  16

                                                                                                                       17

                                                                                                                            18

                                                                                                                                 19




                                                                         Problem Number




                                                                                GPT-4
                                                                             GPT-3.5 Turbo

           Figure 6: Number of iterations required by GPT-4 and GPT-3.5 Turbo on problems with 5 blocks.



                                                                             13
                                                      Planning using Neuro Symbolic Reasoning


A.1.2   GPT-4 and GPT-3.5 Turbo with 6 blocks
We analyze the number of iterations of computerexamples needed by GPT-4 and GPT-3.5 on 20 random problems with
6 blocks.



                                 10


                                  9


                                  8


                                  7
              Number of Trials




                                  6


                                  5


                                  4


                                  3


                                  2


                                  1


                                  0
                                      0

                                          1

                                              2

                                                  3

                                                       4

                                                           5

                                                               6

                                                                   7

                                                                       8

                                                                             9

                                                                                  10

                                                                                       11

                                                                                            12

                                                                                                 13

                                                                                                      14

                                                                                                           15

                                                                                                                16

                                                                                                                     17

                                                                                                                          18

                                                                                                                               19
                                                                       Problem Number




                                                                              GPT-4
                                                                           GPT-3.5 Turbo

         Figure 7: Number of iterations required by GPT-4 and GPT-3.5 Turbo on problems with 6 blocks.




                                                                           14
B   Natural Language Constraints to Logic

       1. Pick-up Constraints




    from z3 import *

    # Let's denote our block of interest with the integer '0'
    the_block = 0

    # Create the states
    s1 = State('s1')
    s2 = State('s2')

    # Constraint 1: The block must be clear and on the table in state s1
    constraint1 = And(s1.table(the_block), s1.clear(the_block))

    # Constraint 2: The block must not be in the hand in state s1
    constraint2 = Not(s1.hand(the_block))

    # Constraint 3: The block must be in the hand in state s2
    constraint3 = s2.hand(the_block)

    # Constraint 4: The block must not be on the table in state s2 and must not be clear
    constraint4 = And(Not(s2.table(the_block)), Not(s2.clear(the_block)))
                             Planning using Neuro Symbolic Reasoning




# Constraint 5: For all other blocks x, the state of the hand, table, and clear should remain the
same between s1 and s2
x = Int('x')
constraint5 = ForAll([x], And(s1.table(x) == s2.table(x), s1.hand(x) == s2.hand(x), s1.clear(x) ==
s2.clear(x)), paTerns=[x != the_block])

# Constraint 6: For all blocks x, y, the state of the stacked should remain the same between s1
and s2
x = Int('x')
y = Int('y')
constraint6 = ForAll([x, y], s1.stacked(x, y) == s2.stacked(x, y))

# Combine all constraints
constraints = And(constraint1, constraint2, constraint3, constraint4, constraint5, constraint6)

# Solve
solver = Solver()
solver.add(constraints)
if solver.check() == sat:
   model = solver.model()
   print(model)
else:
   print("No soluZon found")




                                                 16
                      Planning using Neuro Symbolic Reasoning




2. Put-down Constraints




                                        17
                               Planning using Neuro Symbolic Reasoning




from z3 import *

def put_down(s1, s2, block):
  solver = Solver()

  # 1. The block is in the hand in state s1.
  solver.add(s1.hand(block) == True)

  # 2. The block is not on the table in state s1.
  solver.add(s1.table(block) == False)

  # 3. The block is not in the hand in state s2.
  solver.add(s2.hand(block) == False)

  # 4. The block is on the table in state s2.
  solver.add(s2.table(block) == True)

  # 5. The block is clear in state s2.
  solver.add(s2.clear(block) == True)

  # For all other blocks x, the state of the hand, table, and clear should remain the same
between s1 and s2.
  x = Int('x')
  solver.add(ForAll([x], And(x != block, s1.hand(x) == s2.hand(x), s1.table(x) == s2.table(x),
s1.clear(x) == s2.clear(x))))

  # For all blocks x, y, the state of the stacked should remain the same between s1 and s2.
  x = Int('x')
  y = Int('y')
  solver.add(ForAll([x, y], s1.stacked(x, y) == s2.stacked(x, y)))

  # Check the constraints and print the result
  if solver.check() == sat:
     print(solver.model())
  else:
     print("No soluZon found")




                                                    18
                       Planning using Neuro Symbolic Reasoning




3. Stack Constraints




                                         19
Planning using Neuro Symbolic Reasoning




                  20
                              Planning using Neuro Symbolic Reasoning




from z3 import Not, And, Or, ForAll, Implies, IntSort, FuncZon, BoolSort, Int, Solver

class State:
   def __init__(self, name):
     self.table = FuncZon(f'{name}_table', IntSort(), BoolSort())
     self.hand = FuncZon(f'{name}_hand', IntSort(), BoolSort())
     self.stacked = FuncZon(f'{name}_stacked', IntSort(), IntSort(), BoolSort())
     self.clear = FuncZon(f'{name}_clear', IntSort(), BoolSort())
     self.handsfree = FuncZon(f'{name}_handsfree', BoolSort())

def stack(s1, s2, block1, block2):
  x = Int('x')
  y = Int('y')
  constraints = []

  # For all blocks x other than these two blocks, the state of the hand, table, and clear should
remain the same between the states s1 and s2
  constraints.append(ForAll(x, Implies(And(x != block1, x != block2), And(s1.hand(x) ==
s2.hand(x), s1.table(x) == s2.table(x), s1.clear(x) == s2.clear(x)))))

  # For all blocks x, y, where neither x is block1, nor y is block2, the state of being stacked
should remain the same between s1 and s2
  constraints.append(ForAll([x, y], Implies(And(x != block1, y != block2), s1.stacked(x, y) ==
s2.stacked(x, y))))

   # The block is either stacked from the table or from the hand
   constraints.append(Or(
     And(
        # If the block1 is being stacked from the table
        s1.table(block1), # The block1 is on the table in state s1
        Not(s1.stacked(block1, block2)), # Neither block1 nor block2 are stacked on each other
in state s1
        s1.clear(block1), # Block1 is clear in state s1
        s1.clear(block2), # Block2 is clear in state s1
        s1.handsfree(),      # The agent's hand is free in state s1
        Not(s2.table(block1)), # Block1 is not on the table in state s2
        Not(s2.hand(block1)), # Block1 is not in the agent's hand in state s2
        s2.stacked(block1, block2), # Block1 is stacked on block2 in state s2
        s2.clear(block1), # Block1 is clear in state s2
        Not(s2.clear(block2)), # Block2 is not clear in state s2
        s2.handsfree()       # The agent's hand is free in state s2
     ),
     And(
        # If the block1 is being stacked from the hand




                                                 21
                            Planning using Neuro Symbolic Reasoning




        s1.hand(block1), # The block1 is in the agent's hand in state s1
        Not(s1.stacked(block1, block2)), # Neither block1 nor block2 are stacked on each other
in state s1
        s1.clear(block2), # Block2 is clear in state s1
        Not(s1.handsfree()), # The agent's hand is not free in state s1
        Not(s2.table(block1)), # Block1 is not on the table in state s2
        Not(s2.hand(block1)), # Block1 is not in the agent's hand in state s2
        s2.stacked(block1, block2), # Block1 is stacked on block2 in state s2
        s2.clear(block1), # Block1 is clear in state s2
        Not(s2.clear(block2)), # Block2 is not clear in state s2
        s2.handsfree()     # The agent's hand is free in state s2
      )
   ))

  return And(constraints)




                                              22
                         Planning using Neuro Symbolic Reasoning




4. Unstack Constraints




                                           23
Planning using Neuro Symbolic Reasoning




                  24
                              Planning using Neuro Symbolic Reasoning




from z3 import *

def unstack(s1, s2, block1, block2):
  x, y = Ints('x y')
  blocks = [x, y]
  blocks_except = [b for b in blocks if b != block1 and b != block2]

  # Invariants for all blocks
  invariants = And(
     ForAll([x], Implies(x != block1, And(s1.table(x) == s2.table(x), s1.hand(x) == s2.hand(x),
s1.clear(x) == s2.clear(x)))),
     ForAll([x], Implies(x != block2, And(s1.table(x) == s2.table(x), s1.hand(x) == s2.hand(x),
s1.clear(x) == s2.clear(x)))),
     ForAll([x, y], Implies(And(x != block1, y != block2), s1.stacked(x, y) == s2.stacked(x, y))),
  )

  # Block unstacked to the table
  unstack_to_table = And(
    s1.stacked(block1, block2),
    s1.clear(block1),
    s1.handsfree(),
    Not(s2.stacked(block1, block2)),
    s2.table(block1),
    s2.clear(block1),
    s2.clear(block2),
    s2.handsfree()
  )

  # Block unstacked to the hand
  unstack_to_hand = And(
    s1.stacked(block1, block2),
    s1.clear(block1),
    s1.handsfree(),
    Not(s2.stacked(block1, block2)),
    s2.hand(block1),
    Not(s2.clear(block1)),
    s2.clear(block2),
    Not(s2.handsfree())
  )

  return And(invariants, Or(unstack_to_table, unstack_to_hand))




                                                  25
