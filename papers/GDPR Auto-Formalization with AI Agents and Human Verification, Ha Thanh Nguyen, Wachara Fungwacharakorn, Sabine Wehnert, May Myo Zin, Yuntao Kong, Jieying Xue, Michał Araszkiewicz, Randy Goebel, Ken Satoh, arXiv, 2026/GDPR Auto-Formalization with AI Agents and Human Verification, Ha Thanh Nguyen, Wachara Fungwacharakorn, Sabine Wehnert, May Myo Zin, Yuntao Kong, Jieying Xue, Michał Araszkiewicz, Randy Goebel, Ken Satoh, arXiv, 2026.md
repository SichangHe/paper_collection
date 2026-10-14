                                                    GDPR Auto-Formalization with AI Agents and Human
                                                                      Verification
                                                    Ha Thanh Nguyen                           Wachara Fungwacharakorn                                    Sabine Wehnert
                                            Center for Juris-Informatics, ROIS-DS           Center for Juris-Informatics, ROIS-DS            Ruhr-University Bochum, RC-Trust
                                                        Tokyo, Japan                                    Tokyo, Japan                                Bochum, Germany

                                                        May Myo Zin                                      Yuntao Kong                                        Jieying Xue
                                            Center for Juris-Informatics, ROIS-DS           Center for Juris-Informatics, ROIS-DS           Center for Juris-Informatics, ROIS-DS
                                                        Tokyo, Japan                                    Tokyo, Japan                                    Tokyo, Japan

                                                   Michał Araszkiewicz                                  Randy Goebel                                         Ken Satoh
arXiv:2604.14607v2 [cs.AI] 2 May 2026




                                            Uniwersytet Jagielloński w Krakowie            Alberta Machine Intelligence Institute,          Center for Juris-Informatics, ROIS-DS
                                                     Kraków, Poland                                University of Alberta                                Tokyo, Japan
                                                                                               Edmonton, Alberta, Canada
                                        Abstract                                                                  permissions, and a distinction between substantive rights and pro-
                                        We study the overall process of automatic formalization of GDPR           cedural safeguards. As a result, outputs that are logically consistent
                                        provisions using large language models, within a human-in-the-            may still be legally invalid or misleading.
                                        loop verification framework. Rather than aiming for full autonomy,           We argue that full autonomy is not appropriate for this task. In-
                                        we adopt a role-specialized workflow in which LLM-based AI com-           stead, legal formalization requires a verification-centered approach,
                                        ponents, operating in a multi-agent setting with iterative feedback,      where generation a formal representation is treated as provisional
                                        generate legal scenarios, formal rules, and atomic facts. This is cou-    and correctness is established through structured scrutiny.
                                        pled with independent verification modules which include human               To this end, we propose a human-in-the-loop, multi-agent frame-
                                        reviewers’ assessment of representational, logical, and legal cor-        work. A drafting agent generates scenarios, rules, and facts, while
                                        rectness. Using this approach, we construct a high-quality dataset        multiple verifier agents independently evaluate representational,
                                        to be used for GDPR auto-formalization, and analyze both suc-             logical, and legal correctness. This role separation is designed to
                                        cessful and problematic cases. Our results show that structured           reduce both bias and surface disagreements.
                                        verification and targeted human oversight are essential for reliable         Using this framework, we construct a curated dataset for GDPR
                                        legal formalization, especially in the presence of legal nuance and       auto-formalization through iterative refinement, automated verifi-
                                        context-sensitive reasoning.                                              cation, and selective human validation.1 Our analysis shows that
                                                                                                                  LLMs perform well on trigger-based legal conditions but fail on
                                                                                                                  absolute rights, narrowly scoped exceptions, omission-based viola-
                                        CCS Concepts                                                              tions, and procedural–substantive distinctions. These failures arise
                                        • Computing methodologies → Knowledge representation                      primarily from abstraction choices rather than logical errors.
                                        and reasoning; • Applied computing → Law.                                    Contributions. (1) A verification-centered framework for legal
                                                                                                                  formalization using role-specialized AI agents; (2) empirical insights
                                        Keywords                                                                  into failure modes of AI-generated legal formalizations; and (3) a
                                        GDPR auto-formalization, legal formalization, human-in-the-loop           curated dataset for GDPR auto-formalization to support future
                                        verification, multi-agent AI, defeasible legal reasoning, Pythen, legal   research.
                                        knowledge representation, AI and Law
                                                                                                                  2        Related Work
                                                                                                                  This section reviews prior work in three closely related areas: legal
                                        1    Introduction                                                         formalization, the automation of formalization using AI techniques,
                                                                                                                  and prior efforts to formalize the GDPR. While each line of re-
                                        Recent advances in large language models (LLMs) have made it
                                                                                                                  search contributes important foundations, none directly addresses
                                        increasingly feasible to generate structured representations from
                                                                                                                  the problem of reliably validating automatically generated legal
                                        natural language at scale. In legal informatics, this has renewed
                                                                                                                  formalizations for complex regulations such as the GDPR.
                                        interest in legal formalization: translating legal norms into machine-
                                        executable representations for automated reasoning and compli-
                                                                                                                  2.1       Legal Formalization
                                        ance assessment. The General Data Protection Regulation (GDPR)
                                        has emerged as a key test case due to its complexity and practical        Legal formalization serves as the necessary initial step for auto-
                                        relevance [31].                                                           mated legal reasoning, by aiming to translate complex legal texts
                                           However, the main challenge is not generating syntactically            into machine-executable logical representations while preserving
                                        valid rules, but ensuring legal faithfulness. Legal norms involve         1 The dataset is available at https://huggingface.co/datasets/nguyenthanhasia/gdpr-
                                        open-textured concepts, conditional obligations, role-dependent           cases.
                                                                                                                         Nguyen Ha Thanh et al.


legal meaning. Theoretical research in this domain spans historical     effective on benchmark datasets [13], these models were not de-
legal philosophy and modern computational logic. Historically, the      signed for domains which require precise symbolic reasoning, such
debate over Legal Formalism has shaped the understanding of law         as general legal reasoning [2].
as a system of abstract concepts subject to processing by deduction,       Recent advances have delivered further leverage with large lan-
which is in contrast with later Realist critiques that highlighted      guage models (LLMs), which can be used to generate logic programs
the social and policy choices inherent in legal interpretation. This    (e.g., Datalog [1], ASP [2], FOL [14, 28]) via prompting or fine-tuning
tension underpins the modern challenge of formalizing laws open         [14, 15]. Other results employ specialized techniques like Chain-of-
texture [6] and continues to shape contemporary approaches to           Instruction (CoI) prompting to guide the generative process toward
computational legal formalization.                                      structured logical outputs, such as those in Defeasible Deontic Logic
   Early computational work on legal formalization focuses on           (DDL) [7]. A noted critical challenge is the scarcity of annotated
building legal expert systems based on logic programming lan-           legal datasets (informal-formal pairs), which has guided researchers
guages, such as PROLOG [24, 25]. Foundational research often fo-        to explore methods like back-translation and model specialization
cuses on adopting various non-classical logics, such as Deontic         to generate high-quality training data, or to use LLMs in zero-shot
Logic [8, 26] (to express obligations and permissions) and Defeasible   or few-shot settings [3]. Some studies also show how LLMs can
Logic [18, 20] (to manage rule conflicts and exceptions common in       produce executable logic from natural language queries with high
legal texts).                                                           fluency, though often at the cost of formal correctness [1, 15].
   Current practice often integrates these logics within structured        To address these challenges, hybrid neuro-symbolic approaches
frameworks like LegalRuleML [12] and leverages domain ontolo-           integrate LLMs with logic engines. For instance, some systems
gies to supply a shared vocabulary of legal concepts that supports      in legal reasoning use LLMs to extract candidate rules in Prolog,
rule formalization. Another approach intends to make represen-          validated via symbolic execution for soundness and consistency
tations more accessible to legal scholars. For example, PROLEG          [9]. These approaches increasingly treat logic generation as an
[23], derived from PROLOG, aims to separate negation-as-failure         interpretable intermediate layer, which should enable verifiable
from exceptions, in order to mirror the legal practice of switching     reasoning. By combining LLMs’ linguistic flexibility with logic
the burden of proof. Other approaches involve designing new pro-        solvers’ precision, current methods aim to bridge natural language
gramming languages for representing legal rules, such as Catala         and formal rule-based representations.
[16], or using controlled natural languages, such as Attempto Con-         Despite these advances, most automated formalization approaches
trolled English [5, 27] and Logical English [10, 11]. These languages   emphasize syntactic validity, logical consistency, or execution cor-
restrict their syntax so that sentences translate unambiguously         rectness. They rarely address whether a generated rule faithfully
into executable logical forms. However, current practices on legal      captures the normative scope of a legal provision, whether excep-
formalization still rely on manual or semi-manual processes, and        tions are applied too broadly, or whether procedural requirements
while being rigorous, they are often cited as time-consuming and        are mistakenly encoded as conditions that negate substantive rights.
expertise-reliant. Addressing this challenge requires both advanced     Within this perspective, verification is thus treated primarily as a
information extraction techniques [21] and careful consideration        technical problem, rather than a legal one.
of regulatory trade-offs; this motivates our automated yet human-
verified approach.
   While these approaches provide expressive and legally informed       2.3    GDPR Formalization
formalisms, they largely presuppose that the formalization itself       The General Data Protection Regulation (GDPR) is often used in
is correct. They offer limited guidance on how to validate formal       legal formalization studies, driven by the need for automated com-
representations that are generated automatically, particularly when     pliance checking, risk assessment, and enforcement of data subject
errors arise from abstraction choices, scope misalignment, or subtle    rights. The formalizataion of GDPR provides the challenge of a
misinterpretations of legal conditions and exceptions.                  highly structured, multi-layered approach to translating complex,
                                                                        principle-based legislation in GDPR into actionable logic. Research
                                                                        in this area is anchored by the creation of specialized, large-scale
                                                                        knowledge bases, such as DAPRECO [22]. This repository contains
                                                                        hundreds of GDPR rules formalized using sophisticated logics, of-
2.2    Automating Formalization                                         ten Reified Input/Output (RIO) Logic—an extension of I/O logic
AI researchers have long been seeking to automate the complex           designed to handle the complex deontic and structural aspects of
translation from natural language law to formal logic to overcome       legal norms—and encoded using the standardized XML formalism,
the labor-intensive nature of manual formalization. In semantic         LegalRuleML. This work showcases the effective, manual applica-
parsing, early systems like CHILL used inductive logic program-         tion of logic to model permissions, obligations, and prohibitions
ming to learn mappings from sentences to Prolog queries [29],           across the breadth of the regulation.
which demonstrated feasibility but revealed limited scalability be-        A key enabler of this work is an ontology-level conceptualiza-
yond narrow domains. Grammar-based approaches, such as those            tion of GDPR entities and relations. In particular, PrOnto (Privacy
by [30] improved compositional generalization but required logical      Ontology) [19] models core GDPR concepts (e.g., data categories,
form annotations. Neural semantic parsers introduced encoder-           processing purposes, legal bases, and roles such as Controller and
decoder architectures that translate text to structured logical forms   Processor) and provides the semantic grounding needed to interpret
such as lambda calculus or Prolog-like representations [4]. While       and maintain large rule sets consistently.
GDPR Auto-Formalization with AI Agents and Human Verification


   However, existing GDPR formalization efforts are largely manual        indicate only the existence of a right, independent of whether the
and expert-driven. While they provide authoritative examples of           controller subsequently complies. For permissibility-based provi-
what correct formalization looks like, they do not address how            sions, the boolean leable expresses permissibility under the modeled
such formalizations can be obtained reliably through automated or         conditions and exceptions, rather than a holistic assessment of com-
semi-automated processes. In particular, they do not consider how         pliance across the entire regulation.
LLM-generated rules should be validated, how human oversight                 These semantic choices are deliberately simple and transparent.
should be integrated, or how disagreements and ambiguities should         Rather than aiming for full legal completeness, they provide a
be systematically analyzed during dataset construction.                   stable and interpretable foundation for studying where automated
                                                                          formalization succeeds or fails, and for subjecting generated rules
3     Task Definition and Formalism                                       to both automated and human verification.
Here we define our auto-formalization task and introduce the formal
representation used for legal rules and reasoning. Our purpose is         4     Methodology
to make explicit what is being generated, what is being evaluated,        Here we describe the verification-centered process by which GDPR
and under which semantic assumptions correctness is assessed,             auto-formalization samples are generated, evaluated, refined, and
independently of the generation pipeline described below.                 selectively retained. Rather than treating data generation as a purely
                                                                          generative task, the methodology emphasizes structured verifica-
3.1    Task Definition                                                    tion, role separation, and staged and bounded iterative refinement
We pursue the task of GDPR auto-formalization coupled with hu-            to ensure legal and logical reliability.
man expert verification. Given the natural-language text of a GDPR           The overall process employs five distinct AI agents: one Drafter
article, the objective is to construct structured, machine-executable     Agent responsible for initial generation, and four Verifier Agents
representations that support legal reasoning while remaining faith-       tasked with independent quality assessment. Automated verifica-
ful to the normative content of the provision.                            tion is complemented by human validation and legal expert review,
   Each data sample consists of: (i) a scenario describing a concrete     through which representative high-quality samples and system-
factual situation with a binary legal question, (ii) a set of atomic      atic failure cases are identified and curated. The overview of the
facts extracted from the scenario, (iii) a rule tree representing the     pipeline is demonstrated in Figure 1.
legal norm, and (iv) a boolean label obtained by evaluating the rule
against the facts.                                                        4.1      Data Generation Pipeline
   The task goes beyond generating executable logic: a formal-            Our data generation pipeline automates the transformation of
ization is considered correct only if it preserves the scope of the       GDPR articles into structured, machine-readable formalisms. This
legal norm, respects condition–exception structures, and does not         process consists of three primary stages: generation, automated
conflate procedural safeguards with substantive rights.                   verification, and human validation, operating in a feedback loop to
   Legal rules are represented using the Pythen framework [17],           progressively enhance data quality.
a Python-based formalism for defeasible legal reasoning. Rules
                                                                          4.1.1 Automated Content Generation. The process is initiated by
are encoded as condition–exception structures (“rule trees”) and
                                                                          the Drafter Agent, which generates the core components of a sample
evaluated against extracted facts to produce a boolean outcome.
                                                                          given a target GDPR article:
We treat Pythen as an executable representation layer that enables
systematic evaluation and verification.                                        (1) Scenario Generation: A natural-language narrative of
                                                                                   approximately 200–300 words describing a concrete factual
3.2    Semantics and Evaluation Assumptions                                        situation that falls within the scope of the target GDPR
Rule evaluation is performed by a deterministic RuleTreeEvalu-                     article and concludes with a binary (yes/no) legal question
ator, which computes the truth value of the target predicate by                    about the scenario.
recursively traversing the rule tree and matching conditions against           (2) Rule Formalization: A formal representation of the le-
the provided facts.                                                                gal norm encoded as a Pythen rule_tree, capturing the
   The evaluation procedure follows these assumptions:                             condition-exception structure of the article.
                                                                               (3) Fact Extraction: A set of atomic predicates extracted from
      • A closed set of facts is assumed for each scenario; predicates             the scenario, corresponding to leaf predicates in the rule
        not present in the fact set are treated as not established.                tree and serving as inputs for evaluation.
      • Exceptions have priority over conditions: if any exception
        predicate is satisfied, the rule is defeated regardless of sat-      An illustrative example of a Pythen rule structure is shown in
        isfied conditions.                                                Listing 1. The example is schematic and intended to demonstrate
      • Negation-as-failure is used implicitly for predicates that        the formal pattern rather than any specific GDPR provision.
        are not provable, unless explicitly represented as classical          Listing 1: Illustrative example of a Pythen rule structure.
        negation in the rule tree.                                        {
   The resulting boolean label reflects the outcome of applying                  "p" : " gdpr_art20_data_portability " ,
                                                                                 " op " : " ALL " ,
the formalized rule to the extracted facts under these assumptions.              " conditions " : [
Crucially, note that a positive outcome does not necessarily imply                      " data_subject_requests_portability " ,
legal compliance in practice. For rights-based provisions, this may                     " processing_is_automated " ,
                                                                                                                                             Nguyen Ha Thanh et al.


                                        Stage 1         Stage 2          Stage 3           Stage 4                Stage 5
                                        Drafter       Deterministic    Multi-Agent        Iterative               Human
                                        Agent           Labeling       Verification      Refinement              Validation




                                       Scenario                         Scenario
                                    200-300 Words                        0-100                           6 Annotators
                                    Binary Question                                                         Quality
                                                                      Representation                                          GDPR
                                                       Rule Tree                                          Assessment
                                                                          0-100        Thresholding                           Expert
                                      Rule Tree       Evaluator                                                                Meta-
                                                        Label:                         Average Score    a) Relevance
                                     Pythen JSON                          Logic                                               Review
                                                      True / False                     ≥ Threshold?     b) Formalization
                                     Conditions &                         0-100                                               Validation &
                                      Exceptions                                                        c) Logic                Insights

                                                                          Legal        Feedback Loop
                                     Atomic Facts                         0-100         Drafter Agent    GDPR Autoformalization
                                                                                                               Dataset




                        Figure 1: Overview of the verification-centered generation and validation pipeline.


          " processing_based_on_contract_or_consent "                                              GDPR article, the correctness and completeness of the ex-
     ],                                                                                            tracted facts, and the overall validity of the legal reasoning
     " exceptions " : [ " adversely_affects_others_rights " ]
                                                                                                   implied by the sample.
}

                                                                                          Each Verifier Agent produces a numerical score (ranging from 0
4.1.2 Logical Rule Evaluation. Following the generation of the sce-                    to 100) as well as detailed feedback. The average score across all
nario, rule tree, and facts, a deterministic RuleTreeEvaluator com-                    four agents determines the initial quality assessment of the sample.
ponent then computes a derived label. This component functions as
the execution engine for the Pythen framework. It systematically                       4.1.4 Iterative Refinement through Feedback. The feedback from
traverses the rule_tree, evaluating the logical nodes by apply-                        the four Verifier Agents is systematically passed back to the Drafter
ing the set of extracted facts. The final output is a boolean label                    Agent. This information serves as a potential corrective input for
(True or False), representing the logical outcome of applying the                      the subsequent generation cycle. The Drafter Agent uses this feed-
formalized rule to the given facts.                                                    back to adjust its generation strategy, thus aiming to improve the
   This rule tree is generated specifically to operationalize and                      quality of the scenario, the precision of the rule formalism, and the
answer the yes/no question posed in the scenario; however, its                         relevance of the extracted facts. This iterative process continues
structure also reflects that auto-formalization does not necessarily                   until a generated sample achieves an average score above a pre-
yield a one-to-one correspondence between the natural-language                         defined threshold, at which point it enters the human validation
legal inputs—namely the scenario question and the governing legal                      stage.
norm—and their resulting logical representation.                                          The threshold of 70 was initially selected as a pragmatic balance
                                                                                       point where the averaged feedback from multiple independent Veri-
4.1.3 Multi-Agent Verification Framework. To ensure the quality of
                                                                                       fier Agents indicates sufficient structural correctness and relevance,
the generated data, four specialized Verifier Agents perform auto-
                                                                                       while still allowing minor residual errors to be efficiently resolved
mated evaluation, each focusing on a distinct analytical dimension.
                                                                                       during the subsequent human validation stage. This choice opti-
These agents provide quantitative scores and qualitative feedback:
                                                                                       mizes learning throughput without compromising overall quality
     • Scenario Verifier: Evaluates the relevance, specificity, and                    control.
       realism of the generated scenario in the context of the target
       GDPR article. This agent assesses whether the scenario
       presents sufficient factual detail to enable a determinate                      5      Conlusions
       legal conclusion.                                                               This paper presented a verification-centered, human-in-the-loop
     • Representation Verifier: Validates the syntactic correct-                       framework for GDPR auto-formalization using role-specialized LLM
       ness and structural integrity of the rule_tree according                        agents. The framework generates scenarios, Pythen rule trees, and
       to the Pythen JSON schema. This agent verifies that all                         atomic facts, and subjects them to independent automated verifi-
       predicates are properly formed, that conditions and excep-                      cation and targeted human review, resulting in a curated dataset
       tions are correctly specified, and that the logical operators                   of GDPR auto-formalization samples. Human evaluation shows
       (ANY/ALL) are appropriately applied.                                            that automated formalization is most reliable when legal norms
     • Logical Verifier: Confirms that the label derived by the                        can be expressed through explicit trigger conditions and when sce-
       RuleTreeEvaluator is a logically sound consequence of the                       narios encode legally decisive facts with sufficient precision. More
       rules and facts. This agent independently re-evaluates the                      complex normative structures—such as absolute rights, narrowly
       rule tree against the extracted facts to verify consistency.                    scoped exceptions, omission-based duties, and role-dependent con-
     • Legal Verifier: Conducts a substantive legal analysis of                        straints—continue to require human verification. Future work will
       the sample. This involves assessing the degree to which                         prioritize article-level applicability checks, improved modeling of
       the rule_tree accurately captures the legal nuances of the                      omissions and role separation, and broader coverage across GDPR
GDPR Auto-Formalization with AI Agents and Human Verification


provisions to further clarify the boundaries of reliable legal auto-                         [17] Ha-Thanh Nguyen and Ken Satoh. 2026. PYTHEN: A Flexible Framework for
formalization.                                                                                    Legal Reasoning in Python. arXiv preprint arXiv:2603.15317 (2026).
                                                                                             [18] Donald Nute. 2001. Defeasible logic. In International Conference on Applications
                                                                                                  of Prolog. Springer, 151–169.
Acknowledgements                                                                             [19] Monica Palmirani, Michele Martoni, Arianna Rossi, Cesare Bartolini, and Livio
                                                                                                  Robaldo. 2018. Pronto: Privacy ontology for legal reasoning. In International
This work was supported by the "R&D Hub Aimed at Ensuring                                         Conference on Electronic Government and the Information Systems Perspective.
                                                                                                  Springer, 139–152.
Transparency and Reliability of Generative AI Models" project of the                         [20] Henry Prakken. 2013. Logical tools for modelling legal argument: a study of
MEXT, by JSPS KAKENHI Grant Numbers, 25H00522 and 25H01112,                                       defeasible reasoning in law. Vol. 32. Springer Science & Business Media.
and by JST as part of Adopting Sustainable Partnerships for Inno-                            [21] Damith Premasiri, Tharindu Ranasinghe, Ruslan Mitkov, Mo El-Haj, and Ingo
                                                                                                  Frommholz. 2025. Survey on legal information extraction: current status and
vative Research Ecosystem (ASPIRE), Grant Number JPMJAP25B2.                                      open challenges: D. Premasiri et al. Knowledge and Information Systems 67, 12
                                                                                                  (2025), 11287–11358.
                                                                                             [22] Livio Robaldo, Cesare Bartolini, Monica Palmirani, Arianna Rossi, Michele Mar-
References                                                                                        toni, and Gabriele Lenzini. 2020. Formalizing GDPR provisions in reified I/O
 [1] Mario Alviano, Matteo Capalbo, Georg Gottlob, Irfan Kareem, Fabrizio Lo Scudo,               logic: the DAPRECO knowledge base. Journal of Logic, Language and Information
     and Sebastiano Piccolo. 2025. A Preliminary Evaluation of Open-Source LLMs for               29, 4 (2020), 401–449.
     Datalog-Based Semantic Parsing in the ASVIN Project. In Joint Proceedings of the        [23] Ken Satoh, Kento Asai, Takamune Kogawa, Masahiro Kubota, Megumi Naka-
     Workshops and Doctoral Consortium of the 41st International Conference on Logic              mura, Yoshiaki Nishigai, Kei Shirakawa, and Chiaki Takano. 2010. PROLEG: an
     Programming (ICLP-WS-DC 2025) co-located with 41st International Conference on               implementation of the presupposed ultimate fact theory of Japanese civil code
     Logic Programming (ICLP 2025) (CEUR Workshop Proceedings, Vol. 4117). CEUR-                  by PROLOG technology. In JSAI international symposium on artificial intelligence.
     WS.org. https://ceur-ws.org/Vol-4117/                                                        Springer, 153–164.
 [2] Mario Alviano, Lorenzo Grillo, Fabrizio Lo Scudo, and Luis Angel Rodriguez              [24] Marek J. Sergot, Fariba Sadri, Robert A. Kowalski, Frank Kriwaczek, Peter Ham-
     Reiners. 2025. Integrating Answer Set Programming and Large Language Models                  mond, and H Terese Cory. 1986. The British Nationality Act as a logic program.
     for Enhanced Structured Representation of Complex Knowledge in Natural                       Commun. ACM 29, 5 (April 1986), 370–386.
     Language. In Proceedings of the Thirty-Fourth International Joint Conference on         [25] David M Sherman. 1987. A Prolog model of the income tax act of Canada. In
     Artificial Intelligence, IJCAI 2025, Montreal, Canada, August 16-22, 2025. ijcai.org,        Proceedings of the 1st international conference on Artificial intelligence and law.
     4330–4338. doi:10.24963/IJCAI.2025/482                                                       New York, NY, USA, 127–136.
 [3] Julien Breton, Mokhtar Mokhtar Billami, Max Chevalier, Ha Thanh Nguyen, Ken             [26] Georg Henrik Von Wright. 1951. Deontic logic. Mind 60, 237 (1951), 1–15.
     Satoh, Cassia Trojahn, and May Myo Zin. 2025. Leveraging LLMs for legal terms           [27] Adam Wyner. 2015. From the language of legislation to executable logic programs.
     extraction with limited annotated data. Artificial Intelligence and Law (2025),              In Logic in the theory and practice of lawmaking. Springer, 409–434.
     1–27.                                                                                   [28] Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi, and Faramarz Fekri.
 [4] Li Dong and Mirella Lapata. 2016. Language to Logical Form with Neural                       2024. Harnessing the Power of Large Language Models for Natural Language
     Attention. In Proceedings of the 54th Annual Meeting of the Association for Compu-           to First-Order Logic Translation. In Proceedings of the 62nd Annual Meeting
     tational Linguistics, ACL 2016, August 7-12, 2016, Berlin, Germany, Volume 1: Long           of the Association for Computational Linguistics (Volume 1: Long Papers), ACL
     Papers. The Association for Computer Linguistics. doi:10.18653/V1/P16-1004                   2024, Bangkok, Thailand, August 11-16, 2024, Lun-Wei Ku, Andre Martins, and
 [5] Norbert E Fuchs, Kaarel Kaljurand, and Tobias Kuhn. 2008. Attempto controlled                Vivek Srikumar (Eds.). Association for Computational Linguistics, 6942–6959.
     english for knowledge representation. In Reasoning Web: 4th International Sum-               doi:10.18653/V1/2024.ACL-LONG.375
     mer School 2008, Venice, Italy, September 7-11, 2008, Tutorial Lectures. Springer,      [29] John M. Zelle and Raymond J. Mooney. 1996. Learning to Parse Database Queries
     104–124.                                                                                     Using Inductive Logic Programming. In Proceedings of the Thirteenth National
 [6] Herbert Lionel Adolphus Hart. 2012. The concept of law. OUP Oxford.                          Conference on Artificial Intelligence and Eighth Innovative Applications of Artificial
 [7] Elias Horner, Cristinel Mateis, Guido Governatori, and Agata Ciabattoni. 2025.               Intelligence Conference, AAAI 96, IAAI 96, Portland, Oregon, USA, August 4-8, 1996,
     From Legal Texts to Defeasible Deontic Logic via LLMs: A Study in Automated                  Volume 2, William J. Clancey and Daniel S. Weld (Eds.). AAAI Press / The MIT
     Semantic Analysis. arXiv preprint arXiv:2506.08899 (2025).                                   Press, 1050–1055. http://www.aaai.org/Library/AAAI/1996/aaai96-156.php
 [8] Andrew JI Jones and Marek Sergot. 1992. Deontic logic in the representation of          [30] Luke S. Zettlemoyer and Michael Collins. 2005. Learning to Map Sentences
     law: Towards a methodology. Artificial Intelligence and Law 1, 1 (1992), 45–64.              to Logical Form: Structured Classification with Probabilistic Categorial Gram-
 [9] Manuj Kant, Sareh Nabi, Manav Kant, Roland Scharrer, Megan Ma, and Marzieh                   mars. In UAI ’05, Proceedings of the 21st Conference in Uncertainty in Ar-
     Nabi. 2025. Towards Robust Legal Reasoning: Harnessing Logical LLMs in Law.                  tificial Intelligence, Edinburgh, Scotland, July 26-29, 2005. AUAI Press, 658–
     CoRR abs/2502.17638 (2025). arXiv:2502.17638 doi:10.48550/ARXIV.2502.17638                   666. https://dslpitt.org/uai/displayArticleDetails.jsp?mmnu=1&smnu=2&article_
[10] Robert Kowalski. 2020. Logical English. In Proceedings of Logic and Practice of              id=1209&proceeding_id=21
     Programming (LPOP).                                                                     [31] May-Myo Zin, Sabine Wehnert, Yuntao Kong, Ha-Thanh Nguyen, Wachara
[11] Robert Kowalski, Jacinto Dávila, and Miguel Calejo. 2022. Logical English as a               Fungwacharakorn, Jieying Xue, Michał Araszkiewicz, Randy Goebel, Ken Satoh,
     Programming Language for the Law. In Proceedings of Programming Languages                    and Le-Minh Nguyen. 2026. Can Legislation Be Made Machine-Readable in
     and the Law 2022.                                                                            PROLEG? arXiv preprint arXiv:2601.01477 (2026).
[12] Ho-Pun Lam and Mustafa Hashmi. 2019. Enabling reasoning with LegalRuleML.
     Theory and Practice of Logic Programming 19, 1 (2019), 1–26.
[13] Chen Liang, Jonathan Berant, Quoc V. Le, Kenneth D. Forbus, and Ni Lao. 2017.
     Neural Symbolic Machines: Learning Semantic Parsers on Freebase with Weak
     Supervision. In Proceedings of the 55th Annual Meeting of the Association for
     Computational Linguistics, ACL 2017, Vancouver, Canada, July 30 - August 4,
     Volume 1: Long Papers, Regina Barzilay and Min-Yen Kan (Eds.). Association for
     Computational Linguistics, 23–33. doi:10.18653/V1/P17-1003
[14] Junnan Liu. 2025. Few-Shot Natural Language to First-Order Logic Translation
     via Code Generation. In Proceedings of the 2025 Conference of the Nations of
     the Americas Chapter of the Association for Computational Linguistics: Human
     Language Technologies, NAACL 2025 - Volume 1: Long Papers, Albuquerque, New
     Mexico, USA, April 29 - May 4, 2025, Luis Chiruzzo, Alan Ritter, and Lu Wang
     (Eds.). Association for Computational Linguistics, 10939–10960. doi:10.18653/
     V1/2025.NAACL-LONG.547
[15] Daniel Mendoza, Christopher Hahn, and Caroline Trippel. 2024. Translating
     Natural Language to Temporal Logics with Large Language Models and Model
     Checkers. In Formal Methods in Computer-Aided Design, FMCAD 2024, Prague,
     Czech Republic, October 15-18, 2024, Nina Narodytska and Philipp Rümmer (Eds.).
     IEEE, 1–11. doi:10.34727/2024/ISBN.978-3-85448-065-5_17
[16] Denis Merigoux, Nicolas Chataing, and Jonathan Protzenko. 2021. Catala: a
     programming language for the law. Proceedings of the ACM on Programming
     Languages 5, ICFP (2021), 1–29.
                                                                                                                          Nguyen Ha Thanh et al.


A     Human Verification and Detailed Findings                           incorrectly justify downstream processing by another. These fail-
The human verification stage was conducted by six annotators             ures are not reliably detectable through automated verification
with prior academic and applied experience in artificial intelligence    alone and require human interpretation to identify.
and legal reasoning. Each annotator evaluated a distinct subset             In addition to substantive misalignment, human review also
of instances, with no overlap across annotators. As a result, inter-     highlights inefficiencies in formalization, such as unnecessary rule
annotator agreement metrics were not computed, as the study              chains and incorrect treatment of negation, which do not always
design prioritized expert coverage and throughput over redundancy.       affect the final outcome but can undermine interpretability and
   After the Drafter and Verifier Agents completed their iterative       proper burden allocation. Taken together, these findings indicate
generation and verification cycle, a total of 400 samples exceeded       that automated legal formalization performs reliably only within a
the predefined quality threshold based on aggregated verifier scores.    constrained subset of legal structures, and that human verification
From this pool, human annotators further selected 120 samples that       remains essential for identifying norm-level misrepresentations
exhibited high confidence and minimal ambiguity in their factual         that arise from abstraction, omission, or scope leakage.
and legal structure.
   Each selected case includes the target GDPR article, a scenario       A.2     Qualitative Analysis Summary
description, a formalized rule tree, formalized facts, a labeled out-    The detailed qualitative analysis of both successful ("Good Cases")
come, and feedback from verifier agents. The cases were evaluated        and problematic ("Bad Cases") formalizations is provided in Appen-
according to several criteria: (a) whether the scenario is relevant      dix B. The analysis demonstrates that the automated formalization
to the target GDPR article; (b) whether, given the scenario and          matches expert legal judgment when the underlying legal norm
the article, the rules and facts are reasonably formalized; and (c)      can be expressed through explicit, trigger-based conditions (e.g., a
whether the resulting reasoning is logically sound.                      clean Article 20 portability case). However, failures often occur due
   The 120 samples were then categorized by the annotators into          to abstraction choices, such as controller-agnostic modeling, invali-
good cases and bad cases, reflecting clear alignment or misalign-        dation of hidden nuances in straightforward cases, misplacement
ment with legal expectations. These categorized cases were subse-        of procedural identity verification as a condition, inefficiencies in
quently reviewed by a legal expert acting as a meta-reviewer, who        formalized rule trees, and fact extraction anchored to the original
performed a second-round substantive legal verification.                 setting rather than the proposed change. These findings underscore
                                                                         the necessity of human verification for identifying norm-level mis-
                                                                         representations.
A.1    Overall Findings from Human Evaluation                            B  Detailed Qualitative Analysis of
Human evaluation reveals a clear distinction between cases where            Formalization Cases
automated formalization aligns with expert legal judgment and
cases where it fails in structurally meaningful ways.                    B.1 Illustrative Good Cases
   Across the reviewed cases, successful formalizations share a com-     The following examples illustrate cases where the automated for-
mon pattern: the underlying legal norm can be expressed through          malization matches expert legal judgment. These are not artificially
explicit, trigger-based conditions, and the scenario encodes legally     simple scenarios, but realistic situations in which the system cor-
decisive facts with sufficient precision. In such cases, the generated   rectly models both the logical structure and the legal limits of GDPR
rule trees correctly separate the existence of rights or obligations     provisions. In particular, they demonstrate appropriate abstraction
from subsequent compliance behavior, and the resulting reasoning         choices, a clear distinction between the existence of rights and sub-
aligns with statutory requirements. This pattern is observed in par-     sequent compliance behavior, and accurate representation of legal
ticular for provisions such as Article 20, where rights are defined      conditions and exceptions.
by a finite set of cumulative conditions, and for Article 32, with
                                                                         B.1.1   A Clean Article 20 Portability Case.
scenarios that explicitly encode ongoing security obligations rather
than static safeguards.                                                     Case description. Sofia is a paying subscriber of PulsePath, a
   By contrast, problematic cases consistently involve legal struc-      fitness-tracking application operated under a monthly subscription
tures that resist straightforward condition-exception modeling.          contract. Upon account creation, she provided basic account data
These include absolute or non-derogable rights, cumulative dis-          (name, email, age, height, weight) and connected her smartwatch.
closure duties, omission-based violations, and risk-calibrated obli-     PulsePath processes these data by automated means in its cloud
gations. In these settings, the automated formalizations tend to         infrastructure, including manually entered workout and nutrition
become over-permissive, either by implicitly balancing interests         logs as well as observed data such as step counts, heart rate, sleep
where the law does not permit balancing, by failing to represent         duration, GPS running routes, and workout timestamps. In addi-
legally operative absences as facts, or by collapsing distinct legal     tion, PulsePath generates training readiness scores and suggested
roles and purposes into a single abstraction.                            workout plans using proprietary algorithms.
   A recurring source of error lies in abstraction choices rather than      When deciding to switch to a competing service, EnduroCloud,
syntactic or logical flaws. Several cases exhibit internally coher-      Sofia submits a written request to PulsePath invoking her right to
ent and executable rule trees that nonetheless misrepresent the          data portability under GDPR Article 20. She asks (i) to receive her
legal scope of exceptions, conflate procedural safeguards with sub-      personal data in a structured, commonly used, machine-readable for-
stantive entitlement, or allow lawful processing by one actor to         mat (e.g., CSV or JSON), and (ii) to have the same dataset transmitted
GDPR Auto-Formalization with AI Agents and Human Verification


directly to EnduroCloud via an available API connection, providing         SteelForm contracts an external occupational health provider to
the endpoint and authorization token. PulsePath responds that it           conduct periodic medical assessments, including fatigue screening,
can provide only screenshots or PDF summaries and refuses direct           musculoskeletal evaluations, and mental health questionnaires. The
transmission, citing a lack of support for integrations with com-          provider processes detailed health data under medical confidential-
petitors. It also states, without further explanation, that training       ity and issues fitness determinations (e.g., fit, fit with restrictions,
readiness scores and workout plans will be excluded as "internal           unfit).
analytics."                                                                   In parallel, SteelForm integrates the provider’s digital platform
                                                                           with its internal HR system to streamline workforce planning. As
   Formal rule structure. The agents model the existence of the
                                                                           part of this integration, SteelForm requests access not only to the
Article 20 right using a concise rule that mirrors the statutory
                                                                           fitness determinations but also to underlying medical indicators,
conditions: a data subject request, personal data relating to the
                                                                           such as anxiety scores, medication usage, and risk flags generated
requester, a processing basis in consent or contract, and automated
                                                                           during assessments. SteelForm argues that both entities are jointly
processing. Exceptions are limited to the explicit legal carve-out
                                                                           responsible for workplace safety and therefore operate under a
for adverse effects on the rights and freedoms of others.
                                                                           shared compliance framework.
Listing 2: Core rule capturing the existence of the Article 20
data portability right.                                                       Auto-formalized rule outcome. In the agent-generated formal-
{                                                                          ization, the processing of health data is evaluated at the level of
        "p" : " gdpr_art20_data_portability " ,                            the overall program rather than per controller. Because the occu-
        " op " : " ALL " ,                                                 pational health provider lawfully processes the data under Arti-
        " conditions " : [
                                                                           cle 9(2)(h), the exception is treated as applying globally to the entire
               " data_subject_requests_portability " ,
               " data_is_personal_data_of_subject " ,                      data flow. As a result, the model concludes that subsequent storage
               " processing_based_on_consent_or_contract " ,               and use of detailed health data by SteelForm’s HR department is
               " processing_is_automated "                                 permitted.
        ],
        " exceptions " : [ " adversely_affects_others_rights " ]              Modeling failure. This outcome is legally incorrect. Article 9(2)(h)
}                                                                          authorizes processing by or under the responsibility of health pro-
                                                                           fessionals for occupational or preventive medicine purposes. It
   Outcome. Based on the asserted facts—processing based on con-
                                                                           does not extend to employer-side HR processing for staffing, per-
tract, automated means, and a valid portability request concerning
                                                                           formance management, or operational planning. By collapsing the
Sofia’s personal data—the predicate gdpr_art20_data_portability
                                                                           occupational health provider and the employer into a single undif-
evaluates to true. This reflects the correct legal position: Sofia holds
                                                                           ferentiated controller context, the model erases the legal boundary
the Article 20 right with respect to the personal data she provided
                                                                           that limits how far the exception can travel.
and the data observed from her use of PulsePath, irrespective of
PulsePath’s refusal to comply or its choice of output format.                 Analysis. The failure arises from treating "the program" as the
   The strongest aspect of the agents’ auto-formalization in this          unit of analysis instead of treating each controller and purpose
case is the correct separation between the existence of the right and      separately. In legal reasoning, the permissibility of processing must
the controller’s subsequent compliance behavior. By grounding              be assessed independently for each controller, even where data orig-
the right exclusively in the statutory conditions of Article 20, the       inate from a lawful upstream activity. The auto-formalization fails
model avoids collapsing non-compliant responses—such as offering           to enforce this separation and instead allows a lawful medical ex-
only PDFs, refusing direct transfer, or making vague claims about          ception to leak into non-medical HR decision-making. This results
"internal analytics"—into factors that negate the right itself.            in a false positive: processing is labeled lawful despite the absence
                                                                           of explicit consent or any other applicable Article 9 exception for
B.2       Illustrative Bad Cases                                           the employer.
The negative cases presented below were chosen because they ex-
pose failure modes that are difficult to detect through automated             Interpretive significance. This case illustrates a structural risk
verification alone. In many instances, the generated rule trees are        of controller-agnostic modeling. When controller boundaries are
syntactically valid and internally coherent, and in some cases even        not represented as first-class elements in the rule system, lawful
produce legally correct outcomes. Nevertheless, expert review re-          processing by one actor can incorrectly legitimize downstream pro-
veals deeper modeling errors arising from abstraction choices, scope       cessing by another. The error does not stem from misunderstanding
misalignment, or conflation of procedural and substantive legal            Article 9’s text, but from an abstraction choice that suppresses the
conditions. These cases are therefore illustrative not of random mis-      controller dimension entirely. Human review is required to reintro-
takes, but of structurally meaningful risks inherent in automated          duce this distinction and prevent exception scope expansion across
legal formalization.                                                       organizational roles.

B.2.1     Failure of Controller-Based Modeling.                            B.2.2   Invalidation of Hidden Nuances in Straightforward Cases.

  Case description. A German manufacturing company, SteelForm                Case description. MediShip is a licensed online pharmacy in Ger-
AG, introduces a mandatory occupational health monitoring pro-             many that processes customer data for multiple purposes: fulfilling
gram for machine operators after several workplace accidents.              prescription orders, complying with statutory pharmacy and tax
                                                                                                                                Nguyen Ha Thanh et al.


obligations, preventing fraud and securing its IT systems, and (op-     personal_data_concerns_requester to evaluate to false whenever
tionally) sending promotional emails. In the described case, Anna       identity verification is treated as incomplete or ambiguous by the
orders a prescription asthma inhaler and provides the necessary         agent.
personal and prescription data. While the processing required for
                                                                           Analysis. This modeling choice illustrates how a procedural re-
fulfilment, legal compliance, and fraud prevention is clearly neces-
                                                                        quirement can unintentionally flip the outcome of a rights analysis.
sary and expected, the checkout flow presents a separate, unticked
                                                                        In legal reasoning, identity verification functions as a precondi-
box for marketing emails, which Anna leaves unchecked. A subset
                                                                        tion for execution and safe disclosure, not as a substantive limiter
of the facts, drafted by the Drafter Agent and having passed the
                                                                        on the existence of the Article 20 right itself. By contrast, in the
review stage of the Verifier Agents, is shown in Listing 3.
                                                                        formal representation, failure to satisfy identity_verified collapses
Listing 3: Formalized facts for the marketing-email purpose             the higher-level predicate art20_data_portability_right, even when
in the MediShip case.                                                   all substantive criteria are met. The result is a false negative: the
[
                                                                        right is treated as non-existent rather than temporarily pending
        " necessary_for_legitimate_interests " ,                        verification. This demonstrates that auto-formalization, while seem-
        " necessary_for_contract_performance " ,                        ingly straightforward, is sensitive to how procedural safeguards
        " necessary_for_legal_obligation " ,                            are encoded, and that human review is required to distinguish
        " rights_not_overriding_legitimate_interests "
                                                                        execution-related checks from conditions that genuinely negate a
]
                                                                        legal right.
                                                                        B.2.4     Inefficiencies in Formalized Rule Trees.
   Analysis. At a purely syntactic level, it may appear straight-
forward to auto-formalize the marketing-email processing under             Analysis. In some cases, although the generated rule trees and
GDPR Article 6(1)(f) by checking whether the controller asserts a       facts lead to legally correct outcomes, the rule trees themselves are
legitimate interest and provides an opt-out mechanism. However,         sometimes inefficiently formalized. For example, the rule formaliza-
the natural-language nuances of the case invalidate this formal         tion agent sometimes fails to distinguish between classical negation
pattern. The facts explicitly state that marketing is not necessary     and negation as failure, the latter of which is typically treated as an
for contract performance or legal compliance, and the unticked          exception. As a result, this confusion can produce inefficient rule
consent box signals that the data subject did not expect or agree       trees with unnecessary conditions, as illustrated in the following
to promotional use of her contact details. As a result, the predicate   example:
necessary_for_legitimate_interests is weakly supported at best, and               Listing 5: Example of unnecessary conditions.
the balancing predicate rights_not_overriding_legitimate_interests      {
is contradicted by the data subject’s expressed choice.                         "p" : " no_art9_exception " ,
                                                                                " op " : " ALL " ,
B.2.3     Misplacement of Identity Verification as a Condition.                 " conditions " : [ " no_vital_interests_basis " ,
                                                                                " no_nonprofit_basis " ,
   Case description. In the StrideSync scenario, Nina submits an
                                                                                " not_manifestly_public " ,
Article 20 data portability request covering both receipt of her                " no_legal_claims_basis " ,
data in a machine-readable format and direct transmission to a                  " no_substantial_public_interest " ,
competing controller. Substantively, the request concerns personal              " no_medicine_basis " ,
data relating to Nina, is processed by automated means, and is based            " no_public_health_basis " ,
                                                                                " no_research_archiving_basis " ] ,
on contract and consent. From a legal perspective, these elements               " exceptions " : []
place the request squarely within the scope of Article 20.              },

                                                                            Although the generated rule trees and facts can reach the legally
Listing 4: Excerpt of the rule tree where identity verification
                                                                        correct outcome because the facts explicitly include all conditions
is modeled as a condition.
                                                                        appearing in the rules, such as no_vital_interests_basis. This formal-
{
        "p" : " personal_data_concerns_requester " ,                    ization does not align with standard legal reasoning. In particular,
        " op " : " ALL " ,                                              no_vital_interests_basis should be assumed to hold by default unless
        " conditions " : [                                              its opposite, vital_interests_basis, is established. Treating such nega-
               " identity_verified " ,                                  tions as failure as explicit conditions with classical negations shifts
               " data_is_personal_data_of_requester "
        ],
                                                                        the burden of proof incorrectly and results in unnecessary fact
        " exceptions " : [ " request_is_for_third_party_data " ]        extraction, even though the same legal outcome could be achieved.
}                                                                           Meanwhile, the generated rule trees may contain unnecessary
                                                                        rule chains, as shown below:

   Formal modeling issue. Within the agent-generated rule tree, the              Listing 6: Example of an unnecessary rule chain.
predicate identity_verified is embedded as a mandatory condition        {
                                                                                "p" : " no_a9_exception_applies " ,
for establishing that the requested data concerns the requester.                " op " : " ALL " ,
While this reflects a legitimate procedural safeguard in practice,              " conditions " : [ " no_a9_grounds_true " ] ,
its placement in the logical structure causes the entire predicate              " exceptions " : []
GDPR Auto-Formalization with AI Agents and Human Verification


},                                                                           " info_presented_clearly " ,
{                                                                            " no_ambiguity_in_choice "
       " p " : " no_a9_grounds_true " ,                                  ]
       " op " : " ALL " ,
       " conditions " : [ " not_any_a9_ground_true " ] ,                 Listing 8: Example facts needed to align the representation
       " exceptions " : []                                               with the proposed change.
},
                                                                         [
{
                                                                             " consent_by_pre_ticked_boxes " ,
       " p " : " not_any_a9_ground_true " ,
                                                                             " withdrawal_harder_than_giving " ,
       " op " : " ALL " ,
                                                                             " insufficient_consent_record " ,
       " conditions " : [ . . . ] ,
                                                                             " cannot_link_subject_purpose_time_to_text_version "
       " exceptions " : []
                                                                         ]
},

   Listing 6 shows that, in order to derive no_a9_exception_applies,        Analysis. The False label is correct for the proposed change: pre-
the system must first prove the condition no_a9_grounds_true. To         ticked advertising consent violates the requirement of a clear affir-
establish no_a9_grounds_true, it then needs to prove not_any_a9_         mative action and triggers the pre-ticked-box invalidity; withdrawal
grounds_true. However, since there are no other rules that conclude      friction conflicts with Article 7(3); and omission of the consent
no_a9_grounds_true, the intermediate rule introducing this predi-        text version weakens demonstrability under Article 7(1). However,
cate is redundant and can be eliminated without affecting the final      because the extracted facts do not encode these change-specific vio-
outcome.                                                                 lations, evaluation can be driven toward the baseline configuration
   During the experiments, we also observed that agents sometimes        rather than the proposed change in question.
hack the formalization to achieve the labeled outcomes. For example,
the fact-extraction agent may extract no facts so that the derived
reasoning does not entail an outcome labeled as false. Furthermore,
we found that the logical-validation agent occasionally exceeds its
time limit during validation, indicating that reasoning over complex
logical structures remains challenging.
B.2.5 Fact Extraction Anchored to the Original Setting Rather Than
the Proposed Change.
   Case description. BrightFit GmbH offers two optional consent-
based purposes during onboarding, each controlled by an unticked
toggle and accompanied by purpose-specific information. In the
baseline design, users can proceed without enabling either toggle;
consent is logged with contextual metadata (including the consent
text version); and withdrawal is available via a simple settings con-
trol. The scenario then introduces a proposed change: pre-ticking the
advertising toggle, making withdrawal harder to locate, and weak-
ening records by storing only a timestamp. The yes/no question
asks whether these proposed changes comply with GDPR Article 7.
   Fact extraction inconsistency. Although the rule tree appropri-
ately models Article 7 requirements and invalid consent patterns,
the extracted facts primarily reflect the baseline compliant interface
rather than the proposed non-compliant change (Listing 7). In par-
ticular, predicates such as not_default_opt_in and consent_record_kept
remain present, while change-specific predicates that would ac-
tivate the relevant Article 7 failures are absent (Listing 8). This
misaligns the operative state described by the question with the
factual substrate used for evaluation.
Listing 7: Extracted facts reflect the original compliant inter-
face, not the proposed changes.
[
     " opt_in_action_recorded " ,
     " no_detriment_if_consent_refused " ,
     " separate_consent_for_separate_purposes " ,
     " consent_tied_to_specific_purpose " ,
     " not_default_opt_in " ,
     " data_subject_given_required_info " ,
     " consent_record_kept " ,
