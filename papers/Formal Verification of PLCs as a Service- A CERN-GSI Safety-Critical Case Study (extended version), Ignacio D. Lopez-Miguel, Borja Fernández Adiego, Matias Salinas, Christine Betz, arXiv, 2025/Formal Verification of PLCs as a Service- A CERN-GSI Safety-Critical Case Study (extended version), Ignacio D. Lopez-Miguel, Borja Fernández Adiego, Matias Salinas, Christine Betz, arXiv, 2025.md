                                                Formal Verification of PLCs as a Service: A
                                                  CERN-GSI Safety-Critical Case Study
                                                            (extended version)

                                             Ignacio D. Lopez-Miguel1 , Borja Fernández Adiego2 , Matias Salinas3 , and
                                                                         Christine Betz3
arXiv:2502.19150v1 [cs.SE] 26 Feb 2025




                                                       1
                                                         TU Wien, Vienna, Austria ignacio.lopez@tuwien.ac.at
                                                          2
                                                            CERN, Beams Department, Geneva, Switzerland
                                                                 borja.fernandez.adiego@cern.ch
                                                       3
                                                         GSI, Darmstadt, Germany {m.salinas,c.betz}@gsi.de



                                                 Abstract. The increased technological complexity and demand for soft-
                                                 ware reliability require organizations to formally design and verify their
                                                 safety-critical programs to minimize systematic failures. Formal methods
                                                 are recommended by functional safety standards (e.g., by IEC 61511 for
                                                 the process industry and by the generic IEC 61508) and play a crucial
                                                 role. Their structured approach reduces ambiguity in system require-
                                                 ments, facilitating early error detection. This paper introduces a formal
                                                 verification service for PLC (programmable logic controller) programs
                                                 compliant with functional safety standards, providing external expertise
                                                 to organizations while eliminating the need for extensive internal train-
                                                 ing. It offers a cost-effective solution to meet the rising demands for
                                                 formal verification processes. The approach is extended to include mod-
                                                 eling time-dependent, know-how-protected components, enabling formal
                                                 verification of real safety-critical applications. A case study shows the
                                                 application of PLC formal verification as a service provided by CERN in
                                                 a safety-critical installation at the GSI particle accelerator facility.


                                         1     Introduction

                                            Formal methods play an essential role in ensuring the reliability, quality,
                                         and safety of software systems. They are recommended by industry standards
                                         and provide a mathematical approach to software development. One of these
                                         standards is DO-178C [24] in the aviation domain, which is accompanied by a
                                         guideline on formal methods (DO-333 [25]). The latter enhances the former by
                                         explaining how to use formal methods in every stage of the software lifecycle.
                                            Large scientific installations, like particle accelerators, do not have specific
                                         standards. However, they tend to apply the generic IEC 61508 [13] and IEC
                                             This paper is an extended version of our NFM 2025 paper “Formal Verification of
                                             PLCs as a Service: A CERN-GSI Safety-Critical Case Study”. It adds an appendix
                                             with the complete modeling of a know-how-protected function and with examples of
                                             found discrepancies during verification.
2         Ignacio D. Lopez-Miguel et al.

61511 [17] functional safety standards to design, develop, and validate their
safety-critical software. IEC 61508 recommends using formal approaches in dif-
ferent parts of the software lifecycle according to the criticality of the component.
IEC 61511 recommends the usage of formal methods to specify requirements.
ISO 26262 [18] for road vehicles also recommends the use of formal methods
for critical components, and IEC 61513 [14] for nuclear power plants emphasize
the importance of rigorous development and verification processes to ensure the
safety and reliability of safety-critical systems.
    All these standards agree that, although formal methods can be expensive,
identifying discrepancies between the code and the requirements in the early
development stages results in substantial cost reduction in later phases.
    However, some organizations might lack the resources to introduce formal
methods in their software development process. Formal verification as a ser-
vice addresses this need, offering formal methods expertise. It establishes a win-
win situation where organizations benefit from the skills of experts, and service
providers improve their tools based on the different case studies. It contributes
to quality assurance, enabling organizations to demonstrate to regulatory au-
thorities that exhaustive measures have been taken to ensure safety.
    In this paper, we focus on the formal verification of PLC (programmable logic
controller) programs as a service. Our contributions are summarized below:

 1. We present a collaboration model between the different stakeholders of a
    PLC project development and the formal verification service providers. It
    complies with the functional safety standards by ensuring independence and
    by using formal verification at the early stages of the PLC program lifecycle.
 2. We introduce a methodology based on simulation and formal verification to
    model know-how-protected functions, which are proprietary functions whose
    precise behavior is hidden by the manufacturer (black boxes). They are com-
    monly used in PLC programming, and some include time-dependent com-
    ponents, complicating their modeling. Their exact behavior must be known
    to formally verify a complete PLC program containing these functions.
 3. We show a real case study in which PLCverif [5] was used to verify a safety-
    critical system containing know-how-protected functions at the particle ac-
    celerator installation at GSI Helmholtz Centre for Heavy Ion Research [12].


2      Service approach

2.1     Collaboration model

Figure 1 depicts the proposed diagram to offer formal verification of PLC pro-
grams as a service [20]. It is composed of the following independent teams as
recommended by IEC 61511-1 clause 12 [16] of having an independent body in
charge of validating the critical software:

    – Requirement engineers. They are responsible for analyzing the systems and
      writing their technical requirements using different formalisms. They have
                  Formal Verification as a Service: A CERN-GSI Case Study                   3

   the best knowledge of the actual physical system for which the PLC program
   is developed, and they know how the system should behave. That is why they
   write and distribute the requirements to the other teams.
 – PLC program developers. They follow the requirements handed out by the
   requirement engineers to implement the PLC program. If the requirements
   are clear, the interaction with the requirement engineers can be minimal.
   Their PLC program is then shared with the other two teams.
 – Formal verification engineers. They ensure that the PLC program behaves
   exactly as written in the requirements using formal verification. The require-
   ments engineers are informed when a discrepancy between the PLC code and
   the requirements is found. Then, they work with the developers to solve it.

    It is important to highlight the iterative nature of this process. Especially
when a discrepancy is found, formal verification engineers need to inform re-
quirement engineers, who will work with the developers to find the root cause of
the error. This will lead to updated requirements and/or PLC programs, which
are then given again to the formal verification engineers so they can continue
their work. This process is repeated until no more discrepancies are found.
    Although this process does not
entirely ensure the lack of errors
in the code or in the require-                         Reqiurement CEM, I/O matrix,
                                                        engineers  state machine, etc.
ments due to the possible bugs in
                                                                      vi
                                                                        ol
the program verifier, it drastically
                                                            ts




                                                                         at
                                                         en




                                                                         ed
                                                         m
                                                       m

                                                      ra




                                                                              re
                                                   ire

                                                   og




                                                                 re




                                                                                qu
increases the confidence of the
                                                qu




                                                                 qu
                                                pr




                                                                                ire
                                               re




                                                                   ire
                                                       C




                                                                                     m
                                                    PL




                                                                      m




                                                                                      en
                                                                       en


requirement engineers with the TIA Portal                                     PLCverif

                                                                                       ts
                                                                         ts



                                        PLC program                 Form. verification
PLC program. It also helps them          developers   PLC program       engineers
show authorities they made con-
siderable efforts to guarantee the
                                     Fig. 1. Diagram with the roles of the collabora-
safety of the installation. In fact,
                                     tion, shared information and used tools.
formal verification, compared to
other methods like testing, can
identify more hidden bugs (corner
cases).
    Another important formal method to mention at this point is the synthesis
of PLC programs [33], which would make formal verification redundant since
the code would be correct by construction. However, synthesis tools for PLC
programs are not widespread in the industry.
    In the next two subsections, from Figure 1, we will further explain how the re-
quirement engineers can formalize requirements and how the formal verification
engineers verify the given PLC code according to the formalized requirements.


2.2   Formal specification

Requirements can be represented using diverse formalisms, which should be sim-
ple, clear, and concise for use across the software development lifecycle. The
4          Ignacio D. Lopez-Miguel et al.

examples in this section meet these criteria, were applied in the case study (Sec-
tion 3), and align with functional safety standards. IEC 61511-2 [15] recommends
methods like cause-and-effect matrix, state machines, and logic diagrams; IEC
61511-1 [16] provides examples of state machines and logic diagrams.

    – A Cause-and-effect-matrix (CEM) [8] is a tabular representation of Boolean
      expressions. It is particularly suitable for stateless logic like interlock logic.
      The example from Table 1 assigns values to the outputsVaccording to Out_1 =
                                                                 4
      (In_1 ∧ In_2 ) ∨ (¬In_3 ∧ ¬In_4 ), and Out_2 = i=1 In_i.
    – An input-output matrix (I/O matrix) gives the conditions to set or reset out-
      put variables. One needs to ensure that the inputs are mutually exclusive or
      to specify output priorities. The I/O matrix from Table 2 shows an example.
    – A state machine is a graphical representation used to depict the behavior of
      a system consisting of different states and transitions between them. Figure 2
      shows a simple state machine that changes from two modes depending on
      the requests. For a real example, one can refer to [34, Figure 4.4].


                                    Outputs                                           Outputs
                                  Out_1 Out_2                                       Out_1 Out_2
                            In_1 A1          A1
                                                                                In_1 Reset Reset
                   Inputs




                                                                       Inputs
                            In_2 A1          A1
                            In_3 NA2         A1                                 In_2 Set Reset
                            In_4 NA2         A1                                 In_3 Set    Set

          Table 1. Example of a CEM.                        Table 2. Example of an I/O matrix.

      ¬ Request_Mode_2                   ¬ Request_Mode_1       In_1
                            Request_Mode_1                      In_2                               Out_1

          Mode_1                              Mode_2            In_3

                            Request_Mode_2

     Fig. 2. Example of a state machine.                      Fig. 3. Example of a logic diagram.

    – A logic diagram visually represents logical relationships. Figure 3 depicts an
      example, representing Out_1 = (In_1 ∨ In_2) ∧ In_3.
    – An assertion expresses a property of a program at a particular point in
      the code’s execution. Although this is typically used during software de-
      velopment, it can be used to formalize requirements. They are particularly
      helpful in expressing safety properties, i.e., a state can never be reached.

2.3      Formal verification
Formal verification as a service not only verifies the PLC program but also helps
to amend errors in the requirements, helping requirement engineers understand
the PLC program’s behavior better. To formally verify PLC programs after the
requirements are formalized, PLCverif [6,21] was used. The reasons for using
it are that it is actively developed, has high coverage of PLC languages, uses
state-of-the-art model checkers, has been used in real systems, and is partially
                        Formal Verification as a Service: A CERN-GSI Case Study           5

    Documentation                                    #cycle   1   2    3    4    5    6
                            Function simulation
       analysis
                                                         ON
                Timing diagram
                   creation                        FEEDBACK
                           Assertions and inputs        ACK
   Function modeling
                                generation
                                                      ERROR
               Formal verification


                                                   Fig. 5. Example of a timing diagram for
Fig. 4. Proposed diagram to model a                a simplified version of the FDBACK func-
know-how-protected built-in function.              tion.


automated. Other solutions, such as Arcade.PLC [2], MODCHK [23], PLCIn-
spector [32], STbmc [19] or the ones in [22] lack some of these capabilities.
    Other papers show how to use PLCverif ([7,9,10]), so due to space constraints,
we will focus on the modeling of time-dependent know-how-protected functions.
    PLC programming platforms such as TIA Portal [26] for Siemens PLCs in-
clude know-how-protected functions to simplify some tasks of the PLC developer.
These are proprietary functions whose behavior is hidden by the manufacturer.
To verify PLC programs that use these functions, it is necessary to understand
their behavior precisely. Functions that involve time are particularly challenging,
as they require the propagation of signal values across successive PLC cycles.
    To model these functions, we propose a method that combines simulations
and formal verification (Figure 4). This process produces a model in PLC code of
the know-how-protected function using transparent functions and operators that
can be used in PLCverif as part of the verification of the whole PLC program.
    This process can be considered automata learning since the internal represen-
tation of PLCverif uses control flow automata (CFA) [1]. In fact, the conditions of
the PLC program and the assignments are translated into transitions and assign-
ments in the CFA. However, since no tools generate PLC code from automata,
learning the PLC code directly was deemed more efficient. Furthermore, having
the PLC code allowed us to verify it without any extra effort with PLCverif, and
to include it directly in the verification of the whole PLC project.
    To explain this process (Figure 4), we will use a simplified version of the
know-how protected FDBACK function from TIA Portal [29, section 13.3.7]. It
checks if the inputs ON=0 and FEEDBACK=1, and produces an error otherwise. It
is used to monitor systems. This example is particularly relevant since it involves
time, its documentation is complex, and it was often used in our case study.

 – Documentation analysis. Our simplified FDBACK function checks whether in-
   put ON=0 and input FEEDBACK=1. Output ERROR becomes 1 if this does not
   happen after a given maximum time (e.g., two PLC cycles). Once ERROR=1,
   an acknowledgment ACK is necessary to reset it.
 – Function simulation. Given the documentation, a simple PLC program is
   created to simulate the given function (cf. Appendix A.1).
 – Timing diagram creation. From the simulation of the function and the doc-
   umentation, we produce a timing diagram. The input variables are changed
6         Ignacio D. Lopez-Miguel et al.

      manually to capture all the possible behaviors from the documentation. Fig-
      ure 5 exemplifies a timing diagram for this function. Initially, ON=0 and
      FEEDBACK=1, thus ERROR=0. Then ON turns 1, leading to ERROR=1 after the
      maximum time (two cycles) is reached. Although ON becomes 0 again, ERROR
      keeps its value until there is an acknowledgment (ACK=1) (cf. Appendix A.2).
    – Assertions and inputs generation. The timing diagram is automatically trans-
      lated for every cycle into assignments for the inputs and assertions for the
      outputs. Since ACK is non-deterministic in the first three cycles, no value
      is assigned to it. For the first cycle, the assignments are FEEDBACK :=
      1, ON := 0, and the assertion is cycle = 1 → ¬ERROR (cf. Appendix A.3).
    – Function modeling. Given the documentation, a simple PLC program is cre-
      ated to simulate the given function (cf. Appendix A.4).
    – Formal verification. The modeled function is verified with respect to the gen-
      erated assertions. This ensures that the modeled function behaves as the one
      in TIA Portal with respect to all the simulated scenarios (cf. Appendix A.5).

   This process continues iteratively until no discrepancies are found between
the documentation, the timing diagrams, and the PLC model. The modeling of
the original FDBACK function resulted in about 100 lines of code [4, Line 843].


3      Case study

The approach presented in this paper was applied to verify the Personnel Access
System (PAS) of the FAIR accelerator facility at the GSI Helmholtzzentrum
für Schwerionenforschung [12]. PAS [11] is a very critical system that prevents
personnel from entering areas exposed to particle beams and their radiation.
Thus, a failure in the PAS PLC program could have very severe consequences.
This PLC program is highly configurable, making exhaustive testing unfeasible
due to the enormous number of combinations in the PLC program. Also, it is
developed using TIA Portal, hence, it utilizes know-how-protected functions.
    Due to CERN’s expertise in the verification of different PLC projects [7,10]
and the continuous development of PLCverif, GSI trusted CERN to verify its
PAS PLC project. The collaboration was set up as described in Section 2 with
three independent teams: (i) Requirement engineers (GSI). (ii) Formal verifica-
tion engineers (CERN). (iii) Developers (a different team at CERN).
    A summary of the results produced by this collaboration is shown below:

    – The requirements were formalized according to Section 2.2, leading to a
      better understanding of the desired program behavior and less ambiguities;
    – The PLC program was fully aligned with the formal requirements, amending
      detected discrepancies (cf. Appendix B for examples of found discrepancies);
    – PLCverif was enhanced to support additional know-how-protected functions,
      including FDBACK, CTUD, ESTOP1, and FDB_TIME [29]. They are now included
      in the set of covered functions by PLCverif [5] (delivered together with
      PLCverif in the builtin.scl file) and can be used in future projects.
                  Formal Verification as a Service: A CERN-GSI Case Study            7

4   Conclusion

The presented approach for formal verification as a service can help to detect er-
rors early, reduce ambiguity, and improve requirements precision. To the best of
our knowledge, this is the first time an organization trusted another to formally
verify a complete, real-world, safety-critical PLC project (other collaborations
like ITER-CERN [10] focused on the verification of specific modules). We hope
the presented approach demonstrates that formal methods are feasible, ben-
eficial, and compliant with functional safety standards in safety-critical PLC
projects, enabled by organizational collaborations.
    As part of our future work, we will seek a more automated process of mod-
eling know-how-protected functions to increase the coverage of PLCverif. We
will also work on the automation between requirement specification and verifi-
cation, ultimately leading to correct-by-construction code generation. This is not
a straightforward path due to different challenges, such as a lack of formal tools,
legacy systems, established workshops, regulations, and the need for training.


Acknowledgments

       The project leading to this application has received funding from the Eu-
       ropean Union’s Horizon 2020 research and innovation programme under
grant agreement No 101034440 and by the WWTF project ICT22-023.


References

 1. Beyer, D., Henzinger, T.A., Jhala, R., Majumdar, R.: The software model checker
    Blast. International Journal on Software Tools for Technology Transfer 9(5-6),
    505–525 (Sep 2007). https://doi.org/10.1007/s10009-007-0044-z, https://doi.org/
    10.1007/s10009-007-0044-z
 2. Biallas, S., Brauer, J., Kowalewski, S.: Arcade.PLC: A Verification Platform for
    Programmable Logic Controllers . In: Proceedings of the 27th IEEE/ACM Inter-
    national Conference on Automated Software Engineering. pp. 338–341. ASE 2012,
    ACM (2012), http://publications.embedded.rwth-aachen.de/file/3w
 3. Blanco Vinuela, E., Darvas, D., Sallai, G.: Testing Solutions for Siemens PLCs
    Programs Based on PLCSIM Advanced. In: Proc. ICALEPCS’19. p. 1108. No. 17 in
    International Conference on Accelerator and Large Experimental Physics Control
    Systems, JACoW Publishing, Geneva, Switzerland (10 2020). https://doi.org/10.
    18429/JACoW-ICALEPCS2019-WEPHA018
 4. CERN:        Built-in     functions     (202),     https://gitlab.com/plcverif-oss/
    plcverif-builtin-projects/-/blob/master/builtin.scl
 5. CERN: PLCverif (2024), https://gitlab.com/plcverif-oss
 6. Darvas, D., Viñuela, E.B., Molnár, V.: PLCverif Re-engineered: An Open Plat-
    form for the Formal Analysis of PLC Programs. In: Proc. ICALEPCS’19. pp. 21–
    27. JACoW Publishing, Geneva, Switzerland (08 2020). https://doi.org/10.18429/
    JACoW-ICALEPCS2019-MOBPP01
8       Ignacio D. Lopez-Miguel et al.

 7. Fernandez Adiego, B., Lopez-Miguel, I.D., Tournier, J.C.: Applying Model Check-
    ing to Highly-Configurable Safety Critical Software: The SPS-PPS PLC Program.
    In: Proc. ICALEPCS’21. JACoW Publishing, Geneva, Switzerland (10 2021).
    https://doi.org/10.18429/JACoW-ICALEPCS2021-WEPV042
 8. Fernández Adiego, B., Blanco Viñuela, E., Bonet, M., Charrondiere, M.,
    Hamisch, H., Speroni, R., de Queiroz, M.: Cause-and-Effect Matrix Speci-
    fications for Safety Critical Systems at CERN . In: Proc. ICALEPCS’19.
    JACoW Publishing, Geneva, Switzerland (10 2019). https://doi.org/10.18429/
    JACoW-ICALEPCS2019-MOPHA041
 9. Fernández Adiego, B., Darvas, D., Blanco Viñuela, E., Tournier, J.C., Bliudze, S.,
    Blech, J., González, V.: Applying model checking to industrial-sized PLC pro-
    grams. IEEE Transactions on Industrial Informatics 11, 1400–1410 (12 2015).
    https://doi.org/10.1109/TII.2015.2489184
10. Fernández Adiego, B., et al.: Applying Model Checking to Critical PLC Ap-
    plications: An ITER Case Study. In: Proc. ICALEPCS’17. JACoW Publish-
    ing, Geneva, Switzerland (1 2018). https://doi.org/https://doi.org/10.18429/
    JACoW-ICALEPCS2017-THPHA161
11. Gaßmann, D., et al.: The Personnel Access System for FAIR. In: 14th Interna-
    tional Particle Accelerator Conference, IPAC 2023, Venice, Italy, May 7–12, 2023,
    Proceedings (2023)
12. GSI Helmholtz Centre for Heavy Ion Research: Research Fields and Experiments
    (2024), https://www.gsi.de/en/work/research, accessed = 2024-11-7
13. International Electrotechnical Commission: IEC 61508:2010 — Functional safety of
    electrical/electronic/programmable electronic safety-related systems. International
    standard, International Electrotechnical Commission (2010), https://webstore.iec.
    ch/publication/22273
14. International Electrotechnical Commission: IEC 61513:2011 - Nuclear power plants
    - Instrumentation and control important to safety - General requirements for sys-
    tems. International standard, International Electrotechnical Commission (2011),
    https://webstore.iec.ch/en/publication/5532
15. International Electrotechnical Commission: IEC 61511-2:2016 - Functional safety
    - Safety instrumented systems for the process industry sector - Part 2: Guidelines
    for the application of IEC 61511-1:2016. International standard, International Elec-
    trotechnical Commission (2016), https://webstore.iec.ch/en/publication/25510
16. International Electrotechnical Commission: IEC 61511-1:2016+AMD1:2017 CSV
    - Functional safety - Safety instrumented systems for the process industry sector
    - Part 1: Framework, definitions, system, hardware and application programming
    requirements. International standard, International Electrotechnical Commission
    (2017), https://webstore.iec.ch/en/publication/61289
17. International Electrotechnical Commission: IEC 61511:2024 - Functional safety -
    Safety instrumented systems for the process industry sector. International stan-
    dard, International Electrotechnical Commission (2024), https://webstore.iec.ch/
    en/publication/5527
18. International Organization for Standardization: ISO 26262-6:2018 — Road ve-
    hicles — Functional safety. Part 6: Product development at the software level.
    International standard, International Organization for Standardization (2018),
    https://www.iso.org/standard/68388.html
19. Lee, J., Kim, S., Bae, K.: Bounded Model Checking of PLC ST Programs using
    Rewriting Modulo SMT. Proceedings of the 8th ACM SIGPLAN International
    Workshop on Formal Techniques for Safety-Critical Systems (2022), https://api.
    semanticscholar.org/CorpusID:254126390
                  Formal Verification as a Service: A CERN-GSI Case Study           9

20. Lopez-Miguel, I.D., Fernández Adiego, B., Blanco Viñuela, E., Salinas, M., Betz,
    C.: Working Together for Safer Systems: A Collaboration Model for Verification
    of PLC Code. In: Proc. ICALEPCS’23. JACoW Publishing, Geneva, Switzerland
    (09 2022), https://icalepcs2023.vrws.de/html/auth0780.htm
21. Lopez-Miguel, I.D., Tournier, J.C., Fernández Adiego, B.: PLCverif: Status
    of a Formal Verification Tool for Programmable Logic Controller. In: Proc.
    ICALEPCS’21. JACoW Publishing, Geneva, Switzerland (03 2022). https://doi.
    org/10.18429/JACoW-ICALEPCS2021-MOPV042
22. Ovatman, T., Aral, A., Polat, D., Ünver, A.O.: An Overview of Model Checking
    Practices on Verification of PLC Software. Softw. Syst. Model. 15(4), 937–960
    (Oct 2016). https://doi.org/10.1007/s10270-014-0448-7, https://doi.org/10.1007/
    s10270-014-0448-7
23. Pakonen, Antti and Tahvonen, Topi and Hartikainen, Markus and Pihlanko, Mikko:
    Practical aplications of model checking in the finnish nuclear industry. In: 10th
    International Topical Meeting on Nuclear Plant Instrumentation, Control and Hu-
    man Machine Interface Technologies (2017), https://cris.vtt.fi/en/publications/
    practical-applications-of-model-checking-in-the-finnish-nuclear-i
24. Radio Technical Commission for Aeronautics: DO-178C - Software Considerations
    in Airborne Systems and Equipment Certification. International standard, Radio
    Technical Commission for Aeronautics (2012), https://my.rtca.org/productdetails?
    id=a1B36000001IcmqEAC
25. Radio Technical Commission for Aeronautics: DO-333 - Formal Methods Sup-
    plement to DO-178C and DO-278A. International standard, Radio Techni-
    cal Commission for Aeronautics (2012), https://my.rtca.org/productdetails?id=
    a1B36000001IcfeEAC
26. Siemenes: Totally Integrated Automation Portal (2023), https://www.siemens.
    com/global/en/products/automation/industry-software/automation-software/
    tia-portal.html, accessed on 06/12/2023
27. Siemens: Engineering Tools. S7-PLCSIM V16 online help. Siemens, https:
    //support.industry.siemens.com/cs/attachments/109773149/S7-PLCSIMenUS_
    en-US.pdf
28. Siemens: Function Manual. SIMATIC S7-1500. S7-PLCSIM Advanced. Siemens,
    https://support.industry.siemens.com/cs/attachments/109826194/s7-plcsim_
    advanced_function_manual_en-US.pdf
29. Siemens: Industrial Software SIMATIC Safety - Configuring and Programming.
    SIMATIC,         https://support.industry.siemens.com/cs/attachments/54110126/
    ProgFAILenUS_en-US.pdf
30. Siemens: OpennessScripter: Detailed Documentation. Siemens, https:
    //support.industry.siemens.com/cs/attachments/109742322/109742322_
    OpennessScripter_DOC_V117_en.pdf
31. Siemens: TIA Portal Openness: API for automation of engineering workflows.
    Siemens,        https://support.industry.siemens.com/cs/attachments/109798533/
    TIAPortalOpennessenUS_en-US.pdf
32. Xiong, J., Zhu, G., Huang, Y., Shi, J.: A User-Friendly Verification Approach
    for IEC 61131-3 PLC Programs. Electronics 9(4) (2020). https://doi.org/10.3390/
    electronics9040572, https://www.mdpi.com/2079-9292/9/4/572
33. Yoo, J., Cha, S., Kim, C.H., Song, D.Y.: Synthesis of fbd-based plc design
    from nuscr formal specification. Reliability Engineering & System Safety 87(2),
    287–294 (2005). https://doi.org/https://doi.org/10.1016/j.ress.2004.05.005, https:
    //www.sciencedirect.com/science/article/pii/S0951832004001279
10     Ignacio D. Lopez-Miguel et al.

34. Ádám, Z., et al.: Automated Verification of Programmable Logic Controller Pro-
    grams against Structured Natural Language Requirements. Tech. rep., NASA Ames
    Research Center (03 2023), https://ntrs.nasa.gov/citations/20230003752
                 Formal Verification as a Service: A CERN-GSI Case Study       11

Appendix

A     Modelling of the FDBACK function
In this appendix, we will show in detail an example of modeling a know-how
protected function. We will use the same example as in the main text, i.e., the
FDBACK function. For the steps of the process where we need to interact with
TIA portal (function simulation and timing diagram creation), we will use the
original FDBACK function. For the other parts, we will use the simplified version
that we presented in the section 2.3 to simplify the explanation.

A.1   Function simulation
We created a simple TIA Portal project containing only the function we want to
model. Figure 6 shows the small project structure that was used to simulate the
original FDBACK function. The inputs and outputs of the FDBACK function (called
by the Main_Safety_RTG1 Function Block) are shown in Figure 7 and can be
enabled for simulation.




Fig. 6. Project structure Fig. 7. FDBACK function interface call in the TIA Portal
in TIA Portal to simulate program.
FDBACK function.


A.2   Timing diagram creation
For this project, we used the PLCSIM simulator [27] provided by Siemens, which
is integrated into TIA portal. To simulate the FDBACK function, we manually
forced its inputs according to what we wanted to check from the documentation.
Once the inputs were set, the outputs were observed. Note that safety inputs (in
yellow in Figures 8 to 10) cannot be forced on the simulator. For this reason,
we used a standard Data Block (DB) called std_Block, and we assigned the
variables of this DB to the safety inputs of the FDBACK function. By forcing the
std_Block variables, we can change the input values of the FDBACK function.
    Since PLCSIM does not provide a timing diagram as such, from the manual
simulations, a timing diagram was created manually (cf. table from Figure 11).
12        Ignacio D. Lopez-Miguel et al.

Eventually, this could be automated by using the TIA Openness API [31] and the
PLCSIM advanced simulator [28], which is only available for the S7-1500 PLC
series. The latter provides continuous, cycle-by-cycle, and time-synchronized exe-
cution modes and comes with a C# API, which can be used to automate the sim-
ulation and execution process [3]. Siemens also provides OpennessScripter [30],
which is a tool to simplify the use of the TIA Portal Openness interface.
    Several simulations were performed following all the situations that the docu-
mentation describes. This is an iterative process; more simulations were included
when some behaviors were unclear.
    We will now show three simulation scenarios that can complete a simple
timing diagram. We set values for the input variables of the FDBACK function
and observe its outputs. These simulations show how the system goes through
the following states: (i) no error, (ii) error, (iii) error acknowledged → error
removed. We will only focus on the variables that are part of our simplified
FDBACK function. That is, inputs={ON,FEEDBACK,ACK}, and outputs={ERROR}.

1. Figure 8. There is no error since ON=0 and FEEDBACK=1.

        – ON ← FALSE                             – ACK ← FALSE
        – FEEDBACK ← TRUE                        – ERROR = FALSE




     Fig. 8. Input and output variables of the original FDBACK function in TIA Portal




     Fig. 9. Input and output variables of the original FDBACK function in TIA Portal
                 Formal Verification as a Service: A CERN-GSI Case Study         13

2. Figure 9. There is an error since ON=1 and FEEDBACK=1. The screenshot has
   been taken after waiting for two PLC cycles with those inputs so that the
   ERROR becomes 1.

      – ON ← TRUE                             – ACK ← FALSE
      – FEEDBACK ← TRUE                       – ERROR = TRUE

3. Figure 10. There is no error anymore because now FEEDBACK=TRUE and
   ON=FALSE, and the error has been acknowledged with a rising edge of ACK.

      – ON ← FALSE                            – ACK ← TRUE
      – FEEDBACK ← TRUE                       – ERROR = FALSE




 Fig. 10. Input and output variables of the original FDBACK function in TIA Portal

    These consecutive simulations are annotated in a table like the one from Fig-
ure 11, producing a timing diagram as also shown in Figure 11. The generation
of timing diagrams is concluded when all the aspects from the documentation
are covered and no assertion fails (cf. Appendix A.3 and Appendix A.5).


A.3    Assertions and inputs generation

Once a timing diagram was created, the PLC code for the verification of the
model of a know-how-protected function was generated automatically. It contains
the statements to set the input variables to the corresponding values and the
assertions to check the outputs.
    The spreadsheet used for the simplified FDBACK function is shown in Figure 11.
The table corresponds to the encoding of the timing diagram from Figure 5.
The two blocks of code correspond to the assignments to the input variables
and to the assertions. One can see that the assertions do not contain any input
variable since they are already set to the correct value with the assignment
statements. If there is no assignment for an input variable, it can take any value
non-deteministically.
14      Ignacio D. Lopez-Miguel et al.




Fig. 11. Screenshot of the spreadsheet to generate the code to verify the model of the
simplified know-how protected FEEDBACK function.

    The generated code is the one used in Listing 1.2 to verify the function. For
the modeling of the original FDBACK function, six spreadsheets with 25 cycles
each were used.
    Although it could be possible to have a unique assertion as the one shown
below for each timing diagram, it is preferable to split it into smaller asser-
tions, as in the PLC code from Listing 1.2, to be able to find the root cause of
discrepancies faster.


(cycle = 1 → ¬ERROR) ∧ (cycle = 2 → ¬ERROR) ∧ (cycle = 3 → ¬ERROR)∧
(cycle = 4 → ERROR) ∧ (cycle = 5 → ERROR) ∧ (cycle = 6 → ¬ERROR)


A.4    Function modeling

The model in PLC code of the simplified know-how-protected FDBACK function
can be seen in Listing 1.1. This model was done manually according to the docu-
mentation and simulations. One can see that even though the requirement looks
simple, its implementation is not trivial due to the timing aspect. Furthermore,
                       Formal Verification as a Service: A CERN-GSI Case Study           15

     this is just a simplified version of the real one, whose model in PLC code was
     implemented in about 100 lines of code [4, Line 843].

1  FUNCTION_BLOCK FDBACK_simplified
2      VAR_INPUT
 3         ON : BOOL;
 4             FEEDBACK : BOOL;
 5         ACK : BOOL;
 6     END_VAR
 7     VAR
 8     // Elapsed Time (ET) variable is a Timer On Delay.
 9     // It sets ET.Q to true after a given time
10         ET : TON;
11     END_VAR
12

13      VAR_OUTPUT
14          ERROR : BOOL := FALSE;
15      END_VAR
16

17 BEGIN
18     IF ERROR THEN // manual acknowledgement
19         IF ACK THEN
20             ET(IN := FALSE); // reset timer
21             ERROR := FALSE; // reset the error
22         END_IF;
23     ELSIF NOT (NOT ON AND FEEDBACK) THEN
24         // start timer (ET is the Elapsed Time function)
25         ET(IN := TRUE, PT := 2*200);// 2 cycles (each safety cycle is 200ms)
26         IF ET.Q THEN // if waiting time is over
27             ERROR := TRUE;
28         END_IF;
29     ELSE
30         ET(IN := FALSE); // reset timer
31     END_IF;
32

33   END_FUNCTION_BLOCK
     Listing 1.1. PLC code modeling the simplified know-how protected FDBACK function.

             ¬ON ∧ FEEDBACK ,
                   t := 0                ¬ON ∧ FEEDBACK , t ≤ 2
                                                                                 ¬ACK

                            ¬ON ∧ FEEDBACK ,
                                  t := 0                   ¬(¬ON ∧ FEEDBACK ),
                                                                   t>2
                 ¬ERROR                         ¬ERROR                           ERROR
                           ¬(¬ON ∧ FEEDBACK )


                                                  ACK




           Fig. 12. Timed automaton representing the simplified FDBACK function.
     16      Ignacio D. Lopez-Miguel et al.

        As mentioned in section 2.3, the problem of modeling know-how-protected
     functions can be understood in terms of automata learning. For the simplified
     FDBACK function, the corresponding timed automaton that can be extracted from
     the PLC code is shown in Figure 12.


     A.5    Formal verification

     In order to verify that the model is working as expected, the PLC code shown in
     Listing 1.2 was used. It basically consists of a set of consecutive calls to the model
     of the function FDBACK_simplified."FDBACK_simplified_inst"(). Each call
     represents a PLC cycle. For each cycle, the input variables are set to the values
     according to the timing diagram (see Figure 5). If a variable is not set, its value
     is non-deterministic, as with ACK. At the end of each cycle, it is checked if the
     output variable ERROR has the same value as in the timing diagram.

1 DATA_BLOCK "FDBACK_simplified_inst" FDBACK_simplified
2 BEGIN
3 END_DATA_BLOCK

4

5 FUNCTION_BLOCK call_FDBACK_simplified
6        VAR
7           cycle : INT := 1;
8        END_VAR
9 BEGIN

10

11 // setting the input variables according to the timing diagram
12 // in the cycles where ACK is not set, its value is non−deterministic
13 IF cycle=1 THEN

14     "FDBACK_simplified_inst".FEEDBACK:= TRUE;
15     "FDBACK_simplified_inst".ON := FALSE;
16 ELSIF cycle=2 THEN

17     "FDBACK_simplified_inst".FEEDBACK := TRUE;
18     "FDBACK_simplified_inst".ON := TRUE;
19 ELSIF cycle=3 THEN

20     "FDBACK_simplified_inst".FEEDBACK := TRUE;
21     "FDBACK_simplified_inst".ON := TRUE;
22 ELSIF cycle=4 THEN

23     "FDBACK_simplified_inst".FEEDBACK := TRUE;
24     "FDBACK_simplified_inst".ON := TRUE;
25     "FDBACK_simplified_inst".ACK := FALSE;
26 ELSIF cycle=5 THEN

27     "FDBACK_simplified_inst".FEEDBACK := TRUE;
28     "FDBACK_simplified_inst".ON := FALSE;
29     "FDBACK_simplified_inst".ACK := FALSE;
30 ELSIF cycle=6 THEN

31     "FDBACK_simplified_inst".FEEDBACK := TRUE;
32     "FDBACK_simplified_inst".ON := FALSE;
33     "FDBACK_simplified_inst".ACK := TRUE;
                       Formal Verification as a Service: A CERN-GSI Case Study          17

34   END_IF;
35

36   // check with assertions that the output variables have the same
37   // values than in the timing diagram
38

39   FDBACK_simplified."FDBACK_simplified_inst"() ;
40

41 //#ASSERT(cycle=1 --> ("FDBACK_simplified_inst".ERROR = FALSE)) :
       assertion1;
42 //#ASSERT(cycle=2 --> ("FDBACK_simplified_inst".ERROR = FALSE)) :

       assertion2;
43 //#ASSERT(cycle=3 --> ("FDBACK_simplified_inst".ERROR = FALSE)) :

       assertion3;
44 //#ASSERT(cycle=4 --> ("FDBACK_simplified_inst".ERROR = TRUE)) :

       assertion4;
45 //#ASSERT(cycle=5 --> ("FDBACK_simplified_inst".ERROR = TRUE)) :

       assertion5;
46 //#ASSERT(cycle=6 --> ("FDBACK_simplified_inst".ERROR = FALSE)) :

       assertion6;
47

48   cycle := cycle +1;
49

50   END_FUNCTION_BLOCK

     Listing 1.2. PLC code used to verify the simplified know-how protected FDBACK
     function.

         As already mentioned, PLCverif was used to verify the PLC code modeling
     know-how protected functions. This process was straightforward once the code
     was generated. However, it is essential to highlight how the time was treated
     with PLCverif. Since the time of the PLC cycle is not relevant for verification
     purposes – what is important is when the output of the timer is activated – a
     fixed time of the PLC cycle was fixed. In this case, we used the usual safety time
     of the PLC cycle of T _CYCLE = 100ms. This can be seen in Figure 13 from
     the verification case of PLCverif.
         Furthermore, it is important to allow as many cycles as needed to be able to
     trigger the output of the timer. That is, if the output is triggered after T millisec-
     onds of being started, then we should have at least cc = int(T /T _CYCLE ) + 1
     cycles. We should have also at least the number of cycles that we have in the
     timing diagram ct . Thus, the number of loop unwinding for a bounded model
     checker like CBMC should be max{cc , ct }. In our case, cc = 2 (200ms/100ms)
     and ct = 6, thus we set it to 6. This can be seen in Figure 14 from the verification
     case of PLCverif.
         Once the verification case is executed and we get that all assertions are
     satisfied, as shown in Figure 15, the modeling process is finished. If PLCverif
     reports a violation of an assertion, it will also give us a counterexample. Then,
     we need to investigate where the error is coming from and amend it so that the
     model aligns with the timing diagram.
18      Ignacio D. Lopez-Miguel et al.




     Fig. 13. Verification case of PLCverif. The time of the cycle is set to 100ms.




Fig. 14. Verification case of PLCverif. The loop unwinding is set to 6 to cover all the
cycles in the timing diagram.
                  Formal Verification as a Service: A CERN-GSI Case Study           19




      Fig. 15. Verification report of PLCverif. All the assertions are satisfied.


B    Examples of found discrepancies
This section summarizes the discrepancies found during the verification of differ-
ent PLC projects by CERN, not only during the verification of the GSI project.
The examples are simplified to show where the problem lies more easily. Most
of the discrepancies can be classified into the following three buckets:
1. Incomplete requirements. This is the most common type of discrepancy found.
   The implementation works as expected by the requirement engineers, but the
   requirements have not been formalized correctly.
2. Bugs in the PLC program. It happens when the requirement is correct, but
   the implementation has an error.
3. Minor documentation errors. These are simple errors that are easily fixed.
   A reader can understand the requirements without any issues. For example,
   a misspelled variable would be part of this type of error.
    In the next subsection B.1, we will give some examples of incomplete require-
ments. However, we will not extend the other two types of discrepancies since
they are self-explanatory.
    Other types of problems can also be found during the formal verification of a
PLC project. A recurrent one that appears in the early stages of the collaboration
is what to specify and how to do it formally. Furthermore, simple things like the
exact software used are sometimes not specified, as well as what happens if there
are hardware failures.
    20        Ignacio D. Lopez-Miguel et al.

    B.1      Incomplete requirements

    The examples shown in this subsection are not exhaustive but include the major-
    ity of the most important discrepancies found. We will cover situations related to
    (i) priorities, (ii) incomplete diagrams and tables, (iii) and lack of explanations.
    We will show incomplete requirements and propose solutions to complete them.


    Priorities. Although it is not ideal, different requirements often express con-
    ditions for the same output variables. If no priorities are set, this can lead to
    ambiguities. As an example, let us take the following requirements:
         (R1 ) If v1_up → set v_out.
         (R2 ) If v1_down → reset v_out

       Listing 1.3 shows an example of how this requirement can be implemented.
    In this case, R2 has a higher priority than R1 since if v1_down is true, then
    v_out will be true no matter the value of v1_up. What is executed later has a
    higher priority. However, another implementation could change the order of the
    IF statements, leading to R1 having a higher priority than R1 . This ambiguity
    can be solved by

     1. telling which of the two requirements has a higher priority,
     2. if v1_up and v1_down cannot be true simultaneously (e.g., physical con-
        straints), stating this fact,
     3. adding all the necessary variables in each requirement:
      (R1′ ) If v1_up and not v1_down → set v_out.
      (R2′ ) If v1_down and not v1_up → reset v_out.

1  FUNCTION_BLOCK req_priorities
2      VAR_INPUT
 3         v1_up : BOOL;
 4         v1_down : BOOL;
 5     END_VAR
 6     VAR_OUTPUT
 7         out : BOOL;
 8     END_VAR
 9 BEGIN

10     IF v1_up THEN
11         v_out := TRUE;
12     END_IF;
13     IF v1_down THEN
14         v_out := FALSE;
15     END_IF;
16 END_FUNCTION_BLOCK


    Listing 1.3. PLC code implementing a solution for ambiguous requirements where the
    priorities are not set.
                    Formal Verification as a Service: A CERN-GSI Case Study                                                         21

                                                                     Req. manual mode

             Manual mode                                                                                           Auto mode
                                                                         Req. auto mode
                                         Re                                                                  ∧
                                           q.                                                              de de
                                              ma                                                         mo mo
                                                nu                                                     d  al
                                                               al                                   ce
                           Re                                     mo                             for anu
                             q.
                                f                                    d                       e q. . m
                                       orc                               e                  R e   q
                                          e      d                                              R
                                                     mo                                      ¬
                                                        d  e

                                                                              Forced mode


                   Fig. 16. Example of an incomplete state machine.


Incomplete diagram. Let us take the state machine from Figure 16. It repre-
sents how a system can change its operation mode by requesting it. From manual
mode, it is possible to transition to auto mode and to forced mode. However, it
is not specified what happens when the corresponding requests to transition to
auto mode and to forced mode are both true simultaneously. This is also the
case for the transitions between auto mode to manual mode and forced mode.

        ¬ Req. forced mode ∧                                                                                 ¬ Req. manual mode ∧
         ¬ Req. auto mode                                           Req. manual mode                          ¬ Req. forced mode


           Manual mode                                            Req. auto mode ∧                                 Auto mode
                                                                  ¬ Req. forced mode
                                      Re                                                                    ∧
                                        q.                                                               de de
                                           ma                                                          mo o
                                              n        ua                                            ed al m
                                                                                                   c
                         Re                               l    mo                               for anu
                              q.
                                                                    de                       q.      m
                                 f   orc                                                   Re eq.
                                         e   d                                                R
                                                 mo                                         ¬
                                                      de

                                                                             Forced mode

                                                                  ¬ Req. manual mode


Fig. 17. Example of how the incomplete state machine from Figure 16 can be fixed.

    In order to fix this situation, one needs to specify all the necessary conditions
for each guard so that only one transition is activated at a time. Figure 17 shows
a possible fix to the previous ambiguous state machine. Now, if the system is
in manual mode and there is a simultaneous request to transition both to auto
mode and to forced mode, the system will transition to forced mode.

Lack of explanation. In some cases, we experienced situations where there
was a lack of explanation about certain requirements.
 – Global/Shared/Input-Output variables. When a project comprises dif-
   ferent modules, some variables flow from one module to another. They are
   part of the output variables in one module and of the inputs in other modules.
   Since the requirements are usually formalized per module, these variables can
   be treated as inputs in some modules. However, they are not free inputs for
22       Ignacio D. Lopez-Miguel et al.

      those modules in the sense that they can only take a limited set of possible
      values given by the output of the other module. This fact is usually not
      stated, leading to the violation of properties with values for those variables
      that are not possible. A possible way to formally verify these situations is
      by using assume-guarantees (possible with PLCverif) or contracts.
      Figure 18 shows an example in which the variable v1 is an output of module
      1 and an input of modules 2 and 3. In this case, v1 cannot take any value
      and is limited to the possible values produced by module 1. Therefore, if a
      requirement for module 2 or 3 includes this variable, it might be violated
      with a value for v1 that can never happen. Requirement engineers might
      have already in mind that the value for that variable is limited to a specific
      range given by module 1 but might not have specified it when writing the
      requirements for modules 2 and 3.
                                        inputs                   outputs
                                                      Module 2

                                            v1
                        inputs               outputs
                                 Module 1

                                                 v1
                                        inputs                   outputs
                                                      Module 3


Fig. 18. Example of modules in which a variable v1 is the output from one of them
and the input for the other two.

      As an example, let us take the code for module 1 and module 2 from List-
      ing 1.4 and the following requirement:
  (R3 ) Always, at the end of the execution of module 2, v_2=TRUE.
  1 FUNCTION_BLOCK module_1
  2     VAR_OUTPUT
  3         v_1 : BOOL;
  4     END_VAR
  5 BEGIN

  6     v_1 := FALSE;
  7 END_FUNCTION_BLOCK

  8

  9 FUNCTION_BLOCK module_2
 10     VAR_INPUT
 11         v_1 : BOOL;
 12     END_VAR
 13     VAR_OUTPUT
 14         v_2 : BOOL;
 15     END_VAR
 16 BEGIN

 17     v_2 := NOT v_1;
 18 END_FUNCTION_BLOCK


                                 Listing 1.4. Module 1.
                Formal Verification as a Service: A CERN-GSI Case Study       23

  If we only verify module 2 for every possible value of v_1, we would get the
  counterexample {v_1=TRUE, v_2=FALSE}. However, v_1 only takes the value
  FALSE at the end of module 1, which is the input of module 2. Therefore,
  this counterexample is not real.
  An option to specify this requirement is shown below. We have the assump-
  tion from R4 and the conditional requirement R3′ based on this assumption.
  Now, no counterexamples would be found.
(R4 ) Always, at the end of the execution of module 1, v_1=FALSE.
(R3′ ) Given that v_1=FALSE at the beginning of module 2, always, at the end
       of the execution of module 2, v_2=TRUE.
  Nevertheless, it is important to note that modules are recommended to be
  robust to any possible input values. It can happen that, due to, e.g., hardware
  failures, variables take other values that were not supposed to take.
– Timers. When time is involved in the system, formalizing requirements
  becomes harder and more error-prone. In this case, every step needs to be
  formalized, such as when timers are activated, what happens before reaching
  the total time, what happens afterward, how it is reset, etc.
  Figure 19 shows a state machine in which it is possible to transition from
  mode 1 to mode 2 if φ is true after a certain amount of time. However, it is
  not specified if and how the timer is reset and what happens if φ is not true.
  On the other hand, in Figure 20, we have created a timed automaton speci-
  fying how the timer (clock) works. It can also be reset if ψ is true.

                       φ
            Mode 1           Mode 1’        Timer 3s            Mode 2



              Fig. 19. Example of diagram with ambiguous timer.

                ¬φ



                           ψ, t ≤ 3s
                                                       t > 3s
              Mode 1                   Mode 1’                    Mode 2
                           φ, t := 0


     Fig. 20. Example of timed automaton representing the use of a timer.
