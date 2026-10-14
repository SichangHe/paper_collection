                                                                                    Trustworthy AI Software Engineers
                                                                             Aldeida Aleti                                                                    Baishakhi Ray
                                                                         Monash University                                                                  Columbia University
                                                                              Australia                                                                            USA
                                                                     aldeida.aleti@monash.edu                                                              rayb@cs.columbia.edu

                                                                            Rashina Hoda                                                                        Simin Chen
                                                                        Monash University                                                                   Columbia University
                                                                             Australia                                                                            USA
                                                                    rashina.hoda@monash.edu                                                                sc5687@columbia.edu
                                        Abstract                                                                                        and RovoDev [28] demonstrate the feasibility of increasingly au-
arXiv:2602.06310v2 [cs.SE] 3 Jun 2026




                                        With the rapid rise of AI coding agents, the fundamental premise of                             tonomous Artificial Intelligence (AI) coding agents. These systems
                                        what it means to be a software engineer is in question. In this vision                          promise productivity gains by automating tasks that traditionally
                                        paper, we examine what it means for an AI agent to be considered a                              require substantial human effort [36]. Yet, despite significant tech-
                                        software engineer and then critically think about what makes such                               nical progress, their adoption in practice is tempered by persistent
                                        an agent trustworthy. Grounded in established definitions of SE (SE)                            skepticism regarding their trustworthiness [23]. Empirical evidence
                                        and informed by recent research on agentic AI systems, we concep-                               substantiates these concerns. Prior work shows that LLMs can
                                        tualise AI software engineers as participants in human-AI SE teams                              be untrustworthy [8, 29], misunderstand vulnerabilities [30], hal-
                                        composed of human software engineers and AI agents, and we                                      lucinate [31], memorise training data [4, 13], rely on biased fea-
                                        distinguish trustworthiness as a key property of these systems and                              tures [29], or generate syntactically correct yet semantically invalid
                                        actors rather than a subjective human attitude. Extending on histor-                            programs [27, 32]. These behaviours impact trust in coding agents.
                                        ical perspectives and emerging visions, we identify key dimensions                                  Addressing trustworthiness of AI software engineers first re-
                                        that contribute to the trustworthiness of AI software engineers,                                quires clarifying what it means to be a software engineer in the age
                                        spanning technical quality, transparency and accountability, epis-                              of AI. Established definitions from IEEE, ACM, and the SE Body of
                                        temic humility, and societal and ethical alignment. Beyond defining                             Knowledge (SWEBoK) characterise SE as far more than program-
                                        these dimensions, we address a critical but underexplored challenge:                            ming [10]. Empirical studies of professional practice consistently
                                        how trustworthiness can be operationalised in practice. We there-                               show that a substantial portion of day-to-day work involves non-
                                        fore introduce the notion of evidence-centric inspection, arguing                               coding activities such as eliciting and negotiating requirements,
                                        that developers should evaluate selective signals and justifications                            analysing specifications, reviewing and maintaining code, coordi-
                                        of trustworthiness rather than raw outputs, and we outline impli-                               nating with stakeholders, and documenting design decisions [15].
                                        cations for rethinking verification, validation, and code review in                             It is unclear how present day and emerging AI coding agents can
                                        human-AI SE teams.                                                                              account for socio-technical activities of SE beyond coding. These
                                                                                                                                        activities require judgment, communication, and accountability,
                                        ACM Reference Format:                                                                           among other social constructs. As AI capabilities advance, the role
                                        Aldeida Aleti, Baishakhi Ray, Rashina Hoda, and Simin Chen. 2026. Trust-
                                                                                                                                        of human engineers is shifting toward supervision, orchestration,
                                        worthy AI Software Engineers. In . ACM, New York, NY, USA, 5 pages.
                                                                                                                                        validation, and ethical oversight, raising fundamental questions
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn
                                                                                                                                        about the future of human–AI SE teams. To address this, we ask a
                                                                                                                                        fundamental question: What is an agentic engineer?
                                        1     Introduction                                                                                  Agentic software engineers offer the promise of automation, scal-
                                        Software engineering (SE) is undergoing a disruptive transforma-                                ability, and productivity gains. At the same time, the risks of uncrit-
                                        tion driven by the rapid emergence of Large Language Model                                      ical automation, i.e., automation without adequate understanding
                                        (LLM)-based agents capable of generating, repairing, and analysing                              of its risks and limitations, are substantial. If agentic software engi-
                                        code. Recent advances in agentic systems such as Claude Code [2],                               neers operate without clear behavioural boundaries, accountability
                                        Codex [19] and Kiro [12] and some of the earlier generation agents                              mechanisms, or ethical constraints, failures may become difficult
                                        including AutoCodeRover [35], SWE-agent [33], RepairAgent [3]                                   to diagnose and responsibility and accountability may be obscured.
                                                                                                                                        These tensions highlight the need for agentic engineers that are not
                                        Permission to make digital or hard copies of all or part of this work for personal or           only capable, but also trustworthy. This leads to a second funda-
                                        classroom use is granted without fee provided that copies are not made or distributed
                                        for profit or commercial advantage and that copies bear this notice and the full citation
                                                                                                                                        mental question: What characteristics should agentic engineers
                                        on the first page. Copyrights for components of this work owned by others than the              possess in order to be considered trustworthy?
                                        author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or              Trustworthiness extends beyond raw performance as measured
                                        republish, to post on servers or to redistribute to lists, requires prior specific permission
                                        and/or a fee. Request permissions from permissions@acm.org.                                     by lines of code, and previous work has introduced dimensions such
                                        Conference’17, Washington, DC, USA                                                              as fairness, robustness, transparency, generalization, explainability,
                                        © 2026 Copyright held by the owner/author(s). Publication rights licensed to ACM.               auditability, traceability, alignment with human values, and pri-
                                        ACM ISBN 978-x-xxxx-xxxx-x/YYYY/MM
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn                                                         vacy [14]. Although these dimensions are widely discussed in the
Conference’17, July 2017, Washington, DC, USA                                              Aldeida Aleti, Baishakhi Ray, Rashina Hoda, and Simin Chen


broader trustworthy AI literature, they have not yet been systemat-      activities and emphasize human-AI collaboration [10]. An agentic
ically grounded in the context of AI-based SE agents. Khati et al.       engineer must therefore be able to work not only independently,
[11] conceptualized trust in the context of SE through a systematic      but also in coordination with other AI agents and with human
literature review and identified three key attributes of trustwor-       software engineers, supporting a human-AI collaboration model
thiness for coding models: ability (measured in terms of accuracy,       rather than human replacement, akin to emerging paradigms such
efficiency, and reliability), benevolence (capturing alignment with      as the AI co-scientist [16]. An AI agent should be considered an AI
user and stakeholder goals), and integrity (relating to safe, secure,    software engineer only if it can assume responsibilities consistent
and ethical development practices). While this provides an impor-        with real-world SE practice: working in teams on socio-technical
tant foundation for understanding trust in AI-based coding support,      tasks spanning the SE lifecycle, under constraints and accountabil-
agentic systems extend beyond conventional coding models in both         ity [5, 6]. Recent SE visions emphasise that while AI is reshaping
scope and responsibility. Unlike tools that primarily generate or        the field, humans remain essential for quality, governance, and
complete code, agentic systems are expected to plan tasks, interact      value-sensitive decisions (e.g., Abrahão et al. [1]). Complementary
with tools and environments, make intermediate decisions, and            vision work argues that agentic SE cannot be defined solely in
collaborate with human teammates across the SE lifecycle. As a           terms of code, but must reflect SE foundations, values, and pro-
result, trustworthiness in agentic SE systems must be understood         cesses [10]. Grounded in these perspectives and recent evidence on
more broadly: not only in terms of the quality of their outputs, but     AI’s strengths and limits in realistic SE workflows [17], we identify
also in terms of the soundness of their decision-making processes,       four defining characteristics of an agentic software engineer.
their transparency and accountability, their ability to operate safely
under uncertainty, and their capacity to remain aligned with human           New Idea #1: For an AI agent to be considered an agentic
intentions, team norms, and organizational constraints.                   engineer, it must satisfy four conditions.
    Identifying dimensions of trustworthiness alone is insufficient          i) The agent must be capable of handling a range of SE tasks be-
to support their practical adoption. As agentic systems generate          yond coding such as evolving problem statements, requirements,
increasing volumes of code, it becomes infeasible for human devel-        constraints, ethics, design, testing and operations, requiring it-
opers to inspect everything. Requiring exhaustive human validation        erative refinement under partial information [7].
risks creating cognitive overload and review fatigue, ultimately lim-        ii) The agent must demonstrate agency through planning and
iting the effectiveness of human-AI SE teams. Developer fatigue           tool use, extending beyond code-centric tasks [10, 25].
from reviewing AI generated work is also a rising concern. This              iii) The agent must be collaborative. As SE is fundamentally
leads to a third fundamental question: What should developers             team-based, an agentic engineer must integrate into human
verify and validate when working with agentic software engi-              workflows by supporting coordination, feedback, and negotia-
neers? Addressing this question requires moving beyond abstract           tion [1, 10, 17].
notions of trustworthiness toward actionable practices that enable           iv) The agent must respect human values, constraints, and
developers to selectively inspect, interpret, and rely on AI-generated    ethical responsibility, It must justify decisions, and support ac-
artefacts. In this paper, we argue that this challenge necessitates       countability and oversight, consistent with ethics-by-design and
a shift from artefact-centric inspection toward evidence-centric          sustainability principles [10, 17].
inspection, where developers evaluate signals and justifications of
trustworthiness rather than raw outputs.                                     This working definition intentionally sets a higher bar than
    This vision paper aims to move the discourse beyond productivity-    “autonomous coding” or AI coding agents. It matches emerging
centric narratives of AI in SE, much of which is explicitly or implic-   evidence that real-world usefulness depends on interaction, context,
itly focused on AI replacing human software engineers, towards a         validation, and integration into socio-technical workflows [17], and
principled understanding of trustworthy human-AI SE teams.               it aligns with the push to frame agentic SE as beyond code, grounded
                                                                         in SE foundations, values, and shared vocabulary [10]
2    What is an Agentic Engineer?
Software Engineering (SE) extends beyond coding [10], hence an
                                                                         3   What Makes an Agentic Engineer
agentic engineer must go beyond coding and coding-related ac-                Trustworthy?
tivities. Although current AI agents demonstrate impressive profi-       Trust is a central construct in human-AI collaboration, yet it is
ciency in code generation, repair, and refactoring, SE encompasses       conceptually distinct from trustworthiness [20]. Trust refers to a
a broader range of activities, including requirements gathering          human decision or disposition to rely on an AI system in a given
(e.g., writing user stories), requirements analysis (e.g., analysing     context, while trustworthiness denotes the properties of the system
specifications for ambiguity or inconsistency), architectural design,    that justify such reliance [20]. The two are related but asymmetrical:
testing, and verification, and long-term maintenance and evolution.      humans may place trust in untrustworthy systems, and conversely,
Moreover, SE is a collaborative endeavour, a team effort. Recently,      trustworthy systems may fail to be trusted if their behaviour or
there has been a shift in the SE community from viewing AI agents        intentions are opaque. This distinction is particularly important
as isolated coding tools toward treating them as members of a            in SE, where inappropriate trust can lead to severe technical, or-
SE team [1, 9, 10, 22]. A set of comprehensive, responsible, adap-       ganisational, or societal harm, while insufficient trust may prevent
tive, foundational, translational (CRAFT) values and principles have     realising productivity benefits. We focus on trustworthiness as a
been proposed for agentic SE that expand its focus beyond coding         system property rather than on subjective trust alone.
Trustworthy AI Software Engineers                                                                        Conference’17, July 2017, Washington, DC, USA


    Prior studies of trust describe trust as a dynamic, living concept,    Performance and robustness further shape technical quality. Perfor-
one that can be gained, lost, or recalibrated, sometimes abruptly          mance includes response time, efficiency, scalability, and resilience
in response to failures or incidents [20, 24, 34]. Roychoudhury et         to denial-of-service-like behaviours, while robustness concerns cor-
al. [22] argue that the key barrier to the adoption of AI software en-     rect behaviour under invalid inputs or stressful conditions. Security
gineers is not organisational resistance but developer trust, shaped       is also critical, ensuring that systems resist misuse and vulnerabil-
by day-to-day interactions with AI agents in real workflows. Em-           ities. In addition, cost—spanning developer time, computational
pirical work further suggests that developers approach AI systems          resources, financial expense, and environmental impact-affects
with different default trust positions, shaped by experience, role,        whether systems remain practical and trustworthy at scale. Even
and values, rather than a uniform baseline of skepticism or opti-          a correct system may be untrustworthy if it is prohibitively slow,
mism [26]. These observations suggest that trustworthiness cannot          fragile, or resource-intensive.
be established once and for all; instead, it must support sustained, re-       Transparency and accountability enable responsible reliance. Trans-
calibrated trust relationships over time, including notions of mutual      parency and explainability concern whether stakeholders can un-
trust between human developers and AI agents.                              derstand how and why decisions are made. Traceability enables
    Importantly, no single dimension is both necessary and sufficient      linking outputs to inputs, models, and processes, while auditability
for trustworthiness. It is unlikely that any one dimension alone           and reproducibility support verification. Accountability requires
can guarantee trustworthiness, nor that the absence of a single            that actions and decisions can be justified to different audiences,
dimension always makes a system untrustworthy in all contexts.             ensuring that responsibility is clearly assigned and enforceable,
Rather, trustworthiness emerges from configurations of dimensions          while reproducibility refers to obtaining consistent results under
that collectively justify reliance in a given setting. This motivates      the same conditions. Epistemic humility captures the limits of AI
a multidimensional view that avoids oversimplification while still         knowledge. AI software engineers must communicate uncertainty,
providing structure.                                                       acknowledge limitations, and remain aware of potential biases.
                                                                           Without such humility, systems risk overconfidence, misuse, and
    New Idea #2: A multi-dimensional trustworthiness frame-                misplaced trust, particularly in complex or high-stakes settings.
 work for agentic engineers. we identify several key dimen-                Ethical alignment ensures consistency with human values [21]. This
 sions that are directly related to the trustworthiness of AI soft-        includes fairness, bias mitigation, privacy protection, regulatory
 ware engineers, as shown in Figure 1. These dimensions apply at           compliance, safety, and sustainability. These dimensions are critical
 different levels (system, model, and output) and matter to differ-        given the societal reach of software systems. Failures here may
 ent stakeholders (developers, organisations, and society), often          not be immediately visible at the code level, yet they can signifi-
 over both short- and long-term horizons. They are grounded                cantly erode trust over time. Trustworthiness is also shaped by ethical
 and extend prior work in trustworthy AI [23] and with ground-             alignment and socio-technical practice. Beyond individual systems,
 ing on SE quality models (e.g., SWEBoK), and recent work on               trust depends on how AI software engineers integrate into human
 trustworthiness in AI-assisted development [18].                          teams and broader contexts. Collaboration, alignment with team
                                                                           culture, and support for developer experience influence adoption
                                                                           and effective use. More broadly, societal impact, cultural sensitivity,
                                                                           and sustainability shape whether these systems are perceived as
                                                                           responsible participants in socio-technical ecosystems.


                                                                           4   What should developers verify and validate
                                                                               when working with agentic engineers?
                                                                           Given the key dimensions of trustworthiness introduced in the
                                                                           previous section, a critical open question remains unresolved: what
                                                                           should human developers actually verify and validate when work-
                                                                           ing with agentic software engineers? The trustworthiness dimen-
                                                                           sions are not always translated into actionable inspection practices
                                                                           in real-world SE workflows. Agentic systems generate increasingly
Figure 1: Multidimensional View of Trustworthiness in Agen-                large volumes of code and development artefacts and this gap be-
tic Engineers.                                                             comes more pronounced. Human developers cannot feasibly inspect
                                                                           everything, and requiring them to do so risks cognitive overload,
   Technical quality is foundational to trust. An AI software engi-        review fatigue, and ultimately a breakdown in effective human-
neer cannot be considered trustworthy if it frequently produces            AI collaboration. The challenge, therefore, is not only to define
incorrect results or behaves inconsistently. Correctness refers to         trustworthiness, but to make it inspectable under realistic human
whether outputs meet expected functional requirements, while               constraints.
reliability concerns the system’s ability to deliver acceptable re-           We conceptualise this challenge as a selective visibility problem.
sults consistently over time. These dimensions are often assessed          Agentic engineers operate through multi-step processes involving
using quantitative metrics at the model or output level, but their         planning, tool use, intermediate decisions, and iterative refinement.
implications extend to system-level trust in engineering workflows.        Exposing all intermediate artefacts and reasoning steps is neither
Conference’17, July 2017, Washington, DC, USA                                               Aldeida Aleti, Baishakhi Ray, Rashina Hoda, and Simin Chen


scalable nor useful for developers. Instead, trust must be supported         Taken together, these directions point toward a new class of
through carefully curated visibility into the agent’s behaviour.          tooling that does not simply analyse code, but actively mediates
                                                                          the interaction between human developers and agentic systems by
    New Idea #3: From Artefact-Centric to Evidence-Centric                shaping what is visible, explainable, and verifiable.
 Inspection. We propose a shift from artefact-centric inspection,            These challenges are particularly acute in the context of code
 where developers focus primarily on reviewing final outputs              review. Code review is inherently a socio-technical activity that
 such as code, toward evidence-centric inspection, where the              involves not only identifying defects, but also understanding design
 goal is to assess whether sufficient justification exists to rely on     intent, sharing knowledge, and coordinating team practices. With
 those outputs. In this view, developers do not need to see every-        the introduction of agentic systems, the nature of code review is
 thing; rather, they need to see the right things. These include          fundamentally altered. The volume of generated artefacts increases
 signals about whether the agent’s outputs align with require-            substantially, making exhaustive manual inspection impractical,
 ments and constraints, whether key decisions are grounded in             while the opacity of AI-generated outputs makes reasoning about
 defensible reasoning, and whether uncertainty, assumptions,              their correctness more difficult. As a result, code review risks be-
 and potential failure modes are explicitly communicated. Trust-          coming a bottleneck in human-AI teams.
 worthiness, therefore, becomes a property not only of what the
 system produces, but of what it chooses to reveal.                           New Idea #5: Code Review as Runtime Monitoring. We
                                                                           propose that in human-AI software engineering teams, code
   This shift in perspective has implications for how verification and
                                                                           review should extend beyond pre-merge inspection and become
validation (V&V) are understood in the context of agentic engineers.
                                                                           a continuous, runtime activity. Deployed code is not considered
Traditionally, verification concerns whether a system has been built
                                                                           final, but provisional. AI agents continuously monitor system
correctly, and validation concerns whether the right system has
                                                                           behaviour in production, evaluating execution traces, resource
been built. In human-AI settings, these notions must be extended
                                                                           usage, security signals, and deviations from expected behaviour.
to account for the processes through which artefacts are generated.
                                                                           This reframes code review as a continuous assurance mechanism
Developers must reason not only about the correctness of out-
                                                                           embedded within the system lifecycle, where trustworthiness is
puts, but also about the soundness of the agent’s decision-making
                                                                           established through sustained behavioural validation. As a result,
processes and its interpretation of human intent. This introduces
                                                                           review becomes temporally distributed, adaptive, and tightly
additional layers of verification, including process-level verifica-
                                                                           coupled with system operation, fundamentally dissolving the
tion, which concerns whether the agent’s planning and tool use are
                                                                           boundary between development and deployment.
appropriate, and epistemic verification, which concerns whether
the agent accurately represents its own uncertainty and limitations.
Validation similarly extends beyond outputs to include whether               This perspective highlights a key research gap: the need to trans-
the agent’s behaviour remains aligned with evolving requirements          late abstract dimensions of trustworthiness into concrete, developer-
and constraints. As a result, V&V becomes a multi-level activity          facing interfaces and workflows. While prior work has identified
spanning outputs, processes, and context. Supporting this form of         what properties trustworthy systems should exhibit, significantly
verification requires new theory, techniques and tools that are ex-       less attention has been paid to how these properties are opera-
plicitly focused for developer-facing inspection of trustworthiness.      tionalised in practice, particularly in the context of human–AI col-
While traditional approaches such as testing and static analysis          laboration.
remain necessary, they are insufficient in isolation because they
operate primarily at the level of final artefacts. In contrast, agentic        New Idea #6: From Trustworthiness Properties to Trust
systems require mechanisms that can summarise, structure, and              Interfaces. Designing effective trust interfaces requires un-
expose relevant aspects of their internal processes and decisions.         derstanding not only what information to present, but also
                                                                           when and how to present it in ways that align with developer
     New Idea #4: Rethinking Verification and Validation.                  workflows and cognitive constraints. Without such mechanisms,
 One promising direction is the development of techniques that             human–AI SE teams face a fundamental trade-off between ex-
 distil large volumes of agent activity into concise, meaning-             haustive verification, which is infeasible at scale, and uncritical
 ful representations that highlight key decisions, assumptions,            reliance, which risks misplaced trust. Bridging this gap is es-
 and risks. Traceability mechanisms can further support this by            sential for enabling agentic software engineers to be not only
 linking generated artefacts back to requirements, inputs, and             technically capable, but meaningfully trustworthy in practice.
 intermediate steps, enabling developers to reconstruct how a
 particular outcome was produced. Additionally, systems that ex-          5   Conclusion
 plicitly surface uncertainty, alternative solutions, or known limi-
                                                                          This paper defined key requirements for AI agents to qualify as
 tations can help developers calibrate their trust more effectively.
                                                                          agentic software engineers and introduced key dimensions under-
 Emerging work on automated trustworthiness oracles [18] sug-
                                                                          pinning their trustworthiness. Beyond defining these dimensions,
 gests that it may be possible to automatically generate checks
                                                                          we addressed a critical and underexplored challenge: how trust-
 for properties such as robustness, fairness, or security, thereby
                                                                          worthiness can be operationalised in practice. In particular, we
 guiding developers toward the aspects of a system that warrant
                                                                          posed the question of what developers should verify and validate
 closer inspection.
                                                                          when working with agentic software engineers. We argued that
Trustworthy AI Software Engineers                                                                                                   Conference’17, July 2017, Washington, DC, USA


the scale and complexity of AI-generated artefacts render exhaus-                              [18] Nguyen Tung, L., Cho, S., Du, X., Neelofar, N., Terragni, V., Ruberto, S., and
tive inspection infeasible, and that trustworthiness must instead be                                Aleti, A. Automated trustworthiness oracle generation for machine learning
                                                                                                    text classifiers. Proceedings of the ACM on Software Engineering 2, FSE (2025),
made inspectable through selective, developer-facing evidence. To                                   2382–2405.
this end, we introduced the notion of evidence-centric inspection                              [19] OpenAI. openai/codex: Lightweight coding agent that runs in your terminal.
                                                                                                    https://github.com/openai/codex, 2025.
and outlined implications for rethinking verification and validation                           [20] Pink, S., Quilty, E., Grundy, J., and Hoda, R. Trust, artificial intelligence and
as multi-level activities spanning outputs, processes, and context, as                              software practitioners: an interdisciplinary agenda. AI & SOCIETY 40, 2 (2025),
well as for evolving code review into a computationally supported,                                  639–652.
                                                                                               [21] Rokeach, M. Understanding human values. Simon and Schuster, 2008.
human–AI collaborative practice. We further argued that trustwor-                              [22] Roychoudhury, A., Pasareanu, C., Pradel, M., and Ray, B. Agentic ai software
thiness emerges from configurations of dimensions in context, not                                   engineer: Programming with trust. arXiv preprint arXiv:2502.13767 (2025).
from any single property. Accordingly, we advocate for continu-                                [23] Roychoudhury, A., Păsăreanu, C., Pradel, M., and Ray, B. Agentic ai software
                                                                                                    engineers: Programming with trust. Communications of ACM 69, 5 (Apr. 2026),
ous, context-sensitive assessment and identify the trustworthiness                                  56–58.
measurement gap as a key challenge. We call for future empirical                               [24] Salehi Fathabadi, A., and Leonard, P. " trust equals less death-it’s as simple
                                                                                                    as that": Developing a socio-technical framework for trustworthy defence and
and design-oriented research on trust-aware development prac-                                       security automated systems. In Proceedings of the Second International Symposium
tices, verification strategies, and human-AI collaboration models to                                on Trustworthy Autonomous Systems (2024), pp. 1–10.
enable appropriate and scalable trust in agentic SE systems.                                   [25] Sapkota, R., Roumeliotis, K. I., and Karkee, M. Ai agents vs. agentic ai: A con-
                                                                                                    ceptual taxonomy, applications and challenges. arXiv preprint arXiv:2505.10468
                                                                                                    (2025).
6     Data Availability                                                                        [26] Spiegler, S., Hoda, R., and Pant, A. Images of AI: How AI practitioners view
                                                                                                    the impact of artificial intelligence on society, now and in the future. Technology
There are no data available yet.                                                                    in Society (2025), 103109.
                                                                                               [27] Tan, H., Luo, Q., Jiang, L., Zhan, Z., Li, J., Zhang, H., and Zhang, Y. Prompt-
                                                                                                    based code completion via multi-retrieval augmented generation. ACM Transac-
References                                                                                          tions on Software Engineering and Methodology (2024).
 [1] Abrahão, S., Grundy, J., Pezzè, M., Storey, M.-A., and Tamburri, D. A. Software           [28] Tantithamthavorn, K., Zou, Y., Wong, A., Gupta, M., Wang, Z., Buller, M.,
     engineering by and for humans in an ai era. ACM Transactions on Software                       Jiang, R., Watson, M., Jeong, M., Chen, K., et al. Rovodev code reviewer: A
     Engineering and Methodology 34, 5 (2025), 1–46.                                                large-scale online evaluation of llm-based code review automation at atlassian.
 [2] Anthropic. Claude code overview. https://code.claude.com/docs/en/overview,                     arXiv preprint arXiv:2601.01129 (2026).
     2025.                                                                                     [29] Turpin, M., Michael, J., Perez, E., and Bowman, S. Language models don’t
 [3] Bouzenia, I., Devanbu, P., and Pradel, M. Repairagent: An autonomous, llm-                     always say what they think: Unfaithful explanations in chain-of-thought prompt-
     based agent for program repair. In 2025 IEEE/ACM 47th International Conference                 ing. Advances in Neural Information Processing Systems 36 (2023), 74952–74965.
     on Software Engineering (ICSE) (2025), IEEE Computer Society, pp. 694–694.                [30] Ullah, S., Han, M., Pujar, S., Pearce, H., Coskun, A., and Stringhini, G.
 [4] Chen, S., Pusarla, P., and Ray, B. DyCodeEval: Dynamic benchmarking of                         Llms cannot reliably identify and reason about security vulnerabilities (yet?): A
     reasoning capabilities in code large language models under data contamination. In              comprehensive evaluation, framework, and benchmarks. In 2024 IEEE symposium
     Forty-second International Conference on Machine Learning, ICML 2025, Vancouver,               on security and privacy (SP) (2024), IEEE, pp. 862–880.
     BC, Canada, July 13-19, 2025 (2025).                                                      [31] Wang, C., Zhang, J., Gao, J., Xia, L., Guan, Z., and Chen, Z. Contracttinker: Llm-
 [5] Dam, H. K., Mahala, G., Hoda, R., Zheng, X., and Conati, C. Towards au-                        empowered vulnerability repair for real-world smart contracts. In Proceedings of
     tonomous normative multi-agent systems for human-ai software engineering                       the 39th IEEE/ACM International Conference on Automated Software Engineering
     teams. arXiv preprint arXiv:2512.02329 (2025).                                                 (2024), pp. 2350–2353.
 [6] Donta, P. K., Saleh, A., Li, Y., Vaishnav, S., Fang, K., Feng, H., Xia, Y.,               [32] Wang, Z., Zhou, Z., Song, D., Huang, Y., Chen, S., Ma, L., and Zhang, T.
     Gadekallu, T. R., Zhang, Q., Shi, X., et al. Socio-technical aspects of agentic                Towards understanding the characteristics of code generation errors made by
     ai. arXiv preprint arXiv:2601.06064 (2025).                                                    large language models. In 2025 IEEE/ACM 47th International Conference on
 [7] Fakhoury, S., Naik, A., Sakkas, G., Chakraborty, S., and Lahiri, S. K. Llm-                    Software Engineering (ICSE) (2025), IEEE Computer Society, pp. 717–717.
     based test-driven interactive code generation: User study and empirical evalua-           [33] Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., and
     tion. IEEE Transactions on Software Engineering (2024).                                        Press, O. Swe-agent: Agent-computer interfaces enable automated software
 [8] Gong, J., Duan, N., Tao, Z., Gong, Z., Yuan, Y., and Huang, M. How well do                     engineering. Advances in Neural Information Processing Systems 37 (2024), 50528–
     large language models serve as end-to-end secure code producers? arXiv preprint                50652.
     arXiv:2408.10495 (2024).                                                                  [34] Yang, X. J., Schemanske, C., and Searle, C. Toward quantifying trust dynam-
 [9] Hassan, A. E., Li, H., Lin, D., Adams, B., Chen, T.-H., Kashiwa, Y., and Qiu,                  ics: How people adjust their trust after moment-to-moment interaction with
     D. Agentic software engineering: Foundational pillars and a research roadmap.                  automation. Human Factors 65, 5 (2023), 862–878.
     arXiv preprint arXiv:2509.06216 (2025).                                                   [35] Zhang, Y., Ruan, H., Fan, Z., and Roychoudhury, A. Autocoderover: Au-
[10] Hoda, R. Toward agentic software engineering beyond code: Framing vision,                      tonomous program improvement. In Proceedings of the 33rd ACM SIGSOFT
     values, and vocabulary. In Proceedings of the 2026 IEEE/ACM 48th International                 International Symposium on Software Testing and Analysis (2024), pp. 1592–1604.
     Conference on Software Engineering: Companion Proceedings (2026).                         [36] Ziegler, A., Kalliamvakou, E., Li, X. A., Rice, A., Rifkin, D., Simister, S.,
[11] Khati, D., Liu, Y., Palacio, D. N., Zhang, Y., and Poshyvanyk, D. Mapping                      Sittampalam, G., and Aftandilian, E. Measuring github copilot’s impact on
     the trust terrain: Llms in software engineering-insights and perspectives. ACM                 productivity. Communications of the ACM 67, 3 (2024), 54–63.
     Transactions on Software Engineering and Methodology (2025).
[12] kirodotdev. kirodotdev/Kiro: Kiro — an agentic ide that works alongside you
     from prototype to production. https://github.com/kirodotdev/Kiro, 2025.
[13] Kong, J., Xie, X., and Liu, S. Demystifying memorization in llm-based program
     repair via a general hypothesis testing framework. Proceedings of the ACM on
     Software Engineering 2, FSE (2025), 2712–2734.
[14] Li, B., Qi, P., Liu, B., Di, S., Liu, J., Pei, J., Yi, J., and Zhou, B. Trustworthy ai:
     From principles to practices. ACM Computing Surveys 55, 9 (2023), 1–46.
[15] Meyer, A. N., Barr, E. T., Bird, C., and Zimmermann, T. Today was a good day:
     The daily life of software developers. IEEE Transactions on Software Engineering
     47, 5 (2021), 863–880.
[16] Moons, P., Dou, B., and Desmedt, C. P. Google’s ai co-scientist and openai’s deep
     research: new partners in health research? European Journal of Cardiovascular
     Nursing 24, 5 (2025), 800–807.
[17] Murali, V., Maddila, C., Ahmad, I., Bolin, M., Cheng, D., Ghorbani, N., Fer-
     nandez, R., Nagappan, N., and Rigby, P. C. Ai-assisted code authoring at scale:
     Fine-tuning, deploying, and mixed methods evaluation. Proceedings of the ACM
     on Software Engineering 1, FSE (2024), 1066–1085.
