Logical Methods in Computer Science
Vol. 11(3:19)2015, pp. 1–57                                                           Submitted        Aug. 18, 2014
www.lmcs-online.org                                                                   Published        Sep. 22, 2015




                                FEATHERWEIGHT VERIFAST

                    FRÉDÉRIC VOGELS, BART JACOBS, AND FRANK PIESSENS

     iMinds-DistriNet, Dept. C.S., KU Leuven, Celestijnenlaan 200A, 3001 Leuven, Belgium
     e-mail address: {frederic.vogels, bart.jacobs, frank.piessens}@gmail.com




         Abstract. VeriFast is a leading research prototype tool for the sound modular verifica-
         tion of safety and correctness properties of single-threaded and multithreaded C and Java
         programs. It has been used as a vehicle for exploration and validation of novel program
         verification techniques and for industrial case studies; it has served well at a number of
         program verification competitions; and it has been used for teaching by multiple teachers
         independent of the authors.
            However, until now, while VeriFast’s operation has been described informally in a num-
         ber of publications, and specific verification techniques have been formalized, a clear and
         precise exposition of how VeriFast works has not yet appeared.
            In this article we present for the first time a formal definition and soundness proof of
         a core subset of the VeriFast program verification approach. The exposition aims to be
         both accessible and rigorous: the text is based on lecture notes for a graduate course on
         program verification, and it is backed by an executable machine-readable definition and
         machine-checked soundness proof in Coq.




                                             Introduction
For many classes of safety-critical or security-critical programs, such as operating system
components, internet infrastructure, or embedded software, conventional quality assurance
approaches such as testing, code review, or even model checking are insufficient to detect
all bugs and achieve good confidence in their safety and security; for these programs, the
newer technique of modular formal verification may be the most promising approach.
     VeriFast is a sound modular formal verification approach for single-threaded and mul-
tithreaded imperative programs being developed at KU Leuven. The prototype tool that
implements this approach1 takes as input a C or Java program annotated with precondi-
tions, postconditions, loop invariants, data structure definitions, and proof hints written in
a variant of separation logic [39, 42], and symbolically executes each function/method. It
either reports “0 errors found” or the source location of a potential error. If it reports “0
errors found”, it is guaranteed (modulo bugs in the tool) that no execution of the program
  2012 ACM CCS: [Theory of computation]: Logic—Logic and verification / Programming logic; Se-
mantics and reasoning—Program reasoning.
  Key words and phrases: program verification, separation logic, symbolic execution.
  1
   Download it from http://distrinet.cs.kuleuven.be/software/VeriFast/.



l    LOGICAL METHODS
     IN COMPUTER SCIENCE                DOI:10.2168/LMCS-11(3:19)2015
                                                                                 c
                                                                                CC
                                                                                     F. Vogels, B. Jacobs, and F. Piessens
                                                                                     Creative Commons
2                             F. VOGELS, B. JACOBS, AND F. PIESSENS




will a) perform an illegal memory access such as a null pointer dereference, an access of
unallocated memory, or an access of an array outside of its bounds; b) perform a data race,
where two threads access the same variable concurrently without synchronization, and at
least one access is a write operation; c) violate the user-specified function/method contracts
or the contracts of the library or API functions/methods used by the program. If it reports
an error, it shows a symbolic execution trace that leads to the error, including the symbolic
state (store, heap, and path condition) at each step.
     VeriFast has served as a vehicle for exploration and validation of a number of novel
program verification techniques [26, 29, 49, 48] and for a number of industrial case studies
[41]; it has served well at a number of program verification competitions2; and it has been
used for teaching program verification by the authors as well as by independent instructors
at other institutions3.
     Until now, while VeriFast’s operation has been described informally in a number of
publications [28, 27, 44], and specific verification techniques have been formalized [26, 29,
49, 48], a clear and precise exposition of how VeriFast works has not yet appeared.
     In this article, we present a formal definition of a simplified version of the VeriFast
program verification approach, called Featherweight VeriFast, as well as an outline for a
proof of the soundness of this approach, i.e. that if verification of a program succeeds,
then no execution of the program accesses unallocated memory. Featherweight VeriFast
targets a simple toy programming language with routines, loops, and dynamic memory
allocation and deallocation, and supports routine contracts, loop invariants, separation
logic predicates, and symbolic execution. It captures some of the core aspects of the C
programming language, but leaves out many complexities, including advanced concepts
such as function pointers and concurrency, even though these are supported by VeriFast
[26, 29]. The running example (introduced on p. 4) builds a large linked list in one routine
and tears it down in another one; another example that appears (on p. 46) is the in-place
reversal of a linked list. We use Featherweight VeriFast to verify the safety of both examples.
     We hope that the definitions in this article are clear and the proofs are convincing;
however, to address any shortcomings in this regard, we developed a machine-readable exe-
cutable definition and machine-checked soundness proof of a slight variant of Featherweight
VeriFast, called Mechanised Featherweight VeriFast, in the Coq proof assistant. It is avail-
able at http://www.cs.kuleuven.be/~bartj/fvf/. Furthermore, the executable nature
of the definitions allowed us to test for errors in our programming language semantics and to
verify that the formalized verification algorithm succeeds in verifying the example programs.
     The structure of the article is as follows. In Section 1, we define the syntax of the input
programming language, and we illustrate it with a few example programs. In Section 2, we
illustrate and define the concrete execution of programs in this programming language. In
Sections 3 and 4, we gradually introduce the VeriFast verification approach: in Section 4,
we present the approach itself, called symbolic execution 4; in Section 3, we present an
intermediate type of execution, called semiconcrete execution, that sits between concrete
execution and symbolic execution, which introduces some but not all features of the VeriFast
approach. In Section 5, we discuss Mechanised Featherweight VeriFast. We end the article
with an overview of related work in Section 6 and a conclusion in Section 7.
    2
    See Endnote (a).
    3
    See Endnote (b).
   4We use this term in this article to denote the specific algorithm implemented by VeriFast. It is an
instance of the general approach known in the literature as symbolic execution.
                                       FEATHERWEIGHT VERIFAST                                                3




     This article is based on a slide deck and lecture notes for a graduate course on program
verification, and aims to be usable as an introduction to program verification. In the course,
theory lectures based on this material are interleaved with hands-on lab sessions based on
the VeriFast Tutorial [30]. Acknowledgements of related work are deferred to Section 6.

                                 1. The Programming Language
In this section, we define the syntax of programs and then show an example program.

1.1. Syntax of Programs. The programming language is as follows. An integer expression
e is either an integer literal z, a variable x, an addition e + e, or a subtraction e − e. A
boolean expression b is either an equality comparison e = e, a less-than comparison e < e,
or a negation ¬b of another boolean expression. A command c is either an assignment
x := e of an integer expression e to a variable x, a sequential composition (c; c) of two
commands (whose execution proceeds by first executing the first command and then the
second command), a conditional command if b then c else c, a while loop while b do c,
a routine call r(e) (which calls routine r with argument list e (a line over a letter means a
list of the things denoted by the letter))5, a heap memory block allocation x := malloc(n)
(which allocates a block of heap memory of size n and stores the address of the new block in
variable x), a memory read x := [e] (which reads the value of the memory cell whose address
is given by e and stores it in variable x), a memory write [e] := e (which writes the value of
the second expression into the memory cell whose address is given by the first expression),
or a deallocation command free(e) which releases the memory block allocated by malloc
whose address is given by e. A routine definition rdef is of the form routine r(x) = c which
declares x as the parameter list and c as the body of routine r.
Definition 1.1. Syntax of Programs

                              z ∈ Z, n ∈ N
                              x ∈ Vars
                     e ::=    z | x | e+e | e−e
                     b ::=    e = e | e < e | ¬b
                     c ::=    x := e | (c; c) | if b then c else c | while b do c
                              | r(e) | x := malloc(n) | x := [e] | [e] := e | free(e)
                  rdef ::=    routine r(x) = c


1.2. Example Program. The example program of Figure 1 consists of routine definitions
for routines range and dispose and a main command. Routine range has parameters i, n,
and result; it builds a linked list that stores the integers from i, inclusive, to n, exclusive,
and writes the address of the new linked list into the memory cell whose address is given
by result. If i equals n, the value 0 is written to address result, denoting the empty linked
list. Otherwise, a new linked list node is allocated with two fields; the first field holds the
value of the node, and the second field holds the address of the next node. A recursive call
of routine range is used to build the remaining nodes of the linked list.
   5In this simple language, routines have no return value. A routine can pass a result to its caller by taking
an address where the result should be stored as an argument.
4                           F. VOGELS, B. JACOBS, AND F. PIESSENS




                  routine range(i, n, result) =
                                                     routine dispose(list) =
                    if i = n then
                                                       if list = 0 then
                       [result] := 0
                                                          dummy := dummy
                    else (
                                                       else (
                       head := malloc(2);
                                                          tail := [list + 1];
                       [result] := head;
                                                          free(list);
                       [head] := i;
                                                          dispose(tail)
                       range(i + 1, n, head + 1)
                                                       )
                    )

                         cell := malloc(1); range(0, 100000000, cell);
                         list := [cell]; free(cell); dispose(list)

                                 Figure 1: Example Program

     Routine dispose has the single parameter list. It frees the nodes of the linked list
pointed to by list. If list is 0, this means the linked list is empty and nothing needs to be
done. (Since in this programming language, each if command must specify a command
for the then branch and for the else branch, we specify the command dummy := dummy
for the then branch, which has no effect.) Otherwise, the first node is freed and then a
recursive call of dispose is used to free the remaining nodes.
     The main program calls range to build a linked list holding the numbers 0 through
99999999. Before doing so, however, it allocates a memory cell to hold the address of the
new list. After the range call, the address of the list is read from the cell, the cell is freed,
and finally the list nodes are freed using a call of routine dispose.
     The purpose of Featherweight VeriFast is to verify that programs, like this one, never
fail (i.e. access unallocated memory), i.e. that no execution of the program fails. The
example program has an infinite number of executions: for each possible address of each
linked list node, there is a separate execution. In one execution, the first node is allocated
at address 1000, the second node at address 2000, etc. In another execution, the first node
is allocated at address 123, the second node at address 234, etc. Featherweight VeriFast
must check that none of these infinitely many executions fail.
     Note: in a language like Java, the precise address at which an object is allocated cannot
influence program execution, since the program can only compare two object references for
equality; it cannot compare an object reference with an integer, check if one reference is
less than another one, use literal addresses as object references, etc. However, in C, as well
as in the programming language which we defined above, this is possible, so it is possible to
write programs that fail or not depending on the address picked by malloc. Here is such a
program:
                                     x := malloc(1); [42] := 0
If, in a given execution of this program, the address picked by malloc happens to be 42,
the execution completes normally; otherwise, it fails.
     Note also: While this aspect of memory allocation is peculiar to C, the fact that the
language contains nondeterministic constructs, i.e. constructs whose observable behavior
is not uniquely determined by the language specification, is universal to all programming
languages: any language construct that accepts user input or otherwise interacts with the
                                  FEATHERWEIGHT VERIFAST                                      5




             // s = 0, h = 0
             pair := malloc(2);
             // s = 0[pair := 100], h = {[mb(100, 2), 100 7→ 42, 101 7→ 24]}
             [pair] := 0;
             // s = 0[pair := 100], h = {[mb(100, 2), 100 7→ 0, 101 7→ 24]}
             free(pair)
             // s = 0[pair := 100], h = 0

             where                                    
                                                                     y     if z = x
                f [x := y] = function update = λz.
                                                                     f (z) otherwise
                0 = λx. 0 = empty store = empty heap = {[]} = empty multiset
                {[e1 , . . . , en ]} = 0 + {[e1 ]} + · · · + {[en ]}
                M + {[e]} = M [e := M (e) + 1]

                        Figure 2: Example concrete execution trace

environment is nondeterministic from a verification point of view, since it leads to multiple
possible executions, all of which need to be checked.
    The main point illustrated by the example is that a program may have infinitely many
executions, each of which may be very long (or even infinitely long), and all of these need
to be checked for failure. This is true in all programming languages. Clearly, it is inefficient
or impossible to naively check each execution separately. VeriFast (and Featherweight
VeriFast) perform modular symbolic execution to achieve efficiency. After we define concrete
execution precisely in Section 2, we introduce the Featherweight VeriFast constructs for
modularity in Section 3 and the symbolic execution in Section 4.

                                  2. Concrete Execution
In this section, we provide a formal definition of the behavior of programs of our program-
ming language. We first introduce the notion of concrete execution states by means of two
examples of concrete execution traces (sequences of states reached during an execution). We
then introduce the notion of outcomes, which we use to express failure, nontermination, and
nondeterminism. Finally, we use these concepts to define concrete execution of commands
and safety of a program, and we discuss the verification problem.

2.1. Small Example Concrete Execution Trace. The small example program in Fig-
ure 2 allocates a memory block of size 2, initializes the first element of the block to 0, and
then frees the block. An example execution trace of this program is shown in comments
before and after the code lines. An execution trace is a sequence of execution states (or
states for short). In our simple programming language, a state consists of a store s and a
heap h. A store is a function that maps variables to their current values; a heap is a mul-
tiset (or bag) of heap chunks. A multiset is like a set, except that it may contain elements
more than once. Mathematically, it is a function that maps each potential element to the
number of times it occurs in the multiset. A heap chunk (in concrete executions) is either
a points-to chunk ℓ 7→ v denoting that there is an allocated memory cell at address ℓ whose
6                               F. VOGELS, B. JACOBS, AND F. PIESSENS




current value is v, or a malloc block chunk mb(ℓ, n) denoting that a memory block of size
n was allocated at address ℓ by malloc, i.e. that the memory cells at addresses ℓ through
ℓ + n − 1 are part of a single block, which will be freed as one unit when free is called with
argument ℓ.
      The example programming language makes a few simplifications compared to real ma-
chine states: memory cells may store arbitrary integers, rather than just bytes, and memory
addresses may be arbitrary positive integers, rather than being bounded by the size of in-
stalled memory (or the size of the address space).
      The initial store maps all variables to zero; the initial heap contains no heap chunks,
i.e. it contains all heap chunks zero times, so it is a function that maps all heap chunks to
zero. We denote a function that maps all arguments to zero by 0.
      In the example execution trace, the malloc operation allocates the new block at address
100. Therefore, in the execution state after the malloc operation, the store maps the target
variable pair of the malloc operation to 100, and the heap contains three heap chunks: the
two points-to chunks that correspond to the two memory cells that constitute the newly
allocated block, and the malloc block chunk that records that these two memory cells are
part of the same block. As in C, the initial contents of the newly allocated memory cells
are arbitrary; in the example trace, the contents are 42 and 24. (All numbers that were
picked arbitrarily are shown in orange, to highlight that the program has infinitely many
other executions, that pick these numbers differently.)
      The notation f [a := b] denotes the function that is like f except that it maps argument
a to value b. The notation {[e1 , e2 ]} denotes the multiset with elements e1 and e2 (where
possibly e1 = e2 ). Formally, {[e1 , . . . , en ]} = 0 + {[e1 ]} + · · · + {[en ]}, where M + {[e]} = M [e :=
M (e) + 1]; i.e. the multiset M + {[e]} is like M except that element e occurs once more than
in M .
      The second command, which initializes the memory cell at address pair to zero, causes
the state to change in just one place: the value of the points-to chunk with address 100
changes from 42 to 0.
      Finally, the free command removes the three heap chunks from the heap and leaves it
empty; it does not modify any variables so the store remains unchanged.

2.2. Large Example Concrete Execution Trace.
Example 2.1. Larger Example Concrete Execution Trace See Figure 3.
     Now, let’s look at an execution trace of routine range from the example program intro-
duced earlier. This trace is part of a larger program execution trace. We look at a particular
call of range. As shown in the first state of the trace, the values of parameters i, n, and r are
5, 8, and 41. That is, the caller is asking range to build a linked list with three nodes holding
the values 5, 6, and 7, respectively, and to store the address of the newly built linked list in
the previously allocated memory cell at address 41. At the time of the call, the heap con-
sists of some chunks h0 plus a points-to chunk with address 41 and value 77. (We use both
M + M ′ and M ⊎ M ′ for multiset union, defined as M + M ′ = M ⊎ M ′ = λe. M (e) + M ′ (e).)
     The first statement is the if statement. It checks if i = n. Since this is not the case,
we skip the then branch and execute the else branch. The state upon arrival in the else
branch is unchanged.
                                   FEATHERWEIGHT VERIFAST                                     7




                routine range(i, n, r) =
                s:0[i:5, n:8, r:41], h:h0 ⊎{[417→77]}
                if i = n then l := 0 else (
                s:0[i:5, n:8, r:41], h:h0 ⊎{[417→77]}
                l := malloc(2);
                s:0[i:5, n:8, r:41, l:50], h:h0 ⊎{[417→77,mb(50, 2),507→88,517→99]}
                [l] := i; range(i + 1, n, l + 1)
                    ..
                     . (Execution of 3 nested range calls)
                s:0[i:5, n:8, r:41, l:50], h:h0 ⊎{[417→77,mb(50, 2),507→5,517→60,
                   mb(60, 2),60 7→ 6,61 7→ 70,mb(70, 2),70 7→ 7,71 7→ 0]}
                );
                [r] := l
                s:0[i:5, n:8, r:41, l:50], h:h0 ⊎{[41 7→ 50,mb(50, 2),507→5,517→60,
                   mb(60, 2),607→6,617→70,mb(70, 2),707→7,717→0]}
                where h0 : {[mb(30),307→3,317→40,mb(40, 2),407→4]}

                    Figure 3: Larger Example Concrete Execution Trace

     The execution of the malloc block is as before, in the simple example. In this trace,
the block is allocated at address 50, and the initial values of the memory cells are 88 and
99.
     Then, the first cell of the new block is initialized to i. We do not show the resulting
state; only the value of the points-to chunk with address 50 changes.
     Then, we get the recursive call of range to build the rest of the linked list. We do not
show the execution states reached during the execution of this recursive call (which itself
contains two more calls, one nested within the other); we skip directly to the state reached
upon return from the call.
     At this point, two more linked list nodes have been allocated, at addresses 60 and 70
(in this trace). Also, the linked list is well-formed: the second cell (which serves as the next
field) of the node at address 50 points to the node at address 60, the next field of the node
at address 60 points to the node at address 70, and the next field of the node at address 70
is a null pointer, indicating the end of the linked list.
     The final command writes the address 50 of the newly built linked list to the address 41
provided by the caller; this modifies only the points-to chunk with address 41 in the heap.
     The points to remember about this example trace are that it is long (since it contains
three nested routine executions, which we did not show), that its states have large heaps
with many chunks (here, up to 15 chunks, if we include h0 ), and that routine range has
infinitely many more execution traces like this one, that pick the numbers shown in orange
differently. In subsequent sections, we will define alternative ways of executing programs
where programs have fewer and shorter executions, and execution states have fewer heap
chunks.

2.3. Concrete Execution States. We define the set CStates of concrete execution states.
The concrete stores CStores are the functions from variables to integers. The concrete
predicates (i.e. the concrete chunk names) are the points-to predicate 7→ and the malloc
8                           F. VOGELS, B. JACOBS, AND F. PIESSENS




block predicate mb. The set of concrete chunks is the set of expressions of the form p(ℓ, v),
where p is a concrete predicate, and ℓ and v are integers. We call p the name of the chunk,
and ℓ and v the arguments of the chunk. The concrete heaps are the multisets of concrete
chunks. The concrete states are the pairs of concrete stores and concrete heaps.
    We often use the alternative syntax ℓ 7→ v for the points-to chunk 7→(ℓ, v).
Definition 2.2. Concrete Execution States

                       CStores = Vars → Z
                    CPredicates = {7→, mb}
                      CChunks = {p(ℓ, v) | p ∈ CPredicates, ℓ, v ∈ Z}
                       CHeaps = CChunks → N
                       CStates = CStores × CHeaps
                          ℓ 7→ v is alternative syntax for 7→(ℓ, v)


2.4. Outcomes. In this subsection, we introduce the notion of outcomes, which we use to
express failure, nontermination, and nondeterminism. We first introduce the various types
of outcomes by example. We then provide formal definitions of outcomes, without or with
answers. Finally, we define the concepts of satisfaction of a postcondition by an outcome,
coverage of an outcome by another outcome, and sequential composition of outcomes; we
state some properties; and we introduce some notations.

2.4.1. Outcomes by Example. To define mathematically what the concrete executions of a
given program are, we define the function exec, which takes as arguments a command and
an input state, and returns the outcome of executing the command starting in the given
input state. In simple cases, such as in the case of the assignment command p := 42, the
outcome is a single output state: executing this assignment in the state (0, 0) with an empty
store (i.e. one that maps all variables to zero) and an empty heap results in the single output
state where the store maps p to value 42 and all other variables to zero, and where the heap
is still empty. We call such an outcome a singleton outcome, and we denote the singleton
outcome with output state σ using angle brackets: hσi.
Example 2.3. Concrete Execution: Singleton Outcomes
                           exec(p := 42)((0, 0)) = h(0[p := 42], 0)i
    Note: we define and use function exec in a curried form: instead of defining it as a
function of two parameters (a command and an input state), we define it as a function
of one parameter (a command) that returns another function of one parameter (an input
state) which itself returns an outcome. We call the latter kind of function (a function that
takes an input state and returns an outcome) a mutator. Therefore, exec is a function that
maps commands to mutators.
Example 2.4. Concrete Execution: Demonic Choice

                              exec(p := malloc(0))((0, 0)) =
                                      h(0[p := 1], {[mb(1, 0)]})i
                                 ⊗ h(0[p := 2], {[mb(2, 0)]})i
                                 ⊗ h(0[p := 3], {[mb(3, 0)]})i
                                 ⊗ ···
                                      FEATHERWEIGHT VERIFAST                                              9




                            exec(p := malloc(1))((0, 0)) =
                              h(0[p := 1], {[mb(1, 1), 1 7→ 0]})i
                                 ⊗ h(0[p := 1], {[mb(1, 1), 1 7→ 1]})i ⊗ · · ·
                              ⊗ h(0[p := 2], {[mb(2, 1), 2 7→ 0]})i
                                 ⊗ h(0[p := 2], {[mb(2, 1), 2 7→ 1]})i ⊗ · · ·
                              ⊗ h(0[p := 3], {[mb(3, 1), 3 7→ 0]})i
                                 ⊗ h(0[p := 3], {[mb(3, 1), 3 7→ 1]})i ⊗ · · ·
                              ⊗···
     The outcome of executing a command is not always a single state. Specifically, consider
malloc commands: the command p := malloc(0) allocates a new memory block of size
zero. This means that it does not allocate any memory cells, but it does create an mb
chunk at an address that is different from the address of existing mb chunks. When starting
from an empty heap, this address may be any positive integer. For every distinct address
chosen, there is a different output state. Notice that this choice can be considered demonic:
the program should not fail even if an attacker who tries to make the program fail makes
this choice. Therefore, the outcome returned by exec is a demonic choice over the integers,
where the chosen number is used as the address of the new block in the output state of a
singleton outcome. That is, the operands of the demonic choice outcome in this example are
singleton outcomes. The demonic choice between outcomes o1 and o2 is denoted as o1 ⊗ o2 .
     In the case of the command p := malloc(1), the outcome is a demonic choice over both
the address of the new block and the initial value of the new memory cell.
Example 2.5. Concrete Execution: Failure, Nontermination, Angelic Choice

                     exec([0] := 33)((0, 0)) = ⊥

                     exec(recurse())((0, 0)) = ⊤
                       where routine recurse() = recurse()

                     exec(backtrack(c1 , c2 ))(σ) = exec(c1 )(σ) ⊕ exec(c2 )(σ)
     Singleton outcomes and demonic choices are not the only kinds of outcomes; there are
three more kinds.
     Consider the command [0] := 33 when executed in the empty heap. This is an access
of an unallocated memory cell, i.e. it is a failure. We denote the failure outcome by the
symbol for “bottom”: ⊥.
     Consider the routine call recurse() and assume that routine recurse is defined such that
its body is simply a recursive call of itself. This command performs an infinite recursion;
it does not terminate.6 Nontermination is often considered undesirable; however, in many
other cases, it is intentional: for example, a web server or a database server is not supposed
to terminate unless and until the user instructs it to do so. In any case, VeriFast and
Featherweight VeriFast do not verify termination. Featherweight VeriFast verifies only the
absence of accesses of unallocated memory, so from this point of view a nonterminating
command is a good thing, since it prevents the remainder of the program from executing,
  6In the case of a real programming language, this would lead to a stack overflow error at run time, except
if the compiler performs tail recursion optimization. Neither VeriFast nor Featherweight VeriFast verify the
absence of stack overflows, so we ignore this issue in this formalization.
10                                 F. VOGELS, B. JACOBS, AND F. PIESSENS




including any commands that might fail. Therefore, we represent nontermination with the
symbol for “top”, ⊤, the opposite of ⊥.
     Finally, to round out the “algebra of outcomes”, we introduce also angelic choice. True
angelic choice does not occur in concrete executions of our programming language7; however,
some real programming languages do have a form of angelic choice. For example, the logic
programming language Prolog allows the user to specify multiple alternative ways to solve
a problem. At run time, Prolog will try first the first alternative; if it fails, it restores
the program state and then tries the second alternative. The program as a whole succeeds
if either alternative succeeds: it is as if an angel chooses the right alternative. Another
example is a transactional database: if a schedule fails, the state is rolled back and another
schedule is attempted.
     We introduce angelic choice here to obtain a nice, complete algebra, but also because we
will use angelic choice in our definition of the Featherweight VeriFast verification algorithm.
     In summary, (concrete) mutators are functions from (concrete) input states to outcomes
over (concrete) output states. (Later we will also use outcomes over other state spaces.)
The concrete execution function exec maps commands to concrete mutators.
Definition 2.6. Type of Concrete Execution

                               CMutators = CStates → Outcomes(CStates)
                                    exec ∈ Commands → CMutators


2.4.2. Outcomes: Definition. An outcome N    φ over a state space S is either a singleton out-
come
L     hσi, with σ  ∈  S, or a demonic choice   Φ over the outcomes in Φ, or an angelic choice
    Φ over the outcomes in Φ, where Φ is a setN             L over S. We denote the set of
                                                  of outcomes
outcomes over state space S as Outcomes(S).         Φ and     Φ are called infinitary demonic
and angelic choice, since the set Φ is potentially infinite.
     Binary demonic choice, binary angelic choice, nontermination, and failure can be defined
as special cases of infinitary demonic choice and infinitary angelic choice: binary choices are
choices over the set collecting the two alternatives; nontermination is a demonic choice over
zero alternatives (the attacker is stuck with no alternatives, which is a good thing); failure
is an angelic choice over zero alternatives (the angel is stuck with no alternatives, which is
a bad thing).
Definition 2.7. Outcomes

                                   φ ::=       hσi
                                               N    singleton outcome
                                             | L Φ demonic choice
                                             |    Φ angelic choice
                                          σ∈S ⇒ N hσi ∈ Outcomes(S)
                                Φ ⊆ Outcomes(S) ⇒ L Φ ∈ Outcomes(S)
                                Φ ⊆ Outcomes(S) ⇒    Φ ∈ Outcomes(S)
     7A degenerate form of angelic choice does occur: failure is equivalent to angelic choice over zero alterna-
tives, as we will see later.
                                  FEATHERWEIGHT VERIFAST                                       11




                                   N
                      φ1 ⊗ φ2    = L{φ1 , φ2 }     binary demonic choice
                      φ1 ⊕ φ2    = N{φ1 , φ2 }     binary angelic choice
                           ⊤     = L∅              nontermination
                           ⊥     =   ∅             failure


2.4.3. Outcomes with Answers. Often, it is useful to consider mutators that have not just
an output state but also an answer. We denote a singleton outcome with output state
σ ∈ S and answer a ∈ A by hσ, ai. For uniformity, we treat outcomes without answers like
outcomes whose answer is the unit value tt, the sole element of the unit set unit. That is, we
consider Outcomes(S) a shorthand for Outcomes(S, unit), and hσi a shorthand for hσ, tti.
Definition 2.8. Outcomes with Answers

                             φ ::=      hσ,
                                        N ai singleton outcome
                                      | L Φ demonic choice
                                      |     Φ angelic choice
                          σ ∈S ∧a∈A ⇒ N   hσ, ai ∈ Outcomes(S, A)
                     Φ ⊆ Outcomes(S, A) ⇒ L Φ ∈ Outcomes(S, A)
                     Φ ⊆ Outcomes(S, A) ⇒    Φ ∈ Outcomes(S, A)
                      hσi = hσ, tti ∈ Outcomes(S) = Outcomes(S, unit)


2.4.4. Outcomes: Satisfaction, Coverage. A useful question to ask is whether an outcome
φ ∈ Outcomes(S, A) satisfies a given postcondition Q, where a postcondition can be
modelled mathematically as the set of pairs of output states and answers that satisfy it,
i.e. Q ⊆ S × A. We denote this by φ {Q}.
     We define this recursively as follows:
• A singleton outcome hσ, ai satisfies postcondition Q if the output state σ and answer a
   satisfy Q, i.e. (σ, a)N∈ Q.
• A demonic choice L Φ satisfies Q if all alternatives satisfy Q
• An angelic choice        Φ satisfies Q if some alternative satisfies Q.
     Notice that it follows from this definition that nontermination satisfies all postconditions
(even the postcondition that does not accept any output state), and failure satisfies no
postcondition (not even the postcondition that accepts all output states).
     We also define coverage between outcomes: we say outcome φ covers outcome φ′ , de-
noted φ ⇛ φ′ , if for any postcondition Q, if φ satisfies Q, then φ′ satisfies Q. Intuitively,
this means φ is a “worse” outcome than φ′ ; if φ′ is failure, then φ must be failure, but the
converse does not hold: it is possible that φ is failure but φ′ is not. Another way to look at
this is to say that φ is a safe approximation of φ′ for verification: if we prove that φ satisfies
some postcondition, then it follows that φ′ also satisfies it.
     We lift outcome coverage pointwise to mutators: a mutator C covers a mutator C ′ if
for each input state σ, the outcome of C started in state σ covers the outcome of C ′ started
in state σ.
12                         F. VOGELS, B. JACOBS, AND F. PIESSENS




Definition 2.9. Outcomes: Satisfaction, Coverage

                           φ ∈ Outcomes(S, A) Q ⊆ S × A
                     φ {Q} (“outcome φ satisfies postcondition Q”)

                           hσ,
                            Nai {Q} ⇔ (σ, a) ∈ Q
                            L Φ {Q} ⇔ ∀φ ∈ Φ. φ {Q}
                               Φ {Q} ⇔ ∃φ ∈ Φ. φ {Q}

                              φ ⇛ φ′ ⇔ ∀Q. φ {Q} ⇒ φ′ {Q}
                             C ⇛ C ′ ⇔ ∀σ. C(σ) ⇛ C ′ (σ)


2.4.5. Outcomes: Sequential Composition. An important concept is the sequential compo-
sition φ; C of an outcome φ ∈ Outcomes(S) and a mutator C ∈ S → Outcomes(S ′ ). The
intuition is straightforward: the output states of φ are passed as input states to C. The
result is again an outcome. It is defined as follows:
• if φ is a singleton outcome hσi, the sequential composition is the outcome of passing σ as
   input to C
• if φ is a demonic or angelic choice, the sequential composition is the distribution of the
   sequential composition over the alternatives.
     We also define sequential composition C; C ′ of two mutators C and C ′ : it is simply
the mutator that, for a given input state σ, passes σ to C and composes the outcome
sequentially with C ′ .
Definition 2.10. Outcomes: Sequential composition
              −; − : Outcomes(S) → (S → Outcomes(S ′ )) → Outcomes(S ′ )

                              Nhσi; C = NC(σ)
                             (L Φ); C = L{φ ∈ Φ. (φ; C)}
                             ( Φ); C =      {φ ∈ Φ. (φ; C)}
                                  C; C = λσ. C(σ); C ′
                                      ′


    We have the following important properties of sequential composition:
• Associativity: given three mutators C, C ′ , and C ′′ , first composing C and C ′ and then
  composing the resulting mutator with C ′′ is equivalent to first composing C ′ and C ′′ and
  then composing C with the resulting mutator.
• Monotonicity: if mutator C1 is worse than mutator C1′ , and mutator C2 is worse than
  mutator C2′ , then C1 ; C2 is worse than C1′ ; C2′ .
• Satisfaction: the sequential composition φ; C satisfies the postcondition Q if and only if
  φ satisfies the postcondition that accepts the state σ if C(σ) satisfies Q.
Lemma 2.11 (Associativity of Sequential Composition of Mutators).
                                 (C; C ′ ); C ′′ = C; (C ′ ; C ′′ )
Lemma 2.12 (Monotonicity of Sequential Composition of Mutators). If C1 ⇛ C1′ and
C2 ⇛ C2′ then C1 ; C2 ⇛ C1′ ; C2′ .
                                  FEATHERWEIGHT VERIFAST                                     13




Lemma 2.13 (Satisfaction of Sequential Composition of Mutators).
                                φ; C {Q} ⇔ φ {σ | C(σ) {Q}}


2.4.6. Outcomes: Sequential Composition (with Answers). We can generalize these concepts
to the case of outcomes with answers. If φ is an outcome and C(−) is a function from an-
swers to mutators, i.e. a mutator parameterized by an answer, then we write the sequential
composition of φ and C(−) as x ← φ; C(x); that is, the answer of φ, bound to the vari-
able x, is passed as an input argument to C(−). The definition and the properties are a
straightforward adaptation of the ones given above for outcomes without answers.
Definition 2.14. Outcomes: Sequential composition (with Answers)

               x ← −; −(x) : O (S, A) → (A → S → O (S ′ , B)) → O (S ′ , B)
                     x ←Nhσ, ai; C(x) = C(a)(σ)
                                         N
                    x ← (L Φ); C(x) = L{φ ∈ Φ. (x ← φ; C(x))}
                    x ← ( Φ); C(x) =       {φ ∈ Φ. (x ← φ; C(x))}
                             x ← C; C ′ (x) = λσ. x ← C(σ); C ′ (x)
Lemma 2.15 (Associativity of Sequential Composition of Mutators with Answers).
                  y ← (x ← C; C ′ (x)); C ′′ (y) = x ← C; (y ← C ′ (x); C ′′ (y))
Lemma 2.16 (Monotonicity of Sequential Composition of Mutators with Answers). If
C1 ⇛ C1′ and ∀a. C2 (a) ⇛ C2′ (a) then x ← C1 ; C2 (x) ⇛ x ← C1′ ; C2′ (x).
Lemma 2.17 (Satisfaction of Sequential Composition of Mutators with Answers).
                        x ← φ; C(x) {Q} ⇔ φ {(σ, a) | C(a)(σ) {Q}}


2.4.7. Outcomes: Notations. We introduce some additional notations and concepts that
will be useful in the definition of the executions.                                         N
     We lift demonic and angelic choice to mutators: if C̃ is a set of mutators, then         C̃
is the demonic choice over these mutators. It is the mutator that, for a given input state
σ, demonically chooses between the outcomes obtained by passing σ to the elements of C̃.
Angelic choice over mutators is defined analogously.
                                                N
     We use the “variable binding” notation         i ∈ I. φi to denote the demonic choice over
the outcomes obtained by letting i range over I in φi . We also use this notation for angelic
choice and for choices over mutators.
     As an extension of the variable binding notation, we also allow boolean propositions to
the left of the dot in demonic and angelic choices. If the proposition is true, this has no
effect; otherwise, in the case of angelic choice, this means failure, and in the case of demonic
choice, this means nontermination.
     We define the primitive mutator yield a as the mutator that does not modify the state
and answers a. We define noop as the mutator that does nothing; it merely answers the
unit element tt.
     We define side-effect-only sequential composition C;, C ′ of two mutators C and C ′ as
the mutator that first executes C, and then executes C ′ , and whose answer is the answer of
C. The answer of C ′ is ignored.
14                           F. VOGELS, B. JACOBS, AND F. PIESSENS




Notation 2.18. Outcomes: Notations
                          N            N
                            C̃ = λσ.     {C(σ) | C ∈ C̃}
                          L            L
                            C̃ = λσ.     {C(σ) | C ∈ C̃}
                           N              N
                           L i ∈ I. φi = L{φi | i ∈ I}
                              i ∈ I. φi = {φi | i ∈ I}
                         N                 N
                         L true. φ = φ     L false. φ = ⊤
                           true. φ = φ       false. φ = ⊥
                                       yield a = λσ. hσ, ai
                                         noop = yield tt

                                  C;, C ′ = x ← C; C ′ ; yield x


2.5. Some Auxiliary Definitions. We introduce some further auxiliary notions that will
be useful in the definition of concrete execution of commands.
     The domain of a heap h is the set of domain elements of the form p(ℓ) where a value
v exists such that p(ℓ, v) occurs in h.
     The mutator assume(b), where b is a boolean expression, evaluates b in the given input
store; if b evaluates to true, the mutator does nothing; otherwise, it does not terminate. We
define evaluation JbKs of a boolean expression b or arithmetic expression e under a store s
as follows: Je = e′ Ks = (JeKs = Je′ Ks ), Je < e′ Ks = (JeKs < Je′ Ks ), J¬bKs = ¬JbKs, JzKs = z,
JxKs = s(x), Je + e′ Ks = JeKs + Je′ Ks , and Je − e′ Ks = JeKs − Je′ Ks .
     The mutator store simply returns the current store. The mutator store := s sets the
current store to s. The mutator with(s, C) executes the mutator C under store s and then
restores the original store. Its answer is the answer of C. The mutator eval(e) answers the
value of e under the current store. The mutator x := v updates the store, assigning value
v to variable x.
Definition 2.19. Some Auxiliary Definitions

                          dom(h) = {p(ℓ) | ∃v.N p(ℓ, v) ∈ h}
                       assume(b) = λ(s, h). JbKs = true. h(s, h)i
                             store = λ(s, h). h(s, h), si
                       store := s′ = λ(s, h). h(s′ , h)i
                       with(s′ , C) = s ← store; store := s′ ; C;, store := s
                           eval(e) = λ(s, h). h(s, h), JeKs i
                           x := v = λ(s, h). h(s[x := v], h)i
     We denote mutator C iterated n times as C n . C iterated zero times does nothing; C
iterated n + 1 times is the sequential composition of C and C iterated n times. The demonic
iteration C ∗ of C is C iterated a demonically chosen number of times.
     Concrete consumption of a multiset h of chunks fails if the heap does not contain these
chunks; otherwise, it removes them. Concrete production of a multiset h of chunks blocks if
the heap already contains chunks with the same address, i.e. if the addresses of the chunks
in h are not all pairwise distinct from the addresses of the chunks that are already in the
heap. Otherwise, it adds the chunks to the heap. Concrete consumption and production of
a single chunk α are defined in the obvious way.
                                   FEATHERWEIGHT VERIFAST                                  15




          exec0 (c) = ⊤

          execn+1 (x := e) = v ← eval(e); x := v

          execn+1 (c; c′ ) = execn (c); execn (c′ )

          execn+1 (if b then c else c′ ) =
            assume(b); execn (c) ⊗ assume(¬b); execn (c′ )

          execn+1 (while b do c) =
            (assume(b); execn (c))∗ ; assume(¬b)

          execn+1 (r(e)) = v ← eval(e); with(0[x := v], execn (c))
            where routine r(x) = c

            Nn+1 (x := malloc(n)) =
          exec
                ℓ, v1 , . . . , vn ∈ Z.
               cproduce chunks({[mb(ℓ, n), ℓ 7→ v1 , . . . , ℓ + n − 1 7→ vn ]}); x := ℓ

            Ln+1 (x := [e]) = ℓ ← eval(e);
          exec
               v. cconsume chunk(ℓ 7→ v); cproduce chunk(ℓ 7→ v); x := v

            Ln+1 ([e] := e ) = ℓ ← eval(e); v ← eval(e );
          exec            ′                           ′

               v0 . cconsume chunk(ℓ 7→ v0 ); cproduce chunk(ℓ 7→ v)

            Ln+1 (free(e)) = ℓ ← eval(e);
          exec
                N ∈ N, v1 , . . . , vN ∈ Z.
               cconsume chunks({[mb(ℓ, N ), ℓ 7→ v1 , . . . , ℓ + N − 1 7→ vN ]})
                      N
          exec(c) =       n ∈ N. execn (c)

                        Figure 4: Concrete Execution of Commands

Definition 2.20. Some Auxiliary Definitions

                              C 0 = noop
                           C n+1 = C; C n
                                              n
                                  N
                            C∗ =     n ∈ N.LC ′
                             ′
          cconsume chunks(h ) = λ(s, h).     h ≤ h. h(s, h − h′ )i
            cconsume chunk(α) = cconsumeNchunks({[α]})
           cproduce chunks(h′ ) = λ(s, h).   dom(h) ∩ dom(h′ ) = ∅. h(s, h ⊎ h′ )i
             cproduce chunk(α) = cproduce chunks({[α]})


2.6. Concrete Execution of Commands.
Definition 2.21. Concrete Execution of Commands See Figure 4.
16                          F. VOGELS, B. JACOBS, AND F. PIESSENS




     To define the concrete execution function exec, we first define a helper function execn ,
which is indexed by the maximum depth of the execution. If an execution exceeds the
maximum depth, execn returns ⊤, i.e. the execution does not terminate.
     Therefore, for any command c, exec0 (c) returns the mutator ⊤ (which is the mutator
that for any input state returns the outcome ⊤).
     Execution of an assignment x := e evaluates e and binds variable x to its value.
     Execution of a sequential composition c; c′ is the sequential composition of the execution
of c and the execution of c′ . (Notice that the two semicolons in this rule have different
meanings: the former is part of the syntax of commands defined on Page 3; the latter is the
function defined on Page 12 that takes two mutators and returns a mutator.)
     Execution of an if-then-else command if b then c else c′ demonically chooses between
two branches: in the first branch, it is assumed that the condition b evaluates to true, and
then command c is executed; in the second branch, it is assumed that b evaluates to false,
and then c′ is executed. Notice that this is equivalent to evaluating the condition and then,
depending on whether it evaluates to true or false, executing c or c′ , respectively.
     Execution of a loop while b do c first executes the body some demonically chosen
number of times, after assuming that the loop condition holds, and then assumes that the
condition does not hold.
     Execution of a call r(e) of routine r with argument list e first evaluates e to obtain
values v and then executes the body c of r in a store which binds the parameters x of r to
v.
     Execution of a memory block allocation command x := malloc(n) demonically picks
an address ℓ and values v1 , . . . , vn and produces the malloc block chunk and the n points-to
chunks that constitute the newly allocated memory block. Finally, the execution binds
variable x to the address ℓ.
     Execution of a memory read command x := [e] angelically picks a value v and tries to
consume a points-to chunk at the address given by e and with value v. If it succeeds, it
puts the chunk back and binds x to v.
     Execution of a memory write command [e] := e′ angelically picks an old value v0 and
tries to consume a points-to chunk at the address given by e and with value v0 . If it succeeds,
it puts the chunk back with an updated value.
     Execution of a memory block deallocation command free(e) first evaluates expression
e to an address ℓ and then tries to consume a malloc block chunk and a corresponding
number of points-to chunks at address ℓ.
     Execution of a command demonically chooses a maximum depth and then executes
the command up to that depth. Notice that this is equivalent to executing the command
without a depth bound.

 2.7. Safety of a Program. We say that a program is safe if no execution of the program
 accesses unallocated memory, i.e. no execution fails, when started from the empty state σ0 .
(Notice that the failure outcome is the only outcome that does not satisfy postcondition
“true”.)
      The verification problem addressed by Featherweight VeriFast is to check whether a
 command c is a safe program.
                                 FEATHERWEIGHT VERIFAST                                     17




                                        exec    scexec symexec
                            Recursion   Yes       No     No
                              Looping   Yes       No     No
                            Branching Infinite Infinite Finite
                         Is Algorithm    No       No     Yes

                     Assertions                          Symbols
                     Predicates                       Path Condition
                  Routine contracts                   Fresh Symbols
                   Loop invariants                   Theorem Prover
          exec   −−−−−−−−−−−−−−−→          scexec   −−−−−−−−−−−−−−→        symexec


                         Figure 5: Solving the Verification Problem

Definition 2.22. Safety of a Program
                                        σ0 = (0, 0)
                                     a ⊲ f = f (a)
                          safe program(c) = σ0 ⊲ exec(c) {true}
Definition 2.23 (The Verification Problem).
                                       safe program(c)


2.8. Solving the Verification Problem. See Figure 5.
     How to solve the verification problem? Naively computing the full traces of all execu-
tions of a program is impossible, since traces may be very large or even infinite (due to
recursion and loops), and there may be infinitely many executions (due to the nondetermin-
ism of memory allocation, causing execution to split into infinitely many branches, one for
each choice of address). Therefore, concrete execution itself cannot serve as an algorithm
for checking program safety.
     To obtain an algorithm, we define new kinds of executions that do not exhibit infinitely
long traces and/or infinite branching. Specifically, in Section 3 we define semiconcrete exe-
cution (scexec), where we use routine contracts and loop invariants, expressed as assertions
that use predicates to denote data structures of potentially unbounded size, to limit the
length of execution traces. Specifically, semiconcrete execution executes each routine sepa-
rately, starting from an arbitrary initial state that satisfies the precondition, and checking
that each final state satisfies the postcondition. Correspondingly, a routine call is executed
using the callee’s contract instead of its body. Similarly, a loop body is executed separately,
starting from an arbitrary state that satisfies the loop invariant, and checking that each
final state again satisfies the loop invariant. Execution of a loop first checks that the loop
invariant holds on entry to the loop, and then updates the state to an arbitrary final state
that satisfies the loop invariant. Since routine body and loop body executions are no longer
inlined into the executions of their callers or loops, all executions have finite length.
     However, semiconcrete execution still exhibits infinite branching; therefore, in Section 4
we define the actual verification algorithm of Featherweight VeriFast, which we call symbolic
execution (symexec). It builds on semiconcrete execution but eliminates infinite branching
18                          F. VOGELS, B. JACOBS, AND F. PIESSENS




through the use of symbols and a path condition, such that a single symbol can be used
to represent an infinite number of concrete values. Infinite branching is thus replaced by
picking a fresh symbol. A theorem prover is used to decide equalities between terms and
other conditions involving symbols under a given path condition.
    Our solution to the verification problem is then to execute the program symbolically.
Crucially, the executions are designed such that if symbolic execution of a program succeeds
(sym-safe program(c)), then semiconcrete execution succeeds (sc-safe program(c)), and if
semiconcrete execution succeeds, then concrete execution succeeds (safe program(c)). These
properties are called the soundness of symbolic execution and the soundness of semiconcrete
execution, respectively. In the next two sections, we define these executions and sketch a
proof of their soundness.
Definition 2.24 (Soundness).
                safe program(c) ⇐ sc-safe program(c) ⇐ sym-safe program(c)


                              3. Semiconcrete Execution
In this section, we define semiconcrete execution, which introduces routine contracts and
loop invariants to limit the length of execution traces. Routine contracts and loop invari-
ants are specified using a language of assertions, which specify both the facts (boolean
expressions) and the resources (heap chunks) that are required or provided by a routine or
loop body. To specify potentially unbounded data structures, predicates are used, which are
named, parameterized assertions which may be recursive, i.e. mention themselves in their
definition.
     The structure of this section is as follows. First, we introduce the new concepts involved
in semiconcrete execution using a number of example programs and execution traces. Then,
we formally define semiconcrete execution. Finally, we sketch an approach for proving that
if a program is safe under semiconcrete execution, then it is safe under concrete execution,
i.e. semiconcrete execution is a sound approximation for checking the safety of a program
under concrete execution.

3.1. Annotations by Example. In this subsection, we introduce the kinds of program
annotations required by Featherweight VeriFast by means of some examples.
Example 3.1. Annotations: Simple Example

                               routine swap(cell1, cell2)
                                 req cell1 7→ ?v1 ∗ cell2 7→ ?v2
                                 ens cell1 7→ v2 ∗ cell2 7→ v1
                                 =
                                   value1 := [cell1];
                                   value2 := [cell2];
                                   [cell1] := value2;
                                   [cell2] := value1
                                  FEATHERWEIGHT VERIFAST                                      19




     The example above shows a simple routine swap that swaps the values of two memory
cells whose addresses are given by arguments cell1 and cell2. The body first reads the cells’
original values into variables and then writes each cell’s original value into the other cell.
The routine has been annotated with a routine contract consisting of a precondition (also
known as a requires clause, denoted using keyword req) and a postcondition (also known as
an ensures clause, denoted using keyword ens). The precondition describes the set of initial
states accepted by the routine; the postcondition describes the set of final states generated
by the routine when started from an initial state that satisfies the precondition.
     The precondition of routine swap states that the routine requires two distinct memory
cells to be present in the heap, one at address cell1 and the other at address cell2. Further-
more, it introduces two ghost variables v1 and v2: it binds v1 to the original value of the
cell at address cell1 and v2 to the original value of the cell at address cell2. In general, when
a variable appears in an assertion immediately preceded by a question mark, this is called
a variable pattern. A variable pattern ?x introduces the variable x and binds it to the value
found in the heap corresponding to the position where the variable pattern appears.
     In the example, the purpose of introducing the variables v1 and v2 in the precondition
is so that they can be used in the postcondition to specify the relationship between the
initial state and the final state of the routine. Specifically, the postcondition specifies that
in the final state, the same memory cells are still present in the heap, and their value has
changed such that the new value of the cell at address cell1 equals the original value of the
cell at address cell2 and vice versa.
     Notice that the assertions that serve as the precondition and the postcondition of rou-
tine swap specify only resources (heap chunks). In general, assertions may also specify
facts (boolean expressions). Correspondingly, there are two kinds of elementary assertions:
boolean expressions and predicate assertions. Elementary assertions can be composed using
the separating conjunction ∗. Its meaning is that the facts on the left and the facts on the
right are both true, and that furthermore the resources on the left and the resources on
the right are both present separately, i.e. the heap can be split into two parts such that the
resources specified by the left-hand side of the assertion are in one part and the resources
specified by the right-hand side of the assertion are in the other part. Notice how, in this
respect, separating conjunction differs from ordinary logical conjunction (AND): we have
that a is equivalent to a ∧ a, but we do not have that a is equivalent to a ∗ a. In particular,
a ∗ a specifies that the heap contains two occurrences of each resource specified by a, which
generally is not possible, and therefore a ∗ a is generally unsatisfiable. This also means that
the precondition of routine swap implies that cell1 and cell2 denote distinct addresses.
     Now, consider again the example routine range that we introduced earlier. Recall
that this routine builds a linked list holding the values between argument i, inclusive, and
argument n, exclusive, and writes the address of the first node into the previously allocated
memory cell whose address is given by argument result.
     We show a contract for this routine in Figure 6. The precondition specifies that a
memory cell must exist at the address given by argument result. The postcondition specifies
that this memory cell still exists, and that it now points to a linked list. The latter guarantee
is specified using the predicate list, defined above. The definition of the predicate declares
one parameter, l, and a body, which is an assertion. The body performs a case analysis on
whether l equals 0. If so, it specifies only the trivial fact that 0 equals 0, i.e. it does not
specify anything. Otherwise, it specifies that the heap contains a malloc block chunk of
20                          F. VOGELS, B. JACOBS, AND F. PIESSENS




                          predicate list(l) =
                            if l = 0 then 0 = 0 else
                               mb(l, 2) ∗ l 7→ ?v ∗ l + 1 7→ ?n ∗ list(n)

                          routine range(i, n, result)
                            req result 7→ ?dummy
                            ens result 7→ ?list ∗ list(list)
                            =
                              if i = n then head := 0 else (
                                 head := malloc(2);
                                 [head] := i;
                                 range(i + 1, n, head + 1)
                              );
                              close list(head); [result] := head

                             Figure 6: Annotations: Predicates

size 2 at address l, as well as two memory cells, at addresses l and l + 1, as well as another
linked list pointed to by the memory cell at address l + 1.
     Technically, what happens is that the predicate definition introduces a new kind of
chunk, or more specifically, a new chunk name, and allows this chunk name to be used in
predicate assertions. As a result, in semiconcrete execution, there are two kinds of predicates:
the built-in predicates mb and 7→, and the user-defined predicates. Correspondingly, the
heap contains two kinds of chunks: those whose name is a built-in predicate, and those
whose name is a user-defined predicate. The purpose of chunks corresponding to user-
defined predicates is to “bundle up” zero or more malloc block chunks and points-to chunks,
along with some facts. Such “bundling up” is necessary for writing contracts for routines
that manipulate data structures of unbounded size. For example, it is impossible to write a
postcondition for routine range without using user-defined predicates: a postcondition that
contains m points-to assertions cannot describe a linked list of length greater than m, so
such a postcondition does not hold for a call of range where n − i > m.
     The built-in chunks are created by the malloc statement. How are the user-defined
chunks created? To enable the creation of user-defined chunks, semiconcrete execution
introduces a new form of commands into the programming language, called close commands.
The command close p(e) requires that p is a user-defined predicate; it removes from the
heap the chunks described by the body of the predicate, and checks the facts required by
the body of the predicate, and then adds a user-defined chunk whose name is p and whose
arguments are the values of e. That is, the command bundles up the resources and facts
described by the body of predicate p into a chunk named p.
     In the example, the body of routine range, after allocating the first node and performing
the recursive call to build the rest of the linked list, performs a close operation to bundle
the three chunks of the first node and the list chunk that represents the rest of the linked
list together into a single list chunk.

3.2. Syntax of Annotations. In summary, the programming language syntax extensions
introduced by semiconcrete execution are as follows.
                                  FEATHERWEIGHT VERIFAST                                      21




              routine range(i, n, r)
                  req r 7→ ?dummy ens r 7→ ?list ∗ list(list)
              s:0[i:5, n:8, r:41], h:0
              produce (r 7→ ?dummy)
              s:0[i:5, n:8, r:41], h:{[417→77]}
              if i = n then l := 0 else (
              l := malloc(2);
              s:0[i:5, n:8, r:41, l:50], h:{[417→77,mb(50, 2),507→88,517→99]}
              [l] := i; range(i + 1, n, l + 1)
              consume(l+17→?dummy); produce (l+17→?list ∗ list(list))
              s:0[i:5, n:8, r:41, l:50], h:{[417→77,mb(50, 2),507→5,517→60,list(60)]}
              ); close list(l); [r] := l
              s:0[i:5, n:8, r:41, l:50], h:{[417→50,list(50)]}
              consume(r 7→ ?list ∗ list(list))
              s:0[i:5, n:8, r:41, l:50], h:0

                     Figure 7: Semiconcrete Execution: Example Trace

     A program may now declare a number of routine specifications rspec of the form
routine r(x) req a ens a′ , which associate with the routine name r and parameter list
x the precondition a and postcondition a′ , which are assertions. Furthermore, the syn-
tax of loops is extended to include a loop invariant clause inv a, where a is an assertion.
Furthermore, a program may declare a number of predicate definitions, which associate a
predicate name and a list of parameters with a body, which is an assertion. An assertion a
is a boolean expression b, a predicate assertion p(e, ?x) (where p is either a built-in predi-
cate or a user-defined predicate), a separating conjunction a ∗ a′ , or a conditional assertion
if b then a else a′ . Two new commands are introduced: the open command and the close
command. The open command performs the inverse operation of the close command: it
unbundles a user-defined chunk, i.e. it removes the user-defined chunk from the heap and
adds the chunks described by the body of the predicate.
Definition 3.2. Annotations

                            q ∈ UserDefinedPredicates
                    p ::= 7→ | mb | q
                    a ::= b | p(e, ?x) | a ∗ a | if b then a else a
              preddef ::= predicate q(x) = a
                    c ::= · · · | while b inv a do c | open q(e) | close q(e)
                rspec ::= routine r(x) req a ens a
                         e 7→ ?x is alternative syntax for 7→(e, ?x)


3.3. Semiconcrete Execution: Example Trace. Recall the example concrete execution
trace of routine range in Figure 3. Recall that the notable features of this trace are that
the trace is long, since it contains three nested executions of routine range; that the heap is
large, since it includes the entire heap that existed on entry to the routine, as well as all of
the chunks produced by all of the nested calls; and that there is infinite branching.
22                          F. VOGELS, B. JACOBS, AND F. PIESSENS




     We show an example semiconcrete execution trace for routine range in Figure 7. Recall
that semiconcrete execution executes each routine separately. Therefore, the above trace is
not an excerpt from a larger program trace; rather, it is a complete trace of the execution
of routine range.
     Execution starts in a state where the store binds each parameter to an arbitrary argu-
ment value and the heap is empty. It then produces the precondition: it adds the resources
and assumes the facts specified by the precondition. When producing a predicate assertion
p(e, ?x), the values of the arguments corresponding to the variable patterns ?x are arbitrary.
In the example, a points-to chunk at the address given by parameter result is added to the
heap.
     The execution of the malloc command and the memory write command are the same
as in the concrete execution.
     The routine call is executed not by inlining a nested execution of the body of the routine,
but by using the contract: the precondition is consumed, and then the postcondition is
produced. Consuming an assertion means removing the heap chunks and checking the facts
specified by the assertion. If a fact specified by the assertion is false, execution fails. The
net effect is that the points-to chunk at address 51 gets some arbitrary value (60 in this
trace) and a list chunk is added whose argument is 60.
     The close command collapses the four chunks representing the linked list into a single
chunk list(50).
     Finally, after execution of the routine body is complete, the postcondition is consumed.
It removes all of the heap chunks and leaves the heap empty.
     Generally, in semiconcrete execution, if the heap is left nonempty after a routine exe-
cution, this indicates a memory leak, since the memory described by the remaining chunks
can no longer be accessed by any subsequent operation in the program execution. Indeed, of
the heap chunks that exist at the end of a routine body execution, only the ones described
by the postcondition become available to the caller; the others can no longer be retrieved in
any way. Therefore, as the final step of a routine execution, semiconcrete execution checks
that the heap is empty; if not, routine execution fails.

3.4. Semiconcrete Execution: Types. The set SCStates of semiconcrete states is de-
fined above; the only difference with the concrete states is that the predicates now in-
clude the user-defined predicates, and consequently the chunks now include the user-defined
chunks.
     To formally define semiconcrete command execution, we will define a function scexec
from commands to mutators, similar to function exec for concrete execution. Additionally,
we define functions consume and produce that formalize what it means to consume and
produce an assertion, respectively.
Definition 3.3. Semiconcrete Execution: Types

                        SCStores = Vars → Z
                     SCPredicates = {7→, mb} ∪ UserDefinedPredicates
                       SCChunks = {p(v) | p ∈ SCPredicates , v ∈ Z}
                        SCHeaps = SCChunks → N
                        SCStates = SCStores × SCHeaps
                      SCMutators = SCStates → Outcomes(SCStates)
                                  FEATHERWEIGHT VERIFAST                                      23




                           scexec  ∈ Commands → SCMutators
                           consume ∈ Assertions → SCMutators
                           produce ∈ Assertions → SCMutators


3.5. Some Auxiliary Definitions. The definition of semiconcrete execution uses the fol-
lowing auxiliary mutators, in addition to the ones used by the definition of concrete ex-
ecution. Semiconcrete consumption consume chunks(h) of a multiset of chunks h fails if
the heap does not contain these chunks, and otherwise removes them from the heap. It is
identical to concrete consumption of chunks. Semiconcrete production produce chunks(h)
of a multiset of chunks h adds the chunks to the heap. It differs from concrete production
in that it does not check that the added chunks do not clash with existing chunks in the
heap. Semiconcrete consumption and production of a single chunk α are defined in the
obvious way. The mutator assert(b) asserting a boolean expression b fails if b, evaluated in
the current store, is false, and otherwise does nothing.
Definition 3.4. Some Auxiliary Definitions
                                                     L ′
                    consume chunks(h′ ) = λ(s, h).      h ≤ h. h(s, h − h′ )i
                      consume chunk(α) = consume chunks({[α]})
                     produce chunks(h′ ) = λ(s, h). h(s, h ⊎ h′ )i
                       produce chunk(α) = produce L  chunks({[α]})
                                assert(b) = λ(s, h).   JbKs = true. h(s, h)i


3.6. Producing Assertions. Production of an assertion is defined as follows.
     Production of a boolean expression means assuming it. Recall from the definition of
assume on Page 14 that assuming a boolean expression is equivalent to a no-op if it evaluates
to true, and equivalent to nontermination if it evaluates to false. The effect is that all final
states generated by production satisfy the expression.
     Production of a predicate assertion means demonically choosing a value for each variable
pattern, binding the pattern variable to it, and adding the specified chunk to the heap.
     Producing a separating conjunction means first producing the left-hand side and then
producing the right-hand side. Notice that the variable bindings introduced by the left-hand
side are active when producing the right-hand side. Notice also that this definition correctly
captures the separating aspect of the separating conjunction: if a chunk is specified by both
the left-hand side and the right-hand side, two occurrences of it end up in the heap.
     Producing a conditional assertion is defined analogously to executing a conditional
statement.
Definition 3.5. Producing Assertions

      produce(b) = assume(b)
                                         N ′
      produce(p(e, ?x)) = v ← eval(e);    v . produce chunk(p(v, v ′ )); x := v ′
      produce(a ∗ a′ ) = produce(a); produce(a′ )
      produce(if b then a else a′ ) = assume(b); produce(a) ⊗ assume(¬b); produce(a′ )
24                          F. VOGELS, B. JACOBS, AND F. PIESSENS




3.7. Consuming Assertions. Consumption of an assertion is defined as follows.
     Consuming a boolean expression is equivalent to a no-op if the expression evaluates to
true under the current store; otherwise, it is equivalent to failure.
     Consuming a predicate assertion fails unless there exists a value for each variable pattern
such that the specified chunk can be consumed. If so, each pattern variable is bound to the
corresponding value.
     Consuming a separating conjunction first consumes the left-hand side and then con-
sumes the right-hand side. Notice that this correctly reflects the separating aspect of the
separating conjunction: if the left-hand side and the right-hand side specify the same chunk,
consumption fails unless the heap contains two occurrences of the chunk, which is generally
impossible.
     Consuming a conditional assertion is defined analogously to executing a conditional
statement.
Definition 3.6. Consuming Assertions

                    consume(b) = assert(b)
                    consume(p(e, ?x))
                                  L=
                      v ← eval(e); v ′ . consume chunk(p(v, v ′ )); x := v ′
                    consume(a ∗ a′ ) = consume(a); consume(a′ )
                    consume(if b then a else a′ ) =
                      assume(b); consume(a) ⊗ assume(¬b); consume(a′ )


3.8. Semiconcrete Execution of Commands. Recall that the concrete execution func-
tion exec is defined in terms of the helper function execn . The latter function is defined by
recursion on n.
     In contrast, the semiconcrete execution function scexec is defined directly, by recursion
on the structure of the command. Doing so for the concrete execution function would not
have been possible, since the execution of a routine call involves the execution of the callee’s
body, which obviously is not part of the structure of the call command itself. However,
since in semiconcrete execution routine call involves only production and consumption of
assertions, this simple approach is possible here.
Definition 3.7. Semiconcrete Execution of Commands See Figures 8 and 9.
      Execution of assignments, sequential compositions, and conditional assertions is the
same as in concrete execution.
      Execution of a routine call r(e) looks up routine r’s precondition a and postcondition
a′ , to be interpreted under a parameter list x, and sets up a store that binds the parameters
to the values of the arguments. In this store, it first consumes the precondition and then
produces the postcondition. Notice that the variable bindings generated during consump-
tion of the precondition are active during production of the postcondition, since the output
store of the consumption operation serves as the input store of the production operation.
      Execution of a while loop is relatively complex. It proceeds as follows:
• The loop invariant is consumed.
• An arbitrary new value is assigned to each variable modified by the loop body.
• Execution chooses demonically between two branches:
                                FEATHERWEIGHT VERIFAST                                   25




         scexec(x := e) = v ← eval(e); x := v

         scexec(c; c′ ) = scexec(c); scexec(c′ )

         scexec(if b then a else a′ ) =
           assume(b); scexec(c) ⊗ assume(¬b); scexec(c′ )

         scexec(while e inv a do c) = See Figure 9

         scexec(r(e)) = v ← eval(e); with(0[x := v], consume(a); produce(a′ ))
           where routine r(x) req a ens a′

         scexec(x
           N        := malloc(n)) =
               ℓ, v1 , . . . , vn ∈ Z.
              produce chunks({[mb(ℓ, n), ℓ 7→ v1 , . . . , ℓ + n − 1 7→ vn ]}); x := ℓ

         scexec(x
           L      := [e]) = ℓ ← eval(e);
              v. consume chunk(ℓ 7→ v); produce chunk(ℓ 7→ v); x := v

         scexec([e]
           L        := e′ ) = ℓ ← eval(e); v ← eval(e′ );
              v0 . consume chunk(ℓ 7→ v0 ); produce chunk(ℓ 7→ v)

         scexec(free(e))
           L              = ℓ ← eval(e);
               N ∈ N, v1 , . . . , vN ∈ Z.
              consume chunks({[mb(ℓ, N ), ℓ 7→ v1 , . . . , ℓ + N − 1 7→ vN ]})

         scexec(open p(e)) = v ← eval(e);
           consume chunk(p(v)); with(0[x := v], produce(a))
           where predicate p(x) = a

         scexec(close p(e)) = v ← eval(e);
           with(0[x := v], consume(a)); produce chunk(p(v))
           where predicate p(x) = a

                   Figure 8: Semiconcrete Execution of Commands

– In the first branch, execution proceeds as follows:
  ∗ The heap is emptied, so that heap chunks not described by the loop invariant are
    not available to the loop body.
  ∗ The loop invariant is produced, but the resulting variable bindings are discarded.
  ∗ It is assumed that the loop condition holds.
  ∗ The loop body is executed.
  ∗ The loop invariant is consumed.
  ∗ A leak check is performed, i.e. execution fails if the heap is not empty; otherwise,
    execution blocks.
26                         F. VOGELS, B. JACOBS, AND F. PIESSENS




                targets(x := e)                  =   {x}
                targets(c1 ; c2 )                =   targets(c1 ) ∪ targets(c2 )
                targets(if b then c1 else c2 )   =   targets(c1 ) ∪ targets(c2 )
                targets(r(e))                    =   ∅
                targets(while b inv a do c0 )    =   targets(c0 )
                targets(x := malloc(n))          =   {x}
                targets(x := [e])                =   {x}
                targets([e] := e′ )              =   ∅
                targets(free(e))                 =   ∅
                                     N
                havoc(x) = λ(s, h). Lv ∈ Z. h(s[x := v], h)i
                leakcheck = λ(s, h).   h = 0. ⊤

                scexec(while b inv a do c) =
                  s ← store; with(s, consume(a));
                  havoc(targets(c));
                  (
                     heap := 0;
                     s ← store; with(s, produce(a));
                     assume(b); scexec(c);
                     s ← store; with(s, consume(a));
                     leakcheck
                  ⊗
                     s ← store; with(s, produce(a));
                     assume(¬b)
                  )

                        Figure 9: Semiconcrete Execution of Loops

  – In the second branch, the loop invariant is produced (but the resulting variable bindings
     are discarded), and it is assumed that the loop condition does not hold.
     The definition uses the auxiliary functions targets, havoc, and leakcheck.
     Function targets maps a command to the set of variables modified by the command.
     Function havoc(x) demonically chooses a value for each variable in x and assigns it to
the corresponding variable.
     Function leakcheck fails if the heap is nonempty, and otherwise blocks, i.e. does not
terminate.
     Semiconcrete execution of memory block allocation, memory read, memory write, and
memory block deallocation are the same as in concrete execution.
     Execution of an open command open p(e) first consumes the chunk whose name is
p and whose arguments are the values of e and then produces the body of predicate p,
the latter in a store that binds the predicate parameters x to the values of the argument
expressions e.
     Conversely, execution of a close command close p(e) first consumes the body of pred-
icate p in a store that binds the predicate parameters x to the values of the argument
                                 FEATHERWEIGHT VERIFAST                                   27




expressions e. Then it produces the chunk whose name is p and whose arguments are the
values of e.

3.9. Validity of Routines. In concrete execution, safety of a program simply means that
execution of the main command starting from an empty state does not fail. In semiconcrete
execution, safety of a program means that two things are true: 1) execution of the main
command starting from the empty state does not fail; and 2) all routines are valid.
     Validity of a routine means that its body satisfies its contract. More specifically, it
means that the routine validity mutator does not fail, when started from an empty state.
The routine validity mutator for a given routine r proceeds as follows: 1) it sets up a store
that binds each of the routine’s parameters to a demonically chosen value; 2) it produces
the routine precondition; 3) it semiconcretely executes the routine body; 4) it consumes the
routine postcondition; 5) it checks for leaks.
Definition 3.8. Validity of Routines

                        valid(r) =
                          (0,
                          N 0) ⊲
                              v.
                          with(0[x := v],
                             s′ ← with(0[x := v], produce(a); store);
                             scexec(c);
                             with(s′ , consume(a′ ))
                          );
                          leakcheck
                          {true}
                          where routine r(x) req a ens a′ = c
    Notice that the postcondition is consumed starting from the store saved after produc-
ing the precondition. This ensures that the variable bindings generated by producing the
precondition are visible when consuming the postcondition.

3.10. Semiconcrete Execution: Program Safety. As stated before, safety of a program
in semiconcrete execution means that execution of the main command succeeds when started
from the empty state, and that all routines are valid.
Definition 3.9. Semiconcrete Execution: Program Safety
               sc-safe program(c)   =    (∀r. valid(r)) ∧ σ0 ⊲ scexec(c) {true}
where r ranges over the declared routines of the program.


3.11. Soundness. Now that we have defined safety of a program in semiconcrete execution,
we discuss its relationship with safety of the program in concrete execution. The intended
relationship is that if a program is safe in semiconcrete execution (i.e. all routines are
valid and the main command does not fail when executed semiconcretely starting from the
empty state), then it is safe in concrete execution (i.e. the main command does not fail when
executed concretely starting from the empty state). We call this property the soundness of
semiconcrete execution. In the remainder of this section, we sketch a proof of this property.
28                                F. VOGELS, B. JACOBS, AND F. PIESSENS




3.11.1. Properties of Assertion Consumption and Production. First, we discuss some prop-
erties of assertion consumption and production. To gain more insight into consumption and
production, we here offer an alternative definition of them, in terms of consumption and
                     a     a
production arrows −  →c , −
                          →p ⊆ SCStates × SCStates, defined inductively using the inference
                          a
rules shown below. σ −   →c σ ′ means that consumption of assertion a starting from state σ
                                                 a
succeeds and results in state σ ′ . Similarly, σ −
                                                 →p σ ′ means that production of assertion a
starting from state σ results in state σ ′ .
Definition 3.10. The Consumption Arrow
                                                                   a                               a′
     JbKs = true              h = {[p(JeKs , v)]} ⊎ h′            →c (s′ , h′ )
                                                           (s, h) −                      (s′ , h′ ) −
                                                                                                    →c (s′′ , h′′ )
         b                       p(e,?x)                                          a∗a′
(s, h) −
       →c (s, h)       (s, h) −−−−→c (s[x := v], h′ )                    (s, h) −−→c (s′′ , h′′ )

                                       a                                                 a′
             JbKs = true              →c (s′ , h′ )
                               (s, h) −                   JbKs = false               →c (s′ , h′ )
                                                                              (s, h) −
                   if b then a else a′                            if b then a else a′
             (s, h) −−−−−−−−−−−−→c (s′ , h′ )             (s, h) −−−−−−−−−−−−→c (s′ , h′ )
Definition 3.11. The Production Arrow
                                                                  a                                a′
     JbKs = true              h′ = {[p(JeKs , v)]} ⊎ h            →p (s′ , h′ )
                                                           (s, h) −                      (s′ , h′ ) −
                                                                                                    →p (s′′ , h′′ )
         b                       p(e,?x)                                          a∗a′
(s, h) −
       →p (s, h)           (s, h) −−−−→p (s[x:=v], h′ )                  (s, h) −−→p (s′′ , h′′ )

                                      a                                                  a′
             JbKs = true              →p (s′ , h′ )
                               (s, h) −                   JbKs = false               →p (s′ , h′ )
                                                                              (s, h) −
                   if b then a else a′                            if b then a else a′
             (s, h) −−−−−−−−−−−−→p (s′ , h′ )             (s, h) −−−−−−−−−−−−→p (s′ , h′ )
    Notice that the only difference between the two definitions is the different positions of
h and h′ in the rule for predicate assertions. Consumption of predicate assertions removes
matching chunks, whereas production adds matching chunks.
    Notice that in both cases, there are generally multiple output states for any given input
state: in both cases, there is a distinct output state for each distinct binding of values to
pattern variables in predicate assertions. However, this is much more common in the case
of production than in the case of consumption, since in the case of consumption multiple
bindings are possible only if the heap contains multiple chunks that match the predicate
assertion.
    Given the consumption and production arrows, we can give an alternative definition of
the consumption and production mutators, as shown below.
Lemma 3.12 (Consumption and Production and the Arrows).
                                       L ′    a
                     consume(a) = λσ.    σ ,σ −
                                              →c σ ′ . hσ ′ i
                                       N ′    a
                      produce(a) = λσ.  σ ,σ −→p σ ′ . hσ ′ i
     Notice that the consumption mutator chooses angelically among the output states, and
fails if there are none; production chooses demonically among the output states, and blocks
if there are none.
     We can easily prove some important properties of the consumption and production
arrows. Firstly, consumption is local: if consumption succeeds, then it also succeeds if more
chunks are available, and those additional chunks remain untouched.
                                  FEATHERWEIGHT VERIFAST                              29




Lemma 3.13 (Consumption Locality).
                              a                              a
                             →c (s′ , h′ ) ⇒ (s, h ⊎ h′′ ) −
                      (s, h) −                             →c (s′ , h′ ⊎ h′′ )
    Secondly, consumption is monotonic: if it succeeds, then the resulting heap is a sub-
multiset of the original heap, and consumption also succeeds if only the consumed chunks
are available, and then it yields the empty heap.
Lemma 3.14 (Consumption Monotonicity).
                        a                                               a
                        →c (s′ , h′ ) ⇒ ∃h′′ . h = h′ ⊎ h′′ ∧ (s, h′′ ) −
                 (s, h) −                                               →c (s′ , 0)
   Thirdly, production is the converse of consumption: production adds back the chunks
removed by consumption.
Lemma 3.15 (Production after Consumption (Arrows)).
                                  a                      a
                                →c (s′ , 0) ⇒ (s, h′′ ) −
                         (s, h) −                       →p (s′ , h′′ ⊎ h)
    All of these properties are proved easily by induction on the assertion.
    From these properties of the consumption and production arrows, we can easily derive
corresponding properties of the consumption and production mutators:
Lemma 3.16 (Consumption and Production (with Post-stores)).
                               s1 ← with(s, consume(a); store);
                               s2 ← with(s, produce(a); store);
                               C(s1 , s2 )
                               ⇛
                               L ′
                                  s . C(s′ , s′ )
Lemma 3.17 (Consumption and Production).
                      with(s, consume(a)); with(s, produce(a)) ⇛ noop
     The first lemma states that consuming an assertion and then producing the same as-
sertion starting from the same store, and then performing some mutator C(−, −) parame-
terized by the output stores of the consumption and production, safely approximates doing
nothing to the heap and angelically picking a store and performing C using this store for
both parameters. The second lemma is a simplified version that ignores the output stores:
consuming an assertion and then producing the same assertion starting from the same store
safely approximates doing nothing.

3.11.2. Locality and Modifies. Two important but simple properties of semiconcrete execu-
tion are that it is local and that it modifies only the command’s targets. Locality means
that execution under some initial heap and then adding more chunks safely approximates
first adding those chunks and then executing.
Definition 3.18. Locality
            local C   ⇔      ∀h. C;, produce chunks(h) ⇛ produce chunks(h); C
Lemma 3.19 (Locality of Semiconcrete Execution).
                                         local scexec(c)
30                           F. VOGELS, B. JACOBS, AND F. PIESSENS




Definition 3.20 (Modifies).
                                    x
                                 s ∼ s′ ⇔ s[x := 0] = s′ [x := 0]

                                                                  x
                                                         M
                            modifiedx (s′ ) = λ(s, h).       s ∼ s′ . noop

                 modifiesx C      ⇔     ∀s. modifiedx (s); C ⇛ C;, modifiedx (s)
Lemma 3.21 (Semiconcrete Execution Modifies Targets).
                                     modifiestargets(c) scexec(c)


3.11.3. Heap Refinement. Having discussed the properties of assertion consumption and
production, we now discuss the relationship between semiconcrete command execution and
concrete command execution. For this purpose, we need to characterize the relationship
between semiconcrete states and concrete states.
     We say that a concrete heap hc refines a semiconcrete heap h, denoted hc ⊳ h, if h can
be obtained from hc by closing some finite number of user-defined predicate chunks. This
is expressed formally using the three inference rules shown below.
Definition 3.22 (Heap refinement).
                                                         a
hc ⊳ h    predicate p(x) = a                       →c (s′ , 0)
                                    (0[x := v], h) −                                 hc ⊳ h      h′c ⊳ h′
                      hc ⊳ {[p(v)]}                                     hc ⊳ hc       hc ⊎ h′c ⊳ h ⊎ h′
     The first rule states that if a concrete heap hc refines a heap h that satisfies the body
a of some predicate p, with no chunks left, when consumed under a store that binds the
predicate parameters x to some argument list v, then it refines the singleton heap containing
just the chunk p(v). The second rule states that any heap refines itself. The third rule states
that heap refinement is compatible with heap union.
     Notice that there are typically many concrete heaps that refine a given semiconcrete
heap. Consider for example the semiconcrete heap {[list(50)]}, where predicate list is defined
as in the example earlier. Any concrete heap that contains exactly a linked list starting at
address 50 refines this semiconcrete heap. There are infinitely many such concrete heaps,
corresponding to different list lengths, different addresses of nodes, and different values
stored in the nodes.
     The following property of heap refinement allows us to fold and unfold predicate defi-
nitions:
Lemma 3.23 (Open, Close).
                                                              a
               hc ⊳ h ⊎ {[p(v)]} ⇔ ∃s′ , h′ . (0[x := v], h′ ) −
                                                               →c (s′ , 0) ∧ hc ⊳ h ⊎ h′
where predicate p(x) = a
                                     FEATHERWEIGHT VERIFAST                                          31




3.11.4. Soundness of Semiconcrete Execution of Commands. Given the refinement relation,
we can define a refinement mutator κ that takes a semiconcrete state as input and outputs
a demonically chosen concrete state such that the output heap refines the input heap.
Definition 3.24. Refinement Mutator
                                  O
                     κ = λ(s, h).   hc ∈ CHeaps, hc ⊳ h. h(s, hc )i
    Given the refinement mutator, we can state the main lemma for the soundness of
semiconcrete execution.
Lemma 3.25 (Soundness of Semiconcrete Execution of Commands). If ∀r. valid(r), then
                                      scexec(c); κ ⇛ κ; exec(c)
Proof. It is sufficient to prove
                                   ∀n, c. scexec(c); κ ⇛ κ; execn (c)
By induction on n. The base case is trivial. Assume ∀c. scexec(c); κ ⇛ κ; execn (c). The
goal is ∀c. scexec(c); κ ⇛ κ; execn+1 (c). By case analysis on c.
     It roughly states that, assuming that all routines are valid, executing a command semi-
concretely starting from some semiconcrete state is worse than executing it concretely start-
ing from a demonically chosen corresponding concrete state.
     The lemma can be proven by induction on the depth of concrete execution and a case
analysis on the command. Most cases are trivial; the nontrivial cases are routine calls, while
loops, and open and close commands. The proofs of the latter cases use the properties of
consumption and production.
     Below, we sketch the proof in some more detail for the cases of routine calls and while
loops.
Proof (Routine Calls). Assume routine definition
                                   routine r(x) req a ens a′ = c
The goal is scexec(r(e)); κ ⇛ κ; cexecn+1 (r(e)). This expands to
  v ← eval(e); with(0[x := v], consume(a); produce(a′ )); κ
                                                     ⇛ κ; v ← eval(e); with(0[x := e], cexecn (c))
We have eval(e);, κ ⇛ κ; eval(e). Furthermore, we have monotonicity of sequential compo-
sition of mutators with respect to coverage. Therefore, it is sufficient to fix values v and
prove
          with(0[x := v], consume(a); produce(a′ )); κ ⇛ κ; with(0[x := v], cexecn (c))
Let s = 0[x := v]. Furthermore, we abbreviate with, consume, produce, scexec, and exec as
w, c, p, sce, and e, respectively. The goal then becomes
                              w(s, c(a); p(a′ )); κ ⇛ κ; w(s, en (c))
    By the induction hypothesis, we have sce(c); κ ⇛ κ; en (c) and therefore w(s, sce(c)); κ ⇛
w(s, en (c)). By transitivity and monotonicity of coverage, it is sufficient to prove
w(s, c(a); p(a′ )) ⇛ w(s, sce(c)).
32                                F. VOGELS, B. JACOBS, AND F. PIESSENS




       By validity of r, we have
              O
     (0, 0) ⊲   v. w(0[x := v], s′ ← w(0[x := v], p(a); store);
                                                                 sce(c); w(s′ , c(a′ ))); leakcheck {true}
We abbreviate w(s, C; store) by ws(s, C). Furthermore, we instantiate the demonic choice
using our fixed v, and we use s = 0[x := v], obtaining
                 (0, 0) ⊲ w(s, s′ ← ws(s, p(a)); sce(c); w(s′ , c(a′ ))); leakcheck {true}
It is easy to see that it follows that for any store s0 and heap h0 , we have (s0 , 0) ⊲ w(s, s′ ←
ws(s, p(a)); sce(c); w(s′ , c(a′ ))); produce(h0 ) {s1 , h1 . s1 = s0 ∧ h1 = h0 }. By locality of
assertion consumption, semiconcrete execution, and assertion production, we can shift
produce(h0 ) to the front, obtaining
           (s0 , h0 ) ⊲ w(s, s′ ← ws(s, p(a)); sce(c); w(s′ , c(a′ ))) {s1 , h1 . s1 = s0 ∧ h1 = h0 }
Hence, noop ⇛ w(s, s′ ← ws(s, p(a)); sce(c); w(s′ , c(a′ )).
    The goal now follows by simple rewriting, using the rewriting lemmas seen above for
consumption followed by production:
                w(s, c(a); p(a′ ))
              ⇛ s1 ←ws(s, c(a)); w(s1 , p(a′ ))
              ⇛ s1 ←ws(s, c(a)); noop; w(s1 , p(a′ ))
              ⇛ s1 ←ws(s, c(a)); w(s, s′ ←ws(s, p(a)); sce(c); w(s′ , c(a′ ))); w(s1 , p(a′ ))
              ⇛ s1 ←ws(s, c(a)); s2 ←ws(s, p(a)); w(s, sce(c)); w(s2 , c(a′ )); w(s1 , p(a′ ))
              ⇛ w(s, sce(c)); w(s′′ , c(a′ )); w(s′′ , p(a′ ))
              ⇛ w(s, sce(c))

Proof (Loops). The goal is
                     sce(while b inv a do c); κ ⇛ κ; en+1 (while b inv a do c)
Expanding the definitions, and further abbreviating modified, havoc, assume, leakcheck,
heap := 0, targets(c), s ← store; with(s, consume(a)), and s ← store; with(s, produce(a)) as
m, h, a, lck, clh, x, cc(a), and pc(a), our goal reduces to
     cc(a); h(x); (clh; pc(a); a(b); sce(c); cc(a); lck ⊗ pc(a); a(¬b)); κ ⇛ κ; (a(b); en (c))∗ ; a(¬b)
Using the property (∀s. mx (s); C ⇛ C ′ ) ⇒ C ⇛ C ′ , and fixing s, it is sufficient to prove
     mx (s); cc(a); h(x); (clh; pc(a); a(b); sce(c); cc(a); lck ⊗ pc(a); a(¬b)); κ
                                                                                 ⇛ κ; (a(b); en (c))∗ ; a(¬b)


We now prove the following lemma.
Lemma 3.26. Assume local C and modifiesx C. We have
                          mx (s); h(x); clh; C; lck ⇛ ⊥      ∨    mx (s); h(x) ⇛ C
Proof. We assume the left-hand disjunct is false and we prove the right-hand disjunct. From
this assumption it follows that there exists an initial state (s0 , h0 ) such that
                                 (s0 , h0 ) ⊲ mx (s); h(x); clh; C; lck {true}
                                    FEATHERWEIGHT VERIFAST                                          33



                    x                      x
It follows that s0 ∼ s and for any s1 ∼ s0 we have (s1 , 0) ⊲ C {s′ , h′ . h′ = 0}. Hence, by
                                                   x
modifiesx C, we have (s1 , 0) ⊲ C {s′ , h′ . s′ ∼ s1 ∧ h′ = 0}. Hence, by local C, we have, for
                                      x
any h1 , (s1 , h1 ) ⊲ C {s′ , h′ . s′ ∼ s1 ∧ h′ = h1 }. From this our goal follows.
    We have modifiesx pc(a); a(b); sce(c); cc(a) and local pc(a); a(b); sce(c); cc(a); applying
the lemma, we obtain
  mx (s); h(x); clh; pc(a); a(b); sce(c); cc(a); lck ⇛ ⊥
                                                      ∨ mx (s); h(x) ⇛ pc(a); a(b); sce(c); cc(a)
We consider both cases. In the first case, the goal follows trivially. In the remainder of the
proof, we assume the second case.
    Using the property C2 ⇛ C3 ⇒ C1 ⊗ C2 ⇛ C3 , we drop the left-hand side of the
demonic choice in our goal. Our goal becomes
                  mx (s); cc(a); h(x); pc(a); a(¬b); κ ⇛ κ; (a(b); en (c))∗ ; a(¬b)
Applying the induction hypothesis, we have (a(b); sce(c))∗ ; a(¬b); κ ⇛ κ; (a(b); en (c))∗ ; a(¬b).
By transitivity of coverage and monotonicity of mutator sequential composition with respect
to coverage, it is sufficient to prove
                            mx (s); cc(a); h(x); pc(a) ⇛ (a(b); sce(c))∗
    Note that to prove C ′ ⇛ C ∗ , it is sufficient to prove C ′ ⇛ noop and C ′ ⇛ C; C ′ .
Applying this rule to the goal, the first subgoal is easy to prove (using the properties of
consumption followed by production). Our remaining goal is
               mx (s); cc(a); h(x); pc(a) ⇛ a(b); sce(c); mx (s); cc(a); h(x); pc(a)
     The goal now follows by simple rewriting, using the rewriting lemmas seen above
for consumption followed by production, as well as the properties mx (s) ⇛ mx (s); mx (s),
h(x) ⇛ h(x); h(x), and modifiesx sce(c):
                          mx (s); cc(a); h(x); pc(a)
                     ⇛    mx (s); cc(a); mx (s0 ); h(x); h(x); pc(a)
                     ⇛    mx (s); cc(a); pc(a); a(b); sce(c); cc(a); h(x); pc(a)
                     ⇛    mx (s); a(b); sce(c); cc(a); h(x); pc(a)
                     ⇛    a(b); sce(c); mx (s); cc(a); h(x); pc(a)


3.12. Soundness of Semiconcrete Execution.
Theorem 3.27 (Soundness of Semiconcrete Execution).
                              sc-safe program(c) ⇒ safe program(c)
     The soundness of semiconcrete execution follows directly from the soundness of semi-
concrete execution of commands. Therefore, we are now halfway on our way towards a
formalization and soundness proof of Featherweight VeriFast. Semiconcrete execution is
not suitable as a verification algorithm since it performs infinite branching. In the next
section, we formalize and sketch a soundness proof of Featherweight VeriFast’s symbolic
execution algorithm, which builds on semiconcrete execution but introduces symbols to
eliminate infinite branching.
34                                F. VOGELS, B. JACOBS, AND F. PIESSENS




        routine range(i, n, r)
            req r 7→ ?dummy ens r 7→ ?list ∗ list(list)
        Φ:{i ,n,r}, s:0[i:i, n:n, r:r ], h:0                Φ:{. . . , ς, . . . } = Φ:{. . . , ς = ς, . . . }
        sproduce(r 7→ ?dummy)
        Φ:{i ,n,r ,d}, s:0[i:i , n:n, r:r ], h:{[r 7→d]}
        if i = n then l := 0 else (
        Φ:{i ,n,r ,d, i 6=n}, s:0[i:i , n:n, r:r ], h:{[r 7→d]}
        l := malloc(2);
        Φ:{i ,n,r ,d,l,v ,v ′ , i 6=n,0<l }, s:0[i:i , n:n, r:r , l:l ], h:{[r 7→d,mb(l, 2),l7→v ,l +17→v ′ ]}
        [l] := i; range(i + 1, n, l + 1)
        sconsume(l+17→?dummy); sproduce(l+17→?list ∗ list(list))
        Φ:{i ,n,r ,d,l ,v ,v ′ ,l ′ , i 6=n,0<l }, s:0[i:i , n:n, r:r , l:l ],
        h:{[r 7→d,mb(l , 2),l 7→i ,l +17→l ′ ,list(l ′ )]}
        ); close list(l); [r] := l
        Φ:{i ,n,r ,d,l ,v ,v ′ ,l ′ , i 6=n,0<l }, s:0[i:i , n:n, r:r , l:l ], h:{[r 7→l ,list(l )]}
        sconsume(r 7→ ?list ∗ list(list))
        Φ:{i ,n,r ,d,l ,v ,v ′ ,l ′ , i 6=n,0<l }, s:0[i:i , n:n, r:r , l:l ], h:0

                          Figure 10: Symbolic Execution: Example Trace

                                         4. Symbolic Execution
In this section, we introduce symbolic execution by example, and then provide formal
definitions. Finally, we sketch a soundness proof.

4.1. Symbolic Execution: Example Trace. Recall the example semiconcrete execution
trace for the example routine range in Figure 7. Notice that while the length of this trace
is linear in the size of the body of routine range, there are infinitely many such traces, since
each number shown in orange is picked by demonic choice among all integers (potentially
with some constraints).
      We introduce symbolic execution to arrive at an execution with a finite number of traces
of limited length. Instead of demonically choosing among an infinite set of integers, symbolic
execution uses a fresh symbol to represent an arbitrary number. Symbolic execution states
are like semiconcrete execution states, except that a term may be used instead of a literal
value in the store and the heap. A term is either a literal number, a symbol, or an operation
(addition or subtraction) applied to two terms. In addition to replacing numbers by terms,
symbolic execution adds a third component to the state: the path condition. This is a set
of formulae that define the set of relevant interpretations of the symbols used in the store
and the heap. A formula is either an equality between terms (t = t′ ), an inequality between
terms (t < t′ ), or the negation of another formula.
Example 4.1. Symbolic Execution: Example Trace See Figure 10
      In Figure 10 we show the symbolic execution trace for routine range corresponding to
the semiconcrete execution trace shown before. Note: do not confuse the program variables
and the symbols. The former are shown in an upright font; the latter are shown in a slanted
font. In the symbolic execution trace, the letters shown in orange do not denote branching
(i.e. demonic choices); rather, they show freshly picked symbols.
                                  FEATHERWEIGHT VERIFAST                                   35




    Besides the use of symbols, notice the path condition Φ: it starts out empty; in the else
branch of the if statement, the formula i 6= n is added; and the malloc statement adds the
formula 0 < l .

4.2. Symbolic Execution: Types. The set SStates of symbolic execution states is defined
below. Terms are like expressions, except that they may mention symbols, which represent
a fixed value, instead of program variables, whose value may change through assignments.
Similarly, formulae correspond to boolean expressions.
     Symbolic states are like semiconcrete states, except that terms are used instead of
values in the store and as chunk arguments; furthermore, the state includes an additional
component, called the path condition, which is a set of formulae.
Definition 4.2. Symbolic Execution: Types
                                       ς ∈ Symbols
                     t, ℓ̂, v̂ ∈ Terms ::= z | ς | t + t | t − t
                      ϕ ∈ Formulae ::= t = t | t < t | ¬ϕ

                     ŝ ∈ SStores =    Vars → Terms
                     SPredicates =     {7→, mb} ∪ UserDefinedPredicates
                         SChunks =     {p(v̂) | p ∈ SPredicates, v̂ ∈ Terms}
                     ĥ ∈ SHeaps =     SChunks → N
                 PathConditions =      P(Formulae )
                          SStates =    PathConditions × SStores × SHeaps
                       SMutators =     SStates → Outcomes(SStates)

                     sconsume(a) ∈ Assertions → SMutators
                      sproduce (a) ∈ Assertions → SMutators
                       symexec(c) ∈ Commands → SMutators


4.3. Symbolic Execution: Auxiliary Definitions. As we did for concrete execution and
semiconcrete execution, we introduce a few auxiliary definitions for use in the definition of
symbolic execution. They are as follows.
     In concrete and semiconcrete execution, assuming a boolean expression evaluates the
expression in the current store and blocks if it evaluates to false. In symbolic execution,
this is not possible, since evaluation of a boolean expression under a symbolic store yields a
formula rather than a boolean value. Symbolic execution, therefore, asks an SMT solver, a
type of automatic theorem prover, to try to prove that the formula is inconsistent with the
path condition. If it succeeds, symbolic execution blocks. Otherwise, the formula is added
to the path condition, in order to record that on the remainder of the current symbolic
execution path, of all possible interpretations of the symbols used in the symbolic state,
only the ones that satisfy the formula are relevant.
     We write Φ ⊢SMT ϕ to denote that the SMT solver succeeds in proving that the set of
formulae Φ implies the formula ϕ.
     Similarly, asserting a boolean expression in symbolic execution means evaluating it to
a formula under the current symbolic store and asking the SMT solver to try to prove that
36                               F. VOGELS, B. JACOBS, AND F. PIESSENS




the formula follows from the path condition. If it succeeds, execution proceeds normally;
otherwise, it fails.
      The set Used(Φ) denotes the set of symbols ς for which a formula ς = ς appears in the
path condition Φ. In a well-formed symbolic state, all symbols used in the symbolic state
are in this set.
      fresh(Φ) denotes some symbol that is not in Used(Φ). It is defined using a choice
function ǫ, which maps each nonempty set to some element of that set.
      The mutator fresh picks some symbol ς that is not yet used by the current symbolic
state, records that it is now being used by adding a formula ς = ς to the path condition,
and yields the symbol as its L  answer.
      We define the notation      t. C(t), where C is a mutator parameterized by a term, to
denote angelic choice over all terms that only use symbols that are already being used by
the current symbolic state. FS(t) denotes the set of free symbols that appear in term t,
i.e. the set of symbols used by t.8
      Symbolic consumption sconsume chunks(ĥ) of a multiset ĥ of symbolic terms differs
from concrete and semiconcrete consumption in that it does not simply look for the exact
chunks ĥ in the current heap; rather, it looks for chunks for which the SMT solver succeeds
in proving that their argument terms are equal under all relevant interpretations of the
symbols. For example, suppose the heap contains a chunk list(l ) and the path condition
contains a formula l = l ′ ; then consumption of a chunk list(l ′ ) succeeds, even though the
exact chunk list(l ′ ) does not appear in the symbolic heap. Symbolic production is simpler;
as in semiconcrete execution, it simply adds the specified chunks to the heap. Symbolic
consumption and production of a single symbolic chunk α̂ are defined in the obvious way.
Definition 4.3. Symbolic Execution: Auxiliary Definitions
                                       N
          sassume(ϕ) = λ(Φ, ŝ, ĥ).      Φ 6⊢SMT ¬ϕ. h(Φ ∪ {ϕ}, ŝ, ĥ)i
          sassume(b) = ŝ ← sstore; sassume(JbKŝ )
                                     L
          sassert(b) = λ(Φ, ŝ, ĥ).    Φ ⊢SMT JbKŝ . h(Φ, ŝ, ĥ)i
          Used(Φ) = {ς ∈ Symbols | (ς = ς) ∈ Φ}
          fresh(Φ) = ǫ({ς ∈ Symbols | ς ∈    / Used(Φ)})
          fresh = λ(Φ, ŝ, ĥ). let ς = fresh(Φ) in h(Φ ∪ {ς = ς}, ŝ, ĥ), ςi
          L                     L
             t. C(t) = Φ ← pc; t ∈ Terms, FS(t) ⊆ Used(Φ). C(t)
                                                 N ′′
          sconsume chunks(ĥ′ ) = λ(Φ, ŝ, ĥ).     ĥ ≤ ĥ, Φ ⊢SMT ĥ′′ = ĥ′ . h(Φ, ŝ, ĥ − ĥ′′ )i
          sconsume chunk(α̂) = sconsume chunks({[α̂]})
          sproduce chunks(ĥ′ ) = λ(Φ, ŝ, ĥ). h(Φ, ŝ, ĥ ⊎ ĥ′ )i
          sproduce chunk(α̂) = sproduce chunks({[α̂]})

          where
           ǫ(X)       =    some element of X


     8Since the syntax of terms does not include any binding constructs, all symbols that appear in a term
are free symbols of the term.
                                  FEATHERWEIGHT VERIFAST                                 37




4.4. Symbolic Execution: Definition. The definition of symbolic execution is entirely
analogous to that of semiconcrete execution, except that symbolic versions of the auxiliary
mutators are used and that each demonic choice over all values is replaced by picking a
fresh symbol.
Definition 4.4. Producing Assertions

                sproduce(b) = sassume(b)
                sproduce(p(e, ?x)) =
                                   ′                                ′            ′
                  v̂ ← seval(e); v̂ ← fresh; sproduce chunk(p(v̂, v̂ )); x := v̂
                sproduce(a ∗ a′ ) = sproduce(a); sproduce(a′ )
                sproduce(if b then a else a′ ) =
                  sassume(b); sproduce(a) ⊗ sassume(¬b); sproduce(a′ )
Definition 4.5. Consuming Assertions

                  sconsume(b) = sassert(b)
                  sconsume(p(e, ?x)) =
                                  L ′                          ′            ′
                    v̂ ← seval(e); v̂ . sconsume chunk(p(v̂, v̂ )); x := v̂
                  sconsume(a ∗ a′ ) = sconsume(a); sconsume(a′ )
                  sconsume(if b then a else a′ ) =
                    sassume(b); sconsume(a) ⊗ sassume(¬b); sconsume(a′ )

Definition 4.6. Symbolic Execution of Commands See Figures 11 and 12.
Definition 4.7. Validity of Routines

                       svalid(r) =
                         (∅, 0, 0) ⊲
                         v̂ ← fresh;
                         with(0[x := v̂],
                            ŝ′ ← with(0[x := v̂], sproduce(a); sstore);
                            symexec(c);
                            with(ŝ′ , sconsume(a′ ))
                         );
                         sleakcheck
                         {true}
                         where routine r(x) req a ens a′ = c
Definition 4.8. Symbolic Execution: Program Safety

         sym-safe program(c)      =    (∀r. svalid(r)) ∧ (∅, 0, 0) ⊲ symexec(c) {true}
38                             F. VOGELS, B. JACOBS, AND F. PIESSENS




       symexec(x := e) = v̂ ← seval(e); x := v̂

       symexec(c; c′ ) = symexec(c); symexec(c′ )

       symexec(if b then a else a′ ) =
         sassume(b); symexec(c) ⊗ sassume(¬b); symexec(c′ )

       symexec(while e inv a do c) = See Figure 12

       symexec(r(e)) =
         v̂ ← eval(e); with(0[x := v̂], sconsume(a); sproduce(a′ ))
         where routine r(x) req a ens a′

       symexec(x := malloc(n)) =
         ℓ̂, v̂1 , . . . , v̂n ← fresh; sassume(0 < ℓ̂);
         sproduce chunks({[mb(ℓ̂, n), ℓ̂ 7→ v̂1 , . . . , ℓ̂ + n − 1 7→ v̂n ]}); x := ℓ̂

       symexec(x := [e]) =
                       L
         ℓ̂ ← seval(e); v̂. sconsume chunk(ℓ̂ 7→ v̂); sproduce chunk(ℓ̂ 7→ v̂); x := v̂

       symexec([e] := e′ ) =
                                L
         ℓ̂, v̂ ← seval(e, e′ ); v̂ ′ . sconsume chunk(ℓ̂ 7→ v̂ ′ ); sproduce chunk(ℓ̂ 7→ v̂)

       symexec(free(e)) = ℓ̂ ← seval(e);
         L
           n, v̂1 , . . . , v̂n . sconsume chunks({[mb(ℓ̂, n), ℓ̂1 7→ v̂1 , . . . , ℓ̂n 7→ v̂n ]})

       symexec(open p(e)) = v̂ ← eval(e);
         sconsume chunk(p(v̂)); with(0[x := v̂], sproduce(a))
         where predicate p(x) = a

       symexec(close p(e)) = v̂ ← eval(e);
         with(0[x := v̂], sconsume(a)); sproduce chunk(p(v̂))
         where predicate p(x) = a

                          Figure 11: Symbolic Execution of Commands

4.5. Soundness. We now argue the soundness of symbolic execution with respect to semi-
concrete execution, i.e. that symbolic execution is a safe approximation of semiconcrete
execution, and therefore if symbolic execution does not fail, then semiconcrete execution
does not fail. To do so, we need to characterize the relationship between symbolic states
and semiconcrete states. We do so by means of the concept of an interpretation.
Definition 4.9. Soundness of symbolic execution: Definitions
                                   FEATHERWEIGHT VERIFAST                                       39




                             shavoc(x) = v̂ ← fresh; x := v̂
                                                        L
                             sleakcheck = λ(Φ, ŝ, ĥ).   ĥ = 0. ⊤

                             symexec(while b inv a do c) =
                               ŝ ← sstore; with(ŝ, sconsume(a));
                               shavoc(targets(c));
                               (
                                  sheap := 0;
                                  ŝ ← sstore; with(ŝ, sproduce(a));
                                  sassume(b); symexec(c);
                                  ŝ ← sstore; with(ŝ, sconsume(a));
                                  sleakcheck
                               ⊗
                                  ŝ ← sstore; with(ŝ, sproduce(a))
                                  sassume(¬b);
                               )

                           Figure 12: Symbolic Execution of Loops



           I ∈ Interps = Symbols ⇀ Z = Symbols → Z ∪ {undef}
                 dom I = {ς | I(ς) 6= undef}
                I ⊆ I′ =    ∀ς. I(ς) = undef ∨ I(ς) = I ′ (ς)
                                (s, h) if dom I = Used(Φ) ∧ JΦ, ŝ, ĥKI = true, s, h
            I((Φ, ŝ, ĥ)) =
                                  N ′ otherwise
                                undef
                       ρI = λσ̂.     I ⊇ I, σ, I ′ (σ̂) = σ. hσi
              C I C = C;, ρI ⇛ ρI ; C ′
                         ′

        C(−) I C ′ (−) = ∀I ′ ⊇ I, t, v, JtKI ′ = v. C(t) I ′ C ′ (v)
An interpretation is a partial function from symbols to program values. By partial function,
we mean that it maps each symbol either to a program value (an integer) or to the special
value undef. By this, we reflect that at each point during symbolic execution, only some of
the symbols are in use and the others may be picked by a future execution of mutator fresh.
     We say an interpretation I ′ extends another interpretation I, denoted I ′ ⊇ I, if for each
symbol for which I is defined, I ′ is defined and I ′ maps it to the same value as I.
     We define the evaluation J−KI of a term, a formula, a path condition, a symbolic store,
or a symbolic heap under an interpretation I as the partial function that yields undef if the
interpretation yields undef for any of the symbols that appear in the input, and the output
obtained by replacing all symbols by their value otherwise.
     We also use an interpretation as a partial function from symbolic states to semiconcrete
states, as follows. For an interpretation I and a symbolic state (Φ, ŝ, ĥ), if the domain of I is
exactly Used(Φ), and Φ evaluates to true under I, and the symbolic store and heap ŝ and ĥ
evaluate to a semiconcrete store and heap s and h under I, then the value of (Φ, ŝ, ĥ) under
I is (s, h), and otherwise it is undefined. Notice that this means that the interpretation of
a symbolic state is undefined if the symbolic state is not well-formed, i.e. if it uses symbols
ς for which no formula ς = ς appears in the path condition.
40                           F. VOGELS, B. JACOBS, AND F. PIESSENS




      We now define the interpretation mutator ρI that, for a given symbolic state σ̂, de-
monically chooses an extension I ′ of I for which I ′ (σ̂) is defined and sets the resulting
semiconcrete state as the current state.
      Given this mutator, we define the concept of safe approximation C I C ′ of a semicon-
crete mutator C ′ by a symbolic mutator C under an interpretation I. This holds if C;, ρI
covers ρI ; C ′ .
      We extend this notion to the case of a symbolic operator C(−) parameterized by a term
and a semiconcrete operator C ′ (−) parameterized by a value. It holds if for any extension
I ′ of I, and for any term whose value is defined under I ′ , C(t) safely approximates C ′ (JtKI ′ )
under I ′ .
Definition 4.10. Logical Consequence
                         Φϕ       ⇔     ∀I. JΦKI = true ⇒ JϕKI = true
Assumption 4.11 (SMT Solver Soundness).
                                    Φ ⊢SMT ϕ      ⇒     Φϕ

Soundness of symbolic execution relies on one assumption: that the SMT solver is sound.
That is, if the SMT solver reports success in proving that a formula follows from a path
condition, then it must be the case that this formula does indeed follow from this path
condition. We say a formula follows from a path condition if all interpretations that satisfy
the path condition satisfy the formula.
      It is not necessary for soundness of symbolic execution that the SMT solver be complete,
i.e. that it succeed in proving all true facts. In fact, symbolic execution is sound even when
using an SMT solver that does not even try and always reports failure to prove a fact.
However, in that case symbolic execution itself is highly incomplete, i.e. it fails even if
concrete execution does not fail. Indeed, we do not claim completeness of Featherweight
VeriFast.
      Given these concepts, we can state the soundness lemmas of symbolic execution:
Lemma 4.12 (Soundness).
                                                        N
                 C(−) I C ′ (−) ⇒ v̂ ← fresh;
                                          L     C(v̂) I L v. C ′ (v)
                      C(−) I C ′ (−) ⇒      v̂. C(v̂) I   v. C ′ (v)
                              sassume(b), sassert(b) I assume(b), assert(b)
              JĥKI = h ⇒ sconsume(ĥ), sproduce(ĥ) I consume(h), produce(h)
                          sconsume(a), sproduce(a) I consume(a), produce(a)
                                         symexec(c) I scexec(c)
                                           svalid(r) ⇒ valid(r)
                               sym-safe program(c) ⇒ sc-safe program(c)

Mutator fresh safely approximates demonic choice of a value; angelic choice of a term that
uses only symbols already being used by the current symbolic state safely approximates
angelic choice of a value; symbolic assumption and assertion safely approximate semicon-
crete assumption and assertion; symbolic consumption and production of heap chunks safely
approximate semiconcrete consumption and production of their interpretations; and sym-
bolic execution safely approximates semiconcrete execution. The soundness theorem follows
directly.
                                    FEATHERWEIGHT VERIFAST                                       41




     Proving the properties stated above is mostly easy; below we go into some detail of two
of the more interesting proofs: soundness of fresh and soundness of sassume.
Lemma 4.13 (Soundness of fresh).
                                                                       O
                                  ′
                      C(−)     I C (−) ⇒ v̂ ← fresh; C(v̂)         I         v. C ′ (v)
Proof. We assume the premise and we unfold the definition of safe approximation, of mu-
tator coverage, and of outcome coverage. Fix an input symbolic state (Φ, ŝ, ĥ) and a
postcondition Q. Unfold the definition of fresh. Let ς be the fresh symbol.          N        Assume
(Φ ∪ {ς = ς}, ŝ, ĥ) ⊲ C(ς); ρI {Q}. It is sufficient to prove (Φ, ŝ, ĥ) ⊲ ρI ; v. C ′ (v) {Q}.
Unfolding the definition of ρI in the goal, fix an interpretation I ′ ⊇ I and a semiconcrete
state (s, h) such that I ′ ((Φ, ŝ, ĥ)) = (s, h). Further fix a value v picked by the demonic
choice in the goal. It is sufficient to prove that (s, h) ⊲ C ′ (v) {Q}. We build a new inter-
pretation I ′′ by binding the fresh symbol ς to value v: I ′′ = I ′ [ς := v]. It follows that
I ′′ ((Φ ∪ {ς = ς), ŝ, ĥ)) = (s, h). Using I ′′ , we can rewrite our goal into the following form:
                               (Φ ∪ {ς = ς}, ŝ, ĥ) ⊲ ρI ′′ ; C ′ (v) {Q}
The goal now matches the consequent of our premise C(−) I C ′ (−) after unfolding the
definition of safe approximation, mutator coverage, and outcome coverage. Finally, the
antecedent matches our assumption.
Lemma 4.14 (Soundness of sassume).
                                    sassume(b)       I assume(b)

Proof. Unfold the definition of safe approximation, mutator coverage, outcome coverage,
and ρI . Fix an input symbolic state (Φ, ŝ, ĥ), a postcondition Q, an extension I ′ ⊇ I, and
a semiconcrete state (s, h) such that I ′ ((Φ, ŝ, ĥ)) = (s, h). Unfold the definition of sassume.
Assume Φ 6⊢SMT ¬JbKŝ ⇒ (Φ∪{JbKŝ }, ŝ, ĥ)⊲ρI {Q}. Unfold the definition of assume. Assume
JbKs = true. Our goal reduces to (s, h) ∈ Q.
      Since JΦKI ′ = true and JJbKŝ KI ′ = true, we have Φ 6 ¬JbKŝ . By soundness of the SMT
solver, it follows that Φ 6⊢SMT ¬JbKŝ . Hence, by our assumption above, (Φ ∪ {JbKŝ }, ŝ, ĥ) ⊲
ρI {Q}. In this fact, we unfold ρI and instantiate the demonic choice with I ′ . Since
I ′ ((Φ ∪ {JbKŝ }, ŝ, ĥ)) = (s, h), we obtain (s, h) ∈ Q.
Theorem 4.15 (Soundness of Featherweight VeriFast).
                             sym-safe program(c) ⇒ safe program(c)

Combining the soundness of symbolic execution with respect to semiconcrete execution and
the soundness of semiconcrete execution with respect to concrete execution, we obtain the
soundness of Featherweight VeriFast: if symbolic execution does not fail, then concrete
execution does not fail.

                                       5. Mechanisation
Above we presented a formal definition of Featherweight VeriFast and we gave the highlights
of a proof of its soundness. We hope that the definitions are clear and the proof outline
is convincing. However, the definition, while formal (in the sense of: consisting of symbols
rather than natural language), is written in the general language of mathematics and not
42                         F. VOGELS, B. JACOBS, AND F. PIESSENS




in any particular explicitly defined formal logic, with a well-defined formal language of
formulae and a well-defined formal language of proofs that specifies which formulae are
logically true. Therefore, the precise meaning of the definition might not be clear to all
readers. A fortiori, the soundness proof is not expressed in such a formal language of proofs,
and therefore, there is always the possibility that some of the inferences made are invalid
and the conclusion is false; i.e., it is not an argument that will necessarily convince all
readers.
     To address these limitations, we developed a definition and soundness proof of a slight
variant of Featherweight VeriFast, called Mechanised Featherweight VeriFast, in the machine-
readable formal language of the interactive proof assistant Coq. Coq is a computer program
that takes as input a set of files containing definitions and proofs expressed in its formal
language, and checks that these definitions and proofs are indeed well-formed. Since we
have successfully checked our development with Coq, we can have very high confidence that
the theorems that we have proven are indeed true, with respect to the given definitions.
     Note that it is still possible that Mechanised Featherweight VeriFast contains errors:
it might still be the case that the stated definitions and theorems are not the ones that
we intended; for example, if we made an error in the definition of the concrete execution
such that concrete execution always blocks, or we made an error in the definition of the
symbolic execution such that symbolic execution always fails, then the soundness theorem
holds vacuously and does not really tell us anything meaningful. We partially address this
issue by including a small test suite in our development, where we run the concrete execution
and the symbolic execution on specific example programs, and test that concrete execution
does indeed sometimes fail as expected, and that symbolic execution does indeed sometimes
succeed as expected. Still, we should remain skeptical, and confidence in the relevance of
a formally proven statement can never be 100%. It can be improved further by enlarging
the test suite and/or by proving additional properties of the various executions, e.g. by
relating MFVF’s concrete execution to another programming language semantics found in
the literature.
     While MFVF follows FVF very closely in most respects, there are a few differences,
mainly motivated by the fact that we wanted MFVF to be executable so as to be able to
test it easily, whereas for FVF simplicity is more important. Also, MFVF has a few minor
additional features, which were left out of FVF, again for the sake of simplicity.
     In the remainder of this section, we briefly discuss the main differences between MFVF
and FVF and the executability of MFVF, we show the soundness theorem, and we point
the reader to the full Coq sources which are available online.

5.1. Differences between MFVF and FVF: Syntax. In Figure 13 we show the syntax
of the programming language and the annotations accepted by MFVF. The differences with
FVF are shown in red; as the reader can see, they are very minor.
     The main difference is that MFVF supports routine return values; when executing a
routine call x := r(e), after execution of the routine body ends, the value assigned by the
routine body to variable result is assigned to variable x of the caller.
     A minor difference is in the syntax of open commands: MFVF allows the command to
leave some of the chunk arguments unspecified. The command open q(e, ? ) opens some
chunk that matches the pattern q(e, ? ).
                                   FEATHERWEIGHT VERIFAST                                       43




                          z ∈ Z, n ∈ N
                          x ∈ Vars
                  e ::=   z | x | e+e
                  b ::=   e = e | e < e | ¬b
                  c ::=   x := e | (c; c) | if b then c else c | skip | message text
                          | x := r(e) | x := malloc(n) | x := [e] | [e] := e | free(e)
                          | while b inv a do c | open q(e, ? ) | close q(e)
              rdef ::=    routine r(x) = c

                            q ∈ UserDefinedPredicates
                 p ::=    7 →   | mb | q
                 a ::=    b | p(e, ?x) | a ∗ a | if b then a else a
           preddef ::=      predicate q(x) = a
             rspec ::=    routine r(x) req a ens a

        Figure 13: Syntax of Mechanised Featherweight VeriFast’s input language

    Two new commands are added. The skip command does nothing; it is equivalent to
x := x. The command message text prints message text to the console. This command is
useful in MFVF for testing the executions.

5.2. Differences between MFVF and FVF: Executions. The main difference between
the executions (concrete execution, semiconcrete execution, and symbolic execution) of
MFVF and those of FVF is in the definition and use of the auxiliary mutators for the con-
sumption of heap chunks (cconsume chunks(h), consume chunks(h), and sconsume chunks(ĥ)
in FVF). In FVF, these mutators take as an argument the precise multiset of heap chunks
(up to provable equality for symbolic execution) to be consumed. However, at a typical use
site, only part of the argument list of a chunk is fixed, and the remaining arguments are to
be looked up in the heap. In FVF, this is achieved by angelically choosing these remaining
arguments.
     For example, consider symbolic execution of a heap lookup command:
       FVF:
       symexec(x := [e]) =
                       L
         ℓ̂ ← seval(e); v̂. sconsume chunk(ℓ̂ 7→ v̂); sproduce chunk(ℓ̂ 7→ v̂); x := v̂
       sconsume chunk ∈ SHeaps → SOutcomes(unit)

       MFVF:
       symexec(x := [e]) =
         ℓ̂ ← seval(e); [v̂] ← sconsume chunk(7→, [ℓ̂], 1); sproduce chunk(ℓ̂ 7→ v̂); x := v̂
       sconsume chunk ∈ SPredicates → Terms ∗ → N → SOutcomes(Terms ∗ )

In FVF, symbolic execution of a command of the form x := [e] that reads the memory cell
at address e evaluates e to obtain term ℓ̂, then angelically chooses some term v̂, and then
attempts to consume the points-to chunk that maps address ℓ̂ to this angelically chosen
term v̂. This consumption operation succeeds if a points-to chunk exists in the symbolic
44                           F. VOGELS, B. JACOBS, AND F. PIESSENS




heap such that the SMT solver succeeds in proving that its arguments are equal to ℓ̂ and v̂,
respectively.
     This definition is perfectly fine, except that angelically choosing a term from the set
of all terms (that use only symbols that are already being used by the current symbolic
state) is not directly executable, since that set is infinite, and even if it was finite, it would
be highly inefficient. Therefore, in MFVF, a slightly more complex but directly executable
version of the chunk consumption mutators is used. These mutators consume only a single
chunk at a time, and they take as arguments the predicate name, the list of fixed chunk
arguments, and the number of non-fixed chunk arguments; they return the values of the
non-fixed arguments of the chunk that was consumed as their answer. Correspondingly, in
MFVF, symbolic execution of x := [e], rather than angelically choosing a term for the value
of the cell, retrieves that term as the answer of the sconsume chunk auxiliary mutator.

5.3. Executability. This concludes the discussion of the differences between MFVF and
FVF. We now discuss some specific encoding choices made when defining MFVF to obtain
executable definitions of symbolic execution and concrete execution.
     The most important such choice is in the definition of the type of outcomes. The
definition of inductive type outcome in MFVF is shown below.

          Inductive type name := n Empty set | n bool | n Z | n T(T : Type).

          Fixpoint Itype name(n : type name) : Type := match n with
            | n Empty set ⇒ Empty set
            | n bool ⇒ bool
            |nZ⇒Z
            |nTT ⇒T
            end.

          Inductive set(X : Type) := set (n : type name)(f : Itype name n → X).

          Inductive outcome(S A : Type) :=
          | single(s : S)(a : A)
          | demonic(os : set (outcome S A))
          | angelic(os : set (outcome S A))
          | message(msg : string)(o : outcome S A).

It corresponds exactly to the definition of outcomes given earlier for FVF (except for the
extra case of messages): an outcome φ is                          L hσ, ai with output state
                                          Neither a singleton outcome
σ and answer a, or a demonic choice         Φ or angelic choice      Φ over a set of outcomes
Φ. However, there are two interesting aspects about this definition, and more specifically,
about the type set used for the sets of outcomes.
     First of all, we had to choose this type carefully to obtain a proper inductive definition.
The simplest approach for defining a type for sets of elements of some type X is as follows:
                               Definition set X := X → Prop.
That is, a set of elements of type X is simply a predicate over type X. However, using
this definition of sets in the definition of outcomes would cause Coq to reject the definition
                                  FEATHERWEIGHT VERIFAST                                       45




of outcomes, since it would not be a proper inductive definition. Indeed, it would allow
us to write demonic (λ . True), denoting the demonic choice over all outcomes, including
demonic (λ .True) itself, defeating the crucial notion that each value of an inductive type is
built from smaller values of that type, and thus rendering proof by induction unsound.
    Perhaps the simplest possible definition for a type of sets of elements of type X that is
compatible with inductive definitions is the following:
                   Inductive set(X : Type) := set (I : Type)(f : I → X).
This type allows a set to be constructed by providing an index type I and a function f that
maps each value of type I to some value of type X. For example, the set containing exactly
the integers 24 and 42 can be constructed as follows:
                               set bool (λb. if b then 24 else 42)
Using this type of sets in the definition of outcomes would be accepted by Coq.
     However, another problem would still remain: we would like to write a Coq function
that takes the outcome of symbolically executing some program starting from the empty
symbolic state, and decides if that outcome satisfies postcondition True, i.e., if symbolic
execution has failed or not. An outcome satisfies postcondition True iff the outcome is
a singleton outcome, or it is a demonic choice over some set of outcomes, each of which
satisfies postcondition True, or it is an angelic choice over some set of outcomes, at least
one of which satisfies postcondition True (or it is a message outcome and its continuation
satisfies postcondition True). So, for demonic and angelic choice over some set of outcomes,
we need to be able to enumerate the elements of the set. Given the definition of sets above, it
would be necessary to enumerate the elements of the index type I. Unfortunately, however,
this is not generally possible: the index type might be infinite.
     However, MFVF’s definition of symbolic execution uses only very restricted forms of
demonic or angelic choice: it only uses blocking, failure, and binary choice, i.e., choices over
zero elements or two elements. So, if in symbolic execution we use as index types only the
type Empty set and the type bool, can we write our Coq function? Unfortunately, still no,
because this would require our function to perform a case analysis on a comparison between
the index type of a set and the types Empty set or bool, and Coq’s execution engine does not
support this. Coq’s execution engine supports only pattern matching on values of inductive
types, and types themselves are not values of inductive types.
     The solution we adopted for this problem is to not directly allow arbitrary types to be
specified as the index type when constructing a set, but rather to define an inductive type
type name of type names, with names for type Empty set, for type bool, and for the type
Z of integers, and a fallback case n T for arbitrary types. We also defined an interpretation
function Itype name for these type names that maps each type name to its corresponding
type. By using type names and the interpretation function in the definition of sets, we were
able to write a Coq function that decides whether an outcome satisfies postcondition True.
(For the cases n Z and n T this function is not executable, but since symbolic execution
uses only the other two cases, it executes properly for the outcomes of symbolic execution.)
     Figure 14 shows an example where we run symbolic execution to check validity of a
routine that performs in-place reversal of a linked list. Function svalid routine (the syntax
of the example is slightly simplified from the actual Coq development) takes as arguments a
list of predicate definitions (in the example, just the definition listDef of the list predicate),
a list of routine specifications (in the example, an empty list, since the list reversal routine
46                            F. VOGELS, B. JACOBS, AND F. PIESSENS




          Definition listDef :=
            predicate list(l) =
              if l = 0 then 0 = 0 else mb(l, 2) ∗ l 7→ ∗ l + 1 7→ ?next ∗ list(next).

          Compute svalid routine [listDef] [] [l] list(l) list(result)
            (
               close list(b);
               while ¬(a = 0) inv list(a) ∗ list(b) do (
                  open list(a);
                  n := [a + 1]; [a + 1] := b; b := a; a := t;
                  close list(b)
               );
               open list(a);
               result := b
            ).
          ok

               Figure 14: Running MFVF on an in-place list reversal routine

does not itself perform any routine calls), a list of parameters (in the example, just a single
parameter l, a pointer to the linked list to be reversed), a precondition (in the example,
list(l), expressing that the routine expects to find a linked list at address l), a postcondition
(in the example, list(result), expressing that after the routine completes, the routine’s result
will point to a linked list), and the body of the routine to be verified. Coq command
Compute evaluates a Coq expression and prints the result: in the example, the result is ok,
indicating that the routine was verified successfully.
      MFVF includes an executable definition of symbolic execution and a semi-executable
definition of concrete execution. Concrete execution is semi-executable in the sense that
we have been able to write Coq functions that compute, for a given input program and a
given sequence of values for demonic choices over the booleans or the integers, if concrete
execution, for those choices, ends up in a singleton outcome or in failure.
      For example, consider the program that allocates a memory cell and then accesses the
memory cell at address 42. If the newly allocated memory cell was allocated at address 42,
execution succeeds; otherwise, it fails.
      We can easily check that both execution paths do indeed behave as expected, using the
Coq functions atZ, isSingle, and isFail shown in Figure 15. As shown in the figure, using Coq’s
Compute command, and by first picking value 2 for the depth of concrete execution (any
greater value would do as well) and then 42 for the address of the newly allocated memory
block, we can confirm that we end up in a singleton outcome, and that by alternatively
picking address 43 we end up in failure.
      The definition of function atZ exploits the fact that there is a separate case for type Z
in type type name, and that concrete execution of malloc commands uses this type name
in its demonic choice.
                                FEATHERWEIGHT VERIFAST                                   47




             Definition atZ z o := match o with
               | Some (demonic (set n Z o′ )) ⇒ Some (o′ z)
               | ⇒ None end.
             Definition isSingle o :=
               match o with Some (single ) ⇒ true | ⇒ false end.
             Definition isFail o := match o with
               | Some (angelic (set n Empty set )) ⇒ true
               | ⇒ false end.

             Definition o := cstate0 ⊲ exec [] (x := malloc(1); [42] := 123).

             Compute Some o ⊲ atZ 2 ⊲ atZ 42 ⊲ isSingle.
             true
             Compute Some o ⊲ atZ 2 ⊲ atZ 43 ⊲ isFail.
             true

                      Figure 15: Testing MFVF concrete execution

5.4. Soundness. The Coq statement of the soundness theorem is shown below: if symbolic
execution of a program does not fail, then concrete execution of that program does not fail.
The proof is accepted by Coq.

            Theorem soundness rspecs pdefs rdefs c :
              svalid program rspecs pdefs rdefs c = ok →
              cvalid program rdefs c.
            Proof.
            ···
            Qed.

            Print Assumptions soundness.
            Coq.Sets.Ensembles.Extensionality Ensembles
            Coq.Logic.Classical Prop.classic
            Coq.Logic.IndefiniteDescription.constructive indefinite description
            Coq.Logic.FunctionalExtensionality.functional extensionality dep

We can use Coq’s Print Assumptions command to check which axioms are used (directly
or indirectly) in the proof of the soundness theorem. Only the four listed axioms are used:
they are axioms of classical logic, offered by the Coq standard library.
     The Coq development can be browsed in HTML and PDF form and the full sources
can be downloaded at http://www.cs.kuleuven.be/˜bartj/fvf/.

                                    6. Related work

6.1. Hoare logic, separation logic. A more abstract, higher-level approach for reasoning
about imperative pointer-manipulating programs is given by separation logic [39, 42, 38],
which is an extension of Hoare logic [24].
48                           F. VOGELS, B. JACOBS, AND F. PIESSENS




                                              If
             Assign                           {b ∧ b′ } c {b′′ }  {b ∧ ¬b′ } c′ {b′′ }
             {b[e/x]} x := e {b}
                                                  {b} if b′ then c else c′ {b′′ }

             While                                      Seq
                    {b ∧ b′ } c {b}                     {b} c {b′ }     {b′ } c′ {b′′ }
              {b} while b′ do c {b ∧ ¬b′ }                     {b} c; c′ {b′′ }

           Conseq                                             Exists
            b ⇒ b′     {b′ } c {b′′ }   b′′ ⇒ b′′′            ∀v. {b[v/x]} c {b′ [v/x]}
                        {b} c {b′′′ }                            {∃x. b} c {∃x. b′ }

              Figure 16: The main axioms and inference rules of Hoare logic

      Hoare logic deals with program correctness judgments (also known as Hoare triples) of
the form {b} c {b′ }, where b, the precondition, and b′ , the postcondition, are boolean expres-
sions (as in Definition 1.1, except that they may also contain additional logical operators
such as conjunction and quantification), and c is a command that does not involve the heap
(i.e., it does not allocate, deallocate, or access heap cells); the judgment means that c, when
started with a store that satisfies precondition b, if it terminates, terminates with a store
that satisfies postcondition b′ :
                        ∀s. JbKs = true ⇒ s ⊲ exec(c) {s′ . Jb′ Ks′ = true}
      Hoare logic defines a number of axioms and inference rules for deriving correctness
judgments; the main ones are shown in Figure 16. Here, b[e/x] denotes the boolean expres-
sion obtained by substituting expression e for variable x in b, and b ⇒ b′ denotes that b
implies b′ in all stores, i.e. ∀s. JbKs ⇒ Jb′ Ks .
      For example, we can derive the judgment {0 ≤ n} i := 0; while i < n do i := i + 1 {i =
n} using the proof tree in Figure 17.
      A more convenient representation of this proof tree is in the form of the proof outline of
Figure 18, where assertions inserted between components of a sequential composition indi-
cate applications of the Seq rule, and multiple consecutive assertions indicate applications
of the Conseq rule.
      Separation logic extends Hoare logic with additional assertion logic constructs and
proof rules for reasoning conveniently about heap-manipulating programs. The syntax
of separation logic assertions extends the syntax of logical formulae with constructs for
specifying the heap: the assertion emp states that the heap is empty; the points-to assertion
e 7→ e′ states that the heap consists of exactly one heap cell, mapping address e to value
e′ , and the separating conjunction P ∗ Q states that the heap can be split into two disjoint
parts such that P holds for one part and Q holds for the other. Instead of Featherweight
VeriFast’s ?x syntax, separation logic uses regular existential quantification. Formally:
                s, h  emp       ⇔h=∅
                s, h  e 7→ e′   ⇔ h = {(JeKs , Je′ Ks )}
                s, h  P ∗ Q     ⇔ ∃h1 , h2 . h = h1 ⊎ h2 ∧ s, h1  P ∧ s, h2  Q
                s, h  ∃x. P     ⇔ ∃v. s[x := v], h  P
                s, h  b         ⇔ JbKs = true
                                      FEATHERWEIGHT VERIFAST                                   49




                                                    Assign
                                        (h)   (i)             (j)
                                                                    Conseq
                                                    (g)
                                                        While
                                (d)                 (e)                      (f )
                      Assign                                                        Conseq
                (b)                                     (c)
                                                             Seq
                                  (a)
                 (a)     {0 ≤ n} i := 0; while i < n do i := i + 1 {i = n}
                 (b)     {0 ≤ n} i := 0 {i ≤ n}
                 (c)     {i ≤ n} while i < n do i := i + 1 {i = n}
                 (d)     i≤n⇒i≤n
                 (e)     {i ≤ n} while i < n do i := i + 1 {i ≤ n ∧ ¬(i < n)}
                 (f )    i ≤ n ∧ ¬(i < n) ⇒ i = n
                 (g)     {i ≤ n ∧ i < n} i := i + 1 {i ≤ n}
                 (h)     i ≤ n∧i < n ⇒i+1 ≤ n
                 (i)     {i + 1 ≤ n} i := i + 1 {i ≤ n}
                 (j)     i≤n⇒i≤n

            Figure 17: Proof tree in Hoare logic for a simple example program

                                          {0 ≤ n}
                                          i := 0;
                                          {i ≤ n}
                                          while i < n do
                                             {i ≤ n ∧ i < n}
                                             {i + 1 ≤ n}
                                             i := i + 1
                                             {i ≤ n}
                                          {i ≤ n ∧ ¬(i < n)}
                                          {i ≤ n}

           Figure 18: Proof outline in Hoare logic for a simple example program

In separation logic, predicates are typically treated like inductive definitions, i.e. their mean-
ing is taken to be the smallest interpretation (i.e. set of heaps) that satisfies the definition;
such an interpretation always exists (by the Knaster-Tarski theorem) provided that predi-
cates are used inside of predicate definitions only in positive positions, i.e. not under nega-
tions or on the left-hand side of implications [40]. The typical example of such a predicate
is the predicate lseg(ℓ, ℓ′ ) denoting a linked list segment from a starting node ℓ (inclusive)
to a limiting node ℓ′ (exclusive):
                          def
              lseg(ℓ, ℓ′ ) = ℓ = ℓ′ ∧ emp ∨ ∃v, n. ℓ 7→ v ∗ ℓ + 1 7→ n ∗ lseg(n, ℓ′ )
Separation logic’s program logic extends Hoare logic’s inference system with axioms for the
heap manipulation commands and the frame axiom (see Figure 19). The former are small
axioms: they mention only the heap cells required for the command to succeed. The frame
axiom allows the small axioms to be lifted to larger heaps. Similarly, one can write small
50                          F. VOGELS, B. JACOBS, AND F. PIESSENS




     Cons                                                    Dispose
     {emp} x := cons(v, v ′ ) {x 7→ v ∗ x + 1 7→ v ′ }       {ℓ 7→ v} dispose(ℓ) {emp}

            Read                                         Write
            {ℓ 7→ v} x := [ℓ] {ℓ 7→ v ∧ x = v}           {ℓ 7→ v} [ℓ] := v ′ {ℓ 7→ v ′ }

                      Frame
                          {P } c {Q}
                                         if targets(c) ∩ freevars(R) = ∅
                       {P ∗ R} c {Q ∗ R}

                   Figure 19: The additional proof rules of separation logic

          {lseg(i, 0)}
          j := 0;
          {lseg(i, 0) ∗ lseg(j, 0)}
          while i 6= 0 do (
             {lseg(i, 0) ∗ lseg(j, 0) ∧ i 6= 0}
             {∃v, n. i + 1 7→ n ∗ i 7→ v ∗ lseg(n, 0) ∗ lseg(j, 0)}
                {i + 1 7→ n ∗ i 7→ v ∗ lseg(n, 0) ∗ lseg(j, 0)} Rule Exists. Fix v, n.
                   {i + 1 7→ n} Rule Frame.
                   k := [i + 1];
                   {i + 1 7→ n ∧ k = n}
                {(i + 1 7→ n ∧ k = n) ∗ i 7→ v ∗ lseg(n, 0) ∗ lseg(j, 0)}
                {i + 1 7→ k ∗ i 7→ v ∗ lseg(k, 0) ∗ lseg(j, 0)}
                   {i + 1 7→ k} Rule Frame.
                   [i + 1] := j;
                   {i + 1 7→ j}
                {i + 1 7→ j ∗ i 7→ v ∗ lseg(k, 0) ∗ lseg(j, 0)}
                {lseg(k, 0) ∗ lseg(i, 0)}
                j := i;
                {lseg(k, 0) ∗ lseg(j, 0)}
                i := k
                {lseg(i, 0) ∗ lseg(j, 0)}
             {lseg(i, 0) ∗ lseg(j, 0)}
          )
          {lseg(i, 0) ∗ lseg(j, 0) ∧ i = 0}
          {lseg(j, 0)}

Figure 20: A proof outline in separation logic of a program that performs an in-place reversal
           of a linked list

specifications for routines and use the frame axiom to lift those to the larger heap present
in a given calling context.
    Figure 20 shows a proof outline in separation logic for a program that performs an
in-place reversal of a linked list.
    VeriFast could be considered to be a type of “separation logic theorem prover”, by
interpreting the input files as a separation logic Hoare triple that serves as the proof goal
                                  FEATHERWEIGHT VERIFAST                                     51




and the annotations as hints to direct the construction of the proof. From this point of view,
VeriFast applies the separation logic frame rule when verifying loops and routine calls.


6.2. Separation logic tools.
 6.2.1. Smallfoot. Smallfoot [9] was a breakthrough in program verification tool development;
 it was successful in its goal of showcasing for the first time the power of separation logic
 for automated program verification and analysis. Like FVF, it takes as input an annotated
 program and checks each procedure against its contract. The programming language is very
 similar: like FVF’s, it is a simple while language with procedures. The main difference is
 that it includes concurrency constructs (resource declarations, parallel procedure calls, and
 conditional critical regions). The annotation language is very similar as well: a precondition
 and postcondition must be specified for each procedure, and a loop invariant must be
 specified for each loop; these are not inferred. (If one of these is omitted, it defaults to
 emp.) The main difference is that besides the points-to assertion, Smallfoot has built-in
 predicates for trees, list segments, doubly-linked lists, and xor lists, does not support user-
 defined predicates, and does not require open or close commands or any other kinds of proof
 hints (other than the procedure and loop annotations mentioned above). Another difference
 is that it does not support (even FVF’s very restricted form of) existential quantification.
      The main difference in Smallfoot’s functional behavior is that it is automatic: thanks
 to a complete, decidable proof theory for the supported assertion language, Smallfoot never
 requires proof hints. In particular, not only does it automatically fold and unfold the defini-
 tions of the inductive predicates (which in FVF requires open and close ghost commands),
 it also has sufficient rules built in to reason automatically about inductive properties such
 as appending two list segments. In FVF, this would require defining and calling a recursive
“lemma” routine that establishes the property.
      While Smallfoot’s algorithm is in many ways more powerful and more interesting than
 FVF’s, FVF’s goal is educational, and we believe its presentation in this article succeeds
 better at clearly conveying the essence of VeriFast’s operation, especially to an audience
 that is new to formal methods, than the presentation of Smallfoot’s operation [9, 8] does.

6.2.2. Other tools. Smallfoot’s algorithm has been used as a basis for shape analysis algo-
rithms that automatically infer loop invariants and postconditions [21], and even precon-
ditions [13]. These algorithms have been implemented in a tool called Infer [12] that has
successfully been exploited commercially. Another tool based on these ideas, called SLAyer
[10], is being used inside Microsoft to verify Windows device drivers.
     These techniques have been extended to a concurrent setting, e.g. to infer invariants
for shared resources [14]. Integration of separation logic and rely-guarantee reasoning [31]
has led to tools SmallfootRG [15] for verifying safety properties and Cave [47] for verifying
linearizability of fine-grained concurrent modules.
     Extensions of separation logic for dealing with object-oriented programming patterns
such as dynamic binding have been implemented in the tool jStar [22] that takes as input a
Java program, a precondition and postcondition for each method, and a set of inference and
abstraction rules, and attempts to automatically apply these rules to verify each method
body against its specification. jStar does not require (or support) annotations inside method
bodies.
52                          F. VOGELS, B. JACOBS, AND F. PIESSENS




    The HIP/SLEEK toolstack [16] uses separation logic-based symbolic execution to au-
tomatically verify shape, size, and bag properties of programs. Like VeriFast, it supports
user-defined recursive predicates to express the shape of data structures.

6.2.3. Proof assistant-based approaches. Like VeriFast, the tools mentioned above take as
input annotated programs and then run without further user interaction. Another approach
is to see program verification as a special case of interactive proof development, and to
extend proof assistants like Isabelle/HOL and Coq with theories defining program syntax
and semantics and specification formalisms, as well as lemmas and tactics (reusable proof
scripts) for aiding users in discharging proof obligations.
     Holfoot [46] is an implementation of Smallfoot inside the HOL 4 theorem prover. In
addition to the features supported by Smallfoot it can handle data and supports interactive
proofs. Moreover, it can handle arrays. Simple specifications with data like copying a list
can be handled automatically. More complicated ones like fully functional specifications of
filtering a list, mergesort, quicksort or an implementation of red-black trees require user
interaction. During this interaction all the features of the HOL 4 theorem prover can be
used, including the interface to external SMT solvers like Yices.
     Ynot [18] is a library for the Coq proof assistant which turns it into a full-fledged en-
vironment for writing and verifying imperative programs. In the tradition of the Haskell
IO monad, Ynot axiomatizes a parameterized monad of imperative computations, where
the type of a computation specifies not only what type of data it returns, but also what
Hoare-logic-style precondition and postcondition it satisfies. On top of the simple axiomatic
base, the library defines a separation logic. Specialized automation tactics are able to dis-
charge automatically most proof goals about separation-style formulas that describe heaps,
meaning that building a certified Ynot program is often not much harder than writing that
program in Haskell.
     Bedrock [17] is a Coq library for mostly-automated verification of low-level programs
in computational separation logic; a major difference from Ynot is that it has improved
support for reasoning about code pointers.
     Charge! [7] is a set of tactics for working with a shallow embedding of a higher-order
separation logic for a subset of Java in Coq.
     The Verified Software Toolchain project [5, 6, 3] has produced a separation logic for C,
called Verified C, in the form of a Coq library, as well as a Smallfoot implementation in Coq,
extractable to OCaml, called VeriSmall [4], both proven sound in Coq with respect to the
operational semantics of C against with the CompCert project [37] verified the correctness of
their C compiler, thus obtaining that the compiled program satisfies the verified properties.

6.3. Non-separation logic tools. Another approach for extending Hoare logic to reason
about programs with pointers (or other kinds of aliasing, such as Java’s object references) is
to simply treat the heap as a program variable whose value is a function that maps addresses
to values, and to retain regular classical logic as the assertion language. The following tools
are based on this approach.
     In this approach, the separation logic frame rule and small axioms that allow a sim-
ple syntactic treatment of heap mutation and procedure effect framing are generally not
available, but other approaches to procedure effect framing may be used. Most alternative
approaches are variants of dynamic frames [32], where a module uses abstract variables
                                  FEATHERWEIGHT VERIFAST                                     53




of type “set of memory locations” to abstractly specify which memory locations are modi-
fied by a procedure as well as which memory locations may influence the value of abstract
variables.
     VCC [19] is a verifier for concurrent C programs annotated with contracts expressed in
classical logic. For each C function, VCC generates a set of verification conditions (using a
variant of weakest preconditions [20]) to be discharged by an SMT solver. For modularity,
it uses the admissible invariants approach: a two-state invariant may be associated with
each C struct instance s, which may mention the fields of s as well as those of other struct
instances s′ , provided it is admissible: any update of s′ .f that satisfies the invariant of s′
must preserve the invariant of s. By encoding an ownership system on top of this approach,
it can be used both for precise reasoning about fine-grained concurrency and for reasoning
in a dynamic frames-like style about sequential code. VCC has been used to verify a large
part of the Microsoft Hyper-V hypervisor.
     Other important non-separation logic tools include Chalice [36] (a verifier for concurrent
Java-like programs based on implicit dynamic frames [43]), Dafny [35], KeY [1], and KIV
[45].
     As in the case of separation logic-based approaches, some non-separation logic-based
verification efforts have been carried out in a general-purpose proof assistant rather than a
specialized tool. Notable in this category are the L4.verified project [34], which verified an
OS microkernel consisting of 8KLOC of C code in Isabelle/HOL, and the Verisoft project
[2], which performed large parts of the pervasive verification, also in Isabelle/HOL, of the
complete software stack (plus parts of the hardware), including microkernel, kernel, and
applications, of a secure e-mail system and an embedded automotive system.

6.4. Semantic framework: Outcomes. In our formalization, to express and relate the
semantics of the programming language and the verification algorithm, via the intermediary
of semiconcrete execution, we developed the semantic framework based on outcomes, with
the important derived concepts of mutators, postcondition satisfaction, and coverage. This
enabled us to deal conveniently with failure, nontermination, and both demonic and angelic
nondeterminism.
     This framework is essentially nothing more than the predicate transformer semantics
proposed by Dijkstra [20]:
                                    exec(c) {Q} ≡ wp(c, Q)
     Also, mutators with answers are essentially a combination of a state monad and a
continuation monad.
     Our choice of defining the set of outcomes as an inductive datatype, rather than a pred-
icate over postconditions (i.e. a function from postconditions to bool, such that mutators
would be predicate transformers or functions from predicates to predicates) or, equiva-
lently, a state-continuation monad, has two advantages: firstly, we immediately have that
all outcomes are monotonic (postcondition satisfaction is preserved by weakening of the
postcondition); and secondly, our Coq encoding of concrete execution yields not an unex-
ecutable function to bool but an (infinite-branching) execution tree which we can explore,
as shown in Section 5.
54                               F. VOGELS, B. JACOBS, AND F. PIESSENS




6.5. Machine-checked tools. An effort similar to our executable machine-checked encod-
ing into Coq of Featherweight VeriFast is the executable machine-checked encoding into
Coq of Smallfoot, called VeriSmall [4].
     Whereas VeriSmall’s primary purpose is to serve as the basis for a certified program
verification tool chain, MFVF’s primary purpose is to serve as evidence for the correctness
of the presentation of FVF and its soundness proof in this article. Therefore, MFVF mirrors
the presentation very closely, and is more optimized for reading than VeriSmall.

                                             7. Conclusion
We presented a formal definition and outlined a soundness proof of Featherweight VeriFast,
thus hopefully achieving a clear and precise exposition of a core subset of the VeriFast
approach for sound modular verification of imperative programs. We also described our
executable definition and machine-checked soundness proof of Mechanised Featherweight
VeriFast, a slight variant of Featherweight VeriFast, in the Coq proof system.
      Future work includes: extending Featherweight VeriFast to include additional features
of VeriFast, such as lemma functions, inductive datatypes and fixpoint functions, concur-
rency, fractional permissions, function pointers, lemma function pointers, predicate fami-
lies, and higher-order predicates9; extending the executable definition of Mechanised Feath-
erweight VeriFast so that it can be used as a higher-assurance drop-in replacement for
VeriFast to verify annotated C source code files; and linking the resulting tool to existing
formalisations of C semantics, such as CompCert [37].

Acknowledgements. We would like to thank the anonymous reviewers for their helpful
comments. This work was supported in part by the Research Fund KU Leuven and by EU
project ADVENT.

                                               References
 [1] Wolfgang Ahrendt, Bernhard Beckert, Reiner Hähnle, and Peter H. Schmitt. Key: A formal method
     for object-oriented systems. In Marcello M. Bonsangue and Einar Broch Johnsen, editors, FMOODS,
     volume 4468 of Lecture Notes in Computer Science, pages 32–43. Springer, 2007.
 [2] Eyad Alkassar, Wolfgang Paul, Artem Starostin, and Alexandra Tsyban. Pervasive verification of an
     OS microkernel: Inline assembly, memory consumption, concurrent devices. In Peter O’Hearn, Gary T.
     Leavens, and Sriram Rajamani, editors, Verified Software: Theories, Tools, Experiments (VSTTE 2010),
     volume 6217 of Lecture Notes in Computer Science, pages 71–85, Edinburgh, UK, August 2010. Springer.
 [3] Andrew W. Appel. Verified software toolchain. In ESOP, 2011.
 [4] Andrew W. Appel. VeriSmall: Verified Smallfoot shape analysis. In CPP, 2011.
 [5] Andrew W. Appel. Verification of a cryptographic primitive: Sha-256. ACM Trans. Program. Lang.
     Syst., 37(2):7:1–7:31, April 2015.
 [6] Andrew W. Appel, Robert Dockins, Aquinas Hobor, Lennart Beringer, Josiah Dodds, Gordon Stewart,
     Sandrine Blazy, and Xavier Leroy. Program Logics for Certified Compilers. Cambridge University Press,
     New York, NY, USA, 2014.
 [7] Jesper Bengtson, Jonas Braband Jensen, and Lars Birkedal. Charge! a framework for higher-order
     separation logic in Coq. In ITP, 2012.
 [8] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Symbolic execution with separation logic. In
     APLAS, 2005.
     9Note that these advanced features have already been formalized, with machine-checked soundness proofs,
separately [29, 26].
                                       FEATHERWEIGHT VERIFAST                                              55




 [9] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. Smallfoot: Modular automatic assertion
     checking with separation logic. In FMCO, 2006.
[10] Josh Berdine, Byron Cook, and Samin Ishtiaq. SLAyer: Memory safety for systems-level code. In CAV,
     2011.
[11] Michael Butler and Wolfram Schulte, editors. FM 2011: Formal Methods - 17th International Sympo-
     sium on Formal Methods, Limerick, Ireland, June 20-24, 2011. Proceedings, volume 6664 of Lecture
     Notes in Computer Science. Springer, 2011.
[12] Cristiano Calcagno and Dino Distefano. Infer: an automatic program verifier for memory safety of C
     programs. In Proc. 3rd NASA Formal Methods Symposium, number 6671 in Lecture Notes in Computer
     Science. Springer, 2011.
[13] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. Compositional shape
     analysis by means of bi-abduction. In Zhong Shao and Benjamin C. Pierce, editors, Proceedings of
     the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages, POPL 2009,
     Savannah, GA, USA, January 21-23, 2009, pages 289–300. ACM, 2009.
[14] Cristiano Calcagno, Dino Distefano, and Viktor Vafeiadis. Bi-abductive resource invariant synthesis. In
     APLAS, number 5904 in LNCS, pages 259–274. Springer, 2009.
[15] Cristiano Calcagno, Matthew Parkinson, and Viktor Vafeiadis. Modular safety checking for fine-grained
     concurrency. In SAS, number 4634 in LNCS, pages 233–238. Springer, August 2007.
[16] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. Automated verification of
     shape, size and bag properties via user-defined predicates in separation logic. Sci. Comput. Program.,
     77(9):1006–1036, 2012.
[17] Adam Chlipala. Mostly-automated verification of low-level programs in computational separation logic.
     In Mary W. Hall and David A. Padua, editors, PLDI, pages 234–245. ACM, 2011.
[18] Adam Chlipala, J. Gregory Malecha, Greg Morrisett, Avraham Shinnar, and Ryan Wisnesky. Effective
     interactive proofs for higher-order imperative programs. In Graham Hutton and Andrew P. Tolmach,
     editors, ICFP, pages 79–90. ACM, 2009.
[19] Ernie Cohen, Markus Dahlweid, Mark A. Hillebrand, Dirk Leinenbach, Michal Moskal, Thomas Santen,
     Wolfram Schulte, and Stephan Tobies. VCC: A practical system for verifying concurrent C. In Stefan
     Berghofer, Tobias Nipkow, Christian Urban, and Makarius Wenzel, editors, Theorem Proving in Higher
     Order Logics, 22nd International Conference, TPHOLs 2009, Munich, Germany, August 17-20, 2009.
     Proceedings, volume 5674 of Lecture Notes in Computer Science, pages 23–42. Springer, 2009.
[20] Edsger W. Dijkstra. Guarded commands, nondeterminacy and formal derivation of programs. CACM,
     18(8):453–457, August 1975.
[21] Dino Distefano, Peter O’Hearn, and Hongseok Yang. A local shape analysis based on separation logic.
     In TACAS, 2006.
[22] Dino Distefano and Matthew Parkinson. jStar: Towards practical verification for java. In OOPSLA,
     2008.
[23] Jean-Christophe Filliâtre, Andrei Paskevich, and Aaron Stump. The 2nd verified software competition:
     Experience report. In Vladimir Klebanov and Sarah Grebing, editors, COMPARE2012: 1st Interna-
     tional Workshop on Comparative Empirical Evaluation of Reasoning Systems, Manchester, UK, June
     2012. EasyChair.
[24] C. A. R. Hoare. An axiomatic basis for computer programming. Communications of the ACM,
     12(10):576–583, October 1969.
[25] Marieke Huisman, Vladimir Klebanov, and Rosemary Monahan. VerifyThis Verification Competition
     2012 - organizer’s report. Technical Report Karlsruhe Reports in Informatics 2013, 1, Karlsruhe Institute
     of Technology, Faculty of Informatics, 2013.
[26] Bart Jacobs and Frank Piessens. Expressive modular fine-grained concurrency specification. In Thomas
     Ball and Mooly Sagiv, editors, POPL, pages 271–282. ACM, 2011.
[27] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem Penninckx, and Frank Piessens.
     VeriFast: A powerful, sound, predictable, fast verifier for C and Java. Invited paper. In Mihaela Gheo-
     rghiu Bobaru, Klaus Havelund, Gerard J. Holzmann, and Rajeev Joshi, editors, NASA Formal Methods,
     volume 6617 of Lecture Notes in Computer Science, pages 41–55. Springer, 2011.
[28] Bart Jacobs, Jan Smans, and Frank Piessens. A quick tour of the VeriFast program verifier. In APLAS
     2010, volume 6461 of LNCS, pages 304–311, Heidelberg, 2010. Springer.
56                              F. VOGELS, B. JACOBS, AND F. PIESSENS




[29] Bart Jacobs, Jan Smans, and Frank Piessens. Verification of unloadable modules. In Butler and Schulte
     [11], pages 402–416.
[30] Bart Jacobs, Jan Smans, and Frank Piessens. The VeriFast program verifier: a tutorial. Available from
     http://www.cs.kuleuven.be/~ bartj/verifast/, 2014.
[31] Cliff B. Jones. Specification and design of (parallel) programs. In IFIP Congress, pages 321–332, 1983.
[32] Ioannis T. Kassios. Dynamic frames: support for framing, dependencies and sharing without restrictions.
     In FM, 2006.
[33] Vladimir Klebanov, Peter Müller, Natarajan Shankar, Gary T. Leavens, Valentin Wüstholz, Eyad Alka-
     ssar, Rob Arthan, Derek Bronish, Rod Chapman, Ernie Cohen, Mark A. Hillebrand, Bart Jacobs,
     K. Rustan M. Leino, Rosemary Monahan, Frank Piessens, Nadia Polikarpova, Tom Ridge, Jan Smans,
     Stephan Tobies, Thomas Tuerk, Mattias Ulbrich, and Benjamin Weiß. The 1st verified software compe-
     tition: Experience report. In Butler and Schulte [11], pages 154–168.
[34] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick, David Cock, Philip Derrin, Dham-
     mika Elkaduwe, Kai Engelhardt, Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and
     Simon Winwood. seL4: Formal verification of an OS kernel. In Proceedings of the 22nd ACM Symposium
     on Operating Systems Principles, pages 207–220, Big Sky, MT, USA, Oct 2009. ACM.
[35] K. Rustan M. Leino. Developing verified programs with dafny. In Rajeev Joshi, Peter Müller, and An-
     dreas Podelski, editors, VSTTE, volume 7152 of Lecture Notes in Computer Science, page 82. Springer,
     2012.
[36] K. Rustan M. Leino and Peter Müller. A basis for verifying multi-threaded programs. In ESOP, 2009.
[37] Xavier Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):107–115,
     2009.
[38] Peter W. O’Hearn. A primer on separation logic (and automatic program verification and analysis).
     In Tobias Nipkow, Orna Grumberg, and Benedikt Hauptmann, editors, Software Safety and Security;
     Tools for Analysis and Verification, number 33 in NATO Science for Peace and Security Series. IOS
     Press, 2012. Marktoberdorf Summer School 2011 Lecture Notes.
[39] Peter W. O’Hearn, John Reynolds, and Hongseok Yang. Local reasoning about programs that alter
     data structures. In CSL, 2001.
[40] Matthew Parkinson and Gavin Bierman. Separation logic and abstraction. In POPL 2005, 2005.
[41] Pieter Philippaerts, Jan Tobias Mühlberg, Willem Penninckx, Jan Smans, Bart Jacobs, and Frank
     Piessens. Software verification with VeriFast: Industrial case studies. Science of Computer Programming,
     2013.
[42] J. C. Reynolds. Separation logic: a logic for shared mutable data structures. In LICS, 2002.
[43] Jan Smans, Bart Jacobs, and Frank Piessens. Implicit dynamic frames. ACM Trans. Program. Lang.
     Syst., 34(1):2, 2012.
[44] Jan Smans, Bart Jacobs, and Frank Piessens. Verifast for java: A tutorial. In Dave Clarke, James Noble,
     and Tobias Wrigstad, editors, Aliasing in Object-Oriented Programming, volume 7850 of Lecture Notes
     in Computer Science, pages 407–442. Springer, 2013.
[45] B. Tofan, G. Schellhorn, and W. Reif. A compositional proof method for linearizability applied to a
     wait-free multiset. In iFM, 2014.
[46] Thomas Tuerk. A separation logic framework for HOL. Technical Report UCAM-CL-TR-799, University
     of Cambridge, Computer Laboratory, June 2011.
[47] Viktor Vafeiadis. Automatically proving linearizability. In CAV, 2010.
[48] Gijs Vanspauwen and Bart Jacobs. Sound symbolic linking in the presence of preprocessing. In Robert M.
     Hierons, Mercedes G. Merayo, and Mario Bravetti, editors, SEFM, volume 8137 of Lecture Notes in
     Computer Science, pages 122–136. Springer, 2013.
[49] Frédéric Vogels, Bart Jacobs, Frank Piessens, and Jan Smans. Annotation inference for separation logic
     based verifiers. In Roberto Bruni and Jürgen Dingel, editors, FMOODS/FORTE, volume 6722 of Lecture
     Notes in Computer Science, pages 319–333. Springer, 2011.
                                                    NOTES                                                                        57




                                                    Notes
 (a)
       Results of the VeriFast team:
                        Competition                 Conference                         Result
           1st Verified Software Competition [33]   VSTTE 2010            roughly tied with all other teams
           2nd Verified Software Competition [23]   VSTTE 2012                 score 570/600, rank 8
                        VerifyThis [25]              FM 2012                         sole winner
 (b)
    by Jesper Bengtson (at ITU Copenhagen), Alexey Gotsman (at ENS Lyon), Dilian Gurov (at KTH
Stockholm), and Stephan van Staden (at ETH Zurich)




                                               This work is licensed under the Creative Commons Attribution-NoDerivs License. To view
                                               a copy of this license, visit http://creativecommons.org/licenses/by-nd/2.0/ or send a
                                               letter to Creative Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or
                                               Eisenacher Strasse 2, 10777 Berlin, Germany
