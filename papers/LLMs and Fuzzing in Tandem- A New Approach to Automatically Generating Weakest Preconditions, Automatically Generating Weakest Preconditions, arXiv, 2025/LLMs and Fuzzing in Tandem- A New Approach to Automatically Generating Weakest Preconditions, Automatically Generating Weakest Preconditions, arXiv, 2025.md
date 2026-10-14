                                                      LLMs and Fuzzing in Tandem: A New Approach to
                                                       Automatically Generating Weakest Preconditions

                                                              Daragh King1*, Vasileios Koutavas1 and Laura Kovacs2
                                           1*
                                                Department of Computer Science and Statistics, Trinity College Dublin, Dublin, Ireland.
                                                               2
                                                                 Faculty of Informatics, TU Wien, Vienna, Austria.
arXiv:2507.05272v2 [cs.SE] 17 Dec 2025




                                                                *Corresponding author(s). E-mail(s): kingd6@tcd.ie;
                                                     Contributing authors: vasileios.koutavas@tcd.ie; laura.kovacs@tuwien.ac.at;


                                                                                              Abstract
                                                The weakest precondition (WP) of a program describes the largest set of initial states from which
                                                all terminating executions of the program satisfy a given postcondition. The generation of WPs is
                                                an important task with practical applications in areas ranging from verification to run-time error
                                                checking. This paper proposes the combination of Large Language Models (LLMs) and fuzz testing
                                                for generating WPs. In pursuit of this goal, we introduce Fuzzing Guidance (FG); FG acts as a means
                                                of directing LLMs towards correct WPs using program execution feedback. FG utilises fuzz testing
                                                for approximately checking the validity and weakness of candidate WPs, this information is then fed
                                                back to the LLM as a means of context refinement. We demonstrate the effectiveness of our approach
                                                on a comprehensive benchmark set of deterministic array programs in Java. Our experiments indicate
                                                that LLMs are capable of producing viable candidate WPs, and that this ability can be practically
                                                enhanced through FG.

                                                Keywords: Weakest Precondition, Fuzzing, Correctness, LLMs, Verification




                                         1 Introduction                                               for the method to behave as intended.1 Knowing
                                                                                                      the pre- and postconditions of a method suffice
                                         Pre- and postconditions are fundamental for-                 to ensure its correctness to external calling meth-
                                         malisms for specifying program behaviour, orig-              ods – thereby enabling compositional program
                                         inating from the seminal work of Floyd [1] and               reasoning.
                                         Hoare [2]. Beyond Hoare-logic itself, these for-                 There can be many pre- and postconditions for
                                         malisms are a cornerstone in many software engi-             a given method m, but finding the right ones is
                                         neering, verification, and debugging techniques;             crucial for effective compositional reasoning. If m’s
                                         these include design-by-contract [3], abstract               precondition is too permissive (allowing too many
                                         interpretation [4], program refinement [5], sym-             initial states) or its postcondition too restrictive
                                         bolic execution [6], and runtime assertion check-            (rejecting too many final states), reasoning about
                                         ing [7].
                                             The postcondition of a program method speci-
                                         fies the desired property of the program state upon            1
                                                                                                          In total correctness specifications, a precondition also guar-
                                         termination. On the other hand, the precondition             antees termination of the method; in this paper we restrict our
                                                                                                      attention to programs that terminate for any input.
                                         specifies the required property of the initial state


                                                                                                  1
m’s behaviour may fail. Conversely, if m’s pre-             context refinement. The benefits of this combined
condition is too restrictive or postcondition too           approach are:
permissive, reasoning about methods calling m               • Superior performance in WP generation : The
may fail.
                                                              combination of LLMs and FG can greatly
    This need for precision has led to the notion
                                                              improve the quality/correctness of generated
of a weakest precondition (WP), i.e. the most
                                                              WPs when compared to zero-shot prompting;
permissive precondition for which m’s executions
                                                              this is especially true for (typically) cheaper
lead to final states satisfying its postcondition.2
                                                              non-reasoning models (e.g. GPT-4o [33]),
The weakest precondition calculus [8] was the first
                                                              enabling them to achieve comparable perfor-
manual method for deriving the weakest precondi-
                                                              mance to their (typically) more expensive rea-
tion from a method’s code and desired postcondi-
                                                              soning counterparts (e.g. O4-mini [34]).
tion. Subsequent techniques have sought to auto-            • Increased scope : Unlike previous works in WP
matically derive preconditions, either sufficient
                                                              inference that rely on formal methods, our use
(though often not weakest) [9–23] or necessary
                                                              of LLMs for generating WPs has no inherent
ones [24]. However, since the problem is undecid-
                                                              limitation in the programs it can handle. This
able in the presence of loops, user intervention
                                                              increases the potential scope and use of WPs
remains an essential fallback.
                                                              in practice. Indeed, our experiments include
    Studies and tools regarding the generation of
                                                              programs which fall outside the scope of previ-
WPs (and their requisite loop invariants) typically
                                                              ous work – these include variants of problems
reside on the more mathematical side of computer
                                                              revolving around the use of binary search and
science, relying on formal methods. On the other
                                                              sorting (see the supplementary material link for
end of the spectrum lie more heuristic-based, data
                                                              example-four in Section 8).
driven fields, such as fuzz testing [25] and machine        • Model-driven evolution : Although the general
learning [26]. Fuzz testing generates pseudo ran-
                                                              performance progress of LLMs is not guar-
dom inputs for a program under test in an attempt
                                                              anteed, whatever evolutions do occur in the
to trigger buggy or unwanted behaviour. Fuzz
                                                              future will be readily reflected in our approach.
testing has seen far-reaching success [27], and is
                                                              Relying on LLMs enables this background-
actively deployed in industry [28]. While fuzz test-
                                                              improvement to materialise in our method for
ing has grown in popularity, machine learning has
                                                              WP generation.
given rise to LLMs [29].
    In recent years, LLMs have found extensive                  Section 2 describes the methodology of FG;
and successful applications to software engineer-           outlining a high-level structure of the programs
ing, including code generation [30], code repair [31]       used, the prompts utilised, and the constituent
and invariant inference [32]. Although LLMs suffer          phases of fuzz testing. Following this, Section 3
from inherent drawbacks (e.g. stochastic outputs,           depicts a motivating example; here, GPT-4o and
hallucinations, etc.), it is natural to question the        FG interact to produce the correct WP for a
extent to which these techniques can contribute to          particular program.
the inherently manual process of WP generation.                 Section 4 details our experimental analysis. We
    This paper broaches a new frontier in the               introduce the four benchmark sets of Java pro-
automatic generation of WPs. First, we employ               grams used in our work, and outline the LLM-FG
LLMs to act as generators for candidate WPs.                configurations utilised for generating WPs. Detail-
Second, we introduce Fuzzing Guidance (FG) as               ing our results, we explore if LLMs can generate
a means for refining these candidate WPs and                sensible WP candidates and whether FG can aid
steering LLMs towards generating correct WPs.               them in doing so by enabling iterative phases of
FG relies upon two distinct phases of fuzz test-            context refinement.
ing to validate and ensure the weakness of an                   Proceeding to the tail-end of the paper, we
LLM-generated WP; the results of these fuzzing              provide a discussion of our work in Section 5 –
phases are then fed back to the LLM as a means of           detailing the relevant threats to validity and the
                                                            limitations of our approach. Section 6 overviews
                                                            related work. Section 7 outlines future directions,
 2
     And its dual, the strongest postcondition.             and Section 8 concludes.


                                                        2
                                              Repair-Weakness Prompt
                                                    + Strong WP                                                     Context: You have the following Java program containing a method named 'foo'.
                                                                                                                    You must determine the weakest precondition for 'foo' so that:
Initial WP Prompt                                                                                   Likely
                                                   Validity            Likely Valid   Weakness                          - The method’s postcondition is always satisfied.
         +          LLM                                                                           Weakest
                                                   Fuzzing             Precondition    Fuzzing
      Program                                                                                    Precondition           - No exceptions or errors are reachable.
                           Repair-Valid Prompt
                          + Invalid Precondition                                                                    Task A: Identify this weakest precondition.
                                                                                                                    Task B: Create a public Java method named 'precondition' that checks this
                                                                                                                    weakest precondition.

                                                                                                                    Adhere to the following requirements:
Fig. 1 Fuzzing Guidance Workflow.                                                                                       - It must accept the same arguments as 'foo'.
                                                                                                                        - It must return 'false' if the precondition is not satisfied and 'true'
                                                                                                                        otherwise.

2 Method                                                                                                                - It may include a for loop if necessary.
                                                                                                                        - Before this method, provide a single brief comment describing the
                                                                                                                        precondition in pseudo-code.
                                                                                                                        - Integrate this 'precondition' method into the original Java program and
This section outlines our methodology for the gen-                                                                      return the complete updated program.

eration of Weakest Preconditions (WPs) using                                                                        Output Format: Return only the updated Java program (do not include any other
                                                                                                                    additional text), which includes
LLMs and Fuzzing Guidance (FG). The overar-                                                                             - The original 'foo' method - this should be unchanged.
                                                                                                                        - The newly added 'precondition' method.
ching workflow for this process can be seen in                                                                      Provide no additional explanations beyond the program code and the required
Fig 1 – the fuzzing phases and prompts depicted                                                                     comment. Reason through your solution internally.

are detailed in the Section 2.2 and Section 2.3
respectively.                                                                                                       Fig. 2 LLM prompt to generate WPs, i.e. the initial-WP
                                                                                                                    prompt.
2.1 Input Programs
                                                                                                                    2.2.1 Validity-fuzzing
The input programs considered for this work fol-
low a common high-level structure (an example                                                                       This phase of fuzzing is employed to help check
can be seen in Fig 5 in Section 3). Specifically, the                                                               that a candidate WP is valid. A candidate WP
programs considered are implemented in Java and                                                                     is valid if all initial program states which satisfy
feature a deterministic looping computation over                                                                    the WP wind up satisfying the program’s given
arrays; these programs consist of:                                                                                  postcondition after it is executed.
• A single ‘static int’ method named ‘foo’ which                                                                        Validity-fuzzing attempts to generate pseudo-
                                                                                                                    random initial states which adhere to a candidate
  accepts three arrays a, b, c as inputs.
• A postcondition implemented in code which                                                                         WP, but which do not satisfy a program’s post-
                                                                                                                    condition; i.e. they cause the program to throw
  checks a desired property for some subset of
                                                                                                                    an exception. If such an input is found then we
  the input arrays; an exception is thrown if the
                                                                                                                    can conclude that the candidate WP is not valid;
  postcondition is not satisfied.
• A successful return value of 0.                                                                                   otherwise we can posit that the WP is likely-valid.

   The looping computations contained within                                                                        2.2.2 Weakness-fuzzing
each program range over a varied set of tasks, e.g.
array copying, arithmetic, sorting, search, etc. For                                                                Given a WP that is already deemed to be likely-
example, the program in Fig 5 of Section 3, copies                                                                  valid, weakness-fuzzing attempts to ensure that
elements of array a into array b.                                                                                   the same WP is likely-weakest. A candidate WP is
   Additionally, it is worth noting that each pro-                                                                  weakest if it accounts for all initial program states
gram’s single method is named ‘foo’ to prevent                                                                      which result in the program’s postcondition being
any unnecessary direction being given to the LLM                                                                    satisfied after it is executed.
being prompted.                                                                                                         Weakness-fuzzing attempts to generate
                                                                                                                    pseudo-random initial states which do not adhere
                                                                                                                    to a candidate WP, but which do satisfy a pro-
2.2 Fuzzing Guidance Phases                                                                                         grams postcondition; i.e. no exception is thrown.
FG utilises the JQF fuzz testing tool [35] to                                                                       If such an input is found then we can conclude
carry out two distinct phases of fuzz testing                                                                       that the candidate WP is not weakest; otherwise
for candidate WPs. These phases are termed                                                                          we can posit that the WP is likely-weakest.
validity-fuzzing and weakness-fuzzing ; the outputs
of which act as feedback to the LLM being utilised
for WP generation.



                                                                                                                3
You have a Java program that contains:                                               You have a Java program that contains:
    - A method called 'foo', which may reach an error state under certain                - A method called 'foo', which may reach an error state under certain
    inputs.                                                                              inputs.
    - A method called 'precondition', intended to represent the weakest                  - A method called 'precondition', intended to represent the weakest
    precondition for 'foo'.                                                              precondition for 'foo'.

The current implementation of 'precondition' is incorrect. Specifically, there       The current implementation of 'precondition' is incorrect. Specifically, there
is a known set of input values for which 'precondition' returns 'true'               is a known set of input values for which 'foo' returns successfully and
(indicating the precondition is satisfied), but passing these same inputs to         'precondition' returns 'false' - indicating that the inputs do not satisfy the
'foo' actually triggers an error state. The aforementioned inputs follow:            given precondition, but still result in a succesful execution of 'foo'.
[Insert Inputs]                                                                      This implies that the precondition defined by the 'precondition' method may
                                                                                     not be weakest. The aforementioned inputs follow:
Task:                                                                                [Insert Inputs]
    1. Analyze the existing 'foo' method and the incorrect 'precondition'
    method.                                                                          Task:
    2. Determine why the current 'precondition' method fails to exclude the              1. Analyze the existing 'foo' method and the incorrect 'precondition'
    problematic inputs.                                                                  method.
    3. Rewrite or adjust 'precondition' so that it correctly represents the              2. Determine why the current 'precondition' method fails to correctly
    true                                                                                 account for the above inputs.
    weakest precondition for 'foo', ensuring that when 'precondition' returns            3. Rewrite or adjust 'precondition' so that it correctly represents the
    'true', 'foo' will not reach an error with the same inputs.                          true weakest precondition for 'foo'.

Goal:                                                                                Goal:
Provide the corrected 'precondition' method so that 'foo' never encounters an        Provide the corrected 'precondition' method so that 'foo' never encounters
error when the corrected 'precondition' returns 'true'.                              an error when the corrected 'precondition' returns 'true', and that the
                                                                                     corrected 'precondition' method truly represents the weakest precondition for
Output Format: Return only the updated Java program (do not include any other        'foo'.
additional text), which includes
    - The original 'foo' method - this should be unchanged.                          Output Format: Return only the updated Java program (do not include any other
    - The corrected 'precondition' method.                                           additional text), which includes
                                                                                         - The original 'foo' method - this should be unchanged.
Provide no additional explanations beyond the program code and the required              - The corrected 'precondition' method.
comment. Reason through your solution internally.
                                                                                     Provide no additional explanations beyond the program code and the required
                                                                                     comment. Reason through your solution internally.


Fig. 3 LLM prompt to repair or replace invalid WPs, i.e.
the repair-validity prompt.                                                          Fig. 4 LLM prompt to repair or replace strong WPs, i.e.
                                                                                     the repair-weakness prompt.
2.3 Prompting
                                                                                         Besides intention and functionality, there are
Our method for generating WPs relies on three
                                                                                     additional aspects to our prompts which are worth
underlying prompts for LLM interactions; these
                                                                                     discussing. Each of our prompts ends with ‘Rea-
will be referred to as the initial-WP prompt
                                                                                     son through your solution internally.’. This is
(Fig. 2), the repair-validity prompt (Fig. 3), and
                                                                                     done to encourage the LLM to utilise a chain-of-
the repair-weakness prompt (Fig. 4).
                                                                                     thought [36] process that does not reveal these
    The initial-WP prompt tasks the LLM with
                                                                                     ‘thoughts’ in the corresponding output; this makes
WP generation for a particular program. In isola-
                                                                                     the parsing of LLM’s responses more straightfor-
tion (i.e. when FG is not employed) this prompting
                                                                                     ward. One might argue that this restriction on
method can be viewed as a zero-shot prompting
                                                                                     the LLM’s outputs might affect how they can
strategy [36]. The outcomes to this zero-shot strat-
                                                                                     be interpreted; we mitigate this issue through
egy are revealed through the results for the GPT-
                                                                                     the use of the following phrase in our initial-
4o and O4-mini experimental configurations in
                                                                                     WP prompt – ‘provide a single brief comment
Section 4.
                                                                                     describing the precondition in pseudo-code.’. This
    The repair-validity and repair-weakness
                                                                                     addendum ensures that 1) there is an easily-read
prompts expect to deal with an already existing
                                                                                     reasoning behind the LLM’s response, and 2) there
candidate WP. The repair-validity prompt pro-
                                                                                     exists a counter-point to the code generated when
vides the LLM with inputs which highlight that
                                                                                     it does not align with expectations.
the current candidate WP is not valid (as derived
through validity-fuzzing, Section 2.2.1); the LLM
is then tasked with repairing the current WP or                                      2.4 Fuzzing Guidance Cycles
replacing it with a newly generated WP. Simi-                                        The outputs derived from the individual validity-
larly, the repair-weakness prompt provides the                                       and weakness-fuzzing phases (Section 2.2) are
LLM with inputs which highlight that the current                                     combined with their respective repair prompts
candidate WP is not the weakest possible (as                                         (Section 2.3) in an effort to steer the LLM
derived through weakness-fuzzing, Section 2.2.2);                                    towards generating higher-quality candidate WPs
the same task of WP repair or generation is then                                     in terms of validity and weakness respectively.
also put forth to the LLM.                                                           This describes the essence of FG, but a little more
                                                                                     needs to be said when considering how it is used


                                                                                 4
public static int foo(int[] a, int[] b, int[] c) {          initial-WP prompt (Fig. 2). This results in the fol-
    int N = a.length;
    if (N == 0 || b.length != N) {                          lowing ‘precondition’ method being generated (i.e.
        throw new RuntimeException();                       the initial candidate WP) in Fig. 6.
    }

    int i = 0;
    while (i < N) {                                         // Precondition: 'a' and 'b' must have the same
        b[i] = a[i];                                        // non-zero length,
        i++;                                                // and 'c' should be at least of length 'a'.
    }                                                       public static boolean precondition
                                                            (int[] a, int[] b, int[] c) {
    int[] b_clone = b.clone();                                  return a.length > 0 && a.length == b.length
    sort(b_clone);                                              && c.length >= a.length;
                                                            }
    i = 0;
    while (i < N) {
        if (b[i] != b_clone[i])                             Fig. 6 Initial candidate WP generated for P (Fig. 5).
            throw new RuntimeException();
        i++;
    }

    return 0;                                               3.2 Ensuring Validity
}
                                                            Given the initial candidate WP generated (Fig. 6)
Fig. 5 Example program P from the ‘Sorting’ benchmark       for program P , we can now proceed to checking
set (Section 4.1).                                          its validity using validity-fuzzing (Section 2.2.1).
                                                            Validity-fuzzing quickly highlights an issue with
in practice – we must define how the two phases of          the given candidate; the following inputs satisfy
FG combine to define an FG-cycle. An FG-cycle               the candidate WP (i.e. ‘precondition’ in Fig. 6
consists of:                                                returns true) but ultimately result in a failing
                                                            execution of P .
1. A maximum of X iterations of validity-fuzzing
   and repair.
2. A single iteration of weakness-fuzzing and               int[] a = {1401919545, 267222264, 1358618764};
                                                            int[] b = {739288021, 776171394, -594227544};
   repair.                                                  int[] c = {427235608, -506959485, 1997723943,
                                                                      -498207265, 733576341};
Step 2 follows the successful completion of Step
1 (cf. Fig. 1). Multiple FG-cycles can be used in               The program P , along with the invalid candi-
practice to generate WPs.                                   date WP and the preceding inputs, are integrated
                                                            into the repair-validity prompt (Fig. 3); using this
3 Motivating Example                                        prompt the LLM is tasked with amending the
                                                            invalid candidate WP. This results in Fig. 7. Upon
This section outlines the generation of a correct           inspection, this ‘precondition’ method appears to
weakest precondition using an LLM (GPT-4o [33])             be a valid candidate for P ’s WP; another round
and Fuzzing Guidance (FG). We will do so for an             of validity fuzzing provides evidence that this is
example program P (Fig. 5) from our ‘Sorting’               so. Now, we must attempt to see if this candidate
benchmark set (Section 4.1). (See the supplemen-            WP is likely-weakest.
tary material link for example-one in Section 8).
   Before proceeding, it is worth re-noting that            3.3 Ensuring Weakness
the comments in the following code snippets are
generated by the LLM in question (Section 2.3).             Through validity-fuzzing, we now have a candi-
                                                            date WP (Fig. 7) that we believe to be a valid
3.1 Initial Weakest Precondition                            precondition for the program P . Our goal now
                                                            is to check the weakness of the candidate WP
    Generation
                                                            with weakness-fuzzing (Section 2.2.2). Weakness-
First, we prompt the LLM to generate its initial            fuzzing proceeds to highlight a problem with the
candidate WP by appending program P to the                  current candidate WP; the following inputs do not
                                                            satisfy the WP (i.e. i.e. ‘precondition’ in Fig. 7



                                                        5
// Precondition: 'a' and 'b' must have the same               // Precondition: 'a' and 'b' must have the same
// non-zero length,                                           // non-zero length,
// 'c' should be at least of length 'a',                      // and 'c' must have a length that is
// and 'a' must be sorted in non-decreasing order             // irrelevant to the execution success of 'foo'.
// to ensure 'b' remains sorted.                              // Additionally, 'a' naturally
public static boolean precondition                            // becomes sorted when it has identical elements.
(int[] a, int[] b, int[] c) {                                 public static boolean precondition
    if (a.length == 0                                         (int[] a, int[] b, int[] c) {
    || a.length != b.length                                       return a.length > 0 && a.length == b.length;
    || c.length < a.length) {                                 }
        return false;
    }
                                                              Fig. 8 A step backwards for FG? Another candidate WP
    for (int i = 0; i < a.length - 1; i++) {                  for P (Fig. 5)
        if (a[i] > a[i + 1]) {
            return false;
        }
    }
                                                              3.4 Ensuring Validity and Weakness
    return true;
                                                                  Again
}
                                                              The current candidate WP (Fig. 8) must undergo
                                                              validity-fuzzing again. As before in Section 3.2,
Fig. 7 A likely-valid but too-strong candidate WP for P
(Fig. 5).
                                                              validity-fuzzing finds a set of inputs which high-
                                                              light the invalidity of the current candidate (these
                                                              inputs are omitted for brevity). Once again, the
returns false) but result in a successful execution           repair of the current candidate WP must take
of P :                                                        place with the repair-validity prompt. This pro-
                                                              cess results in the following candidate WP:
int[] a = {-1286467063};
int[] b = {0};
int[] c = {};                                                 // Precondition: 'a' and 'b' must have the same
                                                              // non-zero length,
                                                              // and 'a' must be sorted in non-decreasing order,
                                                              // since 'b' is a direct clone of 'a' before
     By accounting for the preceding inputs and               // sorting the clone.
                                                              public static boolean precondition
inspecting P again, we can see that the restriction           (int[] a, int[] b, int[] c) {
on the input array c in the current candidate WP                  if (a.length == 0 || a.length != b.length) {
                                                                      return false;
(Fig. 7) is unnecessary. Therefore, through the                   }
processes of validity-fuzzing and weakness-fuzzing,
                                                                  for (int i = 0; i < a.length - 1; i++) {
we can determine that our current candidate WP                        if (a[i] > a[i + 1]) {
is likely a valid precondition for P , but that it is                     return false;
                                                                      }
demonstrably not the weakest (i.e. it is too strong)              }
because of the unnecessary condition on the length
                                                                  return true;
of c.                                                         }
     The program P , along with the strong can-
didate WP and the preceding weakness-fuzzing                  Fig. 9   A likely-valid and -weakest WP for P (Fig. 5).
outputs, are integrated into the repair-weakness
prompt (Fig. 4); this prompt tasks the LLM
with amending the strong WP – resulting in the                    Given the latest candidate WP in Fig. 9,
candidate WP of Fig. 8.                                       validity-fuzzing and weakness-fuzzing both suc-
     Immediately we can observe that there appears            ceed in succession; therefore this candidate is
to be something amiss with the latest candidate               likely-valid and likely-weakest. Through manual
WP (Fig. 8). It appears simpler than the can-                 inspection we can see that this is, in fact, the
didate in Fig. 7, and more akin to the invalid                correct WP for program P .
candidate depicted in Fig. 6 (although it does do
away with the unnecessary restraints on the array             3.5 Conclusion
c mentioned previously). We must undergo valid-
                                                              Overall, we can see from this example how FG can
ity fuzzing again to ensure that the quality of the
                                                              enable the generation of correct WPs. Through
candidate WP has not regressed.
                                                              several bouts of back-and-forth between LLM


                                                          6
interations and different phases of fuzz testing, we           Contribution of FG : as described in Section 2,
arrived at a candidate WP that is correct.                 FG attempts to steer the LLM towards generating
                                                           correct WPs through program execution feedback.
3.6 Additional Remarks                                     We are interested in observing how and when FG
                                                           is deployed, and whether or not it can mean-
Notice that P (Fig. 5) calls an external method            ingfully guide the LLM in the aforementioned
‘sort’, and that no additional information was pro-        goal.
vided to the LLM about this method. Despite this,              These criteria will be discussed in the per-
the approach taken here has arrived at the correct         configuration performance summaries provided in
WP for P – from this, we can conclude that LLMs            Section 4.4.
can reason about unknown but well-understood
methods like ‘sort’.
    The above phenomena is of practical benefit
                                                           4.1 Benchmark Sets
in terms of prompting, but there is also a dan-            This work utilises four distinct sets of bench-
ger of missing important information regarding             mark programs. Each program within these sets
the behaviour of these unspecified method calls. If        is implemented in Java and follows the high-level
such a concern exists, one could augment the code          program structure outlined in Section 2.1. The fol-
with the pre- and post-conditions of these meth-           lowing points will give a brief overview of each
ods, allowing the LLM reason more robustly in a            set:
compositional manner.
                                                           • ‘Existential’ benchmarks: this set contains 20
                                                             programs; the correct WPs for the programs of
4 Evaluation of Weakest                                      this benchmark set require existential quantifi-
  Precondition Generation                                    cation over the array content. For example, a
                                                             description of a correct WP for some program
The core focus of this work is to deploy LLMs and            P in this set might look like – ‘there exists a
fuzz testing towards the task of generating weak-            valid index i for the input array a such that
est preconditions (WPs); the method employed                 a[i] = 100’.
here is outlined in detail in Section 2 – in brief,        • ‘Universal’ benchmarks: this set contains 36
LLM prompting for WP generation is augmented                 programs; the correct WPs for the programs of
with Fuzzing Guidance (FG) in order to steer                 this benchmark set require universal quantifi-
the LLM toward generating correct WPs. In this               cation over the array content. For example, a
section we outline our results pertaining to this            description of a correct WP for some program P
goal, comparing the results of WP generation with            in this set could look like – ‘for all valid indices
and without FG. In assessing and presenting these            i of the input array b, b[i] = 2i’.
results we are primarily concerned with the three          • ‘Sorting’ benchmarks: this set contains 8 pro-
following criteria: Correctness, Stability, and the          grams. The computations performed in each
Contribution of FG.                                          program feature sorting in some manner. For
    Correctness : for a particular program, the cor-         example, the program in Fig 5 (of Section 3)
rectness of a generated WP is defined in relation            features a sorted array in its postcondition.
to the program’s ground-truth WP. These ground-            • ‘Search’ benchmarks: this set contains 6 pro-
truth WPs are known a priori (through manual                 grams; each of which feature binary-search over
derivation) and the comparison with generated                an input array. Again, these examples express
WPs is performed manually; if a generated WP                 properties with both existential and universal
is deemed semantically equivalent to its ground-             quantification over the array content.
truth counter part then it is correct.
    Stability : we complete k iterations of WP gen-        4.2 Experimental Set Up and
eration for each benchmark set and experimental
                                                               Configurations
configuration. This allows us to look for con-
sistency in the WPs generated and assess the               The set up for our experimental evaluations can
stability of both the LLM outputs and FG usage.            be described through the following features:



                                                       7
Table 1 Resulting statistics for each benchmark set and configuration, obtained across k = 5 iterations.

                                                               # Correct WPs             FG Usage            FG Success
     Configuration     Benchmark           # Programs    Min–Max (Avg., Avg.%)         Min–Max (Avg.)      Min–Max (Avg.)

                       Existential                  20        10 – 12 (11, 55.00 %)                   –                   –
                       Universal                    36      24 – 27 (26.2, 72.78 %)                   –                   –
     GPT-4o
                       Sorting                       8         2 – 4 (2.8, 35.00 %)                   –                   –
                       Search                        6         4 – 5 (4.2, 70.00 %)                   –                   –

                       Existential                  20      16 – 17 (16.6, 83.00 %)            5 – 7 (6)         5 – 6 (5.6)
                       Universal                    36        32 – 34 (33, 91.67 %)         6 – 10 (7.8)         6 – 9 (6.8)
     GPT-4o-FG
                       Sorting                       8         4 – 6 (5.4, 67.50 %)          4 – 6 (4.6)         2 – 4 (2.6)
                       Search                        6         5 – 6 (5.8, 96.67 %)          1 – 2 (1.8)         1 – 2 (1.6)

                       Existential                  20      18 - 19 (18.6, 93.00 %)                   –                   –
                       Universal                    36      34 - 35 (34.8, 96.67 %)                   –                   –
     O4-mini
                       Sorting                       8         7 - 8 (7.8, 97.50 %)                   –                   –
                       Search                        6         5 - 6 (5.4, 90.00 %)                   –                   –

                       Existential                  20           20 - 20 (20, 100 %)         1 – 2 (1.4)         1 – 2 (1.4)
                       Universal                    36           36 - 36 (36, 100 %)         1 – 2 (1.2)         1 – 2 (1.2)
     O4-mini-FG
                       Sorting                       8              8 - 8 (8, 100 %)         0 – 1 (0.2)         0 – 1 (0.2)
                       Search                        6              6 - 6 (6, 100 %)         0 – 1 (0.6)         0 – 1 (0.6)




• LLMs: We employ GPT-4o [33] and O4-                            4.3.1 Tables
  mini [34] from OpenAI. These represent perfor-
                                                                 The results of Table 1 depict a set of performance
  mant and accessible LLMs from the categories
                                                                 statistics obtained from k = 5 iterations of eval-
  of non-reasoning and reasoning models respec-
                                                                 uations. The majority of the tables headings are
  tively.
                                                                 self-explanatory, though we believe some clarifi-
• Benchmark Sets: The four sets of benchmark
                                                                 cation regarding ‘FG Usage’ and ‘FG Success’ is
  programs used are described in Section 4.1.
                                                                 warranted.
  The structure of these programs follows the
                                                                     The ‘FG Usage’ statistics denote the min, max,
  description outlined in Section 2.1.
                                                                 and average number of programs where FG was
• Number of Iterations k : This defines the number
                                                                 employed in an attempt to direct the LLM in the
  of times WP-generation occurs for each pro-
                                                                 task of WP generation. For example, on the ‘Uni-
  gram in each benchmark set. We fix k = 5 for
                                                                 versal’ benchmark set, GPT-4o-FG employed FG
  all of the experiments described.
                                                                 for a minimum of 6 programs, a maximum of 10
• Fuzzing Parameters: These parameters influ-
                                                                 programs, and an average of 7.8 programs per
  ence how FG is deployed. We allow a maximum
                                                                 iteration.
  of 10 attempts of validity-fuzzing (Section 2.2.1)
                                                                     The ‘FG Success’ statistics denote the min,
  for each FG-cycle (Section 2.4). We also set a
                                                                 max, and average number of programs where FG
  maximum fuzzing time of 10s for each validity-
                                                                 was employed successfully – i.e. where FG enabled
  and weakness-fuzzing (Section 2.2.2) invoca-
                                                                 the generation of a correct WP. For example,
  tion.
                                                                 on the ‘Existential’ benchmark set, GPT-4o-FG
   Overall, the four LLM and FG configurations                   employed FG successfully for a minimum of 5 pro-
investigated are: GPT-4o without FG (GPT-4o ),                   grams, a maximum of 6 programs, and an average
GPT-4o with FG (GPT-4o-FG ), O4-mini with-                       of 5.6 programs per iteration.
out FG (O4-mini ), and O4-mini with FG (O4-                          From this table alone, we can already conclude
mini-FG ). The labels in parenthesis correspond                  that the use of FG has led to a marked improve-
to the configuration labels in both the plots of                 ment in the generation of correct WPs; this is
Fig.(s) 10, 11, 12, 13 and Table 1.                              true across all benchmark sets and LLMs used.
                                                                 For GPT-4o (a non-reasoning model), FG provides
4.3 Description of the Results Table                             the greatest improvements in correctness; while in
    and Figures                                                  the case of O4-mini (a reasoning model), FG has
                                                                 enabled the achievement of a perfect correctness
Before delving into the summaries of the obtained                score across every iteration.
results, this section provides a brief descriptive aid
to the figures and tables referenced in Section 4.4.


                                                           8
                               WP Correctness Statistics for 'Existential' Benchmarks (N=20)                                                                                                          WP Correctness Statistics for 'Universal' Benchmarks (N=36)
                                                              (a)                                                               (b)                                                                                             (a)                                                                (b)
                         20                                                                                                                                                                   36
                                                                                                                                                                                              34
                         18                                                                                                                                                                   32
                                                                                                                                                                                              30
                         16                                                                                                                                                                   28
    No. of Correct WPs




                                                                                                                                                                         No. of Correct WPs
                         14                                                                                                                                                                   26
                                                                                                                                                                                              24
                         12                                                                                                                                                                   22
                                                                                                                                                                                              20
                         10                                                                                                                                                                   18
                                                                                                                                                                                              16
                          8                                                                                                                                                                   14
                                                                                                                                                                                              12
                          6                                                                                                                                                                   10
                          4                                                                                                                                                                    8
                                                                                                                                                                                               6
                          2                                                                                                                                                                    4
                                                                                                                                                                                               2
                          0                                                                                                                                                                    0
                                                              (c)                                                               (d)                                                                                             (c)                                                                (d)
                    100                                                                                100        100          100         100        100                                100                                                                          100          100            100           100          100
                                                                                                             95         95                                  95                                                                                                                           97.2           97.2          97.2         97.2
                                                                                                                                                                                                                              94.4                                          94.4
                     90                                                                                                              90          90                                       90       91.7
                                                                                                                                                                                                                88.9
                                                                                                                                                                                                                                          91.7          91.7
                              85             85                                          85
                     80                                      80            80                                                                                                             80
                                                                                                                                                                                                          75           75            75
 % of Correct WPs




                                                                                                                                                                      % of Correct WPs
                     70                                                                                                                                                                   70                                                     72.2
                                                                                                                                                                                                                                                               66.7
                     60                               60                                                                                                                                  60
                                       55                                           55            55
                     50                                               50                                                                                                                  50
                     40                                                                                                                                                                   40
                     30                                                                                                                                                                   30
                     20                                                                                                                                                                   20
                     10                                                                                                                                                                   10
                      0                                                                                                                                                                    0
                                   1              2               3             4             5          1          2            3           4          5                                             1            2             3           4             5            1            2              3             4            5
                                                           Iterations                                                        Iterations                                                                                     Iterations                                                          Iterations

                                            GPT-4o-FG                           GPT-4o                  O4-mini-FG                        O4-mini                                                              GPT-4o-FG                         GPT-4o                O4-mini-FG                              O4-mini

Fig. 10 WP correctness statistics for the ’Existential’                                                                                                              Fig. 11 WP correctness statistics for the ’Universal’
benchmark set, in absolute and relative terms.                                                                                                                       benchmark set, in absolute and relative terms.


4.3.2 Figures                                                                                                                                                        along with some observations – Table 1 is implic-
                                                                                                                                                                     itly referenced throughout.
Fig.(s) 10, 11, 12, 13 depict the correctness results
obtained for each benchmark set and iteration.
Each of these figures contains four plots (a)-(d).
                                                                                                                                                                     4.4.1 GPT-4o without FG (GPT-4o)
    Plots (a) and (b) outline the number of correct                                                                                                                  This configuration resulted in the lowest average
WPs generated; these line graphs can aid us in                                                                                                                       correctness results for all benchmark sets. We can
gleaning information about the correctness results                                                                                                                   also observe a wide variance here – with an aver-
achieved per iteration and observe whether or not                                                                                                                    age correctness percentage of 35% and 72.78%
they are stable. For example, consider the line                                                                                                                      respectively, GPT-4o performs poorly at attain-
graph for GPT-4o-FG in plot (a) of Fig. 11, this                                                                                                                     ing the correct WPs for the ‘Sorting’ benchmarks
shows us that the number of correct WPs gener-                                                                                                                       while performing relatively well on the ‘Universal’
ated by this config on the ‘Universal’ benchmark                                                                                                                     benchmarks. There is also evidence to suggest that
set hovers between 32 and 34 (out of a possible                                                                                                                      the results of this set-up are consistent; this can be
36) – indicating result stability.                                                                                                                                   seen in the relative similarity of the min and max
    Plots (c) and (d) portray the same correct-                                                                                                                      number of correct WPs generated per benchmark
ness information in terms of percentages; these bar                                                                                                                  set – as a result, we can conclude that GPT-4o
charts enable us to more clearly see the relative                                                                                                                    is consistently incorrect also. This notion of con-
performance differences between the experimen-                                                                                                                       sistent incorrectness is also evident in plots (a) of
tal configurations. For example, observe the bar                                                                                                                     Fig. 10 and Fig. 11 as the line-graphs appear rel-
chart for O4-mini in plot (d) of Fig. 10, this                                                                                                                       atively stable. When we look at the same plots in
shows us that the percentage of correct WPs gen-                                                                                                                     Fig. 12, and Fig. 13, we can observe a more erratic
erated by O4-mini on the ‘Existential’ benchmark                                                                                                                     performance (exacerbated by the small size of the
set always underperforms O4-mini-FG in each                                                                                                                          corresponding benchmark sets).
iteration.
                                                                                                                                                                     4.4.2 GPT-4o with FG (GPT-4o-FG)
4.4 Result Summaries per                                                                                                                                             Through the use of FG we can see how the per-
    Configuration                                                                                                                                                    formance of the base-line GPT-4o config can be
Resulting statistics for each benchmark set and                                                                                                                      significantly improved upon. This is made evi-
experimental configuration can be seen in Table 1.                                                                                                                   dent by the fact that GPT-4o-FG achieves higher
The following provides a summary of these results,                                                                                                                   average correctness results than GPT-4o across


                                                                                                                                                                 9
                                                                                                     WP Correctness Statistics for 'Sorting' Benchmarks (N=8)
all benchmark sets. Additional evidence that FG                                                                            (a)                                                                  (b)
is responsible for this performance boost can be                                       8
                                                                                       7
seen in the ‘FG Success’ results. For example, the




                                                                  No. of Correct WPs
                                                                                       6
‘Sorting’ benchmark set sees the largest increase                                      5
                                                                                       4
in average correctness (from 35% for GPT-4o to                                         3
67.50% for GPT-4o-FG ) and this coincides with                                         2

the proportionally largest average value for ‘FG                                       1
                                                                                       0
Success’. Another point in support of the efficacy                            100
                                                                                                                           (c)
                                                                                                                                                                   100 100      100 100
                                                                                                                                                                                                (d)
                                                                                                                                                                                               100 100       100 100   100

of FG can be seen through the consistent superi-                               90
                                                                                                                                                                                                                             87.5
                                                                               80
ority of GPT-4o-FG when compared to GPT-4o ;                                               75             75              75




                                                           % of Correct WPs
                                                                               70
                                                                               60                                                                    62.5
this is portrayed clearly in plots (a) and (c) of                              50                                  50                  50

Fig.(s) 10, 11, 12, 13                                                         40
                                                                                                                                37.5                        37.5
                                                                               30
                                                                                                    25                                          25
                                                                               20
4.4.3 O4-mini without FG (O4-mini )                                            10
                                                                                0
                                                                                                1              2               3            4           5            1            2              3             4         5
                                                                                                                        Iterations                                                           Iterations
Even without the use of FG, O4-mini performs
exceptionally well in the task of generating cor-                                                        GPT-4o-FG                            GPT-4o                O4-mini-FG                              O4-mini
rect WPs – in fact, the lowest average correctness        Fig. 12 WP correctness statistics for the ’Sorting’ bench-
result for O4-mini is 90.00% (on the ‘Search’             mark set, in absolute and relative terms.
benchmark set). When considering experimental
configurations that do not use FG, the superiority                                                   WP Correctness Statistics for 'Search' Benchmarks (N=6)
                                                                                                                           (a)                                                                  (b)
of O4-mini in this problem setting is reinforced
                                                                                       6
by observing that the lowest average correctness
                                                                  No. of Correct WPs

                                                                                       5
score for O4-mini (90.00% on the ‘Search’ bench-                                       4
mark set) is still higher than the highest average                                     3
correctness score achieved by GPT-4o (72.78%                                           2
on the ‘Universal’ benchmark set). Although O4-                                        1

mini is dominant over GPT-4o, GPT-4o-FG can                                            0
                                                                                                                           (c)                                                                  (d)
                                                                              100
appear to give O4-mini a ‘run for its money’ –                                 90
                                                                                           100            100             100                        100           100          100            100           100 100   100 100



this is evidenced by comparable average correct-                               80                               83.3                   83.3                              83.3         83.3           83.3
                                                           % of Correct WPs




                                                                               70
ness scores for each benchmark set apart from                                  60
                                                                                                 66.7                           66.7          66.7          66.7


                                                                               50
‘Sorting’. This comparable performance between                                 40
GPT-4o-FG and O4-mini is further highlighted                                   30
                                                                               20
in each relevant plot of Fig.(s) 10, 11, 12, 13.                               10
                                                                                0
                                                                                                1              2               3            4           5            1            2              3             4         5
                                                                                                                        Iterations                                                           Iterations
4.4.4 O4-mini with FG (O4-mini-FG)
                                                                                                         GPT-4o-FG                            GPT-4o                O4-mini-FG                              O4-mini
When O4-mini is enabled with FG we can see
that the correct WP is attained for every program,        Fig. 13 WP correctness statistics for the ’Search’ bench-
                                                          mark set, in absolute and relative terms.
in every benchmark set, and for every iteration.
Similar to what was observed in GPT-4o-FG ’s
summary (Section 4.4.1), the greatest increase in         value swap between two variables in their respec-
average correctness (over the corresponding base-         tive loop computations (see the supplementary
line configuration O4-mini ) also coincides with          material link for example-two in Section 8). In
the largest proportional value of ‘FG Success’.           each instance, GPT-4o produced a candidate WP
                                                          which failed to account for this swapping of values
4.5 Notable Cases                                         – this was true for every evaluation carried out; in
                                                          the end, GPT-4o never generated a correct WP
4.5.1 GPT-4o Can’t Swap                                   for these programs.
                                                              Another interesting point regarding the afore-
This case concerns three programs from the ‘Exis-
                                                          mentioned programs is that FG generally did not
tential’ benchmark set and the GPT-4o config-
uration. These three programs each perform a


                                                     10
help. The WPs that were required by these pro-               we have significantly reduced the risk of this threat
grams postconditions were complex enough that                by creating our benchmark programs from scratch,
validity-fuzzing (Section 2.2.1) could not produce           and hosting them in private repositories.
any corresponding inputs for testing. This prob-                 As is common with many empirical studies in
lem arises due to the random-input generators of             software engineering, our work is inherently lim-
the underlying fuzz testing tool JQF [35]. This              ited by the scope of the experimental benchmarks
phenomena resulted in validity-fuzzing phases                used. We attempted to alleviate this concern
‘passing’ with invalid candidate WPs. Here, the              by ensuring that our benchmark programs cov-
combined inadequacies of GPT-4o and FG led to                ered a range of common programming operations
a perfect storm for poor performance.                        and tasks, e.g. arithmetic, sorting, search, loop-
                                                             ing computations, etc. However, we have only
4.5.2 O4-mini’s Trouble with Integer                         explored relatively small programs operating over
      Arithmetic                                             integer arrays. A more extensive experimentation
                                                             with real code is necessary to support the prac-
This example regards a program in the ‘Universal’            tical benefits of our technique, which we leave to
benchmark set (see the supplementary material                future work.
link for example-three in Section 8). Here, O4-
mini produced a candidate WP that is correct
for mathematical arithmetic, but that is actu-               6 Related Work
ally invalid when considering integer arithmetic in
                                                             The combination of LLMs with formal meth-
Java. The initial WP generated was susceptible to
                                                             ods and additional software analysis techniques
integer overflow and this flaw was picked up by
                                                             is leading to a burgeoning sub-field of computer
the validity-fuzzing phase of FG. This feedback
                                                             science.
was then given to O4-mini and the LLM could
                                                                 Recent works have employed LLMs with for-
then produce the correct WP; this behaviour was
                                                             mal tools to generate program properties that
observed in each iteration carried out.
                                                             are adjacent to weakest preconditions (WPs);
                                                             much of this work has revolved around invari-
5 Discussion                                                 ant generation – a key component for software
                                                             verification. The authors of [32] use LLMs to gen-
5.1 Threats to Validity                                      erate loop invariants that are then validated by
The main threats to validity arise from our use              the Vampire theorem-prover [39]; these validated
of LLMs. The outputs of LLMs are inherently                  invariants are then used to replace loops within
stochastic in nature [37], and so the results that we        the context of bounded model checking [40]. The
have derived may not be exactly reproducible. We             work of [41] introduces the Lemur framework
attempt to mitigate the severity of this threat by           where LLMs are used to generate and repair can-
providing the prompts and logs of our interactions           didate invariants that are then used within the
with the OpenAI API.                                         ESBMC [42] and UAtomizer [43] frameworks. The
    Another threat arises when we consider the               authors of [44] fine-tune LLMs in an attempt to
range of LLMs employed. This work solely features            infer invariants for Java programs (such that these
models from a single vendor (OpenAI) and there-              invariants are likely to be Daikon [45] generated).
fore the results that we have produced are biased            In a task adjacent to invariant generation, the
in this respect; the argument could be made that             authors of [46] use LLMs to generate postcondi-
other models may perform significantly better or             tions from natural language documentation. Addi-
worse, and that our results do not represent this            tionally, [47] does not use LLMs, but instead opts
potential variety.                                           to use deep-reinforcement-learning to synthesize
    Additionally, data leakage [38] is typically a           program invariants.
concern for many studies which rely on LLMs.                     The task of generating preconditions has also
Data leakage occurs when the information from                been approached on several fronts [9–23]. The
a test set (e.g. benchmark programs) is already              authors of [23] and [21] use logical abductive infer-
present in the training data of an LLM. We believe           ence to infer the provably weakest preconditions
                                                             for a class of deterministic and non-deterministic


                                                        11
array programs. The works of [18] and [19] employ           mechanism of Fuzzing Guidance (FG) for aiding
a more dynamic approach, utilising data-driven              LLMs towards this goal. The effectiveness of our
execution loops in order to learn likely precondi-          approach was demonstrated on a comprehensive
tions. Our work differs from the above in that we           benchmark set of deterministic array programs in
combine fuzzing and LLMs in a unique manner to              Java.
derive WPs; additionally, our approach can handle               In concrete terms, we found that O4-mini was
problem variants (including sorting and search),            generally superior to GPT-4o in generating correct
that the aforementioned techniques cannot (see              WPs. Additionally, we observed that FG enabled
the supplementary material link for example-four            O4-mini to consistently generate the correct WPs
in Section 8).                                              for all of the benchmark programs studied. Our
                                                            results also showed that a less performant model
7 Future Work                                               such as GPT-4o, when enabled with FG, could
                                                            achieve competitive performance relative to the
There are several avenues for future work which             baseline O4-mini model (i.e. O4-mini without
arise from this current study, a number of which            FG).
stem from the limitations of our current approach               Overall, our results indicate that LLMs are
towards generating weakest preconditions (WPs).             capable of producing viable candidate WPs, and
For example, the WPs that are derived through               that this ability is enhanced through FG.
LLMs and Fuzzing Guidance (FG) are only ever
                                                            Supplementary material. Log files detail-
likely -valid and likely -weakest (see Section 2.2);
                                                            ing GPT interactions and fuzzing invocations:
this is due to the inherently incomplete nature
                                                            https://doi.org/10.5281/zenodo.17018494
of fuzz testing (and thus FG). One direction for
future work would seek to concretely verify the             Acknowledgements. This work was con-
weakness and validity of a candidate WP that                ducted with the financial support of the Research
had been generated through an LLM with FG;                  Ireland Centre for Research Training in Digitally-
this could be done through the use of a formal              Enhanced Reality (d-real) under Grant No.
reasoning tool like Vampire [39].                           18/CRT/6224, Taighde Éireann – Research Ire-
    Another path for future work would seek to              land under Grant number 13/RC/2094/\ 2, and
expand the capabilities of the fuzz testing tool            the ERC Consolidator Grant ARTIST 101002685.
which undergirds FG – namely, JQF [35]. This                For the purpose of Open Access, the author has
work might include creating a more adept and                applied a CC BY public copyright licence to any
flexible orchestrator for FG, such that FG could            Author Accepted Manuscript version arising from
be applied to a greater range of programs beyond            this submission.
those studied here.
    Bug-finding is another application of the               References
approach outlined in this work. Anecdotally, we
found that WPs could be generated for real-world             [1] Floyd, R.W.: Assigning meanings           to
programs which were similar to the benchmarks                    programs1 .  Mathematical    Aspects      of
here; these WPs were then able to avoid known                    Computer Science 19, 19 (1967)
exception-triggering test cases and reveal other
fault-inducing test cases that were not already              [2] Hoare, C.A.R.: An axiomatic basis for com-
known. We also found that buggy programs could                   puter programming. Commun. ACM 12,
be revealed in a roundabout manner when the WP                   576–580 (1969)
generated by an LLM with FG does not fit with a
programmer’s expected WP.                                    [3] Meyer, B.: Applying ’design by contract’.
                                                                 Computer 25(10), 40–51 (1992) https://doi.
                                                                 org/10.1109/2.161279
8 Conclusion
                                                             [4] Cousot, P., Cousot, R.: Abstract inter-
This work investigated the use of LLMs (specifi-
                                                                 pretation: a unified lattice model for
cally GPT-4o and O4-mini) for generating weakest
preconditions (WPs) and introduced our novel


                                                       12
    static analysis of programs by construc-                   In: De Nicola, R. (ed.) Programming Lan-
    tion or approximation of fixpoints. In:                    guages and Systems, pp. 253–267. Springer,
    Proceedings of the 4th ACM SIGACT-                         Berlin, Heidelberg (2007)
    SIGPLAN Symposium on Principles of Pro-
    gramming Languages. POPL ’77, pp. 238–                 [13] Moy, Y.: Sufficient preconditions for modu-
    252. Association for Computing Machin-                      lar assertion checking. In: Logozzo, F., Peled,
    ery, New York, NY, USA (1977). https://                     D.A., Zuck, L.D. (eds.) Verification, Model
    doi.org/10.1145/512950.512973 . https://doi-                Checking, and Abstract Interpretation, pp.
    org.elib.tcd.ie/10.1145/512950.512973                       188–202. Springer, Berlin, Heidelberg (2008)

 [5] Back, R.-J.J., Akademi, A., Wright, J.V.,             [14] Astorga, A., Madhusudan, P., Saha, S.,
     Schneider, F.B., Gries, D.: Refinement Cal-                Wang, S., Xie, T.: Learning stateful precon-
     culus: A Systematic Introduction, 1st edn.                 ditions modulo a test generator. In: Proceed-
     Springer, Berlin, Heidelberg (1998)                        ings of the 40th ACM SIGPLAN Confer-
                                                                ence on Programming Language Design and
 [6] King, J.C.: A program verifier. PhD thesis,                Implementation, pp. 775–787 (2019)
     USA (1970). AAI7018026
                                                           [15] Cousot, P., Cousot, R., Logozzo, F.: Precon-
 [7] Rosenblum, D.S.: A practical approach to                   dition inference from intermittent assertions
     programming with assertions. IEEE Transac-                 and application to contracts on collections.
     tions on Software Engineering 21(1), 19–31                 In: International Workshop on Verification,
     (1995) https://doi.org/10.1109/32.341844                   Model Checking, and Abstract Interpreta-
                                                                tion, pp. 150–168 (2011). Springer
 [8] Dijkstra, E.W.: Guarded commands, nonde-
     terminacy and formal derivation of programs.          [16] Gehr, T., Dimitrov, D., Vechev, M.: Learning
     Commun. ACM 18(8), 453–457 (1975) https:                   commutativity specifications. In: Computer
     //doi.org/10.1145/360933.360975                            Aided Verification: 27th International Con-
                                                                ference, CAV 2015, San Francisco, CA, USA,
 [9] Bourdoncle, F.: Abstract debugging of                      July 18-24, 2015, Proceedings, Part I 27, pp.
     higher-order imperative languages. In: Pro-                307–323 (2015). Springer
     ceedings of the ACM SIGPLAN 1993 Con-
     ference on Programming Language Design                [17] Moy, Y.: Sufficient preconditions for mod-
     and Implementation. PLDI ’93, pp. 46–                      ular assertion checking. In: Proceedings of
     55. Association for Computing Machin-                      the 9th International Conference on Verifi-
     ery, New York, NY, USA (1993). https://                    cation, Model Checking, and Abstract Inter-
     doi.org/10.1145/155090.155095 . https://doi-               pretation. VMCAI’08, pp. 188–202. Springer,
     org.elib.tcd.ie/10.1145/155090.155095                      Berlin, Heidelberg (2008)

[10] Calcagno, C., Distefano, D., O’Hearn, P.W.,           [18] Padhi, S., Sharma, R., Millstein, T.: Data-
     Yang, H.: Footprint analysis: A shape analy-               driven precondition inference with learned
     sis that discovers preconditions. In: Nielson,             features. ACM SIGPLAN Notices 51(6), 42–
     H.R., Filé, G. (eds.) Static Analysis, pp.                56 (2016)
     402–418. Springer, Berlin, Heidelberg (2007)
                                                           [19] Sankaranarayanan, S., Chaudhuri, S.,
[11] Cousot, P., Cousot, R.: Modular static pro-                Ivančić, F., Gupta, A.: Dynamic inference
     gram analysis. In: Horspool, R.N. (ed.) Com-               of likely data preconditions over predicates
     piler Construction, pp. 159–179. Springer,                 by tree learning. In: Proceedings of the
     Berlin, Heidelberg (2002)                                  2008 International Symposium on Software
                                                                Testing and Analysis, pp. 295–306 (2008)
[12] Gulwani, S., Tiwari, A.: Computing proce-
     dure summaries for interprocedural analysis.          [20] Seghir, M.N., Kroening, D.: Counterexample-
                                                                guided precondition inference. In: Felleisen,


                                                      13
    M., Gardner, P. (eds.) Programming Lan-                    Anwar, S., Usman, M., Akhtar, N., Barnes,
    guages and Systems, pp. 451–471. Springer,                 N., Mian, A.: A comprehensive overview
    Berlin, Heidelberg (2013)                                  of large language models. arXiv preprint
                                                               arXiv:2307.06435 (2023)
[21] Sumanth Prabhu, S., Fedyukovich, G.,
     D’Souza, D.: Maximal quantified precondi-             [30] Chen, B., Zhang, F., Nguyen, A., Zan,
     tion synthesis for linear array loops. In:                 D., Lin, Z., Lou, J.-G., Chen, W.: Codet:
     European Symposium on Programming, pp.                     Code generation with generated tests. arXiv
     245–274 (2024). Springer                                   preprint arXiv:2207.10397 (2022)

[22] Zhou, Z., Dickerson, R., Delaware, B., Jagan-         [31] Jiang, N., Liu, K., Lutellier, T., Tan, L.:
     nathan, S.: Data-driven abductive inference                Impact of code language models on auto-
     of library specifications. Proc. ACM Pro-                  mated program repair. In: 2023 IEEE/ACM
     gram. Lang. 5(OOPSLA) (2021) https://doi.                  45th International Conference on Software
     org/10.1145/3485493                                        Engineering (ICSE), pp. 1430–1442 (2023).
                                                                IEEE
[23] Sumanth Prabhu, S., D’Souza, D.,
     Chakraborty, S., Venkatesh, R., Fedyukovich,          [32] Pirzada, M.A., Reger, G., Bhayat, A.,
     G.: Weakest precondition inference for non-                Cordeiro, L.C.: Llm-generated invariants
     deterministic linear array programs. In:                   for bounded model checking without loop
     International Conference on Tools and Algo-                unrolling. In: Proceedings of the 39th
     rithms for the Construction and Analysis of                IEEE/ACM International Conference on
     Systems, pp. 175–195 (2024). Springer                      Automated Software Engineering, pp. 1395–
                                                                1407 (2024)
[24] Cousot, P., Cousot, R., Fähndrich, M.,
     Logozzo, F.: Automatic inference of necessary         [33] OpenAI: Hello GPT-4o (2025). https:
     preconditions. In: Giacobazzi, R., Berdine,                //openai.com/index/hello-gpt-4o/ Accessed
     J., Mastroeni, I. (eds.) Verification, Model               2025-27-05
     Checking, and Abstract Interpretation, pp.
     128–148. Springer, Berlin, Heidelberg (2013)          [34] OpenAI:          introducing-o3-and-o4-mini
                                                                (2025).          https://openai.com/index/
[25] Manès, V.J., Han, H., Han, C., Cha, S.K.,                 introducing-o3-and-o4-mini/        Accessed
     Egele, M., Schwartz, E.J., Woo, M.: The art,               2025-27-05
     science, and engineering of fuzzing: A survey.
     IEEE Transactions on Software Engineering             [35] Padhye, R., Lemieux, C., Sen, K.: Jqf:
     47(11), 2312–2331 (2019)                                   Coverage-guided property-based testing in
                                                                java. In: Proceedings of the 28th ACM SIG-
[26] Jordan, M.I., Mitchell, T.M.: Machine learn-               SOFT International Symposium on Software
     ing: Trends, perspectives, and prospects. Sci-             Testing and Analysis, pp. 398–401 (2019)
     ence 349(6245), 255–260 (2015)
                                                           [36] Schulhoff, S., Ilie, M., Balepur, N., Kahadze,
[27] Zhu, X., Wen, S., Camtepe, S., Xiang, Y.:                  K., Liu, A., Si, C., Li, Y., Gupta, A., Han,
     Fuzzing: a survey for roadmap. ACM Com-                    H., Schulhoff, S., et al.: The prompt report:
     puting Surveys (CSUR) 54(11s), 1–36 (2022)                 A systematic survey of prompting techniques.
                                                                arXiv preprint arXiv:2406.06608 5 (2024)
[28] Bounimova, E., Godefroid, P., Molnar, D.:
     Billions and billions of constraints: White-          [37] Vaswani, A., Shazeer, N., Parmar, N., Uszko-
     box fuzz testing in production. In: 2013 35th              reit, J., Jones, L., Gomez, A.N., Kaiser, L.,
     International Conference on Software Engi-                 Polosukhin, I.: Attention is all you need.
     neering (ICSE), pp. 122–131 (2013). IEEE                   Advances in neural information processing
                                                                systems 30 (2017)
[29] Naveed, H., Khan, A.U., Qiu, S., Saqib, M.,


                                                      14
[38] Inan, H.A., Ramadan, O., Wutschitz, L.,                      transform natural language intent into for-
     Jones, D., Rühle, V., Withers, J., Sim, R.:                 mal method postconditions? Proceedings of
     Training data leakage analysis in language                   the ACM on Software Engineering 1(FSE),
     models. arXiv preprint arXiv:2101.05405                      1889–1912 (2024)
     (2021)
                                                              [47] Si, X., Naik, A., Dai, H., Naik, M., Song,
[39] Kovács, L., Voronkov, A.: First-order                        L.: Code2inv: A deep learning framework
     theorem proving and vampire. In: Inter-                       for program verification. In: Computer Aided
     national Conference on Computer Aided                         Verification: 32nd International Conference,
     Verification, pp. 1–35 (2013). Springer                       CAV 2020, Los Angeles, CA, USA, July 21–
                                                                   24, 2020, Proceedings, Part II 32, pp. 151–164
[40] Clarke, E., Biere, A., Raimi, R., Zhu, Y.:                    (2020). Springer
     Bounded model checking using satisfiability
     solving. Formal methods in system design
     19(1), 7–34 (2001)

[41] Wu, H., Barrett, C., Narodytska, N.: Lemur:
     Integrating large language models in auto-
     mated program verification. arXiv preprint
     arXiv:2310.04870 (2023)

[42] Menezes, R.S., Aldughaim, M., Farias, B.,
     Li, X., Manino, E., Shmarov, F., Song, K.,
     Brauße, F., Gadelha, M.R., Tihanyi, N.,
     et al.: Esbmc v7. 4: Harnessing the power
     of intervals: (competition contribution). In:
     International Conference on Tools and Algo-
     rithms for the Construction and Analysis of
     Systems, pp. 376–380 (2024). Springer

[43] Heizmann, M., Dietsch, D., Greitschus, M.,
     Leike, J., Musa, B., Schätzle, C., Podelski, A.:
     Ultimate automizer with two-track proofs:
     (competition contribution). In: International
     Conference on Tools and Algorithms for the
     Construction and Analysis of Systems, pp.
     950–953 (2016). Springer

[44] Pei, K., Bieber, D., Shi, K., Sutton, C., Yin,
     P.: Can large language models reason about
     program invariants? In: International Confer-
     ence on Machine Learning, pp. 27496–27520
     (2023). PMLR

[45] Ernst, M.D., Perkins, J.H., Guo, P.J., McCa-
     mant, S., Pacheco, C., Tschantz, M.S., Xiao,
     C.: The daikon system for dynamic detec-
     tion of likely invariants. Science of computer
     programming 69(1-3), 35–45 (2007)

[46] Endres, M., Fakhoury, S., Chakraborty, S.,
     Lahiri, S.K.: Can large language models


                                                         15
