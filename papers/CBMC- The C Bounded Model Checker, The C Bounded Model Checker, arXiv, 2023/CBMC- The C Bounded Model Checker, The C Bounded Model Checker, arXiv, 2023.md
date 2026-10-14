                                        CBMC
                                        The C Bounded Model Checker

                                        Daniel Kroening, Peter Schrammel and Michael Tautschnig
arXiv:2302.02384v1 [cs.SE] 5 Feb 2023




                                        1 Introduction

                                        The C Bounded Model Checker (CBMC) [9] demonstrates the violation of assertions
                                        in C programs, or proves safety of the assertions under a given bound. CBMC
                                        implements a bit-precise translation of an input C program, annotated with assertions
                                        and with loops unrolled to a given depth, into a formula. If the formula is satisfiable,
                                        then an execution leading to a violated assertion exists.
                                           CBMC is one of the most successful software verification tools. Its main advan-
                                        tages are its precision, robustness and simplicity. CBMC is shipped as part of several
                                        Linux distributions. It has been used by thousands of software developers to ver-
                                        ify real-world software, such as the Linux kernel, and powers commercial software
                                        analysis and test generation tools. Table 1 gives an overview of CBMC’s features.
                                           CBMC is also a versatile tool that can be applied to solve many practical program
                                        analysis problems such as bug finding, property checking, test input generation,
                                        detection of security vulnerabilities, equivalence checking and program synthesis.
                                           This chapter will give an introduction into CBMC, including practical examples
                                        and pointers to further reading. Moreover, we give insights about the development
                                        of CBMC itself, showing how its performance evolved over the last decade.
                                           Section 2 gives an overview of the verification approach implemented by CBMC.
                                        Section 3 gives a tutorial on how to use CBMC for various verification problems.
                                        A strength of CBMC is its proven applicability to real-world C programs; Section 4


                                        Daniel Kroening
                                        University of Oxford, United Kingdom and Diffblue Ltd, Oxford, United Kingdom e-mail:
                                        kroening@cs.ox.ac.uk
                                        Peter Schrammel
                                        University of Sussex, Brighton, United Kingdom and Diffblue Ltd, Oxford, United Kingdom e-
                                        mail: p.schrammel@sussex.ac.uk
                                        Michael Tautschnig
                                        Queen Mary University of London, United Kingdom e-mail: michael.tautschnig@qmul.ac.uk


                                                                                                                                1
2                                   Daniel Kroening, Peter Schrammel and Michael Tautschnig

explains the features that enable this. Section 5 describes the components of CBMC’s
architecture. Section 6 gives an overview of how the performance of CBMC evolved
over the last 10 years, before wrapping up in Section 7.

Languages           C, GOTO
Properties          assert, memory safety, arithmetic overflow, division-by-zero, memory leaks
Environments        Linux, Mac OS, Windows, BSD
Technologies used   symbolic execution, bounded model checking, SAT and SMT solving
Other features      compilation and linking of entire projects into GOTO via goto-cc
Strengths           memory safety, floating point arithmetic
Weaknesses          limited support for unbounded verification

                                Table 1: CBMC Features


Software Project. The CPROVER framework (including CBMC) is implemented in
C++ and has about 250 KLOC. CPROVER is maintained by Daniel Kroening with
more than 60 contributors. It is made publicly available under a BSD-style license.
The source code and binaries for popular platforms are available at https://www.
cprover.org/cbmc and https://github.com/diffblue/cbmc. There is a detailed installation
guide at https://www.cprover.org/cprover-manual/installation/.



2 Verification Approach

For a given Kripke structure, bounded model checking [6, 7] is a semi-decision pro-
cedure that translates bounded unfoldings of a transition relation and LTL formulae
to propositional satisfiability problems. Soundness is achieved by incrementing the
bound until a witness is found, but completeness can only be achieved when the
number of steps to reach all states is finite.
   CBMC implements bounded model checking for software, specifically for C
programs. In this setting, the transition relation is specified by the C program and the
semantics laid out in the C language standards [3], with the initial state determined by
the program’s entry point. As specification, the program is annotated with assertions
rather than using LTL formulae. A bounded unfolding of the transition relation
amounts to a bounded number of execution steps of the program. As a more practical
notion of bounded unfolding, however, the bounded unfolding is typically instantiated
via bounded unrolling of loops and recursive procedure calls.
   Via such a bounded unfolding CBMC reduces questions about program paths
to constraints that can be solved by off-the-shelf Boolean Satisfiability (SAT) or
Satisfiability Modulo Theories (SMT) [4] solvers. With the SAT back end, and given
a program annotated with assertions, CBMC produces a CNF formula the solutions
of which describe program paths leading to assertion violations. A model of this
formula then amounts to a counterexample.
CBMC                                                                               3

1   int abs(int x) {
2     int y = x;
3

4       if(x < 0) {
5         y = -x;
6       }
7
8       return y;
9   }

                             Listing 1: Source code (abs.c)


1  CBMC version 5.12 (cbmc-5.12-d8598f8-557-g1edf4d91f) 64-bit x86_64 macos
2  Parsing abs.c
 3 Converting

 4 Type-checking abs
 5 Generating GOTO Program

 6 Adding CPROVER library (x86_64)

 7 Removal of function pointers and virtual functions
 8 Generic Property Instrumentation

 9 Running with 8 object bits, 56 offset bits (default)

10 Starting Bounded Model Checking
11 size of program expression: 45 steps

12 simple slicing removed 0 assignments

13 Generated 0 VCC(s), 0 remaining after simplification
14 VERIFICATION SUCCESSFUL


               Listing 2: CBMC output of command C1 for abs.c (Listing 1)



   Before looking at the architecture in detail, let us consider an example. The
program in Listing 1 shall be an attempt to compute the absolute value of an integer-
typed input. To run CBMC on this program, we need to specify the name of the
source file (abs.c) and the entry point abs:
        cbmc --function abs abs.c                                                 C1
with the output shown in Listing 2. This output provides the following information:
• Line 1 reports the version of CBMC being run (including the exact Git revision
  the CBMC executable was built from) and the platform it is running on.
• Lines 2–5 report the source code being processed by the C front end of CBMC.
• Lines 6–8 are status updates of the instrumentation steps.
• Line 9 confirms the (configurable) pointer encoding being used.
• Lines 10–13 are status and statistics of symbolic execution. Notably, the input
  here caused zero verification conditions (VCCs) to be generated.
• Line 14 is CBMC’s conclusive answer that no specification was violated. With
  the information in the preceding line (zero VCCs), however, this is vacuous: there
4                                      Daniel Kroening, Peter Schrammel and Michael Tautschnig

10 Starting Bounded Model Checking
11 size of program expression: 46 steps
12 simple slicing removed 7 assignments

13 Generated 1 VCC(s), 1 remaining after simplification
14 Passing problem to propositional reduction

15 converting SSA

16 Running propositional reduction
17 Post-processing

18 Solving with MiniSAT 2.2.1 with simplifier

19 221 variables, 203 clauses
20 SAT checker: instance is SATISFIABLE

21 Runtime decision procedure: 0.00414769s
22

23 ** Results:
24 abs.c function abs
25 [abs.overflow.1] line 5 arithmetic overflow on signed unary minus in -x: FAILURE

26

27   ** 1 of 1 failed (2 iterations)
28   VERIFICATION FAILED

              Listing 3: CBMC output of command C2 for abs.c (Listing 1)



      were no assertions for CBMC to check. Indeed, the source code did not contain
      any assert statements.
We could now either insert assert statements, or make use of CBMC’s built-in
specifications. In this case, arithmetic overflow is of particular interest. Let us invoke
CBMC again, with signed-integer overflow assertions enabled:
      cbmc --function abs --signed-overflow-check abs.c                                   C2
We now obtain the output shown in Listing 3 (with the initial lines skipped): Not
only is the final verdict different (“VERIFICATION FAILED”), we also see further
differences:
• Line 11 now reports one additional step, and line 13 confirms that a verification
  condition is now generated, i.e., we have a non-empty specification.
• An actual formula is being generated (lines 14–17). This formula is passed to and
  processed by a SAT solver (lines 18–20), which determines it to be satisfiable. As
  reported in line 21, the SAT solver spent approximately 4 ms to compute a model.
• The satisfiable formula amounts to a violated assertion, which is reported in
  lines 23–27. Specifically, an arithmetic overflow was detected (line 25).
• The overall verdict is summarised in the last line of output.
The Boolean verification result and the one-line summary of the violated specifica-
tion typically are not sufficient for a software engineer to debug the problem reported
by CBMC. As a model checker, CBMC internally computes a full counterexample.
CBMC                                                                                   5

23 ** Results:
24 abs.c function abs
25 [abs.overflow.1] line 8 arithmetic overflow on signed unary minus in -x: FAILURE

26
27   Trace for abs.overflow.1:
28

29 State 17 file abs.c line 1 thread 0
30 ----------------------------------------------------
31   INPUT x: -2147483648 (10000000 00000000 00000000 00000000)
32
33 State 20 file abs.c line 1 thread 0
34 ----------------------------------------------------
35   x=-2147483648 (10000000 00000000 00000000 00000000)
36

37 State 21 file abs.c line 2 function abs thread 0
38 ----------------------------------------------------
39   y=0 (00000000 00000000 00000000 00000000)
40
41 State 22 file abs.c line 2 function abs thread 0
42 ----------------------------------------------------
43   y=-2147483648 (10000000 00000000 00000000 00000000)
44

45 Violated property:
46   file abs.c line 5 function abs
47   arithmetic overflow on signed unary minus in -x
48   !(x == -2147483648)
49

50   ** 1 of 1 failed (2 iterations)
51   VERIFICATION FAILED

              Listing 4: CBMC output of command C3 for abs.c (Listing 1)



In case of programs, a counterexample amounts to an execution trace. CBMC will
print the steps leading to a failing assertion with the --trace command-line option:
      cbmc --function abs --signed-overflow-check --trace abs.c                       C3
We now obtain the output shown in Listing 4 (again, initial lines are skipped).
   CBMC now prints the input value (line 31) that will trigger an arithmetic overflow.
The value is printed both in decimal notation and in binary notation, grouped as 8-bit
bytes. In this case the binary value is particularly insightful: this is the maximum
negative number representable when using two’s complement over 32 bits. The
arithmetic overflow then occurs in line 5 of abs.c as reported in lines 45–48 of
CBMC’s counterexample output.
   CBMC implements the above steps following the pipeline outlined in Figure 2 of
Section 5. In that section, we will break down each of CBMC’s components in detail
to understand how CBMC arrives at its results.
6                                 Daniel Kroening, Peter Schrammel and Michael Tautschnig

3 Using CBMC

CBMC uses assertions to specify program properties. Assertions are specifications
over the state of the program when the program reaches a particular program location.
Assertions are often written by the programmer using the assert macro.
    In addition to the assertions written by the programmer, assertions for specific
properties can also be generated automatically by CBMC, often relieving the pro-
grammer from expressing properties that should hold in any well-behaved program.
This assertion generator performs a conservative static analysis to determine program
locations that potentially contain a bug. Due to the imprecision of the static analysis,
it is important to emphasise that these generated assertions are only potential bugs,
and that the model checker first needs to confirm that they are indeed genuine bugs.
    The assertion generator supports the subsequent verification of the following
properties:
• Buffer overflows. For each array access, check whether the upper and lower bounds
  are violated.
• Pointer safety. Search for NULL-pointer dereferences or dereferences of other invalid
  pointers.
• Memory leaks. Check whether the program constructs dynamically allocated data
  structures that are subsequently inaccessible.
• Division by zero. Check whether there is a division by zero in the program.
• Not-a-Number. Check whether floating-point computation may result in NaNs.
• Arithmetic overflow. Check whether a numerical overflow occurs during an arith-
  metic operation or type conversion.
• Undefined shifts. Check for shifts with excessive distance.
All the properties described above are reachability properties. They are always of
the form "Is there a path through the program such that some property is violated?"
The counterexamples to such properties are always program paths. Stepping through
these counterexamples is similar to debugging programs.



3.1 Handling Loops

As CBMC performs Bounded Model Checking, all loops have to have a finite upper
run-time bound in order to guarantee that all bugs are found. CBMC can optionally
check that sufficient unwinding is performed.
   As an example, consider the program binsearch.c in Listing 5. If you run
CBMC on this function, you will notice that the unwinding does not stop on its own.
The built-in simplifier is not able to determine a runtime bound for this loop. The
unwinding bound has to be given as a command line argument:
    cbmc binsearch.c --function binsearch --unwind 6 --bounds-check
         --unwinding-assertions
                                                                                     C4
CBMC                                                                             7

 1 int binsearch(int x)
 2 {
 3   int a[16];
 4   signed low = 0, high = 16;
 5

 6       while(low < high)
 7       {
 8         signed middle = low + ((high - low) >> 1);
 9

10           if(a[middle] < x)
11             high = middle;
12           else if(a[middle] > x)
13             low = middle + 1;
14           else // a[middle]==x
15             return middle;
16       }
17

18       return -1;
19   }

                               Listing 5: Source code (binsearch.c)


 1 ** Results:
 2 binsearch.c function binsearch
 3 [binsearch.unwind.0] line 6 unwinding assertion loop 0: SUCCESS
 4 [binsearch.array_bounds.1] line 10

 5   array ‘a’ lower bound in a[(signed long int)middle]: SUCCESS
 6 [binsearch.array_bounds.2] line 10

 7   array ‘a’ upper bound in a[(signed long int)middle]: SUCCESS
 8 [binsearch.array_bounds.3] line 12
 9   array ‘a’ lower bound in a[(signed long int)middle]: SUCCESS
10 [binsearch.array_bounds.4] line 12

11   array ‘a’ upper bound in a[(signed long int)middle]: SUCCESS
12 ...

13 VERIFICATION SUCCESSFUL


              Listing 6: CBMC output of command C4 for binsearch.c (Listing 5)



The resulting output is shown in Listing 6. CBMC verifies that the array ac-
cesses are within the bounds; note that this actually depends on the result of the
right shift in Line 8 of the program. In addition, as CBMC is given the option
--unwinding-assertions, it also checks that sufficient unwinding is done, i.e., it
proves a runtime bound.
    For any lower unwinding bound, there are traces that demonstrate that more loop
iterations are possible. Thus, CBMC will report that the unwinding assertion has
failed. As usual, a counterexample trace that documents this can be obtained with
the option --trace.
8                                   Daniel Kroening, Peter Schrammel and Michael Tautschnig

 1 _Bool nondet_bool();                       22 int main()
 2 unsigned int nondet_unsigned_int();        23 {
 3 _Bool LOCK = 0;                            24   unsigned got_lock = 0;
 4                                            25   unsigned times = nondet_unsigned_int();
 5 _Bool lock()                               26
 6 {                                          27       while(times > 0)
 7   if(nondet_bool())                        28       {
 8   {                                        29         if(lock())
 9     assert(!LOCK);                         30         {
10     LOCK = 1;                              31           got_lock++;
11     return 1;                              32           /* critical section */
12   }                                        33         }
13                                            34
14       return 0;                            35           if(got_lock != 0)
15   }                                        36             unlock();
16                                            37
17 void unlock()                              38           got_lock--;
18 {                                          39           times--;
19   assert(LOCK);                            40       }
20   LOCK = 0;                                41   }
21 }


                            Listing 7: Source code (lock.c)


    CBMC can also be used for programs with unbounded loops. In this case, CBMC
is used for bug hunting only; CBMC does not attempt to find all bugs. The program
lock.c in Listing 7 is an example of a program with a user-specified property. The
while loop in the main function has no (useful) runtime bound. Thus, a bound has
to be set on the amount of unwinding that CBMC performs. There are two ways to
do so:
1. The --unwind command-line parameter can to be used to limit the number of
   times loops are unwound.
2. The --depth command-line parameter can be used to limit the number of pro-
   gram steps to be processed.
For the example of Listing 7, with a loop unwinding bound of one, no bug is
found. But for a bound of two, CBMC detects a trace that violates an assertion.
Without unwinding assertions, or when using the --depth command-line switch,
CBMC does not necessarily prove the program correct, but it can be helpful to find
program bugs. More information on limiting unwinding of loops can be found at
https://www.cprover.org/cprover-manual/cbmc/unwinding/.



3.2 Using Built-in Checks

   The issue of buffer overflows has obtained wide public attention. A buffer is a
contiguously allocated chunk of memory, represented by an array or a pointer in
CBMC                                                                                9

 1   #include <stdio.h>
 2

 3 int main (int argc, char** argv)
 4 {
 5   char password[8] = {’s’,’e’,’c’,’r’,’e’,’t’,’!’,’\0’};
 6   char buffer[16] = {’\0’, };
 7   int tmp;
 8   int index = 0;
 9

10       printf("Enter your name: ");
11       while ((tmp = getchar()) != ’\n’)
12       {
13         buffer[index] = tmp;
14         ++index;
15       }
16

17       printf("%s\n",buffer);
18
19       return 0;
20   }

                                  Listing 8: Source code (login.c)



C. Programs written in C do not provide automatic bounds checking on the buffer,
which means a program can – accidentally or deliberately – write beyond a buffer.
The example program in Listing 8 is a syntactically valid C program, compiling and
executing (seemingly) without any errors. If compiled on a system with the stack
growing downwards, such as x86, the following can be observed:
 1 > gcc login.c -o login
 2 > ./login
 3 Enter your name: Daniel
 4 Daniel

 5 > ./login
 6 Enter your name: Sim Sala Bim ...

 7 Sim Sala Bim ...secret!


   What has happened? The end of a character string in C is determined by a ’\0’
character. When we enter more than 15 characters then buffer will not have any ’\0’
character at the end and printf will continue printing characters beyond the memory
allocated for buffer until it encounters a ’\0’ character or crashes due to a memory
access violation (segmentation fault). Depending on the memory layout this might
lead to disclosure of confidential data. In our case above, the password is printed to
the terminal.
   Could we have found this problem with the help of CBMC? Yes, CBMC is able
to check whether memory accesses beyond the bounds of an allocated object are
possible. When we run
         cbmc login.c --unwind 20 --bounds-check                                  C5
10                                  Daniel Kroening, Peter Schrammel and Michael Tautschnig

CBMC reports
1 ** Results:
2 login.c function main
3 [main.array_bounds.2] line 13

4   array ‘buffer’ upper bound in buffer[(signed long int)index]:
5   FAILURE
6 [main.array_bounds.1] line 13

7   array ‘buffer’ lower bound in buffer[(signed long int)index]:
8   SUCCESS

This means that the program is indeed faulty. Inspecting the trace (--trace) as
shown in Listing 9 confirms that the problem occurs when we assign to buffer after
index has been incremented to 16.



1 ...
2 State 251 file login.c function main line 13 thread 0
3 ----------------------------------------------------

4   buffer[15l]=-1 (11111111)
5
6  State 252 file login.c function main line 14 thread 0
7  ----------------------------------------------------
 8   index=16 (00000000 00000000 00000000 00010000)
 9 ...

10 State 259 file <builtin-library-getchar> function getchar line 15 thread 0
11 ----------------------------------------------------

12   INPUT getchar: -1 (11111111 11111111 11111111 11111111)
13 ...
14 Violated property:

15   file login.c function main line 13 thread 0
16   array ‘buffer’ upper bound in buffer[(signed long int)index]
17   !((signed long int)index >= 16l)

    Listing 9: CBMC output for command C5 with --trace for login.c (Listing 8)



   If we enter further characters we would write beyond buffer and thus overwrite
data on the stack. In particular, such bugs can be exploited to overwrite the return
address of a function, thus enabling the execution of arbitrary code.
   CBMC is capable of detecting such bugs by checking these lower and upper
bounds, even for arrays with dynamic size: The two options --bounds-check and
--pointer-check instruct CBMC to look for errors related to pointers and array
bounds. When invoked with --show-properties, CBMC will print the list of
properties it checks:
      cbmc login.c --show-properties --bounds-check --pointer-check                    C6
Note that it lists, among others, a property labelled with “array ‘buffer’ upper bound”
together with the location of the faulty array access:
1   Property main.array_bounds.1:
CBMC                                                                                 11

2   file login.c line 13 function main
3   array ‘buffer’ lower bound in buffer[(signed long int)index]
4   (signed long int)index >= 0l
5

6 Property main.array_bounds.2:
7   file login.c line 13 function main
8   array ‘buffer’ upper bound in buffer[(signed long int)index]
9   !((signed long int)index >= 16l)

    As you can see, CBMC largely determines the property it needs to check itself.
This is realised by means of a preliminary static analysis, which relies on computing
a fixed point on various abstract domains. These automatically generated properties
need not necessarily correspond to bugs – these are just potential flaws for abstract
interpretation might be imprecise. Whether these properties hold or correspond to
actual bugs needs to be determined by further analysis.
    CBMC performs this analysis using symbolic simulation, which is facilitated by
a translation of the program into a formula. The formula is then combined with the
property. Let’s look at the formula that is generated by CBMC’s symbolic simulation:
    cbmc login.c --unwind 20 --show-vcc --bounds-check --pointer-check              C7
With this option, CBMC performs the symbolic simulation and prints the verification
conditions as a conjunction of equations. A verification condition needs to be proven
to be valid by a decision procedure in order to assert that the corresponding property
holds. Let’s run the decision procedure:
    cbmc login.c --unwind 20 --bounds-check --pointer-check                         C8
   CBMC transforms the equation (that can be printed using --show-vcc) into
CNF and passes this formula to a SAT solver (cf. [15] for background on such
transformations). It then determines which of the properties that it has generated for
the program hold and which do not. Using the SAT solver, CBMC detects that the
property for the object bounds of buffer does not hold, and will display:
1 [main.array_bounds.2] line 13
2   array ‘buffer’ upper bound in buffer[(signed long int)index]:
3   FAILURE

   To aid the understanding of the problem, CBMC can generate a counterexample
trace for failed properties. To obtain this trace of Listing 9, run:
    cbmc login.c --unwind 20 --bounds-check --pointer-check --trace                 C9
CBMC then prints a counterexample trace, that is, a program trace that begins with
main and ends in a state which violates the property. In our example, the program
trace ends in the faulty array access. It also gives the values the input variables must
have for the bug to occur. In this example, the results of (repeated calls to) getchar
must be ones to trigger the out-of-bounds array access. If one adds a branch to the
example that requires that the input is no more than 15 characters, the bug is fixed
and CBMC will report that the proofs of all properties have been successful.
12                                  Daniel Kroening, Peter Schrammel and Michael Tautschnig

3.3 Built-In Functions and Types

The CPROVER framework, which encompasses CBMC, provides built-in functions
and types in order to access internal functionality of the verifier, which can be used
to implement functionality that the source language itself does not provide.
    In addition to the assert(condition) function provided by assert.h, there is a
__CPROVER_assert(condition, "description") which allows to attach a custom description
to properties.
    The function __CPROVER_assume(condition) adds an expression as a constraint to the
program. If the expression evaluates to false on a path, the execution of this pro-
gram path aborts without failure. Assumptions are used to restrict non-deterministic
choices made by the program. As an example, suppose we wish to model a non-
deterministic choice that returns a number between 1 and 100. There is no integer
type with this range. We therefore use __CPROVER_assume to restrict the range of a
non-deterministically chosen integer:
1   unsigned int nondet_uint();
2

3 unsigned int one_to_hundred()
4 {
5   unsigned int result=nondet_uint();
6   __CPROVER_assume(result>=1 && result<=100);
7   return result;
8 }


   This function returns the desired integer from 1 to 100. The user must ensure that
the condition given as an assumption is actually satisfiable by some non-deterministic
choice, otherwise the model checking step will pass vacuously.
   Also note that assumptions are never retroactive. They only affect assertions (or
other properties) that follow them in program order. This is best illustrated with an
example. In the following variant of the above program the assumption has no effect
on the assertion, which means that the assertion will fail:
1   unsigned int nondet_uint();
2

3 unsigned int one_to_hundred()
4 {
5   unsigned int result=nondet_uint();
6   assert(result<100);
7   __CPROVER_assume(result>=1 && result<=100);
8   return result;
9 }


   Assumptions do restrict the search space, but only for assertions that follow. As
an example, this program, with the same assertion now placed (in program order)
after the assumption, will pass:
1   unsigned int nondet_uint();
2

3   unsigned int one_to_hundred()
4   {
CBMC                                                                                        13

 5       unsigned int result=nondet_uint();
 6       __CPROVER_assume(result>=1 && result<=100);
 7       assert(result<100);
 8       return result;
 9   }

  Beware that non-determinism cannot be used to obtain the effect of universal
quantification in assumptions. For example:
 1 int main()
 2 {
 3   int a[10], x, y;
 4
 5       x=nondet_int();
 6       y=nondet_int();
 7       __CPROVER_assume(x>=0 && x<10 && y>=0 && y<10);
 8

 9       __CPROVER_assume(a[x]>=0);
10
11       assert(a[y]>=0);
12   }

   The assertion in Line 11 fails as x and y need not have the same value. Line 9 only
ensures that there exists and index x such that a[x]>=0.

Built-in Types. __CPROVER_bitvector[size] is used to specify a bit vector with arbitrary
but fixed size. The usual integer type modifiers signed and unsigned can be applied.
The usual arithmetic promotions will be applied to operands of this type.
    __CPROVER_floatbv[total_size][mantissa_size] specifies an IEEE-754 floating point
number with arbitrary but fixed size. total_size is the total size (in bits) of the
number, and mantissa_size is the size (in bits) of the mantissa, or significand (not
including the hidden bit, thus for single precision this should be 23). The IEEE
floating-point arithmetic rounding mode can be set by assigning to the global vari-
able __CPROVER_rounding_mode.
    __CPROVER_fixedbv[total_size][fraction_size] specifies a fixed-point bit vector with
arbitrary but fixed size. total_size is the total size (in bits) of the type, and fraction_size
is the number of bits after the radix point.

Concurrency. Asynchronous threads are created by preceding an instruction with a la-
bel with the prefix __CPROVER_ASYNC_. Atomic sections are delimited by __CPROVER_atomic_begin()
and __CPROVER_atomic_end().
   The complete CPROVER API documentation can be found at https://www.cprover.
org/cprover-manual/api/.
14                                      Daniel Kroening, Peter Schrammel and Michael Tautschnig

 1   #include <assert.h>                          19 int main()
 2   #include <pthread.h>                         20 {
 3                                                21   pthread_t t1,t2;
 4   pthread_mutex_t mutex;                       22   pthread_mutex_init(&mutex, 0);
 5   int balance = 1000;                          23
 6                                                24       int amount1 = -3000;
 7 void* transaction(void* amount)                25       pthread_create(&t1, 0, transaction, &amount1);
 8 {                                              26       int amount2 = 9000;
 9   // pthread_mutex_lock(&mutex);               27       pthread_create(&t2, 0, transaction, &amount2);
10                                                28
11       int current = balance;                   29       pthread_join(t1, 0);
12       current += *(int *)amount;               30       pthread_join(t2, 0);
13       balance = current;                       31       assert(balance == 6000);
14                                                32

15       // pthread_mutex_unlock(&mutex);         33       pthread_mutex_destroy(&mutex);
16                                                34       return 0;
17       return 0;                                35   }
18   }

                              Listing 10: Source code (account.c)


3.4 Built-In Library

Most C programs make use of functions provided by a library. Instances are func-
tions from the standard ANSI-C library such as malloc or printf. The verification of
programs that use such functions has two requirements:
1. Appropriate header files have to be provided. These header files contain declara-
   tions of the functions that are to be used.
2. Appropriate definitions have to be provided.
   Most C compilers come with header files for the ANSI-C library functions. CBMC
ships definitions of commonly used functions, such as memory allocation or string
manipulation. These functions often over-approximate the behaviour prescribed by
the C standard to aid sound verification. An example of such library functions
provided by CBMC is (a subset of) the pthread library, which is used by the
following example.
   The bank account program in Listing 10 uses the pthread library to launch two
threads to execute transactions on a bank account. CBMC has support for the pthread
library, so we can model check this concurrent program by simply running cbmc
account.c. CBMC reports promptly:
 1 ** Results:
 2 ...
 3 account.c function main

 4 [main.assertion.1] line 29 assertion balance == 6000: FAILURE

 5 ...
 6 VERIFICATION FAILED
CBMC                                                                                  15

   This program suffers from a race condition. Race conditions may occur in multi-
threaded programs when the result of a computation depends on the interleaving of
the execution of instructions from concurrent threads. By inspecting the trace we
can even see why the race condition is happening:
1 ...
2 State 108 file account.c function transaction line 12 thread 1
3 ----------------------------------------------------

4   balance=-2000 (11111111 11111111 11111000 00110000)
5 ...

6 State 137 file account.c function transaction line 12 thread 2

7 ----------------------------------------------------
8   balance=9000 (00000000 00000000 00100011 00101000)
9 ...


Thread 1 withdraws 3000 and sets the balance to -1000, but then thread 2 overwrites
the balance with 10000 added to the initial balance, resulting in 9000 instead of the
expected 6000.
   Obviously, the program can be repaired by making the update of the balance
atomic. We can uncomment the locks in lines 9 and 13 in Listing 10 and verify with
CBMC that the program works correctly now.



3.5 Test Inputs

CBMC can be used to automatically generate test inputs that satisfy a certain code
coverage criteria. Common coverage criteria include branch coverage, condition cov-
erage and Modified Condition/Decision Coverage (MC/DC). Among others, MC/DC
is required by several avionics software development guidelines to ensure adequate
testing of safety critical software. Briefly, in order to satisfy MC/DC, for every con-
ditional statement containing Boolean decisions, each Boolean variable should be
evaluated one time to “true” and one time to “false,” in a way that affects the outcome
of the decision.
    In the following, we are going to demonstrate how to apply the test suite generation
functionality in CBMC. The program pid.c in Listing 11 is an excerpt from a real-
time embedded benchmark PapaBench [19], and implements part of a fly-by-wire
autopilot for an Unmanned Aerial Vehicle (UAV). We have adjusted it slightly for
our purposes.
    The aim of function climb_pid_run is to control the vertical climb of the UAV. It
is called from the reactive loop in the main function. The behaviour of this simple
controller, supposing that the desired speed is 0.5 meters per second, is plotted in
Figure 1.
    The main function has been augmented to model the inputs that are acquired in
each time step. The functions __CPROVER_input and __CPROVER_output are used to report an
input or output value. Note that they do not generate input or output values, just report
their values. The first argument is a string constant to distinguish multiple inputs and
16                                      Daniel Kroening, Peter Schrammel and Michael Tautschnig

28 void climb_pid_run()
29 {
30   float err=estimator_z_dot-desired_climb;
31
32       float fgaz=CLIMB_PGAIN*(err+CLIMB_IGAIN*climb_sum_err)+
33                  CLIMB_LEVEL_GAZ+CLIMB_GAZ_OF_CLIMB*desired_climb;
34
35       float pprz=fgaz*MAX_PPRZ;
36       desired_gaz=((pprz>=0 && pprz<=MAX_PPRZ) ? pprz : (pprz>MAX_PPRZ ? MAX_PPRZ : 0));
37
38       /** pitch offset for climb */
39       float pitch_of_vz=(desired_climb>0) ? desired_climb*CLIMB_PITCH_OF_VZ_PGAIN : 0;
40       desired_pitch=NAV_PITCH+pitch_of_vz;
41

42       climb_sum_err=err+climb_sum_err;
43       if (climb_sum_err>MAX_CLIMB_SUM_ERR) climb_sum_err=MAX_CLIMB_SUM_ERR;
44       if (climb_sum_err<-MAX_CLIMB_SUM_ERR) climb_sum_err=-MAX_CLIMB_SUM_ERR;
45   }
46

47 int main()
48 {
49   while(1)
50   {
51     /** Non-deterministic input values */
52     desired_climb=nondet_float();
53     estimator_z_dot=nondet_float();
54

55        /** Range of input values */
56        __CPROVER_assume(desired_climb>=-MAX_CLIMB && desired_climb<=MAX_CLIMB);
57        __CPROVER_assume(estimator_z_dot>=-MAX_CLIMB && estimator_z_dot<=MAX_CLIMB);
58

59        __CPROVER_input("desired_climb", desired_climb);
60        __CPROVER_input("estimator_z_dot", estimator_z_dot);
61

62        climb_pid_run();
63

64        __CPROVER_output("desired_gaz", desired_gaz);
65        __CPROVER_output("desired_pitch", desired_pitch);
66       }
67       return 0;
68   }

                             Listing 11: Part of source code (pid.c)



outputs (inputs are typically generated using non-determinism, as described here).
The string constant is followed by an arbitrary number of values of arbitrary types.
   Listing 12 shows a pretty-printed version of a test suite computing using the
following call to CBMC:
         cbmc pid.c --cover mcdc --unwind 6                                                   C10
CBMC                                                                               17




                           Fig. 1: Behaviour of PID controller

 1 Test suite:
 2 Test 1.
 3   (iteration 1) desired_climb=-1.000000f, estimator_z_dot=1.000000f
 4

 5 Test 2.
 6   (iteration 1) desired_climb=-1.000000f, estimator_z_dot=1.000000f
 7   (iteration 2) desired_climb=1.000000f, estimator_z_dot=-1.000000f
 8
 9 Test 3.
10   (iteration 1) desired_climb=0.000000f, estimator_z_dot=-1.000000f
11   (iteration 2) desired_climb=1.000000f, estimator_z_dot=-1.000000f
12

13 Test 4.
14   (iteration 1) desired_climb=1.000000f, estimator_z_dot=-1.000000f
15   (iteration 2) desired_climb=1.000000f, estimator_z_dot=-1.000000f
16   (iteration 3) desired_climb=1.000000f, estimator_z_dot=-1.000000f
17   (iteration 4) desired_climb=1.000000f, estimator_z_dot=-1.000000f
18   (iteration 5) desired_climb=0.000000f, estimator_z_dot=-1.000000f
19   (iteration 6) desired_climb=1.000000f, estimator_z_dot=-1.000000f
20

21 Test 5.
22   (iteration 1) desired_climb=-1.000000f, estimator_z_dot=1.000000f
23   (iteration 2) desired_climb=-1.000000f, estimator_z_dot=1.000000f
24   (iteration 3) desired_climb=-1.000000f, estimator_z_dot=1.000000f
25   (iteration 4) desired_climb=-1.000000f, estimator_z_dot=1.000000f
26   (iteration 5) desired_climb=-1.000000f, estimator_z_dot=1.000000f
27   (iteration 6) desired_climb=-1.000000f, estimator_z_dot=1.000000f

     Listing 12: Generated test suite for pid.c (Listing 11) using command C10



It shows a test suite that achieves close to 100% MC/DC coverage (obviously, the
return statement in main is not covered). The test inputs that need to be supplied for
each time step are listed for each test.
18                                Daniel Kroening, Peter Schrammel and Michael Tautschnig

   CBMC supports various other coverage criteria apart from MC/DC, such as
branch and condition coverage. Moreover, the __CPROVER_cover(condition); statement
can be used to define a custom coverage criterion.



4 Verifying Real-World Software

Existing software projects usually do not come in a single source file that may simply
be passed to a model checker. Rather, they come in a multitude of source files in
different directories and refer to external libraries and system-wide options. A build
system then collects the configuration options from the system and compiles the
software according to build rules.
    Running software verification tools on projects like these is greatly simplified by a
compiler that first collects all the necessary models into a single model file. goto-cc
is such a model file extractor. It uses the compiler’s (e.g., GCC’s) preprocessor to
turn text into actual C code. The result of preprocessing is passed on to the internal
C parser (built and evolved as part of the CBMC tools for more than ten years).
This parser supports several C dialects, including GCC’s extensions, Visual Studio,
CodeWarrior, and ARM-CC. Alongside the C dialect goto-cc also has to (and does)
interpret any relevant command line options of all these tools as they may affect the
semantics of the program. goto-cc builds an intermediate representation, called
“goto programs” – a control-flow graph like representation – rather than executable
binaries.
    Build systems at times first produce executables to use as part of the build process,
or invoke linkers that inspect object files. goto-cc can also build hybrid binaries that
contain both executable code as well as models for verification. To enable this mode,
create a link to the goto-cc binary by the name of goto-gcc. In this mode, first
the original compiler or linker is invoked. This produces an object file or executable,
in ELF format (e.g., containing x86/64 bit instructions). Next, goto-cc is invoked
as either compiler or linker, using the same command line options as those that
were passed to the original compiler or linker. When compiling, this step, as noted
above, produces an intermediate representation of the compilation unit. To cope with
arbitrary build systems, the resulting intermediate representation is added as new
section to the ELF object file or executable. When using goto-cc for linking it thus
reads the extra section from the various input files, performs linking, and then adds
the result of linking onto the output file produced by the original linker. goto-cc
also supports an equivalent approach for OS X, which uses a different object-file
format. There, so-called fat binaries are built to simulate the described behaviour.
Extensions to support linker scripts in this process are discussed in [12].
    Note that adding the intermediate representation onto the original object file is
a key step. The result guarantees that the file remains executable or usable by the
original linker; operations such as renaming or building archives will always be
applied to both the result of unmodified compilation as well as the intermediate
representation, without any extra work being required. This enables running CBMC
CBMC                                                                                                19

on various packages of a Linux distribution [16, 17, 11]. Alternatively, all such steps
would need to be traced, e.g., by replacing system libraries, as is done in ECLAIR1.
   Some software projects come with their own libraries. Also, the goal may be to
analyse a library by itself. For this purpose it is possible to use goto-cc to link
multiple model files into a library of model files. An object file can then be linked
against this model library. For this purpose, goto-cc also features a linker mode.
   To enable this linker mode, create a link to the goto-cc binary by the name
of goto-ld (Linux and Mac) or copy the goto-cc binary to goto-link.exe
(Windows). The goto-ld tool can now be used as a seamless replacement for the
ld tool present on most Unix (-based) systems and for the link tool on Windows.
   Further information can be found at https://www.cprover.org/cprover-manual/
goto-cc/.



5 Architecture

Bounded model checkers such as CBMC reduce questions about program paths-
to constraints that can be solved by off-the-shelf SAT or SMT solvers. With the
SAT back end, and given a program annotated with assertions, CBMC outputs a
CNF formula the solutions of which describe program paths leading to assertion
violations. In order to do so, CBMC performs the following main steps, which are
outlined in Figure 2, and are explained below.


   source program         C parsing         Type checking               GOTO
                                                                                       Front End
                                                                      conversion



                                                  GOTO



                          Analysis &            Property               Symbolic
                        transformation      instrumentation            execution       Middle End



                                                    SSA



                          Formula
                          encoding               SAT solver


                                                                                       Back End
                                                              Counterexample       7
                                      Fig. 2: CBMC Overview


1 https://bugseng.com/products/eclair/discover
20                                Daniel Kroening, Peter Schrammel and Michael Tautschnig

5.1 Command-line Front End

The command line front end processes options given by the user and configures
CBMC accordingly. The general command syntax to call CBMC is
     cbmc [options ...] [file.c ...]                                                C11
where [options ...] are described below and [file.c ...] are zero or more
source file names. Typical user-supplied parameters are loop unwinding limits, or
the system architecture to be assumed, i.e., the bit-width of basic data types and endi-
anness, and operating system specific configuration parameters. If the user chooses
not to override the platform configuration, then the system architecture configuration
defaults to the specification of the platform CBMC has been compiled on. In the fol-
lowing we provide a description of the most commonly used command-line options;
further options controlling specific parts of CBMC’s architecture are discussed in
subsequent sections.

• General options:
     – --help, -h, -?: Display copyright information and the list of command line
       options.
     – --version: Show the current version.

• Platform configuration:
     – --function 𝑓 : Use function 𝑓 as program entry point instead of “main”.
     – -I 𝑝𝑎𝑡ℎ: Add 𝑝𝑎𝑡ℎ to the C preprocessor’s search path for expanding
       #include directives. This option may be given multiple times, which is the
       case for -D 𝑚𝑎𝑐𝑟𝑜 as well:
     – -D 𝑚𝑎𝑐𝑟𝑜: Define the C preprocessor macro 𝑚𝑎𝑐𝑟𝑜, where 𝑚𝑎𝑐𝑟𝑜 is either
       only a macro name or of the form 𝑛𝑎𝑚𝑒=𝑣𝑎𝑙𝑢𝑒.
     – --16, --32, --64: Set the bit-width of the C type int to 16, 32, or 64 bits,
       respectively.
     – --LP64, --ILP64, --LLP64, --ILP32, --LP32: Set the bit-widths of int,
       long, and pointers as defined in [23].
     – --little-endian, --big-endian: Set endianness for conversions between
       words and bytes.
     – --unsigned-char: Make char type unsigned.
     – --ppc-macos, --i386-macos, --i386-linux, --i386-win32, --win32,
       and --winx64: Set platform-specific defines, bit-widths, and endianness ac-
       cording to the given processor and operation-system combination.
• Options controlling the user interface:
     – --json-ui, --xml-ui: Change CBMC’s output to JSON or XML format-
       ted text, respectively. --json-interface, --xml-interface extend this to
       consuming options via JSON or XML, respectively. Such output (and input)
       is more suitable for machine processing.
CBMC                                                                                      21

   – --verbosity 𝑛: Sets the amount of status information printed while running
     CBMC. 𝑛 = 0 disables all output other than test cases, 𝑛 ≥ 1 enables error
     messages, 𝑛 ≥ 2 adds warnings, 𝑛 ≥ 6 enables progress information (𝑛 = 6 is
     the default), 𝑛 ≥ 8 adds statistics, and 𝑛 ≥ 9 yields debugging information.



5.2 Language Front End

CBMC uses “GOTO programs” as intermediate representation. In this language, all
non-linear control flow, such as if/switch-statements, loops and jumps, is translated to
equivalent guarded goto statements. These statements are gotos that include optional
guards, such that these guarded gotos also suffice to model if/else branching. The
most important classes of statements left at this intermediate level are assignments,
gotos, function calls, declarations, assertions, and assumptions.
    For C/C++ input source, CBMC arrives at this intermediate representation by first
invoking a C preprocessor (for example, cl on Microsoft Windows systems or gcc
-E on Unix-like systems, but other compiler tool-chains are supported as well as
discussed in Section 4) and then passing the result to CBMC’s C or C++ parser. The
output of the preprocessor can inspected by calling CBMC with --preprocess.
CBMC uses its own C and C++ parser rather than relying on existing tool chains,
which enables supporting multiple C/C++ dialects including various GCC exten-
sions. The C or C++ parser yields a parse tree annotated with source file- and line
information. The parse tree with annotated type information can be inspected by call-
ing CBMC with --show-parse-tree. Other language front ends, for example the
Java front end [13], have a different parsing work-flow, but ultimately also proceed
to type checking:
    Type checking populates a symbol table by traversing the parse tree, collecting all
type names and symbol identifiers, and assigning bit-level type information to each
symbol and expression that is found. To view the symbol table, invoke CBMC with
--show-symbol-table. CBMC aborts if any inconsistencies are detected by type
checking. As an experiment, comparing the output of cbmc --16 abs.c vs. cbmc
--32 abs.c shows how type checking affects bit-level types, and thus also the
expansion of constants to different bit vectors:
    When type checking succeeds, CBMC generates one GOTO program for each
procedure or method found in the parse tree. Furthermore, it adds a new main
function that first calls an initialisation function for objects with static lifetime and
then calls the original program entry function.
    For the earlier example of abs.c as shown in Listing 1, running
   cbmc --function abs --signed-overflow-check --show-goto-functions                    C12
yields the output shown in Listing 13. In this output, each GOTO program (each
procedure) starts with its name (lines 1, 19, and 26) and ends with an END_FUNCTION
GOTO-program instruction (lines 17, 24, and 46). Each instruction includes the
source location that it originates from (lines 2, 4, etc.). The instruction itself is printed
22                                   Daniel Kroening, Peter Schrammel and Michael Tautschnig

     constant                               constant
      * type: signedbv                       * type: signedbv
          * width: 16                            * width: 32
          * #c_type: signed_int                  * #c_type: signed_int
      * value: 0000000000000000              * value: 00000000000000000000000000000000
      * #source_location:                    * #source_location:
        * file: abs.c                          * file: abs.c
        * line: 4                              * line: 4
        * function: abs                        * function: abs
        * working_directory: /home             * working_directory: /home
      * #base: 10                            * #base: 10



 1 abs                                                 25

 2    // 0 file abs.c line 2 function abs              26 __CPROVER__start
 3    signed int y;                                    27    // 10 no location
 4    // 1 file abs.c line 2 function abs              28    __CPROVER_initialize();
 5    y = x;                                           29    // 11 file abs.c line 1
 6    // 2 file abs.c line 4 function abs              30    signed int x;
 7    IF !(x < 0) THEN GOTO 1                          31    // 12 file abs.c line 1
 8    // 3 file abs.c line 5 function abs              32    x = NONDET(signed int);
 9    ASSERT !(x == -2147483648)                       33    // 13 file abs.c line 1
10    // 4 file abs.c line 5 function abs              34    INPUT("x", x);
11    y = -x;                                          35    // 14 file abs.c line 1
12    // 5 file abs.c line 8 function abs              36    abs(x);
13 1: abs#return_value = y;                            37    // 15 file abs.c line 1
14    // 6 file abs.c line 8 function abs              38    return0 = abs#return_value;
15    dead y;                                          39    // 16 file abs.c line 1
16    // 7 file abs.c line 9 function abs              40    dead abs#return_value;
17    END_FUNCTION                                     41    // 17 file abs.c line 1
18                                                     42    OUTPUT("return", return0 );
19 __CPROVER_initialize                                43    // 18 no location
20    // 8 file <built-in-additions> line 20           44    dead x;
21    // Labels: __CPROVER_HIDE                        45    // 19 no location
22    __CPROVER_rounding_mode = 0;                     46    END_FUNCTION
23    // 9 no location
24    END_FUNCTION


       Listing 13: GOTO programs output by command C12 for abs.c (Listing 1)



in a C-like syntax. For example, lines 3 and 30 denote declarations of variables,
which may go out of scope – each such point is denoted by a corresponding dead
instruction, as can be found in lines 15 and 44. Instructions in lines 5, 13, among
others, denote assignments. Furthermore line 13 carries a label: it is the branch
target of the (conditional) goto in line 7. This conditional goto encodes the control
flow resulting from the if statement in line 4 of Listing 1.

Analysis and Transformation. The case of line 13 is peculiar in that it constitutes the
result of return-instruction removal: to keep the classes of instructions to be con-
CBMC                                                                                 23

sidered by analyses as small as possible, we simulate the effect of return statements
via goto and assignments to global, thread-local variables. Further transformations,
though not applicable to this example, include replacing function pointers. First,
function pointers are resolved via a light-weight static analysis that checks for type
compatibility between formal parameters of declared functions and the actual pa-
rameters at the point of call through a function pointer. All matching targets are
combined to a list of conditional calls, where a branch is taken if the actual value of
the function pointer matches the address of the target function. Thereby we arrive at
a static call graph.

Property Instrumentation. In line 9 we find the generated assertion as we used
--signed-overflow-check. This assertion guards the possible undefined be-
haviour resulting from negation in line 11. Such assertions are generated using
light-weight and over-approximating data-flow analyses as discussed in Section 3.
   Options controlling this instrumentation process include:
•   --bounds-check: Ensure each indexed access to an array is within its bounds.
•   --pointer-check: Ensure deferencing is only used with pointers to live objects.
•   --div-by-zero-check: Ensure that no divisor is zero.
•   --signed-overflow-check, --unsigned-overflow-check: Check the ab-
    sence of arithmetic over- and underflow on signed or unsigned integers, respec-
    tively.
•   --conversion-check: Ensure that type casts are not applied to values that could
    not be represented in the target type.
•   --undefined-shift-check: Ensure shifts do not exceed the bit-width of the
    type of the object being shifted.
•   --float-overflow-check, --nan-check: Ensure that floating-point opera-
    tions do not result in positive or negative infinity, or not-a-number, respectively.
•   --enum-range-check: Ensure that enum-typed objects never take a value other
    than the declared enum constants for that type.


Using GOTO Programs. GOTO programs as described above can be serialised and
deserialised and and from a custom binary format. This approach enables the use
of goto-cc as discussed in Section 4. Further tools that work on GOTO programs
include goto-instrument, a transformation tool, and goto-diff, implementing
the equivalent of the text-based Unix tool diff for GOTO programs.



5.3 Symbolic Execution

Options controlling program instrumentation and loop unwinding:
• --no-library: By default CBMC ships an abstracted version of system library
  functions. This options disables inclusion of such code.
24                                Daniel Kroening, Peter Schrammel and Michael Tautschnig

• --show-goto-functions: Display the GOTO functions after instrumentation
  as described in Section 5.2. This option is primarily useful for debugging pur-
  poses.
• --no-assumptions: The programmer can add assumptions to the program under
  scrutiny using the __CPROVER_assume( 𝑥 ) built-in. That is, for all paths considered by
  CBMC, the property 𝑥 must evaluate to true true at the program point where the
  built-in was inserted. If --no-assumptions is set, assumptions will be ignored.
• --function 𝑓 : Use function 𝑓 as program entry point instead of “main”.
• --depth 𝑘: Perform at most 𝑘 steps along any path while symbolically executing
  the program. This results in unsound verification, unless 𝑘 steps suffice to reach
  all states.
• --unwind 𝑘, --unwindset 𝐿:𝑘,..., --show-loop-ids: Unwind loops, re-
  cursions, and backward gotos at most 𝑘 times. With --unwindset 𝐿:𝑘,... the
  unwinding bound 𝑘 is set for loop with id 𝐿 only, where 𝐿 can be found using
  --show-loop-ids, which lists all loops with their identifiers.
  Successful verification while using --unwind or --unwindset is unsound, un-
  less the specified bounds amount to complete loop unwinding. To ensure sound
  (but possibly incomplete) verification, add --unwinding-assertions:
• --unwinding-assertions, --partial-loops: Whenever the loop unwinding
  bounds specified using --unwind or --unwindset are reached, CBMC inserts
  an assumptions that the loop condition indeed no longer holds, i.e., the loop
  would indeed be left. This may rule out feasible execution paths, and thus results
  in unsound verification as noted above. To avoid this source of unsoundness,
  --unwinding-assertions can be specified such that instead of assumptions
  assertions are inserted. The assertion checks that the loop exit condition is indeed
  always fulfilled, i.e., the number of unwinding steps was sufficient.
  With the parameter --partial-loops, neither assumptions nor assertions are
  generated during loop unwinding. This may be useful for experiments, but does
  result in verification of a possibly very different program, because each loop is
  replaced by a fixed number of conditional repetitions of the loop body without
  any checks whether the loop condition evaluates to false at the end. This may
  result in traces that cannot occur in the original program.
    As CBMC implements a variant of bounded model checking it has to pay special
attention to loops. Unlike the original bounded model checking algorithm presented
in [6], CBMC currently does not increase the maximum length of paths as bounded
model checking proceeds, and is thus not complete. Instead, CBMC eagerly unwinds
loops up to a fixed bound, which can be specified by the user on a per-loop basis or
globally, for all loops. In the course of this unwinding step, CBMC also translates
the GOTO functions to static single assignment (SSA) form [2, 22, 14]. At the end
of this process the program is represented as a mathematical equation over renamed
program variables in guarded statements. The guards determine whether, given a
concrete program execution, an assignment is actually made.
CBMC                                                                               25

   The basic idea of CBMC is to model a program’s execution up to a bounded
number of steps. Technically, this is achieved by a process that essentially amounts
to unwinding loops. This concept is best illustrated with a generic example:
1 int main(int argc, char **argv) {
2   while(cond) {
3     BODY CODE
4   }
5 }


   A BMC instance that will find bugs with up to five iterations of the loop would
contain five copies of the loop body, and essentially corresponds to checking the
following loop-free program:
1  int main(int argc, char **argv) {
2    if(cond) {
 3     BODY CODE COPY 1
 4     if(cond) {
 5       BODY CODE COPY 2
 6       if(cond) {
 7         BODY CODE COPY 3
 8         if(cond) {
 9           BODY CODE COPY 4
10           if(cond) {
11             BODY CODE COPY 5
12           }
13         }
14       }
15     }
16   }
17 }


    Note the use of the if statement to prevent the execution of the loop body in the
case that the loop ends before five iterations are executed. The construction above is
meant to produce a program that is trace equivalent with the original programs for
those traces that contain up to five iterations of the loop.
    In many cases, CBMC is able to determine automatically an upper bound on the
number of loop iterations. This may even work when the number of loop unwindings
is not constant. Consider the following example:
1   _Bool f();
2

3  int main()
4  {
 5   for(int i=0; i<100; i++)
 6   {
 7     if(f()) break;
 8   }
 9   assert(0);
10 }


    The loop in the program above has an obvious upper bound on the number of
iterations, but note that the loop may abort prematurely depending on the value that
26                                Daniel Kroening, Peter Schrammel and Michael Tautschnig

is returned by f(). CBMC is nevertheless able to automatically unwind the loop to
completion.
    This automatic detection of the unwinding bound may fail if the number of loop
iterations is highly data-dependent. Furthermore, the number of iterations that are
executed by any given loop may be too large or may simply be unbounded. For
this case, CBMC offers the command-line option --unwind 𝐵, where 𝐵 denotes
a number that corresponds to the maximal number of loop unwindings CBMC
performs on any loop.
    Note that the number of unwindings is measured by counting the number of
backjumps. In the example above, note that the condition i<100 is in fact evaluated
101 times before the loop terminates. Thus, the loop requires a limit of 101, and
not 100.
    In [1] we presented an extension to perform efficient bounded model checking of
concurrent programs, which symbolically encodes partial orders over read and write
accesses to shared variables.




5.4 SAT/SMT Back Ends

The resulting equation is translated into a CNF formula by bit-precise modelling of
all expressions plus the Boolean guards (cf. [10]). Here it should be noted that CBMC
also supports other decisions procedures as back ends, such as SMT (satisfiability
modulo theories) solvers [20, 21], in which case an encoding other than CNF is used.
These back ends can be selected using command-line options such as --smt2 (to
use the default SMT2 solver, currently Z3), --z3 to use Z3 [18], or --cvc4 to select
CVC4 [5].
    The CNF formula, which can be printed using --dimacs, is passed to the SAT
solver, which tries to find a satisfying assignment. Here, such an assignment corre-
sponds to a path violating at least one of the assertions in the program under scrutiny.
Conversely, if the formula is unsatisfiable, no assertion can be violated with the given
unwinding bounds. CBMC supports multiple properties in the program and queries
the solver iteratively in order to decide the result for each of the properties.
    If a satisfying assignment was found, the bounded model checker has determined
a counterexample to the specification given in terms of assertions. To turn the model
of the SAT formula into information useful for the user of CBMC, it is translated
into a list of assignments. CBMC finds this sequence by consulting the equation
of guarded statements: each statement with a guard evaluating to true under the
computed model constitutes an assignment occurring in the counterexample. The
actual values being assigned are also found in the model of the SAT formula. The
resulting counterexample output is as previously shown in Listing 4.
CBMC                                                                                                                                                                                                                                                                                                               27


                                                                                                                                                    overall
                 2000

 SV-COMP Score   1000


                    0


                 -1000


                 -2000


                 -3000




                                                                                                                                                                                                                               CBMC 5.10
                                                                                                                                                                                                                                           CBMC 5.11
                                                                                                                                                                                                                                                       CBMC 3/19
                                                                                                                                                                                                                                                                   CBMC 6/19
                                                                                                                                                                                                                                                                               CBMC 5.12
                                                                                                                                                                                                                                                                                           CBMC 5.13
                                                                                                                                                                                                                                                                                                       CBMC 5.20
                         CBMC 4.0
                                    CBMC 4.1
                                               CBMC 4.2
                                                          CBMC 4.3
                                                                     CBMC 4.4
                                                                                CBMC 4.6
                                                                                           CBMC 4.7
                                                                                                      CBMC 4.9
                                                                                                                 CBMC 5.0
                                                                                                                            CBMC 5.1
                                                                                                                                       CBMC 5.2
                                                                                                                                                  CBMC 5.3
                                                                                                                                                             CBMC 5.4
                                                                                                                                                                        CBMC 5.5
                                                                                                                                                                                   CBMC 5.6
                                                                                                                                                                                              CBMC 5.7
                                                                                                                                                                                                         CBMC 5.8
                                                                                                                                                                                                                    CBMC 5.9
                                                                                                                                                   Release

                                               Fig. 3: Score time line over all selected benchmarks


6 Performance History

CBMC has been continuously developed for more than 15 years, but has it actually
become better over the years? To answer this question, we benchmarked 22 CBMC
versions from version 4.0 (June 2011) to 5.20 (December 2020).2 We used 9 cate-
gories from SV-COMP3 and ran them using BenchExec4 on a machine with Ubuntu
16.04 and an Intel Xeon Platinum 8175M CPU, 2.50GHz with resource limits of
15 GB and 900 s.
   Figure 3 shows the evolution of CBMC’s SV-COMP score5 on the all the selected
benchmarks. Note that the scores cannot be compared with the official SV-COMP
results because the rules changed over the years as well as the benchmark sets.
CBMC won SV-COMP 2014 with a version based on 4.5, and was ranked third in
SV-COMP 2015 with a version based on 4.9.
   In terms of SV-COMP score, CBMC has improved substantially in the more than
9 years spanned by these versions. In particular, the versions towards CBMC 5.0

2 Ports of the older versions are available in the cbmc-x.y-patch branches in https://github.com/
diffblue/cbmc. The corresponding SV-COMP wrapper scripts are in the cbmc-x.y branches in
https://github.com/diffblue/cprover-sv-comp.
3 ReachSafety-Arrays, ReachSafety-BitVectors, ReachSafety-ControlFlow, ReachSafety-
Floats,  ReachSafety-Heap,     ReachSafety-Loops,       MemSafety-Arrays,      MemSafety-
Heap,   MemSafety-LinkedLists;    version   https://github.com/sosy-lab/sv-benchmarks/tree/
b8369a395d4749eb7eee1c3bd8149a3dc799e7f3
4 https://github.com/sosy-lab/benchexec/releases/tag/1.17
5 One point for finding a bug in an unsafe benchmark; -32 points for incorrectly claiming it safe.
2 points for proving a safe benchmark correct; -16 points for incorrectly reporting a bug.
28                                                                   Daniel Kroening, Peter Schrammel and Michael Tautschnig


                            1000
                                                                                                     CBMC 4.0    CBMC 5.5
                                                                                                     CBMC 4.1    CBMC 5.6
                                                                                                     CBMC 4.2    CBMC 5.7
                                                                                                     CBMC 4.3    CBMC 5.8
                             100                                                                     CBMC 4.4    CBMC 5.9
                                                                                                     CBMC 4.6   CBMC 5.10
                                                                                                     CBMC 4.7   CBMC 5.11
                                                                                                     CBMC 4.9   CBMC 3/19
                                                                                                     CBMC 5.0   CBMC 6/19
                              10
CPU Time (s)




                                                                                                     CBMC 5.1   CBMC 5.12
                                                                                                     CBMC 5.2   CBMC 5.13
                                                                                                     CBMC 5.3   CBMC 5.20
                                                                                                     CBMC 5.4
                               1




                              0.1




                             0.01
                                    0




                                           100




                                                    200




                                                                   300




                                                                                400




                                                                                      500




                                                                                               600
                                                           Correct benchmarks



                                         Fig. 4: CPU time quantile plot over all selected benchmarks


                            1x1011
                                                                                                     CBMC 4.0    CBMC 5.5
                                                                                                     CBMC 4.1    CBMC 5.6
                                                                                                     CBMC 4.2    CBMC 5.7
                                                                                                     CBMC 4.3    CBMC 5.8
                            1x1010                                                                   CBMC 4.4    CBMC 5.9
                                                                                                     CBMC 4.6   CBMC 5.10
Peak Memory Usage (bytes)




                                                                                                     CBMC 4.7   CBMC 5.11
                                                                                                     CBMC 4.9   CBMC 3/19
                                                                                                     CBMC 5.0   CBMC 6/19
                            1x109                                                                    CBMC 5.1   CBMC 5.12
                                                                                                     CBMC 5.2   CBMC 5.13
                                                                                                     CBMC 5.3   CBMC 5.20
                                                                                                     CBMC 5.4
                            1x108




                            1x107




                            1x106
                                     0




                                            100




                                                     200




                                                                   300




                                                                                400




                                                                                      500




                                                                                               600




                                                           Correct benchmarks



                                    Fig. 5: Peak memory usage quantile plot over all selected benchmarks


(2014-2015) were a huge improvement in comparison to early CBMC 4.x versions
(2011-2013). A second wave of improvements is visible from CBMC 5.7 to 5.9
(2017-2018).
   Looking at the quantile plot of CPU time in Figure 4, we can also observe these
improvements up to CBMC 5.0 (with a notable jump from 4.4 to 4.6 and 4.6 to
5.0) followed by some stagnation up to CBMC 5.7 (and a regression in 5.4). There
was, however, substantial speed up from CBMC 5.7 to 5.9 (with a regression in 5.8)
and further less noteworthy speed improvements in most recent versions. The big
improvements from CBMC 4.4 to 4.6, 4.6 to 5.0 and 5.7 to 5.9 also brought about
a major reduction in memory consumption, as the quantile plot of peak memory
usage in Figure 5 shows. These improvements can mainly be attributed to enhanced
CBMC                                                                                                                        29


               1000
                                                                                                     CBMC 4.0    CBMC 5.5
                                                                                                     CBMC 4.1    CBMC 5.6
                                                                                                     CBMC 4.2    CBMC 5.7
                                                                                                     CBMC 4.3    CBMC 5.8
                100                                                                                  CBMC 4.4    CBMC 5.9
                                                                                                     CBMC 4.6   CBMC 5.10
                                                                                                     CBMC 4.7   CBMC 5.11
                                                                                                     CBMC 4.9   CBMC 3/19
                                                                                                     CBMC 5.0   CBMC 6/19
                 10
CPU Time (s)




                                                                                                     CBMC 5.1   CBMC 5.12
                                                                                                     CBMC 5.2   CBMC 5.13
                                                                                                     CBMC 5.3   CBMC 5.20
                                                                                                     CBMC 5.4
                  1




                0.1




               0.01
                      0



                          10



                                 20



                                           30



                                                 40



                                                         50



                                                                60



                                                                        70



                                                                                   80



                                                                                          90



                                                                                               100
                                                 Correct benchmarks



                               Fig. 6: CPU time quantile plot over ReachSafety-Loops


               1000
                                                                                                     CBMC 4.0    CBMC 5.5
                                                                                                     CBMC 4.1    CBMC 5.6
                                                                                                     CBMC 4.2    CBMC 5.7
                                                                                                     CBMC 4.3    CBMC 5.8
                100                                                                                  CBMC 4.4    CBMC 5.9
                                                                                                     CBMC 4.6   CBMC 5.10
                                                                                                     CBMC 4.7   CBMC 5.11
                                                                                                     CBMC 4.9   CBMC 3/19
                                                                                                     CBMC 5.0   CBMC 6/19
                 10
CPU Time (s)




                                                                                                     CBMC 5.1   CBMC 5.12
                                                                                                     CBMC 5.2   CBMC 5.13
                                                                                                     CBMC 5.3   CBMC 5.20
                                                                                                     CBMC 5.4
                  1




                0.1




               0.01
                      0




                           20




                                      40




                                                60




                                                         80




                                                                  100




                                                                             120




                                                                                        140




                                                                                               160




                                                 Correct benchmarks



                                Fig. 7: CPU time quantile plot over MemSafety-Heap


expression simplification before encoding SSA into a SAT formula. CBMC 5.9 intro-
duced on-demand definitions for compiler-built-in functions, which gave a constant
speed-up of half a second. It is visible on benchmarks with short runtime.
   The improvements were not uniform over all the categories. For example, CBMC’s
performance on the ReachSafety-Loops category shows only small variations (see
Figure 6). These benchmarks are quite simple integer programs, which already
CBMC 4.0 supported very efficiently and solved roughly the same number of bench-
marks at a comparable speed as the latest version.
   A totally different picture can be seen in Figure 7 for the MemSafety-Heap bench-
marks. These benchmarks use more complex language features such as dynamic
memory allocation, pointers and structs. CBMC has not only become significantly
30                                                  Daniel Kroening, Peter Schrammel and Michael Tautschnig


               1000
                                                                                    CBMC 4.0    CBMC 5.5
                                                                                    CBMC 4.1    CBMC 5.6
                                                                                    CBMC 4.2    CBMC 5.7
                                                                                    CBMC 4.3    CBMC 5.8
                100                                                                 CBMC 4.4    CBMC 5.9
                                                                                    CBMC 4.6   CBMC 5.10
                                                                                    CBMC 4.7   CBMC 5.11
                                                                                    CBMC 4.9   CBMC 3/19
                                                                                    CBMC 5.0   CBMC 6/19
                 10
CPU Time (s)




                                                                                    CBMC 5.1   CBMC 5.12
                                                                                    CBMC 5.2   CBMC 5.13
                                                                                    CBMC 5.3   CBMC 5.20
                                                                                    CBMC 5.4
                  1




                0.1




               0.01
                      0



                          5



                                 10



                                      15



                                              20



                                                       25



                                                                30



                                                                     35



                                                                          40



                                                                               45
                                           Correct benchmarks



                              Fig. 8: CPU time quantile plot over ReachSafety-Floats


faster, but also produces far fewer incorrect results (from a sixth incorrect results
in CBMC 4.6 down to a single incorrect result since CBMC 5.9). The gap between
CBMC 4.4 and 4.6 is due to the introduction of a memory leak instrumentation,
which enabled proving these properties.
    The latest improvements between 3/19 and 5.20 were due to significant enhance-
ments in the symbolic execution. For example, the data structures for performing
constant propagation and storing points-to sets have been optimised to avoid unnec-
essary copying. Field-sensitive constant propagation for structures and cell-sensitive
constant propagation for arrays have been introduced as well as propagation of con-
ditions has been introduced in order to filter points-to sets and avoid exploration of
unfeasible branches.
    Figure 8 shows the evolution of CPU time on the ReachSafety-Floats benchmarks.
CBMC’s floating point decision procedure has seen a sustained period of bug fixes
and optimisations, in particular between CBMC 4.2 and 5.0. CBMC 5.8 introduced
a more complete built-in library for math.h, which explains that later 5.x versions
solve many more benchmarks than the earlier ones.
    Overall, we observe that the performance evolution of CBMC was not so much
dominated by a few major features that gave a massive performance boost, but rather
improved through a steady stream of incremental enhancements and bug fixes.



7 Future Directions

CBMC has proven to be able to verify and find bugs in real, large-scale software
projects. Despite successes [8], the use of a software verification tool in such a
context is far from an easy task that often requires expert users. Moreover, it requires
CBMC                                                                                              31

a significant amount of manual work to divide and conquer the application in a
modular way and writing harnesses and stub functions with realistic assumptions
about the environment the program is executing in. Hence, besides the perpetual
endeavours of improving CBMC’s performance, improving the usability of the tool
for CBMC users is the main focus of development.



References

 1. Alglave, J., Kroening, D., Tautschnig, M.: Partial orders for efficient bounded model checking
    of concurrent software. In: CAV, LNCS, vol. 8044, pp. 141–157 (2013)
 2. Alpern, B., Wegman, M.N., Zadeck, F.K.: Detecting equality of variables in programs. In:
    POPL, pp. 1–11 (1988)
 3. American National Standards Institute: ANSI/ISO/IEC 9899-1999: Programming Languages
    — C. American National Standards Institute, 1430 Broadway, New York, NY 10018, USA
    (1999)
 4. Barrett, C., Sebastiani, R., Seshia, S.A., Tinelli, C.: Satisfiability Modulo Theories, Frontiers
    in Artificial Intelligence and Applications, vol. 185, chap. 26, pp. 825–885. IOS Press (2009)
 5. Barrett, C.W., Conway, C.L., Deters, M., Hadarean, L., Jovanovic, D., King, T., Reynolds, A.,
    Tinelli, C.: CVC4. In: G. Gopalakrishnan, S. Qadeer (eds.) Computer Aided Verification -
    23rd International Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011. Proceedings,
    Lecture Notes in Computer Science, vol. 6806, pp. 171–177. Springer (2011). DOI 10.1007/
    978-3-642-22110-1\ 14. URL https://doi.org/10.1007/978-3-642-22110-1 14
 6. Biere, A., Cimatti, A., Clarke, E.M., Zhu, Y.: Symbolic model checking without BDDs. In:
    Tools and Algorithms for the Construction and Analysis of Systems, Lecture Notes in Computer
    Science, vol. 1579, pp. 193–207. Springer (1999)
 7. Biere, A., Heule, M., van Maaren, H., Walsh, T. (eds.): Handbook of Satisfiability, Frontiers
    in Artificial Intelligence and Applications, vol. 185. IOS Press (2009)
 8. Chong, N., Cook, B., Eidelman, J., Kallas, K., Khazem, K., Monteiro, F.R., Schwartz-
    Narbonne, D., Tasiran, S., Tautschnig, M., Tuttle, M.R.: Code-level model checking in the
    software development workflow at amazon web services. Softw. Pract. Exp. 51(4), 772–797
    (2021). DOI 10.1002/spe.2949. URL https://doi.org/10.1002/spe.2949
 9. Clarke, E.M., Kroening, D., Lerda, F.: A tool for checking ANSI-C programs. In: TACAS,
    LNCS, vol. 2988, pp. 168–176 (2004)
10. Clarke, E.M., Kroening, D., Yorav, K.: Behavioral consistency of c and verilog programs using
    bounded model checking. In: DAC, pp. 368–371. ACM (2003)
11. Cook, B., Döbel, B., Kroening, D., Manthey, N., Pohlack, M., Polgreen, E., Tautschnig, M.,
    Wieczorkiewicz, P.: Using model checking tools to triage the severity of security bugs in
    the xen hypervisor. In: 2020 Formal Methods in Computer Aided Design, FMCAD 2020,
    Haifa, Israel, September 21-24, 2020, pp. 185–193. IEEE (2020). DOI 10.34727/2020/isbn.
    978-3-85448-042-6\ 26. URL https://doi.org/10.34727/2020/isbn.978-3-85448-042-6 26
12. Cook, B., Khazem, K., Kroening, D., Tasiran, S., Tautschnig, M., Tuttle, M.R.: Model checking
    boot code from AWS data centers. In: Computer Aided Verification - 30th International
    Conference, CAV 2018, Held as Part of the Federated Logic Conference, FloC 2018, Oxford,
    UK, July 14-17, 2018, Proceedings, Part II, Lecture Notes in Computer Science, vol. 10982,
    pp. 467–486. Springer (2018). DOI 10.1007/978-3-319-96142-2\ 28. URL https://doi.org/
    10.1007/978-3-319-96142-2 28
13. Cordeiro, L.C., Kesseli, P., Kroening, D., Schrammel, P., Trtík, M.: JBMC: A bounded model
    checking tool for verifying Java bytecode. In: Computer Aided Verification, CAV, LNCS, vol.
    10981, pp. 183–190. Springer (2018)
14. Cytron, R., Ferrante, J., Rosen, B.K., Wegman, M.N., Zadeck, F.K.: An efficient method of
    computing static single assignment form. In: POPL, pp. 25–35 (1989)
32                                     Daniel Kroening, Peter Schrammel and Michael Tautschnig

15. Kroening, D., Strichman, O.: Decision Procedures - An Algorithmic Point of View, Second
    Edition. Texts in Theoretical Computer Science. An EATCS Series. Springer (2016). DOI
    10.1007/978-3-662-50497-0. URL https://doi.org/10.1007/978-3-662-50497-0
16. Kroening, D., Tautschnig, M.: Automating software analysis at large scale. In: MEMICS,
    Lecture Notes in Computer Science, vol. 8934, pp. 30–39. Springer (2014). DOI 10.1007/
    978-3-319-14896-0 3. URL http://dx.doi.org/10.1007/978-3-319-14896-0 3
17. Malacaria, P., Tautschnig, M., Distefano, D.: Information leakage analysis of complex C code
    and its application to OpenSSL. In: ISoLA, Lecture Notes in Computer Science, vol. 9952,
    pp. 909–925 (2016). DOI 10.1007/978-3-319-47166-2 63. URL http://dx.doi.org/10.1007/
     978-3-319-47166-2 63
18. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: C.R. Ramakrishnan, J. Rehof
    (eds.) Tools and Algorithms for the Construction and Analysis of Systems, 14th International
    Conference, TACAS 2008, Held as Part of the Joint European Conferences on Theory and
    Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings,
    Lecture Notes in Computer Science, vol. 4963, pp. 337–340. Springer (2008). DOI 10.1007/
    978-3-540-78800-3\ 24. URL https://doi.org/10.1007/978-3-540-78800-3 24
19. Nemer, F., Cassé, H., Sainrat, P., Bahsoun, J.P., Michiel, M.D.: Papabench: a free real-time
    benchmark. In: 6th Intl. Workshop on Worst-Case Execution Time (WCET) Analysis, July 4,
    2006, Dresden, Germany, OASICS, vol. 4 (2006). URL http://drops.dagstuhl.de/opus/volltexte/
     2006/678
20. Nieuwenhuis, R., Oliveras, A., Tinelli, C.: Abstract DPLL and abstract DPLL modulo theories.
    In: LPAR, Lecture Notes in Computer Science, vol. 3452, pp. 36–50. Springer (2004)
21. Nieuwenhuis, R., Oliveras, A., Tinelli, C.: Solving sat and sat modulo theories: From an abstract
    davis–putnam–logemann–loveland procedure to dpll(). J. ACM 53(6), 937–977 (2006)
22. Rosen, B.K., Wegman, M.N., Zadeck, F.K.: Global value numbers and redundant computations.
    In: POPL, pp. 12–27 (1988)
23. The Open Group: Data Size Neutrality and 64-bit Support. IEEE (1998)
