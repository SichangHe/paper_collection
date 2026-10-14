                                                     A Unit Proofing Framework for Code-level
                                                         Verification: A Research Agenda
                                            Paschal C. Amusuo              Parth V. Patil              Owen Cochell               Taylor Le Lievre         James C. Davis
                                               Purdue University          Purdue University       Michigan State University        Purdue University       Purdue University



                                            Abstract—Formal verification provides mathematical guaran-           of unit proofs. In §III, we assessed 11 unit proofs used to verify
                                         tees that a software is correct. Design-level verification tools        a widely-used operating system. Although 5 of them correctly
                                         ensure software specifications are correct, but they do not expose      caught severe defects, 6 had faults that obscured others.
                                         defects in actual implementations. For this purpose, engineers
arXiv:2410.14818v2 [cs.SE] 30 Apr 2025




                                         use code-level tools. However, such tools struggle to scale to             We believe that empirically-based guidelines and enhanced
                                         large software. The process of “Unit Proofing” mitigates this           tool support will make unit proofing easier and enable early
                                         by decomposing the software and verifying each unit indepen-            discovery of code-level defects. We propose a research agenda
                                         dently. We examined AWS’s use of unit proofing and observed             for a principled end-to-end unit proofing framework that can
                                         that current approaches are manual and prone to faults that             support software engineers in each stage of the unit proofing
                                         mask severe defects. We propose a research agenda for a unit
                                         proofing framework, both methods and tools, to support software         process. The proposed framework comprises of methods and
                                         engineers in applying unit proofing effectively and efficiently. This   tools and will help software engineers decompose a software
                                         will enable engineers to discover code-level defects early.             into optimal verifiable units, develop correct unit proofs for
                                            Index Terms—Vision, Formal methods, Empirical software eng.          each unit, validate and repair faulty unit proofs, and ensure
                                                               I. I NTRODUCTION                                  unit proofs are updated as the software evolves. We identify
                                            Software underlies many critical digital and cyber-physical          eight open questions that will need to be addressed, and share
                                         systems. Code-level defects, such as arithmetic errors and              our future plans to this end. If the proposed unit proofing
                                         memory corruption vulnerabilities, compromise system safety             framework helps software engineers verify their software code
                                         and security and cause significant losses [1]. For example,             during development, then it will disrupt existing defect-finding
                                         a null-pointer bug in CrowdStrike Falcon in 2024 impacted               practices such as static analysis, unit testing, and fuzzing.
                                         global transportation systems and caused over $5 billion in
                                         damages [2]. Traditional engineering practices, such as test-
                                         ing [3], [4], program analysis [5], and runtime sandboxing
                                         [6], can detect or mitigate such defects. However, these
                                         methods validate software only approximately and cannot
                                         guarantee correct behavior on all inputs. In contrast, formal
                                         verification [7] proves software correctness, guaranteeing no
                                         code-level defects. This raises an important (and perennial)
                                         question [8]: how to make formal verification more cost-
                                         effective for software engineers?
                                            Engineering tools and processes help reduce the cost of
                                         applying a technology. For formal methods, there are code-              Fig. 1: Overview of Unit Proofing. To verify function 2,
                                         level verification tools, e.g., the C and Rust bounded model            an engineer models its input, shared resources, and other
                                         checkers (CBMC [9], Kani [10]). To improve both engineering             functions. A verifier can then check it in isolation.
                                         and tool scalability, engineers decompose the software and
                                         verify individual functions within it via unit proofs [11].               II. C ODE - LEVEL V ERIFICATION AND U NIT P ROOFING
                                         These unit proofs model the function’s interaction with other             This section introduces code-level verification (CLV) and
                                         software components and verify the function using this model.           unit proofing as a process for applying CLV on large software.
                                         We refer to the process of developing, using, and maintaining
                                         unit proofs as unit proofing. Organizations such as AWS [12]            A. Formally Verifying Software Implementations
                                         and ARM [13] have adopted unit proofing to ensure software                 Many tools verify software implementations using a variety
                                         correctness and memory safety.                                          of formal methods [9], [15], [16]. This paper focuses on tools
                                            Since code-level verification depends on the unit proofs,            that use Bounded Model Checking (BMC) [17] as they require
                                         they must be correct. However, there is limited guidance and            the least human effort [18], can automatically verify properties
                                         tool support for constructing unit proofs. Existing guidelines          like memory safety, and are being adopted by major software
                                         are ad hoc and require expertise [14]. There is little publicly-        organizations [12], [13]. We refer the reader to other works
                                         available tool support, leading to costly manual development            for comparisons of such tools [18], [19].
                                                                         Table I: Assessing unit proofs on known vulnerabilities. Only
 1   int MODEL_get_max_len() { return rand(); }
 2                                                                       5 of the 11 vulnerabilities were exposed by the existing
 3   char* get_ipv6_str(char *ipv6_str, uint8 *buffer) {                 FreeRTOS unit proofs. UP: Unit Proofing.
 4       assume(valid_pointer(ipv6_str));
 5       struct in6_addr ipv6_addr;
 6       memcpy(&ipv6_addr, buffer, 16);                                   Recreated Vuln   Exposed        Reason            UP Stage
 7       assert(buffer != NULL);
 8       assert(sizeof(buffer) >= 16);
                                                                          CVE-2018-16523      No       Insuff. properties     Design
 9       int max_len = MODEL_get_max_len();                               CVE-2018-16524      No      Function Modeling     Development
10       ... // logic to convert buffer to IPv6 string                    CVE-2018-16525      No       Out-of-date Proofs   Maintenance
11       assert(valid_ipv6(ipv6_str));                                    CVE-2018-16527      No      Insuff. Input Model   Development
12   }                                                                    CVE-2018-16600      No      Insuff. Input Model   Development
                                                                          CVE-2018-16603      No      Insuff. Input Model   Development
Listing 1: Verifying function implementations with a unit proof.          CVE-2021-31571     Yes              —                 —
Developers can specify functional properties (blue) and provide a         CVE-2018-16526     Yes              —                 —
model for a called function. Tools can introduce program-agnostic         CVE-2018-16599     Yes              —                 —
properties (red). Verification tools check that these properties hold.    CVE-2018-16601     Yes              —                 —
                                                                          CVE-2018-16602     Yes              —                 —

   Bounded Model Checkers (BMCs) verify software correct-
ness by ensuring all program states satisfy specific properties          compositional bounded model checking on real software [24],
within a bound (e.g., up to loop iteration count or recursion            [25] and abstract software models [26], [27]. We focus on unit
depth) [17]. As Listing 1 shows, properties may be defined               proofing due to its adoption by major software companies,
by developers (blue) or generated (red). BMC tools translate             including AWS and ARM.
the software and properties to formal logic and use constraint
solvers to verify the properties in all program states [20].                   III. E XPLORATORY S TUDY OF U NIT P ROOFING
   BMC has been applied in both industry (e.g., AWS li-                     Many questions arise when considering any engineer-
braries [12], ARM confidential computing firmware [13])                  ing process, such as “Does it work?” and “What does it
and open-source projects (e.g., Firecracker, Hifitime, S2N-              cost?” [28]. While there are empirical evaluations of code-
Quic [21]). Beyer et al. [22] report that BMC tools find                 level tools on software benchmarks [22], no studies address
significantly more bugs in less time compared to testing                 their effectiveness on real software or within the unit
and fuzzing tools. However, BMC struggles with state space               proofing process. As a first step, we ask:
explosions when applied to large software systems.                       RQ: Do engineers’ typical unit proofs expose targeted defects?
B. Unit Proofing for Enabling Code-level Verification                       We evaluated this question using FreeRTOS unit proofs and
   To apply BMC tools in practice, several papers have de-               reported vulnerabilities (CVEs). FreeRTOS was chosen due
scribed similar engineering processes [12], [13]. One example            to its widespread use and available unit proofs [29]. CVEs
is AWS’s verification of embedded software and data structure            were used as they typically reflect critical memory safety
libraries [12]. In their process, engineers develop unit proofs          vulnerabilities, which the unit proofs intend to address [29].
and use them to verify individual functions in the software.
                                                                         A. Methodology
We refer to this process as “Unit Proofing”.
   Unit proofing comprise four stages. (1) Software is first                Dataset: We collected all 21 CVEs affecting FreeRTOS
decomposed into manageable units. (2) Unit proofs are then               from the National Vuln. Database (NVD) as of March 2024.
created to configure verification and model the unit’s envi-             We selected those affecting memory safety with sufficient
ronment, including input, resources, and undefined functions             details for reproduction, yielding 11 CVEs. For each, we
(Figure 1). (3) Initial proofs may include misconfigurations,            identified the affected function and the associated unit proofs.
inaccurate input or function models, causing prolonged veri-                Vulnerability Recreation: Following the vulnerability de-
fication, low coverage, or false positives and negatives. These          scription, we removed any input validations introduced in
faults are investigated and the proofs repaired. (4) Finally, as         the function that fixed the vulnerability. Attempts to build
software evolves, proofs must be updated to remain aligned               and evaluate versions that predate the vulnerability fix failed,
with their respective units. Manually completing these steps,            mostly due to unavailable or incompatible dependencies.
as reported by Chong et al. [12], is costly and error-prone.                Unit Proof Assessment: We executed the unit proofs using
   Unit proofing shares similarities with unit testing and com-          CBMC v5.95.1 and assessed whether the vulnerability was
positional verification. Like unit tests, AWS’s unit proofs are          reported. If not, we repaired the unit proofs as needed.
developed together with the software, stored in the same repos-
itory, and executed in continuous integration workflows [12].            B. Results
However, unit tests check correctness on specific inputs, while            Only 5/11 recreated vulnerabilities were exposed by FreeR-
unit proofs verify correctness across all possible inputs within         TOS unit proofs (Table I). With changes to the unit proofs, all
the model [23]. Compared with compositional verification,                vulnerabilities were exposed and one new high-severity vul-
unit proofing is an engineering process that enables composi-            nerability found (CVE-2024-38373). Unit proofs are effective,
tional bounded model checking. There are works that automate             but unit proof engineers can err.
                                                                                  maintain unit proofs for accurate code-level verification. We
                                                                                  first outline the goals of each proofing stage and identify open
                                                                                  research questions. Then, we present the framework’s design
                                                                                  (Figure 2) and concrete research plans for implementation.
                                                                                  Once completed, the tools will be integrated into standard
                                                                                  software engineering workflows, facilitating early detection of
                                                                                  code-level defects.

                                                                                  A. Unit Proofing Stages and Open Questions
                                                                                    Here, we discuss the unit proofing stages introduced in §II-B
Fig. 2: An end-to-end agenda for unit proof engineering.                          and identify Open Questions (OQs) within them.
Software engineers use a set of tools and intelligent agents                      Software Decomposition: The goal here is to minimize unit
to verify the memory safety of applications.                                      proofing effort but ensure each unit is solvable.

C. Observations on Unit Proofing Failures                                          OQ1: How can we estimate a function’s verification time
                                                                                   and UP effort?
   There were four reasons for the unit proofing failures.
                                                                                   OQ2: How should a software be decomposed optimally?
   1) Insufficient Verification Properties (CVE-2018-16523):
BMC tools can verify program-agnostic properties, but require                       Unit proofing involves decomposing software into function
the properties to be enabled. The unit proof for CVE-2018-                        units and verifying each one. The decomposition strategy
16523, a division-by-zero defect, missed the issue because the                    impacts the number of unit proofs, the complexity of their
division-by-zero property was disabled 1 . The rationale behind                   models, and verification tractability. Smaller units are solvable
disabling specific correctness checks remains unclear.                            but require creating more unit proofs to cover the software.
   2) Insufficient Input Modeling (e.g., CVE-2018-16527):                         Additionally, the effort to create a unit proof depend on the
Unit proofs must model inputs broadly enough to cover all                         complexity of the models it requires. Units with complex
call sites yet precisely enough to avoid false positives. CVE-                    input structures or that access multiple shared resources may
2018-16527 only occurs when the header of the input packet is                     require more effort to create unit proof models. Hence, an
truncated. The unit proof for the affected function incorrectly                   optimal decomposition should minimize unit proofing efforts
assumed the input packet always contained the header.                             but ensure all units are solvable.
   3) Insufficient Function Modeling (CVE-2018-16524): To
simplify verification, unit proofs use function models to re-                     Unit Proof Design and Development: The goal here is to learn
place specific called functions, retaining essential behaviors                    how to develop correct unit proofing models for functions with
and properties. In CVE-2018-16524, an out-of-bound pointer                        complex interactions with other software components.
computed in the verified function was only accessed in a re-
                                                                                   OQ3: How can we generate correct unit proof models?
placed function. The replaced function’s model failed to check
the pointer’s validity, leaving the vulnerability undetected.                        Unit proofs require models of a function’s inputs, shared
   4) Out-of-date Unit Proofs (CVE-2018-16525): The vulner-                       resources, and replaced functions. The complexity of these
able function’s signature was changed but the new signature                       models depends on the complexity of interactions within
was not propagated to the unit proof. As CBMC supported                           the software. The accuracy of the models affects verification
making calls to undefined functions and only reported cover-                      properties such as coverage, soundness and completeness.
age on the reachable lines of code, the updated function was                      Under-constrained models are easy to develop but lead to false
no longer verified. When we fixed this unit proof, we exposed                     positives [30]. Conversely, over-constrained models hinder bug
and reported a new vulnerability 2 .                                              detection (§III). The modeling complexity is increased in
 Summary of Findings: The default unit proofs only                                stateful software where shared state variables can be influenced
 exposed 5/11 vulnerabilities. When fixed, all 11 CVEs were                       by the function’s callers and other functions in the software.
 exposed. The gaps were caused by insufficient properties,                        Unit Proof Validation and Repair: The goal here is to learn
 insufficient modelling, and out-of-date proofs.                                  how to investigate and repair faults within unit proofs.

                                                                                   OQ4: How do unit proof faults prevent defect exposure?
IV. R ESEARCH AGENDA : A U NIT P ROOFING F RAMEWORK                                OQ5: How can we repair faulty unit proofs?
  This section proposes a unit proofing framework, compris-
ing four novel tools, to help software engineers develop and                         Faulty unit proof models or configurations can produce low
                                                                                  coverage, false positives or prevent defect exposure. Fixing
  1 From CBMC v6, this property is enabled by default.
  2 In response to our disclosure, CBMC’s default behavior for undefined
                                                                                  these faults requires understanding the different kinds of faults,
functions was changed to report errors instead of warnings. See https://github.   how they manifest and how they affect verification. Addition-
com/diffblue/cbmc/pull/8292.                                                      ally, fixing unit proof faults still rely on the developer expertise
and experience as existing unit proofing guidelines [31] do not     detection abilities, and identifying necessary interventions for
provide specific interventions for fixing faults.                   different faults. Investigating and fixing proof faults requires
Unit Proof Evolution and Maintenance: The goal here is to           a deep understanding of program semantics. Hence, using the
automatically update unit proofs as the software changes.           developed taxonomy, the repairer will detect faults by com-
                                                                    bining the fast but imprecise program analysis techniques the
 OQ7: How do software changes affect unit proofs?                   code reasoning abilities of large language models (LLMs) [39],
 OQ8: What is the minimum unit proof change required to             [40]. We will explore two hybrid approaches: one using
 reverify a changed software?                                       search-based repairs with LLMs as a fallback for precision,
                                                                    and another enhancing repair tools with insights from LLMs.
   Software evolves, and §III shows that failing to update unit     Both approaches will be evaluated for effectiveness.
proofs leads to incorrect verification. Since unit proofs verify       4) Proof Updater: The proposed proof updater will keep
interacting functions, changes in one proof can invalidate          unit proofs synchronized with software changes. When the
others. Frequent software changes can make it impractical           software changes, the updater will identify affected unit proofs,
to regenerate or validate unit proofs after every change [12].      assess their validity, and apply necessary updates. An empirical
Understanding how software changes will affect unit proofs,         study will examine how software changes impact proofs, what
and repairing misaligned unit proofs, will ensure unit proofs       invalidates them, and how they are fixed. To validate updates,
remain consistent with the software.                                the updater will reverify affected functions, comparing results
                                                                    with prior data using metrics like coverage and violation
B. The Unit Proofing Framework Design                               reports. Initially, the proof repairer (§IV-B3) will be used
   Here, we present concrete research plans for actualizing         to resolve invalidated proofs. In future iterations, we plan to
each component of the proposed framework.                           develop an LLM agent that, informed by empirical insights,
   1) Software Decomposer: This tool will employ novel              can propose specific updates to the proof that realigns it with
algorithms to minimize unit count while ensuring verification       the changed software.
completes within a set time. This requires new methods to
                                                                                          V. F UTURE P LANS
estimate model complexity and verification time. Building on
research linking program features to specification size and         Ongoing Work: We have two active efforts towards the proof
effort [32], [33], we will analyze unit proofs to understand how    builder and proof repairer.
program features influence complexity and duration. These in-          First, we are evaluating the effectiveness and cost of the
sights will guide a cost estimator design that evaluates function   property-violation guided learning approach for the proof
features to estimate complexity and verification time and a         builder by manually developing unit proofs for functions in
decomposer algorithm to iteratively replace the most expensive      four selected software, identifying necessary interventions for
functions with models. We will also explore a bottom-up             coverage gaps and property violations, and assessing defect
approach using graph decomposition algorithms [34], [35] to         classes exposed by the unit proofs. Insights from this study
partition call graphs, balancing verification time and modeling     have been used to refine unit proof development guidelines.
complexity to minimize overall costs.                                  Second, we are leveraging program analysis and LLMs to
   2) Proof Builder: A unit proof requires sound and complete       automate proof building and repair. The proof repairer uses
models for accurate verification. In stateful systems or those      fault insights and interventions from the first study to fix
using shared resources, the resource model also depends on          generic unit proofs. We plan to assess the accuracy of the
prior execution sequences. Traditional learning-based assume-       developed proofs against manually developed ones and their
guarantee reasoning [36], [37] refines assumptions iteratively      performance in developing proofs for new software.
using counterexamples, but applying this to functions with          Longer-Term: Our research agenda will take many people
multiple interactions is costly due to the need for repeated        many years. We invite the software engineering research
model checking [38]. To address this, we propose to use             community to join us. Together, we can develop a world where
a property-violation guided learning approach, starting with        every function is verified as it is being written.
generic proof models and refining the models only until
all reachable code is covered and reported violations are                                 VI. C ONCLUSION
resolved. Refinements will be informed by interventions from           In this paper, we present a research agenda for a unit
the proof repairer (§IV-B3). The learned models will then be        proofing framework that will enable engineers verify their
propagated as assertions to the respective components, with         software implementations. The framework is motivated by our
violations indicating defects. This approach will also help         exploratory study of AWS’s unit proofs. It comprises tools and
indicate specific execution paths that trigger a defect.            methods to decompose a software, develop and repair unit
   3) Proof Repairer: The proof repairer will detect faults         proofs, and keep proofs updated as the software evolves.
in unit proofs and intelligently suggest fixes. To design the          Acknowledgement: This project is being supported by a
repairer, we will develop a taxonomy of unit proof faults and       Rolls Royce research grant.
interventions by empirically studying existing and new unit            Data availability: Our artifact contains the data for §III. See
proofs, assessing their coverage, violation reports, and bug        https://doi.org/10.5281/zenodo.14660073.
                               R EFERENCES                                         [22] Dirk Beyer and Thomas Lemberger. Software verification: Testing vs.
                                                                                        model checking. In Hardware and Software: Verification and Testing.
 [1] Dharun Anandayuvaraj, Matthew Campbell, Arav Tewari, and James C                   Springer, 2017. 99–114.
     Davis. FAIL: Analyzing software failures from the news using LLMs.            [23] CBMC as unit testing - CBMC. https://model-checking.github.io/
     In the 39th IEEE/ACM International Conference on Automated Software                cbmc-training/cbmc/overview/unit-testing.html. Accessed: 2024-10-03.
     Engineering, ASE ’24.                                                         [24] Chia Yuan Cho, Vijay D’Silva, and Dawn Song. BLITZ: Compositional
 [2] Shweta Sharma.            Counting the cost of CrowdStrike: the                    bounded model checking for real-world programs. In 2013 28th
     bug that bit billions.               https://www.cio.com/article/3478068/          IEEE/ACM International Conference on Automated Software Engineer-
     counting-the-cost-of-crowdstrike-the-bug-that-bit-billions.html.                   ing (ASE), pages 136–146.
     Accessed: 2024-10-07.                                                         [25] Bernhard Beckert, Michael Kirsten, Jonas Klamroth, and Mattias Ul-
 [3] Paschal C. Amusuo, Ricardo Andrés Calvo Méndez, Zhongwei Xu,                     brich. Modular verification of JML contracts using bounded model
     Aravind Machiry, and James C. Davis. Systematically detecting packet               checking. In Tiziana Margaria and Bernhard Steffen, editors, Leveraging
     validation vulnerabilities in embedded network stacks. In 2023 38th                Applications of Formal Methods, Verification and Validation: Verification
     IEEE/ACM International Conference on Automated Software Engineer-                  Principles, pages 60–80. Springer International Publishing, 2020.
     ing (ASE), pages 926–938. ISSN: 2643-1572.                                    [26] S. Bensalem, M. Bozga, T.-H. Nguyen, and J. Sifakis. Compositional
 [4] Sanoop Mallissery and Yu-Sung Wu. Demystify the fuzzing methods:                   verification for component-based systems and application. IET Software,
     A comprehensive survey. ACM Comput. Surv., 56(3):71:1–71:38, 2023.                 4(3):181–193, 2010. Publisher: IET Digital Library.
 [5] M. Pistoia, S. Chandra, S. J. Fink, and E. Yahav. A survey of static          [27] Darren Cofer, Andrew Gacek, Steven Miller, Michael W. Whalen, Brian
     analysis methods for identifying security vulnerabilities in software              LaValley, and Lui Sha. Compositional verification of architectural
     systems. IBM Systems Journal, 46(2):265–288, 2007.                                 models. In Alwyn E. Goodloe and Suzette Person, editors, NASA Formal
 [6] Paschal C. Amusuo, Kyle A. Robinson, Tanmay Singla, Huiyun Peng,                   Methods, pages 126–140. Springer, 2012.
     Aravind Machiry, Santiago Torres-Arias, Laurent Simon, and James C.           [28] Kelechi G. Kalu, Taylor R. Schorlemmer, Sophie Chen, Kyle A. Robin-
     Davis. ZTD$ {JAVA}$: Mitigating software supply chain vulnerabilities              son, Erik Kocinare, and James C. Davis. Reflecting on the use of the
     via zero-trust dependencies.                                                       policy-process-product theory in empirical software engineering. In
 [7] C. A. R. Hoare. An axiomatic basis for computer programming.                       Proceedings of the 31st ACM Joint European Software Engineering
     Commun. ACM, 12(10):576–580, October 1969.                                         Conference and Symposium on the Foundations of Software Engineering,
 [8] Jim Woodcock, Peter Gorm Larsen, Juan Bicarregui, and John Fitzger-                ESEC/FSE 2023, pages 2112–2116.
     ald. Formal methods: Practice and experience. ACM Computing Surveys,          [29] FreeRTOS/FreeRTOS/test/CBMC at main · FreeRTOS/FreeRTOS. https:
     41(4):1–36, 2009.                                                                  //github.com/FreeRTOS/FreeRTOS/tree/main/FreeRTOS/Test/CBMC.
 [9] Daniel Kroening and Michael Tautschnig. CBMC – c bounded model                     Accessed: 2024-10-08.
     checker. In Erika Ábrahám and Klaus Havelund, editors, Tools and            [30] Evgeny Novikov. Klever: Enabling model checking for the linux
     Algorithms for the Construction and Analysis of Systems, pages 389–                kernel.        https://forge.ispras.ru/attachments/download/7361/Klever
     391. Springer, 2014.                                                               %20Enabling%20Model%20Checking%20for%20the%20Linux%
[10] Getting started - the kani rust verifier. https://model-checking.github.io/        20Kernel.pdf.
     kani/. Accessed: 2024-10-01.                                                  [31] Writing a good proof - CBMC. https://model-checking.github.io/
[11] Yannick Moy, Emmanuel Ledinot, Hervé Delseny, Virginie Wiels, and                 cbmc-training/management/Write-a-good-proof.html. Accessed: 2024-
     Benjamin Monate. Testing or formal verification: DO-178c alternatives              10-05.
     and industrial experience. IEEE Software, 30(3):50–57, 2013. Confer-          [32] Mark Staples, Rafal Kolanski, Gerwin Klein, Corey Lewis, June An-
     ence Name: IEEE Software.                                                          dronick, Toby Murray, Ross Jeffery, and Len Bass. Formal specifications
[12] Nathan Chong, Byron Cook, Konstantinos Kallas, Kareem Khazem,                      better than function points for code sizing. In 2013 35th International
     Felipe R. Monteiro, Daniel Schwartz-Narbonne, Serdar Tasiran, Michael              Conference on Software Engineering (ICSE), pages 1257–1260.
     Tautschnig, and Mark R. Tuttle. Code-level model checking in the              [33] Daniel Matichuk, Toby Murray, June Andronick, Ross Jeffery, Gerwin
     software development workflow. In the ACM/IEEE 42nd International                  Klein, and Mark Staples. Empirical study towards a leading indicator
     Conference on Software Engineering: Software Engineering in Practice,              for cost of formal software verification. In 2015 IEEE/ACM 37th IEEE
     ICSE-SEIP ’20, pages 11–20.                                                        International Conference on Software Engineering, volume 1, pages
[13] Tong Wu, Shale Xiong, Edoardo Manino, et al. Verifying components of               722–732. ISSN: 1558-1225.
     arm(r) confidential computing architecture with ESBMC. https://arxiv.         [34] Haohua Zhang, Hai Zhao, Wei Cai, Jie Liu, and Wanlei Zhou. Using
     org/abs/2406.04375v1, 2024. Accessed: 2024-10-04.                                  the k-core decomposition to analyze the static structure of large-scale
[14] Ghada Bahig and Amr El-Kadi. Formal verification of automotive design              software systems. The Journal of Supercomputing, 53(2):352–369, 2010.
     in compliance with ISO 26262 design verification guidelines. IEEE             [35] Vishal Karande, Swarup Chandra, Zhiqiang Lin, Juan Caballero, Latifur
     Access, 5:4505–4516, 2017.                                                         Khan, and Kevin Hamlen. BCD: Decomposing binary code into
[15] Makarius Wenzel, Lawrence C. Paulson, and Tobias Nipkow. The                       components using graph-based clustering. In Proceedings of the 2018 on
     isabelle framework. In Theorem Proving in Higher Order Logics, pages               Asia Conference on Computer and Communications Security, ASIACCS
     33–38, 2008.                                                                       ’18, pages 393–398. Association for Computing Machinery.
[16] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha             [36] Jamieson M. Cobleigh, Dimitra Giannakopoulou, and Corina S.
     Subasinghe, Yi Zhou, Jon Howell, Bryan Parno, and Chris Hawblitzel.                PĂsĂreanu. Learning assumptions for compositional verification. In
     Verus: Verifying rust programs using linear ghost types. Proc. ACM                 Hubert Garavel and John Hatcliff, editors, Tools and Algorithms for the
     Program. Lang., 7:85:286–85:315, 2023.                                             Construction and Analysis of Systems, pages 331–346. Springer, 2003.
[17] Edmund Clarke, Armin Biere, Richard Raimi, and Yunshan Zhu.                   [37] D. Giannakopoulou, C.S. Pasareanu, and H. Barringer. Assumption
     Bounded model checking using satisfiability solving. Formal Methods                generation for software component verification. In Proceedings 17th
     in System Design, 19(1):7–34, 2001.                                                IEEE International Conference on Automated Software Engineering,,
[18] Rovedy Aparecida Busquim e Silva, José Manuel Parente de Oliveira,                pages 3–12, 2002. ISSN: 1938-4300.
     and Jorge Sousa Pinto. A case study on model checking and deductive           [38] Jamieson M. Cobleigh, George S. Avrunin, and Lori A. Clarke. Break-
     verification techniques of safety-critical software. Universidade Federal          ing up is hard to do: An evaluation of automated assume-guarantee
     de Campina Grande (UFCG), 2012. Accepted: 2015-05-20T14:33:25Z.                    reasoning. ACM Trans. Softw. Eng. Methodol., 17(2):7:1–7:52, 2008.
[19] Bernhard Beckert and Reiner Hähnle. Reasoning and verification: State        [39] Chongzhou Fang, Ning Miao, Shaurya Srivastav, Jialin Liu, Ruoyu
     of the art and current trends. IEEE Intelligent Systems, 29(1):20–29,              Zhang, Ruijie Fang, Asmita, Ryan Tsang, Najmeh Nazari, Han Wang,
     2014.                                                                              and Houman Homayoun. Large language models for code analysis: Do
[20] Martin Brain, Peter Schrammel, and Johannes Kloos. CBMC: Back-                     LLMs really do their job? In Proceedings of the 33rd USENIX Security
     ground concepts. https://diffblue.github.io/cbmc/background-concepts.              Symposium (USENIX Security 24), 2024.
     html. Accessed: 2024-10-03.                                                   [40] Daye Nam, Andrew Macvean, Vincent Hellendoorn, Bogdan Vasilescu,
[21] Rahul Kumar. How open source projects are using kani to write better               and Brad Myers. Using an LLM to help with code understanding.
     software in rust | AWS open source blog. AWS Open Source Blog, 2023.               In Proceedings of the IEEE/ACM 46th International Conference on
     Accessed: 2024-10-02.                                                              Software Engineering, ICSE ’24, pages 1–13, 2024.
