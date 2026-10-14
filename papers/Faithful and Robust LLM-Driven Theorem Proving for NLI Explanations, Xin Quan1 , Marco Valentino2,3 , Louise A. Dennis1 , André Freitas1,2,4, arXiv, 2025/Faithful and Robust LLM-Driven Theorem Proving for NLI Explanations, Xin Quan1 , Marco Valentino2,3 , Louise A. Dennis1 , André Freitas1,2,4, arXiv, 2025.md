                                         Faithful and Robust LLM-Driven Theorem Proving for NLI Explanations
                                                          Xin Quan1 , Marco Valentino2,3 , Louise A. Dennis1 , André Freitas1,2,4
                                                             1
                                                               Department of Computer Science, University of Manchester, UK
                                                                             2
                                                                               Idiap Research Institute, Switzerland
                                                                 3
                                                                   School of Computer Science, University of Sheffield, UK
                                                          4
                                                            National Biomarker Centre, CRUK-MI, University of Manchester, UK
                                                                           1
                                                                             {name.surname}@manchester.ac.uk
                                                                                  2
                                                                                    {name.surname}@idiap.ch

                                                                   Abstract                                 Marasović, 2021; Chen et al., 2021; Thayaparan
                                                 Natural language explanations play a funda-                et al., 2020; Valentino et al., 2022). Providing
arXiv:2505.24264v1 [cs.CL] 30 May 2025




                                                 mental role in Natural Language Inference                  sound and logically valid natural language expla-
                                                 (NLI) by revealing how premises logically                  nations lies at the core of NLI, as such transparent
                                                 entail hypotheses. Recent work has shown                   justifications enhance both interpretability and reli-
                                                 that the interaction of large language models              ability for downstream tasks (Camburu et al., 2018;
                                                 (LLMs) with theorem provers (TPs) can help                 Valentino et al., 2022; He et al., 2024). Recent
                                                 verify and improve the validity of NLI explana-
                                                                                                            methods, in particular, have leveraged the infer-
                                                 tions. However, TPs require translating natural
                                                 language into machine-verifiable formal repre-             ential and linguistic capabilities of large language
                                                 sentations, a process that introduces the risk of          models (LLMs) by integrating them with external
                                                 semantic information loss and unfaithful inter-            theorem provers (TPs) to automatically verify the
                                                 pretation, an issue compounded by LLMs’ chal-              logical validity of explanations for NLI (Pan et al.,
                                                 lenges in capturing critical logical structures            2023; Olausson et al., 2023; Quan et al., 2024b;
                                                 with sufficient precision. Moreover, LLMs are              Dalal et al., 2024).
                                                 still limited in their capacity for rigorous and
                                                                                                               However, these integrated neuro-symbolic ap-
                                                 robust proof construction within formal verifi-
                                                 cation frameworks. To mitigate issues related              proaches still face notable challenges. First, auto-
                                                 to faithfulness and robustness, this paper in-             mated theorem provers (ATP) require a machine-
                                                 vestigates strategies to (1) alleviate semantic            verifiable formal language, yet LLMs often fail to
                                                 loss during autoformalisation, (2) efficiently             produce precise autoformalisations, underscoring
                                                 identify and correct syntactic errors in logical           their limited capacity to faithfully convert complex
                                                 representations, (3) explicitly use logical ex-            natural language inputs into rigorous formal rep-
                                                 pressions to guide LLMs in generating struc-               resentations (Wu et al., 2022; Jiang et al., 2024;
                                                 tured proof sketches, and (4) increase LLMs’
                                                                                                            Quan et al., 2024b). Second, syntactic errors are
                                                 capacity of interpreting TP’s feedback for it-
                                                 erative refinement. Our empirical results on               frequently introduced during the autoformalisation
                                                 e-SNLI, QASC and WorldTree using different                 process, leading to reduced theorem-proving suc-
                                                 LLMs demonstrate that the proposed strategies              cess rates when dealing with more complex mate-
                                                 yield significant improvements in autoformali-             rial inferences (Pan et al., 2023; Olausson et al.,
                                                 sation (+18.46%, +34.2%, +39.77%) and expla-               2023; Zhang et al., 2024). Third, when provided
                                                 nation refinement (+29.5%, +51.5%, +41.25%)                with external feedback on complex explanations,
                                                 over the state-of-the-art model. Moreover, we
                                                                                                            LLMs often struggle to combine axioms (expla-
                                                 show that specific interventions on the hybrid
                                                 LLM-TP architecture can substantially improve              nations) into cohesive proofs and effectively self-
                                                 efficiency, drastically reducing the number of             correct, limiting their effectiveness in more com-
                                                 iterations required for successful verification.1          plex NLI settings (Quan et al., 2024a,b).
                                                                                                               In this paper, we build upon the state-of-the-
                                         1       Introduction
                                                                                                            art LLM-based theorem proving framework for
                                         Recent studies in Natural Language Inference                       NLI, Explanation-Refiner (Quan et al., 2024b). In
                                         (NLI) have developed models to leverage natu-                      particular, we explore methodologies to improve
                                         ral language explanations as a mechanism for rea-                  the faithfulness of autoformalisation and deliver
                                         soning in support of a hypothesis (Wiegreffe and                   a more robust way to effectively and efficiently
                                             1
                                            Code and data are available at: https://github.com/neuro-       provide logically valid explanations. We further
                                         symbolicai/faithful_and_robust_nli_refinement                      examine how varying degrees of dataset complex-

                                                                                                        1
                                                                                                                                          shows "∃x y. Person x ∧ Alone x ∧ Field y ∧
                                                                                 ∃x. OnePerson(x) ⟷ (Person(x) ∧ Alone(x))
                                                                                                                                          Outdoors y ∧ In x y"
                                                     (2) Quantifier Check                                                                                                                 (3) Consistency Check
                                                         and Refinement                                                                                                                        and Refinement
                                                                                 ∀x. OnePerson(x) ⟷ (Person(x) ∧ Alone(x))                shows False




                                                      Subject: One person                                                                                                                                    Proof Found
                                     (1) Syntactic
                                                      Verb Phrase: is a person alone                           (ii) Autoformalisation                                                                                                Verified
                                                      Main Verb: is                                                                                                 (iii) Theorem Proving                                          Explanation
                                        Parsing
                                                      Subject Complement: a person
                                                                                                              Check and Refinement
                                                      Adverbial Modifier (Manner): alone
                                                                                                                                                                                                      No Proof Found

Premise:                                                                                                                     (4) Propositions Extraction
There is one person lying in a                                                                                                                                          proof -
large, green field.                                                                                                          A: one person (from                          (* From the premise, we have known information about one person,
                                                                                                                             Explanatory Sentence 1)                    lying, agent, field, large, green, and in. *)
Hypothesis:                                                                                                                  B: a person alone (from                      from asm have "OnePerson x ∧ Field y ∧ In x y" by simp
There is a person alone in a field                                                                                           Explanatory Sentence 1)                      (* There is a logical equivalence between one person and a person
outdoors.
                                                         (i) Autoformalisation                                                                                          alone from explanation sentence 1. *)
                                                                                                                                                                          (* Using the equivalence, we can infer that if OnePerson x, then Person
                                                                                                                              (5) Relations Extraction                  x and Alone x. *)
                                                                                                                                                                          then have "Person x ∧ Alone x" using explanation_1 by blast
Initial Explanation:                                                                                                         Equivalent(A, B)                             (* We already have Field y from the premise. *)
One person is a person alone.                                                                                                Equivalent(one person, a                     (* Since the field is large and green, it can be considered outdoors. *)
                                                                                                                             person alone)                                (* Therefore, we can infer Outdoors y. *)
                                                                                                                                                                          then have "Field y ∧ Outdoors y" sledgehammer
                                                                                                                                                                          (* Combining all the inferred information, we have Person x, Alone x,
                                                                                                                              (6) Derive Implications                   Field y, Outdoors y, and In x y. *)
                                                                                                                             Implies(B, A)                                then show ?thesis <ATP>
                                                 New Explanation:                                                                                                        qed
                                                 One person is a person alone.
                                                                                                                             Implies(a person alone, one
                                                                                                                             person)                                    end
                                                 A field can be outdoors, and if a person is in
                                                                                                                             Implies(A, B)
                                                 a field, they can be considered outdoors
                                                                                                                             Implies(one person, a
                                                                                                                             person alone)


                                                                                                                                                                     (6) Extract Failed Proof Step

                                                                                                                                                                                  (* We already have Field y from the premise. *)
                                                                                                                                                                                    (* Since the field is large and green, it can be
                                                                                                                        (iv) Explanation Refinement                               considered outdoors. *)
                                                                                                                                                                                    (* Therefore, we can infer Outdoors y. *)
                                                                                                                                                                                    then have "Field y ∧ Outdoors y" sledgehammer



Figure 1: An illustration of our proposed interventions for improving LLM-driven theorem proving for NLI. The
interventions employ different techniques including syntactic parsing, quantifier refinement, logical consistency
refinement, and logical expression extraction to guide LLMs in generating more faithful and robust proof sketches
for NLI and effectively refine natural language explanations. This approach provides more structured and explicit
feedback by pinpointing the exact logical errors identified in the explanations.


ity in multi-hop reasoning affect the reliability of                                                                          posed framework improves the faithfulness of aut-
proof step generation in LLM-Driven theorem prov-                                                                             oformalisation by 18.46%, 34.2%, 39.77%, respec-
ing. In general, we implement a neuro-symbolic                                                                                tively, compared to Explanation-Refiner. Addition-
framework to address the following research ques-                                                                             ally, the number of refined explanations produced
tions: RQ1: "To what extent can we deliver faithful                                                                           by our framework exceeds that of Explanation-
autoformalisation that preserves semantic infor-                                                                              Refiner across all LLMs: raising refinement rates
mation?" RQ2: "What types of syntactic errors                                                                                 from 41% to 95%, 17% to 90%, and 7% to 73%
commonly appear in formal representations, and                                                                                across all three datasets. To summarise, the main
how effectively can state-of-the-art LLMs refine                                                                              contributions of this paper are:
these errors?" RQ3: "Can state-of-the-art LLMs
generate structured proof steps that can effectively                                                                              1. We introduce Faithful-Refiner, a novel neuro-
provide feedback to refine explanations with com-                                                                                    symbolic framework that provides more ro-
plex sentences and logical relations?"                                                                                               bust and faithful verification and refinement
   To answer these questions, we investigate how                                                                                     of explanations in NLI, surpassing existing
to systematically leverage syntactic parsing during                                                                                  LLM-driven theorem-proving approaches.
autoformalisation to guide LLMs generate logical                                                                                  2. We conduct a quantitative evaluation of ex-
representation of explanations. In addition, we de-                                                                                  planation refinement and autoformalisation
fine the general autoformalisation error types and                                                                                   across different LLMs, achieving an average
use LLMs to refine these errors explicitly from the                                                                                  improvement of 29.5%, 51.5%, and 41.25%
output message of a TP. Furthermore, we propose                                                                                      more refined explanations, as well as 5.06%,
a method to extract the logical propositions, rela-                                                                                  6.86%, and 32.16% on syntactic errors reduc-
tions and implications to guide LLMs to generate                                                                                     tion compared to the state-of-the-art.
proof sketches for automated theorem proving and
explanation refinement.                                                                                                           3. We adopt a range of automatic metrics to mea-
   Our empirical evaluation on e-SNLI (Camburu                                                                                       sure the quality of explanations and autofor-
et al., 2018), QASC (Khot et al., 2019), and                                                                                         malisation, showing that the proposed frame-
WorldTree (Jansen et al., 2018) shows that the pro-                                                                                  work significantly improve the faithfulness of

                                                                                                                        2
       the autoformalisation process.                             premise) and a proof goal (derived from the hypoth-
                                                                  esis). After formalising the input sentences, we
    4. We also perform a manual evaluation to assess              apply a quantifier and a logical consistency check
       the perceived quality of the formalised logical            along with a refinement process.
       forms and conduct an extensive ablation study,
                                                                     Similar to Jiang et al. (2022b) and Quan et al.
       elucidating the role of each proposed compo-
                                                                  (2024b), we adopt Isabelle/HOL (Nipkow et al.,
       nent and identifying key factors influencing
                                                                  2002) to formally verify the constructed the-
       automated theorem proving for NLI.
                                                                  ory. Specifically, we invoke the Sledgehammer
2     Automated Theorem Proving for                               tool (Paulson and Blanchette, 2012) within Is-
      Explanation-Based NLI                                       abelle/HOL to call upon multiple automated the-
                                                                  orem provers (e.g., CVC42 , Vampire3 ), which
In this paper, we define an explanation Ei as a                   attempt to prove the theorem derived from the
set of facts {f1 , f2 , . . . , fn } that establish a logi-       translated NLI tasks. If any prover succeeds, we
cally valid entailment between premises pi and a                  conclude that the explanation is logically sound,
hypothesis hi , such that pi ∪ Ei |= hi holds.                    thereby confirming that the premise entails the hy-
   In this work, we leverage an external theorem                  pothesis.
prover T P to systematically verify these entail-                    If no proof is found, we use an LLM to ex-
ments in an automated manner. Specifically, given                 tract logical propositions and relations from the
the set of input sentences S = pi ∪ {hi } ∪ Ei , we               natural language explanations. We then employ
aim to build a set of logical forms ϕ = {Φ(s) |                   an intermediate propositional representation to de-
s ∈ S}, where Φ is the autoformalisation process                  rive further implications among these propositions,
that converts natural language sentences into sym-                prompting the LLM to generate a step-by-step
bolic representations. From these logical forms,                  proof sketch—rather than having the LLM serve di-
we construct a theory Θ = (A, τ ), where A =                      rectly as a proof planner as in Explanation-Refiner.
{a1 , a2 , . . . , an } is the set of axioms derived from
                                                                     Finally, we iteratively attempt to prove each sub-
formalising Ei , and τ is the theorem to be proven,
                                                                  proof step, gathering information about failed steps,
composed of pi and hi . If an automated theorem
                                                                  using it as feedback to prompt the LLM to generate
prover (AT P ) can derive a valid proof for Θ, we
                                                                  an updated explanation to refine the logical errors
conclude that Ei is sound and logically valid. Oth-
                                                                  identified in the previous proof sketch and start a
erwise, we refine Ei by using the failed proof steps
                                                                  new iteration.
as feedback, iteratively generating a refined expla-
nation Ei′ that ultimately leads to a valid justifica-            3.1     Isabelle/HOL Theory Generation
tion.
                                                                  Autoformalisation plays a critical role in integrat-
3     Methodology                                                 ing theorem provers with LLMs, especially for
                                                                  complex sentence structures. Similar to Quan et al.
To effectively enhance the joint inference capabili-
                                                                  (2024b), we apply Neo-Davidsonian event-based
ties and robustness between LLMs and theorem
                                                                  semantics (Parsons, 1990) to formalising the nat-
provers for explanation-based NLI, we propose
                                                                  ural language sentences within each aspect of an
a novel framework to enhance three key compo-
                                                                  event with distinct predicates. This approach pro-
nents: autoformalisation, logical and syntactic error
                                                                  vides a robust foundation for formalising explana-
checking and refinement, and LLM-guided proof
                                                                  tory sentences while maximising content preserva-
construction. As illustrated in Figure 1, the pipeline
                                                                  tion (Maienborn et al., 2011).
begins with the automated formalisation of natural
                                                                     However, simply using few-shot prompting for
language into logical representations.
                                                                  autoformalisation does not guarantee a faithful pro-
   Unlike the previous state-of-the-art approach
                                                                  cess, which may lead to inconsistencies between
(i.e., Explanation-Refiner), we begin with a syn-
                                                                  the natural and formal languages expressions. To
tactic parsing step that guides LLMs in translating
                                                                  alleviate this, we begin by performing syntactic
natural language elements into a formal specifica-
                                                                  parsing via the LLMs on all provided sentences to
tion compatible with theorem provers. The LLM is
                                                                  extract their grammatical structure, identifying the
prompted to automatically formalise the explana-
tory sentences into axioms and construct a theorem                   2
                                                                         https://cvc4.github.io/
                                                                     3
composed of assumption clauses (drawn from the                           https://vprover.github.io/projects.html


                                                              3
(* Explanation 1: A man and woman are at the park . *)
axiomatization where
  explanation_1 : "∃x y z . Man x ∧ Woman y ∧ Park z ∧ At x z ∧ At y z "
theorem hypothesis :
  (* Premise : A man and woman sit on a park bench with a set of newlyweds behind *)
  assumes asm : " Man x ∧ Woman y ∧ ParkBench z ∧ Newlyweds w ∧ Sit e ∧ Agent e x ∧ Agent e y ∧ Patient e z
       ∧ Behind w z "
  (* Hypothesis : People outside *)
  shows "∃x. People x ∧ Outside x "
proof -
  (* From the premise, we have information about a man and a woman sitting on a park bench . *)
  from asm have " Man x ∧ Woman y " by blast
  (* Explanation 1 states that a man and a woman are at the park . *)
  (* This implies that they are outside, as parks are typically outdoor locations . *)
  from explanation_1 have "∃x y z . Man x ∧ Woman y ∧ Park z ∧ At x z ∧ At y z " by blast
  (* Since a man and a woman are at the park, they are outside . *)
  then have " People x ∧ Outside x " <ATP>
  then show ? thesis <ATP>
qed



Figure 2: An example of a proof sketch constructed by the model to verify an explanation from the e-SNLI dataset.
In this example, while ATPs find proofs for the first two steps using proof tactics, they fail to derive People x∧
Outside x due to missing premises. The feedback provided by Isabelle is then adopted in the next iteration to refine
the explanation and the proof sketch.


main predicate-argument structure. These elements                      ods (Pan et al., 2023; Zhang et al., 2024; Gandarela
are subsequently mapped onto the agent, event ac-                      et al., 2025) to address them. In our work, we
tion, and patient roles within a Neo-Davidsonian                       categorise the errors in this phase into three main
event semantics framework. For example, consider                       dimensions: quantifier scoping error, syntax errors,
the sentence "The father and son kicked the ball".                     and logical inconsistencies.
We can parse it as:
                         S                                             Quantifier Scoping Error The quantifiers indi-
                                                                       cate the scope of logical deductions. In syntheti-
                                                                       cally generated datasets quantifiers are constrained
            NP-SBJ                             VP                      to predefined settings. In contrast, in naturally oc-
                                                                       curring NL settings, incorrect quantifiers in axioms
                                         V        NP-OBJ               may still prove a theorem within a formal system,
The     father     and       son                                       but when those logical forms are restated in natu-
                               kicked the ball                         ral language, their soundness may fail to hold in
indicating that "The father and son" is the subject                    the real world. For example, one cannot declare
while "the ball" is the object. Thus we could build                    “all animals are mammals." Thus, we introduce a
the Neo-Davidsonian event semantics to formalise                       quantifier check and refinement soft-critique stage
it as:                                                                 to prompt the LLM to compare the quantifiers in
∃xyze . ( Father ( x ) ∧ Son ( y ) ∧ Ball ( z ) ∧ Kicked ( e ) ∧       the logical forms against real-world knowledge,
       Agent ( e, x ) ∧ Agent ( e, y ) ∧ Patient ( e, z ) )            thereby avoiding any over-scoped quantifiers.
By leveraging such a process, we construct a clear                     Syntax Errors Internal syntax errors, primarily
representation indicating that the father and the son                  those caused by missing brackets or type unifica-
are the agents performing the event (kick), while                      tion conflicts of logical variables, can often be iden-
the ball is the patient receiving the action, thus                     tified through the theorem prover’s output. Once
capturing all relevant semantic information in the                     identified through a hard critique via the TP, these
transition from natural language to formal language.                   errors can be systematically refined or corrected
We then construct the Isabelle/HOL theory with                         by adjusting the syntax or revising type declara-
axioms (explanatory sentences) and the theorem                         tions. We then employ an LLM for refinement to
(premise and hypothesis sentences).                                    support the systematic correction of these output
3.2    Autoformalisation Critiques                                     errors (constrained within up to five iterations).

Recent studies have identified errors and inconsis-                    Logical Inconsistencies In a formal system, if
tencies in LLM-generated outputs as a challenge in                     contradictory or meaningless axioms are intro-
autoformalisation and have proposed several meth-                      duced, the system becomes inconsistent. By the

                                                                   4
principle of explosion (ex falso [sequitur] quodli-         ments partially indicates how the logical expression
bet), any proposition can then be derived from such         guides LLMs to build the step-wise proof steps,
an inconsistency. To test such errors within the            while we replace the proof tactics with <ATP>,
autoformalised axioms, we construct a modified              which uses Sledgehammer (Isabelle’s automated
theorem τFalse by replacing the conclusion of τ             theorem proving tool) to search for proofs. In Is-
with "False". We then attempt to prove this modi-           abelle/HOL, proof tactics are commands that sys-
fied theorem, if the TP finds a proof, it indicates a       tematically decompose complex proofs into sim-
contradiction within the axioms. In this case, we           pler sub-goals, automating routine steps such as
use an LLM to refine the axioms and attempt to              simplification. Typically, one is asked to prove a
solve the contradictions.                                   statement X given assumptions Y by using proof
                                                            tactics Z, where Z includes commands like simp
3.3      Proof, Verification and Refinement                 (for simplification), auto (for automatic reasoning),
After autoformalisation checking and refinement,            and blast (for first-order reasoning). These tac-
we employ the theorem prover T P to verify the log-         tics instruct Isabelle’s proof engine on how to pro-
ical validity of the axioms and determine whether           cess a proof step by applying appropriate rules,
A |= τ holds. We first use the Sledgehammer tool            simplifications, or other reasoning methods. Once
in Isabelle/HOL for ATPs to automatically find a            Sledgehammer finds a proof, only the explanatory
proof of the theorem. If a proof is found, we extract       sentences (axioms) used in that proof are retained
all possible proofs from Sledgehammer’s results             as the final refined explanation. For example, if
and state that the explanation is logically valid. If       the proof is written as “assms explanation_1 ex-
Sledgehammer fails to find a proof, we construct a          planation_2 by blast”, then only explanation 1 and
proof sketch to attempt a step-by-step proving us-          explanation 2 constitute the minimal set of explana-
ing ATPs based on a set of logical interpretations.         tory sentences required to entail the hypothesis.

Logical Propositions, Relations and Implica-                Explanation Refinement If the automated the-
tions Liu et al. (2025) employ logical expressions          orem prover fails or finds no proofs in a previous
to guide LLMs and mitigate information loss in              proof step, we extract that proof step along with
intermediate reasoning processes. Similarly, we             the proof strategy from the comments part as feed-
begin with a logical proposition extraction step. In        back to prompt the LLM to refine the logical error
this step, we use an LLM to extract logical propo-          (i.e., missing premises) of the related explanatory
sitions and relations from the explanation Ei . Con-        sentences and process into next iteration to itera-
sider the following extracted logical relations as an       tively verify and refine the explanation. After the
example: A: it is raining; B: the grass is wet; C:          explanation refinement, we drop any explanatory
kids can play outside; D: kids are happy as well            sentences that are not included in the proof, as they
as the following logical relations: A → B (if it is         are deemed unnecessary to deriving the hypothesis
raining, the grass is wet) and B → ¬C (if the grass         from the premise and then proceed to the next iter-
is wet, kids cannot play outside). Next, we leverage        ation cycle. We followed the same prompts used in
the extracted logical relations using a SymPy-based         Explanation-Refiner (Quan et al., 2024b) for auto-
propositional-level representation (Meurer et al.,          formalisation. Prompts used for syntactic parsing,
2017) 4 to derive additional implications based on          quantifier refinement, logical consistency and proof
formal logical laws. For instance, from the example         steps generation are reported in Appendix E.
above, SymPy can deduce A → ¬C (if it is raining,
                                                            4     Empirical Evaluation
kids cannot play outside). Algorithm 1 shows the
implementation of SymPy to find derived logical             4.1    Datasets and Models
implications.                                               We conducted experiments with four state-of-the-
                                                            art LLMs within the proposed framework: GPT-
Proof Sketch By combining the logical propo-
                                                            4o (OpenAI, 2023), GPT-4o-mini (OpenAI, 2023),
sitions, relations, and these derived implications,
                                                            Llama3.1-70b (Grattafiori et al., 2024), Deepseek-
the LLM can construct a step-by-step guided proof
                                                            V3 (DeepSeek-AI, 2024). Following Quan et al.
sketch that establishes a logical reasoning chain
                                                            (2024b), we applied three sampled NLI datasets
to prove the goal. As shown in Figure 2, the com-
                                                            of e-SNLI (Camburu et al., 2018), QASC (Khot
   4
       https://www.sympy.org/en/index.html                  et al., 2019), and WorldTree (Jansen et al., 2018)

                                                        5
                                  e-SNLI                         QASC                    WorldTree
                         Init. Final #Iter #Calls Init. Final #Iter #Calls Init. Final #Iter #Calls
          Explanation-Refiner
          Llama3.1-70b   23%    51%   4.08   34.56   4%        18%   4.07   37.49   2%   15%   5.23   51.61
          GPT-4o-mini    13%    30%   3.65   32.55   3%        20%   5.12   44.84   0%    4%   5.00   46.12
          GPT-4o         31%    71%   3.62   32.34   4%        26%   4.35   38.45   2%   13%   4.18   39.26
          Deepseek-V3    25%    69%   2.82   27.74   4%        38%   3.71   35.97   3%   31%   4.52   42.64
          Our Approach
          Llama3.1-70b   36%    78%   2.38   16.28   11%       68%   2.90   25.40   6%   52%   4.62   35.72
          GPT-4o-mini    32%    77%   2.27   16.62   12%       71%   3.35   27.10   5%   47%   4.75   36.50
          GPT-4o         39%    89%   1.54   10.24   10%       79%   3.22   22.32   9%   56%   3.86   26.16
          Deepseek-V3    41%    95%   1.50    9.52   17%       90%   2.53   20.18   7%   73%   3.55   25.30


Table 1: Comparison of our approach with Explanation-Refiner on different LLMs across three datasets. Init.
represents the number of explanations that are initially verified as logically valid. Final indicates the number of
explanations that are refined within a maximum of 10 iterations, while #Iter indicates the average iteration required
to refine an explanation. #Calls shows the average number of LLM calls needed to fully refine an explanation.


each comprising 100 instances. We compare our                  entific explanations requiring multi-hop reasoning.
approach with Explanation-Refiner (Quan et al.,                By contrast, our framework refines a significantly
2024b), a state-of-the-art LLM-driven theorem                  larger number of explanations in WorldTree, un-
prover for NLI that adopts a similar pipeline but              derscoring its capacity to handle more challenging
without incorporating the specific strategies for              inference scenarios. Furthermore, the current ap-
guiding autoformalisation via syntactic parsing,               proach requires fewer LLM calls on average to
performing consistency and quantification checks,              fully refine an explanation, resulting in reduced in-
and guide refinement via proof sketches and ex-                ference time and cost compared to the Explanation-
plicit implication derivation.                                 Refiner (See Table 1). The average number of
                                                               LLM calls was reduced by 58.60%, 39.39%, and
4.2   Results                                                  31.15% on e-SNLI, QASC, and WorldTree, respec-
The proposed architectural interventions effec-                tively, across all LLMs. Applying our approach
tively improve the verification and refinement                 with Deepseek-V3 on the e-SNLI dataset yields the
of natural language explanations. Table 1 and                  most significant reduction, at 65.68%.
Figure 3 compares our proposed framework with
Explanation-Refiner on the tasks of verifying and
refining natural language explanations across mul-             The refinement process effectively corrects aut-
tiple LLMs. The results show that our approach                 oformalisation errors. Figure 3d, 3e, and 3f
more effectively and efficiently refines explana-              present the number of theories in the last itera-
tory sentences for explanation-based NLI. In con-              tion containing syntactic and inconsistency errors
trast, Explanation-Refiner achieves substantially              over five syntax error refinement iterations, com-
lower refinement rates, for example, 51% versus                paring our proposed framework with Explanation-
78% in e-SNLI for Llama3.1, 69% versus 95% for                 Refiner. Overall, our framework yields fewer syn-
Deepseek-V3, 30% versus 77% for GPT-4o-mini,                   tactic errors. By incorporating syntactic parsing
and 71% versus 89% for GPT-4o. Furthermore,                    into autoformalisation, it guides LLMs to capture
Explanation-Refiner generally requires more iter-              fine-grained logical properties of natural language
ations to refine each explanation, indicating that             sentences, thereby reducing type unification errors
although it may identify specific logical errors, it           in constructed theories. Empirically, most syntactic
is less efficient. For instance, Explanation-Refiner           errors diminish considerably within the first three
requires an average of 4.31 iterations in the QASC             iterations, after which the rate of improvement sta-
dataset, compared to 3.0 for our approach. Its per-            bilises. The evaluation results of the number of
formance is particularly limited on the WorldTree              theories that contain logical consistency errors are
dataset, which contains complex, real-world sci-               shown in Figure 5.

                                                           6
Number of Logically Valid Explanations   100                                                              e-SNLI                                                                                                     100                                                             QASC                                                                                                       100                                                   WorldTree




                                                                                                                                                                            Number of Logically Valid Explanations




                                                                                                                                                                                                                                                                                                                                                       Number of Logically Valid Explanations
                                                             ER-GPT-4o-mini                                                                                                                                                              ER-GPT-4o-mini                                                                                                                                                             ER-GPT-4o-mini
                                                             ER-GPT-4o                                                                                                                                                                   ER-GPT-4o                                                                                                                                                                  ER-GPT-4o
                                          80                 ER-Llama3.1-70b                                                                                                                                          80                 ER-Llama3.1-70b                                                                                                                                         80                 ER-Llama3.1-70b
                                                             ER-Deepseek-V3                                                                                                                                                              ER-Deepseek-V3                                                                                                                                                             ER-Deepseek-V3
                                                             Our-GPT-4o-mini                                                                                                                                                             Our-GPT-4o-mini                                                                                                                                                            Our-GPT-4o-mini
                                          60                 Our-GPT-4o                                                                                                                                               60                 Our-GPT-4o                                                                                                                                              60                 Our-GPT-4o
                                                             Our-Llama3.1-70b                                                                                                                                                            Our-Llama3.1-70b                                                                                                                                                           Our-Llama3.1-70b
                                                             Our-Deepseek-V3                                                                                                                                                             Our-Deepseek-V3                                                                                                                                                            Our-Deepseek-V3
                                          40                                                                                                                                                                          40                                                                                                                                                                         40

                                          20                                                                                                                                                                          20                                                                                                                                                                         20

                                           0                                                                                                                                                                           0                                                                                                                                                                          0
                                                0                         2                       4                  6                      8                          10                                                   0                        2                      4                   6                      8                          10                                                   0                        2                    4                 6                       8                           10
                                                                                                      Iteration                                                                                                                                                                 Iteration                                                                                                                                                                Iteration
                                                                                                   (a)                                                                                                                                                                        (b)                                                                                                                                                                      (c)
                                                                         Internal Syntax Errors e-SNLI                                                                                                                                               Internal Syntax Errors QASC                                                                                                                                       Internal Syntax Errors WorldTree
                                         80                                                                                                                                                                          80                                                                                                                                                                         80
                                                                                                             Ours-Llama3.1-70b3.1-70b                                                                                                                                                   Ours-Llama3.1-70b3.1-70b                                                                                                                                               Ours-Llama3.1-70b3.1-70b
                                         70                                                                  Ours-Deepseek-V3                                                                                        70                                                                 Ours-Deepseek-V3                                                                                        70                                                             Ours-Deepseek-V3
 Number of Theory contain Errors




                                                                                                                                                                             Number of Theory contain Errors




                                                                                                                                                                                                                                                                                                                                                        Number of Theory contain Errors
                                                                                                             Ours-GPT-4o-mini                                                                                                                                                           Ours-GPT-4o-mini                                                                                                                                                       Ours-GPT-4o-mini
                                         60                                                                  Ours-GPT4o                                                                                              60                                                                 Ours-GPT4o                                                                                              60                                                             Ours-GPT4o
                                                                                                             ER-Llama3.1-70b                                                                                                                                                            ER-Llama3.1-70b                                                                                                                                                        ER-Llama3.1-70b
                                         50                                                                  ER-Deepseek-V3                                                                                          50                                                                 ER-Deepseek-V3                                                                                          50                                                             ER-Deepseek-V3
                                                                                                             ER-GPT-4o-mini                                                                                                                                                             ER-GPT-4o-mini                                                                                                                                                         ER-GPT-4o-mini
                                         40                                                                  ER-GPT4o                                                                                                40                                                                 ER-GPT4o                                                                                                40                                                             ER-GPT4o
                                         30                                                                                                                                                                          30                                                                                                                                                                         30
                                         20                                                                                                                                                                          20                                                                                                                                                                         20
                                         10                                                                                                                                                                          10                                                                                                                                                                         10
                                          0                                                                                                                                                                           0                                                                                                                                                                          0
                                                    1                             2                       3                             4                              5                                                        1                            2                      3                              4                              5                                                        1                            2                    3                            4                                5
                                                                                                      Iteration                                                                                                                                                                 Iteration                                                                                                                                                                Iteration
                                                                                                   (d)                                                                                                                                                                        (e)                                                                                                                                                                        (f)

       Figure 3: Top – Number of logically valid explanations at each refinement iteration. Bottom – Number of theories
       that contain internal syntactic errors at each syntax error refinement stage.
                                                                                               e-SNLI Faithfulness                                                                                                                                                        QASC Faithfulness                                                                                                                                                    WorldTree Faithfulness
                                         1.0                                                                                                                                                                         1.0                                                                                                                                                                        1.0
                                         0.9            Explanation-Refiner                                                                                                                                          0.9            Explanation-Refiner                                                                                                                                         0.9                                                                                           Explanation-Refiner
                                                                                                                                                                                                                                                                                                                                         0.8566
                                                        Our Approach                                                       0.8443                             0.8537
                                                                                                                                                                                                                                    Our Approach                                                      0.8247                                                                                                                                                                                  Our Approach
                                         0.8                                                     0.7608
                                                                                                                                                0.7384
                                                                                                                                                                                                                     0.8                                                    0.7638                                                                                                              0.8
    Average Faithfulness




                                                                                                                                                                                Average Faithfulness




                                                                                                                                                                                                                                                                                                                                                           Average Faithfulness
                                                                0.7163
                                         0.7                                          0.6732
                                                                                                                  0.6530
                                                                                                                                                                                                                     0.7                    0.6763                                                                                                                                              0.7                                                                                                               0.6527
                                                    0.6179                                                                                                                                                                                                                                                                 0.6288                                                                                                                                            0.6340
                                         0.6                                                                                                                                                                         0.6                                         0.5892
                                                                                                                                                                                                                                                                                             0.5693                                                                                             0.6                                                  0.5821
                                                                                                                                                                                                                                                                                                                                                                                                                       0.5213                                                                       0.5325
                                         0.5                                                                                                                                                                         0.5        0.4983
                                                                                                                                                                                                                                                                                                                                                                                                0.5                                                                 0.4835

                                         0.4                                                                                                                                                                         0.4                                                                                                                                                                        0.4                                         0.3471
                                                                                                                                                                                                                                                                                                                                                                                                           0.3248
                                         0.3                                                                                                                                                                         0.3                                                                                                                                                                        0.3
                                         0.2                                                                                                                                                                         0.2                                                                                                                                                                        0.2
                                         0.1                                                                                                                                                                         0.1                                                                                                                                                                        0.1
                                         0.0                                                                                                                                                                         0.0                                                                                                                                                                        0.0
                                                Llama3.1-70b                      Deepseek-V3                    GPT-4o-mini                      GPT-4o                                                                    Llama3.1-70b                     Deepseek-V3                    GPT-4o-mini                      GPT-4o                                                                    Llama3.1-70b                     Deepseek-V3                GPT-4o-mini                        GPT-4o


                                                                                                   (a)                                                                                                                                                                        (b)                                                                                                                                                                      (c)
                                          Llama3.1-70b (ER)                   GPT-4o (ER)                        GPT-4o-mini (Ours)               ER Trend Line                                                       Llama3.1-70b (ER)                  GPT-4o (ER)                        GPT-4o-mini (Ours)               ER Trend Line                                                       Llama3.1-70b (ER)                  GPT-4o (ER)                    GPT-4o-mini (Ours)                 ER Trend Line
                                          Deepseek-v3 (ER)                    Llama3.1-70b (Ours)                GPT-4o (Ours)                    Ours Trend Line                                                     Deepseek-v3 (ER)                   Llama3.1-70b (Ours)                GPT-4o (Ours)                    Ours Trend Line                                                     Deepseek-v3 (ER)                   Llama3.1-70b (Ours)            GPT-4o (Ours)                      Ours Trend Line
                                          GPT-4o-mini (ER)                    Deepseek-v3 (Ours)                                                 e-SNLI                                                               GPT-4o-mini (ER)                   Deepseek-v3 (Ours)                                                   QASC                                                               GPT-4o-mini (ER)                   Deepseek-v3 (Ours)                                         WorldTree
                                            1.0                                                                                                                                                                         1.0                                                                                                                                                                        1.0
                                            0.9                                                                                                                                                                         0.9                                                                                                                                                                        0.9
                                            0.8                                                                                                                                                                         0.8                                                                                                                                                                        0.8
                                            0.7                                                                                                                                                                         0.7                                                                                                                                                                        0.7
                                            0.6                                                                                                                                                                         0.6                                                                                                                                                                        0.6
                          Utility




                                                                                                                                                                                                      Utility




                                                                                                                                                                                                                                                                                                                                                                                 Utility




                                            0.5                                                                                                                                                                         0.5                                                                                                                                                                        0.5
                                            0.4                                                                                                                                                                         0.4                                                                                                                                                                        0.4
                                            0.3                                                                                                                                                                         0.3                                                                                                                                                                        0.3
                                            0.2                                                                                                                                                                         0.2                                                                                                                                                                        0.2
                                            0.1                                                                                                                                                                         0.1                                                                                                                                                                        0.1
                                            0.0 1         2                   3         4             5      6         7            8       9            10                                                             0.0 1         2                  3         4            5       6         7            8       9            10                                                             0.0 1         2                  3         4          5     6         7            8         9            10
                                                                                                 Iteration                                                                                                                                                                  Iteration                                                                                                                                                                Iteration

                                                                                                   (d)                                                                                                                                                                        (e)                                                                                                                                                                        (f)

       Figure 4: Top – The average faithfulness of the autoformalisation process across different LLMs. Bottom – The
       utility of explanation at different refinement iterations. A higher utility indicating the newly refined explanation are
       more likely be used in the proof of next iteration.


     Syntactic parsing improves faithfulness in aut-                                                                                                                                                                                                                                    Refiner, with an average of 0.7938, 0.7804, and
     oformalisation. We convert the autoformalised                                                                                                                                                                                                                                      0.5975, compared to 0.6706, 0.5714, and 0.4220
     logical forms back into natural language sentences                                                                                                                                                                                                                                 across all three datasets. Our findings indicate that
     using a rule-based algorithm that reconstructs each                                                                                                                                                                                                                                certain models exhibit comparatively lower similar-
     sentence from its action/verb predicates and corre-                                                                                                                                                                                                                                ity scores than others. Further investigation reveals
     sponding argument information. We then calculate                                                                                                                                                                                                                                   that models such as Llama3.1-70b tend to gener-
     the cosine similarity between these reconstructed                                                                                                                                                                                                                                  ate non-existent predicates during formalisation in
     (informalised) sentences between the original sen-                                                                                                                                                                                                                                 Explanation-Refiner, resulting in over-generation
     tences as the faithfulness of autoformalisation, as                                                                                                                                                                                                                                that undermines faithfulness and introduces extra-
     shown in Figure 4. Our approach shows a gener-                                                                                                                                                                                                                                     neous information into the theory. More details
     ally higher faithfulness compared to Explanation-                                                                                                                                                                                                                                  about the rule-based algorithm are included in the


                                                                                                                                                                                                                                                                                    7
                                                                           e-SNLI                            QASC                          WorldTree

                                                              Init.        Final         #Iter    Init.      Final       #Iter    Init.         Final         #Iter

                  Ablations on our approach

                  GPT-4o (- logical relations)                34%      74%(−15%)         2.24     12%      58%(−21%)      3.46    6%       38%(−18%)          4.36
                  GPT-4o (- detailed feedback)                35%      83%(−6%)          2.86     13%      56%(−23%)      4.45    5%       17%(−39%)          6.46
                  GPT-4o (- refine quantifiers)               34%      87%(−2%)          1.63     14%      83%(+4%)       2.89    7%        49%(−7%)          3.65
                  GPT-4o (- refine syntax errors)             21%      74%(−15%)         2.34     5%       58%(−21%)      4.11    2%       24%(−32%)          6.48
                  Deepseek-V3 (- logical relations)           39%      89%(−6%)          1.68     16%      77%(−13%)      2.64    10%      58%(−15%)          4.01
                  Deepseek-V3 (- detailed feedback)           31%      86%(−9%)          3.22     22%      69%(−21%)      4.12    6%       41%(−32%)          6.13
                  Deepseek-V3 (- refine quantifiers)          34%      96%(+1%)          1.64     14%      93%(+3%)       1.89    6%        70%(−3%)          3.23
                  Deepseek-V3 (- refine syntax errors)        28%      77%(−18%)         2.69     12%      68%(−22%)      2.84    4%       46%(−27%)          5.32


                                                                  e-SNLI                                    QASC                                 WorldTree

                                                         V.           I.           Q.             V.          I.          Q.              V.            I.            Q.

         Explanation-Refiner

         GPT-4o                                         9%            3%           6%            18%         9%          18%              33%           8%           16%
         Deepseek-V3                                    27%           3%           10%           34%         9%          25%              44%           23%           31%

         Ablations

         GPT-4o (- refine quantifiers)                  9%            2%     10%(+4%)            13%         2%        23%(+5%)           38%           6%      19%(+6%)
         GPT-4o (- refine syntax errors)              16%(+7%)        1%           3%          38%(+20%)     3%          7%         56%(+23%)           3%            16%
         Deepseek-V3 (- refine quantifiers)             25%           5%     16%(+6%)            31%         14%      35%(+10%)           32%           11%     38%(+7%)
         Deepseek-V3 (- refine syntax errors)       38%(+11%)         4%           11%         51%(+17%)     9%          15%        67%(+23%)           21%           27%



Table 2: Top – Ablation study on the impacts of removing components from the overall architecture. Bottom –
Comparison of manually evaluated variable, implication, and quantifier errors in the autoformalisation process from
a randomly sampled set of 100 Isabelle/HOL theories across all iterations for each LLM.


Appendix B.                                                                                      Detailed feedback and syntax error refinement
                                                                                                 have the highest impact. The most significant
                                                                                                 drop in performance is observed from remov-
Logically guided proof sketches provide effec-
                                                                                                 ing detailed feedback and syntax error refinement
tive feedback for explanation refinement. By
                                                                                                 steps. Providing detailed, step-level feedback to
constructing proof steps from logical propositions,
                                                                                                 the LLM proves significantly more effective than
relations, and derived implications, our method
                                                                                                 using only a binary signal (i.e., provable or unprov-
more precisely pinpoints logical errors, enabling
                                                                                                 able). When replacing detailed with binary feed-
the LLM to iteratively refine explanatory sentences
                                                                                                 back, the number of refined explanations dropped
in subsequent attempts to prove the theorem. As
                                                                                                 substantially; for instance, GPT-4o showed a 39%
shown in Figure 4, the average utility defined as the
                                                                                                 decrease in refined explanations in the WorldTree
proportion of newly introduced explanations that
                                                                                                 dataset. Excluding the syntactic error refinement
are applied in the next iteration’s proof remains
                                                                                                 stage frequently yielded theories that failed under
consistently higher for our approach compared to
                                                                                                 theorem prover scrutiny, thereby producing little to
Explanation-Refiner, even as the number of itera-
                                                                                                 no useful feedback for subsequent refinement.
tions increases. In contrast, Explanation-Refiner’s
utility markedly decreases over successive itera-                                                Logical expression aids LLMs in proof sketches
tions.                                                                                           generation, reducing hallucinations that could
                                                                                                 lead to incorrect or failed proof construction for
4.3   Ablation Study                                                                             explanation refinement. Eliminating the logical
                                                                                                 expression-guided proof step generation compo-
We conducted several ablation studies to evaluate                                                nent led to an increase in required iterations for
the impact of the proposed components. Table 2                                                   explanation refinement and a reduction in the total
shows the results on GPT-4o and Deepseek-V3,                                                     number of successfully refined explanations. These
while Table 3 in Appendix A shows the full abla-                                                 findings highlight the importance of logical expres-
tions.                                                                                           sions in constructing coherent proofs and mitigat-

                                                                                           8
ing hallucinations that otherwise result in incorrect         Theorem-Proving with LLMs Proof generation
or failed proofs.                                             refers to the task of generating intermediate proof
                                                              steps as tactic predictions in automated theorem
Variable and quantifier errors significantly im-              proving (Li et al., 2024). Recent work harness
pact the faithfulness of autoformalisation. We                LLMs to produce formal proof scripts (Polu and
further conducted a human evaluation on three                 Sutskever, 2020; Jiang et al., 2022a; Zhao et al.,
types of errors: variable errors (identifiable by the         2023; Xin et al., 2024b; First et al., 2023; Frieder
theorem prover), implication errors, and quantifier           et al., 2024; Welleck and Saha, 2023a,b; Thakur
errors (not identifiable by the theorem prover) as            et al., 2024; Poulsen et al., 2024), often by trans-
shown in Table 2. Our findings suggest that us-               lating high-level reasoning into low-level tactics.
ing LLMs for autoformalisation still leaves notable           Quan et al. (2024b), for example, prompts the LLM
gaps, particularly in accurately handling variables           to first produce a rough, informal inference strat-
and quantifiers. As shown in Table 2, removing the            egy in natural language, and then automatically for-
quantifier refinement did not substantially alter the         malise this strategy into Isabelle/HOL proof steps.
number of refined explanations. However, human                Jiang et al. (2024) utilises a tactic generator and a
evaluation indicates that the number of quantifier-           proof search module to select tactics during proof
related errors increased when this refinement was             construction to build a proof tree from the root
omitted. Explanation-Refiner does not apply a syn-            goal. Liu et al. (2025) use propositional logic, in-
tactic parsing and quantifier refinement, resulting           troduce Logic-of-Thought prompting, a technique
in more errors being introduced for variable, im-             that appends logically enriched descriptions to the
plication and quantifier errors as shown in Table 2.          original context, thereby improving informational
Thus, we introduced both syntax error refinement              completeness and bolstering the LLMs logical rea-
and quantifier error refinement processes. Our re-            soning ability. In contrast, our approach synthe-
sults show a significant reduction in the overall             sises logical reasoning guidance in close iterative
error rate following the corresponding soft-critique          dialogue with automated provers to provide more
model refinements.                                            robust and interpretable proofs in contrast to LLM-
                                                              driven single-pass methods.
5   Related Work
LLM-Symbolic Integration Recent approaches
have attempted to integrate LLMs with external                6   Conclusion
symbolic models through autoformalisation – i.e.,
the translation of informal statements into formal
representations. Recent work explores this task in            In this paper, we proposed formally-guided meth-
both mathematical (Wu et al., 2022; Jiang et al.,             ods to address the challenges involved in using
2022b; Agrawal et al., 2022; Zhang et al., 2024;              external theorem provers to verify and refine nat-
Xin et al., 2024a; Lu et al., 2024a,b; Leang et al.,          ural language explanations in the domain of natu-
2025) and logical (Olausson et al., 2023; Quan                ral language inference. By incorporating syntactic
et al., 2024a; Kirtania et al., 2024; Lee et al., 2025;       parsing, targeted syntactic error checking, logical-
Raza and Milic-Frayling, 2025) domains using                  relation guidance, and detailed feedback at each
the support of automated theorem provers. Sev-                proof step, our approach significantly outperforms
eral studies (Pan et al., 2023; Jiang et al., 2024;           prior work in both faithfulness of autoformalisation
Quan et al., 2024b) transform natural language sen-           and robustness of iterative explanation refinement.
tences into logical forms based on LLMs. Qi et al.            Ablation studies underscore the importance of each
(2025) integrate symbolic provers into the genera-            component in reducing syntactic issues, maintain-
tion process of logical reasoning problems and pro-           ing consistency, and promoting more efficient log-
pose a multi-hop first-order logic (FOL) reasoning            ical verification and refinement. This framework
dataset. In contrast, our work tackles real-world oc-         opens avenues for more transparent, reliable, and
currences of material inferences rather than purely           scalable NLI systems. Moving forward, we plan to
synthetic data, thereby requiring more robust se-             explore more advanced theorem-proving strategies
mantic representations and autoformalisation pro-             with LLMs and domain-specific expansions, ulti-
cess to capture the complexity of multi-step reason-          mately advancing toward increasingly interpretable
ing over material inferences.                                 and robust end-to-end NLI pipelines.

                                                          9
Limitations                                                    Qianglong Chen, Feng Ji, Xiangji Zeng, Feng-Lin
                                                                 Li, Ji Zhang, Haiqing Chen, and Yin Zhang. 2021.
Although our framework substantially improves                    KACE: Generating knowledge aware contrastive ex-
both the consistency of autoformalisation and the                planations for natural language inference. In Pro-
                                                                 ceedings of the 59th Annual Meeting of the Associa-
robustness of explanation verification, certain limi-
                                                                 tion for Computational Linguistics and the 11th Inter-
tations remain. First, LLMs can still introduce vari-            national Joint Conference on Natural Language Pro-
able inconsistencies, erroneous implications, and                cessing (Volume 1: Long Papers), pages 2516–2527,
incorrect quantifiers that are not fully resolved by             Online. Association for Computational Linguistics.
automated checking. Second, some explanations
                                                               Dhairya Dalal, Marco Valentino, Andre Freitas, and
require nuanced real-world knowledge or domain-                  Paul Buitelaar. 2024. Inference to the best expla-
specific axioms that exceed current formal reason-               nation in large language models. In Proceedings
ing capabilities, requiring expert oversight. Finally,           of the 62nd Annual Meeting of the Association for
the reliability of our iterative refinement pipeline             Computational Linguistics (Volume 1: Long Papers),
                                                                 pages 217–235, Bangkok, Thailand. Association for
hinges on high-quality LLM output and proof-step
                                                                 Computational Linguistics.
feedback; degraded model performance or noisy
system responses can hinder successful verification.           DeepSeek-AI. 2024. Deepseek-v3 technical report.
Future work may explore more advanced semantic                   Preprint, arXiv:2412.19437.
checks, stronger model calibration, and selective
human intervention to further enhance faithfulness             Emily First, Markus N. Rabe, Talia Ringer, and
                                                                 Yuriy Brun. 2023. Baldur: Whole-proof generation
and correctness.                                                 and repair with large language models. Preprint,
                                                                 arXiv:2303.04910.
Ethical statement
                                                               Simon Frieder, Julius Berner, Philipp Petersen, and
While this work focuses on the introduction of                   Thomas Lukasiewicz. 2024. Large language models
mechanisms for improving the control and logical                 for mathematicians. Preprint, arXiv:2312.04556.
consistency properties of LLM-based NLI, having
an overall positive impact, further investigations             João Pedro Gandarela, Danilo S. Carvalho, and André
                                                                 Freitas. 2025. Inductive learning of logical theories
are needed to understand the specific conditions in              with llms: An expressivity-graded analysis. Preprint,
which these methods can perform. The application                 arXiv:2408.16779.
of these methods on real-world or critical settings
need to be complemented by human supervision or                Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri,
                                                                 Abhinav Pandey, Abhishek Kadian, and Ahmad Al-
extensive quantitative and qualitative assessment.               Dahle. 2024. The llama 3 herd of models. Preprint,
                                                                 arXiv:2407.21783.
Acknowledgments
                                                               Xuanli He, Yuxiang Wu, Oana-Maria Camburu,
This work was partially funded by the SNSF project               Pasquale Minervini, and Pontus Stenetorp. 2024. Us-
NeuMath (200021_204617), by the EPSRC grant                      ing natural language explanations to improve robust-
EP/T026995/1, “EnnCore” under Security for all                   ness of in-context learning. In Proceedings of the
in an AI-enabled society, by the CRUK National                   62nd Annual Meeting of the Association for Compu-
                                                                 tational Linguistics (Volume 1: Long Papers), pages
Biomarker Centre, and supported by the Manch-                    13477–13499, Bangkok, Thailand. Association for
ester Experimental Cancer Medicine Centre and the                Computational Linguistics.
NIHR Manchester Biomedical Research Centre.
                                                               Peter Jansen, Elizabeth Wainwright, Steven Mar-
                                                                 morstein, and Clayton Morrison. 2018. WorldTree:
References                                                       A corpus of explanation graphs for elementary sci-
                                                                 ence questions supporting multi-hop inference. In
Ayush Agrawal, Siddhartha Gadgil, Navin Goyal,                   Proceedings of the Eleventh International Confer-
  Ashvni Narayanan, and Anand Tadipatri. 2022. To-               ence on Language Resources and Evaluation (LREC
  wards a mathematics formalisation assistant using              2018), Miyazaki, Japan. European Language Re-
  large language models. Preprint, arXiv:2211.07524.             sources Association (ELRA).

Oana-Maria Camburu, Tim Rocktäschel, Thomas                    Albert Jiang, Konrad Czechowski, Mateja Jamnik, Pi-
  Lukasiewicz, and Phil Blunsom. 2018. e-snli: Natu-             otr Milos, Szymon Tworkowski, Wenda Li, and
  ral language inference with natural language explana-          Yuhuai Tony Wu. 2022a. Thor: Wielding hammers
  tions. In Advances in Neural Information Processing            to integrate language models and automated theorem
  Systems, volume 31. Curran Associates, Inc.                    provers. In NeurIPS.


                                                          10
Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,                Aaron Meurer et al. 2017. SymPy: symbolic computing
  Wenda Li, Jiacheng Liu, Mateja Jamnik, Timo-                      in Python. PeerJ Comput. Sci., 3:e103.
  thée Lacroix, Yuhuai Wu, and Guillaume Lample.
  2022b. Draft, sketch, and prove: Guiding for-                   Tobias Nipkow, Markus Wenzel, and Lawrence C Paul-
  mal theorem provers with informal proofs. ArXiv,                  son. 2002. Isabelle/HOL: a proof assistant for
  abs/2210.12283.                                                   higher-order logic. Springer.

Dongwei Jiang, Marcio Fonseca, and Shay Cohen. 2024.              Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
  LeanReasoner: Boosting complex logical reasoning                  Armando Solar-Lezama, Joshua Tenenbaum, and
  with lean. In Proceedings of the 2024 Conference of               Roger Levy. 2023. LINC: A neurosymbolic approach
  the North American Chapter of the Association for                 for logical reasoning by combining language models
  Computational Linguistics: Human Language Tech-                   with first-order logic provers. In Proceedings of the
  nologies (Volume 1: Long Papers), pages 7497–7510,                2023 Conference on Empirical Methods in Natural
  Mexico City, Mexico. Association for Computational                Language Processing, pages 5153–5176, Singapore.
  Linguistics.                                                      Association for Computational Linguistics.

Tushar Khot, Peter Clark, Michal Guerquin, Pe-                    OpenAI. 2023. GPT-4 technical report.            CoRR,
  ter Alexander Jansen, and Ashish Sabharwal. 2019.                 abs/2303.08774.
  QASC: A dataset for question answering via sentence
  composition. In AAAI.                                           Liangming Pan, Alon Albalak, Xinyi Wang, and
                                                                    William Wang. 2023. Logic-LM: Empowering large
Shashank Kirtania, Priyanshu Gupta, and Arjun Rad-                  language models with symbolic solvers for faithful
  hakrishna. 2024. LOGIC-LM++: Multi-step refine-                   logical reasoning. In Findings of the Association
  ment for symbolic formulations. In Proceedings of                 for Computational Linguistics: EMNLP 2023, pages
  the 2nd Workshop on Natural Language Reasoning                    3806–3824, Singapore. Association for Computa-
  and Structured Explanations (@ACL 2024), pages                    tional Linguistics.
  56–63, Bangkok, Thailand. Association for Compu-
  tational Linguistics.                                           Terence Parsons. 1990. Events in the Semantics of En-
                                                                    glish: A Study in Subatomic Semantics. MIT Press.
Joshua Ong Jun Leang, Giwon Hong, Wenda Li,
  and Shay B. Cohen. 2025. Theorem prover as                      Lawrence Charles Paulson and Jasmin Christian
  a judge for synthetic data generation. Preprint,                  Blanchette. 2012. Three years of experience with
  arXiv:2502.13137.                                                 sledgehammer, a practical link between automatic
                                                                    and interactive theorem provers. In IWIL@LPAR.
Jinu Lee, Qi Liu, Runzhi Ma, Vincent Han, Ziqi Wang,
   Heng Ji, and Julia Hockenmaier. 2025. Entailment-              Stanislas Polu and Ilya Sutskever. 2020. Generative
   preserving first-order logic representations in natural           language modeling for automated theorem proving.
   language entailment. Preprint, arXiv:2502.16757.                 Preprint, arXiv:2009.03393.

Zhaoyu Li, Jialiang Sun, Logan Murphy, Qidong Su,                 Seth Poulsen, Sami Sarsa, James Prather, Juho
  Zenan Li, Xian Zhang, Kaiyu Yang, and Xujie Si.                   Leinonen, Brett A. Becker, Arto Hellas, Paul Denny,
  2024. A survey on deep learning for theorem proving.              and Brent N. Reeves. 2024. Solving proof block
  In First Conference on Language Modeling.                         problems using large language models. In Proceed-
                                                                    ings of the 55th ACM Technical Symposium on Com-
Tongxuan Liu, Wenjiang Xu, Weizhe Huang, Yuting                     puter Science Education V. 1, SIGCSE 2024, page
  Zeng, Jiaxing Wang, Xingyu Wang, Hailong Yang,                    1063–1069, New York, NY, USA. Association for
  and Jing Li. 2025. Logic-of-thought: Injecting logic              Computing Machinery.
  into contexts for full reasoning in large language
  models. Preprint, arXiv:2409.17539.                             Chengwen Qi, Ren Ma, Bowen Li, He Du, Binyuan
                                                                    Hui, Jinwang Wu, Yuanjun Laili, and Conghui
Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong,                  He. 2025. Large language models meet symbolic
   Zhengying Liu, and Zhijiang Guo. 2024a. For-                     provers for logical reasoning evaluation. Preprint,
   malalign: Automated alignment evaluation for auto-               arXiv:2502.06563.
   formalization. Preprint, arXiv:2410.10135.
                                                                  Xin Quan, Marco Valentino, Louise Dennis, and An-
Jianqiao Lu, Yingjia Wan, Zhengying Liu, Yinya Huang,               dre Freitas. 2024a. Enhancing ethical explanations
   Jing Xiong, Chengwu Liu, Jianhao Shen, Hui Jin,                  of large language models through iterative symbolic
   Jipeng Zhang, Haiming Wang, Zhicheng Yang, Jing                  refinement. In Proceedings of the 18th Conference of
   Tang, and Zhijiang Guo. 2024b. Process-driven auto-              the European Chapter of the Association for Compu-
   formalization in lean 4. Preprint, arXiv:2406.01940.             tational Linguistics (Volume 1: Long Papers), pages
                                                                    1–22, St. Julian’s, Malta. Association for Computa-
C. Maienborn, K. von Heusinger, and P. Portner. 2011.               tional Linguistics.
   Semantics: An International Handbook of Natural
   Language Meaning. Number v. 1 in Handbooks of                  Xin Quan, Marco Valentino, Louise A. Dennis, and An-
   Linguistics and Communication Science. De Gruyter                dre Freitas. 2024b. Verification and refinement of nat-
   Mouton.                                                          ural language explanations through LLM-symbolic


                                                             11
  theorem proving. In Proceedings of the 2024 Con-             Xueliang Zhao, Wenda Li, and Lingpeng Kong. 2023.
  ference on Empirical Methods in Natural Language               Decomposing the enigma: Subgoal-based demonstra-
  Processing, pages 2933–2958, Miami, Florida, USA.              tion learning for formal theorem proving. Preprint,
  Association for Computational Linguistics.                     arXiv:2305.16366.
Mohammad Raza and Natasa Milic-Frayling. 2025.
 Instantiation-based formalization of logical reason-
 ing tasks using language models and logical solvers.
                                                               A    Ablation study
 Preprint, arXiv:2501.16961.                                   Table 3 shows the overall results on the ablation
Amitayush Thakur, George Tsoukalas, Yeming Wen,                study for all LLMs.
 Jimmy Xin, and Swarat Chaudhuri. 2024. An in-
 context learning agent for formal theorem-proving.            B    Informalisation
 Preprint, arXiv:2310.04353.
                                                               We perform an autoformalisation process that
Mokanarangan Thayaparan, Marco Valentino, and
 André Freitas. 2020. A survey on explainabil-                 transforms natural language sentences into Neo-
 ity in machine reading comprehension. Preprint,               Davidsonian event-based semantics by leveraging
 arXiv:2010.00389.                                             their underlying structure. One way to measure
Marco Valentino, Mokanarangan Thayaparan, and An-              the faithfulness of this autoformalisation is to trans-
 dré Freitas. 2022. Case-based abductive natural lan-          late the constructed logical forms back into natural
 guage inference. In Proceedings of the 29th Inter-            language and then compare the generated (infor-
 national Conference on Computational Linguistics,             malised) sentences with the original ones using
 pages 1556–1568, Gyeongju, Republic of Korea. In-
 ternational Committee on Computational Linguistics.
                                                               cosine similarity.
                                                                  We employ a rule-based method to transform
Sean Welleck and Rahul Saha. 2023a. Llmstep:                   Neo-Davidsonian logical forms back into coherent
  Llm proofstep suggestions in lean. arXiv preprint
  arXiv:2310.18457.
                                                               natural language. First, we parse a logical form
                                                               that may contain multiple conjuncts, typically con-
Sean Welleck and Rahul Saha. 2023b.           Llmstep:         nected by the logical “and” operator (∧). Each con-
  Llm proofstep suggestions in lean.          Preprint,
                                                               junct is treated as an atomic predicate with the gen-
  arXiv:2310.18457.
                                                               eral structure Predicate(arg1 , arg2 , . . . ). Once the
Sarah Wiegreffe and Ana Marasović. 2021. Teach me to          form is separated into atomic predicates, we distin-
  explain: A review of datasets for explainable natural
                                                               guish between role predicates (e.g., Agent(e1 , x),
  language processing. Preprint, arXiv:2102.12060.
                                                               Patient(e1 , y)) and entity-attribute predicates
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus              (e.g., Child(x), Blonde(x)). The role predicates
  Rabe, Charles Staats, Mateja Jamnik, and Christian           specify how each entity participates in the event
  Szegedy. 2022. Autoformalization with large lan-
  guage models. In Advances in Neural Information              (agent, patient, theme, location, etc.), while the at-
  Processing Systems, volume 35, pages 32353–32368.            tribute predicates detail intrinsic properties of those
  Curran Associates, Inc.                                      entities (for instance, “child,” “blonde,” “small,” or
Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren,              “plastic”).
  Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and                    After identifying these predicates, we group to-
  Xiaodan Liang. 2024a. Deepseek-prover: Advancing             gether all attributes describing the same entity vari-
  theorem proving in llms through large-scale synthetic        able. In particular, we parse the attributes from
  data. Preprint, arXiv:2405.14333.
                                                               right to left, treating the rightmost attribute as
Huajian Xin, Z. Z. Ren, Junxiao Song, Zhihong Shao,            the head noun and the preceding ones as adjec-
  Wanjia Zhao, Haocheng Wang, Bo Liu, Liyue Zhang,             tives. For example, if a single entity x is associ-
  Xuan Lu, Qiushi Du, Wenjun Gao, Qihao Zhu, De-
  jian Yang, Zhibin Gou, Z. F. Wu, Fuli Luo, and               ated with Child(x) and Blonde(x), we combine
  Chong Ruan. 2024b. Deepseek-prover-v1.5: Har-                those attributes to form a concise descriptor such
  nessing proof assistant feedback for reinforcement           as “blonde child.” Likewise, if another entity y has
  learning and monte-carlo tree search. Preprint,              attributes Plastic(y) and Small(y), we might call
  arXiv:2408.08152.
                                                               it “small plastic”.
Lan Zhang, Xin Quan, and Andre Freitas. 2024. Consis-             Next, we convert these role–entity pairings into
  tent autoformalization for constructing mathematical         simple event-level sentences. For each event ei ,
  libraries. In Proceedings of the 2024 Conference on
  Empirical Methods in Natural Language Processing,
                                                               we identify which entity is the Agent and which is
  pages 4020–4033, Miami, Florida, USA. Association            the Patient (or any other role labels), then build
  for Computational Linguistics.                               a straightforward sentence. For instance, if x is

                                                          12
                                           Logical Consistency Errors e-SNLI                                                      Logical Consistency Errors QASC                                                       Logical Consistency Errors WorldTree
                                  80                                                                                     80                                                                                    80
                                                                   Ours-Llama3.1-70b                                                                     Ours-Llama3.1-70b                                                                       Ours-Llama3.1-70b
                                  70                               Ours-Deepseek-V3                                      70                              Ours-Deepseek-V3                                      70                                Ours-Deepseek-V3
Number of Theory contain Errors




                                                                                       Number of Theory contain Errors




                                                                                                                                                                             Number of Theory contain Errors
                                                                   Ours-GPT-4o-mini                                                                      Ours-GPT-4o-mini                                                                        Ours-GPT-4o-mini
                                  60                               Ours-GPT4o                                            60                              Ours-GPT4o                                            60                                Ours-GPT4o
                                                                   ER-Llama3.1-70b                                                                       ER-Llama3.1-70b                                                                         ER-Llama3.1-70b
                                  50                               ER-Deepseek-V3                                        50                              ER-Deepseek-V3                                        50                                ER-Deepseek-V3
                                                                   ER-GPT-4o-mini                                                                        ER-GPT-4o-mini                                                                          ER-GPT-4o-mini
                                  40                               ER-GPT4o                                              40                              ER-GPT4o                                              40                                ER-GPT4o
                                  30                                                                                     30                                                                                    30
                                  20                                                                                     20                                                                                    20
                                  10                                                                                     10                                                                                    10
                                   0                                                                                      0                                                                                     0
                                       1         2         3           4          5                                           1        2         3           4          5                                           1          2         3           4          5
                                                       Iteration                                                                             Iteration                                                                               Iteration
                                                       (a)                                                                                   (b)                                                                                     (c)

                                       Figure 5: Number of theories that contain logical consistency error at each syntax error refinement stage.

      Original Sentence : The boy is inside of the building .
      Logical Form 1: ∃x y e . Boy ( x ) ∧ Building ( y ) ∧ Inside ( e ) ∧ Agent ( e, x ) ∧ Patient ( e, y )
      Informalised Sentence 1: Boy in side building .
      Sentence Similarity : 0.9344

      Logical Form 2: ∃x y e . Boy ( x ) ∧ Building ( y ) ∧ Inside ( e ) ∧ Agent ( e, x )
      Informalised Sentence 2: Boy in side .
      Sentence Similarity : 0.8127



                                                       Figure 6: An example of the faithfulness between two informalised logical forms


“blonde child” and y is “small plastic item,” the cor-                                                                                             utilised API calls for GPT-4o (gpt-4o-2024-08-06)
responding natural language description might by                                                                                                   (OpenAI, 2023), GPT-4o-mini (gpt-4o-mini-2024-
constructed from the event verb “Puts” as “blonde                                                                                                  07-18) (OpenAI, 2023), Deepseek-V3 (Deepseek-
child puts small plastic item” The specific event                                                                                                  V3-671b) (DeepSeek-AI, 2024), and Llama3.1-70b
verb (“puts,” “picks,” “hands over,” etc.) would                                                                                                   (LLama3.1-70b-Instruct) (Grattafiori et al., 2024).
depend on how the event predicate itself is repre-                                                                                                 All temperature is set to 0.
sented in the logical form.
   In cases where the logical form contains implica-                                                                                               D       Runtime Examples
tion, we divide the logical forms into sub-formulas.                                                                                               Tables 4, 5, and 6, together with Figures 7, 8, 9, 10,
Complex operators and connectives (i.e. ∨) will                                                                                                    and 11, show the runtime examples for the e-SNLI,
be mapped carefully to their closest equivalents in                                                                                                QASC, and WorldTree datasets, respectively.
English.
   As shown in Figure 6, different formalised log-                                                                                                 E       Prompts
ical forms can affect the faithfulness of the auto-
                                                                                                                                                   Tables 7, 9, 8, and 10 show the prompts we
formalisation. For instance, Logical Form 2 omits
                                                                                                                                                   used for syntactic parsing, logical proposition
the Patient argument, causing the rule-based sys-
                                                                                                                                                   extraction, logical relation extraction, and proof
tem to skip translating the predicate information
                                                                                                                                                   construction. Complete prompts details can
for the building back into natural language, and
                                                                                                                                                   be found at https://github.com/neuro-symbolic-
thus producing an unfaithful representation.
                                                                                                                                                   ai/faithful_and_robust_nli_refinement.
    C                                  Datasets, LLMs and Theorem Prover
  The datasets used in our experiments are sourced
  from open academic works and include samples
  from e-SNLI (Camburu et al., 2018), QASC (Khot
  et al., 2019), and WorldTree (Jansen et al., 2018).
  We employed Isabelle/HOL (Nipkow et al., 2002)
  as the theorem prover, which is distributed under
  the revised BSD license, and used Explanation-
  Refiner (Quan et al., 2024b) as our baseline work,
  which is under the MIT license. Additionally, we

                                                                                                                                             13
 Algorithm 1: Deriving logical implications with SymPy
  Input :logical_information: string with propositions and relations
  Output :result: string with processed relations and implications
1 logical_props, logical_exprs ← ParseInput(logical_information)

2   if logical_exprs = ∅ then
3        result ← format_propositions(logical_props)
  4      return result
 5 else
  6      Initialise symbols_dict, symbol_meanings ← {}
  7      foreach (key, value) ∈ logical_props do
  8            sanitized_key ← sanitize(key)
  9            symbol ← create_symbol(sanitized_key)
10             Update symbols_dict and symbol_meanings
11       end foreach
12       // Define SymPy logical operators dictionary
13       logical_operators ← {
14             symbols_dict, Not: SymPy negation,
15             And: SymPy conjunction,
16             Or: SymPy disjunction,
17             Implies: SymPy implication,
18             Equivalent: SymPy equivalence
19       }
20       propositions ← []
21       initial_implications ← ∅
22       foreach expr ∈ logical_exprs do
23             expr ← replace_symbols(expr)
24             // Evaluate using SymPy’s logical operators
25             prop ← evaluate_with_sympy(expr, logical_operators)
26             // Apply SymPy’s simplification rules
27             simplified_prop ← sympy.simplify(prop)
28             propositions.append(prop)
29             initial_implications.add(simplified_prop)
30       end foreach
31       derived_implications ← ∅
32       logical_atoms ← get_atoms(propositions)
33       literals ← logical_atoms ∪ {¬atom | atom ∈ logical_atoms}
34       // Use SymPy’s satisfiability checker
35       foreach (antecedent, consequent) ∈ literals × literals do
36             if antecedent ̸= consequent then
37                   implication ← antecedent =⇒ consequent
38                   // Check using SymPy’s logical rules
39                   is_new ← ¬equivalent_to_any(implication, initial_implications)
40                   is_valid ← check_entailment(propositions, implication)
41                   if is_new and is_valid then
 42                        derived_implications.add(implication)
43                   end if
44             end if
45       end foreach
46       result ← format_output(logical_props, logical_exprs, derived_implications)
47       return result
48 end if




                                                             14
                                                                         e-SNLI                           QASC                        WorldTree

                                                           Init.         Final        #Iter   Init.       Final      #Iter    Init.        Final         #Iter

                   Ablations on our approach

                   Llama3.1-70b (- logical relations)      34%       74%(−4%)         2.43     9%       58%(−10%)    2.94     7%      44%(−8%)           5.42
                   Llama3.1-70b (- detailed feedback)      32%      66%(−12%)         3.42    10%       34%(−34%)    3.64      5%     24%(−28%)          8.12
                   Llama3.1-70b (- refine quantifiers)     28%       77%(−1%)         2.18     9%        68%(−0%)    2.88     3%      50%(−2%)           4.52
                   Llama3.1-70b (- refine syntax errors)   18%      57%(−21%)         4.58     5%       53%(−15%)    4.47      3%     30%(−20%)          6.12
                   GPT-4o-mini (- logical relations)       27%      65%(−12%)         2.31    11%       57%(−14%)    4.12     6%      27%(−20%)          5.19
                   GPT-4o-mini (- detailed feedback)       30%      62%(−15%)         4.56     9%       46%(−25%)    3.87     3%      19%(−28%)          6.21
                   GPT-4o-mini (- refine quantifiers)      26%       78%(+4%)         2.10     5%        73%(+2%)    2.92     4%      46%(−1%)           5.13
                   GPT-4o-mini (- refine syntax errors)    15%      43%(−34%)         2.86     3%       34%(−37%)    3.65      3%     10%(−37%)          5.21
                   GPT-4o (- logical relations)            34%      74%(−15%)         2.24    12%       58%(−21%)    3.46      6%     38%(−18%)          4.36
                   GPT-4o (- detailed feedback)            35%       83%(−6%)         2.86    13%       56%(−23%)    4.45      5%     17%(−39%)          6.46
                   GPT-4o (- refine quantifiers)           34%       87%(−2%)         1.63    14%        83%(+4%)    2.89     7%      49%(−7%)           3.65
                   GPT-4o (- refine syntax errors)         21%      74%(−15%)         2.34     5%       58%(−21%)    4.11      2%     24%(−32%)          6.48
                   Deepseek-V3 (- logical relations)       39%       89%(−6%)         1.68    16%       77%(−13%)    2.64     10%     58%(−15%)          4.01
                   Deepseek-V3 (- detailed feedback)       31%      86%(−9%)          3.22    22%       69%(−21%)    4.12     6%      41%(−32%)          6.13
                   Deepseek-V3 (- refine quantifiers)      34%       96%(+1%)         1.64    14%        93%(+3%)    1.89     6%      70%(−3%)           3.23
                   Deepseek-V3 (- refine syntax errors)    28%      77%(−18%)         2.69    12%       68%(−22%)    2.84      4%     46%(−27%)          5.32


                                                               e-SNLI                                    QASC                               WorldTree

                                                      V.           I.            Q.           V.           I.        Q.               V.           I.            Q.

           Explanation-Refiner

           Llama3.1-70b                              24%           10%       10%              43%         12%       34%               45%          15%           27%
           GPT-4o-mini                               18%            8%        7%              41%         8%        32%               39%          9%            29%
           GPT-4o                                    9%            3%        6%               18%         9%        18%               33%          8%            16%
           Deepseek-V3                               27%           3%        10%              34%          9%       25%               44%          23%           31%

           Ablations

           Llama3.1-70b (- refine quantifiers)        23%           8%     13%(+3%)           39%         11%      43%(+9%)        43%             13%     36%(+9%)
           Llama3.1-70b (- refine syntax errors)   41%(+17%)       10%        9%           53%(+10%)       8%        34%        65%(+20%)          11%       23%
           GPT-4o-mini (- refine quantifiers)         14%           5%     11%(+4%)           35%         10%     47%(+15%)        41%             10%     34%(+5%)
           GPT-4o-mini (- refine syntax errors)    39%(+21%)       4%         9%           63%(+21%)      7%         12%        55%(+16%)          7%        23%
           GPT-4o (- refine quantifiers)               9%           2%     10%(+4%)           13%         2%      23%(+5%)         38%             6%      19%(+3%)
           GPT-4o (- refine syntax errors)          16%(+7%)        1%        3%           38%(+20%)       3%         7%        56%(+23%)          3%        16%
           Deepseek-V3 (- refine quantifiers)         25%           5%     16%(+6%)           31%         14%     35%(+10%)        32%             11%     38%(+7%)
           Deepseek-V3 (- refine syntax errors)    38%(+11%)        4%       11%           51%(+17%)       9%        15%        67%(+23%)          21%       27%


Table 3: Top – Ablation study on the impacts of removing components on the analysis of number of explanation
refined across three datasets. Bottom – Comparison of manually evaluated variable, implication, and quantifier errors
in the autoformalisation process from a randomly sampled set of 100 Isabelle/HOL theories across all iterations for
each LLM.




 Dataset   Problem                                     Explanation                                    Logic Info                                          Iteration Validity
 e-SNLI    Premise: A smiling woman                    A violin is an instru-                         Logical Propositions:                                      0     Valid
           is playing the violin in front              ment.                                          A: a violin (from Explanatory
           of a turquoise background.                                                                 Sentence 1)
           Hypothesis: A woman is                                                                     B: an instrument (from Explana-
           playing an instrument.                                                                     tory Sentence 1)
                                                                                                      Logical Relations:
                                                                                                      Implies(A, B)
                                                                                                      Implies(a violin, an instrument)
                                                                                                      Derived Implications: none


     Table 4: An example of a verified logically valid explanation in the e-SNLI dataset without refinement.




                                                                                      15
theory esnli_3_0
imports Main
…
consts
Violin :: "entity ⇒ bool"
Instrument :: "entity ⇒ bool"
Woman :: "entity ⇒ bool"
…
Patient :: "event ⇒ entity ⇒ bool"
InFrontOf :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: A violin is an instrument. *)
axiomatization where
  explanation_1: "∀x. Violin x ⟶ Instrument x"

theorem hypothesis:
  (* Premise: A smiling woman is playing the violin in front of a turquoise background. *)
  assumes asm: "Woman x ∧ Violin y ∧ Background z ∧ Turquoise z ∧ Smiling x ∧ Playing e ∧ Agent e x ∧ Patient e y ∧
InFrontOf x z"
  (* Hypothesis: A woman is playing an instrument. *)
  shows "∃x y e. Woman x ∧ Instrument y ∧ Playing e ∧ Agent e x ∧ Patient e y"
  using assms explanation_1 by blast

end


              Figure 7: An example of an autoformalised Isabelle/HOL theory in the e-SNLI dataset.




Dataset     Problem                       Explanation               Logic Info                          Iteration Validity
QASC        Hypothesis: Some viruses      Some viruses have an      Logical Propositions:                  0      Invalid
            have a coating of phospho-    envelope of phospho-      A: some viruses have an enve-
            lipids.                       lipids and proteins.      lope of phospholipids and pro-
                                          Proteins are sometimes    teins (from Explanatory Sen-
                                          coats of a virus.         tence 1)
                                                                    B: proteins are coats of a virus
                                                                    (from Explanatory Sentence 2)
                                                                    Logical Relations:
                                                                    none
                                                                    Derived Implications: none

QASC        Hypothesis: Some viruses      Some viruses have an      Logical Propositions:                  1      Valid
            have a coating of phospho-    envelope of phospho-      A: viruses have an envelope
            lipids.                       lipids and proteins.      of phospholipids and proteins
                                          Proteins are sometimes    (from Explanatory Sentence 1)
                                          coats of a virus.         B: proteins are coats of a virus
                                          An envelope can be        (from Explanatory Sentence 2)
                                          considered a type of      C: an envelope is a type of coat-
                                          coating.                  ing (from Explanatory Sentence
                                          Phospholipids are a       3)
                                          component of the enve-    D: phospholipids are a compo-
                                          lope of some viruses.     nent of the envelope (from Ex-
                                                                    planatory Sentence 4)
                                                                    Logical Relations:
                                                                    Implies(A, D)
                                                                    Implies(viruses have an enve-
                                                                    lope of phospholipids and pro-
                                                                    teins, phospholipids are a com-
                                                                    ponent of the envelope)
                                                                    Derived Implications: none


          Table 5: An example of how an explanation in the QASC dataset can be refined in one iteration..



                                                           16
theory qasc_16_0
imports Main
…
consts
Virus :: "entity ⇒ bool"
…
Coat :: "entity ⇒ bool"
Coating :: "entity ⇒ bool"

(* Explanation 1: Some viruses have an envelope of phospholipids and proteins. *)
axiomatization where
  explanation_1: "∃x y z w e. Virus x ∧ Envelope y ∧ Phospholipids z ∧ Proteins w ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Of y z ∧ Of y w"

(* Explanation 2: Proteins are sometimes coats of a virus. *)
axiomatization where
  explanation_2: "∃x y. Protein x ∧ Virus y ∧ Coat x ∧ Of x y"

theorem hypothesis:
  assumes asm: "Virus x ∧ Phospholipids z"
  (* Hypothesis: Some viruses have a coating of phospholipids. *)
  shows "∃x y z e. Virus x ∧ Coating y ∧ Phospholipids z ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Of y z”
proof –
  (* From Explanation 1, we know that some viruses have an envelope of phospholipids and proteins. *)
  from explanation_1 obtain x y z w e where "Virus x ∧ Envelope y ∧ Phospholipids z ∧ Proteins w ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Of y z ∧ Of y w" by blast
  (* We need to show that some viruses have a coating of phospholipids. *)
  (* Since an envelope can be considered a type of coating, we can infer that y is a coating. *)
  then have "Virus x ∧ Coating y ∧ Phospholipids z ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Of y z" sledgehammer
  then show ?thesis <ATP>
qed

end



                   Figure 8: An example of an autoformalised Isabelle/HOL theory in the QASC dataset.




theory qasc_16_1
imports Main
…
consts
Virus :: "entity ⇒ bool"
…
PartOf :: "entity ⇒ entity ⇒ bool"

(* Explanation 1: Some viruses have an envelope of phospholipids and proteins. *)
axiomatization where
  explanation_1: "∃x y z w e. Virus x ∧ Envelope y ∧ Phospholipids z ∧ Proteins w ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Component y z ∧ Component y w"

(* Explanation 2: Proteins are sometimes coats of a virus. *)
axiomatization where
  explanation_2: "∃x y. Protein x ∧ Virus y ∧ Coat x y"

(* Explanation 3: An envelope can be considered a type of coating. *)
axiomatization where
  explanation_3: "∀x. Envelope x ⟶ Coating x"

(* Explanation 4: Phospholipids are a component of the envelope of some viruses. *)
axiomatization where
  explanation_4: "∃x y z. Phospholipids x ∧ Envelope y ∧ Virus z ∧ Component y x ∧ PartOf y z"

theorem hypothesis:
  assumes asm: "Virus x ∧ Phospholipids z"
  (* Hypothesis: Some viruses have a coating of phospholipids. *)
  shows "∃x y z e. Virus x ∧ Coating y ∧ Phospholipids z ∧ Have e ∧ Agent e x ∧ Patient e y ∧ Component y z"
  using explanation_1 explanation_3 by blast

end



                   Figure 9: An example of an autoformalised Isabelle/HOL theory in the QASC dataset.




                                                                               17
Dataset   Problem                      Explanation                  Logic Info                         Iteration Validity
WorldTree Hypothesis: A forest fire    wildfire is when a forest    Logical Propositions:                 0      Invalid
          would cause deer to die or   catches fire.                A: wildfire (from Explanatory
          leave a woodland.            fire causes harm to          Sentence 1)
                                       trees; to forests; to        B: forest catches fire (from Ex-
                                       living things.               planatory Sentence 1)
                                       a deer is a kind of          C: fire causes harm to trees
                                       animal.                      (from Explanatory Sentence 2)
                                       an animal is a kind of       D: fire causes harm to forests
                                       living thing.                (from Explanatory Sentence 2)
                                       killing means harming        E: fire causes harm to living
                                       something         causing    things (from Explanatory Sen-
                                       death.                       tence 2)
                                       a deer lives in a forest.    F: deer (from Explanatory Sen-
                                       woodland means forest.       tence 3)
                                       natural disasters can        ...
                                       cause animals to leave       Q: forest is a kind of environ-
                                       an environment.              ment (from Explanatory Sen-
                                       a wildfire is a kind of      tence 10)
                                       natural disaster.            Logical Relations:
                                       a forest is a kind of        Equivalent(A, B)
                                       environment.                 Implies(C, D)
                                                                    ...
                                                                    Implies(M, Q)
                                                                    Derived Implications: Im-
                                                                    plies(Not(O), Not(A))
                                                                    Implies(B, A)
                                                                    ...
                                                                    Implies(L, Q)

WorldTree Hypothesis: A forest fire    Woodland means forest.       Logical Propositions:                 1      Valid
          would cause deer to die or   A wildfire is a kind of      A: woodland (from Explanatory
          leave a woodland.            natural disaster.            Sentence 1)
                                       A deer is a kind of ani-     B: forest (from Explanatory Sen-
                                       mal.                         tence 1) ...
                                       An animal is a kind of       L: lives in a forest (from Ex-
                                       living thing.                planatory Sentence 9)
                                       A forest is a kind of en-    Logical Relations:
                                       vironment.                   Equivalent(A, B)
                                       Natural disasters can        Implies(C, D)
                                       cause animals to leave       ...
                                       an environment.              Implies(I, Implies(B, Not(G)))
                                       Fire causes harm to          Derived Implications: Im-
                                       trees; to forests; to liv-   plies(E, Not(D))
                                       ing things.                  Implies(E, Not(K))
                                       A forest fire is a kind of   ...
                                       wildfire.                    Implies(Not(G), Not(E))
                                       A deer lives in a forest.


     Table 6: An example of how an explanation in the WorldTree dataset can be refined in one iteration.




                                                          18
theory worldtree_19_0
imports Main
…
Die :: "event ⇒ bool"

(* Explanation 1: Wildfire is when a forest catches fire. *)
axiomatization where
   explanation_1: "∀x. Wildfire x ⟷ (∃y e z. Forest y ∧ Catch e ∧ Agent e y ∧ Patient e z ∧ Fire z)"

(* Explanation 2: Fire causes harm to trees; to forests; to living things. *)
axiomatization where
  explanation_2: "∀x y e. Fire x ∧ Harm e ∧ Agent e x ⟶ (Patient e y ∧ (Tree y ∨ Forest y ∨ LivingThing y))"

(* Explanation 3: A deer is a kind of animal. *)
axiomatization where
  explanation_3: "∀x. Deer x ⟶ Animal x"

(* Explanation 4: An animal is a kind of living thing. *)
axiomatization where
  explanation_4: "∀x. Animal x ⟶ LivingThing x"

(* Explanation 5: Killing means harming something causing death. *)
axiomatization where
  explanation_5: "∀e1 e2 x y. Killing e1 ⟷ (Harming e2 ∧ Agent e2 x ∧ Cause e2 ∧ Patient e2 y ∧ Death y)"

(* Explanation 6: A deer lives in a forest. *)
axiomatization where
  explanation_6: "∃x y e. Deer x ∧ Forest y ∧ Live e ∧ Agent e x ∧ In x y"

(* Explanation 7: Woodland means forest. *)
axiomatization where
  explanation_7: "∀x. Woodland x ⟷ Forest x"

(* Explanation 8: Natural disasters can cause animals to leave an environment. *)
axiomatization where
  explanation_8: "∀x y z. NaturalDisaster x ∧ Animal y ∧ Environment z ⟶ (∃e1 e2. Cause e1 ∧ Agent e1 x ∧ Leave e2 ∧ Agent e2 y ∧ Patient e2 z)"

(* Explanation 9: A wildfire is a kind of natural disaster. *)
axiomatization where
  explanation_9: "∀x. Wildfire x ⟶ NaturalDisaster x"

(* Explanation 10: A forest is a kind of environment. *)
axiomatization where
  explanation_10: "∀x. Forest x ⟶ Environment x"

theorem hypothesis:
  assumes asm: "ForestFire x ∧ Deer y ∧ Woodland z”
  (* Hypothesis: A forest fire would cause deer to die or leave a woodland. *)
  shows "∃e1 e2. (Die e1 ∧ Agent e1 y) ∨ (Leave e2 ∧ Agent e2 y ∧ Patient e2 z)"
proof -
  (* From the premise, we have known information about ForestFire, Deer, and Woodland. *)
  from asm have "ForestFire x" and "Deer y" and "Woodland z" apply simp
  (* Explanation 7: Woodland means forest. *)
  (* Using the equivalence between Woodland and Forest, we can infer Forest z. *)
  from `Woodland z` have "Forest z" apply (simp add: assms)
  (* Explanation 9: A wildfire is a kind of natural disaster. *)
  (* Since ForestFire is a type of Wildfire, we can infer that it is a NaturalDisaster. *)
  from `ForestFire x` have "Wildfire x" by (simp add: assms)
  then have "NaturalDisaster x" sledgehammer
  (* Explanation 3 and 4: A deer is a kind of animal, and an animal is a kind of living thing. *)
  (* We can infer that Deer y is an Animal and a LivingThing. *)
  from `Deer y` have "Animal y" <ATP>
  then have "LivingThing y" <ATP>
  (* Explanation 10: A forest is a kind of environment. *)
  (* Since we have Forest z, we can infer that it is an Environment. *)
  from `Forest z` have "Environment z" <ATP>
  (* Explanation 8: Natural disasters can cause animals to leave an environment. *)
  (* Since we have a NaturalDisaster x, Animal y, and Environment z, we can infer that the animal may leave the environment. *)
  from `NaturalDisaster x` and `Animal y` and `Environment z` have "∃e2. Leave e2 ∧ Agent e2 y ∧ Patient e2 z" <ATP>
  (* We have shown that a forest fire would cause deer to leave a woodland. *)
  then show ?thesis <ATP>
qed
end



                    Figure 10: An example of an autoformalised Isabelle/HOL theory in the WorldTree dataset.

                                                                 Table 7: Prompts used for syntactic parsing.

 SYSTEM: You are an expert in linguistics. You will be provided with some sentences, please do a syntactic parse for each
 word in that sentence. Some instructions:
 1. You must give me the answer for all provided sentences. 2. Do not add any notes. 3. If no premise sentence provided,
 include it in the answer as none. 4. Retain the answer words in their original form within the provided sentence.
 USER: Here are some examples:
 Hypothesis Sentence:
 1. A woman is playing an instrument.
 Subject: A woman
 Verb Phrase: is playing an instrument
 - Main Verb: playing
 - Auxiliary Verb: is
 Direct Object: an instrument
 ...
 <<<<<<<<<<<<<
 Provided sentences:

 Answer:



                                                                                                       19
theory worldtree_19_1
imports Main
…
Die :: "event ⇒ bool"

(* Explanation 1: Woodland means forest. *)
axiomatization where
  explanation_1: "∀x. Woodland x ⟷ Forest x"

(* Explanation 2: A wildfire is a kind of natural disaster. *)
axiomatization where
  explanation_2: "∀x. Wildfire x ⟶ NaturalDisaster x"

(* Explanation 3: A deer is a kind of animal. *)
axiomatization where
  explanation_3: "∀x. Deer x ⟶ Animal x"

(* Explanation 4: An animal is a kind of living thing. *)
axiomatization where
  explanation_4: "∀x. Animal x ⟶ LivingThing x"

(* Explanation 5: A forest is a kind of environment. *)
axiomatization where
  explanation_5: "∀x. Forest x ⟶ Environment x"

(* Explanation 6: Natural disasters can cause animals to leave an environment. *)
axiomatization where
  explanation_6: "∀x y z. NaturalDisaster x ∧ Animal y ∧ Environment z ⟶ (∃e. Leave e ∧ Agent e y ∧ Patient e z)"

(* Explanation 7: Fire causes harm to trees; to forests; to living things. *)
axiomatization where
  explanation_7: "∀x y z w. Fire x ∧ (∃e. Harm e ∧ (Tree y ∨ Forest z ∨ LivingThing w) ⟶ (Patient e y ∨ Patient e z ∨ Patient e w))"

(* Explanation 8: A forest fire is a kind of wildfire. *)
axiomatization where
  explanation_8: "∀x. ForestFire x ⟶ Wildfire x"

(* Explanation 9: A deer lives in a forest. *)
axiomatization where
  explanation_9: "∃x y e. Deer x ∧ Forest y ∧ Lives e ∧ Agent e x ∧ In x y"

theorem hypothesis:
  assumes asm: "ForestFire x ∧ Deer y ∧ Woodland z"
  (* Hypothesis: A forest fire would cause deer to die or leave a woodland. *)
  shows "∃e1 e2. (Die e1 ∧ Agent e1 y) ∨ (Leave e2 ∧ Agent e2 y ∧ Patient e2 z)"
  by (meson assms explanation_1 explanation_2 explanation_3 explanation_5 explanation_6 explanation_8)

end




              Figure 11: An example of an autoformalised Isabelle/HOL theory in the WorldTree dataset.




                                                                       20
                        Table 8: Prompts used for extracting logical propositions and relations

SYSTEM: You are an expert in symbolic reasoning. You will be provided with an explanation. You need to extract the
logical propositions and the corresponding logical relations from the explanation.
USER: Here are some examples:
Provided Explanatory Sentences:
Explanatory Sentence 1: If it is raining, the grass will be wet.
Explanatory Sentence 2: Having a picnic is equivalent to having a meal on the grass.

Answer:
Logical Propositions:
A: it is raining (from Explanatory Sentence 1)
B: the grass will be wet (from Explanatory Sentence 1)
C: having a picnic (from Explanatory Sentence 2)
D: having a meal on the grass (from Explanatory Sentence 2)

Logical Relations:
Implies(A, B): A → B
Equivalent(C, D): C ↔ D

<<<<<<<<<<<<<
Provided Explanatory Sentences:

Answer:

Logical Propositions:

Logical Relations:




                                    Table 9: Prompts used for refining quantifiers.

SYSTEM: You are an expert in semantics, formal language and neo-davidsonian event semantics. You will be provided with
some sentences. These sentences have been transferred into Isabelle/HOL symbolic language. However, the quantifiers in
the logical form may not be defined correctly.There might be missing variables after the quantifiers for arguments inside
the parentheses of the predicate-argument forms of an axiom or a theorem. The quantifier may not reflect to real-world
knowledge. Refine the logical forms if there are any quantifiers that are not defined correctly.

Here are some examples:
Provided Iabelle code:
(* Explanation 1: Many consumers feed at more than one trophic level. *)
axiomatization where
explanation_1: "∀x e. Consumer x −→ (Feed e ∧ Agent e x ∧ At e y ∧ MoreThanOneTrophicLevel y)"

Answer:
Explanation 1 states "Many consumers" and in real-world knowledge, some consumers are omnivores or generalists that
feed across multiple trophic levels, but it use the universal quantifier ’∀’ in explanation_1. We should use the existential
quantifier ’∃’ instead.
For the quantifier variables in explanation_1, the variable ’y’ is missing.
...
<<<<<<<<<<<<<
Strictly follow my instructions.

Provided Isabelle code:

Answer:




                                                            21
                                     Table 10: Prompts used for building proofs.

SYSTEM: You are an expert in Isabelle theorem prover, first-order logic and Davidsonian event semantics. You will be
provided with premises, explanations and hypothesis sentences. You will be provided with an Isabelle code which consists
of some axioms, a theorem hypothesis that needs to be proven. The logical form of axioms indicates some explanation
sentences, the logical form after "assume asm:" indicates a premise sentence and the logical form after "shows" indicates
a hypothesis sentence. The natural language form is stated as the comments. You will be provided with some logical
propositions, logical relations and derived logical rules from the explanation sentences to help you construct the proof. You
need to construct a proof about how to prove the theorem hypothesis in "proof -" and "qed" sections using the premise
(logical form after "assume asm:") and explanations (axioms). The proof should be derived from the premise and explanation
sentences. You don’t need to state the automated theorem prover you will need to use. You just need to write a proof sketch.
Some instructions:
1. ’sorry’ and ‘fix’ command is not allowed.
...
5. leave the automated theorem prover and proof tactic as <ATP>
...
<<<<<<<<<<<<<
Strictly follow my instructions.

Premise Sentence:

Explanation Sentences:

Hypothesis Sentence:

Provided Isabelle Code:

Logical Information:

Known Information:

Try to prove:

Answer:




                                                             22
