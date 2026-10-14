                                             Debugging Program Verification Proof Scripts
                                                                            – Tool Paper –



                                                     Bernhard Beckert, Sarah Grebing, and Alexander Weigl

                                                                Karlsruhe Institute of Technology
                                                          {beckert,sarah.grebing,weigl}@kit.edu
arXiv:1804.04402v1 [cs.LO] 12 Apr 2018




                                               Abstract. Interactive program verification is characterized by itera-
                                               tions of unfinished proof attempts. To support the process of construct-
                                               ing a complete proof, many interactive program verification systems of-
                                               fer a proof scripting language as a text-based way to describe the non-
                                               automatic steps in a proof. Such scripting languages are beneficial, but
                                               users spent a lot of effort on inspecting proof scripts and the proofs they
                                               construct to detect the cause when a proof attempt is unsuccessful and
                                               leads to unintended proof states. We present an offline and replay de-
                                               bugger to support the user in analyzing proof attempts performed with
                                               proof scripts. This debugger adapts successful concepts from software de-
                                               bugging to the area of proof script debugging. The tool is built on top of
                                               KeY, a system for deductive verification of Java programs. The debugger
                                               and its graphical user interface are designed to support program verifi-
                                               cation in particular, the underlying concepts and the implementation,
                                               however, are adaptable to other provers and proof tasks.


                                         1    Introduction

                                         Motivation. Proving complex properties of programs requires user guidance,
                                         which can come in the form of program annotations as well as user interaction
                                         during proof construction. Providing the right guiding information that allows
                                         a verification system to find a proof is, in general, an iterative process of re-
                                         peated failed attempts. Also, the characteristics of program verification proofs
                                         are considerably different from proofs of mathematical theorems (such as prop-
                                         erties of algebraic structures). Proofs in program verification consist of many
                                         structurally and/or semantically similar cases that are syntactically large, but
                                         usually of low intrinsic complexity. The mechanism for providing user guidance
                                         needs to reflect this peculiarity of proofs in the program verification domain and
                                         provide appropriate means for interaction. To support the iterative process of
                                         constructing proofs, many interactive program verification systems offer a proof
                                         scripting language as a text-based way to describe the non-automatic steps in a
                                         proof. Such scripting languages are beneficial, but users spent a lot of effort on
                                         inspecting proof scripts and the proofs they construct to detect the cause when
                                         a proof attempt is unsuccessful and leads to unintended proof states.
                                             Contribution. In this paper, we describe our tool psdbg, an offline and re-
                                         play debugger adapting successful concepts from software debugging to the area
of proof script debugging. It implements our interaction concept for interactive
program verification described in [1]. psdbg combines point-and-click with text-
based interaction based on a scripting language for proofs, kps (Sect. 2). The
replay functionalities offered by our tool allow the user to analyze unfinished
proof attempts by using functionalities known from software debugging like for-
ward stepping, breakpoints, and the visualization of the proof script state and
proof. Furthermore, step-back and replay of proof commands are supported.
Partial proof scripts can be extended by either appending new script commands
(text-based) or by point-and-click selection of proof rules and commands. Addi-
tionally, psdbg contains aids for writing proof scripts such as the generation of
a case-distinction expressions for goal selection and a visualization of the result
of term matching expressions.
    psdbg is available at formal.iti.kit.edu/psdbg together with a video
of its usage.
    Underlying verification system. We have chosen to built psdbg on top
of the KeY system, which is an interactive theorem prover for the verification
of Java programs at source code level [2]. KeY is based on a sequent calculus
for Java Dynamic Logic. It was successfully applied to verify real world Java
programs, e.g., implementations of Timsort [3] and Dual-Pivot Quicksort [4].
KeY constructs an explicit proof object, i.e., all proof steps and rule applications
are available to the user at any time in addition to the current open goals.
This enables a more fine-grained stepping functionality down to the level of
single calculus rule applications. KeY offers point-and-click interaction for prover
guidance. Combining KeY with a script component allows to automate user
actions without losing the advantages of point-and-click interaction. Also, this
combination provides more stable guidance in situations where the proof problem
evolves. psdbg is designed to support program verification in particular, the
underlying concepts and the implementation, however, are adaptable to other
provers and proof tasks (Sect. 4).
    Related work. The need to analyze failed proof attempts in interactive
theorem proving has lead to different mechanisms for gaining insight into proof
construction. The interactive theorem provers Isabelle [5] and Coq [6] both pro-
vide text-based interaction, and the way in which proofs are constructed allows
to step over tactics, to revert a tactic application, and to add tactic invocations
iteratively. The user can inspect the proof states between tactic applications. To
get a deeper insight into tactics, both tools allow for the use of debuggers for
the language in which the tactics and the tools are implemented (Standard ML
respectively OCaml). While tactics implement generic proof strategies indepen-
dent from the concrete proof problem, proof scripts are usually tailored to the
current verification task. This difference manifests itself when debugging proof
scripts in contrast to debugging tactics. Additionally, Hupel proposes an inter-
active tracing of Isabelle’s simplification tactic [7]. Lean’s metaframework [8]
– an API to the theorem prover lean – provides support for classical program
debuggers to step through the execution of the declarative language of Lean.

                                         2
1    script quicksort_split() {
2      autopilot_prep;       //perform symbolic execution and simplify
3      foreach { tryclose; } //try to close all trivial cases
4      foreach { simp_upd;   seqPermFromSwap; andRight; }
5      cases {
6        case match ‘==> seqDef(_,_,_) = seqDef(_,_,_)‘: auto;
7        case match ‘==> (\exists ?X (\exists ?Y _))‘ :
8            instantiate var=X with=‘i_0‘;
9            instantiate var=Y with=‘j_0‘;
10           auto;
11     } }



     Fig. 1. A proof script for proving correctness of the split method of Quicksort (see
     Appendix A, line 76). The first lines perform a pre-processing. After application of
     simplification steps and a rule specific for the data type sequence (seqPermFromSwap),
     user guidance in the form of quantifier instantiations is required (lines 8–9). The match
     expression in line 7 matches sequents that contain a formula which consists of at
     least two nested existential quantifiers and binds the concrete terms of the quantified
     variables to the schema variables ?X resp. ?Y to be used in in lines 8 and 9 where they
     are parameters for the proof command instantiate.


     2     Language for Proof Scripts
     In this section, we introduce the basic concepts of the Key Proof Script (kps)
     language. As an example, we use a script constructing a proof for the correctness
     of the pivotal split in a Quicksort implementation (see Fig. 1).1
         State. A proof state consists of a set of proof goals of which at most one is
     selected . The main part of a proof goal is an open verification condition. In ad-
     dition, it assigns values to variables. These variables are goal-local , i.e., changing
     the value of a variable has only local effect. When a new goal is created, it in-
     herits its parent goal’s assignment. The configuration of the underlying theorem
     prover (e.g., the particular heuristic used for proof search) is accessible and can
     be changed via a special subset of these variables.
         Mutators. As proof construction is characterized by selecting and manipu-
     lating goals, kps provides goal selectors and mutators. Mutators are commands
     which modify a single proof goal by either manipulating the verification condi-
     tion or changing the variable assignment. Mutators for verification conditions
     are either calls to sub-scripts (to construct sub-proofs) or commands from the
     underlying theorem prover. In the example in Fig. 1, one of the mutators is
     autopilot prep (line 2), an internal prover strategy of KeY, that performs
     symbolic execution of the program to be verified with intermediate simplification
     steps. Another mutator in the example is instantiate (lines 8 and 9), which
     is a rule with parameters var and with. This rule instantiates the quantified
     variable var with a term. If a proof state contains more than one goal, before
     applying mutators a single goal has to be selected, as described in the following.
         Goal selectors. With goal selectors one picks goals from the current state for
     mutator application. kps provides the following selectors: foreach, theonly,
     1
         The full Java source code and its specification can be found in Appendix A.


                                                3
cases. With foreach, a mutator is applied to all proof goals (lines 3 and 4 in
Fig. 1). The cases selector is used to make case distinctions over proof goals
based on matching pattern expressions (in lines 5 to 10 there are two cases). In
addition to syntactical patterns, matching expressions can be semantic, and they
can refer to local goal variables; see [1] for more details. This kind of selection
statement allows to mutate similar goals in the same way. After the evaluation
of a matching expression, the state is updated by variable bindings.


3   Tool Features and Their Use

Program verification is an iterative process of unsuccessful proof attempts. The
user needs to find the reason why proof construction failed. In the case of proof
debugging, the user investigates whether the last state of the proof script, in-
cluding the remaining verification conditions, matches his or her mental model
of the proof, and how this state was reached. To support the user, our tool makes
use of the analogy between writing programs and writing proof scripts presented
in [1]. This analogy enables us to adopt mechanisms from software debugging
systems to the analysis of failed proof attempts.
    Visualization. Like software debuggers, psdbg offers different views on the
proof states as shown in Fig. 2: ¬ The source code of the proof script, with the
next command to be executed being highlighted. ­ A list of the current proof
goals and the; the currently selected proof goal is highlighted. This window pane
allows different representations of the goals to be used, e.g., branching labels
which are introduced by the underlying verification system to identify certain
proof branches like induction base, step and use case. ® Below, the selected proof
goal is shown in full textual representation; this view supports the application
of rules on selected terms in the interactive mode. ¯ The lower left pane shows
the source code of the Java program being verified. The highlighted lines are the
executed Java statements corresponding to the selected proof goal. ° The proof
tree, i.e., the explicit proof object constructed by KeY is displayed. Note that,
only a small portion of the proof tree can be seen, showing the beginning of the
proof, where no branching has occurred yet. ± The toolbar contains the buttons
that are used for stepping through the proof script’s execution. Not shown in the
screenshot of Figure 2 is the editor for writing and evaluating match expressions
and the window with proof command documentation. Note that not all views
are open all the time – rather the user may choose which views to see.
    Breakpoints and stepping. For the analysis of proof script executions,
psdbg allows to set breakpoints and to use stepping functionalities. The tool
supports line breakpoints with and without a boolean condition. Script execution
pauses when a breakpoint is reached and – in case a condition is provided – if
moreover the state reached satisfies the breakpoint’s condition.
    When script execution is paused, the user can use the stepping functionalities
(by using the respective buttons in the toolbar).
    For stepping, statements can either be compound (blocks or prover strategies)
or atomic (e.g., single rule applications or variable assignments). The functions


                                        4
                          ±
                          ¬                                                   °


                                                                              ­



                                                                              ®

                                   ¯


                        Fig. 2. The user interface of psdbg




step into and step over have the usual behavior known from software debug-
ging: step over executes until the end of the compound statement, while step
into allows the user to inspect the execution of the constituents of a compound
statements in more detail (e.g., if invoked before a block or a call to a sub-script).
If step into is invoked for a native command of the underlying proof system, there
are two possibilities: if the proof command is a prover strategy, the user is pre-
sented with the partial proof tree that corresponds to the execution of the that
strategy. Stepping into a single (atomic) calculus rule behaves like step over .

    In addition to step over and step into, two more stepping functions are avail-
able to inspect script execution in reverse: step over reverse and step into reverse.
These allow the user to inspect proofs from end to start. This reverse inspection
of proof states is possible due to the (partial) explicit proof object provided by
the underlying verification system.

    Interactive manipulation of proof goals. When the execution of a script
is completed with some open proof goals remaining, the user has the possibility to
interactively manipulate these open goals (e.g., using point-and-click interaction
provided by the underlying verification system). Our tool allows to make these
user interactions persistent automatically by recording and appending them to
the end of the proof script upon leaving the interactive mode.


                                          5
4    System Architecture
psdbg consists of three main components (Fig. 3), which are built on top of
an underlying theorem prover. (1) The user interface needs direct access to the
theorem prover to allow interactive execution of goal mutators and to extract
information for visualization, e.g., the executed Java source code lines. Integra-
tion of new additional views and state projection is supported by the use of a
docking framework and full access to the underlying stack. (2) Execution con-
trol is a layer that provides the debugging logic to the UI, e.g., stepping, state
tracing and breakpoints. (3) The interpreter is the heart of the architecture.
It executes the proof script and performs the calls to the goal mutators of the
theorem prover.
    The debugging logic is separated from the interpreter core and the user in-
terface. The UI is in parts dependent on the underlying theorem prover, i.e., the
shape of the goals and the prover’s user interaction style (in KeY the goals are
sequents, and KeY uses a point-and-click style for interaction).
    For the adaption to a different theorem                   User Interface
prover, the interpreter provides well-defined
extension points—so the execution control                      Execution Control

and interpreter core are independent to the                           Interpreter
kind of proof goals. The extensions points are             Matching               Settings
                                                    Goals              Mutators
the handler of goal mutators, and special vari-
ables (prover settings) and the evaluation of                Theorem Prover

matchings against verification conditions. The
matching mechanism supports a special lan-
                                                 Fig. 3. Block diagram of the archi-
guage for pattern matching of proof goals. tecture. The blue hatched parts are
The current pattern language is optimized for provided by our tool.
KeY’s sequents and needs to be adapted when
using other types of proof goals.

5    Future Work
For future work, we will explore the usability of psdbg and kps on larger and
more complex verification tasks, where script modularization becomes necessary.
We plan to better visualise relations between different views, e.g., showing the
relation between the proof script and the program to be verified. Also, better
support for proof exploration is planned, so that less manual effort is required.

Acknowledgements. Special thanks go to An Thuy Tien Luong who provided
valuable comments concerning the usage of psdbg and the proof scripting lan-
guage.

References
 1. Beckert, B., Grebing, S., Ulbrich, M.: An interaction concept for program verifi-
    cation systems with explicit proof object. [9] 163–178


                                            6
 2. Ahrendt, W., Beckert, B., Bubel, R., Hähnle, R., Schmitt, P.H., Ulbrich, M., eds.:
    Deductive Software Verification - The KeY Book: From Theory to Practice. Volume
    10001 of LNCS. Springer (2016)
 3. de Gouw, S., Rot, J., de Boer, F.S., Bubel, R., Hähnle, R.:               Openjdk’s
    java.utils.collection.sort() is broken: The good, the bad and the worst case. [10]
    273–289
 4. Beckert, B., Schiffl, J., Schmitt, P.H., Ulbrich, M.: Proving jdk’s dual pivot quick-
    sort correct. [11] 35–48
 5. Nipkow, T., Paulson, L.C., Wenzel, M.: Isabelle/HOL — A Proof Assistant for
    Higher-Order Logic. Volume 2283 of LNCS. Springer (2002)
 6. Bertot, Y., Castran, P.: Interactive Theorem Proving and Program Development:
    Coq’Art The Calculus of Inductive Constructions. 1st edn. Texts in Theoretical
    Computer Science An EATCS Series. Springer-Verlag Berlin Heidelberg (2004)
 7. Hupel, L.: Interactive simplifier tracing and debugging in isabelle. [12] 328–343
 8. Ebner, G., Ullrich, S., Roesch, J., Avigad, J., de Moura, L.: A metaprogramming
    framework for formal verification. PACMPL 1(ICFP) (2017) 34:1–34:29
 9. Strichman, O., Tzoref-Brill, R., eds.: Hardware and Software: Verification and
    Testing - 13th International Haifa Verification Conference, HVC 2017, Haifa, Israel,
    November 13-15, 2017, Proceedings. Volume 10629 of Lecture Notes in Computer
    Science., Springer (2017)
10. Kroening, D., Pasareanu, C.S., eds.: Computer Aided Verification - 27th Inter-
    national Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Pro-
    ceedings, Part I. Volume 9206 of Lecture Notes in Computer Science., Springer
    (2015)
11. Paskevich, A., Wies, T., eds.: Verified Software. Theories, Tools, and Experiments
    - 9th International Conference, VSTTE 2017, Heidelberg, Germany, July 22-23,
    2017, Revised Selected Papers. Volume 10712 of Lecture Notes in Computer Sci-
    ence., Springer (2017)
12. Watt, S.M., Davenport, J.H., Sexton, A.P., Sojka, P., Urban, J., eds.: Intelligent
    Computer Mathematics - International Conference, CICM 2014, Coimbra, Portu-
    gal, July 7-11, 2014. Proceedings. Volume 8543 of Lecture Notes in Computer
    Science., Springer (2014)




                                           7
     A    QuickSort.java

1    /**
2     * This example formalizes and verifies the wellknown quicksort
3     * algorithm for int-arrays algorithm. It shows that the array
4     * is sorted in the end and that it contains a permutation of
5     * the original input.
6     *
7     * The    proofs  for    the main    method   sort(int[])    runs
8     * automatically   while    the   other two    methods    require
9     * interaction. You     can load    the files    "sort.key" and
10    * "split.key" from the example’s directory to execute the
11    * according proof scripts.
12    *
13    * The permutation property requires some interaction: The idea
14    * is that the only actual modification on the array are swaps
15    * within the "split" method. The sort method body contains
16    * three method invocations which each maintain the permutation
17    * property. By a repeated appeal to the transitivity of the
18    * permutation property, the entire algorithm can be proved to
19    * only permute the array.
20    *
21    * To establish monotonicity, the key is to specify that the
22    * currently handled block contains only numbers which are
23    * between    the   two    pivot   values   array[from-1]     and
24    * array[to]. The first and last block are exempt from one of
25    * these conditions since they have only one neighbouring
26    * block.
27    *
28    * The example has been added to show the power of proof
29    * scripts.
30    *
31    * @author Mattias Ulbrich, 2015
32    */
33
34   class Quicksort {
35
36       /*@ public normal_behaviour
37         @ ensures \dl_seqPerm(\dl_array2seq(array),
38         @                          \old(\dl_array2seq(array)));
39         @ ensures (\forall int i; 0<=i && i<array.length-1;
40         @                     array[i] <= array[i+1]);
41         @ assignable array[*];
42         @*/
43       public void sort(int[] array) {
44           if(array.length > 0) {
45               sort(array, 0, array.length-1);
46           }
47       }
48
49       /*@ public normal_behaviour
50         @ requires 0 <= from;
51         @ requires to < array.length;
52         @ requires from > 0 ==> (\forall int x; from<=x &&
53         @                            x<=to; array[x] > array[from-1]);
54         @ requires to < array.length-1 ==>
55         @            (\forall int x; from<=x && x<=to; array[x] <= array[to+1]);
56         @ ensures \dl_seqPerm(\dl_array2seq(array), \old(\dl_array2seq(array)));
57         @ ensures (\forall int i; from<=i && i<to; array[i] <= array[i+1]);
58         @ ensures from > 0 ==>
59         @           (\forall int x; from<=x && x<=to; array[x] > array[from-1]);
60         @ ensures to < array.length-1 ==>
61         @                (\forall int x; from<=x && x<=to; array[x] <= array[to+1]);
62         @ assignable array[from..to];
63         @ measured_by to - from + 1;
64         @*/
65       private void sort(int[] array, int from, int to) {



                                               8
66            if(from < to) {
67                int splitPoint = split(array, from, to);
68                sort(array, from, splitPoint-1);
69                sort(array, splitPoint+1, to);
70            }
71        }
72
73        /*@ public normal_behaviour
74          @ requires 0 <= from && from < to && to <= array.length-1;
75          @ requires from > 0 ==> (\forall int x; from<=x && x<=to;
76          @                                array[from-1] < array[x]);
77          @ requires to < array.length-1 ==> (\forall int y; from<=y && y<=to;
78          @                                            array[y] <= array[to+1]);
79          @ ensures \dl_seqPerm(\dl_array2seq(array), \old(\dl_array2seq(array)));
80          @ ensures from <= \result && \result <= to;
81          @ ensures (\forall int m; from <= m && m <= \result;
82          @                     array[m] <= array[\result]);
83          @ ensures (\forall int n; \result < n && n <= to;
84          @                     array[n] > array[\result]);
85          @ ensures from > 0 ==> (\forall int x; from<=x && x<=to;
86          @                     array[from-1] < array[x]);
87          @ ensures to < array.length-1 ==> (\forall int y; from<=y && y<=to;
88          @                     array[y] <= array[to+1]);
89          @ assignable array[from..to];
90          @*/
91        private int split(int[] array, int from, int to) {
92
93            int i = from;
94            int pivot = array[to];
95
96            /*@
97              @ loop_invariant from <= i && i <= j;
98              @ loop_invariant from <= j && j <= to;
99              @ loop_invariant \dl_seqPerm(\dl_array2seq(array),
100             @                                \old(\dl_array2seq(array)));
101             @ loop_invariant (\forall int k; from <= k && k < i; array[k] <= pivot);
102             @ loop_invariant (\forall int l; i <= l && l < j; array[l] > pivot);
103             @ loop_invariant from > 0 ==>
104             @       (\forall int x; from<=x && x<=to; array[from-1] < array[x]);
105             @ loop_invariant to < array.length-1 ==>
106             @       (\forall int y; from<=y && y<=to; array[y] <= array[to+1]);
107             @ decreases to + to - j - i + 2;
108             @ assignable array[from..to-1];
109             @*/
110           for(int j = from; j < to; j++) {
111               if(array[j] <= pivot) {
112                   int t = array[i];
113                   array[i] = array[j];
114                   array[j] = t;
115                   i++;
116               }
117           }
118
119           array[to] = array[i];
120           array[i] = pivot;
121
122           return i;
123
124       }
125   }




                                              9
