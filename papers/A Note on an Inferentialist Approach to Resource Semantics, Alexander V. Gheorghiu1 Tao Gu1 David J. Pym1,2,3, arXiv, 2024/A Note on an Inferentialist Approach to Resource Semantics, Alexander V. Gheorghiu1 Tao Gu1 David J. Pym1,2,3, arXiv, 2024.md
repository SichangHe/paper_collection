                                                       A Note on an Inferentialist Approach to Resource Semantics

                                                                   Alexander V. Gheorghiu1               Tao Gu1         David J. Pym1,2,3

                                                                         {alexander.gheorghiu.19, tao.gu.18, d.pym}@ucl.ac.uk

                                             A central concept within informatics is that of a distributed system (Coulouris et al., 2011).
                                         From the systems modelling perspective, with a little abstraction, one can think of a distributed
arXiv:2405.06491v1 [cs.LO] 10 May 2024




                                         system as comprising delimited collections of interconnected component systems (Collinson et al.,
                                         2012; Caulfield and Pym, 2015). These systems ultimately comprise interconnected locations, at
                                         which are situated resources, relative to which processes execute — consuming, creating, moving,
                                         combining, and otherwise manipulating resources as they evolve, so delivering the system’s ser-
                                         vices. This broad definition applies across the many complex socio-economic-technical systems
                                         that define and support our world including physical and organizational infrastructure (e.g., city
                                         roads, management structures, etc.), telecommunication networks (e.g., the world wide web),
                                         and real-time process control systems (e.g., aircraft control systems).
                                             An important use of logic is to represent, understand, and reason about such systems; this
                                         determines the field of logical systems modelling. To this end, one requires an interpretation
                                         of logical formulae in terms of the resources and states of the system; such an interpretation is
                                         called a resource semantics of the logic. We propose the following encompassing definition:
                                                 A resource semantics for a system of logic is an interpretation of its formulae as assertions
                                                 about states of processes and is expressed in terms of the resources that are manipulated by
                                                 those processes.
                                         There is no intended restriction on the assertions that are to be included in the scope of this
                                         definition and assertions may refer not only to ground states but may also be ‘higher-order’
                                         statements about state transitions. Moreover, the manipulation of resources by the system’s
                                         processes is general and includes, inter alia, consuming/using resources, creating resources,
                                         copying/deleting resources, and moving resources between locations.
                                             There are, perhaps, two canonical examples of resource interpretations of logics that merit
                                         discussion, the number-of uses reading of Linear Logic (LL) (Girard, 1987) and the sharing/sepa-
                                         ration reading of the logic of Bunched Implications (BI) (O’Hearn and Pym, 1999). While both
                                         are applicable to systems modelling, these two readings work in different ways and are related
                                         to different ways of doing the modelling. The number-of-uses reading (Lafont, 1993; Hoare,
                                         1985) for LL concerns the dynamics of the system: formulae denote processes and resources
                                         themselves. Note, it is available only through LL’s proof theory, and is not reflected in LL’s
                                         truth-functional semantics (Girard, 1995). Meanwhile, the sharing/separation reading (Pym,
                                         2019) of BI concerns the composition and state of the system; this is best exemplified by its
                                         essential place in program verification — see, for example, the use of Separation Logic (Reynolds,
                                         2002). It proceeds through the (ordered-monoidal/relational) model-theoretic semantics of BI.
                                             Both readings are useful, but they are individually limited for systems modelling: shar-
                                         ing/separation expresses the structure of distributed systems, and number-of-uses expresses
                                          1
                                              Department of Computer Science, University College London, London WC1E 6BT, UK
                                          2
                                              Department of Philosophy, University College London, London WC1E 6BT, UK
                                          3 Institute of Philosophy, University of London, London WC1E 7HU, UK
the dynamics of the resources involved. Also, they operate in completely different paradigms:
number-of-uses proceeds from LL’s proof theory, while sharing/separation proceeds from the se-
mantics of BI. We suggest that proof-theoretic semantics (P-tS) (Schroeder-Heister, 2018) offers
a unified framework for resource semantics able to express both parts of a distributed system.
    In the semantic paradigm of P-tS, inferentialism, meaning emerges from rules of infer-
ence (Brandom, 2000). This stands in contrast to, for example, denotationalism, wherein
the meaning of logical structures is grounded in reference to abstract algebraic structures, as in
model-theoretic semantics. Much of the groundwork for P-tS has been provided by Prawitz
(2006 [1965]), Dummett (1991), Schroeder-Heister (2006), and Piecha and Schroeder-Heister
(2019).
    Recently, Gheorghiu et al. (2023) and Buzoku (2024) have provided P-tS for (intuitionistic)
LL, and Gu et al. (2024) have provided P-tS for BI, all building on essential work by Sandqvist
(2015). Relative to these results, Gheorghiu et al. (2024) have initiated an inferentialist ac-
count of resource semantics that uniformly expresses both number-of-uses readings and shar-
ing/separation interpretations of the logics. Moreover, they have illustrated its application to
both modelling the security architecture of an airport and to multi-factor authentication.
    These semantics are all given by an inductively defined judgment relation called support such
that transmission of validity is defined as follows:
                 S(·)                                   U             S(U )
             Γ   B ϕ    iff   ∀C ⊇ B, ∀U ∈ R(A), if     C Γ, then     C     ϕ            (Gen-Inf)

Let us spell out each ingredient of (Gen-Inf) and their roles in the resource semantics, which
describes the execution of a certain policy in a system:
   – ϕ specifies an assertion describing (a possible state of) the system

   – Γ specifies a policy describing the executions of a system’s processes

   – R(A) is some concept of atomic resource

   – S(·) is some contextual atomic resource — that is, whenever S(·) is combined with some
     atomic resource in U ∈ R(A), it returns a ‘richer’ atomic resource S(U )

   – B, C are ‘bases’ (a basic concept in P-tS) and model the policy governing the system
     described by the assertions.
                                                            S(·)
Putting these all together, the support judgement Γ B ϕ says that, if policy Γ were to
be executed with contextual resource S(·) based on the model B, then the result state would
satisfy ϕ. (Gen-Inf) explains how such execution is triggered: for arbitrary model C that extends
B, if policy Γ is met in model C using some resource U , then Γ could be executed, and the
resulting state — which consumes U in the available contextual resource S(·) — satisfies ϕ. This
summarizes an inferentialist approach to resource semantics.
    Distributed systems play a crucial role in society and logic is a primary tool for representing,
understanding, and reasoning about them, with resource semantics being a key tool. Adopting
logical inferentialism, particularly through recent advancements in the proof-theoretic semantics
of substructural logics used to handle the two primary approaches to resource semantics, offers
a unified approach for handling resource semantics in the logical modelling of systems. This ap-
proach not only encapsulates existing methodologies but also introduces novel, refined features,
enhancing our capabilities in this domain.

                                                 2
References

Brandom, R. (2000), Articulating Reasons: An Introduction to Inferentialism, Harvard Univer-
  sity Press.
Buzoku, Y. (2024), ‘A Proof-theoretic Semantics for Intuitionistic Linear Logic’,
  arXiv:2402.01982. Submitted.
Caulfield, T. and Pym, D. (2015), Modelling and simulating systems security policy, in Proc.
  8th SIMUTools ’15, ICST, 9–18.
Collinson, M., Monahan, B. and Pym, D. (2012), A Discipline of Mathematical Systems Mod-
  elling, College Publications.
Coulouris, G., Dollimore, J., Kindberg, T. and Blair, G. (2011), Distributed Systems: Concepts
  and Design, 5th edn, Addison-Wesley.
Dummett, M. (1991), The Logical Basis of Metaphysics, Harvard University Press.
Gheorghiu, A. V., Gu, T. and Pym, D. J. (2023), Proof-theoretic Semantics for Intuitionistic
  Multiplicative Linear Logic, in R. Ramanayake and J. Urban, eds, ‘Automated Reasoning
  with Analytic Tableaux and Related Methods — TABLEAUX’, Springer, pp. 367–385.
Gheorghiu, A. V., Gu, T. and Pym, D. J. (2024), ‘Inferentialist resource semantics’,
  arXiv:2402.09217. Accepted at Mathematical Foundations of Programming Semantics —
  MFPS, 2024.
Girard, J.-Y. (1987), ‘Linear Logic’, Theoretical Computer Science 50(1), 1–101.
Girard, J.-Y. (1995), Linear Logic: its syntax and semantics, in ‘Advances in Linear Logic’,
  LMS Lecture Notes, CUP, 1–42.
Gu, T., Gheorghiu, A. V. and Pym, D. J. (2024), ‘Proof-theoretic-semantics for the Logic of
  Bunched Implications’, arXiv:2311.16719.
Hoare, C. A. R. (1985), Communicating Sequential Processes, Prentice-Hall International.
Lafont, Y. (1993), ‘Introduction to Linear Logic’. Lecture notes from TEMPUS Summer School
  on Algebraic and Categorical Methods in Computer Science, Brno, Czech Republic.
O’Hearn, P. W. and Pym, D. J. (1999), ‘The Logic of Bunched Implications’, Bulletin of Symbolic
  Logic 5(2), 215–244.
Piecha, T. and Schroeder-Heister, P. (2019), ‘Incompleteness of Intuitionistic Propositional Logic
  with respect to Proof-theoretic Semantics’, Studia Logica 107(1), 233–246.
Prawitz, D. (2006 [1965]), Natural Deduction: A Proof-theoretical Study, Courier Dover Publi-
  cations.
Pym, D. J. (2019), ‘Resource Semantics: Logic as a Modelling Technology’, ACM SIGLOG
  News 6(2), 5–41.
Reynolds, J. C. (2002), Separation Logic: A Logic for Shared Mutable Data Structures, in Proc.
  LICS 2002, IEEE, 55–74.
Sandqvist, T. (2015), ‘Base-extension Semantics for Intuitionistic Sentential Logic’, Logic Jour-
  nal of the IGPL 23(5), 719–731.
Schroeder-Heister, P. (2006), ‘Validity Concepts in Proof-theoretic Semantics’, Synthese
  148(3), 525–571.
Schroeder-Heister, P. (2018), Proof-Theoretic Semantics, in E. N. Zalta, ed., ‘The Stanford
  Encyclopedia of Philosophy’, Spring 2018 edn.




                                                3
