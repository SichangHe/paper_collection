                                               Vision: An Extensible Methodology for Formal
                                               Software Verification in Microservice Systems
                                                     1st Connor Wojtak                                   2nd Darek Gajewski                              3rd Tomas Cerny
                                           Electrical and Computer Engineering                  Electrical and Computer Engineering             Electrical and Computer Engineering
                                                    University of Arizona                                University of Arizona                           University of Arizona
                                                   Tucson, Arizona, USA                                 Tucson, Arizona, USA                            Tucson, Arizona, USA
                                                 connorwojtak@arizona.edu                               dgajewski@arizona.edu                             tcerny@arizona.edu



                                           Abstract—Microservice systems are becoming increasingly                         static analysis exist for addressing concerns like verifying se-
arXiv:2509.02860v1 [cs.SE] 2 Sep 2025




                                        adopted due to their scalability, decentralized development,                       curity policies or analyzing system architecture, these existing
                                        and support for continuous integration and delivery (CI/CD).                       approaches have significant limitations and costs [6].
                                        However, this decentralized development by separate teams
                                        and continuous evolution can introduce miscommunication and                            Considering E2E tests, microservice systems inherently use
                                        incompatible implementations, undermining system maintain-                         more endpoints and connections due to their basis on inter-
                                        ability and reliability across aspects from security policy to                     service communication. Thus, a more extensive suite of E2E
                                        system architecture. We propose a novel methodology that                           tests is needed to comprehensively verify the entire system.
                                        statically reconstructs microservice source code into a formal                     This places significant burden on development and operations
                                        system model. From this model, a Satisfiability Modulo Theories
                                        (SMT) constraint set can be derived, enabling formal verification.                 teams to maintain full coverage for E2E service verification.
                                        Our methodology is extensible, supporting software verification                    Microservices also often undergo continuous small, iterative
                                        across multiple cross-cutting concerns. We focus on applying the                   changes [1], meaning tests can easily fall out of date or fail
                                        methodology to verify the system architecture concern, present-                    to provide complete coverage, making complete verification
                                        ing formal reasoning to validate the methodology’s correctness                     even more time consuming for developers. In addition, com-
                                        and applicability for this concern. Additional concerns such as
                                        security policy implementation are considered. Future directions                   prehensive testing can be compute-intensive, which can incur
                                        are established to extend and evaluate the methodology.                            significant cost as microservice systems scale [6].
                                           Index Terms—Microservices, Verification, Static Analysis, Sys-                      While some existing static analysis techniques address these
                                        tem Modeling, SMT Solving, Maintainability, Decentralization                       shortcomings, they also have limitations. They may focus on
                                                                                                                           one concern and check rules exclusively rather than simulta-
                                                                   I. I NTRODUCTION                                        neously to ensure a system satisfies a concern [7].
                                                                                                                               We propose a static and extensible methodology for formal
                                           The integration of cloud-native systems within modern en-                       software verification in microservice systems by reverse engi-
                                        terprises has redefined the landscape of software architecture,                    neering system source code into an intermediate formal model.
                                        particularly through the adoption of Microservice Architecture                     From this, an extensible constraint model can be generated that
                                        (MSA) [1]. However, while considerable work has been done                          unifies rules for cross-cutting concerns. Using the constraint
                                        to model and formally verify monolithic and cloud-native                           model, an SMT solver can verify a system satisfies all con-
                                        systems such as in reviews by Jawaddi et al. [2] and Souri                         straints for every concern considered or modify the system
                                        et al. [3], we find little work that performs formal software                      to satisfy them. This approach addresses limitations in both
                                        verification in microservices systems at the application layer.                    existing static analysis and testing methods, revolutionizing
                                           Microservices, unlike monolithic and cloud-native systems,                      application-level software verification in microservice systems
                                        are generally developed by separate development teams in                           by reducing developer burden, development costs, and testing
                                        separate repositories [4]. This fragmented approach to de-                         costs through the application of formal methods.
                                        velopment means that developers lack a complete overview                               This paper is organized as follows. Section II elaborates on
                                        of the system, which increases the burden for cross-cutting                        the problem’s background and related work. Section III iden-
                                        concerns such as security, business, and system architecture.                      tifies our methodology. Section IV presents formal discussion
                                        This is compounded by a lack of centralized governance in                          and validation of our methodology. Section V outlines our
                                        microservice systems to verify concerns are properly addressed                     future research questions. Section VI concludes our paper.
                                        [1], [5]. While solutions such as end-to-end (E2E) testing or
                                                                                                                                     II. BACKGROUND AND R ELATED W ORK
                                           © 2025 IEEE. Personal use of this material is permitted. Permission from           With the widespread adoption of MSA, tools to perform
                                        IEEE must be obtained for all other uses, in any current or future media,          dynamic analysis and static analysis for MSA have been
                                        including reprinting/republishing this material for advertising or promotional
                                        purposes, creating new collective works, for resale or redistribution to servers   growing in number. Analysis or testing of software systems
                                        or lists, or reuse of any copyrighted component of this work in other works.       serves multiple aspects, mainly to keep a system reliable and
available. The DevOps Research and Assessment (DORA)                a three-stage process, as shown in Figure 1, in which we
metrics, which measure the frequency of deployments and             create an intermediate model, create an SMT constraint model,
issues, are critical for any enterprise to measure. These four      and perform consistency verification. The intermediate model
metrics are the frequency of deployments, the number of issues      encodes various aspects of the system such as architecture,
caused by deployments, the lead time needed for a successful        authorization policy, data entities, and other additional aspects.
push to production, and the mean time to recovery [8].              These are then traversed to generate constraints to enforce
   Dynamic analysis, which involves real-time testing or profil-    rules for various concerns, which are supplied to an SMT
ing of systems, has been used to detect issues or architectural     solver to determine if the system satisfies the generated rules.
degradation in the system. Maruf et al. [9] combine dynamic         We focus on describing encodings and constraints for verify-
analysis tools with anomaly detection, utilizing quality met-       ing the system architecture concern shown in Figure 1. We
rics and anti-patterns, to detect architectural degradation in      also discuss possible extensions for the authorization policy
microservice systems. Sotomayor et al. [10] make use of             concern. We describe the encoding of the intermediate model,
runtime testing in microservices and look at different levels of    generation of the SMT constraint model, and constraint solving
testing tools for unit testing, performance testing, and system     in Sections III-A, III-B, and III-C, respectively.
verification. However, this can be expensive, especially with
MSA, as the log volume and telemetry data grows with the            A. Intermediate Model Encoding
number of services within the microservice environment [6].            1) Model Definition: Applying static analysis techniques on
   While static analysis methods cannot replace specific test-      the microservice system code repositories, such as traversing
ing, such as performance testing of systems, the use of static      an abstract syntax tree or performing pattern matching, allows
analysis can be employed to perform software verification at a      for the extraction of the system architecture, data entities, and
significantly lower cost and time, leading to the discovery of      security policies ((1) and (2) in Figure 1). We then create an
issues before they are deployed into real-time environments.        intermediate model ((3) in Figure 1) where we formally define
   Existing tools, such as CIMET [7], can utilize static analysis   a microservice system as a tuple with four core attributes,
to identify architecture rules that are violated across multiple    extensible by an arbitrary number of additional attributes:
microservices repositories. However, a tool like this can only
consider antipatterns one at a time when scanning the code                         S “ pM, E, E_parent, G, . . .q
repository, and is also unable to suggest changes. Our tool
will be able to consider all the rules simultaneously, allowing     Where:
for fixes to incorporate these rules without introducing further      M “ tM S1 , . . . , M Sn u is the set of microservices.
degradation in the system. Cerny et al. [11] catalog antipatterns     E “ tE1 , . . . , Em u is the set of all endpoints. Many
in microservices, which tools like CIMET [7] can detect.                  endpoints belong to a single microservice.
Abdelfattah et al. [12] apply ReSSa, a predecessor to CIMET           E_parent : E Ñ M maps an endpoint to its single parent
for static analysis, to enumerate data entity accesses along              microservice.
endpoint call chains to calculate access rights.                      G Ď E ˆ E is the directed graph representing remote service
   Formal methods have been previously used for software                  calls between endpoints.
verification. However, methods such as Armando et al. [13],            Now consider the concern that a microservice system sat-
which formalizes methods for authorization policy consistency,      isfies a set of architectural rules (ARs) to prevent antipatterns
or Lattuada et al. [14], which makes use of a solver for            from forming. Examples of such antipatterns could include
eliminating bugs in software, are designed to address issues        cyclic dependencies between endpoints or microservices with a
in traditional monolithic systems.                                  large number of inbound or outbound connections. These rules
   There are some cloud-native solutions such as how Backes         primarily depend on the endpoints and service calls between
et al. [15] utilizes AWS’ Zelkova system and formal methods         them; however, an extension of the model is necessary to
to verify IAM policies. Additionally, Panda et al. [16] dis-        identify cyclic dependencies. Thus, the following extension
cusses formal methods for verifying communication behaviors         of S, SAR , can be defined as follows:
between microservices. However, these solutions are at the
infrastructure layer and network layers, respectively — not at            SAR “ pM, E, E_parent, G, L, L_endpointq
the application layer working with the system source code.
                                                                    Where:
This is echoed by other systematic literature reviews such as
Souri et al. [3] or Jawaddi et al. [2] that identify little to no    M, E, E_parent, and G are the same as defined in S.
work on formal software verification in microservice systems         L “ pℓ1 , . . . ℓm q defines the topological ordering of
at the application layer. Our methodology aims to fill this gap.         endpoints where m is the size of E and
                                                                         @i P t1, . . . , mu, ℓi P Z and Z is the set of integers.
                     III. M ETHODOLOGY                               L_endpoint : E Ñ L maps an endpoint Ei to its
  Formally verifying a microservice system requires encoding             ordering Li .
aspects of the system into an SMT constraint model that can be        On the other hand, consider the concern of enforcing
supplied to any SMT solver such as Z3 or CVC5. We propose           authorization policy at the endpoint and data entity levels in
      A     Intermediate Model Encoding                      B    SMT Constraint Model Generation                           C   Consistency Verification

                                                                                                 6                                                        Satisfiable
                    1                                   4                   5                         Generate
    Traversal of                       2                   Generate              Generate                ...                              Satisfiable?
                                            Pattern      Authorization            System             Constraints          8                              YES
   Abstract Syntax
                                           Matching         Policy              Architecture                               Verify Model
        Tree
                                                          Constraints           Constraints                                      via             NO
                           Code
                                                                                                                            SMT Solver
                        Repositories                                                                                                        Solve for 9
                                                                                                                             (i.e., Z3)
                                                      Authorization Policy System Architecture           ...                               Modifications
                                                             Endpoint                                                                           via
                                                                                No Hub-Like                                                 Optimizer
                                                            Permitted
                                                                                 Services                ...                                (i.e., Z3)
                                                              Roles             Constraint
      3         Intermediate Model                          Constraint
                                                              Data              No Long Call                                                               Satisfiable
                               System                         Entity                                                                NO
              System                                                              Chains                 ...                               Satisfiable?
                             Authorization                  Operations          Constraint
            Architecture                                                                                                                                  YES
                                Policy                      Constraint
                                                                 ...                 ...                 ...
                                   ...
             System
                               (Additional                                                                                                Unsatisfiable
           Data Entities                                                                                       7     SMT
                                Aspects)
                                                                                                                   Constraint                             Modifications
                                                                                                                    Model

Fig. 1. An overview of the verification process, starting with the creation of an intermediate model from which various constraint sets can be generated.
These sets form a constraint model that can be supplied to a solver to verify the microservice system.

a microservice system. Then, the following extension of S,                           enable the enforcement of business rules related to personally
Sauthorization , can be defined as follows:                                          identifiable information in later steps. This model makes
                                                                                     some simplifications compared to a real-world microservice.
          Sauthorization “ pM, E, E_parent, G, D, A, O,                              For example, G is simplified in that endpoints might make
                A_operations, R, E_permitted, . . .q                                 remote service calls based on a condition rather than on
                                                                                     every invocation of an endpoint. However, for our constraints
Where:
                                                                                     addressing the authorization policy and architecture concerns,
 M, E, E_parent, and G are the same as defined in S.                                 whether a service call is conditional is irrelevant. Instead, the
 D “ tD1 , . . . , Dh u is the set of data entities.                                 potential for a service call to be made from one endpoint to
 A “ tA1 , . . . , Aj u is the set of data entity accesses for an                    another is enough to identify it as a call in G. However, if a
     entity in D (where an entity is created, read, etc.).                           constraint were to arise requiring information on conditional
     There is at most one data entity access for each data                           service calls, S could be extended to include which calls are
     entity in D for each endpoint in E.                                             made only under particular conditions. Thus, simplifications
 O “ tO1 , . . . , Ok u is the set of possible operations that can                   made by the model can likely be addressed by extending the
     be performed on a data entity (often consisting of four                         model.
     entries: create, read, update, and delete).                                        2) Model Representation: Having defined the formal model
 A_operations : A Ñ PpOq maps an instance of a data                                  S and its extensions, we now describe how this model is
     entity access to the set of operations the access                               encoded into a solver-compatible format so that an SMT
     performs (where PpOq is the power set of O).                                    constraint model can then be generated.
 R “ tR1 , . . . , Rℓ u is the set of possible roles users can                          For S:
     assume in the microservice system.
                                                                                      M can be represented as a set M where Mi P M is a
 E_permitted : E Ñ PpRq maps an endpoint to the set
                                                                                          subset of distinct endpoints from E where i P r0, n ´ 1s.
     of roles (where PpRq is the power set of R).
                                                                                      E can be represented as a set E where each Ei P E “ i
   These two extensions can be combined into a single exten-                              where i is an integer and i P r0, m ´ 1s.
sive model Scombined for authorization policy and architectural                       E_parent can be represented as an array of integers
rule verification. This could be defined as:                                              Eparents where each element Eparentsi is an integer
  Scombined “ pM, E, E_parent, G, L, L_endpoint, D,                                       j P r0, n ´ 1s such that Eparents piq “ j, where
                                                                                          i P r0, m ´ 1s corresponds to an endpoint in E and j
              A, O, A_operations, R, E_permitted, . . .q                                  corresponds to the endpoint’s parent microservice in M.
where each variable listed is as defined previously in S, SAR ,                       G can be represented as an adjacency list or matrix G such
and Sauthorization .                                                                      that Grisrjs “ T rue iff there is an edge from Ei to Ej
   As needed, additional variables could be added to address                              for i P E, j P E. Otherwise Grisrjs “ F alse.
further concerns. For example, variables such as fields or                              For SAR :
attributes of data entities can be added to the model to                              L can be represented as an integer array L of size m.
 L_endpoint, in practice, is subsumed by the array L                  constraint preventing cyclic dependencies, Ccycle , is defined as
    where the topological order of endpoint Ei , is simply            follows based on the model Scombined :
    given by Lris.                                                                                ľ
                                                                                      Ccycle “         Lres ă Lre1 s
                                                                                                 pe,e1 qPG
B. SMT Constraint Model Generation
   Once the microservice system is encoded into an intermedi-            4) Constraints for Other Concerns: While we only for-
ate model (S or one of its extended versions), the intermediate       mally define constraints for the architectural concern, con-
model can be traversed to generate constraints that address           straints can be generated for other concerns. For example,
various concerns (such as (4), (5), and (6) in Figure 1).             consider the concern regarding authorization policies. Con-
                                                                      straints could be generated to ensure roles have consistent
   We provide examples of constraints that can be enforced for
                                                                      access to data entities across microservices and constraints to
the system architecture concern, which focuses on preventing
                                                                      ensure authorized roles can complete call chains. Using the
common microservice antipatterns [11]. From this catalog of
                                                                      extended model Sauthorization , it is feasible to enforce said
antipatterns, we formally define three constraints to identify
                                                                      constraint, as it contains information about permitted roles to
and prevent hub-like dependencies and cyclic dependencies.
                                                                      endpoints, data entity operations, and relationships between all
For G, we consider only the edges that are present in the
                                                                      the endpoints, data entities, etc.
system at the time of analysis. We do not allow the solver to
suggest adding edges to the system (only removing existing               As the constraints are generated, they can be stored together
ones), as traversing the entire E ˆ E graph search space would        to form a unified SMT constraint set ((7) in Figure 1).
be intractable.                                                       When generating the architectural and security constraints,
                                                                      we hold all sets of variables in the model constant except
   1) No Intraservice Remote Calls Constraint: In a microser-
                                                                      for the system connections (G) and the endpoint permitted
vice system, generally no endpoint should make a remote ser-
                                                                      roles (E_permitted). Variables are held constant either by
vice call to another endpoint in the same microservice; instead,
                                                                      directly creating a constraint that ensures the variable matches
they should invoke service functions programmatically. This
                                                                      the actual system or by generating constraints programmat-
also subsumes a rule that no endpoint can make a remote
                                                                      ically on the assumption that a variable is held constant.
service call to itself. The constraint enforcing this rule, Cnirc ,
                                                                      When considering different concerns, different combinations
is defined as follows based on the model Scombined :
                                                                      of variables could be held constant based on which aspects of
                  ľ                                                   the system should be changed to address the concern.
     Cnirc “             E_parentpe1 q ‰ E_parentpe2 q
              pe1 ,e2 qPG
                                                                      C. Consistency Verification
  2) No Hub-like Dependencies Constraint: In a microser-                 After the constraint set is complete, an SMT solver ((8) in
vice system, a hub-like dependency introduces centralization,         Figure 1) can be used to verify that the microservice system
which can lead to scalability issues in a microservice system         meets the defined rules or constraints. We can create a verifier
and introduce a single point of failure as many services              by taking a constraint system and holding all variables constant
depend on it [11]. This translates into our problem space as a        via constraints that assert the variables match the actual state of
microservice having a large number of endpoints with many             the microservice system. This verifier can determine whether
inbound and outbound connections. The constraint preventing           the existing system satisfies the constraints for each concern.
these hub-like dependencies, Chub , is defined as follows based          On the other hand, if the existing system fails to satisfy the
on the model Scombined :                                              constraints for each concern, an optimizer ((9) in Figure 1)
              ľ       ÿ                                               such as Z3’s optimizer can take the original constraint system
    Chub “        r          pconnEj ,e ` conne,Ej qs ą τ             and solve for a set of variables that makes the system conform
             Mi PM Ej PMi ,ePE
                                                                      to the constraints, with an objective function that minimizes
Where:                                                                the number of changes that made to the existing microservice
                                                                      system. This objective function was selected as, while it may
 connEa ,Eb “ 1 iff Grasrbs “ T rue and connEa ,Eb “ 0                suggest changes that are not optimal due to missing high-
     otherwise.                                                       level context or reasoning (i.e., suggesting regular users be
 τ is a user-defined threshold that, for higher values, permits       able to access an admin-only endpoint to satisfy a constraint),
     more dependency on a single microservice, and for                it provides locations in the system for developers to investigate
     lower values, permits less dependency on a single                the best solution to the inconsistency.
     microservice.                                                       As the system scales to have a large number of microser-
   3) No Cyclic Dependencies Constraint: In a microservice            vices and endpoints, or the number of concerns simultaneously
system, a cyclic dependency occurs when a call to an endpoint         considered increases, the number of constraints generated
triggers a chain of remote service calls that ultimately lead         could feasibly become intractible to satisfy. In these situations,
back to the original endpoint [11]. More formally, it means           it may be prudent to consider the constraint set for each
that G contains a cycle and cannot be topologically sorted. The       concern separately to maintain efficient running time. While
                               TABLE I                                                                    TABLE II
                   M ODEL TO S YSTEM T RACEABILITY                                           I DENTIFIED S YSTEM C ONNECTIONS

    Model Component                 Extracted From                           Endpoint Paths                                         Encoding
    M: Microservices                Project structure, manifest files,       GET /adminbasic/contacts to GET                       E0 ñ E21
                                    build files (i.e., a pom.xml file)       /contactservice/contacts
    E: Endpoints                    REST controller definitions and          DELETE /adminbasic/contacts/{contactsId} to           E1 ñ E22
                                    route annotations/decorators             DELETE /contactservice/contacts/{contactsId}
    E_parent: Endpoint Parents      Location of controller definitions in    PUT /adminbasic/contacts to PUT                       E2 ñ E23
                                    project structure                        /contactservice/contacts
    G: Call Graph Edges             Traversal of abstract syntax tree        POST /adminbasic/contacts to POST                     E3 ñ E24
                                    connecting endpoints and REST            /contactservice/contacts/admin
                                    calls (with REST calls identified via    GET /adminbasic/prices to GET                         E4 ñ E29
                                    framework-specific calls)                /priceservice/prices
    L: Ordering of Endpoints        Not extracted from the system —          DELETE /adminbasic/prices/{pricesId} to DELETE        E5 ñ E30
                                    used by the SMT solver to perform        /priceservice/prices/{pricesId}
                                    the topological ordering                 PUT /adminbasic/prices to PUT                         E6 ñ E31
    L_endpoint: Endpoint Ordering   Not extracted from the system —          /priceservice/prices
                                    used by the SMT solver to map an         POST /adminbasic/prices to POST                       E7 ñ E32
                                    endpoint to its ordering                 /priceervice/prices/admin

this limits the solver’s ability to identify a set of variables sat-        [18] due to its size, the number of system connections,
isfying constraints across all concerns, for large microservice             and its focus on representing a real-world microservice sys-
systems, the methodology remains beneficial for identifying                 tem [17] 1 . We select three of 45 microservices to encode
and resolving issues for each separate concern.                             into our model — ts-admin-basic-info-service,
        IV. F ORMAL R EASONING AND S OUNDNESS                               ts-contacts-service, and ts-price-service. We
                                                                            chose these services because they have numerous system
 We present a formal discussion of the base intermediate                    connections and are representative of the rest of the system.
model S, the intermediate model SAR , and the SMT constraint                   We classify ts-admin-basic-info-service as M0
model for addressing the architectural concern.                             and identify 21 endpoints; therefore, M0 “ tE0 , . . . , E20 u.
A. Intermediate Model Soundness                                             Meanwhile, Eparents ris “ 0, @i P r0, 20s, with i correspond-
   1) Extracting Model Information: As a first step in validat-             ing to Ei and Eparents ris corresponding to M0 .
ing our intermediate model, we identify how the information                    We classify ts-contacts-service as M1 and identify
in the model can be extracted from the source code. Table I                 8 endpoints; therefore M1 “ tE21 , . . . , E28 u. Meanwhile,
illustrates each component of SAR (and thus also S) and where               Eparents ris “ 1, @i P r21, 28s, with i corresponding to Ei
each component can be extracted from in the source code.                    and Eparents ris corresponding to M1 .
This does highlight some potential shortcomings. Namely,                       We classify ts-price-service as M2 and identify
the model will only be as accurate as the static analysis                   7 endpoints; therefore M2 “ tE29 , . . . , E35 u. Meanwhile,
that extracts information from the source code. While static                Eparents ris “ 2, @i P r29, 35s, with i corresponding to Ei
analysis can prepare a mostly accurate representation, it is                and Eparents ris corresponding to M2 .
difficult, if not impossible, to generate an exact call graph.                 Since this is the subset of microservices we are consid-
Furthermore, the static analysis tool generally needs to target             ering, M “ tM0 , M1 , M2 u. By definition, each Ei “ i;
a specific programming language, framework, and/or libraries.               therefore, E “ t0, 1, . . . , 35u. Between these endpoints,
   However, based on Table I, we can see that it is possible to             we identify multiple connections from ts-admin-basic-
extract all of the necessary information to a reasonable degree             info-service to ts-contacts-service and ts-
of accuracy. Furthermore, the extraction of the information is              price-service, which are shown in Table II. Based on
generalizable to any language with an abstract syntax tree,                 these connections, for every Ei ñ Ej in Table II, Grisrjs “
meaning that obtaining a highly accurate intermediate model                 T rue. This completes the construction of S from TrainTicket’s
of the system is a matter of developing an accurate enough                  source code.
tool to statically extract the necessary information for each                  Since L is not extracted from the microservice system
programming language, framework, etc. Once a tool is devel-                 but is instead a transitive element used only at the solver
oped for a specific language or framework, it could be used                 level to perform topological ordering of endpoints, L can be
by all projects developed with that language or framework.                  initialized to an array of all zeroes of length m, one entry for
Therefore, we conclude that the definition of our model is                  each endpoint. This completes the construction of SAR from
based on real microservice system constructs and that we can                TrainTicket’s source code.
extract the information necessary to construct the model.                   B. SMT Constraint Model Correctness
   2) Encoding Model Information: To further support the
soundness of our intermediate model, we manually work                         We assert the correctness of the constraint model by pre-
out how a representative subset of the TrainTicket mi-                      senting the following formal proofs.
croservice system benchmark can be encoded into our for-                      1 The TrainTicket repository used is available at https://github.
mal model. We selected TrainTicket [17] as our bench-                       com/FudanSELab/train-ticket. We use the code from commit ID
mark from a dataset of microservice system benchmarks                       313886e99befb94be6cd45f085c98e0019f59829.
 1) No Intraservice Remote Calls Constraint:                           Theorem 3. Based on Proposition 2 and the definition of
Goal: Prove Cnirc ensures that a call from one endpoint                    Ccycle , enforcing Ccycle ensures G has no cycles across
   to another can exist iff both endpoints are in different                the entirety of S and its extensions.
   microservices.                                                        These proofs illustrate that the constraints enforce their
Axiom 1. By definition, E_parent(ei ) gives the microser-             respective rules for the model S and its extensions. Since we
   vice that ei belongs to.                                           demonstrate the soundness of the model, we can also therefore
Lemma 1. By Axiom 1, E_parentpe1 q ‰ E_parentpe2 q                    assert that enforcing these rules for the model also enforces
   asserts that e1 and e2 do not share the same parent                them on the actual microservice system encoded into S or one
   microservices.                                                     of its extended versions, formally illustrating the validity of
Lemma 2. By Lemma 1 and definition of G, Cnirc asserts                both the intermediate model and constraint model.
   that e1 and e2 do not share the same parent microservice
                                                                                       V. R ESEARCH Q UESTIONS
   for each possible edge in G.
Proposition 1. By Lemma 2 and the fact that G is a                       While we have outlined an extensible methodology for ver-
   representation of G, Cnirc asserts that every call in S            ifying concerns in microservice systems, a significant amount
   (and extended versions of S) occurs from @e1 P Mi to               of future work is necessary to fully explore the potential and
   @e2 P Mj where Mi ‰ Mj .                                           limitations of this methodology. We propose three research
Theorem 1. Based on Proposition 1, Cnirc asserts that a call          questions to guide this future work.
   can only occur from an endpoint in one microservice to                RQ1: How does this methodology’s running time, compute
   an endpoint in another unique microservice across all of           resource usage, code coverage, and DORA metrics compare to
   S and its extensions.                                              existing methods that use static analysis (such as programmat-
 2) No Hub-like Dependencies Constraint:                              ically scanning systems and generating metrics) or dynamic
                                                                      analysis (such as performing end-to-end testing)?
Goal: Prove Chub ensures that no microservice has a sum
                                                                         RQ2: How does the methodology’s runtime and compute
   of inbound and outbound calls to and from its endpoints
                                                                      resource usage scale as the number of microservices, number
   that is greater than τ .
                                                                      of endpoints, number of system connections, etc., increase?
Corollary        1.    By      definition    of       connEa ,Eb ,
   ř                                                                  Can specialized solving, optimization, or incremental model
       Ej PMi ,ePE pconnEj ,e ` conne,Ej q sums all inbound           construction techniques be applied to improve scalability?
   connections to Ej from any e P E and outbound
                                                                         RQ3: What other concerns could our methodology be
   connections from Ej to any e P E for every Ej P Mi .
                                                                      extended to address, and what constraints would need to be
Lemma 3. Based on Corollary 1 and definition of τ , Chub
                                                                      generated?
   asserts that the sum from Corollary 1 is less than τ for
                                                                         We propose RQ1 to quantify the potential benefit of our
   @Mi P M .
                                                                      methodology. Meanwhile, we ask RQ2 to identify any poten-
Theorem 2. Based on Lemma 3, Chub ensures that no
                                                                      tial limitations on tractability and efficiency as the number of
   microservice in S and its extensions can have a sum of
                                                                      concerns considered increases and the size of the microservice
   inbound and outbound calls to and from its endpoints that
                                                                      system grows larger. Finally, we identify RQ3 to increase the
   is greater than the threshold τ .
                                                                      utility of the methodology by leveraging its extensibility.
 3) No Cyclic Dependencies Constraint:                                   These research questions can be addressed through a
Goal: Prove that Ccycle ensures graph G (and thus G) contains         combination of formal proofs and empirical experiments on
   no cycles.                                                         microservice system benchmarks or industry systems, when
Axiom 2. By definition of L and E, every endpoint Ei is               possible. Addressing these research questions will help extend
   assigned ordering Li .                                             the methodology and help remedy any current shortcomings
Axiom 3. Ccycle asserts that, for each edge from e to e1 in           of the methodology.
   G, Lres ă Lre1 s.
Corollary 4. Assume there is a cycle present in G consisting                                VI. C ONCLUSION
   of a set of endpoints Y and that Einitial is some endpoint            We advance an extensible methodology for software verifi-
   in the Y . Then Y consists of endpoints such that there            cation in microservice systems. While existing static analysis
   are edges from Einitial to some ei P Y , which may have            and runtime testing techniques can be used to verify concerns
   edges between other ej P Y that eventually lead back to            in microservice systems, our methodology has the potential to
   Einitial .                                                         offer a more cost-effective, maintainable, and comprehensive
Lemma 4. Under the assumption of Corollary 4, applying                approach to verification compared to these existing techniques.
   Axioms 2 and 3 would mean that Lreinitial s ă Lrei s ă                Of course, this methodology is not meant to completely
   . . . ă Lrej s ă Lreinitial s. Since Lreinitial s ă Lreinitial s   replace existing testing and static analysis methods in all use
   is false for @Lreinitial s P Z where Z is the set of integers,     cases. For example, our methodology does not test functional-
   this is a contradiction.                                           ity. However, it does verify that the system meets requirements
Proposition 2. Based on Lemma 4, Axioms 2 and 3 hold iff              for various concerns and has the potential to do this aspect
   there is no cycle present in G.                                    of verification much more efficiently than testing or static
analysis. While there are some potential limitations to our                      [13] A. Armando and S. Ranise, “Automated symbolic analysis of
methodology, the novelty of applying formal methods for                               arbac-policies (extended version),” 2010, arXiv:1012.5590. [Online].
                                                                                      Available: https://arxiv.org/abs/1012.5590
microservice system verification and the potential benefits over                 [14] A. Lattuada, T. Hance, J. Bosamiya, M. Brun, C. Cho, H. LeBlanc,
existing methods make this approach well worth exploring and                          P. Srinivasan, R. Achermann, T. Chajed, C. Hawblitzel, J. Howell,
evaluating.                                                                           J. R. Lorch, O. Padon, and B. Parno, “Verus: A practical foundation
                                                                                      for systems verification,” in Proceedings of the ACM SIGOPS 30th
                                                                                      Symposium on Operating Systems Principles, ser. SOSP ’24. New
                                F UNDING                                              York, NY, USA: Association for Computing Machinery, 2024, p.
   This work was supported by the National Science Founda-                            438–454. [Online]. Available: https://doi.org/10.1145/3694715.3695952
                                                                                 [15] J. Backes, P. Bolignano, B. Cook, C. Dodge, A. Gacek, K. Luckow,
tion under Grant No. 2409933.                                                         N. Rungta, O. Tkachuk, and C. Varming, “Semantic-based automated
                                                                                      reasoning for AWS access policies using SMT,” in 2018 Formal
                              R EFERENCES                                             Methods in Computer Aided Design (FMCAD), 2018, pp. 1–9. [Online].
 [1] T. Černý, M. Donahoo, and M. Trnka, “Contextual understanding of               Available: https://doi.org/10.23919/FMCAD.2018.8602994
     microservice architecture: current and future directions,” ACM SIGAPP       [16] A. Panda, M. Sagiv, and S. Shenker, “Verification in the age of
     Applied Computing Review, vol. 17, pp. 29–45, Jan. 2018. [Online].               microservices,” in Proceedings of the 16th Workshop on Hot Topics
     Available: https://doi.org/10.1145/3183628.3183631                               in Operating Systems, ser. HotOS ’17. New York, NY, USA:
 [2] S. N. A. Jawaddi, M. H. Johari, and A. Ismail, “A review                         Association for Computing Machinery, 2017, p. 30–36. [Online].
     of microservices autoscaling with formal verification perspective,”              Available: https://doi.org/10.1145/3102980.3102986
     Software: Practice and Experience, vol. 52, no. 11, pp. 2476–2495,          [17] X. Zhou, X. Peng, T. Xie, J. Sun, C. Xu, C. Ji, and W. Zhao,
     2022. [Online]. Available: https://doi.org/10.1002/spe.3135                      “Benchmarking microservice systems for software engineering
 [3] A. Souri, N. J. Navimipour, and A. M. Rahmani, “Formal verification              research,” in Proceedings of the 40th International Conference
     approaches and standards in the cloud computing: a comprehensive and             on Software Engineering: Companion Proceeedings, ser. ICSE ’18.
     systematic review,” Computer Standards & Interfaces, vol. 58, pp. 1–22,          New York, NY, USA: Association for Computing Machinery, 2018, p.
     2018. [Online]. Available: https://doi.org/10.1016/j.csi.2017.11.007             323–324. [Online]. Available: https://doi.org/10.1145/3183440.3194991
 [4] D. Amoroso d’Aragona, X. Li, T. Cerny, A. Janes, V. Lenarduzzi, and         [18] D. Amoroso d’Aragona, A. Bakhtin, X. Li, R. Su, L. Adams, E. Aponte,
     D. Taibi, “One microservice per developer: Is this the trend in OSS?”            F. Boyle, P. Boyle, R. Koerner, J. Lee, F. Tian, Y. Wang, J. Nyyssölä,
     in European Conference on Service-Oriented and Cloud Computing.                  E. Quevedo, S. M. Rahaman, A. S. Abdelfattah, M. Mäntylä,
     Springer Nature Switzerland, 2023, pp. 19–34. [Online]. Available:               T. Cerny, and D. Taibi, “A dataset of microservices-based open-source
     https://doi.org/10.1007/978-3-031-46235-1 2                                      projects,” in Proceedings of the 21st International Conference on
 [5] X. Zhou, S. Li, L. Cao, H. Zhang, Z. Jia, C. Zhong, Z. Shan, and                 Mining Software Repositories, ser. MSR ’24. New York, NY, USA:
     M. A. Babar, “Revisiting the practices and pains of microservice                 Association for Computing Machinery, 2024, p. 504–509. [Online].
     architecture in reality: An industrial inquiry,” Journal of Systems              Available: https://doi.org/10.1145/3643991.3644890
     and Software, vol. 195, p. 111521, 2023. [Online]. Available:
     https://doi.org/10.1016/j.jss.2022.111521
 [6] S. Smith, E. Robinson, T. Frederiksen, T. Stevens, T. Cerny,
     M. Bures, and D. Taibi, “Benchmarks for end-to-end microservices
     testing,” in 2023 IEEE International Conference on Service-Oriented
     System Engineering (SOSE), 2023, pp. 60–66. [Online]. Available:
     https://doi.org/10.1109/SOSE58276.2023.00013
 [7] T. Cerny, G. Goulis, and A. S. Abdelfattah, “Towards Change
     Impact Analysis in Microservices-based System Evolution,” in 2025
     IEEE International Conference on Software Analysis, Evolution
     and Reengineering (SANER). Los Alamitos, CA, USA: IEEE
     Computer Society, Mar. 2025, pp. 159–169. [Online]. Available:
     https://doi.org/10.1109/SANER64311.2025.00023
 [8] A. I. Daraojimba, D. Kisina, O. S. Adanigbo, B. C. Ubanadu,
     N. A. Ochuba, and T. P. Gbenle, “Systematic review of key
     performance metrics in modern devops and software reliability
     engineering,” International Journal of Future Engineering Innovations,
     vol. 1, no. 1, pp. 101–107, 2024. [Online]. Available: https:
     //doi.org/10.54660/IJFEI.2024.1.1.101-107
 [9] A. Al Maruf, A. Bakhtin, T. Cerny, and D. Taibi, “Using
     microservice telemetry data for system dynamic analysis,” in
     2022 IEEE International Conference on Service-Oriented System
     Engineering (SOSE), 2022, pp. 29–38. [Online]. Available: https:
     //doi.org/10.1109/SOSE55356.2022.00010
[10] J. P. Sotomayor, S. C. Allala, P. Alt, J. Phillips, T. M. King, and
     P. J. Clarke, “Comparison of runtime testing tools for microservices,”
     in 2019 IEEE 43rd Annual Computer Software and Applications
     Conference (COMPSAC), vol. 2, 2019, pp. 356–361. [Online].
     Available: https://doi.org/10.1109/COMPSAC.2019.10232
[11] T. Cerny, A. S. Abdelfattah, A. A. Maruf, A. Janes, and D. Taibi,
     “Catalog and detection techniques of microservice anti-patterns and
     bad smells: A tertiary study,” Journal of Systems and Software, vol.
     206, p. 111829, 2023. [Online]. Available: https://doi.org/10.1016/j.jss.
     2023.111829
[12] A. Abdelfattah, M. Schiewe, J. Curtis, T. Cerny, and E. Song,
     “Towards security-aware microservices: On extracting endpoint data
     access operations to determine access rights,” in Proceedings
     of the 13th International Conference on Cloud Computing and
     Services Science - CLOSER, 2023, pp. 15–23. [Online]. Available:
     https://doi.org/10.5220/0011707500003488
