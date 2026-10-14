                                                     2LS: Heap Analysis and Memory Safety
                                                                    (Competition Contribution)⋆

                                              Martin Hruška3 , Viktor Malı́k3 , Peter Schrammel⋆⋆1,2 , and Tomáš Vojnar3
                                                     1
                                                         Diffblue Ltd, Oxford, UK 2 University of Sussex, Brighton, UK
                                                             3
                                                               FIT BUT, IT4Innovations Centre of Excellence, CZ
arXiv:1903.00712v2 [cs.SE] 3 Jan 2020




                                               Abstract 2LS is a framework for analysis of sequential C programs that can
                                               verify and refute program assertions and termination. The 2LS framework is
                                               built upon the CPROVER infrastructure and implements template-based syn-
                                               thesis techniques, e.g. to find invariants and ranking functions, and incremental
                                               loop unwinding techniques to find counterexamples and k-induction proofs. The
                                               main improvements in this year’s version are the ability of 2LS to analyse pro-
                                               grams requiring combined reasoning about shape and content of dynamic data
                                               structures, and an instrumentation for memory safety properties.


                                        1 Overview
                                        2LS is a static analysis and verification tool for sequential C programs. At its core, it
                                        uses the kIkI algorithm (k-invariants and k-induction) [1], which integrates bounded
                                        model checking, k-induction, and abstract interpretation into a single, scalable frame-
                                        work. kIkI relies on incremental SAT solving in order to find proofs and refutations of
                                        assertions, as well as to perform termination analysis [2].
                                            This year’s competition version introduces new product and power domain combin-
                                        ations to support invariant inference for programs that manipulate shape and content of
                                        dynamic data structures [4]. Moreover, there is an improved encoding of memory safety
                                        properties.

                                        Architecture. The architecture of 2LS has been described in previous competition
                                        contributions [6,5]. In brief, 2LS is built upon the CPROVER infrastructure [3] and thus
                                        uses GOTO programs as the internal program representation. The analysed program is
                                        translated into an acyclic, over-approximate single static assignment (SSA) form, in
                                        which loops are cut at the edges returning to the loop head. Subsequently, 2LS refines
                                        this over-approximation by computing inductive invariants in various abstract domains
                                        represented by parametrised logical formulae, so-called templates [1]. The competition
                                        version uses the zones domain for numerical variables in combination with our shape
                                        domain for pointer-typed variables and the symbolic paths domain described below.
                                        The SSA form is bit-blasted into a propositional formula and given to a SAT solver. The
                                        kIkI algorithm then incrementally amends the formula to perform loop unwindings and
                                        invariant inference based on template-based synthesis [1].
                                        ⋆
                                           The Czech authors were supported by the Czech Science Foundation project 17-12465S,
                                           H2020 ECSEL Aquas project, the IT4IXS: IT4Innovations Excellence in Science project
                                           (LQ1602), and the FIT BUT internal project FIT-S-17-4014.
                                        ⋆⋆
                                           Jury member: p.schrammel@sussex.ac.uk.
2 New Features
The major improvements for SV-COMP’20 are all related to analysis of heap-manipu-
lating programs. We build on the shape domain presented last year [5] and introduce
abstract domain combinations that allow us to analyse both shape and content of dy-
namic data structures. Furthermore, we present encoding of assertions that are used for
verifying memory safety properties.

2.1 Combinations of Abstract Domains
The new capability of 2LS to jointly analyse shape and content of dynamic data struc-
tures takes advantage of the template-based synthesis engine of 2LS. Invariants are
computed in various abstract domains where each domain has the form of a template
while relying on the analysis engine to handle the domain combinators.

Memory model In our memory model, we represent dynamically allocated objects by
so-called abstract dynamic objects. Each such object is an abstraction of a number of
concrete dynamic objects allocated by the same malloc call (i.e. at the same program
location) [4].

Shape Domain For analysing the shape of the heap, we use an improved version of
the shape domain that we introduced last year [5]. The domain over-approximates the
points-to relation between pointers and symbolic addresses of memory objects in the
analysed program: for each pointer-typed variable and each pointer-typed field of an
abstract dynamic object p, we compute the set of all addresses that p may point to [4].

Template Polyhedra Domain For analysing numerical values, we use the template
polyhedra abstract domains, particularly the interval and the zones domains [1].

Shape and Polyhedra Domain Combination Since both domains have the form of
a template formula, we simply use them side-by-side in a product domain combination—
the resulting formula is a conjunction of the two template formulae [4].
This combination allows 2LS to infer,                        ao1
e.g., invariants describing an unbounded
singly-linked list whose nodes contain           next       ...          next      NULL
values between 1 and 10. We show an ex-         val= 3                 val= 10
ample of such a list in Figure 1. Here, all
list nodes are abstracted by a single ab- Figure 1. Unbounded singly-linked list abstrac-
stract dynamic object ao1 (i.e. we assume ted by an abstract dynamic object ao1 .
that they are all allocated at the same pro-
gram location). The invariant inferred by 2LS for such a list might look as follows:
              (ao1 .next = &ao1 ∨ ao1 .next = NULL) ∧ ao1 .val ∈ [1, 10]              (1)
The first disjunction describes the shape of the list—the next field of each node points
to some node of the list or to NULL1 . The second part of the conjunct is then an invariant
 1
     Here, ao1 .f is an abstraction of the f fields of all concrete objects represented by ao1 . Ana-
     logously, &ao1 is an abstraction of symbolic addresses of all represented objects.
in the interval domain over all values stored in the list—it expresses the fact that the
value of each node lies in the interval between 1 and 10.

2.2 Symbolic Paths
To improve precision of the analysis, we let 2LS compute different invariants for dif-
ferent symbolic paths taken by the analysed program. We require a symbolic path to
express which loops were executed at least once. This allows us to distinguish situ-
ations when an abstract dynamic object does not represent any really allocated object
and hence the invariant for such abstract dynamic object is not valid [4].
     The symbolic path domain allows us to iteratively compute a set of symbolic paths
p1 , . . . , pn (represented by guard variables in the SSA) with associated shape and data
invariants I1 , . . . , In . The aggregated invariant is then p1 ⇒ I1 ∧ · · · ∧ pn ⇒ In , which
corresponds to a power domain combination.

2.3 Memory Safety
To verify memory safety, appropriate assertions are inserted into the program. We now
describe the structure of these assertions for different types of memory errors.

Dereferencing/Freeing a NULL Pointer To check for this kind of errors, we add an
assertion p 6= NULL to each location where *p or free(p) occurs [4]. Since the shape
domain over-approximates the set of all addresses that p may point to, absence of such
errors can be proven. If an error is found, we use BMC to check its reachability.

Dereferencing/Freeing a Freed Pointer Using a single abstract dynamic object to rep-
resent multiple concrete objects poses problems when trying to determine if a particular
concrete object (within the abstract one) has already been freed or not. To resolve this,
for each abstract dynamic object aoi , we non-deterministically select a single concrete
object represented by aoi and materialize it as aoco                           co
                                                  i . After that, every time aoi is freed,
we non-deterministically set a special variable fr to true. This allows us to generate an
assertion p 6= fr for each location containing *p or free(p) [4].

Memory Leaks To find a memory leak, we check whether, at the end of the program,
there is an object aoco                     co            co
                     i such that fr 6= &aoi . If such aoi exists, there is a memory leak
present (some object represented by the corresponding aoi has has not been freed). On
the other hand, absence from memory leaks can only be proven for programs without
loops (or with loops that can be fully unwound). This is because checking that fr may be
equal to a materialized object aoco
                                  i is not sufficient to prove that all objects represented
by the corresponding abstract object aoi were freed [4].


3 Strengths and Weaknesses
This year’s improvements mostly influenced results in the MemSafety category where
2LS narrowly missed the podium in 4th place. There were many new benchmarks and
a new sub-category (MemCleanup) whose benchmarks were handled well by 2LS.
     One of the main strengths of 2LS is verification of programs requiring joint reas-
oning about shape and content of dynamic data structures. There were no such bench-
marks in previous SV-COMP editions, thus, we contributed 10 of our own benchmarks.
Combining our shape domain with the zones domain for value analysis allows 2LS to
successfully verify 9 out of 10 of these benchmarks (the last one has timed out). None
of the other tools was able to verify more than 3 of these benchmarks.
     Still, there remain a lot of challenges and limitations. The heap domain is quite
simple and over-approximates the heap too much to allow us to analyse complicated
properties of dynamic data structures. Moreover, reasoning about array contents is still
lacking, and the 2LS’ algorithm kIkI does not yet support recursion. Moreover, there
is a large number of unconfirmed witnesses, especially in the termination analysis (500
points lost).

4 Tool Setup
The competition submission is based on 2LS version 0.7.2 The archive contains the bin-
aries needed to run 2LS (2ls-binary, goto-cc), and so no further installation is needed.
There is also a wrapper script 2ls which is used by Benchexec to run the tools over
the verification benchmarks. See the wrapper script also for the relevant command line
options given to 2LS. The further information about the contents of the archive could
be find in the README file. The tool info module for 2LS is called two ls.py and the
benchmark definition file 2ls.xml. As a back end, the competition submission of 2LS
uses Glucose 4.0. 2LS competes in all categories except Concurrency and Java.

5 Software Project
2LS is maintained by Peter Schrammel with pull requests contributed by the com-
munity.3 It is publicly available under a BSD-style license. The source code is available
at http://www.github.com/diffblue/2ls.

References
1. Brain, M., Joshi, S., Kroening, D., Schrammel, P.: Safety Verification and Refutation by k-
   Invariants and k-Induction. In: SAS. LNCS, vol. 9291, pp. 145–161. Springer (2015)
2. Chen, H.Y., David, C., Kroening, D., Schrammel, P., Wachter, B.: Bit-Precise Procedure-
   Modular Termination Proofs. TOPLAS 40 (2017)
3. Clarke, E.M., Kroening, D., Lerda, F.: A tool for checking ANSI-C programs. In: TACAS.
   LNCS, vol. 2988, pp. 168–176. Springer (2004)
4. Malı́k, V., Hruska, M., Schrammel, P., Vojnar, T.: Template-based verification of heap-
   manipulating programs. In: FMCAD. pp. 103–111 (2018)
5. Malı́k, V., Martiček, Š., Schrammel, P., Srivas, M., Vojnar, T., Wahlang, J.: 2LS: Memory
   Safety and Non-termination (Competition Contribution). In: TACAS. pp. 417–421. Springer
   (2018)
6. Schrammel, P., Kroening, D.: 2LS for Program Analysis (Competition Contribution). In:
   TACAS. LNCS, vol. 9636, pp. 905–907. Springer (2016)

 2
     Executable available at https://gitlab.com/sosy-lab/sv-comp/archives-2020
 3
     https://github.com/diffblue/2ls/graphs/contributors
