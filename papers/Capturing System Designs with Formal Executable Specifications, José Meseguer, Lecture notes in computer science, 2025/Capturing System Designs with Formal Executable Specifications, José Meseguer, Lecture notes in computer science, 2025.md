                Capturing System Designs with
               Formal Executable Specifications

                                    José Meseguer(B)

         University of Illinois at Urbana-Champaign, Urbana, IL 61801, USA
                                 meseguer@illinois.edu



       Abstract. Basing system designs on informal specifications and apply-
       ing formal methods after system implementation greatly reduces the ben-
       efits that formal methods can provide. Systems of high quality and trust-
       worthiness can be developed in a faster and much more efficient way by
       capturing system designs with formal executable specifications and sub-
       jecting them to automated formal verification from the earliest stages of
       system design. Even greater benefits can be gained by making such for-
       mal designs highly composable and reusable by means of formal patterns.
       The experience on using the rewriting-logic-based language Maude and
       its tool environment and formal patterns for all these purposes is pre-
       sented and illustrated with concrete examples. The benefits of combining
       model-based design approaches with the one based on formal executable
       specifications is also discussed an illustrated with examples.

       Keywords: System Design · Executable Specifications · Formal Pat-
       terns · Qualitative and Quantitative Properties · Rewriting Logic · Maude


1    Introduction
Many important theoretical and practical advances have taken place in the area
of Formal Methods (FMs), and impressive applications have been developed.
Furthermore, FMs and their associated tools are now routinely used in many
industries. However, their full potential remains partly unexploited. In pg. 57 of
a recent FMs survey [47], I gave my own view about their future in a position
statement where, among other things, I said (emphasis added):
    Rather than focusing mostly on [code] verification, [formal methods]
    should support system design, validation, evolution and maintenance
    from the earliest stages. For this, use of executable formal specifications
    for fast system modeling and analysis before implementation is crucial.
The problem at present is that many complex systems are still designed in an
informal manner. This happens not just for the proprietary designs of many
companies, but even when international bodies responsible for agreeing on and
carefully documenting the standards of a widely used system —e.g., a new com-
munication protocol, or a programming language— capture its design mostly
informally. Let me give three examples that I know well:

© The Author(s) 2025
A. Boronat and G. Fraser (Eds.): FASE 2025, LNCS 15693, pp.1–32, 2025.
https://doi.org/10.1007/978-3-031-90900-9_1
2         J. Meseguer

1. Until 2007, when S. Chen, J. Meseguer, R. Sasse, H. J. Wang and Y.M. Wang
   used a formal executable semantics of Internet Explorer (IE) in Maude to
   uncover 13 new types of visual spoofing attacks on IE [27], hundreds of
   thousands of dollars were yearly lost due to such kinds of attacks, and no
   meaningful way existed to predict and prevent new attacks.
2. Until 2012, when C. Ellison and G. Rosu gave the first full formal executable
   semantics of C (in K, automatically translated to Maude by the K-Maude
   tool [105,104]) [43], no complete formal specification of C existed. This K
   semantics uncovered semantic flaws in several C theorem provers.
3. Until 2023, when S. Liu, H. Duan, L. Heimes, M. Bearzi, J. Vieli, D. Basin
   and A. Perrig gave the first formal executable semantics (in Maude) of the
   end-to-end name resolution behavior of DNS [61], many attacks were regu-
   larly perpetrated on DNS, and several more, which were uncovered in [61],
   were confirmed on popular DNS implementations.

As the above examples illustrate, the most disastrous consequence of informal
specifications is their utter lack of predictive power. In fact:

    – It is virtually impossible to predict the problematic behaviors of a complex
      system based on its informal specifications before it is built.
    – Even after a complex system has been implemented, lack of a formal ex-
      ecutable specification makes it very difficult to systematically uncover its
      often subtle flaws and vulnerabilities.

The second point is illustrated by the systems (1)–(3) described above, which all
had heavily tested, mature implementations.1 But the first point is much more
important than the second, for the simple reason that design errors are typically
several orders of magnitude more expensive than coding errors.
    Let me further comment on these two points: formal executable specifications
can be used in two different ways: (i) in a post facto analysis of an already
implemented system, or (ii) one can use formal executable specifications ab
origine, that is, from the earliest stages of a system’s design. As the above
examples (1)–(3) illustrate, formal executable specifications can be extremely
valuable in a post facto specification and analysis of a system. However, post
facto specification and analysis is neither the most cost effective nor the most
fruitful application of FMs for three reasons:

1. Inferring a formal executable specification from a large, already implemented
   system is very labor-intensive. I have detailed knowledge about this problem
   in both the case of IE (Example 1) and in the case of the Maude specification
   of the Cassandra key-value store used in [67].
2. Due to large system size and complexity (easily hundreds of thousands or
   even millions of lines of code) a formal specification inferred from a system
   implementation usually provides only partial knowledge about the system.
1
    In the case of C, the executable specification of Ellison and Rosu was able to pass
    more tests than those passed by the GNU compiler using the GNU torture suite.
                                            Formally-Driven System Design          3

   For example, besides the 13 new types of visual spoofing attacks uncovered by
   the Maude specification of IE, one more attack type was later found because
   some additional IE functionality had not been modeled in the original Maude
   specification of IE.
3. While the uncovering of a system’s design flaws by means of a post facto
   analysis based on a formal executable specification inferred from its imple-
   mentation can be extremely valuable, the cost of fixing those design flaws
   after the system has been implemented can be quite high: this is an engi-
   neering fact of life about late discovery of design errors.

In response to the reasons I have just given, somebody could object as follows:
    We already knew all that back in the times of stepwise refinement in
    structured programming. And we have since then learned considerably
    more about program extraction from propositions in intuitionistic type
    theory. Isn’t all you have said just old hat?
I would answer that objection by making a crucial distinction between:
 – Formal System Specifications, in which a computational mathematical
   model of a system is captured by a formal executable specification in a com-
   putational logic, and
 – Formal Property Specifications, in which formal requirements about the
   desirable correctness and quantitative properties that a system should satisfy
   are captured in various, usually non-executable, logics.
Both kinds of specifications are essential: they complement each other, and both
should be used ab origine, since the earliest stages of system design. The problem
with the above objection is that it confuses the early uses of property specifica-
tions —i.e., of formal system requirements expressed, for example, as Hoare logic
triples, or as intuitionistic logic propositions— with something completely dif-
ferent, namely, that we should also use formal executable specifications from the
very beginning and that this is crucial. But why? Let me give six reasons:

1. Formal specifications of large systems may contain bugs. This ap-
   plies to both formal requirements and to executable specifications. The big
   difference is that an executable specification is in fact a declarative program
   that can, not only be tested and debugged like any other program, but can
   also, as in the case of Maude (see §4), be model checked to uncover subtle
   design flaws in early designs. This kind of debugging is usually not possible
   for property specifications. Imagine, for example, an axiomatic semantics of
   C in Hoare logic. One cannot use the GNU torture suite —as Ellison and
   Rosu did for their K semantics of C— to debug a C axiomatic semantics.
2. KISS. Since a formal executable specification is a declarative program, the
   entry barrier for engineers to write such specifications is quite low: just learn-
   ing another programming language. This is typically not the case for formal
   property specifications, which may require expert acquaintance with com-
   plex logics. Let me give one example from my direct experience about the
4      J. Meseguer

   use of Maude. In the late 90’s and early 2000’s I was involved in the early
   applications of Maude to systems biology [42] that has subsequently been
   vigorously developed under the leadership of Carolyn Talcott and other re-
   searchers. The first Maude executable specification thus developed —a model
   of a mammalian cell and its molecular biology reactions (over 500 of them)—
   was not developed by a computer scientist, but by Merryl Knapp, a biologist
   with no previous acquaintance with Maude. Since Maude axioms are rewrite
   rules specifying local concurrent transitions in a system, rewrite rules had
   an obvious one-to-one correspondence with molecular biology reactions.
3. Small is beautiful. Formal executable specifications of a system are orders
   of magnitude smaller than system implementations in a conventional lan-
   guage (Examples (1)–(3) underscore this). And they are much more under-
   standable than a conventional implementation. For example, the executable
   formal semantics of C by Ellison and Rosu had about 1,000 rules in K, with
   each language feature captured by a few rules with an obvious meaning.
4. Executable specifications are much easier to verify than imperative
   code. To begin with, they are simpler and much smaller. A further key
   advantage is that the verification process never leaves mathematics. This is
   because, as explained in §2, an executable formal specification is a theory
   T in a computational logic, and its formal requirements are formulas φ in
   some, usually non-executable, property specification logic. By contrast, an
   imperative programming language is an engineering artifact that needs a
   precise mathematical semantics before any formal program verification worth
   its name can get off the ground. Even more importantly, verification of formal
   executable designs can uncover costly design errors much more easily and
   much earlier than verification of system implementations.
5. Easy, rapid exploration of alternative designs. In traditional system
   development it is very costly to explore alternative designs, for the obvious
   reason that informal specifications cannot predict system behavior on which
   design changes should be based. Since design changes after implementation
   can be prohibitively expensive, exploration of design alternatives often be-
   comes unfeasible. This is not at all the case when a system design is captured
   by a formal executable specification: alternative changes are easy to make. In
   Maude, it may just require changing a few rewrite rules; and quick feedback
   about the correctness and quantitative properties of alternative designs can
   easily be gained by automatic verification methods (see §4 and §5.2).
6. Gold standard for code generation. If an executable specification lan-
   guage has high performance, a system specification may be directly used as
   a system implementation. Alternatively, an executable formal design may be
   either transformed into a correct-by construction implementation as done,
   for example, in [68], or may be compiled into a lower level language for
   further efficiency, as done by K’s compilation into LLVM.

Having motivated the usefulness of capturing system designs with formal exe-
cutable specifications, I explain in §2 how a computational logic supports such
specifications. In §3 I then explain how formal patterns can increase the mod-
                                                 Formally-Driven System Design            5

ularity and reusability of formal system designs. Verification of qualitative and
quantitative properties of Maude designs is then discussed in §4. I summarize
my own experience about formal executable designs in §5. The relationship with
model-based design is discussed in §6. Conclusions are presented in §7.


2     Capturing System Designs in a Computational Logic

The ideas I am presenting are logic-independent : various logics can be chosen as
executable formal specification languages. But not all logics are suitable for this
purpose, simply because many, although they are mechanizable, i.e., a theorem
prover can mechanize their inference rules, are not executable in the obvious,
intuitive sense that the logic itself, or a suitable subset of its theories, can be
efficiently implemented as a declarative programming language. I call a logic
enjoying these properties a computational logic. For example, the λ-calculus, the
π-calculus, Horn logic, confluent theories in equational logic, and rewriting logic
are all computational logics in this sense. However, not all computational logics
can support system specification equally well. For example, the λ-calculus and
equational logic can both nicely express deterministic systems, but are not a
good fit for specifying non-deterministic ones, whereas the opposite is the case
for Horn logic. I present below some requirements on a computational logic L
that I have found particularly useful for system specification purposes.


2.1     Requirements on the Computational Logic L

In my own experience, for a computational logic L to be an expressive semantic
framework for executable formal system design it is highly desirable that L
supports features such as the following:


 1. implementable as a high-performance declarative programming language
 2. can naturally specify both deterministic systems and a wide range of con-
    current systems, including concurret object-oriented systems
 3. an executable system specification, i.e., a theory T in L, has an associated
    initial model 2 that defines a mathematical model of the system thus specified
 4. supports logical reflection
 5. supports the specification of real-time and probabilistic systems
 6. availability of advanced algorithmic and deductive formal verification meth-
    ods and tools in a variety of property-specification logics, including logics
    expressing quantitative properties.
2
    More generally, T can be a parameterized theory associating a free model to each
    model of its parameter theory P . In this way, T defines a parametric family of systems.
    This desirable property of L can be captured by the requirement that L is a liberal
    institution [48].
6       J. Meseguer



Let me unpack requirement (6). By requirement (3), a theory T in L specifying a
given system defines a mathematical model of such a system as an initial model
IT , which is precisely the link between the system specification T and its formal
requirements R. Formal requirements in R may be expressed in a variety of
(typically non-computational) property specification logics. That is, each formal
requirement φ ∈ R is a formula in one such logic. The link between T and R
is then simple: T meets a formal requirement φ ∈ R iff IT |=L′ φ, where L′ is
the property specification logic of formula φ, and |=L′ denotes the satisfaction
relation between models and formulas in L′ . For example, IT may provide the
mathematical model of a communication protocol, and φ may express a safety
or liveness property about such a protocol in some temporal logic. What (6)
expects is that advanced algorithmic and deductive formal methods and tools are
available to prove formal requirements about IT in various property specification
logics L′ , including logics expressing quantitative properties.

Maude’s [28] computational logic, namely, rewriting logic [73,24] and its real-
time and probabilistic extensions (see [91,63]) provides a semantic framework
for system specification meeting requirements (1)–(6). For how requirements
(1)–(5) are met by rewriting logic and Maude see [75,74,71,30,91,63]. I discuss
in detail how Maude meets requirement (6) in §4.

I explain in §3 below how a computational logic L meeting requirements (1)–(6)
can support modular and reusable development of system designs by means of
formal patterns.


3   Formal Patterns for Modular System Design
This section summarizes and borrows ideas from [76,78]. I refer to those two
publications for further details. Formal patterns are formally specified generic
solutions to commonly occurring computational problems. Being generic, a formal
pattern applies, not just to a single system, but to a typically infinite class of
systems that satisfy specified semantic requirements. Application of a formal
pattern to a system satisfying the formal pattern’s input requirements results
in a new system with new functionality that is correct by construction. Such
correctness takes the form of an assume-guarantee formal assurance: assuming
that the original system meets the formal pattern’s semantic requirements, then
the application of the formal pattern to such a system is guaranteed to enjoy
specific correctness properties.
   Formal patterns are very useful for formal system design because, as it will
become clear in what follows, they support a high degree of genericity, reusability
and modularity of system designs. In this way, a system design, instead of being
a one of a kind design that has to be developed and verified from scratch, can
reuse many existing generic system components, algorithms and program trans-
formations for free, as well as the correctness properties already verified for those
                                             Formally-Driven System Design       7

components, algorithms and program transformations. This can greatly reduce
design and verification efforts and can substantially increase system quality.


3.1    Formal Patterns in Declarative Programming Languages

Mathematically, a formal pattern is a theory transformation P that maps a
declarative program in a computational logic L, that is, a theory T in the class
C of L-theories satisfying the pattern’s input requirements, perhaps with some
additional parameters p, into a new theory P (T, p) specifying the new correct-
by-construction system generated by P , i.e., we can describe P as a (possibly
partial) function,

                    P : C × Params ∋ (T, p) 7→ P (T, p) ∈ Th L

where Th L denotes the category of finitary theories in the language’s computa-
tional logic L. I assume throughout that L enjoys the requirements presented
in §2.1. We can therefore view P as a meta-program, that is, as a program that
transforms a declarative program T into another declarative program P (T, p).
Thanks to requirement (4) in §2.1 (logical reflection), programs in L can be meta-
represented as data structures,3 so that the meta-program P is also a program
in the same computational logic L.
    Although in some applications (e.g., [2]) the purpose of a formal pattern P
may be one of optimization and/or specialization of a declarative program T ∈ C,
in L, in many other applications P (T, p) may instead be a substantial extension
of T with completely new features and capabilities; that is, P (T, p) is often a
more sophisticated system, enjoying new features and properties not available
in T . Nevertheless, the assume-guarantee properties of P often include the fact
that P will in some appropriate sense be semantics-preserving. But in general
this should not be understood in the sense that T and P (T, p) have the same
semantics. Instead, the semantics of P (T, p) will often extend that of T while
respecting T itself, which may remain intact as a subcomponent of P (T, p). This
is in fact the case for many formal patterns (see, e.g., [110,112,111,26,4,39,50]).
From the point of view of code reusability this means that the code of T is not
changed at all by P . That is, T is kept intact and encapsulated as a subcom-
ponent. This gives formal patterns powerful modularity, code understandability
and reusability, and verification scalability properties.
    In yet other kinds of examples of formal pattern (e.g., [81,10,68,63,66]), the
input theory T may not be kept as a subcomponent of P (T, p). Instead, the
assume-guarantee properties relating T and P (T, p) may include considerably
more general semantics-preserving properties such as the existence of a simula-
tion or bisimulation (including the case of a stuttering simulation or bisimula-
tion), between P (T, p) and T .
3
    In Maude this is supported by its META-LEVEL module.
8       J. Meseguer

3.2    Application Areas

Formal patterns specified as Maude meta-programs have been defined and proved
correct in various application areas, including:

 1. Cyber-physical systems
     – Formal Patterns for Safe Operation of Medical Devices [110,112,111]
     – Physically Asynchronous/Logically Sinchronous (PALS) pattern for real-
       time distributed systems [83,81], and Multi-Rate PALS [10,8,15]
 2. Security
     – Cookies [26] (for DDoS protection)
     – Adaptive Selective Verification (ASV) [4] (for DDoS protection)
     – Server Replicator (SR) and ASV+SR [39] (for DDoS protection)
     – Protocol Dialects [46]
 3. Distributed systems’ implementation and model checking
     – The D Transformation [68] for correct-by-construction distributed sys-
       tem implementation.
     – The P , Sim and M transformations for statistical model checking (SMC)
       analysis [63]
     – The M Transformation for automatically verifying consistency proper-
       ties of Distributed Transaction Systems [66]
 4. Theorem proving and executability transformations
     – The E 7→ E ≡ [50] and E 7→ E: [79] Transformations
                                 Ω
     – The R 7→ Rl and R 7→ RΣ1 ,l,r Transformations [77]
     – The R 7→ RU Transformation [35]
     – Partial Evaluation Transformations [2].

Detailed discussion of the above formal patterns is beyond the scope of this
paper. I refer to [76,78] for overviews of many of them, and to the references
given for each formal pattern for full details. Nevertheless, the P , Sim, M and
D transformations, as well as PALS, will make cameo appearances later in the
paper.


4     Qualitative and Quantitative Verification of Designs

I explain here how Maude meets requirement (6) from §2.1. Some of the require-
ments of a Maude system design may be quantitative. For example, they may
involve time, space, power or performance requirements; and they may involve
probabilities. They are typically specified in timed or probabilistic logics. Other
requirements, e.g., a system invariant, do not involve quantities and are then
called qualitative. They are typically specified in standard logics such as first-
order logic, temporal logics such as LTL and CTL*, Hoare logic and so on. The
difference between these two kinds of properties is not always clear-cut.
    Requirement (6) is important for system design because qualitative and quan-
titative properties are not independent. Quantitative requirements may be as
                                            Formally-Driven System Design        9

important as non-safety-critical qualitative ones, and a balance between them
may be needed. I provide a good illustration of this balancing need in §5.2.
    A Maude distributed system design is a rewrite theory R = (Σ, E, R), where
(Σ, E) is an equational theory (in fact an equational program) specifying the
system’s data types and auxiliary functions, and R is a collection of rewrite
rules describing the distributed system’s local concurrent transitions. The initial
model TR is a mathematical model of the distributed system R, but its states
are elements of the initial algebra TΣ/E of its equational theory (Σ, E).

Verification of Qualitative Requirements. Some of the formal requirements
of R may be purely functional and qualitative because they only involve TΣ/E .
For such requirements, the following Maude tools can verify various functional
properties: (i) the Church-Rosser Checker [37]; (ii) the Maude Termination Tool
(MTT) [34]; (iii) the Sufficient Completeness Checker (SCC) [51]; and (iv) the
New Inductive Theorem Prover (NuITP) [38].
    Many other qualitative formal requirements of R will involve TR , i.e., the
distributed system’s behavior. Some of these requirements, expressible in modal
logic as reachability requirements (e.g. invariants) or as LTL properties, can be
verified in Maude itself, either by (1) explicit state model checking features such
as: (i) the search command, (ii) its LTL model checker; or (iii) the extension
of the LTL model checker to verify properties under user-specified strategies
reported in [99], which will soon be added to Maude; or by (2) infinite-state,
narrowing-based model checking of invariants with the fvu-narrow command.
    Infinite-state model checking of LTL properties is instead supported by the
Maude Logical Model Checker tool [7]; and explicit-state model checking in
the richer logic LTLR is supported by Maude’s LTLR Model Checker tool [9].
Furthermore, the tool described in §6 of [97] makes it possible to model check
CLT* and µ-calculus temporal logic properties of Maude designs through an
interface to the LTSim model checker [52].

Verification of Quantitative or Mixed Requirements. I view real-time re-
quirements as mixed. The Real-Time Maude tool [91] can model check real-time
requirements expressed in either LTL or in timed CTL (TCTL). For quantita-
tive properties of actor-based distributed system designs involving both time and
probabilities, properties can be expresses in the QuaTEx quantitative probabilis-
tic temporal logic [1] and can be model checked in the parallel statistical model
checker PVesStA [3]. At present, the best tool supporting integrated statistical
model checking verification of Maude actor-based distributed system designs is
the Actors2PMaude tool [63], because it includes PVesStA as a subcomponent
and implements the P , S and M formal patterns mentioned in §3.2, which as
explained and demonstrated in [63], makes it much easier for a user to transform
a distributed Maude design into a probabilistic rewrite theory in the PMaude
language extension [1]. In addition to all these tools, the QMaude tool [98] sup-
ports both probabilistic (in PRISM [55] and Storm [32]) and statistical model
checking (in MultiVeStA [103]) of probabilisitic rewrite theories.
10     J. Meseguer

5    Experience Using Maude in Early System Design

As I have already pointed out, the formal design methodology of using formal
executable specifications ab origine in system design, implementation and ver-
ification is computational-logic-independent : any declarative language directly
based on a computational logic L can be used; but I have also pointed out in §2
that not all computational logics are equally expressive, or equally well-suited
for designing systems.
    All this implies that various computational logics can be and have been used
for this purpose. It is outside the scope of this paper to survey all such efforts.
What I can do here is to describe efforts which I have fairly detailed knowledge
about, namely, those using rewriting logic and Maude for this purpose. Even
within Maude, I am sure that there are various such uses I am unfamiliar with.
Let me mention several uses of Maude for early system design, implementation
and verification that, among others, I know about:

 1. Design, implementation and verification of the IBOS browser (more on this
    in §5.1).
 2. Design, implementation and verification of the ROLA distributed database
    (more on this in §5.2).
 3. The N-Tube provably secure inter-domain bandwidth reservation algorithm
    is a novel network algorithm with strong guarantees against DDoS attacks
    proposed by T. Weghorn, S. Liu et al. in [115]. N-Tube’s design was captured
    as a rewrite theory in Maude. Furthermore, to subject N-Tube’s design to
    detailed performance analysis by statistical model checking, N-Tube’s Maude
    design was then extended into a probabilistic rewrite theory in PMaude and
    was analyzed by statistical model checking in PVeStA [3].
 4. Design, implementation and validation of new Maude language features.
    Exploiting rewriting logic’s logical reflection and its support by Maude’s
    META-LEVEL module, most of the advanced features that have been added to
    Maude over the years have first been designed, implemented and validated
    in Maude. This has been greatly helped by the Full Maude language exten-
    sion [36,28], a metalevel Maude program that allows adding new features to
    Maude by reflection. I like to say that, at any point in time, Full Maude is
    what Maude will be. Only after a long experimentation in Full Maude (or in
    the Maude-NPA tool [44]) with a new Maude feature has it been later imple-
    mented in C++ for greater efficiency. Advanced features that have been so
    designed and implemented in Maude and have later been added to Maude’s
    C++ implementation include:
      – Parameterized theories, modules, and views.
      – Object-oriented modules.
      – Maude’s strategy language.
      – Unification algorithms modulo axioms.
      – Variant narrowing, Variant unification, and Variant-based reachability.
 5. Design, implementation and validation of Formal Tools. Rewriting logic
    is a good match for designing and building formal tools. This is so because
                                            Formally-Driven System Design       11

      it is a flexible logical framework [69], which can naturally represent many
      logics and formal inference systems by representing each inference rule in the
      given logic or system as a (possibly conditional) rewrite rule. This has been
      systematically exploited in designing and building formal tools in Maude in
      two ways:
      (1) Formal verifications tools for Maude such as:
        – Maude’s Church-Rosser and Coherence Checkers [37].
        – Maude’s Termination Tool (MTT) [34].
        – Maude’s Sufficient Completeness Checker (SCC) [51].
        – Maude’s Logical Model Checker [7].
        – Maude’s LTLR Model Checker [9].
        – Maude’s Inductive Theorem Prover (ITP) [31].
        – Maude’s New Inductive Theorem Prover (NuITP) [38].
        – Real-Time Maude [91]
        – PMaude Tool and statistical model checking environment (Actors2PMaude)
           [63].
      (2) Tools for other logics and specification formalisms such as, e.g.,
        – A LOTOS execution and analysis environment [114].
        – CafeInMaude translator from CafeOBJ to Maude and its formal verifi-
           cation environment [95].
        – The L-Framework, a Maude executable implementation of a meta-logical
           framework to mechanize and prove properties about a wide variety of
           sequent-based logics meta-represented as rewrite theories [90].
        – The HOL/Nuprl proof translator to transfer large libraries of theorems
           in the HOL theorem prover to theorems in the classical extension of
           NuPrl [109]. This translator defined a map of entailment systems (in the
           sense of the theory of general logics [72]) between the logics of HOL and
           NuPrl. The hand proof of correctness of this translator was later verified
           in the Twelf theorem prover [102].
        – The AADL2Maude [94] and SynchAADL2Maude [13] tools, giving se-
           mantics in Real-Time Maude to models of cyber-physical systems in
           the behavioral subset of the AADL modeling language and supporting
           model checking verification of such models. These tools are integrated
           with OSATE. I give more details on both of them in §6.2.

It is impossible to give details within this paper about all the above-mentioned
system designs and implementations. I can, however, illustrate the Maude-based
design methodology used in all of them by briefly summarizing two such designs,
namely, those of IBOS and ROLA.

5.1     IBOS
After a talk by Shuo Chen at the University of Illinois reporting on how Maude
had been used to uncover 13 types of previously unknown visual spoofing attacks
on IE, my colleague Sam King came to my office and posed to me the following
question, with roughly the following words:
12        J. Meseguer

      Why don’t we design and build a browser that is secure by design?

Sam’s question exemplified the enormous advantage of ab origine uses of formal
executable specifications over post facto uses: In a large system like IE with
over one million lines of code, it was possible and very useful to use Maude to
uncover and correct4 some security vulnerabilities; but it was essentially hopeless
to achieve strong security guarantees about the IE implementation itself.
    That conversation in my office was the start of a very fruitful 4-person (S.
King, J. Meseguer, S. Tang and R. Sasse) collaboration on the design of such
a secure-by-design browser: the Illinois Browser and Operating System (IBOS).
Sam was the Ph.D. advisor of Shuo Tang, and I advised the Ph.D. of Ralf Sasse.
Ralf was of course thoroughly familiar with Maude and formal verification. Shuo
took my CS 476 course to also become familiar with specification and verification
in Maude. The design of IBOS was captured in Maude from the very beginning
of the project. Sam and Shuo took the lead on deciding the architecture of IBOS,
including that of its small kernel, so as to meet specific security requirements,
and also on implementing IBOS in C++, whereas Ralf and I focused on improv-
ing the Maude formal design and verifying its security properties. Shuo and Ralf
interacted very closely, particularly to ensure that the C++ kernel implementa-
tion (about 60,000 lines of C++) developed by Shuo as part of his Ph.D. thesis
[113] fully agreed with the Maude design. Ralf undertook the model checking ver-
ification of IBOS’s security properties as part of his Ph.D. thesis [100]. The four
of us reported on the IBOS project and its formal specification and verification
in [101]. A deductive verification of the IBOS security properties in reachability
logic was later carried out in [106]. I summarize below the description of IBOS
given in [101] and [106] and refer to [101,106,113,100,107] for further details.
    The IBOS architecture can be graphically described as follows:




4
     The publication of [27] was delayed for about a year to allow the IE team to correct
     the security vulnerabilities uncovered by the verification of the Maude IE design.
                                              Formally-Driven System Design         13

    A key security property enforced by IBOS is the same-origin policy (SOP):
it isolates web apps from different origins, where an origin is represented as a
tuple of a protocol, a domain name, and a port number. The main components
of IBOS are:

 – Kernel, built on top of the L4Ka::Pistachio micro-kernel. Its main task is to
   enforce that inter-process communications meet the IBOS security policies.
 – Network Process. A network process is responsible for managing network
   connections to a specific origin. It understands how to encode and decode
   TCP datagrams and Ethernet frames and can send and receive frames from
   the network interface card (NIC).
 – Web App represents a specific instance of a web page loaded in a particular
   browser tab. Web apps know how to render HTML documents. As per SOP,
   each web page is labeled by its origin.
 – Browser UI. The browser user interface (UI) minimally includes the address
   bar and the mouse pointer and extends to any input mechanism.
 – Display. The display represents the rendered web app shown to the user; it
   is blank when no web app has loaded. For security, it cannot modify the UI.

    The security properties of IBOSVcan be formally expressed as an invariant P ,
which is itself a conjunction P = 1≤i≤11 Pi of eleven simpler invariants [106].
P implies the two main V  security properties of IBOS, namely, (i) SOP, which is
the conjunction SOP = 1≤i≤11 Pi , and  V (ii) the address bar correctness (ABC)
property, which is P10 . The invariant 1≤i≤10 Pi was verified by Ralf Sasse by
model checking [101,100], whereas P itself was deductively verified in reachability
logic by Stephen Skeirik as part of his Ph.D. thesis at Illinois [106,107].
    IBOS was an academic project. It did not become a commercial product.
IBOS demonstrated that a secure browser can be fruitfully designed and imple-
mented by capturing its design ab origine in a formal executable specification.


5.2   ROLA

The formal design, verification and implementation in Maude of the Read atOm-
icity and prevention of Lost updAtes (ROLA) distributed database [65] is part
of a much bigger joint effort by researchers at the University of Illinois and
the University of Oslo to formally specify in Maude and to verify the quali-
tative (consistency properties) and quantitative (performance properties) of a
wide range of industrial and academic distributed databases. To the best of my
knowledge, this was the first time that those distributed databases, lacking in
virtually all cases any prior formal specifications, were thus formally specified in
Maude and analyzed with respect to their consistency and performance proper-
ties. I refer to the survey [17] for details about this bigger research effort. What is
unique about both ROLA, as compared to all the other industrial and academic
distributed data bases described in [17], is that the Maude specifications of all
14        J. Meseguer

other databases were post facto efforts to specify and verify systems already im-
plemented.5 Instead, ROLA was designed, verified and implemented in Maude
ab origine.
    Another unique aspect of ROLA is that it illustrates how easy, fast and in-
expensive it is to explore the design space in search of an optimal design (w.r.t.
given requirements) by means of executable formal specifications. As already
pointed out in §1, it is usually very costly, and seldom done, to explore design
alternatives for a system developed from informal specifications. But it is even
more difficult and costly to compare different distributed systems with respect to
some correctness and performance requirements. To begin with, different systems
may be implemented in different programming languages, so that experimentally
comparing their behavior and performance may not allow answering the coun-
terfactual question: How would they compare if they had been implemented in
the same programming language? Answering this question might provide partial
evidence for the really crucial question: Is the design of system A better than
that of system B w.r.t. some given correctness and performance requirements?
Let me explain how the design of ROLA provides an answer to this question.
    Most modern distributed databases have large numbers of users, sometimes
located all over the world, with data stored and replicated across various data
centers. For these systems performance, and specifically availability, is as im-
portant as correctness, and specifically database consistency properties. In dis-
tributed database design there is an unavoidable tension between consistency
and availability, particularly when the network can be partitioned [23]. The fine
art of distributed database system design involves finding the right balance be-
tween availability and consistency in the design space. Such a balance actually
depends on the kinds of applications envisioned for the given database. For ex-
ample, the database of a social network will typically have considerably weaker
consistency requirements than those of a bank or a medical information system;
and this can be exploited to increase the performance of a social network.
    Exploring the distributed database design space can be guided by the degree
of database consistency needed for the system in question. Providing a greater
degree of consistency than necessary for a given application will often result in
loss of performance, including poorer availability. The work of Cerone et al. [25]
has provided a formal axiomatization of a hierarchy of increasingly stronger con-
sistency models —with read atomicity (RA) as the weakest and serializability
(SER) as the stronger—, as pictured in the black-marked models of the consis-
tency hierarchy of Figure 1 from [65]. The significance of ROLA is that it found
a previously unexplored sweetspot in the design space by adding one more node
to the consistency hierarchy of [25], namely the update atomic (UA) consistency,
marked in red in Figure 1, and has demonstrated clear performance advantages
5
     This should be qualified. New Maude designs of variants or extensions of already-
     implemented systems were also developed, verified and evaluated, such as alternative
     designs of Cassandra [62] and RAMP [64], and Megastore-CGC [49], a novel exten-
     sion of Google’s Megastore design. What all this work shows is that formal executable
     specifications can easily explore design alternatives for already implemented systems.
                                            Formally-Driven System Design        15

for this sweetspot, which is well suited for social media applications. The poten-
tial usefulness of UA was already conjectured in [25], but was left as a future
possibility.




Fig. 1. ROLA’s update atomic (UA) consistency model added to the hierarchy of con-
sistency models of Cerone et al. [25]




Due to space limitations I refer to [25] for further details on the consistency
models in Figure 1, and to [65] for a more detailed discussion of other related
consistency models and properties. For my design exploration purposes here,
the question I would like to focus on is: What database system designs ensuring
either parallel snapshot isolation (PSI) (the node right below UA) or something
slightly weaker than PSI existed prior to ROLA? The answer is that two such
system designs existed, namely, the Walter protocol [108] implementing PSI,
and the Jessy protocol [6], implementing the non-monotonic snapshot isolation
(NMSI) consistency model, which is weaker than PSI but satisfies causal con-
sistency (CC). Note that, unlike Walter and Jessy, ROLA does not satisfy CC,
but, as explained in [65], CC is not essential for social network applications such
as friendship networks. The main question then is: What are the gains in per-
formance obtained by focusing on the UA sweetspot? As I pointed out above,
this question would be hard to settle by comparing system implementations of
Walter, Jessy and ROLA. Furthermore, it would require implementing ROLA
before any such comparison became possible, thus defeating the design explo-
ration purpose. However, based on Maude formal executable specifications of
Walter, Jessy and ROLA (with the replication features of Walter and Jessy dis-
abled to obtain a fair comparison), and enriching these three specifications with
a common probability distribution on the time required for inter-node commu-
nication to obtain three associated probabilistic rewrite theories [63], it has been
possible to answer this question by statistical model checking analysis using the
PVeStA tool [3]. The answer is that, as shown in Figure 2 from [65], ROLA
clearly outperforms both Walter and Jessy in all performance requirements for
all read/write transaction rates.
16                                       J. Meseguer


                                              Workload on 25 Partitions with Uniform Distribution                                                                Workload on 25 Partitions with 90% Read-only Txns

                               40                                                                                                                     4
                                                                                           ROLA-50 keys
Avg. Latency (103 time unit)




                                                                                                                  Avg. Latency (103 time unit)
                               35                                                                                                                3.5
                                                                                          ROLA-200 keys
                               30                                                          Walter-50 keys                                             3
                                                                                          Walter-200 keys
                               25                                                                                                                2.5
                                                                                           Jessy-50 keys
                               20                                                         Jessy-200 keys                                              2
                               15                                                                                                                1.5
                               10                                                                                                                     1
                               5                                                                                                                 0.5            ROLA-uniform          Walter-uniform              Jessy-uniform
                                                                                                                                                                  ROLA-zipf              Walter-zipf                 Jessy-zipf
                               0                                                                                                                      0
                                    0    10     20     30      40     50     60      70       80      90    100                                           50                    100                         150                        200

                                                        Percentage of Read-only Txns                                                                                                  Number of Keys


                                               Workload on 100 Keys with Uniform Distribution                                                                        Workload on 100 Keys with Zipf Distribution

                               40                                                                                                                12
                                                                                            ROLA-10 par                                                                                                                ROLA-10 par
Avg. Latency (103 time unit)




                                                                                                                  Avg. Latency (103 time unit)
                               35
                                                                                            ROLA-30 par                                          10                                                                    ROLA-30 par
                               30                                                           Walter-10 par                                                                                                              Walter-10 par
                                                                                            Walter-30 par                                        8                                                                     Walter-30 par
                               25
                                                                                            Jessy-10 par                                                                                                               Jessy-10 par
                               20                                                           Jessy-30 par                                         6                                                                     Jessy-30 par
                               15
                                                                                                                                                 4
                               10
                                                                                                                                                 2
                               5
                               0                                                                                                                 0
                                    0    10     20     30      40     50     60      70       80      90    100                                       0    10      20      30     40        50         60         70     80       90         100

                                                        Percentage of Read-only Txns                                                                                       Percentage of Read-only Txns




                                        Fig. 2. Average latency comparison across varying workload conditions.


    For the model checking verification of ROLA’s consistency requirements I re-
fer the reader to §6 of [65]. This still leaves open the matter of ROLA’s implemen-
tation, and raises the question of how consistent would the ROLA performance
predictions be with experimental evaluations of ROLA. These two issues were
addressed in the subsequent paper [68]. In fact, [68] answered a much broader
question, namely:
                               Is it possible to automatically generate a correct-by-construction imple-
                               mentation of a distributed system design priorly captured in Maude?
This question was answered by means of a formal pattern, namely, the D-
transformation mentioned in §3.2. The point is that Maude is not only a lan-
guage to model and verify properties of concurrent systems using the Maude
interpreter and its formal tools. Thanks to its support for external objects, in-
cluding TCP/IP sockets, it is also a language to program and implement open
distributed systems [33]. What the D-transformation formal pattern does is to
transform an object-oriented system design in Maude into a distributed im-
plementation of it, also in Maude, that is stuttering bisimilar to the design.
Using the D-transformation it was then possible to automatically transform the
ROLA Maude design into a ROLA implementation and to experimentally evalu-
ate ROLA. As explained in [68], ROLA’s distributed implementation was exper-
imentally evaluated in two different scenarios, named ROLA_A and ROLA_B,
and the performance predictions for each scenario obtained by statistical model
checking of the ROLA design were compared with the corresponding experimen-
tal evaluations of its implementation. These results are summarized in Figure
3 from [68] and show a substantial agreement between the ROLA performance
                                                                                                                   Formally-Driven System Design                                  17

    predictions and the corresponding experimental evaluations. I refer to [68] for
    further details.


                                       Statistical Model Checking - ROLA_A                                                         Statistical Model Checking - ROLA_B
Throughput (txn/time unit)




                                                                                          Throughput (txn/time unit)
                             2.1                                                                                       2.5
                                           5 Partitions                                                                             95% Reads
                             1.8
                                           3 Partitions                                                                    2
                                                                                                                                    50% Reads
                             1.5                                                                                       1.5


                             1.2                                                                                           1


                             0.9                                                                                       0.5


                             0.6                                                                                           0
                                   0          25          50          75     100                                               0        10        20        30        40    50    60

                                                   Percentage Reads                                                                               Concurrent Clients
                               Distributed Maude Implementation - ROLA_A                                               Distributed Maude Implementation - ROLA_B
                                                                                                              400

                             400           5 Partitions                                                                            95% Reads
Throughput (txn/s)




                                           3 Partitions                            Throughput (txn/s)         300                  50% Reads
                             300


                                                                                                              200
                             200


                                                                                                              100
                             100



                               0                                                                                       0
                                   0          25          50          75     100                                           0        5        10        15        20    25   30   35

                                                   Percentage Reads                                                                           Concurrent Clients


    Fig. 3. ROLA: Comparison between statistical model checking (top) and distributed
    Maude implementation (bottom). Experiments ROLA_A (left) and ROLA_B (right)
    measure throughput for different number of partitions and different ratios of reads
    when varying ratios of reads and concurrent clients, respectively.




    6                              From Modeling Languages to Formal Designs

    Software modeling languages are widely used for software design. In this section
    I discuss the relationships between the model-based approach to design and
    the approach based on formal executable specification of designs that I have
    presented here. I would like to begin by asking the question:

                               How can formal executable specifications support and complement model-
                               based system design?

    I, together with other collaborators, as well as many other researchers, have
    spent substantial efforts over the years trying to provide practical, useful an-
    swers to this question. On the one hand, model-based approaches tend to be
    fairly intuitive and are widely adopted in industry, but it seems fair to say that
    to the degree to which they lack a formal executable semantics, they remain rel-
    atively weak in their predictive power. On the other hand, the design approach
    based on formal excutable specifications that I have presented has remarkable
18     J. Meseguer

capabilities for formally verifying designs and predicting their behaviors. Also,
for distributed systems, in the case of Maude, both approaches share a com-
mon object-based nature. Why not combining both approaches? A practical way
to facilitate this combination is to develop formal plugins for existing software
modeling languages that: (i) provide a formal semantics for the models in such
a language, and (ii) make simulation and formal analysis of models possible by
mapping each model to its formal semantics.
    In my view, the simplest and conceptually most satisfactory way of under-
standing these plugins is as mappings between modeling languages. To be concrete
for illustration purposes, let me choose Maude. It is perfectly consistent with ev-
erything I have said in this paper to call Maude a software formal modeling
language. Let M be another software modeling language. Then, a Maude-plugin
for M is simply (the implemention of) a formal semantics map:

                               J_K : M −→ Maude

that assigns to each model M ∈ M a corresponding Maude executable specifica-
tion JM K ∈ Maude, that is, a rewrite theory JM K, which is a formal executable
specification of the design formerly captured as M in the modeling language M.
     In Maude, mappings of this kind have been defined for a wide
range of modeling languages by many researchers including, e.g.,
[116,88,87,45,53,54,117,5,29,85,84,40,86,20,19,21,22,18,96]. This is just a sample:
it is impossible for me to do justice to such a large body of work here. But I can
give a flavor for the usefulness of formal plugins by focusing on two important
modeling languages for real-time and embedded systems, namely, Ptolemy II [41]
and AADL (http://www.aadl.info/). When M is either Ptolemy II or AADL,
the semantic mapping defining the formal plugin is more specific, namely, it has
the form:
                           J_K : M −→ RealTimeMaude
where Real-Time Maude [91] is the language and tool already mentioned in §5.
Such a semantic mapping maps each model M in either Ptolemy II or AADL
to a formal specification JM K in Real-Time Maude, i.e., to a real-time rewrite
theory, which is a special type of rewrite theory containing a model (which can
be either discrete or continuous) of time and modeling time elapse in a system.
My discussion of Ptolemy II and AADL below borrows ideas and examples from
[14], [13] and [82].

6.1   Ptolemy II
Ptolemy II [41] is a widely used graphical modeling and simulation language
tool for real-time and embedded systems. It supports design and simulation of
concurrent, real-time, embedded systems expressed in several models of com-
putation (MoCs), such as state machines, data flow, and discrete-event models,
that govern the interaction between concurrent components. A user can visually
design and simulate hierarchical models, which may combine different MoCs.
Furthermore, Ptolemy II has code generation capabilities to translate models
                                                       Formally-Driven System Design   19

into other modeling or programming languages such as C or Java. Discrete-
Event (DE) models are among the most central in Ptolemy II. Their semantics
is defined by the tagged signal model [56]. The work by Bae et al. in [11,14]
endows DE models in Ptolemy II with formal analysis capabilities by: (i) defin-
ing a semantics for them as real-time rewrite theories; (ii) automating such a
formal semantics as a model transformation using Ptolemy II’s code generation
features; (iii) providing a Real-Time Maude plugin, so that Ptolemy II users can
use an extended GUI to define temporal logic properties of their models in an
intutitive syntax and can invoke Real-Time Maude from the GUI to model check
their models. Let us see an example.

A Ptolemy Example. Figure 4 shows a Ptolemy II model from [14] of a
fault-tolerant traffic light system at a pedestrian crossing, consisting of one car


             HierarchicalTrafficLight




                                        TrafficLight
  Decision
                                                             TrafficLight




                  Normal

                                                            Error




        Fig. 4. A hierarchical fault-tolerant traffic light system in Ptolemy II.



light and one pedestrian light. Each light is represented by a set of set vari-
able actors (Pred and Pgrn represent the pedestrian light, and Cred, Cyel, and
20     J. Meseguer

Cgrn represent the car light). A light is on iff the corresponding variable has
the value 1. The Finite State Machine (FSM) actor Decision “generates” fail-
ures and repairs by alternating between staying in location Normal for 15 time
units and staying in location for Abnormal for 5 time units, and by sending
events to the TrafficLight through its Error and Ok ports accordingly. During
normal operations, the lights are controlled by the FSM actors CarLight and
PedestrianLight (their FSM’s are not shown in the figure) that send values to
set the variables; in addition, CarLight sends signals to the PedestrianLight
actor through its Pgo and Pstop output ports.
    For M this hierarchical Ptolemy II model, the semantic mapping M 7→ JM K
realized as a Real-Time Maude plugin associates to M a Real-Time Maude
specification that can then be formally analyzed by model checking. I refer to
[14] for further details about the real-time rewrite theory JM K for this example
and the formal verification of its properties.
    Real-Time Maude analysis (including automatically generating Real-Time
Mude models from Ptolemy II models) of such Ptolemy II DE models has been
integrated into Ptolemy II, and has been used, e.g., to uncover a previously
undetected flaw in the raffic light model: The yellow light may not be blinking
when the taffic light system is in Abnormal mode [60].

6.2   AADL
AADL (http://www.aadl.info/) is a standard for modeling embedded systems
that is widely used in avionics and other safety-critical applications. However,
AADL lacks a formal semantics, which severely limits both unambiguous com-
munication among model developers and the formal analysis of AADL models.
In [94] Ölveczky et al. defined a formal object-based real-time concurrent se-
mantics for a behavioral subset of AADL in rewriting logic, which includes the
essential aspects of AADL’s behavior annex. Such a semantics is directly exe-
cutable in Real-Time Maude and provides an AADL simulator and LTL model
checking tool called AADL2Maude. AADL2Maude is integrated with OSATE, so
that OSATE’s code generation facility is used to automatically transform AADL
models into their corresponding Real-Time Maude specifications. Such trans-
formed models can then be executed and model checked by Real-Time Maude.
One difficulty with AADL models is that, by being made up of various hierarchi-
cal components that communicate asynchronously with each other, their model
checking formal analysis can easily experience a combinatorial explosion. How-
ever, many such models express designs of distributed embedded systems which,
while being asynchronous, should behave in a virtually synchronous way. This
suggests the possibility of using the PALS formal pattern [80] already mentioned
in §3.2, which reduces distributed real-time systems with virtual synchrony to
synchronous ones, to pass from simple synchronous systems, which have much
smaller state spaces and are much easier to model check, to semantically equiv-
alent asynchronous systems, which often cannot be directly model checked but
can be verified indirectly through their synchronous counterparts. This has led
to the design of the Synchronous AADL sublanguage in [13], where the user
                                              Formally-Driven System Design         21

can specify synchronous AADL models by using a sublanguage of AADL with
some special keywords. A synchronous rewriting semantics for such models has
also been defined in [13]. Using OSATE’s code generation facility, synchronous
AADL models can be transformed into their corresponding Real-Time Maude
specifications in the SynchAADL2Maude tool, which is provided as a plugin to
OSATE. Likewise, the user can define temporal logic properties of synchronous
AADL models based on their features, without requiring knowledge of the under-
lying formalism, and can model check such models in Real-Time Maude. More
recently, Bae and others have extended Synchronous AADL, including the in-
tegration into OSATE, to multirate systems [16], hybrid systems [59,57], and
multirate hybrid systems [12,58]. In the hybrid systems cases, the semantics is
formalized using rewriting modulo SMT, and the main forms of analysis sup-
ported are randomized simulation, (bounded) symbolic reachability analysis, and
their combination. Somewhat surprisingly, the performance of such Maude-with-
SMT reachability analysis in many cases outperforms dedicated hybrid automata
reachability tools such as HyComp, SpaceEx, Flow∗, and dReach [59]. The effec-
tiveness of HybridSynchAADL and MR-HybridSynchAADL has been illustrated
on systems of collaborating drones.

A Synchronous AADL Example (from [13]). I sketch below a model of an
avionics system based on a specification by Steve Miller and Darren Cofer at
Rockwell-Collins [83]. A full description of this model is given in [13]; here I just
give an impressionistic description of it and refer to [13] for additional details.
The details, as such, are not the point of the example: the key point is to illustrate
the idea that a synchronous AADL model can be viewed as a synchronous com-
position of state machines (one such machine per AADL component), which are
formalized in the Real-Time Maude semantics as separate objects that change
their state synchronously.
    In integrated modular avionics (IMA), a cabinet is a chassis with a power
supply, internal bus, and general purpose computing, I/O, and memory cards.
Aircraft applications are implemented using the resources in the cabinets. There
are always two or more physically separated cabinets on the aircraft so that phys-
ical damage does not take out the computer system. The active standby system
considers the case of two cabinets and focuses on the logic for deciding which side
is active. Each side can fail, and a failed side can recover after failure. In case one
side fails, the non-failed side should be the active side. In addition, the pilot can
toggle the active status of the sides. The full functionality of each side depends
on the two sides’ perception of the availability of other system components. An
AADL-like graphical description of the system is shown in Figure 5, and the
following is a fragment of its top-level textual representation, which declares the
architecture of the system, with the three subcomponents sideOne, sideTwo,
and env, and with immediate data connections (denoted by the arrow ‘->’) from
the environment to the two sides, and with delayed data connections (‘->>’)
between the two sides. Each subcomponent contains a thread specification (not
shown) in AADL’s behavior annex.
22     J. Meseguer


                ActiveStandbySystem.impl                      SynchAADL::Synchronous => true
                                                              SynchAADL::SynchPerod => 2ms



                                         env: Environment.impl


                 side1Failed       side1FullyAvail           side2FullyAvail       side2Failed




                      sideOne:                  manualSelection          sideTwo:
                      Side1.impl                                         Side2.impl
                                                side1ActiveSide

                                                side2ActiveSide




               Fig. 5. The architecture of the active standby system.


system implementation ActiveStandbySystem.impl
  properties
  SynchAADL::Synchronous => true;    SynchAADL::SynchPeriod => 2 ms;
  subcomponents
    sideOne: system Side1.impl; sideTwo: system Side2.impl;
    env: system Environment.impl;
  connections
    data port sideOne.side1ActiveSide ->> sideTwo.side1ActiveSide;
    data port sideTwo.side2ActiveSide ->> sideOne.side2ActiveSide;
    data port env.side1FullyAvail -> sideOne.side1FullyAvail;
    data port env.side1FullyAvail -> sideTwo.side1FullyAvail;
    ...
end ActiveStandbySystem.impl;

Again, as for Ptolemy II, the key point for AADL is that, for M a synchronous
AADL model, the semantic mapping M 7→ JM K realized as an AADL plugin
associates to M a Real-Time Maude specification that can then be formally
analyzed by model checking. For the details of how this is done for the above
active standby example I refer the reader to [13]; and for examples in the further
extended plugins of Synchronous AADL to [16,59,57,12,58].


7    Conclusions
I have argued that capturing system designs in executable formal specifications
ab origine is one of the best and most cost-effective ways of developing system
designs of high quality and to verify their qualitative and quantitative require-
ments. I am not alone in holding this position. My proposed ideas are logic-
independent, and various researchers have been using different logics for this
purpose, not only in academia, but also in industry. For example, researchers
                                             Formally-Driven System Design        23

at Amazon web services have reported remarkable improvements in their design
and verification processes by adopting a formal design approach similar to mine
based on Lamport’s TLA+ [89].
    I have also argued that the choice of the computational logic on which to
capture system designs is a non-trivial matter deserving careful decisions; and
I have given six requirements that, in my own experience, make a logic enjoy-
ing them better suited for the task. I have also addressed the issue of design
modularity and reusability and have proposed that formal patterns can greatly
increase modularity and reusability and amortize design and verification efforts.
    I have then reported on my own experience in formal system design using
rewriting logic and Maude, illustrating that experience with concrete examples.
I have also explained the formal verification capabilities for both qualitative and
quantitative properties available in Maude and in its formal tool environment.
    Finally, I have summarized my own experience and that of many other re-
searchers about the benefits of combining formal-executable-specification-based
design and model-based design in a synergistic way by means of formal plug-
ins, illustrating those benefits by concrete examples in the area of real-time and
embedded systems.
    The future looks bright, but there are no easy victories. I think that certain
high-payoff areas may both greatly benefit from formal-executable-specification-
based design and can widely spread those benefits. They include:
 – Standards bodies, since capturing system standards in formal executable
   specifications can greatly increase system quality and trustworthiness. The
   example I mentioned about DNS and its formal specification in [61] dramat-
   ically underscores this prediction.
 – Programming languages, an area I illustrated with the example of the C
   formal executable semantics in K [43]. Many advances have taken place in the
   rewiriting logic semantics research project [70,82], and mature technologies
   based on these advances have been developed in companies such as RV Inc.
   that make this a ripe area.
 – Formal plugins for software modeling languages. As I have argued in §6, the
   synergy between the formal-executable-specification-based and the model-
   based approaches to system design can yield remarkable benefits. But this
   requires hard work on well-engineered new plugins and on case studies to
   facilitate the adoption of this synergistic approach in practice.
 – Generation of efficient correct-by-construction implementations from formal
   executable designs. Various research teams are making important advances
   to eliminate the formal gap between verified designs and implementations.

Acknowledgments. I thank the ETAPS organizers for giving me the opportunity of
presenting these ideas at ETAPS 2025 in Hamilton, Ontario. I am grateful to Francisco
Durán, Santiago Escobar, Si Liu, Narciso Martí-Oliet, Peter Ölveczky and Carolyn
Talcott for their very helpful comments that have allowed me to improve the paper.

Disclosure of Interests. The author has no competing interests to declare that are
relevant to the content of this article.
24      J. Meseguer

References

  1. Agha, G., Meseguer, J., Sen, K.: PMaude: Rewrite-based specification language
     for probabilistic object systems. Electr. Notes Theor. Comput. Sci. 153(2), 213–
     239 (2006)
  2. Alpuente, M., Cuenca-Ortega, A., Escobar, S., Meseguer, J.: A partial evaluation
     framework for order-sorted equational programs modulo axioms. J. Log. Algebraic
     Methods Program. 110 (2020)
  3. AlTurki, M., Meseguer, J.: PVeStA: A parallel statistical model-checking and
     quantitative analysis tool (2011), in Proc. CALCO 2011, Springer LNCS 6859,
     386–392
  4. AlTurki, M., Meseguer, J., Gunter, C.: Probabilistic modeling and analysis of
     DoS protection for the ASV protocol. Electr. Notes Theor. Comput. Sci. 234,
     3–18 (2009)
  5. Aoumeur, N., Saake, G.: Integrating and rapid-prototyping UML structural and
     behavioural diagrams using rewriting logic. In: Pidduck, A.B., Mylopoulos, J.,
     Woo, C.C., Özsu, M.T. (eds.) Advanced Information Systems Engineering, 14th
     International Conference, CAiSE 2002, Toronto, Canada, May 27-31, 2002, Pro-
     ceedings. Lecture Notes in Computer Science, vol. 2348, pp. 296–310. Springer
     (2002), http://dx.doi.org/10.1007/3-540-47961-9
  6. Ardekani, M.S., Sutra, P., Shapiro, M.: Non-monotonic snapshot isolation: Scal-
     able and strong consistency for geo-replicated transactional systems. In: IEEE
     32nd Symposium on Reliable Distributed Systems, SRDS 2013, Braga, Portu-
     gal, 1-3 October 2013. pp. 163–172. IEEE Computer Society (2013). https:
     //doi.org/10.1109/SRDS.2013.25, https://doi.org/10.1109/SRDS.2013.25
  7. Bae, K., Escobar, S., Meseguer, J.: Abstract Logical Model Checking of Infinite-
     State Systems Using Narrowing. In: Rewriting Techniques and Applications
     (RTA’13). LIPIcs, vol. 21, pp. 81–96. Schloss Dagstuhl–Leibniz-Zentrum fuer In-
     formatik (2013)
  8. Bae, K., Krisiloff, J., Meseguer, J., Ölveczky, P.C.: Designing and verifying dis-
     tributed cyber-physical systems using multirate PALS: an airplane turning control
     system case study. Sci. Comput. Program. 103, 13–50 (2015)
  9. Bae, K., Meseguer, J.: Model checking linear temporal logic of rewriting formulas
     under localized fairness. Sci. Comput. Program. 99, 193–234 (2015)
 10. Bae, K., Meseguer, J., Ölveczky, P.C.: Formal patterns for multirate distributed
     real-time systems. Sci. Comput. Program. 91, 3–44 (2014)
 11. Bae, K., Ölveczky, P.C.: Extending the Real-Time Maude semantics of Ptolemy
     to hierarchical DE models. In: Ölveczky [92], pp. 46–66, http://dx.doi.org/10.
     4204/EPTCS.36.3
 12. Bae, K., Ölveczky, P.C.: Formal model engineering of distributed CPSs us-
     ing AADL: From behavioral AADL models to Multirate Hybrid Synchronous
     AADL. In: FACS’23. Lecture Notes in Computer Science, vol. 14485, pp. 127–
     152. Springer (2023)
 13. Bae, K., Ölveczky, P.C., Al-Nayeem, A., Meseguer, J.: Synchronous AADL and its
     formal analysis in Real-Time Maude. In: Qin, S., Qiu, Z. (eds.) ICFEM. Lecture
     Notes in Computer Science, vol. 6991, pp. 651–667. Springer (2011)
 14. Bae, K., Ölveczky, P.C., Feng, T.H., Lee, E.A., Tripakis, S.: Verifying hierarchical
     Ptolemy II discrete-event models using Real-Time Maude. Sci. Comput. Program.
     77(12), 1235–1271 (2012)
                                               Formally-Driven System Design          25

15. Bae, K., Ölveczky, P.C., Meseguer, J.: Definition, semantics, and analysis of mul-
    tirate synchronous AADL. In: FM. Lecture Notes in Computer Science, vol. 8442,
    pp. 94–109. Springer (2014)
16. Bae, K., Ölveczky, P.C., Meseguer, J.: Definition, semantics, and analysis of
    Multirate Synchronous AADL. In: FM’14. Lecture Notes in Computer Science,
    vol. 8442, pp. 94–109. Springer (2014)
17. Bobba, R., Grov, J., Gupta, I., Liu, S., Meseguer, J., Ölveczky, P.C., Skeirik, S.:
    Survivability: Design, formal modeling, and validation of cloud storage systems
    using Maude. In: Campbell, R.H., Kamhoua, C.A., Kwiat, K.A. (eds.) Assured
    Cloud Computing, chap. 2, pp. 10–48. Wiley-IEEE Computer Society Press (2018)
18. Boronat, A., Meseguer, J.: An algebraic semantics for MOF. Formal Asp. Comput.
    22(3-4), 269–296 (2010)
19. Boronat, A.: MOMENT: A Formal Framework for MOdel ManageMENT. Ph.D.
    thesis, Universitat Politècnica de València, Spain (2007)
20. Boronat, A., Carsí, J.A., Ramos, I.: Automatic reengineering in MDA using
    rewriting logic as transformation engine. In: Gold, N., Systä, T. (eds.) Proceed-
    ings of the 9th European Conference on Software Maintenance and Reengineer-
    ing, CSMR 2005, Manchester, UK, March 21-23, 2005, Proceedings. pp. 228–231.
    IEEE Computer Society (2005)
21. Boronat, A., Heckel, R., Meseguer, J.: Rewriting logic semantics and verifica-
    tion of model transformations. In: Chechik, M., Wirsing, M. (eds.) Fundamen-
    tal Approaches to Software Engineering, 12th International Conference, FASE
    2009, Held as Part of the Joint European Conferences on Theory and Prac-
    tice of Software, ETAPS 2009, York, UK, March 22-29, 2009. Proceedings. Lec-
    ture Notes in Computer Science, vol. 5503, pp. 18–33. Springer (2009), http:
    //dx.doi.org/10.1007/978-3-642-00593-0
22. Boronat, A., Meseguer, J.: MOMENT2: EMF model transformations in Maude.
    In: Vallecillo, A., Sagardui, G. (eds.) Actas de las XIV Jornadas de Ingeniería del
    Software y Bases de Datos, JISBD 2009, San Sebastián, España, Septiembre 8-11,
    2009. pp. 178–179 (2009)
23. Brewer, E.A.: Towards robust distributed systems (abstract). In: Proceedings of
    the Nineteenth Annual ACM Symposium on Principles of Distributed Computing.
    p. 7. ACM (2000)
24. Bruni, R., Meseguer, J.: Semantic foundations for generalized rewrite theories.
    Theor. Comput. Sci. 360(1-3), 386–414 (2006)
25. Cerone, A., Bernardi, G., Gotsman, A.: A framework for transactional consis-
    tency models with atomic visibility. In: Proc. 26th International Conference on
    Concurrency Theory, CONCUR 2015. LIPIcs, vol. 42, pp. 58–71. Schloss Dagstuhl
    - Leibniz-Zentrum fuer Informatik (2015)
26. Chadha, R., Gunter, C.A., Meseguer, J., Shankesi, R., Viswanathan, M.: Modular
    preservation of safety properties by cookie-based DoS-protection wrappers. In:
    Proc. FMOODS 2008. LNCS, vol. 5051, pp. 39–58. Springer (2008)
27. Chen, S., Meseguer, J., Sasse, R., Wang, H.J., Wang, Y.M.: A systematic approach
    to uncover security flaws in GUI logic. In: IEEE Symposium on Security and
    Privacy. pp. 71–85. IEEE (2007)
28. Clavel, M., Durán, F., Eker, S., Meseguer, J., Lincoln, P., Martí-Oliet, N., Talcott,
    C.: All About Maude – A High-Performance Logical Framework. Springer LNCS
    Vol. 4350 (2007)
29. Clavel, M., Egea, M.: ITP/OCL: A rewriting-based validation tool for UML+OCL
    static class diagrams. In: Johnson, M., Vene, V. (eds.) Algebraic Methodology
26      J. Meseguer

     and Software Technology, 11th International Conference, AMAST 2006, Kures-
     saare, Estonia, July 5-8, 2006, Proceedings. Lecture Notes in Computer Science,
     vol. 4019, pp. 368–373. Springer (2006), http://dx.doi.org/10.1007/11784180
 30. Clavel, M., Meseguer, J., Palomino, M.: Reflection in membership equational
     logic, many-sorted equational logic, Horn logic with equality, and rewriting logic.
     In: Gadducci, F., Montanari, U. (eds.) Proc. 4th. Intl. Workshop on Rewriting
     Logic and its Applications. vol. 71. ENTCS, Elsevier (2002)
 31. Clavel, M., Palomino, M., Riesco, A.: Introducing the ITP tool: a tutorial. The-
     oretical Computer Science 12, 1618–1650 (2006)
 32. Dehnert, C., Junges, S., Katoen, J., Volk, M.: A Storm is coming: A modern
     probabilistic model checker. In: Majumdar, R., Kuncak, V. (eds.) Computer Aided
     Verification - 29th International Conference, CAV 2017, Heidelberg, Germany,
     July 24-28, 2017, Proceedings, Part II. Lecture Notes in Computer Science, vol.
     10427, pp. 592–600. Springer (2017)
 33. Durán, F., Eker, S., Escobar, S., Martí-Oliet, N., Meseguer, J., Rubio, R., Tal-
     cott, C.L.: Programming open distributed systems in Maude. In: Bruni, A.,
     Momigliano, A., Pradella, M., Rossi, M., Cheney, J. (eds.) Proceedings of the
     26th International Symposium on Principles and Practice of Declarative Pro-
     gramming, PPDP 2024, Milano, Italy, September 9-11, 2024. pp. 7:1–7:12. ACM
     (2024), https://doi.org/10.1145/3678232.3678237
 34. Durán, F., Lucas, S., Meseguer, J.: MTT: The Maude Termination Tool (system
     description). In: IJCAR 2008. Lecture Notes in Computer Science, vol. 5195, pp.
     313–319. Springer (2008)
 35. Durán, F., Lucas, S., Meseguer, J.: Termination modulo combinations of equa-
     tional theories. In: Frontiers of Combining Systems, 7th International Symposium,
     FroCoS 2009, Trento, Italy, September 16-18, 2009. Proceedings. Lecture Notes
     in Computer Science, vol. 5749, pp. 246–262. Springer (2009)
 36. Durán, F., Meseguer, J.: Maude’s module algebra. Sci. Comput. Program. 66(2),
     125–153 (2007)
 37. Durán, F., Meseguer, J.: On the Church-Rosser and coherence properties of con-
     ditional order-sorted rewrite theories. J. Algebraic and Logic Programming 81,
     816–850 (2012)
 38. Durán, F.J., Escobar, S., Meseguer, J., Sapiña, J.: Nuitp: An inductive the-
     orem prover for equational program verification. In: Bruni, A., Momigliano,
     A., Pradella, M., Rossi, M., Cheney, J. (eds.) Proceedings of the 26th Inter-
     national Symposium on Principles and Practice of Declarative Programming,
     PPDP 2024, Milano, Italy, September 9-11, 2024. pp. 6:1–6:11. ACM (2024),
     https://doi.org/10.1145/3678232.3678236
 39. Eckhardt, J., Mühlbauer, T., AlTurki, M., Meseguer, J., Wirsing, M.: Stable avail-
     ability under denial of service attacks through formal patterns. In: de Lara, Zis-
     man (eds.) FASE. LNCS, vol. 7212, pp. 78–93. Springer (2012)
 40. Egea, M., Rusu, V.: Formal executable semantics for conformance in the MDE
     framework. Innovations in Systems and Software Engineering 6(1-2), 73–81 (2009)
 41. Eker, J., Janneck, J.W., Lee, E.A., Liu, J., Liu, X., Ludvig, J., Neuendorffer, S.,
     Sachs, S., Xiong, Y.: Taming heterogeneity—the Ptolemy approach. Proceedings
     of the IEEE 91(2), 127–144 (2003)
 42. Eker, S., Knapp, M., Laderoute, K., Lincoln, P., Meseguer, J., Sonmez, K.: Path-
     way logic: Symbolic analysis of biological signaling. In: Proceedings of the Pacific
     Symposium on Biocomputing. pp. 400–412 (January 2002)
 43. Ellison, C., Rosu, G.: An executable formal semantics of C with applications. In:
     Field, J., Hicks, M. (eds.) POPL. pp. 533–544. ACM (2012)
                                             Formally-Driven System Design          27

44. Escobar, S., Meadows, C., Meseguer, J.: Maude-NPA: cryptographic protocol
    analysis modulo equational properties. In: Foundations of Security Analysis and
    Design V, FOSAD 2007/2008/2009 Tutorial Lectures, LNCS, vol. 5705, pp. 1–50.
    Springer (2009)
45. Fernández Alemán, J.L., Toval Álvarez, J.A.: Can intuition become rigorous?
    Foundations for UML model verification tools. In: Titsworth, F.M. (ed.) Pro-
    ceedings of the 11th International Symposium on Software Reliability Engineer-
    ing, ISSRE 2000, San Jose, CA, USA, October 8-11, 2000. pp. 344–355. IEEE
    Computer Society (2000), http://dx.doi.org/10.1109/ISSRE.2000.885885
46. Galán, D., García, V., Escobar, S., Meadows, C.A., Meseguer, J.: Protocol di-
    alects as formal patterns. In: Tsudik, G., Conti, M., Liang, K., Smaragdakis,
    G. (eds.) Computer Security - ESORICS 2023 - 28th European Symposium on
    Research in Computer Security, The Hague, The Netherlands, September 25-29,
    2023, Proceedings, Part II. Lecture Notes in Computer Science, vol. 14345, pp.
    42–61. Springer (2023)
47. Garavel, H., ter Beek, M.H., van de Pol, J.: The 2020 expert survey on formal
    methods. In: ter Beek, M.H., Nickovic, D. (eds.) Formal Methods for Industrial
    Critical Systems - 25th International Conference, FMICS 2020, Vienna, Austria,
    September 2-3, 2020, Proceedings. Lecture Notes in Computer Science, vol. 12327,
    pp. 3–69. Springer (2020)
48. Goguen, J., Burstall, R.: Institutions: Abstract model theory for specification and
    programming. Journal of the ACM 39(1), 95–146 (1992)
49. Grov, J., Ölveczky, P.C.: Increasing consistency in multi-site data stores:
    Megastore-CGC and its formal analysis. In: Giannakopoulou, D., Salaün, G.
    (eds.) Software Engineering and Formal Methods - 12th International Confer-
    ence, SEFM 2014, Grenoble, France, September 1-5, 2014. Proceedings. Lecture
    Notes in Computer Science, vol. 8702, pp. 159–174. Springer (2014)
50. Gutiérrez, R., Meseguer, J., Rocha, C.: Order-sorted equality enrichments modulo
    axioms. Sci. Comput. Program. 99, 235–261 (2015)
51. Hendrix, J., Meseguer, J., Ohsaki, H.: A sufficient completeness checker for lin-
    ear order-sorted specifications modulo axioms. In: Automated Reasoning, Third
    International Joint Conference, IJCAR 2006. pp. 151–155 (2006)
52. Kant, G., Laarman, A., Meijer, J., van de Pol, J., Blom, S., van Dijk, T.: LTSmin:
    High-performance language-independent model checking. In: Baier, C., Tinelli,
    C. (eds.) Tools and Algorithms for the Construction and Analysis of Systems -
    21st International Conference, TACAS 2015, Held as Part of the European Joint
    Conferences on Theory and Practice of Software, ETAPS 2015, London, UK,
    April 11-18, 2015. Proceedings. Lecture Notes in Computer Science, vol. 9035,
    pp. 692–707. Springer (2015)
53. Knapp, A.: Generating rewrite theories from UML collaborations. In: Futatsugi,
    K., Nakagawa, A.T., Tamai, T. (eds.) Cafe: An Industrial-Strength Algebraic
    Formal Method, pp. 97–120. Elsevier (2000)
54. Knapp, A.: A Formal Approach to Object-Oriented Software Engineering. Shaker
    Verlag, Aachen, Germany (2001), phD thesis, Institut für Informatik, Universität
    München, 2000.
55. Kwiatkowska, M.Z., Norman, G., Parker, D.: PRISM 4.0: Verification of prob-
    abilistic real-time systems. In: Gopalakrishnan, G., Qadeer, S. (eds.) Com-
    puter Aided Verification - 23rd International Conference, CAV 2011, Snowbird,
    UT, USA, July 14-20, 2011. Proceedings. Lecture Notes in Computer Science,
    vol. 6806, pp. 585–591. Springer (2011)
28      J. Meseguer

 56. Lee, E.A.: Modeling concurrent real-time processes using discrete events. Ann.
     Software Eng. 7, 25–45 (1999)
 57. Lee, J., Bae, K., Ölveczky, P.C.: An extension of HybridSynchAADL and its
     application to collaborating autonomous UAVs. In: ISoLA’22. Lecture Notes in
     Computer Science, vol. 13703, pp. 47–64. Springer (2022)
 58. Lee, J., Bae, K., Ölveczky, P.C.: Rigorous model engineering of hierarchical multi-
     rate CPSs in MR-HybridSynchAADL. In: ISoLA’24. Lecture Notes in Computer
     Science, vol. 15220, pp. 243–262. Springer (2024)
 59. Lee, J., Kim, S., Bae, K., Ölveczky, P.C.: HybridSynchAADL: Modeling and for-
     mal analysis of virtually synchronous CPSs in AADL. In: CAV’21. Lecture Notes
     in Computer Science, vol. 12759, pp. 491–504. Springer (2021)
 60. Lepri, D., Ábrahám, E., Ölveczky, P.C.: Sound and complete timed CTL model
     checking of timed Kripke structures and real-time rewrite theories. Science of
     Computer Programming 99, 128–192 (2015)
 61. Liu, S., Duan, H., Heimes, L., Bearzi, M., Vieli, J., Basin, D.A., Perrig, A.: A
     formal framework for end-to-end DNS resolution. In: Schulzrinne, H., Misra,
     V., Kohler, E., Maltz, D.A. (eds.) Proceedings of the ACM SIGCOMM 2023
     Conference, ACM SIGCOMM 2023, New York, NY, USA, 10-14 September
     2023. pp. 932–949. ACM (2023). https://doi.org/10.1145/3603269.3604870,
     https://doi.org/10.1145/3603269.3604870
 62. Liu, S., Ganhotra, J., Rahman, M.R., Nguyen, S., Gupta, I., Meseguer, J.: Quan-
     titative analysis of consistency in NoSQL key-value stores. Leibniz Trans. Embed.
     Syst. 4(1), 03:1–03:26 (2017)
 63. Liu, S., Meseguer, J., Ölveczky, P.C., Zhang, M., Basin, D.A.: Bridging the se-
     mantic gap between qualitative and quantitative models of distributed systems.
     Proc. ACM Program. Lang. 6(OOPSLA2), 315–344 (2022)
 64. Liu, S., Ölveczky, P.C., Ganhotra, J., Gupta, I., Meseguer, J.: Exploring design
     alternatives for RAMP transactions through statistical model checking. In: Proc.
     Formal Methods and Software Engineering - 19th International Conference on
     Formal Engineering Methods, ICFEM 2017. Lecture Notes in Computer Science,
     vol. 10610, pp. 298–314. Springer (2017)
 65. Liu, S., Ölveczky, P.C., Wang, Q., Gupta, I., Meseguer, J.: Read atomic trans-
     actions with prevention of lost updates: ROLA and its formal analysis. Formal
     Aspects Comput. 31(5), 503–540 (2019)
 66. Liu, S., Ölveczky, P.C., Zhang, M., Wang, Q., Meseguer, J.: Automatic analysis
     of consistency properties of distributed transaction systems in Maude. In: Proc.
     TACAS 2019, Part II. Lecture Notes in Computer Science, vol. 11428, pp. 40–57.
     Springer (2019)
 67. Liu, S., Rahman, M.R., Skeirik, S., Gupta, I., Meseguer, J.: Formal modeling and
     analysis of Cassandra in Maude. In: Formal Methods and Software Engineering
     – 16th International Conference on Formal Engineering Methods, ICFEM 2014,
     Luxembourg, Luxembourg, November 3-5, 2014. Proceedings. Lecture Notes in
     Computer Science, vol. 8829, pp. 332–347. Springer (2014)
 68. Liu, S., Sandur, A., Meseguer, J., Ölveczky, P.C., Wang, Q.: Generating correct-
     by-construction distributed implementations from formal Maude designs. In:
     Proc. NASA Formal Methods: 12th International Symposium, NFM 2020,. Lec-
     ture Notes in Computer Science, vol. 12229, pp. 22–40. Springer (2020)
 69. Martí-Oliet, N., Meseguer, J.: Rewriting logic as a logical and semantic frame-
     work. In: Gabbay, D., Guenthner, F. (eds.) Handbook of Philosophical Logic,
     2nd. Edition, pp. 1–87. Kluwer Academic Publishers (2002), first published as
     SRI Tech. Report SRI-CSL-93-05, August 1993
                                            Formally-Driven System Design         29

70. Meseguer, J., Roşu, G.: The rewriting logic semantics project. Theoretical Com-
    puter Science 373, 213–237 (2007)
71. Meseguer, J., Talcott, C.: Semantic models for distributed object reflection. In:
    Proceedings of ECOOP’02, Málaga, Spain, June 2002. pp. 1–36. Springer LNCS
    2374 (2002)
72. Meseguer, J.: General logics. In: et al., H.D.E. (ed.) Logic Colloquium’87. pp.
    275–329. North-Holland (1989)
73. Meseguer, J.: Conditional rewriting logic as a unified model of concurrency. The-
    oretical Computer Science 96(1), 73–155 (1992)
74. Meseguer, J.: A logical theory of concurrent objects and its realization in the
    Maude language. In: Agha, G., Wegner, P., Yonezawa, A. (eds.) Research Di-
    rections in Concurrent Object-Oriented Programming, pp. 314–390. MIT Press
    (1993)
75. Meseguer, J.: Twenty years of rewriting logic. J. Algebraic and Logic Programming
    81, 721–781 (2012)
76. Meseguer, J.: Taming distributed system complexity through formal patterns. Sci.
    Comput. Program. 83, 3–34 (2014)
77. Meseguer, J.: Generalized rewrite theories, coherence completion, and symbolic
    methods. J. Log. Algebraic Methods Program. 110 (2020)
78. Meseguer, J.: Building correct-by-construction systems with formal patterns. In:
    Madeira, A., Martins, M.A. (eds.) Recent Trends in Algebraic Development Tech-
    niques - 26th IFIP WG 1.3 International Workshop, WADT 2022, Aveiro, Por-
    tugal, June 28-30, 2022, Revised Selected Papers. Lecture Notes in Computer
    Science, vol. 13710, pp. 3–24. Springer (2022)
79. Meseguer, J.: Checking sufficient completeness by inductive theorem proving. In:
    Bae, K. (ed.) Rewriting Logic and Its Applications - 14th International Work-
    shop, WRLA@ETAPS 2022, Munich, Germany, April 2-3, 2022, Revised Selected
    Papers. Lecture Notes in Computer Science, vol. 13252, pp. 171–190. Springer
    (2022)
80. Meseguer, J., Ölveczky, P.C.: Formalization and correctness of the PALS archi-
    tectural pattern for real-time systems. In: 12th International Conference on For-
    mal Engineering Methods (ICFEM 2010). vol. 6447, pp. 303–320. Springer LNCS
    (2010)
81. Meseguer, J., Ölveczky, P.C.: Formalization and correctness of the PALS archi-
    tectural pattern for distributed real-time systems. Theor. Comput. Sci. 451, 1–37
    (2012)
82. Meseguer, J., Rosu, G.: The rewriting logic semantics project: A progress report.
    Inf. Comput. 231, 38–69 (2013)
83. Miller, S., Cofer, D., Sha, L., Meseguer, J., Al-Nayeem, A.: Implementing logical
    synchrony in integrated modular avionics. In: Proc. 28th Digital Avionics Systems
    Conference. IEEE (2009)
84. Mokhati, F., Badri, M.: Generating Maude specifications from UML use case
    diagrams. Journal of Object Technology 8(2), 319–136 (2009)
85. Mokhati, F., Gagnon, P., Badri, M.: Verifying UML diagrams with model check-
    ing: A rewriting logic based approach. In: Mathur, A., Wong, W.E. (eds.) Pro-
    ceedings of the Seventh International Conference on Quality Software, QSIC 2007,
    Portland, Oregon, USA, October 11-12, 2007. pp. 356–362. IEEE Computer So-
    ciety (2007)
86. Mokhati, F., Sahraoui, B., Bouzaher, S., Kimour, M.T.: A tool for specifying and
    validating agents’ interaction protocols: From Agent UML to Maude. Journal of
    Object Technology 9(3), 59–77 (2010)
30      J. Meseguer

 87. Nakajima, S.: Using algebraic specification techniques in development of object-
     oriented frameworks. In: Wing, J.M., Woodcock, J., Davies, J. (eds.) FM’99 -
     Formal Methods, World Congress on Formal Methods in the Development of
     Computing Systems, Toulouse, France, September 20-24, 1999, Proceedings, Vol-
     ume II. Lecture Notes in Computer Science, vol. 1709, pp. 1664–1683. Springer
     (1999)
 88. Nakajima, S., Futatsugi, K.: An object-oriented modeling method for algebraic
     specifications in CafeOBJ. In: Proceedings of the 19th International Conference
     on Software Engineering, ICSE’97, Boston, Massachussets, May 17-23, 1997. ACM
     Press (1997)
 89. Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker, M., Deardeuff, M.:
     How Amazon web services uses formal methods. Commun. ACM 58(4), 66–73
     (2015)
 90. Olarte, C., Pimentel, E., Rocha, C.: A rewriting logic approach to specification,
     proof-search, and meta-proofs in sequent systems. Journal of Logical and Alge-
     braic Methods in Programming 130, 100827 (2023)
 91. Ölveczky, P.C., Meseguer, J.: Semantics and pragmatics of Real-Time Maude.
     Higher-Order and Symbolic Computation 20(1–2), 161–196 (2007)
 92. Ölveczky, P.C. (ed.): Proceedings of the First International Workshop on Rewrit-
     ing Techniques for Real-Time Systems, RTRTS 2010, Longyearbyen, Spitsbergen,
     Norway, April 6-9, 2010. Electronic Proceedings in Theoretical Computer Science,
     Computing Research Repository (CoRR)
 93. Ölveczky, P.C. (ed.): Rewriting Logic and its Applications. 8th International
     Workshop, WRLA 2010, Held as a Satellite Event of ETAPS 2010, Paphos,
     Cyprus, March 20-21, 2010, Revised Selected Papers, Lecture Notes in Computer
     Science, vol. 6381. Springer (2010)
 94. Ölveczky, P.C., Boronat, A., Meseguer, J.: Formal semantics and analysis of be-
     havioral AADL models in Real-Time Maude. In: FMOODS/FORTE’10. Lecture
     Notes in Computer Science, vol. 6117, pp. 47–62. Springer (2010)
 95. Riesco, A., Ogata, K.: An integrated tool set for verifying cafeobj specifications.
     Journal of Systems and Software 189, 111302 (2022). https://doi.org/https:
     //doi.org/10.1016/j.jss.2022.111302
 96. Rivera, J.E., Durán, F., Vallecillo, A.: On the behavioral semantics of real-time
     domain specific visual languages. In: Ölveczky [93], pp. 174–190
 97. Rubio, R., Martí-Oliet, N., Pita, I., Verdejo, A.: Strategies, model checking and
     branching-time properties in Maude. J. Log. Algebraic Methods Program. 123,
     100700 (2021)
 98. Rubio, R., Martí-Oliet, N., Pita, I., Verdejo, A.: QMaude: Quantitative specifi-
     cation and verification in rewriting logic. In: Chechik, M., Katoen, J., Leucker,
     M. (eds.) Formal Methods - 25th International Symposium, FM 2023, Lübeck,
     Germany, March 6-10, 2023, Proceedings. Lecture Notes in Computer Science,
     vol. 14000, pp. 240–259. Springer (2023)
 99. Rubio, R., Martí-Oliet, N., Pita, I., Verdejo, A.: Model checking strategy-
     controlled systems in rewriting logic. CoRR abs/2401.07616 (2024)
100. Sasse, R.: Security models in rewriting logic for cryptographic protocols and
     browsers. Ph.D. thesis, University of Illinois at Urbana-Champaign (2012),
     http://hdl.handle.net/2142/34373
101. Sasse, R., King, S.T., Meseguer, J., Tang, S.: IBOS: A correct-by-construction
     modular browser. In: FACS 2012. Lecture Notes in Computer Science, vol. 7684,
     pp. 224–241. Springer (2013)
                                               Formally-Driven System Design          31

102. Schürmann, C., Stehr, M.O.: An executable formalization of the hol/nuprl con-
     nection in the metalogical framework twelf. pp. 150–166 (11 2006). https:
     //doi.org/10.1007/11916277_11
103. Sebastio, S., Vandin, A.: MultiVeStA: statistical model checking for discrete
     event simulators. In: Horváth, A., Buchholz, P., Cortellessa, V., Muscariello, L.,
     Squillante, M.S. (eds.) 7th International Conference on Performance Evaluation
     Methodologies and Tools, ValueTools ’13, Torino, Italy, December 10-12, 2013.
     pp. 310–315. ICST/ACM (2013)
104. Şerbănuţă, T.F.: A Rewriting Approach to Concurrent Programming Language
     Design and Semantics. Ph.D. thesis, Department of Computer Science, University
     of Illinois at Urbana-Champaign (2010), http://hdl.handle.net/2142/18252,
     http://hdl.handle.net/2142/18252
105. Şerbănuţă, T.F., Roşu, G.: K-Maude: A rewriting based tool for semantics of
     programming languages. In: Ölveczky [93], pp. 104–122
106. Skeirik, S., Meseguer, J., Rocha, C.: Verification of the IBOS browser security
     properties in reachability logic. In: Proc. WRLA 2020. LNCS, vol. 12328, pp.
     176–196. Springer (2020)
107. Skeirik, S.: Rewriting-based symbolic methods for distributed system verification.
     Ph.D. thesis, University of Illinois at Urbana-Champaign (2019), http://hdl.
     handle.net/2142/106224
108. Sovran, Y., Power, R., Aguilera, M.K., Li, J.: Transactional storage for geo-
     replicated systems. In: Wobber, T., Druschel, P. (eds.) Proceedings of the 23rd
     ACM Symposium on Operating Systems Principles 2011, SOSP 2011, Cascais,
     Portugal, October 23-26, 2011. pp. 385–400. ACM (2011). https://doi.org/10.
     1145/2043556.2043592, https://doi.org/10.1145/2043556.2043592
109. Stehr, M.O., Naumov, P., Meseguer, J.: The HOL/NuPRl proof translator—
     A practical approach to formal interoperability. In: Proc. 14th Intl. Conf. on
     Theorem Proving In Higher Order Logics (TPHOL’2001) Edinburgh, Scotland,
     September 2001. pp. 329–345. Springer LNCS 2152 (2001)
110. Sun, M., Meseguer, J.: Distributed real-time emulation of formally-defined pat-
     terns for safe medical device control. In: Ölveczky [92], pp. 158–177, http:
     //dx.doi.org/10.4204/EPTCS.36.9
111. Sun, M., Meseguer, J.: Formal specification of button-related fault-tolerance mi-
     cropatterns. In: Rewriting Logic and Its Applications - 10th International Work-
     shop, WRLA 2014, Held as a Satellite Event of ETAPS, Grenoble, France, April
     5-6, 2014, Revised Selected Papers. Lecture Notes in Computer Science, vol. 8663,
     pp. 263–279. Springer (2014)
112. Sun, M., Meseguer, J., Sha, L.: A formal pattern architecture for safe medical
     systems. In: Proc. WRLA 2010. vol. 6381, pp. 157–173. Springer LNCS (2010)
113. Tang, S.: Towards Secure Web Browsing. Ph.D. thesis, University of Illinois at
     Urbana-Champaign (2011), 2011-05-25, http://hdl.handle.net/2142/24307
114. Verdejo, A.: Building tools for LOTOS symbolic semantics in maude. In: Formal
     Techniques for Networked and Distributed Systems - FORTE 2002, 22nd IFIP
     WG 6.1 International Conference Houston, Texas, USA, November 11-14, 2002,
     Proceedings. pp. 292–307 (2002)
115. Weghorn, T., Liu, S., Sprenger, C., Perrig, A., Basin, D.: N-tube: Formally verified
     secure bandwidth reservation in path-aware internet architectures. In: 2022 IEEE
     35th Computer Security Foundations Symposium (CSF). pp. 147–162 (2022)
32      J. Meseguer

116. Wirsing, M., Knapp, A.: A formal approach to object-oriented software engineer-
     ing. In: Meseguer, J. (ed.) Proceedings of the First International Workshop on
     Rewriting Logic and its Applications, WRLA’96, Asilomar, California, September
     3-6, 1996. Electronic Notes in Theoretical Computer Science, vol. 4, pp. 322–360.
     Elsevier (1996), http://dx.doi.org/10.1016/S1571-0661(04)00046-5
117. Wirsing, M., Knapp, A.: A formal approach to object-oriented software engineer-
     ing. Theoretical Computer Science 285(2), 519–560 (2002), http://dx.doi.org/
     10.1016/S0304-3975(01)00367-X




Open Access. This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution, and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
    The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
