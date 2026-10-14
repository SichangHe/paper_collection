                                             AutoDeduct: A Tool for Automated Deductive
                                                        Verification of C Code
arXiv:2501.10889v1 [cs.LO] 18 Jan 2025




                                             Jesper Amilon1 , Dilian Gurov1 , Christian Lidström2 , Mattias
                                                    Nyberg1,3 , Gustav Ung1,3 , and Ola Wingbrant3
                                               1
                                                   KTH Royal Institute of Technology, Stockholm, Sweden
                                                        2
                                                          Fondazione Bruno Kessler, Trento, Italy
                                                             3
                                                               Scania AB, Södertälje, Sweden

                                                                       January 22, 2025


                                                                             Abstract
                                                  Deductive verification has become a mature paradigm for the verifi-
                                              cation of industrial software. Applying deductive verification, however,
                                              requires that every function in the code base is annotated with a func-
                                              tion contract specifying its behaviour. This introduces a large overhead
                                              of manual work. To address this challenge, we introduce the AutoDeduct
                                              toolchain, built on top of the Frama-C framework. It implements a com-
                                              bination of techniques to automatically infer contracts for functions in
                                              C programs, in the syntax of ACSL, the specification language of Frama-
                                              C. Contract inference in AutoDeduct is implemented as two plugins for
                                              Frama-C, each inferring different types of annotations. We assume that
                                              programs have an entry-point function already equipped with a contract,
                                              which is used in conjunction with the program source code to infer con-
                                              tracts for the helper functions, so that the entry-point contract can be
                                              verified. The current release of AutoDeduct is the first public prototype,
                                              which we evaluate on an example adapted from industrial software.


                                         1    Introduction
                                         Over the past 6 years, we have used the Frama-C framework for the deductive
                                         verification of industrial automotive software, together with the heavy-vehicles
                                         manufacturer Scania [14, 19, 18, 12]. A key insight from our experience is that
                                         deductive verification imposes a huge manual overhead to annotate the code
                                         with specifications, and that this is a major obstacle for deductive verification
                                         to become a practically viable option for the industry. To overcome this obstacle,
                                         we have worked towards developing techniques that automatically infer ACSL
                                         specifications. In this paper, we report on the first prototype of our toolchain


                                                                                  1
AutoDeduct, which automates the deductive verification process of C programs
through a combination of inference techniques.
    When working with programs in languages such as C, each file typically
has only a few C functions serving as entry-points, but they are implemented
through numerous helper functions. To apply deductive verification, every func-
tion is expected to be annotated with a contract. Often, one also needs to add
further annotations for the verification to succeed, such as annotations speci-
fying memory safety or which memory location a function is allowed to access.
In our toolchain, we implement several techniques for property-guided contract
inference, to automatically generate specifications that otherwise must be pro-
vided manually. As we illustrate in the evaluation (Section 4), AutoDeduct is
well-suited for deductive verification of C code in embedded systems, where
requirements typically specify a module, and not individual C functions.

Related work. The weakest pre-condition calculus, pioneered by Dijkstra [8],
was an early method for automatic specification inference: given a post-condition,
the weakest pre-condition sufficient to establish the post-condition can be com-
puted through syntactic predicate transformations defined over program state-
ments. As presented by Moy [13], pre-conditions that are not necessarily the
weakest can be computed by a combination of abstract interpretation and quan-
tifier elimination. Seghir et al. presented an approach based on Counterexample-
Guided Abstraction Refinement (CEGAR) to inferring pre-conditions [15, 16].
     Applying the dual notion of strongest post-conditions [8] (or function sum-
maries) is another approach to specification inference. Strongest post-conditions
are computed from a program and a pre-condition, and characterise the fi-
nal states that result from executions from states satisfying the pre-condition.
Strongest post-conditions can be computed through symbolic execution [9] for
programs without unbounded loops. Sinleton et al. proposed an algorithm for
transforming exponentially large post-conditions resulting from strongest post-
condition computation into more concise forms [17].
     Maximal specification inference generalises weakest pre-condition inference
by considering specifications for multiple functions simultaneously. Albargh-
outhi et al. present a counter-example guided approach, which is based on
multi-abduction [1].

Contribution. This paper presents the first public prototype release of the
AutoDeduct toolchain (Section 3), using a novel combination of techniques to
automatically infer contracts for helper functions in the context of an entry-
point contract, and off-the-shelf technology for verification of C programs. It
is built on top of the Frama-C [10, 7] framework, and infers function contracts
for usage in deductive verification in Frama-C. The contract inference in the
toolchain consists of two separate Frama-C plugins, performing complementary
forms of contract inference. The paper also presents an initial evaluation on a
C program adapted from industrial software (Section 4).



                                       2
 1   int r e a d _ i n p u t() {                   12   /* @ r e q u i r e s in >= 0;
 2     return in ;                                 13          ensures
 3   }                                             14              in <= 10 == > out == in * in
 4   void w r i t e _ o u t p u t( int x ) {       15              && in > 10 == > out == 100;
 5     out = x ;                                   16   */
 6   }                                             17   void main () {
 7                                                 18      int tmp = r e a d _ i n p u t() ;
 8   int saturate ( int x , int lim ) {            19      tmp = saturate ( tmp , 10) ;
 9     if ( x > lim ) return lim ;                 20      tmp = tmp * tmp ;
10     else return x ;                             21      w r i t e _ o u t p u t( tmp ) ;
11   }                                             22   }

Figure 1: Example program with a main function and three helper functions,
where only the main function is given a contract.


2      Background
Frama-C [7] is an open-source modular platform for static analysis of C programs.
It features plugins such as WP [5], used for deductive verification based on the
weakest pre-condition calculus, and Eva [6], used for showing absence of runtime
errors by abstract interpretation. Frama-C also allows users to write new plug-
ins to extend its capabilities.
    The specifications to be verified deductively with Frama-C are provided to
the program as annotations written in the ANSI C Specification Language
(ACSL) [4]. In particular, ACSL offers function contracts, which are used to
specify the functional behaviour of a given C function. An example of an ACSL
function contract can be seen in Figure 1. The contract is primarily expressed
through the requires and ensures clauses. The former clause asserts that a
condition must hold directly before the function call, and has to be shown to
hold at each call site. The latter clause asserts that a condition must hold di-
rectly upon return. Variables occurring in this clause can refer either to their
value in the post-state of the function, or in the pre-state if used with the \old
predicate. In addition to these conditions, a frame condition may also be added,
specifying which memory locations may be modified by the function, and is ex-
pressed through the assigns keyword.


3      The AutoDeduct Toolchain
AutoDeduct is a toolchain for automated deductive verification of C programs.
The intended use case is a C module, for the entry-point function of which
an ACSL contract has been provided. AutoDeduct will infer contracts for the
helper functions, and then verify the program using WP. The verification with
WP ensures that the entry-point function satisfies the provided contract, and
that every helper function satisfies its inferred contract. Thus, the necessary
trust base for the verification engineer does not extend beyond the mature WP
plugin of Frama-C. Aside from verifying the program, the toolchain produces as
an artefact a fully annotated program. In the domain of contract inference tools,
we consider AutoDeduct as a toolchain for property-guided contract inference,


                                               3
                   AutoDeduct
    C module                     Tricera
                                                                               Verification
                    Frama-C                                   Annotated         succeeded
                                Functional       Auxilliary     C file
                                 contract         contract                WP
                                 inference       inference
      ACSL                                                                     Verification
   specification                                                                  failed
                                                    Eva


                        Contract inference                Verification


                       Figure 2: Architecture of AutoDeduct


meaning that it infers contracts that are strong enough for verifying the current
program, but they may not generalise to other contexts.
    We classify annotations within ACSL contracts as either functional or aux-
iliary [11]. The functional annotations directly concern the behaviour of the
function, typically by relating input values to output values of program vari-
ables. Auxiliary annotations are those that do not directly specify the functional
behaviour, but may be needed for the verification to succeed, e.g., to specify
memory safety. Previously, we have worked on these inference paradigms sepa-
rately, but with the AutoDeduct tool, we bring them together under one roof.
    AutoDeduct is implemented in the form of two separate Frama-C plugins,
one for functional annotations and the other one for auxiliary annotations. The
architecture of the AutoDeduct toolchain is shown in Figure 2. AutoDeduct is
available as a Docker image on its Github page1 , or in the accompanying artifact.
    We shall use Figure 1 as a running example to explain the auxiliary and
functional inference components of AutoDeduct, and illustrate its usage. The
example is a C program that structurally resembles code from the embedded
systems domain. The entry-point of the program reads the input, performs
some calculations, and writes the output. Specifically, it sets the output to
the maximum value of 100 and the square of the input. The main function
uses three helper functions, read_input, saturate, and write_output. The
ACSL contract for the main function specifies the intended behaviour of the
program. By running AutoDeduct on the program, we infer contracts for the
helper functions, and verify the program using WP. The inferred contracts for
saturate and read_input are shown in Figure 3. Note that we have formatted
the contracts for readability.

Functional contract inference. The functional contract inference compo-
nent of AutoDeduct is a Frama-C plugin [3] (previously referred to as the Saida
plugin), which assumes that the entry-point is annotated with an ACSL con-
tract. It then uses as backend the Horn-clause based model checker TriCera for
inference of functional aspects of the helper functions contracts. TriCera encodes
  1 https://github.com/rse-verification/auto-deduct-toolchain




                                             4
1    /* @ r e q u i r e s 0 <= x <= 2 1 4 7 4 8 3 6 4 7 ; // A u x i l i a r y
2         r e q u i r e s lim == 10 && x == in ; // F u n c t i o n a l
3         e n s u r e s // F u n c t i o n a l
4             0 <= \ result <= 10 && out == \ old ( out ) &&
5             in == \ old ( in ) && \ old ( lim ) == 10 && \ old ( x ) == \ old ( in ) &&
6             (\ result == \ old ( in ) == > (10 >= \ old ( in ) >= 0) ) &&
7             (\ result == 10 == > \ old ( in ) >= 10) &&
8             (\ result == \ old ( in ) || \ result == 10) ;
9         a s s i g n s \ nothing ; */ // A u x i l i a r y
10   int saturate ( int x , int lim ) ;
11
12   /* @ r e q u i r e s 0 <= x <= 100 && \ valid (& out ) ; // A u x i l i a r y
13         r e q u i r e s // F u n c t i o n a l
14             ( in * in == x && 0 <= in <= 10) || (10 * 10 == x && in >= 11) ;
15         e n s u r e s 0 <= out <= 100; // A u x i l i a r y
16         e n s u r e s // F u n c t i o n a l
17      (( in * in == \ old ( x ) && 0 <= in <= 10) || (10 * 10 == \ old ( x ) && in >= 11) )
18                 && in == \ old ( in ) && \ old ( x ) == out ;
19         a s s i g n s out ; */ // A u x i l i a r y
20   void w r i t e _ o u t p u t( int x ) ;

       Figure 3: Inferred contracts for the program write_output and saturate


     the program as a set of Horn clauses, where each called function is associated
     with a pair of predicates representing the pre-condition and post-condition. An
     interpretation for these predicates represents sufficient conditions for the pro-
     gram to be correct. Based on this solution, contracts for the helper functions
     can be extracted. For further technical details on the interplay between TriCera
     and AutoDeduct, we refer to our earlier work [2, 3].
         After running the functional inference component, we obtain a contract for
     every helper function. For example, for the saturate function, the key parts of
     the functional aspect of the contract are the two conjuncts on lines 6 and 7. The
     contract also illustrates that inferred contracts can be highly context-specific;
     for example, the contract for saturate requires lim == 10, as this is the value
     of this parameter at the only function call.

     Auxiliary contract inference. The auxiliary contract inference component
     of AutoDeduct is implemented as another Frama-C plugin [18, 12] (referred to
     as the ISP plugin in previous work). For the inferred contracts in Figure 3,
     the auxiliary aspects include specifying ranges for variable values, the validity
     of pointers, and memory locations that are assigned to. All these annotations
     are derived from an abstract interpretation of the program, using the Frama-
     C plugin Eva as the backend. The specification for pointer validity ensures
     that all pointers used in the program are valid, as shown in the contract for
     write_output. The assigns clauses stem from the analysis by Eva; for example,
     the contract for write_output now specifies that only the variable out may be
     assigned to.

     Running the toolchain. The AutoDeduct toolchain is intended to be used
     mainly as a command-line tool. It assumes as input a C program, where the
     entry-point function is equipped with an ACSL contract, and can be run by


                                                      5
invoking a script: ./autodeduct filename.c. The user may also run each
step separately as follows. The functional contract inference component is run
by ./autodeduct -func filename.c, which runs the functional inference and
outputs the file tmp_inferred_source_merged.c. Next, the auxiliary contract
inference is invoked with ./autodeduct -aux tmp_inferred_source_merged.c,
which outputs the now fully annotated file annotated.c. The fully annotated
program can be verified with WP using ./autodeduct -wp annotated.c.

Limitations. While we support a relatively large subset of C and ACSL, there
are currently some limitations in the toolchain. In general, the auxiliary infer-
ence component supports a larger subset than the functional inference compo-
nent. Notable features not supported for functional inference are floating-point
arithmetic and stack pointers. C features supported by neither functional nor
auxiliary inference include pointer arithmetic, nested pointers, and local static
variables. AutoDeduct also does not support the general use of logic functions
in ACSL contracts. While the toolchain supports programs with loops, we have
yet to implement the automated inference of loop invariants.


4    Evaluation
We evaluate AutoDeduct on a case study consisting of a C module of ca. 1400
LOC, taken from the automotive industry. We have previously verified the
module using Frama-C [14] by manually annotating it, in an effort that took 2
person-months. We have also shown previously that the auxiliary annotation
component of AutoDeduct can infer almost all of the needed auxiliary annota-
tions [12].
    Due to the current limitations in the toolchain, we consider a simplified
version (which can be found in the accompanying artifact) of the module and
5 of its requirements. In the simplified module, which consists of 123 LOC, we
have removed the parts not relevant for the specified requirements and, e.g.,
rewritten certain pointer constructs. It has an entry-point function annotated
with a function contract, and 5 helper functions without contracts. The contract
specifies 5 requirements on the module, formulated by engineers at Scania, each
one represented by a separate ensures clause in the contract, and an assigns
clause that specifies the variables that the module may write to.
    When applying AutoDeduct on the simplified module, the verification suc-
ceeds in roughly 23 s, of which 18 s are spent on functional inference, 2 s on
auxiliary, and 3 s on verification with WP. Moreover, the toolchain produces as
output a fully annotated version of the module, with inferred contracts for all
the helper functions. The inferred contracts contain the necessary requires,
ensures, and assigns clauses. We did not compare AutoDeduct against other
tools, since we are not aware of any existing toolchain for deductive verification
that can automatically verify such C programs using contract inference.




                                        6
5    Conclusion
We have presented the AutoDeduct toolchain for automated deductive verifica-
tion of C code, based on Frama-C and a combination of techniques for contract
inference. We believe our toolchain to be the first one to offer such a high
degree of automation. The case study illustrates our vision and shows that
AutoDeduct can automatically verify industrial C code specified with industrial
requirements. Future work will foremost focus on covering all features of C
and ACSL needed to automatically verify the full version of the module used
here and other modules taken from the automotive industry. We also plan to
enhance the user feedback in the case of failed verification results.



References
 [1] Albarghouthi, A., Dillig, I., Gurfinkel, A.: Maximal specification syn-
     thesis. In: Proceedings of the 43rd Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, POPL 2016, St.
     Petersburg, FL, USA, January 20 - 22, 2016. pp. 789–801 (2016).
     https://doi.org/10.1145/2837614.2837628
 [2] Alshnakat, A., Gurov, D., Lidström, C., Rümmer, P.: Constraint-Based
     Contract Inference for Deductive Verification, pp. 149–176. Springer In-
     ternational Publishing, Cham (2020). https://doi.org/10.1007/978-3-030-
     64354-6_6
 [3] Amilon, J., Esen, Z., Gurov, D., Lidström, C., Rümmer, P.: An
     Exercise in Mind Reading: Automatic Contract Inference for Frama-
     C, pp. 553–582. Springer International Publishing, Cham (2024).
     https://doi.org/https://doi.org/10.1007/978-3-031-55608-1_13
 [4] Baudin, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y.,
     Prevosto, V.: ACSL: ANSI/ISO C Specification Language (2024),
     http://frama-c.com/download/acsl.pdf
 [5] Baudin, P., Bobot, F., Correnson, L., Dargaye, Z., Blan-
     chard,   A.:    WP     Plug-in  Manual.  CEA    LIST (2024),
     https://frama-c.com/download/frama-c-wp-manual.pdf
 [6] Bühler,  D.,   Cuoq,   P.,  Yakobowski,   B.:    Eva              -      The
     Evolved   Value    Analysis  plug-in.   CEA    LIST                   (2024),
     http://frama-c.com/download/frama-c-eva-manual.pdf
 [7] Correnson, L., Cuoq, P., Kirchner, F., Maroneze, A., Prevosto, V., Puc-
     cetti, A., Signoles, J., Yakobowski, B.: Frama-C User Manual. CEA LIST,
     Inria, http://frama-c.com/download/frama-c-user-manual.pdf



                                      7
 [8] Dijkstra, E.W.: Guarded commands, nondeterminacy and formal
     derivation of programs. Commun. ACM 18(8), 453–457 (Aug 1975).
     https://doi.org/10.1145/360933.360975
 [9] Gordon, M., Collavizza, H.: Forward with Hoare. In: Reflections
     on the Work of C. A. R. Hoare., pp. 101–121. Springer (2010).
     https://doi.org/10.1007/978-1-84882-912-1_5
[10] Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.:
     Frama-C: A Software Analysis Perspective. Formal Aspects of Computing
     (2015). https://doi.org/10.1007/978-3-642-33826-7_16
[11] Lidström, C.: Automated Deductive Verification of Safety-Critical Em-
     bedded Software. Ph.D. thesis, KTH, Theoretical Computer Science, TCS
     (2024), qC 20240223
[12] Manjikian, H.: Improving the Synthesis of Annotations for Partially Au-
     tomated Deductive Verification. Master’s thesis, KTH Royal Institute of
     Technology (2021)

[13] Moy, Y.: Sufficient preconditions for modular assertion checking. In: Ver-
     ification, Model Checking, and Abstract Interpretation, 9th International
     Conference, VMCAI 2008, San Francisco, USA, January 7-9, 2008, Pro-
     ceedings. pp. 188–202 (2008). https://doi.org/10.1007/978-3-540-78163-
     9_18
[14] Nyberg, M., Gurov, D., Lidström, C., Rasmusson, A., Westman, J.: Formal
     verification in automotive industry: Enablers and obstacles. In: Lever-
     aging Applications of Formal Methods, Verification and Validation. In-
     dustrial Practice: 8th International Symposium, ISoLA 2018, Proceed-
     ings, Part IV. p. 139–158. Springer-Verlag, Berlin, Heidelberg (2018).
     https://doi.org/10.1007/978-3-030-03427-6_14
[15] Seghir, M.N., Kroening, D.: Counterexample-guided precondition in-
     ference. In: Programming Languages and Systems - 22nd European
     Symposium on Programming, ESOP 2013, Held as Part of the Euro-
     pean Joint Conferences on Theory and Practice of Software, ETAPS
     2013, Rome, Italy, March 16-24, 2013. Proceedings. pp. 451–471 (2013).
     https://doi.org/10.1007/978-3-642-37036-6_25
[16] Seghir, M.N., Schrammel, P.: Necessary and sufficient preconditions via
     eager abstraction. In: Programming Languages and Systems - 12th Asian
     Symposium, APLAS 2014, Singapore, November 17-19, 2014, Proceedings.
     pp. 236–254 (2014). https://doi.org/10.1007/978-3-319-12736-1_13
[17] Singleton, J.L., Leavens, G.T., Rajan, H., Cok, D.R.:      Infer-
     ring concise specifications of APIs. CoRR abs/1905.06847 (2019),
     http://arxiv.org/abs/1905.06847



                                      8
[18] Skantz, D.: Synthesis of Annotations for Partially Automated Deductive
     Verification. Master’s thesis, KTH Royal Institute of Technology (2021)
[19] Ung, G., Amilon, J., Gurov, D., Lidström, C., Nyberg, M., Palm-
     skog, K.: Post-hoc formal verification of automotive software with in-
     formal requirements: An experience report. In: 2024 IEEE 32nd Inter-
     national Requirements Engineering Conference (RE). pp. 287–298 (2024).
     https://doi.org/10.1109/RE59067.2024.00035




                                     9
