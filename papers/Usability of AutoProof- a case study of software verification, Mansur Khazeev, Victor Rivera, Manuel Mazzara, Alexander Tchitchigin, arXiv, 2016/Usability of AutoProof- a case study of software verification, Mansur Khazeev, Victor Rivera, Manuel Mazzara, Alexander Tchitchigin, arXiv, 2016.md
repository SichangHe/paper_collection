                                                                   Usability of AutoProof:
                                                             a case study of software verification
                                                            Mansur Khazeev∗ , Victor Rivera† , Manuel Mazzara‡ and Alexander Tchitchigin§
                                                                              Innopolis University, Software Engineering Lab.
                                                                                              Innopolis, Russia
                                                Email: ∗ m.khazeev@innopolis.ru, † v.rivera@innopolis.ru, ‡ m.mazzara@innopolis.ru, § a.chichigin@innopolis.ru


                                           Abstract—Many verification tools come out of academic               equip classes with contracts and annotations to help the tool
                                        projects, whose natural constraints do not typically lead to a
arXiv:1605.01663v1 [cs.SE] 5 May 2016




                                                                                                               to prove certain properties.
                                        strong focus on usability. For widespread use, however, usability is
                                        essential. Using a well-known benchmark, the Tokeneer problem,           The main goal resented in this paper is to provide insights on
                                        we evaluate the usability of a recent and promising verification       how easy/difficult is for users (mainly engineers without deep
                                        tool: AutoProof. The results show the efficacy of the tool in          knowledge of formal verification) to use current methodologies
                                        verifying a real piece of software and automatically discharging
                                        nearly two thirds of verification conditions. At the same time,        and tools for the development of software with high level of
                                        the case study shows the demand for improved documentation             assurance, in particular on the use of the AutoProof tool.
                                        and emphasizes the need for improvement in the tool itself and
                                        in the Eiffel IDE.                                                        Generally, to prove the correctness of a program one needs
                                                                                                               some mechanisms to express what the program is supposed to
                                                               I. I NTRODUCTION                                do and clearly state it in the specifications that are used later
                                                                                                               to verify the program. Eiffel programming language natively
                                           Modern systems have grown fast in complexity, and demand            supports these mechanisms by means of contracts. Eiffel
                                        for quality. Focus on quality, in turn, demands stronger atten-        is an object-oriented programming language which directly
                                        tion to the entire development life-cycle. With the tendency           implements the concepts of Design-by-Contract (DbC) [1], [6].
                                        to reuse and integration, the need for software quality is even        The key concept is viewing the relationship between a class
                                        more important since applications and components have to rely          and its clients as a formal agreement, expressing each party’s
                                        on each other with partial knowledge of the implementation             rights and obligations. This is realized equipping methods with
                                        and based on interface only.                                           pre- and post-conditions, and classes with invariants. The key
                                           Tools for software verification allow the application of the-       feature of the Eiffel language is indeed the idea that all the
                                        oretical principles in practice, in order to ensure that nothing       methods might and should contain contracts.
                                        bad will ever happen (safety). The extra effort required by the
                                        use of these tools is certainly not for free and comes with               Contracts and annotations used in Eiffel are used by Au-
                                        increased development costs [1]. There is a common belief in           toProof to statically verify the consistency of the classes. To
                                        industry that developing software with high level of assurance         demonstrate the usability of the tool, the Tokeneer project [7]
                                        is too expensive, therefore not acceptable, especially for non         was implemented in Eiffel and AutoProof was used to verify
                                        safety-critical or financially-critical applications.                  the consistency of the code. The Tokeneer project is a sys-
                                                                                                               tem specified and implemented by National Security Agency
                                           Tools and techniques for the formal development of soft-
                                                                                                               (NSA). Initially, NSA carried out this challenge to prove that
                                        ware have played a key role on demystifying this belief. There
                                                                                                               it is possible to develop secure systems rigorously in a cost
                                        are several approaches, for instances abstract interpretation
                                                                                                               effective manner. Since its development, it became a testing
                                        and model checking [2], [3], that seek the automation to
                                                                                                               range for different software development methodologies and
                                        formally proving certain conditions of systems. However,
                                                                                                               verification tools. Results of the project are publicly available.
                                        these techniques tend to verify simple properties only. On the
                                                                                                               This paper reports on the use of AutoProof to verify an
                                        other end of the spectrum, there are interactive techniques for
                                                                                                               Eiffel implementation of Tokeneer and also reports on how
                                        verification such theorem provers [4]. These techniques aim at
                                                                                                               easy/difficult is for users to use the tool, e.g. the burden of
                                        more complex properties, but demand the interaction of users
                                                                                                               helping the tool by means of annotations in the code.
                                        to help the verification.
                                           Nowadays, there are new approaches that aim at finding                 The rest of the paper is organized as follows: Section II
                                        a good trade-off between both techniques, e.g. auto-active:            introduces the Tokeneer project, Eiffel and the AutoProof
                                        users are not needed during the verification process (it is            tool. Section III describes the methodology used to verify the
                                        automatically performed); they are required instead to provide         implementation of the Tokeener project. Section IV presents
                                        guidance to the proof using annotations. AutoProof [5], is a           empirical results helping to draw conclusions. Section V
                                        static auto-active verifier for functional properties of object-       is devoted to related work and Section VI concludes and
                                        oriented programs. Using AutoProof, users write code and               mentions future work.
                                                                        In order to ensure the entrance of users to the enclave, TIS
                                                                     implements a series of protocols and checks (the use of smart
                                                                     cards and biometrics) to grant or deny the entrance to it. This
                                                                     paper discusses one of these protocols: the Enrollment to the
                                                                     ID Station. The protocol starts in a state where the user is
                                                                     not enrolled. Users can request enrollment and then insert a
                                                                     FLOPPY (it retains an internal view of the last data written)
                                                                     for the system to proceed. The system reads the information
                                                                     in the floppy and either fails the enrollment process, in which
                                                                     case takes the process to the initial state, or correctly validates
                                                                     the data in the floppy.

                                                                     B. Eiffel
                                                                        Eiffel is a real complex object oriented programming lan-
                                                                     guage that natively supports Design-by-Contract methodology.
                                                                     Users can specify the behavior of Eiffel classes by equipping
                                                                     them with contracts: pre- and post-conditions and class invari-
                       Fig. 1.   The Tokeneer System                 ants, that are represented as assertions.

                                                                            class
                         II. P RELIMINARIES                                  ACCOUNT
                                                                            create make
A. The Tokeneer Project
                                                                            feature −− Initialization
   In 2002, with the aim to prove/disprove the common believe                make −−Initialize empty account.
in industry that development of software of high level of                     do
assurance is too expensive and therefore not feasible, the                     balance := 0
National Security Agency (NSA) asked Altran to undertake a                    ensure
                                                                               balance set: balance = 0
research project to develop part of an existing secure system,                end
the Tokeneer System, in accordance with Altran’s Correctness
by Construction development process. The system was spec-                   feature −− Access
ified using Z notation [8] and implemented in Ada [9]. The                   balance : INTEGER −− Balance of account.
project was successfully delivered in 2003 within 260 days of
                                                                            feature −− Element change
effort, and later, in 2008, all the results were made available by           deposit (amount : INTEGER)
NSA to the software development and security communities in                    −− Deposit ‘amount’ on account.
order to demonstrate the possibility to develop secure systems                require
in a cost effective manner. It includes the “Core” Tokeneer                    amount not negative : amount >= 0
ID System Software, test cases derived from the system test                   do
                                                                               balance := balance + amount
specification, “Support” Tokeneer ID System Software and                      ensure
test tokens and biometric data, project documents. Since the                   balance increased : balance =
delivery, the Tokeneer project has become a milestone point                           old balance + amount
and a testing range for different verification tools before                   end
applying them in industrial projects. Despite the fact that after
                                                                             withdraw (amount : INTEGER)
delivery 4 bugs1 were found, the system is still deemed to be                 −− Withdraw ‘amount’ from account.
very secure.                                                                 require
   Tokeneer is a secure enclave consisting of a set of system                 enough balance : amount <= balance
components, some housed inside the enclave and some outside,                 do
as depicted in Figure 1. The ID Station (TIS) is part of the                  balance := balance - amount
                                                                             ensure
larger Tokeneer system. It has four connected peripherals,                    balance decreased : balance = old balance - amount
namely, a fingerprint reader, a smartcard reader (users use To-              end
kens -smartcards- as identification), a door and visual display.
The objective of the enclave is to ensure that anyone who                   invariant
enters the enclave has a proper access, and no one else can                  non negative balance : balance >= 0
                                                                            end
access to the enclave.

  1 According to [7]                                                                    Fig. 2.   ACCOUNT Eiffel class
   Figure 2 depicts a reduced implementation of a Bank                     class
Account. In Eiffel, creation procedures are listed under the                 ID STATION
keyword create, for class ACCOUNT, routine make is used                        . . . Some lines were omitted. . .
as a creation procedure. The class defines a class attribute               create
                                                                             make
balance to represent the current balance of the account. It also           feature −−Initialization
defines two routines (methods), deposit and withdraw. de-                    make
posit implements a deposit of amount amount of money to the                    note
account and withdraw implements withdrawing money. Eiffel                         status : creator
encourages software developers to express formal properties of                 do
                                                                                  . . . Some lines were omitted. . .
classes by writing assertions. Routine pre-conditions express                  end
the requirements that clients must satisfy whenever they call a            end
routine. They are introduced in Eiffel by the keyword require.
Routine deposit imposes a pre-condition on the call, the
                                                                              Fig. 3.   Initialisation of ID STATION Eiffel class.
client must pass as an argument a non-negative number (i.e.
amount not negative: amount >= 0) for the routine to
work correctly: a negative value might invalidate the invariant
                                                                    the Eiffel language constructs: in-lined assertions such as
of the class. Routine post-conditions, introduced in Eiffel
                                                                    check (assert in other programming languages), types, multi-
by the keyword ensure, express conditions that the routine
                                                                    inheritance, polymorphism.
(the supplier) guarantees on method exit, assuming the pre-
condition. Routine deposit guarantees that the balance of the         III. V ERIFICATION OF T OKENEER USING AUTO P ROOF
account will be the previous value of the balance (expressed
in Eiffel by the keyword old: the value on entrance of the             The Tokeneer project was implemented in Eiffel following
routine) plus the amount being deposited. Routine withdraw          the specifications file 41 2.pdf (see [7]) of the Tokeneer
imposes the constraint to the caller that the argument must be      System and equipping classes with contracts. This research
less than or equal to the current balance of the account to avoid   work encompasses only the enrolment process of the whole
having negative value in the balance. The routine ensures that,     Tokeneer System therefore it implements only the entities
after execution, the new value of balance will be the value         involved in this process.
on routine entry minus the amount withdrawn.                           One of the main parts of TIS is the ID STATION (see
   A class invariant must be satisfied by every instance of         Figure 8) - it describes how all components of the system are
the class whenever the instance is externally accessible: after     related to each other: one of the components is implemented in
creation, and after any call to an exported routine of the          class INTERNAL S (not shown here) whose responsibility is
class (public routines). The invariant appears in a clause          to keep knowledge of the status of user entry and the enclave
introduced by the keyword invariant. Class ACCOUNT’s                and to hold a timeout when relevant; another component is
invariant imposes the restriction that class attribute balance      implemented on class FLOPPY (not shown here) that retains
can never be negative (i.e. non negative balance: balance           an internal view of the last data written to the floppy as
>= 0).                                                              well as the current data on the floppy. ID STATION displays
                                                                    the configuration data on the screen which is implemented
C. AutoProof                                                        in SCREEN DISPLAY. There are a number of messages
   AutoProof [5] is a static verifier of contracts for Eiffel       that may appear on the TIS screen. The Real World types
programs. It follows the auto-active paradigm where verifica-       (described in [7] Specification document, section 2.7.1) of
tion is done completely automated, similar to model checking        the system such as messages that appear on the display and
[3], but users are expected to feed the classes providing           screen, were implemented all together in class CONST which
additional information in the form of annotations to help the       implements the constants used in the TIS. And finally, a
proof. AutoProof identifies software issues without the need        number of interactions between all these entities within the
of executing the code, therefore opening a new frontier for         enclave are implemented in ENCLAVE OPERS.
“static debugging”, software verification and reliability, and in      AutoProof does not make any assumptions out of box there-
general for software quality.                                       fore users are expected to feed the Eiffel classes for a succeed
   AutoProof verifies the functional correctness of Eiffel          verification. This is expressed by means of Eiffel’s note clause.
classes. It translates Eiffel code to Boogie programs [10] and      note clause enables users to attach addition information to the
calls the Boogie tool to generate verification conditions: logic    class that is ignored by the Eiffel’s compiler. AutoProof uses
formulas whose validity entails correctness of the input pro-       this information to succeed in the verification. For instance,
grams. Finally, retrieves the answer back to Eiffel. AutoProof      Autoproof’s annotation status defines which procedure is used
verifies that routines satisfy pre- and post-conditions, mainte-    to initialize newly created objects: Figure 3 depicts procedure
nance of class invariants, loops and recursive calls termination,   make with annotation note (e.g. note status: creator) to help
integer overflow and non Void (null in other programming            Autoproof to discharge the corresponding proof obligations
languages) references calls. The tool also supports most of         related to creation procedures: the procedure will be called
       RequestEnrolment                                                     invariant
       EnrolContext                                                             constants.display message.has(current display)
                                                                                constants /= Void
       ΞKeyStore
       ΞAuditLog                                                                Fig. 6.     Invariants of ID STATION Eiffel class.
       ΞInternal
       enclaveStatus = notEnrolled                                          feature −−Element Change
       floppyPresence = absent                                                set current display(v: STRING)
                                                                                require
       currentScreen0 .screenMsg = insertEnrolmentData                           constants.display message.has(v)
                                                                                 modify model(”current display”, Current)
       currentDisplay0 = blank                                                  do
                                                                                 current display := v
                                                                                ensure
               Fig. 4.    Z schema of RequestEnrolment                           current display = v
                                                                                end

       make
         . . . Some lines were omitted. . .                                       Fig. 7.    Feature equipped with modify clause
        ensure
         enclave status = cons floppy.not enrolled
         floppy presence = cons internal.absent                         Figure 6 depicts the class invariant for class ID STATION.
         token removal timeout = 0
        end                                                          It states that a message displayed on the display outside the en-
                                                                     clave is one of the available from the list of messages (i.e. con-
                                                                     stants.display message.has(current display)) and that
                Fig. 5.   ensure clause in feature make              class attribute constants is attached to an object (i.e. con-
                                                                     stants /= Void).
                                                                        Figure 7 shows the implementation of procedure
only when an object of this class is being created, AutoProof        set current display. Its first pre-condition was added
needs to verify a creation routine only once.                        to satisfy the invariant ensuring that argument v belongs to
   note clause is also used to define models queries to express      the allowed displayed messages. The second pre-condition
the abstract state space of a classes. Model queries are part of     restricts the procedure to change values only to model query
model-based contracts to help users to write abstract and con-       current display.
cise specifications [11], they are used to specify the behavior         Figure 8 shows the final version of class ID STATION:
of the class. In Eiffel, this is specified by adding a note clause   with the respective annotations for Autoproof to successfully
at the beginning of the class followed with a keyword model:         verify the class. In class ID STATION, class attributes cur-
and listing one or more attributes of the class. Model queries       rent screen and current display implements the physical
are also used to describe frame conditions: which allocations        screen and display, respectively, of the enclave.
are allowed to be modified by procedures. In Eiffel, frame
conditions are listed using the modify clause, which lists the                              IV. E MPIRICAL R ESULTS
model queries that the feature is allowed to modify, as shown           The usability of a verification tool cannot be considered
in Figure 7 (i.e. modify model(”current display”, Current)).         in isolation and, in particular, cannot be hived off by the
   According to RequestEnrolment (a Z-schema that is a               effectiveness of the tool itself. First, as a general observation,
part of the formal specification of the project Tokeneer),           the cost of using an instrument can only be justified by its re-
which is presented in Figure 4, requesting enrolment involves        turn, which can ultimately be linked to financial consideration
EnrolContext, KeyStore, AuditLog, Internal. Schemas in Z             by top management. Second, and this aspect is less general
consist of an upper part, in which some variables are declared,      and more peculiar to the auto-active verification approach,
and a lower part, which describes the relationship between           a tool like AutoProof is as much effective and usable as
values and variables. The notation Ξ indicates an operation in       is its ability to discharge verification conditions completely
which the state does not change, and the apostrophe indicates        automatically, without feeding the code of annotation overhead
the state of the variable after the change [12]. RequestEn-          or requiring particular tweaking. Finally, the necessity for
rolment specifies that the ID station will request enrolment         users to add further annotations and dedicate extra effort
by displaying a request string on the screen and keeping             (and considerable time) is, by itself, an obstacle to adoption
the display blank. This is only possible while there is no           and (technically) an usability issue. Verification tools should
Floppy present. Therefore, initially floppyPresence = absent         require minimal annotational effort and give valuable feedback
and enclaveStatus set to notEnrolled. An ensure clause was           when verification fails.
used in the creation procedure to guarantee this after the              The case study analyzed in this paper presented good results
initialization of ID STATION object:                                 in term of automatic discharge of verification conditions,
       class                                                                           V. R ELATED W ORK
         ID STATION
           . . . Some lines were omitted. . .                        Formal/mathematical notations have existed for a long time
                                                                  and have been used to specify and verify systems. Examples
       create                                                     are process algebras [15], specification languages like Z [16],
         make                                                     B [17] and Event-B [18]. The Vienna Development Method
                                                                  (VDM) is one of the earliest attempts to establish a formal
       feature −−Initialization
         make                                                     method for the development of computer systems [19]. A
           note                                                   survey of these (and others) formalisms can be found in [20]
            status: creator                                       while a discussion on the methodological issues of a number
           do                                                     of formal methods is presented in [21].
            create constants
                                                                     All these approaches (and others described in the literature)
            current display := constants.blank
            create current screen.make                            still leave an open issue, i.e., they are built around strict
                                                                  formal notations which affect the development process from
            create cons floppy                                    the very beginning. These approaches demonstrate a low
            enclave status := cons floppy.not enrolled            level of flexibility. To overcome this problem, a seamless
            token removal timeout := 0
                                                                  methodological connection built on top of a portfolio of
            create cons internal                                  diverse notations and methods is presented in [22]. Another
            floppy presence := cons internal.absent               approach is presented in [14], [23] using [24], where users
           ensure                                                 start the development of system from a strict formal notation
            enclave status = cons floppy.not enrolled             (i.e. Event-B), to then automatically translate it to Java code
            floppy presence = cons internal.absent
                                                                  with JML [25] specifications embedded (following Design-by-
            token removal timeout = 0
           end                                                    Contract methodology). Even though this approach enables
                                                                  users with less mathematical expertise to work on formal
       feature −−Element Change                                   development, it does not give a seamlessly methodology for
         set current display(v: STRING)                           the development as presented in this paper.
           require
            constants.display message.has(v)
                                                                     On the other side, Design-by-contract [6] when combined
            modify model(”current display”, Current)              with AutoProof technology offers the pros of both rigorous
           do                                                     methodologies and supporting tools able to semi-automate the
            current display := v                                  process. Before this to be available for the average developer
           ensure                                                 it is however necessary to improve the users’ experience.
            current display = v
           end
                                                                  A comparison between different approaches (for example
                                                                  Event-b/Rodin and Design-by-contract/AutoProof) is beyond
       feature −−Access                                           the scope of this paper and it is left as future work.
         constants : CONST
         current screen : SCREEN DISPLAY                                                VI. C ONCLUSION
         current display : STRING
       invariant                                                     AutoProof allows for “static debugging”, i.e. debugging be-
         constants.display message.has(current display)           comes possible without the need of executing the program. The
         constants /= Void                                        most effective way to release correct software is a combination
       end
                                                                  of static debugging and traditional run-time debugging. Being
                                                                  all human activities (therefore including programming and
             Fig. 8.   Verified ID STATION Eiffel class.          testing itself) error-prone, there is no magic or free lunches
                                                                  out there. Abandoning testing and adopting a proof-oriented
                                                                  approach does not make miracles, debugging remains a trial-
                                                                  and-error long and laborious process. AutoProof does not
though not comparable to others seen in literature [13]. In       change the rules of the game: developers will have to try,
total there were 38 generated proof. Of these, 22 (58%) were      observe the results and make changes as a consequence. A
discharged automatically, 8 (21%) could not be satisfied, and     proof-oriented approach does not make the process smoother
the rest (21%) failed due to internal errors, which in our case   and necessarily simpler. However, it makes it more accurate
were basically caused by the attempt to create objects in the     and robust, therefore effective. Adjustment can be now focused
contract, and that is not allowed by the tool. As observed        on the the implementation side (possibly sinergically with run-
before, the success of verification is unsurprisingly linked to   time debugging), on the specification side (the contracts used
the complexity of programs [13]. Previous literature mostly       to annotate the code as integral part of the code itself), or in
dealt with students users and university projects. The use of     the proof itself (fine-tuning may be necessary for AutoProof
Tokeener as a benchmark demands for detailed comparisons          and its behind-the-curtains machinery to be able to prove
with different verification efforts (for example, [14]).          correctly).
   All this comes with a cost: the willingness and ability of                 [11] N. Polikarpova, C. A. Furia, and B. Meyer, “Specifying reusable
the user to use extra tools and being able to master them, and                     components,” in Proceedings of the 3rd International Conference on
                                                                                   Verified Software: Theories, Tools, and Experiments (VSTTE’10) (G. T.
possibly invest extra time in the process. On the other side, it                   Leavens, P. O’Hearn, and S. Rajamani, eds.), vol. 6217 of Lecture Notes
is necessary for the tools to be simple to master and to provide                   in Computer Science, pp. 127–141, Springer, August 2010.
intelligible feedback.                                                        [12] J. Spivey, “An introduction to Z and formal specifications,” Software
                                                                                   Engineering Journal, 1989.
   The Tokeener project case study showed the efficacy of                     [13] C. A. Furia, C. M. Poskitt, and J. Tschannen, “The autoproof verifier:
AutoProof in verifying a real piece of software, the complexity                    Usability by non-experts and on standard code,” in Proc. Formal
of which can be compared not only with most of the commer-                         Integrated Development Environment (F-IDE 2015), vol. 187, pp. 42–
                                                                                   55, Electronic Proceedings in Theoretical Computer Science (EPTCS),
cial Off-the-Shelf software, but also with safety and financial-                   2015.
critical applications, both in terms of computational logic                   [14] V. Rivera, S. Bhattacharya, and N. Cataño, “Undertaking the tokeneer
and architectural organization. AutoProof is capable to verify                     challenge in Event-B,” To appear in 4th FME Workshop on Formal
                                                                                   Methods in Software Engineering (FormaliSE), 2016.
industrial software and may well be adopted in commercial                     [15] J. C. M. Baeten, “A brief history of process algebra,” Theor. Comput.
companies and its use injected into the development process.                       Sci., vol. 335, no. 2-3, pp. 131–146, 2005.
However, some obstacles have been identified that could                       [16] J. Abrial, S. A. Schuman, and B. Meyer, “Specification language,” in
                                                                                   On the Construction of Programs, pp. 343–410, 1980.
prevent its broader adoption.                                                 [17] J. Abrial, The B-book - assigning programs to meanings. Cambridge
   As result of an academic effort, documentation is not at par                    University Press, 2005.
with commercial software, in particular for what concerns the                 [18] J.-R. Abrial, Modeling in Event-B: System and Software Engineering.
                                                                                   New York, NY, USA: Cambridge University Press, 1st ed., 2010.
size of the library of correctly verified examples: tutorials on              [19] C. B. Jones, Software Development: A Rigorous Approach. Englewood
the official website are quite useful, but not enough. On top of                   Cliffs, N.J., USA: Prentice Hall International, 1980.
this, the tool itself has limitations. First, existing implementa-            [20] M. Mazzara and A. Bhattacharyya, “On modelling and analysis of dy-
                                                                                   namic reconfiguration of dependable real-time systems,” in Proceedings
tions need to be modified in order to be verified. This would                      of the 2010 Third International Conference on Dependability, DEPEND
represent an unsurmountable obstacle in most institutions since                    ’10, (Washington, DC, USA), pp. 173–181, IEEE Computer Society,
the overall cost of code adaptation may overrun the saves                          2010.
                                                                              [21] M. Mazzara, “Deriving specifications of dependable systems: toward a
occurring to the testing phase. This consideration may be                          method,” in Proceedings of the 12th European Workshop on Dependable
different, however, for safety-critical systems. Second, the                       Computing, EWDC, 2009.
Eiffel IDE - necessary for functioning - calls for increased                  [22] R. Gmehlich, K. Grau, A. Iliasov, M. Jackson, F. Loesch, and M. Maz-
                                                                                   zara, “Towards a formalism-based toolkit for automotive applications,”
stability and robustness.                                                          1st FME Workshop on Formal Methods in Software Engineering (For-
                                                                                   maliSE), 2013.
                       ACKNOWLEDGMENTS                                        [23] V. Rivera, N. Cataño, T. Wahls, and C. Rueda, “Code generation for
                                                                                   Event-B.” To appear in International Journal on STTT, 2016.
   We would like to thank Innopolis University for logistic and               [24] V. Rivera and N. Cataño, “Translating Event-B to JML-Specified Java
financial support, and the laboratories of Software Engineering                    programs,” in 29th ACM SAC, (Gyeongju, South Korea), March 24-28
                                                                                   2014.
(SE) and Service Science and Engineering (SSE) for the                        [25] G. T. Leavens, A. L. Baker, and C. Ruby, “Preliminary design of jml:
intellectual engagement and vivid discussions.                                     A behavioral interface specification language for java,” SIGSOFT Softw.
                                                                                   Eng. Notes, vol. 31, pp. 1–38, May 2006.
                             R EFERENCES
 [1] B. Meyer, Touch of Class: Learning to Program Well with Objects and
     Contracts. Springer Publishing Company, Incorporated, 1 ed., 2009.
 [2] P. Cousot and R. Cousot, “Abstract interpretation: A unified lattice model
     for static analysis of programs by construction or approximation of fix-
     points,” in Proceedings of the 4th ACM SIGACT-SIGPLAN Symposium
     on Principles of Programming Languages, POPL ’77, (New York, NY,
     USA), pp. 238–252, ACM, 1977.
 [3] E. M. Clarke, Jr., O. Grumberg, and D. A. Peled, Model Checking.
     Cambridge, MA, USA: MIT Press, 1999.
 [4] D. W. Loveland, Automated Theorem Proving: A Logical Basis (Fun-
     damental Studies in Computer Science). sole distributor for the U.S.A.
     and Canada, Elsevier North-Holland, 1978.
 [5] J. Tschannen, C. A. Furia, M. Nordio, and N. Polikarpova, “Autoproof:
     Auto-active functional verification of object-oriented programs,” in 21st
     International Conference, TACAS 2015, London, UK, April 11-18, 2015.
     Proceedings, pp. 566–580, 2015.
 [6] B. Meyer, Object-oriented software construction, ch. 11: Design by
     Contract: building reliable software. Prentice Hall PTR, 1997.
 [7] AdaCore, “Tokeneer.” http://www.adacore.com/sparkpro/tokeneer/download,
     accessed in April 2016.
 [8] J.-R. Abrial, S. Schuman, and B. Meyer, “Specification Language,” in On
     the Construction of Programs, R. M. McKeag and A. M. Macnaghten,
     editors, pp. 343–410, Cambridge University Press, 1980.
 [9] J. Barnes, High Integrity Software: The SPARK Approach to Safety and
     Security. Boston, MA, USA: Addison-Wesley Longman Publishing Co.,
     Inc., 2003.
[10] K. R. M. Leino, “This is boogie 2,” tech. rep., June 2008.
