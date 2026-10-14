                                         ATA: A Neuro-Symbolic Approach to Implement
                                         Autonomous and Trustworthy Agents

                                         David Peer                                                                                    david.peer@otera.ai
                                         Otera
                                         Austria

                                         Sebastian Stabinger                                                                   sebastian.stabinger@otera.ai
                                         Otera
                                         Austria
arXiv:2510.16381v1 [cs.CL] 18 Oct 2025




                                                                                              Abstract

                                                   Large Language Models (LLMs) have demonstrated impressive capabilities, yet their deploy-
                                                   ment in high-stakes domains is hindered by inherent limitations in trustworthiness, including
                                                   hallucinations, instability, and a lack of transparency. To address these challenges, we in-
                                                   troduce a generic neuro-symbolic approach, which we call Autonomous Trustworthy Agents
                                                   (ATA). The core of our approach lies in decoupling tasks into two distinct phases: Offline
                                                   knowledge ingestion and online task processing. During knowledge ingestion, an LLM trans-
                                                   lates an informal problem specification into a formal, symbolic knowledge base. This formal
                                                   representation is crucial as it can be verified and refined by human experts, ensuring its cor-
                                                   rectness and alignment with domain requirements. In the subsequent task processing phase,
                                                   each incoming input is encoded into the same formal language. A symbolic decision engine
                                                   then utilizes this encoded input in conjunction with the formal knowledge base to derive a
                                                   reliable result. Through an extensive evaluation on a complex reasoning task, we demon-
                                                   strate that a concrete implementation of ATA is competitive with state-of-the-art end-to-end
                                                   reasoning models in a fully automated setup while maintaining trustworthiness. Crucially,
                                                   with a human-verified and corrected knowledge base, our approach significantly outperforms
                                                   even larger models, while exhibiting perfect determinism, enhanced stability against input
                                                   perturbations, and inherent immunity to prompt injection attacks. By generating decisions
                                                   grounded in symbolic reasoning, ATA offers a practical and controllable architecture for
                                                   building the next generation of transparent, auditable, and reliable autonomous agents.


                                         1    Introduction

                                         Large language models (LLMs) have demonstrated impressive capabilities across a wide spectrum of natural
                                         language processing tasks, ranging from question answering, text summarization, and machine translation
                                         to complex applications utilizing multi-agent implementations (Comanici et al., 2025; Jiang et al., 2024).
                                         They not only achieve high performance, but also allow for control via natural language prompts, making
                                         them accessible to non-experts. This ease of interaction opens up a wide range of applications and use-cases
                                         in various industries, particularly as it empowers non-computer scientists to effectively use and control these
                                         systems. Nevertheless, especially in high-stakes industries such as insurance, healthcare, finance, and law, it
                                         is crucial that the decisions made by autonomous agents are not only accurate but also trustworthy. Kowald
                                         et al. (2024) defines six important requirements for trustworthy AI: (R1) accuracy and stability, (R2) human
                                         agency and oversight, (R3) transparency and explainability, (R4) privacy and security, (R5) accountability,
                                         and (R6) fairness and non-discrimination. While LLMs have demonstrated impressive performance, enabling
                                         a wide range of new applications, we argue that current systems do not yet fully satisfy these trustworthy
                                         AI requirements:
                                             Note: This text was corrected and improved with Gemini 2.5 Pro
Autonomous Trustworthy Agents - White Paper




     Figure 1: An overview of the proposed approach called Autonomous Trustworthy Agents (ATA).


While initial prompting of LLMs appears simple, achieving the very high accuracy required in high-stakes
applications demands advanced prompt-engineering expertise and skills, as noted by Vu & Oppenlaender
(2025) (R2). This difficulty is compounded by the fact that LLMs are known to hallucinate and exhibit
instability, even in purportedly deterministic setups (Guan et al., 2025; Kalai et al., 2025) (R1). Moreover,
changes to the prompt can negatively affect performance on other parts of the sample distribution, compli-
cating proper control and necessitating a robust benchmarking and testing framework (R1, R2). It is known
that reasoning LLMs contain invalid reasoning steps or hallucinated conclusions which negatively impacts
the transparency and explainability of those models (R3) (Bilal et al., 2025; Lu et al., 2025). Furthermore,
LLMs are known to be vulnerable to prompt injection attacks (Liu et al., 2024b) and since LLM providers
typically do not offer on-premise execution, ensuring on-premise data privacy for users is often impossible
(R4). Finally, LLMs exhibit biases (R6), an issue that remains an open research topic (Resnik, 2025).
Several frameworks and approaches have been presented in the past to adress certain limitations of LLMs.
For example Yao et al. (2022) presented ReAct to combine reasoning and acting in an interleaved manner
in order to improve reasoning of LLMs and to make them even more generic. Instead, we introduce an
approach to address the aforementioned limitations of trustworthiness, named Autonomous Trustworthy
Agents (ATA), that combines the strengths of LLMs with the advantages of symbolic methods. Instead of
querying a LLM with a single, large prompt, the task is split into two distinct building blocks: Knowledge
ingestion and task processing (Figure 1). The first block, knowledge ingestion, is responsible for translating
an informal problem specification into a formal, symbolic knowledge base. The second block, task processing,
evaluates an incoming natural language input in order to derive a reliable result w.r.t this formal knowledge
base.
Knowledge ingestion makes use of the impressive coding capabilities of LLMs (Jiang et al., 2024) to convert
an informal problem specification into a formal language. This formal representation can be an imperative
programming language, such as Python or C++, but also a declarative one, such as Prolog or first-order
logic. A key benefit is that the resulting formal representation can be verified and corrected by human
experts ensuring that the natural language representation matches the formal representation. This oversight
allows for the removal of hallucinations and the correction of misunderstandings that can easily arise from
specifications given in natural language. The task processing step processes an unstructured, natural language
input at runtime, in order to produce a desired result that complies with the knowledge base. To achieve this,
the informal input is first encoded into a formal representation that complies with the knowledge base. This
step is typically a fairly well understood NLP task such as text classification, named entity recognition, or
relation extraction. Subsequently, a deterministic decision engine evaluates the formal representation of the
input with respect to the formalized knowledge base. The usage of a symbolic (rather than neural) decision


                                                      2
Autonomous Trustworthy Agents - White Paper




Figure 2: A graphical illustration of the claims processing task. A policyholder has signed or agreed to
certain T&Cs from a policy provider. The task is to decide if a certain claim is covered by the contract or
not.


engine not only guarantees stability through deterministic executions, but also avoids prompt injection
attacks. Additionally, a human-in-the-loop process can be triggered to review certain queries or results based
on specific conditions. While ATA is a generic approach that can improve the trustworthiness significantly
as shown later in this paper, it is not applicable for every task and not always straightforward to implement.
To demonstrate the applicability and advantages of this general approach, we also present a concrete ATA
implementation for autonomous claims processing. In this use case, a policyholder files a claim under a
contract governed by a certain terms and conditions (T&Cs) policy. The T&C document represents the
informal specification while the claim is the input that needs to be processed. An autonomous agent then
determines, on behalf of the policy provider, whether the claim is covered by the contract. An illustration
for claims processing is given in Figure 2. This task is really challenging, as it requires a deep understanding
of the T&Cs and the claim itself, as well as the ability to reason about the relationship between these two
documents: Policies are formulated in natural language, defining rules that must be fulfilled for a claim to
be covered and rules that exclude certain claims from coverage. Those rules are split over multiple sections
and many pages of text. The task is therefore not only to understand a certain claim, but also to find the
relevant rules in the T&Cs and to reason about them. Rules are not only logically complex involving multiple
conditions that must be satisfied, but also words used in the T&Cs are often redefined within the context
of the contract. For example, contracts might define what constitutes a relative of a policyholder. Although
T&Cs are written in natural language, they are typically of high quality and consistency. In contrast,
claims are typically written by policyholders who lack legal expertise and may be under emotional stress
due to their circumstances. This often results in claims that contain inconsistencies, missing information,
or spelling errors. Consequently, implementing a robust human-in-the-loop process is essential for successful
system deployment—one that can detect and handle edge cases or trigger manual review when specific
conditions are met.
ATA is a valuable pattern to implement autonomous trustworthy agents for claims processing: A transpiler
converts natural language T&Cs into a declarative formal language, namely, many-sorted first-order logic.
First-order logic is quite readable and therefore easy to verify and correct by human experts while still being
a formal language that can be processed by automatic theorem provers. During task processing, the input
encoder axiomizes each claim into the same formal language such that the decision engine, an automatic
theorem prover, can formally prove the validity of the claim w.r.t. the T&C. A graphical illustration and
implementation of the pattern is given in Figure 3. While we use large reasoning models (gemini-2.5-pro
with thinking) for the knowledge ingestion process, we demonstrate in section 4 that AT Agents that utilize
small LLMs (gemini-2.5-flash without thinking) during task processing are very stable, with zero variance
in the results, while outperforming LLMs with built-in reasoning. This can be explained by the fact that


                                                       3
Autonomous Trustworthy Agents - White Paper




axiomization requires the LLM only for named entity recognition and relation extraction, tasks that LLMs
without reasoning capabilities can solve very well. We also demonstrate that the controllability of the
proposed system allows users to easily fix issues locally, ensuring no negative global effects on other cases.
Therefore, the performance can be significantly increased in a controlled manner, outperforming even the
larger gemini-2.5-pro reasoning model by more than 10 percentage points, while being much more token-
efficient and faster in terms of latency. As a positive side-effect, we show that AT Agents are not longer
vulnerable to prompt injection attacks, a desired property for agents that should operate autonomously.
The paper is structured as follows: In the next section 2 we discuss related work. In section 3 we show
how to implement AT Agents for claims processing. In section 4 we present an extensive evaluation of this
approach and finally conclude in section 5.

2   Related Work

LLMs and Informal Reasoning Large Language Models (LLMs) have already demonstrated impressive
capabilities across a wide range of tasks. Subsequent work by Wei et al. (2022); Yao et al. (2023), among
others, revealed that step-by-step thinking processes can significantly enhance these results. This insight
has spurred the development of several advanced reasoning models, such as those presented by Comanici
et al. (2025); Dubey et al. (2024); Rastogi et al. (2025); Guo et al. (2025). A survey on reinforced LLM
reasoning is given by Xu et al. (2025). These models improve performance by increasing the computational
budget at test-time. Shojaee et al. (2025) demonstrated, however, that reasoning is not universally beneficial,
identifying the existence of several distinct complexity regimes. Their analysis distinguishes between low-,
medium-, and high-complexity regimes, finding that reasoning provides the most significant advantage in
the medium-complexity region.

LLMs and Formal Reasoning Benchmarks and a systematic evaluation of LLMs on logic tasks are
provided by Lin et al. (2025). Their findings offer critical insights into the scalability of LLM reasoning with
respect to logical problems of increasing complexity. One solution might be the combination of symbolic
and neural methods, often referred to as neurosymbolic artificial intelligence. A comprehensive survey on
neurosymbolic AI is provided by Renkhoff et al. (2024). We particularly emphasize the integration of LLMs
with formal reasoning methods to construct trustworthy systems. The concept of combining LLMs with
formal methods such as propositional logic, Satisfiability Modulo Theories (SMT), and Boolean Satisfiability
(SAT) solvers is a novel topic of interest. For instance, Hao et al. (2024) introduced a planning framework
that combines an LLM with an SMT solver to solve multi-constraint planning problems. Liu et al. (2024a)
employed LLMs to translate problems into propositional logic expressions, which can then be verified using
automated theorem provers like Prover9 (McCune, 2005–2010). Similarly, Olausson et al. (2023) utilized
first-order logic solvers to address logical reasoning challenges. In their approach, the LLM functions as a
parser, translating natural language into first-order logic to derive provably correct conclusions. Perhaps the
most closely related work is that of Ganguly et al. (2024) on proof reasoning. They introduced a framework
and an interpreter to convert natural language statements (online) into formal logic, incorporating an error-
correction loop for instances where a proof attempt fails. The output of a successful proof is subsequently
cross-referenced with classical natural language reasoning to ensure a consistent conclusion or to trigger a
human-in-the-loop intervention upon failure. In a subsequent publication, they demonstrated a method for
estimating the confidence of a generated formal system (Ganguly et al., 2025).

LLMs and Formal Reasoning for Trustworthy AI Comprehensive studies on trustworthy LLMs have
been conducted by Liu et al. (2023), with specific examinations in high-stakes domains such as healthcare
provided by Aljohani et al. (2025). These studies conclude that most existing solutions are narrowly scoped
and lack cross-dimensional integration, which limits their effectiveness in real-world settings with respect
to the requirements for trustworthy AI outlined by Kowald et al. (2024). A common limitation of the
aforementioned methods that combine LLMs with formal methods is their reliance on online formalization,
where the LLM formalizes each new problem instance at runtime before it is passed to a theorem prover.
This approach is susceptible to issues such as model hallucination or the introduction of tautologies during
formalization, which can lead to erroneous conclusions. In contrast, we propose a substantially different


                                                       4
Autonomous Trustworthy Agents - White Paper




Figure 3: Concrete implementation of ATA for claims processing with knowledge ingestion and task process-
ing: The T&C formalization is done only once per T&C optionally with human expert corrections, while the
claim axiomization is done fully autonomously for each claim. The final decision is made by an automatic
theorem prover that checks the validity of the claim w.r.t. the T&C. The overview also shows how human
experts can (1) correct the T&C formalization and (2) review certain claims if certain conditions are met.


framework for trustworthiness that decouples the formalization of the knowledge base (in our case T&Cs)
from the axiomization of a specific claim. The knowledge base formalization is performed only once for
each T&C document, with an optional step for human expert corrections in order to fix errors or to remove
hallucinations. Conversely, the axiomization of a given claim is performed fully autonomously for each new
instance. This separation renders the system more controllable, stable, and trustworthy, as the foundational
knowledge base is static and verified before any claims are processed against it.

3   AT Agents for Claims Processing

This section demonstrates how AT Agents can be implemented for claims processing. In a typical claims
processing workflow, a policyholder submits a natural language claim detailing an event for which they seek
coverage. This claim must then be evaluated against the governing terms and conditions (T&C) to determine
its validity, as illustrated in Figure 2.
Within our proposed ATA framework, the T&C document is first formalized into many-sorted first-order
logic by a T&C formalizer (transpiler). This one-time formalization step can optionally include verification
and correction by human experts. When a new claim is submitted, it is axiomized into the same formal
language to create a set of facts representing the claim (input encoding). An automatic theorem prover
(decision engine) then evaluates these facts in conjunction with the formalized T&C to determine coverage.
This approach ensures that decisions are not only accurate but also transparent and explainable, as each
decision corresponds to a proof that can be traced through the underlying axioms and formulas. Figure 3
provides an overview of this implementation.
Before the method is presented in detail, we introduce the necessary terminology and concepts from many-
sorted first-order logic and satisfiability modulo theories (SMT).




                                                     5
Autonomous Trustworthy Agents - White Paper




3.1     Preliminaries

We follow the notation and definitions from Jovanović & Barrett (2011) for many-sorted first-order logic,
but interpret a Σ-theory T as a set of sentences rather than a class of structures.

Syntax A signature Σ = (S, F , P) is a triple consisting of a set of sorts S, a set of function symbols F,
and a set of predicate symbols P. Each function and predicate symbol is associated with an arity, which is a
tuple of sorts from S. Functions with an arity of a single sort are called constants. We write CONSTANT:Sort
to denote that the constant is of a certain sort. We assume the standard notions of Σ-terms, Σ-atoms, and
Σ-formulas. A Σ-literal is an atom or its negation. A variable is free in a formula if it is not bound by a
quantifier. A sentence is a formula without free variables. We denote the set of variables of sort σ occurring
in a formula ϕ as varsσ (ϕ), and the set of all variables as vars(ϕ).

Semantics A Σ-interpretation A over a set of variables X and signature Σ is a map that interprets: Each
sort σ ∈ S as a non-empty domain Aσ , each variable x ∈ X of sort σ as an element xA ∈ Aσ , each function
symbol f ∈ F of arity σ1 × · · · × σn → τ as a function f A : Aσ1 × · · · × Aσn → Aτ , and each predicate
symbol p ∈ P of arity σ1 × · · · × σn as a subset pA of Aσ1 × · · · × Aσn . The interpretation of terms and
the truth-value of formulas are defined inductively based on their structure. For a term t, we denote its
evaluation under A as tA . For a formula ϕ, we denote its truth-value (true or false) as ϕA . A Σ-formula
ϕ is satisfiable if it evaluates to true in some Σ-interpretation over at least the variables in vars(ϕ). If an
interpretation A satisfies ϕ, we write A |= ϕ.

Theory A Σ-theory T is a set of Σ-sentences. An interpretation A is a model of T , written A |= T , if it
satisfies every sentence in T . A formula ϕ is T -satisfiable, denoted as A |=T ϕ or simply A |= ϕ if T is clear,
if there exists a model of T that also satisfies ϕ. A formula ϕ is T -valid if it is satisfied by all models of T .

3.2     Method

The AT Agents implementation proposed in this section for claims processing defines a Σ-signature and a
Σ-theory T for a certain T&C and checks the T -validity of a claim to decide if it is covered or not. This
involves the following concrete implementations for the abstract AT components presented in Figure 1:

        1. T&C Formalization (Transpiler): The formalization of T&Cs establishes the initial signature ΣF =∅ =
           (S, ∅, P) and the theory T . This foundational work is an offline process, performed only once per
           T&C document, optionally allowing for human verification and corrections.
        2. Claim Axiomization (Input Encoder): The second step is the axiomization of a claim, which extends
           the signature Σ = (S, F, P) with new constants F. All facts and relations between constants F
           w.r.t P are formally represented in ϕ.
        3. Automated Theorem Proving (Decision Engine): Finally, the T -validity for a goal ψ and claim ϕ is
           checked with an automatic theorem prover to decide if the claim is covered or not. The theorem
           prover additionally returns a minimal set of axioms and sentences that were proof-relevant or a
           counter example. Therefore, decisions are not only formally verified but also explainable and a
           human review can be triggered in case certain conditions (e.g. a certain predicate was used) are
           met.

The following subsections describe all steps in more detail.

3.2.1     T&C Formalization (Transpiler) - Definition of ΣF =∅ and Theory T

Σ-sorts S The first component of the signature ΣF =∅ is the set of sorts S. Each sort represents a fun-
damental class-of-interest relevant to the T&C domain. For instance, in a travel T&C, determining if an
individual is covered necessitates a sort Person. For a car insurance T&C, both the insured object and the
parties involved must be tracked, requiring both a Car sort and a Person sort.


                                                        6
Autonomous Trustworthy Agents - White Paper




Σ-predicates P       Predicates P are partitioned into two distinct types: conditions and goals (P = PC ∪ PG ).

        1. Conditions (PC ): These predicates formalize the criteria that must be satisfied for a claim to
           be covered. For example, a T&C rule might depend on a relative being sick. This requires the
           predicate is_sick of type Person and is_relative of type Person × Person. A crucial aspect
           of T&C formalization is the redefinition of common terms. For instance, a contract may explicitly
           exclude cousins from the definition of a relative. To account for this, each condition predicate
           is defined by its symbolic name and its precise natural language definition, which is essential for
           accurate axiomization.
        2. Goals (PG ): These predicates are used to determine the final outcome of the claim. The primary
           goal is represented by is_covered. Depending on the T&C, additional goal predicates may be
           necessary. For instance, in travel insurance, it might be essential to distinguish between coverage
           for trip cancellations and coverage for medical emergencies. In such cases, separate goal predicates
           like is_covered_cancellation and is_covered_medical would be defined.

Σ-theory T With the signature Σ established, the next step is to define the Σ-theory T . This theory
comprises a set of Σ-sentences that logically encode the complex rules, conditions, and implicit properties
(such as predicate symmetries or transitive relations) found within the T&Cs. Every rule or condition in
the natural language T&Cs is systematically translated into one or more Σ-sentences using the previously
defined sorts and predicates. The core structure for these formalizations is always the following universally
quantified implication:

                                         ∀x1 , . . . , xn .(C1 ∨ · · · ∨ Ck ) → G

Here, x1 , . . . , xn are variables corresponding to sorts s1 , . . . , sn ∈ S. The antecedent is a disjunction of
clauses C1 , . . . , Ck , where each clause is a conjunction of literals utilizing condition predicates P ∈ PC . The
consequent, or goal G, is a literal with predicate PG ∈ PG .
The T&C formalization, as described above, can be performed fully automatically using LLMs (in this work,
we use gemini-2.5-pro). Nevertheless, without human expert verification or corrections, the formalization
might contain errors or hallucinations. In the experimental section 4, we compare the performance of a fully
automated T&C formalization with a human expert-verified formalization to assess the impact of potential
errors in the formalization process leading to possible future work as well.

3.2.2     Claim Axiomization (Input Encoder) - Definition of Σ, ϕ

Given a certain claim text and a formalized T&C (ΣF =∅ , T ), the next step is to axiomize the claim by
extending the signature ΣF =∅ with F to Σ = (S, F, P) and to define a set of facts or axioms ϕ that represent
the claim.

Σ-functions F First, the text is checked against each sort s ∈ S. Whenever an entity of sort s can be
identified in the claim, a corresponding Σ-constant is defined and added to F . For example, in a travel claim
"Alice is the sister of Bob" with S = {P erson} we define the constants ALICE:Person and BOB:Person. This
process is known as Named Entity Recognition (NER) in the NLP community. Note that NER is executed
for each sort individually in order to reduce the impact of changes i.e. if a sort is changed, added or removed,
there is provably no impact on any other sort.

Claim Axioms ϕ Next, we define all facts ϕ that represent the natural language claim in a formal way.
The Vaxiomization ϕ of a claim is a conjunction of each fact ϕi that can be found in the claim such that
       m
ϕ = i=1 ϕi . An axiom ϕi is a literal with predicate P ∈ P and terms t1 , . . . , tn of sorts s1 , . . . , sn where
ti ∈ F. For example, the claim "Alice is the sister of Bob" is axiomized as is_sister(ALICE, BOB). This
task is known as Relation Extraction (RE) in the NLP community. Similar to the entity recognition step,
relation extraction is executed for each predicate individually in order to reduce the impact of changes, and
to improve the stability of the proposed approach.


                                                            7
Autonomous Trustworthy Agents - White Paper




Note: For both, NER as well as RE we exploit the gemini-2.5-flash model without reasoning as we found
that small models without reasoning are sufficient for this task.

3.2.3    Automated Theorem Proving (Decision Engine) - Check T -validity

Finally, we can prove the validity of a specific claim regarding its coverage by checking the T -validity of
ϕ w.r.t a certain goal ψ. All goal predicates are specified in PG during the T&C formalization. For each
predicate P ∈ PG , we can define a goal ψ of the form P (t1 , . . . , tn ) where t1 , . . . , tn are constants in F of
sorts s1 , . . . , sn respectively. Most SMT solvers check for satisfiability. Therefore, to check the T -validity
of a goal we need to check the T -unsatisfiability of the negated goal instead. E.g. to prove that Alice is
covered, we need to check the T -unsatisfiability of ψ = ¬is_covered(ALICE). Then we can decide if the
claim is covered or not as follows: If ψ ∧ ϕ is T -unsat then the claim is covered. If ψ ∧ ϕ is T -sat then the
claim is not covered and the model A |=T ψ ∧ ϕ is a counter example.
Solvers such as z3 (De Moura & Bjørner, 2008) can not only find a counter-example in case of T -satisfiability,
but in case of T -validity also return a so-called unsat core, which is a minimal subset of the axioms as well
as sentences in T that are sufficient to prove the T -validity of ψ ∧ ϕ. Therefore, we can not only provide an
answer if a claim is covered or not, but explain which constants, predicates and sentences in T were used
to prove the validity. This information also enables us to trigger human review when critical predicates or
rules are involved in the proof. For example, if the proof depends on a predicate indicating that a person
was seriously injured, a human expert could review the case before rendering a final decision.
Finally, its worth mentioning that the satisfiability problem for first-order logic is undecidable. But since all
functions in F are of arity 0, the Herbrand universe of Σ is finite. Therefore, checking the T -satisfiability of
ψ ∧ ϕ is decidable and the automatic theorem prover will always terminate with a result.

4     Evaluation
To validate the trustworthiness of AT Agents, we evaluate our system against the key properties of trust-
worthy AI as defined by Kowald et al. (2024). Depending on the nature of each property, we conduct either
quantitative or qualitative evaluations.

4.1     Setup

Model: First of all, we selected a standard setup to compare reasoning of LLMs with the proposed AT
Agents. We use gemini-2.5-flash as our default model for its cost-effectiveness, speed, and strong perfor-
mance on our task. Whenever we evaluate different models, we explicitly mention it. We used the official
09/2025 deployments for gemini and version gpt-5-2025-08-07 as well as gpt-4.1-2025-04-14 for evaluating the
gpt models. In Figure 4, we evaluate the effect of the reasoning budget on the accuracy of claims processing.
This analysis is motivated by Shojaee et al. (2025), who demonstrated that reasoning can counterintuitively
have a negative effect on performance in certain scenarios. It can be concluded that reasoning is beneficial
for claims processing. gemini-2.5-flash additionally offers a dynamic reasoning budget that automatically
adjusts the reasoning budget based on the complexity of the task. We found that this dynamic budget not
only matches the performance of the best fixed budget but also does not require any hyperparameter tuning.
Therefore, we use it as a default in all experiments.
The proposed AT Agent for claims processing uses gemini-2.5-flash without thinking for input encoding
(NER for defining constants F and RE for defining ψ ∧ϕ) to be able to compare our neuro-symbolic approach
with the baseline. The transpiler (T&C formalization) utilizes gemini-2.5-pro with a dynamic reasoning
budget as it requires more advanced models to formalize complex T&C rules (Lin et al., 2025).

Data: To evaluate our approach on claims processing and demonstrate its generalizability, we utilized
three datasets from distinct insurance domains: travel (130 claims), electronics (240 claims), and dental
(230 claims). Each dataset includes the T&C document, ranging from 20 to 50 pages in length, along with
the unstructured text of the insurance claims and its ground-truth. Due to data privacy constraints, these
datasets are not publicly available at the time of writing.


                                                          8
Autonomous Trustworthy Agents - White Paper




                                                    Effect of Thinking Budget on Accuracy

                                               70




                                Accuracy (%)
                                               60




                                               50
                                                                          Budget Limit
                                                                         Dynamic budget

                                                            103                104
                                                          Thinking Budget (tokens)

Figure 4: The effect of the thinking budget on the accuracy and standard deviation evaluated on the travel in-
surance dataset from 0 to its maximum of 25k tokens. The blue line shows the accuracy of gemini-2.5-flash
with reasoning and a fixed thinking budget. The red line shows the accuracy of gemini-2.5-flash with
reasoning and a dynamic thinking budget.

                         Table 1: Accuracy comparison across insurance domains.


              Model                                            Travel          Electronic      Dental
              gemini-2.5-flash                              50.98 ± 0.55       60.67 ± 0.0    76.09 ± 0.0
              gemini-2.5-flash + reasoning                  65.88 ± 1.18       73.13 ± 1.9   91.5 ± 0.35
              ATA                                           72.94 ± 0.0       74.00 ± 0.0     88.64 ± 0.0



4.2   (R1) Accuracy & Stability

Accuracy: First we compare the accuracy of the AT Agents against the baseline LLM. More precisely, we
compare our neuro-symbolic approach with built-in end-to-end reasoning capabilities of LLMs.
Table 1 shows the accuracy comparison between ATA and the gemini-2.5-flash baseline, evaluated with
and without its reasoning capabilities, across the three insurance domains. The results lead to several key
observations: First, enabling reasoning for the baseline LLM yields a substantial performance increase of
15–20 percentage points on all datasets. This not only confirms the benefit of reasoning for this task, but
also underscores the inherent complexity of determining claim coverage with respect to a given T&C docu-
ment. Next, ATA achieves the highest accuracy on two of the three datasets and demonstrates competitive
performance on the third. We wish to emphasize that our objective is not merely to outperform end-to-end
reasoning LLMs in terms of accuracy, but rather to remain competitive while providing additional properties
such as transparency, explainability, and stability, which are explored in the following subsections. A key
advantage of our approach is its inherent controllability. This feature allows a human expert to inspect and
correct the automatic T&C formalization, a process that, as demonstrated in a later section, can signifi-
cantly improve the final accuracy. To maintain a fair comparison with the baseline LLM—an end-to-end
system that offers no intermediate checkpoints for human intervention—we evaluate the impact of human
corrections separately in subsequent experiments.

Stability We evaluate ATA’s robustness by assessing three distinct types of stability. First, intrinsic
stability measures the determinism of the system. To test this, we set the LLM’s temperature parameter to
zero and process the identical input multiple times, expecting consistent outputs. Second, extrinsic stability
assesses the system’s robustness to minor, semantically neutral perturbations of the input; i.e. the approach
should yield the same outcome for paraphrased inputs that do not alter the underlying meaning. Finally,


                                                                 9
Autonomous Trustworthy Agents - White Paper




Table 2: The stability of the system with respect to changing the underlying LLM. Whenever possible we
disabled reasoning for ATA. The superscript 1 indicates that model reasoning is not available or was disabled,
while the superscript 2 indicates that the model has a dynamic thinking budget.


              Model                      ATA          ATA + Human Corr.                LLM
              gemini-2.5-flash           72.941                 87.171                 65.882
              gemini-2.5-pro             70.592                 83.532                 76.502
              gpt-4.1                    70.241                 80.251                 63.531
              gpt-5                      70.592                 84.712                 68.752
              Average               71.09 ± 1.07            83.92 ± 2.49           68.66 ± 4.89



LLM stability evaluates the performance consistency when the underlying language model is substituted
with a different one, thereby testing the modularity and generalizability of our approach.
The results for intrinsic stability are shown via the standard deviation in Table 1. The end-to-end reasoning
model exhibits some instability, as its complex, multi-step generation process can introduce stochasticity even
at zero temperatures, as shown by (Atil et al., 2024). Conversely, while disabling reasoning for the baseline
model increases stability, this comes at the cost of a significant drop in accuracy. In contrast, our ATA is
perfectly deterministic with competitive performance. ATA does not need built-in LLM reasoning during
task processing as it confines the LLM’s role to NER and RE tasks, which are sufficiently straightforward for
the model to produce consistent results while the neuro-symbolic approach ensures a competitive accuracy
as well. This determinism is a highly desirable property, as it allows the impact of any changes to the system
to be assessed reliably.
To measure extrinsic stability, we generated three distinct, semantically equivalent paraphrases for each
claim in the travel dataset using gemini-2.5-pro. We then evaluated the performance variation across
these paraphrased inputs for both the reasoning baseline (gemini-2.5-flash) and ATA. The standard
deviation of the accuracy metric for the baseline increased from 1.18 to 1.47 (+0.29), whereas for ATA it
increased only marginally from 0.0 to 0.15 (+0.15). These results demonstrate that while both systems
exhibit relative robustness to input phrasing, ATA is substantially more stable when faced with semantically
equivalent variations in claim wording.
Finally, we evaluated LLM stability by substituting the gemini-2.5-flash backbone with several alter-
natives: gemini-2.5-pro, gpt-4.1, and gpt-5. As shown in Table 2, the performance of ATA remained
highly stable, with a standard deviation of just 1.07 across the different models. In contrast, the end-to-
end reasoning approach was substantially less stable, exhibiting a standard deviation of 4.89. This result
demonstrates that our proposed approach is more robust to changes in the underlying LLM, highlighting
its forward-compatibility with future models. The same experiment also demonstrates that even with hu-
man corrections to the T&C formalization (detailed in the next section), ATA maintains high stability with
a standard deviation of 2.49, compared to 4.89 for the end-to-end reasoning LLM, while simultaneously
achieving significantly higher accuracy. Details for human corrections are explained in the next section.

4.3   (R2) Human Agency & Oversight

Kowald et al. (2024) identify human agency and oversight as fundamental requirements for trustworthy AI.
Human agency ensures that users retain control over the AI system’s actions, while human oversight (human-
in-the-loop) provides the mechanisms for intervention and monitoring throughout the decision-making pro-
cess. ATA is explicitly designed to support both principles.

Human Agency The design of ATA allows for human corrections directly after the transpilation step.
This is a critical juncture where expert knowledge can be applied to verify and refine the formal representation
of the specification before they are used in an automated setup. By enabling experts to review and adjust



                                                      10
Autonomous Trustworthy Agents - White Paper




Table 3: We categorized errors and manually fixed those by comparing the natural language rule with the
formalization.


                             Model                                   Accuracy
                             ATA without human correction               72.94
                                Added missing clauses                    + 4.71
                                Added missing predicates                 + 4.82
                                Redefined ambigious predicates           + 4.70
                             ATA with human corrections                87.17



the formalization, we ensure that the system’s foundational understanding of the rules aligns with human
interpretations and expectations.
We demonstrate this controllability through an experiment where we manually corrected the automatically
generated T&C formalization. More precisely, we compared each natural language rule with its formaliza-
tion and identified discrepancies without using any examples from our dataset. Our analysis of the initial
formalization revealed three primary error categories: (1) missing clauses from the original T&C, (2) missing
logical predicates required to represent a clause, and (3) ambiguous or imprecise predicate definitions.
While the autoformalization component could undoubtedly be improved, our objective here is not to perfect
this specific module. Instead, we aim to showcase the significant value of the human refinement that our
architecture enables. By manually correcting the identified formalization errors, we can quantify the per-
formance improvement directly attributable to human agency. Although this correction was performed by
the authors and serves as a proof-of-concept, the experiment highlights ATA’s potential to leverage expert
knowledge for enhancing both reliability and accuracy.
As detailed in Table 3, these targeted manual corrections of errors 1-3 led to a significant performance
improvement on the travel dataset. As demonstrated, each category of correction contributed to a measurable
increase in accuracy. This indicates that rules are independent of one another, allowing each to be corrected
in isolation—a desirable property that is absent in classical prompting approaches where changes to one rule
may unpredictably affect the interpretation of others. The accuracy rose from 72.94% to 87.17%, a substantial
increase of 14.23 percentage points. The table also provides a breakdown of this improvement, isolating the
impact of correcting each category of formalization error. Crucially, after these human corrections, the ATA
approach, which utilizes the efficient gemini-2.5-flash without reasoning for task processing, surpasses the
performance of even the most advanced end-to-end reasoning LLMs, such as gpt-5 and gemini-2.5-pro,
by a significant margin as shown in Table 2.

Human Oversight ATA is also designed to facilitate robust human oversight through a system of config-
urable, rule-based triggers. These triggers can activate human-in-the-loop workflows under specific, prede-
fined conditions (e.g. an invalid claim) to situations where the reasoning process invokes certain high-stakes
rules or critical predicates. E.g. a human can be triggered whenever the predicate is_seriously_injured
is proof relevant.
This mechanism enables fine-grained control over when to involve a human expert, ensuring that their
attention is directed exclusively toward the most ambiguous, critical, or sensitive decisions. Crucially, when
an expert is involved, the system’s inherent transparency and explainability provide the full reasoning chain
that led to their involvement. This allows the expert to quickly understand the context, make an informed
decision, and permit the formal system to proceed to a consistent and verifiable final judgment as shown in
the next section.




                                                     11
Autonomous Trustworthy Agents - White Paper




4.4   (R3) Transparency & Explainability

Transparency Transparency in ATA is achieved through the formal representation of knowledge. Each
rule in the T&C is explicitly defined as a formal sentence within the theory T , and each fact in a claim is
represented as a formal axiom in ϕ. This explicit formalization ensures that every component of the system’s
knowledge base is accessible and interpretable by human experts.

Explainability The explanation generated by ATA depends on the outcome of a formal proof attempt for
a given goal. For any such goal, there are two primary outcomes: it can be proven valid, or it can be found
to be invalid (i.e. a counter example exists).
Given a goal is valid, a minimal unsat core can be extracted. This core contains all the axioms and rules that
are required to derive that a goal is valid. This core highlights the precise set of T&C rules and claim-specific
facts that logically entail the goal. This allows an expert to efficiently trace and verify the deductive steps
that led to the conclusion. Additionally, each axiom and rule can be linked into its origin in order to provide
full traceability as well.
Conversely, when a goal is invalid, the prover can be used to generate counterexamples. For example, if the
goal is_covered is invalid, the resulting counterexample would depict a scenario consistent with all rules
where the claim is not covered, thus clearly explaining the proof’s failure. Standard provers such as Z3
(De Moura & Bjørner, 2008) natively support both, returning a minimal unsat core in case of validity and
generating a model in case of invalidity.

4.5   (R4) Privacy & Security

Privacy The processing of sensitive information, such as insurance claims, demands stringent data privacy
measures. The highest level of privacy is achieved when data is processed on-premise or even on-device,
never leaving the owner’s device. This operational constraint, however, often precludes reliance on large,
cloud-based AI models and necessitates architectures that can deliver high performance using smaller, more
efficient alternatives. To assess our approach’s suitability for such privacy-critical and resource-constrained
environments, we evaluated its performance using the most lightweight gemini-2.5-flash-lite model.
Remarkably, even with this lightweight backbone, the human-corrected ATA system achieved an accuracy
of 76.19%, a result that is on-par with the performance of the much larger, state-of-the-art gemini-2.5-pro
end-to-end model (76.50%). Results are quite behind the human-corrected ATA with gemini-2.5-flash
(87.17%), but we believe that a fine-tuned gemini-2.5-flash-lite model on NER and RE could close this
gap further and enable high performance in secure, on-premise or on-device settings. These experiment are
left for future work.

Security A significant security advantage of our approach is its inherent immunity to prompt injection
attacks. This is a direct consequence of the system’s architecture, which, as illustrated in Figure 3, com-
pletely decouples natural language processing from the final decision-making logic. The output is generated
exclusively by a formal prover that operates on structured inputs, meaning there is no natural-language
bridge from the user input to the final output that could be exploited.
The only components in the ATA approach that utilize an LLM online are for input encoding (NER and
RE). However, the attack surface here is strictly limited, as (1) the output of this components is constrained
to a predefined schema of predicates and sorts and (2) the output of the prover is always boolean (valid /
invalid). Consequently, even if an attacker were able to manipulate the LLM’s output, they could at worst
alter the factual data fed to the prover. They would be unable to introduce new logical rules, modify the
reasoning process itself, or inject arbitrary instructions, ensuring the integrity of the formal evaluation.

4.6   (R5) Accountability

As defined by Kowald et al. (2024), accountability involves the obligation to justify one’s conduct to an
authority. While establishing a complete accountability framework is a broad challenge that involves or-


                                                       12
Autonomous Trustworthy Agents - White Paper




ganizational policies and legal compliance, technical systems must provide the necessary foundations. Our
approach contributes to this by ensuring that every decision is accompanied by a verifiable, formal proof.
The high degree of transparency and explainability, derived from the unsat core or a counterexample, cre-
ates a clear audit trail. This trail allows human stakeholders to scrutinize the system’s reasoning, which
is a prerequisite for assigning responsibility. Although our work provides these technical enablers, the im-
plementation of formal accountability processes remains an organizational matter beyond the scope of this
paper.

4.7   (R6) Fairness & Non-discrimination

It is well-established that AI systems can reflect and amplify existing societal biases, potentially leading to
discriminatory outcomes for vulnerable groups (Resnik, 2025). In our approach, this risk is still present at the
axiomization step, where an LLM is used to perform NER and RE on unstructured claim data. Therefore,
we want to clearly state and warn that this important challenge is not solved through the usage of our ATA
approach.

5     Conclusion

In this paper, we introduced Autonomous Trustworthy Agents (ATA), a generic neuro-symbolic approach
designed to address the inherent limitations of Large Language Models (LLMs) in high-stakes domains,
such as their susceptibility to hallucinations, instability, and lack of transparency. Our approach decouples
task execution into two distinct phases: An offline knowledge ingestion step, where an LLM translates an
informal specification into a formal, human-verifiable knowledge base, and an online task processing step,
where incoming queries are handled by a deterministic symbolic decision engine. By combining the natural
language understanding capabilities of LLMs with the rigor and reliability of formal methods, ATA offers a
practical and controllable architecture for building the next generation of transparent, auditable, and reliable
autonomous agents.
Our extensive evaluation on the complex reasoning task of autonomous claims processing demonstrates
that ATA implementations are competitive with state-of-the-art end-to-end reasoning models in a fully
automated setup. Crucially, we showed that by leveraging human agency to verify and correct the formalized
knowledge base, our approach significantly outperforms even larger models. The resulting system exhibits
perfect determinism, enhanced stability against input perturbations, and inherent immunity to prompt
injection attacks. Furthermore, by grounding decisions in symbolic reasoning, ATA provides a transparent
and auditable architecture where every conclusion is accompanied by a formal proof or a counterexample,
enabling robust explainability and human oversight. While our approach mitigates many security and
stability risks, we acknowledge that the potential for bias during the natural language understanding steps
of claim axiomization remains an open challenge.

References
Manar Aljohani, Jun Hou, Sindhura Kommu, and Xuan Wang. A comprehensive survey on the trustworthi-
 ness of large language models in healthcare. arXiv preprint arXiv:2502.15871, 2025.

Berk Atil, Sarp Aykent, Alexa Chittams, Lisheng Fu, Rebecca J Passonneau, Evan Radcliffe, Guru Rajan
  Rajagopal, Adam Sloan, Tomasz Tudrej, Ferhan Ture, et al. Non-determinism of" deterministic" llm
  settings. arXiv preprint arXiv:2408.04667, 2024.
Ahsan Bilal, David Ebert, and Beiyu Lin. Llms for explainable ai: A comprehensive survey. arXiv preprint
 arXiv:2504.00125, 2025.

Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon,
 Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5: Pushing the frontier with ad-
 vanced reasoning, multimodality, long context, and next generation agentic capabilities. arXiv preprint
 arXiv:2507.06261, 2025.


                                                      13
Autonomous Trustworthy Agents - White Paper




Leonardo De Moura and Nikolaj Bjørner. Z3: an efficient smt solver. TACAS’08/ETAPS’08, pp. 337–340,
  Berlin, Heidelberg, 2008. Springer-Verlag. ISBN 3540787992.
Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman,
 Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. arXiv e-prints,
 pp. arXiv–2407, 2024.
Debargha Ganguly, Srinivasan Iyengar, Vipin Chaudhary, and Shivkumar Kalyanaraman. PROOF OF
  THOUGHT : Neurosymbolic program synthesis allows robust and interpretable reasoning. In The First
  Workshop on System-2 Reasoning at Scale, NeurIPS’24, 2024. URL https://openreview.net/forum?
  id=Pxx3r14j3U.
Debargha Ganguly, Vikash Singh, Sreehari Sankar, Biyao Zhang, Xuecen Zhang, Srinivasan Iyengar, Xiaotian
  Han, Amit Sharma, Shivkumar Kalyanaraman, and Vipin Chaudhary. Grammars of formal uncertainty:
  When to trust llms in automated reasoning tasks. arXiv preprint arXiv:2505.20047, 2025.
Bryan Guan, Tanya Roosta, Peyman Passban, and Mehdi Rezagholizadeh. The order effect: Investigating
  prompt sensitivity to input order in llms. arXiv preprint arXiv:2502.04134, 2025.
Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma,
  Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement
  learning. arXiv preprint arXiv:2501.12948, 2025.
Yilun Hao, Yongchao Chen, Yang Zhang, and Chuchu Fan. Large language models can solve real-world
  planning rigorously with formal verification tools. arXiv preprint arXiv:2404.11891, 2024.
Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. A survey on large language models
  for code generation. arXiv preprint arXiv:2406.00515, 2024.
Dejan Jovanović and Clark Barrett. Sharing is caring: Combination of theories. In International Symposium
  on Frontiers of Combining Systems, pp. 195–210. Springer, 2011.
Adam Tauman Kalai, Ofir Nachum, Santosh S Vempala, and Edwin Zhang. Why language models halluci-
  nate. arXiv preprint arXiv:2509.04664, 2025.
Dominik Kowald, Sebastian Scher, Viktoria Pammer-Schindler, Peter Müllner, Kerstin Waxnegger, Lea
 Demelius, Angela Fessl, Maximilian Toller, Inti Gabriel Mendoza Estrada, Ilija Šimić, et al. Establishing
 and evaluating trustworthy ai: overview and research challenges. Frontiers in Big Data, 7:1467222, 2024.
Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter Clark, and
  Yejin Choi. Zebralogic: On the scaling limits of LLMs for logical reasoning. In Forty-second International
  Conference on Machine Learning, 2025. URL https://openreview.net/forum?id=sTAJ9QyA6l.
Tongxuan Liu, Wenjiang Xu, Weizhe Huang, Yuting Zeng, Jiaxing Wang, Xingyu Wang, Hailong Yang, and
  Jing Li. Logic-of-thought: Injecting logic into contexts for full reasoning in large language models. arXiv
  preprint arXiv:2409.17539, 2024a.

Xiaogeng Liu, Zhiyuan Yu, Yizhe Zhang, Ning Zhang, and Chaowei Xiao. Automatic and universal prompt
  injection attacks against large language models. arXiv preprint arXiv:2403.04957, 2024b.
Yang Liu, Yuanshun Yao, Jean-Francois Ton, Xiaoying Zhang, Ruocheng Guo, Hao Cheng, Yegor Klochkov,
  Muhammad Faaiz Taufiq, and Hang Li. Trustworthy llms: a survey and guideline for evaluating large
  language models’ alignment. arXiv preprint arXiv:2308.05374, 2023.

Jiahao Lu, Ziwei Xu, and Mohan Kankanhalli. Reasoning llms are wandering solution explorers. arXiv
  preprint arXiv:2505.20296, 2025.
W. McCune. Prover9 and mace4. http://www.cs.unm.edu/~mccune/prover9/, 2005–2010.




                                                     14
Autonomous Trustworthy Agents - White Paper




Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang, Armando Solar-Lezama, Joshua Tenenbaum, and
  Roger Levy. LINC: A neurosymbolic approach for logical reasoning by combining language models with
  first-order logic provers. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), Proceedings of the 2023
  Conference on Empirical Methods in Natural Language Processing, pp. 5153–5176, Singapore, December
  2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.emnlp-main.313. URL https:
  //aclanthology.org/2023.emnlp-main.313/.

Abhinav Rastogi, Albert Q Jiang, Andy Lo, Gabrielle Berrada, Guillaume Lample, Jason Rute, Joep Bar-
 mentlo, Karmesh Yadav, Kartik Khandelwal, Khyathi Raghavi Chandu, et al. Magistral. arXiv preprint
 arXiv:2506.10910, 2025.
Justus Renkhoff, Ke Feng, Marc Meier-Doernberg, Alvaro Velasquez, and Houbing Herbert Song. A sur-
  vey on verification and validation, testing and evaluations of neurosymbolic artificial intelligence. IEEE
  Transactions on Artificial Intelligence, 5(8):3765–3779, 2024.
Philip Resnik. Large language models are biased because they are large language models. Computational
  Linguistics, pp. 1–21, 2025.
Parshin Shojaee, Iman Mirzadeh, Keivan Alizadeh, Maxwell Horton, Samy Bengio, and Mehrdad Farajtabar.
  The illusion of thinking: Understanding the strengths and limitations of reasoning models via the lens of
  problem complexity. arXiv preprint arXiv:2506.06941, 2025.
An Vu and Jonas Oppenlaender. Prompt engineer: Analyzing skill requirements in the ai job market. arXiv
 preprint arXiv:2506.00058, 2025.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information
  processing systems, 35:24824–24837, 2022.
Fengli Xu, Qianyue Hao, Zefang Zong, Jingwei Wang, Yunke Zhang, Jingyi Wang, Xiaochong Lan, Jiahui
  Gong, Tianjian Ouyang, Fanjin Meng, et al. Towards large reasoning models: A survey of reinforced
  reasoning with large language models. arXiv preprint arXiv:2501.09686, 2025.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. React:
  Synergizing reasoning and acting in language models. In The eleventh international conference on learning
  representations, 2022.
Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan.
  Tree of thoughts: Deliberate problem solving with large language models. Advances in neural information
  processing systems, 36:11809–11822, 2023.




                                                    15
