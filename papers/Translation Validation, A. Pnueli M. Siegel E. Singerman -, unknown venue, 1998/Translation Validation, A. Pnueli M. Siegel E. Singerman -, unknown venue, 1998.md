                       Translation            Validation           *


                      A. Pnueli     M. Siegel      E. Singerman **

                    Weizmann Institute of Science, Rehovot, Israel


       A b s t r a c t . We present the notion of translation validation as a new ap-
       proach to the verification of translators (compilers, code generators).
       Rather than proving in advance that the compiler always produces a
       target code which correctly implements the source code (compiler verifi-
       cation), each individual translation (i.e. a run of the compiler) is followed
       by a validation phase which verifies that the target code produced on this
       run correctly implements the submitted source program.
       Several ingredients are necessary to set up the - fully automatic - trans-
       lation validation process, among which are:
         1. A common semantic framework for the representation of the source
            code and the generated target code.
         2. A formalization of the notion of "correct implementation" as a re-
            finement relation.
         3. A syntactic simulation-based proof method which allows to automat-
            ically verify that one model of the semantic framework, representing
            the produced target code, correctly implements another model which
            represents the source.
       These, and other ingredients are elaborated in this paper, in which we
       illustrate the new approach in a most challenging case. We consider
       a translation (compilation) from the synchronous multi-clock data-flow
       language SIGNALto asynchronous (sequential) C-code.


1    Introduction
In this paper, we present the notion of translation validation as a new approach
to the verification of translators (compilers, code generators). The idea of trans-
lation validation is the following: Rather than proving in advance that the com-
piler always produces a target code which correctly implements the source code
(compiler verification), each individual translation (i.e. a run of the compiler) is
followed by a validation phase which verifies that the target code produced on
this run correctly implements the submitted source code.
    Since compiler verification is an extremely complex task and every change
to the compiler (even minor revisions) requires redoing the proof, compiler ver-
ification tends to "freezes" the compiler design, and discourages any future im-
provements and revisions. This drawback is avoided in the translation validation
 * This research was done as part of the European Community project SACRES (EP
   20897) and was supported in part by the Minerva Foundation and an infrastructure
   grant from the Israeli Ministry of Sciences and Art.
** Current address: Computer Science Laboratory, SRI International, Menlo Park, Cal-
   ifornia.
                                       152


approach since it compares the input and the output of the compiler for each
individual run independently of how the output is generated from the input.
    The concept of translation validation is depicted in Fig. 1.




                                             Bad = ~ o u n t e r Exam~~~ple

            Compiler 1         Analyzer
                                             Good ~          ~


                                                       I Rudimentary 1
                                                         Proof CheckerJ
                                                       /             ",,,
                                                      O.K.          Not O.K.
                                                                 Fault Indication
                  Fig. 1. The concept of Translation Validation



    Both the source and the target programs are fed as inputs to an Analyzer.
If the analyzer finds that the generated target program correctly implements
the source program, it generates a detailed proof script. If the analyzer fails
to establish the correct correspondence between source and target, it produces
a counter-example. The counter example consists of a scenario in which the
generated code behaves differently than the source code. Thus, the counter-
example provides an evidence that the compiler is faulty and needs to be fixed.
    The following ingredients are necessary to set up the - fully automatic -
translation validation process:
 1. A common semantic framework for the representation of the source code and
    the generated target code.
 2. A formalization of the notion of "correct implementation" as a refinement
    relation, based on the common semantic framework.
 3. A proof method which allows to prove that one model of the semantic frame-
    work, representing the produced target code, correctly implements another
    model which represents the source.
 4. Automation of the proof method, to be carried out by the analyzer which,
    if successful, will also generate a proo/script; and
 5. A rudimentary proo/checker that examines the proof script produced by
    the analyzer and provides the last confirmation for the correctness of the
    translation.
   These ingredients are elaborated in this paper, in which we illustrate the
new approach in a most challenging case. We consider a translation (compila-
                                       153


tion) from the synchronous multi-clock data-flow language SIGNAL [BGJ91] to
asynchronous (sequential) C-code.
    As part of the Esprit-supported SACRES project (Safety Critical Embedded
Systems), the proposed translation validation tool described here is expected to
provide repeated validation of each run of the translator. To increase the confi-
dence in the correctness of the validation tool itself, it has been structured into
an analyzer which produces a proof script and a (rudimentary) proof checker.
This decomposition enables us to make the proof checker, which is responsible
for providing the last seal of approval, very simple and almost "verifiable by
inspection".
    The paper is structured as follows. The next section introduces the basic
notions: We present the small, yet representative, SIGNAL pprogram MUX; give
the generated C-code of MUX, and explain why it "correctly implements" the
source code. Then, we turn to the formal side. In Section 3 we introduce the
synchronous transition system (STS) computational model. This formalism is
used as the common semantic base for the description of both the synchronous
source and the asynchronous target programs (SIGNAL and C resp., in our ex-
ample). Section 4 formalizes the notion of "correct implementation" by means
of a refinement relation. A generalization of the refinement-mapping simulation
method is advocated as a proof method for the refinement relation. Automation
of this proof method, based on syntactic representation of an appropriate proof
rule, is the topic of Section 5, and finally, concluding remarks appear in Section
6. A more detailed discussion of the proof-checker and the decision procedures
that were used is saved for the full version.


Related Work

Work in a similar direction was recently reported by Cimatti et al. [C97]. Due to
the similarity between the source and target languages, the translation they con-
sidered is rather straightforward, and is therefore verified using a much simpler
technique than the one we develop here.
    Another related work is the "Proof-Carrying Code" mechanism of Necula
and Lee, cf. [NL96,N97]. We believe that the translation validation approach
may have several advantages over proof-carrying code. The translation valida-
tion framework is more general due to its abstract computational model and
refinement notions, which the proof-carrying code method does not enjoy. An-
other important advantage of translation validation is that it is fully automatic,
while in proof-carrying code the crucial part of the correctness proof, namely,
the verification condition, is generated manually.


2   An Illustrative       Example

In this section we first illustrate details of the compilation process by means
of an example and then explain the principles which underly the translation
validation process.
                                               154


    SIGNAL [BGJ91] is a synchronous programming language used for design and
implementation of reactive systems. Statements of SIGNAL a r e intended to relate
clocks (frequencies) as well as values of the various (internal and external) signal
flows involved in a given reactive system. Variables (signals) in SIGNAL , as is
often the case in synchronous languages, are volatile. T h a t is, they only hold
values at specific time instances along a computation. P u t differently, variables
are absent almost everywhere along a computation.
    Consider the following SIGNAL program:

process MUX=
     ( ? integer FB
       ' integer N
      )
          (l N:= FB default (ZN-I)
           i ZN:= N $ I
           [ FB'=when (ZN<=I)
           l)
      where
         integer ZN init I ;
end

    This program uses the integer variable FB as input, the integer variable N
as output and the local variable ZN. The body of MUX is composed of three
statements which are executed concurrently as follows. An input FB is read and
copied to N. If N is greater than 1 it is successively decremented by referring to
ZN, which holds the previous value of N (using $ to denote the "previous value"
operator) . No new input value for FB is accepted until ZN becomes (or is, in
case of a previous non-positive input value for FB) less than or equal to 1. This
is achieved by the satatement

 FB^=when (ZN<=I),

which is read "the clock of FB is on when ZN _< 1", and allows FB to be present
only when ZN < 1. A possible computation of this program is:

        N:3     - - '~    N:2     ~    N:I           ~        5   "~    N'4     ~   ...
       ZN : 1            ZN : 3       ZN ' 2             ZN   1        ZN ' 5



   Where _l_ denotes the absence of a signal. Note that SIGNAL programs are
not expected to terminate.
   Let us now consider the C-code obtained by compiling a SIGNAL program.
The main-program consists basically of two functions:

 - An initialization function, which is called once to provide initial values to
   the program variables.
 - An iteration function which is called repeatedly in an infinite loop. This
   function, whose body calculates the effect of one synchronous "step" of the
   abstract program, is the essential part of the concrete code.
                                                               155


      The iteration function obtained by compiling MUX is given below.

logical MUX_iterate()
{
i0:            hl = TRUE;
Ii:            h2 = ZN <= I;
12:            if (h2)
12.1:               read(FB);
13:            if (h2)
13.1:               N = FB;
               else
13.2:               N = ZN - i;
14:            write(N);

15:            Z N = N;
               return TRUE;
}

Remark 1. The labels are not generated by the compiler but have been added
for reference.

    The C-code introduces explicit boolean variables to represent the clocks of
SIGNAL variables and events. Variable hl is the clock of N and ZN, and h2 is
the clock of FB.
    The C program works as follows. If h2, the clock of FB, has the value true,
a new value for FB is read and assigned to the variable N. If h2 is false, N gets
the value ZN - 1. In both cases the updated value of N is output (at 14) and also
copied into ZN, for reference in the next s t ep.
   A computation of this program is given below. We skip some of the inter-
mediate states and use the notation X : 9 to denote that variable X has an
arbitrary value.

     N'*                       N:*                    N:*                 N'*                 N:3
    ZN : 1      ..._~*       ZN . 1     __~*        ZN : 1      __~     ZN . 1      _._~*    ZN . 1
    hl:*                 |    hl:t                   hl:t                hl:t                 hl:t
    h2:*                      h2:t                   h2:t                h2:t                 h2:t
    pc " l 0                 p c : 12               p c . 13           pc : /3.1             p c : 15



       N:3                     N:3                  N:3                  N:3                  N:2
    7,N : 3     _._~*       ~,N : 3     ~         ZN : 3       ._~     ZN : 3      _~*      ZN ' 3      __~
     ]11 : t             /   hl . t                hl : t               hl ' t               hl ' t           " " "
     h2 : t                  h2 . f                h2 : f               h2 : f              h2 : f
    p c : 10             ~, p c . | 2          ~, p c : 13            pc ' 13.2             pc : |5


    Note the introduction of the variable pc which is the program counter point-
ing to the location of the statement which is next to be executed. When com-
paring this computation to the computation of the SIGNAL program, one finds
that the location 15 is of particular interest: at this location the values of the
concrete variables FB, N, and ZN, whose absence or presence is determined by
the variables hl and h2, coincide with the values of the corresponding abstract
variables.
                                                             156


    Taking into account t h a t h l is the clock of N and ZN and t h a t h2 is the
clock of FB, we have an accurate state correspondence between the computation
of the SIGNAL program and the following computation of the C-code, where we


          (F,3)_
             N:3
           ZN : 1
            hl . t
                      --.h.*
                                 N:2
                               ZN : 3
                                hl : t
                                          ...~*
                                                  (F,3}_(FBs)_(F.}
restrict our observations to subsequent visits at location 15:

                                                     N:I
                                                   ZN : 2
                                                    hl . t
                                                                   _..~*
                                                                             N:5
                                                                           ZN ' 1
                                                                            hl : t
                                                                                      ...~*
                                                                                                N'4
                                                                                              ZN : 5
                                                                                               hl : t
                                                                                                         _..~*
                                                                                                         ~       " " "
            h2 : t             h 2 : .f            h2 . J                   h2 " t            h 2 : ~r
           pc . 15             pc : 15             pc . 15                 pc : t 5           pc : 15



    The central observation is t h a t there exists a designated control location in the
C-code (15 in our example) where the variables of the concrete (target) system
correspond to their abstract (source) counterparts. This is a general p a t t e r n
for programs generated by the SACRES compiler. Intuitively, the generated C-
code correctly implements the original SIGNAL program if the sequence of states
obtained at the designated control location corresponds to a possible sequence
of states in the abstract system.
    In the rest of the paper, we show how this approach can be put on formal
grounds and yield a fully automatic translation validation process.


3          The       Computational                Model

In this section, we present synchronous transition systems (STS), which is the
computational model on which the process of translation validation is based.
    We assume a vocabulary of typed variables )2. Some of the variables are
identified as persistent while the others are identified as volatile. The volatile
variables are intended to represent signals in the sense of the language SIGNAL.
The domains of volatile variables contain the designated element _L to indicate
absence of the respective signal.
    A state s is a type-consistent interpretation of ];, assigning to each variable
v E )2 a value s[v] over its domain. We denote by Z the set of all states over )2.

D e f i n i t i o n 1. The following components define a synchronous transition sys-
tem (STS) A = (V,O,p,E) (cf. [PS97]):

    - -   V C_ 1) : A finite set of system variables.
    -     O : An initial condition. A satisfiable assertion characterizing the initial
          states of system A.
    -     p : A transition relation. This is an assertion p(V, W), which relates a state
          s E Z to its possible successors s r E E by referring to both unprimed and
          primed versions of the system variables. An unprimed version of a system
          variable refers to its value in s, while a primed version of the same vari-
          able refers to its value in s ~. If (s, s ~) ~ p(V, W), we say that state s ~ is a
          p-successor of state s.
    -     E C V : A set of externally observable variables.

          Next, we define a computation of an STS.
                                                   157


D e f i n i t i o n 2. Let A = (V, O, p, E) be an STS. The infinite sequence
a = so, s l , s 2 , . . . , where si E Z for each i E 1~, is a computation of A if it
satisfies the following requirements:

                      Initiation :  so ~ 0
                      Consecution : (si, si+l) ~ p              for each i E 1~.

      We denote by HAll the set of computations of the STS A.

3.1     S T S r e p r e s e n t a t i o n o f t h e SIGNAL p r o g r a m
The SIGNAL program MUX is represented by the STS A = (V, O, p, E), where
           Y = {FB, N, ZN, x.N}

           O = (FB = & A N = _ L A Z N = _ k A x . N = _L)

                                       if FB ~ #_L then FB ~             }
                           A N ~=      else if ZN ~ _ L t h e n ZN ~ - 1
                                       else _L
                           A x . N ~= if N ~7~_Lthen N ~else x.N
                    V
           p=
                                        if N ~ =_L then _l_           }
                           A Z N ~=     else if x . N = _ L t h e n 1
                                        else x.N
                          A ZN ~ < 1 ++ FB ~ 7~ _L
                    V    FB ~ = _L A N ~ = _L A ZN ~ = _L Ax.N ~ = x.N)

           E = {FB, N, ZN}


      Two points here require further explanation:
 - Besides maintaining all variables occurring in the SIGNAL-program as volatile
   variables, the STS-encoding of SIGNAL-programs introduces persistent m e m -
   orization variables for those variables occurring in S-expressions. In our ex-
   ample, there is only one memorization variable, namely, x.N.
 - The second disjunct of p guarantees the stutter robustness of A. T h a t is,
   at any step, the system may choose to take a stutter (idling) step in which
   all signals are set to _L and all memorization variables retain their previous
   values.

3.2     STS representation            of the C program

The representation of the C code is less straightforward than that of the SIGNAL
program. So, we first present the STS and then follow with detailed explanations.
     The C code is described by STS C presented below. The predicate pres(U) =
A v e v ( V ~ = v) in this presentation expresses that the variables in set U _C V
remain unchanged during the current transition, cf. [MP91].
                                             158


   C = (V, O, p, E) where

         V = {FB, N, ZN, x.N, h l , h 2 , p c }

         O = (FB ~t •          ~ 2 A ZN = 1 A x . N = 2 A p c =      lo)

                 V (pc = l0 A h l ' = true A pc r = ll A pres(V \ {pc, hl}))
                 V (pc = il A h2' = (ZN < 1) A pc' = 12 A pres(V \ {pc, h2}))
                 V (pc -- 12 A h2 A pc' = 12.1 A pres(V \ {pc}))
                 V (pc = 12 A ~h2 A pc' = I3 A pres(Y \ {pc)))
                 V (pc = 12.1 A FB' ~ .L A p e = la A pres(V \ {pc, FB}))
         p=      V (pc = la A h 2 A p c ' = 13.1 Apres(V \ {pc}))
                 V (pc = 13 A ~h2 A pc ~ = 13.2 A pres(V \ {pc}))
                 V (pc = is.1 A N' = FB A pc t = la A pres(V \ {pc, N}))
                 V (pc = 13.2 A N' = ZN - 1 A p e = 14 ^ pres(V \ {pc, N}))
                 V (pc = l,t A x.N' = N A pc' = 15 A pres(V \ {pc, x.N}))
                 V (pc = 15 ^ ZN' = N A pc' = lo ^ pres(V \ {pc, ZN}))

         E = {FB, N, ZN}

     Some remarks are in order.
I n p u t f o r FB: Being at location 12.1, we allow FB to take an arbitrary non-
      bottom value, which corresponds to a new input for FB from the environ-
      ment. If h2 is false and we proceed directly from 12 to 13, the value of FB
      remains unchanged as stated by the pres(V \ {pc}) clause.
O u t p u t o f N: The explicit writing of N at location 14 in the C-program has
      been removed; instead, the memorization of N is introduced.
T h e o b s e r v a t i o n p o i n t : As explained above, entering location 15 means t h a t
      the m u x _ i t e r a t e function has cumulatively computed one transition of the
      abstract system. The values of the persistent variables FB, N, and ZN are
      considered to be present only when being at location 15 and if their respective
      clock expressions have the value true. This will become apparent when we
      define the refinement mapping from STS C to STS A. All other persistent
      variables are considered internal.
M e m o r i z a t i o n o f N: The generated C-code does not use any memorization
      variables but rather encode memorization by means of scheduling. In order
      to match the abstract memorization variables we augment the STS-encoding
      of the generated C-program with memorization variables which have the
      same name as their abstract counterparts. The general pattern for memo-
      rization is that all variables which are memorized in the abstract system, are
      memorized in the concrete system directly before entering the observation lo-
       cation, i.e. the location where the state correspondence is to be established.
                                          159


      In our example, the value of N is copied to a memorization variable x.N, at
      location 14, just before the observation location 15.


4     Correct Implementation: Refinement

In this section, we consider the notion of correct implementation which is the
relation t h a t should hold between a source code and its correct translation. We
suggest t h a t the appropriate relation is t h a t of refinement adapted to our special
circumstances t h a t involve a translation from a synchronous language such as
SIGNAL into an asynchronous language such as C.
    In general, we consider refinement between an abstract system A and a con-
crete system C. System A can be viewed as a specification or a high-level de-
scription of the application we wish to construct, while C is a description closer
to the final implementation. An elaborate development process m a y progress
through several refinement steps, each making the representation more concrete.
In m a n y cases, the abstract system is described in a more declarative style while
the concrete system is presented in a more operational/imperative style.
    In order to make the implementation refinement relation maximally effective,
we should make it as liberal as possible, provided the essential features of the
system are preserved.


4.1     Refinement between Systems

Consider the two systems A = (VA , ~gA, PA, EA) and C = (Vc, (9 c, Pc, E c ) , to
which we refer as the abstract and concrete systems, respectively.
    We assume t h a t E A C_ E c . T h a t is, the abstract observable variables are a
subset of the concrete observable variables.
    For T 6 {A,C}, we denote by E r , the set of T-states, i.e., the set of states
obtained by assigning values to the variables Vr . We denote by E~. the set of
states which only assign values to the variables in E r C_ Vr .
    For a state s 6 Z r , we denote by s ~ the restriction of s to the subset
of observable T-variables, i.e., to E r. This restriction can be lifted point-wise
to a computation a 6 IITII, denoted by a E, and then to the complete set of
computations IITIh denoted by IITII~.
    For the two systems A and C, we define an interface mapping to be a function



m a p p i n g each concrete state s 6 Z c to an abstract observable state I ( s ) 6 E l .
     An interface mapping 2: is said to be a clocked mapping if, for each observable
variable x 6 E A (which also belongs to E c since E A C_ E c) and every concrete
state s 6 E c ,

      z(~)[~] : s[~]     or      Z(~)[~] = I.
                                           160


T h a t is, the effect of the mapping I on a variable x which is observable in both
systems is either to preserve its value (S(s)[x] = s[x]) or to declare it absent at
the current abstract state (2:(s)[x] = J_).
     We can point-wise lift the interface mapping Z to a concrete computation
a E IICIh denoted by 2:(a), and then to the complete set of concrete computations
IICIh denoted by E(lIVll ).

Definition 3. For systems A and C with EA C_ Ec, and a clocked interface
mapping Z from C to A, we say that C refines A relative to Z if Z(IICII ) c
JfAIJ
T h a t is, C refines A relative to E if applying the mapping I to any concrete
computation ~ E IICII, we obtain an abstract computation restricted to the
observable variables E A .

Definition 4. For systems A and C, we say that C refines A if there exists a
clocked interface mapping 5[ from C to A such that C refines A relative to I .
   We write C _ A to denote the fact that system C refines system A. In the
next section we investigate a proof method which allows to establish that C E A
indeed holds for some given A, C E STS.


4.2     Proving Refinement by the Method of Refinement Mapping
        (Simulation)
As proof method for the refinement notion introduced above we employ a gener-
alization of the well-established concept of simulation with refinement mapping
[AL91]. Refinement mappings define a correspondence between the variables of a
concrete system and the variables of an abstract system such that observations
are preserved. Refinement mappings, or more generally simulation techniques
(see, e.g., [Jon91,LV91]), are the means to inductively prove a semantically de-
fined notion of containment between observable behaviors.
    Note that, while we employed the notion of clocked interface mapping in
the definition of refinement, requiring mapping of concrete states only to the
observable part of the abstract state, a general refinement mapping is expected
to yield a mapping of a concrete state to a full abstract state. Thus, a refinement
mapping can be viewed as one of the many possible extensions of an interface
mapping.
    We define a refinement mapping from C to A to be a function f : Z c
~A, mapping concrete to abstract states. A refinement mapping f is called a
clocked refinement mapping if it satisfies
      f(s)[x] =s[x]   or   f(s)[x] = _L,     for every s e ~ c and x e E A.

From now on, we restrict our attention to clocked refinement mappings, which
preserve the observables up to stuttering.
    The proposed proof method for refinement is based on finding an inductive
refinement mapping as defined below. In the definition, we denote by ~ r the set
                                             161


of all reachable states of system C, i.e., all states appearing in some computation
of C.

Definition 5. A clocked refinement mapping f : E c ---+ E A is called inductive
if it satisfies the requirements of

    - Initiation: s ~ Oc implies f ( s ) ~ OA, for all s e ~ c , and
    - Propagation: (s, s') ~ Pc implies (f(s), f ( s ' ) ) ~ PA, for all s, s' ~ ~ .

The use of an inductive refinement mapping as a proof method is stated in the
next theorem.

T h e o r e m 1. If f : S c ----+ S a is an inductive (clocked) refinement mapping
from C to A, then C E_ A.


5      Automating          the   Translation Validation Process

The proof method presented in the previous section was based on an inductive
refinement mapping formulated in semantic terms. Among other things, it as-
sumed an available characterization of the set of reachable concrete states Z~
which is very difficult to compute for even the simplest systems.
    In the quest for automating the process, we present in this section a syn-
tactical representation of the notions of refinement mapping, and its associated
proof method. In this, we follow the ideas in [Lam91,KMP94] and adapt them
to deal with the particular notion of refinement needed for our case. Then, we
describe how the main components used in the proof can be computed, so that
the translation validation process can be carried out fully automatically.


5.1      Syntactic Representation and P r o o f Rules
Consider two STSS A and C with EA C_ EC, to which we refer as the abstract and
the concrete system, respectively. Let ~ : VA - - ~ g(Vc) be a substitution that
replaces each abstract variable v E VA by an expression s over the concrete
variables Vc. Such a substitution ~ induces a mapping between states, denoted
by -~. Let s c be some state in ~ c ; we refer to s c as a concrete state. The
abstract state s A ~f ~ ( s c) corresponding to s o under substitution ~ assigns to
each variable v E V A the value of expression Ev evaluated in s c . In this way,
refinement mappings can be syntactically defined by means of an appropriate
substitution ~.
    Now we show how to syntactically formulate the requirements of initia-
tion, propagation, and preservation of observation (the requirement that -~ is
a clocked refinement mapping) for such a state function 6 . For an expression
or state formula qo over VA, we define the formula (resp. expression) ~[c~] over
Vc obtained from ~ by replacing each occurrence of v E V A by gv. In the case
that qa contains a primed variable v ~, this variable is replaced by E~v obtained by
replacing all occurrences of variables v E Vc in s by their primed versions.
                                              162


    Given a concrete state s c and substitution c~, we have that the value of any
   evaluated over -d>(sc) is the same as the value of ~[~] evaluated over s c . This
holds, since in both cases ~ is evaluated using for v E V A its value in -5~(sv)
which is the same as the value of Ev evaluated over s c . In particular, for a state
formula ~ over VA we have ~ ( s c ) ~ ~ iff s c ~ ~[a]. This equivalence allows to
write the proof obligations of Definition 5 as stated in the following syntactical
proof rule REF for proving refinement of STS-systems.
    Definition 5 imposed the requirement of inductiveness only with respect to
reachable C-states. Since these are difficult to characterize precisely, rule REF
makes the stronger requirement which is that the mapping be inductive with
respect to all states satisfying some C-invariant inv. If inv is indeed a C-invariant
then all C-reachable states must satisfy inv and, therefore, inductiveness over
all inv-states clearly implies inductiveness over all reachable states.


                For assertion inv and substitution c~ : VA --+ E(Vc)
              R1. O c --~ inv                           inv holds initially
              R 2 . inv A PC --+ i n d                  inv is propagated
              R 3 . O c --+ OA[O~]                      Initiation
              R4. inv A PC --r pn[ot]                   Propagation
              rts.   inv             =.   v     =   •   for all v E EA
                                  CEA

                               Rule REF: Proving Refinement

      Two existential quantifications are hidden in this rule: "find an invariant
inv and a substitution a, s.t . . . . ". Generally, finding inv and a is left to the
ingenuity of the verifier. In order for rule REF to be useful in a fully automatic
translation validation process, an appropriate invariant of the concrete system
and a suitable substitution have to be generated automatically.


5.2     Generating         inv a n d a

In general, there is no chance of developing an algorithm which, presented with
arbitrary systems A and C, can automatically construct the needed invariant inv
and refinement substitution a as well as automatically verify the validity of the
premises in rule REF. The reason that this is possible in the case of translation
validation applied to the language SIGNAL is that we rely on some very strong
assumptions about the connections between A and C, based on the fact that C
was produced as a result of translation of system A by a code generator of a
very specific structure and mode of operation.
    The general structure of the main loop in the C-code is illustrated in the
figure below.
                                                                      163




            CalculaeCock xpessm s                                    ~hl                 TRUE                    \

           ................................                                 h_2__=_ Z.N_ _<=_)_ ............

           ........                    ....   -;-;     .....                 .............                            i
                           tj~.,j                                    \<~j                                                 ,,
                             T read(FB)                              T!h2?


       ,                                                                                                                  ,

       i                                               CalculateOutputs                                                   i
       '                          "~N=FB                           _(~           N=Z,-!~                                  '

       t. . . . . . . . . . . . . . . . . . . . . . ~. . . . . . . . . . . . . . . . . . . . . . . . . . . . .        J



                                                ....           ~                     .....................                    /
       ,                                                                   ZN=       N                                    ,
       I UpdatePast-DependentVariables ~
       L. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .   J



    As we see in the figure, the body of the infinitely repeated loop consists of
the following stages:

 1. Calculation of clock expressions. This stage assigns values to the boolean
    auxiliary variables hi, i - 1,... ,k. Each of these variables is associated
    with an abstract observable variable, and is used to represent the "exis-
    tence"/"absence" of it.
 2. Reading inputs. This stage reads the inputs of program, sometimes condi-
    tioned on the values of the appropriate clock variables.
 3. Calculating outputs. This stage calculates the value of output variables.
 4. Writing outputs. This stage write to external files (or channels) the com-
    puted values of output variables.
 5. Update "previous" expressions. This stage updates the values of (usually lo-
    cal) variables defined by expressions containing the previous operator ($).

    We use this special structure for the construction of the invariant inv and
the substitution a. We start by noting that using the program counter variable
pc, which is always a member of Vc, we can present the refinement substitution
a as follows:

 1. For each memorization variable x.v EVA, we include in a the substitution

                                                               x,v           )        x.v.
                                           164


 2. For every other variable v 6 VA, we include in ~ the substitution

                   v      ~    i f pc = ~obs A c l k ( v ) t h e n v e l s e _L,

    where clk(v) is the clock expression for v, indicating whether a new value
    had been assigned to v in the current iteration.
    The detailed algorithm for computing the clock expressions above, and the
accumulative invariant inv, which is omitted here for lack of space, is described in
the full version of this paper. The construction is based on viewing the main loop
of the C-code (procedure MUX-iterate, in our example) as a (cyclic) directed
graph, in which ~0 and ~obs are two of the nodes, and every edge e is labeled by
either a guard 7(e) or an action which can be a read into an input variable, a
write out of an output variable, or an assignment to a (local or output) variable.
For an edge labeled by an action, we can take its guard to be true.
    The clock expression clk(v) is computed by considering the guards along
paths leading to assignments to v. For the MUX-example, the clock expressions
obtained are
                            clk(FB) = h2
                            clk(N) = h2 V-~h2 (= true)
                            clk(ZN) = h2 V ~h2 (= true)
Based on this, the identification of the observation point as 15 and the general
"skeleton" of c~ given above, we obtain the following refinement substitution

                   FB           I" if h2 A pc --15 then F B e l s e _L
                   N            / if p c = l s t h e n  N e l s e _L
               :   ZN      ---+    if p c = l s t h e n ZNelse _L
                   x.N            x.N

   The invariant i n v is computed by taking the initial values of variables, and
then adding the cumulative effect of the actions that are executed along paths.
For the MUX-example, we obtain the following proposal for an invariant

              A FB#_L A N#_L A ZN#_L
              A pC 6 {/0, ll, 12, /2.1, /3, /3.1, /3.2, /4, /5}
              A pc 6 {11,12,12.1,13,13.1,13.2,14,15} -'+ h l
              A pc 6 {12,12.1,13,13.1,13.2,14,15}        -~ h2 = (ZN < 1)
              A pc 6 {/4,/5} Ah2                         --+ N = FB
     inv =    A pc 6 {/4,/5} A -~h2                      --+ N = ZN - 1
              A pc = 12.~                                --+ h2
              A pc = /3.1                                ~ h2
              A pc =/3.2                                 --~ -~h2
              A pc # 15       --~       ZN = (if x.N = _L t h e n 1 e l s e x.N)
              A pc = 15                                  -~ x.N = N

    We have verified all the premises of rule REF, using the TLV proof system of
[PS96]. The script files, which are omitted here for lack of space, will appear in
the full version of this paper.
                                       165


6    Conclusions

We introduced the new approach of translation validation, described the main
components of the construction together with the underline theory, and pre-
sented an illustrative example of the method by validating a compilation from a
synchronous language to an asynchronous one.
    The concept of translation validation is general, and the interest is obviously
not limited to translations from SIGNAL to C. We believe that the main ideas
presented in this paper can serve as a basis to the translation validation for a
large family of source and target languages.
    Our intuitionis based on the following. First, the STS computational model
is very general and can model both synchronous and asynchronous languages.
Second, the existence of designated control location(s) in the STS computations
of the source and target programs, that can serve as an observation point(s) for
comparing the values of a set of externally observable variables (input/output
variables, for example), is a reasonable thing to expect for. Otherwise, in what
sense could one say that the target program correctly implements the submitted
source code? Finally, our notion of refinement via an interface mapping and the
associated proof method, based on syntactic representation of the refinement
mapping, is again of a general kind.
    The approach described here seems to work in all cases that the source and
the target programs each consist of a repeated execution of a single loop body,
and the correspondence between the executions is such that a single loop itera-
tion in the source corresponds to as single iteration in the target. This seems to
be a characteristic of most code generators for synchronous languages such as
Esterel [BG], Lustre [CHPP87], and Statecharts [H87], as well as for languages
such as Unity [CMB88].
    It is clear that a translation validation "tool-set" should be tailored for the
particular translator (compiler) involved. The construction can be carried out
by following (and modifying) the guidelines of the framework presented here. (In
some cases, it may be useful to augment the translator as to make it easier to
identify the observation points.) We suspect that in some cases the construction
would turn out to be simpler than what was called for in the example presented
here. This is so because most of the difficulties we had faced were due to the fact
that SIGNAL is a synchronous language while C in asynchronous.


References

[AL91]     M. Abadi and L. Lamport. The existence of refinement mappings. Theo-
           retical Computer Science, 82(2), 1991.
[BG]       G. Berry and G. Gonthier. The Synchronous Programming Language Es-
           terel, Design, Semantics, Implementation. Technical Report 327, INRIA.
[BGJ91]    A. Benviniste, P. Le Guernic, and C. Jacquemot. Synchronous program-
           ming with event and relations: the SIGNAL language and its semantics.
           Science of Computer Programming, 16, 1991.
                                        166


[c97]    A. Cimatti, F. Giunchiglia, P. Pecchiari, B. Pietra, J. Profeta, D. Romano,
         P. Traverso, and B. Yu. A Provably Correct Embedded Verifier for the
         Certification of Safety Critical Software. In O. Grumberg, editor, Proc. 9~h
         Intl. Conference on Computer Aided Verification (CA V'97), Lect. Notes in
         Comp. Sci., vol. 1254, pages 202-213. Springer-Verlag, 1997.
[CHPP87] P. Caspi, N. Halbwachs, D. Piland, and J. Plaice. LUSTRE, a Declarative
         Language for Programming Synchronous Systems. POPL'87, ACM Press,
         pages 178-188, 1987.
[CMB88] K. M. Chandy and J. Misra. Parallel Program Design. Addison-Wesley,
         1988.
[H87]    D. Harel. Statecharts: A Visual Formalism for Complex Systems. Science
         of Computer Programming, 8, pages 231-274, 1987.
[Jon91]  B. Jonsson. Simulations between specifications of distributed systems. In
         J. C. M. Baeten and J. F. Groote, editors, CONCUR '91, volume 527 of
         LNCS, 1991.
[KMP94] Y. Kesten, Z. Manna, and A. Pnueli. Temporal verification of simulation
         and refinement. In J.W. de Bakker, W.-P. de Roever, and G. Rozenberg,
         editors, A Decade of Concurrency, volume 803 of Lect. Notes in Comp. Sci.
         Springer-Verlag, 1994.
[Lam91]  L. Lamport. The temporal logic of actions. Technical Report 79, DEC,
         Systems Research Center, December 1991. To appear in Transactions on
         programming Languages and Systems.
[LV91]   N. Lynch and F. Vaandrager. Forward and backward simulations for timing
         based systems. In Real-Time: Theory in Practice, volume 600 of LNCS,
         1991.
IMP91]   Z. Manna and A. Pnueli. The Temporal Logic of Reactive and Concurrent
         Systems. Springer Verlag, 1991.
[MP95]   Z. Manna and A. Pnueli. Temporal Verification of Reactive Systems: Safety.
         Springer-Verlag, New York, 1995.
[N97]    G. C. Necula. Proof-Carrying Code. In POPL'97, ACM press, pages 106-
         119, 1997.
[NL96]   G. C. Necula and P. Lee. Safe kernel extensions without run-time checking.
         In Second Symposium on Operating Systems Design and Implementations,
         Usenix, 1996.
[PS96]   A. Pnueli and E. Shahar. A platform for combining deductive with al-
         gorithmic verification. In R. Alur and T. Henzinger, editors, Proc. 8~h
         Intl. Conference on Computer Aided Verification (CA V'96), Lect. Notes in
         Comp. Sci., pages 184-195. Springer-Verlag, 1996.
[PS97]   A. Pnueli and E. Singerman. Fair synchronous transition systems and their
         liveness proofs. Technical report, Weizmann Institute of Science, 1997.
         Sacres Report.
