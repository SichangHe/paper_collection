 SYMDIFF: A Language-Agnostic Semantic Diﬀ
       Tool for Imperative Programs

                      Shuvendu K. Lahiri1 , Chris Hawblitzel1 ,
                      Ming Kawaguchi2, and Henrique Rebêlo3
                      1
                        Microsoft Research, Redmond, WA, USA
                         2
                           University of California, San Diego
                      3
                        Federal University of Pernambuco, Brazil


       Abstract. In this paper, we describe SymDiﬀ, a language-agnostic tool
       for equivalence checking and displaying semantic (behavioral) diﬀerences
       over imperative programs. The tool operates on an intermediate veriﬁ-
       cation language Boogie, for which translations exist from various source
       languages such as C, C# and x86. We discuss the tool and the front-end
       interface to target various source languages. Finally, we provide a brief
       description of the front-end for C programs.


1    Introduction
An evolving software module undergoes several changes — refactoring, feature
additions and bug ﬁxes. Such changes may introduce compatibility bugs or re-
gression bugs that are detected much later in the life-cycle of the software. There
is a need for tools that can aid the developers understand the impact of changes
faster. Such tools will complement “syntactic diﬀ” tools such as WinDiﬀ and
GNU Diﬀ on one hand, and regression testing based change validation (that
provides limited coverage) on the other.
   In this paper, we describe the design of SymDiﬀ (Symbolic Diﬀ), a seman-
tic diﬀerencing tool for imperative programs. Unlike most existing equivalence
checking tools for software, the tool operates on an intermediate veriﬁcation
language called Boogie [1] (and hence language-agnostic). This provides a sep-
aration of concerns — the core analysis algorithms are independent of source
language artifacts (object-orientation, generics, pointer arithmetic etc.) and are
therefore reusable across diﬀerent languages. To perform scalable equivalence
checking, we leverage the modular program veriﬁer in Boogie that exploits the
Satisﬁability Modulo Theories (SMT) solver Z3 [4]. A novel feature of the tool is
that it displays abstract counterexamples for equivalence proofs by highlighting
intra-procedural traces in the two versions (see Figure 1), a semantic extension
to diﬀering source lines highlighted by syntactic diﬀ tools.
   Because of the language-agnostic nature of the tool, one only needs a transla-
tor from the source language (such as C) to Boogie (many of which already ex-
ist). We describe the front-end interface required from such translators to target
SymDiﬀ. Finally, we brieﬂy describe the implementation of one such front-end
for C programs.

P. Madhusudan and S.A. Seshia (Eds.): CAV 2012, LNCS 7358, pp. 712–717, 2012.

c Springer-Verlag Berlin Heidelberg 2012
                        SYMDIFF: A Language-Agnostic Semantic Diﬀ Tool             713




Fig. 1. Output of SymDiﬀ for displaying semantic diﬀerences for C programs. The
yellow source lines highlight a path, and the gray lines display values of some program
expressions after each statement in the trace.


2    SymDiﬀ

SymDiﬀ operates on programs in an intermediate veriﬁcation language
Boogie [1]. Boogie is an imperative language consisting of assignments, asser-
tions, control-ﬂow and procedure calls. Variables (globals, locals and procedure
parameters) and expressions can be either of a scalar type τ or a map type [τ  ]τ .
We currently restrict SymDiﬀ to the non-polymorphic subset of Boogie. A Boo-
gie program may additionally contain symbolic constants, functions, and axioms
over such constants and functions.
   SymDiﬀ takes as input two loop-free Boogie programs and a conﬁguration ﬁle
that matches procedures, globals, and constants from the two programs. Loops,
if present, can be unrolled up to a user-speciﬁed depth, or may be extracted
as tail-recursive procedures. The default conﬁguration ﬁle matches procedures,
parameters, returns and globals with the same name; the user can modify it to
specify the appropriate conﬁguration. The tool can (optionally) take a list of
procedures that are assumed to be equivalent (e.g. procedures that do not call
into any procedures with modiﬁcations). For each pair of matched procedures f1
and f2 , SymDiﬀ checks for partial equivalence — terminating executions of f1
and f2 under the same input states result in identical output states. The input
state of a procedure consists of the value of parameters and globals (hereafter
referred to as a single variable gl ) on entry, and the output state consists of the
value of the globals and returns on exit.
714     S.K. Lahiri et al.

                                                Given two programs P1 and P2 and
procedure Eq.f1.f2(x){                       a pairing of procedures over the two
  var gl0;                                   programs, the algorithm below checks
  gl0 := gl; //copy the globals              for equivalence modularly. For each
  r1 := inline call f1(x);
                                             pair of paired procedures f1 and f2 ,
  gl1 := gl; //store output globals
                                             we create a new Boogie procedure
  gl := gl0; //restore globals
  r2 := inline call f2(x);                   Eq.f1 .f2 (Figure 2) that checks par-
  gl2 := gl; //store output globals          tial equivalence of f1 and f2 . To en-
  assert (r1 == r2 && gl1 == gl2);           able modular checking, the procedure
}                                            calls inside Eq.f1 .f2 (i.e. callees of f1
                                             and f2 ) are replaced by uninterpreted
Fig. 2. Procedure for checking equivalence functions that update the modiﬁed
of f1 and f2                                 globals and the return; the input to
                                             the functions are parameters and the
                                             globals that are read by the proce-
dure. The resulting set of procedures {Eq.fi .fj | fi ∈ P1 , fj ∈ P2 } (one for
each matched pair fi and fj ) are analyzed by the Boogie modular veriﬁer us-
ing veriﬁcation condition generation [1] and SMT solver Z3. We omit details
of veriﬁcation condition generation here; it suﬃces to know that it transforms
a program (a set of annotated procedures) to a single logical formula whose
validity implies that the program does not fail. In our case, if all the Eq.fi .fj
procedures are veriﬁed, then the matched procedure pairs in P1 and P2 are par-
tially equivalent. On the other hand, if the assertion in any Eq.fi .fj procedure
cannot be proved by Boogie, we extract a set of intraprocedural paths through
fi and fj and report them to the user. We modiﬁed Boogie to produce multiple
(up to a user-speciﬁed limit) counterexample traces for the same assertion.
   In addition to the purely modular approach, SymDiﬀ oﬀers various options
for inlining callees (to improve precision at the cost of scalability) for the case of
non-recursive programs. There are options for either inlining (a) every callee, (b)
only the callees that can’t be proved equivalent, or (c) only behaviors in callees
that can’t be proved equivalent (diﬀerential inlining [8]). These options require
a bottom-up traversal of the call graph of procedures.

3     Interface for Source Languages
In this section, we brieﬂy describe the important considerations for adapting
SymDiﬀ for a source imperative language such as C, C#, or x86. First, one
needs a translator for the language (say C) that performs two tasks: (i) repre-
sents the state of a program (e.g. variables, pointers and the heap) explicitly in
terms of scalar and map variables in Boogie, and (ii) translates each statement
in the source language to a sequence of statements in Boogie. The precision and
soundness of the resulting tool will be parameterized by how faithful the trans-
lator is. Many such translators exist today with various precision and soundness
trade-oﬀs. For example, HAVOC [3] translates C programs to Boogie; Spec# [2]
converts C# programs to Boogie; there have also been translators from binary
(x86) programs to Boogie [5].
                       SYMDIFF: A Language-Agnostic Semantic Diﬀ Tool         715

   When two procedures cannot be proven equivalent, SymDiﬀ generates coun-
terexample traces on the source programs (Figure 1). The counterexample
contains an intra-procedural trace for each procedure and values of “relevant”
program expressions (of scalar type) for each statement. We have found this to
be the most useful feature of the tool when applied to real examples. This feature
requires two pieces of (optional) additional information in the translated Boogie
programs, for each source line translated:
 – The source ﬁle and the line number have to be provided as attributes.
 – For each scalar valued program expression e to be displayed in the trace
   (e.g. e->oper in Line 10 of the ﬁrst program in Figure 1), associate the
   corresponding expression in Boogie.
Note that this requires only a one time change to the translator for the source
language to Boogie.
Non-deterministic Statements. In the presence of non-deterministic state-
ments (such as the Boogie statement havoc x that scrambles a variable x), a
procedure may not be equivalent to itself. Source language translators often use
non-deterministic statements such as havoc to model allocation, eﬀect of I/O
methods such as scanf, calls to external APIs etc. To use SymDiﬀ eﬀectively,
we require that the translators use deterministic statements to model such cases.
We provide an example of deterministic modeling of allocation for C programs
in the next section. SymDiﬀ also models external procedures as deterministic (in
their parameters) transformers using uninterpreted functions.

3.1   C Front End
In this section, we brieﬂy describe the implementation of the front-end for C pro-
grams. The tool takes two directories (for the two versions) containing a set of
.c ﬁles and a makeﬁle. We use the HAVOC [3] tool to translate C programs into
Boogie programs. HAVOC uses maps to model the heap of the C program [3],
where pointer and ﬁeld dereferences are modeled as select or updates of a map.
By default, HAVOC assumes that the input C programs are ﬁeld safe (i.e. dif-
ferent ﬁeld names cannot alias) and maintains a map per word-valued (scalar
or pointer) ﬁeld and type. For example, the statement x->f := *(int*)y; is
modeled as f[x+4] := T int[y]; using two maps f and T int of type [int]int
(assuming oﬀset of f is 4 inside x).
   We modiﬁed HAVOC to incorporate deterministic modeling of allocation (for
malloc and free) and I/O methods (such as scanf, getc) [8]. Here we sketch the
modeling of allocation: we maintain a (ghost) global variable allocvar, which
can be modiﬁed by calls to malloc and free. malloc is modeled as follows
(in Boogie) : malloc(n:int) returns (r:int) {r := allocvar; allocvar
:= newAlloc(allocvar, n);}, where newAlloc is an uninterpreted function.
The speciﬁcation for free is similar. The modeling ensures that two identi-
cal sequences of malloc and free return the same (but arbitrary) sequence of
pointers. This suﬃces for many examples, but can be incomplete in the presence
716    S.K. Lahiri et al.

Table 1. Results on Siemens benchmarks. “Proc” stands for procedures, “Time” is
the time taken by SymDiﬀ to analyze all the “Changed” procedures.

  Example        #LOC #Proc #Versions #Changed Time (sec) # Paths Enum Time (sec)
                                      procs (Avg) (Avg)    (Avg)      (Avg)
 tcas             173   9      42         1.2      0.64     26.72      1.19
 print tokens     727  18      7          1.4      1.30    357.43      2.87
 print tokens2’   569  19      10         1.1      0.90    169.36      1.25
 replace          563  21      32         1.1      0.96     20.38      2.11
 schedule         412  18      9          1.1      0.94     16.00      1.99
 schedule2        373  16      10          1       0.83     10.60      0.99
 print tokens2 n4 569  19      1           1       1.13     7560      56.83
 print tokens2 n6 569  19      1           1       1.30   >10,000     160.63
 print tokens2 e4 569  19      1           1       3.50     4200      24.02
 print tokens2 e6 569  19      1           1      32.96   >10,000     150.61




of diﬀerent allocation orders. We also added an option to generate the infor-
mation required to display the counterexample traces. For each statement, we
generate any pointer or scalar subexpression in the trace. For example, for the
C statement x->f.g->h = y[i] + z.f; we add the expressions {x, x->f.g,
x->f.g->h, y[i], z.f} whose values will be displayed in the trace. For pro-
cedure calls, we add the expressions in the arguments and the return. Figure 1
shows the semantic diﬀ as a pair of traces over two programs. The second pro-
gram performs some refactoring and feature addition (case for MULT). A syntactic
diﬀ tool gets confused by the refactoring and oﬀers little idea about the change
in behavior.
   Table 1 describes an evaluation of SymDiﬀ on a set of medium-sized C pro-
grams representing the Siemens benchmarks from the SIR repository [10]. Each
program comes with multiple versions representing injection of real and seeded
faults. The benchmark print tokens2’ represents a slightly altered version of
the print token2 benchmark, where we change a constant loop iterating 80
times to one over a symbolic constant n. The experiments were performed on a
3GHz Windows 7 machine with 16GB of memory. We used a loop unroll depth
of 2 for the examples. The runtime of SymDiﬀ (“Time”) does not include the
time required to generate Boogie ﬁles. The number of intraprocedural paths
(“Paths”) correspond to the number of feasible paths inside Eq.f1 .f2 that reach
the return statement, and “Enum Time” is the time inside Z3 to enumerate them
using an ALL-SAT procedure. The ﬁrst few rows indicate that the tool scales
well for ﬁnding diﬀerences when the number of intraprocedural paths is less than
1000. To investigate the eﬀect of large number of paths, we created two sets of
examples print token2 n<k> and print tokens2 e<k> (with loop unrolling of
k), for semantically diﬀerent and equivalent procedures respectively. The results
indicate that the tool scales better on semantically diﬀerent procedures, perhaps
due to the large number of paths leading to a diﬀerence. For the equivalent cases
too, the scalability appears to be better than the approach of enumerating paths
outside Z3. In addition to these examples, the tool has been successfully applied
to C programs several thousand lines large.
                         SYMDIFF: A Language-Agnostic Semantic Diﬀ Tool            717

4     Conclusion and Related Work
In this paper, we describe the design of a language-agnostic semantic diﬀerencing
tool for imperative programs. We have currently developed a front-end for C
programs. We have also built a preliminary front-end for x86 programs that we
have applied to perform compiler validation. We are also developing a front-end
for .NET programs using a variation of the Spec# tool chain. We are currently
working on making a binary release of the tool along with the C front end at
http://research.microsoft.com/projects/symdiff/.
Related Work. There have been a few recent static tools for performing seman-
tic diﬀ for programs. Jackson and Ladd [7] use dependencies between input and
the output variables of a procedure — it does not use any theorem provers. The
approach of regression veriﬁcation [6] uses SMT solvers to check equivalence of C
programs in the presence of mutual recursion, without requiring all procedures to
be equivalent. This is the work closest to ours1 , and the main diﬀerence lies in the
language agnostic nature of our tool, generation of abstract counterexamples, and
the modeling of the heap. Diﬀerential symbolic execution [9] uses symbolic exe-
cution to enumerate paths to check for equivalence. Our preliminary experience
shows that the use of veriﬁcation conditions instead of path enumeration often
helps SymDiﬀ scale to procedures with several thousand intraprocedural paths.

References
 1. Barnett, M., Chang, B.-Y.E., DeLine, R., Jacobs, B., M. Leino, K.R.: Boogie:
    A Modular Reusable Veriﬁer for Object-Oriented Programs. In: de Boer, F.S.,
    Bonsangue, M.M., Graf, S., de Roever, W.-P. (eds.) FMCO 2005. LNCS, vol. 4111,
    pp. 364–387. Springer, Heidelberg (2006)
 2. Barnett, M., M. Leino, K.R., Schulte, W.: The Spec# Programming System: An
    Overview. In: Barthe, G., Burdy, L., Huisman, M., Lanet, J.-L., Muntean, T. (eds.)
    CASSIS 2004. LNCS, vol. 3362, pp. 49–69. Springer, Heidelberg (2005)
 3. Condit, J., Hackett, B., Lahiri, S.K., Qadeer, S.: Unifying type checking and prop-
    erty checking for low-level code. In: POPL, pp. 302–314 (2009)
 4. de Moura, L., Bjørner, N.S.: Z3: An Eﬃcient SMT Solver. In: Ramakrishnan, C.R.,
    Rehof, J. (eds.) TACAS 2008. LNCS, vol. 4963, pp. 337–340. Springer, Heidelberg
    (2008)
 5. Godefroid, P., Lahiri, S.K., Rubio-González, C.: Statically Validating Must Sum-
    maries for Incremental Compositional Dynamic Test Generation. In: Yahav, E.
    (ed.) SAS 2011. LNCS, vol. 6887, pp. 112–128. Springer, Heidelberg (2011)
 6. Godlin, B., Strichman, O.: Regression veriﬁcation. In: DAC, pp. 466–471 (2009)
 7. Jackson, D., Ladd, D.A.: Semantic diﬀ: A tool for summarizing the eﬀects of mod-
    iﬁcations. In: ICSM, pp. 243–252 (1994)
 8. Kawaguchi, M., Lahiri, S.K., Rebêlo, H.: Conditional equivalence. Technical Report
    MSR-TR-2010-119, Microsoft Research (2010)
 9. Person, S., Dwyer, M.B., Elbaum, S.G., Pasareanu, C.S.: Diﬀerential symbolic
    execution. In: SIGSOFT FSE, pp. 226–237 (2008)
10. Software-artifact Infrastructure Repository,
    http://sir.unl.edu/portal/index.html

1
    Ofer Strichman has helped incorporate the algorithm into SymDiﬀ.
