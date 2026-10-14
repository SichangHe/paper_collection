                                                              Continuous Verification of Large Embedded Software
                                                                  using SMT-Based Bounded Model Checking

                                                    Lucas Cordeiro                              Bernd Fischer                     Joao Marques-Silva
                                               University of Southampton                 University of Southampton              University College Dublin
                                                lcc08r@ecs.soton.ac.uk                   b.fischer@ecs.soton.ac.uk                    jpms@ucd.ie
arXiv:0911.3784v1 [cs.SE] 19 Nov 2009




                                                                 Abstract                                 bottleneck in verifying large embedded software, despite at-
                                                                                                          tempts to cope with increasing system complexity by apply-
                                            The complexity of software in embedded systems has in-        ing SMT (Satisfiability Modulo Theories) solvers [1, 8, 12].
                                        creased significantly over the last years so that software ver-       We address this bottleneck with a new concept called
                                        ification now plays an important role in ensuring the overall     continuous verification. It aims to automatically detect de-
                                        product quality. In this context, SAT-based bounded model         sign errors and integration problems as quickly as possi-
                                        checking has been successfully applied to discover subtle         ble by exploiting information from the software configu-
                                        errors, but for larger applications, it often suffers from the    ration management (SCM) system, systematically focusing
                                        state space explosion problem. This paper describes a new         the verification effort on new or modified functions. We use
                                        approach called continuous verification to detect design er-      equivalence checking to determine whether modified func-
                                        rors as quickly as possible by looking at the Software Con-       tions need to be re-verified formally and we use existing test
                                        figuration Management (SCM) system and by combining               cases to reduce the search space for the model checker, thus
                                        dynamic and static verification to reduce the state space         combining dynamic and static verification. We show that
                                        to be explored. We also give a set of encodings that pro-         the continuous verification approach substantially reduces
                                        vide accurate support for program verification and use dif-       the verification time of large embedded software.
                                        ferent background theories in order to improve scalability            We also exploit the different background theories of
                                        and precision in a completely automatic way. A case study         SMT solvers and combine different theories and solvers,
                                        from the telecommunications domain shows that the pro-            based on an analysis of the syntactic structure of a given
                                        posed approach improves the error-detection capability and        ANSI-C program. We then demonstrate that this combi-
                                        reduces the overall verification time by up to 50%.               nation significantly improves the performance of software
                                                                                                          model checking for a wide range of embedded software
                                                                                                          benchmarks from the telecommunications domain. This
                                                                                                          is the first work that exploits the syntactic structure of an
                                        1 Introduction                                                    ANSI-C program in order to combine different encodings
                                                                                                          and SMT solvers for BMC of embedded software.
                                            Embedded computer systems are used in a wide range of             We describe how these new (compared to our previous
                                        sophisticated applications, such as mobile phones or set-top      work [8]) contributions are realized in ESBMC, the Effi-
                                        boxes providing internet connectivity. The functionality de-      cient SMT-Based Bounded Model Checker. ESBMC ex-
                                        manded for such systems has increased significantly and an        tends CBMC [6] to support different theories and different
                                        increasing number of functions are implemented in software        SMT solvers and to make use of high-level information to
                                        rather than hardware. As a consequence, the verification of       simplify and reduce the unrolled formula size. Experimen-
                                        the software design and the correctness of its implementa-        tal results show that our approach scales significantly bet-
                                        tion have become increasingly difficult.                          ter than both the SAT-based and SMT-based versions of the
                                            Bounded model checking (BMC) has been successfully            CBMC model checker. In addition, the continuous verifi-
                                        applied to verify embedded software and discovered subtle         cation approach and the combination of different encodings
                                        errors in real designs [3]. BMC generates verification con-       and solvers allow us to go deeper into the system (compared
                                        ditions (VCs) that reflect the exact path in which a statement    to software model checkers only) and explore more exhaus-
                                        is executed, the context in which a given function is called,     tively the state space (compared to testing only). This hy-
                                        and the bit-accurate representation of the expressions. Prov-     brid solution is suitable for checking properties in large state
                                        ing the validity of these VCs remains the main performance        spaces.
2 Continuous Verification                                           1 unsigned s i g n a l I n v e r t e r ( i n t s i g n a l ) {
                                                                    2   unsigned i n v e r t e r ;
   Our approach has its roots in the continuous integration         3   i f ( s i g n a l >= 0 )
(CI) practice described by Fowler [11]. CI relies on every          4       inverter = signal ;
                                                                    5   else
developer to create and execute unit, functional and inte-
                                                                    6       i n v e r t e r = −1∗ s i g n a l ;
gration tests before committing their source code to a sin-         7   return i n v e r t e r ;
gle source repository. It also assumes the existence of an          8 }
automated unit test framework. The SCM is then used to
perform the system build and test processes in a completely                                             (a)
automatic way. In continuous verification, we use the same
                                                                    1 unsigned s i g n a l I n v e r t e r ( i n t s i g n a l ) {
information (i.e., development history and test cases) in a
                                                                    2   i f ( s i g n a l < 0)
different way to improve the coverage and substantially re-
                                                                    3       return −s i g n a l ;
duce the verification time throughout the development of a          4   else
product or product line. We use SMT-based bounded model             5       return s i g n a l ;
checking to verify for each system build that the entire sys-       6 }
tem still satisfies all properties given as assertions by the de-
signers, as well as a range of language-specific safety prop-                                           (b)
erties such as the absence of arithmetic under- and overflow,
out-of-bounds array indexing, or nil-pointer dereferencing.                Figure 2. (a) Original function to invert the
Figure 1 shows the main elements and steps of the con-                     sign of signal. (b) Optimized version.
tinuous verification approach; the gray boxes indicate core
steps. Section 3 describes the software verification process
in more detail.                                                         re-verifying the function. However, and more importantly,
                                                                        it also reduces overall system verification efforts because it
                             SCM
                                                   Property             limits the propagation of changes through the system: if we
                                                     LTL
                                                                        can prove the two versions of the function computationally
                                                                        equivalent, then we do not need to re-verify any other func-
                                                   Buechi
                    Check for modifications
                                                  Automata
                                                                        tion that depends it (unless that function has been changed
                                                                        as well). Of course, proving the equivalence of two func-
                       Modified Functions
                                                   Property             tions is in general undecidable, due to unbounded memory
                                                  Assertions
                                                                        usage [16], and the effort we spend in trying to do so might
                                                                        be wasted. However, in our experience, this does not occur
                                                                        very often, since a high degree of predictability is a desir-
             Dynamic         Test         Static
            Verification     Suite      Verification
                                                                        able design characteristic in embedded software (i.e., dy-
                                                                        namic memory allocations and recursion are discouraged).
              Check property and path coverage                              As an example, consider the two versions of the signal-
                                                                        Inverter function shown in Figure 2. They were extracted
                                                                        from the embedded software of two releases of a medical
           Figure 1. Continuous Verification                            device product. In order to prove the equivalence of these
                                                                        two ANSI-C functions, we compare their input-output re-
   For large embedded software, the computational effort                lations. We thus first (i) remove from each function the
to re-verify the entire software from scratch is too high,              variable declarations and return statements, (ii) convert the
and is largely wasted if, as is often the case, the changes             function bodies into single static assignment (SSA) form
are small [11]. For each system build, we thus consult                  [17] (i.e., we introduce fresh variables by subscripting the
the SCM to identify the functions and methods that have                 original name such that every assignment has a unique left
actually been modified and focus on these. We then use                  hand side), and (iii) conjoin all program statements. These
equivalence checking to determine whether they need to be               operations produce two intermediate formulas α1 and α2
re-verified formally: if we can prove that the old and new              representing the functions’ computations, as shown below.
versions of a function are functionally equivalent, then we
do not need to show for the new version any of the prop-                  inverter 1 = signal 1
erties already shown for the old version. This reduces the                ∧ inverter 2 = −1 ∗ signal 1
immediate verification effort because proving the equiva-                 ∧ inverter 3 = (signal 1 ≥ 0 ? inverter 1 : inverter 2 )
lence of two function versions is often less expensive than               signal ′2 = (signal ′1 < 0 ? −signal ′1 : signal ′1 )
                                                                          Buechi Automata                   ANSI-C Monitor
   For the actual equivalence check, we identify the input
variables (i.e., signal 1 = signal ′1 ), and show using SMT-                                              choice = nondet_uint()%2;
based bounded model checking that, given the representa-                                                  switch (state) {
                                                                                                            case init:
tion of the function bodies, the output variables then also                                                   if (r || !p)
coincide:                                                                                                        state=S3;
                                                                                                               else if (choice==0)
                                                                                                                 state=S1;
 (α1 ∧ α2 ∧ (signal 1 = signal ′1 )):(inverter 3 = signal ′2 )                 S1          S2
                                                                                                               else if (choice==1)
                                                                                                                 state=S2;
                                                                                                               break;
2.1    Specifying Temporal Properties with                                                                  case S1:
       Büchi Automata                                                                                        ...
                                                                               S3
                                                                                                            ...
                                                                                                          }
    In addition to the language-specific safety properties, we
can also show user-specified properties. These can be given
directly as assertions in the code, using C’s assert macro          Figure 3. Specifying Temporal Properties for
to state an assumption, or as formulas in linear-time tempo-        Software.
ral logic (LTL), which can track temporal properties of the
software design. We translate the LTL formulas into Büchi
automata using the Wring tool [21] and further into ANSI-        propositional expressions over the variables p and r. Fig-
C and merge them into the code. The resulting ANSI-C             ure 3 shows the non-determininistic Büchi automaton that
program then monitors the design’s progress and watches          represents the LTL formula (1) and its corresponding ANSI-
out for violations of the specified properties (as described     C monitor. The transition function δ is given by the follow-
in Section 3).                                                   ing table.
    As an example, we extract two properties from the spec-
ification of the medical device, and show how they can be                              1     r ∨ ¬p r ¬p
modelled and used in the context of the continuous verifica-                   init {S1, S2}   S3   init init
tion. The device, called a pulse oximeter [7], is responsible                  S1     S1       S1    S3 S1
for measuring the oxygen saturation (SpO2 ) and heart rate                     S2     S2       S2    S2 S3
(HR) in the blood system using a non-invasive method. In                       S3     S3       S3    S3 S3
particular, we verify (a) the data flow to compute the HR
value that is provided by the pulse oximeter sensor hard-
                                                                 From the initial state, we can transition to S3 if r∨¬p holds,
ware and (b) whether the user of the pulse oximeter is ca-
                                                                 stay in the initial state if either r, or ¬p holds, or nondeter-
pable of adjusting the sample time of the embedded device.
                                                                 ministically transition to either S1 or S2 if none of the three
The properties (a) and (b) can be expressed using the fol-
                                                                 properties hold (denoted by 1). This automaton will accept
lowing LTL pattern:
                                                                 all infinite words that represent computations in which each
                       AG (p → F r)                        (1)   state in which p holds will eventually be followed by a state
                                                                 in which r holds. In order to model the nondeterministic
Here, A (“for all paths”), G (“always”), and F (“eventu-         transition of the Büchi-automata in the ANSI-C specifica-
ally”) are the LTL quantifiers, and p and r represent the        tion, we use a function nondet uint() (which returns any
required pre- and post-states. In the example, for the prop-     number of type unsigned int) and then restricts its returning
erty (a), p denotes the state that the buffer contains HR and    value to the domain {0, 1}. The property is then checked by
SpO2 raw data, while r denotes the state that defines the re-    using a “monitor” in such a way that the C program moni-
spective HR value. Consequently, any state containing the        tors the design’s progress and watches out for a specific type
HR and SpO2 raw data in the buffer is eventually followed        of error up to the bound k. An assertion is then used to claim
by a state representing the respective HR value.                 that an error is never encountered. In our example, we en-
    A Büchi automaton is a finite automaton over infinite       sure that the buffer is not empty and contains the computed
words. It differs from a standard finite automaton over fi-      HR and SpO2 values.
nite words in the definition of accepting a word, which is
based on passing through an accepting state infinitely of-       2.2    Generalizing Test Cases
ten (rather than terminating in a final state) [5]. The Büchi
automata we consider here work over computation traces,             After detecting new and/or modified functions, we use
i.e., sequences of states of the program to be analyzed.         the existing unit test cases to reduce the state space to be ex-
These are abstracted by the predicates of interest (here p and   plored by the model checker. In this phase, we first run the
r). Hence the “words” can be represented by sequences of         unit tests, keeping track of which inputs have already been
     used. We then guide the model checker to visit states that         1  s t a t i c void t e s t C i r c u l a r B u f f e r ( void ){
     have not been visited previously. In addition, the test cases      2      i n t s e n D a t a [ ] = { 1 , −128 , 9 8 , 8 8 , 5 9 ,
     also help to reduce the state space to be explored in another       3                                 1 , −128 , 9 0 , 0 , −37};
     way: by using the test stubs, we can break the global model         4     int i ;
     (containing the entire program) into local models (contain-         5     initLog (5);
     ing only the functions under test) and generate on-demand           6     f o r ( i = 0 ; i <10; i ++)
                                                                         7         insertLogElem ( senData [ i ] ) ;
     the reachable states to be visited by the model checker, start-
                                                                         8     f o r ( i = 5 ; i <10; i ++)
     ing with the state described by the test case. We can so            9         TEST ASSERT EQUAL INT ( s e n D a t a [ i ] ,
     reduce the number of paths and variables to be considered          10                                             removeLogElem ( ) ) ;
     during model checking.                                             11 }

        As an example consider the three simple C functions
     shown in Figure 4 that were also extracted from the pulse
     oximeter embedded software, and one of the test cases                     Figure 5. A unit test for the functions shown
     shown in Figure 5. The functions implement a simple cir-                  in Figure 4.
     cular buffer using a FIFO (First In, First Out) policy. The
     test case checks whether messages are correctly added to
     and removed from the circular buffer using the FIFO policy.            line 12 in Figure 4). However, in general this approach
     Other test cases check for buffer underflow and/or overflow            can lead to false positives because the non-deterministic
     and whether the elements are lost before reading them from             choice of values for program variables may force the ex-
     the buffer.                                                            ploration of paths that are infeasible in the original pro-
                                                                            gram. Rather than modifying the program we thus modify
 1 s t a t i c char b u f f e r [BUFFER MAX ] ;
                                                                            the test stubs and replace the concrete input values by non-
 2 v o i d i n i t L o g ( i n t max ) {
                                                                            deterministic choices. Here, we replace the initialization
 3     b u f f e r s i z e = max ;
 4     f i r s t = next = 0;                                                of the array senData (see line 2 and 3 of Figure 5) by int
 5 }
                                                                            senData[] = {nondet int(),. . . ,nondet int()}. We then use
 6                                                                          assume-statements to force the model checker away from
7  i n t removeLogElem ( v o i d ) {                                        the values that have already been explored during testing.
 8     f i r s t ++;                                                        In order to block larger parts of the search space, we use
 9     r e t u r n b u f f e r [ f i r s t −1];                             the given concrete values from all stubs and combine the
10 }                                                                        respective values into a single interval for each variable or
11
                                                                            array element; here we assume that all “obvious” bound-
12 void i ns er t L ogE l em ( i n t b ) {                                  ary values are used in some of the stubs, so that we are not
13   i f ( next < b u f f e r s i z e ) {
                                                                            blocking parts of the search space contain “obvious” errors
14      buffer [ next ] = b ;
                                                                            but force the model checker towards the “unobvious” er-
15      n e x t = ( n e x t +1)% b u f f e r s i z e ;
16      a s s e r t ( n e x t <b u f f e r s i z e ) ;                      rors. In the example, we thus add an assume-statement such
17   }                                                                      as assume(senData[0]<=1 && senData[0]>=42) and are
18 }                                                                        then able to find two bugs related to overflow and under-
                                                                            flow.

        Figure 4. Implementation of a circular buffer.
                                                                            3 SMT-based Bounded Model Checking of
         The pulse oximeter sources contain seven test cases,                 Embedded ANSI-C Software
     which intend to cover all possible execution paths related
     to the circular buffer, and during dynamic verification, we                In BMC, the program to be analyzed is modelled as a
     are not able to find any bug in the circular buffer implemen-          state transition system, which is built by extracting its be-
     tation with these. However, the implementation is flawed:              haviour from the control-flow graph (CFG) [17]. This graph
     the array buffer is declared to be of type char[] (see line 1 in       is used as part of a translation process from program text to
     Figure 4) but we assign an element b of type int (see line 14)         SSA-form. A node in the CFG represents either a deter-
     The test cases do not uncover this error because they happen           ministic or non-deterministic assignment or a conditional
     to use only integer values that can safely be cast to a char.          statement, while an edge in the CFG represents the ability
         Using SMT-based BMC, we can detect this bug by                     of the program to change the control location.
     non-determininistically assigning a value to the parame-                   A state transition system M = (S, S0 , γ) is an abstract
     ter b (i.e., by adding an assignment b = nondet int() after            machine that consists of a set of states S (where S0 ⊆ S
represents the set of initial states) and γ ⊆ S × S is the          1 i n t main ( ) {
concrete transition relation [5]. A state s ∈ S consists of         2 int a [2] , i , x ;
the value of the program counter pc and the values of all           3 if    ( x ==0)
program variables. An initial state s0 assigns the initial pro-     4     a [ i ]=0;
                                                                    5 else
gram location of the CFG to the pc. We identify each tran-
sition γ = (si , si+1 ) between two states si and si+1 with         6     a [ i +2]=1;
                                                                    7 assert ( a [ i +1]==1);
a logical formula γ(si , si+1 ) that captures the constraints
                                                                    8 }
on the corresponding values of the program counter and the
program variables.                                                                                      (a)
    Given a transition system M, a property φ, and a bound
k, BMC unrolls the system k times and translates it into            1 g1 ==      ( x1 == 0 )
a verification condition ψ such that ψ is satisfiable if and        2 a1 ==      ( a0 WITH [ i 0 : = 0 ] )
                                                                    3 a2 ==      a0
only if φ has a counterexample of depth less than or equal
                                                                    4 a3 ==      ( a2 WITH [ 2 + i 0 : = 1 ] )
to k. The VC ψ is a quantifier-free formula in a decidable          5 a4 ==      ( g1 ? a1 : a3 )
subset of first-order logic, which is then checked for satis-       6 t 1 ==     ( a4 [ 1 + i 0 ] == 1 )
fiability by an SMT solver. In this work, we are interested
in checking two classes of properties: safety and liveness.                                             (b)
The model checking problem associated with SMT-based
BMC for checking safety properties is then formulated by                   Figure 6. (a) A C program with violated prop-
constructing the following logical formula [1, 12]:                        erty. (b) The C program of (a) in SSA form.
                                               property
                           k−1
                           ^                      z}|{
         ψ k = I (s0 ) ∧         γ (si , si+1 ) ∧ ¬φkG       (2)
                                                                        Here, we focus on how to reduce the number of redundant
                           i=0
                |            {z            }                            variables generated from the BMC instances.
                        constraints
                                                                            We use the code in Figure 6 as a running example. Fig-
where φkG represents a safety property φG in step k, I is the           ure 6(a) shows a syntactically valid C program that acci-
function for the set of initial states of M and γ (si , si+1 ) is       dentally writes to an address outside the allocated memory
the function of the transition relation of M at time steps i            region of the array a (line 6). Figure 6(b) shows the pro-
                                   Vk−1                                 gram in SSA form, where it only consists of if instructions,
and i + 1. Hence, the formula i=0 γ (si , si+1 ) unrolls the
                                                                        assignments and assertions. As we can see in Figure 6(b),
transition system and then represents the set of all execu-
                                                                        for each assignment of the form a = expr (lines 4 and 6 from
tions of M up to the length k or less. ¬φkG represents the
                                                                        Figure 6(a)), the left-hand side variable is replaced by a new
condition that φG is violated by a bounded execution of M
                                                                        variable (e.g., a1 , a3 ). In addition, the if condition in line 3
of length k or less. A counterexample for a property φG is
                                                                        is replaced by a guard (e.g., g1 ), the array index i in lines 3,
a sequence of states s0 , s1 , . . . , sk with s0 ∈ S0 , sk ∈ S,
                                                                        6 and 7 is replaced by i0 (note that the variable i is not mod-
and γ (si , si+1 ) for 0 ≤ i < k. Liveness properties φF are
                                                                        ified in the C program of Figure 6(a)) and the assert macro
checked by encoding ¬φiF in a loop within a bounded exe-
                                                                        in line 7 is replaced by a Boolean variable t1 . From this
cution of length at most k, such that φF is negated on each
                                                                        representation, we build the constraints (C) and properties
state in the loop [3]. In this case, formula (2) is rewritten as:
                                                                        (P ) formulae shown in (4) and (5) using the quantifier-free
                        k−1                      k
                                                        !               fragment of the first-order theories (e.g., linear arithmetic,
                         ^                      _
          k
        ψ = I (s0 ) ∧        γ (si , si+1 ) ∧      ¬φFi
                                                              (3)       arrays), which are then passed to an SMT solver as C∧¬P
                       i=0                     i=0                      to check satisfiability.

  For further information about the main software compo-                                                               
                                                                                         g1 := (x1 = 0)
nents of our ESBMC tool, we refer the reader to [8].                                    ∧ a1 := store(a0 , i0 , 0)     
                                                                                                                       
                                                                                  C :=  ∧ a2 := a0
                                                                                                                       
                                                                                                                                     (4)
3.1    Optimizations                                                                    ∧ a3 := store(a2 , 2 + i0 , 1) 
                                                                                         ∧ a4 := ite(g1 , a1 , a3 )
   ESBMC implements some standard code optimization
                                                                                                                   
techniques such as constant folding, forward substitution,                                i0 ≥ 0 ∧ i0 < 2
and reduction of variables [17]. In our previous work [8],                               ∧ 2 + i0 ≥ 0 ∧ 2 + i0 < 2 
we described how constant folding and forward substitution                         P :=                            
                                                                                         ∧ 1 + i0 ≥ 0 ∧ 1 + i0 < 2                  (5)
are implemented in the context of bounded model checking.                                 ∧ select(a4 , i0 + 1) = 1
   However, the SSA transformation in the CBMC front-               in the fractional part if there are bits missing after the radix
end introduces redundant variables, which creep into the            point (e.g., 0.75 + 0.125 = h0000.1100i + h0000.0010i) or
formula passed into the SMT-solver, thus increasing the             we add bits from the left using sign-extension if there are
search space. Figure 6(b) shows an example of an addi-              bits missing before the radix point. On the other hand, us-
tional (redundant) variable (i.e., a2 ) created in order to keep    ing rational arithmetic, we encode fixed-point numbers by
                                                                                     m+n
the value of array a before the if statement in line 3 of Fig-      mapping {0, 1}         → Q, which extracts the integer part
ure 6(a). In our back-end, we eliminate functionally deter-         and divides the fraction part hF i /2n and finally converts
mined variables by substitution. In our running example,            the resulting number to a rational one in base 10. As a re-
a2 == a0 holds in all states, so we can eliminate this con-         sult, the arithmetic operations are performed in the domain
straint and the variable a2 by substituting every occurrence        of Q instead of R and there is no need to add missing bits to
of a2 by a0 . we thus rewrite (4) as:                               the integer and fractional parts. In general, the drawback is
                                                                  that some numbers are not precisely represented with fixed-
                   g1 := (x1 = 0)                                   point arithmetic. However, we have not detected any false
                 ∧ a1 := store(a0 , i0 , 0)                       positives due to use of fixed-point arithmetic in any of our
          C :=  ∧ a3 := store(a0 , 2 + i0 , 1) 
                                                             (6)
                                                                    benchmarks.
                   ∧ a4 := ite(g1 , a1 , a3 )

Eliminating functionally determined variables allows us to          3.2.2 Dynamic Memory Allocation
remove most of the intermediate variables generated dur-            Although dynamic memory allocation is discouraged in em-
ing the symbolic execution and consequently the size of the         bedded software, ESBMC is capable of model checking
final formula to be sent to the SMT solver.                         programs that use it through the ANSI-C functions mal-
                                                                    loc and free. ESBMC checks two properties related to dy-
3.2    Encodings                                                    namic memory allocation: (i) whether the argument to any
                                                                    malloc, free, or dereferencing operation is a dynamic ob-
   In this section, we focus on new encodings (compared to          ject (IS DYNAMIC OBJECT) and (ii) whether the argument
our previous work [8]) that allow us to analyze more com-           to any free or dereferencing operation is still a valid object
plex ANSI-C programs and show how to exploit different              (VALID OBJECT).
data types and solvers to speed up the verification process.            Formally, let po be a pointer expression that points to the
                                                                    object o of type t and let a be an array of type t and size
3.2.1 Fixed-Point Arithmetic                                        n, where n is of integer type and represents the number of
                                                                    elements to be allocated. In our encoding, each dynamic
Embedded applications from discrete control and telecom-            object has an unique identifier denoted by ρk , where the
munications domains often require arithmetic on non-                subscript k indicates the objects “serial number” in sequen-
integral numbers. However, full floating-point arithmetic           tial order of all dynamically created objects. Let i be an
is too heavyweight to be encoded into the BMC framework;            integer variable that indicates the position in which the ob-
instead, we approximate it by fixed-point arithmetic and use        ject pointed to by po must be stored in array a. We thus
two different representations: in base 2 (when dealing with         encode IS DYNAMIC OBJECT as a literal ld with the fol-
bit-vector arithmetic) and in base 10 (when dealing with ra-        lowing constraint:
tional arithmetic). Hence, in fixed-point arithmetic, we en-                                         !
code the numbers using the integer part and fractional part                             k−1
                                                                                         _
(i.e., after the radix point “.”) [16]. For instance, the num-                 ld ⇔          ρn = po ∧ (0 ≤ i < n)              (7)
bers 0.75 and 0.125 are fixed-point numbers with two-digit                             n=0

and three-digit fractional parts respectively. The number               To check for invalid objects, we add one additional bit
0.75 can be represented as h0000.11i in base 2 or 3/4 in base       field ν to each dynamic object to indicate whether it is still
10 while the number 0.125 can represented as h0000.0010i            alive or not. Let ⊥ denote the state that the object is not
in base 2 or 125/1000 in base 10. Given a rational number           alive. We then encode VALID OBJECT as a literal lv with
R that consists of an integer part I with m bits and a frac-        the following constraint:
tion part F with n bits, we represent R by I.F and denote
it by hI.F i /2n .                                                                        lv ⇔ (po .ν 6= ⊥)                     (8)
    Using bit-vector arithmetic, we encode fixed-point arith-
metic exactly as in binary encoding and assume that the
                                                                    3.2.3 Exploiting Datatypes and Solvers
numbers have the same bitwidth before and after the radix
point. If the numbers do not have the same bitwidth (e.g., if       Modern SMT solvers provide ways to model the program
we want to sum 0.75 and 0.125), we add zeros from the right         variables as bit-vectors or as elements of a numerical do-
    main (e.g., Z, Q, or R). If the program variables are mod-         versa, we encode the corresponding variables as bit-vectors
    elled as bit-vectors of fixed size, then the result of the anal-   and switch the SMT solver either to Boolector (if no point-
    ysis can be precise (w.r.t. the ANSI-C semantics), depend-         ers are used) or Z3 (if pointers are used).
    ing on the size considered for the bit-vectors. On the other
    hand, if the program variables are modelled as numerical           4 Experimental Evaluation
    values, then the result of the analysis is independent from
    the actual binary representation, but the analysis may not be
                                                                           The experimental evaluation of our work consists of
    precise when arithmetic expressions are involved. As a mo-
                                                                       three parts. Section 4.1 contains the results of applying
    tivating example, consider the following small C program
                                                                       ESBMC to the verification of six sets of ANSI-C bench-
    from [6] as shown in Figure 7.
                                                                       marks. The purpose of this first part is to check the error-
                                                                       detection capability of ESBMC since most of these bench-
1  i n t main ( ) {
                                                                       marks contain ANSI-C programs with and without bugs.
2      u n s i g n e d char a , b ;
 3     u n s i g n e d i n t r e s u l t =0 , i ;                      Section 4.2 contains the experimental results of applying
 4     a= n o n d e t u c h a r ( ) ;                                  ESBMC and CBMC to the verification of embedded soft-
 5     b= n o n d e t u c h a r ( ) ;                                  ware used in the telecommunications domain. The purpose
 6     f o r ( i = 0 ; i <8; i ++)                                     of this second part is to evaluate ESBMC’s relative perfor-
 7         i f ( ( b>>i )&1)                                           mance against CBMC using embedded software industrial
 8              r e s u l t +=( a<<i ) ;                               applications. Section 4.3 contains the results of applying the
 9     a s s e r t ( r e s u l t == a ∗b ) ;                           continuous verification approach, described in Section 2, to
10 }
                                                                       large embedded software used in a commercial product.
                                                                           All experiments were conducted on an otherwise idle In-
       Figure 7. A C program that uses shift-and-add                   tel Pentium Dual CPU, 2GHz with 4 GB of RAM running
       to multiply two numbers.                                        Linux OS. For all benchmarks, the time limit has been set
                                                                       to 3600 seconds for each individual property. All times
                                                                       given are wall clock time in seconds as measured by the
        This program nondeterministically selects two values of        unix time command through a single execution.
    type unsigned char and uses bitwise AND, right- and left-
    shift operations to multiply them. Reasoning about this pro-       4.1    Error-Detection Capability
    gram by means of integer arithmetic produces wrong results
    if the bit-level operators are treated as uninterpreted func-          As a first step, we analyze to which extent ESBMC is
    tions (UFs). Although UFs simplify the proofs, they ignore         able to handle standard ANSI-C benchmarks. For this pur-
    the semantics of the operators and consequently make the           pose, we analyzed the programs in the VERISEC, NECLA,
    formula weaker. In addition, the majority of the software          SNU-RT, PowerStone, and WCET benchmarks. VERISEC
    model checkers (e.g., SMT-CBMC [1] and BLAST [14])                 and NECLA are not related to embedded software, but
    fail to check the assertion in line 9. On the other hand, bit-     they allow us to check the error-detection capability of the
    vector arithmetic allows us to encode bit-level operators in a     model checkers since these benchmarks provide ANSI-C
    more accurate way. However, in our benchmarks, we noted            programs with and without bugs including dynamic me-
    that the majority of VCs are solved faster if we model the         mory allocation, interprocedural dataflow, aliasing, and
    basic datatypes as integer and/or real. Consequently, we           string manipulation. The remaining three benchmarks con-
    have to trade off between speed and accuracy which might           tain ANSI-C constructs found in embedded software.
    be two competing goals in formal verification using SMT.               Table 1 summarizes the results of applying ESBMC to
        Based on the extent to which the SMT solvers support           the verification of the standard ANSI-C benchmarks; a de-
    the domain theories and on experimental results obtained           tailed description of these experimental results is avail-
    with a large set of benchmarks, we developed a simple but          able at users.ecs.soton.ac.uk/lcc08r/esbmc.
    effective heuristic to determine the best representation for       Here, #L denotes the total number of lines of code, B de-
    the program variables as well as the best SMT-solver to be         notes the unwinding bound, and #P denotes the number of
    used in order to check the properties of a given ANSI-C            properties to be verified for each ANSI-C program. The
    program. Our default representation for encoding the con-          Time columns contain the total time in seconds to check all
    straints and properties of ANSI-C programs are integers and        properties of a given ANSI-C program, broken down into
    reals, respectively, and our default solver is Z3. We then ex-     frontend (i.e., encoding) and backend (i.e., decision proce-
    plore the CFG representation of the program. If we find            dure). Failed indicates how many properties failed during
    expressions that involve bit operations (e.g., <<, >>, &, |,       the verification process; properties can fail for two reasons:
    ⊕) or typecasts from signed to unsigned datatypes and vice-        either due to time out (TO) or due to memory out (MO).
                                                                               Time                         #P




                                                                               Procedure
                                                                 Encoding


                                                                               Decision




                                                                                                             Violated
                                                                                                   Passed



                                                                                                                        Failed
                                                                                           Total
                                   Module         #L #P
                               1   VERISEC       9090 2148 190.85 228.35  419.2 1946 202 0
                               2   NECLA         1011 208   59.28   88.9 148.18 188 20 0
                               3   SNU-RT        3102 790 3166.94 12.18 3179.12 762 28 0
                               4   WCET          3430 726   72.72   8.28     81 722    4 0
                               5   POWERSTONE    2957 2053 127.36 913.64  1041 2043 10 0



                          Table 1. Results of the error-detection capability with ESBMC.


   As mentioned previously, benchmarks VERISEC and                          as modules exStbResolution and exStbHDMI due to time
NECLA contain ANSI-C programs with and without bugs                         out and segmentation fault. Both CBMC and ESBMC fail
and all inputs are replaced by nondeterministic one. In                     to model check the module exStbDemo, which contains
these benchmarks, ESBMC is able to detect common de-                        approximately 31KLOC and represents the largest mod-
sign errors related to buffer overflow, aliasing, dynamic me-               ule that we analyzed. However, the results indicate that
mory allocation, and string manipulation. In the remaining                  ESBMC scales significantly better than CBMC for prob-
benchmarks, ESBMC is able to model check ANSI-C pro-                        lems that involve tight interplay between non-linear arith-
grams that involve tight interplay between non-linear arith-                metic, bit operations, pointers and arrays.
metic, bit operations, pointers and array manipulations. In
addition, ESBMC was able to find undiscovered bugs in the                   4.3        Scalability
SNU-RT, WCET, and PowerStone benchmarks related to
arithmetic overflow, invalid pointer and pointer arithmetic.                    In order to model check the exStbDemo module we apply
We also checked the effect of eliminating functionally de-                  the continuous verification approach as described in Sec-
termined variables and we observed that the total verifica-                 tion 2; Table 3 summarizes the results. Here, #TC denotes
tion time can only be reduced by 0.3% to 1% in the bench-                   the total number of test cases. For the dynamic verifica-
marks. We believe that the SMT solvers already eliminate                    tion, we use the EmbUnit1 unit test framework, which pro-
the redundant variables during the pre-processing phase.                    vides means to apply assertion-based verification in embed-
                                                                            ded software written in C through a set of macros to assert
4.2    Comparison to CBMC                                                   strings, integers, pointer value, and conditions.
                                                                                As described in Section 4.2, the state-of-the-art model
   In order to evaluate ESBMC’s performance relative to                     checkers fail to verify the properties of the exStbDemo ap-
CBMC, we analyzed the embedded software used in a com-                      plication due to memory limitations. However, if we use
mercial product from NXP semiconductors [18], a set-top                     the test cases to guide the state space exploration, we can
box that is used in high definition internet protocol (IP) and              not only define the functions, but also the state variables
hybrid digital TV applications. The embedded software of                    that were not yet fully explored during dynamic verifica-
this platform relies on the Linux operating system and use                  tion. As a result, in the function commandLoop, ESBMC
the LinuxDVB, DirectFB and ALSA applications.                               finds a property violation related to an invalid pointer in
                                                                            4.39 seconds using an unwinding bound of 6. However,
   We evaluated CBMC version 3.3.2 and we invoked both
                                                                            we are not able to increase further the unwinding bound of
tools (i.e., CBMC and ESBMC) by setting manually the file
                                                                            functions commandLoop and getCommand due to memory
name, the unwinding bound and the overflow check. CBMC
                                                                            limitations.
has support for SAT and SMT solvers in the back-end and
                                                                                We had access, from the NXP development team, to four
in our comparison we use the SMT solver Z3 for evaluating
                                                                            different product releases (PRs) that contain the applica-
both tools CBMC and ESBMC. Table 2 shows the results
                                                                            tion exStbDemo. Based on these four PRs, we identified
when applying SAT-based CBMC, SMT-based CBMC and
                                                                            the functions and methods that have actually been modi-
ESBMC to the verification of the embedded applications.
                                                                            fied and focus on these since the computational effort to
SAT-based CBMC performs better than SMT-based CBMC
                                                                            re-verify each system build from scratch is too high. The
since it is able to analyze one additional embedded applica-
                                                                            four PRs are shown on the right-hand side in Table 3 as PR
tion (viz. exStbCc).
                                                                            10, 11, 12, 13. The development time of each PR is about
   CBMC is not able to check the modules exStbKey,
exStbFb, and exStbDemo due to memory limitations as well                      1 EmbUnit. http://embunit.sourceforge.net/
                                                         SAT-based CBMC                                                     SMT-based CBMC                                             ESBMC
                                                        Time          #P                                                    Time       #P                                     Time                              #P




                                                 Procedure




                                                                                                                    Procedure




                                                                                                                                                                      Procedure
                                                 Decision




                                                                                                                    Decision




                                                                                                                                                                      Decision
                                                                                            Violated




                                                                                                                                                  Violated




                                                                                                                                                                                                                Violated
                                                                                 Passed




                                                                                                                                         Passed




                                                                                                                                                                                                       Passed
                                                                                                        Failed




                                                                                                                                                             Failed




                                                                                                                                                                                                                               Failed
                                                                 Total




                                                                                                                                 Total




                                                                                                                                                                                         Total
           Module           #L    B  #P
      1    exStbKey         558   1   22    0.1   3.13 22 0    0 0.18 3.13 22 0    0   0.02    1.09 22 0    0
      2    exStbHDMI       1508   11  41      †      †   0 0 41     †    †   0 0 41 128.44 211.02 41 0      0
      3    exStbLED         430   10  59   MO     MO     0 0 59 TO TO        0 0 59    1781 1817.61 59 0    0
      4    exStbHwAcc      1432 1000 115 0.146    2.44 115 0   0 0.71 3.05 115 0   0  0.013   0.937 115 0   0
      5    exStbResolution 353   150 32     TO     TO    0 0 32 TO TO        0 0 32 1179.34 1596.62 32 0    0
      6    exStbFb          689   30  48   MO     MO     0 0 48     †    †   0 0 48   50.53 138.31 48 0     0
      7    exStbCc          331  200   5 174.49 198.19   5 0   0 TO TO       0 0   5  31.24   46.13   5 0   0
      8    exStbDemo       30902 17 267    MO     MO     0 0 267 MO MO       0 0 267    MO      MO    0 0 267



   Table 2. Results of the comparison between CBMC and ESBMC. Time-outs are represented with TO
   in the Time column; Examples that exceed available memory are represented with MO in the Time
   column; Internal errors in the tool are represented with † in the Time column.


                                                                     ESBMC                                                         EmbUnit                                         Subversion
                                                             Time (s)                                  #P
                                                     Procedure
                                                     Decision




                                                                                                        Violated
                                                                                          Passed



                                                                                                                   Failed
                                                                         Total




            Function                  B #P                                                                                      #TC      Time (s)                 PR10            PR11           PR12              PR13
       1    getCommand                6 237 <0.2             4.39     236 1                                        0             18       <0.1                     X               X              X
       2    commandLoop               6 237 70.22 128.41 237 0                                                     0             26       <0.1                     X                                                       X
       3    checkCommandParams       17 229 73.29 161.14 229 0                                                     0             4        <0.1                     X               X               X                       X
       4    checkEndOfPvrStream      20 228 <0.1             4.34     228 0                                        0             3        <0.1                     X                                                       X
       5    checkEndOfIPStream       20 228 <0.1             3.99     228 0                                        0             3        <0.1                     X
       6    checkEndOfMediaStream 20 228 <0.1                3.97     228 0                                        0             4        <0.1                     X
       7    setupFramebuffers        17 228 <0.1             4.22     228 0                                        0             2        <0.1                     X               X                                       X
       8    setupFBResolution        17 228 <0.1             3.92     228 0                                        0             2        <0.1                     X                               X
                              Total verification time in seconds for each PR                                                                                     314.38       169.75             169.45         298.11


                                 Table 3. Results of the continuous verification approach.


one month and each one contains new features, enhance-                                                      ent search strategies on multi-core machines [15]. It is the
ments (through refactoring), and bug fixes. We use PR10                                                     main interface to the SPIN model checker to verify larger
as a reference (and starting point) to compare with PR11,                                                   systems. This approach, however, involves large communi-
PR11 to compare against PR12 and so on. The functions                                                       cation overhead and does not take into account information
2-8 shown in Table 3 do not present input/output relations                                                  from the SCM system in order to focus the verification ef-
and the function getCommand is not equivalent in PR10,                                                      fort on new and/or modified functions.
PR11 and PR12. However, if we compare PR10 to PR11                                                             Peled proposes a set of combinations between model
and PR12, we can reduce the verification time by up to 50%                                                  checking and testing, which includes black box checking,
since functions checkEndOfIPStream and checkEndOfMe-                                                        adaptive model checking, and unit checking [19]. However,
diaStream are not modified in four different versions. In                                                   he does not consider the development history from the SCM
addition, the function commandLoop, which represents one                                                    system and also uses explicit model checking based on au-
of the hardest functions, is only modified in PR13.                                                         tomata theory, which does not scale well due to the number
                                                                                                            of program variables and data type widths [10]. In addition,
5 Related Work                                                                                              Peled only describes the techniques, but does not apply it to
                                                                                                            any commercial product. Gunter and Peled [13] extend this
   One way of tackling large verification problems is to                                                    approach by proposing a symbolic verification approach for
leverage both parallelism and search diversity [15]. Holz-                                                  a unit of code, also called unit checking. The authors, how-
mann et al. describe the Swarm tool that allows to use differ-                                              ever, apply this approach only to check whether a complex
number diverges to infinity, while we focus on the verifi-        the state space coverage and to verify quickly the negation
cation of large embedded software. Sen proposes an ap-            of properties in larger state spaces.
proach to execute a program concretely and symbolically
by combining random testing and symbolic execution [20].          References
This approach, however, might fail to compute concrete val-
ues that satisfy a given path constraint due to the constraint     [1] A. Armando, J. Mantovani, and L. Platania. Bounded model
solver performance.                                                    checking of software using SMT solvers instead of SAT
    SMT-based BMC is gaining popularity in the formal ver-             solvers. Int. J. Softw. Tools Technol. Transf., vol(11), pp.
ification community due to the advent of sophisticated SMT             69–83, 2009.
solvers built over efficient SAT solvers [4, 9]. Ganai and         [2] D. Babić and A. J. Hu. Calysto: Scalable and Precise Ex-
                                                                       tended Static Checking. In ICSE, pp. 211–220, 2008.
Gupta describe a verification framework for BMC which              [3] A. Biere. Bounded model checking. In Handbook of Satis-
extracts high-level design information from an extended fi-            fiability, pp. 457–481. 2009.
nite state machine (EFSM) and applies several techniques           [4] R. Brummayer and A. Biere. Boolector: An efficient SMT
to simplify the BMC problem [12]. However, the authors                 solver for bit-vectors and arrays. In TACAS, LNCS 5505, pp.
flatten the structures and arrays into scalar variables in such        174–177, 2009.
a way that they use only the theory of integer and real arith-     [5] E. Clarke, O. Grumberg, and D. Peled. Model Checking.
                                                                       The MIT Press, Cambridge, MA, 2000.
metic, which does not reflect precisely the ANSI-C seman-          [6] E. Clarke et al. A tool for checking ANSI-C programs. In
tics. Armando et al. also propose a BMC approach using                 TACAS, LNCS 2988, pp. 168–176, 2004.
SMT solvers for ANSI-C programs [1]. In this approach,             [7] L. Cordeiro et al. Agile development methodology for em-
however, they only make use of linear arithmetic (addition             bedded systems: A platform-based design approach. In
and multiplication by constants), arrays, records and bit-             ECBS, pp. 195–202, 2007.
vectors and as a consequence, their SMT-CBMC prototype             [8] L. Cordeiro, B. Fischer, and J. Marques-Silva. SMT-based
does not address important constructs of the ANSI-C lan-               bounded model checking for embedded ANSI-C software.
                                                                       To appear in ASE. http://eprints.ecs.soton.ac.uk/18166/.
guage (e.g., non-linear arithmetic and bit-shift operations).
                                                                       2009.
    Recently, a number of static checkers have been devel-         [9] L. M. de Moura and N. Bjørner. Z3: An efficient SMT
oped in order to trade off scalability and precision. Ca-              solver. In TACAS, LNCS 4963, pp. 337–340, 2008.
lysto is a static checker that is able to verify VCs related      [10] V. D’Silva, D. Kroening, and G. Weissenbacher. A sur-
to arithmetic overflow, nil-pointer dereferencing and asser-           vey of automated techniques for formal software verifica-
tions specified by the user [2]. The VCs are passed to the             tion. IEEE Trans. on CAD of Integrated Circuits and Sys-
SMT solver SPEAR which supports bit-vector arithmetic                  tems, 27(7):1165–1178, 2008.
                                                                  [11] M. Fowler.        Continuous Integration.      ThoughtWorks.
and is customized for the VCs generated by Calysto. How-
                                                                       http://martinfowler.com, 2006.
ever, Calysto does not support float-point operations and un-     [12] M. K. Ganai and A. Gupta. Accelerating high-level bounded
soundly approximates loops by unrolling them only once.                model checking. In ICCAD, pp. 794–801, 2006.
As a consequence, soundness is relinquished for perfor-           [13] E. L. Gunter and D. Peled. Model checking, testing and veri-
mance. Saturn is another efficient static checker that scales          fication working together. Formal Asp. Comput., 17(2):201–
to larger systems, but with the drawback of losing precision           221, 2005.
                                                                  [14] T. A. Henzinger et al.                     BLAST: Berkeley
by supporting only the most common integer operators and
                                                                       Lazy       Abstraction     Software      Verification  Tool.
performing at most two unwindings of each loop [22].                   http://mtc.epfl.ch/software-tools/blast/, 2009.
                                                                  [15] G. J. Holzmann, R. Joshi, and A. Groce. Tackling large veri-
6 Conclusions                                                          fication problems with the swarm tool. In SPIN, LNCS 5156,
                                                                       pp. 134–143, 2008.
                                                                  [16] D. Kroening and O. Strichman. Decision Procedures: An
   In this work, we have defined a new concept called con-             Algorithmic Point of View. Springer Publishing Company,
tinuous verification and we have applied it to the verifica-           Incorporated, 2008.
tion of large embedded software used in the telecommuni-          [17] S. S. Muchnick. Advanced compiler design and implemen-
cations domain. In addition, we have described a new set               tation. Morgan Kaufmann Publishers Inc., 1997.
                                                                  [18] NXP. High definition IP and hybrid DTV set-top box
of encodings that allow us to reason accurately about em-
                                                                       STB225. http://www.nxp.com/, 2009.
bedded software by discovering subtle bugs in several in-         [19] D. Peled. Model checking and testing combined. In ICALP,
dustrial applications and to scale for large embedded soft-            pp. 47–63, 2003.
ware. Furthermore, the experimental results show that our         [20] K. Sen. Concolic testing. In ASE, pp. 571–572, 2007.
SMT-based model checker (ESBMC) outperforms both the              [21] F. Somenzi and R. Bloem. Efficient Büchi automata from
SAT-based and SMT-based CBMC [6] model checker if we                   LTL formulae. In In CAV, LNCS 1855, pp. 247–263, 2000.
                                                                  [22] Y. Xie and A. Aiken. Scalable error detection using Boolean
consider the verification of embedded software. As a result,           satisfiability. SIGPLAN Not., vol(40), pp. 351–363, 2005.
our approach represents a promising direction to improve
