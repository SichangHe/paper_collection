                                             Finding Model-Checkable Needles in Large
                                            Source Code Haystacks: Modular Bug-Finding
                                              via Static Analysis and Dynamic Invariant
                                                               Discovery
                                           Mohammad Amin Alipour,∗ Alex Groce,∗ Chaoqiang Zhang,∗ Anahita Sanadaji,∗ and Gokul Caushik,∗
                                                                         ∗ School of Electrical Engineering and Computer Science

                                                                                       Oregon State University
arXiv:1609.06382v1 [cs.SE] 20 Sep 2016




                                                             {alipourm,grocea,zhangch,alipourm,sanandaa,caushikg}@onid.oregonstate.edu


                                            Abstract—In this paper, we present a novel marriage          when a research team drives the system design and real-
                                         of static and dynamic analysis. Given a large code base         world deadlines and constraints are removed, its role in
                                         with many functions and a mature test suite, we propose         most critical system development efforts is typically rele-
                                         using static analysis to find functions 1) with assertions
                                         or other evident correctness properties (e.g., array bounds     gated to verifying (or finding bugs in) small components.
                                         requirements or pointer access) and 2) with simple enough       One approach to escaping this limitation is to enhance the
                                         control flow and data use to be amenable to predicate-          fundamental scalability of model checking by using ab-
                                         abstraction based or bounded model checking without hu-         straction or other techniques to manage huge state spaces,
                                         man intervention. Because most such functions in realistic      and especially by using compositional reasoning [4], [6],
                                         software systems in fact rely on many input preconditions
                                         not specified by the language’s type system (or annotated       [9], [10] to handle large code bases. Such efforts are an
                                         in any way), we propose using dynamically discovered            important contribution, but thus far have yet to crack
                                         invariants based on a program’s test suite to characterize      anything like the 1 million LOC mark in an automated
                                         likely preconditions, in order to reduce the problem of false   fashion.
                                         positives. While providing little in the way of verification,      Beyond the fundamental problem of the state space
                                         this approach may provide an additional quick and highly
                                         scalable bug-finding method for programs that are usually       explosion, there is a second scalability problem with
                                         considered “too large to model check.” We present a simple      most current model checking tools: they are far less
                                         example showing that the technique can be useful for a more     “industrially hardened” than commercial static analysis
                                         typically “model-checkable” code base, even in the presence     tools, and fail for a variety of essentially engineering
                                         of a poorly designed test suite and bad invariants.             reasons for very large code bases — partly because they
                                            While new tools and techniques are being devised to          are seldom tested on more than a few thousand lines of
                                         conquer software verification problems, software systems        code at a time. Model checking tools work best, and most
                                         themselves are becoming more complicated, with multiple         automatically, when given code fragments only the size
                                         layers of software/hardware interactions, functioning in        of a few small functions, in which case both predicate
                                         dynamic, uncertain environments. Even where teams of            abstraction [4] and bounded model checking [3], [5] can
                                         model checking experts are in place, and formal veri-           be used even by upper-level undergraduate students to
                                         fication is acknowledged as a valuable practice, model          verify properties and find subtle bugs. This fact may lie
                                         checking is seldom applied to complete modern code              behind the success of model checkers for finding bugs in
                                         bases for realistic-scaled systems. For example, while          container classes [15].
                                         model checking was applied to small portions (typically            This paper proposes and presents very preliminary
                                         10,000 lines or less) of the code base for NASA/JPL’s           results for a novel “modular” method for applying model
                                         Curiosity rover [12], even the Laboratory for Reliable          checking automatically to real-world code bases that does
                                         Software did not attempt to apply model checking to the         not require conquering the state-space explosion prob-
                                         full approximately 2 million lines of Curiosity software.       lem, or automatically decomposing such a system into
                                            Static analysis methods, on the other hand, are ex-          components in the traditional fashion for verification.
                                         pected to scale to real-world code bases. Even the popular      We propose to exploit precisely the current strengths of
                                         technical press [14] has noted the use of Coverity and          model checking by mining a large code base for small,
                                         other tools on huge code bases for the Curiosity rover, the     self-contained, portions of code suitable for push-button
                                         CERN particle accelerator, and other big mission-critical       model checking. The core idea is to use static analysis
                                         systems.                                                        to identify functions (or small sets of functions) without
                                            While model checking can be applied to whole systems         recursion or recursive datatypes, overly complex pointer
                          Figure 1: The core workflow of our modular verification approach


manipulations, or whatever other features typically frus-       system is run, with instrumentation inserted to extract
trate model checking efforts. Additionally, such code           trace information over the suitable functions. Dynamic
fragments should contain assertions or other statements         invariant generation takes program traces and identifies,
(e.g. array or pointer accesses, system calls) that make        via “empirical” rather than static means, invariants —
it easy to generate properties to check without human           propositions that are true for all observed executions of
intervention. We call our search verification task triage:      the system. These invariants are then used to annotate the
our contribution is to propose that one effective way to        triage-identified functions with “preconditions” generaliz-
apply model checking to large systems is to simply cherry       ing the data values seen during execution of the test suite.
pick the parts of the system that can be model checked.         The annotated pieces of code are model checked, with the
This turns on its head the usual effort to apply human          expectation that any bugs detected are likely to be real
effort to verifying the components of most interest in          faults since the invariants ensure that data ranges and
a large system, which can proceed independently. Our            relationships are like those observed over the test suite.
approach to “modular verification” works more like many         As a simple example, consider the case of a function f
static analysis algorithms, which “give up” on pointers         that takes as one input a value int m. In typical world-
when alias analysis fails, and abandon overly complex           world C code, m may in fact represent a highly constrained
paths. A more fanciful way to understand the idea is            quantity, such as the number of minutes since midnight,
to consider the not infrequent occasion of a graduate           but the type system will not express this constraint.
student or model checking researcher combing a large,           Model checking f without this information may produce a
critical system (e.g. OpenSSL) for some functions suitable      counterexample involving, for example, integer overflow
for specification and verification. We aim to replace such      due to multiplying m by 60. Even if a real off-by-one bug
a human with a static analysis algorithm that is less           exists when m = 1, the overflow bug may be much easier
intelligent, but much faster and able to generate many          for a SAT solver in a bounded model checker to detect.
likely candidates rather than being satisfied after finding     Model checking the code with the added assumption
one or two functions.                                           that 0 <= m < 3600, however, the model checker will
   Unfortunately, naive verification task triage plus model     report the real bug. Even though 1 did not appear in the
checking is unlikely to yield effective results, even for the   test suite, the generalization algorithms in the invariant
purpose of bug finding. We believe that most functions          detector generalized the actual input range to include it.
in complex code bases rely on preconditions over inputs         Extremely large values of m also did not appear during
and data values accessed that are not represented by the        test suite execution, of course, but the range observed
language’s type system or by other annotations. Model           was sufficiently small that invariant detection proposed
checking without these preconditions will probably lead         that the range was likely restricted.
to an unmanageable number of uninteresting bug reports             An obvious objection to this approach is that the in-
— the false positives that have always plagued static           variants from a test suite will often over-constrain the
analysis efforts.                                               behavior of many small components, unless the test suite
   We propose to mitigate this problem by using dynamic         is very high quality. We hope that even highly inaccurate
invariant detection [7] in a (to our knowledge) novel           invariants may allow a model checker to find a real bug.
way: as a tool for generating approximations of pre-            For example, in the case of f, if the test suite falsely
conditions needed to avoid false positives in large code        suggests that 0 <= m < 60 because tests only run for
bases. The idea, shown in Figure 1, involves a two-             1 hour, the model checker can still find the real bug.
stage workflow. First, we perform verification task triage      Our claim is that our use of dynamic invariants relies on
to identify suitable small pieces of code to model checking     their ability to crudely “carve away” the data values that
a large code base. Then, the test suite for the large           a function is not expected to work rather than on their
                                                                 public void add(int x) {
strict accuracy. A gross underapproximation of behavior
                                                                     Node current = root;
can still lead to the discovery of real bugs, while an
                                                                     if (root == null) {
overappoximation buries a user in false positives. We
                                                                        br0 = br0 + 1;
provide suggestive evidence for the possibility that poor
                                                                        root = new Node(x);
invariants can still be useful by applying our technique to
                                                                        return;
a simple container class and a radically non-representative
                                                                     }
test suite. A more complex example with hand-generated
                                                                     while (current.value != x) {
“invariants” shows that even simple triage can discover
                                                                        if (x < current.value) {
useful targets for verification and avoid false positives
                                                                             if (current.left == null) {
using invariants.
                                                                                br1 = br1 + 1;
   In the remainder of the paper, we first discuss key
                                                                                current.left = new Node(x);
related work in Section I, to place our core idea in context,
                                                                             } else {
elaborate our proof-of-concept example in Section II,
                                                                                br2 = br2 + 1;
demonstrate verification triage in Section III, and discuss
                                                                                current = current.left;}
the challenges in bringing the full vision of a “static
                                                                             } else {
analysis-like” approach to modularity for model checking
                                                                             if (current.right == null) {
in Section IV.
                                                                                br3 = br3 + 1;
                     I. R ELATED W ORK                                          current.right = new Node(x);
                                                                             } else {
   To our knowledge, the idea of mining large code
                                                                                br4 = br4 + 1;
bases for arbitrary sub-components suitable for model
                                                                                current = current.right;
checking has not been previously explored. The most
                                                                             }
closely related ideas are efforts to scale model checking
                                                                        }
by approximating the weakest precondition under which a
                                                                     }
sub-component satisfies its correctness properties [2], [6],
                                                                 }
[11]. The primary difference is that where these methods
aim to learn or iterate to a “good” assumption that is           Figure 2: Function add after instrumentation for branch count.
as weak as possible, we simply want a precondition that
removes false positives, even if it is too strong, and, of
course, that such methods have no concept of mining a
                                                                 this.br1 one of { 0, 1, 2 }
code base for possible targets for model checking.
                                                                 this.br3 one of { 0, 1, 2 }
               II. E XAMPLE : B INARY T REES                        Using these invariants (which restrict the structure to
   As a simple example of how our approach might work            up to two right children or up to two left children), we
in practice, assuming that an effective verification task        generate a simple CBMC harness, knowing (thanks to our
triage can be designed, we apply our method to a fre-            triage and invariant examination) that a shallow loop
quently studied binary tree implementation [8], [15]. We         unwinding will suffice, and that no types encountered are
use a RepOK function to test the validity of the tree            likely to make verification difficult, as shown in Figure 4.
structure, and have implemented a simple random testing             With this extremely restricted harness, CBMC was able
system to test it, shown in Figure 3. We choose to verify        to find the bug in binary tree [8], despite the fact that
the remove function, and instrument the code for the             the shallow random testing did not discover the bug.
binary tree with extended invariants [1], as shown in
Figure 2/footnoteInstrumentation for add, not remove is                    III. S IMPLE V ERIFICATION TASK T RIAGE
shown as it is easier to follow. to help us limit the behavior
of the code to valid trees only. We use Daikon [7] to              Given that using even poor tests to generate potentially
infer invariants from all traces generated during random         incorrect invariants for model checking can still lead to
testing. Extended invariants introduce history variables         fast, effective bug discovery, the core of our modular
that allow Daikon to provide “invariants” in the form            verification approach becomes finding functions where
of code coverage facts as well as more traditional data          this can be applied to large, real-world code bases. Figure
invariants, to capture relationships such as, e.g., that a       5 shows a function from the source code for version 1.6 of
loop always executes a number of times equal to twice            Mozilla’s SpiderMonkey JavaScript engine. This function
the value of a certain input. Unfortunately, when running        was automatically identified using a very simple 100-line
the random tester for 5,000 tests, we choose to use tests        Python script that crawls through a set of C source files
with a maximum length of only 4 steps, which leads to            and identifies functions that:
extended invariants that radically underapproximate the            •   do contain at least some assert statement or poten-
behavior of the class:                                                 tially crashing memory dereference (i.e., functions
    Random rand = new Rand(20);
                                                                Calling a “bad” function is not necessarily a problem,
    for(i = 0; i < N; i ++){
                                                                because the return value may be replaced by a value
      BinTree SUT = new BinTree();
                                                                generated by our invariant generator in many cases.
      for(int j = 0; j < M; j++){
                                                                   Even using this simplistic version of triage, however, we
        int op = rand.nextInt(3);
                                                                can obtain results. Reading through the roughly 40K lines
        int value = rand.nextInt(20);
                                                                of non-comment C code in SpiderMonkey 1.6 would be a
        switch(op){
                                                                time-consuming task for a human, even ignoring the need
           case 0:
                                                                to resolve typedefs. The 11 functions chosen as possible
             SUT.add(value);
                                                                verification targets by the simple algorithm include some
             break;
                                                                unsuitable targets (including one case where the textual
           case 1:
                                                                type analysis fails to notice a complex compiler state
             SUT.remove(value);
                                                                structure parameter). A few functions are simple bit-
             break;
                                                                twiddling or offset-computing code that can be trivially
           case 2:
                                                                verified without invariants. The code in Figure 5 however
             SUT.find(value);
                                                                is of considerably more interest. It implements the Boyer-
             break;
                                                                Moore-Harspool substring-finding algorithm [13]. After
        }
                                                                resolving the types to ground C types and choosing string
        assert(SUT.RepOK());
                                                                sizes based on jsfunfuzz tests, we were able to incre-
      }
                                                                mentally increase loop bounds to not only verify memory
    }
                                                                safety for chosen strings, but to “discover” the worst case
     Figure 3: A simple random tester for the BinTree.          complexity of the algorithm, the point where unwinding
                                                                assertions held. When we introduce an off-by-one error
void main()                                                     into the code (a case that should not be found by our
{ int v1,v2,v3,v4; // symbolic inputs                           testing due to the values chosen for start, we believe),
                                                                CBMC instantly detects the error.
    /* Using calls for simplicity;                                 On the one hand, because the size of strings analyzed is
       in practice would encode structure                       relatively small, this is not a complete verification of the
       from Daikon invariants as a series                       Boyer-Moore-Horspool implementation in SpiderMonkey.
       of assumptions. */                                       On the other hand, in practice for bug finding, an informal
    add(v1);                                                    “small model” assumption suggests that most code that
    add(v2);                                                    works for all small inputs works for large inputs, at least
    add(v3);                                                    short of integer overflow problems. Note that the small
                                                                input size bounds in our verification are used to also gen-
    /* Invariant */                                             erate small array sizes, so we can detect memory safety
    assume(0<=br1 && br1<=2 &&                                  problems with small inputs, because our memory bounds
           0<=br2 && br2<=2);                                   are also artificially small due to the way we translate the
                                                                code into a verification problem. One problem with this
    remove(v4);                                                 approach is that when small inputs can lead to larger
    assert(repOK);                                              outputs, and this invariant is not detected, our approach
}                                                               might result in false positives. It remains to be seen how
                                                                important this is in practice.
           Figure 4: CBMC Harness for BinTree.                     That a Boyer-Moore-Horspool implementation is the
                                                                most interesting verification target detected by our initial
                                                                triage system is fitting. The problem of finding a substring
      that have a “specification” even without human in-        is often discussed (as in the Wikipedia entry for the
      tervention) and                                           algorithm) as the “needle in a haystack” problem with
   • do not take parameters or declare local variables that     the pattern to find called the “needle.” Our approach
      cannot be resolved to simple C types (int, short, long,   is essentially the search for model-checkable needles in
      void, and char).                                          the haystacks of large, complex software systems not
   This triage approach is both over-restrictive (in many       otherwise amenable to formal verification without large
cases functions taking structures or arrays as input can        investments of expert effort.
be handled easily) and not restrictive enough (it does not
filter out functions with recursion or references to global            IV. C ORE C HALLENGES AND F UTURE W ORK
values of “bad” types). In practice, we expect triage to          We speculate that while model checking cannot apply
require a deeper static analysis that includes more types       to as many functions as static analysis, our method may
and uses summaries of functions called by a function.           be of considerable value for bug detection because of the
jsint
js_BoyerMooreHorspool(const jschar *text, jsint textlen,
                          const jschar *pat, jsint patlen,
                          jsint start)
{
        jsint i, j, k, m;
        uint8 skip[BMH_CHARSET_SIZE];
        jschar c;


           JS_ASSERT(0 < patlen && patlen <= BMH_PATLEN_MAX);
           for (i = 0; i < BMH_CHARSET_SIZE; i++)
               skip[i] = (uint8)patlen;
           m = patlen - 1;
           for (i = 0; i < m; i++) {
               c = pat[i];
               if (c >= BMH_CHARSET_SIZE)
                    return BMH_BAD_PATTERN;
               skip[c] = (uint8)(m - i);
           }
           for (k = start + m;
                 k < textlen;
                 k += ((c = text[k]) >= BMH_CHARSET_SIZE) ? patlen : skip[c]) {
               for (i = k, j = m; ; i--, j--) {
                    if (j < 0)
                        return i + 1;
                    if (text[i] != pat[j])
                        break;
               }
           }
           return -1;
}

                             Figure 5: Verification target from Mozilla SpiderMonkey 1.6 source.


precision and complete exploration of model checking.            actual invariants from the test suites for our subject
However, the critical question is whether dynamic invari-        programs.
ants can actually produce accurate enough preconditions
to reduce the false positive rate to a manageable level.                                    R EFERENCES
Determining whether dynamic invariants over even poor
test suites can still find bugs for realistic systems requires   [1] M.A. Alipour and A. Groce. Extended program invariants: appli-
the development of a tool for automatic verification task            cations in testing and fault localization. In Proceedings of the 2012
triage. Our initial efforts suggest that this task is complex,       Workshop on Dynamic Analysis, pages 7–11. ACM, 2012.
                                                                 [2] R. Alur, P. Madhusudan, and W. Nam. Symbolic compositional ver-
though not infeasible. In particular, our early efforts to           ification by learning assumptions. In Computer Aided Verification,
triage C programs have shown that the first steps are                pages 289–292. Springer, 2005.
identifying code patterns that frustrate a particular model      [3] Armin Biere, Alessandro Cimatti, Edmund M. Clarke, and Yunshan
                                                                     Zhu. Symbolic model checking without BDDs. In Tools and
checker, and this requires a complete analysis of the                Algorithms for the Construction and Analysis of Systems, pages 193–
accessed data types and call graphs from each function               207, 1999.
for “bad” patterns, like complex recursive data structures       [4] S. Chaki, E. Clarke, A. Groce, S. Jha, and H. Veith. Modular veri-
                                                                     fication of software components in C. In International Conference
or system calls. We have identified some likely candidate            on Software Engineering, pages 385–395, 2003.
functions in the Mozilla JavaScript engine and SQLite,           [5] E. Clarke, D. Kroening, and F. Lerda. A tool for checking ansi-c
and plan to use these modest sized code bases to tune                programs. Tools and Algorithms for the Construction and Analysis
                                                                     of Systems, pages 168–176, 2004.
a method for handling larger programs with more com-
                                                                 [6] J.M. Cobleigh, G.S. Avrunin, and L.A. Clarke. Breaking up is hard
plex build environments. The next steps are continued                to do: an investigation of decomposition for assume-guarantee
development of the triage tools and experimentation with             reasoning. In Proceedings of the 2006 international symposium on
                                                                     Software testing and analysis, pages 97–108. ACM, 2006.
 [7] M.D. Ernst, J.H. Perkins, P.J. Guo, S. McCamant, C. Pacheco, M.S.
     Tschantz, and C. Xiao. The daikon system for dynamic detection of
     likely invariants. Science of Computer Programming, 69(1):35–45,
     2007.
 [8] J. Geldenhuys, M.B. Dwyer, and W. Visser. Probabilistic symbolic
     execution. In Proceedings of the 2012 International Symposium on
     Software Testing and Analysis, pages 166–176. ACM, 2012.
 [9] M. Gheorghiu Bobaru, C. Păsăreanu, and D. Giannakopoulou. Au-
     tomated assume-guarantee reasoning by abstraction refinement.
     In Computer Aided Verification, pages 135–148. Springer, 2008.
[10] M. Gheorghiu Bobaru, C. Păsăreanu, and D. Giannakopoulou. Au-
     tomated assume-guarantee reasoning by abstraction refinement.
     In Computer Aided Verification, pages 135–148. Springer, 2008.
[11] D. Giannakopoulou, Z. Rakamarić, and V. Raman. Symbolic
     learning of component interfaces. Static Analysis, pages 248–264,
     2012.
[12] Alex Groce, Gerard Holzmann, Rajeev Joshi, and Ru-Gang Xu.
     Putting flight software through the paces with testing, model
     checking, and constraint-solving. In International Workshop on
     Constraints in Formal Verification, pages 1–15, 2008.
[13] R. N. Horspool. Practical fast searching in strings. Software -
     Practice & Experience, 10(6):501–506, 1980.
[14] Anna Leach. Boffins zapped ’2,000 bugs’ from Curiosity’s 2
     MILLION lines of code. http://www.theregister.co.uk/2012/08/
     22/mars rover software coverity/.
[15] W. Visser, C.S. Păsăreanu, and R. Pelánek. Test input generation for
     Java containers using state matching. In Proceedings of the 2006
     international symposium on Software testing and analysis, pages
     37–48. ACM, 2006.
