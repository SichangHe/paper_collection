                                                                          Formally Verified SAT-Based AI Planning

                                                                               Mohammad Abdulaziz1,2            Friedrich Kurz2
                                                                                   1. King’s College London, The United Kingdom
                                                                                     2. Techniche Universität München, Germany




                                                                    Abstract                                Röger, and Helmert 2017. A fundamental problem with cer-
arXiv:2010.14648v5 [cs.AI] 7 Mar 2023




                                                                                                            tified computation for classical planning, as well as other
                                          We present an executable formally verified SAT encoding of        PSPACE-complete problems, is that no succinct certificates
                                          ground classical AI planning problems. We use the theorem
                                          prover Isabelle/HOL to perform the verification. We exper-
                                                                                                            exist unless NP = PSPACE (Arora and Barak 2009, Chap-
                                          imentally test the verified encoding and show that it can be      ter 4).
                                          used for reasonably sized standard planning benchmarks. We            Thirdly, there is formal verification, where system prop-
                                          also use it as a reference to test a state-of-the-art SAT-based   erties are verified by means of a mechanically checkable
                                          planner, showing that it sometimes falsely claims that prob-      formal mathematical proof. This gives the highest possi-
                                          lems have no solutions of certain lengths.                        ble trust in a program. Unlike certified computation, for-
                                                                                                            mal verification guarantees program completeness, in addi-
                                                                Introduction                                tion to its output correctness. Nonetheless, formal verifica-
                                                                                                            tion needs intensive effort, and it is usually much harder for
                                        Planning systems are becoming more and more scalable and            a formally verified program to perform as efficiently as an
                                        efficient, as shown by different planning competitions (Long        unverified program since verifying all performance optimi-
                                        et al. 2000; Coles et al. 2012; Vallati et al. 2015), making        sations is usually infeasible. Nonetheless, formal verifica-
                                        them suited for realistic applications. Since many applica-         tion has seen recent wide-spread success. Notable applica-
                                        tions of planning are safety-critical, increasing the trustwor-     tions include a verified OS kernel (Klein et al. 2009), a ver-
                                        thiness of planning algorithms and systems is instrumental          ified SAT-solver (Blanchette et al. 2018), a verified model
                                        to their widespread adoption. Consequently there currently          checker (Esparza et al. 2013), a verified conference sys-
                                        are substantial efforts to improve the trustworthiness of plan-     tem (Kanav, Lammich, and Popescu 2014), a verified opti-
                                        ning systems (Howey, Long, and Fox 2004; Eriksson, Röger,          mised C compiler (Leroy 2009), and, in the context of plan-
                                        and Helmert 2017; Abdulaziz, Norrish, and Gretton 2018;             ning, verified validators (Abdulaziz and Lammich 2018; Ab-
                                        Abdulaziz and Lammich 2018).                                        dulaziz and Koller 2022), and algorithms for bounding plan
                                           Increasing trustworthiness of software is a well-studied         lengths (Abdulaziz, Norrish, and Gretton 2018).
                                        problem. Three approaches have been tried in the litera-
                                        ture (Abdulaziz, Mehlhorn, and Nipkow 2019). Firstly, a                 Encoding planning problems as logical formulae has a
                                        system’s trustworthiness can be increased by applying soft-         long history (McCarthy and Hayes 1981). SAT-based plan-
                                        ware engineering techniques, e.g. programming at the right          ning (Kautz and Selman 1992) is the most successful such
                                        level of abstraction, code reviewing, and testing. Although         approach, where the question of whether a planning problem
                                        these practices are relatively easy to implement, they are in-      has a solution of bounded length is encoded into proposi-
                                        complete.                                                           tional (SAT) formulae. For a sound and complete encoding,
                                                                                                            a formula for a length bound (aka horizon) h is satisfiable iff
                                           Secondly, there is certified computation, where the given
                                                                                                            there is a solution with length bounded by h. A series of such
                                        program computes, along with its output, a certificate show-
                                                                                                            formulae for increasing horizons are passed to a SAT solver
                                        ing why this output is correct. This relegates the burden of
                                                                                                            until a plan is found. The encoding of Kautz and Selman
                                        trustworthiness to the certificate checker, which should be
                                                                                                            was significantly improved by exploiting problem symme-
                                        much simpler than the system whose output is to be certi-
                                                                                                            tries (Rintanen 2003), state invariants, and by parallelising
                                        fied, and thus is less error prone. Certified computation was
                                                                                                            the encodings (Rintanen, Heljanko, and Niemelä 2006). In
                                        pioneered by Mehlhorn and Näher 1998 who used it for their
                                                                                                            this paper we present a formally verified ∀-step parallel en-
                                        LEDA library. In the realm of planning, this approach was
                                                                                                            coding of classical planning (Kautz and Selman 1996; Rin-
                                        pioneered by Howey, Long, and Fox who developed the plan
                                                                                                            tanen, Heljanko, and Niemelä 2006). Using it as a reference,
                                        validator VAL (Howey, Long, and Fox 2004). Also, certify-
                                                                                                            we discover bugs in the state-of-the-art SAT-based planner
                                        ing unsolvability for planning was pioneered by Eriksson,
                                                                                                            Madagascar (Rintanen 2012). We also show that our encoder
                                        Copyright © 2023, Association for the Advancement of Artificial     is an order of magnitude slower than Madagascar, which is
                                        Intelligence (www.aaai.org). All rights reserved.                   reasonable for formally verified software.
                                                                                                                     p cnf 6 15
                                                                                                    1
Motivation Before we delve into details, we find it sensi-        1
                                                                  begin_variable
                                                                                      begin_state
                                                                                      0             begin_operator
                                                                                                                     3 0
                                                                                                                     -5 0
ble to answer the question of why to verify a SAT encod-          var1                end_state     move r0 r1
                                                                                                                     -4 0
                                                                  -1                  begin_goal    0
ing of planning? The first motivation is to demonstrate the       2                   1             1
                                                                                                                     ...
                                                                                                                     5 -6 1 0
process of formally verifying a state-of-the-art planning al-     Atom at-robby(r0)   0 1           0 0 0 1
                                                                                                                     -3 4 1 0
                                                                  Atom at-robby(r1)   end_goal      0
gorithm. Secondly, a verified planner can be used as a refer-     end_variable                      end_operator
                                                                                                                     -5 6 0
                                                                                                                     -1 1 0
ence implementation, against which unverified planners can
be tested. Thirdly, SAT encodings of planning are particu-        Figure 1: The first three listings are the concrete syntax of
larly suited for formal verification since the process of en-     a planning problem in Fast Downward’s translator format.
coding the problem into a SAT formula is not the compu-           The fourth listing is a CNF-DIMACS formula.
tational bottleneck. This means that not much effort needs
to be put into verifying different implementation optimisa-       most successful algorithm verification efforts (Klein et al.
tions. Also, importantly, verified SAT solving technology is      2009; Blanchette et al. 2018; Esparza et al. 2013; Kanav,
continuously advancing, which means that the performance          Lammich, and Popescu 2014).
of verified planning using the verified encoding will contin-        For compilers, a different approach is used: one splits
uously improve. E.g. the verified SAT solver by Blanchette        the compiler into smaller translation steps, and verifies each
et al. is one to two orders of magnitude slower than Min-         one of those steps separately. In the end, the composition of
isat (Eén and Sörensson 2003), and the verified unsatisfi-      those verified transformations is the verified compiler. This
ability certificate checker GRAT (Lammich 2017) is faster         approach was used in all notable verified compilers (Leroy
than DRAT-trim (Wetzler, Heule, and Jr 2014). Lastly, the         2009; Kumar et al. 2014). We follow this methodology.
problem of increasing trustworthiness of ‘traditional’ SAT-       Isabelle/HOL We perform the verification using the inter-
based planning was most recently raised by Eriksson and           active theorem prover Isabelle/HOL (Nipkow, Paulson, and
Helmert (2020). They stated, as an open problem, certify-         Wenzel 2002), which is a theorem prover for Higher-Order
ing that an unsatisfiable SAT formula encoding a planning         Logic. Roughly speaking, Higher-Order Logic can be seen
problem indeed shows a lower bound on the solution length.        as a combination of functional programming with logic. Is-
We address this open problem and show it is solvable with         abelle is designed for trustworthiness: following the Logic
formal verification.                                              for Computable Functions approach (LCF) (Milner 1972),
                                                                  a small kernel implements the inference rules of the logic.
Approach Overview Our approach has two focuses,                   Around the kernel there is a large set of tools that imple-
which we try to highlight in this paper. The first is minimis-    ment proof tactics and high-level concepts like algebraic
ing trusted code. To reduce the trusted code base we make         datatypes and recursive functions. Bugs in these tools can-
sure the encoder and the decoder take (produce) as input          not lead to inconsistent theorems being proved, but only to
(output) abstract syntax trees (AST) of the formats used in       error messages when the kernel refuses a proof.
the input (output) files. This way we only trust parsing and
pretty printing components. The encoder takes an AST of           Availability All theorems in this paper were formally
Fast-Downward’s translator format (Helmert 2006) as input         proved in Isabelle/HOL. We attach an appendix describing
(hereafter, FD-AST) and produces an AST of the standard           the formalisation of interesting definitions and concepts. The
DIMACS-CNF format. This DIMACS-CNF is passed to an                full formal proofs can be found at https://www.isa-afp.org/
unverified SAT solver. If the SAT solver finds a model for        entries/Verified SAT Based AI Planning.html and the veri-
the encoded formula, our verified decoder takes the AST of        fied planner based on these proofs can be found at https:
the DIMACS model and the FD-AST and produces a plan               //github.com/mabdula/Verified-SAT-Based-Planning.
only if the model entails the CNF encoding of the FD-AST.
If the SAT solver finds the formula unsatisfiable, we take                                 Background
the unsatisfiability certificate and pass it, together with the   In this paper, lists (sets) of objects are written between
DIMACS-CNF encoding, to the formally verified unsatisfi-          square brackets (curly braces). E.g. [a, b, c] ({a, b, c}) de-
ability certificate checker of Lammich 2017. Accordingly,         notes the list (set) of objects a, b and c. We also make use
all outputs of our system have formal guarantees, whether         of the choice function ch, which, for a non-empty set s, de-
the output is a plan or a conclusion that none exists.            notes an arbitrary element of s. If s = {}, ch is undefined.
   The second is engineering tradeoffs for feasible verifica-     A mapping f : V → A is a set of maplets, s.t., for every
tion. Formally verifying a reasonably big piece of software       v 7→ a ∈ f , v ∈ V and a ∈ A, and, if v 7→ a1 ∈ f and
is a daunting task. E.g. it has been reported that the size of    v 7→ a2 ∈ f , then a1 = a2 . For a mapping f , we define
the proof scripts for verifying the OS kernel seL4 is quadrat-    f (v) to be a if v 7→ a ∈ f , otherwise it is undefined. Also,
ically as big as the C implementation of the kernel (Klein        for a mapping f : V → A, D(f ) denotes {v | v 7→ a ∈ f }.
et al. 2009). Thus, a major verification effort like verifying    We call f a complete mapping iff D(f ) = V . Otherwise, we
a SAT-based planner needs careful engineering and modu-           call it a partial mapping.
larisation. For complicated algorithms, the most successful          There are multiple formalisms to represent planning and
approach is stepwise refinement, where one starts with an         logical formulae. Some of those formalisms are geared to-
abstract version of the algorithm and verifies it. Then one       wards being file formats and others are abstract formalisms
devises more optimised versions of the algorithm, and only        that are geared towards performing abstract and pen-and-
proves the optimisations correct. This approach was used in       paper reasoning. Since the main goal of our development is
to minimise trusted (i.e. unverified) code, we aim at having              The abstract syntax tree of that problem is ([(v0 , 2)], {v0 7→
our verified program (i) take as input as close a representa-             0}, {v0 7→ 1}, (move, 0, {}, {([], v0 , 0, 1)})). A solution to
tion as possible to the actual input format (i.e. Fast-Down-              this problem is [move].
ward’s translator format1 ) and (ii) produce as output a for-             We limit ourselves to problems without conditional effects
mat that is as close to the output file format as possible (i.e.          and with only consistent preconditions, defined as follows.
the DIMACS-CNF format). However, although we want our
                                                                          Definition 4 (Valid FD-AST Problem). We call a problem
verified program to operate on inputs (outputs) that are as
                                                                          (V, I, G, O) to be valid iff (i) it is well-formed, (ii) epre = ∅,
close as possible to the input (output) files, it cannot directly
                                                                          for any (name, ps, es) ∈ O and (epre, v, l, m) ∈ es,
operate on the input (output) strings. In particular, the input
                                                                          i.e. it has no conditional effects, and (iii) for any vari-
strings have to be parsed into ASTs, and the program has to
                                                                          able v ∈ D(p1 ) ∩ D(p2 ) where p1 , p2 ∈ {ps}, where
produce an output that is also an AST, which is to be pretty
                                                                          (name, ps, es) ∈ O, we have p1 (v) = p2 (v), i.e. all pre-
printed into an output file.
                                                                          conditions are consistent.
Definition 1 (FD-AST). An FD-AST is a tuple (V, I, G, O),                    To formally verify our encoding, we need to formalise the
where V : N → N is the variables section, I : N → N is                    definitions in Isabelle/HOL’s logic. As input, we use the for-
the initial state, G : N → N is the goal, and O is the set of             malisation of FD-AST developed by Abdulaziz and Lam-
operators. For each v 7→ Dv ∈ V , v stands for a variable                 mich 2018. Listing 1 in the appendix and the associated de-
and Dv is the number of assignments this variables can take.              scription review the formalisation of FD-AST.
An operator is a tuple (name, ps, es), where name is the op-                 Note that this representation of planning problems, as
erator’s name, ps : N × N is a partial mapping called the                 well as the final SAT formula, have features which make
prevail preconditions, and es is a set of effects. An effect is a         it is too cumbersome for abstract pen-and-paper reasoning.
tuple (epre, v, l, m), where epre : N → N is a partial map-               However, we need to start from representations which are
ping called the effect’s precondition and v, l, m ∈ N. If epre            as close as possible to the input/output file to reduce trusted
is non-empty the effect is called conditional.                            code. In particular, if we prove our encoding to be correct
Note: in parsing, we ignore parts of the format that are irrele-          on other more abstract representations, we will have to use
vant to our encoding, e.g. metric, mutex, and axiom sections.             trusted (i.e. unverified) pre-processing programs to convert
Definition 2 (Well-Formedness). An FD-AST (V, I, G, O)                    between the files and the more abstract representation. We
is well-formed iff (i) I is a well-formed state w.r.t. the prob-          also note that this software is only a simple parser if one
lem, (ii) G is a well-formed partial state w.r.t. the problem,            considers the input to be in FD’s translator’s format, which
(iii) all operators have distinct names, and (iv) every op-               is our claimed input. The trusted code base is significantly
erator is well-formed w.r.t. the problem. A (partial) state s             larger if one considers the input to be a PDDL domain and
is well-formed w.r.t. a problem (V, I, G, O) iff it is a (par-            instance, as the conversion then includes grounding and the
tial) mapping s.t. D(s) ⊆ D(V ), and for any v ∈ D(s),                    computation of invariants, etc.
s(v) < V (v). An operator (name, ps, es) is well-formed iff                  The rest of the paper is structured s.t. there is a section
(i) ps is a well-formed partial state, (ii) v1 6= v2 , for every          describing every intermediate representation and translation
(epre1 , v1 , l1 , m1 ), (epre2 , v2 , l2 , m2 ) ∈ es and (iii) for ev-   step, with the associated correctness theorem.
ery (epre, v, l, m) ∈ es: (iii)(1) epre is a well-formed partial
state, and (iii)(2) l, m < V (v).                                                     Translating FD-AST to FDR
Definition 3 (Execution). An operator (name, ps, es) is ex-               Although we can define our encoding directly on FD-AST,
ecutable in a state s iff ps ⊆ s and, for each effect                     we opted to firstly translate the FD-AST to the Finite Do-
(epre, v, l, m) ∈ es, v 7→ l ∈ s, if 0 ≤ l. The state resulting           main Representation (FDR), which is another representation
from executing the operator is                                            of planning problems with multi-valued state variables. FDR
                                                                          is more abstract than FD-AST. This facilitates smoother for-
   (s \ {v 7→ l | ∃(epre, v, l, m) ∈ es ∧ epre ⊆ s})∪                     mal reasoning, e.g. it is more suitable for stating algorithms
               {v 7→ m | ∃(epre, v, l, m) ∈ es ∧ epre ⊆ s},               and theorem statements, while FD-AST is a file format. In
 i.e. it is the same as s, except that it assigns variables ac-           most expositions in planning literature, there is not a dis-
cording to the effects whose preconditions are satisfied.                 tinction between file formats and the abstract formalisms on
   A solution to a problem P is a list of names                           which algorithms and theorems are stated. The actual im-
[name1 , name2 , . . . namen ] s.t. there is a mapping sol :              plementations, however, start from a file format, like Fast
{name1 . . . namen } → O s.t. sol(namei ) ∈ O, for                        Downward’s translator format, which is simplified to a more
all 1 ≤ i ≤ n, and the sequence of operators                              abstract formalism. In our case, nonetheless, we make the
[sol(name1 ), sol(name2 ), . . . sol(namen )] are executable in-          distinction between the two formalisms since our main goal
order starting at I, and the goal is a subset of the state re-            is a formal correctness guarantee on an implementation of a
sulting from executing all operators.                                     planner, including the translation of FD-AST to FDR.
Example 1. Figure 1 shows a planning problem in Fast                      Definition 5 (Finite Domain Representation). An FDR plan-
Downward’s translator syntax that models a robot that is                  ning problem Ψ is a tuple (V, R, I, O, G), where V is the set
in one room and whose goal is to move to another room.                    of state variables, R : V → Av is mapping from variables
                                                                          to sets of assignments, O is a set of operators, I is the ini-
   1
       http://www.fast-downward.org/TranslatorOutputFormat                tial state, and G is the goal. Each variable (operator) has a
unique natural number index, where, for a variable v ∈ V               [op01 , op02 , . . . ] are the operators from the given FDR plan
(operator op ∈ O), its index is 0 ≤ vi <S|V | (0 ≤ opi <               whose preconditions are satisfied.
|O|). For FDR, a (partial) state s : V → {R(v) | v ∈ V }
is a mapping, and D(s) = {v | v 7→ a ∈ s}. A (par-                     Proof sketch. Both statements are proved by induction on
tial) state s is valid iff for any v 7→ a ∈ s we have that             the length of the given plan, while generalising over the ini-
a ∈ R(v). A valid operator is a pair of valid partial states           tial state of P , and then careful unfolding of Definitions 1,
op = (p, e), where p is the precondition, denoted by p(op),            2, 3, 4, 5, Encoding 1 and Decoding 1.
and e is the effect, denoted by e(op). We denote the the               Note: since FDR execution function is total, while that of
execution of a sequence of operators ops at a state s by               FD-AST is not, operators whose preconditions are not satis-
ops(s), and it is defined as follows: if ops is not empty              fied have to be removed when decoding the FDR plan.
and if for the first operator (p, e) in ops we have p ⊆ s                 Before we close this section we note a few points re-
then ops(s) = ops0 (op(s)), where ops0 is the tail (i.e. ev-           garding the formal proof of the above theorem. The proof
ery element but the first) of ops and op(s) is defined to be           of this theorem does not have complicated mathematical
{v 7→ a | if v ∈ D(e) then a = e(v ) else s(v )}. Other-               ideas or constructions. However, the main difficulty is cor-
wise, ops(s) = s. Ψ is a valid FDR problem iff I is a valid            rectly formulating the definitions of well-formed and valid
state, G is a valid partial state, and O is a set of valid op-         FD-ASTs, valid FDRs and the encoding and the decoding.
erators. A solution for Ψ is an operator sequence ops where            Due to the many conjuncts and components of these defini-
all operator in ops come from O and G ⊆ ops(I).                        tions, their interactions make formally stating these defini-
Note: in contrast to FD-AST plan execution semantics, FDR              tions and proving the theorem a very error-prone and cum-
execution semantics are defined as a total function, where             bersome process. E.g. a detail in the formal proof, which
plan execution always returns the last state reached before            would be glossed over in a pen-and-paper treatment, is to
the first operator whose preconditions are not satisfied. A            show that encoding a well-formed valid FD-AST results in a
total execution function makes many of the formal proofs               valid FDR, which is necessary for using the different the-
easier.                                                                orems about FDR problems. Proving that depends on the
   Translating FD-ASTs into FDR problems is done using                 assumption that the AST operators have no conditional ef-
the following encoding.                                                fects, a fact which we only understood during our develop-
Encoding 1. For an FD-AST problem P = (V, I, G, O),                    ment of the formal proof. To overcome these difficulties, we
let FDRV = {v | ∃n. (v, n) ∈ V } and FDRR = {v 7→                      employed deliberate engineering efforts to make the formal
{0 . . . n − 1} | (v, n) ∈ V }. For an FD-AST effect e =               proof more modular. E.g. we split the encoding of FD-AST
(epre, v, l, m), let eold denote v 7→ l and enew denote v 7→           operator to FDR operators into multiple stages. First, the ef-
m. For an operator op = (name, ps, es), let FDRO (op) =                fect preconditions are removed and added into the operator’s
(ps ∪ {eold | e ∈ es}, {enew | e ∈ es}). For the FD-AST                preconditions, resulting in a simpler FD-AST, with no effect
problem P , its encoding as an FDR problem, FDR(P ), is                preconditions. Then, we define a function to encode these
(FDRV , FDRR , I, {FDRO (op) | op ∈ O}, G).                            simpler FD-ASTs into FDRs. More details on these proof
                                                                       engineering efforts are in the appendix.
   For the other direction of this encoding, we devise a de-
coding function AST that, given a solution for the FDR                             Translating FDR to STRIPS
problem FDR(P ), decodes it into a solution for P .
                                                                       Since a SAT encoding only has propositional variables, we
Decoding 1. First, for a set s let ch(s) denote an arbi-               need to compile the multi-valued state variables of FDR to
trary element of s if s is not empty, and undefined other-             propositional values. Instead of performing the compilation
wise. For an FDR operator op, let AST (op) = ch{name |                 of the multi-valued variables together with the compilation
FDRO ((name, ps, es)) = op}, where O are the operators in              of the transition relation in one step, we opted to do them
P.                                                                     in separate steps, where we first compile FDR problems to
Example 2. The compiled FDR equivalent to the FD-AST                   STRIPS problems and then compile STRIPS problems into
problem P in Example 1, FDR(P ), is                                    SAT formulae. This decision is not of much theoretical im-
  
           FDRV = {v0 }, FDRR = {v0 7→ {0, 1}},
                                                                      portance, but more geared towards making the verification
                                                                 ,     more modular and thus more manageable.
    I = {v0 7→ 0}, FDRO = {op0 }, FDRG = {v0 7→ 1}
                                                                       Definition 6 (STRIPS Problem). An FDR problem Π =
 where op0 = ({v0 7→ 0}, {v0 7→ 1}).
                                                                       (V, R, I, O, G) is a STRIPS problem iff R(v) = {⊥, >}, for
   The following theorem represents the soundness and com-             all v ∈ V . When constructing STRIPS mappings, we denote
pleteness of this compilation step.                                    v 7→ > with v and v 7→ ⊥ with v.
Theorem 1. Let P be a valid FD-AST problem. We                         Encoding 2. Consider an FDR problem Ψ                     =
have that: (i) if [name1 , name2 , . . . ] is a plan for               (V, R, I, O, G). Our FDR problem compiled to STRIPS is
P then [FDRO (ch(Oname1 ), FDRO (Oname2 ), . . . ] is a                             ϕ = {(v, a) | a ∈ R(v) ∧ v ∈ V }, 
                                                                                         V
plan for the FDR task FDR(P ), where, for namei ,
                                                                                   ϕR = {(v, a) 7→ {>, ⊥} | (v, a) ∈ ϕV },
Onamei = {op | ∃ ps0 es0 .op ∈ O ∧ op = (namei , ps0 , es0 )},            ϕ(Ψ) =                                             ,
and (ii) if [op1 , op2 , . . . ] is a plan for the FDR task FDR(P ),                              ϕS (I), ϕS (G),            
then [AST (op01 ), AST (op02 ), . . . ] is a plan for P , where                       ϕO = {(ϕS (p), ϕS (e)) | (p, e) ∈ O}.
where, for a (partial) state s, ϕS (s) is defined as                     Encoding 3. Consider a given natural number h and a
   {(v, a) | s(v) = a ∧ v ∈ D(s)}∪                                       STRIPS problem Π = (V, R, I, O, G). For a STRIPS state
                                                                         s, let st denote the propositional formula
       {(v, a) | s(v) 6= a ∧ v ∈ D(s) ∩ V ∧ a ∈ R(v)}                     ^                                  ^
                                                                         ( v ∈ {v | v 7→ > ∈ s}. v t ) ∧ ( v ∈ {v | v ∈ s}. ¬v t )
Example 3. Consider the FDR problem FDR(P ) in exam-
ple 2. For that FDR problem, we have                                      Also, for a variable v ∈ V , let add(v) = {(p, e) | v ∈ e} ∩

                  ϕV = {(v0 , 0), (v0 , 1)},
                                                                        O and del(v) = {(p, e) | v ∈ e} ∩ O. The encoding Φ(Π, h)
                                                                         is the conjunction of the following propositional formulae:
       ϕR = {(v0 , 0) 7→ {⊥, >}, (v0 , 1) 7→ {⊥, >}},
                                                                                                        I0
                                                             
                                                                                                                                  (i)
ϕS (I) = {(v0 , 0), (v0 , 1)}, ϕS (G) = {(v0 , 0), (v0 , 1)},
                                                             
                                                                                                          Gh                              (ii)
        ϕO = {({(v0 , 0), (v0 , 1)}, {(v0 , 0), (v0 , 1)})}                    ^                 ^
                                                                                                                 t            t
                                                                                   t ∈ {0..h}.       op ∈ O. op −→ p(op) ∧
Decoding 2. For an FDR problem Ψ = (V, R, I, O, G) and                                                                                   (iii)
an operator (p, e) ∈ ϕO , let                                                                                   opt −→ e(op)t+1
 ϕ−1
  O (p, e) = ({v 7→ a | (v, a) ∈ p}, {v 7→ a | (v, a) ∈ e})
                                                                                   ^                 ^
                                                                                       t ∈ {1..h}.       v ∈ V. ¬v t−1 ∧ v t −→
Note: we ignore negative effects when decoding STRIPS op-                                                     _                          (iv)
erators since they only ensure operator effect consistency.                                                      op ∈ add(v). opt
   The soundness and completeness theorems of this encod-                          ^                 ^
ing of FDR problems follow.                                                            t ∈ {1..h}.       v ∈ V. v t−1 ∧ ¬v t −→
                                                                                                              _                           (v)
Theorem 2. For a valid FDR problem Ψ (i) if                                                                        op ∈ del(v). opt
[op0 , . . . , opk ] solves the STRIPS problem Π = ϕ(Ψ), then              ^                 ^
ψ = [ϕ−1                       −1                                              t ∈ {1..h}.       (op, op0 ) ∈ intrfr(O). opt ∨ ¬op0t (vi)
            O (op0 ), . . . , ϕO (opk )] is a solution for Ψ. (ii) if
[op0 , . . . , opk ] solves Ψ, then π = [ϕO (op0 ), . . . , ϕO (opk )]   This encoding is defined over the atoms
solves the STRIPS problem ϕ(Π).                                          {v t | v ∈ V ∧ 0 ≤ t ≤ h} ∪ {opt | op ∈ O ∧ 0 ≤ t < h}
Proof sketch. (i) We show that G ⊆ ψ(I) and moreover                        In the encoding above the first conjunct stands for the ini-
ϕ−1                  −1
  O (op0 ), . . . , ϕO (opk ) ∈ O where G and O are the goal             tial state, the second for the goal, the third for the transi-
state respectively operator set of Ψ. The first part of the proof        tion relation, the fourth and fifth are the frame axioms, and
is by induction over π with arbitrary initial state.                     the last is a constraint ensuring that if more than one oper-
(ii)We show that G               ⊆     π(I) and moreover                 ator execute in the same step, they are not interfering op-
ϕO (op0 ), . . . , ϕO (opk ) ∈ O where G and O are the                   erators. Also note that the actual encoding we verified only
goal state respectively operator set of Π. The first part of the         computes the formula in CNF form, but we use syntactic
proof is by induction over ψ with arbitrary initial state.               sugar in our definition
                                                                                             W and examples to improve readability,
                                                                         e.g. x1 ∧ x2 −→ y ∈ {y1 , y2 , ..}.yVis syntactic sugar for
        Encoding STRIPS Problems as SAT                                  ¬x1 ∨ ¬x2 ∨ y1 ∨ y2 .., and x −→ y ∈ {y1 , y2 , ..}.y is
In this step we encode the question of whether a STRIPS                  syntactic sugar for (¬x ∨ y1 ) ∧ (¬x ∨ y2 ) ∧ ...
problem has a plan of length at most h into a propositional              Example 4. Consider the STRIPS problem ϕ(FDR(P ))
satisfiability formula. In our formalisation, we use Michaelis           from Example 3. Let h = 1 be the horizon. The encoding
and Nipkow’s formalisation of propositional logic. Due to                is the conjunction of
lack of space and since they are standard, we only describe
its syntax and semantics in the appendix. The specific encod-                                (v0 , 0)0 ∧ ¬(v0 , 1)0          (i)
ing we use is similar to the parallel ∀-step encoding used by                                    ¬(v0 , 0)1 ∧ (v0 , 1)1                   (ii)
Rintanen, Heljanko, and Niemelä. We limit operators to ones                            (op00 −→ (v0 , 0)0 ∧ ¬(v0 , 1)0 )∧
without conditional effects, require a total initial state, and                                                                          (iii)
constrain preconditions and the goal to conjunctions of liter-                               (op00 −→ ¬(v0 , 0)1 ∧ (v0 , 1)1 )
als. These restrictions are always satisfied by problems pro-                            (¬(v0 , 0)0 ∧ (v0 , 0)1 −→ ⊥)∧
duced by Encoding 2. Informally, such a parallel encoding                                                                                (iv)
constitutes an unrolling of the transition relation underlying                             (¬(v0 , 1)0 ∧ (v0 , 1)1 −→ op00 )
the STRIPS problem, which allows more than one operator                                 ((v0 , 0)0 ∧ ¬(v0 , 0)1 −→ op00 )∧
to execute in one time step, as long as those operators are                                                                               (v)
                                                                                               ((v0 , 1)0 ∧ ¬(v0 , 1)1 −→ ⊥)
non-interfering. This allows for the encoding to be signifi-
cantly more compact in practice, compared to only allowing                                                 >                             (vi)
one operator per step.                                                   Decoding 3. Consider a horizon h, a STRIPS problem
Definition 7 (Interference). Two STRIPS operators o1 =                   Π = (V, R, I, O, G) and a model M  Φ(Π, h). Let, for
(p1 , e1 ) and o2 = (p2 , e2 ) are interfering iff {v | v 7→ > ∈         a set s, list(s) denote an arbitrary list which contains all
pi }∩{v | v 7→ ⊥ ∈ ej } =  6 ∅, for all i 6= j, and i, j ∈ {1, 2}.       the elements of s, s.t. |s| = |list(s)|. Let for a list of lists
For a set of STRIPS operators O, we denote the set of pairs              ls = [l0 , l1 , ..], flat(ls) denote the list l0 _l1 , .., where _ is
of interfering operators in O by intrfr(O).                              the list append function. The decoding function is defined
Φ−1 (Π, h, M) = flat([list({op | op0 ∈ M}), list({op |                       ∃φ1 , φ2 . φ = φ1 ∨ φ2 , (ii) [], if φ = ⊥, (iii) [−1, 1], if
op1 ∈ M}), .., list({op | oph−1 ∈ M})]).                                     φ = >, (iv) [−simp(φ0 )], if ∃φ0 . φ = ¬φ0 , and (v) [int(φ)],
Example 5. For the propositional formula in Example 4, a                     if φ is an atom. Let simp(φ) be defined recursively as fol-
                                                                             lows:(i) simp(φ1 )_simp(φ2 ), if ∃φ1 , φ2 . φ = φ1 ∧ φ2 and
model is {(v0 , 0)0 , (v0 , 1)0 , (v0 , 0)1 , (v0 , 1)1 , op00 }. The de-
                                                                             (ii) [simpORs(φ)] otherwise.
coded plan is [op0 ].
                                                                             Note: int and var are adapted from Knuth 1998, Section 4.4
   This translation to SAT is sound and complete.                            on encoding numbers with arbitrary radixes. Also, note that
Theorem 3. For a valid STRIPS problem Π and a hori-                          simp is only well-defined if the given formula is a CNF,
zon h:(i) if M is a model for Φ(Π, h), then Φ−1 (Π, h, M)                    which is not problematic since the formulae produced by Φ
is a solution for Π and (ii) if ops is a solution for Π and                  are CNF for a valid STRIPS problem.
|ops| ≤ h, then there is a model for Φ(Π, h).                                Example 6. Consider the CNF formula from Example 4.
Proof sketch. (i) This proof is by induction on the horizon,                 First consider the following two orderings for the vari-
with generalising the initial state. It depends, crucially, on               ables encoding operators and state variables: [op0 ] and
the fact that non-interference implies that any order of oper-               [(v0 , 0), (v0 , 1)]. The mapping of the time indexed vari-
ators coming from a single step is executable.                               ables to natural numbers is: int(op00 ) = 1, int(op10 ) = 2,
(ii) Let the operators in ops be [op0 , op1 , .., op|ops|−1 ]. We            int((v0 , 0)0 ) = 3, int((v0 , 0)1 ) = 4, int((v0 , 1)0 ) = 5,
                                                                             and int((v0 , 1)1 ) = 6. Applying simp to that formula re-
construct a model for Φ(Π, h) by considering the sequence
                                                                             sults in [[3], [−5], [−4], [6], [−1, 3], [−1, −5], [−1, −4], [−1,
of states traversed by executing the plan π at I, which can
                                                                             6], [3, −4], [5, −6, 1], [−3, 4, 1], [−5, 6], [−1, 1]]. This AST is
be recursively specified as s0 = I, and st+1 = opt (st ) for
                                                                             then pretty printed as DIMACS-CNF concrete syntax, like
0 < t ≤ h. The model we construct is
                                                                             the one in Fig. 1, which only shows 7 clauses.
    {optt | 0 ≤ t < |ops|}∪
                                                                             Decoding 4. Consider a DIMACS-CNF AST encoding a
       {optt | 0 ≤ t 6= t0 < |ops|} ∪ {stt | 0 ≤ t ≤ |ops|}
            0
                                                                             STRIPS problem (V, R, I, O, G) and a horizon h. Let,
                                                                             for an integer n, the function var(n) be defined as:
                                                                             (i) (O(|n|−1 mod h))(|n|−1)÷h , if |n| < 1+h|O| (ii) (V(k
   Before we conclude, we note that other encoding methods                   mod h))k÷h , where k = |n| − h|O| − 1, otherwise. Now, let
from FDR to SAT have also been proposed, e.g. Balyo 2013.                    lit(n) be the literal var(n), if 0 < n, and ¬var(n) otherwise.
        Abstract SAT Formulae to DIMACS                                      The correctness theorem for this step is as follows.
The SAT formulae produced by Encoding 3 are structured                       Theorem 4. For a valid STRIPS problems Π and a hori-
in the following way: (i) the formulae use the connectives                   zon h: (i) if {l1 , l2 , ..} is a model for Φ(Π, h), then
∧, ∨, → and ¬ and (ii) atoms representing state variables                    {simp(l1 ), simp(l2 ), ..} is a model for simp(Φ(Π, h)), and
and operators are indexed by the time step. In a pen-and-                    (ii) if [n1 , n2 , ..] is a model for simp(Φ(Π, h)), then
paper exposition this would be enough. However, this is                      {lit(n1 ), lit(n2 ), ..} is a model for Φ(Π, h).
not enough in our case because there is still an encoding
                                                                             Proof sketch. The proof of both statements is by structural
step to simplify these structured formulae to DIMACS-CNF,
                                                                             induction on the formula Φ(Π, h).
which is the representation of SAT formulae used in prac-
tice, and we do not want to trust that step. Thus, as a last                   The overall encoding correctness follows (Listing 4).
step, we present the following encoding of structured formu-
lae to DIMACS-CNF ASTs. That encoding has to simplify                        Theorem 5. For a valid FD-AST P and a horizon h: (i) if
the connectives as well as replace the structured variables                  [n1 , n2 , ..] is a model for simp(Φ(ϕ(FDR(P )), h)) then a
with integers.                                                               plan for P is [AST (ϕ−1                    −1
                                                                                                      O (op1 )), AST (ϕO (op2 )), ..], where
                                                                                                   −1
                                                                             [op1 , op2 , ..] = Φ (Π, h, {lit(n1 ), lit(n2 ), ..}), and (ii) if
Definition 8 (DIMACS-CNF). A DIMACS-CNF AST is a                             [name1 , name2 , .., nameh ] is a plan for P , then there is a
list of lists of non-zero integers. A list of non-zero integers              model for simp(Φ(ϕ(FDR(P )), h)).
[l1 , l2 , .., lm ] is a model for a DIMACS-CNF AST [c1 =
[l11 , l12 ..], c2 = [l21 , l22 ..], .., cn = [ln1 , ln2 ..]] iff for each   Proof sketch. From Theorems 1, 2, 3 and 4.
ci , for 1 ≤ i ≤ n, there is lj ∈ ci , where 1 ≤ j ≤ m, and,
for each 1 ≤ j, k ≤ m, lj 6= −lk .
Encoding 4. For a STRIPS problems (V, R, I, O, G),                                          Experimental Evaluation
fix an arbitrary ordering V (O) of V (O) s.t. for a                          We use Isabelle/HOL’s code generator to generate a Stan-
state variable (operator) v (op), vi (opi ) is the index                     dard ML implementation of our correct encoding. Readers
of v (op) in V (O). For an atom a and a horizon h,                           interested in implementation details can inspect the attache-
let int(a) be defined as: (i) 1 + t + opi (h + 1), if                        ment. We evaluate the performance of our encoding com-
∃opt . a = opt and (ii) 1 + |O|(h + 1) + t + vi (h + 1)                      pared to the ∀-step encoding of Rintanen, Heljanko, and
if ∃v t . a = v t . For a propositional formula φ that                       Niemelä 2006 as computed by Madagascar when invariant
has no conjunctions, let simpORs(φ) be defined re-                           generation is disabled. Although this setup has a weakness,
cursively as follows:(i) simpORs(φ1 )_simpORs(φ2 ), if                       namely, that Madagascar takes the PDDL domain as input
                               SAT                               UNSAT                 encodings of some Rovers instances, while it succeeds for
                  Madagascar    Verified Encoding   Madagascar     Verified Encoding   our encodings. We note that Madagascar’s ∀-step encoding
     newopen        3128             2897             2214               2205
                                                                                       is linear in size due to the use of auxiliary variables to repre-
     logistics       986              358             1031               452
                                                                                       sent the operator interference clauses, while ours is quadratic
     elevators       75                14              61                 44
                                                                                       (see Fig. .3). A hypothesis is that auxiliary variables inter-
      rover          270              233              172               121
                                                                                       fere with Kissat’s deduction mechanisms, as has been re-
     storage         66                35              41                 33
                                                                                       ported about compact encodings in other contexts (Knuth
    pipesworld       46                9               74                 7
                                                                                       2015)[Section 7.2.2.2]. However, this needs further study.
    nomystery        83                13              197                15
                                                                                       (ii) Since our verified implementation is purely functional
       zeno          180               54              70                 28
                                                                                       in Standard ML, computing our encoding takes longer time
      hiking         45                6               100                11
                                                                                       than Madagascar’s, e.g. we use balanced trees instead of ar-
       TPP           106               46              71                 30
                                                                                       rays, causing every access/update to be worst-case logarith-
    Transport        78                2               134                18
                                                                                       mic instead of constant time. This leads to our encoding to
      GED            68                19              105                19
                                                                                       have a worse total (i.e. grounding, encoding and solving)
   woodworking       99                51              17                 20
                                                                                       running time, despite the fact that our encoding is usually
      visitall       74                53              279               131
                                                                                       solvable in shorter time (see Fig. .4). A bigger problem is
    openstacks       62               —                316                62
                                                                                       that, as Standard ML does not support lazy evaluation and
     satellite       46                34              20                 20
                                                                                       has poor memory management in general, our encoding fre-
    scanalyzer       88                4               88                 9
                                                                                       quently runs out of memory as it computes the entire en-
     tidybot         24               —                12                 —
                                                                                       coding in memory before producing any output (see Fig. .5).
      trucks         45                8               117                29
                                                                                       This leads to less of our encodings being solved by Kissat
    parcprinter      113               63              128               111
                                                                                       compared to the ones produced by Madagascar (see Table 1).
   maintenance       35                34              —                  —
      pegsol         114               3               200               237
   blocksworld       31                25              30                 30
     floortile       221               54              361               281                                    Discussion
     barman          20               —                208                34
    Thoughtful       —                —                —                  5            We presented an executable formally verified SAT encoding
                                                                                       of AI planning. We showed details of the verification pro-
Table 1: Number of solved satisfiable and unsatisfiable for-                           cess, and experimentally tested our encoding. Experiments
mulae solved by Kissat for our encoding and the encoding                               show that, although our verified encoder is primarily hin-
generated by Madagascar.                                                               dered by its memory consumption, it can handle planning
                                                                                       problems of reasonable sizes, where it can solve, or show
                                                                                       bounded length plan non-existence. By testing Madagas-
while our system takes the grounded output of Fast Down-                               car’s encoding against our verified encoding, we discovered
ward’s translator, it should indicate the scalability of the ver-                      that Madagascar sometimes mistakenly claims that prob-
ified encoding and can be used to test Madagascar’s com-                               lems have no solutions of a certain length. Also, compared to
pleteness. We compute the encodings of different planning                              Madagascar, our encoding can be more efficiently processed
domains from previous competitions and then feed them                                  by the SAT solver Kissat. The size of the verified Standard
to the SAT solver Kissat, opting for a 30 minutes time-                                ML program is around 1.2K lines of code, and the size of
out and a 8GB memory limit for encoding and solving.                                   the formal proof is around 17.5K lines of proof scripts.
We generate the encodings for horizons 2, 5, 10, 20, 50,                                  One goal of our work here is to showcase theorem prov-
100, and the bounds generated by the algorithm of Abdu-                                ing and its application to verification as a methodology to in-
laziz 2019. We record a few findings. Firstly, we found a                              crease trustworthiness of planning software and, more gen-
bug in Madagascar: it produces unsatisfiable formulae for in-                          erally, AI software. Although there are other approaches to
stances and horizons, despite those instances having ∀-step                            increase reliability of AI systems, most notably certification
plans bounded by the horizon. This happens in at least 24 in-                          for planning or SMT-based methods for verifying properties
stances of different variants of the Rovers and PARCPrinter                            of neural networks, we believe that correct-by-construction
domains. This is because Madagascar adds incorrect action                              algorithms have their niche. For instance, this is the case
mutex constraints which rule out valid ∀-step plans, thus                              when there are not general certification methods or when de-
causing Madagascar to not be complete. The fact that such a                            sired formal properties are too complex for automated meth-
well-established planning system has such bugs demonstrate                             ods to practically handle.
that it is imperative we verify planning systems, especially                              As future work, the most interesting direction is to verify
that there no generally succinct unsolvablity certificates do                          the encoding of costs by Abdulaziz 2021, yielding formally
not exist for AI planning algorithms.                                                  verified certificates of cost optimality. Another direction is
   Secondly, we compare the performances of our encod-                                 optimising the memory consumption of our implementation,
ing and Madagascar. (i) For most instances, our encoding                               e.g. via lazy evaluation (Lochbihler and Stoop 2018), or by
is solved by Kissat in significantly shorter time than Mada-                           using a low-level target language instead of Standard ML,
gascar (see Fig. .2). Kissat fails to terminate on Madagascar                          like LLVM (Lammich 2022).
                        References                                Kanav, S.; Lammich, P.; and Popescu, A. 2014. A Confer-
Abdulaziz, M. 2019. Plan-Length Bounds: Beyond 1-Way              ence Management System with Verified Document Confi-
Dependency. In The 33rd AAAI Conference on Artificial In-         dentiality. In The 26th International Conference on Com-
telligence (AAAI).                                                puter Aided Verification (CAV).
                                                                  Kautz, H. A.; and Selman, B. 1992. Planning as Satisfiabil-
Abdulaziz, M. 2021. Cost Optimal Planning as Satisfiabil-         ity. In 10th European Conference on Artificial Intelligence
ity. In The Workshop on Heuristics and Search for Domain-         (ECAI).
Independent Planning (HSDIP).
                                                                  Kautz, H. A.; and Selman, B. 1996. Pushing the Envelope:
Abdulaziz, M.; and Koller, L. 2022. Formal Semantics and          Planning, Propositional Logic and Stochastic Search. In
Formally Verified Validation for Temporal Planning. In The        13th National Conference on Artificial Intelligence (NCAI).
36th AAAI Conference on Artificial Intelligence (AAAI).           Klein, G.; Elphinstone, K.; Heiser, G.; Andronick, J.; Cock,
Abdulaziz, M.; and Lammich, P. 2018. A Formally Verified          D.; Derrin, P.; Elkaduwe, D.; Engelhardt, K.; Kolanski, R.;
Validator for Classical Planning Problems and Solutions. In       Norrish, M.; Sewell, T.; Tuch, H.; and Winwood, S. 2009.
The 30th International Conference on Tools with Artificial        seL4: Formal Verification of an OS Kernel. In 22nd ACM
Intelligence (ICTAI).                                             Symposium on Operating Systems Principles 2009 (SOSP).
Abdulaziz, M.; Mehlhorn, K.; and Nipkow, T. 2019. Trust-          Knuth, D. E. 1998. The Art of Computer Programming, Vol-
worthy Graph Algorithms (Invited Paper). In The 44th Inter-       ume II: Seminumerical Algorithms, 3rd Edition.
national Symposium on Mathematical Foundations of Com-            Knuth, D. E. 2015. The Art of Computer Programming, Vol-
puter Science (MFCS).                                             ume 4, Fascicle 6: Satisfiability.
Abdulaziz, M.; Norrish, M.; and Gretton, C. 2018. Formally        Kumar, R.; Myreen, M. O.; Norrish, M.; and Owens, S.
Verified Algorithms for Upper-Bounding State Space Diam-          2014. CakeML: A Verified Implementation of ML. In The
eters. J. Autom. Reason.                                          41st Symposium on Principles of Programming Languages
                                                                  (POPL).
Arora, S.; and Barak, B. 2009. Computational Complexity -
A Modern Approach.                                                Lammich, P. 2017. The GRAT Tool Chain - Efficient
                                                                  (UN)SAT Certificate Checking with Formal Correctness
Balyo, T. 2013. Relaxing the Relaxed Exist-Step Parallel          Guarantees. In SAT.
Planning Semantics. In 25th IEEE International Conference         Lammich, P. 2022. Refinement of Parallel Algorithms down
on Tools with Artificial Intelligence (ICTAI).                    to LLVM. In 13th International Conference on Interactive
Blanchette, J. C.; Fleury, M.; Lammich, P.; and Weidenbach,       Theorem Proving (ITP).
C. 2018. A Verified SAT Solver Framework with Learn,              Leroy, X. 2009. Formal Verification of a Realistic Compiler.
Forget, Restart, and Incrementality. J. Autom. Reason.            Commun. ACM.
Coles, A. J.; Coles, A.; Olaya, A. G.; Celorrio, S. J.; López,   Lochbihler, A.; and Stoop, P. 2018. Lazy Algebraic Types
C. L.; Sanner, S.; and Yoon, S. 2012. A Survey of the Sev-        in Isabelle/HOL. In Isabelle Workshop.
enth International Planning Competition. AI Mag.                  Long, D.; Kautz, H. A.; Selman, B.; Bonet, B.; Geffner, H.;
Eén, N.; and Sörensson, N. 2003. An Extensible SAT-solver.      Koehler, J.; Brenner, M.; Hoffmann, J.; Rittinger, F.; Ander-
In Internation Conference on Theory and Applications of           son, C. R.; Weld, D. S.; Smith, D. E.; and Fox, M. 2000. The
Satisfiability Testing (SAT).                                     AIPS-98 Planning Competition. AI Mag.
Eriksson, S.; and Helmert, M. 2020. Certified Unsolvability       McCarthy, J.; and Hayes, P. J. 1981. Some Philosophi-
for SAT Planning with Property Directed Reachability. In          cal Problems from the Standpoint of Artificial Intelligence.
The 30th International Conference on Automated Planning           Readings in Artificial Intelligence.
and Scheduling (ICAPS).                                           Mehlhorn, K.; and Näher, S. 1998. From Algorithms to
                                                                  Working Programs: On the Use of Program Checking in
Eriksson, S.; Röger, G.; and Helmert, M. 2017. Unsolvabil-       LEDA. In 23rd International Symposium Mathematical
ity Certificates for Classical Planning. In The 27th Interna-     Foundations of Computer Science (MFCS).
tional Conference on Automated Planning and Scheduling
(ICAPS).                                                          Michaelis, J.; and Nipkow, T. 2018. Formalized Proof Sys-
                                                                  tems for Propositional Logic. In The 23rd International
Esparza, J.; Lammich, P.; Neumann, R.; Nipkow, T.;                Conference on Types for Proofs and Programs (TYPES).
Schimpf, A.; and Smaus, J.-G. 2013. A Fully Verified Exe-         Milner, R. 1972. Logic for Computable Functions Descrip-
cutable LTL Model Checker. In 25th International Confer-          tion of a Machine Implementation. Technical report, Stan-
ence on Computer Aided Verification (CAV).                        ford University.
Helmert, M. 2006. The Fast Downward Planning System. J.           Nipkow, T.; Paulson, L. C.; and Wenzel, M. 2002. Is-
Artif. Intell. Res.                                               abelle/HOL - A Proof Assistant for Higher-Order Logic.
Howey, R.; Long, D.; and Fox, M. 2004. VAL: Automatic             Rintanen, J. 2003. Symmetry Reduction for SAT Rep-
Plan Validation, Continuous Effects and Mixed Initiative          resentations of Transition Systems. In The 13th Interna-
Planning Using PDDL. In 16th IEEE International Con-              tional Conference on Automated Planning and Scheduling
ference on Tools with Artificial Intelligence (ICTAI).            (ICAPS).
Rintanen, J. 2012. Planning as Satisfiability: Heuristics. Ar-
tif. Intell.
Rintanen, J.; Heljanko, K.; and Niemelä, I. 2006. Plan-
ning as Satisfiability: Parallel Plans and Algorithms for Plan
Search. Artif. Intell.
Vallati, M.; Chrpa, L.; Grzes, M.; McCluskey, T. L.; Roberts,
M.; and Sanner, S. 2015. The 2014 International Planning
Competition: Progress and Trends. AI Mag.
Wetzler, N.; Heule, M.; and Jr, W. A. H. 2014. DRAT-trim:
Efficient Checking and Trimming Using Expressive Clausal
Proofs. In International Conference on Theory and Applica-
tions of Satisfiability Testing (SAT).
                                                                     38   definition execute :: name ⇒ state ⇒ state
        Appendix: Formalisation of Different                                where execute name s =
                                                                     40       case lookup_operator name of
            Concepts in Isabelle/HOL                                            Some (_,_,effs,_) ⇒
                                                                     42           s ++ map_of (map (λ(_,x,_,v). (x,v)) (filter (
Isabelle/HOL’s syntax Isabelle’s syntax is a variation of                               eff_enabled s) effs))
                                                                              | None ⇒ undefined
Standard ML combined with standard mathematical nota-                44   fun path_to
tion. Function application is written infix, and functions can              where path_to s [] s' ←→ s'=s
                                                                     46     | path_to s (π#πs) s' ←→
be curried, i.e. function f applied to arguments x1 . . . xn                  enabled π s ∧ path_to (execute π s) πs s'
is written as f x1 . . . xn instead of the standard nota-            48   definition valid_plan :: plan ⇒ bool
                                                                            where valid_plan πs = ∃s' ∈ G. path_to I πs s'
tion f (x1 , . . . , xn ). Also, it supports lambda terms, e.g.
λx y. x + y represents a function that takes two arguments
and adds them.                                                          To formally verify the encoding, we formalise the defi-
   We make use of the following predefined functions in Is-          nitions of planning problems, SAT formulae, and their se-
abelle/HOL:(i) map is the high-order function that returns a         mantics in the language of Isabelle/HOL. Referring to List-
list after applying a function to each element of a given list,      ing 1, we now review the formalisation of the definitions of
(ii) fst and snd are functions that extract the first and sec-       FD-AST and DIMACS-CNF to give the reader a feel of this
ond members of a pair, (iii) distinct is predicate meaning           process and because the main theorems are stated in terms
that elements of a list are distinct, (iv) filter is a high-         of them. However, in the rest of the paper we only show
-order function that removes members that do not satisfy a           the formalisation of definition or a concept when we think
given predicate from a list, (v) [] stands for an empty list,        modelling it in Isabelle/HOL’s language or as a functional
# stands for the list append operation, (vi) set takes a list        program is interesting.
and returns its set of elements, (vii) @ concatenates two lists,     Abstract Syntax Trees Elements of the syntax tree are
(viii) foldr applies a function to elements of a given list,         type synonyms, i.e. abbreviations for types. The most ba-
while accumulating the results, (ix) zip takes two lists of          sic concept is that of a name, which is defined as an Is-
equal length and returns a list of equal length s.t. position i      abelle/HOL string (line 1). A variables, effects, operators
in the output list is the pair of elements at position i in the      and problems are is modelled as tuples with the obvious
two given lists, (x) for mappings f and g, f ⊆m g means              members (lines 2-8). Note: nat option models an optional
that any argument mapped to a value by f is mapped to the            natural number value. Generally, an α option is an algebraic
same value by g, (xi) map of takes a list of pairs and re-           data type consisting of the union between two types: one
turns a function that corresponds to that list, (xii) ◦ denotes      to represent no value and one that represents existence of a
function composition, (xiii) ++ takes two maps and merges            value of type α. For variables, we use it to express that a vari-
them, with precedence to its right argument.                         able has an optional axiom layer. An assignment (ast ass)
                                                                     is a pair, representing the variable and the assigned value.
Formalising Basic Definitions in Isabelle/HOL
                                                                     For a problem, the variable and operator sections are lists of
 Listing 1: FD-AST and DIMACS-CNF                                    variables and operators, respectively. The initial state is a list
     type_synonym name = string                                      of natural numbers whose length has to be equal to the num-
 2   type_synonym ast_variable = name × nat option × name listing
     type_synonym ast_effect =
                                                                     ber of state variables, and the goal is a list of ast ass. We
 4         ast_ass list × nat × nat option × nat                     define functions to access the state variables, initial state, the
     type_synonym ast_operator =
 6         name × ast_ass list × ast_effect list × nat               goal and the set of actions of a given problem AST, and refer
     type_synonym ast_initial_state = nat list                       to them as astD, astI, astG and astδ, respectively.
 8   type_synonym ast_goal = ast_ass list
     type_synonym ast_problem =                                         The AST of DIMACS-CNF is a list of lists of integers,
10         ast_var_sec × ast_initial_state × ast_goal × ast_op_sec
     definition wf_partial_state ps = distinct (map fst ps)
                                                                     where each list represents a line in the DIMACS file, i.e. a
12              ∧ (∀(x,v) ∈ set ps. x < numVars ∧ v < numVals x)     clause, and each integer represents a literal. The AST of a
     fun wf_operator :: ast_operator ⇒ bool
14     where wf_operator (name, pres, effs, cost) =                  model for a DIMACS-CNF AST is a list of integers.
         wf_partial_state pres
16       ∧ distinct (map (λ(epres, v, l, m). v) effs)                Well-Formedness Definitions of well-formedness of
         ∧ (∀(epres,x,vp,v) ∈ set effs.
18           wf_partial_state epres                                  states, operators and problems are rather straightforward
20
         ∧ x < numVars ∧ v < numVals x
         ∧ (case vp of None ⇒ True | Some v ⇒ v<numVals x))
                                                                     formalisations of Definition 2 (lines 13-26). We note two
     definition well_formed =                                        parts of the Isabelle’s syntax: (i) the case-of statement in
22         length astI = numVars
         ∧ (∀x<numVars. astI!x < numVals x)
                                                                     wf operator is a switch between the different constructors
24       ∧ wf_partial_state astG                                     for a data type, and cases are separated with |, (ii) the pred-
         ∧ (distinct (map fst astδ))
26       ∧ (∀π ∈ set astδ. wf_operator π)                            icate well formed takes an implicit argument P standing
     definition valid_states :: state set                            for the problem, but it is fixed outside the definition using a
28     where valid_states = {s. dom s = Dom ∧ (∀x ∈ Dom. the (s x)
             ∈ range_of_var x)}                                      namespace like mechanism referred to as locale.
     definition subsuming :: pstate ⇒ state set
30     where subsuming partial = {s ∈ valid_states. partial ⊆m s}    Semantics To formalise the semantics we define predi-
     definition eff_enabled :: state ⇒ ast_effect ⇒ bool
32     where eff_enabled s = λ(epres,_,_,_). s ∈ subsuming (map_of   cates and functions that describe action execution. We first
              epres)
     definition enabled :: name ⇒ state ⇒ bool
                                                                     define two functions that, w.r.t. the problem, return the set
34     where enabled name s = case lookup_operator name of           of valid states and the set of valid states subsuming a given
           Some (_,pres,effs,_) ⇒ s ∈ subsuming (map_of pres)
36           ∧ s ∈ subsuming (map_of (implicit_pres effs))
                                                                     state (lines 27-31). Based on that, Definition 3 is formalised
         | None ⇒ False                                              (lines 31-43), and we recursively define a path between two
states (line 44), and, lastly, define a predicate (line 48) char-    list of effects using the higher-order function map, and lastly
acterising plans.                                                    (iv) rem implicit pres ops which lifts the last function
   The semantics of CNF-DIMACS formulae and their mod-               to an FD-AST problem by applying it to the list of operators
els are formalised on lines 50-53.                                   in the problem..
                                                                        The next step is translating an FD-AST resulting from ap-
Formalising FDR and Encoding FD-AST                                  plying rem implicit pres ops, whose operators have no
 Listing 2: FDR problems and semantics
                                                                     effect preconditions, to FDR. The variables in the FDR are
                                                                     the list of natural numbers below the number of variables
     type_synonym ('var, 'dom) state = 'var * 'dom
 2   type_synonym ('var, 'dom) assignment = 'var × 'dom
                                                                     in the FD-AST. Since the FD-AST initial state is a list of
     record ('var, 'dom) sas_plus_operator =                         values, the initial state is translated by just adding to every
 4     precondition_of :: ('var, 'dom) assignment list
       effect_of :: ('var, 'dom) assignment list                     one of those values the variable to which it is assigned. Con-
 6   record ('var, 'dom) sas_plus_problem =                          structing the FDR range map, which maps every variable to
       variables_of :: 'var list
 8     operators_of :: ('var, 'dom) sas_plus_operator list           a list of natural numbers, is done using the function abs -
       initial_of :: ('var, 'dom) state                              range map. It is done by applying zip to two arguments,
10     goal_of :: ('var, 'dom) state
       range_of :: 'var * 'dom list                                  the first of which is the list of variables in the FD-AST, com-
12   fun execute_serial_plan_sas_plus
       where execute_serial_plan_sas_plus s [] = s
                                                                     puted by abs ast variable section. The second argument is
14     | execute_serial_plan_sas_plus s (op # ops)                   more involved. The function get range computes the list
         = (if is_operator_applicable_in s op
16       then execute_serial_plan_sas_plus (                         of assignments a variable can take, given one entry from the
                execute_operator_sas_plus s op) ops                  variables section. The second argument to zip is thus a list
         else s)
18   fun rem_effect_implicit_pres:: ast_effect ⇒ ast_effect where    of lists of natural numbers, each of which representing a the
       rem_effect_implicit_pres (preconds, v, implicit_pre, eff) =
               (preconds, v, None, eff)
                                                                     assignment of a variable. The operators are translated in a
20   definition implicit_pres :: ast_effect list ⇒ ast_ass list      straightforward way: the preconditions are taken as they are,
       where implicit_pres effs =
22       map (λ(_,v,vpre,_). (v,the vpre))
                                                                     and the effects are extracted by mapping a lambda function
             (filter (λ(_,_,vpre,_). vpre6=None) effs)               that, given an effect, extracts the affected variable and its
24   fun rem_implicit_pres :: ast_operator ⇒ ast_operator where
       rem_implicit_pres (name, preconds, effects, cost) =           new value as a pair.
26         (name, (implicit_pres effects) @ preconds, map
                  rem_effect_implicit_pres effects, cost)
                                                                        The way we modularly divide the encoding of FD-AST
     fun rem_implicit_pres_ops :: ast_problem ⇒ ast_problem where    problems into FDR problems made the proof of the first
28     rem_implicit_pres_ops (vars, init, goal, ops) = (vars, init
             , goal, map rem_implicit_pres ops)                      statement of Theorem 1 more modular, and thus manage-
     definition abs_ast_goal :: nat_sas_plus_state                   able. A detail in the formal proof, which would be glossed
30     where abs_ast_goal = map_of astG
     definition abs_ast_initial_state :: nat_sas_plus_state          over in a pen-and-paper treatment, is to show that translat-
32     where abs_ast_initial_state = map_of (zip [0..<length astI]
               astI)
                                                                     ing enocding a well-formed FD-AST will result into a valid
     definition abs_range_map :: (nat * nat list)                    FDR, which is necessary for using the different theorems
34     where abs_range_map =
             map_of (zip abs_ast_variable_section
                                                                     about FDR problems. Proving that depends on the assump-
36                        (map get_range astDom))                    tion that the AST actions have no conditional effects. The
     definition abs_ast_operator :: ast_operator ⇒
           nat_sas_plus_operator                                     second theorem that we prove about this translation is that it
38     where abs_ast_operator = λ(name, preconditions, effects,      preserves completeness.
             cost).
              L precondition_of = preconditions,                        Modelling the decoding function is relatively straight-
40              effect_of = [(v, x). (_, v, _, x) ← effects] M
     definition decode_abs_plan ops = map (fst o the o
                                                                     forward and is done using decode abs plan. Firstly note
           lookup_action) (rem_condless_ops I ops)                   that ◦ denotes function composition. The function decode -
                                                                     abs plan firstly removes the operators whose preconditions
   Concepts from Definition 5 are formalised in Listing 2.           are not statisfied when the operator sequence is executed at
A state is formalised as a mapping from a variable type to           the initial state. It then applies three steps to each of the op-
a domain type. An assignment is formalised as a variable-            erators in the given FDR plan: first it looks up the equivalent
value pair. ’var and ’dom are polymorphic type parameters            FD-AST operator, then it checks if the lookup operation was
that can be instantiated. These type variables are instantiated      successful using the function the, and lastly it extracts the
with the type nat when translating from FD-AST to FDR.               name of operator using fst, which returns the first element
An operator and an FDR problem are formalised as records.            in a given tuple.
   The most interesting part is modelling the encoding and
decoding as functional programs in Isabelle/HOL’s lan-               Formalising the Encoding of STRIPS Problems
guage. Encoding an FD-AST operator is done in multiple               into SAT
stages to make verifying the encoding more modular. First,
the effect preconditions are removed and added into the op-          Listing 3 shows parts of our encoding formalisation. SAT-
erator’s preconditions. This first step is further modularly         Plan variables are data types with two distinct constructors
implemented using (i) rem implicit pres ops, which re-               State and Operator storing time index and a number
moves the effect preconditions from one given effect, and            identifying the operator (line 1). Lines 2-22 show the oper-
replaces it with None, (ii) implicit pres which extracts             ator encoding. Importance was given to construct CNF for-
the implicit preconditions from a given effect, (iii) rem -          mulas immediately to facilitate the proof that the encoding
implicit pres which applies the previous two functions               is in CNF form. We use folds to construct the conjunctions
to an operator, thus lifting rem implicit pres ops to a              with base value ¬⊥.
 Listing 3: SATPlan encoding

     datatype sat_plan_variable = State nat nat | Operator nat nat
 2   definition encode_all_operator_preconditions :: "'var
           strips_problem ⇒ 'var strips_operator list ⇒ nat ⇒
           sat_plan_variable formula"
     where "encode_all_operator_preconditions Π ops t =
 4     let l = List.product [0..<t] ops
       in foldr (∧) (map (λ(t, op). encode_operator_precondition Π
              t op) l) (¬⊥)"
 6   definition encode_all_operator_effects :: "'var strips_problem
           ⇒ 'var strips_operator list ⇒ nat ⇒ sat_plan_variable
           formula"
     where "encode_all_operator_effects Π ops t =
 8     let l = List.product [0..<t] ops
       in foldr (∧) (map (λ(t, op). encode_operator_effect Π t op)
              l) (¬⊥)"
10   definition encode_operators :: "'var strips_problem ⇒ nat ⇒
           sat_plan_variable formula"
     where "encode_operators Π t =
12     let ops = operators_of Π
       in encode_all_operator_preconditions Π ops t ∧
             encode_all_operator_effects Π ops t"




Formalising the Final Correctness Theorem
 Listing 4: Overall Encoding Correctness

     definition dimacs_model :: int list ⇒ int list list ⇒ bool
 2     where dimacs_model ls cs = (∀c ∈ set cs.
         (∃l ∈ set ls. l ∈ set c))
 4         ∧ distinct (map dimacs_lit_to_var ls)
     lemma encode_sound:
 6     Jvalid_plan P πs; length πs ≤ h; encode h P = Inl
             cnf_formulaK =⇒
              (∃dimacs_M. dimacs_model dimacs_M cnf_formula)
 8   lemma encode_complete:
       encode h P = Inr err =⇒
10       ¬(well_formed P ∧ (∀op ∈ set (astδ P). consistent_pres_op
                op) ∧
         (∀op ∈ set (astδ P). is_standard_operator op))
12   lemma decode_sound:
       decode M h P = Inl plan =⇒ valid_plan P plan
14   lemma decode_complete:
       decode M h P = Inr err =⇒
16             ¬ (well_formed P ∧
                 (∀op ∈ set (astδ P). consistent_pres_op op) ∧
18               (∀π ∈ set (astδ P). is_standard_operator π) ∧
                 dimacs_model M (SASP_to_DIMACS' h P))


  In Isabelle/HOL formalisations of Theorem 5 is shown in
Listing 4 between lines (5-18). We formalised the function
encode in Isabelle/HOL’s language s.t., given a horizon and
FD-AST, it returns either Inl and a SAT formula, if the en-
coding is successfully computed, or Inr and an error mes-
sage. Similarly, decode returns either Inl and a plan, if the
decoding is successful, or Inr and an error message other-
wise.
            Figure .2                      Figure .3                      Figure .4                      Figure .5




Figure .6: Comparison of different performance indicators for our encoding and Madagascar’s on satisfiable and on unsatisfiable
formulae. Different plots show the running times of Kissat, the number of clauses, the number of variables, the total running
time of computing the encoding as well as solving the formulae, and the maximum memory needed for computing the encoding
as well as solving the formulae.
