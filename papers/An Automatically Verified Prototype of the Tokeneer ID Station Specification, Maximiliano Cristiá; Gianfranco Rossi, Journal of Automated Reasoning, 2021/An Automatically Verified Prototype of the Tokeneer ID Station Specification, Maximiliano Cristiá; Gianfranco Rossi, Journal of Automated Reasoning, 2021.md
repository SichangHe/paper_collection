                                        TO BE COMPLETED                                                                                                                                 1




                                                   An Automatically Verified Prototype of the
                                                       Tokeneer ID Station Specification
                                                                                     Maximiliano Cristiá and Gianfranco Rossi

                                              Abstract—The Tokeneer project was an initiative set forth by the National Security Agency (NSA, USA) to be used as a demonstration
                                              that developing highly secure systems can be made by applying rigorous methods in a cost effective manner. Altran Praxis (UK) was
                                              selected by NSA to carry out the development of the Tokeneer ID Station. The company wrote a Z specification later implemented in
                                              the SPARK Ada programming language, which was verified using the SPARK Examiner toolset. In this paper, we show that the Z
                                              specification can be easily and naturally encoded in the {log} set constraint language, thus generating a functional prototype.
arXiv:2009.00999v1 [cs.SE] 2 Sep 2020




                                              Furthermore, we show that {log}’s automated proving capabilities can discharge all the proof obligations concerning state invariants as
                                              well as important security properties. As a consequence, the prototype can be regarded as correct with respect to the verified
                                              properties. This provides empirical evidence that Z users can use {log} to generate correct prototypes from their Z specifications. In
                                              turn, these prototypes enable or simplify some verification activities discussed in the paper.

                                              Index Terms—Tokeneer ID Station specification, Z notation, {log}, constraint programming, prototyping.

                                                                                                                   ✦



                                        1    I NTRODUCTION                                                             effective (i.e., they are not more expensive than traditional
                                                                                                                       development processes) [6], [7].
                                        F    ORMAL methods (FM) are still questioned with respect
                                             to their actual value to deliver software at a reasonable
                                        cost. Formal methods researchers and practitioners have
                                                                                                                           Altran Praxis applied its own Correctness by Construc-
                                                                                                                       tion development process to the TIS software. The second
                                                                                                                       phase of this development process consists in writing a Z
                                        proved many times that formal methods can deliver soft-
                                                                                                                       [8], [9] formal specification of the user requirements. The
                                        ware of unmatched quality, e.g. [1], [2]. The FM community
                                                                                                                       Z specification is central to the development process as
                                        has also shown that high quality is not an impediment to
                                                                                                                       it is used as the correctness criteria for many verification
                                        keep costs low when total cost of ownership and critical
                                                                                                                       activities.
                                        systems are considered [3], [4]. However, most of the soft-
                                                                                                                           The work described in this paper starts from this Z
                                        ware industry is still reluctant to apply FM, and frequently
                                                                                                                       specification. More precisely, we first encode the Z speci-
                                        is unaware of their possible value. Even critical software
                                                                                                                       fication in the {log} set constraint programming language
                                        providers do not always apply FM and are not obligated
                                                                                                                       [10], [11], [12]. This provides a functional prototype of the
                                        to do so as standards do not always mandate a formal
                                                                                                                       Z specification. We say ‘encode’ and not ‘implement’ due
                                        approach, e.g. IEC 61508 Safety Integrity Level 4.
                                                                                                                       to the close resemblance between the {log} language and
                                            In this context the National Security Agency (NSA) of the
                                                                                                                       Z; however, the encoding provides an implementation in
                                        U.S.A. conducted a project aiming at providing evidence to
                                                                                                                       the form of a prototype. In a second step, we use {log}’s
                                        software vendors that formal techniques can deliver high
                                                                                                                       constraint solving capabilities to automatically prove that
                                        quality software in time and within budget. In particular
                                                                                                                       the prototype verifies all the state invariants defined in the
                                        NSA chose the Tokeneer ID Station (TIS) which makes part
                                                                                                                       Z specification as well as all but one of the security prop-
                                        of the Tokeneer system. Tokeneer provides protection to
                                                                                                                       erties stated by Altran Praxis team—this amounts to dis-
                                        secure information held on a network of workstations sit-
                                                                                                                       charge 523 proof obligations. This constitutes a step forward
                                        uated in a physically secure enclave. TIS, in turn, is a stand-
                                                                                                                       with respect to the original project as these invariants and
                                        alone trusted entity responsible for performing biometric
                                                                                                                       properties were not machine-checked by Altran Praxis at
                                        verification of the user. NSA asked Altran Praxis (then
                                                                                                                       the specification level. Besides, this implies that the {log}
                                        Praxis Critical Systems) to provide an implementation of
                                                                                                                       program is an automatically verified functional prototype
                                        TIS conforming to Common Criteria’s EAL5-level [5] and to
                                                                                                                       of the Z specification. This provides empirical evidence that
                                        disclose to the public domain all the deliverables produced
                                                                                                                       Z users can use {log} to generate correct prototypes from
                                        during system development. As said, the ultimate goal of
                                                                                                                       their Z specifications. The paper discusses some verification
                                        NSA was to show that this kind of development efforts
                                                                                                                       activities that can be carried out or simplified once the {log}
                                        are feasible (i.e., they achieve reliable software) and cost-
                                                                                                                       prototype is available.
                                                                                                                           The present work aims at providing more empirical
                                        •   M. Cristiá is with Universidad Nacional de Rosario and CIFASIS, Ar-       evidence that FM-based tools such as {log} can effectively
                                            gentina.
                                            E-mail: cristia@cifasis-conicet.gov.ar                                     be used in industrial projects willing to provide high quality
                                        •   G. Rossi is with Universitá di Parma, Italy.                              software without incurring in increased costs or delayed
                                            E-mail: gianfranco.rossi@unipr.it                                          schedules.
                                        to be completed                                                                    The paper assumes the reader has some exposure to
TO BE COMPLETED                                                                                                                2

Z specification—otherwise the reader can consult any Z             As we will show, introducing existentially quantified vari-
textbook, e.g. [9].                                                ables in {log} is harmless, while introducing the cardinality
    The paper is structured as follows. The Z specification of     operator is not.
the Tokeneer project is briefly introduced in Section 2, along        Z schemas are heavily used to give structure to the
with the security properties the system should enforce. {log}      main concepts formalized in the specification. For example,
is presented in Section 3 by means of examples. Section 4          Certificate is used to define:
discusses the encoding of the Z specification in {log}. Sec-
tion 5 shows how the {log} prototype is verified by running               AttCertificate
automated proofs of state invariants and security properties;             Certificate
Section 5.3 discusses some other verification activities that             baseCertId : CertificateId
can be done with the prototype. A quantitative report of                  tokenID : TOKENID
some key aspects of this endeavor is presented in Section 6.
In Section 7 we put our results in the context of other works      which in turn is used to define:
that used the Tokeneer project as a case study. In Section 8              PrivCert
we present our conclusions.                                               AttCertificate
                                                                          role : PRIVILEGE
2   T HE Z S PECIFICATION OF THE TIS                                      clearance : Clearance
The Tokeneer project carried out be Altran Praxis has been
thoroughly documented in part due to the requirements of           which is used to define a Token:
the Common Criteria [6], [13]. In this section we will focus              Token
on the Z specification generated during the project. The goal             tokenID : TOKENID
is for the reader to have an idea of the complexity and
peculiarities of the Z specification. We will not explain it              idCert : IDCert
in full in part because, precisely, encoding it in {log} can be           privCert : PrivCert
done in a completely formal manner; understanding what                    iandACert : IandACert
the specification is about is unnecessary.                                authCert : optional AuthCert
    The Z specification is a 117 pages long document con-
taining formal Z code plus informal explanatory statements            It can be said that the specification is divided into
about it [14]. There is also an 11 pages long document             two parts: the real world peripherals interacting with
stating security properties the Z specification must verify        the TIS and the TIS itself. The state of all real world
[15]. Whenever we refer to “the (Z) specification” we mean         entities is modeled with the RealWorld schema which
these two documents, unless stated differently; and by “the        is divided into two schemas, TISControlledRealWorld and
team” we mean the Altran Praxis development team that              TISMonitoredRealWorld. In total RealWorld comprises 11 state
worked out the specification.                                      variables. In turn, the TIS state is modeled in schema
    The Z specification is written in a more or less standard      IDStation which includes 12 schemas representing different
fashion. However, it starts by introducing two polymorphic         subsystems. In total IDStation declares 36 state variables.
operators working in tandem that are somewhat unusual:             The definition of IDStation follows the style of most Z
                                                                   specifications1:
    optional X == {x : F X | #x ≤ 1}
    the[X] == {x : X • {x} 7→ x}                                          IDStation
                                                                          ...
optional is used to indicate that a variable can hold a value
                                                                          DoorLatchAlarm
or nil, as for example in:
                                                                          ...
       Certificate                                                        currentDisplay : DISPLAYMESSAGE
       id : CertificateId                                                 currentScreen : Screen
       validityPeriod : P TIME
                                                                          status ∈ {gotFinger, waitingFinger, . . . } ⇒
       isValidatedBy : optional KEYPART
                                                                               ((∃ ValidToken • goodT(θValidToken) = . . . )
                                                                                    ∨ (∃ TokenWithValidAuth • . . . ))
meaning that the certificate can be validated by some (asym-              ...
metric cryptographic) key or it cannot. When the key does                 currentScreen.screenStats = displayStats(θStats)
exist and has to be retrieved from the certificate, then the the
operator comes into play; for instance:
                                                                   That is, it includes several schemas, declares two variables
    the cert.isValidatedBy = issuerCert.subjectPubK                and 8 state invariants. Note that these state invariants are
                                                                   conjoined with those declared in some of the included
Concerning the encoding of the Z specification in {log}, it is     schemas (e.g. DoorLatchAlarm). This implies a total of 13
important to note that optional can be defined as follows:         state invariants. The reader can see two of them in the
    optional X == {x : F X | x = ∅ ∨ (∃ y : X | x = {y})}          summary of the schema shown above. The first one gives
                                                                   an idea of the complexity of some of the predicates: it is a
Likely, the team opted by the first definition in an attempt to
keep the number of quantified formulas as low as possible.          1. We use ellipses to shorten the presentation.
TO BE COMPLETED                                                                                                                  3

quantified formula using Z’s θ operator. The θ operator is            This second approach has the advantage that all pre-
one of the most complex logical operators of the Z notation.      conditions are explicit making the transition to the imple-
   Some of the state variables in RealWorld and IDStation         mentation simpler, but it has the disadvantage of having to
have a non-enumerated free type, as for example:                  discharge proof obligations.
                                                                      In encoding the Z specification in {log} we opted for
    KEYBOARD ::= noKB | badKB | keyedOpshh. . .ii
                                                                  this second approach because we want the {log} prototype
which means the presence of structured infinite types.            to be closer to an implementation (than the Z specification)
    The specification defines 25 major operations plus 3          and because {log} can automatically discharge these proof
that group some of these operations (e.g. TISUserEntryOp          obligations (see Section 5).
specifying the complete authentication process)2 . All TIS op-
erations are state transitions over RealWorld and IDStation.      2.2 Security Properties
Many of these operations are assembled from simpler oper-
                                                                  The team stated 6 security properties the specification must
ation schemas by means of some non-trivial schema expres-
                                                                  verify; one of them is not formalized, so we will not consider
sions; for instance:
                                                                  it. The team provided informal proofs of these properties.
                    b StartArchiveLog ∨ . . .
    TISArchiveLogOp =                                             According to the documentation the most important of these
    StartArchiveLog =b                                            properties is Property 1; we reproduce an excerpt of it here
         (StartArchiveLogOK o9 UpdateFloppy)                      for the reader to have an idea of its complexity:
         ∨ StartArchiveLogWaitingFloppy                               ∆IDStation; ∆RealWorld |
         ∨ [ BadAdminLogout | . . . ]                                    TISOpThenUpdate
    There is a particularly important operation schema,                  ∧ latch = locked ∧ latch′ = unlocked
namely TISProcessing, specifying the overall processing ac-           ⊢
tivity of the TIS because it is used to state some important             (∃ ValidToken • goodT(θValidToken) = . . .
security properties as we will see. TISProcessing “calls” 20                  ∧ UserTokenOKNoCurrCheck
TIS operations and updates the audit log:                                     ∧ FingerOK)
                                                                         ∨
    TISProcessing = b                                                    (∃ TokenWithValidAuth • goodT(. . . ) = . . .
        (· · · ∨ TISUserEntryOp ∨ · · · ∨ TISAdminOp ∨ . . . )                ∧ UserTokenWithOKAuthCertNoCurrCheck)
        ∧ LogChange                                                      ∨
                                                                         (∃ ValidToken • goodT(θValidToken) = . . .
2.1 State Invariants                                                          ∧ authCert 6= ∅ ∧ (the authCert).role = guard)
The specification follows the Z style concerning the en-
coding of state invariants. This means that state invari-         where:
ants are declared in the predicate part of the state schema           TISOpThenUpdate =
                                                                                      b TISProcessing o9 TISUpdate
(i.e., IDStation). Including the state invariants in the state
schema implies that all operations trivially verify them. We      That is, the property must be proved for 20 of the TIS
exemplify this with a simple example not taken from the           operations, followed by the TISUpdate operation.
specification.                                                        It is important to remark that the above formula does
                                                                  not really correspond to the property the team would have
          b [x : Z | 0 ≤ x ]
    State =                                                       wanted to prove—we call it the intended property. This is
       b [∆State | x′ = x − 1]
    Op =                                                          acknowledged by team in the technical documentation [15,
                                                                  page 11, ‘Note on arguments’]. The formula formalizing the
Op cannot violate the state invariant (0 ≤ x) because the
                                                                  intended property cannot be expressed in the Z notation.
state invariant is part of Op’ definition:
                                                                  Indeed, that formula would have to predicate over (infinite)
    [∆State | x′ = x − 1]                                         sequences of states instead of pairs of states as stated by the
    ≡ [x , x ′ : Z | 0 ≤ x ∧ x ′ = x − 1 ∧ 0 ≤ x ′ ]              semantics of the Z notation [16], [17]. It is easy to observe
                                                                  that TIS is actually a reactive system perhaps making Z not
So Op cannot be called when x = 0 because Op’s predicate
                                                                  the best notation to specify it.
implies 0 < x. This is called implicit precondition and raises
                                                                      We remark this point because we make an extra effort to
due to the interaction between the state invariant and the
                                                                  overcome this limitation when proving the validity of Prop-
operation predicate.
                                                                  erty 1 for the {log} prototype (see Section 5.2.1). Hence, we
    Another approach concerning state invariants is to prove
                                                                  end up producing not only a mechanized (automated) proof
that each operation verifies them. In this case the state
                                                                  of Property 1 but also we produce proofs of several other
invariant is not encoded in the state schema, preconditions
                                                                  properties that together provide much stronger arguments
are explicitly stated and a proof obligation is introduced:
                                                                  that the intended property actually holds.
    State =
          b [x : Z ]
        b [State | 0 ≤ x]
    Inv =                                                         3   T HE {log} C ONSTRAINT S OLVER
                                 ′                                {log} is a public available satisfiability solver and a
       b [∆State | 0 < x ∧ x = x − 1]
    Op =
    proof obligation Inv ∧ Op ⇒ Inv        ′                      set-based, constraint-based programming language imple-
                                                                  mented in Prolog [12]. {log} implements a decision pro-
 2. These are the operation schemas whose names begin with TIS.   cedure for the theory of hereditarily finite sets, i.e., finitely
TO BE COMPLETED                                                                                                                         4

nested sets that are finite at each level of nesting [10]; a deci-       Being a satisfiability solver, {log} can be used as an auto-
sion procedure for a very expressive fragment of the class of        mated theorem prover. To prove that formula φ is a theorem,
finite set relation algebras [11], [18]; a decision procedure for    {log} has to be called to prove that ¬ φ is unsatisfiable.
restricted intensional sets (RIS) [19], [20]; and uses Prolog’s
                                                                     Example 2. We can prove that set union is commutative by
CLP(Q) to provide a decision procedure for integer linear
                                                                        asking {log} to prove the following is unsatisfiable:
arithmetic [21]. In {log} sets and binary relations are first-
class entities of the language. At the core of these decision                un(A, B, C) & un(B, A, D) & C neq D.
procedures is set unification [22]. The set terms defined
in all these three decision procedures can be combined in               As there are no sets satisfying this formula {log} answers
several ways: binary relations are hereditarily finite sets             no. Note that the formula can also be written with the
whose elements are ordered pairs and so set operators can               nun constraint: un(A, B, C) & nun(B, A, C).
take binary relations as arguments; RIS can be passed as
arguments to set operators and freely combined with exten-               {log} is also a programming language at the intersection
sional sets. {log} is an untyped formalism; variables are not        of declarative programming, set programming [25] and
declared; typing information can be encoded by means of              constraint programming. {log} programs can be structured
constraints. Several in-depth empirical evaluations provide          by means of clauses—as in Prolog. A clause can be seen
evidence that {log} is able to solve non-trivial problems            as a subroutine or procedure. Clauses can receive zero or
[11], [18], [19], [20], [23], in particular as an automated          more arguments. The only way a clause can return a value
verifier of security properties [24]. Given that {log} has           is by means of one or more of its arguments. Under certain
been extensively described elsewhere, in this section we will        conditions clauses behave as formulas. That is a {log} clause
show a few examples for the reader to understand how it              can be seen as both a program and a formula. The following
works.                                                               examples show the formula-program duality of {log} code
    In {log} set operators are encoded as constraints. For           along with the notion of clause.
example: un(A, B, C) is a constraint interpreted as C = A ∪ B.       Example 3. If we want a program that updates function F
{log} implements a wide range of set and relational opera-              in X with value Y provided X belongs to the domain of
tors covering most of those used in Z. For instance, in is              F and get an error otherwise, the {log} code can be the
a constraint interpreted as set membership (i.e., ∈); = is set          following:
equality; dom(F, D) corresponds to dom F = D; subset(A, B)
corresponds to A ⊆ B; comp(R, S, T) is interpreted as                        update(F, X, Y, F , Error) :-
T = R o9 S (i.e., relational composition); and apply(F, X, Y)                  F = {[X, V ]/F1} & [X, V ] nin F1 &
is equivalent to pfun(F) & [X, Y] in F, where pfun(F)                          F = {[X, Y]/F1} &
constrains F to be a (partial) function. Formulas in {log} are
                                                                               Error = ok
conjunctions (&) and disjunctions (or) of constraints; they
must finish with a dot (as a Prolog query). Negation in {log}                  or
is introduced by means of so-called negated constraints. For                   comp({[X, X]}, F, {}) &
example nun(A, B, C) is interpreted as C 6= A ∪ B and nin                      Error = err.
corresponds to ∈   / —in general, a constraint beginning with
‘n’ identifies a negated constraint. For formulas to lay inside         That is, update is a clause that receives F, X and Y and
the decision procedures implemented in {log}, users must                returns the modified F in F and the error code in Error—
only use this form of negation.                                         think of F as the value of F in the next state. As &
    The fact that set operators take a relational rather than a         and or are logical connectives and = is logical equality,
functional form makes it necessary to introduce variables to            the order of the ‘instructions’ is irrelevant w.r.t. the
write compound expressions.                                             functional result—although it can have an impact on the
                                                                        performance. Variable F1 is an existentially quantified
Example 1. The Z expression x ∈ A ∩ B ∩ C is encoded as                 variable representing the ‘rest’ of F w.r.t. to [X, V ]. If
   X in M & inters(A, B, W ) & inters(W , C, M).                        [X, V ] does not belong to F then the unification between F
                                                                        and {[X, V ]/F1} will fail thus making update to execute
Set terms can be of the following forms:                                the other branch.
                                                                        Now we can call update by providing inputs and waiting
   •   A variable is a set term; variable names must start              for outputs:
       with an uppercase letter.
   •   {} is the term interpreted as the empty set.                          update({[setlog, 5], [hello, earth], [tokeneer, model]},
   •   {x/A} is called extensional set and is interpreted as                         hello, world, G, E).
       {x} ∪ A; A must be a set term, x can be any term ac-
       cepted by {log} (basically, any Prolog uninterpreted             returns:
       symbol, integers, lists, ordered pairs, etc.).
                                                                             G = {[hello, world], [setlog, 5], [tokeneer, model]}
   •   ris(X in A, φ) is called restricted intensional set (RIS)
       and is interpreted as {x : x ∈ A ∧ φ} where φ is any                  E = ok
       {log} formula; A must be a set term and X is a bound
       variable local to the RIS. Actually, RIS have a more             Since update is also a formula we can prove properties
       complex and expressive structure [19], [20].                  true of it.
TO BE COMPLETED                                                                                                                   5

Example 4. If Error is equal to err then X does not belong to       Given that {x : x ∈ A ∧ φ} is the interpretation of ris(X in
   the domain of F. In order to prove this property we need         A, φ), the r.h.s. of (1) can be expressed as the {log} formula:
   to call {log} on its negation:
                                                                            subset(A, ris(X in A, φ))
        update(F, X, Y, F , err) & dom(F, D) & X in D.
                                                                    In {log} we have defined the foreach constraint to make
   Then, {log} answers no because the formula is unsatisfi-         RUQ easier to write:
   able.
                                                                            foreach(X in A, φ) :- subset(A, ris(X in A, φ)).
    As Example 3 shows, variables introduced in the clause
body (e.g. F1) are existentially quantified variables. This            We use these features to encode the Z specification
is important because of the way existentially quantified            in {log}, to automatically prove invariance lemmas and
formulas of the Z specification are encoded in {log}.               properties, and to provide a correct prototype of the Z
    {log} implements set unification but syntactic Prolog           specification in the form of a {log} program.
unification is still available as part of it. Prolog unification
comes handy to encode some Z features and predicates.
Example 5. The ‘dot’ notation used in Z to access compo-            4   E NCODING THE TIS S PECIFICATION IN {log}
   nents of ordered pairs and variables of schema types, can        In the introduction, we say ‘encoding’ and not ‘imple-
   be encoded by means of Prolog unification. For instance          menting’ the TIS specification due to the close resemblance
   if x : A × B, then the Z expression: h = x.1 can be encoded      between the Z and {log} languages. That is, our point is that
   as X = [X1, X2] & H = X1 or even as X = [H , X2].                writing {log} code from the specification is considerably
   Further, since X2 seems to be uninteresting yet another
                                                                    more natural, evident and semantically equivalent than
   encoding is X = [H , ].
                                                                    writing, say, SPARK code. Then, it looks like more as an
Example 6. A more elaborated example is the encoding of             encoding than as an implementation. In particular, {log}
   the Z predicate x ∈ dom f as [X, ] inF. Indeed, [X, ] inF is     implements all the logical, set and relational operators used
   readily rewritten as F = {[X, ]/F1} which is interpreted         in the TIS specification. Furthermore, these operators are
   as ‘there is a pair in F whose first component is X’, which      not mere imperative implementations but real executable
   in turn means that X belongs to the domain of F. A               mathematical definitions. That is, they behave as logical or
   more direct encoding is dom(F, D) & X in D but it                mathematical objects, as we have shown in Section 3. In
   requires to compute the domain while the first encoding          other words, the {log} prototype is a formula quite as the
   does not, meaning that the first encoding will, in general,      TIS specification is. We say ‘quite’ because of two reasons:
   yield more efficient {log} code. Yet another encoding is
                                                                        •     The {log} code can be used to compute results. Then,
   ncomp({[X, X]}, F, {}) which uses the negated constraint
                                                                              {log} programmers may pay attention to implemen-
   of the comp constraint. That is, ncomp({[X, X]}, F, {}) is
                                                                              tation issues, such as efficiency.
   equivalent to comp({[X, X]}, F, F1) & F1 neq {}, which
                                                                        •     For different programming reasons (e.g. use of Pro-
   is a fourth encoding.
                                                                              log and set unification) we introduce some modifica-
    As can be seen, frequently, unification introduces exis-                  tions in the {log} code w.r.t. the specification.
tentially quantified variables. In many circumstances these
quantified formulas can be dealt with in a decidable manner         This takes the discussion to another issue: the {log} code is a
[10], [11], [18], [19], [20]. A key aspect to preserve decidabil-   prototype and not a program. Hence, users cannot expect the
ity is not to use logical negation but the negated constraints      same computing efficiency from the {log} code than from a
provided by {log}.                                                  typical imperative implementation. For instance, engineers
                                                                    can use the prototype to analyze functional scenarios but
Example 7. Concerning formula x ∈ dom f of Example 6, the           they cannot draw efficiency estimations. This section will
   encoding of its negation, x 6∈ dom f , in {log} cannot be        make these points clear.
   done simply with a formula such as ∀ Y : [X, Y] nin F
                                                                        The {log} encoding of the TIS specification as well
   because this formula is outside the set of admissible
                                                                    as all the proof obligations can be found online:
   {log} formulas. Conversely, the decidable way to handle
                                                                    http://people.dmi.unipr.it/gianfranco.rossi/SETLOG/
   this negation is either: dom(F, D) & X nin D; or
                                                                    APPLICATIONS/tokeneer.zip.
   comp({[X, X]}, F, {}).
                                                                        In general, each Z schema is encoded as a {log} clause.
    The last example opens the issue of universal quanti-           The variables declared in the schema become arguments
fiers in {log}. In {log} universally quantified formulas are        of the clause. In many cases, if the schema declares vari-
provided by mean of RIS. In effect, the introduction of             ables through schema inclusion then the arguments of the
RIS in {log} allows for the definition of restricted universal      clause are those schemas instead of the variables declared
quantifiers (RUQ). In general, if A is a set, then a RUQ is a       inside them. This somewhat preserves the structure of the
formula of the following form:                                      specification. Schemas whose predicate part is empty are
                                                                    encoded as tuples of variables. We preserved the identifiers
    ∀x ∈ A : φ                                                      used in the specification as much as possible in the {log}
It is easy to prove the following:                                  code. Recall that {log} variables (constants) must start with
                                                                    an uppercase (lowercase) letter; while clauses can start only
    (∀ x ∈ A : φ) ⇔ A ⊆ {x : x ∈ A ∧ φ}                       (1)   with a lowercase letter. Next state variables (e.g. x′ ) are
TO BE COMPLETED                                                                                                                   6

encoded as {log} variables decorated with an underscore              making CurrentUserToken = goodT(_) superfluous—
(e.g. X )3 .                                                         actually, we included it to make the encoding more simi-
    Figures 1 and 2 show parts of the encoding. In Figure            lar to the specification. Finally, the last three existentially
1 the specification is at the left and the corresponding             quantified predicates are encoded along the same lines.
encoding in {log}, at the right. We attempted to align each          That is, the encoding of schema CertOK is called on each
row of the specification with the corresponding row in {log}.        certificate contained in the Token. Note that, for instance,
In Figure 2 the specification is at the top and the encoding at      (∃ IDCert . . . ) corresponds to variable IDC; thus θIDCert =
the bottom. In general, the encoding in {log} is longer than         idCert corresponds to IDC = [[Id,VP,IVB],[_,_]];
the corresponding Z code, as is expected for any lower-level         and [Id,VP,IVB] is the Certificate passed in as argument
representation, but not that much (see Section 6).                   to certOK.
    Consider Figure 1. As can be seen, schema CurrentToken               Now consider Figure 2. Schema BioCheckRequired spec-
is encoded as clause currentToken. CurrentToken declares             ifies part of the ValidateUserTokenOK operation which
several variables through the inclusion of schema ValidToken         in turn is part of the TISValidateUserToken operation.
which in turns declares those variables through the inclu-           BioCheckRequired makes a ‘delta’ on IDStation and RealWorld;
sion of schema Token. Then, in this case currentToken                this is hidden in schema UserEntryContext. This is reflected
has two arguments: Token, corresponding to schema Token;             in the encoding as clause bioCheckRequired waits for
and Now, corresponding to variable now. In order to make             IDStation and IDStation_, meaning that the clause
Token a valid one, validToken(Token) is conjoined.                   transitions from the former to the latter. As explained in
As expected, validToken is the encoding of schema                    Section 2, IDStation includes 12 schemas and declares two
ValidToken (not shown). In the specification TIME is a syn-          variables. Then, the encoding for IDStation is a 14-tuple
onym for N, so Now is constrained to be a non-negative               respecting the declaration order given in the specification.
integer by asserting 0 =< Now. Given that Token is a                 As mentioned in Section 2.1, the invariants stated inside
schema declaring five variables it is encoded as a 5-tuple:          IDStation are moved out of it; see Section 5 for further
Token = [_,IDC,PC,IAC,_] where the correspondence                    details. Note that IDStation′ is encoded as IDStation_.
between Z and {log} variables is implemented by decla-                   As BioCheckRequired states ΞUserToken the encoding
ration order. Thus, PC corresponds to the third variable             forces UserToken and UserToken_ to be the first ele-
declared in Token, i.e., privCert. In currentToken only IDC,         ments of IDStation and IDStation_, respectively, while
PC and IAC play some role, so the other two are hidden by            UserToken_ = UserToken is conjoined to the clause.
putting underscores in their positions. The named variables              AddElementsToLog is an operation schema making a
can have any name because they are existentially quantified          ‘delta‘ on the auditing subsystem, AudiLog, and accessing
inside the clause. Besides, Token = [_,IDC,PC,IAC,_]                 the configuration subsystem, Config. In {log} this schema
forces the unification of the actual argument to be a 5-tuple;       corresponds to clause addElementsToLog. The clause is
in case this is not true the clause will fail. The specifica-        called inside a delay predicate for efficiency reasons. After
tion variables corresponding to IDC, PC and IAC are of               the first proof obligations were discharged it was evident
schema types (e.g. privCert : PrivCert, see Section 2), so they      that addElementsToLog was taking too long while not
are encoded as tuples, e.g. PC = [_,PVP,_,_,_,_,_].                  contributing to the proofs. Hence, we ask {log} to delay its
In this particular case PVP corresponds to the Z expres-             execution as much as possible. AddElementsToLog’s predicate
sion privCert.validityPeriod (recall Example 5). Therefore, the      starts by asserting the existence of a finite set of audit
predicate stated in CurrentToken is encoded as shown in              records, newElements. The {log} encoding reflects that fact
Example 1.                                                           by declaring variable _NewElements inside the clause and
    Still in Figure 1, UserTokenOK’s predicate is based on a         passing it to addElementsToLog. This simplifies the en-
quantified schema expression using the θ operator. The type          coding of some tricky parts of the specification.
of currentUserToken is:                                                  In BioCheckRequired, status is a variable declared in
                                                                     schema Internal (which is one of the 12 schemas included
    TOKENTRY ::= noT | badT | goodThhTokenii                         in IDStation). The encoding uses unification to access the
Then, currentUserToken ∈ ran goodT means that the current            corresponding variable, Status. Indeed, unification forces
user token is indeed a Token. That is, the predicate is              Internal to be the 12th component of IDStation and it
equivalent to ∃ t : Token • currentUserToken = goodT(t).             is used again to force Status to be the first component of
Avoiding quantified formulas is important but the encoding           Internal. Then, we can state Status = gotUserToken.
can introduce an existentially quantified variable without           Note how the change of state of status is encoded by assert-
getting into troubles: CurrentUserToken = goodT(_).                  ing Status_ = waitingFinger.
Along the same lines, the predicate (∃ CurrentToken •                    The predicate ¬ UserTokenWithOKAuthCert is encoded
. . . ) is easily encoded with currentToken(Token,Now);              by calling the negation of userTokenWithOK AuthCert.
that is, by asserting the existence of variables Token               As explained in Section 3 (see Example 7), in or-
and Now satisfying currentToken. Then, θValidToken                   der to preserve decidability (general) logical negation
refers to the Token asserted in (∃ CurrentToken • . . . ).           should not be used. Instead, the negation has to be
So, goodT(Token) = CurrentUserToken is asserted in                   written in terms of {log} constraints. Given that Fig-
{log}. This implies that goodT(_) = goodT(Token), thus               ure 1 includes the encoding of UserTokenOK, Figure 3
                                                                     shows the encoding of ¬ UserTokenOK (in place of
  3. The prime symbol is not allowed as part of a variable name in   ¬ UserTokenWithOKAuthCert, which is nonetheless similar).
Prolog+{log}.                                                        There are several reasons for which the user token is not
TO BE COMPLETED                                                                                                                         7



         CurrentToken                                                         currentToken(Token,Now) :-
                                                                                Token = [_,IDC,PC,IAC,_] &
                                                                                  IDC = [[_,VP,_],[_,_]] &
                                                                                  PC = [_,PVP,_,_,_,_,_] &
                                                                                  IAC = [_,IVP,_,_,_,_] &

         ValidToken                                                              validToken(Token) &
         now : TIME                                                              0 =< Now &

         now ∈ idCert.validityPeriod                                             Now in M2 &
             ∩ privCert.validityPeriod                                             inters(VP,PVP,M1) &
             ∩ iandACert.validityPeriod                                            inters(M1,IVP,M2).


         UserTokenOK                                                          userTokenOK(
         KeyStore                                                                 KeyStore,
         UserToken                                                                UserToken,CurrentTime,Now) :-
         currentTime : TIME                                                     0 =< CurrentTime &
                                                                                UserToken = [CurrentUserToken,_] &

         currentUserToken ∈ ran goodT                                            CurrentUserToken = goodT(_) &

         ∃ CurrentToken •                                                        currentToken(Token,Now) &
                                                                                   Token = [_,IDC,PC,IAC,_] &
                                                                                     IDC = [[Id,VP,IVB],[_,_]] &
                                                                                     PC = [PCId,PCVP,PCIVB,_,_,_,_] &
                                                                                     IAC = [IAId,IAVP,IAIVB,_,_,_] &

               (goodT(θValidToken) = currentUserToken                                goodT(Token) = CurrentUserToken &
               ∧ now = currentTime                                                   Now = CurrentTime &
               ∧ (∃ IDCert • θIDCert = idCert ∧ CertOK)                              certOK(KeyStore,[Id,VP,IVB]) &
               ∧ (∃ PrivCert • θPrivCert = privCert ∧ CertOK)                        certOK(KeyStore,[PCId,PCVP,PCIVB]) &
               ∧ (∃ IandACert •                                                      certOK(KeyStore,[IAId,IAVP,IAIVB]).
                        θIandACert = iandACert ∧ CertOK))



Fig. 1. Comparison between Z code and {log} code (part 1). Similarities are not only syntactic but semantic as well.


OK. The first one occurs when the current user token                       4.1 Potential Problems with the Encoding
does not belong to the range of goodT. This implies that
it must be either noT or badT (see TOKENTRY above).                        In spite of the similarities between Z and {log}, in passing
The encoding is CurrentUserToken in {noT, badT}.                           from the specification to the prototype several changes were
The other cases occur when there is a token : Token                        introduced. We claim that, still, the prototype is a faithful
such that currentUserToken = goodT(token). In this                         representation of the specification as it is possible to prove
case, (token, now) might not conform a current to-                         that the former verifies essential properties of the latter—
ken (not_currentToken(Token,Now)); or now might                            see Section 5. However, some of the changes might cause
not coincide with currentTime (Now neq CurrentTime);                       troubles when proving new properties. In this section we
or any of the certificates stored in token is not OK                       give a brief account of these differences.
(not_certOK(KeyStore,[_,_,_])).                                                Types are not always encoded. Z is a typed formalism, {log}
                                                                           is not. Typing information can be encoded using set mem-
                                                                           bership and constraints such as pfun. We encoded the typ-
    To close this section, note that the {log} encoding of                 ing information needed to prove the properties discussed
ValidateUserTokenOK turns out to be quite ’natural’ (both,                 in Section 5. Some typing information is given as state
syntactically and semantically). This encoding becomes sort                invariants—as is nonetheless the case when, for instance,
of a pattern by means of which most of the Z specification                 a set is implemented as a list. The encoding assumes the
is encoded. Considering the size and complexity of the TIS                 Z specification has been type-checked. Then, the encoding
Z specification, it can be argued that {log} can be used as                needs to check only the types of input values and the initial
an effecitive prototyping/programming language to encode                   state. It would be possible to provide a type-checker for
many other Z specifications.                                               {log} programs based on special-purpose typing constraints.
TO BE COMPLETED                                                                                                        8




        BioCheckRequired
        UserEntryContext
        ΞUserToken
        ΞDoorLatchAlarm
        ΞStats
        AddElementsToLog
        status = gotUserToken
        userTokenPresence = present
        ¬ UserTokenWithOKAuthCert ∧ UserTokenOK
        currentDisplay′ = insertFinger
        status′ = waitingFinger


                         b BioCheckRequired ∨ BioCheckNotRequired
     ValidateUserTokenOK =
   bioCheckRequired(IDStation,RealWorld,RealWorld_,IDStation_) :-
     IDStation = [UserToken,_,_,DoorLatchAlarm,_,_,Config,Stats,
                  KeyStore,_,AuditLog,Internal,_,CurrentScreen] &
       UserToken = [_,UserTokenPresence] & DoorLatchAlarm = [CurrentTime,_,_,_,_,_] &
       Internal = [Status,_,_] & CurrentScreen = [ScreenStats,_,ScreenConfig] &
     RealWorld = [_,TISMonitoredRealWorld] &
       TISMonitoredRealWorld = [Now,_,_,_,_,_,_] &
     IDStation_ = [UserToken_,_,_,DoorLatchAlarm_,_,_,_,Stats_,
                 _,_,AuditLog_,Internal_,CurrentDisplay_,CurrentScreen_] &
       Internal_ = [Status_,_,_] & CurrentScreen_ = [ScreenStats_,_,ScreenConfig_] &

      userEntryContext(IDStation,RealWorld,RealWorld_,IDStation_) &

      UserToken_ = UserToken &
      DoorLatchAlarm_ = DoorLatchAlarm &
      Stats_ = Stats &

      delay(addElementsToLog(Config,_NewElements,AuditLog,AuditLog_),false) &

      Status = gotUserToken &
      UserTokenPresence = present &

      delay(not_userTokenWithOKAuthCert(KeyStore,UserToken,CurrentTime),false) &
        userTokenOK(KeyStore,UserToken,CurrentTime,Now) &

      CurrentDisplay_ = insertFinger &
      Status_ = waitingFinger &

      ScreenStats_ = ScreenStats &
      ScreenConfig_ = ScreenConfig.

   validateUserTokenOK(IDStation,RealWorld,RealWorld_,IDStation_) :-
     bioCheckRequired(IDStation,RealWorld,RealWorld_,IDStation_)
     or
     bioCheckNotRequired(IDStation,RealWorld,RealWorld_,IDStation_).

Fig. 2. Comparison between Z code and {log} code (part 2). Similarities are not only syntactic but semantic as well.
TO BE COMPLETED                                                                                                                    9

not_userTokenOK(KeyStore,UserToken,                                 when all the operands remain variable. We were able to
                CurrentTime,Now) :-                                 circumvent this issue by enclosing its encoding inside a
  UserToken = [CurrentUserToken,_] &                                delay predicate.

   (CurrentUserToken in {noT, badT}                                     As the empirical data shows (Section 5), these issues do
    or                                                              not threaten the chances of using {log} as a verification tool
    CurrentUserToken = goodT(Token) &                               for industrial-strength Z specifications.
      Token = [_,IDC,PC,IAC,_] &
         IDC = [[Id,VP,IVB],[_,_]] &
         PC = [PCId,PCVP,PCIVB,_,_,_,_] &
         IAC = [IAId,IAVP,IAIVB,_,_,_] &                            5   A V ERIFIED P ROTOTYPE
    (not_currentToken(Token,Now)
      or                                                            Now that we have the {log} program, we can use {log}
      Now neq CurrentTime                                           to prove properties of it. We automatically prove two kinds
      or                                                            of properties: invariance lemmas and security properties. In
      not_certOK(KeyStore,[Id,VP,IVB])                              any case, recall that {log} can prove a theorem by proving
      or                                                            that its negation is unsatisfiable. If the theorem is of the
      not_certOK(KeyStore,[PCId,PCVP,PCIVB])                        form p ⇒ q, then one should ask {log} to check if p ∧ ¬ q is
      or                                                            unsatisfiable. In doing so consider that: a) the negation in ¬ q
      not_certOK(KeyStore,[IAId,IAVP,IAIVB])                        should be encoded as indicated in Sections 3 and 4; and b) if
    )                                                               p ∧ ¬ q happens to be satisfiable, {log} will produce a finite
   ).                                                               representation of all the possible solutions (countermodels
                                                                    or counterexamples). This last feature comes handy to find
Fig. 3. Encoding of ¬ UserTokenOK                                   out what are the possible causes for the formula not to be a
                                                                    theorem.
                                                                        Section 6 provides quantitative figures about the verifi-
    Elements beyond {log}’s expressiveness. There are a few ele-    cation work carried out with {log}.
ments in the specification that are beyond the expressiveness
of {log}. Schema types cannot be encoded as sets of records.
In this particular specification this feature is used only once
                                                                    5.1 Invariance Lemmas
and can be circumvented. Free types declaring non-constant
elements (e.g. TOKENTRY above) cannot be encoded as sets.           As explained in Section 2.1, we move the state invariants
However, it is possible to assert that a variable is of that type   included in schema IDStation out of it; this includes all the
(e.g. userTokenOK and not_userTokenOK), and that all                state invariants written in the schemas included in IDStation.
the elements of a set are of that type by means of the foreach      In doing so, we must: a) add pre- or post-conditions to some
constraint; not needed in this specification. {log} cannot          operations; and b) prove that each TIS operation preserves
express N nor Z. It can express that a variable belongs to          each invariant.
them and that all the elements of a set belong to them (this            Concerning a), for instance, the encoding of UnlockDoor
is used to encode the type of sizeElement). For this reason,        is augmented with the following conditions:
we cannot encode the type of authPeriod and some values
given in InitConfig. It is doubtful how these values can be         unlockDoor(DoorLatchAlarm,Config,
implemented in any programming language as they entail                          DoorLatchAlarm_) :-
to store a Cartesian product where one of the sets is N.            ......
    Predicate outside the decision procedure. The universally         (LatchUnlockDuration neq 0 &
quantified predicate in schema ValidEnrol (not included for            CurrentLatch_ = unlocked &
brevity) lays outside the decision procedures implemented              DoorAlarm_ = silent
in {log}—and evidence suggests that this is a fundamental              or
problem [11], [26]. The problem is that the property asserted          LatchUnlockDuration = 0 &
for all elements in issuerCerts depends on issuerCerts itself.         CurrentLatch_ = locked &
In other words, for each element in issuerCerts there must             (AlarmSilentDuration neq 0 &
exist another element in it fulfilling a certain property.               DoorAlarm_ = silent
This creates a sort of recursive definition. However, the                or
predicate can be encoded and it can be used for running the              AlarmSilentDuration = 0 &
prototype. Problems could arise if {log} is asked to decide              (CurrentDoor = open &
the satisfiability of a formula involving it, when issuerCerts            DoorAlarm_ = alarming
remains variable. In that case {log} might enter an infinite              or
loop. This is apparently not the case for the set of properties           CurrentDoor = closed &
considered in the Tokeneer project.                                       DoorAlarm_ = silent
    Computationally      hard    predicate.    The     predicate         )
oldElements ∪ auditLog′ = auditLog ∪ newElements in                    )
schema AddElementsToLog is computationally very hard                  ).
TO BE COMPLETED                                                                                                                  10

for TISUnlockDoor to preserve the invariant stated in schema     5.2 Security Properties
DoorLatchAlarm:
                                                                 All security properties formalized by the team—i.e., Prop-
                                                                 erty 1-4 and 6—are encoded in {log}. However, Property
    currentLatch = locked ⇔ currentTime ≥ latchTimeout
                                                                 2 cannot be proved by {log} because it requires a decision
    doorAlarm = alarming ⇔
                                                                 procedure for integer intervals—which is, in fact, part of our
         (currentDoor = open
                                                                 current work. Properties 3, 4 and 6 are proved as formalized
              ∧ currentLatch = locked
                                                                 by the team. For instance, the encoding of Property 3 is the
              ∧ currentTime ≥ alarmTimeout)
                                                                 following4 :
Note that the encoding of the invariant is closer to an          property3 :-
implementation based on conditional statements than the            idStationInv01(IDStation) &
Z invariant and that it takes into account other predicates        (tisEarlyUpdate(IDStation,RealWorld,
included in UnlockDoor like latchTimeout′ = currentTime +                          RealWorld_,IDStation_)
latchUnlockDuration. This would help in passing from the            or
{log} prototype to a definitive implementation.                     tisUpdate(IDStation,RealWorld,
    Concerning b), for each TIS operation we discharge a                      RealWorld_,IDStation_)
proof obligation of the form:                                      ) &
                                                                 ......
    Invariant ∧ TISOperation ⇒ Invariant′                          Latch_ = locked &
                                                                   CurrentDoor_ = open &
encoded as:                                                        CurrentTime_ >= AlarmTimeout &
                                                                   Alarm_ neq alarming.
invariant(IDStation) &
tisOperation(IDStation,RealWorld,
             RealWorld_, IDStation_) &                           5.2.1 Proving Property 1
not_invariant(IDStation_).                                       As we have explained in Section 2.2, the formalization of
where not_invariant          is   the   {log}   negation    of   Property 1 given by the team does not actually capture the
invariant.                                                       intended property. This is acknowledged by the team in the
                                                                 technical documentation. The intended property requires to
Example 8. The state invariant included in IDStation:            consider different execution sequences of the TIS operations.
                                                                 Each of these sequences takes the system from the initial
        enclaveStatus                                            state to a state where the property holds. The point made by
             ∈
             / { notEnrolled, waitingEnrol, waitingEndEnrol }    the team is that the system can follow only those sequences.
                  ⇒ ownName 6= nil                                   Therefore, we make one more step by proving that the
                                                                 system can only execute those state sequences. Once the
   is encoded as:                                                system arrives at the desired state, we prove that Property 1
                                                                 holds. Hence, the proof of Property 1 involves (automat-
idStationInv07(IDStation) :-                                     ically) discharging 16 proof obligations—11 to prove the
  IDStation =                                                    system can only execute certain state changes; 4 to prove
     [...,KeyStore,...,Internal,...] &                           that some properties hold at some of the traversed states;
     KeyStore = [_,OwnName] &                                    and 1 to prove Property 1. This proof strategy follows the
     Internal = [_,EnclaveStatus,_] &                            informal proof made by the team [15, Section 3.2.1, pages
  (EnclaveStatus in {notEnrolled,                                8-10].
                      waitingEnrol,
                                                                     Before giving details on the encoding of these proofs,
                      waitingEndEnrol}
                                                                 it should be noted that in doing them we have to add
   or
                                                                 enclaveStatus 6= waitingStartAdminOp as an hypothesis to
   OwnName neq {}
                                                                 many of the auxiliary lemmas—otherwise they do not hold.
  ).
                                                                 This is so because, without that hypothesis, TISShutdownOp
while its negation is:                                           can be executed violating some desired properties. To the
                                                                 best of our knowledge, this extra hypothesis and the prob-
not_idStationInv07(IDStation) :-                                 lems with TISShutdownOp are not mentioned in the docu-
  IDStation =                                                    mentation. Maybe this is obvious for the team and so they
    [...,KeyStore,...,Internal,...] &                            omitted it in the documentation.
    KeyStore = [_,OwnName] &                                         Figures 4 and 5 depict the state sequences that lead the
    Internal = [_,EnclaveStatus,_] &                             system to the state where Property 1 holds. Figure 6 shows
  EnclaveStatus nin {notEnrolled,                                the encoding of a lemma stating that if the system ever
                     waitingEnrol,                               reaches status = gotUserToken it is because the before state
                     waitingEndEnrol} &                          was status = quiescent—i.e., the first transition of Figure 4.
  OwnName = {}.
                                                                   4. The ellipsis replace the unification between IDStation and the
                                                                 other arguments with tuples to have access to the variables.
TO BE COMPLETED                                                                                                                 11

That is, the {log} code corresponds to the negation of the        a fluent reading knowledge of Z” [6]— the latter being not
following formula:                                                easy to find.
                                                                      A more elaborated activity would be to use the {log}
    ∆IDStation; ∆RealWorld |
                                                                  prototype as part of a model-based testing method, e.g. [27],
       TISOpThenUpdate
                                                                  [28], [29]. Let’s call P{log} and PSPARK the {log} prototype and
       ∧ enclaveStatus 6= waitingStartAdminOp
                                                                  the SPARK implementation corresponding to the Z specifi-
       ∧ status′ = gotUserToken ∧ status′ 6= status
                                                                  cation, respectively. Given a test case generated from the
    ⊢
                                                                  specification, run it on both P{log} and PSPARK and compare
       status = quiescent
                                                                  the outputs generated by each of them to decide whether
where TISOpThenUpdate is the composition between the              or not the test case has uncovered an error in PSPARK . The
disjunction of all the TIS operations and the TISUpdate           output generated by P{log} should be deemed correct as
operation [15, page 5].                                           the prototype verifies all the stated properties. Hence, if the
    We prove one such lemma for each transition shown             output generated by PSPARK does not coincide it should be
in Figures 4 and 5. In this way, the {log} prototype is           concluded that there is an error in it. Furthermore, {log}
guaranteed to follow only those state sequences when it           itself can be used as a test case generator in the context of Z
comes to the validity of Property 1.                              specifications [23].
    Next, we prove that when the system reaches some of the           Along the same line, P{log} can be used as a runtime
states depicted in Figures 4 and 5 some properties hold. For      or reference monitor of PSPARK . Reference monitors have
example, when passing from gotUserToken to waitingEntry,          been proposed as a way to control the execution of secure
the user token is checked for validity and the presence in        systems, e.g. [30], [31]. In this scenario, P{log} and PSPARK
the token of an authorization certificate is checked as well.     execute in parallel in such a way that every input sent
Figure 7 shows the encoding of this lemma. As can be              to PSPARK is also sent to P{log} . If the outputs differ an
seen, we need pfun(IssuerKey_) as an hypothesis. In Z             alarm is fired. Clearly, the control is ex post (due to the,
terms, this means that issuerKey′ is a partial function, which    possibly sensible, different execution speeds) but in some
is the type given to the variable in the specification. This      circumstances this is much better than nothing. For example,
hypothesis is proved to be a state invariant and so it can be     in case a malfunction in PSPARK allows an unauthorized
assumed without loss of generality.                               access to the enclave, the late alarm fired by P{log} would
    Finally, Property 1 itself is proved by assuming the          allow for security personnel to correct the situation before is
properties shown to be valid in the intermediate states.          too late.
    Having discharged all the proof obligations concerning            The intention behind these proposals and the mere fact
state invariants and those concerning security properties,        of using {log} is to show that {log} can be useful, and not
the {log} prototype is correct w.r.t. them. Therefore, it can     that it should replace existing tools or techniques used in
be used as a correct implementation of the specification, at      development processes such as Altran Praxis’ Correct by
least on what concerns to the proven properties.                  Construction. {log} can fill some gaps when it comes to pro-
                                                                  totyping, automated proof and counterexample generation
5.3 The Prototype as a Verification Tool                          in the context of set-based specifications.
The prototype can be used as an analysis tool taking advan-
tage of its correctness. The most natural activity is to use it   6   QUANTITATIVE R EPORT
as an implementation to evaluate how the system behaves           Besides proving all the lemmas described in Sections 5.1 and
in specific functional scenarios.                                 5.2 we prove that:
Example 9. We may want to analyze different scenarios
    when the enclave’s door is unlocked by asking {log} to            1)   Every disjunct of all the TIS operations is satisfiable.
    execute the following:                                                 This verification is important because, as operations
                                                                           act in the antecedent of lemmas, if they are unsatisfi-
DLA = [5,locked,_,_,_,_] &
                                                                           able then the lemma holds trivially. See for example
C = [10,4,_,_,_,_,_,_] &
                                                                           Property 1 in Section 2.2.
doorLatchAlarmInv(DLA) & configInv(C,100) &
                                                                      2)   The initial state satisfies all the state invariants.
unlockDoor(DLA,C,DLA_).
                                                                           This is a standard verification step when state in-
where part of the first solution is:                                       variants are involved.
DLA_ = [5,locked,unlocked,silent,9,19]                                3)   The conjunction of the negation of a schema and the
Observe that we give the before state (e.g. DLA), check                    schema itself is unsatisfiable, while those schemas
    whether it satisfies the invariants, and then run                      are independently satisfiable.
    unlockDoor waiting for the next state (DLA_). Besides,                 This applies only to those schemas whose negation
    note that the before state is only partially given (cf. the            appears either in the specification or as part of a
    underscores in DLA) which allows to analyze several                    lemma. These proofs are done to gain confidence in
    scenarios in one run.                                                  that each negation has been correctly written.
Being able to execute these scenarios in the presence of             Table 1 summarizes key quantitative measures about
the customer can help to “check that this vital step [Z           the effort involved during this work. The first measured
specification] has been achieved correctly” without needing       magnitude is effort (man-hours). It is difficult and can be
a person “with full knowledge of the problem domain and           misleading to estimate the effort needed to conduct the
TO BE COMPLETED                                                                                                                        12




                        gotUserToken           waitingFinger            gotFinger         waitingUpdateToken     waitingEntry




          quiescent     waitingEntry                                                                       waitingRemoveTokenSuccess




 waitingRemoveTokenFail


Fig. 4. Sequences of state changes leading to status = waitingRemoveTokenSuccess




           enclaveQuiescent, ∅             gotAdminToken, ∅                  enclaveQuiescent, 6= ∅        waitingStartAdminOp, 6= ∅


Fig. 5. Sequences of state changes leading to enclaveStatus = waitingStartAdminOp, rolePresent 6= ∅




   property1_01 :-
     IDStation = [_,_,_,DoorLatchAlarm,_,_,_,_,_,_,_,Internal,_,_] &
       Internal = [Status,EnclaveStatus,_] &
     EnclaveStatus = enclaveQuiescent &
     Status neq quiescent &
     tisOpThenUpdate(M,IDStation,RealWorld,RealWorld_,IDStation_) &
     IDStation_ = [_,_,_,_,_,_,_,_,_,_,_,Internal_,_,_] &
       Internal_ = [Status_,_,_] &
     Status neq Status_ & Status_ = gotUserToken.

Fig. 6. Encoding of a state change lemma




property1_09 :-
  IDStation = [_,_,_,_,_,_,_,_,_,_,_,Internal,_,_] &
     Internal = [Status,EnclaveStatus,_] &
  Status = gotUserToken & EnclaveStatus = enclaveQuiescent &
  tisOpThenUpdate(M,IDStation,RealWorld,RealWorld_,IDStation_) &
  IDStation_ = [UserToken_,_,_,_,_,_,_,_,KeyStore_,_,_,Internal_,_,_] &
     UserToken_ = [CurrentUserToken_,_] &
     Internal_ = [Status_,_,_] &
  Status_ = waitingEntry &
  (not_tokenWithValidAuth(CurrentUserToken_)
   or
   KeyStore_ = [IssuerKey_,_] &
   pfun(IssuerKey_) &
   not_userTokenWithOKAuthCertNoCurrencyCheck(KeyStore_,UserToken_,_)
  ).

Fig. 7. Encoding of a lemma stating an intermediate property
TO BE COMPLETED                                                                                                                13

work carried out with {log} because it was done on an             Gb of main memory, running Linux Ubuntu 18.04.4 (LTS)
academic environment rather than a corporate one. Nev-            64-bit with kernel 4.15.0-106-generic. {log} 4.9.6-21c over
ertheless, we think that an approximate number could help         SWI-Prolog (multi-threaded, 64 bits, version 7.6.4) was used
others. Our effort estimate for encoding the Z specification      during the experiments.
and discharging all the 523 proof obligations is between              The execution time of each collection of proof obligations
40 and 120 man-hour. It depends on the experience of              is given by T in the following {log} formula:
the engineer with Z, {log}, proof strategies and automated
                                                                  prolog_call(get_time(Ti)) &
proof. Note that the effort reported by the team to write the
                                                                  <collection proof obligations>
Z specification and conduct informal proofs is 233.5 man-
                                                                  prolog_call(get_time(Te)) &
hour [7, Appendix B, page 71, item 3000]. A more elaborated
                                                                  prolog_call(T is Te - Ti).
tool environment could further reduce our estimate.
    The next measured magnitude is size. As can be seen, the      where prolog_call is a {log} facility to access the Prolog
{log} prototype is around 30% larger than the Z specification     interpreter.
measured in lines of code (LOC), but it is more than the              The {log} code used in this work can be down-
double in terms of kilobytes. This is consistent with the         loaded from http://people.dmi.unipr.it/gianfranco.rossi/
fact that any implementation is expected to be more ver-          SETLOG/APPLICATIONS/tokeneer.zip along with instruc-
bose than the specification. This verbosity can be observed       tions to set up the environment.
in Figures 1 and 2. The {log} code for proof obligations
(lemmas) is considerably larger than the prototype, but it
                                                                  7 OTHER         WORKS        ABOUT       THE     TOKENEER
means less than 10 LOC per lemma and it contains pretty-
printing predicates to simplify proof execution. Much of the      P ROJECT
proof obligations code can be automatically generated—we          Besides members of the team in charge of the Tokeneer
did so with a few simple bash scripts but in an industrial        project, other researchers have used it as a case study, a
environment it can be done much better.                           benchmark or just as an industrial-scale problem. We will
    The last aspect we measure concerns the number of proof       comment on the most relevant ones w.r.t. our work.
obligations (523) and the time {log} spends in discharging            Rivera et al. [32] undertake the Tokeneer project in
them (851 seconds). As can be seen, most of the proof             Event-B. They use the Rodin toolset for discharging proof
obligations corresponds to invariance lemmas as well as           obligations and the EventB2Java code generator to create
the computing time to discharge them (548 seconds). Most          a Java program from the Event-B model. The TIS model
of the time is spent in proving the invariance of three TIS       consists of an abstract machine and 6 refinements. The full
operations (TISEnrolOp, TISValidateUserToken and TISPoll).        development resulted in 334 proof obligations, of which
In average, each proof obligation runs in 1.6 seconds. There      more than 90% are discharged automatically using Rodin.
are at least two possible ways to reduce the computing            These proof obligations should coincide with a subset of
time: parallelization and what we call proof programming. In      those proved with {log}. Rivera and his colleagues prove
effect, every lemma can be discharged independently of the        Properties 1, 2 and 3 with Rodin, although it is not clear
others and so each of them can be run in a different thread.      whether or not they are automatically discharged. As can
Prolog provides high-level parallelization predicates (e.g.       be seen, {log} is able to automatically discharge 100% of the
concurrent/4) that can be easily used to considerably             proof obligations. Besides, {log} produces a prototype while
reduce the computing time.                                        the Event-B approach needs to apply EventB2Java. Likely,
    Proof programming refers to the application of some           the resulting Java program will be more efficient than the
{log} control predicates (e.g. delay) to impose some or-          {log} prototype, but the former is only a program while the
der in the execution of constraints. As we have shown in          latter is a program and a formula. Although it is not exactly
Section 5, enclosing a constraint in a delay predicate can        the same, there is a sort of Java version of {log} called JSetL
speed up the execution of the prototype. However, if the          [33], [34].
delayed constraint is important to discharge a particular             Answer Set Programming, which is close to constraint
proof obligation the proof will take longer compared to a         programming, has been used to generate counterexamples
goal where that constraint is not delayed. Hence, the best        for false and unprovable verification conditions (VC) of the
strategy is to delay a constraint for a proof while not to        Tokeneer project [35]. These VC correspond to those gener-
delay it for another. This requires some proof programming.       ated during the verification of the SPARK implementation.
In general proof programming has to be applied only to            As we have shown, {log} returns a finite representation of
some constraints. It is an area that deserves to be further       all the solutions of any satisfiable formula. These solutions
explored.                                                         are counterexamples when the intention is to discharge a
    The numbers reported in Table 1 provide evidence about        VC—that is, the VC is negated, submitted to {log} and it
the usefulness of {log} as a verification tool for Z specifica-   returns a solution (counterexample) meaning that the VC is
tions.                                                            not a theorem. Along the same lines, in a technical report,
                                                                  Jackson and Passmore apply an SMT solving-based tool to
                                                                  prove SPARK VC of the Tokeneer project [36]. The tool calls
6.1 Platform where the verification was executed                  CVC 3, Yices, Z3 and Simplify. Roughly, the tool proves
The verification of the {log} prototype of the TIS specifi-       more than 90% of the VC. Tokeneer has also been used as
cation was performed on a Latitude E7470 (06DC) with a            a case study for the formal verification framework Echo
4 core Intel(R) CoreTM i7-6600U CPU at 2.60GHz with 8             [37]. Echo uses PVS as a theorem prover and SPARK as
TO BE COMPLETED                                                                                                                       14

                                                           TABLE 1
                                                  Summary of Quantitative Report


                                                              E FFORT
                                 From 40 to 120 man-hour (prototype + proofs)

                                                               S IZE
                                                                                KLOC        KB YTE
                                 Z (LATEX)                                        2          52
                                 P ROTOTYPE ({log})                               2.6       108
                                 L EMMAS ({log})                                  5.1       276

                                                     P ROOF O BLIGATIONS (L EMMAS )
                                                  C OLLECTION                  N UMBER     T IME ( S )
                                 N EGATIONS                                         93         4
                                 I NVARIANCE                                     325         533
                                       TISEnrolOp                                            107
                                       TISValidateUserToken                                  114
                                       TISPoll                                               281
                                 S ATISFIABILITY OF INITIAL STATE                   12         0.1
                                 S ATISFIABILITY OF OPERATIONS                      74         0.9
                                 S ECURITY PROPERTIES                               19       313

                                 T OTALS                                         523         851



programming language. According to the paper “in 90%               anomalous behaviors. {log} can be used in place of Alloy
of the cases, the PVS theorem prover could not prove the           and its analyzer. In fact the Alloy Analyzer does not imple-
implication lemmas completely automatically”.                      ment a decision procedure for sets and binary relations, as
    Although, the VC are at the SPARK level and the proof          the one provided by {log}. Then, the Alloy Analyzer might
obligations discharged by {log} and Rodin (cf. Rivera et           fail in finding a counterexample while {log} might not.
al. above) are at the specification level, there should be a
clear relation between them as the SPARK program should
implement the specification. Hence, {log} looks promising
                                                                   8     C ONCLUSIONS
as a VC verifier.                                                  We have encoded the Z specification of the Tokeneer project
    Abdelhalim et al. [38] apply CSP to formalize fUML ac-         in {log}. This encoding can be used as a functional pro-
tivity diagrams and FDR as a model checker to the Tokeneer         totype. Then, we used {log} to automatically proved hun-
specification. Specifically the authors found several dead-        dreds of proof obligations over the prototype itself. That
lock scenarios in the form of counterexamples generated by         is, we took advantage of the formula-program duality of
FDR.                                                               {log} code to produce a verified prototype w.r.t. the proven
    The work authored by Moy and Wallenburg [39] is in-            properties. In this way, {log} is used as a programming
teresting because they find problems in Tokeneer, although         language and a verification engine using the same and
it was formally verified. Moy and Wallenburg’s goal is to          only representation of the system. The case study provides
find out why these problems were not found when the                evidence that {log} can be helpful in analyzing set-based
system was verified and to propose verification activities         formal specifications like those written in the Z formal
that could have detected these problems. Specifically, the au-     notation.
thors propose to complement formal verification with static            The most interesting future work is to apply {log} to
analysis and code reviews. {log} might be considered as part       discharge the verification conditions generated during the
of the toolbox proposed by Moy and Wallenburg as it is             verification of the SPARK implementation.
at the intersection of several programming and verification
paradigms. For instance, it can be used to perform proofs          R EFERENCES
and to run functional scenarios.
                                                                   [1]   X. Leroy, “Formal verification of a realistic compiler,” Commun.
    Woodcock at al. [29] apply an assertion-guided model-
                                                                         ACM, vol. 52, no. 7, pp. 107–115, 2009. [Online]. Available:
based robustness testing method to the Tokeneer project.                 http://doi.acm.org/10.1145/1538788.1538814
Robustness testing checks that a system can handle unex-           [2]   T. C. Murray, D. Matichuk, M. Brassil, P. Gammie, T. Bourke,
pected user input or software failures. They use a model of              S. Seefried, C. Lewis, X. Gao, and G. Klein, “sel4: From general
                                                                         purpose to a proof of information flow enforcement,” in 2013
the system for code generation (the Z original specification)            IEEE Symposium on Security and Privacy, SP 2013, Berkeley, CA,
and a separate model for test case generation (an Alloy                  USA, May 19-22, 2013. IEEE Computer Society, 2013, pp. 415–429.
model); these models are independently produced from the                 [Online]. Available: https://doi.org/10.1109/SP.2013.35
requirements. The test case specifications are fed into the        [3]   S. King, J. Hammond, R. Chapman, and A. Pryor, “Is
                                                                         proof more cost-effective than testing?” IEEE Trans. Software
Alloy Analyzer, and test cases are automatically generated               Eng., vol. 26, no. 8, pp. 675–686, 2000. [Online]. Available:
as counterexamples. This allowed the authors to detect nine              https://doi.org/10.1109/32.879807
TO BE COMPLETED                                                                                                                                           15

[4]  A. Hall and R. Chapman, “Correctness by construction:                       [23] M. Cristiá, G. Rossi, and C. S. Frydman, “{log} as a test case
     Developing a commercial secure system,” IEEE Software,                           generator for the Test Template Framework,” in SEFM, ser. Lecture
     vol. 19, no. 1, pp. 18–25, 2002. [Online]. Available: https:                     Notes in Computer Science, R. M. Hierons, M. G. Merayo, and
     //doi.org/10.1109/52.976937                                                      M. Bravetti, Eds., vol. 8137. Springer, 2013, pp. 229–243.
[5] Common Criteria Recognition Arrangement, “Common criteria                    [24] M. Cristiá and G. Rossi, “Automated proof of Bell–LaPadula
     for information technology security evaluation, part 1:                          security properties,” J. Autom. Reasoning, vol. n/a, no. n/a, jul
     Introduction and general model, version 3.1. release 5,” Tech. Rep.,             2020. [Online]. Available: https://link.springer.com/article/10.
     2017. [Online]. Available: https://www.commoncriteriaportal.                     1007/s10817-020-09577-6
     org/files/ccfiles/CCPART1V3.1R5.pdf                                         [25] J. T. Schwartz, R. B. K. Dewar, E. Dubinsky, and E. Schonberg,
[6] J. Barnes, R. Chapman, R. Johnson, J. Widmaier, D. Cooper, and                    Programming with Sets - An Introduction to SETL, ser. Texts and
     B. Everett, “Engineering the Tokeneer enclave protection soft-                   Monographs in Computer Science. Springer, 1986. [Online].
     ware,” in Proceedings of the IEEE International Symposium on Secure              Available: http://dx.doi.org/10.1007/978-1-4613-9575-1
     Software Engineering. IEEE, 2006.                                           [26] H. Andréka, S. R. Givant, and I. Németi, Decision problems for
[7] D. Cooper and J. Barnes, “Tokeneer ID Station EAL5                                equational theories of relation algebras. American Mathematical Soc.,
     demonstrator: Summary report,” Altran Praxis, Tech. Rep.,                        1997, vol. 604.
     2008. [Online]. Available: https://www.adacore.com/uploads/                 [27] P. Stocks and D. Carrington, “A Framework for Specification-
     downloads/Tokeneer Report.pdf                                                    Based Testing,” IEEE Transactions on Software Engineering, vol. 22,
[8] J. M. Spivey, The Z notation: a reference manual. Hertfordshire, UK,              no. 11, pp. 777–793, Nov. 1996.
     UK: Prentice Hall International (UK) Ltd., 1992.                            [28] M. Cristiá, P. Albertengo, C. S. Frydman, B. Plüss, and P. Rodrı́guez
[9] B. Potter, J. Sinclair, and D. Till, An introduction to formal specification      Monetti, “Tool support for the Test Template Framework,” Softw.
     and Z. Prentice Hall PTR Upper Saddle River, NJ, USA, 1996.                      Test., Verif. Reliab., vol. 24, no. 1, pp. 3–37, 2014.
[10] A. Dovier, C. Piazza, E. Pontelli, and G. Rossi, “Sets and constraint       [29] J. Woodcock, E. G. Aydal, and R. Chapman, “The tokeneer
     logic programming,” ACM Trans. Program. Lang. Syst., vol. 22,                    experiments,” in Reflections on the Work of C. A. R. Hoare,
     no. 5, pp. 861–931, 2000.                                                        A. W. Roscoe, C. B. Jones, and K. R. Wood, Eds. Springer,
[11] M. Cristiá and G. Rossi, “Solving quantifier-free first-order                   2010, pp. 405–430. [Online]. Available: https://doi.org/10.1007/
     constraints over finite sets and binary relations,” J. Autom.                    978-1-84882-912-1\ 17
     Reasoning, vol. 64, no. 2, pp. 295–330, 2020. [Online]. Available:          [30] G. Betarte, J. D. Campo, C. Luna, and A. Romano, “Formal
     https://doi.org/10.1007/s10817-019-09520-4                                       analysis of Android’s permission-based security model,,” Sci.
[12] G. Rossi, “{log},” http://people.dmi.unipr.it/gianfranco.rossi/setlog.Home.html, Ann. Comp. Sci., vol. 26, no. 1, pp. 27–68, 2016. [Online]. Available:
     2008. [Online]. Available: http://people.dmi.unipr.it/gianfranco.                https://doi.org/10.7561/SACS.2016.1.27
     rossi/setlog.Home.html                                                      [31] C. Luna, G. Betarte, J. D. Campo, C. Sanz, M. Cristiá,
[13] A. Praxis”. (2008) Tokneer software and project documents. [On-                  and F. Gorostiaga, “A formal approach for the verification
     line]. Available: http://www.adacore.com/uploads/downloads/                      of the permission-based security model of Android,” CLEI
     tokeneer.zip                                                                     Electron. J., vol. 21, no. 2, 2018. [Online]. Available: https:
[14] J. Barnes, “Tokeneer ID Station: Formal specification,”                          //doi.org/10.19153/cleiej.21.2.3
     Altran Praxis, Tech. Rep., 2008, find it as /toke-                          [32] V. Rivera, S. Bhattacharya, and N. Cataño, “Undertaking
     neer/docs/41 2 Formal Functional Specification/41 2.pdf in-                      the tokeneer challenge in event-b,” in Proceedings of the 4th
     side tokeneer.zip. [Online]. Available: http://www.adacore.                      FME Workshop on Formal Methods in Software Engineering,
     com/uploads/downloads/tokeneer.zip                                               FormaliSE@ICSE 2016, Austin, Texas, USA, May 15, 2016. ACM,
[15] D. Cooper, “Tokeneer ID Station: Security properties,”                           2016, pp. 8–14. [Online]. Available: https://doi.org/10.1145/
     Altran Praxis, Tech. Rep., 2008, find it as /to-                                 2897667.2897671
     keneer/docs/40 4 Security Properties/40 4.pdf inside toke- [33] M. Cristiá and G. Rossi, “Programming in Java with restricted
     neer.zip. [Online]. Available: http://www.adacore.com/uploads/                   intensional sets,” in Proceedings of the 3rd International Workshop on
     downloads/tokeneer.zip                                                           Sets and Tools co-located with the 6th International ABZ Conference,
[16] A. Evans, “An improved recipe for specifying reactive systems                    SETS@ABZ 2018, Southamptom, UK, June 5, 2018., ser. CEUR
     in Z,” in ZUM ’97: The Z Formal Specification Notation, 10th                     Workshop Proceedings, M. Cristiá, D. Delahaye, and C. Dubois,
     International Conference of Z Users, Reading, UK, April 3-4, 1997,               Eds., vol. 2199. CEUR-WS.org, 2018, pp. 17–31. [Online].
     Proceedings, ser. Lecture Notes in Computer Science, J. P. Bowen,                Available: http://ceur-ws.org/Vol-2199/paper2.pdf
     M. G. Hinchey, and D. Till, Eds., vol. 1212. Springer, 1997, pp. 275–       [34] G. Rossi and F. Bergenti, “Nondeterministic programming in Java
     294. [Online]. Available: https://doi.org/10.1007/BFb0027293                     with JSetL,” Fundam. Inform., vol. 140, no. 3-4, pp. 393–412, 2015.
[17] L. Lamport, “TLZ,” in Z User Workshop, Cambridge, UK, 29-30                      [Online]. Available: https://doi.org/10.3233/FI-2015-1260
     June 1994, Proceedings, ser. Workshops in Computing, J. P. Bowen [35] F. Schanda and M. Brain, “Using answer set programming in the
     and J. A. Hall, Eds. Springer/BCS, 1994, pp. 267–268. [Online].                  development of verified software,” in Technical Communications
     Available: https://doi.org/10.1007/978-1-4471-3452-7\ 15                         of the 28th International Conference on Logic Programming, ICLP
[18] M. Cristiá and G. Rossi, “A set solver for finite set relation                  2012, September 4-8, 2012, Budapest, Hungary, ser. LIPIcs, A. Dovier
     algebra,” in Relational and Algebraic Methods in Computer Science                and V. S. Costa, Eds., vol. 17. Schloss Dagstuhl - Leibniz-
     - 17th International Conference, RAMiCS 2018, Groningen, The                     Zentrum für Informatik, 2012, pp. 72–85. [Online]. Available:
     Netherlands, October 29 - November 1, 2018, Proceedings, ser. Lecture            https://doi.org/10.4230/LIPIcs.ICLP.2012.72
     Notes in Computer Science, J. Desharnais, W. Guttmann, and                  [36] P. B. Jackson and G. O. Passmore, “Proving SPARK verification
     S. Joosten, Eds., vol. 11194. Springer, 2018, pp. 333–349. [Online].             conditions with SMT solvers,” University of Edinburgh, Tech.
     Available: https://doi.org/10.1007/978-3-030-02149-8\ 20                         Rep., 2009. [Online]. Available: http://homepages.inf.ed.ac.uk/
[19] ——, “A decision procedure for restricted intensional sets,” in                   pbj/papers/vct-dec09-draft.pdf
     Automated Deduction - CADE 26 - 26th International Conference [37] X. Yin and J. C. Knight, “Formal verification of large software
     on Automated Deduction, Gothenburg, Sweden, August 6-11, 2017,                   systems,” in Second NASA Formal Methods Symposium - NFM 2010,
     Proceedings, ser. Lecture Notes in Computer Science, L. de Moura,                Washington D.C., USA, April 13-15, 2010. Proceedings, ser. NASA
     Ed., vol. 10395. Springer, 2017, pp. 185–201. [Online]. Available:               Conference Proceedings, C. A. Muñoz, Ed., vol. NASA/CP-2010-
     https://doi.org/10.1007/978-3-319-63046-5\ 12                                    216215, 2010, pp. 192–201.
[20] ——, “Automated reasoning with restricted intensional sets,” [38] I. Abdelhalim, J. Sharp, S. A. Schneider, and H. Treharne,
     CoRR, vol. abs/1910.09118, 2019. [Online]. Available: http:                      “Formal verification of tokeneer behaviours modelled in fuml
     //arxiv.org/abs/1910.09118                                                       using CSP,” in Formal Methods and Software Engineering - 12th
[21] C. Holzbaur, F. Menezes, and P. Barahona, “Defeasibility in                      International Conference on Formal Engineering Methods, ICFEM
     CLP(Q) through generalized slack variables,” in CP, ser. Lecture                 2010, Shanghai, China, November 17-19, 2010. Proceedings, ser.
     Notes in Computer Science, E. C. Freuder, Ed., vol. 1118. Springer,              Lecture Notes in Computer Science, J. S. Dong and H. Zhu,
     1996, pp. 209–223.                                                               Eds., vol. 6447. Springer, 2010, pp. 371–387. [Online]. Available:
[22] A. Dovier, E. Pontelli, and G. Rossi, “Set unification,” Theory Pract.           https://doi.org/10.1007/978-3-642-16901-4\ 25
     Log. Program., vol. 6, no. 6, pp. 645–701, 2006.                            [39] Y. Moy and A. Wallenburg, “Tokeneer: Beyond formal program
TO BE COMPLETED                                                        16

    verification,” Embedded Real Time Software and Systems, vol. 24,
    2010.




                     Maximiliano Cristiá to be completed.



     PLACE
     PHOTO
      HERE




                     Gianfranco Rossi to be completed.



     PLACE
     PHOTO
      HERE
