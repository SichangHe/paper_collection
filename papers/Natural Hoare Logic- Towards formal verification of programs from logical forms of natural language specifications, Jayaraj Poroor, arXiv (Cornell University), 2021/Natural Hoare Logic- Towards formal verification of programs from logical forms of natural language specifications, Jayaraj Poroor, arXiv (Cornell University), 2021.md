                                            Natural Hoare Logic: Towards formal verification of programs
                                                from logical forms of natural language specifications
                                                                                               Jayaraj Poroor
                                                                                           jayaraj.poroor@gmail.com
                                                                                                    JIFFY.ai
                                        ABSTRACT                                                                 Hoare logic [16]1 and its variants are established formal
                                        Formal verification provides strong guarantees of correctness         techniques for proving that a program satisfies its specifica-
                                                                                                              tion in the form of pre-condition, post-condition assertions.
arXiv:2103.05779v1 [cs.PL] 4 Mar 2021




                                        of software, which are especially important in safety or secu-
                                        rity critical systems. Hoare logic is a widely used formalism            Hoare logic assertions are specified as triples of the form
                                        for rigorous verification of software against specifications in       {P}S{Q}, where P and Q are logical assertions on program vari-
                                        the form of pre-condition/post-condition assertions. The ad-          ables. The meaning of the triple is that: if program variables
                                        vancement of semantic parsing techniques and higher com-              satisfy the condition P and the program S is executed, then
                                        putational capabilities enable us to extract semantic content         the program variables satisfy the condition Q provided the
                                        from natural language text as formal logical forms, with in-          program terminates. This is called the partial correctness
                                        creasing accuracy and coverage.                                       assertion. We may extend it to total correctness with the
                                           This paper proposes a formal framework for Hoare logic-            additional assertion that the program will terminate when
                                        based formal verification of imperative programs using logi-          starting at a variable state satisfying P. In this paper, we
                                        cal forms generated from compositional semantic parsing of            consider only partial correctness. If we do not consider ex-
                                        natural language assertions. We call our reasoning approach           ception conditions, for loop-free programs partial correctness
                                        Natural Hoare Logic. This enables formal verification of soft-        coincide with total correctness.
                                        ware directly against safety requirements specified by a do-             Semantic parsing [18] is a collection of techniques whose
                                        main expert in natural language.                                      objective is to obtain a formal representation of meaning
                                           We consider both declarative assertions of program invari-         from natural language sentences. For most part, the research
                                        ants and state change as well as imperative assertions that           in semantic parsing is concerned with obtaining a represen-
                                        specify commands which alter the program state. We discuss            tation of meaning that can be interpreted by a computer to
                                        how the reasoning approach can be extended using domain               perform the task at hand, such as querying a database to
                                        knowledge and a practical approach for guarding against se-           obtain results. Semantic parsing covers a spectrum of tech-
                                        mantic parser errors.                                                 niques from shallow to deep. Shallow semantic parsing tech-
                                                                                                              niques such as semantic role labelling [30] aims to identify
                                                                                                              semantic roles (such as agent or location) associated with
                                                                                                              the events specified in a sentence. In contrast, deep seman-
                                        1    INTRODUCTION                                                     tic parsing aims to extract a rich representation of meaning
                                        Formal verification techniques [50] are a collection of tech-         known as logical forms in a formal system such as the λ-
                                        niques that can be used to provide strong guarantees of cor-          calculus [5].
                                        rectness and security for software. They are especially desir-           In this paper we concern ourselves with formal logical
                                        able in safety critical software such as the control software         forms generated by semantic parsers in the form of λ-calculus
                                        of medical devices [24] or security sensitive portions of a           expressions. λ-calculus is preferred over first order logic for
                                        software system [2]. In order to perform formal verification          logical forms since it allows us to define semantics compo-
                                        we must specify the correctness or security requirements in a         sitionally using function composition and function applica-
                                        formal language. For instance, consider the following natural         tion, from logic forms representing meanings of constituents.
                                        language specification of a safety requirement of a medical           Compositional semantics is originally due to Richard Mon-
                                        infusion pump from [35]:                                              tague [34] and hence is broadly called Montague semantics
                                            “The infusion manager shall stop infusion whenever a              [17]. Simply-typed λ-calculus [10] with pre-defined constants
                                                         critical alarm occurs.” [35]                         for logical connectives and quantifiers, known as the higher-
                                                                                                              order logics2 , is commonly employed as the formal language
                                           Such natural language specifications are typically given by        for logical forms [7]. In this paper we consider logical forms
                                        domain experts who understand the safety requirements of              in this formal language3 . Owing to the expressive power
                                        the particular field. However, in order to formally verify the        of λ-calculus we do not lose any generality. Other logical
                                        system against these requirements, we must specify them in            1 Also called Floyd-Hoare logic since Floyd had developed a similar
                                        a formal language, which cannot be typically done by the              system for Flowchart programs earlier[14].
                                        domain expert. The objective of this paper is to propose a            2 Higher-order logics may also be considered as a generalization of first

                                        general method that enables software to be formally verified          order logic.
                                                                                                              3 The lambda calculator available at http://lambdacalculator.com/ is
                                        directly against requirements specified by a domain expert            a great educational tool for natural language semantics in the λ-
                                        in natural language.                                                  calculus.
                                                                                                          1
,,                                                                                                                              Jayaraj Poroor


forms like λ-DCS [25] can be readily expressed in terms of                                                               {I}
λ-calculus.                                                                                             R

   We propose a framework for associating logical forms gen-
                                                                                       L                                    S
erated from assertions about program state made in natural                                              R
language to pre-condition/post-condition assertions in Hoare
logic. We call our framework, Natural Hoare Logic (NHL).                                                                 {I}
Our objective is to enable formal verification of programs
from natural language assertions.                                      Figure 1: Invariant proofs in Hoare logic from logical forms.

2     THE PROPOSED FRAMEWORK
We introduce the proposed framework with the help of sim-                We may use the semantic expressions corresponding to
ple examples. We use the notation text to denote the se-               the entities present in the natural language specification to
mantics of text in λ-calculus. We use identifier to denote the         construct the relation, as below.
semantic function or constant corresponding to identifier ap-
pearing in the sentence.                                                                   R , ∃x · balance(x) = _balance                 (3)
   Consider the statement:                                                It may be noted that ∃x · P = ∃ λx · P.
           All balances must be greater than zero.                        Given a logical form L specifying a program invariant4
                                                                       and an LFPL relation R, we may prove that the program S
   where,                                                              satisfies the invariant by establishing the Hoare triple {I} S {I},
   balances = λx· balance(x), a function that returns the bal-         where I is the strongest condition that satisfies:
ance value, given an account. For the sake of simplicity, in
our examples, we restrict our semantic domain (and hence                                        L ∧ R =⇒ I =⇒
                                                                                                            6 R                           (4)
our domain of discourse) to accounts.                                     The condition, I =⇒ 6   R is required to remove the corre-
   greater than = λx, y· x > y                                         spondance relation from the Hoare logic assertions. In prac-
   zero = λx· 0, which we may simply write as 0.                       tice, I should be an assertion on program variables without
   all = ∀. ∀ is simply a higher-order function constant in            any correspondence to logical forms. Presence of the corre-
our logic that takes a truth-valued function f and evaluates           spondence relation in Hoare logic assertions may cause the
to true if f evalutes to true for all values.                          proof to fail owing to the predicate transformer nature of
   The semantics of the entire sentence may be composed                Hoare logic rules. The Hoare logic rules will transform the
from the constituent semantics to get:                                 program variables in the assertions while the variables in the
   All balances must be greater than zero =                            logical forms remain unchanged. This results in the LFPL re-
                                                                       lation specifications in the assertions to become inconsistent
                      ∀x · balance(x) > 0                   (1)
                                                                       as Hoare logic rules get applied.
   Please note that, ∀x · P is a short-hand for ∀ λx · P. We              The requirement that I is the strongest condition that
omit explicit type annotations in the logical forms used in            satisfies the above constraint ensures that a weakened form
our examples.                                                          of the user requirement is not take up for proof.
   Now, consider the following program fragment that simply               Figure 1 visualizes how R relates the invariant specified in
increments a variable representing balance:                            the logical form L to pre-condition P and post-condition Q.
                                                                       The arrow {Q} → S → {P} shows the direction of the proof.
                  _balance := _balance + 1                  (2)        Program execution and the state transformation occurs in
                                                                       the opposite direction.
To avoid name confusion we prefix the names of program                    Using the Hoare triple in Equation 21 for proving logical
variables with underscore (e.g., _balance).                            form 1 on program 2:
                                                                          Since:
2.1    Invariant declaratives                                                {∀x · balance(x) > 0} ∧ ∃x · balance(x) = _balance           (5)
In order to prove that the program holds the invariant spec-
ified by the logical form in Equation 1, we must relate the
variables occuring in the logical form to the variables occur-                                                      _balance > 0          (6)
ing in the program.                                                      We need to prove:
    We specify the relation between the logical form and pro-
gram variables via a formal relation. We call this the logical                                          {_balance > 0}                    (7)
form - program logic relation (LFPL relation). This is similar                               _balance := _balance + 1                     (8)
in spirit to the state relations [49] from the refinement theory                                        {_balance > 0}                    (9)
[11] used to prove formal correspondence (forward/backward
simulations) between an abstract specification and its con-            4 We considerthe invariant to hold true only before and after the
crete implementation.                                                  program execution, not in the intermediate states.
                                                                   2
Natural Hoare Logic                                                                                                                   ,,


   We can prove this by considering a stronger post-condition                                                            {P}
_balance > 1 and applying the assignment rule, and then                                                 R

applying the consequence rule to weaken the post-condition
                                                                                       L                                  S
to get back the invariant.                                                                             R′
   The LFPL relation simply specifies the formal association
between the logical form and the program variables. We may                                                               {Q}
make a general assertion in natural language and then use
the LFPL relation to establish the association. For example,                Figure 2: Hoare logic proofs from imperative logical forms.
consider the natural language assertion:
              All values must be greater than zero.
   Its corresponding logical form may be:                                     R ′ is obtained by replacing the variable x by post(x) in
                                                                           the body of R, assuming the R relation is on a single logical
                          ∀x · valueof (x) > 0                (10)
                                                                           variable x. If there are multiple logical variables, then the
   In this case, the LFPL relation would specify that the                  post function must be applied on all of them.
program variable _balance is the value of an account, as                      Given a L which is a logical form of the imperative asser-
follows:                                                                   tion, we may prove that a program S satisfies the specified
                                                                           imperative command, by proving the following:
                      ∃x · valueof (x) = _balance             (11)
                                                                                                {L ∧ R} S {L ∧ R ′ }                (13)
2.2    Imperatives
                                                                                                                                    (14)
Consider the statement:
                       Increment the balance.                                 This is simpler than that of the invariant because post-
   This is an imperative sentence, specifying a command to                 condition and pre-condition use different LFPL relations, R
be performed. Semantics of imperatives are much more chal-                 and R ′ .
lenging than that of declarative statements [21]. A common                    Figure 2 visualizes how LFPL relations R and R ′ are used
approach for specifying semantics of imperative sentences is               for Hoare logic proofs from imperative logical forms.
by introducing modal operators[20, 38]. In this paper, we do                  For the sentence, increment the balance the Hoare triple
not consider imperatives in a general setting, instead restrict            to prove becomes:
ourselves to considering only those imperative statements                     We need to prove:
that specify operations on program state.                                                   {L ∧ ∃x · balance(x) = _balance}        (15)
   As a result, we explicitly model a restricted form of modal-
ity as a logical relation between the current state of the world                                   _balance := _balance + 1         (16)
(before-state) and the state after the command has been car-                          {L ∧ ∃x · balance(post(x)) = _balance}        (17)
ried out (after-state)5 . We define a function post that maps
elements to their after-state. Therefore, λx· balance(post(x))             where L = ∀x · balance(post(x)) = balance(x) + 1.
gives the balance of an account after the specified command                  Applying the assignment rule to the post-condition, we get
has been carried out. The semantics of ‘increment’ can be                  the following assertion, from which the pre-condition follows:
defined as a higher order function as follows:
   increment = λf · ∀x · f(post(x)) = f(x) + 1                                       L ∧ ∃x · balance(post(x)) = _balance + 1       (18)
   This allows such imperative commands to be composed
with the semantics of its objects, enabling compositional se-              2.3   Conditional imperatives
mantics, e.g,                                                              We consider conditional imperatives where the conditional
   increment the balance = ∀x · balance(post(x)) =                         and imperative parts are specified separately. An example of
balance(x) + 1                                                             a conditional imperative statement is:
   Of course we are unable to model general imperative state-
ments such as: you may increment the balance. However, we                    IF: the balance is greater than 0 THEN: increment the
believe our approach is useful enough for specifying pre-                                             balance.
condition/post-conditions assertions on sequential impera-                   The proof approach for imperatives may be extended to
tive programs.                                                             conditional imperatives in a straightforward manner.
   In addition to the R relation defined previously, we also                 If E is the logical form of the conditional part and L, then
define an R ′ relation as:                                                 the proof rule is:

                                                                                              {L ∧ R ∧ E} S {L ∧ R ′ }              (19)
             R ′ , ∃x · balance(post(x)) = _balance           (12)
                                                                                                                                    (20)
5 We may consider this as a modality with two possible worlds repre-
sented by the before-state and after-state.                                  The proof rule is visually illustrated in Figure 3.
                                                                       3
,,                                                                                                                       Jayaraj Poroor


                                    R                                            All balances must be greater than zero
             L∧E                                {P}



               L                                 S                                         ∀x · balance(x) > 0                   (25)
                                R′
                                                                        Consider the domain knowledge that the balance of an
                                                {Q}                   account is its value, which we may express logically as:

                                                                                       ∀x · balance(x) = valueof (x)             (26)
Figure 3: Hoare logic proofs from logical forms of conditional
imperatives.                                                             We may use this and our previous proof to now infer, that
                                                                      program S satisfies new invariant in Equation 25, without
                                R                                     having to go through the proof again.
              L                                 {P}
                                                                         In many domains, formalized domain knowledge exists in
                                                                      the form of domain ontologies in languages such as the web
              L′                                 S                    ontology language[33] (which has a logical basis in descrip-
                               R′                                     tion logics [3]). For instance the ontological assertion that A
                                                                      isa B can be expressed as:
                                                {Q}
                                                                                           ∀x · A(x) =⇒ B(x)                     (27)
Figure 4: Hoare logic proofs from pre/post-condition logical
                                                                         Bringing such knowledge to aid in our reasoning is likely
forms.
                                                                      to be quite beneficial.

2.4     Pre/Post-condition declaratives                               2.6   Guarding against semantic parser errors
Another form of natural language specification we consider            Owing to the variety and ambiguity in natural language sen-
is the declarative specification of the pre-condition and post-       tences, semantic parsers are probabilistic parsers. The parse
condition separately. For instance:                                   (and the resultant logical form) with the highest probabil-
  IF: the balance is greater than 0 THEN AFTER: balance               ity is taken as the selected parse (logical form). This need
                 must be remain non-negative                          not always be the correct parse. Since we are targeting for-
   This case is simpler than the imperative specification. The        mal verification of programs, we need to guard against these
Hoare logic assertion would be:                                       errors. In this section, we consider one practical approach.
                                                                         Given a language of logical forms generated by a semantic
                                                                      parser, we define a function from logical forms to natural
                       {L ∧ R} S {L ′ ∧ R ′ }             (21)        language, let’s call this function N. We may use this function
                                                          (22)        to paraphrase the user input in the manner understood by
                                                                      the system. Given a natural language sentence S input by a
     where L ′ is the logical form of the post-condition and L        user and if its logical form generated by a semantic parser is
is the logical form of the pre-condition.                             S, then we could ask back the user:
   Figure 4 visualizes how LFPL relations R and R ′ are used
for Hoare logic froms for logical forms of pre/post-condition                             Did you mean: N(S)?
assertions.                                                              If the answer is yes we proceed, otherwise we could show
                                                                      the N-mappings of other probable logical forms (if available)
2.5     Extending with domain knowledge                               for user to choose from. User’s selection may also be used
In this section we discuss how our reasoning technique can            as a form of labelling for retraining the model. If the user is
be extended using domain knowledge specified in the form of           unable to choose, then the system may prompt the user to
logical expressions. For example, consider the sentence and           rephrase the specification (perhaps as simpler sentences).
its logical form below:                                                  Of course it is important for the N-function to generate
              All values must be greater than zero                    a consistent and understandable natural language represen-
                                                                      tation. This is usually a simpler problem than the semantic
   Logical form:
                                                                      parsing itself.
                                                                         Semantic parsing based on synchronous context free gram-
                     ∀x · valueof (x) > 0               (23)
                                                                      mars (SCFG) [48] is especially interesting to address this
   Using the LFPL relation below, assume that we have al-             problem. This approach recasts semantic parsing as a ma-
ready established proof for this invariant for some program           chine translation problem - that of translating from natural
S.                                                                    language to the language of logical forms. This enables the
                                                                      parsing to be inverted to generate natural language state-
                  ∃x · valueof (x) = _balance             (24)        ments from logical forms, automically giving us the function
     Now consider a new sentence and its logical form:                N from the learnt grammar.
                                                                  4
Natural Hoare Logic                                                                                                                  ,,


3    BRIEF REVIEW OF RELATED FIELDS                                    and low level. A Hoare Logic for Java embedded in the Is-
In this section, we briefly review Hoare logics and seman-             abelle/HOL theorem prover[37] is given in [46]. A Hoare logic
tic parsing since our framework attempts to connect logical            for realistic machine code is presented in [36].
forms that are outcomes of semantic parsing with Hoare logic              The principle of forward (backward) simulations from the
assertions on programs.                                                refinement theory [11] may be used to prove formal corre-
                                                                       spondence between an abstract specification and concrete
Hoare logic                                                            implementation. This enables us to prove formal properties
                                                                       on the abstract specification using Hoare logic (or equivalent
We briefly review the basic Hoare logic rules. The simplest
                                                                       methods) which then carries over to the concrete implemen-
rule is the axiom of assignment:
                                                                       tation owing to the simulation proofs. Formal verification of
                                                                       complex programs such as the seL4 microkernel takes this
                       {Q[E/x]} x := E {Q}                  (28)
                                                                       approach [22].
   The notation Q[E/x] stands for the expression obtained af-             Mechanization of Hoare logic proofs involve first generat-
ter all instances of the variable x occuring in Q is substituted       ing verification conditions by a verification condition gener-
with expression E.                                                     ator (VCG) that apply Hoare logic rules on the annotated
   The rule for sequential composition can be used to infer            code [32]. The verification conditions are then typically me-
the pre-condition/post-condition asserts of a program from             chanically checked by an automated theorem prover.
its sequential components:

                        {P} S1 {Q}     {Q} S2 {R}                      Semantic parsing
                             {P} S1 ; S2 {R}         (29)              Combinatory categorical grammars (CCGs) [45] is a well
                                                                       studied and powerful method to achieve compositional se-
   The conditional rule may be applied to reason about if-
                                                                       mantics. CCGs employ a few general purpose combinatory
else statements.
                                                                       rules along with a highly lexicalized grammar that maps to-
                 {E ∧ P} S1 {Q}        {¬E ∧ P} S2 {Q}                 kens/phrases to categories. CCG2Lambda [31] is a recent
                      {P} if E then S1 else S2 {Q}  (30)               work that compositionally maps CCG trees to λ-terms.
                                                                          Compositional semantics can also be achieved by attach-
  The consequence rules allows us to strengthen the pre-
                                                                       ing logical forms to context-free syntactic parsing rules (usu-
condition and weaken the post-condition:
                                                                       ally parsing is done on tokens/phrases tagged with semantic
                P =⇒ P ′      {P ′ } S {Q ′ }   Q ′ =⇒ Q               annotations)6 . Whenever a context-free syntactic rule is ap-
                                                                       plied, the attached logical form is composed with the logical
                                {P} S {Q}               (31)
                                                                       forms of the constituents to generate a resultant logical form.
    Reasoning about loops is done using the while loop rule:              Semantic parsing based on synchronous context free gram-
                              {I ∧ E} S {I}                            mars (SCFG) is proposed in [48]. This approach recasts se-
                                                                       mantic parsing as a machine translation problem - that of
                    {I} while E do S {¬E ∧ I}              (32)
                                                                       translating from natural language to the language of logical
   Here I is the loop invariant. One of the primary difficulties       forms. This also enables the parsing to be inverted to gener-
in automating Hoare logic proofs is the construction of loop           ate natural language statements from logical forms. The abil-
invariants. In general, the code must be manually annotated            ity to invert logical forms to natural language statements is
with loop invariants for Hoare logic proofs to go through.             especially interesting for the problem being addressed in this
   The Hoare logic axioms and inference rules provide an ax-           paper. This enables us to give a natural language feedback of
iomatic semantics for an imperative programming language.              what the system has understood regarding the natural lan-
Hoare logic rules may be recast as rules for obtaining weak-           guage specification made by the domain expert. This acts
est pre-conditions from post-condition assertions (or equiv-           as a check against any potential errors introduced by the
alently, strongest post-conditions from pre-condition asser-           semantic parser.
tions). The weakest pre-condition or predicate transformer                Compositional semantics using dependency-based parse
semantics is originally due to Dijskstra [12].                         structures is discussed in [27]. More recently, in [41], a compo-
   In recent years, the basic Hoare logic [1] has been ex-             sitional semantics is defined over universal dependency parse
tended to support formal verification of complex and real-             trees. Here the λ-calculus logical forms capture semantics in
world code. For instance, separation logic [42] is one of its          Neo-Davidsonian or event style [8].
variants used for proving correctness properties of programs              Since natural language parsing involves ambiguity, a
with pointer data structures. Crash Hoare Logic [9] extends            learnt scoring model (usually a linear or a log-linear model)
Hoare logic with special crash assertions and recovery pro-            is applied during the semantic parsing to keep track of most
cedures that enables formal reasoning about crash recovery.            probable parses [28]. Learning weights in the scoring model
The paper establishes formal proofs using this extended logic          is done in a supervised setting. Recently techniques for weak
for FSCQ file system.
   A number of researchers have worked on defining Hoare               6 e.g.,    SippyCup    semantic       parser     available    at
logics for real-world programming languages, both high level           https://github.com/wcmac/sippycup
                                                                   5
,,                                                                                                                                    Jayaraj Poroor


supervision wherein the sentences are labelled with the de-                   [6] Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang.
notations (i.e., the results of executing the logical forms) are                  2013. Semantic parsing on freebase from question-answer pairs.
                                                                                  In Proceedings of the 2013 conference on empirical methods in
being investigated [6, 26, 47] replacing the need for strong                      natural language processing. 1533–1544.
supervision using parse tree annotations or even annotating                   [7] Bob Carpenter. 1997. Type-logical semantics. MIT press.
                                                                              [8] Lucas Champollion. 2015. The interaction of compositional se-
sentences with the logical forms. This brings in the problem                      mantics and event semantics. Linguistics and Philosophy 38, 1
of program induction, i.e., inducing logical forms from deno-                     (2015), 31–66.
tations, which is a key challenge that must be solved when                    [9] Haogang Chen, Daniel Ziegler, Tej Chajed, Adam Chlipala,
                                                                                  M Frans Kaashoek, and Nickolai Zeldovich. 2015. Using Crash
labelling with denotations.                                                       Hoare logic for certifying the FSCQ file system. In Proceedings of
   Another approach to semantic parsing [44] takes advan-                         the 25th Symposium on Operating Systems Principles. 18–37.
tage of semantic lexicons based on specific linguistic theo-                 [10] Alonzo Church. 1940. A formulation of the simple theory of types.
                                                                                  The journal of symbolic logic 5, 2 (1940), 56–68.
ries such as VerbNet[43] which is based on Levin’s theory of                 [11] Willem-Paul De Roever, Kai Engelhardt, and Karl-Heinz Buth.
verb alternation classes[23] and FrameNet[4] which is based                       1998. Data refinement: model-oriented proof methods and their
                                                                                  comparison. Number 47. Cambridge University Press.
on frame semantics [13].                                                     [12] Edsger W Dijkstra. 1975. Guarded commands, nondeterminacy
   A yet another approach is to target a narrow domain spe-                       and formal derivation of programs. Commun. ACM 18, 8 (1975),
cific language such as the structured query language (SQL).                       453–457.
                                                                             [13] Charles J Fillmore et al. 2006. Frame semantics. Cognitive lin-
In such a case the semantic parser may directly generate                          guistics: Basic readings 34 (2006), 373–400.
the SQL (DSL) or may first generate an intermediate logi-                    [14] RM FL00. 1967. Assigning Meanings to Programs. In Proceedings
cal form, which is then automatically translated to the DSL                       of Symposium in Applied Mathematics.
                                                                             [15] David Harel, Dexter Kozen, and Jerzy Tiuryn. 2001. Dynamic
(SQL). Natural language to SQL is a well studied problem                          logic. In Handbook of philosophical logic. Springer, 99–217.
[51]. The current state of the art supports SQL queries with-                [16] Charles Antony Richard Hoare. 1969. An axiomatic basis for
                                                                                  computer programming. Commun. ACM 12, 10 (1969), 576–
out joins using deep learning models. Such deep learning                          580.
models have also become state-of-the-art in semantic role                    [17] Theo Janssen. 2011. Montague semantics. (2011).
labelling.                                                                   [18] Aishwarya Kamath and Rajarshi Das. 2018. A survey on semantic
                                                                                  parsing. arXiv preprint arXiv:1812.00978 (2018).
   A semantic parser for parsing natural language sentences                  [19] Rohit Kate and Raymond Mooney. 2007. Semi-supervised learn-
to if-this-then-that recipes is given in [40], targeting the                      ing for semantic parsing using support vector machines. In Hu-
IFTTT service [39]. Their natural language specifications                         man Language Technologies 2007: the Conference of the North
                                                                                  American Chapter of the Association for Computational Lin-
are somewhat similar to the conditional imperative forms                          guistics; Companion Volume, Short Papers. 81–84.
discussed in this paper. However, their semantic parser out-                 [20] Magdalena Kaufmann. 2019. Fine-tuning natural language im-
                                                                                  peratives. Journal of Logic and Computation 29, 3 (2019), 321–
put is in the form of IFTTT recipes rather than λ-calculus                        348.
logical forms. Their parsing approach is based on KRISP [19]                 [21] Stefan Kaufmann and Magdalena Schwager. 2009. A unified anal-
that uses a classifier with a string subsequence kernel [29] for                  ysis of conditional imperatives. In Semantics and linguistic the-
                                                                                  ory, Vol. 19. 239–256.
mapping the natural language sentences to most probable                      [22] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andron-
production rules.                                                                 ick, David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engel-
                                                                                  hardt, Rafal Kolanski, Michael Norrish, et al. 2009. seL4: Formal
                                                                                  verification of an OS kernel. In Proceedings of the ACM SIGOPS
4    CONCLUSION AND FUTURE WORK                                                   22nd symposium on Operating systems principles. 207–220.
                                                                             [23] Beth Levin. 1993. English verb classes and alternations: A pre-
Hoare logic belongs to a general class of formal systems used                     liminary investigation. University of Chicago press.
for reasoning about programs. The results presented here                     [24] Chunxiao Li, Anand Raghunathan, and Niraj K Jha. 2013. Im-
may also be employed to reason with other program logics                          proving the trustworthiness of medical device software with for-
                                                                                  mal verification methods. IEEE Embedded Systems Letters 5, 3
such as the dynamic logic[15]. We intend to further validate                      (2013), 50–53.
the NHL framework with more elaborate examples and case                      [25] Percy Liang. 2013. Lambda dependency-based compositional se-
                                                                                  mantics. arXiv preprint arXiv:1309.4408 (2013).
studies. Exploring the use of domain knowledge to aid rea-                   [26] Percy Liang. 2016. Learning executable semantic parsers for nat-
soning, investigating approaches for a formal soundess proof,                     ural language understanding. Commun. ACM 59, 9 (2016), 68–
and mechanization of the framework are other lines of future                      76.
                                                                             [27] Percy Liang, Michael I Jordan, and Dan Klein. 2013. Learning
work.                                                                             dependency-based compositional semantics. Computational Lin-
                                                                                  guistics 39, 2 (2013), 389–446.
                                                                             [28] Percy Liang and Christopher Potts. 2015. Bringing machine learn-
REFERENCES                                                                        ing and compositional semantics together. Annu. Rev. Linguist.
 [1] Krzysztof R Apt and Ernst-Rüdiger Olderog. 2019. Fifty years                 1, 1 (2015), 355–376.
     of Hoare’s logic. Formal Aspects of Computing 31, 6 (2019),             [29] Huma Lodhi, Craig Saunders, John Shawe-Taylor, Nello Cristian-
     751–807.                                                                     ini, and Chris Watkins. 2002. Text classification using string
 [2] Matteo Avalle, Alfredo Pironti, and Riccardo Sisto. 2014. For-               kernels. Journal of Machine Learning Research 2, Feb (2002),
     mal verification of security protocol implementations: a survey.             419–444.
     Formal Aspects of Computing 26, 1 (2014), 99–123.                       [30] Lluís Màrquez, Xavier Carreras, Kenneth C Litkowski, and
 [3] Franz Baader, Ian Horrocks, and Ulrike Sattler. 2004. Description            Suzanne Stevenson. 2008. Semantic role labeling: an introduc-
     logics. In Handbook on ontologies. Springer, 3–28.                           tion to the special issue.
 [4] Collin F Baker, Charles J Fillmore, and John B Lowe. 1998. The          [31] Pascual Martínez-Gómez, Koji Mineshima, Yusuke Miyao, and
     berkeley framenet project. In 36th Annual Meeting of the Asso-               Daisuke Bekki. 2016. ccg2lambda: A compositional semantics
     ciation for Computational Linguistics and 17th International                 system. In Proceedings of ACL-2016 System Demonstrations.
     Conference on Computational Linguistics, Volume 1. 86–90.                    85–90.
 [5] Hendrik P Barendregt et al. 1984. The lambda calculus. Vol. 3.          [32] John Matthews, J Strother Moore, Sandip Ray, and Daron Vroon.
     North-Holland Amsterdam.                                                     2006. Verification condition generation via theorem proving. In
                                                                         6
Natural Hoare Logic                                                                                                                           ,,


     International Conference on Logic for Programming Artificial                  arXiv:1702.03196 (2017).
     Intelligence and Reasoning. Springer, 362–376.                           [42] John C Reynolds. 2002. Separation logic: A logic for shared mu-
[33] Deborah L McGuinness, Frank Van Harmelen, et al. 2004. OWL                    table data structures. In Proceedings 17th Annual IEEE Sympo-
     web ontology language overview. W3C recommendation 10, 10                     sium on Logic in Computer Science. IEEE, 55–74.
     (2004), 2004.                                                            [43] Karin Kipper Schuler. 2005. VerbNet: A broad-coverage, compre-
[34] Richard Montague. 1973. The proper treatment of quantification                hensive verb lexicon. (2005).
     in ordinary English. In Approaches to natural language. Springer,        [44] Lei Shi and Rada Mihalcea. 2005. Putting pieces together: Com-
     221–242.                                                                      bining FrameNet, VerbNet and WordNet for robust semantic pars-
[35] Anitha Murugesan, Michael W Whalen, Sanjai Rayadurgam, and                    ing. In International conference on intelligent text processing
     Mats PE Heimdahl. 2013. Compositional verification of a medical               and computational linguistics. Springer, 100–111.
     device system. In Proceedings of the 2013 ACM SIGAda annual              [45] Mark Steedman and Jason Baldridge. 2011. Combinatory cat-
     conference on High integrity language technology. 51–64.                      egorial grammar. Non-Transformational Syntax: Formal and
[36] Magnus O Myreen and Michael JC Gordon. 2007. Hoare logic for                  explicit models of grammar (2011), 181–224.
     realistically modelled machine code. In International Conference         [46] David von Oheimb. 2001. Hoare logic for Java in Isabelle/HOL.
     on Tools and Algorithms for the Construction and Analysis of                  Concurrency and Computation: Practice and Experience 13, 13
     Systems. Springer, 568–582.                                                   (2001), 1173–1214.
[37] Tobias Nipkow, Lawrence C Paulson, and Markus Wenzel. 2002.              [47] Bailin Wang, Ivan Titov, and Mirella Lapata. 2019. Learning
     Isabelle/HOL: a proof assistant for higher-order logic. Vol. 2283.            semantic parsers from denotations with latent structured align-
     Springer Science & Business Media.                                            ments and abstract programs. arXiv preprint arXiv:1909.04165
[38] Despina Oikonomou. 2016. Imperatives are existential modals:                  (2019).
     Deriving the strong reading as an implicature. In Semantics and          [48] Yuk Wah Wong and Raymond Mooney. 2007. Learning synchro-
     linguistic theory, Vol. 26. 1043–1062.                                        nous grammars for semantic parsing with lambda calculus. In
[39] Steven Ovadia. 2014. Automate the internet with “if this then                 Proceedings of the 45th Annual Meeting of the Association of
     that”(IFTTT). Behavioral & social sciences librarian 33, 4                    Computational Linguistics. 960–967.
     (2014), 208–211.                                                         [49] Jim Woodcock and Jim Davies. 1996. Using Z: Specification ‚Re-
[40] Chris Quirk, Raymond Mooney, and Michel Galley. 2015. Lan-                    finement ‚and Proof. (1996).
     guage to code: Learning semantic parsers for if-this-then-that           [50] Jim Woodcock, Peter Gorm Larsen, Juan Bicarregui, and John
     recipes. In Proceedings of the 53rd Annual Meeting of the Asso-               Fitzgerald. 2009. Formal methods: Practice and experience.
     ciation for Computational Linguistics and the 7th International               ACM computing surveys (CSUR) 41, 4 (2009), 1–36.
     Joint Conference on Natural Language Processing (Volume 1:               [51] Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2sql:
     Long Papers). 878–888.                                                        Generating structured queries from natural language using rein-
[41] Siva Reddy, Oscar Täckström, Slav Petrov, Mark Steedman, and                  forcement learning. arXiv preprint arXiv:1709.00103 (2017).
     Mirella Lapata. 2017. Universal semantic parsing. arXiv preprint




                                                                          7
